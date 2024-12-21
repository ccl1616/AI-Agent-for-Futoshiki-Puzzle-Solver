"""
Each futoshiki board is represented as a dictionary with string keys and
int values.
e.g. my_board['A1'] = 8

Empty values in the board are represented by 0

An * after the letter indicates the inequality between the row represented
by the letter and the next row.
e.g. my_board['A*1'] = '<' 
means the value at A1 must be less than the value
at B1

Similarly, an * after the number indicates the inequality between the
column represented by the number and the next column.
e.g. my_board['A1*'] = '>' 
means the value at A1 is greater than the value
at A2

Empty inequalities in the board are represented as '-'

"""
import sys

#======================================================================#
#*#*#*# Optional: Import any allowed libraries you may need here #*#*#*#
#======================================================================#
import time
import numpy as np
#=================================#
#*#*#*# Your code ends here #*#*#*#
#=================================#

ROW = "ABCDEFGHI"
COL = "123456789"

class Board:
    '''
    Class to represent a board, including its configuration, dimensions, and domains
    '''
    
    def get_board_dim(self, str_len):
        '''
        Returns the side length of the board given a particular input string length
        '''
        d = 4 + 12 * str_len
        n = (2+np.sqrt(4+12*str_len))/6
        if(int(n) != n):
            raise Exception("Invalid configuration string length")
        
        return int(n)
        
    def get_config_str(self):
        '''
        Returns the configuration string
        '''
        return self.config_str
        
    def get_config(self):
        '''
        Returns the configuration dictionary
        '''
        return self.config
        
    def get_variables(self):
        '''
        Returns a list containing the names of all variables in the futoshiki board
        '''
        variables = []
        for i in range(0, self.n):
            for j in range(0, self.n):
                variables.append(ROW[i] + COL[j])
        return variables
    
    def convert_string_to_dict(self, config_string):
        '''
        Parses an input configuration string, retuns a dictionary to represent the board configuration
        as described above
        '''
        config_dict = {}
        
        for i in range(0, self.n):
            for j in range(0, self.n):
                cur = config_string[0]
                config_string = config_string[1:]
                
                config_dict[ROW[i] + COL[j]] = int(cur)
                
                if(j != self.n - 1):
                    cur = config_string[0]
                    config_string = config_string[1:]
                    config_dict[ROW[i] + COL[j] + '*'] = cur
                    
            if(i != self.n - 1):
                for j in range(0, self.n):
                    cur = config_string[0]
                    config_string = config_string[1:]
                    config_dict[ROW[i] + '*' + COL[j]] = cur
                    
        return config_dict
        
    def print_board(self):
        '''
        Prints the current board to stdout
        '''
        config_dict = self.config
        for i in range(0, self.n):
            for j in range(0, self.n):
                cur = config_dict[ROW[i] + COL[j]]
                if(cur == 0):
                    print('_', end=' ')
                else:
                    print(str(cur), end=' ')
                
                if(j != self.n - 1):
                    cur = config_dict[ROW[i] + COL[j] + '*']
                    if(cur == '-'):
                        print(' ', end=' ')
                    else:
                        print(cur, end=' ')
            print('')
            if(i != self.n - 1):
                for j in range(0, self.n):
                    cur = config_dict[ROW[i] + '*' + COL[j]]
                    if(cur == '-'):
                        print(' ', end='   ')
                    else:
                        print(cur, end='   ')
            print('')
    
    def __init__(self, config_string):
        '''
        Initialising the board
        '''
        self.config_str = config_string
        self.n = self.get_board_dim(len(config_string))
        if(self.n > 9):
            raise Exception("Board too big")
            
        self.config = self.convert_string_to_dict(config_string)
        self.domains = self.reset_domains()
        
        self.forward_checking(self.get_variables()) # do the first forward checking on every variables
        
        
    def __str__(self):
        '''
        Returns a string displaying the board in a visual format. Same format as print_board()
        '''
        output = ''
        config_dict = self.config
        for i in range(0, self.n):
            for j in range(0, self.n):
                cur = config_dict[ROW[i] + COL[j]]
                if(cur == 0):
                    output += '_ '
                else:
                    output += str(cur)+ ' '
                
                if(j != self.n - 1):
                    cur = config_dict[ROW[i] + COL[j] + '*']
                    if(cur == '-'):
                        output += '  '
                    else:
                        output += cur + ' '
            output += '\n'
            if(i != self.n - 1):
                for j in range(0, self.n):
                    cur = config_dict[ROW[i] + '*' + COL[j]]
                    if(cur == '-'):
                        output += '    '
                    else:
                        output += cur + '   '
            output += '\n'
        return output
        
    def reset_domains(self):
        '''
        Resets the domains of the board assuming no enforcement of constraints
        '''
        domains = {}
        variables = self.get_variables()
        for var in variables:
            if(self.config[var] == 0):
                domains[var] = [i for i in range(1,self.n+1)]
            else:
                domains[var] = [self.config[var]]
                
        self.domains = domains
                
        return domains
        
    def forward_checking(self, reassigned_variables):
        '''
        Runs the forward checking algorithm to restrict the domains of all variables based on the values
        of reassigned variables
        '''
        #======================================================================#
		#*#*#*# TODO: Write your implementation of forward checking here #*#*#*#
		#======================================================================#
        # print("before reduce")
        # print(self.domains)

        for var in reassigned_variables:
            assigned_value = self.config[var]  # Get the assigned value of the reassigned variable
            if assigned_value == 0:
                continue    # if this variable is not assigned, don't reduce it
            # reduce others domain if var is assigned
            # Get the row and column of the variable
            row = ROW.index(var[0])
            col = COL.index(var[1])
            
            # Forward check all variables in the same row
            for i in range(self.n):
                other_var = ROW[row] + COL[i]
                if other_var != var and assigned_value in self.domains[other_var]:
                    self.domains[other_var].remove(assigned_value)
            
            # Forward check all variables in the same column
            for i in range(self.n):
                other_var = ROW[i] + COL[col]
                if other_var != var and assigned_value in self.domains[other_var]:
                    self.domains[other_var].remove(assigned_value)
            
            # INEQUALITIES
            # reduce for inequalities. column inequalities. A1*
            if col < self.n - 1:  # Right neighbor
                ineq = ROW[row] + COL[col] + '*'
                right_var = ROW[row] + COL[col + 1]
                if ineq in self.config and self.config[ineq] == '<':    # var < right
                    # right_var should be greater than assigned_value
                    if self.config[right_var] != 0:  # If next var is assigned
                        if assigned_value >= self.config[right_var]:
                            return None
                    self.domains[right_var] = [num for num in self.domains[right_var] if num > assigned_value]
                elif ineq in self.config and self.config[ineq] == '>':  # var > right
                    # right_var should be smaller than assigned_Value
                    if self.config[right_var] != 0:  # If next var is assigned
                        if assigned_value <= self.config[right_var]:
                            return None
                    self.domains[right_var] = [num for num in self.domains[right_var] if num < assigned_value]
                    
            if col > 0:  # Left neighbor
                ineq = ROW[row] + COL[col - 1] + '*'    # ineq on the left neighbor
                left_var = ROW[row] + COL[col - 1]
                if ineq in self.config and self.config[ineq] == '<':    # left < var
                    # left_var should be smaller than assigned_value
                    if self.config[left_var] != 0:  # If next var is assigned
                        if self.config[left_var] >= assigned_value:
                            return None
                    self.domains[left_var] = [num for num in self.domains[left_var] if num < assigned_value]
                elif ineq in self.config and self.config[ineq] == '>':  # left > var
                    # left_var should be greater than assigned_value
                    if self.config[left_var] != 0:  # If next var is assigned
                        if self.config[left_var] <= assigned_value:
                            return None
                    self.domains[left_var] = [num for num in self.domains[left_var] if num > assigned_value]
            # reduce for inequalities. row inequalities. A*1
            if row < self.n - 1:  # Down neighbor
                ineq = ROW[row] + '*' + COL[col]    # ineq on var
                down_var = ROW[row + 1] + COL[col]
                if ineq in self.config and self.config[ineq] == '<':    # var < down_var
                    if self.config[down_var] != 0:  # If next var is assigned
                        if assigned_value >= self.config[down_var]:
                            return None
                    self.domains[down_var] = [num for num in self.domains[down_var] if num > assigned_value]
                    
                elif ineq in self.config and self.config[ineq] == '>':  # var > down_var
                    if self.config[down_var] != 0:  # If next var is assigned
                        if assigned_value <= self.config[down_var]:
                            return None
                    self.domains[down_var] = [num for num in self.domains[down_var] if num < assigned_value]
                    
            if row > 0:  # Up neighbor
                ineq = ROW[row - 1] + '*' + COL[col]    # ineq on up_var
                up_var = ROW[row - 1] + COL[col]
                if ineq in self.config and self.config[ineq] == '<':    # up_var < var
                    if self.config[up_var] != 0:  # If next var is assigned
                        if self.config[up_var] >= assigned_value:
                            return None
                    self.domains[up_var] = [num for num in self.domains[up_var] if num < assigned_value]
                elif ineq in self.config and self.config[ineq] == '>':  # up_var > var
                    if self.config[up_var] != 0:  # If next var is assigned
                        if self.config[up_var] <= assigned_value:
                            return None
                    self.domains[up_var] = [num for num in self.domains[up_var] if num > assigned_value]

        # print("after reduce")
        # print(self.domains)
        # edge case
        if any(len(self.domains[var]) < 1 for var in self.domains):
            # print("return None for ", var)
            return None
        return self  # Return the board if forward checking succeeded
        #=================================#
		#*#*#*# Your code ends here #*#*#*#
		#=================================#
        
    #=================================================================================#
	#*#*#*# Optional: Write any other functions you may need in the Board Class #*#*#*#
	#=================================================================================#
    def select_unassigned_variable(self):
        # select unassigned variable with smallest domain

        # select unassigned var
        unassigned_vars = [var for var in self.domains if (self.config[var] == 0)]
        # Sort unassigned variables based on the size of their domains
        unassigned_vars.sort(key=lambda var: len(self.domains[var]))
        # Return the variable with the smallest domain
        return unassigned_vars[0] if unassigned_vars else None  # Return None if no unassigned variable is found
        return None
    
    def create_solved_board(self):
        # debug check
        if any(len(board.domains[var]) != 1 for var in board.domains):
            print("some domain is not in size 1")
            exit(1)
            return
        # re-write config_str
        # replace entries of numbers with board.config[var] assigned number. other symbols remains
        new_config_str = ""
        # Iterate through the original config_str to maintain non-number entries
        index = 0  # To track position in the original config_str
        for r in ROW[:self.n]:
            for c in COL[:self.n]:
                var = r + c
                # Check if current character in config_str is a number (0 means unassigned)
                if self.config[var] != 0:
                    new_config_str += str(self.config[var])  # Assigned number
                    index += 1
                else:
                    # Maintain original characters (0 or other symbols) from config_str
                    new_config_str += self.config_str[index]
                    index += 1
                if c != COL[self.n - 1]:
                    new_config_str += self.config_str[index]
                    index += 1
        
            if r != ROW[self.n - 1]:
                new_config_str += self.config_str[index : index + self.n]  # Add separators (or adjust based on your format)
                index += self.n
        self.config_str = new_config_str
        return
    
    def is_complete(self):
        # return true if this board is complete
        # check by domain size
        # if all(len(board.domains[var]) == 1 for var in board.domains): check by domains will bring error :)?
        #     self.create_solved_board()
        #     return True
        # check by config assignment
        variables = self.get_variables()
        if all(board.config[var] != 0 for var in variables):
            board.create_solved_board()
            return True
        return False
    #=================================#
	#*#*#*# Your code ends here #*#*#*#
	#=================================#

