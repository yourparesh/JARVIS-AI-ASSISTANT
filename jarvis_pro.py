import os
import webbrowser
import datetime
import requests
import speech_recognition as sr
import pyttsx3
import re
import unicodedata

from dotenv import load_dotenv
from google import genai
from groq import Groq




load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")






gemini_client = None
groq_client = None

if GEMINI_API_KEY:
    gemini_client = genai.Client(
        api_key=GEMINI_API_KEY
    )

if GROQ_API_KEY:
    groq_client = Groq(
        api_key=GROQ_API_KEY
    )





engine = pyttsx3.init()

engine.setProperty("rate", 150)
engine.setProperty("volume", 1.0)






def clean_for_voice(text):
    text = str(text)

    
    text = text.replace("’", "'")
    text = text.replace("“", '"')
    text = text.replace("”", '"')
    text = text.replace("–", "-")
    text = text.replace("—", "-")

    
    text = text.replace("**", "")
    text = text.replace("##", "")
    text = text.replace("#", "")
    text = text.replace("---", "")
    text = text.replace("|", " ")
    text = text.replace("`", "")
    text = text.replace("*", "")
    text = text.replace("_", "")

    
    text = text.encode("ascii", "ignore").decode("ascii")

    return text.strip()


def speak(text):
    print("Jarvis:", text)

    try:
        voice_text = clean_for_voice(text)

        print("Speaking:", voice_text)

        engine.stop()
        engine.say(voice_text)
        engine.runAndWait()

        print("Voice completed.")

    except Exception as e:
        print("Voice Error:", e)


def take_command():

    recognizer = sr.Recognizer()

    with sr.Microphone() as source:

        print("\nListening...")

        recognizer.adjust_for_ambient_noise(
            source,
            duration=0.5
        )

        try:

            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=10
            )

        except sr.WaitTimeoutError:

            print("No speech detected.")

            return ""


    try:

        print("Recognizing...")

        command = recognizer.recognize_google(
            audio
        )

        print("You:", command)

        return command.lower()


    except sr.UnknownValueError:

        speak(
            "Sorry, I could not understand you."
        )

        return ""


    except sr.RequestError:

        speak(
            "Speech recognition service is unavailable."
        )

        return ""



def ask_gemini(question):

    if not gemini_client:

        return None

    try:

        response = gemini_client.models.generate_content(

            model="gemini-3.6-flash",

            contents=(

                "Answer the user's question clearly and briefly. "

                "Use simple language. "

                "Give a spoken-friendly answer in maximum 5 short sentences. "

                "Do not use markdown tables, headings, bullet symbols, "

                "or unnecessary special characters. "

                "If the user asks in Marathi, answer in Marathi. "

                "If the user asks in Hindi, answer in Hindi. "

                "If the user asks in English, answer in English.\n\n"

                "User question: "

                + question
            )
        )

        return response.text


    except Exception as e:

        print(
            "Gemini Error:",
            repr(e)
        )

        return None


def ask_groq(question):

    if not groq_client:

        print("Groq client is not available.")

        return None

    try:

        response = groq_client.chat.completions.create(

            model="openai/gpt-oss-120b",

            messages=[

                {
                    "role": "system",

                    "content": (

                        "You are Jarvis, a helpful voice assistant. "

                        "Answer the user's question clearly and briefly. "

                        "Use maximum 5 short sentences. "

                        "Use simple spoken language. "

                        "Do not use markdown tables, headings, "

                        "bullet symbols, or unnecessary special characters. "

                        "If the user speaks Marathi, answer in Marathi. "

                        "If the user speaks Hindi, answer in Hindi. "

                        "If the user speaks English, answer in English."
                    )
                },

                {
                    "role": "user",

                    "content": question
                }

            ]
        )

        answer = response.choices[0].message.content

        return answer


    except Exception as e:

        print(
            "Groq Error:",
            repr(e)
        )

        return None


def ask_ai(question):

    print("\nThinking...")


    
    answer = ask_gemini(question)

    if answer:

        print("\nGemini Answer:")

        print(answer)

        return answer


    print("\nGemini unavailable.")

    print(
        "Switching to Groq backup..."
    )


    answer = ask_groq(question)

    if answer:

        print("\nGroq Answer:")

        print(answer)

        return answer


    
    return (
        "Sorry, I am unable to answer "
        "that right now."
    )


def get_weather():

    try:

        url = (
            "https://wttr.in/Pune"
            "?format=%C+%t"
        )

        response = requests.get(
            url,
            timeout=5
        )

        if response.status_code == 200:

            weather = response.text.strip()

            return (
                "The current weather in Pune is "
                + weather
            )

        return (
            "Sorry, I could not get the weather."
        )


    except Exception:

        return (
            "Sorry, weather service is unavailable."
        )



speak(
    "Hello Paresh. "
    "Jarvis is here. "
    "How can I help you?"
)


while True:

    command = take_command()

    if not command:

        continue



    if (
        "open google" in command
        or "google open" in command
    ):

        speak(
            "Opening Google"
        )

        webbrowser.open(
            "https://www.google.com"
        )

    elif (
        "open youtube" in command
        or "youtube open" in command
    ):

        speak(
            "Opening YouTube"
        )

        webbrowser.open(
            "https://www.youtube.com"
        )

    elif "time" in command:

        current_time = datetime.datetime.now().strftime(
            "%I:%M %p"
        )

        speak(
            "The current time is "
            + current_time
        )


    elif "date" in command:

        current_date = datetime.datetime.now().strftime(
            "%d %B %Y"
        )

        speak(
            "Today's date is "
            + current_date
        )


    elif (
        "weather" in command
        or "temperature" in command
        or "temp" in command
    ):

        weather_answer = get_weather()

        speak(
            weather_answer
        )


    elif (
        "exit" in command
        or "stop" in command
        or "stop it" in command
        or "goodbye" in command
        or "quit" in command
    ):

        speak(
            "Goodbye Paresh. "
            "See you later."
        )

        break


    else:

        answer = ask_ai(
            command
        )

        speak(
            answer
        )
