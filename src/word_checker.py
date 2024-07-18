from typing import List


class WordChecker:
    def __init__(
        self,
        minimum_size: int,
        ignore_chars_file: str,
        ignore_chars_file_encoding: str,
        dictionary_check: bool,
        dictionary_file: str,
        dictionary_file_encoding: str,
    ):
        self.minimum_size = minimum_size
        self.ignore_chars_file_encoding = ignore_chars_file_encoding
        self.dictionary_file_encoding = dictionary_file_encoding
        self.special_characters = self.__get_special_characters(
            ignore_chars_file, ignore_chars_file_encoding
        )
        self.dictionary = set()
        if dictionary_check:
            self.__build_dictionary(dictionary_file, dictionary_file_encoding)

    @staticmethod
    def __get_special_characters(file_location: str, encoding: str) -> str:
        with open(file_location, "r", encoding=encoding) as file:
            return file.readlines()[1]

    def __build_dictionary(self, dictionary_file: str, encoding: str):
        with open(dictionary_file, "r", encoding=encoding) as file:
            lines = file.readlines()
            for line in lines:
                self.dictionary.add(line.strip())

    def simple_word_check(self, word: str) -> bool:
        """
        Checks if the input text is a word. Return true if the text contains any characters that do not belong to
        the ignore list and is bigger than the minimum size.
        """
        if len(word) < self.minimum_size:
            return False
        for char in word:
            if char not in self.special_characters:
                return True
        return False

    def dictionary_word_check(self, word: str) -> bool:
        """
        Checks if the input text is a word in the dictionary.
        """
        if word in self.dictionary:
            return True
        return False

    def clean_word(self, word: str) -> List[str]:
        """
        Take a word and clean it up. If the word has ignorable characters, they are removed and the word is split
        at these positions. Returns a list of words resulting from this process.
        """
        word = word.strip().lower()
        clean_words = []
        if self.simple_word_check(word):
            for special_char in self.special_characters:
                special_char_index = word.find(special_char)
                while special_char_index != -1:
                    word = (
                        word[:special_char_index] + " " + word[special_char_index + 1 :]
                    )
                    special_char_index = word.find(special_char)
            clean_words = word.split()
        return clean_words
