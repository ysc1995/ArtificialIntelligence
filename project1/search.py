# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util

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

class Node():
    def __init__(self,state):
        self.state =state


class Node2():


    def __init__(self,state,direction,parent,cost):
        self.state=state
        self.direction = direction
        self.parent= parent
        if parent==None:
            self.cost = cost
        else:
            self.cost = cost + parent.cost

    def getParent(self):
        return self.parent
    def getDirection(self):
        return self.direction
    def getState(self):
        return self.state
    def getCost(self):
        return self.cost

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """

    """"
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    print "successors: ", problem.getStartState()
    """

    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    e = Directions.EAST
    n = Directions.NORTH

    root = problem.getStartState()
    stack = util.Stack()
    stack.push(problem.getSuccessors(root))
    queue = util.Queue()
    queue.push(root)
    trace = util.Queue()



    for i in stack.pop():
        currentnode = Node()

        currentnode = i
        if i not in queue:
            stack.push(problem.getSuccessors(i))
            if problem.isGoalState(i):
                break
            queue.push(i)
    """


    stack = util.Stack()
    stack.push(Node2(problem.getStartState(), None, None,0))
    checklist = set()
    #set stack and checklist for checking if already visited

    while (not stack.isEmpty()):
        currentnode = stack.pop()
        if problem.isGoalState(currentnode.getState()):
            #if get the goal, find the path to start and reverse it
            actions = []
            actionsreverse = []

            while currentnode.getDirection() is not None:
                actions.append(currentnode.getDirection())
                currentnode = currentnode.getParent()

            for i in range(0 , len(actions)):
                actionsreverse.append(actions.pop())

            return actionsreverse
        if currentnode.getState() not in checklist:
            #if no goal, check if is visited. if not, push to stack and add visited

            checklist.add(currentnode.getState())
            for successor in problem.getSuccessors(currentnode.getState()):
                stack.push(Node2(successor[0], successor[1], currentnode,successor[2]))



    return []

    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    queue = util.Queue()
    queue.push(Node2(problem.getStartState(), None, None,0))
    checklist = set()
    while (not queue.isEmpty()):
        currentnode = queue.pop()
        if problem.isGoalState(currentnode.getState()):
            actions = []
            actionsreverse = []

            while currentnode.getDirection() is not None:
                actions.append(currentnode.getDirection())
                currentnode = currentnode.getParent()

            for i in range(0, len(actions)):
                actionsreverse.append(actions.pop())

            return actionsreverse
        if currentnode.getState() not in checklist:

            checklist.add(currentnode.getState())
            for successor in problem.getSuccessors(currentnode.getState()):
                queue.push(Node2(successor[0], successor[1], currentnode,successor[2]))

    "*** YOUR CODE HERE ***"
    #util.raiseNotDefined()

def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    pqueue = util.PriorityQueue()
    pqueue.push(Node2(problem.getStartState(), None, None, 0),0)
    checklist = set()
    while (not pqueue.isEmpty()):
        currentnode = pqueue.pop()
        if problem.isGoalState(currentnode.getState()):
            actions = []
            actionsreverse = []

            while currentnode.getDirection() is not None:
                actions.append(currentnode.getDirection())
                currentnode = currentnode.getParent()

            for i in range(0, len(actions)):
                actionsreverse.append(actions.pop())

            return actionsreverse
        if currentnode.getState() not in checklist:

            checklist.add(currentnode.getState())
            for successor in problem.getSuccessors(currentnode.getState()):
                pqueue.push(Node2(successor[0], successor[1], currentnode, successor[2]), Node2(successor[0], successor[1], currentnode, successor[2]).getCost())
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."

    pqueue = util.PriorityQueue()
    pqueue.push(Node2(problem.getStartState(), None, None, 0), 0)
    checklist = set()
    while (not pqueue.isEmpty()):
        currentnode = pqueue.pop()
        if problem.isGoalState(currentnode.getState()):
            actions = []
            actionsreverse = []

            while currentnode.getDirection() is not None:
                actions.append(currentnode.getDirection())
                currentnode = currentnode.getParent()

            for i in range(0, len(actions)):
                actionsreverse.append(actions.pop())

            return actionsreverse
        if currentnode.getState() not in checklist:

            checklist.add(currentnode.getState())
            for successor in problem.getSuccessors(currentnode.getState()):
                pqueue.push(Node2(successor[0], successor[1], currentnode, successor[2]), Node2(successor[0], successor[1], currentnode, successor[2]).getCost()+heuristic(Node2(successor[0], successor[1], currentnode, successor[2]).getState(),problem))
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
