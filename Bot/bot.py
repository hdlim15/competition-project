from __future__ import print_function # Debugging purposes
import sys
import random

def dbg(text):
    print(text, file=sys.stderr)
    sys.stderr.flush()

class Bot:

    def __init__(self):
        pass

    def do_turn(self, game):
        legal = game.board.legal_moves()

        if len(legal) == 0:
            return "pass"

        self.end_game(game)

    # For when the bot is secluded and need not worry about the other bot
    def end_game(self, game):
