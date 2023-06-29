import random

import pygame

from values import ORIENTATION


class Movement:
    class SolveMove:
        solve_delay = 200
        type = pygame.event.custom_type()

        @classmethod
        def disable_timer(cls):
            pygame.time.set_timer(cls.type, 0, 0)

        @classmethod
        def enable_timer(cls, moves):
            pygame.time.set_timer(cls.type, cls.solve_delay, len(moves))

    def __init__(self) -> None:
        self._solve_moves = []
        self.log_moves = []

    def auto_solve(self, moves):
        self._solve_moves = moves
        if len(moves) == 0:
            self.SolveMove.disable_timer()
        else:
            self.SolveMove.enable_timer(moves)

    def random_move(self):
        mod_key = self._get_random_mod()
        self.move(random.choice(ORIENTATION.IN_TUPLE) + mod_key)

    def move(self, movements):
        movements = self.__filter_moves(movements)
        for command in movements:
            command, reverse, times = self.__check_move(command)
            if self.__exist(command):
                self.__add_log(command, reverse, times)
                self.__process_move(command, reverse, times)
        self.draw_cube()

    def update(self):
        if len(pygame.event.get(self.SolveMove.type)) > 0:
            if len(self._solve_moves) > 0:
                self.move(self._solve_moves[0])
                del self._solve_moves[0]
            else:
                self.SolveMove.disable_timer()

    def get_faces_for_movement(self, orientation):
        match orientation:
            case ORIENTATION.FRONT:
                return self.faces[:5] + [None]
            case ORIENTATION.UP:
                return self.faces[:3] + [None] + self.faces[4:]
            case ORIENTATION.RIGHT:
                return self.faces[:4] + [None] + self.faces[5:]
            case ORIENTATION.DOWN:
                return self.faces[:1] + [None] + self.faces[2:]
            case ORIENTATION.LEFT:
                return self.faces[:2] + [None] + self.faces[3:]
            case ORIENTATION.BACK:
                return [None] + self.faces[1:]

    def get_rows_and_cols_for_movement(self, movement, faces):
        face_front, face_up, face_right, face_down, face_left, face_back = faces
        rows_and_cols = [
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
        ]
        match movement:
            case ORIENTATION.FRONT:
                rows_and_cols[1] = list(face_up[-1])
                rows_and_cols[8] = [row[0] for row in face_right]
                rows_and_cols[3] = list(face_down[0])
                rows_and_cols[10] = [row[-1] for row in face_left]
            case ORIENTATION.UP:
                rows_and_cols[5] = list(face_back[0])
                rows_and_cols[2] = list(face_right[0])
                rows_and_cols[0] = list(face_front[0])
                rows_and_cols[4] = list(face_left[0])
            case ORIENTATION.RIGHT:
                rows_and_cols[6] = [row[-1] for row in face_front]
                rows_and_cols[7] = [row[-1] for row in face_up]
                rows_and_cols[11] = [row[0] for row in face_back]
                rows_and_cols[9] = [row[-1] for row in face_down]
            case ORIENTATION.DOWN:
                rows_and_cols[5] = list(face_back[-1])
                rows_and_cols[2] = list(face_right[-1])
                rows_and_cols[0] = list(face_front[-1])
                rows_and_cols[4] = list(face_left[-1])
            case ORIENTATION.LEFT:
                rows_and_cols[6] = [row[0] for row in face_front]
                rows_and_cols[7] = [row[0] for row in face_up]
                rows_and_cols[11] = [row[-1] for row in face_back]
                rows_and_cols[9] = [row[0] for row in face_down]
            case ORIENTATION.BACK:
                rows_and_cols[1] = list(face_up[0])
                rows_and_cols[8] = [row[-1] for row in face_right]
                rows_and_cols[3] = list(face_down[-1])
                rows_and_cols[10] = [row[0] for row in face_left]

        return rows_and_cols

    def rotate_face(self, face, reverse):
        if reverse:
            face[:] = [
                [face[0][2], face[1][2], face[2][2]],
                [face[0][1], face[1][1], face[2][1]],
                [face[0][0], face[1][0], face[2][0]],
            ]
        else:
            face[:] = [
                [face[2][0], face[1][0], face[0][0]],
                [face[2][1], face[1][1], face[0][1]],
                [face[2][2], face[1][2], face[0][2]],
            ]

    def apply_side_rotation(self, movement, faces, rows_and_cols, reverse):
        face_front, face_up, face_right, face_down, face_left, face_back = faces
        (
            row_front,
            row_up,
            row_right,
            row_down,
            row_left,
            row_back,
            col_front,
            col_up,
            col_right,
            col_down,
            col_left,
            col_back,
        ) = rows_and_cols
        match movement:
            case ORIENTATION.FRONT:
                if reverse:
                    face_up[-1][:] = col_right
                    for index, row in enumerate(face_right):
                        row[0] = row_down[::-1][index]
                    face_down[0][:] = col_left
                    for index, row in enumerate(face_left):
                        row[-1] = row_up[::-1][index]
                else:
                    face_up[-1][:] = col_left[::-1]
                    for index, row in enumerate(face_right):
                        row[0] = row_up[index]
                    face_down[0][:] = col_right[::-1]
                    for index, row in enumerate(face_left):
                        row[-1] = row_down[index]
            case ORIENTATION.UP:
                if reverse:
                    face_back[0][:] = row_right
                    face_right[0][:] = row_front
                    face_front[0][:] = row_left
                    face_left[0][:] = row_back
                else:
                    face_back[0][:] = row_left
                    face_right[0][:] = row_back
                    face_front[0][:] = row_right
                    face_left[0][:] = row_front
            case ORIENTATION.RIGHT:
                if reverse:
                    for index, row in enumerate(face_front):
                        row[-1] = col_up[index]
                    for index, row in enumerate(face_up):
                        row[-1] = col_back[::-1][index]
                    for index, row in enumerate(face_back):
                        row[0] = col_down[::-1][index]
                    for index, row in enumerate(face_down):
                        row[-1] = col_front[index]
                else:
                    for index, row in enumerate(face_front):
                        row[-1] = col_down[index]
                    for index, row in enumerate(face_up):
                        row[-1] = col_front[index]
                    for index, row in enumerate(face_back):
                        row[0] = col_up[::-1][index]
                    for index, row in enumerate(face_down):
                        row[-1] = col_back[::-1][index]
            case ORIENTATION.DOWN:
                if reverse:
                    face_back[-1][:] = row_left
                    face_right[-1][:] = row_back
                    face_front[-1][:] = row_right
                    face_left[-1][:] = row_front
                else:
                    face_back[-1][:] = row_right
                    face_right[-1][:] = row_front
                    face_front[-1][:] = row_left
                    face_left[-1][:] = row_back
            case ORIENTATION.LEFT:
                if reverse:
                    for index, row in enumerate(face_front):
                        row[0] = col_down[index]
                    for index, row in enumerate(face_up):
                        row[0] = col_front[index]
                    for index, row in enumerate(face_back):
                        row[-1] = col_up[::-1][index]
                    for index, row in enumerate(face_down):
                        row[0] = col_back[::-1][index]
                else:
                    for index, row in enumerate(face_front):
                        row[0] = col_up[index]
                    for index, row in enumerate(face_up):
                        row[0] = col_back[::-1][index]
                    for index, row in enumerate(face_back):
                        row[-1] = col_down[::-1][index]
                    for index, row in enumerate(face_down):
                        row[0] = col_front[index]
            case ORIENTATION.BACK:
                if reverse:
                    face_up[0][:] = col_left[::-1]
                    for index, row in enumerate(face_left):
                        row[0] = row_down[index]
                    face_down[-1][:] = col_right[::-1]
                    for index, row in enumerate(face_right):
                        row[-1] = row_up[index]
                else:
                    face_up[0][:] = col_right
                    for index, row in enumerate(face_left):
                        row[0] = row_up[::-1][index]
                    face_down[-1][:] = col_left
                    for index, row in enumerate(face_right):
                        row[-1] = row_down[::-1][index]

    def _get_random_mod(self):
        return (
            "'"
            if random.randint(0, 1) == 1
            else ("2" if random.randint(0, 1) == 1 else "")
        )

    def __is_reverse(self, command):
        return command[1] in ("'", "3")

    def __get_times(self, command):
        if command[1] == "2":
            return 2
        return 1

    def __is_redundant(self, command):
        return command[1] == "1"

    def __exist(self, command):
        return command in ORIENTATION.IN_TUPLE

    def __check_move(self, command):
        move_key = command[0]
        if len(command) == 2:
            reverse = self.__is_reverse(command)
            times = self.__get_times(command)
            redundance = self.__is_redundant(command)
            if (not reverse) and (times == 1) and not (redundance):
                raise Exception("Illegal movement")
            return move_key, reverse, times
        return move_key, False, 1

    def __add_log(self, command, reverse, times):
        self.log_moves.append(command + ("'" if reverse else "2" if times == 2 else ""))

    def __process_move(self, command, reverse, times):
        for _ in range(times):
            faces = self.get_faces_for_movement(command)
            rows_and_cols = self.get_rows_and_cols_for_movement(command, faces)

            self.rotate_face(faces[ORIENTATION.IN_TUPLE.index(command)], reverse)
            self.apply_side_rotation(command, faces, rows_and_cols, reverse)

    def __filter_moves(self, movements):
        if type(movements) is str:
            return movements.split(" ")
