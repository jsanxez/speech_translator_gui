import tkinter as tk
import threading
import pyaudio
import wave
import time
import speech_recognition as sr
# pdf
from reportlab.pdfgen import  canvas
from reportlab.lib.pagesizes import A4
# Open
from tkinter import filedialog
# Save
from tkinter.filedialog import asksaveasfile


class App():
    chunk = 1024 
    sample_format = pyaudio.paInt16 
    channels = 2
    fs = 44100  
    r = sr.Recognizer()
    file_path = ""
    
    frames = []  
    def __init__(self, master):
        self.isrecording = False

        # nested frames
        self.frame1 = tk.Frame(main)

        self.button1 = tk.Button(main, text='Grabar', bg='blue', fg='white', command=self.startrecording)
        self.button2 = tk.Button(main, text='Detener', bg='red', fg='black', command=self.stoprecording)
        self.l1 = tk.Label(self.frame1, text="Documento de salida (.pdf): ")
        self.btn_explorer = tk.Button(self.frame1, text='Guardar como...', command=self.save_file)
        # check
        self.state_var = tk.IntVar()
        self.audio_state = tk.Checkbutton(main, text=" Guardar audio?", variable=self.state_var)
        self.entry_s = tk.Text(main, height= 5, width=50, wrap="word")
        self.l2 = tk.Label(main, text="Asunto de la reunión: ")
        self.l3 = tk.Label(main, text="Estado...")
        
        self.l1.pack(side=tk.LEFT)
        self.l1.pack(padx=10, pady=5)
        self.btn_explorer.pack(side=tk.RIGHT)
        self.btn_explorer.pack(padx=10, pady=5)
        # nested frame
        self.frame1.pack(side=tk.TOP)

        #check
        self.audio_state.pack(padx=10, pady=5)

        self.l2.pack(padx=10, pady=5)
        self.entry_s.pack(padx=10, pady=5)

        self.button1.pack(side=tk.LEFT)
        self.button1.pack(padx=70, pady=5)

        self.button2.pack(side=tk.RIGHT)
        self.button2.pack(padx=70, pady=5)

        self.l3.pack(padx=5, pady=5)

    def startrecording(self):
        self.p = pyaudio.PyAudio()  
        self.stream = self.p.open(format=self.sample_format,channels=self.channels,rate=self.fs,frames_per_buffer=self.chunk,input=True)
        self.isrecording = True

        #self.filename = self.filename_entry.get()
        self.filename = self.file_path
        print(f"Nombre y ruta del archivo pdf(fuera de la funcion): {self.file_path}\n")
        #self.filename = self.filename + ".txt"

        # Guardando hora de inicio:
        with open(self.file_path, 'w') as outfile:
            outfile.write(time.strftime("Hora inicio: %d-%M-%Y %H:%M:%S\n"))
        
        print('Recording')
        self.l3.configure(text="Grabando...")
        t = threading.Thread(target=self.record)
        t.start()

    def stoprecording(self):
        self.isrecording = False
        print('recording complete')
        self.l3.configure(text="Finalizado.")
        self.filename = self.file_path
        #self.filename = self.filename + ".txt"

        self.audioname = time.strftime("reunion_%d-%M-%Y_%H_%M_%S")
        self.audioname = self.audioname + ".wav"
        wf = wave.open(self.audioname, 'wb')

        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(self.sample_format))
        wf.setframerate(self.fs)
        wf.writeframes(b''.join(self.frames))
        wf.close()

        #---- inicio de la supuesta funcion
        recorded_audio = sr.AudioFile(self.audioname)
        with recorded_audio as source:
            audio = self.r.record(source)
            try:
                text = self.r.recognize_google(audio, language='es-ES')
                with open(self.filename, 'a') as outfile:
                    outfile.write(text)
                    outfile.write(time.strftime("\nHora final: %d-%M-%Y %H:%M:%S"))
            except:
                self.l3.configure(text="Error en el reconocimiento!")
        #---- fin de la supuesta funcion

        #main.destroy()

    def record(self):
        while self.isrecording:
            data = self.stream.read(self.chunk)
            self.frames.append(data)

    def browser_files(self):
        filename = filedialog.askopenfilename(
                initialdir = ".",
                title = "Select a file",
                filetypes = (("PDF files",
                ".pdf"),
                ("all files",
                "*.*")))

    def save_file(self):
        files = [("All files", "*.*"),
                ("PDF Files", "*.pdf"),
                ("Text Document", "*.txt")]
        file = asksaveasfile(filetypes = files, defaultextension=files)
        file_path = file.name
        print(f"Nombre y ruta del archivo dentro de la funcion: {file_path}")



main = tk.Tk()
main.title('Speech Translator')
main.geometry('600x250')

app = App(main)
main.mainloop()

c = canvas.Canvas("hola_mundo.pdf", pagesize=A4)
c.drawString(0, 830, "Hola, mundo!")
c.save()
