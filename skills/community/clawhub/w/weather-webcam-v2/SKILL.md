---
name: Weather&Webcam
description: Fetches current weather from Open-Meteo API and automatically captures a live webcam image from Meteoblue or Windy for the requested location. Use it when the user asks for the weather and wants to see a real image of the current conditions.
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["agent-browser", "curl"] },
      },
  }
---

# Weather Location

This skill automates weather data retrieval using Open-Meteo and live webcam image capture using **agent-browser**.

## Workflow

1.  **Get Coordinates (Geocoding)**:
    - Execute `curl -s "https://geocoding-api.open-meteo.com/v1/search?name=[Location]&count=1&language=es&format=json"` to resolve city name to coordinates.

2.  **Get weather (Open-Meteo)**:
    - Execute `curl -s "https://api.open-meteo.com/v1/forecast?latitude=[Lat]&longitude=[Lon]&current=temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m"` to get real-time data.

3.  **Search for Webcam**:
    - Web search for `site:meteoblue.com [Location] webcam` or `site:windy.com [Location] webcam`.
    - Select the direct link to the location's webcam page.

4.  **Capture Image (Agent Browser Method)**:
    - Use **agent-browser** to navigate and interact:
      ```bash
      /home/user/.npm-global/bin/agent-browser --session-name webcam open "[URL]"
      ```
    - **Interaction**:
      - Click "OK/Accept" on cookie banners using `snapshot` + `click @ref`.
    - **Extraction**:
      - Use `eval` to find the highest resolution URL (look for `/full/` and `original.jpg`):
        ```javascript
        Array.from(document.querySelectorAll('img')).map(img => img.src).filter(src => src.includes('original.jpg') && src.includes('/full/'))[0]
        ```
    - **Download**:
      - Download with `curl` to `/home/user/.openclaw/workspace/webcam.jpg`.

5.  **User Response**:
    - Send with `message(action=send, media="/home/user/.openclaw/workspace/webcam.jpg", caption="[City]: [Icon] [Temp]°C [Humidity]% [Wind]km/h\n[Comment]")`.
    - Respond with `NO_REPLY`.

## Optimization (Token Saving)

1. **Open-Meteo API**: Faster, keyless, and more reliable than wttr.in.
2. **Agent Browser**: Priority method for Alex to ensure interaction (cookies) and high-quality images.
3. **Session Persistence**: Use `--session-name webcam` to keep cookies.
