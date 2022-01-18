import pygame
import random

# creating the data structure for pieces
# setting up global vars
# functions
# - create_grid
# - draw_grid
# - draw_window
# - rotating shape in main
# - setting up the main
 
"""
10 x 20 square grid
shapes: S, Z, I, O, J, L, T
represented in order by 0 - 6
"""
 
pygame.font.init()

#screen variables

s_width = 800
s_height = 700
WIN=pygame.display.set_mode((s_width,s_height))
pygame.display.set_caption("TERIS GAME USING PYGAME MODULE !")

# GLOBALS VARS
high_score=0
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 20 height per block
block_size = 30

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height



 
# SHAPE FORMATS
 
S = [['.....',
      '......',
      '..00..',
      '.00...',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]
 
Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]
 
I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]
 
O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]
 
J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]
 
L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]
 
T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]
 
shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]
# index 0 - 6 represent shape
 
 
class Piece(object):
    def __init__(self,x,y,shape):
        self.x=x  
        self.y=y  
        self.shape=shape 
        self.color=shape_colors[shapes.index(shape)]
        self.rotation=0
 
def create_grid(locked_positions={}):
    grid=[[(0,0,0) for x in range(10)] for x in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j,i) in locked_positions:
                c=locked_positions[(j,i)]
                grid[i][j]=c  


    return grid
 
def convert_shape_format(shape):
    positions = []
    shaping = shape.shape[shape.rotation % len(shape.shape)]
 
    for i, line in enumerate(shaping):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))
 
    for i, pos in enumerate(positions):
        positions[i] = (pos[0]-2 , pos[1] -2)
 
    return positions

def valid_space(shape, grid):
    accepted_pos=[[(j,i) for j in range(10) if grid[i][j] == (0,0,0) ] for i in range(20)]  
    accepted_pos=[j for sub in accepted_pos for j in sub ]
    shaped=convert_shape_format(shape)
    for pos in shaped:
        if pos not in accepted_pos:
            if pos[1]>-1:
                return False
    return True

def check_lost(positions):
    for pos in positions:
        x,y=pos
        if y < 0:
            return True 
    return False 
 
def get_shape():
    return Piece(5,0,random.choice(shapes))
 
 
def draw_text(write, size, color, surface):
    font =pygame.font.SysFont("Arial BLACK",size,bold=True)
    text = font.render(write,1,color)
    surface.blit(text, (s_width/2 - text.get_width()/2,s_height/2 - text.get_height()/2))

   
def draw_grid(surface, grid):

    for i in range(len(grid)):
        pygame.draw.line(surface,(255,255,255),(top_left_x,top_left_y+i*block_size),(top_left_x+play_width,top_left_y+i*block_size))
        for j in range(len(grid[i])):
            pygame.draw.line(surface,(255,255,255),(top_left_x+j*block_size,top_left_y),(top_left_x+j*block_size,top_left_y+play_height))


def fix_rows(grid, locked):
    inc=0
    for i in range(len(grid)-1,-1,-1):
        row=grid[i]
        if (0,0,0) not in row :
            inc += 1 
            ind=i 
            for j in range(len(row)):
                del locked[(j,i)]
    if inc>0:
        for key in sorted(list(locked), key = lambda x : x[1])[:: -1]:
            x,y=key 
            if y<ind:
                newKey = (x,y + inc)
                locked[newKey] = locked.pop(key)

    return inc * 10
 
def draw_next_shape(shape, surface):
    
    font =pygame.font.SysFont("Arial Black",30)
    text = font.render("NEXT SHAPE", 1 , (255,255,255))
    
    x = top_left_x +play_width +30 
    y=top_left_y + play_height -400
    shaping = shape.shape[shape.rotation % len(shape.shape)]

    for i , line in enumerate(shaping):
        row = list(line)
        for j,column in enumerate(row):
            if column == '0' :
                pygame.draw.rect(surface , shape.color , (x + j*block_size , y + i*block_size , block_size ,block_size ))

    surface.blit(text, (x , y-20))


def draw_window(surface,grid,score,high_score):

    surface.fill((0,0,0))
    pygame.font.init()
    font=pygame.font.SysFont("Arial Black",50)
    text=font.render("TETRIS GAME!",1,(255,255,255))
    surface.blit(text,((s_width-text.get_width())/2,20))


    font=pygame.font.SysFont("Arial Black",25)
    text = font.render("SCORE : "+ str(score),1,(255,255,255))
    surface.blit(text,(top_left_x-200,s_height//2-50))
    text = font.render("HIGH SCORE : "+ str(high_score),1,(255,255,255))
    surface.blit(text,(top_left_x-240,s_height//2+50))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface,grid[i][j],(top_left_x+j*block_size,top_left_y+i*block_size,30,30))

    draw_grid(surface,grid)

    pygame.draw.rect(surface,(0,255,0),(top_left_x,top_left_y,play_width,play_height),5)
 
def main():
    global high_score
    locked_positions={}
    grid=create_grid(locked_positions)

    change_piece=False
    run=True
    current_piece = get_shape()
    next_piece=get_shape()
    clock=pygame.time.Clock()
    fall_time=0
    fall_speed=0.27 
    score = 0

    while run:
        grid=create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()



        #PIECE FALLING CODE FOR TETRIS
        if fall_time/1000 > fall_speed:
            fall_time=0
            current_piece.y+=1 
            if not(valid_space(current_piece,grid)) and current_piece.y >= 0:
                    current_piece.y-=1
                    change_piece = True


        #PYGAME EVENTS IN TETRIS
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
                pygame.display.quit()
                quit()

            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_LEFT:
                    current_piece.x-=1
                    if not (valid_space(current_piece,grid)) and current_piece.y>0:
                        current_piece.x+=1
                if event.key==pygame.K_RIGHT:
                    current_piece.x+=1
                    if not (valid_space(current_piece,grid)) and current_piece.y>0:
                        current_piece.x-=1
                if event.key==pygame.K_DOWN:
                    current_piece.y+=1
                    if not (valid_space(current_piece,grid)) and current_piece.y>0:
                        current_piece.y -= 1                   
                if event.key==pygame.K_UP:

                    current_piece.rotation+=1
                    if not (valid_space(current_piece,grid)) and current_piece.y>0:
                        current_piece.rotation -= 1

                if event.key == pygame.K_SPACE:
                   while valid_space(current_piece, grid):
                       current_piece.y += 1
                   current_piece.y -= 1

        shape_pos = convert_shape_format(current_piece)

        for i in range(len(shape_pos)):
            x,y=shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        if change_piece:
            for pos in shape_pos:
                p =(pos[0] , pos[1])
                locked_positions[p] = current_piece.color 

            current_piece=next_piece  
            next_piece = get_shape()
            change_piece=False
            if check_lost(locked_positions):
                run = False

            score += fix_rows(grid , locked_positions)
            if high_score <score:
                high_score = score
        
 

        draw_window(WIN,grid,score,high_score)
        draw_next_shape(next_piece,WIN)
        pygame.display.update()

    WIN.fill((0,0,0))
    draw_text("YOU LOST",30,(255,255,255),WIN)
    pygame.display.update()
    pygame.time.delay(1500)

def main_menu():
    run = True
    while run :
        WIN.fill((0,0,0))
        draw_text("PRESS ANY KEY TO CONTINUE",30,(255,255,255),WIN)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False 
            if event.type == pygame.KEYDOWN:
                main()
    pygame.quit()
 
if __name__ == '__main__':
    main_menu()