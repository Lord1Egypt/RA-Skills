---
name: wikipedia-nearby
description: Find nearby Wikipedia articles based on geographic location. Use when user asks about "nearby places", "what's around me", "places near [location]", "Wikipedia nearby", or wants to discover points of interest, historical sites, restaurants, or landmarks in a specific area using Wikipedia's geolocation API.
---

# Wikipedia Nearby

## Overview

Wikipedia has a built-in geolocation feature that finds articles (places, landmarks, restaurants, museums, etc.) near any location. This skill covers how to access and use Wikipedia Nearby.

## Primary URL

**https://en.wikipedia.org/wiki/Special:Nearby**

This page uses browser geolocation (GPS) to show Wikipedia articles near your current location.

## API Access

For programmatic access without browser geolocation, use Wikipedia's APIs:

### Geolocation Search
```
https://en.wikipedia.org/w/api.php?action=query&list=geosearch&gscoord={lat}%7C{lng}&gsradius=10000&gslimit=50&format=json
```

Parameters:
- `gscoord`: Latitude and longitude separated by `|` (e.g., `35.6762%7C139.6503` for Tokyo)
- `gsradius`: Search radius in meters (default: 1000, max: 10000)
- `gslimit`: Maximum results (default: 10, max: 500)

### Get Article Details
```
https://en.wikipedia.org/w/api.php?action=query&titles={title}&prop=extracts&exintro&explaintext&format=json
```

## Usage Patterns

### 1. Current Location (Browser Required)
Direct user to https://en.wikipedia.org/wiki/Special:Nearby and allow browser geolocation.

### 2. Specific Location
If user provides coordinates or a place name:
1. Use geocode API or search to get lat/lng
2. Query Wikipedia geosearch API
3. Return results with titles, distances, and brief descriptions

### 3. Known Coordinates
If user provides lat/lng directly, skip geocoding and query directly:

```
https://en.wikipedia.org/w/api.php?action=query&list=geosearch&gscoord=-6.2088%7C106.8456&gsradius=5000&gslimit=20&format=json
```

Example for Jakarta (-6.2088, 106.8456):

```bash
curl "https://en.wikipedia.org/w/api.php?action=query&list=geosearch&gscoord=-6.2088%7C106.8456&gsradius=5000&gslimit=10&format=json"
```

### 4. Parse and Present Results

The API returns:
```json
{
  "query": {
    "geosearch": [
      {
        "pageid": 12345,
        "title": "Monas",
        "lat": -6.175392,
        "lon": 106.827153,
        "dist": 450,
        "primary"
      }
    ]
  }
}
```

Present results as:
- **Name** (distance from center)
- Brief extract if available

## Location Sharing from Telegram/WhatsApp

When user shares location via Telegram or WhatsApp:

**Telegram:** Receives `location` object with `latitude` and `longitude`

**WhatsApp:** Receives `location` message with `latitude` and `longitude`

Extract coordinates and query directly:
```bash
curl "https://en.wikipedia.org/w/api.php?action=query&list=geosearch&gscoord={lat}%7C{lng}&gsradius=5000&gslimit=20&format=json"
```

## Example Workflow

**User shares location from Telegram/WhatsApp:**

1. Extract `latitude` and `longitude` from the incoming location message
2. Query Wikipedia geosearch API:
```bash
curl "https://en.wikipedia.org/w/api.php?action=query&list=geosearch&gscoord=-6.175392%7C106.827153&gsradius=5000&gslimit=10&format=json"
```
3. Present results with name, distance, and brief extract if available

**User asks:** "What's near Monas in Jakarta?"

1. Get Monas coordinates: -6.175392, 106.827153
2. Query geosearch API with radius 2km
3. Present top 10 results with distance and brief description

## Notes

- Wikipedia Nearby primarily works well for densely-populated areas with many Wikipedia articles
- Results are limited to articles with geographic coordinates in Wikipedia's database
- For very remote areas, results may be sparse or empty
- Wikipedia articles are available in many languages; consider using `uselang` parameter if relevant
