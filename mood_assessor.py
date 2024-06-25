import datetime
import os

MOODS = {'happy': 2,'relaxed': 1,'apathetic': 0,'sad': -1,'angry': -2}

def get_user_mood():
    while True:
        mood = input("Enter your current mood: ").strip().lower()
        if mood in MOODS:
            return MOODS[mood]
        else:
            print("Invalid mood. Please enter one of: happy, relaxed, apathetic, sad, angry.")

def check_if_entered_today():
    try:
        with open('data/mood_diary.txt', 'r', encoding='utf-8') as file:
            entries = file.readlines()
            if entries:
                last_entry = entries[-1].strip().split(',')
                date_last_entry = last_entry[0]
                today = str(datetime.date.today())
                if date_last_entry == today:
                    return True
    except FileNotFoundError:
        pass
    
    return False

def record_mood_diary(mood_value):
    today = str(datetime.date.today())
    entry = f"{today},{mood_value}\n"

    if not os.path.exists('data'):
        os.makedirs('data')
    
    with open('data/mood_diary.txt', 'a', encoding='utf-8') as file:
        file.write(entry)

def check_disorders():
    try:
        with open('data/mood_diary.txt', 'r', encoding='utf-8') as fp:
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
    except FileNotFoundError:
        return None

def assess_mood():
    if check_if_entered_today():
        print("Sorry, you have already entered your mood today.")
        return
    
    mood_value = get_user_mood()
    record_mood_diary(mood_value)
    
    try:
        with open('data/mood_diary.txt', 'r', encoding='utf-8') as file:
            entries = file.readlines()
        
        if len(entries) < 7:
            return
        
        recent_entries = entries[-7:]
        sum_moods = sum(int(entry.strip().split(',')[1]) for entry in recent_entries)
        average_mood = round(sum_moods / 7)
        
        if average_mood in MOODS.values():
            diagnosis = {v: k for k, v in MOODS.items()}[average_mood]
        else:
            diagnosis = average_mood
        
        disorders_diagnosis = check_disorders()
        
        if disorders_diagnosis:
            print(f"Your diagnosis: {disorders_diagnosis.capitalize()}!")
        else:
            print(f"Your diagnosis: {diagnosis.capitalize()}!")

    except FileNotFoundError:
        pass

