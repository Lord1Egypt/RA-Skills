---
summary: "Real-time traffic intelligence using TomTom API"
read_when:
  - User asks about traffic, commute times, or departure planning
  - User wants to integrate traffic data with meeting alerts
  - User needs real-time congestion information
---

# Traffic Intelligence Skill

## Overview
Provides real-time traffic monitoring, route calculation, and departure planning using TomTom Traffic API (2,500 free requests/day).

## Prerequisites
1. TomTom Developer Account: https://developer.tomtom.com/
2. API Key from TomTom Traffic API
3. Set environment variable: `export TOMTOM_API_KEY="your_key_here"`

## Configuration
Default locations are configured for Seattle/Bellevue area. Edit `./traffic-check.js` to update:
- `CONFIG.locations`: Set your home, work, and frequent destinations
- `CONFIG.buffers`: Adjust parking, coffee, and meeting buffer times

## Usage

### Direct CLI Commands
```bash
# Check current commute (home → work)
node ./traffic-check.js check

# Plan departure for 8:00 AM meeting
node ./traffic-check.js meeting 08:00

# Test API connection
node ./traffic-check.js test
```

### Integration with Meeting Alerts
The traffic module can be called from other scripts to enhance meeting alerts with real-time traffic data.

### Example Integration
```javascript
const TrafficIntelligence = require('./traffic-check.js');
const traffic = new TrafficIntelligence(process.env.TOMTOM_API_KEY);

// Get traffic-aware departure time for coffee meeting
const route = await traffic.calculateRoute(home, coffeeShop);
const meetingInfo = traffic.calculateDepartureTime(
  meetingTime,
  route.totalTimeMinutes,
  { meetingBuffer: 10 }
);

console.log(traffic.generateAlert(route, meetingInfo));
```

## API Limits
- **Free Tier:** 2,500 requests/day
- **Recommendation:** Cache results for 5-10 minutes during peak hours
- **Monitoring:** Check TomTom dashboard for usage statistics

## Error Handling
- Missing API key: Error message with setup instructions
- API failure: Graceful degradation with cached/last-known data
- Network issues: Retry logic with exponential backoff

## Security Notes
- API key stored in environment variable (not in code)
- No sensitive location data logged
- Rate limiting to prevent accidental overuse

## Future Enhancements
1. Historical traffic patterns
2. Weather integration (rain/snow impact)
3. Multiple route alternatives
4. Public transit integration
5. Traffic camera status

---
**Maintainer:** Agent M
**Last Updated:** 2026-03-19
**Status:** Operational