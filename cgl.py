import pygame
import math
from collections import Counter

def grid(x):
    return x*34

def search(list,value):
    try:
        a = list.index(value)
    except ValueError:
        return -1
    return a

class Blocks(pygame.sprite.Sprite):
    def __init__(self, place):
        
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((30, 30))
        self.image.fill(pygame.Color("white"))

        self.rect = self.image.get_rect()
        self.rect.move_ip(grid(place[0]),grid(place[1]))

class Game:
    def __init__(self):
        self.blocks = pygame.sprite.Group()
        self.paused = True
    
    def add_block(self, block):
        self.blocks.add(block)
    
    def update(self):
        if(self.paused == True):
            return
        #get the position of all cells
        moves = []
        for i in self.blocks:
            moves.append([i.rect[0], i.rect[1]])
        
        #verify if the cells has neighbours
        for now in moves:
            neighbours = []
            for friend in moves:
                if(friend == now):
                    continue
                if(abs(friend[0]-now[0]) <= 34 and abs(friend[1]-now[1]) <= 34):
                    neighbours.append(friend)
            
            #if there arent 3 or 2 neighbours or here are more than 3, search the block that correspond to the coordenades of now and remove it
            if(len(neighbours) < 2 or len(neighbours) > 3):
                for i in self.blocks:
                    if(i.rect[0:2] == now):
                        self.blocks.remove(i)
                        del moves[moves.index(i.rect[0:2])]
        #get the coordenades of the limits of each cell
        space=[]
        for i in moves:
            #the left space
            #       
            #     #x
            #
            space.append([i[0]-grid(1),i[1]])
            #the top left space
            #     #  
            #      x
            #
            space.append([i[0]-grid(1),i[1]-grid(1)])
            #the top space
            #      # 
            #      x
            #
            space.append([i[0],i[1]-grid(1)])
            #the bottom left space
            #       
            #      x
            #     #
            space.append([i[0]-grid(1),i[1]+grid(1)])
            #the bottom space
            #       
            #      x
            #      #
            space.append([i[0],i[1]+grid(1)])
            #the bottom right space
            #       
            #      x
            #       #
            space.append([i[0]+grid(1),i[1]+grid(1)])
            #the right space
            #       
            #      x#
            #      
            space.append([i[0]+grid(1), i[1]])
            #the top right space
            #       #
            #      x
            #      
            space.append([i[0]+grid(1),i[1]-grid(1)])
        
        #count how repeated are each coordenades
        counter = dict(Counter([tuple(item) for item in space]))
        
        for i in space:
            #if the value in the counter is equal to 3 and there isnt any cell in that position, create one
            if(counter.get(tuple(i)) == 3 and search(list(moves),i)==-1):
                #create a block with the coordenades and add it on the group sprite
                b=Blocks([i[0]/34,i[1]/34])
                self.add_block(b)
                #update moves list to not repeat the same place
                moves.append(i)

    #create cell from the mouse position  
    def create(self, mouse_pos):
        approx_x = math.ceil((mouse_pos[0]/34)-1)
        approx_y = math.ceil((mouse_pos[1]/34)-1)
        block = Blocks([approx_x,approx_y])
        self.add_block(block)
    
    #delete cell from the mouse position
    def delete(self, mouse_pos):
        approx_x = math.ceil((mouse_pos[0]/34)-1)
        approx_y = math.ceil((mouse_pos[1]/34)-1)
        for i in self.blocks:
            if(i.rect[0]/34 == approx_x and i.rect[1]/34 == approx_y):
                self.blocks.remove(i)

    def show_blocks(self):
        return self.blocks

#debug stuff
if(__name__=="__main__"):
    g = Game()
    g.paused=False
    b2 = Blocks([1,1])
    b1=Blocks([1,0])
    b=Blocks([0,0])
    g.add_block(b2)
    g.add_block(b1)
    g.add_block(b)
    g.update()