import pygame
from game.rocket import Rocket, Vector2

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("My Game")
        self.clock = pygame.time.Clock()
        self.is_running = True
        self.fps_max = 60
        self.dt = 0.0

        self.rocket = Rocket(400, 300)

    def run(self):
        while self.is_running:
            self.handle_events()
            self.update()
            self.render()
            self.dt = self.clock.get_time() / 1000.0
            self.clock.tick(self.fps_max)

        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

    def update(self):
        self.rocket.update(self.dt)

    def render(self):
        self.screen.fill((0, 0, 0))

        speed_text = f"Speed: {self.rocket.vel.length():.2f}"
        speed_font = pygame.font.Font(None, 24)
        speed_surface = speed_font.render(speed_text, True, (255, 255, 255))
        self.screen.blit(speed_surface, (10, 10))

        position_text = f"power: {self.rocket.power}"
        position_surface = speed_font.render(position_text, True, (255, 255, 255))
        self.screen.blit(position_surface, (10, 50))
        print(self.rocket.vel.angle_to(Vector2(1, 0)), self.rocket.angle)
        self.rocket.render(self.screen)

        pygame.display.flip()