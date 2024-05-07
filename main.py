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

starting_state = [['L', 'A', 'N'], 
                  ['F', '-', 'N'], 
                  ['S', 'R', 'E']]

class Wheel:
    def __init__(self, state):
        self.state = state
        self.children = []
        self.depth = 0
        self.heuristic = 0
        self.cost = 0
        self.tree_id = 0

# returns array position of the sergeant
def find_sergeant(curr_state):
    for i in range(len(curr_state)):
        if curr_state[i] == 1:
            return i

def move_forward(board, sp): #sp = sergeant position
    
