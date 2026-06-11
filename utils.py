import pygame
import random
import json
import os

# Window dimensions
WIDTH = 800
HEIGHT = 800

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)

# Drawing parameters
STROKE = 10
CROSS = 0.4
XBORDER = 100
YBORDER = 100
XOFFSET = int((WIDTH - XBORDER * 2) / 6)
YOFFSET = int((HEIGHT - YBORDER * 2) / 6)
XCROSS = int(XOFFSET * CROSS)
YCROSS = int(YOFFSET * CROSS)
POINT = int(XOFFSET * 0.4)

# State signs
BOT_ = -1
NULL_ = 0
PLAYER_ = 1

# Reinforcement learning parameters
STARTING_LEARNING_RATE = 1.0
MIN_LEARNING_RATE = 0.05
LEARNING_RATE_DECAY = 0.00001
STARTING_EPSILON = 1.0
MIN_EPSILON = 0.05
EPSILON_DECAY = 0.00001
DISCOUNT_FACTOR = 0.8
WIN_REWARD = 15
LOSE_REWARD = -14
DRAW_REWARD = 0.5
CONTINUE_REWARD = 0

EMPTY_QTABLE = {}

# Bot class definition
class Bot:
    def __init__(self, name, sign = BOT_):
        self.name = name
        self.sign = sign
        self.qtable = self.initialize_qtable()
        self.learning_rate = STARTING_LEARNING_RATE
        self.epsilon = STARTING_EPSILON
        self.discount_factor = DISCOUNT_FACTOR
    
    # Saves the qtable you pass it to a json file named after the bot
    def save_qtable(self, qtable):
        filename = f"qtables/{self.name}_qtable.json"
        qtable_serializable = {str(k): v for k, v in qtable.items()}
        with open(filename, "w") as file:
            json.dump(qtable_serializable, file, indent = 4)

    # Loads the qtable from a json file named after the bot to the bot qtable
    def load_qtable(self):
        filename = f"qtables/{self.name}_qtable.json"
        with open(filename, "r") as file:
            qtable_loaded = json.load(file)
        qtable = {eval(k): v for k, v in qtable_loaded.items()}
        return qtable

    # Clears the qtable of the bot and saves it to the json file
    def clear_qtable(self):
        self.qtable = EMPTY_QTABLE.copy()
        self.save_qtable(self.qtable)

    # Does everything all in one and gives the qtable to the __init__ method
    def initialize_qtable(self):
        filename = f"qtables/{self.name}_qtable.json"
        if os.path.exists(filename):
            try:
                qtable = self.load_qtable()
            except (json.JSONDecodeError, ValueError):
                qtable = EMPTY_QTABLE.copy()
                self.save_qtable(qtable)
        else:
            qtable = EMPTY_QTABLE.copy()
            self.save_qtable(qtable)
        return qtable

    # Gets the qvalue of the state and the action. If it doesn't exist, it creates a new one with a random value. It creates all the values of the actions for that state. The qtable is a dictionary filled with lists, one for each state (they go from 0 to 8)
    def get_qvalue(self, state, action):
        if state not in self.qtable:
            self.qtable[state] = [0 for i in range(9)]
        return self.qtable[state][action]

    # Gets the action. If epsilon is high, it's moe likely to return a random action, otherwise it outputs the best one according to the qtable
    def get_action(self, state, play_random = False, play_set = False):
        valid_actions = [i for i, pos in enumerate(state) if pos == NULL_]
        if (random.random() < self.epsilon or play_random) and not play_set:
            return random.choice(valid_actions)
        else:
            return max(valid_actions, key = lambda action: self.get_qvalue(state, action))
    
    # Updates the qtable, but doesn't save it to the json file. Uses a simplified version of the qlearning formula
    def update_qtable(self, reward, action, state, old_state):
        if state not in self.qtable:
            self.qtable[state] = [0 for i in range(9)]
        if old_state not in self.qtable:
            self.qtable[old_state] = [0 for i in range(9)]

        if reward == CONTINUE_REWARD:
            self.qtable[old_state][action] += self.learning_rate * (reward + self.discount_factor * max(self.qtable[state]) - self.qtable[old_state][action])
        else:
            self.qtable[old_state][action] += self.learning_rate * (reward - self.qtable[old_state][action])
    
    # Updates the qtable. It updates all the moves played by the bot based on the final reward
    def update_history(self, final_reward, history):
        for state, action in reversed(history):
            if state not in self.qtable:
                self.qtable[state] = [0 for i in range(9)]
            self.qtable[state][action] += self.learning_rate * (final_reward - self.get_qvalue(state, action))
            final_reward *= self.discount_factor
    
    def update_variables(self):
        self.learning_rate = max(self.learning_rate * (1 - LEARNING_RATE_DECAY), MIN_LEARNING_RATE)
        self.epsilon = max(self.epsilon * (1 - EPSILON_DECAY), MIN_EPSILON)

