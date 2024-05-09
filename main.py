import numpy
from treelib import Node, Tree
import copy
import heapq
import time

# the flander's wheel is isomorphic to the sliding 8 puzzle!
# this array represents where the top of the wheel is the top right
goal_state = [['R', 'S', 'F'], 
              ['E', '-', 'L'], 
              ['D', 'N', 'A']]

goal_coords = {'R': (0, 0), 'S': (0, 1), 'F': (0, 2),
               'E': (1, 0), '-': (1, 1), 'L': (1, 2),
               'D': (2, 0), 'N': (2, 1), 'A': (2, 2)}

class Wheel:
    def __init__(self, state: list[list[int]]):
        self.state = state
        self.children = []
        self.depth = 0
        self.heuristic = 0
        self.cost = 0
        self.tree_id = 0
    def __lt__(self, other):
        return self.cost < other.cost

starting_state = Wheel([['L', 'A', 'N'], 
                        ['F', '-', 'D'], 
                        ['S', 'R', 'E']])

def print_state(state):
    for i in range(3):
        print(state[i])
    print()

def print_wheel(state): # just to show how state is isomorphic
    print('   / '+state[0][2]+' \   ')
    print('  '+state[0][1]+'      '+state[0][1])
    print(' /  \  /  \\')

# returns array position of the blank circle in the wheel
def find_blank(curr_state):
    for i in range(3):
        for j in range(3):
            if curr_state[i][j] == '-':
                return i, j
        
def up(state): # coordinates of blank circle
    row, col = find_blank(state)
    if (row-1) < 0:
        return # move not possible
    new_state = copy.deepcopy(state)
    above = state[row-1][col]
    new_state[row][col] = above
    new_state[row-1][col] = '-'
    return new_state

def down(state):
    row, col = find_blank(state)
    if (row+1) > 2:
        return # move not possible
    new_state = copy.deepcopy(state)
    down = state[row+1][col]
    new_state[row][col] = down
    new_state[row+1][col] = '-'
    return new_state

def left(state):
    row, col = find_blank(state)
    if (col-1) < 0:
        return # move not possible
    new_state = copy.deepcopy(state)
    left = state[row][col-1]
    new_state[row][col] = left
    new_state[row][col-1] = '-'
    return new_state

def right(state):
    row, col = find_blank(state)
    if (col+1) > 2:
        return # move not possible
    new_state = copy.deepcopy(state)
    right = state[row][col+1]
    new_state[row][col] = right
    new_state[row][col+1] = '-'
    return new_state

def expand_state(wheel: Wheel, tree: Tree, curr_tree_id):
    state = wheel.state # 
    children = [] # we will append all the expanded nodes here
    moves = [] # make a list of all moves here
    moves.append(up(state))
    moves.append(down(state))
    moves.append(left(state))
    moves.append(right(state))
    for move in moves: # for each move
        if move:
            temp = Wheel(copy.deepcopy(move))
            curr_tree_id += 1
            temp.tree_id = curr_tree_id
            children.append(temp)
    for c in children:
        tree.create_node(c.state, c.tree_id, parent=wheel.tree_id)
        c.depth = wheel.depth +1
    wheel.children = children
    return children, curr_tree_id # children = a list of wheel objects

def manhattan_distance(state):
    distance_sum = 0
    for i in range(3):
        for j in range(3):
            goal = goal_state[i][j]
            curr = state[i][j]
            if curr != '-': # we don't want to include the blank's distance
                dist = abs(i - goal_coords[curr][0]) + abs(j - goal_coords[curr][1])
                distance_sum += dist
    return distance_sum

def queuing(heuristic, states, children, depth, expanded):
    for child in children: # for each child in children
        if str(child.state) not in expanded: # if it hasn't already been expanded
            if heuristic == 3: # depending on which heuristic we use
                gx = manhattan_distance(child.state) # calculate the g(x)
                child.heuristic = gx # set it in the child
            cost = depth + gx # calculate the cost, which is depth + g(x)
            child.cost = cost # set the cost in the child
            heapq.heappush(states, (cost, child)) # push that child onto the heap with the cost
            # so that it will be ordered in the heap by cost and can be dequeued in order
    return states # return the states

def general_search(heuristic, starting_state, tree_id):
    states = []
    expanded = set() # using a set so nothing can be repeated
    heapq.heapify(states)
    tree = Tree()
    tree_id += 1

    if heuristic == 3:
        starting_state.heuristic = manhattan_distance(starting_state.state)

    starting_state.cost = starting_state.heuristic
    starting_state.tree_id = tree_id
    tree.create_node(starting_state.state, tree_id)
    heapq.heappush(states, (starting_state.cost, starting_state))
    q_size = 0
    expanded_count = 0

    while len(states) > 0:
        q_size = max(len(states), q_size)
        curr = heapq.heappop(states)
        curr_state = copy.deepcopy(curr[1]) # bc the heap is tuples of (cost, wheel)

        print('Best state to expand with g(x): ', curr_state.depth, ' and h(x): ', curr_state.heuristic)
        print_state(curr_state.state)

        if numpy.array_equal(curr_state.state, goal_state): # wheel has been solved!
            print('Flanders Wheel has been solved!')
            print('Number of nodes expanded: ', expanded_count)
            print('Max queue size: ', q_size)
            print('Depth of solution is: ', curr_state.depth)
            return curr_state.state
        else:
            if str(curr_state.state) not in expanded:
                expanded.add(str(curr_state.state))
                expand = expand_state(curr_state, tree, tree_id)
                expanded_count += 1
                states = queuing(heuristic, states, curr_state.children, curr_state.depth, expanded)
                tree_id += expand[1]
    
    if len(states) == 0:
        print('There is no solution to this problem!')

    return tree

test = Wheel([['S', 'F', 'L'], 
              ['R', '-', 'E'], 
              ['D', 'N', 'A']])
print('Solving the Flanders Wheel puzzle!')
start = time.time()
tree = general_search(3, test, 0)
end = time.time()
elapsed = end - start
print('Time elapsed:', round(elapsed, 1))
print(tree)