#!/usr/bin/env python3
import json
import os
import argparse
from urllib import request, parse, error

API_URL = "https://api.weather.yandex.ru/v2/forecast"

CONDITION_RU = {
    "clear": "ясно",
    "partly-cloudy": "малооблачно",
    "cloudy": "облачно с прояснениями",
    "overcast": "пасмурно",
    "drizzle": "морось",
    "light-rain": "небольшой дождь",
    "rain": "дождь",
    "moderate-rain": "умеренный дождь",
    "heavy-rain": "сильный дождь",
    "continuous-heavy-rain": "проливной дождь",
    "showers": "ливень",
    "wet-snow": "дождь со снегом",
    "light-snow": "небольшой снег",
    "snow": "снег",
    "snow-showers": "снегопад",
    "hail": "град",
    "thunderstorm": "гроза",
    "thunderstorm-with-rain": "гроза с дождём",
    "thunderstorm-with-hail": "гроза с градом",
}


def getenv_required(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Environment variable {name} is not set")
    return value


def fetch_weather():
    key = getenv_required("YANDEX_WEATHER_KEY")
    lat = getenv_required("YANDEX_WEATHER_LAT")
    lon = getenv_required("YANDEX_WEATHER_LON")

    params = parse.urlencode({
        "lat": lat,
        "lon": lon,
        "lang": "ru_RU",
        "limit": 2,
        "hours": "false",
    })

    url = f"{API_URL}?{params}"

    req = request.Request(url, headers={
        "X-Yandex-Weather-Key": key,
        "Accept": "application/json",
    })

    try:
        with request.urlopen(req, timeout=20) as resp:
            payload = resp.read().decode("utf-8", errors="replace")
    except error.HTTPError as e:
        payload = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP error {e.code}: {payload}")

    return json.loads(payload)


def cond(code):
    return CONDITION_RU.get(code, code)


def build_result(data):
    fact = data.get("fact", {})
    forecasts = data.get("forecasts", [])

    result = {
        "now": {
            "temp": fact.get("temp"),
            "feels_like": fact.get("feels_like"),
            "condition": cond(fact.get("condition")),
            "wind_speed": fact.get("wind_speed"),
        }
    }

    if forecasts:
        today = forecasts[0]
        parts = today.get("parts", {})
        result["today"] = {
            "day_temp": parts.get("day", {}).get("temp_max"),
            "night_temp": parts.get("night", {}).get("temp_min"),
            "condition": cond(parts.get("day", {}).get("condition")),
        }

    if len(forecasts) > 1:
        tomorrow = forecasts[1]
        parts = tomorrow.get("parts", {})
        result["tomorrow"] = {
            "day_temp": parts.get("day", {}).get("temp_max"),
            "night_temp": parts.get("night", {}).get("temp_min"),
            "condition": cond(parts.get("day", {}).get("condition")),
        }

    return result


def print_text(res):
    now = res.get("now", {})

    print("Сейчас:")
    print(f"Температура: {now.get('temp')} °C")
    print(f"Ощущается как: {now.get('feels_like')} °C")
    print(f"Погода: {now.get('condition')}")
    print(f"Ветер: {now.get('wind_speed')} м/с")

    if "today" in res:
        t = res["today"]
        print("\nСегодня:")
        print(f"Днём: {t.get('day_temp')} °C")
        print(f"Ночью: {t.get('night_temp')} °C")
        print(f"Описание: {t.get('condition')}")

    if "tomorrow" in res:
        t = res["tomorrow"]
        print("\nЗавтра:")
        print(f"Днём: {t.get('day_temp')} °C")
        print(f"Ночью: {t.get('night_temp')} °C")
        print(f"Описание: {t.get('condition')}")


def main():
    parser = argparse.ArgumentParser(description="Yandex Weather SmartHome")
    parser.add_argument("--json", action="store_true", help="Output JSON instead of text")
    args = parser.parse_args()

    try:
        data = fetch_weather()
        result = build_result(data)

        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print_text(result)

    except Exception as e:
        err = {"ok": False, "error": str(e)}
        if args.json:
            print(json.dumps(err, ensure_ascii=False))
        else:
            print(f"Ошибка получения погоды: {e}")


if __name__ == "__main__":
    main()
