#!/usr/bin/env python3
import argparse
import gzip
import json
import urllib.error
import urllib.parse
import urllib.request
from os import environ
from typing import Any, Dict, List


WEATHER_ICON_MAP = {
    "100": "\u2600\ufe0f",
    "101": "\ud83c\udf24\ufe0f",
    "102": "\u26c5",
    "103": "\ud83c\udf25\ufe0f",
    "104": "\u2601\ufe0f",
    "150": "\ud83c\udf19",
    "151": "\ud83c\udf24\ufe0f",
    "152": "\u2601\ufe0f",
    "300": "\ud83c\udf26\ufe0f",
    "301": "\u26c8\ufe0f",
    "302": "\u26a1",
    "303": "\u26c8\ufe0f",
    "304": "\ud83c\udf28\ufe0f",
    "305": "\ud83c\udf27\ufe0f",
    "306": "\ud83c\udf27\ufe0f",
    "307": "\ud83c\udf27\ufe0f",
    "308": "\ud83c\udf27\ufe0f",
    "309": "\ud83c\udf26\ufe0f",
    "310": "\ud83c\udf27\ufe0f",
    "311": "\ud83c\udf27\ufe0f",
    "312": "\ud83c\udf27\ufe0f",
    "313": "\ud83c\udf28\ufe0f",
    "314": "\ud83c\udf27\ufe0f",
    "315": "\ud83c\udf27\ufe0f",
    "316": "\ud83c\udf27\ufe0f",
    "317": "\ud83c\udf27\ufe0f",
    "318": "\ud83c\udf27\ufe0f",
    "399": "\ud83c\udf27\ufe0f",
    "400": "\ud83c\udf28\ufe0f",
    "401": "\ud83c\udf28\ufe0f",
    "402": "\u2744\ufe0f",
    "403": "\u2744\ufe0f",
    "404": "\ud83c\udf28\ufe0f",
    "405": "\ud83c\udf28\ufe0f",
    "406": "\ud83c\udf28\ufe0f",
    "407": "\ud83c\udf28\ufe0f",
    "408": "\ud83c\udf28\ufe0f",
    "409": "\u2744\ufe0f",
    "410": "\u2744\ufe0f",
    "499": "\ud83c\udf28\ufe0f",
    "500": "\ud83c\udf2b\ufe0f",
    "501": "\ud83c\udf2b\ufe0f",
    "502": "\ud83d\ude37",
    "503": "\ud83c\udf2a\ufe0f",
    "504": "\ud83c\udf2a\ufe0f",
    "507": "\ud83c\udf2a\ufe0f",
    "508": "\ud83c\udf2a\ufe0f",
    "509": "\ud83c\udf2b\ufe0f",
    "510": "\ud83c\udf2b\ufe0f",
    "511": "\ud83d\ude37",
    "512": "\ud83d\ude37",
    "513": "\ud83d\ude37",
    "514": "\ud83c\udf2b\ufe0f",
    "515": "\ud83c\udf2b\ufe0f",
    "900": "\ud83d\udd25",
    "901": "\u2744\ufe0f",
    "999": "\ud83c\udf21\ufe0f",
}


def fail(message: str, status: int = 1) -> None:
    payload = {"success": False, "error": message}
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    raise SystemExit(status)


def get_api_key(explicit_key: str | None) -> str:
    key = explicit_key or environ.get("QWEATHER_API_KEY")
    if not key:
        fail("Missing API key. Set --api-key or QWEATHER_API_KEY.")
    return key


def get_api_host(explicit_host: str | None) -> str:
    host = explicit_host or environ.get("QWEATHER_API_HOST")
    if not host:
        fail("Missing API host. Set --api-host or QWEATHER_API_HOST.")
    return host


