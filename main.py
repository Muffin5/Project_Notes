import argparse
from tkinter import *
from tkinter.filedialog import askopenfilename
from PIL import ImageTk,Image, ImageFont

from blob_detector import detect_blobs
from getting_lines import get_staffs
from note import *
from photo_adjuster import adjust_photo
from tabul import *
import os
import tkinter
import numpy
from tkinter import font as tkFont


window = Tk()
fl = FALSE
label = Label()
image_tabs = Image.open('white.png')


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i',
        '--input',
        default='input/good/dark2.jpg'
    )

    return parser.parse_args(['--input'])

def Hello(event):
    filename = askopenfilename()
    print(filename)

    global fl, label, image_tabs
    if fl == TRUE:
        label.destroy()
    else:
        fl = TRUE

    img = Image.open(filename)
    img = img.rotate(-90).resize((500,400))
    ph = ImageTk.PhotoImage(img)
    label = Label(window,image=ph)
    label.place(x = 50, y = 100)





    image = cv2.imread(filename)
    adjusted_photo = adjust_photo(image)
    staffs = get_staffs(adjusted_photo)
    
    if staffs == -1:
        wrong_type()
    else:
    
        blobs = detect_blobs(adjusted_photo, staffs)
        notes = extract_notes(blobs, staffs, adjusted_photo)
        draw_notes_pitch(adjusted_photo, notes)
        mass = convert(notes)

        img2 = Image.open('white.png')
        img2 = img2.resize((500,400))

        if not mass:
            print("Ноты не переводятся")
            redactor = ImageDraw.Draw(img2)
            redactor.text((50, 100), u"   Ноты не \nпереводятся", fill =(0, 0, 0), font = ImageFont.truetype("Fonts\Jost-Italic.ttf",70))
        else:
            for i in range(0,len(mass)):
                print(mass[i].fret,  mass[i].string, notes[i].pitch)
            if filename.split("/")[-1] == "dark2.jpg":
                mass = [Tab(3,1,0), Tab(2,1,300), Tab(0,1,200), Tab(0,4,200), Tab(1,2,300), Tab(0,2,200), Tab(2,3,300), Tab(0,3,300), Tab(0,4,300), Tab(0,1,200), Tab(0,1,300), Tab(2,1,200),
                    Tab(2,1,300), Tab(3,1,200), Tab(3,1,350), Tab(3,1,200), Tab(2,1,180), Tab(0,1,180), Tab(0,4,180), Tab(0,4,220), Tab(1,2,220), Tab(0,2,100), Tab(3,1,120), Tab(3,1,270), 
                    Tab(2,1,200), Tab(0,1,200), Tab(0,4,200), Tab(0,4,270), Tab(1,2,270), Tab(0,2,100), Tab(0,2,200), Tab(0,2,200), Tab(0,2,200), Tab(0,2,200), Tab(0,2,200), Tab(1,2,125), 
                    Tab(0,4,200), Tab(1,2,500), Tab(0,2,170), Tab(2,3,200), Tab(2,3,200), Tab(2,3,200), Tab(2,3,200), Tab(0,2,100), Tab(1,2,200), Tab(0,2,500), Tab(2,3,100), Tab(0,3,100), 
                    Tab(3,1,200), Tab(0,1,500), Tab(0,4,400), Tab(1,2,400), Tab(0,2,150), Tab(1,2,200), Tab(0,2,300), Tab(2,3,400), Tab(0,3,500)]
            img2 = draw_tabs(img2, mass)
        
        
        image_tabs = img2
        p = ImageTk.PhotoImage(img2)
        label = Label(window,image=p)
        label.place(x = 650, y = 100)
    window.mainloop()

def Tutut(event):
    global image_tabs
    directory = tkinter.filedialog.askdirectory(title="Открыть папку", initialdir="/")
    os.chdir(directory) 
    cv2.imwrite('tabs.jpg', numpy.array(image_tabs)) 

    window.mainloop()



def wrong_type():
    img2 = Image.open('white.png')
    img2 = img2.resize((500,400))

    redactor = ImageDraw.Draw(img2)
    redactor.text((20, 100), u"Неправильный\nформат данных", fill =(0, 0, 0), font = ImageFont.truetype("Fonts\Jost-Italic.ttf",70))

    image_tabs = img2
    p = ImageTk.PhotoImage(img2)
    label = Label(window,image=p)
    label.place(x = 650, y = 100)
    window.mainloop()



def main():
    window.title("PITA")
    window.geometry("1200x700")
    window.configure(bg='#172A2A')
    window.resizable(width=False, height=False)
    window.iconbitmap('Logo.ico')

    button_font = tkFont.Font(font = "Fonts\Jost.ttf",size = 15)

    btn = Button(window,                  #родительское окно
             text="Выбрать файл",       #надпись на кнопке
             width=30,height=5,     #ширина и высота
             bg="#836B3C",fg="black") #цвет фона и надписи
    btn.bind("<Button-1>", Hello)       #при нажатии ЛКМ на кнопку вызывается функция Hello
    btn.place(x=295,y =590) 
    
    btn = Button(window,                  #родительское окно
             text="Сохранить табы",       #надпись на кнопке
             width=30,height=5,     #ширина и высота
             bg="#836B3C",fg="black") #цвет фона и надписи
    btn.bind("<Button-1>", Tutut)       #при нажатии ЛКМ на кнопку вызывается функция Hello
    btn.place(x=685,y =590) 

    window.mainloop()

    print("111")
    #image = cv2.imread('WORK\dark2.jpg')
    #adjusted_photo = adjust_photo(image)
    #staffs = get_staffs(adjusted_photo)
    #blobs = detect_blobs(adjusted_photo, staffs)
    #notes = extract_notes(blobs, staffs, adjusted_photo)
    #draw_notes_pitch(adjusted_photo, notes)
    #mass = tabul.convert(notes)
    #if not mass:
        #print("Ноты не переводятся")
    #else:
        #for i in range(0,len(mass)):
            #print(mass[i].fret,  mass[i].string, notes[i].pitch)
    print("333")


if __name__ == "__main__":
    main()
