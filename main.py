from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from plyer import audio
from time import sleep
from google_speech import transcribe_file

Builder.load_string('''
<RecordRecognize>:
    orientation: 'vertical'
    spacing: 10
    padding: 10
    Label:
        text: root.text
    
    Button:
        id: rec
        text: Record
        on_release: root.record()

''')


class RecordRecognize(BoxLayout):
    text = StringProperty('')

    def record(self):
        audio.start()
        sleep(6)
        audio.stop()
        self.recognize()

    def recognize(self):
        self.text = transcribe_file('/sdcard/testrecorder.3gp')


class RecApp(App):
    def build(self):
        return RecordRecognize()


RecApp().run()
