import pyttsx3
import speech_recognition as sr
import datetime
import requests

# Initialize the text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-US')
        print(f"You said: {query}")
        return query.lower()
    except Exception as e:
        print("Sorry, I could not understand.")
        return "None"

def greet_user():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good morning!")
    elif 12 <= hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")

def get_weather(city):
    api_key = ""
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(base_url).json()
    if response.get("cod") != "404":
        main = response["main"]
        temperature = main["temp"]
        weather_desc = response["weather"][0]["description"]
        return f"The temperature in {city} is {temperature} degrees Celsius with {weather_desc}."
    else:
        return "City not found."

def main():
    greet_user()
    while True:
        query = listen()

        if "weather" in query:
            speak("Which city?")
            city = listen()
            weather = get_weather(city)
            speak(weather)

        elif "time" in query:
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {current_time}")

        elif "exit" in query or "bye" in query:
            speak("Goodbye!")
            break

        else:
            speak("I didn't catch that. Can you repeat?")

if __name__ == "__main__":
    main()
