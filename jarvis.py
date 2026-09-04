import pyttsx3

engine = pyttsx3.init()

def speak(text):
    print("Jarvis:", text)
    engine.say(text)
    engine.runAndWait()

speak("Hello sir")

speak("How are you?")

speak("I am ready to help you.")