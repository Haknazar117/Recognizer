import time
import speech_recognition as sr
from jnius import autoclass

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
    MediaRecorder = autoclass('android.media.MediaRecorder')
    AudioSource = autoclass('android.media.MediaRecorder$AudioSource')
    OutputFormat = autoclass('android.media.MediaRecorder$OutputFormat')
    AudioEncoder = autoclass('android.media.MediaRecorder$AudioEncoder')
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mRecorder = self.MediaRecorder()
        self.mRecorder.setAudioSource(AudioSource.MIC)
        self.mRecorder.setOutputFormat(OutputFormat.MPEG_3)
        self.mRecorder.setOutputFile('/sdcard/testrecorder.3gp')
        self.mRecorder.setAudioEncoder(AudioEncoder.AMR_NB)
        self.mRecorder.prepare()
    
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
