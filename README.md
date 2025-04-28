# Sudoko Solver

###### By Yehonatan Yeret

## Description

This is a simple Sudoku solver that uses backtracking to find a solution to a given Sudoku puzzle. The program takes a
9x9 grid as input, where empty cells are represented by 0s, and fills in the grid with the correct numbers according to
Sudoku rules.

The Sudoko is generated using the `generate_sudoku` function, which creates a random Sudoku puzzle with a unique
solution. The program also includes a function to print the Sudoku grid in a readable format.

The algorithm is `CSP (Constraint Satisfaction Problem)` based, which means it uses constraints to reduce the search
space and find a solution more efficiently. The program also includes a function to check if a number can be placed in a
given cell without violating Sudoku rules.

## Algorithm

* step 1. find all the cells that have the the minimum number of possibilities, the
  func: `find_min_possible_values_cell()`.


* step 2. from those cells, find the cell that effects the most cells, the func: `find_most_effecting_cell()`.


* step 3. assign the cell with the value that will effect the least number of cells, the
  func: `find_least_effecting_value()`.

Then the algorithm will repeat itself until it finds a solution or there are no more cells to assign values to.

## Usage

There is 2 options to use the program:

1. with your own Sudoku puzzle:

```python
from Sudoku import sudoko_solver

sudoku = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]
# Solve the Sudoku puzzle
solution = sudoko_solver(sudoku)
```

2. or just let the program generate a random Sudoku puzzle for you:

```python
from Sudoku import sudoko_solver

# Solve the Sudoku puzzle
solution = sudoko_solver()
```


## Requirements
* Python3
* pygame (for the GUI)
* arcade (for the sound in the game)

## Installation
```bash
pip install pygame
pip install arcade
```

## Run the program
```bash
python main.py
```
## GUI
The GUI is built using the `pygame` library. The program displays the Sudoku grid and allows the user to input numbers
by clicking on the cells. Or moving with the arrow keys.

The program includes a button for choosing a speed (1-3, default is 1).

* 1 - slow (5 FPS)
* 2 - medium (30 FPS)
* 3 - fast (280 FPS)

## Sound
The program includes sound effects for the following events:
* When the user changes the sell with the arrow keys or clicks on a cell.
* When the user starts the solution process.

## Credits
* [pygame](https://www.pygame.org/) - for the GUI
* [arcade](https://arcade.academy/) - for the sound
* [Sudoku](https://en.wikipedia.org/wiki/Sudoku) - for the game rules
* *Lev Academic Center (JCT)* - for the course (introduction to AI and data science)
