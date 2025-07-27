import pygame
import pygame_gui
import time


pygame.init()
# Set up the display
width, height = 1080, 720
screen = pygame.display.set_mode((width, height))
# Set the title of the window
pygame.display.set_caption("My Pygame Window")

#making the ground
ground_color = (255,255,255)
ground_height = 100  # Height of the ground
ground_rect = pygame.Rect(0, height - ground_height, width, ground_height)

class objects:
    def __init__(self, x, y, width, height, vertical_velocity=0, horizontal_velocity=0):
        self.rect = pygame.Rect(x, 520 - y, width, height)
        self.vertical_velocity = vertical_velocity
        self.horizontal_velocity = horizontal_velocity
        self.weight = 1
        self.momentum = self.weight * vertical_velocity
        self.vertical_direction = -1
        self.color = (255, 255, 255)

    def collide(self):
        self.vertical_velocity *= -0.5 #elasticity
        self.horizontal_velocity *= 0.9  # friction

    def update(self):
        # Update position based on velocity
        self.rect.y += self.vertical_velocity
        self.rect.x += self.horizontal_velocity
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def apply_velocity(self, delta_velocity):
        self.vertical_velocity += delta_velocity
        self.momentum = self.weight * self.vertical_velocity

    def apply_gravity(self, gravity):
        time.sleep(0.01)
        self.vertical_velocity += gravity * 0.1

main1 = objects(  100 #x position
                , 200 #y position
                , 50  #width
                , 50  #height
                , vertical_velocity=0
                , horizontal_velocity=10)


#constants
gravity = 9.8  # Gravity constant

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # Fill the screen with a color (RGB)
    screen.fill((0, 0, 0))  # Fill with black
    # Draw the ground
    pygame.draw.rect(screen, ground_color, ground_rect)

    # Update the object
    main1.draw(screen)
    main1.apply_gravity(gravity)
    main1.update()

    if main1.rect.colliderect(ground_rect):
        main1.collide()
        main1.rect.bottom = ground_rect.top


    # Update the display
    pygame.display.flip()
# Quit Pygame
pygame.quit()