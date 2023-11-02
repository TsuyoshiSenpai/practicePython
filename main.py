import pygame
import random
import pygame.time
from game import Game
from variables import Variables

var = Variables()
game = Game()

pygame.init()

game.initialize(var)

game.rulesInit(var)

while var.input_active:
    game.waitingForInput(var)

while var.running:
    game.run(var)


# Завершение PyGame
pygame.quit()