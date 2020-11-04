import time
import wave
import speech_recognition as sr
from audiostream import get_input

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

r = sr.Recognizer()

Builder.load_string('''
<Recorder>:
    orientation: 'vertical'
    Label:
        id: text
    Button:
        id: record
        text: "Record"
        on_release: root.record_audio()

''')


class Recorder(BoxLayout):
    frames = []

    def mic_callback(self, buf):
        print('got', len(buf))
        self.frames.append(buf)

    def record_audio(self):
        microphone = get_input(callback=self.mic_callback)
        microphone.start()

        time.sleep(5)

        microphone.stop()

        wf = wave.open("test.wav", 'wb')
        wf.setnchannels(microphone.channels)
        wf.setsampwidth(2)
        wf.setframerate(microphone.rate)
        wf.writeframes(b''.join(self.frames))
        wf.close()
        self.recognize()

    def recognize(self):
        with sr.AudioFile("test.wav") as source:
            audio = r.listen(source)

        try:
            # recognize speech using Google Speech Recognition
            value = r.recognize_google(audio)
            self.ids["text"].text = str(value)

        except sr.UnknownValueError:
            self.ids["text"].text = "Oops! Didn't catch that"

        except sr.RequestError as e:
            self.ids["text"].text = "Couldn't request results from Google Speech Recognition service; {0}".format(e)


class RecordApp(App):
    def build(self):
        return Recorder()


RecordApp().run()
