# voice_phrase_compare.py
# --------------------
# This script registers a spoken authentication phrase once,
# then repeatedly asks the user to say it again until it matches.
#
# Required libraries: SpeechRecognition, pyttsx3, pyaudio, time

import speech_recognition as sr
import pyttsx3
import time
import sys

def speak(text):
    """Convert text to speech."""
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def countdown(seconds):
    """Show a visible countdown before recording."""
    for i in range(seconds, 0, -1):
        sys.stdout.write(f"\r⏳ Recording in {i}...")
        sys.stdout.flush()
        time.sleep(1)
    print("\r🎙️ Start speaking now!                ")

def record_phrase(prompt, delay=2):
    """Record user's speech after a short countdown and return recognized text."""
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    while True:
        speak(prompt)
        print(f"\n🟢 {prompt}")
        countdown(delay)

        with mic as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio, language="en-US")
            print("🗣️ Recognized text:", text)
            return text.lower().strip()

        except sr.UnknownValueError:
            speak("I couldn't understand you. Please say it again.")
            print("⚠️ Could not understand the audio. Let's try again.")
            time.sleep(1)

        except sr.RequestError:
            speak("Error with the recognition service.")
            print("❌ Recognition service error. Retrying...")
            time.sleep(2)

def main():
    speak("Let's register your authentication phrase.")
    print("===============================================")
    print("STEP 1: Registration - say your authentication phrase once.")
    print("STEP 2: Verification - repeat it until it matches.")
    print("===============================================")
    time.sleep(1)

    # Register phrase once
    ref_text = record_phrase("Please say your authentication phrase now.", delay=2)
    speak("Your authentication phrase has been registered.")
    print(f"\n📝 Registered phrase: '{ref_text}'")

    # Infinite authentication loop
    while True:
        time.sleep(1)
        test_text = record_phrase("Now say your authentication phrase to verify.", delay=2)

        print("\n🔍 Comparing phrases...")
        if ref_text == test_text:
            print("✅ Authentication successful. The phrases match.")
            speak("Authentication successful. Access granted.")
            break
        else:
            print("❌ Authentication failed. The phrases do not match.")
            speak("Authentication failed. Please try again.")

            print("\n🔁 Waiting before next attempt...")
            time.sleep(3)

if __name__ == "__main__":
    main()
