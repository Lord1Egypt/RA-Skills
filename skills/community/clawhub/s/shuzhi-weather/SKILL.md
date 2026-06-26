---
name: shuzhi-weather
description: This skill should be used when users need to query weather information via the Shuzhi Weather API with HMAC-SHA256 authentication. It provides hourly weather forecasts based on latitude and longitude coordinates. Users must configure app_key and app_secret in ~/.openclaw/skills/shuzhi-weather/config.json before using this skill.
---

# Shuzhi Weather Skill

This skill enables querying weather forecasts using the Shuzhi Weather API with HMAC-SHA256 authentication, providing hourly weather data for any location.

## Configuration Requirements

**IMPORTANT**: Before using this skill, you must configure your API credentials:

Create the configuration file at `~/.openclaw/skills/shuzhi-weather/config.json` with the following content:

```json
{
  "app_key": "your_app_key_here",
  "app_secret": "your_app_secret_here"
}
```

Replace `your_app_key_here` and `your_app_secret_here` with your actual Shuzhi API credentials.

### Configuration Priority

The skill follows this configuration priority order:
1. User's config.json at `~/.openclaw/skills/shuzhi-weather/config.json` (highest priority)
2. Platform environment variables (if available)
3. Default values (if any exist)

## When to Use This Skill

Activate this skill when:
- Users ask for weather forecasts or weather information
- Users inquire about temperatures at specific locations
- Users mention weather-related queries that require current or future data
- Users provide location names and expect weather details

## Skill Components

### Scripts

The `scripts/get_weather.py` script provides a reliable way to fetch weather data from the Shuzhi Weather API with HMAC-SHA256 authentication. This script:
- Loads credentials from the user's config.json file
- Generates dual HMAC-SHA256 signatures (URL signature + body signature)
- Makes authenticated POST requests to the Shuzhi API
- Returns structured weather data including hourly temperatures

### References

The `references/api_response_format.md` contains documentation about the Shuzhi Weather API, including:
- Request parameters (longitude, latitude, hourly data types)
- Response format and field meanings
- HMAC-SHA256 authentication mechanism
- Error handling and response codes

## Workflow

When this skill is activated:

1. **Check configuration** - Verify that `~/.openclaw/skills/shuzhi-weather/config.json` exists and contains valid credentials. If not, prompt the user to configure it.

2. **Extract location information** from the user's query. This may include:
   - City names (e.g., "Beijing", "Shanghai", "Guangzhou")
   - Specific coordinates (latitude, longitude)
   - Descriptive locations

3. **Convert location to coordinates**:
   - If city name is provided, use geocoding to get latitude and longitude
   - If coordinates are provided directly, use them as-is
   - Common city coordinates: Beijing (39.9042, 116.4074), Shanghai (31.2304, 121.4737), Guangzhou (23.1291, 113.2644)

4. **Execute the weather script** using the coordinates:
   - Run `scripts/get_weather.py` with longitude and latitude parameters
   - The script loads credentials from config.json
   - Returns structured weather data including hourly temperatures

5. **Present results** to the user in a natural, readable format:
   - Summarize key information (current temperature, high/low, forecast)
   - Include relevant time information (next 24 hours or specific times mentioned)
   - Use units appropriate to the context (Celsius by default)

## Important Notes

- The Shuzhi Weather API requires HMAC-SHA256 authentication with dual signatures
- Credentials must be configured in `~/.openclaw/skills/shuzhi-weather/config.json` before use
- Coordinate format: longitude first, then latitude
- The API endpoint uses POST method with JSON body
- Response code 200 indicates success
- If credentials are missing or invalid, inform the user to check their config.json file

## Example Interactions

User: "What's the weather like in Beijing?"
Action: Check config exists, extract "Beijing", use coordinates (39.9042, 116.4074), run script, present forecast

User: "Will it be cold in Shanghai tomorrow?"
Action: Extract "Shanghai" and "tomorrow", use coordinates (31.2304, 121.4737), run script, present tomorrow's temperature

User: "Get the temperature for longitude 116.4074 and latitude 39.9042"
Action: Use provided coordinates directly, run script, present hourly data

User: "How hot will it be in Guangzhou today?"
Action: Extract "Guangzhou", use coordinates (23.1291, 113.2644), run script, identify maximum temperature for today

## Error Handling

If configuration is missing:
- Inform the user that credentials need to be configured
- Provide instructions on creating `~/.openclaw/skills/shuzhi-weather/config.json`
- Show the required JSON format

If API request fails:
- Check if credentials are valid
- Verify network connectivity
- Display error message from the API response
- Suggest checking the configuration file
