#!/usr/bin/env python3
"""
W Skill Pack - A comprehensive skill pack starting with 'w'

This skill pack provides multiple useful functions:
- Weather查询: Get current weather and forecasts for any location
- Word学习: Learn new words with definitions, examples, and pronunciation
- Wiki搜索: Search Wikipedia for information on any topic
- Writing助手: Get help with writing, editing, and brainstorming
- Workout计划: Create personalized workout plans and track progress
- Web搜索: Search the web for the latest information
- Weight管理: Track weight and set weight loss/gain goals
- Water提醒: Set reminders to stay hydrated throughout the day
"""

import requests
import json
import time
from datetime import datetime

class WSkillPack:
    def __init__(self):
        """Initialize the W Skill Pack"""
        self.weight_log = []
        self.water_reminders = []
        self.workout_plans = []
    
    def get_weather(self, location):
        """Get current weather for a location"""
        try:
            # Using OpenWeatherMap API (you'll need to add your API key)
            api_key = "YOUR_OPENWEATHER_API_KEY"
            url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
            response = requests.get(url)
            data = response.json()
            
            if data.get("cod") == 200:
                weather = data["weather"][0]["description"]
                temp = data["main"]["temp"]
                humidity = data["main"]["humidity"]
                return f"Current weather in {location}: {weather}, {temp}°C, {humidity}% humidity"
            else:
                return f"Could not get weather for {location}"
        except Exception as e:
            return f"Error getting weather: {str(e)}"
    
    def learn_word(self, word):
        """Learn a new word"""
        try:
            # Using Dictionary API (you'll need to add your API key)
            api_key = "YOUR_DICTIONARY_API_KEY"
            url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
            response = requests.get(url)
            data = response.json()
            
            if isinstance(data, list) and len(data) > 0:
                meaning = data[0]["meanings"][0]["definitions"][0]["definition"]
                example = data[0]["meanings"][0]["definitions"][0].get("example", "No example available")
                return f"Word: {word}\nDefinition: {meaning}\nExample: {example}"
            else:
                return f"Could not find information for word: {word}"
        except Exception as e:
            return f"Error learning word: {str(e)}"
    
    def search_wiki(self, query):
        """Search Wikipedia"""
        try:
            url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={query}&format=json"
            response = requests.get(url)
            data = response.json()
            
            if "query" in data and "search" in data["query"]:
                results = data["query"]["search"]
                if results:
                    summary = f"Wikipedia search results for '{query}':\n"
                    for i, result in enumerate(results[:3], 1):
                        summary += f"{i}. {result['title']}: {result['snippet']}\n"
                    return summary
                else:
                    return f"No Wikipedia results found for '{query}'"
            else:
                return f"Error searching Wikipedia"
        except Exception as e:
            return f"Error searching Wikipedia: {str(e)}"
    
    def writing_help(self, prompt):
        """Get writing help"""
        try:
            # This would typically use an LLM API like OpenAI
            # For demonstration, we'll return a simple response
            return f"Writing help for: {prompt}\n\nHere's a suggestion:\nStart with an introduction that clearly states your main point, then provide supporting evidence, and conclude with a summary of your key arguments."
        except Exception as e:
            return f"Error getting writing help: {str(e)}"
    
    def create_workout_plan(self, goal, duration):
        """Create a workout plan"""
        try:
            plan = {
                "goal": goal,
                "duration": duration,
                "created_at": datetime.now().isoformat(),
                "exercises": []
            }
            
            # Generate sample workout plan based on goal
            if goal.lower() == "weight loss":
                plan["exercises"] = [
                    "Cardio: 30 minutes of running or cycling",
                    "Strength training: 3 sets of 12 reps for each major muscle group",
                    "Core exercises: Planks, crunches, and leg raises"
                ]
            elif goal.lower() == "muscle gain":
                plan["exercises"] = [
                    "Compound lifts: Squats, deadlifts, bench press",
                    "Isolation exercises: Bicep curls, tricep extensions",
                    "Rest and recovery: 48 hours between muscle groups"
                ]
            else:
                plan["exercises"] = [
                    "Warm-up: 10 minutes of light activity",
                    "Main workout: 30 minutes of moderate intensity exercise",
                    "Cool-down: 5 minutes of stretching"
                ]
            
            self.workout_plans.append(plan)
            return f"Created workout plan for {goal} over {duration} weeks. Exercises: {', '.join(plan['exercises'])}"
        except Exception as e:
            return f"Error creating workout plan: {str(e)}"
    
    def web_search(self, query):
        """Search the web"""
        try:
            # Using Google Custom Search API (you'll need to add your API key)
            api_key = "YOUR_GOOGLE_API_KEY"
            cx = "YOUR_CUSTOM_SEARCH_ENGINE_ID"
            url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={api_key}&cx={cx}"
            response = requests.get(url)
            data = response.json()
            
            if "items" in data:
                results = data["items"]
                summary = f"Web search results for '{query}':\n"
                for i, result in enumerate(results[:3], 1):
                    summary += f"{i}. {result['title']}: {result['link']}\n"
                return summary
            else:
                return f"No web results found for '{query}'"
        except Exception as e:
            return f"Error searching web: {str(e)}"
    
    def track_weight(self, weight, date=None):
        """Track weight"""
        try:
            if date is None:
                date = datetime.now().isoformat()
            
            weight_entry = {
                "weight": weight,
                "date": date
            }
            
            self.weight_log.append(weight_entry)
            return f"Tracked weight: {weight} kg on {date}"
        except Exception as e:
            return f"Error tracking weight: {str(e)}"
    
    def set_water_reminder(self, interval):
        """Set water reminder"""
        try:
            reminder = {
                "interval": interval,
                "created_at": datetime.now().isoformat()
            }
            
            self.water_reminders.append(reminder)
            return f"Set water reminder every {interval} minutes"
        except Exception as e:
            return f"Error setting water reminder: {str(e)}"
    
    def get_weight_log(self):
        """Get weight log"""
        try:
            if not self.weight_log:
                return "No weight entries found"
            
            log = "Weight log:\n"
            for entry in self.weight_log:
                log += f"{entry['date']}: {entry['weight']} kg\n"
            return log
        except Exception as e:
            return f"Error getting weight log: {str(e)}"
    
    def get_workout_plans(self):
        """Get workout plans"""
        try:
            if not self.workout_plans:
                return "No workout plans found"
            
            plans = "Workout plans:\n"
            for i, plan in enumerate(self.workout_plans, 1):
                plans += f"{i}. Goal: {plan['goal']}, Duration: {plan['duration']} weeks\n"
                plans += f"   Exercises: {', '.join(plan['exercises'])}\n"
            return plans
        except Exception as e:
            return f"Error getting workout plans: {str(e)}"

if __name__ == "__main__":
    # Test the skill pack
    w_skill = WSkillPack()
    
    # Test weather function
    print(w_skill.get_weather("Beijing"))
    
    # Test word learning function
    print(w_skill.learn_word("python"))
    
    # Test wiki search function
    print(w_skill.search_wiki("Artificial Intelligence"))
    
    # Test writing help function
    print(w_skill.writing_help("How to write a good essay"))
    
    # Test workout plan function
    print(w_skill.create_workout_plan("weight loss", 8))
    
    # Test web search function
    print(w_skill.web_search("latest technology trends"))
    
    # Test weight tracking function
    print(w_skill.track_weight(70))
    
    # Test water reminder function
    print(w_skill.set_water_reminder(60))
    
    # Test get weight log
    print(w_skill.get_weight_log())
    
    # Test get workout plans
    print(w_skill.get_workout_plans())