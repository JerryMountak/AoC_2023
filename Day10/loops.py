import sys
sys.setrecursionlimit(100000)

loop_map = []

def find_loop(i,j,board,dir,map=[]):
    match dir:
        case 'u':
            pipe = board[i-1][j]
            match pipe:
                case '|':
                    loop_map[i-1][j] = True
                    find_loop(i-1,j,board,'u',map)
                case '7':
                    loop_map[i-1][j] = True
                    find_loop(i-1,j,board,'l',map)
                case 'F':
                    loop_map[i-1][j] = True
                    find_loop(i-1,j,board,'r',map)
                case _:
                    if pipe == 'S':
                        return
        case 'd':
            pipe = board[i+1][j]
            match pipe:
                case '|':
                    loop_map[i+1][j] = True
                    find_loop(i+1,j,board,'d',map)
                case 'J':
                    loop_map[i+1][j] = True
                    find_loop(i+1,j,board,'l',map)
                case 'L':
                    loop_map[i+1][j] = True
                    find_loop(i+1,j,board,'r',map)
                case _:
                    if pipe == 'S':
                        return
        case 'l':
            pipe = board[i][j-1]
            match pipe:
                case '-':
                    loop_map[i][j-1] = True
                    find_loop(i,j-1,board,'l',map)
                case 'L':
                    loop_map[i][j-1] = True
                    find_loop(i,j-1,board,'u',map)
                case 'F':
                    loop_map[i][j-1] = True
                    find_loop(i,j-1,board,'d',map)
                case _:
                    if pipe == 'S':
                        return
        case 'r':
            pipe = board[i][j+1]
            match pipe:
                case '-':
                    loop_map[i][j+1] = True
                    find_loop(i,j+1,board,'r',map)
                case 'J':
                    loop_map[i][j+1] = True
                    find_loop(i,j+1,board,'u',map)
                case '7':
                    loop_map[i][j+1] = True
                    find_loop(i,j+1,board,'d',map)
                case _:
                    if pipe == 'S':
                        return
        case 'start':
            loop_map[i][j] = True
            if i != 0:
                find_loop(i,j,board,'u',map)
            if j != len(board)-1:
                find_loop(i,j,board,'r',map)
            if i != len(board)-1:
                find_loop(i,j,board,'d',map)
            if j != 0:
                find_loop(i,j,board,'l',map)


board = []

with open("input.txt") as f:
    for i,line in enumerate(f):
        tmp = list(line)
        tmp.pop(-1)
        board.append(tmp)
        if 'S' in line:
            start = (i,line.index('S'))

loop_map = [[False for _ in line] for line in board]
find_loop(start[0],start[1],board,'start')

print(int((sum([sum(i) for i in zip(*loop_map)]))/2))

is_inside = False
res = 0

for i,line in enumerate(board):
    for j,p in enumerate(line):
        if loop_map[i][j] and (p in {'|', 'L', 'J'}):
            is_inside = not is_inside
        elif not loop_map[i][j] and is_inside:
            res += 1

print(res)