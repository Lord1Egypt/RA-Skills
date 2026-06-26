# Weather Skill - Get Current Temperature

A paid skill that returns the current weather temperature for any location.

## Features

- Get current temperature for any city
- Returns temperature in Celsius
- Uses wttr.in for weather data (free, no API key needed)

## Price

- **0.001 USDT** per call
- Payment via SkillPay (BNB Chain)

## Usage

Simply call the skill with a city name:
- "What's the weather in Tokyo?"
- "Temperature in Beijing"
- "Weather in London"

## Integration

This skill uses SkillPay for payment processing:
- API Key: sk_93c5ff38cc3e6112623d361fffcc5d1eb1b5844eac9c40043b57c0e08f91430e
- Price: 0.001 USDT per call

## Example Response

```json
{
  "city": "Beijing",
  "temperature": "25°C",
  "condition": "Sunny",
  "humidity": "45%",
  "wind": "10 km/h"
}
```
