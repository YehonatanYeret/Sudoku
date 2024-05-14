from arcade import sound as arcade
import pygame
import random

pygame.init()

# Constants
WINDOW_WIDTH = 720
WINDOW_HEIGHT = 720
MARGIN = 100
table_width = WINDOW_WIDTH - 2 * MARGIN
table_height = WINDOW_HEIGHT - 2 * MARGIN

FPS_SOLUTION = 2920
FPS = 720
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BLUE = (173, 216, 230)
BLUE = (104, 185, 222)
LIGHT_RED = (179, 64, 76)
COLOR = LIGHT_RED
FONT = pygame.font.Font(None, 40)
IS_FINISH = False
IS_START = False
SPEED = 3

# Initialize the pygame
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
screen.fill(WHITE)
pygame.display.set_caption("Sudoku")
clock = pygame.time.Clock()


# Algorithm############################################################################################################

# Function to find an empty location in the grid
def find_empty_location(arr, l):
    for row in range(9):
        for col in range(9):
            if arr[row][col] == 0:
                l[0] = row
                l[1] = col
                return True
    return False


# Function to check if the number is in the row
def is_used_in_row(arr, row, num):
    for i in range(9):
        if arr[row][i] == num:
            return True
    return False


# Function to check if the number is in the column
def is_used_in_col(arr, col, num):
    for i in range(9):
        if arr[i][col] == num:
            return True
    return False


# Function to check if the number is used in the box (3x3 grid)
def is_used_in_box(arr, box_col, box_row, num):
    for i in range(3):
        for j in range(3):
            if arr[box_row * 3 + i][box_col * 3 + j] == num:
                return True
    return False


# Function that check if the place is safe
def is_safe(arr, col, row, num):
    return (not is_used_in_row(arr, row, num) and
            not is_used_in_col(arr, col, num) and
            not is_used_in_box(arr, col // 3, row // 3, num))


# Function that solve the sudoku
def solution(arr):
    # l is for the location that we in the middle of solving
    l = [0, 0]

    # if there is no empty locations at the sudoku
    if not find_empty_location(arr, l):
        return True

    # the next empty location
    row = l[0]
    col = l[1]

    # go through all the numbers between 1 and 9 and try to insert them into [row, col]
    for num in range(1, 10):

        # if the location is safe -> insert the number
        if is_safe(arr, col, row, num):
            arr[row][col] = num
            if IS_START:
                display_number(arr, row, col, fps=FPS_SOLUTION)

            # the recursion part, go to try the next location
            if solution(arr):
                return True

            # if the recursion return back without solution -> we need to
            # try again that place
            arr[row][col] = 0
            if IS_START:
                display_number(arr, row, col, fps=FPS_SOLUTION)

    # if we go through the numbers and there is no solution
    return False


# Generate the sudoku #############################################################################################

# Function to clear the grid
def clear_grid(grid):
    for i in range(9):
        for j in range(9):
            grid[i][j] = 0


# Function to generate the sudoku
def generate_sudoku(grid):
    clear_grid(grid)
    for i in range(40):
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        num = random.randint(1, 9)
        if is_safe(grid, col, row, num):
            grid[row][col] = num
        else:
            i -= 1

    # Copy the grid to check if there is a solution
    check_arr = [[grid[i][j] for j in range(9)] for i in range(9)]

    return solution(check_arr)


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
            if arr[i][j] != 0:
                text = FONT.render(str(arr[i][j]), True, BLACK)
                screen.blit(text, (j * table_width // 9 + 20 + MARGIN, i * table_height // 9 + 20 + MARGIN))

                pygame.display.flip()
                clock.tick(FPS_SOLUTION)


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
    if arr[row][col] != 0:
        # Display the number in the correct location
        screen.blit(FONT.render(str(arr[row][col]), True, COLOR),
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
    clock.tick(FPS_SOLUTION)

    # Show that we are in solution
    text = FONT.render("Solving...", True, BLACK)
    screen.blit(text, (WINDOW_WIDTH // 2 - 50, 30))

    # Display the grid
    draw_grid()
    pygame.display.flip()
    display_speed_options()
    clock.tick(FPS_SOLUTION)

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
    grid = [[0 for _ in range(9)] for _ in range(9)]
    grid = [[5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]]

    # IS_START = generate_sudoku(grid)
    # while not IS_START:
    #     IS_START = generate_sudoku(grid)

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
                    FPS_SOLUTION = 90
                    SPEED = 1
                    display_speed_options()
                elif 45 <= x <= 95 and 40 <= y <= 60:
                    FPS_SOLUTION = 720
                    SPEED = 2
                    display_speed_options()
                elif 70 <= x <= 120 and 40 <= y <= 60:
                    FPS_SOLUTION = 2920
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
                num = grid[row][col]

                if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                    grid[row][col] = 1
                elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                    grid[row][col] = 2
                elif event.key == pygame.K_3 or event.key == pygame.K_KP3:
                    grid[row][col] = 3
                elif event.key == pygame.K_4 or event.key == pygame.K_KP4:
                    grid[row][col] = 4
                elif event.key == pygame.K_5 or event.key == pygame.K_KP5:
                    grid[row][col] = 5
                elif event.key == pygame.K_6 or event.key == pygame.K_KP6:
                    grid[row][col] = 6
                elif event.key == pygame.K_7 or event.key == pygame.K_KP7:
                    grid[row][col] = 7
                elif event.key == pygame.K_8 or event.key == pygame.K_KP8:
                    grid[row][col] = 8
                elif event.key == pygame.K_9 or event.key == pygame.K_KP9:
                    grid[row][col] = 9
                elif event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                    to_print = True
                    grid[row][col] = 0

                display_number(grid, row, col, num)


if __name__ == '__main__':
    main()
