print("Importing libraries ... ")
from openai import OpenAI
import pygame
import render
import keyboard as kboard
import pyperclip as pyclip
import threading as thr
print("Done importing ✓")

#variables init
BUTTON_COLOURS = ((80,80,80), (120,120,120), (120, 230, 120), (100, 255, 100), (0, 0, 0)) # the last one is the extra color for padding
INFIELDS_COLOURS = ((100,100,100), (150,230,150))
current_api_key = None
running = True
openai_inisialised = False

name_of_the_audio = ''
name_of_the_result = ''
clipboard_text = ''

input_fields = []
buttons = []
finished_transcribing_thread = True
#variables init end

def check_all_buttons_ready(except_buttons: list):
    new_buttons_ready = []
    for index in range(len(buttons_ready)):
        if index in except_buttons:
            continue
        else:
            new_buttons_ready.append(buttons_ready[index])
    
    if all(new_buttons_ready):
        return True
    else:
        return False        
    
def transcribe():
    if not openai_inisialised:
        #OpenAI inisialisation
        try:
            print("OpenAI inisialisation")
            client = OpenAI(api_key=current_api_key)
            print("Inisialised succesfuly ✓")
        except:
            print("Client failed to load try running the code again, if the error will remain to pop up, ask Leo to fix the key to the openai ")
            return None
    #Audio file loading with the name of name_of_the_audio
    try:
        audio_file = open(name_of_the_audio, "rb")
        print("Audio file loaded succesfuly ✓")
    except FileNotFoundError:
        print("Aduio file wasnt found, there is no file in the folder or it is not named audio.mp3 ")
        return None
    except:
        print("Unknown error while loading file, it was found though :) Just try running the code again ")
        return None
        

    
    try:
        print("Transcibing...")
        transcription = client.audio.transcriptions.create(model="whisper-1", file=audio_file)
        print("Transcribing succesfuly ✓")
    except:
        print("Transcribing failed, check internet avialability or run the code again, possibly the format of your audio is not supported\nIt is advised to use mp3,mp4,mpeg and wav")
        return None
        

    print(transcription)

    text_file = open(name_of_the_result,'w')
    text_file.write(transcription.text)
    text_file.close()

    audio_file.close()
    
    finished_transcribing_thread = True

#Inisialisations of the input fields and buttons
main_screen = render.Screen((600,500))
input_fields.append(render.InputField(main_screen, position = (10, 10), font = None, font_colour = (0, 0, 0), font_size = 22, bg_colour1 = INFIELDS_COLOURS[1], bg_colour2 = INFIELDS_COLOURS[0], 
                                      offset = 5, border = 3, min_width = 50, extra_width = 10))
input_fields.append(render.InputField(main_screen, position = (10, 40), font = None, font_colour = (0, 0, 0), font_size = 22, bg_colour1 = INFIELDS_COLOURS[1], bg_colour2 = INFIELDS_COLOURS[0], 
                                      offset = 5, border = 3, min_width = 50, extra_width = 10))
input_fields.append(render.InputField(main_screen, position = (10, 70), font = None, font_colour = (0, 0, 0), font_size = 22, bg_colour1 = INFIELDS_COLOURS[1], bg_colour2 = INFIELDS_COLOURS[0], 
                                      offset = 5, border = 3, min_width = 50, extra_width = 10))

buttons.append(render.Button(main_screen, position = (440, 10), rect_padding=True, text='Submit audio name',font = None, font_colour = (0, 0, 0), font_size = 22, bg_colours = BUTTON_COLOURS,      #button 0
                                      offset = 5, border = 0, width = 30, extra_width = 10, extra_Rectborder = 3))

buttons.append(render.Button(main_screen, position = (440, 40), rect_padding=True, text='Submit text file name', font = None, font_colour = (0, 0, 0), font_size = 22, bg_colours = BUTTON_COLOURS, #button 1
                                      offset = 5, border = 0, width = 30, extra_width = 10, extra_Rectborder = 3))

buttons.append(render.Button(main_screen, position = (440, 70), rect_padding=True, text='Submit api_key', font = None, font_colour = (0, 0, 0), font_size = 22, bg_colours = BUTTON_COLOURS, 
                                      offset = 5, border = 0, width = 30, extra_width = 10, extra_Rectborder = 3))

buttons.append(render.Button(main_screen, position = (255, 400), rect_padding=True, text='Transcribe', font = None, font_colour = (250, 250, 250), font_size = 24, bg_colours = BUTTON_COLOURS,     #button 2
                                      offset = 5, border = 0, width = 30, extra_width = 10, extra_Rectborder = 3))

buttons.append(render.Button(main_screen, position = (255, 300), rect_padding=True, text='Reset api_key', font = None, font_colour = (250, 250, 250), font_size = 24, bg_colours = BUTTON_COLOURS,  #button 3
                                      offset = 5, border = 0, width = 30, extra_width = 10, extra_Rectborder = 3))

buttons_ready = [False for _ in buttons]

transcribeThread = thr.Thread(target=transcribe)

while running:
    main_screen.screen.fill(main_screen.fill)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        for field in input_fields:
            field.check_input(event)
        for button in buttons:
            button.check_ready(event)
            
    if kboard.is_pressed('ctrl+v'):
        clipboard_text = pyclip.paste()
        if clipboard_text is not None:
            for field in input_fields:
                if field.active:
                    field.text = clipboard_text
        

    #displaying all the buttons
    for field in input_fields:
        field.display_input()
    for button in buttons:
        button.display()
        
    # checking if the buttons are ready or not:
    for index in range(len(buttons)):
        if buttons[index].state == 3:
            buttons_ready[index] = True
            #for button 0 the the audio file name will be saved
            if index == 0:
                name_of_the_audio = input_fields[index].text
            #for button 1 the name of the result text fiel will be saved
            elif index == 1:
                name_of_the_result = input_fields[index].text
            elif index == 2:
                current_api_key = input_fields[index].text
            elif index == 3:
                openai_inisialised = False
        else:
            #   if the buttons are ready then the buttons ready bool will be assigned true respectfully to their index in buttons list
            #   if the buttons arent ready then the bool will be false
            buttons_ready[index] = False
            
    pygame.display.flip()

    main_screen.clock.tick(120)  # limits FPS to 120
    
    if check_all_buttons_ready(except_buttons=[4]) and finished_transcribing_thread:
        finished_transcribing_thread = False
        
        print("in the if")
        
        transcribeThread.start()
        
        print("after start")
        for button in buttons:
            button.state = 0
pygame.quit()
exit()
# pygame setup
