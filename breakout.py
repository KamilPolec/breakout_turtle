import turtle as t
from random import randint
import numpy as np


def calculate_reflection(direction=None, magnitude=None):
    r = (direction - (2 * (np.dot(direction, magnitude)) / magnitude))
    return r


def right():
    if paddle.xcor() < 200:
        paddle.setx(paddle.xcor() + 20)


def left():
    if paddle.xcor() > -205:
        paddle.setx(paddle.xcor() - 20)


t.title("day-87-breakout-game")
t.bgcolor("black")
t.setup(500, 600)
t.screensize(450, 550)
t.tracer(n=False)

paddle = t.Turtle("square")
ball = t.Turtle("square")

blocks = []
for i in range(0, 55):
    blocks.append(t.Turtle("square"))

for block in blocks:
    t.colormode(255)
    block.color((randint(0, 255), randint(0, 255), randint(0, 255)))
    block.shapesize(0.7, 2, 1)
    block.penup()
    blocks[0].setpos(-230, 255)
    if blocks.index(block) % 11 == 0:
        block.setpos(blocks[blocks.index(block) - 11].position() + (0, -20))
    else:
        block.setpos(blocks[blocks.index(block) - 1].position() + (45, 0))

ball.color("gray")
ball.shapesize(0.7)
ball.penup()
ball.left(90)

paddle.color("white")
paddle.shapesize(1, 4, 1)
paddle.penup()
paddle.sety(-270)

ball.setpos(paddle.position() + (0, 20))

t.update()
t.tracer(n=True)
t.listen()

t.onkey(right, "Right")
t.onkey(left, "Left")


ball.speed(1)
ball.setheading(100)
while len(blocks) > 0:
    ball.forward(10)
    for block in blocks:
        if ball.xcor() + 20 >= block.xcor() >= ball.xcor() - 20 and ball.ycor() >= block.ycor() - 20 or ball.ycor() > 280:
            block.speed(0)
            block.setpos(500, 500)
            ball.setheading(calculate_reflection(direction=ball.heading(), magnitude=ball.speed()))
    if ball.xcor() + 50 >= paddle.xcor() >= ball.xcor() - 50 and ball.ycor() <= paddle.ycor() + 20:
        ball.setheading(calculate_reflection(direction=ball.heading(), magnitude=ball.speed()))
        ball.speed() + randint(0, 3)
    #moving upwards
    if 180 > ball.heading() > 0:
        #right bounce
        if ball.xcor() > 230:
            print(f"Before {ball.heading()}")
            ball.setheading(calculate_reflection(direction=ball.heading(), magnitude=ball.speed()) + 180)
            print(f"After {ball.heading()}")
        #left bounce
        elif ball.xcor() < -230:
            ball.setheading(calculate_reflection(direction=ball.heading(), magnitude=ball.speed()) + 180)
    else:
        #moving downwards
        if ball.xcor() > 230:
            ball.setheading(calculate_reflection(direction=ball.heading(), magnitude=ball.speed()) + 180)

        elif ball.xcor() < -230:
            ball.setheading(calculate_reflection(direction=ball.heading(), magnitude=ball.speed()) + 180)
    if ball.ycor() < -300:
        print("You Lost")
        break

t.mainloop()