#================================================================================#
#*#*#*# Optional: You may write helper functions in this space if required #*#*#*#
#================================================================================#        

#=================================#
#*#*#*# Your code ends here #*#*#*#
#=================================#

def backtracking(board):
    '''
    Performs the backtracking algorithm to solve the board
    Returns only a solved board
    '''
    #==========================================================#
	#*#*#*# TODO: Write your backtracking algorithm here #*#*#*#
	#==========================================================#
    
    # is board complete (each variables is not 0), then return board
    if board.is_complete():
        board.create_solved_board()
        return board
    
    # Select variable with smallest domain (MRV heuristic)
    var = board.select_unassigned_variable()
    # print(f"\nSelected variable: {var}")
    # print(f"Available values: {board.domains[var]}")
    
    if not var:
        return None
    # Try each value in the domain
    domain_values = list(board.domains[var])  # Make a copy of the domain values
    # Try each value in the domain
    for value in domain_values:
        # print(f"\nTrying {var} = {value}")
        # Create deep copies of current state
        original_config = board.config.copy()
        original_domains = {k: list(v) for k, v in board.domains.items()}  # Deep copy of domains
        
        # Assign value and check constraints
        board.config[var] = value
        result = board.forward_checking([var])
        
        if result:  # Forward checking succeeded
            # print(f"Forward checking passed for {var} = {value}")
            # Recursive call
            new_result = backtracking(board)
            if new_result:  # Solution found
                return new_result
            # print(f"Backtracking from {var} = {value}")  # Debug backtracking
        # else:
        #     print(f"Forward checking failed for {var} = {value}")
            
        # Restore state before trying next value
        board.config = original_config
        board.domains = original_domains
    
    # print(f"No valid value found for {var}, backtracking...")
    return None
    #=================================#
	#*#*#*# Your code ends here #*#*#*#
	#=================================#
    
