from typing import List

import ebooklib
from bs4 import BeautifulSoup
from ebooklib import epub
from pypdf import PdfReader

from src.word_checker import WordChecker

HYPHEN_CHAR = "-"


class WordCounter:
    def __init__(
        self,
        file: str,
        encoding: str,
        word_checker: WordChecker,
    ):
        self.__readers = {
            "txt": self._read_text,
            "pdf": self._read_pdf,
            "epub": self._read_epub,
            "html": self._read_html,
        }
        file_extension = file.strip().split(".")[-1]
        reader = self.__readers.get(file_extension)
        if reader is None:
            raise TypeError(f"File format not supported: {file_extension}")

        self.file_name = file
        self.encoding = encoding
        self.word_checker = word_checker
        self.file_text = ""
        self.words = []
        self.words_frequency = {}
        self.words_frequency_list_sorted = []
        self.invalid_words = []
        self.invalid_words_frequency = {}
        self.invalid_words_frequency_list_sorted = []
        reader()

    def _read_text(self):
        with open(self.file_name, "r", encoding=self.encoding) as file:
            self.file_text = file.read()

    def _read_pdf(self):
        pdf_reader = PdfReader(self.file_name)
        pages = pdf_reader.pages
        for page in pages:
            self.file_text += "\n" + page.extract_text()

    def _read_epub(self):
        book = epub.read_epub(self.file_name)
        pages = book.get_items_of_type(ebooklib.ITEM_DOCUMENT)
        for page in pages:
            html_parser = BeautifulSoup(page.get_content(), "html.parser")
            self.file_text += "\n" + html_parser.get_text()

    def _read_html(self):
        self._read_text()
        html_parser = BeautifulSoup(self.file_text, "html.parser")
        self.file_text = html_parser.get_text()

    @staticmethod
    def _fix_words_with_hyphen(words: List[str]):
        word_number = len(words)
        i = 1
        while i < word_number:
            if words[i][-1] == HYPHEN_CHAR:
                words[i] = words[i] + words.pop(i + 1)
                word_number -= 1
            if words[i][0] == HYPHEN_CHAR:
                words[i - 1] = words[i - 1] + words.pop(i)
                word_number -= 1
                i -= 1
            i += 1

    def _is_valid_word(self, word: str) -> bool:
        is_valid = self.word_checker.dictionary_word_check(word)
        return is_valid

    def _test_if_joining_word_become_valid(self, words: List[str]) -> list:
        became_valid = False
        joined_until = 0

        word = words[0]
        for w in range(1, len(words)):
            word += words[w]
            joined_until += 1
            if self._is_valid_word(word):
                became_valid = True
                break

        return [became_valid, joined_until, word]

    def _test_if_removing_hyphen_word_become_valid(self, word: str) -> list:
        hyphen_index = word.find(HYPHEN_CHAR)
        word = word[:hyphen_index] + word[hyphen_index + 1 :]
        became_valid = self._is_valid_word(word)
        return [became_valid, word]

    def _check_words_in_dictionary(
        self,
        join_test_limit: int,
        test_invalid_words_with_hyphen: bool,
    ):
        word_number = len(self.words)
        i = 0
        while i < word_number:
            is_valid = self._is_valid_word(self.words[i])

            if not is_valid and test_invalid_words_with_hyphen:
                (
                    became_valid,
                    fixed_word,
                ) = self._test_if_removing_hyphen_word_become_valid(self.words[i])
                if became_valid:
                    self.words[i] = fixed_word
                    is_valid = True

            if not is_valid and join_test_limit > 0:
                words_to_join = self.words[i : i + join_test_limit + 1]
                (
                    became_valid,
                    joined_until,
                    joined_word,
                ) = self._test_if_joining_word_become_valid(words_to_join)

                if became_valid:
                    del self.words[i : i + joined_until + 1]
                    self.words.insert(i, joined_word)
                    word_number -= joined_until
                    is_valid = True

            if not is_valid:
                self.invalid_words.append(self.words.pop(i))
                word_number -= 1

            i += 1

    def get_file_words(
        self,
        fix_words_with_hyphen: bool,
        test_words_in_dictionary: bool,
        join_test_limit: int,
        test_invalid_words_with_hyphen: bool,
    ):
        words_raw = self.file_text.split()

        if fix_words_with_hyphen:
            self._fix_words_with_hyphen(words_raw)

        for word in words_raw:
            clean_words = self.word_checker.clean_word(word)
            for clean_word in clean_words:
                if len(clean_word) >= self.word_checker.minimum_size:
                    self.words.append(clean_word)
                else:
                    self.invalid_words.append(clean_word)

        if test_words_in_dictionary:
            self._check_words_in_dictionary(
                join_test_limit, test_invalid_words_with_hyphen
            )

    def count_words_frequency(self):
        for word in self.words:
            word_frequency = self.words_frequency.get(word)
            if word_frequency is None:
                self.words_frequency[word] = 1
            else:
                self.words_frequency[word] = word_frequency + 1

        for invalid in self.invalid_words:
            word_frequency = self.invalid_words_frequency.get(invalid)
            if word_frequency is None:
                self.invalid_words_frequency[invalid] = 1
            else:
                self.invalid_words_frequency[invalid] = word_frequency + 1

    def sort_words_by_frequency(self):
        word_frequency_list = []
        invalid_word_frequency_list = []
        for word, frequency in self.words_frequency.items():
            word_frequency_list.append([word, frequency])
        for invalid, frequency in self.invalid_words_frequency.items():
            invalid_word_frequency_list.append([invalid, frequency])

        self.words_frequency_list_sorted = sorted(
            word_frequency_list, key=lambda x: x[1], reverse=True
        )
        self.invalid_words_frequency_list_sorted = sorted(
            invalid_word_frequency_list, key=lambda x: x[1], reverse=True
        )
