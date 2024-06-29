from typing import List

import ebooklib
from ebooklib import epub
from pypdf import PdfReader
from bs4 import BeautifulSoup


class WordCounter:
    def __init__(self, file: str, encoding="utf8", remove_characters_file="remove_characters.txt"):
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
        self.special_characters = self.__get_special_characters(remove_characters_file)
        self.file_text = ""
        self.words = []
        self.words_frequency = {}
        self.words = []
        reader()

    def __get_special_characters(self, file_location: str) -> str:
        with open(file_location, "r", encoding=self.encoding) as file:
            return file.readlines()[1]

    def _read_text(self):
        with open(self.file_name, "r", encoding=self.encoding) as file:
            self.file_text = file.read()

    def _read_pdf(self):
        pdf_reader = PdfReader(self.file_name)
        pages = pdf_reader.pages
        for page in pages:
            self.file_text += '\n' + page.extract_text()

    def _read_epub(self):
        book = epub.read_epub(self.file_name)
        pages = book.get_items_of_type(ebooklib.ITEM_DOCUMENT)
        for page in pages:
            html_parser = BeautifulSoup(page.get_content(), 'html.parser')
            self.file_text += "\n" + html_parser.get_text()

    def _read_html(self):
        self._read_text()
        html_parser = BeautifulSoup(self.file_text, 'html.parser')
        self.file_text = html_parser.get_text()

    def _is_word(self, word: str) -> bool:
        if len(word) == 0:
            return False
        for char in word:
            if char not in self.special_characters:
                return True
        return False

    def _clean_word(self, word: str) -> List[str]:
        word = word.strip().lower()
        clean_words = []
        if self._is_word(word):
            for special_char in self.special_characters:
                special_char_index = word.find(special_char)
                while special_char_index != -1:
                    word = word[:special_char_index] + " " + word[special_char_index + 1:]
                    special_char_index = word.find(special_char)
            clean_words = word.split()
        return clean_words

    def get_file_words(self):
        words_raw = self.file_text.split()
        words = []
        for word in words_raw:
            clean_words = self._clean_word(word)
            for clean_word in clean_words:
                words.append(clean_word)
        self.words = words

    def count_words_frequency(self):
        for word in self.words:
            word_frequency = self.words_frequency.get(word)
            if word_frequency is None:
                self.words_frequency[word] = 1
            else:
                self.words_frequency[word] = word_frequency + 1

    def sort_words_by_frequency(self):
        pass



