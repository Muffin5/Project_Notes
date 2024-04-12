import argparse
from tkinter import *
from tkinter.filedialog import askopenfilename
from PIL import ImageTk, Image, ImageFont

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
flag_label = FALSE
label = Label()
image_tabs = Image.open("images/white.png")


def Conversion(event):
    filename = askopenfilename()

    global flag_label, label, image_tabs
    if flag_label == TRUE:
        label.destroy()
    else:
        flag_label = TRUE

    img = Image.open(filename)
    img = img.rotate(-90).resize((500, 400))
    ph = ImageTk.PhotoImage(img)
    label = Label(window, image=ph)
    label.place(x=50, y=100)

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

        img2 = Image.open("images/white.png")
        img2 = img2.resize((500, 400))

        if not mass:
            redactor = ImageDraw.Draw(img2)
            redactor.text(
                (50, 100),
                "   Ноты не \nпереводятся",
                fill=(0, 0, 0),
                font=ImageFont.truetype("Fonts\Jost-Italic.ttf", 70),
            )
        else:
            img2 = draw_tabs(img2, mass)

        image_tabs = img2
        p = ImageTk.PhotoImage(img2)
        label = Label(window, image=p)
        label.place(x=650, y=100)
    window.mainloop()


def Save(event):
    global image_tabs
    directory = tkinter.filedialog.askdirectory(title="Открыть папку", initialdir="/")
    os.chdir(directory)
    cv2.imwrite("tabs.jpg", numpy.array(image_tabs))

    window.mainloop()


def wrong_type():
    img2 = Image.open("images/white.png")
    img2 = img2.resize((500, 400))

    redactor = ImageDraw.Draw(img2)
    redactor.text(
        (20, 100),
        "Неправильный\nформат данных",
        fill=(0, 0, 0),
        font=ImageFont.truetype("Fonts\Jost-Italic.ttf", 70),
    )

    image_tabs = img2
    p = ImageTk.PhotoImage(img2)
    label = Label(window, image=p)
    label.place(x=650, y=100)
    window.mainloop()


def main():
    window.title("PITA")  # creating an application window
    window.geometry("1200x700")
    window.configure(bg="#172A2A")
    window.resizable(width=False, height=False)
    window.iconbitmap("images/Logo.ico")

    btn_choice = Button(
        window,  # creating a file selection button
        text="Выбрать файл",
        width=30,
        height=5,
        bg="#836B3C",
        fg="black",
    )
    btn_choice.bind("<Button-1>", Conversion)
    btn_choice.place(x=295, y=590)

    btn_save = Button(
        window,  # creating a tab save button
        text="Сохранить табы",
        width=30,
        height=5,
        bg="#836B3C",
        fg="black",
    )
    btn_save.bind("<Button-1>", Save)
    btn_save.place(x=685, y=590)

    window.mainloop()


if __name__ == "__main__":
    main()
