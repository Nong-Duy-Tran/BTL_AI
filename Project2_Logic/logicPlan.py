# logicPlan.py
# ------------
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
In logicPlan.py, you will implement logic planning methods which are called by
Pacman agents (in logicAgents.py).
"""

from typing import Dict, List, Tuple, Callable, Generator, Any
import util
import sys
import logic
import game

from logic import conjoin, disjoin
from logic import PropSymbolExpr, Expr, to_cnf, pycoSAT, parseExpr, pl_true

import itertools
import copy
import logicAgents

pacman_str = 'P'
food_str = 'FOOD'
wall_str = 'WALL'
pacman_wall_str = pacman_str + wall_str
DIRECTIONS = ['North', 'South', 'East', 'West']
blocked_str_map = dict([(direction, (direction + "_blocked").upper()) for direction in DIRECTIONS])
geq_num_adj_wall_str_map = dict([(num, "GEQ_{}_adj_walls".format(num)) for num in range(1, 4)])
DIR_TO_DXDY_MAP = {'North':(0, 1), 'South':(0, -1), 'East':(1, 0), 'West':(-1, 0)}


#______________________________________________________________________________
# QUESTION 1

def sentence1() -> Expr:
    """Returns a Expr instance that encodes that the following expressions are all true.
    
    A or B
    (not A) if and only if ((not B) or C)
    (not A) or (not B) or C
    """
    "*** BEGIN YOUR CODE HERE ***"
    A = Expr('A')
    B = Expr('B')
    C = Expr('C')


    A_and_B = (A | B)
    notA_ifa_notB_or_C = ~A % (~B | C)
    notA_or_notB_C = disjoin([~A, ~B, C])
    return conjoin([A_and_B, notA_ifa_notB_or_C, notA_or_notB_C])
    


def sentence2() -> Expr:
    """Returns a Expr instance that encodes that the following expressions are all true.
    
    C if and only if (B or D)
    A implies ((not B) and (not D))
    (not (B and (not C))) implies A
    (not D) implies C
    """
    "*** BEGIN YOUR CODE HERE ***"
    A = Expr('A')
    B = Expr('B')
    C = Expr('C')
    D = Expr('D')
    
    return conjoin([C%(B|D), A>>((~B)&(~D)), (~(B & ~C)) >> A, ~D >> C])
    


def sentence3() -> Expr:
    """Using the symbols PacmanAlive_1 PacmanAlive_0, PacmanBorn_0, and PacmanKilled_0,
    created using the PropSymbolExpr constructor, return a PropSymbolExpr
    instance that encodes the following English sentences (in this order):

    Pacman is alive at time 1 if and only if Pacman was alive at time 0 and it was
    not killed at time 0 or it was not alive at time 0 and it was born at time 0.

    Pacman cannot both be alive at time 0 and be born at time 0.

    Pacman is born at time 0.
    """
    "*** BEGIN YOUR CODE HERE ***"
    PacmanAlive_1 = PropSymbolExpr('PacmanAlive', time = 1)
    PacmanAlive_0 = PropSymbolExpr('PacmanAlive', time = 0)
    PacmanBorn_0 = PropSymbolExpr('PacmanBorn', time = 0)
    PacmanKilled_0 = PropSymbolExpr('PacmanKilled', time = 0)

    return conjoin([PacmanAlive_1%((PacmanAlive_0 & (~PacmanKilled_0)) | (~PacmanAlive_0 & PacmanBorn_0)), ~(PacmanAlive_0 & PacmanBorn_0), PacmanBorn_0])


def findModel(sentence: Expr) -> Dict[Expr, bool]:
    """Given a propositional logic sentence (i.e. a Expr instance), returns a satisfying
    model if one exists. Otherwise, returns False.
    """
    cnf_sentence = to_cnf(sentence)
    return pycoSAT(cnf_sentence) 
    # Note không quên, bản chất là để kiểm tra xem có tồn tại bất kì giá trị nào thỏa mãn mệnh đề không
    # trả về giá trị dạng Dict nếu có, trả về False nếu không tồn tại

def findModelUnderstandingCheck() -> Dict[Expr, bool]:
    """Returns the result of findModel(Expr('a')) if lower cased expressions were allowed.
    You should not use findModel or Expr in this method.
    """
    a = Expr('A')
    "*** BEGIN YOUR CODE HERE ***"
    # print("a.__dict__ is:", a.__dict__) # might be helpful for getting ideas
    # util.raiseNotDefined()
    a.op = 'a'
    return {a: True}
    "*** END YOUR CODE HERE ***"

def entails(premise: Expr, conclusion: Expr) -> bool:
    """Returns True if the premise entails the conclusion and False otherwise.
    """
    "*** BEGIN YOUR CODE HERE ***"
    result = premise & ~conclusion
    
    if (findModel(result) == False):
        return True
    else:
        return False
    "*** END YOUR CODE HERE ***"

def plTrueInverse(assignments: Dict[Expr, bool], inverse_statement: Expr) -> bool:
    """Returns True if the (not inverse_statement) is True given assignments and False otherwise.
    pl_true may be useful here; see logic.py for its description.
    """
    "*** BEGIN YOUR CODE HERE ***"
    return pl_true(~inverse_statement, assignments)
    "*** END YOUR CODE HERE ***"

#______________________________________________________________________________
# QUESTION 2

def atLeastOne(literals: List[Expr]) -> Expr:
    """
    Given a list of Expr literals (i.e. in the form A or ~A), return a single 
    Expr instance in CNF (conjunctive normal form) that represents the logic 
    that at least one of the literals  ist is true.
    >>> A = PropSymbolExpr('A');
    >>> B = PropSymbolExpr('B');
    >>> symbols = [A, B]
    >>> atleast1 = atLeastOne(symbols)
    >>> model1 = {A:False, B:False}
    >>> print(pl_true(atleast1,model1))
    False
    >>> model2 = {A:False, B:True}
    >>> print(pl_true(atleast1,model2))
    True
    >>> model3 = {A:True, B:True}
    >>> print(pl_true(atleast1,model2))
    True
    """
    "*** BEGIN YOUR CODE HERE ***"
    return disjoin(literals)
    


def atMostOne(literals: List[Expr]) -> Expr:
    """
    Given a list of Expr literals, return a single Expr instance in 
    CNF (conjunctive normal form) that represents the logic that at most one of 
    the expressions in the list is true.
    itertools.combinations may be useful here.
    """
    "*** BEGIN YOUR CODE HERE ***"
    temp = []
    for i in range(len(literals)):
        for j in range(i + 1, len(literals)):
            temp.append(~literals[i] | ~literals[j])
            
    return conjoin(temp)
    "*** END YOUR CODE HERE ***"


def exactlyOne(literals: List[Expr]) -> Expr:
    """
    Given a list of Expr literals, return a single Expr instance in 
    CNF (conjunctive normal form)that represents the logic that exactly one of 
    the expressions in the list is true.
    """
    "*** BEGIN YOUR CODE HERE ***"
    return conjoin([atLeastOne(literals), atMostOne(literals)])
    "*** END YOUR CODE HERE ***"

#______________________________________________________________________________
# QUESTION 3

def pacmanSuccessorAxiomSingle(x: int, y: int, time: int, walls_grid: List[List[bool]]=None) -> Expr:
    """
    Successor state axiom for state (x,y,t) (from t-1), given the board (as a 
    grid representing the wall locations).
    Current <==> (previous position at time t-1) & (took action to move to x, y)
    Available actions are ['North', 'East', 'South', 'West']
    Note that STOP is not an available action.
    """

    '''
    Cách đánh tọa độ của của map
    NHẤN MẠNH LÀ CỦA TOÀN BỘ MAP
    y ^
      |
      |
      |
      |
      |
      |
      |
      |
      ---------------------->x
    '''
    now, last = time, time - 1
    possible_causes: List[Expr] = [] # enumerate all possible causes for P[x,y]_t
    # the if statements give a small performance boost and are required for q4 and q5 correctness
    
    if walls_grid[x][y+1] != 1: # Nếu không có tường ở vị trí (x, y+1)
        possible_causes.append( PropSymbolExpr(pacman_str, x, y+1, time=last)
                            & PropSymbolExpr('South', time=last)) 
        
        # PropSymbolExpr(pacman_str, x, y+1, time=last) là mệnh đề biểu thị vị trí của pacman lúc trước
        # PropSymbolExpr('South', time=last) là mệnh đề biểu thị pacman đang đi về hướng Nam
        # Nói cách khác, mệnh đề trên biểu thị pacman ở vị trí (x,y) tại thời điểm lúc trước và đang đi về hướng Nam

    if walls_grid[x][y-1] != 1:
        possible_causes.append( PropSymbolExpr(pacman_str, x, y-1, time=last) 
                            & PropSymbolExpr('North', time=last))
    if walls_grid[x+1][y] != 1:
        possible_causes.append( PropSymbolExpr(pacman_str, x+1, y, time=last) 
                            & PropSymbolExpr('West', time=last))
    if walls_grid[x-1][y] != 1:
        possible_causes.append( PropSymbolExpr(pacman_str, x-1, y, time=last) 
                            & PropSymbolExpr('East', time=last))
    if not possible_causes:
        return None
    
    "*** BEGIN YOUR CODE HERE ***"
    return PropSymbolExpr(pacman_str, x, y, time=now) % disjoin(possible_causes)
    # Trả về mệnh đề biểu thị pacman ở vị trí (x,y) thời điểm bây giờ khi và chỉ khi
    # pacman ở một trong các tọa độ trên từ trước và có hướng đi tương ứng
    "*** END YOUR CODE HERE ***"


def SLAMSuccessorAxiomSingle(x: int, y: int, time: int, walls_grid: List[List[bool]]) -> Expr:
    """
    Similar to `pacmanSuccessorStateAxioms` but accounts for illegal actions
    where the pacman might not move timestep to timestep.
    Available actions are ['North', 'East', 'South', 'West']
    """
    now, last = time, time - 1
    moved_causes: List[Expr] = [] # enumerate all possible causes for P[x,y]_t, assuming moved to having moved

    # Giống với giải thích phần trên
    if walls_grid[x][y+1] != 1:
        moved_causes.append( PropSymbolExpr(pacman_str, x, y+1, time=last)
                            & PropSymbolExpr('South', time=last))
    if walls_grid[x][y-1] != 1:
        moved_causes.append( PropSymbolExpr(pacman_str, x, y-1, time=last) 
                            & PropSymbolExpr('North', time=last))
    if walls_grid[x+1][y] != 1:
        moved_causes.append( PropSymbolExpr(pacman_str, x+1, y, time=last) 
                            & PropSymbolExpr('West', time=last))
    if walls_grid[x-1][y] != 1:
        moved_causes.append( PropSymbolExpr(pacman_str, x-1, y, time=last) 
                            & PropSymbolExpr('East', time=last))
    if not moved_causes:
        return None

    moved_causes_sent: Expr = conjoin([~PropSymbolExpr(pacman_str, x, y, time=last),
                                        ~PropSymbolExpr(wall_str, x, y),
                                        disjoin(moved_causes)])
    # Mệnh đề thể hiện rằng KHÔNG có pacman ở (x,y) tại thời điểm lúc trước
    # và KHÔNG có tường ở (x,y)
    # và pacman ở một trong các vị trí và hướng di chuyển tương ứng



    failed_move_causes: List[Expr] = [] # using merged variables, improves speed significantly
    auxilary_expression_definitions: List[Expr] = []
    for direction in DIRECTIONS:
        dx, dy = DIR_TO_DXDY_MAP[direction]

        wall_dir_clause = PropSymbolExpr(wall_str, x + dx, y + dy) & PropSymbolExpr(direction, time=last)
        wall_dir_combined_literal = PropSymbolExpr(wall_str + direction, x + dx, y + dy, time=last)
        # Mệnh đề trên biểu thị nếu có tường ở vị trí tương ứng nào đó trước mặt trong khoảng thời gian lúc trước


        failed_move_causes.append(wall_dir_combined_literal)
        # List này là tập hợp của tất cả các giả định của mệnh đề trên


        auxilary_expression_definitions.append(wall_dir_combined_literal % wall_dir_clause)

    failed_move_causes_sent: Expr = conjoin([
        PropSymbolExpr(pacman_str, x, y, time=last),
        disjoin(failed_move_causes)]) 
    # pacman ở vị trí (x,y) và một trong các hướng để đi tiếp lại có vật cản do có tường list trên tạo ra vật cản


    return conjoin([PropSymbolExpr(pacman_str, x, y, time=now)
                     % disjoin([moved_causes_sent, failed_move_causes_sent])] + auxilary_expression_definitions)
    # Mệnh đề thể hiện pacman ở vị trí (x,y) bây giờ
    # khi và chỉ khi pac man ở 
        # KHÔNG có pacman ở (x,y) tại thời điểm lúc trước
        # và KHÔNG có tường ở (x,y)
        # và pacman ở một trong các vị trí và hướng di chuyển tương ứng
    # hoặc có tường ở vị trí mà pacman đi đến
        

def pacphysicsAxioms(t: int, all_coords: List[Tuple], non_outer_wall_coords: List[Tuple], walls_grid: List[List] = None,
                    sensorModel: Callable = None, successorAxioms: Callable = None) -> Expr:
    """
    Given:
        t: timestep
        all_coords: list of (x, y) coordinates of the entire problem
        non_outer_wall_coords: list of (x, y) coordinates of the entire problem,
            excluding the outer border (these are the actual squares pacman can
            possibly be in)
        walls_grid: 2D array of either -1/0/1 or T/F. Used only for successorAxioms.
            Do NOT use this when making possible locations for pacman to be in.
        sensorModel(t, non_outer_wall_coords) -> Expr: function that generates
            the sensor model axioms. If None, it's not provided, so shouldn't be run.
        successorAxioms(t, walls_grid, non_outer_wall_coords) -> Expr: function that generates
            the sensor model axioms. If None, it's not provided, so shouldn't be run.
    Return a logic sentence containing all of the following:
        - for all (x, y) in all_coords:
            If a wall is at (x, y) --> Pacman is not at (x, y)
        - Pacman is at exactly one of the squares at timestep t.
        - Pacman takes exactly one action at timestep t.
        - Results of calling sensorModel(...), unless None.
        - Results of calling successorAxioms(...), describing how Pacman can end in various
            locations on this time step. Consider edge cases. Don't call if None.
    """
    pacphysics_sentences = []

    "*** BEGIN YOUR CODE HERE ***"
    # Tập hợp những suy luận
    # 1. Nếu tường ở đâu thì không có pacman
    posible_location = []
    for x, y in all_coords:
        pacphysics_sentences.append(PropSymbolExpr(wall_str,x,y) >> ~PropSymbolExpr(pacman_str,x,y,time=t))
        
        # 2. Xét vị trí nào pacman có thể, nhưng do pacma chỉ có thể ở 1 vị trí duy nhất nên ta dùng exactlyOne()
        if (x, y) in non_outer_wall_coords:
            posible_location.append(PropSymbolExpr(pacman_str, x,y,time = t))
    
    pacphysics_sentences.append(exactlyOne(posible_location))


    one_action_only = []

    for direction in DIRECTIONS:
        one_action_only.append(PropSymbolExpr(direction, time=t))
    pacphysics_sentences.append(exactlyOne(one_action_only))

    # 3. Tập hợp những mệnh đề tương đương mà có thể nhận được khi quan sát pacman di chuyển
    if sensorModel is not None:
        pacphysics_sentences.append(sensorModel(t, non_outer_wall_coords))
    
    # 4. Tập hợp những mệnh đề liên quan đến việc di chuyển của pacman
    # ví dụ, pacman ở vị trí (3,3) khi mà chi khi nó ở (3,2) và đang đi về Bắc lúc đó
    if successorAxioms is not None and t > 0: # Phải thêm t > 0 do cần kiểm tra tại thời điểm lúc trước
        pacphysics_sentences.append(successorAxioms(t, walls_grid, non_outer_wall_coords))

    "*** END YOUR CODE HERE ***"

    return conjoin(pacphysics_sentences)
    # Bản chất của hàm là trả về tổng hợp các suy luận được yêu cầu cho cả map chơi


def checkLocationSatisfiability(x1_y1: Tuple[int, int], x0_y0: Tuple[int, int], action0, action1, problem):
    """
    Given:
        - x1_y1 = (x1, y1), a potential location at time t = 1
        - x0_y0 = (x0, y0), Pacman's location at time t = 0
        - action0 = one of the four items in DIRECTIONS, Pacman's action at time t = 0
        - action1 = to ensure match with autograder solution
        - problem = an instance of logicAgents.LocMapProblem
    Note:
        - there's no sensorModel because we know everything about the world
        - the successorAxioms should be allLegalSuccessorAxioms where needed
    Return:
        - a model where Pacman is at (x1, y1) at time t = 1
        - a model where Pacman is not at (x1, y1) at time t = 1
    """
    walls_grid = problem.walls
    # Gán giá trị cho biến là tọa độ của tường, Lưu ý là nếu là 1 thì là tường
    # Đọc trong getWalls() của pacman.py

    walls_list = walls_grid.asList()
    # Có vẻ là chuyển thành dạng list

    all_coords = list(itertools.product(range(problem.getWidth()+2), range(problem.getHeight()+2))) 
    # Gán giá trị all_coords là tọa độ của toàn bộ sàn chơi TÍNH CẲ TƯỜNG
    # +2 do trong getWidth() va getHeight() bị trừ đi 2 đơn vị do không tính tường

    non_outer_wall_coords = list(itertools.product(range(1, problem.getWidth()+1), range(1, problem.getHeight()+1)))
    # Cái này thì là không tính tường nên bắt đầu từ 1 và chỉ +1 thôi
    KB = []
    x0, y0 = x0_y0
    x1, y1 = x1_y1

    # We know which coords are walls:
    map_sent = [PropSymbolExpr(wall_str, x, y) for x, y in walls_list]
    # Tạo mệnh đề cho tường của cả map chơi

    KB.append(conjoin(map_sent))

    "*** BEGIN YOUR CODE HERE ***"
    # 1.
    KB.append(pacphysicsAxioms(0, all_coords, non_outer_wall_coords, walls_grid, successorAxioms=allLegalSuccessorAxioms)) # Truyền vào hàm là do nó có dạng Callable
    KB.append(pacphysicsAxioms(1, all_coords, non_outer_wall_coords, walls_grid, successorAxioms=allLegalSuccessorAxioms))

    # 2.
    KB.append(PropSymbolExpr(pacman_str, x0, y0, time=0))

    # 3.
    KB.append(PropSymbolExpr(action0, time=0))
    KB.append(PropSymbolExpr(action1, time=1))


    check = PropSymbolExpr(pacman_str, x1, y1, time=1)
    # Do đề bài yêu cầu kiểm tra tại thời điểm time = 1 là thằng pacman có ở đấy không
    # nên đặt luôn tại đấy

    model1 = findModel(conjoin(KB) & check)
    model2 = findModel(conjoin(KB) & ~check)
    
    return model1, model2
    # Bản chất của hàm là trả về tập giá trị (model) dạng Dict cho những suy luận mà ta được yêu cầu
    "*** END YOUR CODE HERE ***"


#______________________________________________________________________________
# QUESTION 4

def positionLogicPlan(problem) -> List:
    """
    Given an instance of a PositionPlanningProblem, return a list of actions that lead to the goal.
    Available actions are ['North', 'East', 'South', 'West']
    Note that STOP is not an available action.
    Overview: add knowledge incrementally, and query for a model each timestep. Do NOT use pacphysicsAxioms.
    """
    walls_grid = problem.walls
    print(walls_grid)
    width, height = problem.getWidth(), problem.getHeight()
    walls_list = walls_grid.asList()
    
    # problem <- LocMapProblem (logicAgents.py) <- GameState (pacman.py)
    x0, y0 = problem.startState
    # Vị trí khởi tạo

    xg, yg = problem.goal
    # Vị trí đích
    
    # Get lists of possible locations (i.e. without walls) and possible actions
    all_coords = list(itertools.product(range(width + 2), 
            range(height + 2)))
    
    non_wall_coords = [loc for loc in all_coords if loc not in walls_list]
    # Các tọa độ không phải tường

    actions = [ 'North', 'South', 'East', 'West' ]
    KB = []

    "*** BEGIN YOUR CODE HERE ***"
    KB.append(logic.PropSymbolExpr(pacman_str,x0,y0,time= 0))

    for t in range(50):
        # 1.
        print("time step =", t)
        # 2.
        KB.append(exactlyOne([PropSymbolExpr(pacman_str, curr_loc[0], curr_loc[1], time = t) 
                              for curr_loc in non_wall_coords]))
        # Viết comprehension cho ngắn, đại ý là kiểm tra vị trí duy nhất của pacman tại thời điểm t

        # 3. 
        goal = PropSymbolExpr(pacman_str, xg, yg, time=t)
        model = findModel(goal & conjoin(KB))
        if (model):
            return extractActionSequence(model, actions)
        # Xét xem đến đích chưa, đến rồi thì trả về đường đi
        
        # 4.
        KB.append(exactlyOne([PropSymbolExpr(action, time = t) for action in actions]))
        # pacman chỉ có một hành động tại một thời điểm

        # 5.
        for curr_loc in non_wall_coords:
            KB.append(pacmanSuccessorAxiomSingle(curr_loc[0],curr_loc[1],t+1,walls_grid))
        # Méo hiểu sao không dùng được comprehension :))))
        # Đúng ra là xét hết suy luận của tất cả các vị trí mà pacman có thể ở trên bản đồ, vì nó xét trong time = t+1


    "*** END YOUR CODE HERE ***"

#______________________________________________________________________________
# QUESTION 5

def foodLogicPlan(problem) -> List:
    """
    Given an instance of a FoodPlanningProblem, return a list of actions that help Pacman
    eat all of the food.
    Available actions are ['North', 'East', 'South', 'West']
    Note that STOP is not an available action.
    Overview: add knowledge incrementally, and query for a model each timestep. Do NOT use pacphysicsAxioms.
    """
    walls_grid = problem.walls
    width, height = problem.getWidth(), problem.getHeight()
    walls_list = walls_grid.asList()
    (x0, y0), food = problem.start
    food_coords = food.asList()

    # Get lists of possible locations (i.e. without walls) and possible actions
    all_coords = list(itertools.product(range(width + 2), range(height + 2)))

    non_wall_coords = [loc for loc in all_coords if loc not in walls_list]
    actions = ['North', 'South', 'East', 'West']

    KB = []

    # Lưu ý là nó RẤT giống câu 4, chỉ thêm một vài tiêu chí khác

    "*** BEGIN YOUR CODE HERE ***"
    KB.append(PropSymbolExpr(pacman_str, x0, y0, time = 0))
    # Khởi tạo pacman
    for food_coord in food_coords:
        KB.append(PropSymbolExpr(food_str, food_coord[0], food_coord[1], time = 0))
    # Thêm vào KB tất cả thức ăn tại mọi thời điểm
    # Không dùng comprehension được là do nó sẽ trả về một generator
    
    for t in range(50):
         # 1.
        print("time step =", t)
        # 2.
        KB.append(exactlyOne([PropSymbolExpr(pacman_str, curr_loc[0], curr_loc[1], time = t) 
                              for curr_loc in non_wall_coords]))
        
        # 3.
        goal = [~PropSymbolExpr(food_str, food_coord[0], food_coord[1], time=t) for food_coord in food_coords]
        print(goal)
        # Mục tiêu phải là thức ăn phải được ăn hết, cho vào list để kiểm tra xem nó bị ăn chưa
        model = findModel(conjoin(KB + goal))
        # goal và KB đều là list, phải cộng vào
        if (model):
            return extractActionSequence(model, actions)
        
        # 4.
        KB.append(exactlyOne([PropSymbolExpr(action, time = t) for action in actions]))

        # 5.
        for curr_loc in non_wall_coords:
            KB.append(pacmanSuccessorAxiomSingle(curr_loc[0],curr_loc[1],t+1,walls_grid))
        
        # 6.
        for food_coord in food_coords:
            new_t_food = PropSymbolExpr(food_str, food_coord[0], food_coord[1], time = t+1)
            food_loc = PropSymbolExpr(food_str, food_coord[0], food_coord[1], time = t)
            pacman_loc = PropSymbolExpr(pacman_str, food_coord[0], food_coord[1], time = t)
            # Khởi tạo mệnh đề của Food[x,y]_t+1 and Food[x,y]_t and Pacman[x,y]_t

            get_food = pacman_loc & food_loc
            avoid_food = ~pacman_loc & food_loc
            # Mối quan hệ khá đơn giản và hiển nhiên, không giải thích

            # Đề bài yêu cầu nó giống như "transition model"
            # => có vẻ nó tạo suy luận giống như pacmanSuccessorAxiomSingle()

            # Ý tưởng: nếu ăn thằng này tại time = t thì sẽ không còn thằng này tại time = t+1,
            # do food có tọa độ giống hệt nhau và không được làm mới
            still_have_food = avoid_food >> new_t_food
            already_eat = get_food >> ~new_t_food
            KB.append(still_have_food)
            KB.append(already_eat)
        
    "*** END YOUR CODE HERE ***"

#______________________________________________________________________________
# QUESTION 6

def auxiliaryFunction1(KB : list, agent, t: int, all_coords: list, non_outer_wall_coords: list, walls_grid, sensor_mode, successorAxioms, question = 6):
    
    KB.append(pacphysicsAxioms(t, all_coords, non_outer_wall_coords, walls_grid, sensor_mode, successorAxioms))
    # Thêm vào KB tập các suy luận và mệnh đề trong pacphysicsAxioms

    KB.append(PropSymbolExpr(agent.actions[t], time=t))
    # Thêm vào hành động của pacman tại thời điểm t nhưng phải dùng agent.actions
    if question != 8:
        percept_rules = fourBitPerceptRules(t, agent.getPercepts())
        # Chuyển đổi nhận thức của pacman thành mệnh đề
        KB.append(percept_rules)
    
    else :
        KB.append(numAdjWallsPerceptRules(t, agent.getPercepts()))
    # Truyền mệnh đề nhận thức (percept) của pacman vào trong KB

    
def auxiliaryFunction2(possible_locations: list, non_outer_wall_coords, KB: list, t: int):

    for x,y in non_outer_wall_coords:
        pacman_loc = PropSymbolExpr(pacman_str, x, y, time = t)
        # Tạo mệnh đề xét vị trí pacman

        cKB = conjoin(KB)
        # Tách tập các mệnh đề ra để kiểm tra xem pacman có ở vị trí (x,y) hay không 

        if (findModel(cKB & pacman_loc)):
            # print('1'*15)
            possible_locations.append((x, y))
            # Kiểm tra xem nếu bất kì vị trí nào pacman có thể ở đấy thì ta cho vào list possible_locations
        

        # Chứng minh là pacman có thể/không thể ở vị trí (x,y) tại thời điểm t
        elif (entails(cKB, pacman_loc)):
            # print('2'*15)
            KB.append(pacman_loc)

        else:
            # print('3'*15)
            KB.append(~pacman_loc)



def localization(problem, agent) -> Generator:
    '''
    problem: a LocalizationProblem instance
    agent: a LocalizationLogicAgent instance
    '''
    walls_grid = problem.walls
    print(walls_grid)
    walls_list = walls_grid.asList()
    all_coords = list(itertools.product(range(problem.getWidth()+2), range(problem.getHeight()+2)))
    non_outer_wall_coords = list(itertools.product(range(1, problem.getWidth()+1), range(1, problem.getHeight()+1)))

    KB = []
    
    "*** BEGIN YOUR CODE HERE ***"
    # 1.
    for coord in all_coords:
        if coord in walls_list:
            KB.append(PropSymbolExpr(wall_str, coord[0], coord[1]))
            continue

        KB.append(~PropSymbolExpr(wall_str, coord[0], coord[1]))
    # Cho vào KB mệnh đề của cả map mô tả chỗ nào là tường, chỗ nào không
    
    for t in range(agent.num_timesteps):
        possible_locations = []
        auxiliaryFunction1(KB, agent, t, all_coords, non_outer_wall_coords, walls_grid, sensorAxioms, allLegalSuccessorAxioms)
    
        auxiliaryFunction2(possible_locations, non_outer_wall_coords, KB, t)

        agent.moveToNextState(agent.actions[t])
        "*** END YOUR CODE HERE ***"
        yield possible_locations


#______________________________________________________________________________
# QUESTION 7

def auxiliaryFunction3(non_outer_wall_coords: list, KB: list, known_map, t):
    for x, y in non_outer_wall_coords:
        wall_loc = PropSymbolExpr(wall_str, x, y)
        cKB = conjoin(KB)

        if (entails(cKB, wall_loc)):
            known_map[x][y] = 1
            KB.append(wall_loc)
        # Nếu là tường thì update known_map

        elif(entails(cKB, ~wall_loc)):
            known_map[x][y] = 0
            KB.append(~wall_loc)
        # Không thì update không phải

        else:
            known_map[x][y] = -1
        # Không biết thì để tí tính sau



def mapping(problem, agent) -> Generator:
    '''
    problem: a MappingProblem instance
    agent: a MappingLogicAgent instance
    '''
    pac_x_0, pac_y_0 = problem.startState
    KB = []
    all_coords = list(itertools.product(range(problem.getWidth()+2), range(problem.getHeight()+2)))
    non_outer_wall_coords = list(itertools.product(range(1, problem.getWidth()+1), range(1, problem.getHeight()+1)))

    # map describes what we know, for GUI rendering purposes. -1 is unknown, 0 is open, 1 is wall
    known_map = [[-1 for y in range(problem.getHeight()+2)] for x in range(problem.getWidth()+2)]

    # Pacman knows that the outer border of squares are all walls
    outer_wall_sent = []
    for x, y in all_coords:
        if ((x == 0 or x == problem.getWidth() + 1)
                or (y == 0 or y == problem.getHeight() + 1)):
            known_map[x][y] = 1
            outer_wall_sent.append(PropSymbolExpr(wall_str, x, y))

    KB.append(conjoin(outer_wall_sent))
    # RẤT GIỐNG CÂU 6, CHẤP THẦY HỎI
    print(known_map)
    "*** BEGIN YOUR CODE HERE ***"
    KB.append(PropSymbolExpr(pacman_str, pac_x_0, pac_y_0, time=0))
    # Khởi tạo pacman


    if (known_map[pac_x_0][pac_y_0] == 1):
        KB.append(PropSymbolExpr(wall_str, pac_x_0, pac_y_0))
    else:
        KB.append(~PropSymbolExpr(wall_str, pac_x_0, pac_y_0))
    # Kiểm tra vị pacman đứng ban đầu có phải tường hay không
    # Xong thêm mệnh đề vào KB

    for t in range(agent.num_timesteps):
        "*** END YOUR CODE HERE ***"
        auxiliaryFunction1(KB, agent, t, all_coords, non_outer_wall_coords, known_map, sensorAxioms, allLegalSuccessorAxioms)
        # Tương tự câu 6

        auxiliaryFunction3(non_outer_wall_coords, KB, known_map, t)
        # Update Known_map và KB

        agent.moveToNextState(agent.actions[t])
        yield known_map

#______________________________________________________________________________
# QUESTION 8

def slam(problem, agent) -> Generator:
    '''
    problem: a SLAMProblem instance
    agent: a SLAMLogicAgent instance
    '''
    pac_x_0, pac_y_0 = problem.startState
    KB = []
    all_coords = list(itertools.product(range(problem.getWidth()+2), range(problem.getHeight()+2)))
    non_outer_wall_coords = list(itertools.product(range(1, problem.getWidth()+1), range(1, problem.getHeight()+1)))

    # map describes what we know, for GUI rendering purposes. -1 is unknown, 0 is open, 1 is wall
    known_map = [[-1 for y in range(problem.getHeight()+2)] for x in range(problem.getWidth()+2)]

    # We know that the outer_coords are all walls.
    outer_wall_sent = []
    for x, y in all_coords:
        if ((x == 0 or x == problem.getWidth() + 1)
                or (y == 0 or y == problem.getHeight() + 1)):
            known_map[x][y] = 1
            outer_wall_sent.append(PropSymbolExpr(wall_str, x, y))
    
    KB.append(conjoin(outer_wall_sent))

    "*** BEGIN YOUR CODE HERE ***"
    KB.append(PropSymbolExpr(pacman_str, pac_x_0, pac_y_0, time=0))
    # Khởi tạo pacman
    
    
    for t in range(agent.num_timesteps):
        possible_locations = []
        "*** END YOUR CODE HERE ***"
        auxiliaryFunction1(KB, agent, t, all_coords, non_outer_wall_coords, known_map, SLAMSensorAxioms, SLAMSuccessorAxioms, 8)

        auxiliaryFunction2(possible_locations, non_outer_wall_coords, KB, t)

        auxiliaryFunction3(non_outer_wall_coords, KB, known_map, t)

        agent.moveToNextState(agent.actions[t])
        yield (known_map, possible_locations)


# Abbreviations
plp = positionLogicPlan
loc = localization
mp = mapping
flp = foodLogicPlan
# Sometimes the logic module uses pretty deep recursion on long expressions
sys.setrecursionlimit(100000)

#______________________________________________________________________________
# Important expression generating functions, useful to read for understanding of this project.


def sensorAxioms(t: int, non_outer_wall_coords: List[Tuple[int, int]]) -> Expr:
    all_percept_exprs = []
    combo_var_def_exprs = []
    for direction in DIRECTIONS:
        percept_exprs = [] # Lưu ý: Biến này được làm mới qua mỗi vòng
        dx, dy = DIR_TO_DXDY_MAP[direction]
        for x, y in non_outer_wall_coords:
            combo_var = PropSymbolExpr(pacman_wall_str, x, y, x + dx, y + dy, time=t)
            # Ví dụ về giá trị của combo_var: PWALL[0,0,0,1]_1
            # Mệnh đề trên biểu thị pacman ở vị trí (0,0) tại thời điểm time = 1, tường ở vị trí (0,1)
            percept_exprs.append(combo_var)


            combo_var_def_exprs.append(combo_var % (
                PropSymbolExpr(pacman_str, x, y, time=t) & PropSymbolExpr(wall_str, x + dx, y + dy)))
            # Mệnh đề trên biểu thị: mệnh đề combo_var tương đương với 
            # pacman ở vị trí (x,y) tại thời điểm t hội với mệnh đề tường ở vị trí (x+dx, y+dy)

        percept_unit_clause = PropSymbolExpr(blocked_str_map[direction], time = t)
        # Ví dụ về giá trị của percept_unit_clause: NORTH_BLOCKED_1
        # Mệnh đề trên biểu thị phía Bắc bị chặn tại thời điểm 1

        all_percept_exprs.append(percept_unit_clause % disjoin(percept_exprs))
        # List chứa các mệnh đề tương đương, ví dụ như
        # Phía Bắc bị chặn tại thời điểm 1 tương đương với một trong các đường đi của pacman bị chặn lại bởi tường

    return conjoin(all_percept_exprs + combo_var_def_exprs)
    # Trả về chuẩn tắc hội


def fourBitPerceptRules(t: int, percepts: List) -> Expr:
    """
    Localization and Mapping both use the 4 bit sensor, which tells us True/False whether
    a wall is to pacman's north, south, east, and west.
    """
    assert isinstance(percepts, list), "Percepts must be a list."
    assert len(percepts) == 4, "Percepts must be a length 4 list."

    percept_unit_clauses = []
    for wall_present, direction in zip(percepts, DIRECTIONS):
        percept_unit_clause = PropSymbolExpr(blocked_str_map[direction], time=t)
        if not wall_present:
            percept_unit_clause = ~PropSymbolExpr(blocked_str_map[direction], time=t)
        percept_unit_clauses.append(percept_unit_clause) # The actual sensor readings
    return conjoin(percept_unit_clauses)
    # Trả về chuẩn tắc hội của các mệnh đề nhận thức xung quang có tường hay không
    # VD [North_blocked_1,...]


def numAdjWallsPerceptRules(t: int, percepts: List) -> Expr:
    """
    SLAM uses a weaker numAdjWallsPerceptRules sensor, which tells us how many walls pacman is adjacent to
    in its four directions.
        000 = 0 adj walls.
        100 = 1 adj wall.
        110 = 2 adj walls.
        111 = 3 adj walls.
    """
    assert isinstance(percepts, list), "Percepts must be a list."
    assert len(percepts) == 3, "Percepts must be a length 3 list."

    percept_unit_clauses = []
    for i, percept in enumerate(percepts):
        n = i + 1
        percept_literal_n = PropSymbolExpr(geq_num_adj_wall_str_map[n], time=t)
        if not percept:
            percept_literal_n = ~percept_literal_n
        percept_unit_clauses.append(percept_literal_n)
    return conjoin(percept_unit_clauses)


def SLAMSensorAxioms(t: int, non_outer_wall_coords: List[Tuple[int, int]]) -> Expr:
    all_percept_exprs = []
    combo_var_def_exprs = []
    for direction in DIRECTIONS:
        percept_exprs = []
        dx, dy = DIR_TO_DXDY_MAP[direction]
        for x, y in non_outer_wall_coords:
            combo_var = PropSymbolExpr(pacman_wall_str, x, y, x + dx, y + dy, time=t)
            percept_exprs.append(combo_var)
            combo_var_def_exprs.append(combo_var % (PropSymbolExpr(pacman_str, x, y, time=t) & PropSymbolExpr(wall_str, x + dx, y + dy)))

        blocked_dir_clause = PropSymbolExpr(blocked_str_map[direction], time=t)
        all_percept_exprs.append(blocked_dir_clause % disjoin(percept_exprs))

    percept_to_blocked_sent = []
    for n in range(1, 4):
        wall_combos_size_n = itertools.combinations(blocked_str_map.values(), n)
        n_walls_blocked_sent = disjoin([
            conjoin([PropSymbolExpr(blocked_str, time=t) for blocked_str in wall_combo])
            for wall_combo in wall_combos_size_n])
        # n_walls_blocked_sent is of form: (N & S) | (N & E) | ...
        percept_to_blocked_sent.append(
            PropSymbolExpr(geq_num_adj_wall_str_map[n], time=t) % n_walls_blocked_sent)

    return conjoin(all_percept_exprs + combo_var_def_exprs + percept_to_blocked_sent)


def allLegalSuccessorAxioms(t: int, walls_grid: List[List], non_outer_wall_coords: List[Tuple[int, int]]) -> Expr:
    """walls_grid can be a 2D array of ints or bools."""
    all_xy_succ_axioms = []
    for x, y in non_outer_wall_coords: # Xét tọa độ của các điểm nằm BÊN TRONG map
        
        xy_succ_axiom = pacmanSuccessorAxiomSingle(
            x, y, t, walls_grid)
        # Đọc lại hàm pacmanSuccessorAxiomSingle

        if xy_succ_axiom:
            all_xy_succ_axioms.append(xy_succ_axiom)
        # Nếu có tồn tại mệnh đề tương đương nhận được từ hàm trên sẽ được thêm vào trong list
    return conjoin(all_xy_succ_axioms)


def SLAMSuccessorAxioms(t: int, walls_grid: List[List], non_outer_wall_coords: List[Tuple[int, int]]) -> Expr:
    """walls_grid can be a 2D array of ints or bools."""
    all_xy_succ_axioms = []
    for x, y in non_outer_wall_coords:
        xy_succ_axiom = SLAMSuccessorAxiomSingle(
            x, y, t, walls_grid)
        if xy_succ_axiom:
            all_xy_succ_axioms.append(xy_succ_axiom)
    return conjoin(all_xy_succ_axioms)

#______________________________________________________________________________
# Various useful functions, are not needed for completing the project but may be useful for debugging


def modelToString(model: Dict[Expr, bool]) -> str:
    """Converts the model to a string for printing purposes. The keys of a model are 
    sorted before converting the model to a string.
    
    model: Either a boolean False or a dictionary of Expr symbols (keys) 
    and a corresponding assignment of True or False (values). This model is the output of 
    a call to pycoSAT.
    """
    if model == False:
        return "False" 
    else:
        # Dictionary
        modelList = sorted(model.items(), key=lambda item: str(item[0]))
        return str(modelList)


def extractActionSequence(model: Dict[Expr, bool], actions: List) -> List:
    """
    Convert a model in to an ordered list of actions.
    model: Propositional logic model stored as a dictionary with keys being
    the symbol strings and values being Boolean: True or False
    Example:
    >>> model = {"North[2]":True, "P[3,4,0]":True, "P[3,3,0]":False, "West[0]":True, "GhostScary":True, "West[2]":False, "South[1]":True, "East[0]":False}
    >>> actions = ['North', 'South', 'East', 'West']
    >>> plan = extractActionSequence(model, actions)
    >>> print(plan)
    ['West', 'South', 'North']
    """
    plan = [None for _ in range(len(model))]
    for sym, val in model.items():
        parsed = parseExpr(sym)
        if type(parsed) == tuple and parsed[0] in actions and val:
            action, _, time = parsed
            plan[time] = action
    #return list(filter(lambda x: x is not None, plan))
    return [x for x in plan if x is not None]
    # Lười quá dell đọc, nma đề bài bảo là trả về danh sách cách hành động (action) từ lúc đầu đến cuối


# Helpful Debug Method
def visualizeCoords(coords_list, problem) -> None:
    wallGrid = game.Grid(problem.walls.width, problem.walls.height, initialValue=False)
    for (x, y) in itertools.product(range(problem.getWidth()+2), range(problem.getHeight()+2)):
        if (x, y) in coords_list:
            wallGrid.data[x][y] = True
    print(wallGrid)


# Helpful Debug Method
def visualizeBoolArray(bool_arr, problem) -> None:
    wallGrid = game.Grid(problem.walls.width, problem.walls.height, initialValue=False)
    wallGrid.data = copy.deepcopy(bool_arr)
    print(wallGrid)

class PlanningProblem:
    """
    This class outlines the structure of a planning problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the planning problem.
        """
        util.raiseNotDefined()

    def getGhostStartStates(self):
        """
        Returns a list containing the start state for each ghost.
        Only used in problems that use ghosts (FoodGhostPlanningProblem)
        """
        util.raiseNotDefined()
        
    def getGoalState(self):
        """
        Returns goal state for problem. Note only defined for problems that have
        a unique goal state such as PositionPlanningProblem
        """
        util.raiseNotDefined()
