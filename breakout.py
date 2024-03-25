import turtle as t
from random import randint
import numpy as np


def calculate_reflection(direction=None, normal=None):
    normal = normal / np.linalg.norm(normal)
    r = (direction - 2 * (np.dot(direction, normal) / normal))
    return r


def right():
    if paddle.xcor() < 200:
        paddle.setx(paddle.xcor() + 25)


def left():
    if paddle.xcor() > -205:
        paddle.setx(paddle.xcor() - 25)


t.title("day-87-breakout-game")
t.bgcolor("black")
t.setup(500, 600)
t.screensize(450, 550)
t.tracer(n=False)

paddle = t.Turtle("square")
ball = t.Turtle("circle")

block_amount = 55
blocks = [t.Turtle("square") for _ in range(0, block_amount)]

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
# ball.penup()
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

ball.speed(9)

width_limit, height_limit = t.screensize()
width_limit, height_limit = width_limit / 2 + 10, height_limit / 2 + 20

while len(blocks) > 0:
    ball.forward(5)
    for index, block in enumerate(blocks):
        if block.isvisible():

            right_side = block.xcor() + 20
            left_side = block.xcor() - 20
            top = block.ycor() + 20
            bottom = block.ycor() - 20

            # TODO: Ball Hitbox
            ball_y = ball.ycor() - 20 and ball.ycor() + 20
            ball_x = ball.ycor() + 20 and ball.ycor() - 20

            on_the_sides = right_side >= ball.xcor() >= left_side
            in_top_bottom = top >= ball.ycor() >= bottom

            within_hitbox = on_the_sides and in_top_bottom


            if within_hitbox:
                if block.xcor() + 17 < ball.xcor() < right_side or block.xcor() - 17 > ball.xcor() > left_side:
                    print("side hit")
                    block.color("white")

                    t.tracer(False)
                    print(ball.heading())
                    ball.setheading(calculate_reflection(direction=ball.heading(), normal=ball.speed()) + 180)
                    print(ball.heading())
                    ball.forward(1)
                    t.tracer(True)
                    block.ht()
                elif ball.ycor() < top or ball.ycor() > bottom:
                    block.color("white")

                    t.tracer(False)
                    if ball.heading() < 180:
                        ball.setheading(calculate_reflection(direction=ball.heading(), normal=ball.speed()) + (
                                block.xcor() - ball.xcor()))
                        ball.forward(5)
                    elif ball.heading() > 180:
                        ball.setheading(ball.heading() + 270)
                    t.tracer(True)
                    block.ht()

    if ball.xcor() + 50 >= paddle.xcor() >= ball.xcor() - 50 and ball.ycor() <= paddle.ycor() + 12:
        if ball.heading() > 180:
            t.tracer(False)
            ball.setheading(
                calculate_reflection(direction=ball.heading(), normal=ball.speed()) + (paddle.xcor() - ball.xcor()))
            t.tracer(True)

    if ball.ycor() >= height_limit:
        t.tracer(False)
        ball.setheading(calculate_reflection(direction=ball.heading(), normal=ball.speed()))
        ball.forward(5)
        t.tracer(True)
    # Side bounce
    if ball.xcor() >= width_limit or ball.xcor() <= -width_limit:
        t.tracer(False)
        ball.setheading(calculate_reflection(direction=ball.heading(), normal=ball.speed()) + 180 / 1.02)
        ball.forward(5)
        t.tracer(True)
    if ball.ycor() <= -height_limit:
        t.tracer(False)
        ball.setheading(calculate_reflection(direction=ball.heading(), normal=ball.speed()))
        ball.forward(5)
        t.tracer(True)
        # print("You Lost")
        # break

t.mainloop()
