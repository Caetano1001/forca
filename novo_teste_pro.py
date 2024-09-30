#Título: criando uma tela inicial de game
#link do material da aula:https://replit.com/@carlosfeuser/jogo-da-forca-copia#main.py
#Setup de Entrada - Import Bibliotecas-----------------------------------------#
import pygame, sys
import random

#Setup de Entrada - Definições ----------------------------------------------- #
mainClock = pygame.time.Clock()
from pygame.locals import *
pygame.init()
#pygame.display.set_caption('Jogo da forca')
screen = pygame.display.set_mode((700, 850),0,32)
font = pygame.font.SysFont('', 30)

#pygame.init()
winHeight = 600
winWidth = 850
win=pygame.display.set_mode((winWidth,winHeight))

#Definição de imagens
energia0 = 'forca.png'
BLACK = (0, 0, 0)
WHITE = (255,255,255)
RED = (255,0, 0)
GREEN = (187, 170, 154)
BLUE = (0,0,255)
LIGHT_BLUE = (255,255,255)

btn_font = pygame.font.SysFont("arial", 20)
guess_font = pygame.font.SysFont("monospace", 24)
lost_font = pygame.font.SysFont('arial', 25)
word = ''
buttons = []
guessed = []

hangmanPics = [pygame.image.load('hangman0.png'),
pygame.image.load('hangman1.png'),
pygame.image.load('hangman2.png'),
pygame.image.load('hangman3.png'), 
pygame.image.load('hangman4.png'), 
pygame.image.load('hangman5.png'), 
pygame.image.load('hangman6.png')]
pygame.image.load('forca.png')

limbs = 0

#Definição de Escrita de Texto-------------------------------------------------#
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

click = False

#Definição de ações do Menu Inicial--------------------------------------------#
def main_menu():
    while True:

        screen.fill((132, 155, 149))
        draw_text('Jogo da forca', font, (55, 255, 255), screen, 330, 40)

        mx, my = pygame.mouse.get_pos()
        
        button_0 = pygame.Rect(300, 25, 200, 50)
        button_1 = pygame.Rect(300, 200, 200, 50)
        button_2 = pygame.Rect(300, 300, 200, 50)
        button_3 = pygame.Rect(300, 400, 200, 50)
        
        if button_1.collidepoint((mx, my)):
            if click:
                game()
        if button_2.collidepoint((mx, my)):
            if click:
                options()
        if button_3.collidepoint((mx, my)):
            if click:
                exite()

        pygame.draw.rect(screen, (144, 133, 111), button_0)
        pygame.draw.rect(screen, (187, 170, 154), button_1)
        pygame.draw.rect(screen, (187, 170, 154), button_2)
        pygame.draw.rect(screen, (187, 170, 154), button_3)
        draw_text('Jogar', font, (255, 255, 255), screen, 372, 215)
        draw_text('Opções', font, (255, 255, 255), screen, 363, 315)
        draw_text('Sair', font, (255, 255, 255), screen, 378, 415)
        draw_text('JOGO DA FORCA', font, (255, 255, 255), screen, 317, 40)

        image = pygame.image.load('forca.png')  # Replace 'your_image.png' with your actual image file
        image = pygame.transform.scale(image, (250, 250))  # Adjust the size as needed
        # Position the image
        screen.blit(image, (30, 150))
        
        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        mainClock.tick(60)

#Definições dos Submenus dos Botões - Game - Opções - Sair --------------------#

