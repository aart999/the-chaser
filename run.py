import turtle
import random
from collections import deque


def find_path(start, goal):
    queue = deque([start])
    came_from = {start: None}



    while queue:
        current = queue.popleft()

        if current == goal:
            break

        x, y = current
        neighbors = [
            (x+1, y), (x-1, y),
            (x, y+1), (x, y-1)
        ]

        for nx, ny in neighbors:
            if (0 <= nx < n and 0 <= ny < n and
                (nx, ny) not in walls and
                (nx, ny) not in came_from):
                
                came_from[(nx, ny)] = current
                queue.append((nx, ny))

    # reconstruct path
    if goal not in came_from:
        return [] 

    path = []
    cur = goal
    while cur != start:
        path.append(cur)
        cur = came_from[cur]
    path.reverse()
    return path


# ---------------- SCREEN ----------------
screen = turtle.Screen()
turtle.setup(1000,1000)
turtle.title("Grid Chase Game with Walls")
turtle.hideturtle()
turtle.speed(0)
turtle.tracer(0,0)

n = 50
cell_size = 800 / n

# ---------------- GRID ----------------
def draw_line(x1,y1,x2,y2):
    turtle.up()
    turtle.goto(x1,y1)
    turtle.down()
    turtle.goto(x2,y2)

def draw_grid():
    turtle.pencolor('gray')
    turtle.pensize(3)
    x = -400
    for _ in range(n+1):
        draw_line(x,-400,x,400)
        x += cell_size
    y = -400
    for _ in range(n+1):
        draw_line(-400,y,400,y)
        y += cell_size

# ---------------- WALLS ----------------
walls = set()
wall_drawer = turtle.Turtle()
wall_drawer.hideturtle()
wall_drawer.up()
wall_drawer.color("dimgray")

def cell_to_xy(x, y):
    sx = -400 + x * cell_size + cell_size / 2
    sy = -400 + y * cell_size + cell_size / 2
    return sx, sy

def draw_wall(x, y):
    sx, sy = cell_to_xy(x, y)
    wall_drawer.goto(sx - cell_size/2, sy - cell_size/2)
    wall_drawer.begin_fill()
    for _ in range(4):
        wall_drawer.forward(cell_size)
        wall_drawer.left(90)
    wall_drawer.end_fill()

def generate_walls(count=350):
    while len(walls) < count:
        x = random.randint(0, n-1)
        y = random.randint(0, n-1)
        if (x, y) not in [(cell_x, cell_y), (chaser_x, chaser_y)]:
            walls.add((x, y))

def draw_walls():
    for w in walls:
        draw_wall(*w)

# ---------------- PLAYER ----------------
cursor = turtle.Turtle()
cursor.shape("circle")
cursor.color("red")
cursor.shapesize(0.8)
cursor.up()
cursor.speed(0)

cell_x = n // 2
cell_y = n // 2

def goto_cell(x, y):
    cursor.goto(*cell_to_xy(x, y))

# ---------------- CHASER ----------------
chaser = turtle.Turtle()
chaser.shape("circle")
chaser.color("black")
chaser.shapesize(0.8)
chaser.up()
chaser.speed(0)

chaser_x = 0
chaser_y = 0

def goto_chaser(x, y):
    chaser.goto(*cell_to_xy(x, y))


# goal
goal = turtle.Turtle()
goal.shape("circle")
goal.color("green")
goal.shapesize(0.8)
goal.up()
goal.speed(0)

def random_empty_cell():
    while True:
        x = random.randint(0, n-1)
        y = random.randint(0, n-1)
        if ((x, y) not in walls and
            (x, y) != (cell_x, cell_y) and
            (x, y) != (chaser_x, chaser_y)):
            return x, y

goal_x, goal_y = random_empty_cell()

def goto_goal(x, y):
    sx = -400 + x * cell_size + cell_size / 2
    sy = -400 + y * cell_size + cell_size / 2
    goal.goto(sx, sy)

goto_goal(goal_x, goal_y)
screen.update()


# ---------------- GAME LOGIC ----------------
game_over = False

def chase_grid():
    global chaser_x, chaser_y, game_over

    if game_over:
        return

    path = find_path((chaser_x, chaser_y), (cell_x, cell_y))

    if path:
        chaser_x, chaser_y = path[0]
        goto_chaser(chaser_x, chaser_y)

    # collision
    if chaser_x == cell_x and chaser_y == cell_y:
        game_over = True
        turtle.goto(0, 420)
        turtle.color("red")
        turtle.write("GAME OVER", align="center",
                     font=("Arial", 32, "bold"))
        screen.update()
        return

    screen.update()
    screen.ontimer(chase_grid, 200)


def check_win():
    global game_over
    if cell_x == goal_x and cell_y == goal_y:
        game_over = True
        turtle.goto(0, 420)
        turtle.color("green")
        turtle.write("YOU WIN!", align="center", font=("Arial", 32, "bold"))
        screen.update()

def move_up():
    global cell_y
    if cell_y < n - 1:
        cell_y += 1
        goto_cell(cell_x, cell_y)
        check_win()
        screen.update()


# ---------------- MOVEMENT ----------------
def try_move(dx, dy):
    global cell_x, cell_y
    nx, ny = cell_x + dx, cell_y + dy
    if 0 <= nx < n and 0 <= ny < n and (nx, ny) not in walls:
        cell_x, cell_y = nx, ny
        goto_cell(cell_x, cell_y)
        check_win()         
        screen.update()

screen.listen()
screen.onkey(lambda: try_move(0, 1), "Up")
screen.onkey(lambda: try_move(0,-1), "Down")
screen.onkey(lambda: try_move(-1,0), "Left")
screen.onkey(lambda: try_move(1,0), "Right")

# ---------------- START ----------------
draw_grid()
generate_walls()
draw_walls()

goal_x, goal_y = random_empty_cell()
goto_goal(goal_x, goal_y)


goto_cell(cell_x, cell_y)
goto_chaser(chaser_x, chaser_y)

screen.update()
chase_grid()
turtle.mainloop()
