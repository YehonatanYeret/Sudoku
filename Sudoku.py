import pygame
import random
from arcade import sound as arcade

pygame.init()

# Constants
WINDOW_WIDTH = 720
WINDOW_HEIGHT = 720
MARGIN = 100
table_width = WINDOW_WIDTH - 2 * MARGIN
table_height = WINDOW_HEIGHT - 2 * MARGIN

FPS_SOLUTION = 5
FPS = 590
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BLUE = (173, 216, 230)
BLUE = (104, 185, 222)
LIGHT_RED = (179, 64, 76)
COLOR = LIGHT_RED
FONT = pygame.font.Font(None, 40)
IS_FINISH = False
IS_START = False
SPEED = 1

# Initialize the pygame
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
screen.fill(WHITE)
pygame.display.set_caption("Sudoku")
clock = pygame.time.Clock()


# Algorithm ############################################################################################################


# Function to calculate the possible values for a cell
def calculate_possible_values(grid, cell):
    row, col = cell
    used_values = set()

    # Check the row
    for i in range(9):
        if grid[row][i] != 0:
            used_values.add(grid[row][i])

    # Check the column
    for i in range(9):
        if grid[i][col] != 0:
            used_values.add(grid[i][col])

    # Check the box
    box_row = row // 3
    box_col = col // 3
    for i in range(3):
        for j in range(3):
            if grid[box_row * 3 + i][box_col * 3 + j] != 0:
                used_values.add(grid[box_row * 3 + i][box_col * 3 + j])

    # Calculate the possible values for the cell
    possible_values = [i for i in range(1, 10) if i not in used_values]
    return possible_values


# Generate the sudoku CSP solver
def generate_sudoku_csp(arr):
    # Initialize the grid with zeros
    grid = [[[0, []] for _ in range(9)] for _ in range(9)]

    for i in range(9):
        for j in range(9):
            grid[i][j] = [arr[i][j], calculate_possible_values(arr, (i, j))]

    return grid


# Function to update the grid with the possible values after each step (only for who that effected from the last step)
def update_grid(grid, cell):
    row, col = cell

    num = grid[row][col][0]

    # Update the row
    for i in range(9):
        if grid[row][i][0] == 0 and num in grid[row][i][1]:
            grid[row][i][1].remove(num)

    # Update the column
    for i in range(9):
        if grid[i][col][0] == 0 and num in grid[i][col][1]:
            grid[i][col][1].remove(num)

    # Update the box
    box_row = row // 3
    box_col = col // 3
    for i in range(3):
        for j in range(3):
            if grid[box_row * 3 + i][box_col * 3 + j][0] == 0 and num in grid[box_row * 3 + i][box_col * 3 + j][1]:
                grid[box_row * 3 + i][box_col * 3 + j][1].remove(num)


# Function to find the cell with the minimum number of possible values
def find_min_possible_values_cell(grid):
    min_cells = []
    min_values = 10  # Initialize with a value greater than the maximum possible values (9)

    for i in range(9):
        for j in range(9):
            # Find all the empty cells with the minimum number of possible values
            if grid[i][j][0] == 0 and len(grid[i][j][1]) == min_values:
                min_cells.append((i, j))

            # if the cell is empty and has less possible values than the current minimum
            # then update the minimum and the cells
            elif grid[i][j][0] == 0 and len(grid[i][j][1]) < min_values:
                min_values = len(grid[i][j][1])
                min_cells = [(i, j)]

    return min_cells


# Function to find the cell that effecting the most cells
def find_most_effecting_cell(grid, min_cells):
    # If their only one cell with the minimum number of possible values
    if len(min_cells) == 1:
        return min_cells[0]

    # Find the cell that effecting the most cells
    max_effected_cells = 0
    most_effecting_cell = min_cells[0]
    for cell in min_cells:
        row, col = cell
        effected_cells = 0

        # Check the row
        for i in range(9):
            if grid[row][i][0] == 0:
                effected_cells += 1

        # Check the column
        for i in range(9):
            if grid[i][col][0] == 0:
                effected_cells += 1

        # Check the box
        box_row = row // 3
        box_col = col // 3
        for i in range(3):
            for j in range(3):
                if grid[box_row * 3 + i][box_col * 3 + j][0] == 0:
                    effected_cells += 1

        # Update the most effecting cell
        if effected_cells > max_effected_cells:
            max_effected_cells = effected_cells
            most_effecting_cell = cell

    return most_effecting_cell


