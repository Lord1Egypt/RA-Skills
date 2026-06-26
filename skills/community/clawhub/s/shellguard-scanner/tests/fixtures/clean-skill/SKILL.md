---
name: weather-check
version: 1.0.0
description: Check current weather conditions for any location using wttr.in.
author: example-dev
license: MIT
tags:
  - weather
  - utility
---

# Weather Check

Get current weather for any location.

## Usage

Ask your agent "What's the weather in Tokyo?" and it will fetch conditions from wttr.in.

```bash
curl -s "wttr.in/${LOCATION}?format=3"
```
