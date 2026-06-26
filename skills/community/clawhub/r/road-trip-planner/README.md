# Road Trip Planner

A multi-day road trip planning tool based on the Amap personal-map skill.

> China only — requires Amap API Key  
> Dependency: [@lbs-amap/personal-map](https://clawhub.ai/lbs-amap/personal-map)  
> [中文版本](README_CN.md)

## Features

- Design reasonable multi-day road trip itineraries with controlled daily driving time (recommended 4–6 hours)
- Automatically call Amap Web Service APIs for geocoding, POI search, and driving route planning
- Generate QR codes for personal maps that can be opened in the Amap App
- Output daily itinerary guides in Markdown format
- Support closed-loop route design with automatic cross-day mileage completion

## Use Cases

This skill triggers automatically when users mention any of the following:
- Planning a road trip route / road trip / loop route
- Designing a travel itinerary involving multi-city driving
- Generating personal maps / travel maps / route QR codes
- Controlling daily driving time / avoiding fatigued driving
- Querying mileage, gas stations, hospitals, and other supply points along the route

## Installation

```bash
openclaw skills install personal-map
```

## Prerequisites

- [@lbs-amap/personal-map](https://clawhub.ai/lbs-amap/personal-map) skill ([GitHub](https://github.com/amap-demo/amap-sdk-skills) — Amap API wrapper)
- Amap Open Platform Web Service API Key (set env var `AMAP_API_KEY`)

## Core Principles

1. **No fatigued driving**: Keep actual daily driving time under 6 hours, ideally 4–5 hours
2. **Continuous route**: Merge all daily waypoints into a single continuous route
3. **Closed loop**: If start and end are the same city, ensure the endpoint is preserved after deduplication
4. **Daily flexibility**: Leave buffer room in the itinerary; avoid over-scheduling

## File Structure

```
road-trip-planner/
├── SKILL.md         # Main guidance document
├── references/      # Conditional references loaded only when needed
├── examples.md      # Examples (Mongolia East, Qinghai-Gansu, Western Sichuan)
├── README.md        # This file (English)
├── README_CN.md     # Chinese version
├── CLAUDE.md        # Developer reference
├── LICENSE          # MIT license
└── .gitignore
```

## Examples

See [examples.md](examples.md) for the following cases:
- Hulunbuir 8-day loop (Mongolia East)
- Qinghai-Gansu Grand Loop 9-day road trip
- Western Sichuan Mini Loop 5-day road trip

## License

MIT
