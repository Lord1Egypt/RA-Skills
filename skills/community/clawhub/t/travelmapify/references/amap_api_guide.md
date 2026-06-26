# Amap API Usage Guide

## Overview

This guide provides essential information for using Amap Web APIs in the travel-mapify skill.

## Required Setup

### 1. Amap Web API Key
- Obtain a free Amap Web API key from [Amap Console](https://console.amap.com/)
- The key must have permissions for:
  - **Web Service API**: Geocoding and search
  - **JavaScript API**: Map display and interaction

### 2. Local Proxy Server
Due to CORS restrictions, Amap APIs must be accessed through a local proxy server running on port 8769.

#### Proxy Endpoints
- **Search/Geocoding**: `http://localhost:8769/api/search`
  - Parameters: `q` (query), `city` (optional city filter)
  - Returns: JSON with POI results

#### Example Request
```bash
curl "http://localhost:8769/api/search?q=解放碑&city=重庆"
```

#### Example Response
```json
{
  "pois": [
    {
      "id": "B0FFG33I2E",
      "name": "解放碑步行街",
      "location": "106.575329,29.557253",
      "address": "民族路177号",
      "rating": "4.9"
    }
  ]
}
```

## JavaScript API Integration

### Basic Map Initialization
```javascript
var map = new AMap.Map('container', {
    zoom: 17,
    center: [106.575329, 29.557253],
    viewMode: '2D',
    pitch: 0,
    rotation: 0,
    layers: [
        new AMap.TileLayer({
            detectRetina: true
        }),
        new AMap.TileLayer.RoadNet({
            opacity: 1.0
        })
    ],
    mapStyle: 'normal',
    lang: 'zh_cn',
    showLabel: true
});
```

### Marker Creation
```javascript
var marker = new AMap.Marker({
    position: [lng, lat],
    content: `<div style="width:28px;height:28px;background:#f59e0b;color:white;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:bold;font-size:14px;">${number}</div>`,
    offset: new AMap.Pixel(-14, -14),
    draggable: true,
    zIndex: 100
});
```

### Route Line Drawing
```javascript
var polyline = new AMap.Polyline({
    path: routePath, // Array of [lng, lat] coordinates
    strokeColor: "#4a9eff",
    strokeWeight: 4,
    strokeOpacity: 0.95,
    showDir: true,
    dirColor: "#ff6b35",
    dirWidth: 8,
    zIndex: 50,
    lineJoin: 'round',
    lineCap: 'round'
});
```

## Error Handling

### Common Error Codes
- **403**: Invalid or missing API key
- **429**: Rate limit exceeded
- **500**: Server error

### Retry Strategy
Implement exponential backoff for rate limit errors:
```python
import time
import random

def retry_with_backoff(func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return func()
        except RateLimitError:
            if attempt == max_retries - 1:
                raise
            delay = (2 ** attempt) + random.uniform(0, 1)
            time.sleep(delay)
```

## Best Practices

### 1. Coordinate Format
- Always use `[longitude, latitude]` format
- Longitude ranges: -180 to 180
- Latitude ranges: -90 to 90

### 2. City Specification
- Always specify city parameter for geocoding to improve accuracy
- Use Chinese city names when possible (e.g., "重庆" instead of "Chongqing")

### 3. Performance Optimization
- Cache geocoding results to avoid redundant API calls
- Batch process multiple locations when possible
- Use appropriate zoom levels (16-17 for detailed city views)

### 4. User Experience
- Provide loading indicators during API calls
- Handle ambiguous results with user selection dialogs
- Validate coordinates before displaying on map

## Security Considerations

### API Key Protection
- Never expose Amap API keys in client-side code
- Always use local proxy server for API requests
- Implement request validation in proxy server

### Input Validation
- Sanitize all user inputs before API calls
- Validate coordinate ranges before processing
- Escape HTML content in markers and info windows

## Troubleshooting

### No Results Found
1. Check if location name is spelled correctly
2. Try broader search terms
3. Verify city parameter is correct
4. Test with known valid locations

### Map Not Loading
1. Verify Amap API key is valid
2. Check network connectivity
3. Ensure local proxy server is running
4. Test API endpoint directly in browser

### Poor Geocoding Accuracy
1. Add more specific location details (street address, district)
2. Try different search terms
3. Manually verify and adjust coordinates if needed
4. Use multiple geocoding services as fallback