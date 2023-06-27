import pygame

from gameengine.basechild import BaseChild
from gameengine.display import Display
from gameengine.resources import Resources


class Graphical(BaseChild):
    def __init__(self, scale):
        self.cube_surface = Resources.Surface.new((12, 9))
        self.cube_surface.fill((0, 0, 0, 0))
        self.set_scale(scale)

    def set_scale(self, scale):
        self.surface = Resources.Surface.new((12 * scale, 9 * scale))
        self.grid = self.surface.copy()
        self.rect = self.surface.get_rect()
        self.scale = scale
        if scale > 2:
            for y in range(9):
                y_pos = y * scale
                for x in range(12):
                    x_pos = x * scale
                    w = scale // 20
                    if 3 <= x < 6 or 3 <= y < 6:
                        pygame.draw.rect(
                            self.grid,
                            (0, 0, 0),
                            pygame.Rect(x_pos, y_pos, scale, scale),
                            w,
                        )
                        if (x, y) in ((3, 0), (0, 3), (3, 3), (6, 3), (9, 3), (3, 6)):
                            rect = pygame.Rect(
                                x_pos - w,
                                y_pos - w,
                                scale * 3 + w * 2,
                                scale * 3 + w * 2,
                            )
                            pygame.draw.rect(self.grid, (0, 0, 0), rect, w * 4)

    def draw_cube(self):
        for index_face, face in enumerate(self.faces):
            for y, row in enumerate(face):
                match index_face:
                    case 0:
                        y = 3 + y
                    case 2:
                        y = 3 + y
                    case 3:
                        y = 6 + y
                    case 4:
                        y = 3 + y
                    case 5:
                        y = 3 + y
                for x, color in enumerate(row):
                    match index_face:
                        case 0:
                            x = 3 + x
                        case 1:
                            x = 3 + x
                        case 2:
                            x = 6 + x
                        case 3:
                            x = 3 + x
                        case 5:
                            x = 9 + x
                    self.cube_surface.fill(color, pygame.Rect((x, y), (1, 1)))

    def draw(self):
        pygame.transform.scale(self.cube_surface, self.surface.get_size(), self.surface)
        self.surface.blit(self.grid, (0, 0))
        Display.surface.blit(self.surface, self.rect)
