---
name: weather-open-meteo
description: "Get current weather and forecasts via open-meteo.com with optional fallback to wttr.in if available. No API key required."
homepage: https://open-meteo.com/
metadata:
  openclaw:
    emoji: 🌤️
    requires:
      bins:
        - curl
        - jq
---

# Weather Open‑Meteo Skill

This skill provides current weather and simple forecasts by querying the open‑meteo.com public API.  If the geocoding lookup or weather request fails, the skill can fall back to **wttr.in** as a lightweight alternative.

## 📌 Scope & Caveats
* The skill **requires** `curl` **and** `jq`.
* Location parameters are encoded before being sent to the API.
* Examples below demonstrate safe query construction using jq @uri.

## ✅ When to Use
✔ *The user asks* for weather, forecast, temperature, or rain probability for a location.
✖ Not for historical data, severe alerts, or detailed climatology.

## 📋 Commands
The skill accepts a single argument: a location name (city, region, or coordinates in `lat,lon`).

## Open‑Meteo (primary, JSON)

**Geocoding** (co‑ordinates for a place):

```bash
curl -s "https://geocoding-api.open-meteo.com/v1/search?name=São+Paulo\u0026count=1" | jq '.results[0] | {name, latitude, longitude}'
```

**Current weather** (by co‑ordinates):

```bash
curl -s "https://api.open-meteo.com/v1/forecast?latitude=-23.55\u0026longitude=-46.63\u0026current_weather=true" | jq '.current_weather'
```

**7‑day forecast** (by co‑ordinates):

```bash
curl -s "https://api.open-meteo.com/v1/forecast?latitude=-23.55\u0026longitude=-46.63\u0026daily=temperature_2m_max,temperature_2m_min,precipitation_sum\u0026forecast_days=7" | jq '.daily'
```

**Example JSON excerpt**

```json
{
  "latitude": -23.55,
  "longitude": -46.63,
  "current_weather": {
    "temperature": -5.3,
    "windspeed": 3.9,
    "winddirection": 200,
    "weathercode": 80,
    "time": "2024-02-18T14:00"
  }
}
```

📖 [Open‑Meteo API docs](https://open-meteo.com/en/docs)

## wttr.in (fallback)

**One‑liner** (HTML text):

```bash
curl -s "wttr.in/São+Paulo?format=3"
```

**Compact plain‑text**:

```bash
curl -s "wttr.in/São+Paulo?format=1"
```

**PNG image** (for terminals or embeds):

```bash
curl -s -o sp.png "http://wttr.in/São+Paulo?format=1"
```

## 📚 Example (User Query)
> **User:** *What's the weather in São Paulo?*
> **Agent:**
> `Current conditions in São Paulo: 🌤️ +10 °C, 20% chance of rain`

## Tips

- **URL‑encode** city names:
  ```bash
  curl -s "https://geocoding-api.open-meteo.com/v1/search?name=$(echo São Paulo | jq -sRr @uri)"
  ```
- **Use `jq`** to build the query dynamically:
  ```bash
  city="São Paulo"
  lat=$(curl -s "https://geocoding-api.open-meteo.com/v1/search?name=$(echo $city | jq -sRr @uri)" | jq -r '.results[0].latitude')
  lon=$(curl -s "https://geocoding-api.open-meteo.com/v1/search?name=$(echo $city | jq -sRr @uri)" | jq -r '.results[0].longitude')
  ```
- You can pass `latitude` and `longitude` directly if you know them.
- The API is rate‑limited (≈100 requests/min). Keep scripts cached or use short intervals.
