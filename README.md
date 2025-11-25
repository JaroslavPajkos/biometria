PROJEKT HLASOVEJ AUTENTIFIKACIE
===============================

Tento projekt obsahuje dva Python skripty urcene na autentifikaciu pomocou hlasu a frazy.

1. voice_biometric_auth_soft.py  – kombinovana autentifikacia hlas + fraza
2. voice_phrase_compare.py       – autentifikacia len pomocou frazy


POZADOVANA VERZIA PYTHONU
-------------------------
Python 3.11.x (64-bit)


POVINNE KNIZNICE A ICH VERZIE
-----------------------------

Pre voice_biometric_auth_soft.py:
    SpeechRecognition 3.14.3
    pyttsx3 2.99
    sounddevice 0.5.1
    soundfile 0.13.1
    numpy 1.26.4
    Resemblyzer 0.1.4
    PyAudio (pre vstup z mikrofonu)

Pre voice_phrase_compare.py:
    SpeechRecognition 3.14.3
    pyttsx3 2.99
    PyAudio


AKO NAINSTALOVAT KNIZNICE
-------------------------
Spusti v CMD alebo PowerShell:

    pip install SpeechRecognition pyttsx3 sounddevice soundfile numpy Resemblyzer pyaudio

Ak instalacia PyAudio zlyha (bezne na Windows):

    pip install pipwin
    pipwin install pyaudio


POPIS SKRIPTOV
--------------

1. voice_biometric_auth_soft.py
   - nahrava referencnu frazu
   - ulozi ju do WAV suboru
   - vytvori hlasovy odtlacok pomocou Resemblyzer
   - pri overeni porovna:
        (a) text frazy
        (b) podobnost hlasu
   - pristup povoli iba ak obidve podmienky sedia

2. voice_phrase_compare.py
   - jednoduchy system
   - zaregistruje frazu
   - pyta pouzivatela aby ju opakoval
   - porovnava rozpoznany text
   - autentifikacia prebehne uspechom len pri zhode


AKO SPUSTIT SKRIPTY
-------------------

Biometria + fraza:

    python voice_biometric_auth_soft.py

Len fraza:

    python voice_phrase_compare.py


VYSTUPNE SUBORY
----------------
Skript voice_biometric_auth_soft.py vytvara:

    ref_phrase.wav
    test_phrase.wav

Tieto subory sa pri dalsom spusteni prepisu.


NASTAVENIA MIKROFONU VO WINDOWS
-------------------------------
Ak ma system problem s nahravanim:

1. Otevri:
       Ovladaeci panel -> Zvuk -> Zaznam
2. Nastav predvoleny mikrofon na:
       16000 Hz, Mono
3. Vypni moznost:
       "Povolit aplikaciam prevziat vyhradnu kontrolu nad zariadenim"
4. Skontroluj hlasitost mikrofonu


CASTE CHYBY A RIESENIA
----------------------

Chyba: "No module named ..."
Riesenie: Instaluj kniznice v ramci Python 3.11:

    C:\Users\jaros\AppData\Local\Programs\Python\Python311\python.exe -m pip install <balik>

Chyba: "Could not understand audio"
Riesenie: hovorit jasnejsie, kludne zvysit cas nahravania.

Chyba: "No default output device"
Riesenie: aktualizovat ovladace alebo spravne nastavit mikrofon.


KONIEC README
