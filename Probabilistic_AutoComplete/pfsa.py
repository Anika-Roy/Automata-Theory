import argparse
import pytest
import json

 
def construct(file_str: str) -> dict[str, dict[str, float]]:
    """Takes in the string representing the file and returns pfsa

    The given example is for the statement "A cat"
    """
    # generate a Probabilistic Automaton(PFSA) that will work as a letter-level auto-complete

    # split the string into words
    words = file_str.split()

    # convert all the words to lowercase
    words = [word.lower() for word in words]

    # add * to the end of each word
    words = [word + "*" for word in words]

    words_to_remove = set(words)
    # print(words_to_remove)

    # create a dictionary to store the PFSA
    pfsa = {}

    # ----------------Handling the start state---------------
    # add the start state
    pfsa["*"] = {}

    # add the first letters of the words in the dictionary
    for word in words:
        if word[0] not in pfsa["*"].keys():
            pfsa["*"][word[0]] = 0
            pfsa[word[0]] = {}

        # increment the letter's count
        pfsa["*"][word[0]] += 1


    # ----------Handling the rest of the states----------------
    for word in words:
        prefix = word[0]

        # iterate over the letters in the word
        for letter in word[1:]:

            # if the prefix+letter is not in the dictionary, add it
            if prefix+letter not in pfsa.keys():
                pfsa[prefix][prefix+letter] = 0
                pfsa[prefix+letter] = {}

            # increment the letter's count
            pfsa[prefix][prefix+letter] += 1

            # update the prefix
            prefix += letter

    # change frequencies to probabilities
    for prefix in pfsa.keys():
        total = sum(pfsa[prefix].values())
        for letter in pfsa[prefix].keys():
            pfsa[prefix][letter] /= total
            # round off to 2 decimal places
            pfsa[prefix][letter] = round(pfsa[prefix][letter], 2)

    # delete the keys with empty dictionaries
    for key in words_to_remove:
        del pfsa[key]
    
    # print("hello",pfsa)

    return pfsa


def main():
    """
    The command for running is `python pfsa.py text.txt`. This will generate
    a file `text.json` which you will be using for generation.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=str, help="Name of the text file")
    args = parser.parse_args()

    with open(args.file, "r") as file:
        contents = file.read()
        output = construct(contents)

    name = args.file.split(".")[0]

    with open(f"{name}.json", "w") as file:
        json.dump(output, file)


if __name__ == "__main__":
    main()


STRINGS = ["A cat", "A CAT", "", "A", "A A A A"]
DICTIONARIES = [
    {
        "*": {"a": 0.5, "c": 0.5},
        "a": {"a*": 1.0},
        "c": {"ca": 1.0},
        "ca": {"cat": 1.0},
        "cat": {"cat*": 1.0},
    },
    {
        "*": {"a": 0.5, "c": 0.5},
        "a": {"a*": 1.0},
        "c": {"ca": 1.0},
        "ca": {"cat": 1.0},
        "cat": {"cat*": 1.0},
    },
    {
        "*": {},
    },
    {
        "*": {"a": 1.0},
        "a": {"a*": 1.0},
    },
    {
        "*": {"a": 1.0},
        "a": {"a*": 1.0},
    },
]


@pytest.mark.parametrize("string, pfsa", list(zip(STRINGS, DICTIONARIES)))
def test_output_match(string, pfsa):
    """
    To test, install `pytest` beforehand in your Python environment.

    Run `pytest pfsa.py` Your code must pass all tests. There are additional
    hidden tests that your code will be tested on during VIVA.
    """
    result = construct(string)
    assert result == pfsa
