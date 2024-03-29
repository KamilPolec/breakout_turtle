import math
import turtle as t
from random import randint
import numpy as np


def return_reflection(direction=None, normal=None):
    if normal == 360 or normal == 180:
        return (180 - direction) % 360
    elif normal == 90 or normal == 270:
        return (360 - direction) % 360
    else:
        return 180 + (2 * normal - direction % 360)


def collide(ball, normal):
    t.tracer(False)
    ball.setheading(return_reflection(direction=ball.heading(), normal=normal))
    ball.forward(1)
    t.tracer(True)


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
    blocks[0].setpos(-210, 215)
    if blocks.index(block) % 11 == 0:
        block.setpos(blocks[blocks.index(block) - 11].position() + (0, -15))
    else:
        block.setpos(blocks[blocks.index(block) - 1].position() + (41, 0))

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

ball.speed(1)

width_limit, height_limit = t.screensize()
width_limit, height_limit = width_limit / 2 + 10, height_limit / 2 + 20

left_lower = range(40, 51)
left_upper = range(310, 320)
right_upper = range(220, 231)
right_lower = range(130, 141)
corner_angles = []
for index, _ in enumerate(left_lower):
    corner_angles.append(_)
    corner_angles.append(left_upper[index - 1])
    corner_angles.append(right_upper[index - 1])
    corner_angles.append(right_lower[index - 1])



while len(blocks) > 0:
    t.tracer(False)
    for _ in range(0, 2):
        ball.forward(1)
        for index, block in enumerate(blocks):
            if block.isvisible():

                block_hitbox = {
                    'top': block.ycor() + 10,
                    'bottom': block.ycor() - 10,
                    'right': block.xcor() + 20,
                    'left': block.xcor() - 20}

                on_the_sides = block_hitbox['right'] >= ball.xcor() >= block_hitbox['left']
                in_top_bottom = block_hitbox['top'] >= ball.ycor() >= block_hitbox['bottom']

                within_hitbox = on_the_sides and in_top_bottom

                right_hit = block_hitbox['right'] - 2 < ball.xcor() < block_hitbox['right'] and \
                            block_hitbox["top"] - 2 > ball.ycor() > block_hitbox["bottom"] + 2

                left_hit = block_hitbox['left'] + 2 > ball.xcor() > block_hitbox['left'] and \
                           block_hitbox["top"] - 2 > ball.ycor() > block_hitbox["bottom"] + 2
                vertical_hit = ball.ycor() < block_hitbox['top'] or ball.ycor() > block_hitbox['bottom']

                top_right_corner = ball.ycor() >= block_hitbox["top"] - 1 and ball.xcor() <= block_hitbox["right"] - 1
                top_left_corner = ball.ycor() >= block_hitbox["top"] - 1 and ball.xcor() >= block_hitbox["left"] + 1
                bottom_right_corner = ball.ycor() <= block_hitbox["bottom"] + 1 and ball.xcor() <= block_hitbox[
                    "right"] - 1
                bottom_left_corner = ball.ycor() <= block_hitbox["bottom"] + 1 and ball.xcor() >= block_hitbox[
                    "left"] + 1

                corner_hit = top_left_corner or bottom_left_corner or top_right_corner or bottom_right_corner

                moving_left = 90 < ball.heading() < 270
                moving_right = 0 < ball.heading() < 90 or 270 < ball.heading() < 360

                if within_hitbox:
                    if corner_hit and round(ball.heading()) in corner_angles:
                        to_the_right = ball.xcor() > block.xcor()
                        to_the_left = ball.xcor() < block.xcor()
                        if to_the_right and moving_right or to_the_left and moving_left:
                            print("corner inverted")
                            block.color("white")
                            collide(ball=ball, normal=90)
                            block.ht()
                        else:
                            print("corner")
                            block.color("white")
                            ball.setheading(ball.heading() + 180)
                            block.ht()

                    elif right_hit or left_hit:
                        print("side hit")
                        block.color("white")
                        collide(ball=ball, normal=180)
                        block.ht()

                    elif vertical_hit:
                        print("vertical hit")
                        block.color("white")
                        collide(ball=ball, normal=90)
                        block.ht()

        if ball.xcor() + 50 >= paddle.xcor() >= ball.xcor() - 50 and ball.ycor() <= paddle.ycor() + 12:
            t.tracer(False)
            ball.setheading(return_reflection(direction=ball.heading(), normal=270) + paddle.xcor() - ball.xcor())
            ball.forward(1)
            t.tracer(True)
        if ball.ycor() >= height_limit:
            collide(ball=ball, normal=270)
        # Side bounce
        if ball.xcor() >= width_limit or ball.xcor() <= -width_limit:
            t.tracer(False)
            ball.setheading(return_reflection(direction=ball.heading(), normal=180) / 1.02)
            ball.forward(1)
            t.tracer(True)
        # lost ball
        if ball.ycor() <= -height_limit:
            collide(ball=ball, normal=90)
            # print("You Lost")
            # break

    t.tracer(True)
t.mainloop()
