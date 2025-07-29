import pygame
import pygame_gui
import time
from Physics_Objects import PhysicsObjects


pygame.init()
pygame.mixer.init()  # Initialize sound mixer
WIDTH = 1400
HEIGHT = 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Basic Gravity Simulator")

# Initialize UI Manager
ui_manager = pygame_gui.UIManager((WIDTH, HEIGHT))

# Create buttons
start_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(50, 50, 100, 50),
    text='Start',
    manager=ui_manager
)

pause_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(170, 50, 100, 50),
    text='Pause',
    manager=ui_manager
)

reset_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(290, 50, 100, 50),
    text='Reset',
    manager=ui_manager
)

# Create input fields for elasticity and friction
elasticity_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(410, 50, 80, 25),
    text='Elasticity:',
    manager=ui_manager
)

elasticity_input = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect(500, 50, 60, 25),
    manager=ui_manager
)
elasticity_input.set_text('0.8')

friction_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(580, 50, 60, 25),
    text='Friction:',
    manager=ui_manager
)

friction_input = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect(650, 50, 60, 25),
    manager=ui_manager
)
friction_input.set_text('0.35')

apply_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(730, 50, 60, 25),
    text='Apply',
    manager=ui_manager
)

# Create input fields for velocities
h_velocity_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(410, 85, 80, 25),
    text='H Velocity:',
    manager=ui_manager
)

h_velocity_input = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect(500, 85, 60, 25),
    manager=ui_manager
)
h_velocity_input.set_text('10')

v_velocity_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(580, 85, 80, 25),
    text='V Velocity:',
    manager=ui_manager
)

v_velocity_input = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect(650, 85, 60, 25),
    manager=ui_manager
)
v_velocity_input.set_text('0')

apply_velocity_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(730, 85, 60, 25),
    text='Apply',
    manager=ui_manager
)

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Initialize font for stats display
pygame.font.init()
stats_font = pygame.font.Font(None, 24)

# Bounce counter
bounce_count = 0

# Timer variables
simulation_start_time = 0
simulation_elapsed_time = 0

# Real-world unit conversions
PIXELS_PER_METER = 100  # 100 pixels = 1 meter
FRAME_RATE = 60  # 60 FPS

# Load sound effect
try:
    bounce_sound = pygame.mixer.Sound("mixkit-on-or-off-light-switch-tap-2585.wav")
    bounce_sound.set_volume(1)  # Set volume to 30%
except pygame.error:
    bounce_sound = None
    print("Sound file not found - continuing without sound")

#Objects

Object1 = PhysicsObjects(    
    x=100,
    y=200,
    width=50,
    height=50,
    vertical_velocity=0,
    horizontal_velocity=10,
    object_weight=1,
    obj_elasticity=0.8,
    obj_friction=0.35,
    object_color=(255, 255, 255)
)

Ground = PhysicsObjects(
    x=0,
    y=HEIGHT - 50,
    width=WIDTH,
    height=50,
    vertical_velocity=0,
    horizontal_velocity=0,
    object_weight=1,
    obj_elasticity=0.8,
    obj_friction=0.35,
    object_color=(255, 255, 255)
)



# Game loop
running = True
simulation_running = False
clock = pygame.time.Clock()
last_positions = [0,100]

# Drag functionality variables
dragging = False
drag_offset_x = 0
drag_offset_y = 0

