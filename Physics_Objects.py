import pygame
import pygame_gui
import time


class PhysicsObjects:
    '''
    This class makes an object with a rectangle, vertical and horizontal velocity, elasticity, and friction.
    It has methods to collide with the ground, update its position, draw itself on the screen, apply velocity, gravity, 
    friction, and air resistance.

    How to use it?
    make an object, set the values and just call the methods in the main loop.
    '''

    def __init__(self, x, y, width, height, vertical_velocity, 
                 horizontal_velocity, object_weight, obj_elasticity, obj_friction,
                   object_color=(255, 255, 255)):
        
        self.rect = pygame.Rect(x, y, width, height)
        self.vertical_velocity = vertical_velocity
        self.horizontal_velocity = horizontal_velocity
        self.weight = object_weight
        self.vertical_direction = -1
        self.color = (255, 255, 255)
        self.elasticity = obj_elasticity
        self.friction = 1 - obj_friction

    def collide(self):
        self.vertical_velocity *= -self.elasticity
    #what does collide do?
    # It reverses the vertical velocity of the object, simulating a bounce effect.

    def update(self):
        self.rect.y += self.vertical_velocity
        self.rect.x += self.horizontal_velocity
    #what does update do?
    # It updates the position of the object based on its velocities.
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
    #what does draw do?
    # It draws the object on the screen using its rectangle and color.


    def apply_velocity(self, delta_velocity):
        self.vertical_velocity += delta_velocity
    #what does apply_velocity do?
    # It applies a change in vertical velocity to the object.

    def apply_gravity(self, gravity=9.81):
        time.sleep(0.0002)
        self.vertical_velocity += gravity * 0.1
    #what does apply_gravity do?
    # It applies gravity to the object, increasing its vertical velocity over time.

    def apply_friction(self):
        self.horizontal_velocity *= self.friction #friction
    #what does apply_friction do?
    # It applies friction to the horizontal velocity of the object, reducing its speed.

    def apply_air_resistance(self):
        self.vertical_velocity *= 0.999
        self.horizontal_velocity *= 0.999
    #what does apply_air_resistance do?
    # It applies air resistance to the vertical velocity of the object, slightly reducing its speed.