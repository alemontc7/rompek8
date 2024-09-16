from AgenteIA.Entorno import Entorno
from AgenteRK8 import AgenteRK8
import pygame
import sys
import pyttsx3
import time

class Tablero(Entorno):
    def __init__(self):
        Entorno.__init__(self)
        pygame.init()
        self._init_display()
        self._init_images()
        self._init_buttons()
        self.engine = pyttsx3.init()

    def _init_display(self):
        self.WIDTH, self.HEIGHT = 450, 550
        self.GRID_SIZE = 3
        self.CELL_SIZE = 150
        self.BUTTON_HEIGHT = 50
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Rompecabezas 8")

    def _init_images(self):
        images = [pygame.image.load(f"imagen/p0{i}.jpg") for i in range(9)]
        self.images = [pygame.transform.scale(image, (self.CELL_SIZE, self.CELL_SIZE)) for image in images]

    def _init_buttons(self):
        button_font = pygame.font.Font(None, 20)
        button_y = self.HEIGHT - self.BUTTON_HEIGHT - 10
        self.buttons = [
            {
                "text": button_font.render("Agente te da una pista", True, (255, 255, 255)),
                "rect": pygame.Rect(self.WIDTH // 2 - 225, button_y, 150, self.BUTTON_HEIGHT),
                "color": (0, 128, 255),
                "action": self._hint_action
            },
            {
                "text": button_font.render("Agente mueve ficha", True, (255, 255, 255)),
                "rect": pygame.Rect(self.WIDTH // 2 - 75, button_y, 150, self.BUTTON_HEIGHT),
                "color": (0, 200, 0),
                "action": self._agent_move_action
            },
            {
                "text": button_font.render("Agente resuelve todo", True, (255, 255, 255)),
                "rect": pygame.Rect(self.WIDTH // 2 + 75, button_y, 150, self.BUTTON_HEIGHT),
                "color": (200, 0, 0),
                "action": self._solve_all_action
            }
        ]

    def insertar(self, agente):
        self.current_state = agente.estado_inicial
        self.goal_state = agente.estado_meta
        print(f"goal state is {self.goal_state} estado actual es {self.current_state}")
        self.agentes.append(agente)

    def get_current_state(self):
        return [row[:] for row in self.current_state]

    def find_empty_cell(self):
        for i in range(self.GRID_SIZE):
            for j in range(self.GRID_SIZE):
                if self.current_state[i][j] == 0:
                    return i, j
        return None

    def is_adjacent(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1]) == 1

    def is_valid_position(self, pos):
        return 0 <= pos[0] < self.GRID_SIZE and 0 <= pos[1] < self.GRID_SIZE

    def swap_cells(self, pos1, pos2):
        if self.is_valid_position(pos1) and self.is_valid_position(pos2):
            self.current_state[pos1[0]][pos1[1]], self.current_state[pos2[0]][pos2[1]] = \
                self.current_state[pos2[0]][pos2[1]], self.current_state[pos1[0]][pos1[1]]
            print("estado actualizado:")
            for row in self.current_state:
                print(row)
        else:
            print("no se puede")

    def handle_click(self, pos):
        x, y = pos
        grid_x, grid_y = y // self.CELL_SIZE, x // self.CELL_SIZE
        empty_cell = self.find_empty_cell()
        if empty_cell and self.is_adjacent((grid_x, grid_y), empty_cell) and self.is_valid_position((grid_x, grid_y)):
            self.swap_cells((grid_x, grid_y), empty_cell)
        return self.check_win_condition()

    def check_win_condition(self):
        if self.current_state == self.goal_state:
            win_message = "Ganaste!"
            self.engine.say(win_message)
            self.engine.runAndWait()
            return True
        return False

    def _call_solver(self):
        solver = AgenteRK8()
        solver.tecnica = "a_estrella"
        solver.heuristica = "manhattan"
        solver.estado_inicial = self.get_current_state()
        solver.estado_meta = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        solver.programa()
        return solver

    def _apply_move(self, move):
        numero, direccion = move
        empty_cell = self.find_empty_cell()
        for i in range(self.GRID_SIZE):
            for j in range(self.GRID_SIZE):
                if self.current_state[i][j] == numero:
                    self.swap_cells((i, j), empty_cell)
                    return

    def _update_display(self):
        self.screen.fill((200, 200, 200))
        for i in range(self.GRID_SIZE):
            for j in range(self.GRID_SIZE):
                index = self.current_state[i][j]
                self.screen.blit(self.images[index], (j * self.CELL_SIZE, i * self.CELL_SIZE))
        self._draw_buttons()
        pygame.display.flip()

    def _draw_buttons(self):
        for button in self.buttons:
            pygame.draw.rect(self.screen, button["color"], button["rect"])
            text_rect = button["text"].get_rect(center=button["rect"].center)
            self.screen.blit(button["text"], text_rect)

    def _hint_action(self):
        solver = self._call_solver()
        solver.decir_instruccion()

    def _agent_move_action(self):
        solver = self._call_solver()
        if solver.acciones and len(solver.acciones) > 1:
            move = solver.encontrar_movimiento_numeral(solver.acciones[0], solver.acciones[1])
            if move:
                numero, direccion = move
                empty_cell = self.find_empty_cell()
                print(f"tengo que cambiar {numero} por el 0 que esta en {empty_cell}")
                self._apply_move(move)

    def _solve_all_action(self):
        solver = self._call_solver()
        if solver.acciones:
            for i in range(1, len(solver.acciones)):
                move = solver.encontrar_movimiento_numeral(solver.acciones[i-1], solver.acciones[i])
                if move:
                    print(f"Mover {move[0]} {move[1]}")
                    self._apply_move(move)
                    self._update_display()
                    self._handle_events()
                    pygame.time.delay(500)
        else:
            print("No se encontró solución.")
            self.engine.say("No se encontró solución.")
            self.engine.runAndWait()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def ejecutar(self):
        running = True
        while running:
            if self.check_win_condition():
                break
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for button in self.buttons:
                        if button["rect"].collidepoint(event.pos):
                            button["action"]()
                    if self.handle_click(event.pos):
                        running = False

            self._update_display()