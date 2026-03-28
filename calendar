import pyttsx3
import calendar
from datetime import datetime

# ------------------ INIT SPEECH ENGINE ------------------ #


# ------------------ SPEAK FUNCTION ------------------ #
def jarvis_speak(text):
    engine = pyttsx3.init()
    engine.setProperty("rate", 170)

    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[1].id)  # Change if needed
    print(text)
    engine.say(text)
    engine.runAndWait()


month = int(input("Enter Month"))
year = int(input("Enter Year"))

cal = calendar.month(year, month)

print("\n" + cal)
jarvis_speak(f"SIR: Here is the calendar for {calendar.month_name[month]} {year}. Please check the screen.")
