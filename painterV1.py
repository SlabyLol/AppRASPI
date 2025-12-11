#importing Libraries 
from turtle import Turtle,Screen

def clickme(x,y):
    pen.up()
    pen.goto(x,y)
    pen.down()

def dragging(x,y):
    pen.ondrag(None)
    pen.setheading(pen.towards(x,y))
    pen.goto(x,y)
    pen.ondrag(dragging)
#assigning the screen class to screen variable

screen = Screen()
screen.onclick(clickme)

#assigning the Turtle class to pen variable

pen = Turtle()
pen.speed(0) 
pen.ondrag(dragging)

screen.mainloop()