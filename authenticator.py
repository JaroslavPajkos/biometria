# voice_biometric_auth_soft.py
# ----------------------------
# This script performs both phrase and voice-based authentication.
# It guides the user with voice and text and uses a more tolerant voice similarity threshold.
# Fixed version (no freezing) — saves audio to WAV files before processing.

import sounddevice as sd
import soundfile as sf
import numpy as np
import time
import speech_recognition as sr
import pyttsx3
from resemblyzer import VoiceEncoder, preprocess_wav

# Initialize global components
encoder = VoiceEncoder()
engine = pyttsx3.init()
recognizer = sr.Recognizer()

# ===================== Utility Functions =====================

def speak(text):
    """Say and print text simultaneously."""
    print(f"🔊 {text}")
    engine.say(text)
    engine.runAndWait()

def record_audio_to_file(filename="recording.wav", seconds=3, samplerate=16000):
    """Record audio and save it to a WAV file."""
    speak(f"Recording will start in 2 seconds. Get ready.")
    time.sleep(2)
    print(f"🎙️ Recording for {seconds} seconds...")
    speak("Recording now. Please say your phrase clearly.")
    audio = sd.rec(int(samplerate * seconds), samplerate=samplerate, channels=1, dtype='float32')
    sd.wait()
    sf.write(filename, audio, samplerate)
    print(f"✅ Recording saved as {filename}.")
    return filename

def recognize_text_from_file(filename, lang="en-US"):
    """Recognize spoken text from a WAV file."""
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio, language=lang)
            print(f"🗣️ Recognized text: {text}")
            return text.lower().strip()
        except sr.UnknownValueError:
            speak("I couldn't understand you. Please say it again.")
            print("⚠️ Speech not recognized.")
            return None
        except sr.RequestError:
            speak("Speech recognition service error.")
            print("❌ Recognition service error.")
            return None

# ===================== Main Program =====================

def main():
    speak("Welcome to the voice and phrase authentication system.")
    print("===============================================")
    print("STEP 1: Registration - say your authentication phrase once.")
    print("STEP 2: Verification - repeat it until both text and voice match.")
    print("===============================================")
    time.sleep(2)

    # --------- REGISTRATION PHASE ---------
    while True:
        speak("Please say your authentication phrase now.")
        ref_file = record_audio_to_file("ref_phrase.wav", seconds=3)
        ref_text = recognize_text_from_file(ref_file)
        if ref_text:
            speak(f"You registered the phrase: {ref_text}")
            print(f"📝 Registered phrase: '{ref_text}'")
            break
        else:
            speak("Let's try again to register your phrase.")

    ref_emb = encoder.embed_utterance(preprocess_wav(ref_file))
    speak("Your voice and phrase have been registered successfully.")
    time.sleep(1)

    # --------- AUTHENTICATION PHASE ---------
    voice_threshold = 0.65  # lower = more tolerant

    while True:
        speak("Now say your authentication phrase to verify your identity.")
        test_file = record_audio_to_file("test_phrase.wav", seconds=3)
        test_text = recognize_text_from_file(test_file)
        if not test_text:
            continue

        test_emb = encoder.embed_utterance(preprocess_wav(test_file))
        voice_similarity = np.inner(ref_emb, test_emb)
        text_match = (ref_text == test_text)

        print("\n🔍 Comparing results...")
        print(f"🗣️ Phrase match: {text_match}")
        print(f"🎧 Voice similarity: {voice_similarity:.3f} (threshold: {voice_threshold})")

        if text_match and voice_similarity > voice_threshold:
            speak("Authentication successful. Access granted.")
            print("✅ Authentication successful. The phrase and voice match.")
            break
        elif not text_match:
            speak("The phrase does not match. Please say the same words again.")
            print("❌ Phrase does not match.")
        else:
            speak("Voice mismatch. Please repeat the phrase.")
            print("❌ Voice similarity too low.")
        time.sleep(3)

if __name__ == "__main__":
    main()
