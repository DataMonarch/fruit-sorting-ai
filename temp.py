from queue import PriorityQueue
from typing import Tuple
import numpy as np
from copy import deepcopy

class FruitStack:
    # Class to represent the stack of fruits
    # initialize the object with the given fruits and the shape of the stack
    def __init__(self, fruits, shape: Tuple[int, int]=(3, 10)):
        self.fruits = fruits
        self.rows, self.cols = shape
        # board will be initialized as a matrix with shape (shape) and each element will be a Fruit object
        self.board = [[Fruit(np.random.choice(fruits), np.random.randint(1, self.cols+1)) for _ in range(self.cols)] for _ in range(self.rows)]
        self.board = np.array(self.board)

    def is_sorted(self):
        # Check if the board is sorted
        for i in range(self.cols):
            for j in range(1, self.rows):
                if self.board[j][i].size < self.board[j-1][i].size:
                    return False
        return True

    def print_board(self):
        # print the board
        for row in self.board:
            for i, fruit in enumerate(row):
                if i == len(row) - 1:
                    print(fruit)
                else:
                    print(fruit, end=" | ")
            print("-" * (8 * self.cols - 2))

    def find_fruit(self, fruit):
        # Helper function to find the position of a fruit in a state
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] == fruit:
                    return (i, j)
        return None
    
class Fruit:
    # Class to represent a fruit
    def __init__(self, type, size):
        self.type = type
        self.size = size

    def __str__(self):
        return f"{self.type}: {self.size:02d}"

    def __repr__(self):
        return f"{self.type}: {self.size:02d}"
    
class Node:
    # Class to represent a node in the search tree
    def __init__(self, f, g, fruit_stack: FruitStack, path) -> None:
        self.f = f
        self.g = g
        self.stack = fruit_stack
        self.path = path
        
    def __lt__(self, other):
        return self.f < other.f
    
    def __eq__(self, other):
        return self.stack == other.stack
    
    def __hash__(self):
        return hash(self.stack)
    

def heuristic(fruit_stack: FruitStack):
    # Heuristic function for the A* algorithm
    # The heuristic is the sum of all the misplaced fruits
    state = fruit_stack.board
    h = 0
    for i in range(fruit_stack.rows):
        for j in range(1, fruit_stack.cols):
            if state[i][j].size < state[i][j-1].size:
                h += 1
    return h

def get_successors(fruit_stack: FruitStack):
# Generate the successors of a state
    state = fruit_stack.board
    successors = []
    for i in range(fruit_stack.rows):
        for j in range(fruit_stack.cols):
            new_stack = deepcopy(fruit_stack)
            new_state = new_stack.board
            
            if i > 0:
                # Swap with fruit above
                new_state[i][j], new_state[i-1][j] = new_state[i-1][j], new_state[i][j]
                
            if i < fruit_stack.rows - 1:
            # Swap with fruit below
                new_state[i][j], new_state[i+1][j] = new_state[i+1][j], new_state[i][j]
                
            if j > 0:
                # Swap with fruit to the left
                new_state[i][j], new_state[i][j-1] = new_state[i][j-1], new_state[i][j]
                
            if j < fruit_stack.cols - 1:
                # Swap with fruit to the right
                new_state[i][j], new_state[i][j+1] = new_state[i][j+1], new_state[i][j]
                
            new_stack.board = new_state
            successors.append(new_stack)
    return successors

def solve(fruit_stack: FruitStack):
# Initialize open and closed lists
    open_list = PriorityQueue()
    closed_list = set()
    # Add start state to open list with initial cost of 0
    initial_stack = fruit_stack
    start_node = Node(0, 0, initial_stack, [])
    open_list.put(start_node)

    state_no = 0
    while not open_list.empty():
        # Get the node with the lowest f value from the open list
        curr_node = open_list.get()
        print(f">>> Current state: {state_no}")
        # curr_node.stack.print_board()
                
        # Check if current state is the goal state
        if curr_node.stack.is_sorted():
            print("Goal state found!")
            print(f"Path: {curr_node.path}")
            
            return curr_node.path

        # Add current node to closed list
        state_tuple = tuple(tuple(row) for row in curr_node.stack.board)
        closed_list.add(state_tuple)

        # Generate successors and add them to the open list
        for successor in get_successors(curr_node.stack):
            successor_tuple = tuple(tuple(row) for row in successor.board)
            if successor_tuple not in closed_list:
                # Calculate cost of successor node
                new_g = curr_node.g + 1  # Cost of moving to successor is always 1
                new_h = heuristic(successor)
                new_f = new_g + new_h

                # Add successor to open list
                new_path = curr_node.path + [successor]
                new_node = Node(new_f, new_g, successor, new_path)
                open_list.put(new_node)
            else:
                print(f"State {state_no} already visited")
        
        state_no += 1
    # If goal state is not found, return None
    return None


fruit_stack = FruitStack(["a", "o", "b"])
solve(fruit_stack)
