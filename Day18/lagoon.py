import numpy as np
import matplotlib.pyplot as plt
import sys
sys.setrecursionlimit(1000000)

def dig_trench(dig_map,dict):
    grid = []
    cur = (0,0)
    
    for dig in dig_map:
        for _ in range(int(dig[1])):
            cur = (cur[0] + dict[dig[0]][0], cur[1] + dict[dig[0]][1])
            grid.append(cur)

    # Normalize coords
    min_row,_ = min(grid, key=lambda x: x[0])
    _,min_col = min(grid, key=lambda x: x[1])

    if min_row < 0:
        grid = list(map(lambda x: (x[0]+abs(min_row),x[1]), grid))
    if min_col < 0:
        grid = list(map(lambda x: (x[0],x[1]+abs(min_col)), grid))
    
    rows,_ = max(grid, key=lambda x: x[0])
    _,cols = max(grid, key=lambda x: x[1])

    lagoon = np.zeros((rows+1,cols+1))
    
    for i in grid:
        lagoon[i] = 1
    
    return lagoon


def flood_recursive(matrix, start=(1,1)):
    width = len(matrix)
    height = len(matrix[0])
    def fill(x,y,start_color,color_to_update):
        #if the square is not the same color as the starting point
        if matrix[x][y] != start_color:
            return
        #if the square is not the new color
        elif matrix[x][y] == color_to_update:
            return
        else:
            #update the color of the current square to the replacement color
            matrix[x][y] = color_to_update
            neighbors = [(x-1,y),(x+1,y),(x-1,y-1),(x+1,y+1),(x-1,y+1),(x+1,y-1),(x,y-1),(x,y+1)]
            for n in neighbors:
                if 0 <= n[0] <= width-1 and 0 <= n[1] <= height-1:
                    fill(n[0],n[1],start_color,color_to_update)
    #pick a random starting point
    start_x, start_y = start
    start_color = matrix[start_x][start_y]
    fill(start_x,start_y,start_color,9)
    return matrix


def translate_hex(hex_string):
    dir_dic = {'0':'R', '1':'D', '2':'L', '3':'U'}
    dist = int(hex_string[2:7],16)
    direction = dir_dic[hex_string[7]]

    return direction, dist


def dig_map_to_points(dig_map):
    p = (0,0)
    res = []

    for d,s in dig_map:
        p = (p[0]+dir_dict[d[0]][0]*int(s), p[1]+dir_dict[d[0]][1]*int(s))
        res.append(p)

    return res


def polygonArea(vertices):
  #A function to apply the Shoelace algorithm
  numberOfVertices = len(vertices)
  sum1 = 0
  sum2 = 0
  
  for i in range(numberOfVertices-1):
    sum1 += vertices[i][0] *  vertices[i+1][1]
    sum2 += vertices[i][1] *  vertices[i+1][0]
  
  #Add xn.y1
  sum1 += vertices[numberOfVertices-1][0]*vertices[0][1]   
  #Add x1.yn
  sum2 += vertices[0][0]*vertices[numberOfVertices-1][1]   
  
  area = abs(sum1 - sum2) // 2
  return area




dir_dict = {'U':(-1,0), 'D':(1,0), 'L':(0,-1), 'R':(0,1)}

dig_map = [l.split() for l in open('input.txt').read().splitlines()]

a = dig_trench(dig_map, dir_dict)

plt.figure(figsize=(8,6))
plt.imshow(a)


c = flood_recursive(a,(100,100))

res = 0
for line in c:
    for i in line:
        if i:
            res += 1
print("Part1:",res)

plt.figure(figsize=(8,6))
plt.imshow(c)

new_dig_map = [translate_hex(x[2]) for x in dig_map]

b = dig_map_to_points(new_dig_map)
print("Part2:",polygonArea(b) + sum([int(x) for _,x in new_dig_map])//2 + 1)

plt.show()