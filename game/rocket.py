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

    def add_force(self, force: Vector2):
        self.acc += force / self.mass

    def rotate(self, direction: int):
        self.angle += direction
        if self.angle > 180:
            self.angle = -(360 - self.angle)
        elif self.angle < -180:
            self.angle = (360 - self.angle)

    def accelerate(self, dt: float, accelerating: bool = True):
        thrust_vector: Vector2 = Vector2(
            math.cos(math.radians(self.angle)),
            math.sin(math.radians(self.angle))
        ) * self.power * dt
        if not accelerating: thrust_vector = -thrust_vector
        self.add_force(thrust_vector)

    def handle_events(self, dt):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_w]:
            self.accelerate(dt)
        if pressed[pygame.K_s]:
            self.accelerate(dt, False)
        if pressed[pygame.K_d]:
            self.rotate(2)
        if pressed[pygame.K_a]:
            self.rotate(-2)
        if pressed[pygame.K_UP]:
            self.power += 10 if self.power < 10000 else 0
        if pressed[pygame.K_DOWN]:
            self.power -= 10 if self.power > 0 else 0

    def update(self, dt):
        self.handle_events(dt)
        self.vel += self.acc * dt  # Update velocity based on acceleration
        self.pos += self.vel  # Update position based on velocity
        self.acc = Vector2(0, 0)
        self.vel *= self.slip

    def render(self, screen):
        # Base triangle
        points = [Vector2(10, 0), Vector2(-5, -5), Vector2(-2, 0), Vector2(-5, 5)]
        # Rotate points

        points = [p.rotate(self.angle) for p in points]
        # for point in points: point.rotate_ip(angle)

        # Fix y-axis
        points = [Vector2(p.x, p.y) for p in points]

        # Add current position
        points = [self.pos + p * 3 for p in points]

        # Draw triangle
        pygame.draw.polygon(screen, (250, 50, 5), points)