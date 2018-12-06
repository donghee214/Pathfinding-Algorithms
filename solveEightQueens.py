import random
import copy
from optparse import OptionParser
import util

class SolveEightQueens:
    def __init__(self, numberOfRuns, verbose, lectureExample):
        """
        Value 1 indicates the position of queen
        """
        self.numberOfRuns = numberOfRuns
        self.verbose = verbose
        self.lectureCase = [[]]
        if lectureExample:
            self.lectureCase = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0],
            [1, 0, 0, 0, 1, 0, 0, 0],
            [0, 1, 0, 0, 0, 1, 0, 1],
            [0, 0, 1, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            ]
    def solve(self):
        solutionCounter = 0

        for i in range(self.numberOfRuns):
            if self.search(Board(self.lectureCase), self.verbose).getNumberOfAttacks() == 0:
                solutionCounter += 1
        print("Solved: %d/%d" % (solutionCounter, self.numberOfRuns))

    def search(self, board, verbose):
        """
        Hint: Modify the stop criterion in this function
        """
        newBoard = board
        i = 0 
        while True:
            if verbose:
                print("iteration %d" % i)
                print(newBoard.toString())
                print("# attacks: %s" % str(newBoard.getNumberOfAttacks()))
                print(newBoard.getCostBoard().toString(True))
            currentNumberOfAttacks = newBoard.getNumberOfAttacks()
            (newBoard, newNumberOfAttacks, newRow, newCol) = newBoard.getBetterBoard()
            i += 1
            if newNumberOfAttacks == 0:
                break
            elif currentNumberOfAttacks <= newNumberOfAttacks:
                self.newBoard(newBoard.squareArray)
        return newBoard

    def newBoard(self, currentBoard):
        for row in range(0, len(currentBoard)):
            for col in range(0, len(currentBoard)):
                if currentBoard[row][col] == 1:
                    currentBoard[row][col] = 0
                    currentBoard[random.randint(0, len(currentBoard) - 1)][col] = 1

class Board:
    def __init__(self, squareArray = [[]]):
        if squareArray == [[]]:
            self.squareArray = self.initBoardWithRandomQueens()
        else:
            self.squareArray = squareArray

    @staticmethod
    def initBoardWithRandomQueens():
        tmpSquareArray = [[ 0 for i in range(8)] for j in range(8)]
        for i in range(8):
            tmpSquareArray[random.randint(0,7)][i] = 1
        return tmpSquareArray
          
    def toString(self, isCostBoard=False):
        """
        Transform the Array in Board or cost Board to printable string
        """
        s = ""
        for i in range(8):
            for j in range(8):
                if isCostBoard: # Cost board
                    cost = self.squareArray[i][j]
                    s = (s + "%3d" % cost) if cost < 9999 else (s + "  q")
                else: # Board
                    s = (s + ". ") if self.squareArray[i][j] == 0 else (s + "q ")
            s += "\n"
        return s 

    def getCostBoard(self):
        """
        First Initalize all the cost as 9999. 
        After filling, the position with 9999 cost indicating the position of queen.
        """
        costBoard = Board([[ 9999 for i in range(8)] for j in range(8)])
        for r in range(8):
            for c in range(8):
                if self.squareArray[r][c] == 1:
                    for rr in range(8):
                        if rr != r:
                            testboard = copy.deepcopy(self)
                            testboard.squareArray[r][c] = 0
                            testboard.squareArray[rr][c] = 1
                            costBoard.squareArray[rr][c] = testboard.getNumberOfAttacks()
        return costBoard

    def getBetterBoard(self):
        """
        "*** YOUR CODE HERE ***"
        This function should return a tuple containing containing four values
        the new Board object, the new number of attacks, 
        the Column and Row of the new queen  
        For exmaple: 
            return (betterBoard, minNumOfAttack, newRow, newCol)
        The datatype of minNumOfAttack, newRow and newCol should be int
        """
        minNumOfAttack = float('inf')
        bestConfig = None
        newRow = None
        newCol = None
        for row in range(0, len(self.squareArray)):
            for col in range(0, len(self.squareArray)):
                if self.squareArray[row][col] == 1:
                    for i in range(0, len(self.squareArray)):
                        if (i, col) != (row, col):
                            self.squareArray[i][col] = 1
                            self.squareArray[row][col] = 0
                            numOfAttacks = self.getNumberOfAttacks()
                            if numOfAttacks < minNumOfAttack:
                                newRow = i
                                newCol = col
                                minNumOfAttack = numOfAttacks
                                bestConfig = copy.deepcopy(self)
                            self.squareArray[row][col] = 1
                            self.squareArray[i][col] = 0
        return (bestConfig, minNumOfAttack, newRow, newCol)

    def getNumberOfAttacks(self):
        """
        "*** YOUR CODE HERE ***"
        This function should return the number of attacks of the current board
        The datatype of the return value should be int
        """

        numOfAttacks = 0
        visited = set()
        for row in range(0, len(self.squareArray)):
            for col in range(0, len(self.squareArray)):
                if self.squareArray[row][col] == 1:
                    # check horizontal
                    for i in range(0, len(self.squareArray)):
                        if (row, i) != (row,col) and self.squareArray[row][i] == 1 and i not in visited:
                            numOfAttacks += 1

                    # check top right
                    vertical = row
                    horizontal = col
                    while vertical >= 0 and horizontal < len(self.squareArray):
                        if (vertical, horizontal) != (row, col) and self.squareArray[vertical][horizontal] == 1 and horizontal not in visited:
                            numOfAttacks += 1
                        vertical -= 1
                        horizontal += 1

                    # check top left
                    vertical = row
                    horizontal = col
                    while vertical >= 0 and horizontal >= 0:
                        if (vertical, horizontal) != (row, col) and self.squareArray[vertical][horizontal] == 1 and horizontal not in visited:
                            numOfAttacks += 1
                        vertical -= 1
                        horizontal -= 1

                    # check bottom left
                    vertical = row
                    horizontal = col
                    while vertical < len(self.squareArray) and horizontal >= 0:
                        if (vertical, horizontal) != (row, col) and self.squareArray[vertical][horizontal] == 1 and horizontal not in visited:
                            numOfAttacks += 1
                        vertical += 1
                        horizontal -= 1

                    # check bottom right
                    vertical = row
                    horizontal = col
                    while vertical < len(self.squareArray) and horizontal < len(self.squareArray):
                        if (vertical, horizontal) != (row, col) and self.squareArray[vertical][horizontal] == 1 and horizontal not in visited:
                            numOfAttacks += 1
                        vertical += 1
                        horizontal += 1

                    visited.add(col)
        # print(numOfAttacks)
        return numOfAttacks




if __name__ == "__main__":
    #Enable the following line to generate the same random numbers (useful for debugging)
    random.seed(1)
    parser = OptionParser()
    parser.add_option("-q", dest="verbose", action="store_false", default=True)
    parser.add_option("-l", dest="lectureExample", action="store_true", default=False)
    parser.add_option("-n", dest="numberOfRuns", default=1, type="int")
    (options, args) = parser.parse_args()
    EightQueensAgent = SolveEightQueens(verbose=options.verbose, numberOfRuns=options.numberOfRuns, lectureExample=options.lectureExample)
    EightQueensAgent.solve()