def solve_board(board):
    '''
    Runs the backtrack helper and times its performance.
    Returns the solved board and the runtime
    '''
    #================================================================#
	#*#*#*# TODO: Call your backtracking algorithm and time it #*#*#*#
	#================================================================#
    start_time = time.time()
    # board.domains = board.reset_domains()  # Initialize domains once
    solved_board = backtracking(board)
    runtime = time.time() - start_time

    if solved_board:
        return solved_board, runtime
    else:
        return None, -1
    return None, -1 # Replace with return values
    #=================================#
	#*#*#*# Your code ends here #*#*#*#
	#=================================#

def print_stats(runtimes):
    '''
    Prints a statistical summary of the runtimes of all the boards
    '''
    min = 100000000000
    max = 0
    sum = 0
    n = len(runtimes)

    for runtime in runtimes:
        sum += runtime
        if(runtime < min):
            min = runtime
        if(runtime > max):
            max = runtime

    mean = sum/n

    sum_diff_squared = 0

    for runtime in runtimes:
        sum_diff_squared += (runtime-mean)*(runtime-mean)

    std_dev = np.sqrt(sum_diff_squared/n)

    print("\nRuntime Statistics:")
    print("Number of Boards = {:d}".format(n))
    print("Min Runtime = {:.8f}".format(min))
    print("Max Runtime = {:.8f}".format(max))
    print("Mean Runtime = {:.8f}".format(mean))
    print("Standard Deviation of Runtime = {:.8f}".format(std_dev))
    print("Total Runtime = {:.8f}".format(sum))


