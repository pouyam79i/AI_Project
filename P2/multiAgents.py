# multiAgents.py
# --------------
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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        if successorGameState.isWin():
            return 99999
        if successorGameState.isLose():
            return -99999

        min_food_dis = 1
        if len(newFood.asList()) > 0:
            foodDis = [manhattanDistance(f, newPos) for f in newFood.asList()]
            min_food_dis = min(foodDis)
        food_effect_score = (1 / min_food_dis) * 10

        ghost_effect_score = 0
        all_ghosts_far = True
        for i, g in enumerate(newGhostStates):
            ghost_dis = manhattanDistance(g.getPosition(), newPos)
            if newScaredTimes[i] > 8 and ghost_dis < 4:
                # LETS NOT DO THIS NOW :D
                ghost_effect_score += 0
            elif ghost_dis < 4:
                ghost_effect_score -= 50
            if ghost_dis < 4 and newScaredTimes[i] < 8:
                all_ghosts_far = False
        if all_ghosts_far:
            ghost_effect_score += 50

        action_effect_score = 0
        if action == Directions.STOP:
            action_effect_score = -10

        return food_effect_score + ghost_effect_score + action_effect_score + successorGameState.getScore()

        return successorGameState.getScore()

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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        agent_numbers = gameState.getNumAgents()
        
        def maxVal(depth, gameState):
            depth -= 1
            if depth == 0 or gameState.isLose() or gameState.isWin():
                return self.evaluationFunction(gameState)
            max_value = float('-inf')
            for action in gameState.getLegalActions(0):
                max_value = max(max_value, minVal(depth, 1, gameState.generateSuccessor(0, action)))
            return max_value

        def minVal(depth, agentIndex, gameState):
            if gameState.isLose() or gameState.isWin():
                return self.evaluationFunction(gameState)
            min_value = float('inf')
            for action in gameState.getLegalActions(agentIndex):
                if agentIndex < (agent_numbers - 1):
                    # Check next ghost if there is still one left
                    min_value = min(min_value, minVal(depth, agentIndex + 1, gameState.generateSuccessor(agentIndex, action)))
                else:
                    # Next move blongs to pacman
                    min_value = min(min_value, maxVal(depth, gameState.generateSuccessor(agentIndex, action)))
            return min_value

        # root is here (pacman chooses)
        max_value = float('-inf')
        result = Directions.STOP
        for action in gameState.getLegalActions(0):
            value = minVal(self.depth, 1, gameState.generateSuccessor(0, action))
            if value > max_value:
                max_value = value
                result = action

        return result

        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        agent_numbers = gameState.getNumAgents()
        
        def maxVal(depth, gameState, alpha, beta):
            depth -= 1
            if depth == 0 or gameState.isLose() or gameState.isWin():
                return self.evaluationFunction(gameState)
            max_value = float('-inf')
            for action in gameState.getLegalActions(0):
                max_value = max(max_value, minVal(depth, 1, gameState.generateSuccessor(0, action), alpha, beta))
                if beta < max_value:
                    break
                alpha = max(alpha, max_value)
            return max_value

        def minVal(depth, agentIndex, gameState, alpha, beta):
            if gameState.isLose() or gameState.isWin():
                return self.evaluationFunction(gameState)
            min_value = float('inf')
            for action in gameState.getLegalActions(agentIndex):
                if agentIndex < (agent_numbers - 1):
                    # Check next ghost if there is still one left
                    min_value = min(min_value, minVal(depth, agentIndex + 1, gameState.generateSuccessor(agentIndex, action), alpha, beta))
                else:
                    # Next move blongs to pacman
                    min_value = min(min_value, maxVal(depth, gameState.generateSuccessor(agentIndex, action), alpha, beta))
                if min_value < alpha:
                    break
                beta = min(beta, min_value)
            return min_value

        # root is here (pacman chooses)
        alpha = float('-inf')
        beta = float('inf')
        result = Directions.STOP
        for action in gameState.getLegalActions(0):
            value = minVal(self.depth, 1, gameState.generateSuccessor(0, action), alpha, beta)
            if value > alpha:
                alpha = value
                result = action
                
        return result

        util.raiseNotDefined()

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
        "*** YOUR CODE HERE ***"
        
        agent_numbers = gameState.getNumAgents()
        
        def maxVal(depth, gameState):
            depth -= 1
            if depth == 0 or gameState.isLose() or gameState.isWin():
                return self.evaluationFunction(gameState)
            max_value = float('-inf')
            for action in gameState.getLegalActions(0):
                max_value = max(max_value, chanseVal(depth, 1, gameState.generateSuccessor(0, action)))
            return max_value

        def chanseVal(depth, agentIndex, gameState):
            if gameState.isLose() or gameState.isWin():
                return self.evaluationFunction(gameState)

            if not gameState.getLegalActions(agentIndex):
                return self.evaluationFunction(gameState)
            
            chanse_val = 0
            legal_action_number = len(gameState.getLegalActions(agentIndex))
            for action in gameState.getLegalActions(agentIndex):
                if agentIndex < (agent_numbers - 1):
                    # Check next ghost if there is still one left
                    chanse_val += chanseVal(depth, agentIndex + 1, gameState.generateSuccessor(agentIndex, action))
                else:
                    # Next move blongs to pacman
                    chanse_val += maxVal(depth, gameState.generateSuccessor(agentIndex, action))
            chanse_val = chanse_val / legal_action_number
            return chanse_val

        # root is here (pacman chooses)
        max_value = float('-inf')
        result = Directions.STOP
        for action in gameState.getLegalActions(0):
            value = chanseVal(self.depth, 1, gameState.generateSuccessor(0, action))
            if value > max_value:
                max_value = value
                result = action

        return result
        
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    Don't forget to use pacmanPosition, foods, scaredTimers, ghostPositions!
    DESCRIPTION: <write something here so we know what you did>
    """

    pacmanPosition = currentGameState.getPacmanPosition()
    foods = currentGameState.getFood()
    ghostStates = currentGameState.getGhostStates()
    scaredTimers = [ghostState.scaredTimer for ghostState in ghostStates]
    ghostPositions = currentGameState.getGhostPositions()
    
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