# Function to find the val that least effecting on the other cells
def find_least_effecting_value(grid, cell):
    row, col = cell

    if len(grid[row][col][1]) == 0:
        return 0

    min_effected_cells = 10  # Initialize with a value greater than the maximum possible values (9)
    least_effecting_value = grid[row][col][1][0]  # Initialize with the first possible value

    for val in grid[row][col][1]:
        effected_cells = 0

        # Check the row
        for i in range(9):
            if grid[row][i][0] == 0 and val in grid[row][i][1]:
                effected_cells += 1

        # Check the column
        for i in range(9):
            if grid[i][col][0] == 0 and val in grid[i][col][1]:
                effected_cells += 1

        # Check the box
        box_row = row // 3
        box_col = col // 3
        for i in range(3):
            for j in range(3):
                if grid[box_row * 3 + i][box_col * 3 + j][0] == 0 and val in grid[box_row * 3 + i][box_col * 3 + j][1]:
                    effected_cells += 1

        # Update the least effecting value
        if effected_cells < min_effected_cells:
            min_effected_cells = effected_cells
            least_effecting_value = val

    return least_effecting_value


# Function to check if the sudoku is solved
def is_solved(grid):
    for i in range(9):
        for j in range(9):
            if grid[i][j][0] == 0:
                return False
    return True


# Function to solve the sudoku using backtracking
def solution(grid):
    # Find the cell with the minimum number of possible values
    min_cells = find_min_possible_values_cell(grid)

    # If there are no empty cells, the Sudoku is solved
    if len(min_cells) == 0:
        return True

    # Find the cell that affects the most cells
    cell = find_most_effecting_cell(grid, min_cells)

    # Find the value that least affects other cells
    val = find_least_effecting_value(grid, cell)

    # If no valid value is found, return False (no solution)
    if val == 0:
        return False

    # Assign the value to the cell
    grid[cell[0]][cell[1]][0] = val

    # Update the grid with the possible values
    update_grid(grid, cell)

    if IS_START:
        display_number(grid, cell[0], cell[1], fps=FPS_SOLUTION)

    # Recursively solve the grid
    if solution(grid):
        return True

    # Backtrack: Reset the cell and restore the possible values
    grid[cell[0]][cell[1]][0] = 0
    grid[cell[0]][cell[1]][1].append(val)

    if IS_START:
        display_number(grid, cell[0], cell[1], fps=FPS_SOLUTION)

    # Recalculate the possible values for the affected cells
    update_grid(grid, cell)

    # If no solution is found, return False
    return False


# Function to find if some move is possible
def is_safe(arr, col, row, num):
    # Check if the number is already in the row
    for x in range(9):
        if arr[row][x] == num:
            return False

    # Check if the number is already in the column
    for x in range(9):
        if arr[x][col] == num:
            return False

    # Check if the number is already in the 3x3 box
    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if arr[i + start_row][j + start_col] == num:
                return False

    return True


# Function to clear the grid
def clear_grid(grid):
    for i in range(9):
        for j in range(9):
            grid[i][j][0] = 0
            grid[i][j][1] = []


def generate_sudoku(grid):
    attempts = 30
    for i in range(attempts):
        print(f"Attempt {i + 1} of {attempts}")
        clear_grid(grid)  # Reset the grid
        numbers = list(range(1, 10))  # Numbers 1-9
        fill_grid(grid, numbers)
        remove_numbers(grid)  # Remove some numbers to create the puzzle

        # Create a copy of the grid in 1 dimension without the possible values
        check_arr = [[grid[i][j][0] for j in range(9)] for i in range(9)]
        temp_grid = generate_sudoku_csp(check_arr)  # Update the grid with the possible values
        # Check if the Sudoku can be solved
        if solution(temp_grid):
            return True, generate_sudoku_csp(check_arr)

    return False, grid


