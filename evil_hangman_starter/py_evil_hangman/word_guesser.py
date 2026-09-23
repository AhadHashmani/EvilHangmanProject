
class GameState():
    def __init__(self, guesses, word_length, verbose):
        self.word_length = word_length
        self.guessed = []
        self.guesses = guesses # starting number of guesses
        self.done_letters = 0
        self.word = ["-"] * word_length
        self.verbose = verbose
    def print_state(self, wordsRemaining):
        wrStr = "" if not self.verbose else f" ({wordsRemaining} words remain)"
        print(f"\nYou have {self.guesses} incorrect guesses left{wrStr}.")
        print("Used letters: {}".format(" ".join(self.guessed)))
        print("Word: {}".format("".join(self.word)))


# an abstract class defining the word guesser interface
class WordGuesser():
    def __init__(self, guesses, words_file, verbose):
        self.verbose = verbose
        self.guesses = guesses
    def reset(self, word_length):
        self.state = GameState(self.guesses, word_length, self.verbose)
    def get_guess(self):
        # return the next best guess
        # use self.gamestate to inquire about the current status of the game
        raise NotImplementedError # Subclasses should override this method

class WordGuesserHuman(WordGuesser):
    def get_guess(self):
            while True:
                inp = input("Enter guess: ").lower()
                if len(inp) != 1 or inp in self.state.guessed or not inp.isalpha():
                    print("Invalid guess.")
                else:
                    break
            return inp
 
# NOT REQUIRED! This is only for Karma.
class WordGuesserAI():
    def __init__(self, guesses, words_file, verbose):
        self.verbose = verbose
        pass # fill out with code that reads words_file and stores it in a useful data structure
    def reset(self, word_length):
        self.state = GameState(self.guesses, word_length, self.verbose)
        pass # update data structures to reflect word length
    def get_guess(self):
        # The goal here is to create a "reflex" agent that looks at JUST the current gamestate and decides which letter should be picked.
        # You want to pick a letter whose knowledge will split the word space in half.
        pass
