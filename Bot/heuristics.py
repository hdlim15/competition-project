from __future__ import print_function # Debugging purposes
import sys

# Debugging purposes
def dbg(text):
    print(text, file=sys.stderr)
    sys.stderr.flush()


class Heuristics:

	def __init__(self):
		self.enemy_distance = -1
		