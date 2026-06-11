import pygame
import random
import time
import utils

pygame.init()
pygame.font.init()

NAME = "TrisBot2"
WAIT = 0.05
END_WAIT = 0.5

# Pygame setup
screen = pygame.display.set_mode((utils.WIDTH, utils.HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Verdana", 80, bold = True)

pygame.display.set_caption("TRIS")

pygame.display.flip()

# Initialization
def initialize():
    global state
    global running_game
    global first_turn
    global active_sign
    global history

    pygame.event.clear()

    state = (utils.NULL_, utils.NULL_, utils.NULL_, utils.NULL_, utils.NULL_, utils.NULL_, utils.NULL_, utils.NULL_, utils.NULL_)
    running_game = True
    first_turn = True
    active_sign = random.choice([utils.BOT_, utils.PLAYER_])
    # active_sign = utils.BOT_
    history = []

# Main loop. Runs until window is closed
bot = utils.Bot(NAME)
running = True
while running:
    initialize()
    # Wait until the player has lifted the finger from the mouse before trying to get another input
    while pygame.mouse.get_pressed()[0]:
        pygame.event.pump()
    while running_game:
        utils.draw(screen, state, font)

        # Closes window if X is clicked
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                running_game = False
                waiting = False
        
        # Bot plays
        if active_sign == utils.BOT_:
            waiting = False
            if first_turn:
                # action = bot.get_action(state, play_random = True)
                action = bot.get_action(state, play_set = True)
                first_turn = False
            else:
                action = bot.get_action(state, play_set = True)
            history.append((state, action))
            state_as_list = list(state)
            state_as_list[action] = active_sign
            state = tuple(state_as_list)
            time.sleep(WAIT)
        # Player plays
        else:
            # Waits until something is clicked
            waiting = True
            player_action = utils.check_player_input()
            if player_action is not None and state[player_action] == utils.NULL_:
                state_as_list = list(state)
                state_as_list[player_action] = active_sign
                state = tuple(state_as_list)

                waiting = False

                if first_turn:
                    first_turn = False

        # Gets the reward
        reward = utils.get_reward(state, utils.PLAYER_, utils.BOT_)
        if not waiting:
            if reward != utils.CONTINUE_REWARD:
                if reward == utils.WIN_REWARD:
                    print("player wins")
                    text = "PLAYER WINS"
                    color = utils.GREEN
                elif reward == utils.LOSE_REWARD:
                    print("bot wins")
                    text = "BOT WINS"
                    color = utils.RED
                elif reward == utils.DRAW_REWARD:
                    print("draw")
                    text = "DRAW"
                    color = utils.PURPLE
                else:
                    print("something happened here")

                running_game = False

            if active_sign == utils.BOT_:
                active_sign = utils.PLAYER_
            else:
                active_sign = utils.BOT_

    utils.draw(screen, state, font, color = color, text = text)
    time.sleep(END_WAIT)

bot.save_qtable(bot.qtable)

pygame.quit()
pygame.font.quit()