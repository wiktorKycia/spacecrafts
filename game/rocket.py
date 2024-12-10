import pygame
from pygame.math import Vector2
import math

class Rocket:
    def __init__(self, x, y):
        self.x: float = x
        self.y: float = y

        self.vel: Vector2 = Vector2(0, 0)  # Initial velocity
        self.acc: Vector2 = Vector2(0, 0)  # Initial acceleration
        self.pos: Vector2 = Vector2(x, y)

        self.mass: float = 1  # Mass of the rocket
        self.power: float = 500  # Power of the rocket
        self.force: float = self.power

        self.slip: float = 0.99  # Slip factor

        self.angle: float = 0  # Kąt obrotu w stopniach

        self.scale = 3.0

    def add_force(self, force: Vector2):
        """Adds acceleration to the rocket based on the given force"""
        self.acc += force / self.mass

    def rotate(self, angle: int):
        """Rotates the rocket by the given angle"""
        self.angle += angle
        if self.angle > 180:
            self.angle = -(360 - self.angle)
        elif self.angle < -180:
            self.angle = (360 - self.angle)

    def accelerate(self, dt: float, accelerating: bool = True):
        """
        Accelerates the rocket in the direction it is facing
        :param dt: time delta from the last frame
        :param accelerating: if False, the rocket will decelerate
        :return:
        """
        thrust_vector: Vector2 = Vector2(
            math.cos(math.radians(self.angle)),
            math.sin(math.radians(self.angle))
        ) * self.power * dt
        if not accelerating: thrust_vector = -thrust_vector
        self.add_force(thrust_vector)

    def handle_events(self, dt):
        """Handles key presses"""
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_w]: # moving forward
            self.accelerate(dt)
        if pressed[pygame.K_s]: # moving backward
            self.accelerate(dt, False)
        if pressed[pygame.K_d]: # turning right
            self.rotate(2)
        if pressed[pygame.K_a]: # turning left
            self.rotate(-2)
        if pressed[pygame.K_UP]: # increasing power
            self.power += 10 if self.power < 10000 else 0
        if pressed[pygame.K_DOWN]: # decreasing power
            self.power -= 10 if self.power > 0 else 0

    def update(self, dt):
        """Updates the rocket's position and velocity"""
        self.handle_events(dt)
        self.vel += self.acc * dt  # Update velocity based on acceleration
        self.pos += self.vel  # Update position based on velocity
        self.acc = Vector2(0, 0)
        self.vel *= self.slip

    def render(self, screen):
        """Renders the rocket on the screen"""
        # Base shape
        points = [Vector2(10, 0), Vector2(-5, -5), Vector2(-2, 0), Vector2(-5, 5)]

        # Rotate points
        points = [p.rotate(self.angle) for p in points]

        # Add current position
        points = [self.pos + p * self.scale for p in points]

        # Draw triangle
        pygame.draw.polygon(screen, (250, 50, 5), points)