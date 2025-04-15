import gradio as gr
import numpy as np
from PIL import Image, ImageDraw
import random

CELL_SIZE = 20
GRID_SIZE = 20
IMG_SIZE = CELL_SIZE * GRID_SIZE

# Цвета
BG_COLOR = (45, 1, 77)         # Фиолетовый фон
SNAKE_HEAD_COLOR = (255, 105, 180)  # Розовая голова
SNAKE_BODY_COLOR = (255, 182, 213)  # Светло-розовое тело
FOOD_COLOR = (255, 60, 60)

# Направления
DIRS = {'Влево': (-1, 0), 'Вправо': (1, 0), 'Вверх': (0, -1), 'Вниз': (0, 1)}

class SnakeGame:
    def __init__(self):
        self.reset()

    def reset(self):
        self.snake = [(GRID_SIZE//2, GRID_SIZE//2)]
        self.direction = 'Вправо'
        self.spawn_food()
        self.score = 0
        self.game_over = False

    def spawn_food(self):
        while True:
            food = (random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))
            if food not in self.snake:
                self.food = food
                break

    def step(self, action):
        if self.game_over:
            return self.render(), self.score, True
        # Не даём повернуть на 180
        if (action == 'Влево' and self.direction != 'Вправо') or \
           (action == 'Вправо' and self.direction != 'Влево') or \
           (action == 'Вверх' and self.direction != 'Вниз') or \
           (action == 'Вниз' and self.direction != 'Вверх'):
            self.direction = action
        dx, dy = DIRS[self.direction]
        head = (self.snake[0][0] + dx, self.snake[0][1] + dy)
        # Проверка на столкновение
        if (not 0 <= head[0] < GRID_SIZE or not 0 <= head[1] < GRID_SIZE or head in self.snake):
            self.game_over = True
            return self.render(), self.score, True
        self.snake.insert(0, head)
        if head == self.food:
            self.score += 1
            self.spawn_food()
        else:
            self.snake.pop()
        return self.render(), self.score, False

    def render(self):
        img = Image.new('RGB', (IMG_SIZE, IMG_SIZE), BG_COLOR)
        draw = ImageDraw.Draw(img)
        # Еда
        fx, fy = self.food
        draw.rectangle([
            fx*CELL_SIZE, fy*CELL_SIZE, (fx+1)*CELL_SIZE-1, (fy+1)*CELL_SIZE-1
        ], fill=FOOD_COLOR)
        # Тело змейки
        for x, y in self.snake[1:]:
            draw.rectangle([
                x*CELL_SIZE, y*CELL_SIZE, (x+1)*CELL_SIZE-1, (y+1)*CELL_SIZE-1
            ], fill=SNAKE_BODY_COLOR)
        # Голова
        hx, hy = self.snake[0]
        draw.rectangle([
            hx*CELL_SIZE, hy*CELL_SIZE, (hx+1)*CELL_SIZE-1, (hy+1)*CELL_SIZE-1
        ], fill=SNAKE_HEAD_COLOR)
        return img

game = SnakeGame()

def play(action, state):
    if state is None or state.get('game_over', False):
        game.reset()
    else:
        game.snake = state['snake']
        game.direction = state['direction']
        game.food = tuple(state['food'])
        game.score = state['score']
        game.game_over = state['game_over']
    img, score, over = game.step(action)
    new_state = {
        'snake': game.snake,
        'direction': game.direction,
        'food': game.food,
        'score': game.score,
        'game_over': game.game_over
    }
    label = f"Счёт: {score}"
    if over:
        label += " | Игра окончена! Нажмите любую кнопку для новой игры."
    return img, new_state, label

def reset_game():
    game.reset()
    state = {
        'snake': game.snake,
        'direction': game.direction,
        'food': game.food,
        'score': game.score,
        'game_over': game.game_over
    }
    return game.render(), state, f"Счёт: {game.score}"

with gr.Blocks(theme=gr.themes.Soft(primary_hue="purple", secondary_hue="pink")) as demo:
    gr.Markdown("# Змейка на Gradio\nУправляйте с помощью кнопок ниже!")
    image = gr.Image(type="pil", label="Поле")
    score = gr.Textbox(label="Счёт", interactive=False)
    state = gr.State()
    with gr.Row():
        left = gr.Button("⬅️ Влево")
        up = gr.Button("⬆️ Вверх")
        down = gr.Button("⬇️ Вниз")
        right = gr.Button("➡️ Вправо")
    left.click(play, inputs=[gr.Textbox(value="Влево", visible=False), state], outputs=[image, state, score])
    up.click(play, inputs=[gr.Textbox(value="Вверх", visible=False), state], outputs=[image, state, score])
    down.click(play, inputs=[gr.Textbox(value="Вниз", visible=False), state], outputs=[image, state, score])
    right.click(play, inputs=[gr.Textbox(value="Вправо", visible=False), state], outputs=[image, state, score])
    demo.load(reset_game, inputs=None, outputs=[image, state, score])

demo.launch()
