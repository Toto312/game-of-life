import pygame
import math
import cgl

pygame.init()
screen_size=(714,714)
screen = pygame.display.set_mode(screen_size)

clock = pygame.time.Clock()

#create the class game and load the pause variable
game = cgl.Game()
pause = pygame.image.load("pause.png")
pause = pygame.transform.scale(pause,(60,60))

#variables for time and frames
lastnum = 0
tick_speed = 600
FPS = 30

#game mainloop
run = True
while(run):
    
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            #if there is click in the left button, create a cell
            if(pygame.mouse.get_pressed()[0]):
                game.create(pos)
            #if there is click in the right button, delete a cell
            elif(pygame.mouse.get_pressed()[2]):
                game.delete(pos)
        
        elif event.type == pygame.KEYDOWN:
            #if the keydown is the space, pause or despause the game
            if(event.key == pygame.K_SPACE):
                game.paused = not game.paused
    
    screen.fill((0,0,0))
    
    #Show pause if the game is paused
    if(game.paused):
        screen.blit(pause,(19*34,19*34))
    
    #show the sprites
    for sprite in game.show_blocks():
        screen.blit(sprite.image, sprite.rect)
    
    #call this function in much less than 30 times/sec. It would not run well in other pc
    tick_threshold = math.ceil(pygame.time.get_ticks()/tick_speed)
    if(tick_threshold!=lastnum):
        game.update()
        lastnum = tick_threshold
    
    pygame.display.flip()
    clock.tick(FPS)