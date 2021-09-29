import pygame
import os
from random import randint

pygame.init()
screen = pygame.display.set_mode((110, 110))
clock = pygame.time.Clock()

# Making of raster
rasterhor = [(0,0),(110,0),(110,11),(0,11),(0,22),(110,22),(110,33),(0,33),(0,44),(110,44),(110,55),(0,55),(0,66),(110,66),(110,77),(0,77),(0,88),(110,88),(110,99),(0,99),(0,110),(110,110),(0,110)]
rasterver = []
x = 0
y = 0
cont = 0
j = (x,y)
for i in rasterhor:
    x=i[0]
    y=i[1]
    cont=x
    x=y
    y=cont  
    j=(x,y)
    rasterver.append(j)
    
_image_library = {}
def get_image(path):
    global _image_library
    image = _image_library.get(path)
    if image == None:
        canonicalized_path = path.replace('/', os.sep ).replace('\\', os.sep)
        image = pygame.image.load(canonicalized_path)
        _image_library[path] = image
    return image

tilebase = []
for row in range(0,11):
    for col in range(0,11):
        tilebase.append((row,col))  


tile_library = {}
for tile in tilebase:
    tile_library.update({tile: "full"})

clickedlibrary = {}
for tile in tilebase:
    clickedlibrary.update({tile: False})

flaglibrary = {}
for tile in tilebase:
    flaglibrary.update({tile: False})

clearedlibrary = {}
for tile in tilebase:
    clearedlibrary.update({tile: False})

#placing the bombs
bomblibrary = {}
for tile in tilebase:
    bomblibrary.update({tile: False})
    
def random_coordinate():
    randco = (randint(0,9),randint(0,9))
    return randco

def didiwin():
    for tile in tile_library:
      if tile_library[tile]=='full' or bomblibrary[tile]==False:
        return False
    return True

bombs = 17#generate bombs
for bomb in range(bombs): 
  randco = random_coordinate()
  while bomblibrary[randco] == True:
      randco = random_coordinate()
  if bomblibrary[randco] == False:
    bomblibrary[randco]= True


tilesaround = {}
def getsurrounded(tile): 
    tilesaround = {'lb': (tile[0]-1, tile[1]+1), 'mb': (tile[0], tile[1]+1), 'rb': (tile[0]+1, tile[1]+1),
                   'lm': (tile[0]-1,tile[1]), 'rm': (tile[0]+1,tile[1]),
                   'lo': (tile[0]-1,tile[1]-1),  'mo': (tile[0],tile[1]-1), 'ro': (tile[0]+1, tile[1]-1)}
    count = 0
    
    for tile in tilesaround:        
        checkco = tilesaround[tile]
        if checkco[0]>= 0 and checkco[0]<=10 and checkco[1]>= 0 and checkco[1]<=10:
         if bomblibrary [tilesaround[tile]]:
           count = count+1
    
    if count == 1:
        return 'one'
    elif count == 2:
        return 'two'
    elif count == 3:
        return 'three'
    elif count == 4:
        return 'four'
    elif count == 5:
        return 'five'
    elif count == 6:
        return 'six'
    else:
        return 'empty'

def gotclicked(position):
    if position in clickedlibrary and clickedlibrary[position] == False:
        clickedlibrary[position]=True
        if bomblibrary[position]:
            tile_library[position] = 'bomb'
        else:
            clearedlibrary[position] = True
            tile_library[position] = getsurrounded(position)
            if getsurrounded(position) == 'empty':
                clickaround(position)
def rightclicked(position):
    if tile_library[position] == 'full':
        flaglibrary[position] = not flaglibrary[position]

def clickaround(emptyposition):
    gotclicked((emptyposition[0]-1,emptyposition[1]+1))
    gotclicked((emptyposition[0], emptyposition[1]+1))
    gotclicked((emptyposition[0]+1, emptyposition[1]+1))
    gotclicked((emptyposition[0]-1, emptyposition[1]))
    gotclicked((emptyposition[0]+1, emptyposition[1]))
    gotclicked((emptyposition[0]-1, emptyposition[1]-1))
    gotclicked((emptyposition[0], emptyposition[1]-1))
    gotclicked((emptyposition[0]+1, emptyposition[1]-1))
              
once = True #for releasing rightclick

done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    screen.fill((200,255,255))
    
    #drawing the raster
    pygame.draw.lines(screen, (10,0,0), True, rasterhor)
    pygame.draw.lines(screen, (10,0,0), True, rasterver)
    
    #mouse interaction
    pressed = pygame.mouse.get_pressed()
    if pressed[0] == 1:#left click
        clickposition = (pygame.mouse.get_pos())
        click = (int(clickposition[0]/11),int(clickposition[1]/11)) #coordinate to tile
        gotclicked(click)
    if pressed[2] == 1:#right click
        if once:#only first frame of click
            once = False
            clickposition = (pygame.mouse.get_pos())
            click = (int(clickposition[0]/11), int(clickposition[1]/11))
            rightclicked(click)
    if pressed[2] == 0:
                once = True            
                
    #drawing of tilebase
    for tile in tile_library:
        if tile_library[tile] == 'full':
            screen.blit(get_image('full.png'), ((tile[0]*11),(tile[1]*11)))
            if flaglibrary[tile]:
                screen.blit(get_image('flag.png'), ((tile[0]*11),(tile[1]*11)))
        elif tile_library[tile] == 'one':
            screen.blit(get_image('one.png'), ((tile[0]*11),(tile[1]*11)))
        elif tile_library[tile] == 'two':
            screen.blit(get_image('two.png'), ((tile[0]*11),(tile[1]*11)))
        elif tile_library[tile] == 'three':
            screen.blit(get_image('three.png'), ((tile[0]*11),(tile[1]*11)))
        elif tile_library[tile] == 'four':
            screen.blit(get_image('four.png'), ((tile[0]*11),(tile[1]*11)))
        elif tile_library[tile] == 'five':
            screen.blit(get_image('five.png'), ((tile[0]*11),(tile[1]*11)))
        elif tile_library[tile] == 'six':
            screen.blit(get_image('six.png'), ((tile[0]*11),(tile[1]*11)))
        elif tile_library[tile] == 'empty':
            screen.blit(get_image('empty.png'), ((tile[0]*11),(tile[1]*11)))
        elif tile_library[tile] == 'bomb':
            screen.blit(get_image('bomb.png'), ((tile[0]*11),(tile[1]*11)))
            done = True
    if didiwin():
        print("Succes!")
        done=True
    clock.tick(60)
    pygame.display.flip()