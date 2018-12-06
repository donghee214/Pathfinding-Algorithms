"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util
import collections
from heapq import heappush, heappop

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()

def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    startState = problem.getStartState()
    visited = set()

    def dfsHelper(problemCopy, coordinate):
        if problemCopy.isGoalState(coordinate):
            return ['Dummy']

        visited.add(coordinate)
        successors = problemCopy.getSuccessors(coordinate)

        for successor in reversed(successors):
            if successor[0] not in visited:
                res = dfsHelper(problemCopy, successor[0])
                if res:
                    newPath = [successor[1]] + res
                    return newPath

        return False

    path = dfsHelper(problem, startState)
    path.pop()
    return path



def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    "*** YOUR CODE HERE ***"
    startState = problem.getStartState()
    visited = set()
    visited.add(startState)
    firstToVisit = problem.getSuccessors(startState)

    toVisit = collections.deque([[firstToVisit[0]]])
    for i in range(1, len(firstToVisit)):
        toVisit.append([firstToVisit[i]])

    while toVisit:
            path = toVisit.popleft()
            node = path[-1]
            if problem.isGoalState(node[0]):
                ret = []
                for point in path:
                    ret.append(point[1])
                return ret
            if node[0] not in visited:
                visited.add(node[0])
                successors = problem.getSuccessors(node[0])
                for successor in successors:
                    newPath = path.copy()
                    newPath.append(successor)
                    toVisit.append(newPath)


def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    "*** YOUR CODE HERE ***"
    startState = problem.getStartState()
    visited = set()
    visited.add(startState)
    successors = problem.getSuccessors(startState)
    toVisit = []
    for successor in successors:
        heappush(toVisit, (successor[-1], [successor]))

    while toVisit:
        path = heappop(toVisit)
        node = path[-1][-1]
        if problem.isGoalState(node[0]):
            ret = []
            for point in path[-1]:
                ret.append(point[1])
            return ret
        if node[0] not in visited:
            visited.add(node[0])
            successors = problem.getSuccessors(node[0])
            for successor in successors:
                newPath = path[-1].copy()
                newPath.append(successor)
                heappush(toVisit, (path[0] + successor[-1], newPath))

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    "*** YOUR CODE HERE ***"
    startState = problem.getStartState()
    toVisit = []
    visited = set()


    heappush(toVisit,(heuristic(startState, problem), [(startState, False, 0)]))
    while toVisit:
        path = heappop(toVisit)
        node = path[-1][-1]

        if problem.isGoalState(node[0]):
            ret = []
            for point in path[-1]:
                if point[1]:
                    ret.append(point[1])
            return ret

        if node[0] not in visited:
            visited.add(node[0])
            successors = problem.getSuccessors(node[0])
            for successor in successors:
                newPath = path[-1].copy()
                newPath.append(successor)
                heappush(toVisit, (path[0] + successor[-1] + heuristic(successor[0], problem) - heuristic(node[0], problem), newPath))






# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
