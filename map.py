import search
import random
import time
# Module Classes

class City:
    def __init__(self, name, cost):
        self.name = name
        self.cost = cost

COST_TABLE = [
    ['Oradea', 'Sibiu', 151],
    ['Oradea', 'Zerind', 71],
    ['Zerind', 'Arad', 75],
    ['Arad', 'Sibiu', 140],
    ['Arad', 'Timisoara', 118],
    ['Timisoara', 'Lugoj', 111],
    ['Mehadia', 'Lugoj', 70], 
    ['Sibiu', 'Fagaras', 99],
    ['Sibiu', 'Rimnicu Vilcea', 80],
    ['Rimnicu Vilcea', 'Pitesti', 97],
    ['Bucharest', 'Pitesti', 101],
    ['Bucharest', 'Fagaras', 211],
    ['Mehadia', 'Drobeta', 75],
    ['Drobeta', 'Craiova', 120],
    ['Craiova', 'Pitesti', 138],
    ['Craiova', 'Rimnicu Vilcea', 138],
    ['Giurgiu', 'Bucharest', 90]
 ]   

CITIES = [
    {'name': 'Oradea', 'neighbor': ['Zerind', 'Sibiu']},
    {'name': 'Zerind', 'neighbor': ['Oradea', 'Arad']},
    {'name': 'Arad', 'neighbor': ['Zerind', 'Sibiu', 'Timisoara']},
    {'name': 'Sibiu', 'neighbor': ['Oradea', 'Arad', 'Fagaras', 'Rimnicu Vilcea']},
    {'name': 'Timisoara', 'neighbor': ['Arad', 'Lugoj']},
    {'name': 'Lugoj', 'neighbor': ['Timisoara', 'Mehadia']},
    {'name': 'Fagaras', 'neighbor': ['Sibiu', 'Bucharest']},
    {'name': 'Rimnicu Vilcea', 'neighbor': ['Sibiu', 'Pitesti', 'Craiova']},
    {'name': 'Pitesti', 'neighbor': ['Rimnicu Vilcea', 'Craiova', 'Bucharest']},
    {'name': 'Bucharest', 'neighbor': ['Pitesti', 'Fagaras', 'Giurgiu']},
    # {'name': , 'neighbor': }
    {'name': 'Mehadia', 'neighbor': ['Lugoj', 'Drobeta']},
    {'name': 'Drobeta', 'neighbor': ['Mehadia', 'Craiova']},
    {'name': 'Craiova', 'neighbor': ['Drobeta', 'Rimnicu Vilcea', 'Pitesti']},
    {'name': 'Giurgiu', 'neighbor': ['Bucharest']}
]

def getCost(cName1, cName2):
    for i in COST_TABLE:
        if cName1 in i and cName2 in i:
            return i[2]

def getCity(name):
    for c in CITIES:
        if name == c['name']:
            return c.copy()

class MapState:
    def __init__( self, cities, cur, des ):    
        self.cities = cities    
        self.cur = getCity(cur)
        self.des = des       

    def isGoal( self ):    
        if self.cur['name'] == self.des:
            return True
        return False

    def legalMoves( self ):
        """
          Returns a list of legal moves from the current state.        
        """
        return self.cur['neighbor']

    def result(self, move):
        """

        The move should be a string drawn from a list returned by legalMoves.
        Illegal moves will raise an exception, which may be an array bounds
        exception.

        NOTE: This function *does not* change the current object.  Instead,
        it returns a new object.
        """                        
        # Create a copy of the current chess board        
        newMap = MapState(CITIES, move, self.des)        
        # And update it to reflect the move        
        return newMap

    # Utilities for comparison and display
    def __eq__(self, other):
        """
            Overloads '==' such that two eightPuzzles with the same configuration
          are equal.

          >>> EightPuzzleState([0, 1, 2, 3, 8, 5, 8, 7, 8]) == \
              EightPuzzleState([1, 0, 2, 3, 8, 5, 8, 7, 8]).result('left')
          True
        """
        if self.cur['name'] != other.cur['name']:
            return False
        return True

    def __hash__(self):
        return hash(str(self.cur))

    def __getAsciiString(self):
        """
          Returns a display string for the maze
        """
        return self.cur['name']    

    def __str__(self):
        return self.__getAsciiString()

# TODO: Implement The methods in this class

class MapSearchProblem(search.SearchProblem):
    """
      Implementation of a SearchProblem for the  Eight Puzzle domain

      Each state is represented by an instance of an eightPuzzle.
    """
    def __init__(self, rMap):
        "Creates a new EightPuzzleSearchProblem which stores search information."
        self.rMap = rMap

    def getStartState(self):
        return self.rMap

    def isGoalState(self, state):
        return state.isGoal()

    def expand(self,state):
        """
          Returns list of (successor, action, stepCost) pairs where
          each succesor is either left, right, up, or down
          from the original state and the cost is 1.0 for each
        """
        succ = []
        for a in state.legalMoves():
            cost = getCost(state.cur['name'], a)
            succ.append((state.result(a), a, cost))
        return succ

    def getActionCost(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        return sum(actions)

if __name__ == '__main__':    
    rMap = MapState(CITIES, 'Zerind', 'Bucharest')
    problem = MapSearchProblem(rMap)    
    # path = search.GraphSearch(problem).findSolution(4, 4)
    path = search.aStarSearch(problem)
    print(rMap)
    if not path:
        print("Cannot find any path!")
    else:
        print('Algorithm found a path \n%d moves: %s\ncost: %d' % (len(path), str(path), problem.getPathCost()))
