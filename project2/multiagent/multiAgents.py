# multiAgents.py
# --------------
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
#
# Modified by Eugene Agichtein for CS325 Sp 2014 (eugene@mathcs.emory.edu)
#

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        Note that the successor game state includes updates such as available food,
        e.g., would *not* include the food eaten at the successor state's pacman position
        as that food is no longer remaining.
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        currentFood = currentGameState.getFood() #food available from current state
        newFood = successorGameState.getFood() #food available from successor state (excludes food@successor) 
        currentCapsules=currentGameState.getCapsules() #power pellets/capsules available from current state
        newCapsules=successorGameState.getCapsules() #capsules available from successor (excludes capsules@successor)
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        alert = False
        food = ()
        food = newFood.asList()
        gostdis = []
        value1 = 0


        currentghost=newGhostStates[0].getPosition()
        distancetoghost = manhattanDistance(newPos,currentghost)
        if distancetoghost <= 2:
            alert = True
            gostdis.append(distancetoghost)
            value1 = distancetoghost/1.5
        if not alert:
            if len(food) == 0:
                distancetofood = 0
            if len(food) == 1:
                distancetofood = manhattanDistance(newPos, food[0])
            if len(food) >= 2:
                n = 0
                dissum=0
                for i in range(len(food)):
                    dissum +=manhattanDistance(newPos,food[i])
                    n=n+1
                averagedis=dissum/n

                distancetofood = averagedis
        else:
            distancetofood = max(gostdis)

        value2 = 0.5 / (distancetofood + 150) + 1.0 / (len(food) + 1)
        value = value2 - value1
        return value

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"

        result = self.minimaxDecision(gameState, 0)
        return result[0]

    def minimaxDecision(self, gameState, level):
        num = gameState.getNumAgents()
        win = gameState.isWin()
        lost = gameState.isLose()
        if level == self.depth * num :
            return (None, self.evaluationFunction(gameState))
        if win or lost:
            return (None, self.evaluationFunction(gameState))

        if not level % num == 0:
            return self.minValue(gameState, level)
        else:
            return self.maxValue(gameState, level)


    def maxValue(self, gameState, level):

        if len(gameState.getLegalActions(0)) == 0:
            return (None, self.evaluationFunction(gameState))
        v=-100000
        for a in gameState.getLegalActions(0):
            currdecision = self.minimaxDecision(gameState.generateSuccessor(0, a), level + 1)
            if currdecision[1] > v:
                max = (a, currdecision[1])
                v=currdecision[1]
        return max


    def minValue(self, gameState, level):

        if len(gameState.getLegalActions(level % gameState.getNumAgents())) == 0:
            return (None, self.evaluationFunction(gameState))

        v=100000
        for a in gameState.getLegalActions(level % gameState.getNumAgents()):
            currdecision = self.minimaxDecision(gameState.generateSuccessor(level % gameState.getNumAgents(), a), level + 1)
            if currdecision[1] < v:
                min= (a, currdecision[1])
                v=currdecision[1]
        return min




class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        result = self.minimaxDecision(gameState, 0, -100000,100000)
        return result[0]

    def minimaxDecision(self, gameState, level, A, B):
        num = gameState.getNumAgents()
        win = gameState.isWin()
        lost = gameState.isLose()
        if level == self.depth * num:
            return (None, self.evaluationFunction(gameState))
        if win or lost:
            return (None, self.evaluationFunction(gameState))

        if not level % num == 0:
            return self.minValue(gameState, level,A,B)
        else:
            return self.maxValue(gameState, level,A,B)

    def maxValue(self, gameState, level,A,B):

        if len(gameState.getLegalActions(0)) == 0:
            return (None, self.evaluationFunction(gameState))
        v = -100000
        max=(None,-100000)
        for a in gameState.getLegalActions(0):
            currdecision = self.minimaxDecision(gameState.generateSuccessor(0, a), level + 1, A,B)
            if currdecision[1] > v:
                max = (a, currdecision[1])
                v = currdecision[1]
            if v>B:
                return max
            if A < v:
                A = v
        return max

    def minValue(self, gameState, level,A,B):

        if len(gameState.getLegalActions(level % gameState.getNumAgents())) == 0:
            return (None, self.evaluationFunction(gameState))

        v = 100000
        min=(None,v)
        for a in gameState.getLegalActions(level % gameState.getNumAgents()):
            currdecision = self.minimaxDecision(gameState.generateSuccessor(level % gameState.getNumAgents(), a),level + 1,A,B)
            if currdecision[1] < v:
                min = (a, currdecision[1])
                v = currdecision[1]
            if v<A:
                return min
            if B > v:
                B=v
        return min

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        result = self.maxValue(gameState, 0)
        return result[0]

    def getValue(self, gameState,  level):
        num = gameState.getNumAgents()
        win = gameState.isWin()
        lost = gameState.isLose()
        if level == self.depth * num :
            return self.evaluationFunction(gameState)
        if win or lost :
            return self.evaluationFunction(gameState)

        if level % gameState.getNumAgents() == 0:
            return self.maxValue(gameState, level)[1]
        else:
            return self.expValue(gameState, level)

    def maxValue(self, gameState, level):

        if len(gameState.getLegalActions(0)) == 0:
            return (None, self.evaluationFunction(gameState))
        v = -10000
        for a in gameState.getLegalActions(0):

            currdecision = self.getValue(gameState.generateSuccessor(0, a),level+1)
            if currdecision > v:
                v = currdecision
                max=[a,v]

        return max

    def expValue(self, gameState, level):
        if len(gameState.getLegalActions(level % gameState.getNumAgents())) == 0:
            return (None, self.evaluationFunction(gameState))
        sum=0.0
        n=0
        for a in gameState.getLegalActions(level % gameState.getNumAgents()):
            currdecision = self.getValue(gameState.generateSuccessor(level % gameState.getNumAgents(), a),  level+1)
            n+=1
            sum+=currdecision

        expvalue = sum / n

        return expvalue


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <use the currentGameState.getScore() function minus the minimum distance to the ghost>
    """

    currentGhostPosition = []
    mindis=100000

    for currentghostState in currentGameState.getGhostStates():
        currentGhostPosition.append(currentghostState.getPosition())
        for ghost in currentGhostPosition:
            dist = manhattanDistance(currentGameState.getPacmanPosition(), ghost)
            if mindis>dist:
                mindis=dist

    score = currentGameState.getScore()-mindis
    return score


# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
    """
      Your agent for the mini-contest
    """

    def getAction(self, gameState):
        """
          Returns an action.  You can use any method you want and search to any depth you want.
          Just remember that the mini-contest is timed, so you have to trade off speed and computation.

          Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
          just make a beeline straight towards Pacman (or away from him if they're scared!)
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

