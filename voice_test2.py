import asyncio
import edge_tts

async def speak(text):
    voice = "en-US-GuyNeural"
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save("jarvis_voice.mp3")

asyncio.run(speak("Hello sir, I am Jarvis. How can I help you?"))