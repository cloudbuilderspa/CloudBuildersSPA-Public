#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Juego de Snake implementado con principios de código limpio.
Utiliza Pygame para la interfaz gráfica y sigue el patrón de diseño orientado a objetos.
"""

import pygame
import random
import sys
from enum import Enum
from typing import List, Tuple, Optional


class Direction(Enum):
    """Enumeración para las direcciones posibles de movimiento."""
    UP = (0, -1)
    RIGHT = (1, 0)
    DOWN = (0, 1)
    LEFT = (-1, 0)


class Color:
    """Clase para definir los colores utilizados en el juego."""
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)


class Config:
    """Configuración del juego."""
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    GRID_SIZE = 20
    GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
    GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
    FPS = 10
    TITLE = "Snake - Juego Clásico"


class Position:
    """Clase para manejar posiciones en la cuadrícula del juego."""
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if isinstance(other, Position):
            return self.x == other.x and self.y == other.y
        return False

    def get_coordinates(self) -> Tuple[int, int]:
        """Retorna las coordenadas en píxeles para dibujar."""
        return (self.x * Config.GRID_SIZE, self.y * Config.GRID_SIZE)


class Food:
    """Clase que representa la comida en el juego."""
    def __init__(self):
        self.position = self._generate_random_position()
        self.color = Color.RED

    def _generate_random_position(self) -> Position:
        """Genera una posición aleatoria para la comida."""
        x = random.randint(0, Config.GRID_WIDTH - 1)
        y = random.randint(0, Config.GRID_HEIGHT - 1)
        return Position(x, y)

    def respawn(self, snake_positions: List[Position]):
        """Reposiciona la comida evitando la posición de la serpiente."""
        while True:
            new_position = self._generate_random_position()
            if new_position not in snake_positions:
                self.position = new_position
                break

    def draw(self, surface):
        """Dibuja la comida en la pantalla."""
        rect = pygame.Rect(
            self.position.get_coordinates(),
            (Config.GRID_SIZE, Config.GRID_SIZE)
        )
        pygame.draw.rect(surface, self.color, rect)
        pygame.draw.rect(surface, Color.BLACK, rect, 1)


class Snake:
    """Clase que representa la serpiente controlada por el jugador."""
    def __init__(self):
        self.positions = [Position(Config.GRID_WIDTH // 2, Config.GRID_HEIGHT // 2)]
        self.direction = Direction.RIGHT
        self.color = Color.GREEN
        self.growth_pending = False

    def get_head_position(self) -> Position:
        """Retorna la posición de la cabeza de la serpiente."""
        return self.positions[0]

    def update(self):
        """Actualiza la posición de la serpiente según su dirección."""
        head = self.get_head_position()
        direction_value = self.direction.value
        new_position = Position(
            (head.x + direction_value[0]) % Config.GRID_WIDTH,
            (head.y + direction_value[1]) % Config.GRID_HEIGHT
        )

        if new_position in self.positions[1:]:
            return False  # Colisión con el cuerpo

        self.positions.insert(0, new_position)
        
        if not self.growth_pending:
            self.positions.pop()
        else:
            self.growth_pending = False
            
        return True  # Movimiento exitoso

    def grow(self):
        """Hace crecer la serpiente en el próximo movimiento."""
        self.growth_pending = True

    def change_direction(self, new_direction: Direction):
        """Cambia la dirección de la serpiente si es válido."""
        # Evitar que la serpiente se mueva en dirección opuesta
        opposite_directions = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT
        }
        
        if new_direction != opposite_directions.get(self.direction):
            self.direction = new_direction

    def draw(self, surface):
        """Dibuja la serpiente en la pantalla."""
        for position in self.positions:
            rect = pygame.Rect(
                position.get_coordinates(),
                (Config.GRID_SIZE, Config.GRID_SIZE)
            )
            pygame.draw.rect(surface, self.color, rect)
            pygame.draw.rect(surface, Color.BLACK, rect, 1)


class Game:
    """Clase principal que controla la lógica del juego."""
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(
            (Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT)
        )
        pygame.display.set_caption(Config.TITLE)
        
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.font = pygame.font.SysFont('Arial', 26)
        self.game_over = False

    def handle_events(self):
        """Maneja los eventos de teclado y cierre de ventana."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if self.game_over and event.key == pygame.K_r:
                    self.reset_game()
                elif event.key == pygame.K_UP:
                    self.snake.change_direction(Direction.UP)
                elif event.key == pygame.K_RIGHT:
                    self.snake.change_direction(Direction.RIGHT)
                elif event.key == pygame.K_DOWN:
                    self.snake.change_direction(Direction.DOWN)
                elif event.key == pygame.K_LEFT:
                    self.snake.change_direction(Direction.LEFT)
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

    def check_collision(self):
        """Verifica colisiones con la comida."""
        if self.snake.get_head_position() == self.food.position:
            self.snake.grow()
            self.food.respawn(self.snake.positions)
            self.score += 1

    def draw(self):
        """Dibuja todos los elementos del juego en la pantalla."""
        self.screen.fill(Color.BLACK)
        
        # Dibujar elementos del juego
        self.snake.draw(self.screen)
        self.food.draw(self.screen)
        
        # Mostrar puntuación
        score_text = self.font.render(f'Puntuación: {self.score}', True, Color.WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # Mostrar mensaje de game over si es necesario
        if self.game_over:
            game_over_text = self.font.render('¡GAME OVER! Presiona R para reiniciar', True, Color.WHITE)
            text_rect = game_over_text.get_rect(center=(Config.SCREEN_WIDTH//2, Config.SCREEN_HEIGHT//2))
            self.screen.blit(game_over_text, text_rect)
        
        pygame.display.update()

    def reset_game(self):
        """Reinicia el juego a su estado inicial."""
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.game_over = False

    def run(self):
        """Ejecuta el bucle principal del juego."""
        while True:
            self.handle_events()
            
            if not self.game_over:
                # Actualizar estado del juego
                if not self.snake.update():
                    self.game_over = True
                self.check_collision()
            
            self.draw()
            self.clock.tick(Config.FPS)


def main():
    """Función principal para iniciar el juego."""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
