import util

def depthFirstSearch(problem):
    frontier = util.Stack()
    explored = set()
    return graphSearch(frontier, explored, problem, 'DFS')
        
def breadthFirstSearch(problem):
    frontier = util.Queue()
    explored = set()
    return graphSearch(frontier, explored, problem, 'BFS')

def uniformCostSearch(problem):
    frontier = util.PriorityQueue()
    explored = set()
    return graphSearch(frontier, explored, problem, 'UCS')

def depthLimitedSearch(problem, limit):
    return recursiveDLS(Node(problem.getStartState()), problem, limit)

def recursiveDLS(node, problem, limit):
    if problem.isGoalState(node.state):
        return node.getPath()
    elif limit == 0:
        return 'cutoff'
    else:
        cutoff_occured = False
        for action in problem.getSuccessors(node.state):
            child = Node(action[0], node, action[1], action[2])
            result = recursiveDLS(child, problem, limit - 1)
            if result == 'cutoff':
                cutoff_occured = True
            elif result:
                return result
        return 'cutoff' if cutoff_occured else False
        
def iterativeDeepeningSearch(problem):
    depth = 0
    while True:
        result = depthLimitedSearch(problem, depth)
        if result != 'cutoff': 
            return result
        depth += 1

def graphSearch(frontier, explored, problem, method): 
    initState = problem.getStartState()
    if problem.isGoalState(initState):
        return ''
    initNode = Node(initState)
    if method == "UCS":
        frontier.push(initNode, initNode.getPathCost())
    else:
        frontier.push(initNode)
    while True:
        if frontier.isEmpty():
            return False
        curr = frontier.pop()
        explored.add(curr)
        if problem.isGoalState(curr.state):
            return (curr.getPath(), curr.getPathCost())
        for node in problem.getSuccessors(curr.state):
            node = Node(node[0], curr, node[1], node[2])
            nodeList = frontier.list if method != 'UCS' else [item[2] for item in frontier.heap] 
            if node not in explored and node not in  nodeList:
                if method == 'UCS':
                    frontier.push(node, node.getPathCost())
                else:
                    frontier.push(node)
            if method == "UCS" and node in nodeList:
                frontier.update(node, node.getPathCost())


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

    