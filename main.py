from gtts import gTTS
from io import BytesIO
import pygame
import time
import tkinter as tk
import ttkbootstrap as ttk
import PyPDF2
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox
from tkinter.filedialog import asksaveasfilename
import os
from PIL import Image, ImageTk

tts = None
pdf_path = None
language = 'en'

root = tk.Tk()
style = ttk.Style("litera")
root.wm_iconbitmap('favicon.ico')
root.geometry("620x350")  # Size of the window
root.title('Text Reader')

# Upload photo
image = Image.open('Text_Reader_background.png')
# Convert the photo to an object PhotoImage
image = ImageTk.PhotoImage(image)

# Create a Label widget with a photo
label = ttk.Label(root, image=image)

# View the Label widget
label.pack()


def upload_document():
    global pdf_path
    pdf_path = filedialog.askopenfilename(initialdir=os.getcwd())

    if pdf_path == '':
        pass
    elif os.path.splitext(pdf_path)[1] != '.pdf':
        messagebox.showinfo(title="Pdf file not detected.", message="This is not a PDF file.")
        pdf_path = None
    else:
        messagebox.showinfo(title="Success", message="Success file uploaded.")


def check_type_start():
    selected = choose_type.get()
    btn_pause['text'] = 'PAUSE'

    if selected == 'PDF':
        pdf_doc()
    elif selected == 'Text':
        text_doc()
    else:
        messagebox.showinfo(title="Choose Type", message="Choose type: Text or PDF.")


def on_choose_type_select(event):
    selected = choose_type.get()

    if selected == 'PDF':
        btn_select_document['state'] = 'normal'
        enter_text.delete(0, tk.END)
        enter_text['state'] = 'disabled'
    elif selected == 'Text':
        enter_text['state'] = 'normal'
        enter_text.insert(0, 'Enter Text')
        btn_select_document['state'] = 'disabled'
    else:
        btn_select_document['state'] = 'disabled'
        enter_text['state'] = 'disabled'


def on_choose_language_select(event):
    global language
    language = choose_language.get()


def clear_entry(event):
    if enter_text.get() == 'Enter Text':
        enter_text.delete(0, 'end')


def text_doc():
    global tts

    if '' == enter_text.get() or enter_text.get() == 'Enter Text':
        messagebox.showinfo(title="Empty filed", message="Please don't leave empty filed.")
    else:
        text = (enter_text.get())
        pygame.init()
        pygame.mixer.init()
        mp3_fo = BytesIO()
        tts = gTTS(text, lang=language)
        tts.write_to_fp(mp3_fo)
        pygame.mixer.music.load(mp3_fo, 'mp3')
        pygame.mixer.music.play()


def pdf_doc():
    global tts

    if pdf_path is None:
        messagebox.showinfo(title="Select a document", message="First select a document.")
    else:
        pygame.init()
        pygame.mixer.init()
        with open(pdf_path, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            pages = pdf_reader.pages
            text = ''
            for page in pages:
                text += page.extract_text()
            tts = gTTS(text, lang=language)
            mp3_fo = BytesIO()
            tts.write_to_fp(mp3_fo)
            pygame.mixer.music.load(mp3_fo, 'mp3')
            pygame.mixer.music.play()


def pause_unpause():

    if btn_pause['text'] == 'PAUSE':
        pygame.mixer.music.pause()
        btn_pause['text'] = 'UNPAUSE'
    else:
        pygame.mixer.music.unpause()
        btn_pause['text'] = 'PAUSE'


def reset():
    global pdf_path, tts
    pygame.mixer.music.stop()
    btn_pause['text'] = 'PAUSE'
    pdf_path = None
    enter_text.delete(0, 'end')
    tts = None


def save():
    if tts is not None:
        filename = filedialog.asksaveasfilename(initialdir=os.getcwd())
        if filename:
            tts.save(f'{filename}.mp3')
    else:
        messagebox.showinfo(title="Start", message="Press first start.")


choose_type = ttk.Combobox(root, values=['PDF', 'Text'], state='readonly', width=20)
choose_type.set('Choose Type')
choose_type.place(x=5, y=275)
choose_type.bind("<<ComboboxSelected>>", on_choose_type_select)


choose_language = ttk.Combobox(root, values=['en', 'de', 'fr', 'pl', 'es'], state='readonly', width=20)
choose_language.set('Choose Language')
choose_language.place(x=160, y=275)
choose_language.bind("<<ComboboxSelected>>", on_choose_language_select)


enter_text = ttk.Entry(width=22, bootstyle="info", state='disabled')
enter_text.place(x=315, y=275)
enter_text.bind('<Button-1>', clear_entry)


btn_select_document = ttk.Button(root, text="Select Document", width=20, bootstyle=INFO, state='disabled',
                                 command=upload_document)
btn_select_document.place(x=470, y=275)


btn_start = ttk.Button(root, text="START", bootstyle=SUCCESS, command=check_type_start, width=20)
btn_start.place(x=5, y=310)


btn_pause = ttk.Button(root, text="PAUSE", bootstyle=(SECONDARY, OUTLINE), command=pause_unpause, width=20)
btn_pause.place(x=160, y=310)


btn_reset = ttk.Button(root, text="RESET", bootstyle=(DANGER, OUTLINE), command=reset, width=20)
btn_reset.place(x=315, y=310)


btn_save = ttk.Button(root, text="SAVE", bootstyle=(WARNING, OUTLINE), command=save, width=20)
btn_save.place(x=470, y=310)

root.mainloop()
