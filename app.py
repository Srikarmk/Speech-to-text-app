from tkinter import *
def rec():
    import sounddevice as sd
    import queue
    import soundfile as sf             
    import threading
    from tkinter import messagebox

    voice_rec = Tk()
    voice_rec.geometry("360x200")
    voice_rec.title("Speech Recorder")
    voice_rec.config(bg="#F6E4D1")
    q = queue.Queue()
    recording = False
    file_exists = False


    def callback(indata, frames, time, status):
        q.put(indata.copy())

    def threading_rec(x):
        if x == 1:
            t1=threading.Thread(target= record_audio)
            t1.start()
        elif x == 2:
            global recording
            recording = False
            messagebox.showinfo(message="Recording finished")
        elif x == 3: 
            if file_exists:
                data, fs = sf.read("trial.wav", dtype='float32') 
                sd.play(data,fs)
                sd.wait()
            else:

                messagebox.showerror(message="Record something to play")


    def record_audio():
        global recording 
        recording= True   
        global file_exists 
        messagebox.showinfo(message="Recording Audio. Speak into the mic")
        with sf.SoundFile("trial.wav", mode='w', samplerate=44100,channels=2) as file:
                with sd.InputStream(samplerate=44100, channels=2, callback=callback):
                    while recording == True:
                        file_exists =True
                        file.write(q.get())

        

    title_lbl  = Label(voice_rec, text="Speech recorder", bg="#F6E4D1",font=(22)).grid(row=0, column=0, columnspan=3)
    record_btn = Button(voice_rec, text="Record Audio",command=lambda m=1:threading_rec(m))
    stop_btn = Button(voice_rec, text="Stop Recording",command=lambda m=2:threading_rec(m))

    play_btn = Button(voice_rec, text="Play Recording",command=lambda m=3:threading_rec(m))


    record_btn.grid(row=1,column=0)
    stop_btn.grid(row=1,column=1)
    play_btn.grid(row=1,column=2)
    voice_rec.mainloop()

def txt():
    import speech_recognition as sr

    r = sr.Recognizer()

    with sr.AudioFile('trial.wav') as source:
        audio_text = r.listen(source)
        try:
            text = r.recognize_google(audio_text)
            print('Converting audio transcripts into text ...')
            print(text)
        except:
            print('Internet connection needed...')


def visual():
    import matplotlib.pyplot as plt
    import numpy as np
    import wave

    def visualize(path: str):
        raw = wave.open(path)
        signal = raw.readframes(-1)
        signal = np.frombuffer(signal, dtype="int16")
        f_rate = raw.getframerate()
        time = np.linspace(0, len(signal) / f_rate, num=len(signal))
        plt.figure(1)
        plt.title("Sound Wave")
        plt.xlabel("Time")
        plt.plot(time, signal)
        plt.show()

    if __name__ == "__main__":

        path = "P:/Project pbl/trial.wav"

        visualize(path)

def spect():
    # for data transformation
    import numpy as np
    # for visualizing the data
    import matplotlib.pyplot as plt
    # for opening the media file
    import scipy.io.wavfile as wavfile
    Fs, aud = wavfile.read('output.wav')
    # select left channel only
    aud = aud[:, 0]
    # trim the first 125 seconds
    first = aud[:int(Fs * 125)]
    powerSpectrum, frequenciesFound, time, imageAxis = plt.specgram(first, Fs=Fs)
    plt.show()


rec()
txt()
visual()
spect()