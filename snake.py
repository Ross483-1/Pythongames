import turtle
import time
import random

delay = 0.1
score = 0
high_score = 0

# Set up the screen
wn = turtle.Screen()
wn.title("Advanced Snake Game")
wn.bgcolor("black")
wn.setup(width=600, height=600)
wn.tracer(0)

# Snake head
head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("dark green")
head.penup()
head.goto(0,0)
head.direction = "stop"

# Eyes (Left and Right)
left_eye = turtle.Turtle()
left_eye.speed(0)
left_eye.shape("circle")
left_eye.color("white")
left_eye.shapesize(0.3, 0.3)
left_eye.penup()

right_eye = turtle.Turtle()
right_eye.speed(0)
right_eye.shape("circle")
right_eye.color("white")
right_eye.shapesize(0.3, 0.3)
right_eye.penup()

# Pupils (Black dots inside the eyes)
left_pupil = turtle.Turtle()
left_pupil.speed(0)
left_pupil.shape("circle")
left_pupil.color("black")
left_pupil.shapesize(0.1, 0.1)
left_pupil.penup()

right_pupil = turtle.Turtle()
right_pupil.speed(0)
right_pupil.shape("circle")
right_pupil.color("black")
right_pupil.shapesize(0.1, 0.1)
right_pupil.penup()

# Fruit settings configuration
fruits_config = {
    "Apple": {"color": "red", "points": 10, "shape": "circle"},
    "Banana": {"color": "gold", "points": 20, "shape": "triangle"},
    "Grapes": {"color": "purple", "points": 30, "shape": "circle"}
}

# Setup fruit object
food = turtle.Turtle()
food.speed(0)
food.penup()

current_fruit = "Apple"

def spawn_fruit():
    global current_fruit
    current_fruit = random.choice(list(fruits_config.keys()))
    config = fruits_config[current_fruit]
    
    food.shape(config["shape"])
    food.color(config["color"])
    
    x = random.randint(-280, 280)
    y = random.randint(-280, 280)
    food.goto(x, y)

spawn_fruit() # Spawn first fruit

segments = []

# Pen for scoring
pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Score: 0  High Score: 0", align="center", font=("Courier", 18, "bold"))

# Info pen for showing what fruit was eaten
info_pen = turtle.Turtle()
info_pen.speed(0)
info_pen.color("yellow")
info_pen.penup()
info_pen.hideturtle()
info_pen.goto(0, 230)

# Functions to change direction
def go_up():
    if head.direction != "down":
        head.direction = "up"

def go_down():
    if head.direction != "up":
        head.direction = "down"

def go_left():
    if head.direction != "right":
        head.direction = "left"

def go_right():
    if head.direction != "left":
        head.direction = "right"

def move():
    if head.direction == "up":
        head.sety(head.ycor() + 20)
    if head.direction == "down":
        head.sety(head.ycor() - 20)
    if head.direction == "left":
        head.setx(head.xcor() - 20)
    if head.direction == "right":
        head.setx(head.xcor() + 20)
    update_eyes()

def update_eyes():
    hx, hy = head.xcor(), head.ycor()
    
    # Position eyes based on movement direction
    if head.direction == "up":
        left_eye.goto(hx - 6, hy + 6)
        right_eye.goto(hx + 6, hy + 6)
    elif head.direction == "down":
        left_eye.goto(hx + 6, hy - 6)
        right_eye.goto(hx - 6, hy - 6)
    elif head.direction == "left":
        left_eye.goto(hx - 6, hy - 6)
        right_eye.goto(hx - 6, hy + 6)
    elif head.direction == "right" or head.direction == "stop":
        left_eye.goto(hx + 6, hy + 6)
        right_eye.goto(hx + 6, hy - 6)
        
    # Pupils always sit right in the center of the eyes
    left_pupil.goto(left_eye.xcor(), left_eye.ycor())
    right_pupil.goto(right_eye.xcor(), right_eye.ycor())

# Keyboard bindings
wn.listen()
wn.onkeypress(go_up, "w")
wn.onkeypress(go_down, "s")
wn.onkeypress(go_left, "a")
wn.onkeypress(go_right, "d")

# Main game loop
while True:
    wn.update()

    # Check for a collision with the border
    if head.xcor()>290 or head.xcor()<-290 or head.ycor()>290 or head.ycor()<-290:
        time.sleep(1)
        head.goto(0,0)
        head.direction = "stop"

        for segment in segments:
            segment.goto(1000, 1000)
        segments.clear()

        score = 0
        delay = 0.1
        info_pen.clear()
        pen.clear()
        pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 18, "bold"))

    # Check for a collision with the food
    if head.distance(food) < 20:
        points_earned = fruits_config[current_fruit]["points"]
        fruit_color = fruits_config[current_fruit]["color"]
        
        # Display alert text for the fruit eaten
        info_pen.clear()
        info_pen.write(f"Eats {current_fruit}! +{points_earned}", align="center", font=("Courier", 14, "italic"))
        
        # Add a matching color segment
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color(fruit_color)
        new_segment.penup()
        segments.append(new_segment)

        delay -= 0.002
        score += points_earned

        if score > high_score:
            high_score = score
        
        pen.clear()
        pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 18, "bold"))
        
        spawn_fruit()

    # Move the end segments first in reverse order
    for index in range(len(segments)-1, 0, -1):
        x = segments[index-1].xcor()
        y = segments[index-1].ycor()
        segments[index].goto(x, y)

    if len(segments) > 0:
        x = head.xcor()
        y = head.ycor()
        segments[0].goto(x, y)

    move()    

    # Check for head collision with body segments
    for segment in segments:
        if segment.distance(head) < 20:
            time.sleep(1)
            head.goto(0,0)
            head.direction = "stop"
        
            for seg in segments:
                seg.goto(1000, 1000)
            segments.clear()

            score = 0
            delay = 0.1
            info_pen.clear()
            pen.clear()
            pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 18, "bold"))

    time.sleep(delay)

wn.mainloop()
