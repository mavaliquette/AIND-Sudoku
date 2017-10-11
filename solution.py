import itertools
"""
    Defintion of variables to build and set up a sudoku
"""
# Define rows and columns as strings
def cross(A, B):
    return [s + t for s in A for t in B]
rows = 'ABCDEFGHI'
cols = '123456789'
# Define boxes
boxes = cross(rows, cols)
# Define row units
row_units = [cross(r, cols) for r in rows]
# Define column units
column_units = [cross(rows, c) for c in cols]
# Define square units  - Square of 3X3
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
# Define diagonal units
diagonal_units = [[rows[i] + cols[i] for i in range(9)], [rows[::-1][i] + cols[i] for i in range(9)]]
#d_units1 = [[rows[i] + cols[i] for i in range(len(rows))]]
#d_units2 = [[rows[i] + cols[-i - 1] for i in range(len(rows))]]
#diagonal_units = d_units1 + d_units2

unitlist = row_units + column_units + square_units + diagonal_units

# Create a dictionary of peers of each box
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], [])) - set([s])) for s in boxes)

assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    # Don't waste memory appending actions that don't actually change any values
    # if values[box] == value:
    #  return values
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

    # -------------------------------------------------------------------------------------------------

"""
    The naked_twins function eliminates values using the naked twins strategy.
    Input:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
    Output:
        the values dictionary with the naked twins eliminated from peers.
"""

def naked_twins(values):
    for unit in unitlist:

        # Find all boxes with two digits remaining as possibilities
        pairs = [box for box in unit if len(values[box]) == 2]
        # Pairwise combinations
        poss_twins = [list(pair) for pair in itertools.combinations(pairs, 2)]
        for pair in poss_twins:
            box1 = pair[0]
            box2 = pair[1]
            # Find the naked twins
            if values[box1] == values[box2]:
                for box in unit:
                    # Eliminate the naked twins as possibilities for peers
                    if box != box1 and box != box2:
                        for digit in values[box1]:
                            values[box] = values[box].replace(digit,'')
    return values

    # ---------------------------------------------------------------------------------------------------

"""
    The function grid_values converts grid into a dict of {square: char} with '123456789' for empties.
    Input:
        grid(string) - A grid in string form.
    Output:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.     
 """
def grid_values(grid):
    # Define char as a matrix to put values in
    chars = []
    # Define variable empty_box
    values_empty_box = '123456789'
    # Loop for in grid if empty '.' replace it with values_empty_box
    for i in grid:
        if i in values_empty_box:
            chars.append(i)
        elif i == '.':
            chars.append(values_empty_box)
            # Making sure that the size match : 81 values in a Sudoku 9x9
    assert len(chars) == 81
    return dict(zip(boxes, chars))
# -----------------------------------------------------------------------------------------------------------------
# I took this portion of the code in the exercise provided by Udacity
def display(values):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    print
# ----------------------------------------------------------------------------------------------------------------
"""
    This function eliminate values from peers of each box with a single solved value
    Input:
        values: Sudoku in dictionary form.
    Output:
        Resulting Sudoku in dictionary form after eliminating values.
"""
def eliminate(values):
    # Assign solved_values to the assigned digit by going from box to box
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for solved_val_box in solved_values:
        # Assign this value to digit
        digit = values[solved_val_box]
        # print("digit", values[box])
        # For each peers associated with a particular box, eliminate that digit
        for peer in peers[solved_val_box]:
            values[peer] = values[peer].replace(digit,'')
            #assign_value(values, peer, values[peer].replace(digit,''))
    return values
# -----------------------------------------------------------------------------------------------------------------
"""
    The function only_choice finalizes all values that are the only choice for a unit.

    Go through all the units, and when there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: 
        Sudoku in dictionary form.
    Output: 
        Resulting Sudoku in dictionary form after filling in only choices.
"""


def only_choice(values):
    # For each "set" of cols, rows and 3X3 square
    for unit in unitlist:
        for digit in '123456789':
            # Assign dplaces as the assigned digit in that solved box
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values
# -------------------------------------------------------------------------------------------------------------------
"""
    This function reduce_puzzle iterates eliminate() and only_choice() untilthe sudoku remains the same, 
    then it will return the solved sudoku.
    If there is a box with no available values, there is a mistake or the soduku is unsolvable, 
    the function will return False.
    Input: 
        A sudoku in dictionary form.
    Output: 
        The resulting sudoku in dictionary form.
"""
# I took this portion of the code in the exercise provided by Udacity
def reduce_puzzle(values):
    # Check how many boxes have a determined value

    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # print(solved_values_before)
        # Use the Eliminate Strategy
        values = eliminate(values)
        # print("values_eliminate", type(eliminate(values)))
        #print("values_eliminate", eliminate(values))
        # Use the Only Choice Strategy
        values = only_choice(values)
        # print("values_only_choice", type(only_choice(values)))
        # Use the Naked Twins Strategy
        values = naked_twins(values)
        # print("values_naked_twins", type(naked_twins(values)))
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        #print("solved_values_after", solved_values_after)
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
            # print("values_type", type(values))
    return values

# --------------------------------------------------------------------------------------------------------------------
"""
    The function search uses depth-first search and propagation. 
    It finds the box with a minimal number of possible values and solves each of the puzzles obtained by choosing each
    of these values recursively.
    Input:
        A sudoku in dictionary form. 
    Output:
        The resulting sudoku in dictionary form.
"""

# I took this portion of the code in the exercise provided by Udacity
def search(values):
    values = reduce_puzzle(values)
    #print("values", values)
    if values is False:
        return False  ## Failed earlier

    if all(len(values[s]) == 1 for s in boxes):
        return values  ## Solved!

    # Choose one of the unfilled squares with the fewest possibilities
    n, s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt
        # ------------------------------------------------------------------------------------------------------------------
"""
    The function solve finds the solution to a Sudoku grid.
    Input:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Output:
        The dictionary representation of the final sudoku grid. False if no solution exists.
"""
def solve(grid):

    values_grid = grid_values(grid)
    #print("values", values)
    values = search(values_grid)
    return values
    #print("search(values)", search(values))
    #solve('9.1....8.8.5.7..4.2.4....6...7......5..............83.3..6......9................')

if __name__ == '__main__':
    diag_sudoku_grid ='2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    #diag_sudoku_grid = '9.1....8.8.5.7..4.2.4....6...7......5..............83.3..6......9................'
    values = grid_values(diag_sudoku_grid)
    print("values",values)
    display(solve(diag_sudoku_grid))

try:
    from visualize import visualize_assignments
    visualize_assignments(assignments)
except SystemExit:
            pass
except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
