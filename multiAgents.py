# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.

from util import manhattanDistance
from game import Directions
import random, util
from game import Agent

class ReflexAgent(Agent):
    def getAction(self, gameState):
        legalMoves = gameState.getLegalActions()
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)
        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()

        if action == 'Stop':
            return float("-inf")
        for state in newGhostStates:
            if state.getPosition() == newPos and (state.scaredTimer == 0):
                return float("-inf")
        foodList = newFood.asList()
        if not foodList:
            return float("inf")
        minDistance = min([manhattanDistance(newPos, food) for food in foodList])
        return successorGameState.getScore() + (1.0 / minDistance)

def scoreEvaluationFunction(currentGameState):
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    def getAction(self, gameState):
        def minimax(state, agentIndex, depth):
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)
            
            legalActions = state.getLegalActions(agentIndex)
            if not legalActions:
                return self.evaluationFunction(state)

            if agentIndex == 0: # Lượt Pacman (MAX)
                return max(minimax(state.generateSuccessor(agentIndex, action), 1, depth) for action in legalActions)
            else: # Lượt Ghosts (MIN)
                nextAgent = agentIndex + 1
                nextDepth = depth
                if nextAgent == state.getNumAgents():
                    nextAgent = 0
                    nextDepth += 1
                return min(minimax(state.generateSuccessor(agentIndex, action), nextAgent, nextDepth) for action in legalActions)

        legalActions = gameState.getLegalActions(0)
        bestAction = Directions.STOP
        bestScore = float('-inf')
        for action in legalActions:
            score = minimax(gameState.generateSuccessor(0, action), 1, 0)
            if score > bestScore:
                bestScore = score
                bestAction = action
        return bestAction

class AlphaBetaAgent(MultiAgentSearchAgent):
    def getAction(self, gameState):
        def alphaBeta(state, agentIndex, depth, alpha, beta):
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)
            
            legalActions = state.getLegalActions(agentIndex)
            if not legalActions: # Xử lý lỗi mảng rỗng
                return self.evaluationFunction(state)

            if agentIndex == 0: # MAX
                v = float('-inf')
                for action in legalActions:
                    v = max(v, alphaBeta(state.generateSuccessor(agentIndex, action), 1, depth, alpha, beta))
                    if v > beta: return v
                    alpha = max(alpha, v)
                return v
            else: # MIN
                v = float('inf')
                nextAgent = agentIndex + 1
                nextDepth = depth
                if nextAgent == state.getNumAgents():
                    nextAgent = 0
                    nextDepth += 1
                for action in legalActions:
                    v = min(v, alphaBeta(state.generateSuccessor(agentIndex, action), nextAgent, nextDepth, alpha, beta))
                    if v < alpha: return v
                    beta = min(beta, v)
                return v

        legalActions = gameState.getLegalActions(0)
        bestAction = Directions.STOP
        bestScore = float('-inf')
        alpha = float('-inf')
        beta = float('inf')
        for action in legalActions:
            score = alphaBeta(gameState.generateSuccessor(0, action), 1, 0, alpha, beta)
            if score > bestScore:
                bestScore = score
                bestAction = action
            alpha = max(alpha, bestScore)
        return bestAction

class ExpectimaxAgent(MultiAgentSearchAgent):
    def getAction(self, gameState):
        def expectimax(state, agentIndex, depth):
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)
            
            legalActions = state.getLegalActions(agentIndex)
            if not legalActions:
                return self.evaluationFunction(state)

            if agentIndex == 0: # MAX
                return max(expectimax(state.generateSuccessor(agentIndex, action), 1, depth) for action in legalActions)
            else: # EXPECTED
                nextAgent = agentIndex + 1
                nextDepth = depth
                if nextAgent == state.getNumAgents():
                    nextAgent = 0
                    nextDepth += 1
                totalScore = sum(expectimax(state.generateSuccessor(agentIndex, action), nextAgent, nextDepth) for action in legalActions)
                return totalScore / float(len(legalActions))

        legalActions = gameState.getLegalActions(0)
        bestAction = Directions.STOP
        bestScore = float('-inf')
        for action in legalActions:
            score = expectimax(gameState.generateSuccessor(0, action), 1, 0)
            if score > bestScore:
                bestScore = score
                bestAction = action
        return bestAction

def betterEvaluationFunction(currentGameState):
    if currentGameState.isWin(): return 999999
    if currentGameState.isLose(): return -999999

    pos = currentGameState.getPacmanPosition()
    food = currentGameState.getFood()
    ghostStates = currentGameState.getGhostStates()
    capsules = currentGameState.getCapsules()

    score = currentGameState.getScore()

    # Phân loại Ma
    activeGhosts = [g for g in ghostStates if g.scaredTimer == 0]
    scaredGhosts = [g for g in ghostStates if g.scaredTimer > 0]

    foodList = food.asList()
    minFoodDist = min([manhattanDistance(pos, f) for f in foodList]) if foodList else 0
    
    score -= 1.5 * minFoodDist
    score -= 20.0 * len(foodList)
    score -= 20.0 * len(capsules)

    if activeGhosts:
        minActiveGhostDist = min([manhattanDistance(pos, g.getPosition()) for g in activeGhosts])
        if minActiveGhostDist <= 1:
            score -= 99999
        else:
            score -= 2.0 / minActiveGhostDist

    if scaredGhosts:
        minScaredGhostDist = min([manhattanDistance(pos, g.getPosition()) for g in scaredGhosts])
        score -= 2.0 * minScaredGhostDist 

    return score

# Abbreviation
better = betterEvaluationFunction