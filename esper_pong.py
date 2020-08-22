import pygame
import esper
import math

from components import *

FPS = 120
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

BALL_SPAWN_POINT = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
BALL_INIT_VEL = (-50,0)

BINDINGS = {
    'w' : 'PADDLE_UP',
    's' : 'PADDLE_DOWN',
    '1' : 'SPEED_UP',
    '2' : 'SPEED_DOWN'
}

BINDINGS2 = {
    'up' : 'PADDLE_UP',
    'down' : 'PADDLE_DOWN',
}


def lookup_binding(bindings, key, default=None):
    return bindings.get(pygame.key.name(key), default)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
myfont = pygame.font.SysFont('Comic Sans MS', 30)
clock = pygame.time.Clock()

class InputMapperProcessor(esper.Processor):
    def process(self):
        for event in pygame.event.get():
            for ent, input in world.get_component(Input):
                if event.type == pygame.KEYDOWN:
                    action = lookup_binding(input.bindings, event.key)
                    if action is not None:
                        input.actions.append(action)
                if event.type == pygame.KEYUP:
                    action = lookup_binding(input.bindings, event.key)
                    if action is not None and action in input.actions:
                        input.actions.remove(action)


class InputProcessor(esper.Processor):
    def process(self):
        for ent, (input, _, dir, vel) in world.get_components(Input, Paddle, Direction,Velocity):
            if 'PADDLE_UP' in input.actions:
                dir.y = -1
            elif 'PADDLE_DOWN' in input.actions:
                dir.y = 1
            else:
                dir.y = 0

            if 'SPEED_UP' in input.actions:
                vel.y = 10
            if 'SPEED_DOWN' in input.actions:
                vel.y = 5

class PaddleMovementProcessor(esper.Processor):
    def process(self):
        for ent, (_, pos,vel, dir,hitbox) in world.get_components(Paddle, Position, Velocity, Direction, HitBox):
            pos.y += vel.y * dir.y
            pos.y = max(pos.y, 0)
            pos.y = min(pos.y, SCREEN_HEIGHT-hitbox.height)

class BallMovementProcessor(esper.Processor):
    def process(self):
        for ent, (_, pos, dir,vel) in world.get_components(Ball, Position, Direction, Velocity):
            pos.x += (vel.x * (clock.get_time() / 1000) * 10) * dir.x
            pos.y += (vel.y * (clock.get_time() / 1000) * 10) * dir.y

class BallOutOfBoundsProcessor(esper.Processor):
    def process(self):
        for ent, (_, pos,vel,dir) in world.get_components(Ball, Position, Velocity,Direction):
            if pos.x < 0 or pos.x > SCREEN_WIDTH:
                pos.x = BALL_SPAWN_POINT[0]
                pos.y = BALL_SPAWN_POINT[1]
                vel.x = BALL_INIT_VEL[0]
                vel.y = BALL_INIT_VEL[1]
                dir.x *= -1 


class BallCollisionProcessor(esper.Processor):
        def process(self):
            for ent, (_, pos, dir, vel, box) in world.get_components(Ball, Position, Direction, Velocity, HitBox):
                if pos.y < 0 or pos.y > SCREEN_HEIGHT:
                    vel.y *= -1
                for ent2, (_, p_pos, p_box) in world.get_components(Paddle, Position, HitBox):
                    if self.overlaps(pos,box, p_pos, p_box):
                        paddleCenter = p_pos.y + (p_box.height/2)
                        d = paddleCenter - pos.y
                        vel.y += d * -0.5
                        dir.x *= -1
        
        def overlaps(self, ball_pos, ball_box, paddle_pos, paddle_box):
            return ball_pos.x >= paddle_pos.x and ball_pos.x <= paddle_pos.x + paddle_box.width and ball_pos.y >= paddle_pos.y and ball_pos.y <= paddle_pos.y + paddle_box.height

class DrawScreenProcessor(esper.Processor):
    def process(self):
        screen.fill((0,0,0))
        for ent, (pos,draw) in world.get_components(Position, Drawable):
            if draw.shape == "rect":
                pygame.draw.rect(screen, draw.color, (pos.x,pos.y, draw.width, draw.height), 0)
            elif draw.shape == "circle":
                pygame.draw.circle(screen, draw.color, (int(pos.x),int(pos.y)), draw.width, 0)

world = esper.World()
world.add_processor(InputMapperProcessor(), priority=1)
world.add_processor(InputProcessor())
world.add_processor(PaddleMovementProcessor())
world.add_processor(DrawScreenProcessor())
world.add_processor(BallMovementProcessor())
world.add_processor(BallCollisionProcessor())
world.add_processor(BallOutOfBoundsProcessor())

def create_paddle(input, velocity, x,y,width,height,color):
    return world.create_entity(input, Position(x,y-height/2), Paddle(), Drawable("rect", width, height, color), Direction(0,0),Velocity(0,3), HitBox(width,height))

paddle = create_paddle(Input(BINDINGS),None, 20, SCREEN_HEIGHT/2, 20,80, (255,255,255))
paddle2 = create_paddle(Input(BINDINGS2),None, SCREEN_WIDTH-40,SCREEN_HEIGHT/2, 20,80, (255,255,255))
ball = world.create_entity(Ball(),Position(BALL_SPAWN_POINT[0],BALL_SPAWN_POINT[1]), HitBox(5,5), Direction(1,1), Velocity(BALL_INIT_VEL[0],BALL_INIT_VEL[1]), Drawable("circle", 5,10, (255,255,255)))

while True:
    world.process()
    pygame.display.update()
    clock.tick(FPS)