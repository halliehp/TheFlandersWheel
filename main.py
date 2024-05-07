import numpy
from treelib import Node, Tree
import copy
import heapq
import time

# first 10 numbers is the trench
# last three numbers represent the recesses
goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 0, 0, 0]

# 0 represents an empty slot
input_state = [0, 2, 3, 4, 5, 6, 7, 8, 9, 1, 0, 0, 0]

# at every index the possible moves are move left or move right
# if there is an empty spot, besides index 3, 5, 7 where you can move
# up into 10, 11, 12
recess = {3: 10, 5: 11, 7: 12}

class Trench:
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
    
