---
name: weather-poster
description: Generate weather and outfit recommendation posters as SVG. Default region is Wuhan, China. User can specify other cities. Use when user asks for "天气海报", "weather poster", "穿搭海报", or similar.
---

# Weather Poster

Generate a weather and outfit recommendation poster as SVG file.

## Default Behavior

- **Default city**: Wuhan, China
- **User can specify**: Any city (e.g., "北京天气海报", "上海穿搭")

## Workflow

1. Get weather data for the specified city (default: Wuhan)
   - Useweather skill or fetch from wttr.in
   - Extract: temperature, weather condition, wind, humidity

2. Generate outfit recommendations based on weather:
   - Rain → umbrella, raincoat, waterproof shoes
   - Cold (<15°C) → jacket, long pants
   - Hot (>28°C) → light clothing, shorts
   - Sunny → sunglasses, hat

3. Create SVG using the template in assets/

## Assets

- See [TEMPLATE.md](references/TEMPLATE.md) for SVG template structure

## Output

Save as `{city}-weather-poster.svg` in the workspace