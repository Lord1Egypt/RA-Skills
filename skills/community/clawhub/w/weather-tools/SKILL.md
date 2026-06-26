---
name: weather-tools
description: Get current weather and forecasts (no API key required).
homepage: https://wttr.in/:help
metadata: {"clawdbot":{"emoji":"🌤️","requires":{"bins":["curl"]}}}

# Weather

Get weather information using wttr.in (no API key required).

## Current weather

```bash
curl wttr.in
```

Location-specific:
```bash
curl wttr.in/Beijing
```

Compact output:
```bash
curl wttr.in/?format=3
```

## Forecasts

3-day forecast:
```bash
curl wttr.in/?1
```

Tomorrow:
```bash
curl wttr.in/?1T
```

Full forecast:
```bash
curl wttr.in/?2
```

## Output formats

Current temp only:
```bash
curl wttr.in/?format=%t
```

Wind direction and speed:
```bash
curl wttr.in/?format=%w
```

Full location name:
```bash
curl wttr.in/?format=%l
```

Custom format:
```bash
curl wttr.in/?format="%l: %c+%t+%w"
```

## Examples

Beijing current weather:
```bash
curl wttr.in/Beijing
```

Shanghai 3-day forecast:
```bash
curl wttr.in/Shanghai?1
```

Compact format (any location):
```bash
curl wttr.in/Tokyo?format=3
```

Moon phase:
```bash
curl wttr.in/?format=%m
```
