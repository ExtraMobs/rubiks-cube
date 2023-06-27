import twophase.solver as sv

from cube.graphical import Graphical
from cube.movement import Movement
from values import COLOR, ORIENTATION


class Cube(Graphical, Movement):
    def __init__(self, scale):
        Graphical.__init__(self, scale)
        Movement.__init__(self)

        self.reset()

    def update(self):
        Movement.update(self)

    def auto_solve(self):
        Movement.auto_solve(self, sv.solve(self.get_state("URFDLB")).split(" "))

    def reset(self):
        self.faces = self.get_default_pieces()
        self.draw_cube()

    def get_state(self, order=ORIENTATION.IN_TUPLE):
        return "".join(
            [
                ORIENTATION.IN_TUPLE[COLOR.IN_TUPLE.index(color)]
                for orientation in order
                for row in self.faces[ORIENTATION.IN_TUPLE.index(orientation)]
                for color in row
            ]
        )

    @classmethod
    def get_default_pieces(cls):
        faces = []
        for index in range(6):
            faces.append([])
            for y in range(3):
                faces[index].append([])
                for _ in range(3):
                    faces[index][y].append(COLOR.IN_TUPLE[index])
        return faces
