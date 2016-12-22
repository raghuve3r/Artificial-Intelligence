#The program outputs a series of steps to achieve the canonical state of a 15 puzzle game.

#I have used two heuristics to generate to find the costs.

#One being Manahattan distance, which finds the distance of a tile from current position to its final position.
#The next best state is calculated using f(s) = h(s). Where h(s) is the heuristic cost found out using Manhattan distance

#The second is by counting the number of misplaced tiles.
#The next best state is calculated using f(s) = g(s) + f(s),
#              where g(s) is the number of steps taken from initial state to the current state
#              and f(s) is the sum of misplaced tiles

#A function generate_neighbors is used to find the neighbors of a given state.
#The function returns 4 neighbors(generated by moving '0' by one space in all the four directions repectively)

#A function backtrack has been created to construct a path needed to achieve the canonical state of a 15 puzzle.
#The backtrack function takes in a dictionary and returns a final path required to achieve goal state from the initial given board.

#A function get_direction is used to for generating the directions required to solve the puzzle.
#'L','R','U','D' indicate the respective direction '0' has to be moved.

#The function solvable calculates the permutation inversion of a given board.
#The returned value can be used to determine if a given configuration of board is solvable or not.

#Functions create_matrix and convert_to_string are used for convertion.
#That is converting a string representation of a board into matrix and matrix representation into string respectively

#A state variable is defined to keep track of the number of states generated before arriving at the solution
#Timer is used, to calculate the amount of time needed to find solution using both the above mentioned heuristics.

#Both the heuristics perform comparably when the solution to goal state is relatively straight forward.
#But the manhattan distance heuristic outperforms the misplaced tiles heuristics when the path to goal state is complex and requires backtracking
#I chose number of states as a parameter to measure the efficiency.
#The program stops when the number of generated states is more than 3000.
#The number of states never exceed 3000 except for a few configuration of boards,
#and that happens when we consider misplaced tiles heuristics.
#I find the manhattan distance heuristic to be more of a feasible option,
#since it chooses the states carefully and moves towards the goal in an efficient manner

#Reference: http://codereview.stackexchange.com/questions/33473/solving-15-puzzle
#Reference: https://speakerdeck.com/daehn/solving-a-15-puzzle-in-python
#Reference: http://www.codeproject.com/Articles/365553/Puzzle-solving-using-the-A-algorithm-using-Pytho

from copy import deepcopy
import time

#Function to read the board from a text file
def readfile(filename):
    try:
        with open(filename,"r") as file:
            text = file.read().replace('\n', ' ')
            file.close()
        return text
    except IOError:
        print('Enter correct filename!')
        return

#Function to swap the 0 with other numbers
def swap(start,r1,c1,r2,c2):
    term = start[r1][c1]
    start[r1][c1] = start[r2][c2]
    start[r2][c2] = term
    return start

#Function to convert a matrix into a string, for storing in a dictionary
def convert_to_string(start):
    str_list = []
    for r in start:
        for c in r:
            str_list.append(str(c) + " ")
        str_list.append("\n")
    str_list.pop()
    return "".join(str_list)

#Function to calculate manhattan distance between the
#position of a tile from current position to its original position
def manhattan_heuristic(start):
        sum = 0
        for r in range(4):
            for c in range(4):
                n = start[r][c] - 1
                if (n == -1):
                    n = 15
                row = abs(r - n / 4)
                col = abs(c - n % 4)
                sum += row + col
        return sum

#Function to calculate number of misplaced tiles in a given board
def misplaced_tiles_heuristic(start,goal):
        sum = 0
        for r in range(4):
            for c in range(4):
                if start[r][c] != goal[r][c]:
                    sum += 1
        return sum

