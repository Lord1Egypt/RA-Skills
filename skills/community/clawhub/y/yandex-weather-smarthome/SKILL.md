---
name: yandex-weather-smarthome
description: >
  Gets current weather and short forecast (today/tomorrow) for the user's configured home location via Yandex Weather API.
  Trigger when user asks about weather, temperature, wind, conditions, or forecast in Russian/English:
  "какая погода", "погода", "погода на сегодня", "погода на завтра", "прогноз", "weather", "forecast", "weather tomorrow".
metadata:
  openclaw:
    requires:
      bins:
        - python3
      env:
        - YANDEX_WEATHER_KEY
        - YANDEX_WEATHER_LAT
        - YANDEX_WEATHER_LON
    primaryEnv: YANDEX_WEATHER_KEY
    emoji: "WEA"
    aliases:
      - yandex weather
      - weather
      - погода
      - прогноз
    tags:
      - weather
      - forecast
      - yandex
      - smarthome
      - погода
      - прогноз
---

# Yandex Weather SmartHome

## Purpose

Use this skill to quickly return the current weather and short forecast for the user's configured home coordinates.

Data source:
- Yandex Weather API (`https://api.weather.yandex.ru/v2/forecast`)

## Activation Rules

Activate automatically when the user asks about:
- current weather ("какая погода", "погода сейчас", "weather now")
- short forecast ("погода на сегодня", "погода на завтра", "forecast today/tomorrow")
- weather conditions ("температура", "ветер", "осадки", "condition", "wind")

If the request is clearly about weather but location is not specified, use configured home coordinates from environment variables (do not ask for coordinates unless user explicitly requests another city/location).

## Security and Secrets

- Never print or expose `YANDEX_WEATHER_KEY`.
- Never store API keys in files.
- Read credentials only from environment variables.
- If key/config is missing, explain what variable is missing in one short sentence.

## Execution Workflow

1. Run the local script:

```bash
python3 ~/.nanobot/workspace/skills/yandex-weather-smarthome/weather.py
```

2. If the user asked for structured/raw output, run:

```bash
python3 ~/.nanobot/workspace/skills/yandex-weather-smarthome/weather.py --json
```

3. Return weather result in Russian using the exact fixed multiline template below.
4. Do not paraphrase, compress, or rewrite labels/sentences.

## Response Style

- Non-technical user-facing text: do not mention headers, endpoints, or internals unless user asks.
- Always include:
  - current temperature
  - feels like
  - condition
  - wind speed
- Include today/tomorrow forecast when available.
- Use clear units (`°C`, `м/с`).

### Strict Output Contract

- Output MUST match the same section names and field labels:
  - `Сейчас` -> `Температура`, `Ощущается как`, `Погода`, `Ветер`
  - `Сегодня` -> `Днём`, `Ночью`, `Описание`
  - `Завтра` -> `Днём`, `Ночью`, `Описание`
- Do not add extra words in headers (forbidden: `Сейчас дома`, `Сейчас у вас`).
- Do not merge multiple fields into one sentence.
- Do not rewrite in narrative style.
- If a value is missing, keep the same label and print `нет данных`.

Required output format (use exactly this structure and labels):

```text
Сейчас:
Температура: 9 °C
Ощущается как: 4 °C
Погода: облачно с прояснениями
Ветер: 4 м/с

Сегодня:
Днём: 12 °C
Ночью: 1 °C
Описание: пасмурно

Завтра:
Днём: 18 °C
Ночью: 7 °C
Описание: небольшой дождь
```

## Error Handling

- If required env var is missing:
  - Return one short action-oriented message naming the missing variable.
- If HTTP/API error:
  - Retry once.
  - If still failing, return: "Не удалось получить погоду сейчас. Попробуйте чуть позже."
- If script returns partial data:
  - Keep the same template and fill missing values as `нет данных`.

## Required Environment Variables

```bash
YANDEX_WEATHER_KEY=<api_key>
YANDEX_WEATHER_LAT=<latitude>
YANDEX_WEATHER_LON=<longitude>
```

## How to get API key (short)

1. Open Yandex Weather SmartHome page and go to personal cabinet registration.
2. Register with phone number and accept the user agreement.
3. After registration, copy API key from the personal cabinet.
4. Export the key as `YANDEX_WEATHER_KEY`.

Official page with FAQ and onboarding:
- https://yandex.ru/pogoda/b2b/smarthome

Example:

```bash
export YANDEX_WEATHER_KEY="your_key"
export YANDEX_WEATHER_LAT="52.721"
export YANDEX_WEATHER_LON="41.452"
```

## Notes

- The script already localizes weather conditions to Russian.
- Default behavior is text output; use `--json` only when structured output is needed.
