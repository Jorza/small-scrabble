import sys
import random

TILES_USED = 0  # records how many tiles have been returned to user
SHUFFLE = False  # records whether to shuffle the tiles or not


# inserts tiles into myTiles
def getTiles(myTiles):
    global TILES_USED
    while len(myTiles) < 7 and TILES_USED < len(Tiles):
        myTiles.append(Tiles[TILES_USED])
        TILES_USED += 1


# prints tiles and their scores
def printTiles(myTiles):
    tiles = ""
    scores = ""
    for letter in myTiles:
        tiles += letter + "  "
        thisScore = getScore(letter)
        if thisScore > 9:
            scores += str(thisScore) + " "
        else:
            scores += str(thisScore) + "  "

    print("\nTiles : " + tiles)
    print("Scores: " + scores)


# gets the score of a letter
def getScore(letter):
    for item in Scores:
        if item[0] == letter:
            return item[1]


scoresFile = open('scores.txt')
tilesFile = open('tiles.txt')

# read scores from scores.txt and insert in the list Scores
Scores = []
for line in scoresFile:
    line = line.split()
    letter = line[0]
    score = int(line[1])
    Scores.append([letter, score])
scoresFile.close()

# read tiles from tiles.txt and insert in the list Tiles
Tiles = []
for line in tilesFile:
    line = line.strip()
    Tiles.append(line)
tilesFile.close()

# decide whether to return random tiles
rand = input("Do you want to use random tiles (enter Y or N): ")
if rand == "Y":
    SHUFFLE = True
else:
    if rand != "N":
        print("You did not enter Y or N. Therefore, I am taking it as a Yes :P.")
        SHUFFLE = True
        
if SHUFFLE:
    random.shuffle(Tiles)


myTiles = []
getTiles(myTiles)
printTiles(myTiles)

########################################################################
# Write your code below this
########################################################################

"""
 * Purpose: This file is to be used as part of a single-player scrabble game. It will display a set of seven tiles to
            the player (either random or pre-determined as specified by the player) and then get a valid word from the
            player. This input is then checked to ensure it is a valid word and the score of the word is displayed.
            Finally, the highest-scoring word is found, and then displayed along with its score. 
 * Author: OMITTED AS REQUIRED FOR PEER ASSESSMENT
 * Last Modified: 11/04/2018
 * Version: 1.1.6
"""

# Define constant parameters, define global variables.
QUIT_WORD = "***"
ENGLISH_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

userWord = None  # Define userWord in global scope, so can be accessed later to get user input.
validTest = False  # Set starting value for while loop condition.
# validTest is defined in global scope so that it can also be used to check the quit condition.


def valueInList(value, inList, replacementFlag=True):
    """
    Determine if a particular value is in a list. Is a replacement for 'if ___ in ___'.
    Can also be used to track which elements of the list have been used, by popping the element from the list after it
    matches with the target value.
    :param value: A target value of any data type.
    :param inList: The list to search through to find the target value. Can also be a string.
    :param replacementFlag: If 'False', will pop the any matched element from the list. If inList is a string, will be
    set to 'True'. Is optional, defaults to 'True'.
    :return: 'True' if target value was found in inList. Otherwise 'False'.
    """

    # If inList is a string, replacementFlag must be set to 'True'.
    if not replacementFlag and str(type(inList)) != "<class 'list'>":
        replacementFlag = True

    # If value is found in any position in inList, will return 'True'.
    # If the loop executes without finding value in inList, will return 'False'.
    for checkIdx in range(len(inList)):
        if value == inList[checkIdx]:
            if not replacementFlag:
                inList.pop(checkIdx)
            return True
    return False


def isPossibleFromTiles(word, tiles):
    """
    Check if all letters in 'word' are also present in 'tiles', disallowing letters to be double-counted.
    Side-effects: If 'replacementFlag' is set to 'False', will remove all elements from 'tiles' where that element is
    also in 'word'.
    Pre-condition: Requires function 'valueInList()' to be defined.
    :param word: A string or list of characters.
    :param tiles: A list of characters.
    :return: 'True' if all letters in 'word' are also present in 'tiles'. Otherwise 'False'.
    """
    for char in word:
        if not valueInList(char, tiles, False):
            return False
    return True


