# Constants
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900

SCREEN_TITLE = "RUNTIME TERROR"
MAP = ""
MAP_SIZE = 1550

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 5
PLAYER_RUN_MULTIPLIER = 1.5

CAMERA_SPEED = 0.1
VIEWPORT_MARGIN = 200

# Constants used to scale our sprites from their original size
CHARACTER_SCALING = 1
TILE_SCALING = 2
NUMBER_BLOCK_SCALING = TILE_SCALING / 2
NUMBER_SCALING = NUMBER_BLOCK_SCALING * 1.3

MAPS = [
    # "maps/joel-demo.tmx",
    "maps/Main-Spawn.tmx",
    "maps/Castle-Area.tmx",
    "maps/Desert-Area.tmx",
    "maps/Grass-Area.tmx",
    "maps/Urban-Area.tmx",
]

PLAYER_IMAGE_PATH = ":resources:images/animated_characters/male_person/malePerson_idle.png"

LAYER_NAME_WALLS = "walls"
LAYER_NAME_BACKGROUND = "background"
LAYER_NAME_PLAYER = "player"
LAYER_NAME_NUMBER = "Numbers"
LAYER_NAME_NUMBER_HITBOX = "number_hitbox"
LAYER_NAME_NUMBER_SYMBOLS = "number_symbols"
LAYER_NAME_NUMBER_TARGETS = "number_targets"
LAYER_NAME_MATH_PROBLEM_ORIGIN = "math_problems"
LAYER_NAME_EXIT = "exits"

PLAYER_TEXTURES = []
IMG_PATH_EXT = ".png"

CRATE_BASE_PATH = "assets/kenney_sokobanpack/PNG/Default size/Crates/"
CRATE_BLUE_PATH = "assets/kenney_sokobanpack/PNG/Default size/Crates/crate_09.png"
CRATE_BROWN_PATH = "assets/kenney_sokobanpack/PNG/Default size/Crates/crate_07.png"
TRANSPARENT_BOX_PATH = "assets/transparent.png"
TARGET_BOX = "assets/kenney_sokobanpack/PNG/Default size/Crates/crate_29.png"
TILE_SIZE = 32

NUM_BASE_PATH = "assets/kenney_sokobanpack/PNG/Default size/Numbers/"

# ******* DANGER ZONE *******
# Brother Helfrich says to never do this stuff but I'm doing it anyway, sorry james
GLOBAL_SCENE = None
