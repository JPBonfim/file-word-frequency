from datetime import datetime

from src.word_checker import WordChecker
from src.word_counter import WordCounter


def generate_file_with_word_frequency(
    source_file: str,
    source_file_encoding: str = "utf8",
    output_file_encoding: str = "utf8",
    ignore_chars_file: str = "ignore_characters.txt",
    ignore_chars_file_encoding: str = "utf8",
    minimum_word_size: int = 1,
    fix_words_with_hyphen: bool = False,
    dictionary_check: bool = False,
    # These parameters are only considered if dictionary_check = True.
    dictionary_file: str = None,
    dictionary_file_encoding: str = "utf8",
    join_test_limit: int = 0,
    test_invalid_words_with_hyphen: bool = False,
    generate_file_with_invalid_words: bool = False,
):
    """
    Given the path of an input file, generate a text file with all the words in the input file
    ordered from highest to lowest frequency. The file is generated in the directory where the program was run.

    :param source_file:
    Path to the file to be analyzed.
    :param source_file_encoding:
    The text encoding used in the source file. Default is "utf8".
    :param output_file_encoding:
    The encoding to be used in the output files. Default is "utf8".
    :param ignore_chars_file:
    Path to the file with the characters to be ignored when separating words from the text.
    Default is "ignore_characters.txt"
    :param ignore_chars_file_encoding:
    The text encoding used in the ignore_chars file. Default is "utf8".
    :param minimum_word_size:
    Minimum size for the word to be considered. Default is 1.
    :param fix_words_with_hyphen:
    If True, joins the hyphenated words that may have been separated in the text.
    Thus, if a word ends with "-" it is joined to the next word, if the word begins with "-" it
    is joined to the previous word. Default is False.

    :param dictionary_check:
    If True, checks if the words are valid in a dictionary. For this, you need a file with the valid words.
    Default is False.
    :param dictionary_file:
    Path to the dictionary file. Default is None.
    :param dictionary_file_encoding:
    The text encoding used in the dictionary file. Default is "utf8".
    :param join_test_limit:
    If a word is invalid, the program will try to join it with the following words and check if the word becomes valid.
    This is useful for PDF files, where the text may be oddly spaced when extracting it from the file.
    If the value is 1, the program will try to join the next word. If it is 2, it will try with the next word and,
    if it is invalid, it will also try to join with the next one.
    The logic is the same for any larger number. If the value is 0, the test is not performed.
    Default is 0.
    :param test_invalid_words_with_hyphen:
    If True, tests whether an invalid word becomes valid by removing the hyphen. This test (especially in conjunction
    with fix_words_with_hyphen) is useful for documents that separate words that do not fit on the line with a hyphen.
    Default is False
    :param generate_file_with_invalid_words:
    If True, it generates a file with all words considered invalid (not found in dictionary).
    Default is False
    """

    word_checker = WordChecker(
        minimum_size=minimum_word_size,
        ignore_chars_file=ignore_chars_file,
        ignore_chars_file_encoding=ignore_chars_file_encoding,
        dictionary_check=dictionary_check,
        dictionary_file=dictionary_file,
        dictionary_file_encoding=dictionary_file_encoding,
    )

    if not dictionary_check:
        join_test_limit = 0
        test_invalid_words_with_hyphen = False

    word_counter = WordCounter(
        file=source_file,
        encoding=source_file_encoding,
        word_checker=word_checker,
    )

    word_counter.get_file_words(
        fix_words_with_hyphen=fix_words_with_hyphen,
        test_words_in_dictionary=dictionary_check,
        join_test_limit=join_test_limit,
        test_invalid_words_with_hyphen=test_invalid_words_with_hyphen,
    )
    word_counter.count_words_frequency()
    word_counter.sort_words_by_frequency()

    with open("word_frequency.txt", "w", encoding=output_file_encoding) as file:
        for item in word_counter.words_frequency_list_sorted:
            file.write(f"{item[0]} {item[1]}\n")

    if generate_file_with_invalid_words:
        with open("invalid_words.txt", "w", encoding=output_file_encoding) as file:
            for item in word_counter.invalid_words_frequency_list_sorted:
                file.write(f"{item[0]} {item[1]}\n")