#function to generate neighbors of a given board based on position of the zero
def generate_neighbors(start):
        neighbors = []
        w = 4
        h = 4
        for r in range(h):
            for c in range(w):
                if (start[r][c] == 0):
                    if (r == 0):
                        neighbor = deepcopy(start)
                        neighbor = swap(neighbor, r, c, h - 1, c)
                        neighbors.append(neighbor)
                    if (r == h - 1):
                        neighbor = deepcopy(start)
                        neighbor = swap(neighbor, r, c, 0, c)
                        neighbors.append(neighbor)
                    if (c == 0):
                        neighbor = deepcopy(start)
                        neighbor = swap(neighbor, r, c, r, w - 1)
                        neighbors.append(neighbor)
                    if (c == w - 1):
                        neighbor = deepcopy(start)
                        neighbor = swap(neighbor, r, c, r, 0)
                        neighbors.append(neighbor)
                    if (r != 0):
                        neighbor = deepcopy(start)
                        neighbor = swap(neighbor, r, c, r - 1, c)
                        neighbors.append(neighbor)
                    if (r != h - 1):
                        neighbor = deepcopy(start)
                        neighbor = swap(neighbor, r, c, r + 1, c)
                        neighbors.append(neighbor)
                    if (c != 0):
                        neighbor = deepcopy(start)
                        neighbor = swap(neighbor, r, c, r, c - 1)
                        neighbors.append(neighbor)
                    if (c != w - 1):
                        neighbor = deepcopy(start)
                        neighbor = swap(neighbor, r, c, r, c + 1)
                        neighbors.append(neighbor)
        return neighbors

#Function to create a matrix out of a string
def create_matrix(board,dimension):
    mat = []
    board = board.split(' ')
    for x in range(dimension):
        row = []
        for y in range(x*4, (x+1)*4):
            row.append(int(board[y]))
        mat.append(row)
    return mat

#Function to find the position of zero in a given board
def find_zero(board):
    board = create_matrix(board,4)
    for r in range(4):
        for c in range(4):
            if board[r][c] == 0:
                return r,c

#Function to get the directions to solve a board from initial position to goal state
def get_direction(solution):
    n = len(solution)
    d = []
    for i in range(1,n):
        r1,c1 = find_zero(solution[i-1])
        r2,c2 = find_zero(solution[i])
        if r1 == r2:
            if c1 - c2 > 0:
                d.append('L')
            else:
                d.append('R')
        else:
            if r1 - r2 > 0:
                d.append('U')
            else:
                d.append('D')
    return d

#Function to create a goal state of the 15 puzzle board
def create_goal_state(dimension):
    mat = []
    for x in range(dimension):
        row = []
        for y in range(x*4, (x+1)*4):
            if y == 15:
                row.append(0)
            else:
                row.append(y+1)
        mat.append(row)
    return mat

#Function to find the minimum among the neighbors
def get_min_state(path,f_s):
    minimum = 2 ** 30
    neighbor = None
    for elem in path:
        if(elem in f_s.keys()):
            if(f_s[elem] < minimum):
                neighbor = elem
                minimum = f_s[elem]
    return neighbor

#Function to create a path from goal state to initial state
def backtrack(sol, current):
        if (sol.has_key(current)):
            p = backtrack(sol, sol[current])
            return p + [current]
        else:
            return [current]

#Function to solve the board using manhattan heuristics
def solve_manhattan(board,goal):
    states = 0
    start_string = convert_to_string(board)
    start_matrix = board
    goal_string = convert_to_string(goal)
    temp = []
    all_solution = [start_string]
    sol = {}
    f_s = {start_string: manhattan_heuristic(start_matrix)}

    while len(all_solution) != 0:
        current_string = get_min_state(all_solution,f_s)
        if(current_string == goal_string):
            return sol, current_string, states
        current_matrix = create_matrix(current_string,4)
        all_solution.remove(current_string)
        temp.append(current_string)
        neighbors = generate_neighbors(current_matrix)

        for n_m in neighbors:
            current_f_s = manhattan_heuristic(n_m)
            n_s = convert_to_string(n_m)
            if n_s in temp and f_s.has_key(n_s) and current_f_s >= f_s[n_s]:
                continue

            if n_s not in all_solution or (f_s.has_key(n_s) and current_f_s < f_s[n_s]):
                states += 1
                if states > 3000:
                    return 0,0,0
                sol[n_s] = current_string
                f_s[n_s] = current_f_s
                if n_s not in all_solution:
                    all_solution.append(n_s)
    return None

