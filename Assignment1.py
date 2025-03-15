from collections import deque
import time
import copy
import math
import random

initialState = []
initialStateStr = []
givenSol = []

# Class to create new node
class Node:
    def __init__(self, state, stateStr, nextSts, parent, action) :
        self.state = state
        self.stateStr = stateStr
        self.nextSts = nextSts # Children
        self.parent = parent
        self.action = action # Path/Solution
        self.f = 0 # f(n) for heuristic
        self.g = 0 # g(n) for heuristic

# Defined Functions
# Print board 
def printBoard(x) :
    print("+-------------+")
    for i in range(6) : 
        print("|", end = " ")
        for j in range(6) : 
            print(x[6 * i + j], end = " ")
        if i == 2 : print(" ==>")
        else : print("|")
    print("+-------------+") 

# Create child node
def createChild(parent, i, state, stateStr) :
    childAct = copy.copy(parent.action)
    childAct.append(parent.nextSts[i])
    child = Node(state, stateStr, collectMoveData(state, stateStr), parent, childAct)
    return child

# Collect vehicle data of each state
# Calculate the type, orientation, coordinate(x, y) and position of the vehicles
def collectData(stateStr) :
    vehicleData = {}
    for x in stateStr :
        if x not in vehicleData and x != '.':
            vehicleData[x] = {}
            start = stateStr.find(x)
            end = stateStr.rfind(x)
            vehicleType = end - start
            if vehicleType >= 6:
                vehicleData[x]['Direction'] = 'Vertical'
                vehicleData[x]['coordY'] = start % 6
                if vehicleType // 6 == 2 :
                    vehicleData[x]['Type'] = 3
                    vehicleData[x]['coordX'] = [start // 6, (start+6) // 6, end // 6]
                    vehicleData[x]['Position'] = [start, start + 6, end] 
                else :
                    vehicleData[x]['Type'] = 2
                    vehicleData[x]['coordX'] = [start // 6, end // 6]
                    vehicleData[x]['Position'] = [start, end] 
            else :
                vehicleData[x]['Direction'] = 'Horizontal'
                vehicleData[x]['coordX'] = start // 6
                if vehicleType == 2 :
                    vehicleData[x]['Type'] = 3
                    vehicleData[x]['coordY'] = [start % 6, start % 6 + 1 , end % 6]
                    vehicleData[x]['Position'] = [start, start + 1, end] 
                else :
                    vehicleData[x]['Type'] = 2
                    vehicleData[x]['coordY'] = [start % 6, end % 6]
                    vehicleData[x]['Position'] = [start, end]

    return vehicleData

# Find the possible movements of vehicle
def moveData(coord, move, x, state, vehicleData) :
    negative = 0
    positive = 0
    if vehicleData[x][coord][0] > 0 : # Vehicle moves upwards or to the left
        moveN = move
        back = vehicleData[x]['Position'][0]
        edge = vehicleData[x][coord][0]
        while edge > 0 :
            if state[back - moveN] == '.' : 
                negative += 1
                moveN += move
                edge -= 1
            else : break        
    if vehicleData[x][coord][-1] < 5 : # Vehicle moves downwards or to the right
        moveP = move
        front = vehicleData[x]['Position'][-1]
        edge = vehicleData[x][coord][-1]
        while edge < 5 :
            if state[front + moveP] == '.' :
                positive += 1
                moveP += move
                edge += 1
            else : break

    return negative, positive

# Collect the possible movements of vehicles in a state depending on its orientation
# Store all movements as string types in a list
def collectMoveData(state, stateStr) :
    data = collectData(stateStr)
    nextStates = []
    for x in data :
        if data[x]['Direction'] == 'Horizontal' : # If horizontal vehicle, only move to right or left
            result = moveData('coordY', 1, x, state, data)
            for i in range(result[0]) :
                nextStates.append(x + 'L' + str(i+1))
            for i in range(result[1]) :
                nextStates.append(x + 'R' + str(i+1))
        else : # If vertical vehicle, only move downwards or upwards
            result = moveData('coordX', 6, x, state, data)
            for i in range(result[0]) :
                nextStates.append(x + 'U' + str(i+1))
            for i in range(result[1]) :
                nextStates.append(x + 'D' + str(i+1))

    return nextStates
    
# Move vehicle and generate new states
# Store and return new states in a list
def moveVehicle(parentState, parentStr, posAction) :
    childrenState = []
    childrenStr = []
    childData = collectData(parentStr)
    for action in posAction :
        i = action[0]
        childState = parentState.copy()
        if action[1] == 'L' or action[1] == 'U' : # If vehicle moves upwards or to the left
            if action[1] == 'L' : move = 1 # Left
            else : move = 6 # Up
            for n in range(childData[i]['Type']) :
                childState[childData[i]['Position'][n]] = '.'
                childState[childData[i]['Position'][n] - (move * int(action[2]))] = i
        else: # If vehicle moves downwards or to the right
            if action[1] == 'R' : move = 1 # Right
            else : move = 6 # Down
            for n in range(childData[i]['Type'], 0, -1) :
                childState[childData[i]['Position'][n - 1]] = '.'
                childState[childData[i]['Position'][n - 1] + (move * int(action[2]))] = i
        childStr = ""
        for c in childState : childStr += str(c)
        childrenState.append(childState)
        childrenStr.append(childStr)

    return childrenState, childrenStr

# Determine if reach goal state
def goalState(state) :
    if state[16] == 'X' and state[17] == 'X' : return True

# Breadth-First Search #CHANGE
def bfs(i) :
    startTime = time.time()
    # Generate root node
    node = Node(state = initialState[i], stateStr = initialStateStr[i], nextSts = collectMoveData(initialState[i], initialStateStr[i]), parent = None, action = [])
    if goalState(node.state) : return node.action, 1
    q = deque() # Store unexplored nodes
    q.append(node)
    qSet = set((node.stateStr))
    explored = set() # Store explored nodes

    while q : # q is not empty
        if time.time() - startTime > 5400 : return "Fail search", len(explored)  # Exceed time limit        
        node = q.popleft()
        qSetStr = node.stateStr
        qSet.discard(qSetStr)
        # Expand node : Generate new states and create children from node(parent)
        states, statesStr = moveVehicle(node.state, node.stateStr, node.nextSts)
        explored.add(node.stateStr)
        for j in range(len(states)) :
            if node.action and node.action[-1][0] == node.nextSts[j][0] : 
                continue # Avoid moving vehicle that has already been moved in previous action
            child = createChild(node, j, states[j], statesStr[j])
            # If child is unexplored
            if child.stateStr not in explored or child.stateStr not in qSet :
                if goalState(child.state) : return child.action, len(explored) # Check if child reaches goal state
                q.append(child) # If not, store child node into q(explored)
                qSet.add(child.stateStr)  
    else : return "Fail search", len(explored)

# Iterative Deepening
def iterDeep(i) :
    startTime = time.time()
    # Generate root node
    node = Node(state = initialState[i], stateStr = initialStateStr[i], nextSts = collectMoveData(initialState[i], initialStateStr[i]), parent = None, action = [])
    depth = 0

    while depth >= 0 :
        frontier = set() # Store explored nodes
        result, cutOff = dls(node, depth, frontier, startTime) # Carry out depth-limited search
        depth += 1 # Increment depth limit
        if type(result) is list : return result, len(frontier)
        elif not cutOff : return "Fail Search", len(frontier)

# Depth-Limited Search
def dls(node, depth, frontier, exeTime) :
    frontier.add((depth, node.stateStr))
    if time.time() - exeTime > 5400 : return 0, False # Exceed time limit
    if depth == 0 : # If reach depth limit, check if goal state achieved
        if goalState(node.state) : return node.action, True
        else : return 0, True
    else :
        cutOff = False
        # Expand node : Generate new states and create children from node(parent)
        states, statesStr = moveVehicle(node.state, node.stateStr, node.nextSts)
        for i in range(len(states)) :
            if (depth, statesStr[i]) not in frontier:
                if node.action and node.action[-1][0] == node.nextSts[i][0] : 
                    continue # Avoid moving vehicle that has already been moved in previous action
                child = createChild(node, i, states[i], statesStr[i])
                result, cut_off = dls(child, depth - 1, frontier, exeTime) # Recursion
                if type(result) is list : return result, True
                if cut_off : cutOff = True
        return 0, cutOff

# Heuristic Function - Return h(n)
# Check if any vertical vehicle(A) is blocking car X's path
# Check if any horizontal vehicle(B) is blocking the truck in (A)
def heuristic(node) :
    h = 1 # Car X must be moved at least one time
    data = collectData(node.stateStr)
    yCarX = data['X']['coordY'][1]
    moveHoriz = False
    blockHoriz = set()
    carMove = []

    # Check if any vertical vehicle(A) is blocking car X's path
    for i in data :
        if data[i]['Direction'] == 'Vertical' and data[i]['coordY'] > yCarX :
            if data[i]['Type'] == 3 and 5 not in data[i]['coordX']: # Truck is blocking car X
                moveHoriz = True
                blockHoriz.add(data[i]['coordY'])
                carMove.append(i)
                h += 1
            elif 2 in data[i]['coordX'] : h += 1
    # Check if any horizontal vehicle is blocking trucks in (A)
    if moveHoriz :
        for i in data :
            if data[i]['Direction'] == 'Horizontal' and data[i]['coordX'] > 2 and not blockHoriz.isdisjoint(set(data[i]['coordY'])): 
                h += 1    
       
    if goalState(node.state) : h = 0 # If goal state reached, h(n) = 0
    return h

# A* Graph Search        
def aStar(i) :
    startTime = time.time()
    openList = []
    openState = []
    closedList = []
    closedState = []
    # Generate root node
    start = Node(state = initialState[i], stateStr = initialStateStr[i], nextSts = collectMoveData(initialState[i], initialStateStr[i]), parent = None, action = [])
    start.f = heuristic(start)
    openList.append(start)
    openState.append(start.stateStr)

    while openList : # openList is not empty
        if time.time() - startTime > 5400 : return "Fail search", len(closedState) # Exceed time limit
        current = openList[0]
        currentInd = 0
        for index, item in enumerate(openList) : # Find node with lowest f-value and make it the current node
            if item.f < current.f :
                currentInd= index
                current = item
        # Pop current node off openList and add it to closedList
        openList.pop(currentInd)
        openState.pop(currentInd)
        closedList.append(current)
        closedState.append(current.stateStr)
        if goalState(current.state) : return current.action, len(closedState) # Check if current node achieves goal state

        # Expand node : Generate new states and create children from node(parent)
        states, statesStr = moveVehicle(current.state, current.stateStr, current.nextSts)
        for i in range(len(states)) :
            if current.action and current.action[-1][0] == current.nextSts[i][0] : 
                continue # Avoid moving vehicle that has already been moved in previous action
            child = createChild(current, i, states[i], statesStr[i])
            
            # Find child's f-value
            child.g = len(child.action)
            child.f = child.g + heuristic(child)

            if child.stateStr in closedState : continue 
            
            skip = False
            for openNode in openList : # Child is already in openList
                if child.state == openNode.state and child.g > openNode.g : 
                    skip = True
                    break
            if skip : continue
            openList.append(child) # Add child into openList
            openState.append(child.stateStr)

    else : return "Fail search", len(closedState)

# Hill Climbing Search (Greedy search and randomized search are combined in the algorithm)
def hillClimb(start, exeTime) :
    search = 1 # Root node is explored
    if goalState(start.state) : return start, search, heuristic(start)
    else : current = start # If not goal state, make start node as current node

    sidewayLimit = 0
    while sidewayLimit <= 100 : # Set sideway limit
        if time.time() - exeTime > 5400 : return best, totalExplored, bestH # Exceed time limit
        search += 1
        currentF = heuristic(current) # Find h-value of current node
        if goalState(current.state) : return current, search, heuristic(current) # If h-value = 0, goal state achieved
        
        # Expand node : Generate new states and create children from node(parent)
        states, statesStr = moveVehicle(current.state, current.stateStr, current.nextSts)
        neighbours = [] # Create neighbourhood
        neighboursF = []
        for i in range(len(states)) :
            if current.action and current.action[-1][0] == current.nextSts[i][0] : 
                continue # Avoid moving vehicle that has already been moved in previous action
            child = createChild(current, i, states[i], statesStr[i])
            neighbours.append(child) # Add child into neighbourhood
            neighboursF.append(heuristic(child))
        
        if len(neighboursF) == 0 : break # If no neighbours found, break loop

        # Determine next best neighbour
        if min(neighboursF) < currentF : # If best neighbour found, make it as current node
            current = neighbours[neighboursF.index(min(neighboursF))]
        elif min(neighboursF) == currentF : # If best neighbour has the same h-value as current node, carry out sideway search
            sideway = []
            for k in range(len(neighboursF)) :
                if neighboursF[k] == currentF : sideway.append(k)
            ind = random.choice(sideway) # Randomized sideway search
            current = neighbours[ind]
            sidewayLimit += 1
        else : break # If all neighbours have greater h-value, break loop
    return current, search, heuristic(current) # Return local point

# Random Restart Hill Climbing
def randomRestart(i) :
    startTime = time.time()
    # Generate root node
    root = Node(state = initialState[i], stateStr = initialStateStr[i], nextSts = collectMoveData(initialState[i], initialStateStr[i]), parent = None, action = [])
    randomInitStates = []
    best = root
    bestH = heuristic(best)
    totalExplored = 0
    
    # Generate initial states
    states, statesStr = moveVehicle(root.state, root.stateStr, root.nextSts)
    for i in range(len(states)) : randomInitStates.append(createChild(root, i, states[i], statesStr[i]))

    # Random restart is limited to 10 times
    for x in range(10) :
        result, explored, hValue = hillClimb(random.choice(randomInitStates), startTime) # Carry out hill climbing
        totalExplored += explored
        if goalState(result.state) : return result, totalExplored, 0 # Check if goal state is returned
        elif hValue < bestH : # If better state is returned, make it the current best state
            bestH = hValue
            best = result
    else : return best, totalExplored, bestH # Return local/actual solution

# Print solutions to output text file and also print output data on screen
def writeFile(outFile, i, sol, search, typeSearch, time, stateStr = "", bestH = 0) :
    # Print on screen
    print(typeSearch) 
    if typeSearch != "Hill Climb" :
        print("Solution Found:", end = " ")
        if type(sol) is not str :
            for s in sol : print(s, end = " ")
            diff = abs(len(givenSol[i]) - len(sol))
            print("\nCPU Time:", round(time, 2), "Path Cost:", len(sol), "Diff:", diff, "Explored:", search)
        else : 
            print("FAIL SEARCH. No solution is found within time limit")
    else :
        if bestH == 0 : 
            print("Local solution is found.")
            print("Solution Found:", end = " ")
            if type(sol) is not str :
                for s in sol : print(s, end = " ")
            print("\nCPU Time:", round(time, 2), "Path Cost:", len(sol), "Explored:", search)
            print("Final State Board:")
            printBoard(stateStr)
        else :
            print("FAIL SEARCH. No solution is found within time limit.")

    # Print to file
    outFile.write(typeSearch + ": ")
    if type(sol) is not str :
        for i in range(len(sol)) :
            outFile.write(sol[i])
            if (i + 1) % 15 == 0 : outFile.write("\n\t\t\t")
            else : outFile.write(" ")
    else : outFile.write("FAIL SEARCH")
    if typeSearch == "Hill Climb" : outFile.write("\n\n")
    else : outFile.write("\n")

#Main Program
#Read file
outFile = open("output.txt", "w")
outFile.write("==Solutions Found for Rush Hour Game==\n\n")
with open("rh.txt", "r") as f :
    for line in f :
        if "--- RH-input ---" in line : #Read initial states
            l = next(f).strip('\n')
            while l != "--- end RH-input ---" :
                initialStateStr.append(l)
                initialState.append(list(l))
                l = next(f).strip('\n')
        elif "Sol" in line : #Read given solutions
            sol = line
            li = next(f).strip('\n')
            while True : 
                if "Problem" in li : break
                sol += li
                if "." in li : break 
                li = next(f)       
            givenSol.append(sol.split())
f.close()

for x in givenSol :
    x.pop(0)
    x.pop()

#Print board (initial state)
for x in range(len(initialStateStr)) :
    outFile.write("Problem" + str(x + 1) + ":\n")
    print("Problem", end = " ")
    if x < 10 :
        print(x + 1, "(Beginner)")
    elif x < 20 :
        print(x + 1, "(Intermediate)")
    elif x < 30 :
        print(x + 1, "(Advanced)")
    else :
        print(x + 1, "(Expert)")
    print("Initial State:", initialStateStr[x])
    printBoard(initialStateStr[x]) 
    print("Given Solution:", end = " ")
    for y in givenSol[x] : print(y, end = " ")
    print()
    
    # Breadth-First Search
    bfsTime = time.time()
    bfsSol, bfsExplored = bfs(x)
    bfsCpuTime = time.time() - bfsTime
    writeFile(outFile, x, bfsSol, bfsExplored, "BFS", bfsCpuTime)

    # Iterative Deepening Depth-Limited Search
    idsTime = time.time()
    idsSol, idsExplored = iterDeep(x)
    idsCpuTime = time.time() - idsTime
    writeFile(outFile, x, idsSol, idsExplored, "IDDLS", idsCpuTime)

    # A* Graph Search
    aTime = time.time()
    aSol, aExplored = aStar(x)
    aCpuTime = time.time() - aTime
    writeFile(outFile, x, aSol, aExplored, "A*", aCpuTime)

    # Hill Climbing Search (Greedy + Random Restart)
    hillTime = time.time()
    hillSol, hillExplored, bestH = randomRestart(x)
    hillCpuTime = time.time() - hillTime
    writeFile(outFile, x, hillSol.action, hillExplored, "Hill Climb", hillCpuTime, hillSol.stateStr, bestH)
    print()

outFile.close()


        
