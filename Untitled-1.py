


import pyttsx3

engine = pyttsx3.init()

engine.setProperty("rate", 150)
engine.setProperty("volume", 1.0)

print("Voice test starting...")

engine.say("Hello Paresh. This is Jarvis voice test.")

engine.runAndWait()

print("Voice test completed.")