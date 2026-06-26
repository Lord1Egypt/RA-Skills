---
name: qweather
version: 1.0.0
description: >
  天气查询 — 实时天气、天气预报、生活指数、城市搜索。数据源为和风天气 (QWeather)。
  触发词: 天气, 气温, 下雨, 预报, weather, forecast, 穿什么, 洗车,
  紫外线, UV, 空气, 今天天气, 明天天气, 北京天气,
  或任何 "[城市] 天气" 格式的输入。
metadata:
  openclaw:
    requires:
      env:
        - QWEATHER_API_KEY
        - QWEATHER_API_HOST
---

# qweather — Weather Query Skill

Query real-time weather, forecasts, and life indices via QWeather (和风天气) API.

## Quick Start
1. Ensure `QWEATHER_API_KEY` and `QWEATHER_API_HOST` are set (get both at https://console.qweather.com).
2. Run `bun scripts/weather.ts --help` in this skill directory.
3. Pick the matching command from `references/command-map.md`.

## Workflow
1. If the user provides a city name (e.g. "北京", "Shanghai"), first run `lookup` to get the LocationID.
2. Use the LocationID to call `now`, `forecast`, or `indices`.
3. Return the result in natural language.

## Common City Mapping
When the user provides a city name, use the `lookup` command to resolve it to a LocationID. Common examples:
- 北京 → 101010100
- 上海 → 101020100
- 广州 → 101280101
- 深圳 → 101280601

Always use `lookup` for unfamiliar city names to get the correct LocationID.

## Notes
- This skill is script-first and does not run an MCP server.
- Requires `QWEATHER_API_KEY` and `QWEATHER_API_HOST` environment variables.
- API host is per-developer, find yours at https://console.qweather.com/setting
- Data updated every 10-20 minutes for real-time weather.
