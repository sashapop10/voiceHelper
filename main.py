from PyQt5.QtWidgets import QMainWindow, QTextEdit, QMenuBar, QApplication
from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal as Signal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QMainWindow, QTextEdit,
    QAction, QFileDialog, QApplication)
from PyQt5 import QtWidgets, QtGui
from tkinter import *
from tkinter import messagebox as mb
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QLabel, QApplication)
from PyQt5.QtGui import QPixmap
#-----------------------------------------------------------------------------------------------------------------------------------
import pyttsx3
import webbrowser
import smtplib
import random
import speech_recognition as sr
import wikipedia
import datetime
import wolframalpha
import os
import sys
#-----------------------------------------------------------------------------------------------------------------------------------

class OutputLogger(QObject):
    emit_write = Signal(str, int)

    class Severity:
        DEBUG = 0
        ERROR = 1

    def __init__(self, io_stream, severity):
        super().__init__()

        self.io_stream = io_stream
        self.severity = severity

    def write(self, text):
        self.io_stream.write(text)
        self.emit_write.emit(text, self.severity)

    def flush(self):
        self.io_stream.flush()


import sys
OUTPUT_LOGGER_STDOUT = OutputLogger(sys.stdout, OutputLogger.Severity.DEBUG)
OUTPUT_LOGGER_STDERR = OutputLogger(sys.stderr, OutputLogger.Severity.ERROR)

sys.stdout = OUTPUT_LOGGER_STDOUT
sys.stderr = OUTPUT_LOGGER_STDERR


class MainWindow(QMainWindow):



    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Vassistant')
        self.setGeometry(50, 50, 640, 480)


        self.label = QLabel(self)
        pixmap = QPixmap('C:/Users/sasha/Desktop/project/fon.png')
        self.label.setPixmap(pixmap)
        self.resize(pixmap.width(), pixmap.height())

        self.show()


        self.text_edit = QTextEdit()

        OUTPUT_LOGGER_STDOUT.emit_write.connect(self.append_log)
        OUTPUT_LOGGER_STDERR.emit_write.connect(self.append_log)



        self.setCentralWidget(self.text_edit)





    def append_log(self, text, severity):
        text = repr(text)

        if severity == OutputLogger.Severity.ERROR:
            self.text_edit.append('<b>{}</b>'.format(text))
        else:
            self.text_edit.append(text)


if __name__ == '__main__':
    app = QApplication([])

    mw = MainWindow()
    mw.show()




#-----------------------------------------------------------------------------------------------------------------------------------


engine = pyttsx3.init('sapi5')
client = wolframalpha.Client('Your_App_ID')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
    print('Computer: ' + audio)
    engine.say(audio)
    engine.runAndWait()

def greetMe():
    currentH = int(datetime.datetime.now().hour)
    if currentH >= 0 and currentH < 12:
        speak('???????????? ????????')

    if currentH >= 12 and currentH < 18:
        speak('???????????? ????????!')

    if currentH >= 18 and currentH != 0:
        speak('???????????? ??????????!')

greetMe()

speak('?????? ?? ???????? ?????? ?????????????')

def myCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("????????????...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        query = r.recognize_google(audio, language='ru-RU')
        print('User: ' + query + '\n')

    except sr.UnknownValueError:
        speak('???????????????? ?? ???? ???????????? ??????????????,???????????????????? ?????????????? ????!')
        query = str(input('??????????????: '))

    return query

if __name__ == '__main__':

    while True:

        query = myCommand();
        query = query.lower()

        if '???????????? youtube' in query:
            speak('????????????')
            webbrowser.open('www.youtube.com')

        elif '???????????? google' in query:
            speak('????????????')
            webbrowser.open('www.google.co.in')

        elif '???????????? ??????????' in query:
            speak('????????????')
            webbrowser.open('www.gmail.com')

        elif '???????????? ?????????????????????? ????????????' in query:
            speak('????????????')
            webbrowser.open('https://dnevnik.mos.ru/student_diary/student_diary/160377')

        elif '???????????? ????????????????????' in query:
            speak('????????????')
            os.system("C:\\Users\\sasha\\Desktop\\LESSONS.jpg")

        elif '????????' in query:
            speak('????????????')
            speak('????????????????????.')
            sys.exit()

        elif '??????????' in query:
            now = datetime.datetime.now()
            speak("???????????? " + str(now.hour) + ":" + str(now.minute))

        elif '??????????????????????' in query:
            os.system('calc')

        elif '????????' in query:
            speak('????????????????????.')
            sys.exit()
        else:
            query = query
            speak('??????????...')
            try:
                try:
                    res = client.query(query)
                    results = next(res.results).text
                    speak('WOLFRAM-ALPHA says - ')
                    speak('????????????.')
                    speak(results)

                except:
                    results = wikipedia.summary(query, sentences=2)
                    speak('????????????.')
                    speak('WIKIPEDIA ?????????????? - ')
                    speak(results)

            except:
                webbrowser.open('www.google.com')

        speak('?????????????????? ??????????????!')

#-----------------------------------------------------------------------------------------------------------------------------------

    app.exec()
