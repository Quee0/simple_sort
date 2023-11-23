import pygame
import random
import time
import threading
import pysine

WIDTH, HEIGHT = 1800, 900
FPS = 10000
FADE_FPS = 250
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (50, 205, 50)
BARS_AMOUNT = 900

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Basic sorting algorithm')

class Bar:
    def __init__(self,x,value, bar_width, color):
        self.position = pygame.Rect(x, 0, bar_width, (float(value)/BARS_AMOUNT)*HEIGHT)
        self.position.bottomleft = (x, HEIGHT)
        self.value = value
        self.color = color

    def move(self, x):
        self.position.bottomleft = (x, HEIGHT)
    
    def change_color(self,color):
        self.color = color

    def x_position(self):
        return self.position.bottomleft[0]

def play_sound(freq, dur):
    pysine.sine(frequency=freq, duration=dur)

# thread_list = []
def sort_and_move(bars,sorting_index):
    # thread_list.append(threading.Thread(target = play_sound, args=(200.0,1.0)).start())
    # play_sound(400)
    if bars[sorting_index].value < bars[sorting_index-1].value:
        bar1_x = bars[sorting_index-1].x_position()
        bar2_x = bars[sorting_index].x_position()

        #bar 1
        bars[sorting_index-1].move(bar2_x)
        #bar 2
        bars[sorting_index].move(bar1_x)

        bars[sorting_index], bars[sorting_index-1] = bars[sorting_index-1], bars[sorting_index]
    bars[sorting_index].change_color(RED)
    bars[sorting_index-1].change_color(RED)
    sorting_index += 1
    return [bars, sorting_index]

def decolorize(bars):
    
    for bar in bars:
        bar.change_color(WHITE)
    
    return bars

def randomised_list(size,step):
    start_list = [i for i in range(1,size+1,step)]
    end_list = []
    while len(start_list) > 0:
        num = random.randint(1,len(start_list))-1
        end_list.append(start_list[num])
        start_list.pop(num)
    
    return end_list

def draw(bars):
    WIN.fill(BLACK)

    for bar in bars:
        pygame.draw.rect(WIN, bar.color, bar.position)

    pygame.display.update()

def main():
    clock = pygame.time.Clock()
    run = True

    l = randomised_list(BARS_AMOUNT, 1)
    BAR_WIDTH = WIDTH/len(l)
    bars = []
    for i in range(len(l)):
        bars.append(Bar(i*BAR_WIDTH,l[i],BAR_WIDTH, BLACK))
    
    fade_in_list = randomised_list(BARS_AMOUNT, 1)
    fade_in_counter = 0
    fade_in_stop = True

    sorting_index = 1
    greening_index = -1
    counter = len(bars)
    final_uncolor = False

    while run:
        if fade_in_counter == BARS_AMOUNT+1: clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            #RESET
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:

                    l = randomised_list(BARS_AMOUNT, 1)
                    BAR_WIDTH = WIDTH/len(l)
                    bars = []
                    for i in range(len(l)):
                        bars.append(Bar(i*BAR_WIDTH,l[i],BAR_WIDTH, BLACK))

                    fade_in_list = randomised_list(BARS_AMOUNT, 1)
                    fade_in_counter = 0
                    fade_in_stop = True

                    sorting_index = 1
                    greening_index = -1
                    counter = len(bars)
                    final_uncolor = False

        draw(bars)

        if fade_in_counter < BARS_AMOUNT:
            clock.tick(FADE_FPS)
            bars[fade_in_list[fade_in_counter]-1].change_color(WHITE)
            fade_in_counter += 1

        if fade_in_stop and fade_in_counter == BARS_AMOUNT:
            time.sleep(1.5)
            fade_in_counter += 1
            fade_in_stop = False

        if fade_in_counter >= BARS_AMOUNT and final_uncolor == True: 
            final_uncolor = False
            bars = decolorize(bars)
        
        # print(440+(BARS_AMOUNT-counter)*5)
        # print(1-(BARS_AMOUNT - float(counter)/200))

        if fade_in_counter >= BARS_AMOUNT and counter > -1:
            bars = decolorize(bars)
            if sorting_index >= len(bars) or sorting_index >= counter:
                # threading.Thread(target = play_sound, args=[200+(BARS_AMOUNT-counter)*5,BARS_AMOUNT - float(counter)/200]).start()
                sorting_index = 1   
            unpack = sort_and_move(bars, sorting_index)
            bars = unpack[0]
            sorting_index = unpack[1]
            if sorting_index >= counter: counter -= 1
        elif fade_in_counter >= BARS_AMOUNT and counter == -1:
            final_uncolor = True
            counter = -2
        
        if fade_in_counter >= BARS_AMOUNT and counter == -2 and greening_index < len(bars):
            bars[greening_index].change_color(GREEN)
            greening_index+=1

    pygame.quit()

if __name__ == '__main__': 
    main()