def request_json(url: str, api_key: str, timeout_s: float) -> Dict[str, Any]:
    req = urllib.request.Request(
        url,
        headers={
            "X-QW-Api-Key": api_key,
            "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate",
            "User-Agent": "qweather-city-weather-skill/1.0",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout_s) as resp:
            body = resp.read()
            encoding = (resp.headers.get("Content-Encoding") or "").lower()
    except urllib.error.HTTPError as exc:
        fail(f"HTTP {exc.code} calling {url}")
    except urllib.error.URLError as exc:
        fail(f"Network error calling {url}: {exc.reason}")
    except TimeoutError:
        fail(f"Timeout calling {url}")

    if "gzip" in encoding:
        try:
            body = gzip.decompress(body)
        except OSError:
            fail("Failed to decompress gzip response from QWeather.")

    try:
        raw = body.decode("utf-8")
    except UnicodeDecodeError:
        fail("Failed to decode response body as UTF-8.")

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        fail("Failed to parse JSON from QWeather response.")

    code = data.get("code")
    if code != "200":
        fail(f"QWeather API returned code={code}")
    return data


def search_city(query: str, api_key: str, api_host: str, timeout_s: float, number: int) -> List[Dict[str, Any]]:
    encoded = urllib.parse.quote(query)
    url = f"https://{api_host}/geo/v2/city/lookup?location={encoded}&number={number}"
    data = request_json(url, api_key, timeout_s)
    locations = data.get("location") or data.get("city") or []
    if not isinstance(locations, list):
        return []
    return locations


def get_weather(location: str, api_key: str, api_host: str, timeout_s: float) -> Dict[str, Any]:
    encoded = urllib.parse.quote(location)
    url = f"https://{api_host}/v7/weather/now?location={encoded}"
    data = request_json(url, api_key, timeout_s)
    now = data.get("now") or {}
    icon_code = str(now.get("icon", ""))
    return {
        "location": location,
        "text": now.get("text", ""),
        "iconCode": icon_code,
        "icon": WEATHER_ICON_MAP.get(icon_code, "\ud83c\udf21\ufe0f"),
        "temp": now.get("temp"),
        "feelsLike": now.get("feelsLike"),
        "humidity": now.get("humidity"),
        "windDir": now.get("windDir"),
        "windScale": now.get("windScale"),
        "obsTime": now.get("obsTime"),
    }


def pick_location(locations: List[Dict[str, Any]], preferred_name: str | None) -> Dict[str, Any]:
    if not locations:
        fail("No matching city found.")
    if preferred_name:
        target = preferred_name.strip().lower()
        for loc in locations:
            name = str(loc.get("name", "")).strip().lower()
            if name == target:
                return loc
    return locations[0]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="QWeather city code and weather query utility."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--api-key", help="QWeather API key (or QWEATHER_API_KEY env).")
    common.add_argument("--api-host", help="QWeather API host (or QWEATHER_API_HOST env).")
    common.add_argument("--timeout", type=float, default=5.0, help="HTTP timeout in seconds.")

    city = subparsers.add_parser("search-city", parents=[common], help="Search city and return location IDs.")
    city.add_argument("--query", required=True, help="City keyword.")
    city.add_argument("--number", type=int, default=10, help="Max returned cities.")

    weather = subparsers.add_parser("get-weather", parents=[common], help="Get now weather by location ID.")
    weather.add_argument("--location", required=True, help="QWeather location ID or city string.")

    combo = subparsers.add_parser(
        "city-weather", parents=[common], help="Search city then fetch weather using selected location ID."
    )
    combo.add_argument("--query", required=True, help="City keyword.")
    combo.add_argument("--number", type=int, default=10, help="Max returned cities.")
    combo.add_argument(
        "--preferred-name",
        help="Exact city name to prefer when multiple cities are returned.",
    )

    return parser.parse_args()


def run() -> None:
    args = parse_args()
    api_key = get_api_key(args.api_key)
    api_host = get_api_host(args.api_host)

    if args.command == "search-city":
        locations = search_city(args.query, api_key, api_host, args.timeout, args.number)
        payload = {
            "success": True,
            "query": args.query,
            "count": len(locations),
            "locations": locations,
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return

    if args.command == "get-weather":
        weather = get_weather(args.location, api_key, api_host, args.timeout)
        payload = {"success": True, "weather": weather}
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return

    if args.command == "city-weather":
        locations = search_city(args.query, api_key, api_host, args.timeout, args.number)
        selected = pick_location(locations, args.preferred_name)
        location_id = str(selected.get("id", "")).strip()
        if not location_id:
            fail("Selected city has no location id.")
        weather = get_weather(location_id, api_key, api_host, args.timeout)
        # Remove emoji from weather output to avoid encoding issues
        weather_output = {k: v for k, v in weather.items() if k != "icon"}
        payload = {
            "success": True,
            "query": args.query,
            "selectedLocation": {
                "id": location_id,
                "name": selected.get("name"),
                "country": selected.get("country"),
                "adm1": selected.get("adm1"),
                "adm2": selected.get("adm2"),
                "lat": selected.get("lat"),
                "lon": selected.get("lon"),
            },
            "weather": weather_output,
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return

    fail(f"Unknown command: {args.command}")


if __name__ == "__main__":
    run()
