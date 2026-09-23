# Evil Hangman

An implementation of "Evil Hangman" — a version of the classic word-guessing game where the computer word-maker cheats by delaying the choice of a secret word for as long as possible, always steering toward whichever answer keeps the largest set of candidate words still alive.

## Table of Contents
- [How the Game Works](#how-the-game-works)
- [Project Structure](#project-structure)
- [Setup](#setup)
- [Running the Game](#running-the-game)
- [Running Tests](#running-tests)
- [Implementation Notes](#implementation-notes)
- [Command-Line Options](#command-line-options)

## How the Game Works

In traditional Hangman, the word-maker picks a secret word up front and answers every guess honestly.

In **Evil Hangman**, the computer never commits to a single word. Instead, it keeps an entire pool of dictionary words that are still consistent with every guess made so far. On each letter guess, it:

1. Splits the remaining word pool into "families" based on where that letter would appear in each word (e.g., for the letter `"e"`, words are grouped by whether `e` appears at no positions, position `0`, positions `(1, 3)`, etc.)
2. Picks the **largest family** — the answer that keeps the most words still possible
3. Narrows the active word pool down to just that family
4. Reveals the guess result based on that family's pattern (which may mean revealing nothing, i.e., marking the guess as "wrong")

Ties are broken by preferring the family that reveals the **fewest letter occurrences** — this means "the letter isn't in the word at all" is preferred whenever it's tied for the largest family, since it gives the guesser the least information.

As the game progresses, the pool of possible words keeps shrinking. Eventually, once few enough words remain, every one of them may share certain letters — at that point the word-maker is forced to finally reveal true letters. This makes Evil Hangman meaningfully harder than the honest version, especially with a limited number of guesses.

## Project Structure

```
evil_hangman_starter/
├── dictionary.txt              # Word list, one word per line
├── handout.pdf                 # Assignment instructions
├── hangman.py                  # Entry point: normal (human-vs-human) Hangman
├── evil_hangman.py             # Entry point: Evil Hangman (AI word-maker)
└── py_evil_hangman/
    ├── __init__.py
    ├── word_maker.py           # Core implementation: WordMakerHuman + WordMakerAI
    ├── word_guesser.py         # WordGuesserHuman (+ optional WordGuesserAI / "Karma")
    └── game/
        ├── args.py             # Command-line argument parsing
        └── game_manager.py     # Main game loop / referee logic
└── tests/
    └── test_word_maker_ai.py   # Automated correctness tests for WordMakerAI
```

## Setup

**Requirements:** Python 3.9+ and `pytest`

```bash
# (Recommended) create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate      # macOS/Linux
# .venv\Scripts\activate       # Windows

# Install dependencies
python3 -m pip install pytest
```

## Running the Game

From the `evil_hangman_starter/` directory (so `dictionary.txt` resolves correctly):

```bash
cd evil_hangman_starter

# Play against the cheating AI word-maker
python3 evil_hangman.py

# Play against the AI with verbose output (shows remaining word count after each guess)
python3 evil_hangman.py -v

# Give yourself more guesses
python3 evil_hangman.py -v -g 15

# Play normal (honest) Hangman instead
python3 hangman.py
```

## Running Tests

From `evil_hangman_starter/`:

```bash
python3 -m pytest tests/test_word_maker_ai.py
```

Expected output on a correct implementation:

```
======================== 3 passed in 0.XXs ========================
```

## Implementation Notes

All game logic changes are contained in `py_evil_hangman/word_maker.py`, inside the `WordMakerAI` class:

| Method | Responsibility |
|---|---|
| `__init__(words_file, verbose)` | Reads the dictionary once and groups words by length into a `dict[int, list[str]]`, so later lookups are fast |
| `reset(word_length)` | O(1) — retrieves the pre-grouped word list for the requested length and sets it as the active candidate pool |
| `get_letter_positions_in_word(word, letter)` | Returns a sorted tuple of every index at which `letter` appears in `word` |
| `guess(letter)` | Partitions the active pool into families by letter-position pattern, selects the largest family (ties broken toward fewer revealed occurrences), shrinks the active pool to that family, and returns the winning positions |
| `get_amount_of_valid_words()` | Returns the current size of the active candidate pool |
| `get_valid_word()` | Returns any one word from the active pool (used to reveal "the" word if the guesser loses) |

**Efficiency:** Preprocessing the dictionary by word length in `__init__` means `reset()` never has to re-scan the whole dictionary — it's an O(1) lookup, as required by the assignment.

## Command-Line Options

| Flag | Description | Default |
|---|---|---|
| `-f`, `--dictionary-file` | Path to the dictionary file | `dictionary.txt` |
| `-g`, `--guesses` | Number of incorrect guesses allowed | `10` |
| `-v`, `--verbose` | Show the number of remaining valid words after each guess | off |
| `-k`, `--karma` | Use the `WordGuesserAI` instead of manual input (optional "Karma" extension) | off |
