from serpent.environment import Environment
from serpent.utilities import SerpentError

import random
import collections

import serpent.input_controller

import numpy as np


class NumericMatrixEnvionment(Environment):

    def __init__(self, game_api=None, input_controller=None, bosses=None, items=None):
        super().__init__("Numeric Matrix Environment", game_api=game_api, input_controller=input_controller)
        self.reset()

    @property
    def new_episode_data(self):
        return {}

    @property
    def end_episode_data(self):
        return {
            "final_score": self.game_state["current_score"]
        }

    def new_episode(self, maximum_steps=None, reset=False):
        self.reset_game_state()
        
        super().new_episode(maximum_steps=maximum_steps, reset=reset)

    def reset(self):
        self.reset_game_state()
        super().reset()

    def reset_game_state(self):
        self.game_state = {
            "current_score": 0,
            "game_over": False,
            "numeric_matrix": np.zeros(shape=(4,4), dtype=np.uint16),
            "game_matrix": [["", "", "", ""],["", "", "", ""],["", "", "", ""],["", "", "", ""]]
        }

    def update_game_state(self, game_frame):

        context = self.game_api.get_context(game_frame)
        
        if context['game_over']:
            self.game_state['game_over'] = context['game_over']
        else:
            self.game_state['current_score'] = context['current_score']
            self.game_state['game_matrix'] = context['game_matrix']
            self.game_state['numeric_matrix'] = context['numeric_matrix']

        return True