def isValidWord(word, allowedChars, dictList, tiles):
    """
    Check all conditions for a word to be valid:
    1) Only contains allowed characters.
    2) Is present in a given dictionary.
    3) Can be made from a given set of tiles.
    Pre-condition: Requires function 'valueInList()' to be defined.
    Pre-condition: Requires function 'isPossibleFromTiles()' to be defined.
    :param word: A string or list of characters.
    :param allowedChars: A string or list of characters. Determines what characters are allowed in a word.
    :param dictList: A list containing all allowed words (as strings).
    :param tiles: A list of characters.
    :return: 'True' if all conditions are satisfied. Otherwise 'False'.
    """

    # For all conditions, will return 'False' if condition is not satisfied. Otherwise will continue to next condition.

    # Condition 1: Check user's word only has allowed characters.
    # Check each character in turn. Return 'False' if any character is not in 'allowedChars'.
    for char in word:
        if not valueInList(char, allowedChars):
            print("Only use English letters!!!")
            return False

    # Condition 2: Check if user's word exists in the dictionary
    if not valueInList(word, dictList):
        print("I have never heard of this word.")
        return False

    # Condition 3: Check if word can be made using letters available
    # The function 'isPossibleFromTiles()' has side effects, so a copy of 'tiles' is passed.
    if not isPossibleFromTiles(word, tiles[:]):
        print("This word cannot be made using your tiles.")
        return False

    # All conditions satisfied
    print("Cool, this is a valid word.")
    return True


def getWordScore(word):
    """
    Sum all scores of letters in 'word'.
    Pre-condition: Requires function 'getScore()' to be defined.
    :param word: A string or list of characters. Must only contains English letters.
    :return wordScore: The sum of all scores of letters in 'word'.
    """
    wordScore = 0
    for char in word:
        wordScore += getScore(char)
    return wordScore


def getHighWord(tiles, dictList):
    """
    Determine the highest-scoring word, and its score, from a list of available letters and a list of possible words.
    Pre-condition: Requires function 'isPossibleFromTiles()' to be defined.
    Pre-condition: Requires function 'getWordScore()' to be defined.
    :param tiles: A list of available letters, without repetition. Is a list of characters.
    :param dictList: A list containing all allowed words (as strings).
    :return highWord: The highest-scoring word (as a string).
    :return highScore: The highest possible score. Is the score of 'highWord'. If there is no possible valid word,
    return 'highWord' = "" and 'highScore' = 0.
    """

    # Set outputs in global scope so can be accessed later.
    highWord = ""
    highScore = 0

    for entry in dictList:
        # Check entry can be made from tiles. Most entries will fail here, so put this condition first for efficiency.
        if isPossibleFromTiles(entry, tiles[:]):

            # Check if entry is the highest-scoring word. Update outputs if true.
            wordScore = getWordScore(entry)
            if wordScore > highScore:
                highWord = entry
                highScore = wordScore

    return highWord, highScore


# Read words from dictionary.txt and insert in the list Dictionary.
# Dictionary is named following the same style as other list of file contents, Tiles and Scores.
Dictionary = []
dictionaryFile = open("dictionary.txt")
for line in dictionaryFile:
    line = line.strip()  # Remove new-line character.
    Dictionary.append(line)
dictionaryFile.close()


# Get word from user, check if valid. Repeat until valid word given, or user quits.
# Use 'not' in while condition so that loop will also terminate when validTest holds a string.
while not validTest:
    userWord = input("\nEnter a word: ").upper()  # input should be case-insensitive, so make userWord upper-case.

    # Check quit condition. If false, check if word is valid.
    if userWord == QUIT_WORD:
        print("Better luck next time!!!")
        validTest = QUIT_WORD
    else:
        validTest = isValidWord(userWord, ENGLISH_LETTERS, Dictionary, myTiles)

# Check quit condition. Only print score of word if user did not quit.
if validTest != QUIT_WORD:
    # Print score of word
    scoreString = "Score for the word {} is: {}".format(userWord, getWordScore(userWord))
    print(scoreString)

# Whether user quits or not, always show the highest-scoring word(s).

# Find and print highest-scoring word and its score.
highWord, highScore = getHighWord(myTiles, Dictionary)

# Print different strings depending on whether a word has been found.
if highWord != "":
    highString = "\nThe word {} is the word with highest score. Its score is {}".format(highWord, highScore)
else:
    highString = "\nNo word can be made using these tiles"
print(highString)
