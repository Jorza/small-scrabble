from sys import stdin
import math
import sys
import random


TILES_USED = 0 # records how many tiles have been returned to player
CELL_WIDTH = 3 # cell width of the scrabble board
SHUFFLE = False # records whether to shuffle the tiles or not

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


# initialize n x n Board with empty strings
def initializeBoard(n):
    Board = []
    for i in range(n):
        row = []
        for j in range(n):
            row.append("")
        Board.append(row)

    return Board


# put character t before and after the string s such that the total length
# of the string s is CELL_WIDTH.
def getString(s,t):
    global CELL_WIDTH
    s = str(s)
    rem = CELL_WIDTH - len(s)
    rem = rem//2
    s = t*rem + s
    rem = CELL_WIDTH - len(s)
    s = s + t*rem
    return s


# print the Board on screen
def printBoard(Board):
    global CELL_WIDTH
    print("\nBoard:")
    spaces = CELL_WIDTH*" "
    board_str = "  |" + "|".join(getString(item, " ") for item in range(len(Board))) + "|"
    line1 = "--|" + "|".join(getString("", "-") for item in range(len(Board))) + "|"
 
    print(board_str)
    print(line1)
    
    for i in range(len(Board)):
        row = str(i) + " "*(2-len(str(i))) + "|"
        for j in range(len(Board)):
            row += getString(Board[i][j], " ") + "|"
        print(row)
        print(line1)
        
    print()


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
rand = input("Do you want to use random tiles (enter Y or N): ").upper()
if rand == "Y":
    SHUFFLE = True
else:
    if rand != "N":
        print("You did not enter Y or N. Therefore, I am taking it as a Yes :P.")
        SHUFFLE = True
if SHUFFLE:
    random.shuffle(Tiles)


validBoardSize = False
while not validBoardSize:
    BOARD_SIZE = input("Enter board size (a number between 5 to 15): ")
    if BOARD_SIZE.isdigit():
        BOARD_SIZE = int(BOARD_SIZE)
        if BOARD_SIZE >= 5 and BOARD_SIZE <= 15:
            validBoardSize = True
        else:
            print("Your number is not within the range.\n")
    else:
        print("Are you a little tipsy? I asked you to enter a number.\n")


Board = initializeBoard(BOARD_SIZE)
printBoard(Board)

myTiles = []
getTiles(myTiles)
printTiles(myTiles)

########################################################################
# Write your code below this
########################################################################
import re

"""
 * Purpose: This file allows a user to play a modified single-player Scrabble game.
 * Author: OMITTED AS REQUIRED FOR PEER ASSESSMENT
 * Last Modified: 10/05/2018
 * Version: 2.2.21
"""

# Define constant parameters.
QUIT_WORD = "***"
ENGLISH_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
POSITION_MATCH_PATTERN = r"^[0-9]+:[0-9]+:[VHvh]$"


