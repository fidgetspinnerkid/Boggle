"""
Boggle Game and Solver
"""

from random import randint
from itertools import product
from multiprocessing import Pool
from functools import partial
import time

# Puts the dict into a set and a list.
# Set allows for O(1) lookup.
# List allows for use of indexes to split it up for multiprocessing later.
with open('boggleDict.txt', 'r') as wordstxt:
    words_set = frozenset([x[:-1] for x in wordstxt.readlines()])
    words_lst = list(words_set)


def roll_boggle_die():
    """generates a list of random letters
        returns a list of random letters"""
    dieSides = ['AAEEGN',
                'ELRTTY',
                'AOOTTW',
                'ABBJOO',
                'EHRTVW',
                'CIMOTU',
                'DISTTY',
                'EIOSST',
                'DELRVY',
                'ACHOPS',
                'HIMNQU',
                'EEINSU',
                'EEGHNW',
                'AFFKPS',
                'HLNNRZ',
                'DELIRX']
    randIntList = []

    for x in range(16):
        randIntList.append(randint(0, 5))

    dieSidesGame = []
    for x in range(16):
        dieSidesGame.append(dieSides[x][randIntList[x]])

    return dieSidesGame


def order_letters(listToOrder):
    """ orders a list of random letters to form a boggle board
        no return"""
    for x in range(3, 19, 4):
        print(listToOrder[x - 3] + ' ' + listToOrder[x - 2] + ' ' + listToOrder[x - 1] + ' ' + listToOrder[x])


def find_score(listOfWords):
    """returns a list of scores based on a list of words
        listOfWords --> totalScores"""
    scores = {3: 1, 4: 1, 5: 2, 6: 3, 7: 5, 8: 11, 9: 11, 10: 11, 11: 11, 12: 11, 13: 11, 14: 11, 15: 11, 16: 11}
    totalScores = []

    for word in listOfWords:
        totalScores.append(scores[len(word)])

    return totalScores


def spot_adjacent(spot1, spot2):
    """checks if 2 spots are adjacent
       returns True or False"""
    adjacentSpots = {1: [2, 5, 6],
                     2: [1, 3, 5, 6, 7],
                     3: [8, 2, 4, 6, 7],
                     4: [8, 3, 7],
                     5: [1, 2, 10, 6, 9],
                     6: [1, 2, 3, 5, 7, 9, 10, 11],
                     7: [2, 3, 4, 6, 8, 10, 11, 12],
                     8: [11, 3, 4, 12, 7],
                     9: [10, 13, 5, 6, 14],
                     10: [5, 6, 7, 9, 11, 13, 14, 15],
                     11: [6, 7, 8, 10, 12, 14, 15, 16],
                     12: [8, 16, 11, 15, 7],
                     13: [9, 10, 11],
                     14: [9, 10, 11, 13, 15],
                     15: [16, 10, 11, 12, 14],
                     16: [11, 12, 15]}

    if spot2 in adjacentSpots[spot1]:
        return True
    else:
        return False


def index_letter(letter, gridx):
    """returns the spots in which a letter is in a grid
       returns -1 if not in grid"""
    letterInGrid = []

    for x in range(gridx.count(letter)):
        letterInGrid.append(gridx.index(letter))
        gridx.insert(gridx.index(letter), 0)
        gridx.remove(letter)

    if letterInGrid:

        for n, i in enumerate(gridx):
            if i == 0:
                gridx[n] = letter

        return letterInGrid
    else:
        return -1


def valid_path(path):
    """checks if a patha of spots in a grid are valid
       returns True or False"""

    for i, spot in enumerate(path):

        if path.count(spot) >= 2:
            return False

        elif i + 1 == len(path):
            continue

        elif not spot_adjacent(spot + 1, path[i + 1] + 1):
            return False

    return True


def word_in_grid(word, grid):
    """checks if a word is in a boggle grid
    returns True or False"""

    indexWord = []

    word = word.upper()
    for letter in word:

        if index_letter(letter, grid) == -1:
            return False

        indexWord.append(index_letter(letter, grid))

    for items in product(*indexWord):
        if valid_path(items):
            return True

    return False


def in_list(word):
    """checks if a word is in a file
       returns True or False"""
    word = word.lower()

    if word in words_set:
        return True

    return False


def find_longest_word(letterList):
    return max(all_valid_words(letterList), key=len)


def all_valid_words(letterList):
    with Pool(3) as p:
        results = p.map(partial(word_in_grid, grid=letterList), words_lst)

    return [s[1] for s in list(filter(lambda s: results[s[0]], enumerate(words_lst)))]


def play_boggle():
    """plays a game of boggle"""
    letterList = roll_boggle_die()

    wordsFound = []

    End = False
    while not End:
        order_letters(letterList)

        wordToCheck = input("Enter your word(leave blank to quit) : ").upper()

        if wordToCheck == "":
            End = True
            continue

        elif len(wordToCheck) < 3:
            print("Your word must be at least 3 letters long.")
            continue

        elif not word_in_grid(wordToCheck, letterList):
            print(wordToCheck + " is not on the grid.")
            continue

        elif not in_list(wordToCheck):
            print(wordToCheck + " is not a valid word.")
            continue

        elif wordToCheck in wordsFound:
            print(wordToCheck + " has been found.")
            continue

        else:
            print(wordToCheck + " is a valid word!")
            wordsFound.append(wordToCheck)

    scores = find_score(wordsFound)

    total = 0

    for i, word in enumerate(wordsFound):
        print(word + " is worth " + str(scores[i]))
        total += scores[i]

    print("Your total score is " + str(total))
    print("I bet I can find the longest word...")

    longest_word = find_longest_word(letterList)

    print("I found " + longest_word + "!")
    print("You found " + str(len(wordsFound)) + " out of " + str(len(all_valid_words(letterList))) + " possible words!")
    print("THANKS FOR PLAYING!")


if __name__ == "__main__":
    play_boggle()
