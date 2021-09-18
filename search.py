# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
REVERSE_PUSH = False

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """
    trackNode = None
    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def expand(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (child,
        action, stepCost), where 'child' is a child to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that child.
        """
        util.raiseNotDefined()

    def getActions(self, state):
        """
          state: Search state

        For a given state, this should return a list of possible actions.
        """
        util.raiseNotDefined()

    def getActionCost(self, state, action, next_state):
        """
          state: Search state
          action: action taken at state.
          next_state: next Search state after taking action.

        For a given state, this should return the cost of the (s, a, s') transition.
        """
        util.raiseNotDefined()

    def getPathCost(self):
        return SearchProblem.trackNode.getPathCost()

    def getNextState(self, state, action):
        """
          state: Search state
          action: action taken at state

        For a given state, this should return the next state after taking action from state.
        """
        util.raiseNotDefined()

    def getCostOfActionSequence(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()
    
    def getPath(self):
        return SearchProblem.trackNode.getPath()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    fringe = util.Stack()
    return GraphSearch(fringe, problem).search()
    # util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    # util.raiseNotDefined()
    fringe = util.Queue()
    return GraphSearch(fringe, problem).search()


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    # util.raiseNotDefined()
    fringe = util.PriorityQueue()
    return GraphSearch(fringe, problem).search()

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    # util.raiseNotDefined()
    fringe = util.PriorityQueue()
    return GraphSearch(fringe, problem).search(heuristic = heuristic)


class GraphSearch:
    def __init__(self, fringe, problem):
        self.explored = set()
        self.frontier = util.Counter()
        self.fringe = fringe
        self.problem = problem
    
    def pushFringe(self,node, heuristic = lambda x,y: 0):
        cost = node.getPathCost() + heuristic(node.state, self.problem)
        hashNode = node.__hash__()
        self.frontier[hashNode] = cost
        if isinstance(self.fringe, util.PriorityQueue): 
            self.fringe.push(node, cost)
        elif isinstance(self.fringe, util.Queue) or isinstance(self.fringe, util.Stack):
            self.fringe.push(node)
        

    def updateFringe(self, node, heuristic):
        cost = node.getPathCost() + heuristic(node.state, self.problem)
        self.fringe.update(node, cost)

    def popFringe(self):
        popNode = self.fringe.pop()
        hNode = popNode.__hash__()
        if hNode in self.frontier:
            del self.frontier[hNode]
        return popNode

    def search(self, heuristic = lambda x,y: -1): 
        initState = self.problem.getStartState()
        initNode = Node(initState)
        if self.problem.isGoalState(initState):
            return []
        self.pushFringe(initNode)
        while True:
            if self.fringe.isEmpty():
                return []
            curr = self.popFringe()
            self.explored.add(curr)
            if self.problem.isGoalState(curr.state):
                SearchProblem.trackNode = curr
                return curr.getPath()
            for successor in self.problem.expand(curr.state):
                node = Node(successor[0], curr, successor[1], successor[2])
                hnode = node.__hash__()
                if node not in self.explored and hnode not in self.frontier:
                    self.pushFringe(node, heuristic)
                if isinstance(self.fringe, util.PriorityQueue) and hnode in self.frontier:
                    self.updateFringe(node, heuristic)
                    # if heuristic(node.state, self.problem) == 0: # for bfs
                    #     return node.getPath()

class Node:
    def __init__(self, state, parent = None, action = "", stepcost = 0):
        self.parent = parent
        if parent is not None:
            self.pathcost = parent.pathcost + stepcost
        else:
            self.pathcost = stepcost
        self.state = state
        self.action = action
        self.stepcost = stepcost
        SearchProblem.trackNode = self

    def __hash__(self):
        return  self.state.__hash__()
        
    def __eq__(self, other):
        if self.state == other.state:
            return True
        return False

    def getParent(self):
        return self.parent

    def getPathCost(self):
        return self.pathcost

    def getStepCost(self):
        return self.stepcost

    def getPath(self):
        if self.parent is None:
            return []
        return self.parent.getPath() + [self.action]

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
