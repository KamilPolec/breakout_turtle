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
ball = t.Turtle("circle")

blocks = []
for i in range(0, 55):
    blocks.append(t.Turtle("square"))

for block in blocks:
    t.colormode(255)
    block.color((randint(0, 255), randint(0, 255), randint(0, 255)))
    block.shapesize(0.7, 2, 1)
    block.penup()
    blocks[0].setpos(-230, 215)
    if blocks.index(block) % 11 == 0:
        block.setpos(blocks[blocks.index(block) - 11].position() + (0, -25))
    else:
        block.setpos(blocks[blocks.index(block) - 1].position() + (45, 0))

ball.color("gray")
ball.shapesize(0.7)
ball.penup()
ball.left(90)

paddle.color("white")
paddle.shapesize(0.5, 4, 1)
paddle.penup()
paddle.sety(-270)

ball.setpos(paddle.position() + (0, 20))

t.update()
t.tracer(n=True)
t.listen()

t.onkey(right, "Right")
t.onkey(left, "Left")


ball.speed(3)

width_limit, height_limit = t.screensize()
width_limit, height_limit = width_limit/2, height_limit/2

while len(blocks) > 0:
    ball.forward(5)
    for index, block in enumerate(blocks):
        if block.isvisible() and ball.heading() < 180:
            if ball.xcor() + 20 >= block.xcor() >= ball.xcor() - 20 and ball.ycor() >= block.ycor() - 20:
                block.ht()
                t.tracer(False)
                ball.setheading(calculate_reflection(direction=ball.heading(), magnitude=ball.speed()) + (block.xcor() - ball.xcor()))
                t.tracer(True)

    if ball.xcor() + 50 >= paddle.xcor() >= ball.xcor() - 50 and ball.ycor() <= paddle.ycor() + 12 or ball.ycor() >= height_limit:
        if ball.heading() > 180:
            t.tracer(False)
            ball.setheading(calculate_reflection(direction=ball.heading(), magnitude=ball.speed()) + (paddle.xcor() - ball.xcor()))
            t.tracer(True)
    #Side bounce
    if ball.xcor() >= width_limit or ball.xcor() <= -width_limit:
        t.tracer(False)
        ball.setheading((calculate_reflection(direction=ball.heading(), magnitude=ball.speed()) + 180) / 1.02)
        t.tracer(True)
    if ball.ycor() <= -height_limit:
        print("You Lost")
        break


t.mainloop()
