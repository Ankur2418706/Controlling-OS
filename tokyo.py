import streamlit as st
import speech_recognition as sr
import pyttsx3 as pytt
import datetime
import threading
import time
import webbrowser

# ---------------- GLOBAL VARIABLES ----------------
running = False
last_text = ""
response_text = ""
status = "Idle"

# ---------------- SAFE TTS FUNCTION ----------------
def speak(text):
    try:
        engine = pytt.init()   # reinitialize every time (fixes no-sound bug)
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)
        engine.setProperty('rate', 150)

        engine.say(text)
        engine.runAndWait()
        engine.stop()

    except Exception as e:
        print("TTS Error:", e)

# ---------------- COMMAND LOGIC ----------------
def process_command(command):
    command = command.lower().strip()

    if "hello" in command:
        return "Hello! How are you?"

    elif "good" in command:
        return "Nice to hear that."

    elif "about you" in command:
        return "I am also fine."

    elif "old" in command:
        return "age is just a number."

    elif "can you do" in command:
        return "I am at my initial phase, so i can do basic things like opening browser, telling date and time etc."

    elif "your name" in command:
        return "I am TOKYO, your assistant."

    elif "time" in command or "date" in command:
        now = datetime.datetime.now()
        time_str = now.strftime("%H:%M")
        date_str = now.strftime("%d %B %Y")

        return f"Current time is {time_str} and today's date is {date_str}"

    elif "open browser" in command or "open google" in command:
        webbrowser.open("https://www.google.com")
        return "Opening Google in your browser"

    elif "open youtube" in command:
        webbrowser.open("https://www.youtube.com")
        return "Opening YouTube"

    elif "open chat gpt" in command:
        webbrowser.open("https://chat.openai.com")
        return "Opening ChatGPT"

    elif "stop" in command:
        return "Stopping assistant." 

    else:
        return f"{command}"

# ---------------- LISTEN FUNCTION ----------------
def listen_loop():
    global running, last_text, response_text, status

    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 300
    recognizer.dynamic_energy_threshold = True

    mic = sr.Microphone()

    with mic as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)

    while running:
        try:
            status = "🎤 Listening..."

            with mic as source:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)

            command = recognizer.recognize_google(audio).lower()

            last_text = command

            response = process_command(command)
            response_text = response

            speak(response)

            if "stop" in command:
                running = False

        except sr.WaitTimeoutError:
            status = "⏳ No speech detected"

        except sr.UnknownValueError:
            status = "❌ Could not understand"

        except Exception as e:
            status = f"Error: {e}"

# ---------------- STREAMLIT UI ----------------
st.set_page_config(page_title="TOKYO Assistant", page_icon="🤖")

st.title("TOKYO: VOICE ASSISTANT")

col1, col2 = st.columns(2)

if col1.button("▶ Start"):
    if not running:
        running = True
        threading.Thread(target=listen_loop, daemon=True).start()

if col2.button("⛔ Stop"):
    running = False

# ---------------- LIVE DISPLAY ----------------
placeholder = st.empty()

while True:
    with placeholder.container():
        st.info(status)
        st.write("🗣 You said:", last_text)
        st.success("🤖 Response: " + response_text)

    time.sleep(0.5)





    