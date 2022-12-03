import taichi as ti
import numpy
import pygame
from pygame import mixer
ti.init(arch=ti.cpu)
pygame.init()

WIDTH = 1600
HEIGHT = 740

black = (0, 0, 0)
white = (255, 255, 255)
gray = (128, 128, 128)
green = (0, 255, 0)

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('TaichiMusician')
note_font = pygame.font.Font('freesansbold.ttf', 12)

fps = 45
timer = pygame.time.Clock()
sequence = 128
total_notes = 0

frame = []

bpm = 600
playing = True
active_length = 0
active_beat = 1
changed = True
flag = 1
space = 0

# loading sounds
guitar_notes = ["b", "a#", "a", "g#", "g", "f#", "f", "e", "d#", "d", "c#", "c"]
notes = []
for i in range(5,2,-1):
    for j in range(len(guitar_notes)):
            total_notes = total_notes + 1
            notes.append(mixer.Sound('sounds\guitar\guitar-' + guitar_notes[j] + str(i)+ '.wav'))

total_notes = total_notes + 6
notes.append(mixer.Sound('sounds\drum\Analog Crash.wav'))
notes.append(mixer.Sound('sounds\drum\Hihat.wav'))
notes.append(mixer.Sound('sounds\drum\Closed Hihat.wav'))
notes.append(mixer.Sound('sounds\drum\snare2.wav'))
notes.append(mixer.Sound('sounds\drum\snare1.wav'))
notes.append(mixer.Sound('sounds\drum\kick.wav'))

clicked = [[-1 for _ in range(sequence)] for _ in range(total_notes)]

notes_button_posX = ti.field(ti.f32, shape=(sequence, total_notes))
notes_button_posY = ti.field(ti.f32, shape=(sequence, total_notes))
notes_button_lenX = ti.field(ti.f32, shape=(sequence, total_notes))
notes_button_lenY = ti.field(ti.f32, shape=(sequence, total_notes))

pygame.mixer.set_num_channels(total_notes*3)

@ti.kernel
def calculate_note_button_parameter():
    space = (HEIGHT-60)/total_notes
    for i in range(sequence):
        for j in range(total_notes):
            notes_button_posX[i,j] = i * (WIDTH-50) // sequence + 51
            notes_button_posY[i,j] = (j * space)+2

            notes_button_lenX[i,j] = (WIDTH-50 ) // sequence - 1
            notes_button_lenY[i,j] = (HEIGHT)//total_notes -5

def play_notes():
    for i in range(total_notes):
        if clicked[i][active_beat] == 1:
            notes[i].play()


def piant(clicks, beat):
    
    space = (HEIGHT-60)/total_notes
    
    left_box = pygame.draw.rect(screen, gray, (0, 0, 50, HEIGHT), 1)
    
    frame = []
    colors = [gray, white, gray]
    
    num = -1
    for i in range(5,2,-1):
        for j in range(len(guitar_notes)):
            num = num+1
            text = note_font.render(guitar_notes[j] + str(i), True, black)
            screen.blit(text, (20, num*space+space//8))
    num += 1
    text = note_font.render('crash', True, black)
    screen.blit(text, (5, num*space+space//8))
    num += 1
    text = note_font.render('hihat1', True, black)
    screen.blit(text, (5, num*space+space//8))
    num += 1
    text = note_font.render('hihat2', True, black)
    screen.blit(text, (5, num*space+space//8))
    num += 1
    text = note_font.render('snare1', True, black)
    screen.blit(text, (5, num*space+space//8))
    num += 1
    text = note_font.render('snare2', True, black)
    screen.blit(text, (5, num*space+space//8))
    num += 1
    text = note_font.render('kick', True, black)
    screen.blit(text, (5, num*space+space//8))
    
    
    nbpX = notes_button_posX.to_numpy()
    nbpY = notes_button_posY.to_numpy()
    nblX = notes_button_lenX.to_numpy()
    nblY = notes_button_lenY.to_numpy()
    

    for i in range(total_notes):
        pygame.draw.line(screen, gray, (0, (i * space) +space), (50, (i * space) + space), 1)

    for i in range(sequence):
        for j in range(total_notes):
            if clicks[j][i] == -1:
                color = gray
            else:
                color = green
            rect = pygame.draw.rect(screen, color, 
                   [float(nbpX[i][j]), float(nbpY[i][j]), 
                    float(nblX[i][j]), float(nblY[i][j])], 0, 5) 
            frame.append((rect, (i, j)))

    #imp = pygame.image.load("C:\\Users\\DELL\\Downloads\\gfg.png").convert()
    imp = pygame.image.load("icon\\1.png").convert()
    screen.blit(imp, (beat * (WIDTH - 50)//sequence + 35,685))
    active = pygame.draw.rect(screen, green, [beat * (WIDTH - 50)//sequence + 50, 0, (WIDTH - 50)//sequence, total_notes * space], 1 ,1)
    return frame


run = True
calculate_note_button_parameter()
while run:
    timer.tick(fps)
    screen.fill(white)
    frame = piant(clicked, active_beat)

    if changed:
        play_notes()
        changed = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(frame)):
                if frame[i][0].collidepoint(event.pos):
                    coords = frame[i][1]
                    clicked[coords[1]][coords[0]] *= -1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                if playing:
                    playing = False
                elif not playing:
                    playing = True   
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_i:
                flag *= -1
                if flag == 1:
                    playing = True

    length = fps*60 // bpm

    if playing:
        
        if active_length < length:
                active_length += 1
        else: 
            active_length = 0
            
            if flag == -1:
                playing = False
                active_beat = -2
                changed = True

            if active_beat < sequence - 1:
                active_beat += 1
                changed = True
            else:
                active_beat = 0
                changed = True 

    pygame.display.flip()
pygame.quit()