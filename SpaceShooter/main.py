import sys
import pygame
from pygame.locals import *
import pyganim
from settings import SIZE, WHITE
from game_objects import Background, Player, Plasmoid, Meteorite

pygame.init()
pygame.display.set_caption('Hello world!')

screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

explosion_animation = pyganim.PygAnimation([('assets/asteroid_explode{}.png'.format(i+1), 50) for i in range(4)], loop=False)

music = pygame.mixer.Sound('assets/Scene1.ogg')
music.play(-1)

# Groups
all_objects = pygame.sprite.Group()
plasmoids = pygame.sprite.Group()
meteors = pygame.sprite.Group()

explosions = []

# Game objects
background = Background()
player = Player(clock, plasmoids)

all_objects.add(background)
all_objects.add(player)
# plasmoids.add(Plasmoid(player.rect.midtop))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)

    screen.fill(WHITE)

    # background.update()
    Meteorite.process_meteors(clock, meteors)

    all_objects.update()
    plasmoids.update()
    meteors.update()

    meteors_and_plasmoids_collided = pygame.sprite.groupcollide(meteors, plasmoids, True, True)

    for collided in meteors_and_plasmoids_collided:
        explosion = explosion_animation.getCopy()
        explosion.play()
        explosions.append((explosion, (collided.rect.center)))

    # player_and_meteors_collided = pygame.sprite.spritecollide(player, meteors, False)

    # if player_and_meteors_collided:
    #     all_objects.remove(player)

    # screen.blit(background.image, background.rect)
    all_objects.draw(screen)
    plasmoids.draw(screen)
    meteors.draw(screen)

    for explosion, position in explosions:
        if explosion.isFinished():
            explosions.remove((explosion, position))
        else:
            x, y = position
            explosion.blit(screen, (x - 32, y - 32))

    pygame.display.flip()
    clock.tick(30) # 30 - fps кол-во кадров в секунду
