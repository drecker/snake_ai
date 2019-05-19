import random
import time
import tkinter as tk
from game import *

#####
### TODO:
### 1. zatvaranie aplikacie nereaguje na ESC a na krizik zleti
### 2. nejak ti nesedi kruh na konci priamky
#####

def draw_scaled_line(canvas, endpoint1, endpoint2, line_width, scaling_factor = None):
    if scaling_factor is None:
        scaling_factor = scaling

    (x, y), (m, n) = endpoint1, endpoint2
    s = scaling_factor
    canvas.create_line(x*s, y*s, m*s, n*s, width = line_width*s)

def draw_wall(canvas, endpoint1, endpoint2, line_width, scaling_factor = None):
    wall_color = "black"
    draw_scaled_line(canvas, endpoint1, endpoint2, line_width * 2, scaling_factor)
    draw_scaled_circle(canvas, endpoint1, line_width, scaling_factor, fill=wall_color)
    draw_scaled_circle(canvas, endpoint2, line_width, scaling_factor, fill=wall_color)

def draw_scaled_circle(canvas, coor, radius, scaling_factor = None, *args, **kwargs):
    if scaling_factor is None:
        scaling_factor = scaling

    x,y = coor
    x, y, radius = x*scaling_factor, y*scaling_factor, radius*scaling_factor
    canvas.create_oval(x-radius, y-radius, x+radius, y+radius, *args, **kwargs)

def get_score_message(score):
    return "Score: {}".format(score)

def close_window():
  global running
  running = False

game = Game()

scaling = 100
line_width = 5

root = tk.Tk()
root.protocol("WM_DELETE_WINDOW", close_window)
root.title("AI-Snake")

canvas = tk.Canvas(root, width=game.width * scaling, height=game.height * scaling, background="white")
canvas.pack()

score_message = tk.StringVar()
score_label = tk.Label(root, textvariable=score_message)
score_label.pack()

running = True

result = None
while result is not game.DIED and running:
    canvas.delete("all")
    result = game.tick(0)

    if result == game.DIED:
        score_message.set("GAME OVER, score: {}".format(game.score))
    else:
        # Score
        score_message.set(get_score_message(game.score))

    # Food
    draw_scaled_circle(canvas, game.food.pos, game.food.width, fill="red")

    # Walls
    for wall in game.walls:
        draw_wall(canvas, *wall.endpoints, wall.width)

    # Snake
    for snake_piece in game.snake.body:
        draw_scaled_circle(canvas, snake_piece, game.snake.width, fill="black")
    draw_scaled_circle(canvas, game.snake.head_position, game.snake.width, fill="green")

    root.update_idletasks()
    root.update()

    time.sleep(0.1)

while running:

    root.update()
    time.sleep(0.1)
