from logicPlan import *
pacman_str = 'P'
food_str = 'FOOD'
wall_str = 'WALL'
pacman_wall_str = pacman_str + wall_str
DIRECTIONS = ['North', 'South', 'East', 'West']
blocked_str_map = dict([(direction, (direction + "_blocked").upper()) for direction in DIRECTIONS])
geq_num_adj_wall_str_map = dict([(num, "GEQ_{}_adj_walls".format(num)) for num in range(1, 4)])
DIR_TO_DXDY_MAP = {'North':(0, 1), 'South':(0, -1), 'East':(1, 0), 'West':(-1, 0)}


x, y = 0, 0
direction = 'North'
dx, dy = DIR_TO_DXDY_MAP[direction]
simpleExpr = PropSymbolExpr(wall_str+direction, x + dx, y + dy, time = 1)

A = []
A.append(PropSymbolExpr(food_str, x1, y1, time = 0) for x1, y1 in zip([1,2,3], [4,5,6]))
print(A)

