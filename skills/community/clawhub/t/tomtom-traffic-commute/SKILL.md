---
name: TomTom Traffic Commute
slug: tomtom-traffic
description: "Get real-time commute traffic using TomTom Routing API. Live travel times, delays, and ETAs."
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - TOMTOM_API_KEY
      bins:
        - curl
        - bash
    primaryEnv: TOMTOM_API_KEY
    envVars:
      - name: TOMTOM_API_KEY
        required: true
        description: TomTom developer API key (free tier at https://developer.tomtom.com).
    emoji: "🚗"
---

# TomTom Traffic Commute

Get real-time commute traffic data using the TomTom Routing API. Returns distance, travel time with live traffic, delay minutes, and ETAs.

## Setup

1. **Get a TomTom API key** — free tier at [developer.tomtom.com](https://developer.tomtom.com/) (2,500 free transactions/day)
2. **Set the environment variable**: `TOMTOM_API_KEY`

## Quick Start

```sh
export TOMTOM_API_KEY=yourkey
bash scripts/tomtom-traffic.sh "51.5081,-0.0753" "50.8213,-0.1325"
```

## Usage

### Basic query

```sh
export TOMTOM_API_KEY=yourkey
bash scripts/tomtom-traffic.sh <origin-lat,origin-lon> <dest-lat,dest-lon>
```

### Query with departure time

```sh
export TOMTOM_API_KEY=yourkey
bash scripts/tomtom-traffic.sh "51.5081,-0.0753" "50.8213,-0.1325" "2026-06-09T06:45:00+01:00"
```

### Output format

```json
{
  "distance_km": 84.2,
  "travel_time_min": 63,
  "traffic_delay_min": 1,
  "traffic_affected_km": 1.1,
  "departure_time": "2026-06-05T10:43:27+01:00",
  "arrival_time": "2026-06-05T11:46:50+01:00",
  "summary": "84.2 km, 63 min (delay: 1 min)"
}
```

## Automate with Cron

Optionally combine with AgentMail for daily commute email notifications. See [examples/commute-email.sh](examples/commute-email.sh) for a complete workflow.

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/tomtom-traffic.sh` | CLI tool — queries TomTom Routing API. No dependencies. |
| `examples/commute-email.sh` | Optional: TomTom + AgentMail email workflow |

## API Reference

Uses TomTom Routing API v1 `/calculateRoute` endpoint:
- **Endpoint**: `https://api.tomtom.com/routing/1/calculateRoute/{origin}:{dest}/json`
- **Parameters**: `traffic=true`, `routeType=fastest`
- **Auth**: API key in query string (`key=`)
- **Free tier**: 2,500 transactions/day
- **Coordinates**: `lat,lon` format (decimal degrees)
- **Departure time**: optional — defaults to "now"
