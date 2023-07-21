import tkinter as tk
from tkinter import Scrollbar, Text
import threading
import speech_recognition as sr
import pyttsx3
import datetime

class VoiceAssistantApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Voice Assistant")
        self.geometry("400x400")
        self.create_widgets()

        self.assistant_active = False

    def create_widgets(self):
        self.text_display = Text(self, wrap="word")
        self.text_display.pack(fill="both", expand=True)

        self.scrollbar = Scrollbar(self.text_display)
        self.scrollbar.pack(side="right", fill="y")
        self.text_display.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.text_display.yview)

        self.start_button = tk.Button(self, text="Start", command=self.start_assistant)
        self.start_button.pack(side="left", padx=10)

        self.stop_button = tk.Button(self, text="Stop", command=self.stop_assistant)
        self.stop_button.pack(side="right", padx=10)

    def start_assistant(self):
        self.assistant_active = True
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")

        threading.Thread(target=self.run_voice_assistant).start()

    def stop_assistant(self):
        self.assistant_active = False
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")

    def speak(self, text):
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()

    def listen(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            self.add_to_display("Listening...")
            recognizer.pause_threshold = 1
            audio = recognizer.listen(source)

        try:
            self.add_to_display("Recognizing...")
            query = recognizer.recognize_google(audio, language="en-US")
            self.add_to_display(f"User: {query}\n")
            return query
        except Exception as e:
            self.add_to_display(str(e))
            return None

    def run_voice_assistant(self):
        self.add_to_display("Hello! I am your voice assistant. How can I assist you today?")
        while self.assistant_active:
            query = self.listen()

            if query:
                query = query.lower()

                if "hello" in query or "hi" in query:
                    self.add_to_display("Hello! How can I help you?")
                    self.speak("Hello! How can I help you?")
                elif "what is your name" in query:
                    self.add_to_display("I am your voice assistant.")
                    self.speak("I am your voice assistant.")
                elif "what is the time" in query:
                    now = datetime.datetime.now().strftime("%H:%M:%S")
                    self.add_to_display(f"The current time is {now}\n")
                    self.speak(f"The current time is {now}")
                elif "calculate" in query:
                    # Extract the mathematical expression from the query
                    expression = query.replace("calculate", "").strip()
                    try:
                        # Evaluate the expression using eval() and speak the result
                        result = eval(expression)
                        self.add_to_display(f"The result of {expression} is {result}\n")
                        self.speak(f"The result of {expression} is {result}")
                    except Exception as e:
                        self.add_to_display("Sorry, I couldn't perform the calculation. Please try again.\n")
                        self.speak("Sorry, I couldn't perform the calculation. Please try again.")
                elif "exit" in query or "bye" in query:
                    self.add_to_display("Goodbye!\n")
                    self.speak("Goodbye!")
                    self.stop_assistant()
                else:
                    self.add_to_display("Sorry, I didn't understand that. Can you please repeat?\n")
                    self.speak("Sorry, I didn't understand that. Can you please repeat?")

    def add_to_display(self, text):
        self.text_display.configure(state="normal")
        self.text_display.insert("end", text + "\n")
        self.text_display.see("end")
        self.text_display.configure(state="disabled")


if __name__ == "__main__":
    app = VoiceAssistantApp()
    app.mainloop()