from logicPlan import *
x, y = 0, 0
direction = 'North'
dx, dy = DIR_TO_DXDY_MAP[direction]
simpleExpr = PropSymbolExpr(wall_str+direction, x + dx, y + dy, time = 1)

print(simpleExpr)