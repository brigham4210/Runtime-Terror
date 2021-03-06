from enum import Enum

from constant import *
from numbers_and_math import NumberBlock, BlockType, NumberBlockHitbox


class PlayerOrientation(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


class Player(arcade.Sprite):
    def __init__(self, window):
        super().__init__()
        self._block_position_offset = None
        self.window = window

        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.space_pressed = False
        self.shift_pressed = False

        self.orientation: PlayerOrientation = PlayerOrientation.DOWN
        self.block = None

        # Load Textures
        PLAYER_TEXTURES.append(
            arcade.load_texture("assets/kenney_sokobanpack/PNG/Default size/Player/player_08.png"))  # Up
        PLAYER_TEXTURES.append(
            arcade.load_texture("assets/kenney_sokobanpack/PNG/Default size/Player/player_05.png"))  # Down
        PLAYER_TEXTURES.append(
            arcade.load_texture("assets/kenney_sokobanpack/PNG/Default size/Player/player_20.png"))  # Left
        PLAYER_TEXTURES.append(
            arcade.load_texture("assets/kenney_sokobanpack/PNG/Default size/Player/player_17.png"))  # Right

        # Set up the player, specifically placing it at these coordinates.
        self.center_x = 1860
        self.center_y = 1800
        self.scale = CHARACTER_SCALING
        self.texture = PLAYER_TEXTURES[0]

    def setup(self):
        """
        Set up this player sprite. Not currently being used for anything since everything is
        initialized in __init__, but this is here in case we need it.
        """

    def update(self):
        """
        Frame-by-frame logic for the player object. Called by window.on_update().
        """
        self.update_player_speed()
        self.texture_update()
        try:
            self.check_for_block_collisions()
        except AttributeError:
            pass
        self._move_block()
        if self.block is not None and not self.space_pressed:
            self.release_block()

    def update_player_speed(self):
        """
        Calculates speed and moves the player based on which keys are pressed.
        """

        # Calculate speed base on keys pressed
        self.change_x = 0
        self.change_y = 0

        speed = PLAYER_MOVEMENT_SPEED * PLAYER_RUN_MULTIPLIER \
            if self.shift_pressed else PLAYER_MOVEMENT_SPEED

        if self.up_pressed and not self.down_pressed:
            self.change_y = speed
        elif self.down_pressed and not self.up_pressed:
            self.change_y = -speed
        if self.left_pressed and not self.right_pressed:
            self.change_x = -speed
        elif self.right_pressed and not self.left_pressed:
            self.change_x = speed

        self.window.scroll_to_player()

    def on_key_press(self, key, modifiers):
        """Called by the arcade.Window object whenever a key is pressed."""

        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = True
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True
        elif key == arcade.key.SPACE:
            self.space_pressed = True
        elif key == arcade.key.LSHIFT or key == arcade.key.RSHIFT:
            self.shift_pressed = True

    def on_key_release(self, key, modifiers):
        """Called by the arcade.Window object when the user releases a key."""

        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = False
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = False
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False
        elif key == arcade.key.SPACE:
            self.space_pressed = False
        elif key == arcade.key.LSHIFT or key == arcade.key.RSHIFT:
            self.shift_pressed = False

    def texture_update(self):
        """Change the player's texture based on Orientation."""

        if self.up_pressed:
            self.orientation = PlayerOrientation.UP
        if self.down_pressed:
            self.orientation = PlayerOrientation.DOWN
        if self.left_pressed:
            self.orientation = PlayerOrientation.LEFT
        if self.right_pressed:
            self.orientation = PlayerOrientation.RIGHT
        self.texture = PLAYER_TEXTURES[self.orientation.value]

    def grab_block(self, block: NumberBlock):
        """
        Grab a given NumberBlock if it is movable. This will set the
        relative block offset at the moment the player grabbed it.
        """
        if block.block_type == BlockType.MOVABLE \
                or block.block_type == BlockType.INCORRECT:
            self.block = block
            self._block_position_offset = self._get_block_position_offset()
            block.remove_from_sprite_lists()
            self.window.scene.get_sprite_list(LAYER_NAME_PLAYER).append(block)

    def release_block(self):
        """
        Let go of whatever block the player is holding by setting self.block to None.
        Called every time the space bar is released.
        """
        # Moved the call to NumberBlock.auto_move() here instead of inside move_block.
        # This makes it so the player only drops off the block once the space bar is released.
        # Reduces the amount of collision checking that has to happen which should improve performance.
        self.block.auto_move()
        self.block.remove_from_sprite_lists()
        self.window.scene.get_sprite_list(LAYER_NAME_NUMBER).append(self.block)
        self.block = None
        self.window.update_score()

    def check_for_block_collisions(self):
        """
        This is the function that checks if this (the player object) is colliding
        with the hitboxes of any NumberBlocks. It also handles displaying the caption.
        """
        if self.block is None:
            blocks = arcade.check_for_collision_with_list(self,
                                                          self.window.scene.get_sprite_list(LAYER_NAME_NUMBER_HITBOX))
            if len(blocks) != 0:
                assert (isinstance(blocks[0], NumberBlockHitbox))
                hitbox: NumberBlockHitbox = pick_nearest_collision(self, blocks)
                try:
                    block: NumberBlock = hitbox.parent_block
                except AttributeError:
                    print("Hitbox has no attached parent_block for some reason")
                    raise AttributeError
                # Make sure this block is actually a NumberBlock
                assert (isinstance(block, NumberBlock))
                if self.space_pressed:
                    self.grab_block(block)
                    self.window.set_drawing_caption(False)
                else:
                    if block.block_type == BlockType.MOVABLE \
                            or block.block_type == BlockType.INCORRECT:
                        self.window.set_drawing_caption(True)
            else:
                self.window.set_drawing_caption(False)

    def _move_block(self):
        """
        Move the held block along with the player based on an offset relative
        to the player's position.
        This is called by self.update() every frame to ensure the block
        the player is grabbing gets moved along with the player.
        """
        if self.block is not None:
            self.block.move_to(
                self.center_x + self._block_position_offset[0],
                self.center_y + self._block_position_offset[1]
            )

    def _get_block_position_offset(self):
        """
        Determine the position offset for the block relative to the player for
        a given instant in time.
        """
        assert (self.block is not None)
        offset_x = self.block.center_x - self.center_x
        offset_y = self.block.center_y - self.center_y
        offset = 1
        if self.orientation == PlayerOrientation.UP:
            offset_y += offset
        elif self.orientation == PlayerOrientation.DOWN:
            offset_y -= offset
        elif self.orientation == PlayerOrientation.LEFT:
            offset_x -= offset
        else:
            # Assume facing right
            offset_x += offset
        return offset_x, offset_y
