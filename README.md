# file-word-frequency
A program to count the number of occurrences of words in a file and organize them by frequency.

# Usage
Before running the code, install the dependencies with:
~~~
pip install -r requirements.txt
~~~

To use the program, call the function "generate_file_with_word_frequency" in the file "main.py" 
with the desired parameters. The function will generate a text file with all the words in the input file 
ordered from highest to lowest frequency. The file is generated in the directory where the program was run.
~~~python
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
~~~

## Parameters
### `source_file`
Path to the file to be analyzed.

### `source_file_encoding`
The text encoding used in the source file. Default is "utf8".

### `output_file_encoding`
The encoding to be used in the output files. Default is "utf8".

### `ignore_chars_file`
Path to the file with the characters to be ignored when separating words from the text.
Default is "ignore_characters.txt"

### `ignore_chars_file_encoding`
The text encoding used in the ignore_chars file. Default is "utf8".

### `minimum_word_size`
Minimum size for the word to be considered. Default is 1.

### `fix_words_with_hyphen`
If True, joins the hyphenated words that may have been separated in the text.
Thus, if a word ends with "-" it is joined to the next word, if the word begins with "-" it
is joined to the previous word. Default is False.

### `dictionary_check`
If True, checks if the words are valid in a dictionary. For this, you need a file with the valid words.
Default is False.

Here are some lists of words that can be used:
- English: https://github.com/dwyl/english-words
- Portuguese: https://github.com/jfoclpf/words-pt

### `dictionary_file`
Path to the dictionary file. Default is None.

### `dictionary_file_encoding`
The text encoding used in the dictionary file. Default is "utf8".

### `join_test_limit`
If a word is invalid, the program will try to join it with the following words and check if the word becomes valid.
This is useful for PDF files, where the text may be oddly spaced when extracting it from the file.
If the value is 1, the program will try to join the next word. If it is 2, it will try with the next word and,
if it is invalid, it will also try to join with the next one.
The logic is the same for any larger number. If the value is 0, the test is not performed.
Default is 0.

### `test_invalid_words_with_hyphen`
If True, tests whether an invalid word becomes valid by removing the hyphen. This test (especially in conjunction
with fix_words_with_hyphen) is useful for documents that separate words that do not fit on the line with a hyphen.
Default is False

### `generate_file_with_invalid_words`
If True, it generates a file with all words considered invalid (not found in dictionary).
Default is False