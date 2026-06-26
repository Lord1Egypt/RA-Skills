name: w

version: 1.0.0

description: "A comprehensive skill pack starting with 'w', offering weather查询, word learning, wiki search, writing assistant, workout plans, web search, weight management, and water reminder functions. Use when: user needs weather info, wants to learn words, search Wikipedia, get writing help, create workout plans, search the web, track weight, or set water reminders."

---

# W Skill Pack

A comprehensive skill pack starting with 'w', offering multiple useful functions with actual implementation:

## Features and Usage

### 1. Weather查询
- **Function**: Get current weather and forecasts for any location
- **Usage**: `w.get_weather("location")`
- **Example**: `w.get_weather("Beijing")`
- **Returns**: Current weather description, temperature, and humidity

### 2. Word学习
- **Function**: Learn new words with definitions, examples, and pronunciation
- **Usage**: `w.learn_word("word")`
- **Example**: `w.learn_word("python")`
- **Returns**: Word definition and example usage

### 3. Wiki搜索
- **Function**: Search Wikipedia for information on any topic
- **Usage**: `w.search_wiki("query")`
- **Example**: `w.search_wiki("Artificial Intelligence")`
- **Returns**: Top 3 Wikipedia search results

### 4. Writing助手
- **Function**: Get help with writing, editing, and brainstorming
- **Usage**: `w.writing_help("prompt")`
- **Example**: `w.writing_help("How to write a good essay")`
- **Returns**: Writing suggestions and structure advice

### 5. Workout计划
- **Function**: Create personalized workout plans and track progress
- **Usage**: `w.create_workout_plan("goal", duration)`
- **Example**: `w.create_workout_plan("weight loss", 8)`
- **Returns**: Custom workout plan based on goal

### 6. Web搜索
- **Function**: Search the web for the latest information
- **Usage**: `w.web_search("query")`
- **Example**: `w.web_search("latest technology trends")`
- **Returns**: Top 3 web search results

### 7. Weight管理
- **Function**: Track weight and set weight loss/gain goals
- **Usage**: `w.track_weight(weight, date)`
- **Example**: `w.track_weight(70)`
- **Returns**: Confirmation of weight tracking
- **Additional**: `w.get_weight_log()` to view all weight entries

### 8. Water提醒
- **Function**: Set reminders to stay hydrated throughout the day
- **Usage**: `w.set_water_reminder(interval)`
- **Example**: `w.set_water_reminder(60)`
- **Returns**: Confirmation of reminder setup

## Implementation Details

- **Language**: Python 3
- **Dependencies**: requests
- **API Requirements**: Some functions require API keys (OpenWeatherMap, Google Custom Search)
- **Data Storage**: In-memory storage for weight logs, workout plans, and water reminders

## How to Use

1. Install the skill pack
2. Import the WSkillPack class
3. Create an instance: `w = WSkillPack()`
4. Call the desired functions as shown in the usage examples

This skill pack is designed to be a one-stop solution for various daily needs, all starting with the letter 'w' for easy recall and recognition. It provides practical functionality that users can immediately start using after installation.