if __name__ == '__main__':
    if len(sys.argv) > 1:

        # Running futoshiki solver with one board $python3 futoshiki.py <input_string>.
        print("\nInput String:")
        print(sys.argv[1])
        
        print("\nFormatted Input Board:")
        board = Board(sys.argv[1])
        board.print_board()
        
        solved_board, runtime = solve_board(board)
        
        print("\nSolved String:")
        print(solved_board.get_config_str())
        
        print("\nFormatted Solved Board:")
        solved_board.print_board()
        
        print_stats([runtime])

        # Write board to file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")
        outfile.write(solved_board.get_config_str())
        outfile.write('\n')
        outfile.close()

    else:
        # Running futoshiki solver for boards in futoshiki_start.txt $python3 futoshiki.py

        #  Read boards from source.
        src_filename = 'futoshiki_start.txt'
        try:
            srcfile = open(src_filename, "r")
            futoshiki_list = srcfile.read()
            srcfile.close()
        except:
            print("Error reading the sudoku file %s" % src_filename)
            exit()

        # Setup output file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")
        
        runtimes = []

        # Solve each board using backtracking
        for line in futoshiki_list.split("\n"):
            
            print("\nInput String:")
            print(line)
            
            print("\nFormatted Input Board:")
            board = Board(line)
            board.print_board()
            
            solved_board, runtime = solve_board(board)
            runtimes.append(runtime)
            
            print("\nSolved String:")
            print(solved_board.get_config_str())
            
            print("\nFormatted Solved Board:")
            solved_board.print_board()

            # Write board to file
            outfile.write(solved_board.get_config_str())
            outfile.write('\n')

        # Timing Runs
        print_stats(runtimes)
        
        outfile.close()
        print("\nFinished all boards in file.\n")