# Functions for checking input, placing words, calculating score
def valueInList(value, inList, replacementFlag=True):
    """
    Determine if a particular value is in a list. Is a replacement for 'if ___ in ___'.
    Can also be used to track which elements of the list have been used, by popping the element from the list after it
    matches with the target value.
    Side-effects: If 'replacementFlag' is set to 'False', will remove 'value' from 'inList'.
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


def listInList(smallList, bigList):
    """
    Check if all items in 'smallList' are also present in 'bigList', disallowing letters to be double-counted.
    Pre-condition: Requires function 'valueInList()' to be defined.
    :param samllList: A string or list of characters.
    :param bigList: A list of characters.
    :return: 'True' if all items in 'smallList' are also present in 'bigList'. Otherwise 'False'.
    """
    bigList = bigList[:]
    for char in smallList:
        if not valueInList(char, bigList, False):
            return False
    return True


def fileToList(fileName):
    """
    # Read lines from file and insert in a list.
    :param fileName: Name of the file to be read. Include the extension.
    :return: A list containig the content from the file, separated by rows.
    """
    fileList = []
    fileHandle = open(fileName)
    for line in fileHandle:
        line = line.strip()  # Remove new-line character.
        fileList.append(line)
    fileHandle.close()
    return fileList


def isValidInput(word, position, dictList):
    """
    Check if player's input is valid. Checks for a word that only has English letters, and exists in the dictionary, and
    checks for a position in the correct r:c:d format.
    Pre-condition: Requires function 'valueInList()' to be defined.
    Pre-condition: Requires use of regular expressions.
    :param word: player's input word. A string.
    :param position: player's input position. A string.
    :param dictList: A list of all allowed words. This is the dictionary for this Scrabble game
    :return: 'True' if all input is valid, otherwise 'False'.
    """
    # Check player's word only has allowed characters.
    # Check each character in turn. Return 'False' if any character is not in 'allowedChars'.
    for char in word:
        if not valueInList(char, ENGLISH_LETTERS):
            print("That is not a valid word.")
            return False

    # Check if player's word exists in the dictionary.
    if not valueInList(word, dictList):
        print("That word is not in the dictionary.")
        return False

    # Check the format of the position string is valid.
    if not re.match(POSITION_MATCH_PATTERN, position):
        print("That is not a valid position.")
        return False

    # All conditions passed.
    return True


def isOnBoard(word, position, isFirstMove=False):
    """
    Check that the start and end of the player's word are placed within the bounds of the board.
    For the first move, check that the first character of the word has been placed in the required centre position.
    :param word: A valid, playable word. A string.
    :param position: A list of form [row_integer, column_integer, "P"], where 'P' can be either 'H' or 'V'.
    :param isFirstMove: A boolean value. Should be 'True' if and only if it is the first move of the game.
    :return: 'True' if ord is in valid position, otherwise 'False'.
    """

    # Check position indexes are valid
    if position[0] >= BOARD_SIZE or position[1] >= BOARD_SIZE:
        print("All the letters must fit on the board.")
        return False

    # Check position is correct for first move
    if isFirstMove and not (position[0] == position[1] == BOARD_SIZE // 2):
        print("The location in the first move must be {0}:{0}:H or {0}:{0}:V".format(BOARD_SIZE // 2))
        return False

    # Check word does not overhang board boundary.
    # If word is horizontal, must check column index (position[1]) does not go out of bounds
    # If word is vertical, must check row index (position[0]) does not go out of bounds.
    startIndex = position[1] if position[2] == "H" else position[0]
    endIndex = startIndex + len(word)
    if endIndex > BOARD_SIZE:
        print("All the letters must fit on the board.")
        return False

    return True


def copyListOfLists(listToCopy):
    """
    Copies a list of lists such that the inner lists within the copy have unique memory addresses.
    :param listToCopy: A list or list of lists to copy
    :return: A copy of listToCopy.
    """
    copyList = []
    for row in listToCopy:
        copyList.append(row[:])
    return copyList


def placeWord(word, position, Board, myTiles, isFirstMove=False):
    """
    Given a valid word and position, attempt to place that word on the board. Take into account the current positions
    of tiles on the board.
    If the word can be placed on the board, update the players tiles to remove any tiles that must have been played.
    Pre-condition: Requires function 'valueInList()' to be defined.
    :param word: valid playable word to be placed on the board. A string.
    :param position: valid position that locates the word on the board. A list of form [
    row_integer, column_integer, "P"], where 'P' can be either 'H' or 'V'.
    :param Board: The list of lists representing the current board. Contains letters already placed on the board.
    :param myTiles: The list of available tiles to place on the board.
    :param isFirstMove: A boolean value. Should be 'True' if and only if it is the first move of the game.
    :return localBoard: An updated board after the word has been played
    :return localTiles: The updated tiles after the word has been played
    :return: lettersPlayed: A list of tiles that have been played.
    """

    # Create local copies of the board and tiles, in case the move is invalid.
    localBoard = copyListOfLists(Board)
    localTiles = myTiles[:]

    lettersPlayed = []

    # For each letter in word, check the corresponding position on the board - starting from the specified position
    # for the start of the word, and continuing in the specified direction.
    for charIdx, char in enumerate(word):

        if position[2] == "H":
            indexes = (position[0], position[1] + charIdx)
        else:
            indexes = (position[0] + charIdx, position[1])

        if localBoard[indexes[0]][indexes[1]] == "":
            # Where the board holds a blank space, check that player can play the required tile.
            # If true, put tile on the board, and remove from player's tiles.
            # Record what tiles have been played.
            if valueInList(char, localTiles, False):
                localBoard[indexes[0]][indexes[1]] = char
                lettersPlayed.append(char)
            # If false, move is invalid.
            else:
                raise ValueError("You don't have the correct tiles for that move.")

        elif localBoard[indexes[0]][indexes[1]] != char:
            # Where the board holds a letter, check it matches the corresponding letter in the player's word.
            # If this is not the case, the word cannot be played. It would be an illegal move.
            raise ValueError("Your word cannot be placed there.")

    # Check that the player's word uses at least one tile from the board and one tile from the player's tiles.
    if len(lettersPlayed) == 0 or (len(lettersPlayed) == len(word) and not isFirstMove):
        raise ValueError("Your word cannot be placed there.")

    # If conditions satisfied, return new board, tiles and letters played.
    return localBoard, localTiles, lettersPlayed


def getWordScore(word, getHighPlay=False):
    """
    Sum all scores of letters in 'word'.
    If getHighPlay is 'True', subtract the lowest letter score. Since a played word must have at least one letter
    already on the board, this quantity gives the highest possible score for 'word' in any play (the high play score).
    Pre-condition: Requires function 'getScore()' to be defined.
    :param word: A string or list of characters. Must only contains English letters.
    :param getHighPlay: A boolean. Determines whether to to calculate the word score, or the high play score.
    :return: The sum of all scores of letters in 'word'. If getHighPlay is set, subtracts the lowest-scoring letter.
    """
    # Initialise variables
    wordScore = 0
    minScore = 0

    # Add the scores of each character to wordScore
    for char in word:
        charScore = getScore(char)
        wordScore += charScore

        # Track the minimum-scoring character
        if getHighPlay and charScore < minScore:
            minScore = charScore

    if getHighPlay:
        # subtract the lowest-scoring letter.
        wordScore -= minScore
    return wordScore


# Functions for finding best move
def transposeTable(table):
    """
    Find the transpose of a table - A table containing the same values as the original, but with the row and column
    indexes for each element switched. The table must be square (same number of rows amd columns).
    :param table: A table, represented as a list of lists.
    :return: The transpose of 'table', represented as a list of lists.
    """
    transpose = []

    tableSize = len(table)
    for col in range(tableSize):

        # Construct list of column elements in 'table'.
        columnList = []

        # Get item at specific column index from each row
        for row in range(tableSize):
            columnList.append(table[row][col])

        # Append column from original table as a row of the transpose.
        transpose.append(columnList)
    return transpose


def initialiseScoreDictionary(dictionary):
    """
    # Construct ScoreDictionary, where each entry consists of a word, its high play score and its score.
    # Exclude any words that can not possibly fit on the board, and sort in descending order by high play score.
    :param dictionary: A list of all allowed words.
    :return: A list, with entries of the form [high play score, word score, word], sorted in descending order by high
    play score. Contains every word from 'dictionary'that will fit on the board.
    """
    ScoreDictionary = []
    for entry in dictionary:
        if len(entry) <= BOARD_SIZE:
            ScoreDictionary.append([getWordScore(entry, True), getWordScore(entry), entry])
    ScoreDictionary.sort(reverse=True)  # Sort by first column - high play score
    return ScoreDictionary


def getBestFirstMove(myTiles, ScoreDictionary):
    """
    Find the highest-scoring valid combination of the player's tiles that can fit on the board.
    :param myTiles: The list of available tiles.
    :param ScoreDictionary: A list of all available words, stored along with their high play scores and total scores.
    :return bestMove: A tuple containing the high-score, the highest-scoring word, and the position for the word.
    """

    # Initialise output, so can be called in first iteration of loop
    bestMove = 0, None, None

    # Create local copy of ScoreDictionary, so can then sort by total word score (not high play score).
    ScoreDictionaryCopy = copyListOfLists(ScoreDictionary)
    ScoreDictionaryCopy.sort(key=lambda x: x[1], reverse=True)  # Sort by column 1: total word score.

    # Iterate through all possible words, in descending order by total word score.
    for _, wordScore, word in ScoreDictionaryCopy:
        # Check the end of the word will fit on the board, given the start is in the board centre.
        if BOARD_SIZE // 2 + len(word) > BOARD_SIZE:
            continue

        # If current high score is greater than the score for 'word', then don't have to check 'word' or any subsequent
        # words (since ScoreDictionaryCopy is sorted in descending order by score).
        if bestMove[0] >= wordScore:
            return bestMove

        # Check entry can be made from player's tiles. Don't need to check board.
        if listInList(word, myTiles):

            # Check if entry is the highest-scoring word. Update outputs if true.
            if wordScore > bestMove[0]:
                bestMove = (wordScore, word, [BOARD_SIZE // 2, BOARD_SIZE // 2, 'H'])
    return bestMove


def playWordOnBoard(Board, myTiles, word, firstLetterPosition, rowColIdx, wordHighPlayScore, currentHighScore):
    """
    Play a given word at a given position in a row or column of a board. Compare the score with the current best move.
    Return a new best move if one is found.
    :param Board: Current board, represented as a list of lists.
    :param myTiles: List of available tiles to play.
    :param word: Current word for which to find a high-scoring position.
    :param firstLetterPosition: The position of the first letter in the row or column
    :param rowColIdx: The index of the row or column on the board. Used to determine direction of the word.
    :param wordHighPlayScore: the high play score of 'word'.
    :param currentHighScore: The current high score to which any new score is compared.
    :return: bestMove: A tuple containing the high-score, 'word', and the position in r:c:d format for 'word'.
    """

    # Initialise returns variables
    bestMove = None
    skipToNextWord = False

    # Construct a valid position in the format r:c:d to locate the word on the board.
    if rowColIdx < BOARD_SIZE:
        position = [rowColIdx, firstLetterPosition, 'H']  # word placed horizontally
    else:
        position = [firstLetterPosition, rowColIdx - BOARD_SIZE, 'V']  # word placed vertically

    # Attempt to place the word on the board.
    try:
        _, _, lettersPlayed = placeWord(word, position, Board, myTiles)
    except ValueError:
        # word cannot be played. Must return to search for another instance of the item in 'word'.
        return bestMove, skipToNextWord

    # Calculate the score of this placement, update bestMove if required.
    positionScore = getWordScore(lettersPlayed)
    if positionScore > currentHighScore:
        bestMove = positionScore, word, position

    # If positionScore is the highest possible score for this word, skip to the next word.
    if positionScore == wordHighPlayScore:
        skipToNextWord = True

    return bestMove, skipToNextWord


def getBestMoveInList(Board, myTiles, word, wordHighPlayScore, rowColIdx, rowOrColumnList, currentHighScore):
    """
    Find possible moves for a given word in a given row or column, compare the best move with the current best move.
    Return a new best move if one is found.
    :param Board: Current board, represented as a list of lists.
    :param myTiles: List of available tiles to play.
    :param word: Current word for which to find a high-scoring position.
    :param wordHighPlayScore: the high play score of 'word'.
    :param rowColIdx: The index of the row or column in the list of all rows and columns.
    :param rowOrColumnList: The specific row or column to check.
    :param currentHighScore: The current high score to which any new score is compared.
    :return: bestMove: A tuple containing the high-score, 'word', and the best position for 'word' in the list searched.
    """

    # Initialise returns variables
    bestMove = None
    skipToNextWord = False

    # Track which possible first-letter positions ('flp's) have been attempted.
    flpBitlist = [False] * (BOARD_SIZE - len(word) + 1)

    # Iterate through each item in the row/column
    for itemIdx, item in enumerate(rowOrColumnList):
        # Find an instance (and index) of the item in 'word'. If found, try to play 'word' in this position.

        # Skip any blank spaces, since they will never be in 'word'.
        if item == "":
            continue

        # Ignore instances where start and end of word overhang board boundary. Define start and end bounds:
        # start: requires charIdx <= itemIdx, and charIdx < len(word).
        # end: requires BOARD_SIZE - itemIdx >= len(word) - charIdx and charIdx >= 0.
        startBound = itemIdx + 1
        endBound = itemIdx + len(word) - BOARD_SIZE
        highCharIdx = startBound if startBound < len(word) else len(word)
        lowCharIdx = endBound if endBound > 0 else 0

        for charIdx in range(lowCharIdx, highCharIdx):
            if word[charIdx] == item:
                # Find the required position of the first character in 'word'. Will be >= 0.
                firstLetterPosition = itemIdx - charIdx

                # Track which first-letter positions have been tried with a bit list. Avoid re-trying same position.
                if not flpBitlist[firstLetterPosition]:
                    flpBitlist[firstLetterPosition] = True

                    # Determine the board position, play word, get score.
                    possibleBestMove, skipToNextWord = playWordOnBoard(Board, myTiles, word, firstLetterPosition, rowColIdx, wordHighPlayScore, currentHighScore)

                    if possibleBestMove is not None:
                        bestMove = possibleBestMove

                    if skipToNextWord:
                        return bestMove, skipToNextWord
    return bestMove, skipToNextWord


def getBestMove(Board, myTiles, ScoreDictionary, isFirstMove=False):
    """
    Find the highest-scoring possible move, given the current state of the board and the player's tiles.
    :param Board: Current board, represented as a list of lists.
    :param myTiles: List of available tiles to play.
    :param ScoreDictionary: A list of all available words, stored along with their high play scores and total scores.
    :param isFirstMove: A boolean flag. Allows quicker calculation of best move in first move.
    :return bestMove: A tuple containing the high-score, the highest-scoring word, and the position for the word.
    """

    # Handling for first move. If it is the first move, will only run this block of code.
    if isFirstMove:
        return getBestFirstMove(myTiles, ScoreDictionary)

    # Initialise output
    bestMove = 0, None, None

    # Construct list of all rows and columns
    rowsAndColumns = Board + transposeTable(Board)

    # Iterate through all possible words, in descending order by high play score.
    for highPlayScore, _, word in ScoreDictionary:

        # Set early exit condition: If current high score is greater than the highest play score for 'word', then
        # don't have to check 'word' or any subsequent words (since ScoreDictionary is sorted by high play score).
        if bestMove[0] >= highPlayScore:
            break

        # Check word can be constructed out of all tiles in play.
        if not listInList(word, Tiles[:TILES_USED]):
            continue

        # Iterate through through rows, then all columns of the board.
        for rowColIdx in range(len(rowsAndColumns)):

            # Compare the best move in each row or column with the current best move. Return new best move if is found.
            possibleBestMove, skipToNextWord = getBestMoveInList(Board, myTiles, word, highPlayScore, rowColIdx, rowsAndColumns[rowColIdx], bestMove[0])

            if possibleBestMove is not None:
                bestMove = possibleBestMove

            if skipToNextWord:
                break
    return bestMove


def printBestMove(moveScore, bestScore, bestWord, bestPosition):
    """
    Compare player's score and best possible score in this move, print the highest-scoring move in a formatted string.
    :param moveScore: Player's score for the current move.
    :param bestScore: Best possible score for the current move.
    :param bestWord: Word to play to achieve the best possible score.
    :param bestPosition: Position in which 'bestWord' should be played
    """
    if moveScore == bestScore:
        print("Your move was a highest-scoring move. Well done!")
    positionString = ":".join([str(bestPosition[0]), str(bestPosition[1]), bestPosition[2]])
    scoreMessage = "Maximum possible score in this move was " \
                   "{} with word {} at {}.".format(bestScore, bestWord, positionString)
    print(scoreMessage)


# Game functions
def gameInput(dictionary, firstMoveFlag):
    """
    Handle input stage of game. Get input for word to play, and location to play it. Check inputs are valid
    :param dictionary: List of all allowed words.
    :param firstMoveFlag: 'True' is this move is the first move of the game, otherwise 'False'.
    :return (word, position): The inputted word and position, if both are valid. Otherwise returns (None, None).
    """

    failReturn = None, None

    # Get input from player
    word = input("\nEnter your word: ").upper()  # input should be case-insensitive, so make 'word' upper-case.
    # Check quit condition
    if word == QUIT_WORD:
        return QUIT_WORD, None
    position = input("Enter the location in row:col:direction format: ")

    # Check input is valid.
    if not isValidInput(word, position, dictionary):
        return failReturn

    # Redefine 'position' in more usable form, check position on board is valid.
    # Redefining 'position' will not raise errors, as the format of 'position' has already been verified.
    position = position.split(":")
    position = [int(position[0]), int(position[1]), position[2].upper()]
    if not isOnBoard(word, position, firstMoveFlag):
        return failReturn

    return word, position


def gameMove(word, position, Board, myTiles, firstMoveFlag, ScoreDictionary):
    """
    Handle move stage of game. Place tiles on board, calculate player's score. Calculate best possible move and
    score, and print to player.
    :param word: A valid word to be played
    :param position: A valid position in which 'wod' will be played.
    :param Board: The current state of the board, represented as a list of lists
    :param myTiles: The current tiles available to the player.
    :param firstMoveFlag: 'True' is this move is the first move of the game, otherwise 'False'.
    :param ScoreDictionary: A list of all available words, stored along with their high play scores and total scores.
    :return (newBoard, newTiles, moveScore): Updated copies of board and tiles, and player's score. If position cannot
    be played, returns are set to None.
    """

    failReturn = None, None, None

    # Place tiles on board, check if move is valid. If move is invalid, raise 'ValueError'.
    try:
        # Get new copies of board and tiles. Get letters played.
        newBoard, newTiles, lettersPlayed = placeWord(word, position, Board, myTiles, firstMoveFlag)
    except ValueError as e:
        print(e.args[0])
        return failReturn

    # Calculate player's score for this move.
    moveScore = getWordScore(lettersPlayed)

    # Determine and print best move
    bestScore, bestWord, bestPosition = getBestMove(Board, myTiles, ScoreDictionary, firstMoveFlag)
    printBestMove(moveScore, bestScore, bestWord, bestPosition)

    return newBoard, newTiles, moveScore


def gameUpdate(Board, myTiles, newBoard, newTiles, moveScore, totalScore):
    """
    Handle update stage of game. Update board and tiles, prints scores, print updated board and tiles.
    :param Board: The current state of the board, represented as a list of lists.
    :param myTiles: The current tiles available to the player.
    :param newBoard: The updated state of the board.
    :param newTiles: The remaining tiles available to the player after a word has been played.
    :param moveScore: Player's score for the current move.
    :param totalScore: Player's total score in the game so far.
    """
    # Update board and tiles, increment number of moves performed.
    Board.clear()
    myTiles.clear()
    Board += newBoard
    myTiles += newTiles  # Update myTiles to be the remaining tiles after word is placed
    getTiles(myTiles)  # Get new tiles

    # Update total score and print to player.
    print("Your score in this move: " + str(moveScore))
    print("Your total score is: " + str(totalScore))

    # Print new state of board and tiles.
    printBoard(Board)
    printTiles(myTiles)


def playGame(Board, myTiles, Dictionary):
    """
    Plays the Scrabble game, using the provided board, tiles and dictionary.
    :param Board: A square table, represented as a list of lists.
    :param myTiles: A list of tiles available to the player.
    :param Dictionary: A list of all allowed words.
    """

    # Initialise score and move tracking
    totalScore = 0
    moveCounter = 0
    firstMoveFlag = True

    # Construct score dictionary
    ScoreDictionary = initialiseScoreDictionary(Dictionary)

    # game loop
    while len(myTiles) > 0:

        # INPUT STAGE

        word, position = gameInput(Dictionary, firstMoveFlag)
        if word == QUIT_WORD:
            break
        elif word is None:
            print("Invalid Move!")
            continue

        # MOVE STAGE

        newBoard, newTiles, moveScore = gameMove(word, position, Board, myTiles, firstMoveFlag, ScoreDictionary)
        if moveScore is None:
            print("Invalid Move!")
            continue

        # UPDATE STAGE

        totalScore += moveScore
        gameUpdate(Board, myTiles, newBoard, newTiles, moveScore, totalScore)
        moveCounter += 1
        # Update flag so that tiles can be placed anywhere on the board.
        if firstMoveFlag:
            firstMoveFlag = False
    # Print final game info to player.
    print()
    print("Game ended after {} moves, with {} tiles left to be drawn.".format(moveCounter, len(Tiles) - TILES_USED))
    print("Your final score was: " + str(totalScore))


# Game code
Dictionary = fileToList("dictionary.txt")
playGame(Board, myTiles, Dictionary)
