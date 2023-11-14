# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    stack = util.Stack()
    parent = dict()
    visited_node = set()

    start_state = problem.getStartState()
    # namhh: The problem.getSuccessors() return (SuccessorsState, SuccessorsAction, SuccessorsCost) so I applied for start state
    start_node = (start_state, None, 0)
    stack.push(start_node)

    while not stack.isEmpty():
        node = stack.pop()
        # print(node)
        state = node[0]

        if problem.isGoalState(state):
            # namhh Build path
            node_action = node[1]
            path = []
            path.append(node[1])
            while node_action is not None:
                node_parent = parent[node]
                path.append(node_parent[1])
                node = node_parent
                node_action = node_parent[1]
            path.reverse()
            return path[1:] # From 1 because path[0] is StartNodeAction and it's None

        if state not in visited_node:
            visited_node.add(state)

            for successor in problem.getSuccessors(state):
                successor_state = successor[0]

                if successor_state not in visited_node:
                    stack.push(successor)
                    parent[successor] = node

    return []

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    # namhh: The BFS algorithm is just different with DFS at data structures for pending nodes :D. Just change to Queue instead of Stack
    stack = util.Queue()
    parent = dict()
    visited_node = set()

    start_state = problem.getStartState()
    # namhh: The problem.getSuccessors() return (SuccessorsState, SuccessorsAction, SuccessorsCost) so I applied for start state
    start_node = (start_state, None, 0)
    stack.push(start_node)

    while not stack.isEmpty():
        node = stack.pop()
        # print(node)
        state = node[0]

        if problem.isGoalState(state):
            # namhh Build path
            node_action = node[1]
            path = []
            path.append(node[1])
            while node_action is not None:
                node_parent = parent[node]
                path.append(node_parent[1])
                node = node_parent
                node_action = node_parent[1]
            path.reverse()
            return path[1:] # From 1 because path[0] is StartNodeAction and it's None

        if state not in visited_node:
            visited_node.add(state)

            for successor in problem.getSuccessors(state):
                successor_state = successor[0]

                if successor_state not in visited_node:
                    stack.push(successor)
                    parent[successor] = node

    return []

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    queue = util.PriorityQueue()
    parent = dict()
    visited_node = set()
    node_dict = dict() # namhh: For cost management

    start_state = problem.getStartState()
    # namhh: The problem.getSuccessors() return (SuccessorsState, SuccessorsAction, SuccessorsCost) so I applied for start state
    # namhh: In PriorityQueue, this Queue is interested in lowest priority number.
    queue.push(item = (start_state, None), priority=0)
    node_dict[start_state] = 0

    while not queue.isEmpty():
        node = queue.pop()
        # print(node)
        state = node[0]

        if problem.isGoalState(state):
            # return []
            # namhh Build path
            node_action = node[1]
            path = []
            path.append(node[1])
            while node_action is not None:
                node_parent = parent[node]
                path.append(node_parent[1])
                node = node_parent
                node_action = node_parent[1]
            path.reverse()
            return path[1:] # From 1 because path[0] is StartNodeAction and it's None

            
        if state not in visited_node:
            visited_node.add(state)

            for successor in problem.getSuccessors(state):
                successor_state = successor[0]
                successor_cost = successor[2]

                if successor_state not in visited_node:
                    # namhh: Update successor cost
                    real_cost = node_dict[state] + successor_cost
                    queue.push(item=successor[:2], priority=real_cost)
                    # real_current_cost = node.priority + successor_cost
                    # print(real_current_cost)
                    # queue.push(successor)
                    # parent[successor] = node
                    node_dict[successor_state] = real_cost
                    parent[successor[:2]] = node

    return []

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    queue = util.PriorityQueue()
    parent = dict()
    visited_node = set()
    node_dict = dict() # namhh: For cost management

    start_state = problem.getStartState()
    # namhh: The problem.getSuccessors() return (SuccessorsState, SuccessorsAction, SuccessorsCost) so I applied for start state
    # namhh: In PriorityQueue, this Queue is interested in lowest priority number.
    queue.push(item=(start_state, None), priority=0)
    node_dict[start_state] = 0

    while not queue.isEmpty():
        node = queue.pop()
        # print(node)
        state = node[0]

        if problem.isGoalState(state):
            # return []
            # namhh Build path
            node_action = node[1]
            path = []
            path.append(node[1])
            while node_action is not None:
                node_parent = parent[node]
                path.append(node_parent[1])
                node = node_parent
                node_action = node_parent[1]
            path.reverse()
            return path[1:] # From 1 because path[0] is StartNodeAction and it's None

            
        if state not in visited_node:
            visited_node.add(state)

            for successor in problem.getSuccessors(state):
                successor_state = successor[0]
                successor_cost = successor[2]

                if successor_state not in visited_node:
                    # namhh: Update successor cost
                    real_cost = node_dict[state] + successor_cost + heuristic(successor_state, problem)
                    # queue.push(item=successor[:2], priority=real_cost)
                    queue.update(successor[:2], real_cost)
                    # real_current_cost = node.priority + successor_cost
                    # print(real_current_cost)
                    # queue.push(successor)
                    # parent[successor] = node
                    node_dict[successor_state] = real_cost
                    parent[successor[:2]] = node

    return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
