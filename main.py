from gtts import gTTS
from io import BytesIO
import pygame
import time
import tkinter as tk
import ttkbootstrap as ttk
import PyPDF2
from ttkbootstrap.constants import *

root = tk.Tk()
style = ttk.Style("darkly")
root.wm_iconbitmap('favicon.ico')
root.geometry("600x300")  # Size of the window
root.title('Text Reader')


def directly_sound():
    if '' == string_entry.get():
        print('pusty string')
    text = (string_entry.get())
    pygame.init()
    pygame.mixer.init()
    mp3_fo = BytesIO()
    tts = gTTS(text, lang='pl')
    tts.write_to_fp(mp3_fo)
    pygame.mixer.music.load(mp3_fo, 'mp3')
    pygame.mixer.music.play()


def pdf_doc():
    pygame.init()
    pygame.mixer.init()
    with open('document.pdf', 'rb') as f:
        # Wczytaj plik PDF
        pdf_reader = PyPDF2.PdfReader(f)
        # Pobierz wszystkie arkusze
        pages = pdf_reader.pages
        # Utwórz tekst z wszystkich arkuszy
        text = ''
        for page in pages:
            text += page.extract_text()
        # Utwórz obiekt gTTS z tekstem
        tts = gTTS(text, lang='pl')
        # Zapisz mowę syntetyczną do pliku MP3
        # tts.save('document.mp3')
        mp3_fo = BytesIO()
        tts.write_to_fp(mp3_fo)
        pygame.mixer.music.load(mp3_fo, 'mp3')
        pygame.mixer.music.play()


b1 = ttk.Button(root, text="Button 1", bootstyle=SUCCESS, command=directly_sound)
b1.pack(side=LEFT, padx=5, pady=10)


b2 = ttk.Button(root, text="Button 2", bootstyle=(INFO, OUTLINE), command=pdf_doc)
b2.pack(side=LEFT, padx=5, pady=10)

string_entry = ttk.Entry(width=32, bootstyle="info")
string_entry.pack(side=LEFT, padx=5, pady=10)


# Stwórz obiekt Combobox z dwoma opcjami: 'pdf' i 'mój własny tekst'
combo = ttk.Combobox(root, values=['PDF', 'Text'], state='readonly')
combo.set('Choose type')
combo.pack()


root.mainloop()
