import argparse
import pytest
import json
import random


def generate(pfsa: dict[str, dict[str, float]], word_count: int) -> str:
    """Takes in the PFSA and generates a string of `word_count` number of words

    The following string is when the input has only "Cat" as in it's PFSA with
    count of 4.
    """
    # TODO: FILE IN THIS FUNCTION
    count = 0
    string= ""
    
    if pfsa["*"] == {}:
        # print("hello",string)
        return string

    while count < word_count:

        # handle the start state
        prefix = random.choices(list(pfsa["*"].keys()), weights=list(pfsa["*"].values()))[0]

        # now we'll keep appending letters to the word following the probability in json until we reach the end of some word
        # we'll start from the start state
        while True:
            # print(prefix)
            # choose a random letter from the dictionary
            prefix = random.choices(list(pfsa[prefix].keys()), weights=list(pfsa[prefix].values()))[0]

            # if we reach the end of a word, break
            if prefix[-1] == "*":
                # print("break")
                break
        
        if count == word_count - 1:
            string += prefix[:-1]
        else:
            string += prefix[:-1] + " "

        count += 1

    # print("hello",string)
    return string


def main():
    """
    The command for running is `python generator.py text.json 5`. This will
    generate a file `text_sample.txt` which has 5 randomly sampled words.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=str, help="Name of the text file")
    parser.add_argument("count", type=int, help="Sample size to gen")
    args = parser.parse_args()

    with open(args.file, "r") as file:
        data = json.load(file)
        output = generate(data, args.count)

    name = args.file.split(".")[0]

    with open(f"{name}_sample.txt", "w") as file:
        file.write(output)


if __name__ == "__main__":
    main()


DICTIONARIES = [
    {
        "*": {"a": 1.0},
        "a": {"a*": 1.0},
    },
    {
        "*": {"a": 1.0},
        "a": {"a*": 1.0},
    },
    {
        "*": {"a": 1.0},
        "a": {"a*": 1.0},
    },
    {
        "*": {"c": 1.0},
        "c": {"ca": 1.0},
        "ca": {"cat": 1.0},
        "cat": {"cat*": 1.0},
    },
]
STRINGS = [
    "a",
    "a a a a a",
    "",
    "cat cat cat cat",
]
COUNT = [1, 5, 0, 4]

COMBINED = [(d, s, c) for d, (s, c) in zip(DICTIONARIES, zip(STRINGS, COUNT))]


@pytest.mark.parametrize("pfsa, string, count", COMBINED)
def test_output_match(pfsa, string, count):
    """
    To test, install `pytest` beforehand in your Python environment.

    Run `pytest pfsa.py` Your code must pass all tests. There are additional
    hidden tests that your code will be tested on during VIVA.
    """
    result = generate(pfsa, count)
    assert result == string
