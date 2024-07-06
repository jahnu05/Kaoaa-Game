"""Python game interpretation of kaooa game"""

import turtle
import math


class Game:
    """Contains all functions of game"""
    def __init__(self, indexed_indices, neighbouring_indices):
        self.board = {index: None for index in indexed_indices}
        self.crows_placed = 0
        self.vulture_placed = False
        self.vulture_position = None
        self.crows_killed = 0
        self.neighbours = neighbouring_indices

    def place_crow(self, index):
        """ function to place crow on the board"""
        if index != -1 and self.board[index] is None:
            self.board[index] = 'crow'
            self.crows_placed += 1
            return True
        return False

    def place_vulture(self, index):
        """Function to place vulture on the board"""
        if self.board[index] is None:
            self.board[index] = 'vulture'
            self.vulture_placed = True
            self.vulture_position = index
            return True
        return False

    def move_vulture(self, old_index, new_index):
        """Function to move vulture"""
        if self.board[old_index] == 'vulture' and self.board[new_index] is None:
            for neighbour, next_neighbour in neighbours.get(old_index, []):
                if new_index == neighbour:  # If the new index is a neighbour and is empty
                    self.board[old_index] = None
                    toggle_button_color(old_index)
                    self.board[new_index] = 'vulture'
                    self.vulture_position = new_index
                    return True
                if neighbour in self.board and next_neighbour in self.board:
                    # Check if neighbour and next_neighbour are valid keys
                    if self.board[neighbour] == 'crow' and self.board[next_neighbour] is None:
                        if new_index == next_neighbour:
                            # If the new index is the next nearest neighbour of a crow and is empty
                            self.board[neighbour] = None
                            self.crows_killed += 1
                            toggle_button_color(neighbour)
                            self.board[old_index] = None
                            toggle_button_color(old_index)
                            self.board[new_index] = 'vulture'
                            self.vulture_position = new_index
                            return True
        return False

    def move_crow(self, old_index, new_index):
        """Function to move crow"""
        if self.board[old_index] == 'crow' and self.board[new_index] is None:
            for neighbour, _ in neighbours.get(old_index, []):
                if new_index == neighbour:
                    self.board[old_index] = None
                    toggle_button_color(old_index)
                    self.board[new_index] = 'crow'
                    return True
        return False

    def decide_win(self, index):
        """Function to decide winner"""
        # print(index)
        if self.crows_killed >= 4:
            return "Vulture"  # Vulture wins if 4 crows are killed
        if index is not None:
            for neighbour, next_neighbour in neighbours.get(self.vulture_position, []):
                if self.board[neighbour] is None or (
                    next_neighbour != 0 and self.board[next_neighbour] is None
                ):
                    return None  # No winner yet if vulture has open moves
            return "Crow"  # Crow wins if vulture has no open moves
        return None


def is_click_inside_button(x_position, y_position, x_button, y_button):
    """Function to determine if click is inside the circle"""
    distance = math.sqrt((x_position - x_button)**2 + (y_position - (y_button+15))**2)
    return distance <= 30


def get_index(position):
    """ To get index of the point"""
    for index, curr_point in indexed_pts.items():
        if curr_point == position:
            return index
    return -1


SELECTED_CROW = None
SELECTED_VULTURE = None  # Define SELECTED_VULTURE as a global variable
pen = turtle.Turtle()
pen.reset()
pen.penup()
pen.color('#FAF0E6')
pen.hideturtle()


def on_click(x_pos, y_pos):
    """Function to determine the next step after clicking"""
    global SELECTED_CROW, SELECTED_VULTURE
    # Add SELECTED_VULTURE to the global variables
    for position, (but_x, but_y) in intersection_points.items():
        if is_click_inside_button(x_pos, y_pos, but_x, but_y):
            count[0] += 1
            color = None  # Initialize color
            new_x, new_y = None, None  # Initialize new_x and new_y
            if count[0] % 2 == 1 and game.crows_placed < 7:  # player 1 click
                index = get_index(position)
                # print(index)
                if game.place_crow(index):
                    color = "#99BC85"  # Green to place crow
                    new_x, new_y = but_x, but_y
                else:
                    count[0] -= 1
            elif count[0] == 2:  # vulture's turn to place
                index = get_index(position)
                if game.place_vulture(index):
                    color = "#872341"
                    new_x, new_y = but_x, but_y
            elif count[0] % 2 == 0:  # vulture's turn
                count[0] -= 1
                index = get_index(position)
                if SELECTED_VULTURE is None and game.board[index] == 'vulture':
                    SELECTED_VULTURE = index
                    draw_button(but_x, but_y+15, "#AE445A", "#FAF0E6")
                elif SELECTED_VULTURE != -1 and game.board[index] is None:
                    # print("yes")
                    if game.move_vulture(SELECTED_VULTURE, index):
                        color = "#872341"
                        new_x, new_y = but_x, but_y
                        draw_button(but_x, but_y+15, "#FAF0E6", color)
                        # Draw the moved vulture
                        toggle_button_color(SELECTED_VULTURE)
                        # Remove the highlight from the old position
                        SELECTED_VULTURE = None
                        count[0] += 1
                    else:
                        print("Invalid Move! Try Again.")
            elif count[0] % 2 == 1 and game.crows_placed >= 7:  # player 2 click
                index = get_index(position)
                count[0] -= 1
                if SELECTED_CROW is None and game.board[index] == 'crow':
                    SELECTED_CROW = index
                    draw_button(but_x, but_y+15, "#99BC85", "#FAF0E6")
                    # Highlight the selected crow
                elif SELECTED_CROW is not None and game.board[index] == 'crow':
                    # print("entered")
                    # print(SELECTED_CROW)
                    # toggle back the selected crow if some other crow is selected
                    position = indexed_pts[SELECTED_CROW]
                    but_x, but_y = intersection_points[position]
                    draw_button(but_x, but_y+15, "#FAF0E6", "#99BC85")
                    # Unhighlight the previously selected crow
                    SELECTED_CROW = index  # Update the selected crow
                    position = indexed_pts[SELECTED_CROW]
                    but_x, but_y = intersection_points[position]
                    draw_button(but_x, but_y+15, "#99BC85", "#FAF0E6")
                    # Highlight the newly selected crow
                elif SELECTED_CROW is not None and game.board[index] is None:
                    if game.move_crow(SELECTED_CROW, index):
                        color = "#99BC85"
                        new_x, new_y = but_x, but_y
                        draw_button(but_x, but_y+15, color)  # Draw the moved crow
                        toggle_button_color(SELECTED_CROW)
                        # Remove the highlight from the old position
                        SELECTED_CROW = None
                        count[0] += 1
                    else:
                        print("Invalid Move! Try Again.")
            if color and new_x is not None and new_y is not None:
                draw_button(new_x, new_y+15, "#FAF0E6", color)
            pen.goto(540.00, 400.00)
            pen.clear()  # Clear the previous text
            temp_str = 'Crows killed = ' + str(game.crows_killed)
            pen.write(temp_str, align="right", font=("Arial", 30, "bold"))
            result = game.decide_win(game.vulture_position)
            if result is not None:
                board_turtle.penup()
                board_turtle.goto(25, -50)
                board_turtle.reset()
                board_turtle.color("#FAF0E6")
                board_turtle.write(result + " wins!", align="right", font=("Arial", 30, "bold"))
                board_turtle.hideturtle()
                print(f"{result} wins!")
                break