def fill_grid(grid, numbers):
    # Find the first empty cell
    for row in range(9):
        for col in range(9):
            if grid[row][col][0] == 0:
                random.shuffle(numbers)  # Shuffle numbers for randomness
                for num in numbers:
                    if is_safe([[cell[0] for cell in row] for row in grid], col, row, num):
                        grid[row][col][0] = num
                        update_grid(grid, (row, col))  # Update possible values
                        if fill_grid(grid, numbers):  # Recursively fill the grid
                            return True
                        grid[row][col][0] = 0  # Backtrack
                return False
    return True


def remove_numbers(grid):
    # Randomly remove numbers from the grid
    i = 0
    attempts = random.randint(50, 65)
    while i < attempts:
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        if grid[row][col][0] != 0:
            grid[row][col][0] = 0
            update_grid(grid, (row, col))  # Update possible values
            i += 1


# GUI ###############################################################################################################


# Function to draw the grid
def draw_grid():
    for i in range(1, 9):
        if i % 3 == 0:
            pygame.draw.line(screen, BLACK, (i * table_width // 9 + MARGIN, MARGIN),
                             (i * table_width // 9 + MARGIN, WINDOW_HEIGHT - MARGIN), 3)
            pygame.draw.line(screen, BLACK, (MARGIN, i * table_height // 9 + MARGIN),
                             (WINDOW_WIDTH - MARGIN, i * table_height // 9 + MARGIN), 3)
        else:
            pygame.draw.line(screen, BLACK, (i * table_width // 9 + MARGIN, MARGIN),
                             (i * table_width // 9 + MARGIN, WINDOW_HEIGHT - MARGIN), 1)
            pygame.draw.line(screen, BLACK, (MARGIN, i * table_height // 9 + MARGIN),
                             (WINDOW_WIDTH - MARGIN, i * table_height // 9 + MARGIN), 1)


# Function to print the sudoku
def print_sudoku(arr):
    for i in range(9):
        for j in range(9):
            if arr[i][j][0] != 0:
                text = FONT.render(str(arr[i][j][0]), True, BLACK)
                screen.blit(text, (j * table_width // 9 + 20 + MARGIN, i * table_height // 9 + 20 + MARGIN))

                pygame.display.flip()
                clock.tick(FPS)


# Function to draw the solve button
def draw_solve_button():
    pygame.draw.rect(screen, BLUE, (WINDOW_WIDTH // 2 - 50, WINDOW_HEIGHT - 70, 100, 60))
    text = FONT.render("Solve", True, WHITE)
    screen.blit(text, (WINDOW_WIDTH // 2 - 35, WINDOW_HEIGHT - 50))


# Function to display the screen
def display_screen(arr, fps=FPS):
    screen.fill(WHITE)  # Clear the screen
    draw_grid()  # Redraw the grid
    print_sudoku(arr)  # Print the updated sudoku
    draw_solve_button()  # Redraw the solve button
    pygame.display.flip()
    clock.tick(fps)


# Function to display only one number
def display_number(arr, row, col, fps=FPS):
    # Clear the location
    # Display the number in the correct location
    pygame.draw.rect(screen, WHITE,
                     (col * table_width // 9 + 20 + MARGIN, row * table_height // 9 + 20 + MARGIN,
                      table_width // 9 - 30, table_height // 9 - 30))

    # If the number is 0 -> we don't need to display it
    if arr[row][col][0] != 0:
        # Display the number in the correct location
        screen.blit(FONT.render(str(arr[row][col][0]), True, COLOR),
                    (col * table_width // 9 + 20 + MARGIN, row * table_height // 9 + 20 + MARGIN))

    # update the screen
    pygame.display.update(col * table_width // 9 + MARGIN + 0.1, row * table_height // 9 + MARGIN + 0.1,
                          (col + 1) * table_width // 9 + MARGIN - 0.1, (row + 1) * table_height // 9 + MARGIN - 0.1)

    clock.tick(fps)


# Function to display the speed options
def display_speed_options():
    # Display the options
    speed_font = pygame.font.Font(None, 20)
    text = speed_font.render("Choose the speed:", True, BLACK)
    screen.blit(text, (20, 10))

    pygame.draw.line(screen, LIGHT_BLUE, (55, 50), (105, 50), 2)

    for i in range(1, 4):
        if i == SPEED:
            pygame.draw.circle(screen, BLUE, (25 * i + 30, 50), 10)
        else:
            pygame.draw.circle(screen, LIGHT_BLUE, (25 * i + 30, 50), 10)

        text = speed_font.render(str(i), True, BLACK)
        screen.blit(text, (25 * i + 26, 44))

    pygame.display.flip()


# Function that start the solution of the sudoku
def start_solution(grid):
    # Play sound when the user press the solve button
    sound = arcade.Sound("solution_audio.wav", True)
    play = arcade.play_sound(sound, 0.2, 0, True, 1)

    # Clear the screen
    screen.fill(WHITE)
    pygame.display.flip()
    clock.tick(FPS)

    # Show that we are in solution
    text = FONT.render("Solving...", True, BLACK)
    screen.blit(text, (WINDOW_WIDTH // 2 - 50, 30))

    # Display the grid
    draw_grid()
    pygame.display.flip()
    display_speed_options()
    clock.tick(FPS)

    # Restart the grid parameters
    arr = [[grid[i][j][0] for j in range(9)] for i in range(9)]
    grid = generate_sudoku_csp(arr)  # Update the grid with the possible values

    # Start the solution
    print_sudoku(grid)
    finish = solution(grid)

    print_finish(finish, grid)

    # Stop the sound
    arcade.stop_sound(play)


# Function to print the finish message
def print_finish(finish, grid):
    global IS_FINISH

    # Hide the old text
    pygame.draw.rect(screen, WHITE, (WINDOW_WIDTH // 2 - 150, 10, 300, 60))

    # Show the result
    if finish:
        text = FONT.render("Solved!", True, BLACK)
    else:
        text = FONT.render("No Solution!", True, BLACK)

    screen.blit(text, (WINDOW_WIDTH // 2 - 50, 30))
    pygame.display.update(WINDOW_WIDTH // 2 - 100, 0, 300, 70)

    IS_FINISH = True


# Function that mark the box that the user picked
def mark_box(row, col, last_row=-1, last_col=-1):
    if IS_FINISH:
        return

    # Make sound when the user pick a box
    sound = arcade.Sound("moving_box_sound.wav", True)
    arcade.Sound.play(sound, 0.1, 0, False, 30)

    # Clear the last box
    # Display the last number
    if last_row != -1 and last_col != -1:
        pygame.draw.rect(screen, WHITE,
                         (last_col * table_width // 9 + MARGIN + 1, last_row * table_height // 9 + MARGIN + 1,
                          table_width // 9 - 1, table_height // 9 - 1), 3)

    draw_grid()

    # Mark the new box
    pygame.draw.rect(screen, LIGHT_BLUE,
                     (col * table_width // 9 + MARGIN + 1, row * table_height // 9 + MARGIN + 1,
                      table_width // 9 - 1, table_height // 9 - 1), 3)

    pygame.display.flip()


# main func
def main():
    global IS_START
    global FPS_SOLUTION
    global SPEED

    # The location that the user picked
    row = -1
    col = -1

    # The sudoku grid
    grid = [[[0, []] for _ in range(9)] for _ in range(9)]

    IS_START, grid = generate_sudoku(grid)
    if not IS_START:
        arr = [[5, 3, 0, 0, 7, 0, 0, 0, 0],
               [6, 0, 0, 1, 9, 5, 0, 0, 0],
               [0, 9, 8, 0, 0, 0, 0, 6, 0],
               [8, 0, 0, 0, 6, 0, 0, 0, 3],
               [4, 0, 0, 8, 0, 3, 0, 0, 1],
               [7, 0, 0, 0, 2, 0, 0, 0, 6],
               [0, 6, 0, 0, 0, 0, 2, 8, 0],
               [0, 0, 0, 4, 1, 9, 0, 0, 5],
               [0, 0, 0, 0, 8, 0, 0, 7, 9]]

        grid = generate_sudoku_csp(arr)

    display_screen(grid)
    display_speed_options()

    IS_START = True

    while True:
        for event in pygame.event.get():

            # if the user wants to quit
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # if the user wants to pick a box or change the speed
            if event.type == pygame.MOUSEBUTTONDOWN and IS_FINISH is False:

                x, y = pygame.mouse.get_pos()

                if WINDOW_WIDTH // 2 - 50 <= x <= WINDOW_WIDTH // 2 + 50 and WINDOW_HEIGHT - 100 <= y <= WINDOW_HEIGHT:
                    start_solution(grid)

                # if the user wants to change the speed
                elif 20 <= x <= 70 and 40 <= y <= 60:
                    FPS_SOLUTION = 5
                    SPEED = 1
                    display_speed_options()
                elif 45 <= x <= 95 and 40 <= y <= 60:
                    FPS_SOLUTION = 30
                    SPEED = 2
                    display_speed_options()
                elif 70 <= x <= 120 and 40 <= y <= 60:
                    FPS_SOLUTION = 280
                    SPEED = 3
                    display_speed_options()

                else:
                    last_row = row
                    last_col = col

                    # if the location is out of the grid
                    if x < MARGIN or x > WINDOW_WIDTH - MARGIN or y < MARGIN or y > WINDOW_HEIGHT - MARGIN:
                        row = -1
                        col = -1
                    else:
                        row = (y - MARGIN) // (table_height // 9)
                        col = (x - MARGIN) // (table_width // 9)
                        mark_box(row, col, last_row, last_col)

                print(row, col)

            # if the user wants to move with the arrows
            if event.type == pygame.KEYDOWN and row != -1 and col != -1 and IS_FINISH is False:

                # save the last location
                last_row = row
                last_col = col

                if event.key == pygame.K_UP:
                    row = (row - 1) % 9
                elif event.key == pygame.K_DOWN or event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
                    row = (row + 1) % 9
                elif event.key == pygame.K_LEFT:
                    col = (col - 1) % 9
                elif event.key == pygame.K_RIGHT:
                    col = (col + 1) % 9
                elif event.key == pygame.K_TAB:
                    if col == 8:
                        row = (row + 1) % 9
                    col = (col + 1) % 9

                # mark the new box
                mark_box(row, col, last_row, last_col)

            # if the user wants to insert a number
            if event.type == pygame.KEYDOWN and row != -1 and col != -1 and IS_FINISH is False:

                # save the number that was in the location
                num = grid[row][col][0]

                if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                    grid[row][col][0] = 1
                elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                    grid[row][col][0] = 2
                elif event.key == pygame.K_3 or event.key == pygame.K_KP3:
                    grid[row][col][0] = 3
                elif event.key == pygame.K_4 or event.key == pygame.K_KP4:
                    grid[row][col][0] = 4
                elif event.key == pygame.K_5 or event.key == pygame.K_KP5:
                    grid[row][col][0] = 5
                elif event.key == pygame.K_6 or event.key == pygame.K_KP6:
                    grid[row][col][0] = 6
                elif event.key == pygame.K_7 or event.key == pygame.K_KP7:
                    grid[row][col][0] = 7
                elif event.key == pygame.K_8 or event.key == pygame.K_KP8:
                    grid[row][col][0] = 8
                elif event.key == pygame.K_9 or event.key == pygame.K_KP9:
                    grid[row][col][0] = 9
                elif event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                    grid[row][col][0] = 0

                display_number(grid, row, col, num)


if __name__ == '__main__':
    main()
