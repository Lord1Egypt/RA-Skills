#!/usr/bin/env python3
"""Weather Query Skill - wttr.in based example with offline mode."""
from __future__ import annotations

import json
import sys
import urllib.parse
import urllib.request
from typing import Any

OFFLINE_SAMPLE = {
    'current_condition': [
        {
            'temp_C': '15',
            'temp_F': '59',
            'humidity': '45',
            'weatherDesc': [{'value': '晴朗'}],
            'windspeedKmph': '12',
            'observation_time': '09:00',
        }
    ]
}


def parse_weather_payload(city: str, data: dict[str, Any]) -> dict[str, str]:
    current = data['current_condition'][0]
    return {
        'city': city,
        'temp_c': current['temp_C'],
        'temp_f': current['temp_F'],
        'humidity': current['humidity'],
        'weather': current['weatherDesc'][0]['value'],
        'wind': f"{current['windspeedKmph']} km/h",
        'observed': current['observation_time'],
    }


def get_weather(city: str, *, offline: bool = False, timeout: int = 10) -> dict[str, str]:
    try:
        if offline:
            return parse_weather_payload(city, OFFLINE_SAMPLE)

        encoded_city = urllib.parse.quote(city)
        url = f'http://wttr.in/{encoded_city}?format=j1'
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})

        with urllib.request.urlopen(req, timeout=timeout) as response:
            data = json.loads(response.read().decode('utf-8'))
        return parse_weather_payload(city, data)
    except Exception as exc:
        return {'error': str(exc)}


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    if not args:
        print(json.dumps({'error': '请提供城市名，如：python weather.py 北京'}, ensure_ascii=False))
        return 1

    city = args[0]
    offline = '--offline' in args[1:]
    print(json.dumps(get_weather(city, offline=offline), ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
