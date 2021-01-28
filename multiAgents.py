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
import math
import random
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
        #print(legalMoves)
        #print(scores)
        #print(legalMoves[chosenIndex])
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
        GhostLocs = successorGameState.getGhostPositions()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        capsuleLocations = successorGameState.getCapsules()

        "*** YOUR CODE HERE ***"
        """ factors: proximity to food, proximity to ghosts 
        """ 
        if successorGameState.isWin():
            return 10000
        if successorGameState.isLose():
            return -10000

        FoodDistances = []
        foodLocations = newFood.asList()
        for food in foodLocations:
          FoodDistances.append(manhattanDistance(newPos,food))
        closestFood = min(FoodDistances)
        closestFoodLocation = foodLocations[FoodDistances.index(closestFood)]


        GhostsToMe = []
        GhostsToFood = []
        for ghost in GhostLocs:
          GhostsToMe.append(manhattanDistance(newPos,ghost))
          GhostsToFood.append(manhattanDistance(closestFoodLocation,ghost))
        closestGhostToMe = min(GhostsToMe)
        closestGhostToClosestFood = min(GhostsToFood)
        closestGhostLocation = GhostLocs[GhostsToMe.index(closestGhostToMe)] 
        Hueristic = 0.0
        if closestGhostToClosestFood < closestFood:
          if closestGhostToMe > 5:
            Hueristic = (1.0/(closestFood+1.0))*20 - len(foodLocations)*10 - (1/closestGhostToMe)*5
          else:
                Hueristic = (-1/closestGhostToMe)*10000
          #Ghost is closer to me than nearest food so avoid ghost
        else:
          Hueristic = (1.0/(closestFood+1.0))*20 - len(foodLocations)*10 - (1/closestGhostToMe)*5
        return Hueristic
        

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
        bestScore , bestMove = self.minimax(gameState,self.depth,0)
        return bestMove

    def minimax(self,gameState,depth,agentID):
      numGhosts = gameState.getNumAgents() - 1
      legalActions = gameState.getLegalActions(agentID)
      minMove = ''
      maxMove = ''
      if gameState.isWin() or gameState.isLose() or depth ==  0:
          return self.evaluationFunction(gameState) , 0
      if agentID == 0:
        maxVal = -999999
        for action in legalActions:
          val,tempMove = self.minimax(gameState.generateSuccessor(agentID,action),depth, agentID+1)
          if val > maxVal:
            maxVal,maxMove = val,action
        return maxVal, maxMove
      else: 
          minVal = 999999
          if agentID == numGhosts:
            depth = depth - 1
            agentID = -1
          for action in legalActions:
            val,tempMove = self.minimax(gameState.generateSuccessor(agentID,action),depth,agentID+1)
            if val < minVal:
              minVal,minMove = val,action
          return minVal, minMove
        
       

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        bestScore , bestMove = self.alphaBeta(gameState,self.depth,0,-999999,999999)
        return bestMove
      
    def alphaBeta(self,gameState,depth,agentID,alpha,beta):
      numGhosts = gameState.getNumAgents() - 1
      legalActions = gameState.getLegalActions(agentID)
      minMove = ''
      maxMove = ''
      if gameState.isWin() or gameState.isLose() or depth ==  0:
          return self.evaluationFunction(gameState) , 0
      if agentID == 0:
        maxVal = -999999
        for action in legalActions:
          val,tempMove = self.alphaBeta(gameState.generateSuccessor(agentID,action),depth,agentID+1,alpha,beta)
          if val > maxVal:
            maxVal,maxMove = val,action
          alpha = max(alpha,val)
          if beta < alpha:
            break;
        return maxVal, maxMove
      else: 
        minVal = 999999
        if agentID == numGhosts:
          depth = depth - 1
          agentID = -1
        for action in legalActions:
          val,tempMove = self.alphaBeta(gameState.generateSuccessor(agentID,action),depth,agentID+1,alpha,beta)
          if val < minVal:
            minVal,minMove = val,action
          beta = min(beta,val)
          if beta < alpha:
            break;
        return minVal, minMove
    

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
        bestScore , bestMove = self.expectimax(gameState,self.depth,0)
        return bestMove
      
    def expectimax(self,gameState,depth,agentID):
      numGhosts = gameState.getNumAgents() - 1
      legalActions = gameState.getLegalActions(agentID)
      minMove = ''
      maxMove = ''
      
      if gameState.isWin() or gameState.isLose() or depth ==  0:
        return self.evaluationFunction(gameState),0
      
      if agentID == 0:
        maxVal = -999999
        for action in legalActions:
          val,tempMove = self.expectimax(gameState.generateSuccessor(agentID,action),depth, agentID+1)    
          if val > maxVal:
            maxVal,maxMove = val,action
          if maxVal == 99999.0:
            winTrigger = True
        return maxVal, maxMove
      else: 
          minVal = 999999
          averagVal = 0.0
          if agentID == numGhosts:
            depth = depth - 1
            agentID = -1
          for action in legalActions:
            val,tempMove = self.expectimax(gameState.generateSuccessor(agentID,action),depth,agentID+1)
            averagVal = averagVal + val
            if val < minVal:
              minVal,minMove = val,action
          averagVal = averagVal / float(len(legalActions))
          return averagVal, minMove

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
      I basically did the same thing as Q1, Here there are three states if the ghost is farther away then the nearest food the evaluation should favor going towards the food while inversely favoring the distance to the nearest ghost
      if the ghost is closer to the nearest food than the pacman is then check how far away the ghost is
      if the ghost is farther than 4 units you can proceed as normal while taking into account the ghost's distance to you as inversely unfavorable
      if the ghost is closer than 4 units the evaluation only focuses on going away from the ghosts food because losing causes a large loss in points
      We take a signifantly large penalty for the amount of food still left on the grid to encourage the Pacman to finish the board
      The pacman does have a lot of trouble in the end getting the last food dot. I'm not sure what the reason for this is since we had success with this method in Q1
    """
    "*** YOUR CODE HERE ***"
    
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    GhostLocs = currentGameState.getGhostPositions()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    capsuleLocations = currentGameState.getCapsules()
    Hueristic = 0.0
    
    if currentGameState.isWin():
      return 10000
    if currentGameState.isLose():
      return -10000

    FoodDistances = []
    foodLocations = newFood.asList()
    for food in foodLocations:
      FoodDistances.append(manhattanDistance(newPos,food))
    closestFood = min(FoodDistances)
    closestFoodLocation = foodLocations[FoodDistances.index(closestFood)]

    GhostsToMe = []
    GhostsToFood = []
    for ghost in GhostLocs:
      GhostsToMe.append(manhattanDistance(newPos,ghost))
      GhostsToFood.append(manhattanDistance(closestFoodLocation,ghost))
    closestGhostToMe = min(GhostsToMe)
    closestGhostToClosestFood = min(GhostsToFood)
    closestGhostLocation = GhostLocs[GhostsToMe.index(closestGhostToMe)]

    if newPos in currentGameState.getCapsules():
      capsule = 100
    else: 
      capsule = 0
    
    if closestGhostToClosestFood < closestFood:
      if closestGhostToMe > 4:
        Hueristic = (1.0/(closestFood+1.0))*20 - len(foodLocations)*50 - (1/closestGhostToMe)*5
      else:
            Hueristic = (-1/closestGhostToMe)*50
    else:
      Hueristic = (1.0/(closestFood+1.0))*20 - len(foodLocations)*50 - (1/closestGhostToMe)*5
    return Hueristic
# Abbreviation
better = betterEvaluationFunction

