from xmlrpc.client import boolean
#To move you use either W or up arrow to go up and S or down arrow to go down. To shoot you press space
#Ship is from clayster2012 on https://opengameart.org/content/jet-fighter
#Background is from Cethiel https://opengameart.org/content/desert-background-0
#Bullet is from https://opengameart.org/content/bullets-game-asset
#Sound is from https://opengameart.org/content/collaboration-sound-effects-shooting-sounds-002
#Kyle Stearns
import arcade
import pathlib
from enum import auto, Enum
class MoveEnum(Enum):
    NONE = auto()
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


class MinimalSprite(arcade.Sprite):
    def __init__(self, ship_path: str, speed: int, game_window):
        super().__init__(ship_path)
        self.speed = speed
        self.game = game_window

    def move(self, direction: MoveEnum):
        #  as a class exercise, lets fix this so it doesn't go off the window
        if direction == MoveEnum.UP and not self.center_y + self.height / 2 > self.game.height:
            self.center_y += self.speed
        elif direction == MoveEnum.DOWN and not self.center_y - self.height / 2 < 0:
            self.center_y -= self.speed


        else:  # should be MoveEnum.NONE
            pass


class BackgroundSprite(arcade.Sprite):
    def __init__(self, back: str, Scrollspeed: int, game_window):
        super().__init__(back)
        self.speed = Scrollspeed
        self.game = game_window

        self.scale = 2

    def move(self, direction: MoveEnum):

        if self.center_x+self.width/2<self.game.width:
            self.game.Backbool=True
            self.center_x -= self.speed

        else:
            self.center_x -= self.speed
            self.game.Spawned = False
            self.game.Backbool=False

class BulletSprite(arcade.Sprite):
    def __init__(self, bullet: str, BulletSpeed: int, game_window):
        super().__init__(bullet)
        self.speed = BulletSpeed
        self.game = game_window

        self.scale = .05

    def move(self, direction: MoveEnum):

        self.center_x += self.speed * 10


class MimimalArcade(arcade.Window):

    def __init__(self, image_name: str, back_str: str, snow_str: str, shoot_str:str,screen_w: int = 800, screen_h: int = 800):
        super().__init__(screen_w, screen_h)
        self.image_path = pathlib.Path.cwd() / 'Assets' / image_name
        self.background_path = pathlib.Path.cwd() / 'Assets' / back_str
        self.bullet_path = pathlib.Path.cwd() / 'Assets' / snow_str
        self.Shot_sound_path = pathlib.Path.cwd() / 'Assets' / shoot_str
        self.pict = None
        self.background = None
        self.bullet = None
        self.direction = MoveEnum.NONE
        self.backDone=False
        self.Backbool=False
        self.Spawned=False
        self.Bulletbool=False
    def setup(self):
        self.pict = MinimalSprite(str(self.image_path), speed=7, game_window=self)
        self.background = BackgroundSprite(str(self.background_path), Scrollspeed=6, game_window=self)
        self.bullet = BulletSprite(str(self.bullet_path), BulletSpeed = 3, game_window=self)
        self.pict.center_x = 500
        self.pict.center_y = 500
        self.bullet.center_x=self.pict.center_x
        self.bullet.center_y=self.pict.center_y
        self.background.center_x = 600
        self.background.center_y = 400
        self.shot_sound = arcade.load_sound(self.Shot_sound_path)
        self.pictlist = arcade.SpriteList()
        self.backlist = arcade.SpriteList()
        self.bulletlist = arcade.SpriteList()


        self.backlist.append(self.background)
        self.pictlist.append(self.pict)

    def on_update(self, delta_time: float):
        # to get really smooth movement we would use the delta time to
        # adjust the movement, but for this simple version I'll forgo that.
        self.backlist.update()


        self.pict.move(self.direction)
        #I learned to do the for loop with the object and list from the python arcade website
        for self.bullet in self.bulletlist:
            self.bullet.move(self.direction)
            if self.bullet.center_x>self.width:
                self.bulletlist.remove(self.bullet)

        self.bulletlist.update()
        for self.background in self.backlist:
            self.background.move(self.direction)
            if self.background.center_x+self.width<-300:
                self.backlist.remove(self.background)
                self.Spawned=False
                self.Backbool=False

        if self.Backbool==True and self.Spawned==False:
            self.background = BackgroundSprite(str(self.background_path), Scrollspeed=6, game_window=self)
            self.backlist.append(self.background)
            self.background.center_x = 2257
            self.background.center_y = 400
            self.Spawned=True

    def on_draw(self):
        """ Render the screen. """
        arcade.start_render()
        # Code to draw the screen goes here

        self.backlist.draw()
        self.pictlist.draw()
        self.bulletlist.draw()
    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        if key == arcade.key.UP or key == arcade.key.W:
            self.direction = MoveEnum.UP
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.direction = MoveEnum.DOWN
        if key == arcade.key.SPACE:
            self.bullet = BulletSprite(str(self.bullet_path), BulletSpeed=3, game_window=self)
            self.bullet.center_x = self.pict.center_x+100
            self.bullet.center_y = self.pict.center_y

            self.bulletlist.append(self.bullet)
            arcade.play_sound(self.shot_sound)
    def on_key_release(self, key: int, modifiers: int):
        """called by arcade for keyup events"""
        if (key == arcade.key.UP or key == arcade.key.W) and \
                self.direction == MoveEnum.UP:
            self.direction = MoveEnum.NONE
        if (key == arcade.key.DOWN or key == arcade.key.S) and \
                self.direction == MoveEnum.DOWN:
            self.direction = MoveEnum.NONE


def main():
    """ Main method """
    window = MimimalArcade("PlayerShip.png", "Desert Clean.png", "Bullet2.png", "ShootSound.mp3",screen_w=1000)

    window.setup()
    arcade.run()


if __name__ == '__main__':
    main()


