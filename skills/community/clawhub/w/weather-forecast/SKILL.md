---
name: weather-forecast
description: This skill should be used when users ask about weather forecasts, temperature information, or need to retrieve weather data for specific locations. It provides access to the Open-Meteo weather API for getting hourly temperature forecasts based on latitude and longitude coordinates.
---

# Weather Forecast Skill

This skill enables querying weather forecasts using the Open-Meteo API, providing hourly temperature data for any location worldwide.

## When to Use This Skill

Activate this skill when:
- Users ask for weather information or forecasts
- Users inquire about temperatures at specific locations
- Users mention weather-related queries that require current or future data
- Users provide location names and expect weather details

## Skill Components

### Scripts

The `scripts/get_weather.py` script provides a reliable, reusable way to fetch weather data from the Open-Meteo API. This script is used instead of writing API calls from scratch each time because:
- API endpoints and parameters need to be consistent
- Error handling for network requests is standardized
- JSON parsing and data extraction is automated
- The script can be executed without loading into context

### References

The `references/api_response_format.md` contains documentation about the Open-Meteo API response structure, including:
- Request parameters (latitude, longitude, hourly data types)
- Response format and field meanings
- Time zone handling
- Error conditions

## Workflow

When this skill is activated:

1. **Extract location information** from the user's query. This may include:
   - City names (e.g., "Beijing", "Shanghai", "New York")
   - Specific coordinates (latitude, longitude)
   - Descriptive locations (e.g., "my current location")

2. **Convert location to coordinates**:
   - If city name is provided, use geocoding to get latitude and longitude
   - If coordinates are provided directly, use them as-is
   - Common city coordinates (saved in memory): Beijing (39.9042, 116.4074), Shanghai (31.2304, 121.4737), New York (40.7128, -74.0060), London (51.5074, -0.1278), Tokyo (35.6762, 139.6503)

3. **Execute the weather script** using the coordinates:
   - Run `scripts/get_weather.py` with latitude and longitude parameters
   - The script returns structured weather data including hourly temperatures

4. **Present results** to the user in a natural, readable format:
   - Summarize key information (current temperature, high/low, forecast)
   - Include relevant time information (next 24 hours or specific times mentioned)
   - Use units appropriate to the context (Celsius by default, Fahrenheit if requested)

## Important Notes

- The Open-Meteo API provides hourly forecasts, not just current weather
- Temperature values are in Celsius by default
- The API is free and requires no authentication
- Coordinate precision: up to 4 decimal places for better accuracy
- If coordinates are not available for a location, inform the user and ask for coordinates or a different location

## Example Interactions

User: "What's the weather like in Beijing?"
Action: Extract "Beijing", use coordinates (39.9042, 116.4074), run script, present forecast

User: "Will it be cold in Tokyo tomorrow?"
Action: Extract "Tokyo" and "tomorrow", use coordinates (35.6762, 139.6503), run script, present tomorrow's temperature

User: "Get the temperature for latitude 52.52 and longitude 13.41"
Action: Use provided coordinates directly, run script, present hourly data

User: "How hot will it be in Shanghai today?"
Action: Extract "Shanghai", use coordinates (31.2304, 121.4737), run script, identify maximum temperature for today
