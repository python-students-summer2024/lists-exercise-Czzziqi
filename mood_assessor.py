import datetime
import os

def record_mood():
    mood_dictionary = {'happy': 2, 'relaxed': 1, 'apathetic': 0, 'sad': -1, 'angry': -2}
    date_today = datetime.date.today()
    date_today_str = str(date_today)
    while True:
        current_mood = input("Enter your current mood: ").strip().lower()
        
        if current_mood in mood_dictionary:
            mood_value = mood_dictionary[current_mood]
            
            if not os.path.exists('data'):
                os.makedirs('data')
            diary_file = 'data/mood_diary.txt'
            if not os.path.exists(diary_file):
                with open(diary_file, 'w'):
                    pass
            with open(diary_file, 'r') as fp:
                lines = fp.readlines()
                for line in lines:
                    if line.startswith(date_today_str):
                        print("Sorry, you have already entered your mood today.")
                        return False
            with open(diary_file, 'a') as fp:
                fp.write(f"{date_today_str},{mood_value}\n")
                return mood_value
        else:
            print("Invalid response! Please enter one of: happy, relaxed, apathetic, sad, angry")

def get_user_mood():
    if not record_mood():
        print("Sorry, you have already entered your mood today.")
    else:
        print("Mood recorded successfully.")

def check_entries():
    total = 0
    with open('data/mood_diary.txt', 'r') as fp:
        lines = fp.readlines()
        if len(lines) < 7:
            return None
        seven_lines = lines[-7:]
        for line in seven_lines:
            mood_value = line.split(',')[1].strip()
            total += int(mood_value)
        average = round(total / 7.0)
        return average

def check_disorders():
    with open('data/mood_diary.txt', 'r') as fp:
        happy = 0
        relaxed = 0
        apathetic = 0
        sad = 0
        angry = 0
        lines = fp.readlines()
        if len(lines) < 7:
            return None
        seven_lines = lines[-7:]
        for line in seven_lines:
            mood_value = int(line.split(',')[1].strip())
            if mood_value == 2:
                happy += 1
            elif mood_value == 1:
                relaxed += 1
            elif mood_value == 0:
                apathetic += 1
            elif mood_value == -1:
                sad += 1
            elif mood_value == -2:
                angry += 1
        
        if happy >= 5:
            return "manic"
        elif sad >= 4:
            return "depressive"
        elif apathetic >= 6:
            return "schizoid"
        else:
            return None

def assess_mood():
    mood_recorded = record_mood()
    if not mood_recorded:
        return

    average_mood = check_entries()
    if average_mood is not None:
        print(f"Average mood over the last 7 days: {average_mood}")
    
    diagnosis = check_disorders()
    if diagnosis:
        print(f"Your diagnosis: {diagnosis}!")
