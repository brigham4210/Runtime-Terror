import arcade
from numbers_and_math import VisualMathProblem, NumberBlock
from pyglet.math import Vec2
from math import sqrt
from constant import *
from player import Player


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=True)

        # Our scene object
        self.exit_list = None
        self.problem = None
        self.scene = None
        self.player = Player(self)

        # Load Textures
        PLAYER_TEXTURES.append(arcade.load_texture("assets/kenney_sokobanpack/PNG/Default size/Player/player_02.png"))
        PLAYER_TEXTURES.append(arcade.load_texture("assets/kenney_sokobanpack/PNG/Default size/Player/player_05.png"))
        PLAYER_TEXTURES.append(arcade.load_texture("assets/kenney_sokobanpack/PNG/Default size/Player/player_20.png"))
        PLAYER_TEXTURES.append(arcade.load_texture("assets/kenney_sokobanpack/PNG/Default size/Player/player_11.png"))

        # Our physics engine
        self.physics_engine = None
        # Game Logic
        self.map_index = 0  # Index representing which map within global MAPS we're loading for this level.
        self.tile_map = None  # This will hold the actual TileMap object loaded from the .tmx file

        self.camera = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.view_bottom = 0
        self.view_left = 0

        # A Camera that can be used to draw GUI elements
        self.gui_camera = None

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        """Set up the current map/scene/stage/level here. Call this function to restart the game.
        The map file must be loaded first, then the scene object can be initialized from that.
        Then the player sprite can be loaded and added to the scene afterward so that they draw
        in the proper order.
        """
        map_name = "maps/Main-Spawn.tmx"
        # Load the Tiled Map
        layer_options = {
            
        }
        self.tile_map = arcade.load_tilemap(MAPS[self.map_index], TILE_SCALING, layer_options)

        # Initialize Scene from the tilemap
        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        # repeat line 91 and line 88
        # Create the Sprite lists
        self.scene.add_sprite_list(LAYER_NAME_NUMBER_TARGETS)
        self.scene.add_sprite_list(LAYER_NAME_PLAYER)
        self.scene.add_sprite_list(LAYER_NAME_NUMBER)
        self.scene.add_sprite_list(LAYER_NAME_NUMBER_SYMBOLS)
        self.scene.add_sprite_list(LAYER_NAME_NUMBER_HITBOX)

        # self.player_list.append(self.player_sprite)
        self.scene.add_sprite(LAYER_NAME_PLAYER, self.player)
        # self.scene.add_sprite("Player", self.player_sprite)
        self.exit_list = arcade.SpriteList()
        # self.scene.add_sprite("castle", self.castle_sprite)

        # map_name = f":resources:tmx_maps/map2_level_{level}.tmx"
        # my_map = arcade.tilemap.read_tmx(map_name)

        # self.wall_list = arcade.tilemap.process_layer(map_object=my_map, layer_name=walls, scaling=TILE_SCALING, use_spatial_hash=True)

        # Make a test math problem
        self.problem = VisualMathProblem(self.scene, SCREEN_WIDTH / 2 - 200, SCREEN_HEIGHT / 2, 1, 10)
        self.problem.draw()
        # self.problem.log()

        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player, [
                self.scene.get_sprite_list(LAYER_NAME_WALLS),
                self.scene.get_sprite_list(LAYER_NAME_NUMBER)
            ]
        )

    def player_hit_door(self):
        collisions = arcade.check_for_collision_with_list(self.player, self.scene.get_sprite_list(LAYER_NAME_EXIT))
        if len(collisions) > 0:
            self.map_index += 1
            self.setup()
            print("We hit a door to advance to next level")

    # def load_new_level(self):
    #  """
    #   load_new_level() has to be called from update.
    # """

    #   layer_options = {}
    #  self.scene = arcade.Scene.from_tilemap(self.tile_map)
    # self.tile_map = arcade.load_tilemap(MAPS[self.map_index], TILE_SCALING, layer_options)
    # if self.level == 1 :
    #   self.level += 1
    # if self.level == 2:
    #   self.level+= 1
    # if self.level == 3:
    #   self.level += 1

    # if self.player == exit and self.level == 1:
    #   self.player == 2
    #  self.player += 1

    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        arcade.start_render()

        # Draw our Scene
        self.scene.draw()

        self.camera.use()

        # Draw Math Layer
        self.scene.get_sprite_list(LAYER_NAME_NUMBER).update_animation()

        self.caption()

    def on_update(self, delta_time):

        """Movement and game logic"""

        # Move the player with the physics engine
        self.physics_engine.update()
        # self.texture_update()
        # self.load_new_level()
        self.player_hit_door()

        # self.load_new_level()
        # check for exit collision thie is call setup for new levels
        # if self.player_sprite.center_x >= self.end_of_map:
        #   self.level += 1
        # Update the player object
        self.player.update()

    def on_key_press(self, symbol: int, modifiers: int):
        self.player.on_key_press(symbol, modifiers)

    def on_key_release(self, symbol: int, modifiers: int):
        self.player.on_key_release(symbol, modifiers)

    def caption(self):
        """This Function is to display the caption when it touches the boxes"""

        cap = "Press Space to lift it up"

        arcade.draw_text(
            cap,
            self.view_left + SCREEN_WIDTH * 0.3,
            self.view_bottom + SCREEN_HEIGHT * 0.8,
            arcade.csscolor.WHITE,
            30, )

    def scroll_to_player(self):

        # --- Manage Scrolling ---

        # Scroll left
        left_boundary = self.view_left + VIEWPORT_MARGIN
        if self.player.left < left_boundary:
            self.view_left -= left_boundary - self.player.left

        # Scroll right
        right_boundary = self.view_left + self.width - VIEWPORT_MARGIN
        if self.player.right > right_boundary:
            self.view_left += self.player.right - right_boundary

        # Scroll up
        top_boundary = self.view_bottom + self.height - VIEWPORT_MARGIN
        if self.player.top > top_boundary:
            self.view_bottom += self.player.top - top_boundary

        # Scroll down
        bottom_boundary = self.view_bottom + VIEWPORT_MARGIN
        if self.player.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player.bottom

        # Scroll to the proper location
        position = Vec2(self.view_left, self.view_bottom)
        self.camera.move_to(position, CAMERA_SPEED)


def main():
    """Main function"""
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
