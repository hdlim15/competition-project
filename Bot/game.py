from __future__ import print_function # Debugging purposes
import sys
import traceback
import random
import time

from . import board

def dbg(text):
    print(text, file=sys.stderr)
    sys.stderr.flush()


class Game:
    def __init__(self):
        self.initial_timebank = 0
        self.time_per_move = 10
        self.board_width = 0
        self.board_height = 0

        self.my_botid = -1
        self.other_botid = -1

        self.board = None
        self.last_update = 0
        self.last_timebank = 0

    def initialize_settings(self):
        while(True):
            try:
                current_line = sys.stdin.readline().rstrip('\r\n')
                tokens = current_line.split()
                key0 = tokens[0]
                key1 = tokens[1]
                if (key0 == "settings"):
                    if key1 == "timebank":
                        self.timebank = int(tokens[2])
                    elif key1 == "time_per_move":
                        self.time_per_move = int(tokens[2])
                    elif key1 == "your_botid":
                        self.my_botid = int(tokens[2])
                        self.other_botid = 1 - self.my_botid
                    elif key1 == "field_width":
                        self.board_width = int(tokens[2])
                    elif key1 == "field_height":
                        self.board_height = int(tokens[2])
                        self.board = board.Board(self.board_width, self.board_height)
                elif (key0 == "update" and key1 == "game" and tokens[2] == "field"):
                    self.board.find_starting_pos(self.my_botid, tokens[3])
                    return

            except EOFError:
                break
            except KeyboardInterrupt:
                raise
            except:
                # don't raise error or return so that bot attempts to stay alive
                traceback.print_exc(file=sys.stderr)
                sys.stderr.flush()


    def time_remaining(self):
        return self.last_timebank - int(1000 * (time.clock() - self.last_update))

    def issue_order(self, order):
        sys.stdout.write('%s\n' % (order))
        sys.stdout.flush()

    def run(self, bot):
        self.initialize_settings()
        while(True):
            try:
                current_line = sys.stdin.readline().rstrip('\r\n')
                if current_line.startswith("action move"):
                    dbg(current_line[12:])
                    self.last_timebank = int(current_line[12:])
                    self.issue_order(bot.do_turn(self))
                elif current_line.startswith("update game field"):
                    self.board.update_board(current_line)
                elif current_line.startswith("quit"):
                    break
            except EOFError:
                break
            except KeyboardInterrupt:
                raise
            except:
                # don't raise error or return so that bot attempts to stay alive
                traceback.print_exc(file=sys.stderr)
                sys.stderr.flush()