#
# Definição do game
#
def game():
    
    def redraw_game_window():
        global guessed
        global hangmanPics
        global limbs
        win.fill(GREEN)
        # Buttons
        for i in range(len(buttons)):
            if buttons[i][4]:
                pygame.draw.circle(win, BLACK, (buttons[i][1], buttons[i][2]), buttons[i][3])
                pygame.draw.circle(win, buttons[i][0], (buttons[i][1], buttons[i][2]), buttons[i][3] - 2
                                )
                label = btn_font.render(chr(buttons[i][5]), 1, BLACK)
                win.blit(label, (buttons[i][1] - (label.get_width() / 2), buttons[i][2] - (label.get_height() / 2)))

        spaced = spacedOut(word, guessed)
        label1 = guess_font.render(spaced, 1, BLACK)
        rect = label1.get_rect()
        length = rect[2]

        win.blit(label1,(winWidth/2 - length/2, 400))

        pic = hangmanPics[limbs]
        win.blit(pic, (winWidth/2 - pic.get_width()/2 + 20, 150))
        pygame.display.update()


    def randomWord():
        file = open('words (copy).txt')
        f = file.readlines()
        i = random.randrange(0, len(f) - 1)

        return f[i][:-1]


    def hang(guess):
        global word
        if guess.lower() not in word.lower():
            return True
        else:
            return False

    def spacedOut(word, guessed=[]):
        spacedWord = ''
        guessedLetters = guessed
        for x in range(len(word)):
            if word[x] != ' ':
                spacedWord += '_ '
                for i in range(len(guessedLetters)):
                    if word[x].upper() == guessedLetters[i]:
                        spacedWord = spacedWord[:-2]
                        spacedWord += word[x].upper() + ' '
            elif word[x] == ' ':
                spacedWord += ' '
        return spacedWord


    def buttonHit(x, y):
        for i in range(len(buttons)):
            if x < buttons[i][1] + 20 and x > buttons[i][1] - 20:
                if y < buttons[i][2] + 20 and y > buttons[i][2] - 20:
                    return buttons[i][5]
        return None


    def end(winner=False):
        global limbs
        lostTxt = 'Perdeu, toque em qualquer tecla para continuar...'
        winTxt = 'GANHOU!, toque em qualquer tecla para continuar...'
        redraw_game_window()
        pygame.time.delay(1000)
        win.fill(GREEN)

        if winner == True:
            label = lost_font.render(winTxt, 1, BLACK)
        else:
            label = lost_font.render(lostTxt, 1, BLACK)

        wordTxt = lost_font.render(word.upper(), 1, BLACK)
        wordWas = lost_font.render('A frase era: ', 1, BLACK)

        win.blit(wordTxt, (winWidth/2 - wordTxt.get_width()/2, 295))
        win.blit(wordWas, (winWidth/2 - wordWas.get_width()/2, 245))
        win.blit(label, (winWidth / 2 - label.get_width() / 2, 140))
        pygame.display.update()
        again = True
        while again:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    again = False
        reset()


    def reset():
        global limbs
        global guessed
        global buttons
        global word
        for i in range(len(buttons)):
            buttons[i][4] = True

        limbs = 0
        guessed = []
        word = randomWord()

    #MAINLINE


    # Setup buttons
    increase = round(winWidth / 13)
    for i in range(26):
        if i < 13:
            y = 40
            x = 25 + (increase * i)
        else:
            x = 25 + (increase * (i - 13))
            y = 85
        buttons.append([LIGHT_BLUE, x, y, 20, True, 65 + i])
        # buttons.append([color, x_pos, y_pos, radius, visible, char])

    word = randomWord()
    inPlay = True

    while inPlay:
        redraw_game_window()
        pygame.time.delay(10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                inPlay = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    inPlay = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                clickPos = pygame.mouse.get_pos()
                letter = buttonHit(clickPos[0], clickPos[1])
                if letter != None:
                    guessed.append(chr(letter))
                    buttons[letter - 65][4] = False
                    if hang(chr(letter)):
                        if limbs != 5:
                            limbs += 1
                        else:
                            end()
                    else:
                        print(spacedOut(word, guessed))
                        if spacedOut(word, guessed).count('_') == 0:
                            end(True)

    pygame.quit()

def options():
    running = True
    while running:
        screen.fill((0,0,0))

        draw_text('Opções', font, (255, 155, 155), screen, 20, 20)
      #Mudei a cor do texto de opções
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        pygame.display.update()
        mainClock.tick(60)

def exite():
    pygame.quit()
    sys.exit()


main_menu()