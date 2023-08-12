import pygame
from cube.cube import Cube
from gameengine.basescene import BaseScene
from gameengine.display import Display
from gameengine.engine import Engine
from gameengine.keyboard import Keyboard
from gameengine.window import Window
from values import ORIENTATION


class MainScene(BaseScene):
    def __init__(self):
        super().__init__()
        self.color_fill = (127, 127, 127)
        self.cube = Cube(50)

        self.font = pygame.font.SysFont("arial", 15)
        self.font_rendered = self.font.render(
            "Moves keys: F U R D L B\n"
            + "Mod keys:\n"
            + "   Reverse move: LSHIFT + Move\n"
            + "   Two Moves: 2\n"
            + "Reset: DELETE\n"
            + "Auto Solve: END\n"
            + "Single Scramble: PAGE DOWN\n"
            + "Auto Scramble: PAGE UP\n",
            True,
            (0, 0, 0),
        )

        self.add_children(self.cube)

    def update(self):
        super().update()
        if Keyboard.get_pressed(pygame.K_LSHIFT):
            mod_key = "'"
        elif (Keyboard.get_pressed(pygame.K_2) is not None) and (
            Keyboard.get_pressed(pygame.K_KP_2) is not None
        ):
            mod_key = "2"
        else:
            mod_key = ""
        for event in Keyboard.pressed_in_frame[pygame.KEYDOWN]:
            match event.key:
                case pygame.K_f:
                    self.cube.move(ORIENTATION.FRONT + mod_key)
                case pygame.K_u:
                    self.cube.move(ORIENTATION.UP + mod_key)
                case pygame.K_r:
                    self.cube.move(ORIENTATION.RIGHT + mod_key)
                case pygame.K_d:
                    self.cube.move(ORIENTATION.DOWN + mod_key)
                case pygame.K_l:
                    self.cube.move(ORIENTATION.LEFT + mod_key)
                case pygame.K_b:
                    self.cube.move(ORIENTATION.BACK + mod_key)
                case pygame.K_DELETE:
                    self.cube.reset()
                case pygame.K_END:
                    self.cube.auto_solve()
                case pygame.K_PAGEDOWN:
                    self.cube.random_move()
        if Keyboard.get_pressed(pygame.K_PAGEUP):
            self.cube.random_move()
        if Engine.request_quit:
            Engine.system_exit()

    def draw(self):
        super().draw()
        SIX_BLOCKS = self.cube.scale * 6
        Display.surface.blit(self.font_rendered, (SIX_BLOCKS + 5, 2))
        Display.surface.blit(
            self.font.render(
                "\n".join(self.cube.log_moves[-8:][::-1]), True, (0, 0, 0)
            ),
            (SIX_BLOCKS + 5, SIX_BLOCKS + 5),
        )


if __name__ == "__main__":
    Window.set_title("Rubik")
    Window.set_size((600, 450))
    Display.update_display_from_window()

    Engine.set_scene(MainScene())

    Engine.start_loop()