#Function to solve the board using the misplaced tiles heuristics
def solve_misplaced_tiles(board,goal):
    states = 0
    start_string = convert_to_string(board)
    start_matrix = board
    goal_string = convert_to_string(goal)
    temp = []
    all_solution = [start_string]
    sol = {}

    g_s = {start_string : 0}
    f_s = {start_string: g_s[start_string] + misplaced_tiles_heuristic(start_matrix,goal)}

    while len(all_solution) != 0:
        current_string = get_min_state(all_solution,f_s)
        if(current_string == goal_string):
            return sol, current_string, states
        current_matrix = create_matrix(current_string,4)
        all_solution.remove(current_string)
        temp.append(current_string)
        neighbors = generate_neighbors(current_matrix)
        for n_m in neighbors:
            current_g_score = g_s[current_string] + 1
            current_f_s = current_g_score + misplaced_tiles_heuristic(n_m,goal)
            n_s = convert_to_string(n_m)
            if n_s in temp and f_s.has_key(n_s) and current_f_s >= f_s[n_s]:
                continue
            if n_s not in all_solution or (f_s.has_key(n_s) and current_f_s < f_s[n_s]):
                states += 1
                if states > 3000:
                    return 0,0,0
                sol[n_s] = current_string
                g_s[n_s] = current_g_score
                f_s[n_s] = current_f_s
                if n_s not in all_solution:
                    all_solution.append(n_s)
    return None

#Function to check if a board is solvable or not by finding out the permutation inversion
def solvable(board):
    sum = 0
    for x in range(4):
        for y in range(4):
            if board[x][y] == 0:
                sum = x+1

    board_l = []
    for x in range(4):
        for y in range(4):
            board_l.append(board[x][y])

    for i in range(len(board_l)):
        if board_l[i] != 0:
            x = board_l[i]
            for j in range(i+1,len(board_l)):
                if board_l[j] < x and board_l[j] != 0:
                    sum += 1
    return sum%2


#Start of the program

text = readfile('board.txt')
board = create_matrix(text,4)
c = solvable(board)

if c == 0:
    goal = create_goal_state(4)

    start = time.time()
    x,y,z = solve_manhattan(board,goal)
    if x == 0 and y == 0 and z == 0:
        print "\nMore than 3000 states generated using the misplaced tiles heuristic, no solution found yet...."
        print "Discontinued"
    else:
        solution_1 = backtrack(x,y)
        direction_1 = get_direction(solution_1)
        end = time.time() - start
        print 'Solution using the Manhattan distance as heuristics: \n'
        print 'Time taken to find the solution: ',str(end)
        print '''Number of states generated: ''',str(z)
        print 'Moves required to return to canonical form of the board:'
        for d in direction_1:
            print d,
        print " "

    start_2 = time.time()
    p,q,r = solve_misplaced_tiles(board,goal)
    if p == 0 and q == 0 and r == 0:
        print "\nMore than 3000 states generated using the misplaced tiles heuristic, no solution found yet...."
        print "Discontinued"
    else:
        solution_2 = backtrack(p,q)
        direction_2 = get_direction(solution_2)
        end_2 = time.time() - start_2
        print '\nSolution using the misplaced tiles as the heuristics: \n'
        print 'Time taken to find the solution: ',str(end_2)
        print '''Number of states generated: ''',str(r)
        print 'Moves required to return to canonical form of the board:'
        for d in direction_2:
            print d,
else:
    print "Not solvable"

