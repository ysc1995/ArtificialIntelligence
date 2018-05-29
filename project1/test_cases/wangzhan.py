def depthFirstSearch(problem):

    reachedGoal = False
    exploredAll = False

    startState = problem.getStartState()

    exploredStatesDictionary = util.Counter()
    exploredStatesDictionary[0] = problem.getStartState()
    frontierDictionary = util.Counter()
    frontierList = problem.getSuccessors(problem.getStartState())
    # hash table for list of vertices as key
    vectorDictionary = {}

    # create stack to hold the frontier states
    frontierQueue = util.Stack()
    # queue to hold list of actions
    # actionsQueue=util.Queue()
    actionsQueue = []

    # push the frontier states onto the stack
    for i in frontierList:
        fNode = i
        frontierQueue.push(fNode)

    for i in frontierList:
        actionsThisFar = copy.deepcopy(actionsQueue)
        successor = str(i[0])
        vectorDictionary[successor] = actionsThisFar

    # key variable, key to exploredStatesDictionary
    seenAlready = 1
    while reachedGoal == False:

        # get next state to explore, the first state from the stack
        # also save the action required to get to that point
        tempState = frontierQueue.pop()
        nextState = tempState[0]
        nextAction = tempState[1]

        # save the explored state
        exploredStatesDictionary[seenAlready] = nextState
        # save the action taken
        actionsQueue.append(nextAction)

        seenAlready = seenAlready + 1

        # next state becomes current state
        if (exploredAll == True):
            inc = 0
            otherInc = 0

            reset = str(tempState[0])

            newActionsList = vectorDictionary[reset]
            newActionsList.append(tempState[1])

            # empty the old action list
            actionsQueue = copy.deepcopy(newActionsList)

        currentState = nextState

        # check if it is goal
        if (problem.isGoalState(currentState)):
            reachedGoal = True

        else:
            # the current state is not the goal
            # acquire the new frontier


            frontierList = problem.getSuccessors(currentState)
            for i in frontierList:
                actionsThisFar = copy.deepcopy(actionsQueue)
                successor = str(i[0])
                vectorDictionary[successor] = actionsThisFar

            first = frontierList[0]

            # push the unexplored frontier states onto the queue

            explored = False

            counter = 0

            for i in frontierList:

                # counter to keep track of iterations
                explored = False
                exploredAll = False
                for k in exploredStatesDictionary:
                    stateCo = exploredStatesDictionary[k]

                    if ((i[0] == stateCo)):

                        explored = True
                        counter = counter + 1

                        if (counter == ((len(frontierList)))):
                            exploredAll = True


                    elif ((explored == False) and (k == ((len(exploredStatesDictionary))) - 1)):
                        fNode = i
                        frontierQueue.push(fNode)

    "*** YOUR CODE HERE ***"

    return actionsQueue

    util.raiseNotDefined()