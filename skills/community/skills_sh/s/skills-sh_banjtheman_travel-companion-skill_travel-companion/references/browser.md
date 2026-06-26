# Browser Tool Reference

## OpenClaw Browser

The skill uses OpenClaw's managed browser with `profile: "openclaw"`.

**Start the browser:**
```bash
openclaw browser start
```

## All Actions

**navigate** - Load a URL
```json
{
  "action": "navigate",
  "targetUrl": "https://www.instagram.com/explore/locations/tokyo/",
  "profile": "openclaw"
}
```

**snapshot** - Read the current page
```json
{
  "action": "snapshot",
  "snapshotFormat": "ai",
  "profile": "openclaw"
}
```

**wait** - Pause for page to load
```json
{
  "action": "act",
  "request": {
    "kind": "wait",
    "timeMs": 5000
  },
  "profile": "openclaw"
}
```

## URL Patterns

### TikTok
```
https://www.tiktok.com/search?q={query}

Examples:
- https://www.tiktok.com/search?q=fun%20things%20to%20do%20in%20washington%20dc
- https://www.tiktok.com/search?q=best%20food%20tokyo
```

### Instagram
```
https://www.instagram.com/explore/search/keyword/?q={query}
https://www.instagram.com/explore/locations/{city}/

Examples:
- https://www.instagram.com/explore/search/keyword/?q=tokyo%20events
- https://www.instagram.com/explore/locations/miami/
```

### Eventbrite
```
https://www.eventbrite.com/d/{city}/events-{date}/

Examples:
- https://www.eventbrite.com/d/dc--washington/events--january-31-2025/
- https://www.eventbrite.com/d/fl--miami/events--february-14-2025/
```

### Google Maps
```
https://www.google.com/maps/search/{query}/{location}

Examples:
- https://www.google.com/maps/search/things+to+do/tokyo
- https://www.google.com/maps/search/restaurants/miami+beach
```

### Weather.com
```
https://weather.com/weather/today/l/{location}

Examples:
- https://weather.com/weather/today/l/washington-dc
- https://weather.com/weather/today/l/tokyo-japan
```

### Expedia
```
https://www.expedia.com/Flights-Search?trip=roundtrip&from={from}&to={to}&dates={date1},{date2}
https://www.expedia.com/Hotel-Search?destination={city}&dates={checkin},{checkout}
```

## Troubleshooting

### "Can't reach browser"
User must start the browser:
```bash
openclaw browser start
```

### Navigation fails
1. Try simpler URLs
2. Increase wait time (5000ms+ for social sites)
3. Use direct links instead of searches

### Instagram blocking
Instagram may block automated access. Alternatives:
- Use TikTok for local tips
- Use Eventbrite for events
- Use Google Maps for attractions