def toggle_button_color(index):
    """Function to change the color of a button after clicking it"""
    if index in indexed_pts:
        dot = indexed_pts[index]
        circle_x, circle_y = intersection_points[dot]
        color = None  # Initialize color
        if game.board[index] == 'crow':
            color = "#FAF0E6"
        elif game.board[index] == 'vulture':
            color = "#FAF0E6"
        else:
            color = "#FAF0E6"  # Default color for empty points
        draw_button(circle_x, circle_y+15, color)
        return True
    return False


screen = turtle.Screen()
screen.title("Kaooa Game")
screen.bgcolor("#092635")
board_turtle = turtle.Turtle()
board_turtle.hideturtle()
board_turtle.speed(0)
board_turtle.color("#9EC8B9")


def draw_button(x_position, y_position, color2="#FAF0E6", color="#FAF0E6"):
    """To draw colored button"""
    board_turtle.penup()
    board_turtle.goto(x_position, y_position-15)
    board_turtle.pendown()
    board_turtle.pensize(4)
    board_turtle.color(color2, color)
    board_turtle.begin_fill()
    board_turtle.circle(30)
    board_turtle.end_fill()
    board_turtle.penup()


count = [0]
screen.onclick(on_click)
board_turtle.penup()
board_turtle.goto(-400, 100)
board_turtle.pensize(3)
board_turtle.pendown()
intersection_points = {}
for _ in range(5):
    board_turtle.forward(342)
    curr = board_turtle.pos()
    intersection_points[curr] = (curr[0], curr[1] - 15)
    board_turtle.forward(211)
    curr = board_turtle.pos()
    intersection_points[curr] = (curr[0], curr[1] - 15)
    board_turtle.forward(342)
    curr = board_turtle.pos()
    intersection_points[curr] = (curr[0], curr[1] - 15)
    board_turtle.right(144)
draw_button(495.00, 325.00, "#FAF0E6", "#99BC85")
board_turtle.penup()
board_turtle.goto(540.00, 320.00)
board_turtle.pendown()
board_turtle.write("Crow", font=("Arial", 30, "normal"))
board_turtle.penup()
draw_button(495.00, 225.00, "#FAF0E6", "#872341")
board_turtle.penup()
board_turtle.goto(540.00, 220.00)
board_turtle.pendown()
board_turtle.write("Vulture", font=("Arial", 30, "normal"))
board_turtle.penup()
# print(intersection_points)


def pop_close_enough(dictionary, key, tolerance=1):
    """Function to remove unnecessary points from list"""
    for k in list(dictionary.keys()):
        # Convert dict_keys to list to avoid RuntimeError during iteration
        if abs(k[0] - key[0]) < tolerance and abs(k[1] - key[1]) < tolerance:
            dictionary.pop(k)
            return


points_to_remove = [
    (-58.18, 99.87),
    (153.18, 99.87),
    (218.39, -100.81),
    (47.39, -225.05),
    (-123.32, -101.02)
]

for point in points_to_remove:
    pop_close_enough(intersection_points, point)

indexed_pts = {}
IND = 1
for point, (button_x, button_y) in intersection_points.items():
    indexed_pts[IND] = point
    IND += 1
# print(indexed_pts)

neighbours = {
    1: [[5, 3], [6, 8]],
    2: [[8, 6], [9, 3]],
    3: [[5, 1], [9, 2], [4, 0], [10, 0]],
    4: [[3, 9], [5, 6]],
    5: [[3, 10], [6, 7], [4, 0], [1, 0]],
    6: [[8, 2], [5, 4], [1, 0], [7, 0]],
    7: [[6, 5], [8, 9]],
    8: [[6, 1], [9, 10], [2, 0], [7, 0]],
    9: [[3, 4], [8, 7], [2, 0], [10, 0]],
    10: [[3, 5], [9, 8]]
}
for x, y in intersection_points:
    draw_button(x, y)
game = Game(indexed_pts, neighbours)

turtle.mainloop()