while running:
    time_delta = clock.tick(60)/1000.0
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Handle mouse events for dragging
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if Object1.rect.collidepoint(mouse_x, mouse_y):
                    dragging = True
                    drag_offset_x = mouse_x - Object1.rect.x
                    drag_offset_y = mouse_y - Object1.rect.y
        
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button
                dragging = False
        
        if event.type == pygame.MOUSEMOTION:
            if dragging:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                Object1.rect.x = mouse_x - drag_offset_x
                Object1.rect.y = mouse_y - drag_offset_y
                # Only reset vertical velocity when dragging to allow horizontal momentum
                Object1.vertical_velocity = 0
        
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == start_button:
                    simulation_running = True
                    if simulation_start_time == 0:  # Only set start time if not already set
                        simulation_start_time = time.time()
                if event.ui_element == pause_button:
                    simulation_running = False
                if event.ui_element == reset_button:
                    # Reset object to initial position and state
                    Object1.rect.x = 100
                    Object1.rect.y = 200
                    Object1.vertical_velocity = 0
                    Object1.horizontal_velocity = 10
                    bounce_count = 0
                    last_positions = [0, 100]
                    simulation_running = False
                    simulation_start_time = 0  # Reset timer
                    simulation_elapsed_time = 0
                if event.ui_element == apply_button:
                    # Apply new elasticity and friction values
                    try:
                        new_elasticity = float(elasticity_input.get_text()) if elasticity_input.get_text() else 0.8
                        new_friction = float(friction_input.get_text()) if friction_input.get_text() else 0.35
                        
                        # Update object properties - friction needs same calculation as constructor
                        Object1.elasticity = new_elasticity
                        Object1.friction = 1 - new_friction
                        print(f"Applied - Elasticity: {Object1.elasticity}, Friction input: {new_friction}, Friction attribute: {Object1.friction}")
                    except ValueError:
                        # If invalid input, keep current values
                        pass
                if event.ui_element == apply_velocity_button:
                    # Apply new velocity values
                    try:
                        new_h_velocity = float(h_velocity_input.get_text()) if h_velocity_input.get_text() else 10
                        new_v_velocity = float(v_velocity_input.get_text()) if v_velocity_input.get_text() else 0
                        
                        # Update object velocities
                        Object1.horizontal_velocity = new_h_velocity
                        Object1.vertical_velocity = new_v_velocity
                        print(f"Applied Velocities - Horizontal: {Object1.horizontal_velocity}, Vertical: {Object1.vertical_velocity}")
                    except ValueError:
                        # If invalid input, keep current values
                        pass
        
        ui_manager.process_events(event)
    
    ui_manager.update(time_delta)
    
    screen.fill(BLACK)

    # Always draw the ground
    Ground.draw(screen)

    # Only run physics when simulation is running
    if simulation_running:
        # Update elapsed time
        if simulation_start_time > 0 and Object1.horizontal_velocity != 0 and Object1.vertical_velocity != 0:
            simulation_elapsed_time = time.time() - simulation_start_time
            
        Object1.apply_gravity()
        Object1.apply_air_resistance()
        Object1.update()
        
        # Check for collision and play sound when object reaches y=500
        if Object1.rect.y >= 500 and Object1.vertical_velocity > 0:
            # Play sound only once per bounce approach
            if not hasattr(Object1, 'sound_played') or not Object1.sound_played:
                if bounce_sound:
                    bounce_sound.play()
                Object1.sound_played = True
        
        if Object1.rect.colliderect(Ground.rect):
            Object1.collide()
            Object1.rect.y = Ground.rect.top - Object1.rect.height
            bounce_count += 1
            # Reset sound flag for next bounce
            Object1.sound_played = False

        if Object1.rect.y == 620:
            Object1.apply_friction()

        if Object1.rect.bottom >= Ground.rect.top:
                # Store last 5 positions
                last_positions.append(Object1.rect.y)
                if len(last_positions) > 5:
                    last_positions.pop(0)
                
                # Calculate average movement between consecutive positions
                if len(last_positions) > 1:
                    avg_movement = sum([abs(last_positions[i+1] - last_positions[i]) for i in range(len(last_positions)-1)]) / (len(last_positions)-1)
                    
                    if avg_movement <= 0.000000005:
                        Object1.vertical_velocity = 0

    # Always draw the object
    Object1.draw(screen)
    
    # Draw live stats in top left corner
    stats_y_offset = 10  # Start below the buttons

    # Convert to real-world units
    v_velocity_ms = (Object1.vertical_velocity * FRAME_RATE) / PIXELS_PER_METER  # m/s
    h_velocity_ms = (Object1.horizontal_velocity * FRAME_RATE) / PIXELS_PER_METER  # m/s
    x_position_m = Object1.rect.x / PIXELS_PER_METER  # meters
    y_position_m = (HEIGHT - Object1.rect.y) / PIXELS_PER_METER  # meters (inverted, ground = 0)
    height_m = (HEIGHT - 50) / PIXELS_PER_METER  # total height in meters

    # Vertical velocity
    v_vel_text = stats_font.render(f"Vertical Velocity: {v_velocity_ms:.2f} m/s", True, WHITE)
    screen.blit(v_vel_text, (1100, stats_y_offset))
    
    # Horizontal velocity
    h_vel_text = stats_font.render(f"Horizontal Velocity: {h_velocity_ms:.2f} m/s", True, WHITE)
    screen.blit(h_vel_text, (1100, stats_y_offset + 25))
    
    # X coordinate
    x_coord_text = stats_font.render(f"X Position: {x_position_m:.2f} m", True, WHITE)
    screen.blit(x_coord_text, (1100, stats_y_offset + 50))
    
    # Y coordinate (height above ground)
    y_coord_text = stats_font.render(f"Height: {y_position_m:.2f} m", True, WHITE)
    screen.blit(y_coord_text, (1100, stats_y_offset + 75))
    
    # Bounce count
    bounce_text = stats_font.render(f"Bounce Count: {bounce_count}", True, WHITE)
    screen.blit(bounce_text, (1100, stats_y_offset + 100))
    
    # Timer
    timer_text = stats_font.render(f"Time: {simulation_elapsed_time:.2f} s", True, WHITE)
    screen.blit(timer_text, (1100, stats_y_offset + 125))
    
    # Draw UI elements
    ui_manager.draw_ui(screen)

    pygame.display.flip()
    clock.tick(60)
pygame.quit()