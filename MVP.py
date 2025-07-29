import pygame
import pygame_gui
import time

#constants
gravity = 9.8  # Gravity constant
elasticity = 0.5  # Elasticity factor for bounce
friction = 0.5 # Friction factor for horizontal movement

pygame.init()
# Set up the display
width, height = 1080, 720
screen = pygame.display.set_mode((width, height))
# Set the title of the window
pygame.display.set_caption("Basic Gravity Simulator | Pygame")
CLOCK = pygame.time.Clock()
MANAGER = pygame_gui.UIManager((width, height))


#making the ground
ground_color = (255,255,255)
ground_height = 100  # Height of the ground
ground_rect = pygame.Rect(0, height - ground_height, width, ground_height)



class objects:
    def __init__(self, x, y, width, height, vertical_velocity=0, horizontal_velocity=0, obj_elasticity=elasticity, obj_friction=friction):
        self.rect = pygame.Rect(x, 520 - y, width, height)
        self.vertical_velocity = vertical_velocity
        self.horizontal_velocity = horizontal_velocity
        self.weight = 1
        self.momentum = self.weight * vertical_velocity
        self.vertical_direction = -1
        self.color = (255, 255, 255)
        self.elasticity = elasticity
        self.friction = friction
    

    def collide(self):
        self.vertical_velocity *= -self.elasticity  # elasticity
        self.momentum = self.weight * self.vertical_velocity

    def update(self):
        self.rect.y += self.vertical_velocity
        self.rect.x += self.horizontal_velocity
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def apply_velocity(self, delta_velocity):
        self.vertical_velocity += delta_velocity
        self.momentum = self.weight * self.vertical_velocity

    def apply_gravity(self, gravity):
        time.sleep(0.2)
        self.vertical_velocity += gravity * 0.1
        self.momentum = self.weight * self.vertical_velocity
    def apply_friction(self):
        self.horizontal_velocity *= self.friction #friction
    def apply_air_resistance(self):
        self.vertical_velocity *= 0.999
        self.horizontal_velocity *= 0.999

main1 = objects(  100 #x position
                , 200 #y position
                , 50  #width
                , 50  #height
                , vertical_velocity=0
                , horizontal_velocity=10
                , obj_elasticity=elasticity
                , obj_friction=friction
                )

# UI: labeled text entry fields and button
labels = ['x', 'y', 'h_velocity', 'v_velocity', 'elasticity', 'friction']
entries = {}
for i, lbl in enumerate(labels):
    y_pos = 20 + i * 50
    # Label (we simply use a UIButton for static text)
    pygame_gui.elements.UILabel(relative_rect=pygame.Rect((20, y_pos), (120, 30)),
                                text=lbl + ':',
                                manager=MANAGER)
    # Entry field
    entries[lbl] = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((150, y_pos), (150, 30)),
        manager=MANAGER
    )
# Start button
start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 20), (150, 40)),
                                             text='Start',
                                             manager=MANAGER)

#last 5 positions
last_positions = [0,10]

# Main loop
running = True
simulation_started = False
while running:
    UI_REFRESH_RATE = CLOCK.tick(60)/1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == start_button:
                # Get values from text fields and create new object
                try:
                    x = float(entries['x'].get_text()) if entries['x'].get_text() else 100
                    y = float(entries['y'].get_text()) if entries['y'].get_text() else 200
                    h_vel = float(entries['h_velocity'].get_text()) if entries['h_velocity'].get_text() else 10
                    v_vel = float(entries['v_velocity'].get_text()) if entries['v_velocity'].get_text() else 0
                    elast = float(entries['elasticity'].get_text()) if entries['elasticity'].get_text() else elasticity
                    frict = float(entries['friction'].get_text()) if entries['friction'].get_text() else friction
                    # Reset last positions
                    last_positions = [0,10]
                    
                    # Create new object with input values
                    main1 = objects(x, y, 50, 50, v_vel, h_vel, elast, frict)
                    simulation_started = True
                except ValueError:
                    # If invalid input, use defaults
                    main1 = objects(100, 200, 50, 50, 0, 10, elasticity, friction)
                    simulation_started = True
        MANAGER.process_events(event)
    MANAGER.update(UI_REFRESH_RATE)

    # Fill the screen with a color (RGB)
    screen.fill((0, 0, 0))  # Fill with black
    MANAGER.draw_ui(screen)
    # Draw the ground
    pygame.draw.rect(screen, ground_color, ground_rect)


    # Display live object stats on the right side
    font = pygame.font.Font(None, 36)
    stats_x = width - 500  # Position on the right side
    
    # Vertical velocity
    v_vel_text = font.render(f"Vertical Velocity: {main1.vertical_velocity:.2f}", True, (255, 255, 255))
    screen.blit(v_vel_text, (stats_x, 60))
    
    # Horizontal velocity
    h_vel_text = font.render(f"Horizontal Velocity: {main1.horizontal_velocity:.2f}", True, (255, 255, 255))
    screen.blit(h_vel_text, (stats_x, 100))
    
    # X coordinate
    x_coord_text = font.render(f"X Position: {main1.rect.x}", True, (255, 255, 255))
    screen.blit(x_coord_text, (stats_x, 140))
    
    # Y coordinate
    y_coord_text = font.render(f"Y Position: {main1.rect.y}", True, (255, 255, 255))
    screen.blit(y_coord_text, (stats_x, 180))

    # Update the object only if simulation has started
    
    main1.draw(screen)
    if simulation_started:
        main1.apply_gravity(gravity)
        main1.apply_air_resistance()
        main1.update()

        if main1.rect.y == 570:
            main1.apply_friction()

        if main1.rect.colliderect(ground_rect):
            main1.collide()
            main1.rect.bottom = ground_rect.top

        if main1.rect.bottom >= ground_rect.top:
            if abs(last_positions[0] - last_positions[-1]) <= 1:
                main1.vertical_velocity = 0
            # Store last 5 positions
            last_positions.append(main1.rect.y)
            if len(last_positions) > 5:
                last_positions.pop(0)


    # Update the display
    pygame.display.flip()
# Quit Pygame
pygame.quit()