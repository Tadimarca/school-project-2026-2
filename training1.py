import keyboard
import sys
import utils

# Training1.py and Training2.py use sligthly different methods, but are mostly the same

# Initialization
def initialize():
    global state
    global running_game
    global first_turn
    global active_sign
    global history1
    global history2

    state = (utils.NULL_, utils.NULL_, utils.NULL_, utils.NULL_, utils.NULL_, utils.NULL_, utils.NULL_, utils.NULL_, utils.NULL_)
    running_game = True
    first_turn = True
    active_sign = utils.BOT_
    history1 = []
    history2 = []

# Main loop. Runs until window is closed
bot = utils.Bot("TrisBot2")
running = True
while running:
    # Stops the training with Ctrl + W
    if keyboard.is_pressed('ctrl') and keyboard.is_pressed("w"):
        running = False
        running_game = False
    initialize()
    # Runs one game. Goes on forever playing games
    while running_game:
        # If it's the first turn, the action is random, so the bot explores all the options
        """
        if first_turn:
            action = bot.get_action(state, play_random = True)
        else:
            action = bot.get_action(state)
        """
        
        action = bot.get_action(state)

        # Saves the moves that just happened. BOT_ has history1, PLAYER_ has history2. They are needed to update the qtable correctly
        if active_sign == utils.BOT_:
            history1.append((state, action))
        else:
            history2.append((state, action))

        # The current bot plays a move
        state_as_list = list(state)
        state_as_list[action] = active_sign
        state = tuple(state_as_list)
        reward = utils.get_reward(state, active_sign, utils.BOT_ if active_sign != utils.BOT_ else utils.PLAYER_)

        # Partial reward based on immediate events. If it's the last turn, target = reward
        if reward == utils.CONTINUE_REWARD:
            if active_sign == utils.BOT_:
                bot.update_qtable(reward, history1[-1][1], state, history1[-1][0])
            else:
                bot.update_qtable(reward, history2[-1][1], state, history2[-1][0])
            
            # Switches active bots
            if active_sign == utils.BOT_:
                active_sign = utils.PLAYER_
            else:
                active_sign = utils.BOT_
        else:
            running_game = False
        
        first_turn = False
    
    # Updates the whole game after the end of the game. There is a duble learning going on: one for the win, one for the loss, both on the same qtable
    bot.update_history(reward, history1 if active_sign == utils.BOT_ else history2)

    # Inverts the outcome, to train the other side of the bot
    if reward == utils.LOSE_REWARD:
        reward = utils.WIN_REWARD
    elif reward == utils.WIN_REWARD:
        reward = utils.LOSE_REWARD

    bot.update_history(reward, history2 if active_sign == utils.BOT_ else history1)

    bot.update_variables()
    
bot.save_qtable(bot.qtable)

sys.exit()