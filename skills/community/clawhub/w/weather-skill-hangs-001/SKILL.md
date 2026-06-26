# Weather Skill

## Overview

The Weather Skill provides weather information for a specified city.
It is designed to help users quickly understand current weather conditions, including temperature and general climate status, especially for travel planning or daily decision-making.

This skill can be integrated into conversational agents to respond to user queries related to weather conditions.

---

## Use Cases

This skill is suitable for the following scenarios:

* Checking weather conditions before traveling
* Asking about temperature in a specific city
* Getting quick climate information for daily planning
* Supporting voice assistants or chatbots with weather responses

---

## When to Use

Use this skill when:

* The user asks about weather (e.g., "What's the weather in Beijing?")
* The user requests temperature or climate details
* The query involves outdoor planning or travel preparation

---

## Input

The skill accepts the following input:

* **city** (string): The name of the city to query weather for

Example:

```json
{
  "city": "Singapore"
}
```

---

## Output

The skill returns a structured weather description:

* **weather** (string): A human-readable description of the weather

Example:

```json
{
  "weather": "Sunny, 30°C"
}
```

---

## Example Scenarios

### Example 1

Input:

```json
{
  "city": "Beijing"
}
```

Output:

```json
{
  "weather": "Sunny, 25°C"
}
```

### Example 2

Input:

```json
{
  "city": "London"
}
```

Output:

```json
{
  "weather": "Cloudy, 18°C"
}
```

---

## How It Works

This skill processes the input city name and returns a weather description.
Currently, the output is simulated (mock data), but the structure is designed to support integration with real-world weather APIs such as OpenWeather or other meteorological services.

---

## Limitations

* The current version does not fetch real-time data from external APIs
* Weather responses are simulated
* Only major cities are supported in this version

---

## Future Improvements

* Integrate real-time weather APIs
* Support more detailed weather data (humidity, wind, forecast)
* Add multi-language support
* Improve location recognition accuracy
