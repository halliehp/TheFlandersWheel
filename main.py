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

starting_state = [['L', 'A', 'N'], 
                  ['F', '-', 'N'], 
                  ['S', 'R', 'E']]

class Wheel:
    def __init__(self, state: list[list[int]]):
        self.state = state
        self.children = []
        self.depth = 0
        self.heuristic = 0
        self.cost = 0
        self.tree_id = 0

def print_puzzle(puzzle):
    for i in range(3):
        print(puzzle[i])
    print()

# returns array position of the blank circle in the wheel
def find_blank(curr_state):
    for i in range(3):
        for j in range(3):
            if curr_state[i][j] == '-':
                return i, j
        
def up(state): # coordinates of blank circle
    row, col = find_blank(state)
    if (row-1) < 0:
        return None # move not possible
    new_state = copy.deepcopy(state)
    above = state[row-1][col]
    new_state[row][col] = above
    new_state[row-1][col] = '-'
    return new_state

print_puzzle(starting_state)
print_puzzle(up(starting_state))
