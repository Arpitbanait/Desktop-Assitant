import sys
import speech_recognition as sr
import webbrowser
import pyttsx3
from openai import OpenAI

import files_extensions
import musiclib
import shutil
import time
import requests
from gtts import gTTS
from playsound import playsound
import os
import subprocess
import google.generativeai as genai
import asyncio
from bleak import BleakClient,BleakScanner

API_KEY ='AIzaSyBaM2lM-ZXvKVY1-W4tnLbyxIg66iYD6yo'
genai.configure(api_key=API_KEY)

model =genai.GenerativeModel("gemini-2.0-flash")



clipboard_content = None

recognizer = sr.Recognizer()
engine = pyttsx3.init()


def speak(text):

    tts = gTTS(text=text, lang='en')
    filename = "voice.mp3"
    tts.save(filename)
    playsound(filename)
    time.sleep(0.5)
    os.remove(filename)

def file_assistant(command):
    command = command.lower()
    words = command.split()
    file_index = words.index('file')
    file_extype = words[file_index - 1]
    filename = words[-1]
    newfilename = filename + "." + files_extensions.file_types[file_extype]
    if 'create' in command and 'file' in command:

        open( newfilename,'w').close()
        speak(f'File {newfilename} created successfully.')

    elif 'delete' in command and 'file' in command:

        if os.path.exists(newfilename):
            os.remove(newfilename)
            speak(f'File {newfilename} has been deleted.')
        else:
            speak(f'File {newfilename} not found.')

    elif 'read' in command and 'file' in command:

        if os.path.exists(newfilename):
            with open(newfilename, 'r') as f:
                content = f.read() or 'The file is empty.'
            speak(f'Reading file {newfilename}. {content}')
        else:
            speak(f'File {newfilename} not found.')

    elif 'copy' in words:
        global clipboard_content
        if os.path.exists(newfilename):
            with open(newfilename, 'r') as file:
                clipboard_content = file.read()
            speak(f"Content from {newfilename} copied successfully.")
        else:
            speak(f"File {newfilename} not found.")

    elif 'paste' in words:

        file2ind = words.index('to')
        newfile = words[file2ind + 1]
        newfilename2 = newfile + '.'+ filename
        with open(newfilename2, 'w') as file:
            file.write(clipboard_content)

        speak(f"Content pasted successfully into {newfilename2}.")
    else:
        speak("Please use 'paste file' properly.")










def aiprocess(command):
    API_KEY = 'AIzaSyBaM2lM-ZXvKVY1-W4tnLbyxIg66iYD6yo'
    genai.configure(api_key=API_KEY)

    model = genai.GenerativeModel("gemini-1.5-flash")
    chat = model.start_chat()
    response=chat.send_message(command)
    print(response.text)
    speak(response.text)



def search_and_open_folder(folder_name, root_paths=['C:\\', 'D:\\','F:\\']):
    for root in root_paths:
        for dirpath, dirnames, filenames in os.walk(root):
            if folder_name.lower() in [d.lower() for d in dirnames]:
                target_path = os.path.join(dirpath, folder_name)
                os.startfile(target_path)
                speak(f"Opened {folder_name} at {target_path}.")
                return
    speak(f"Folder {folder_name} not found on your system.")


def open_folder(command):
    words = command.lower().split()
    if 'folder' in words:
        folder_index = words.index('folder')
        folder_name = words[folder_index + 1]
        search_and_open_folder(folder_name)
    else:
        speak("I didn't understand which folder to open.")


def processcommand(c):

    if "file" in c.lower():
        file_assistant(c)
    elif "open" in c.lower():
              website = c.lower().split(" ")[-1]
              webbrowser.open(f"https://{website}.com")


    elif "folder" in c.lower():
        folder_name = c.lower().split(" ")[-1]
        open_folder(folder_name)

    elif c.lower().startswith("play"):
        song  = c.lower().split(" ")[1]
        link =  musiclib.music[song]
        webbrowser.open(link)

    elif "stop" in c.lower():
        sys.exit()

    elif "news" in c.lower():

        url = 'https://newsapi.org/v2/top-headlines?country=us&apiKey=1aa60c858d344b8db9eeeabbf5881d5f'
        response = requests.get(url)
        data = response.json()

        for article in data['articles']:
            print(article['title'])
            speak(article['title'])

    elif "weather" in c.lower():

        city = c.lower().split(" ")[-1]
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=bf0e59aac8eccd0e0c6ec7b54cbdc97c"


        response = requests.get(url)
        data = response.json()


        temp_min_kelvin = data['main']['temp_min']
        temp_max_kelvin = data['main']['temp_max']
        wind_speed = data['wind']['speed']


        temp_min_celsius = temp_min_kelvin - 273.15
        temp_max_celsius = temp_max_kelvin - 273.15
        weather_description = data['weather'][0]['description']

        print(f"Weather Condition: {weather_description.capitalize()}")
        speak(f"Weather Condition: {weather_description.capitalize()}")
        print(f"Minimum Temperature: {temp_min_celsius:.2f}°C")
        speak(f"Minimum Temperature: {temp_min_celsius:.2f}°C")
        print(f"Maximum Temperature: {temp_max_celsius:.2f}°C")
        speak(f"Maximum Temperature: {temp_max_celsius:.2f}°C")
        print(f"Wind Speed: {wind_speed} meters per second")
        speak(f"Wind Speed: {wind_speed} meters per second")




    else:

        aiprocess(c)

if __name__ == "__main__":
    speak("Initializing Nova.... ")
    while True:
        r= sr.Recognizer()

        print("recognizing..!")
        try:
            with sr.Microphone() as source:
                print("Listening..!")
                audio = r.listen(source,timeout = 2 ,phrase_time_limit=3)
                word = r.recognize_google(audio)
                if(word.lower() == "nova"):
                   speak("Hello Arpit")
                   with sr.Microphone() as source:
                       print("Nova Active..")
                       audio = r.listen(source)
                       command = r.recognize_google(audio)

                   processcommand(command)

        except Exception as e:
            print("Error; {0}".format(e))






