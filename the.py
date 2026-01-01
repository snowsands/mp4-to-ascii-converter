
import cv2
import math
import numpy as np
import os
import sys 
import tkinter as tk

def get_framerate(video_name):
    video = cv2.VideoCapture(f'{video_name}.mp4')
    fps = video.get(cv2.CAP_PROP_FPS)
    print(f"framerate is {fps} fps")

def extract_convert(video_name):
    video = cv2.VideoCapture(f'{video_name}.mp4')
    
    current_frame = 0
    video_frame = 0
    
    asc = []
    grayscale_map = "@%#*+=-:. " 
    factor = 255 // len(grayscale_map)
    
    height = 200
    width = 666
    
    while(True):
        success, frame = video.read()
        if not success:
            break
        
        # 5
        if current_frame % 5 == 0:
            # converting to grayscale is faster
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            img_array = convert(frame, video_frame, grayscale_map, factor, height, width)
            
            ascii_input = ""
            # .join() function:
            # joins a list of strings and glues them together w/ a given separator
            for row in img_array:
                ascii_input += ''.join(row) + '\\n'
            asc.append(ascii_input)
            video_frame += 1
        current_frame += 1
        
    if not os.path.exists('asciitxtfiles'):
        os.makedirs('asciitxtfiles', exist_ok = True)
    
    with open(f'./asciitxtfiles/{video_name}.txt', 'w') as f:
        for ascii_img in asc:
            f.write(f'{ascii_img}\n')
    
    video.release()
    

def convert(frame, video_frame, grayscale_map, factor, height, width):
    print(f'adding frame {video_frame}')
    img = cv2.resize(frame, (width, height))
    img_array = [[' ' for _ in range(width)] for _ in range(height)]
    
    for i in range(0, height):
        for j in range(0, width):
            # converting to grayscale then assigning to a single brightness value is faster
            #r, g, b = img[i, j]
            #brightness = 0.299 * r + 0.587 * g + 0.114 * b
            
            #brightness = img[i, j]
            index = min(math.floor(img[i, j] / factor), len(grayscale_map) - 1)
            img_array[i][j] = grayscale_map[index]
    return img_array
             
        
# root.after() function:
# runs after a delay -> inputs: delay in ms, function to run, and then args for the called function
# im doing 8 fps so every 125 ms
def display(video_name):
    
    root = tk.Tk()
    root.geometry('1920x1080')
    root.title(video_name)

    text_widget = tk.Text(root, font=("Courier New", 3), bg="black", fg="white")
    text_widget.pack(expand=True, fill="both")
    
    asc = []
    with open(f'./asciitxtfiles/{video_name}.txt', 'r') as f:
        for line in f:
            asc.append(line.replace('\\n', '\n'))
    
    def update_frame(i):
        if i < len(asc): # keeps looping until window is closed
            print(f'displaying frame {i}')
            text_widget.delete('1.0', tk.END)
            text_widget.insert(tk.END, asc[i]) # .replace('\\n', '\n') 
            # do 83 for 12 fps on a 60 fps source video
            root.after(83, update_frame, i + 1)
        else:
            root.after(83, update_frame, 0)
    update_frame(0)
    root.mainloop()
    
    
def extract_prompt():
    while (True):
        s = input('enter the name of the video file inside this folder, exclude the mp4 tag: ')
        if os.path.exists(f'{s}.mp4'):
            print(f'extracting frames from {s}.mp4')
            return s
        else:
            print('invalid filename, try again')


def existing_txts():
    if not os.path.exists('asciitxtfiles'):
        os.makedirs('asciitxtfiles')
        
    if len(os.listdir('asciitxtfiles')) == 0:
        return
    else:
        while (True):
            existing = input('there are existing videos that you could play. would you like to play them? y/n ')
            if existing == 'y':
                break
            elif existing == 'n':
                return
    
    txts = []
    for txt_name in os.listdir('asciitxtfiles'):
        txts.append(txt_name)

    while(True):
        print(txts)
        s = input('these are the available videos to play. enter the video name you would like to play, excluding the .mp4: ')
        if f'{s}.txt' in txts:
            break
        else:
            print('invalid video name, try again')
            
    print(f'displaying {s}')
    display(s)
    sys.exit(0)


def run():
    existing_txts()       
    
    video_name = extract_prompt()
    
    print(f'now extracting {video_name}')
    extract_convert(video_name)
    
    print(input('finished extracting, want to display? '))
    print('displaying')
    display(video_name)
    
    
print(input('Ready to start? '))
run()


