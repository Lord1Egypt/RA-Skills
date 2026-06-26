#!/usr/bin/env python3
import requests
import json
import sys
import os

# wger API integration for viewing logs
BASE_URL = 'https://wger.de/api/v2/'
TOKEN = os.getenv('WGER_TOKEN')  # Set env WGER_TOKEN=your_key

if not TOKEN:
    print("Error: Set WGER_TOKEN env var")
    sys.exit(1)

def view_logs(limit=7, workout_id=None):
    headers = {'Authorization': f'Token {TOKEN}', 'Content-Type': 'application/json'}
    url = f'{BASE_URL}workoutlog/?limit={limit}&format=json'
    if workout_id:
        url += f'&workout={workout_id}'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        print(json.dumps(data, indent=2))
    else:
        print(f"Error: {response.status_code} - {response.text}")

if __name__ == '__main__':
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    workout_id = sys.argv[2] if len(sys.argv) > 2 else None
    view_logs(limit, workout_id)
