from serpent.game_api import GameAPI
import time
from serpent.input_controller import KeyboardKey, KeyboardEvent, KeyboardEvents
from serpent.input_controller import MouseButton, MouseEvent, MouseEvents
import serpent.cv as cv
from serpent.ocr import perform_ocr, extract_ocr_candidates
import numpy as np

class TwentyFourtyEightAPI(GameAPI):
    # A GameAPI is intended to contain functions and pieces of data that are applicable to the 
    # game and not agent or environment specific (e.g. Game inputs, Frame processing)

    def __init__(self, game=None):
        super().__init__(game=game)

        # SAMPLE - Replace with your own game inputs!
        self.game_inputs = {
            "MOVEMENT": {
                "MOVE UP": [KeyboardEvent(KeyboardEvents.DOWN, KeyboardKey.KEY_UP)],
                "MOVE LEFT": [KeyboardEvent(KeyboardEvents.DOWN, KeyboardKey.KEY_LEFT)],
                "MOVE DOWN": [KeyboardEvent(KeyboardEvents.DOWN, KeyboardKey.KEY_DOWN)],
                "MOVE RIGHT": [KeyboardEvent(KeyboardEvents.DOWN, KeyboardKey.KEY_RIGHT)]
            }
        }

    def _is_game_over(self, frame):
        score_region = cv.extract_region_from_image(frame.grayscale_frame, self.game.screen_regions["CURRENT_SCORE"])
        if np.all(score_region == score_region[0][0]):
            return True
        else:
            return False

    def _build_game_matrix(self, frame):
        matrix = [["", "", "", ""],["", "", "", ""],["", "", "", ""],["", "", "", ""]]
        num_mat = np.zeros(shape=(4,4), dtype=np.uint16)

        for rows in range(4):
            for cols in range(4):
                current_tile = cv.extract_region_from_image(frame.frame, self.game.screen_regions["TILES"]["TILE_"+str(rows*4+cols)])                
                match_color = '#%02x%02x%02x' % tuple(current_tile[5, 5, :])
                
                if match_color in self.game.styles:
                    matrix[rows][cols] = list(self.game.point_values.keys())[self.game.styles.index(match_color)]
                    if matrix[rows][cols] != 'blank':
                        num_mat[rows, cols] = int(matrix[rows][cols])
                else:
                    return False, False

        return matrix, num_mat

    def _get_ocr_score(self, frame):
        ''' DEPRECATED: Use get_score(); there is no need to OCR as the score can be constructed
                        from the matrix directly
        '''
        score_region = cv.extract_region_from_image(frame.grayscale_frame, self.game.screen_regions["CURRENT_SCORE"])
        
        images, text_regions = extract_ocr_candidates(score_region)

        if len(images) == 0:
            return None 

        ocr = perform_ocr(images[0], scale=15)
        ocr_cand = ocr.replace(' ', '')
        
        try:
            ocr_int = int(ocr_cand)
        except ValueError:
            ocr_int = None
                
        return ocr_int

    def _get_score(self, game_matrix):
        return np.sum([self.game.point_values[game_matrix[x][y]] for x in range(len(game_matrix)) for y in range(len(game_matrix[0]))])

    def get_context(self, frame):
        # Generate a full contextual wrapping of the current game;
        context = {}

        if self._is_game_over(frame):
            context['game_over'] = True
            return context
        
        context['game_over'] = False
        context['game_matrix'], context['numeric_matrix'] = self._build_game_matrix(frame)

        if not context['game_matrix']:
            return False
            
        context['current_score'] = self._get_score(context['game_matrix'])

        return context

    class MyAPINamespace:

        @classmethod
        def my_namespaced_api_function(cls):
            api = TwentyFourtyEightAPI.instance
