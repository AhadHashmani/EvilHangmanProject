from __future__ import annotations
from collections import defaultdict # You might find this useful
import os

"""
************** READ THIS ***************
************** READ THIS ***************
************** READ THIS ***************
************** READ THIS ***************
************** READ THIS ***************

If you worked in a group on this project, please type the EIDs of your groupmates below (do not include yourself).
Leave it as TODO otherwise.
Groupmate 1: TODO
Groupmate 2: TODO
"""

class WordMakerHuman():
    def __init__(self, words_file, verbose):
        # we need to prompt the player for a word, then clear the screen so that player 2 doesn't see the word.
        self.verbose = verbose
        self.words = {} # Make sure that you understand dictionaries. They will be extremely useful for this project.
        with open(words_file) as wordfile:
            for line in wordfile:
                word = line.strip()
                if len(word) > 0:
                    self.words[word] = True # I could have made this a set() instead.

    def reset(self, word_length):
        # Your AI code should not call input() or print().
        question = ""
        while True:
            question = input(f"Please type in your word of length {word_length}: ")
            if question in self.words and len(question) == word_length:
                break
            print("Invalid word.")
        if not self.verbose:
            print("\n" * 100) # Clear the screen
        self.word = question

    def get_valid_word(self):
        return self.word

    def get_amount_of_valid_words(self):
        return 1 # the only possible word is self.word

    def guess(self, guess_letter):
        idx = self.word.find(guess_letter)
        ret = []
        while idx != -1:
            ret.append(idx)
            idx = self.word.find(guess_letter, idx + 1)
        return ret




class WordMakerAI():
    """
    A new WordMakerAI is instantiated every time you launch the game with evil_hangman.py.
    (However, the test harness can make multiple instances.)
    Between games, the reset() function is called. This should clear any internal gamestate that you have.
    The number of guesses, input gathering, winning, losing, etc. is all managed by the GameManager, so you don't
     have to prompt the user at all. All you need to do is keep track of the active dictionary of still-valid words
     in this game.

    Do not assume anything about the lengths of the words. You will be tested on dictionaries with extremely long words.
    """
    def __init__(self, words_file: str, verbose=False):
        self.verbose = verbose
        self.words_by_length: dict[int, list[str]] = defaultdict(list)
        with open(words_file) as file_obj:
            for line in file_obj:
                word = line.strip()
                if len(word) > 0:
                    self.words_by_length[len(word)].append(word)
        self.active_words: list[str] = []

    def reset(self, word_length: int) -> None:
        # This function starts a new game with a word length of `word_length`.
        self.active_words = list(self.words_by_length.get(word_length, []))

    def get_valid_word(self) -> str:
        # Get a valid word in the active dictionary, to return when you lose
        return self.active_words[0]

    def get_amount_of_valid_words(self) -> int:
        # This function gets the total amount of possible words "remaining"
        return len(self.active_words)

    def get_letter_positions_in_word(self, word: str, guess_letter: str) -> tuple[int, ...]:
        # Returns the positions of guess_letter in word, sorted ascending, 0-indexed.
        result = []
        idx = word.find(guess_letter)
        while idx != -1:
            result.append(idx)
            idx = word.find(guess_letter, idx + 1)
        return tuple(result)

    def guess(self, guess_letter) -> list[int]:
        # Sort all remaining words into families by where guess_letter appears
        families: dict[tuple[int, ...], list[str]] = defaultdict(list)
        for word in self.active_words:
            key = self.get_letter_positions_in_word(word, guess_letter)
            families[key].append(word)

        # Pick the largest family; ties broken by fewest occurrences of guess_letter
        best_key = max(
            families.keys(),
            key=lambda k: (len(families[k]), -len(k))
        )

        self.active_words = families[best_key]
        return sorted(best_key)