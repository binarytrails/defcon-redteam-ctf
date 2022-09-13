# @author Vsevolod Ivanov <seva@binarytrails.net>

import sys

instructions = """
--------------------------------------------------
|                                                |
|            Welcome to Dungeon Dive             |
|   Goal:                                        |
|   Start at point P and reach point E           |
|                                                |
|   Controls:                                    |
|   W = Up                                       |
|   A = Left                                     |
|   S = Down                                     |
|   D = Right                                    |
|                                                |
|   How to Play:                                 |
|   1. Recieve the Map                           |
|   2. Navigate the Map with Controls            |
|   3. In a single string respond with all your  |
|   controls to reach point E from point P       |
|   4. Repeat 1000 times                         |
|   5. Receive the Flag                          |
|                                                |
--------------------------------------------------
"""

# Check if cell (x, y) is valid or not
def is_valid_cell(x, y, N):
    if x < 0 or y < 0 or x >= N or y >= N:
        return False

    return True

def find_paths_util(maze, source, destination, visited, path, paths):
  """Find paths using Breadth First Search algorith """
  # Done if destination is found
  if source == destination:
    paths.append(path[:])  # append copy of current path
    return

  # mark current cell as visited
  N = len(maze)
  x, y = source
  visited[x][y] = True

  # if current cell is a valid and open cell, 
  if is_valid_cell(x, y, N) and maze[x][y]:
    # Using Breadth First Search on path extension in all direction

    # go right (x, y) --> (x + 1, y)
    if x + 1 < N and (not visited[x + 1][y]):
      path.append((x + 1, y))
      find_paths_util(maze,(x + 1, y), destination, visited, path, paths)
      path.pop()

    # go left (x, y) --> (x - 1, y)
    if x - 1 >= 0 and (not visited[x - 1][y]):
      path.append((x - 1, y))
      find_paths_util(maze, (x - 1, y), destination, visited, path, paths)
      path.pop()

    # go up (x, y) --> (x, y + 1)
    if y + 1 < N and (not visited[x][y + 1]):
      path.append((x, y + 1))
      find_paths_util(maze, (x, y + 1), destination, visited, path, paths)
      path.pop()

    # go down (x, y) --> (x, y - 1)
    if y - 1 >= 0 and (not visited[x][y - 1]):
      path.append((x, y - 1))
      find_paths_util(maze, (x, y - 1), destination, visited, path, paths)
      path.pop()

    # Unmark current cell as visited
  visited[x][y] = False

  return paths

def find_paths(maze, source, destination):
  """ Sets up and searches for paths"""
  N = len(maze) # size of Maze is N x N

  # 2D matrix to keep track of cells involved in current path
  visited = [[False]*N for _ in range(N)]

  path = [source]
  paths = []
  paths = find_paths_util(maze, source, destination, visited, path, paths)

  return paths

def clean_line(s):
    clean = ''
    i = 0
    for v in s:
        #print(v)
        if (i % 2 == 0):
            clean += s[i]
        i+=1
    return clean

def find_location(lines, char):
    i = 0
    for row in lines:
        j = 0
        for cell in row:
            if (cell == char):
                #print("({},{}) {}".format(i,j,cell))
                return (i,j)
            j+=1
        i+=1

if __name__ == "__main__":

    map_file = 'map.txt'
    try:
        map_file = sys.argv[1]
    except Exception:
        print('[!] ./dungeon_dive.py <map_file>')
        print('[+] choosing default map.txt file')

    print('[+] instructions:', end='')
    print(instructions, end='')

    print('[+] loading map...')
    map_file = open(map_file, 'r')
    lines = map_file.readlines() #[22:] # one-time header on network socket (part-2)
    for line in lines:
        print(line, end='')

    print('[+] converting unicode map to binary map...')
    clean_lines = []
    for line in lines:
        line = clean_line(line)
        line = line.replace('■', '0')
        line = line.replace(' ', '1')
        print(line)
        clean_lines.append(line)

    start = find_location(clean_lines, 'P')
    end = find_location(clean_lines, 'E')

    # final clean to remove P and E
    i = 0
    for row in clean_lines:
        j = 0
        for cell in row:
            if (cell == 'P' or cell == 'E'):
                line = clean_lines[i]
                line = line.replace('P', '1')
                line = line.replace('E', '1')
                clean_lines[i] = line
            j+=1
        i+=1

    print('[+] start: ',start)
    print('[+] end: ',end)

    maze_ints = []
    for str_row in clean_lines:
        int_row = []
        for str_column in str_row:
            int_row.append(int(str_column))
        maze_ints.append(int_row)

    # Start point and destination
    source = start
    destination = end

    # Find all paths
    paths = find_paths(maze_ints, source, destination)

    print("[+] paths with '->' separator between maze cell locations")
    i = 0
    gamer_path = ''
    for first_path in paths:
        for step in first_path:
            if (i < len(first_path) - 1):
                next_step = first_path[i+1]
                if (step[0] < next_step[0]):
                    gamer_path += 'S'
                elif (step[0] > next_step[0]):
                    gamer_path += 'W'
                elif (step[1] < next_step[1]):
                    gamer_path += 'D'
                elif (step[1] > next_step[1]):
                    gamer_path += 'A'
            i+=1

    print('[+] found gamer wasd path: {}'.format(gamer_path))

