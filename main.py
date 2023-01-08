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

pdf_path = None
language = 'en'

root = tk.Tk()
style = ttk.Style("litera")
root.wm_iconbitmap('favicon.ico')
root.geometry("620x350")  # Size of the window
root.title('Text Reader')

# Wczytaj zdjęcie
image = Image.open('Text_Reader_background.png')
# Przekonwertuj zdjęcie na obiekt PhotoImage
image = ImageTk.PhotoImage(image)

# Utwórz widget Label z zdjęciem
label = ttk.Label(root, image=image)

# Wyświetl widget Label
label.pack()


def upload_image():
    global pdf_path
    pdf_path = filedialog.askopenfilename(initialdir=os.getcwd())
    print(pdf_path)


def check_type_start():
    selected = choose_type.get()

    if selected == 'PDF':
        pdf_doc()
    elif selected == 'Text':
        text_doc()
    else:
        pass




# Funkcja obsługi zdarzenia
def on_choose_type_select(event):
    # Pobierz aktualnie wybraną opcję
    selected = choose_type.get()

    # Jeśli opcja to 'PDF', umożliw kliknięcie przycisku
    if selected == 'PDF':
        btn_select_image['state'] = 'normal'
        enter_text.delete(0, tk.END)
        enter_text['state'] = 'disabled'
    elif selected == 'Text':
        enter_text['state'] = 'normal'
        enter_text.insert(0, 'Enter Text')
        btn_select_image['state'] = 'disabled'
    # W przeciwnym razie deaktywuj przycisk
    else:
        btn_select_image['state'] = 'disabled'
        enter_text['state'] = 'disabled'


def on_choose_language_select(event):
    global language
    language = choose_language.get()

def clear_entry(event):
    enter_text.delete(0, 'end')


def text_doc():

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
    pygame.init()
    pygame.mixer.init()
    with open(pdf_path, 'rb') as f:
        # Wczytaj plik PDF
        pdf_reader = PyPDF2.PdfReader(f)
        # Pobierz wszystkie arkusze
        pages = pdf_reader.pages
        # Utwórz tekst z wszystkich arkuszy
        text = ''
        for page in pages:
            text += page.extract_text()
        # Utwórz obiekt gTTS z tekstem
        tts = gTTS(text, lang=language)
        # Zapisz mowę syntetyczną do pliku MP3
        # tts.save('document.mp3')
        mp3_fo = BytesIO()
        tts.write_to_fp(mp3_fo)
        pygame.mixer.music.load(mp3_fo, 'mp3')
        pygame.mixer.music.play()


# Stwórz obiekt Combobox z dwoma opcjami: 'pdf' i 'mój własny tekst'
choose_type = ttk.Combobox(root, values=['PDF', 'Text'], state='readonly')
choose_type.set('Choose Type')
# choose_type.pack(side=LEFT, padx=5, pady=10)
choose_type.place(x=5, y=275)

# Nasłuchuj zdarzenia <<ComboboxSelected>>
choose_type.bind("<<ComboboxSelected>>", on_choose_type_select)


choose_language = ttk.Combobox(root, values=['en', 'de', 'fr', 'pl', 'es'], state='readonly')
choose_language.set('Choose Language')
choose_language.place(x=160, y=275)

# Nasłuchuj zdarzenia <<ComboboxSelected>>
choose_language.bind("<<ComboboxSelected>>", on_choose_language_select)


enter_text = ttk.Entry(width=30, bootstyle="info", state='disabled')
enter_text.place(x=315, y=275)
enter_text.bind('<Button-1>', clear_entry)


btn_select_image = ttk.Button(root, text="Select Image", width=12, bootstyle=SUCCESS, state='disabled', command=upload_image)
btn_select_image.place(x=515, y=275)


b1 = ttk.Button(root, text="START", bootstyle=SUCCESS, command=check_type_start, width=20)
b1.place(x=5, y=310)


b2 = ttk.Button(root, text="STOP", bootstyle=(DANGER, OUTLINE), command=pdf_doc, width=20)
b2.place(x=160, y=310)

root.mainloop()
