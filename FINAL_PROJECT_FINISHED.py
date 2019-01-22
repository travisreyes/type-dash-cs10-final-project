import pygame as pg #hiiiii
import random 

### Classes ###

# Player Class
class player(object):
    driveRight = [pg.image.load('player_car.png')]

    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 10

    def draw(self, win):

        if self.vel > 0:
            win.blit(self.driveRight[0], (self.x,self.y))


# Computer Class
class comp(object):
    driveRight = [pg.image.load('comp_car.png')]
    
    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.path = [x, end]
        # Vel is how fast the car is going to move
        self.vel = 0

    def draw(self, win):
        self.move()
        
        if self.vel > 0:
            win.blit(self.driveRight[0], (self.x,self.y))


            
    def move(self):
        if self.vel > 0:
            if self.x < self.path[1] + self.vel:
                self.x += self.vel
        else:
            if self.x > self.path[0] - self.vel:
                self.x += self.vel

### File Reader Function ###
def read_file(filename):
    f = open(filename , "r")
    file = f.read()
    return file

### Global Variables ###
MENU = True
BEGIN = True
INSTRUCTION = False
START = False 
EASY = False
MEDIUM = False
HARD = False
ANSWER = random.randint(0,999)
VROOM = 0
GAME_OVER = False
WIN = False
LOSE = False
LENGTH = 0


### Start Screen Function ###
def start_screen():
    global MENU
    global START
    global INSTRUCTION
    global EASY
    global MEDIUM
    global HARD
    global BEGIN
    done = False
    screen = pg.display.set_mode((1080, 720))

    while not done: 

        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
                MENU = False

        keys = pg.key.get_pressed()

        if keys[pg.K_1]:
            done = True
            INSTRUCTION = True
            BEGIN = False
        if keys[pg.K_2]:
            done = True
            MENU = False
            START = True
            EASY = True
            BEGIN = False
        if keys[pg.K_3]:
            done = True
            MENU = False
            START = True
            MEDIUM = True
            BEGIN = False
        if keys[pg.K_4]:
            done = True
            MENU = False
            START = True
            HARD = True
            BEGIN = False
            


        screen.blit(pg.image.load('sc.jpg'), (0,0))

        pg.display.update()

### Instruction Function ###
def instruction_screen():
    global MENU
    global BEGIN
    global INSTRUCTION
    done = False
    screen = pg.display.set_mode((1080, 720))

    while not done:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
                MENU = False

        keys = pg.key.get_pressed()

        if keys[pg.K_1]:
            done = True
            BEGIN = True
            INSTRUCTION = False
            
        screen.blit(pg.image.load('ic.jpg'), (0,0))

        pg.display.update()

### Main Function ###
def main():
    ### Window Variables ###
    global ANSWER
    global VROOM
    global EASY
    global MEDIUM
    global HARD
    global GAME_OVER
    global WIN
    global LOSE
    global LENGTH
    screen = pg.display.set_mode((1080, 720))
    bg = pg.image.load('bg.jpg')
    font = pg.font.Font(None, 50)
    font_in_game = pg.font.Font(None, 60)
    clock = pg.time.Clock()
    input_box = pg.Rect(370, 150, 350, 50)
    word_file = read_file('words.txt')
    word_list = word_file.split()
    color_inactive = pg.Color('lightskyblue3')
    color_active = pg.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    done = False

    def text_in_game(msg, x, y, color):
        screen_text = font_in_game.render(msg, True, color)
        screen.blit(screen_text, (x, y))


    while not done:

        if computer.x >= 800:
            done = True
            START = False
            WIN = False
            LOSE = True

        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            if event.type == pg.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if input_box.collidepoint(event.pos):
                    # Toggle the active variable.
                    active = not active
                else:
                    active = False
                # Change the current color of the input box.
                color = color_active if active else color_inactive
            if event.type == pg.KEYDOWN:
                if active:
                    if event.key == pg.K_RETURN:
                        if word_list[ANSWER] == text:
                            LENGTH = len(word_list[ANSWER])
                            ANSWER = random.randint(0,999)
                            VROOM += 1 
                        text = ''
                    elif event.key == pg.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode


        
        if not GAME_OVER:
            # Background Image
            screen.blit(pg.image.load('bg.jpg'), (0,0))


            ### Text Box Display ###
            # Render the current text.
            txt_surface = font.render(text, True, color)
            # Resize the box if the text is too long.b
            width = max(350, txt_surface.get_width()+15)
            input_box.w = width
            # Blit the text.
            screen.blit(txt_surface, (input_box.x+10, input_box.y+5))
            # Blit the input_box rect.
            pg.draw.rect(screen, color, input_box, 2)

            ### Player Sprite ###
            player.draw(screen)


            ### Computer Sprite ###
            computer.draw(screen)

            ### In Game Text ###
            text_in_game('WORD:', 250, 50, pg.Color('azure4'))
            text_in_game(word_list[ANSWER], 410, 50, pg.Color('black'))

            if VROOM == 1:
                player.x += player.vel * LENGTH
                VROOM = 0
            if EASY: 
                computer.vel = 0.65
                EASY = False
            if MEDIUM:
                computer.vel = 1.15
                MEDIUM = False
            if HARD:
                computer.vel = 1.65
                HARD = False




            ### Display ###
            pg.display.flip()
            clock.tick(30)

            if player.x >= 810:
                GAME_OVER = True
                WIN = True
                LOSE = False

            if computer.x >= 800:
                GAME_OVER = True
                WIN = False
                LOSE = True

        ### GAME OVER ###

        if GAME_OVER:
            if WIN:
                screen.blit(pg.image.load('win.jpg'), (0,0))
                done = False
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        done = True
                pg.display.update()

            if LOSE:
                screen.blit(pg.image.load('lose.jpg'), (0,0))
                done = False
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        done = True
                pg.display.update()

### GAME LOOP ###

if __name__ == '__main__':
    pg.init()
    pg.display.set_caption('Type Dash')
    computer = comp(25, 575, 250, 75, 810)
    player = player(25, 410, 250, 75)
    while MENU:    
        if BEGIN:   
            start_screen()
        if INSTRUCTION:
            instruction_screen()
    if START:
        main()
    pg.quit()
