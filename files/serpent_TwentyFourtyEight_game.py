from serpent.game import Game

from .api.api import TwentyFourtyEightAPI

from serpent.utilities import Singleton

from .environments.numeric_matrix_environment import NumericMatrixEnvionment

import time

class SerpentTwentyFourtyEightGame(Game, metaclass=Singleton):

    def __init__(self, **kwargs):
        kwargs["platform"] = "retroarch"

        kwargs["window_name"] = "RetroArch 2048 v1.0 45655d3" # Ensure that this Window Name is Correct
        
        kwargs["rom_path"] = "" # No rom is used for the 2048 Core
        kwargs["core_path"] = "\\AppData\\Roaming\\RetroArch\\cores\\2048_libretro.dll" # Specify the correct path to the 2048 core DLL

        super().__init__(**kwargs)

        self.api_class = TwentyFourtyEightAPI
        self.api_instance = None

        self.environments = {
            "NUMERIC": NumericMatrixEnvionment
        }
        self.environment_data = dict()

    @property
    def screen_regions(self):
        regions = {
            "CURRENT_SCORE": (50, 12, 89, 251),
            "BEST_SCORE": (8, 263, 97, 502),
            "GAME_BOARD": (106, 11, 506, 504),
            "TILES": {}
        }

        # Tile Size (108, 90)
        # margin size 10

        for ii in range(4):
            # Rows
            for jj in range(4):
                # Columns
                tile_name = "TILE_"+str(ii*4+jj)
                regions["TILES"][tile_name] = (regions["GAME_BOARD"][0] + 10*(ii+1) + 90*ii,
                                               regions["GAME_BOARD"][1] + 10*(jj+1) + 110*jj,
                                               regions["GAME_BOARD"][0] + 100*(ii+1),
                                               regions["GAME_BOARD"][1] + 120*(jj+1))


        return regions
    
    @property
    def point_values(self):
        points = {
                    'blank': 0,
                    '2': 0,
                    '4': 8,
                    '8': 32,
                    '16': 96,
                    '32': 256,
                    '64': 640,
                    '128': 1536,
                    '256': 3584,
                    '512': 8192,
                    '1024': 18432,
                    '2048': 40960,
                    '4096': 90112}

        return points

    @property
    def styles(self):
        # Blank: #eee4da [205, 192, 180]
        # 2: #eee4da     [238, 228, 218]
        # 4: #ede0c8     [237, 224, 200]
        # 8: #f2b179     [242, 177, 121]
        # 16: #f59563    [245, 149, 99]
        # 32: #f67c5f    [246, 124, 95]
        # 64: #f65e3b    [246, 94, 59]
        # 128: #edcf72   [237, 207, 114]
        # 256: #edcc61   [237, 204, 97]
        # 512: #edc850   [237, 200, 80]
        # 1024: #edc53f  [237, 197, 63]
        # 2048: #edc22e  [237, 194, 46]
        # 4096+: #3c3a32 [60, 58, 50]

        styles = [
            '#%02x%02x%02x' % (205, 192, 180),
            '#%02x%02x%02x' % (238, 228, 218),
            '#%02x%02x%02x' % (237, 224, 200),
            '#%02x%02x%02x' % (242, 177, 121),
            '#%02x%02x%02x' % (245, 149, 99),
            '#%02x%02x%02x' % (246, 124, 95),
            '#%02x%02x%02x' % (246, 94, 59),
            '#%02x%02x%02x' % (237, 207, 114),
            '#%02x%02x%02x' % (237, 204, 97),
            '#%02x%02x%02x' % (237, 200, 80),
            '#%02x%02x%02x' % (237, 197, 63),
            '#%02x%02x%02x' % (237, 194, 46),
            '#%02x%02x%02x' % (60, 58, 50)]

        return styles

    def after_launch(self):
        # Call to standard after launch
        super().after_launch()
        
        # Resize Window for Easy Proportions/Extraction
        self.window_controller.resize_window(window_id=self.window_id, width=530, height=573)
        self.window_geometry = self.extract_window_geometry()