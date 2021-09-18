import random
import search

class EightPuzzleState:
    def __init__(self, numbers):
        self.cells = []
        num = numbers.copy()
        index = num.index(0)
        if index / 3 >= 0:
            self.blankLocation = 0, index
        if index / 3 >= 1:
            self.blankLocation = 1, index - 3
        if index / 3 >= 2:
            self.blankLocation = 2, index - 6
        self.cells.append([num[i] for i in range(3)])
        self.cells.append([num[i] for i in range(3,6)])
        self.cells.append([num[i] for i in range(6,9)])
    
    def isGoal(self):
        goal = [[0,1,2], [3,4,5], [6,7,8]]
        if self.cells == goal:
            return True
        return False

    def legalMoves(self):
        moves = []
        row, col = self.blankLocation
        if(row != 0):
            moves.append('up')
        if(row != 2):
            moves.append('down')
        if(col != 0):
            moves.append('left')
        if(col != 2):
            moves.append('right')
        
        return moves

    def result(self, move):
        row, col = self.blankLocation
        if(move == 'up'):
            newrow = row - 1
            newcol = col
        elif(move == 'down'):
            newrow = row + 1
            newcol = col
        elif(move == 'left'):
            newrow = row
            newcol = col - 1
        elif(move == 'right'):
            newrow = row
            newcol = col + 1
        else:
            raise "Illegal Move"

        newPuzzle = EightPuzzleState([0, 0, 0, 0, 0, 0, 0, 0, 0])
        newPuzzle.cells = [values[:] for values in self.cells]
        newPuzzle.cells[row][col] = newPuzzle.cells[newrow][newcol]
        newPuzzle.cells[newrow][newcol] = 0
        newPuzzle.blankLocation = newrow, newcol
        return newPuzzle

    def __eq__(self, other):
        for row in range( 3 ):
            if self.cells[row] != other.cells[row]:
                return False
        return True

    def __hash__(self):
        return hash(str(self.cells))

    def __getAsciiString(self):
        """
          Returns a display string for the maze
        """
        lines = []
        horizontalLine = ('-' * (13))
        lines.append(horizontalLine)
        for row in self.cells:
            rowLine = '|'
            for col in row:
                if col == 0:
                    col = ' '
                rowLine = rowLine + ' ' + col.__str__() + ' |'
            lines.append(rowLine)
            lines.append(horizontalLine)
        return '\n'.join(lines)

    def __str__(self):
        return self.__getAsciiString()

class EightPuzzleSearchProblem():
    def __init__(self, puzzle):
        self.puzzle = puzzle

    def getStartState(self):
        return self.puzzle

    def isGoalState(self, state):
        return state.isGoal()

    def getSuccessors(self, state):
        succ = []
        for a in state.legalMoves():
            succ.append((state.result(a), a, 1))
        return succ

    def getCostOfActions(self, actions):
        return len(actions)

EIGHT_PUZZLE_DATA = [[1, 0, 2, 3, 4, 5, 6, 7, 8],
                     [1, 7, 8, 2, 3, 4, 5, 6, 0],
                     [4, 3, 2, 7, 0, 5, 1, 6, 8],
                     [5, 1, 3, 4, 0, 2, 6, 7, 8],
                     [1, 2, 5, 7, 6, 8, 0, 4, 3],
                     [0, 3, 1, 6, 8, 2, 7, 5, 4]]

def loadEightPuzzle(puzzleNumber):
    return EightPuzzleState(EIGHT_PUZZLE_DATA[puzzleNumber])

def createRandomEightPuzzle(moves=100):
    puzzle = EightPuzzleState([1,2,3,4,0,5,6,7,8])
    # for i in range(moves):
    #     # Execute a random legal move
    #     puzzle = puzzle.result(random.sample(puzzle.legalMoves(), 1)[0])
    return puzzle

if __name__ == '__main__':
    puzzle = createRandomEightPuzzle(25)
    print('A random puzzle:')
    print(puzzle)
    # puzzle.result('left')
    puzzleProb = EightPuzzleSearchProblem(puzzle)
    # moves = puzzleProb.getSuccessors(puzzleProb.getStartState())
    # paths, cost = search.breadthFirstSearch(puzzleProb)
    paths, cost = search.depthFirstSearch(puzzleProb)
    # paths, cost = search.uniformCostSearch(puzzleProb)

    print("{} moves".format(puzzleProb.getCostOfActions(paths)))
    curr = puzzle
    print(paths)
    for path in paths:
        curr = curr.result(path)
        print(curr)
    
