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
    return [s, s, w, s, w, w, s, w]


def buildActions(node, parent):
    action = node[1]
    if action is None: return []
    return buildActions(parent[node], parent) + [action]


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
        print(node)
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
            return path[1:]  # From 1 because path[0] is StartNodeAction and it's None

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
        print(node)
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
            return path[1:]  # From 1 because path[0] is StartNodeAction and it's None

        if state not in visited_node:
            visited_node.add(state)

            for successor in problem.getSuccessors(state):
                successor_state = successor[0]

                if successor_state not in visited_node:
                    stack.push(successor)
                    parent[successor] = node

    return []


def uniformCostSearch(problem: SearchProblem):
    """ Search the node of the least total cost first. """

    # Tạo một hàng đợi ưu tiên để lưu trữ các nút cần khám phá
    priorityQueue = util.PriorityQueue()
    # Tạo một tập để lưu trữ các nút đã được khám phá
    visited = set()
    # Khởi tạo đường dẫn hiện tại và trạng thái hiện tại
    currentPath = []
    currentState = problem.getStartState()
    # Thêm nút bắt đầu vào hàng đợi ưu tiên
    priorityQueue.push((currentState, currentPath), 0)

    while not priorityQueue.isEmpty():
        # Lấy nút có tổng chi phí thấp nhất khỏi hàng đợi ưu tiên
        currentState, currentPath = priorityQueue.pop()
        # Nếu nút hiện tại là nút đích, trả về đường dẫn đến nút đó
        if problem.isGoalState(currentState):
            return currentPath
        # Đánh dấu nút hiện tại là đã được khám phá
        visited.add(currentState)

        # Tạo một danh sách chứa các trạng thái của các nút nằm trong hàng đợi ưu tiên
        frontierStates = []
        for i in priorityQueue.heap:
            frontierStates.append(i[2][0])

        # Duyệt qua tất cả các nút kế thừa của nút hiện tại
        for successor in problem.getSuccessors(currentState):
            # Tạo đường dẫn đến nút kế thừa mới
            successorPath = currentPath + [successor[1]]
            # Nếu nút kế thừa chưa được khám phá và chưa có trong hàng đợi ưu tiên
            if successor[0] not in visited and successor[0] not in frontierStates:
                # Thêm nút kế thừa vào hàng đợi ưu tiên
                priorityQueue.push((successor[0], successorPath), problem.getCostOfActions(successorPath))
            # Nếu nút kế thừa đã có trong hàng đợi ưu tiên
            else:
                # Tìm nút kế thừa trong hàng đợi ưu tiên
                for i in range(0, len(frontierStates)):
                    if successor[0] == frontierStates[i]:
                        # Lấy tổng chi phí của đường dẫn hiện tại đến nút kế thừa
                        storedCost = priorityQueue.heap[i][0]
                        # Lấy tổng chi phí của đường dẫn mới đến nút kế thừa
                        updatedCost = problem.getCostOfActions(successorPath)
                        # Nếu tổng chi phí của đường dẫn mới đến nút kế thừa nhỏ hơn tổng chi phí của đường dẫn hiện tại
                        if storedCost > updatedCost:
                            # Cập nhật tổng chi phí của nút kế thừa trong hàng đợi ưu tiên
                            priorityQueue.update((successor[0], successorPath), updatedCost)
    # Nếu không tìm thấy đường dẫn đến nút đích, trả về rỗng
    return []
def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