# Draws the state on the screen
def draw(screen, state, font, color = RED, text = ""):
    screen.fill(WHITE)
    
    pygame.draw.line(screen, BLACK, (XBORDER + XOFFSET * 2, YBORDER), (XBORDER + XOFFSET * 2, YBORDER + YOFFSET * 6), STROKE)
    pygame.draw.line(screen, BLACK, (XBORDER + XOFFSET * 4, YBORDER), (XBORDER + XOFFSET * 4, YBORDER + YOFFSET * 6), STROKE)
    pygame.draw.line(screen, BLACK, (XBORDER, YBORDER + YOFFSET * 2), (XBORDER + XOFFSET * 6, YBORDER + YOFFSET * 2), STROKE)
    pygame.draw.line(screen, BLACK, (XBORDER, YBORDER + YOFFSET * 4), (XBORDER + XOFFSET * 6, YBORDER + YOFFSET * 4), STROKE)

    x = 1
    y = 1
    for tile in state:
        X = XBORDER + x * XOFFSET
        Y = YBORDER + y * YOFFSET

        if tile == PLAYER_:
            pygame.draw.circle(screen, BLACK, (X, Y), POINT)
            pygame.draw.circle(screen, WHITE, (X, Y), (POINT - STROKE))
        elif tile == BOT_:
            pygame.draw.line(screen, BLACK, (X - XCROSS, Y - YCROSS), (X + XCROSS, Y + YCROSS), int(STROKE * 1.41))
            pygame.draw.line(screen, BLACK, (X + XCROSS, Y - YCROSS), (X - XCROSS, Y + YCROSS), int(STROKE * 1.41))
        elif tile == NULL_:
            """
            pygame.draw.circle(screen, RED, (X, Y), POINT)
            pygame.draw.circle(screen, WHITE, (X, Y), (POINT - STROKE))
            pygame.draw.line(screen, RED, (X - XCROSS, Y - YCROSS), (X + XCROSS, Y + YCROSS), int(STROKE * 1.41))
            pygame.draw.line(screen, RED, (X + XCROSS, Y - YCROSS), (X - XCROSS, Y + YCROSS), int(STROKE * 1.41))
            """
        
        x += 2
        if x >= 6:
            x = 1
            y += 2

    text_surface = font.render(text, True, color)
    text_width, text_height = font.size(text)
    screen.blit(text_surface, ((WIDTH - text_width) // 2, (HEIGHT - text_height) // 2))

    pygame.display.flip()

# Checks if the sign has won
def check_win(state, sign):
    for i in range(3):
        if state[i * 3] == sign and state[i * 3 + 1] == sign and state[i * 3 + 2] == sign:
            return True
        if state[i] == sign and state[i + 3] == sign and state[i + 6] == sign:
            return True
    if state[0] == sign and state[4] == sign and state[8] == sign:
        return True
    if state[2] == sign and state[4] == sign and state[6] == sign:
        return True
    return False

# Check for a draw
def check_draw(state):
    return all(pos != NULL_ for pos in state)

# Gets reward for bot with sign1. Sign2 is the opponent. Runs every turn
def get_reward(state, sign1, sign2):
    if check_win(state, sign1):
        return WIN_REWARD
    elif check_win(state, sign2):
        return LOSE_REWARD
    elif check_draw(state):
        return DRAW_REWARD
    else:
        return CONTINUE_REWARD

# Checks if the player is clicking an empty tile. Gives index of the tile
def check_player_input():
    if pygame.mouse.get_pressed()[0]:
        mouse_x, mouse_y = pygame.mouse.get_pos()

        if XBORDER <= mouse_x <= XBORDER + XOFFSET * 6 and YBORDER <= mouse_y <= YBORDER + YOFFSET * 6:
            x = (mouse_x - XBORDER) // (XOFFSET * 2)
            y = (mouse_y - YBORDER) // (YOFFSET * 2)
            return int(y * 3 + x)
    return None