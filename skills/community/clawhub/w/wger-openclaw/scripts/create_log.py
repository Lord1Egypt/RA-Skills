#!/usr/bin/env python3
import requests
import json
import sys
import os

BASE_URL = 'https://wger.de/api/v2/'
TOKEN = os.getenv('WGER_TOKEN')

if not TOKEN:
    print("Error: Set WGER_TOKEN env var")
    sys.exit(1)

def create_log(date, workout_id, exercises):
    headers = {'Authorization': f'Token {TOKEN}', 'Content-Type': 'application/json'}
    data = {
        'date': date,
        'workout': workout_id,
        'exercises': exercises  # List of dicts: [{'reps': 10, 'weight': 135, 'exercise': exercise_id}]
    }
    response = requests.post(f'{BASE_URL}workoutlog/', json=data, headers=headers)
    if response.status_code in [200, 201]:
        print(f"Log created: {response.json()}")
    else:
        print(f"Error: {response.status_code} - {response.text}")

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage: python create_log.py <date YYYY-MM-DD> <workout_id> <exercises JSON>")
        sys.exit(1)
    date = sys.argv[1]
    workout_id = int(sys.argv[2])
    exercises = json.loads(sys.argv[3])
    create_log(date, workout_id, exercises)
