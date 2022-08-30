import random
import pygame as pyg
from pygame import mixer
def file_loader(fileName):
    file=open(fileName)
    words=file.readlines()
    file.close()
    return [word[:5].upper() for word in words]

# word_guess=file_loader()
word_answers=file_loader("words.txt") # it gives us list of all words
ans=random.choice(word_answers)
print(ans)
width=600
height=700
margin = 10
top_margin=100
bot_margin=100
lr_margin=100


pyg.init()
pyg.font.init()
pyg.display.set_caption("Wordle")
# create screen
screen = pyg.display.set_mode((width,height))

#adding image to background
bg_img = pyg.image.load('Images/bg.jpg')
bg_img = pyg.transform.scale(bg_img,(width,height))

#adding background music

mixer.music.load('background.wav')
mixer.music.play(-1)

Input=""
Guesses=[]
alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
Unguessed= alphabet



#game specific variables
square_size=(width-4*margin-2*lr_margin)//5
font=pyg.font.SysFont("free sans bold",square_size)
font_small=pyg.font.SysFont("free sans bold",square_size//2)
grey=(70,70,80)
green=(6,214,160)
yellow=(255,209,102)
white=(255,255,255)
game_over=False
fillcolor="black"

def determine_unguessed_letters(guesses):
    guessed_letters = "".join(guesses)
    unguessed_letters=""
    for letter in alphabet:
        if letter not in guessed_letters:
            unguessed_letters=unguessed_letters+letter
    return unguessed_letters

def determine_color(guess,j):
    letter=guess[j]
    if letter==ans[j]:
        return green
    elif letter in ans:
        n_target=ans.count(letter)
        n_correct=0
        n_occurence=0
        for i in range(5):
            if guess[i]==letter:
                if i<=j:
                    n_occurence+=1
                if letter==ans[i]:
                    n_correct+=1
        if n_target - n_correct - n_occurence>=0:
            return yellow
    return grey

#animation loop
i = 0
animate=True
while animate:
    # background
    screen.fill((0, 0, 0))
    screen.blit(bg_img, (i, 0))
    screen.blit(bg_img,(width+i,0))
    if (i == -width):
        screen.blit(bg_img, (width + i, 0))
        i = 0
    i -= 1
    # screen.fill(fillcolor)

    # draw unguessed letters
    letters=font_small.render(Unguessed,False,white )
    surface = letters.get_rect(center=(width// 2,top_margin // 2))
    screen.blit(letters, surface)


    #draw guesses
    y=top_margin
    for i in range(6):
        x=lr_margin
        for j in range(5):

            #square
            square=pyg.Rect(x,y,square_size,square_size)
            pyg.draw.rect(screen,grey,square,width=2)

            #letters/words that have already been guessed
            if i<len(Guesses):
                color=determine_color(Guesses[i],j)
                pyg.draw.rect(screen,color,square)
                letter=font.render(Guesses[i][j],False,(255,255,255))
                surface=letter.get_rect(center=(x+square_size//2,y+square_size//2))
                screen.blit(letter,surface)


            #user text input (next guess)
            if i == len(Guesses) and j<len(Input):
                letter = font.render(Input[j], False,grey)
                surface = letter.get_rect(center=(x + square_size // 2, y + square_size // 2))
                screen.blit(letter, surface)

            x += square_size+margin
        y+=square_size+margin

    # correct answer after game over
    if len(Guesses)==6 and Guesses[5]!= ans:
        game_over=True
        letters = font.render(ans, False, white)
        surface = letters.get_rect(center=(width // 2, height-bot_margin // 2-margin))
        screen.blit(letters, surface)
        lose=mixer.Sound('lose.wav')
        lose.play()




    #update the screen
    pyg.display.flip()
    #track user interaction
    for event in pyg.event.get():
        if event.type==pyg.QUIT:
            animate=False
        #user presses key
        elif event.type == pyg.KEYDOWN:
            # escape key to quit the animation
            if event.key == pyg.K_ESCAPE:
                animate = False


            # backspace key
            if event.key == pyg.K_BACKSPACE:
                if len(Input) > 0:
                    Input = Input[:len(Input)-1]
            # return key to submit
            elif event.key==pyg.K_RETURN:
                if len(Input)==5 and Input in word_answers:
                    Guesses.append(Input)
                    Unguessed=determine_unguessed_letters(Guesses)
                    if Input == ans:
                        game_over =True
                        bg_img = pyg.image.load('win.jpg')
                        screen.fill((1,0, 0))
                        screen.blit(bg_img, (i, 0))
                        screen.blit(bg_img, (width + i, 0))
                        if (i == -width):
                            screen.blit(bg_img, (width + i, 0))
                            i = 0
                        i -= 1
                    else:
                        game_over=False
                    Input=""

            # space bar to restart
            elif event.key == pyg.K_SPACE:
                game_over=False
                ans=random.choice(word_answers)
                print(ans)
                Guesses=[]
                Unguessed=alphabet
                Input=""
                aipaaye = mixer.Sound('Aipaye.wav')
                aipaaye.play()

            elif len(Input)<5 and not game_over:
                Input=Input+event.unicode.upper()
                # print(Input)

    pyg.display.update() # display.update function to update the screen with all the elements declared.
