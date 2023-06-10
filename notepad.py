# Importing all required libraries
import tkinter as tk
from tkinter import ttk, messagebox
import json
from ttkbootstrap import Style
import speech_recognition as sr
import time


# Main Window
window = tk.Tk()
window.title("Note Taking App") 
window.geometry("500x500")
style = Style(theme="journal")
style = ttk.Style()

style.configure("TNotebook.Tab", font=("TkDefaultFont",14,"bold"))

# Setting up Notebook Widget
notebook = ttk.Notebook(window, style="TNotebook")
notebook.pack(padx=10, pady=10, fill=tk.BOTH, expan=True)

# Displaying Saved notes
notes = {}
try:
    with open("notes.json", "r") as f:
        notes = json.load(f)
except FileNotFoundError:
    pass


# Add new notes
def add_note():
    # Creating new tab for this new note
    note_frame = ttk.Frame(notebook, padding=10)
    notebook.add(note_frame, text="New Note")

    title_label = ttk.Label(note_frame, text="Title:")
    title_label.grid(row=0, column=0, padx=10, pady=10, sticky="W")

    title_entry = ttk.Entry(note_frame, width=60)
    title_entry.grid(row=0, column=1, padx=10, pady=10)

    content_label = ttk.Label(note_frame, text="Content:")
    content_label.grid(row=1, column=0, padx=10, pady=10, sticky="W")

    content_entry = tk.Text(note_frame, width=60, height=10)
    content_entry.grid(row=1, column=1, padx=10, pady=10)

    # Saving the note
    def save_note():
        title = title_entry.get()
        content = content_entry.get("1.0", tk.END)

        # adding note to the notes dict
        notes[title] = content.strip()

        # saving notes dict to the json file
        with open("notes.json", "w") as f:
            json.dump(notes, f)

        # Adding note to notebook
        note_content = tk.Text(notebook, width=40, height=10)
        note_content.insert(tk.END, content)
        notebook.forget(notebook.select())
        notebook.add(note_content, text=title)

    # Adding a save button to the note frame
    save_button = ttk.Button(note_frame, text="Save", command=save_note, style="secondary.TButton")
    save_button.grid(row=2, column=1, padx=10, pady=10)

    # Adding speech to text functionality within note frame
    def speech():

        r = sr.Recognizer()
        mic = sr.Microphone()
        with sr.Microphone() as mic:
            print("Listening...")
            audio = r.listen(mic)

        try:
            information = " " + r.recognize_google(audio)
            content_entry.insert(tk.END, information)
        except sr.UnknownValueError:
            print("Could not understand audio")
    
    # Adding Speech to text button
    speech_button = ttk.Button(note_frame, text="Speech-Text", command=speech, style="secondary.TButton")
    speech_button.grid(row=3, column=1, padx=10, pady=10)
    
# Loading notes into app everytime the program is run
def load_notes():
    try:
        with open("notes.json", "r") as f:
            notes = json.load(f)
        
        for title, content in notes.items():
            note_content = tk.Text(notebook, width=40, height=10)
            note_content.insert(tk.END, content)
            notebook.add(note_content, text=title)
    
    except FileNotFoundError:
        pass

load_notes()

# Delete a certain note
def delete_note():
    # get current tab
    current_tab = notebook.index(notebook.select())
    note_title = notebook.tab(current_tab, "text")
    
    notebook.forget(current_tab)
    notes.pop(note_title)

    with open("notes.json", "w") as f:
        json.dump(notes, f)

# Add essential buttons to main window
new_button = ttk.Button(window, text="New Note", command=add_note, style="info.TButton")
new_button.pack(side=tk.LEFT, padx=10, pady=10)

delete_button = ttk.Button(window, text="Delete", command=delete_note, style="primary.TButton")
delete_button.pack(side=tk.LEFT, padx=10, pady=10)

window.mainloop()
