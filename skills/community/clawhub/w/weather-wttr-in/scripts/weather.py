#!/usr/bin/env python3
"""
weather-wttr.in - Free weather data from wttr.in
No API key required, no pip packages needed.
Cross-platform: Windows / macOS / Linux (Python 3.6+)

Usage:
    python weather.py [location] [--json] [--today] [--lang=zh]
"""

import sys
import json
import io
import time

# ─── Cross-platform console encoding fix ───
if sys.platform == 'win32':
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    except (AttributeError, OSError):
        pass
    try:
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    except (AttributeError, OSError):
        pass
else:
    try:
        if sys.stdout.encoding and sys.stdout.encoding.lower() not in ('utf-8', 'utf8'):
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    except (AttributeError, OSError):
        pass

from urllib.request import Request, urlopen
from urllib.error import URLError
from urllib.parse import quote

MAX_RETRIES = 3
RETRY_DELAY = 1
TIMEOUT = 15
BASE_URL = "https://wttr.in"
UA = "Mozilla/5.0 (compatible; OpenClaw-weather-Skill/1.0)"


def http_get_json(url, lang='zh'):
    """GET JSON with retries + language support."""
    full_url = f"{url}&lang={lang}"
    last_err = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            req = Request(full_url, headers={
                "User-Agent": UA,
                "Accept": "application/json",
            })
            with urlopen(req, timeout=TIMEOUT) as resp:
                raw = resp.read()
                encoding = resp.headers.get('charset', 'utf-8')
                return json.loads(raw.decode(encoding, errors='replace'))
        except (URLError, TimeoutError, OSError) as e:
            last_err = str(e)
            if attempt < MAX_RETRIES:
                print(f"  [wttr.in] retry {attempt}/{MAX_RETRIES}: {last_err}", file=sys.stderr)
                time.sleep(RETRY_DELAY)
    print(f"  [wttr.in] failed after {MAX_RETRIES} tries: {last_err}", file=sys.stderr)
    return None


def _safe(data, *keys, default='?'):
    """Safe nested dict/list access."""
    d = data
    for k in keys:
        if isinstance(d, dict):
            d = d.get(k, default)
        elif isinstance(d, list) and isinstance(k, int) and k < len(d):
            d = d[k]
        else:
            return default
    return d if d is not None else default


def _weather_text(item):
    """Extract weather description from current_condition."""
    if not isinstance(item, dict):
        return '?'
    wd = item.get('weatherDesc', [])
    if isinstance(wd, list) and wd and isinstance(wd[0], dict):
        first = wd[0]
        for lang in ('lang_zh', 'lang_en', 'value'):
            entries = first.get(lang, [])
            if isinstance(entries, list) and entries:
                t = entries[0].get('value', '')
                if t:
                    return t
        return first.get('value', '?')
    return item.get('weather', '?')


def format_now(d):
    """实况天气格式化."""
    if not d:
        return "❌ 无法获取天气数据"

    cc = _safe(d, 'current_condition', 0)
    if not isinstance(cc, dict):
        return "❌ 天气数据格式异常"

    city = _safe(d, 'nearest_area', 0, 'areaName', 0, 'value', default='')
    region = _safe(d, 'nearest_area', 0, 'region', 0, 'value', default='')
    country = _safe(d, 'nearest_area', 0, 'country', 0, 'value', default='')
    if not city:
        city = _safe(d, 'request', 0, 'query', default='')
    if not city:
        city = ''
    area_parts = [p for p in [city.strip(), region.strip(), country.strip()] if p and p != '?']
    area_str = ', '.join(area_parts) if area_parts else ''

    temp = _safe(cc, 'temp_C')
    feels = _safe(cc, 'FeelsLikeC')
    weather_text = _weather_text(cc)
    wind_kmh = _safe(cc, 'windspeedKmph', default='')
    wind_deg = _safe(cc, 'winddirDegree', default='')
    wind_pt = _safe(cc, 'winddir16Point', default='')
    wind_scale = _safe(cc, 'windScale', default='')
    if wind_scale == '?' or wind_scale == '':
        try:
            k = float(wind_kmh) if wind_kmh else 0
            wind_scale = str(int(k / 3.5 + 0.5) if k > 0 else 0)
        except (ValueError, TypeError):
            wind_scale = '?'
    uv = _safe(cc, 'uvIndex')
    hum = _safe(cc, 'humidity')
    vis = _safe(cc, 'visibility')
    cloud = _safe(cc, 'cloudcover', default='')
    precip = _safe(cc, 'precipMM', default='')
    pressure = _safe(cc, 'pressure')
    obs = _safe(cc, 'localObsDateTime', 'observation_time', default='')

    lines = [f"🌡️ 实况: {temp}°C  体感: {feels}°C {weather_text}"]
    lines.append(f"💧 湿度: {hum}%  💨 风: {wind_pt} {wind_scale}级 {wind_kmh}km/h")
    if vis and vis != '?' and vis != '':
        lines.append(f"👁️ 能见度: {vis}km  ☁️ 云量: {cloud}%")
    if precip and precip != '0.0':
        lines.append(f"🌧️ 降水: {precip}mm")
    if area_str:
        lines.append(f"📍 {area_str}  ⏰ {obs}")
    return '\n'.join(lines)


def format_daily(d, show_hourly=False):
    """3天逐日预报."""
    days = d.get('weather', [])
    if not days:
        return format_now(d)

    lines = []
    for day in days:
        date = day.get('date', '?')
        tmin = _safe(day, 'mintempC', default='?')
        tmax = _safe(day, 'maxtempC', default='?')
        # Day condition from first hourly
        hours = day.get('hourly', [])
        day_txt = _safe(hours, 0, 'weatherDesc', 0, 'value', default='?')
        night_txt = _safe(hours, -1, 'weatherDesc', 0, 'value', default='?')
        uv = _safe(day, 'uvIndex', default='?')
        astro = _safe(days, 0, 'astronomy', 0, default={}) if day == days[0] else {}
        rise = _safe(day, 'astronomy', 0, 'sunrise', default='?')
        set_ = _safe(day, 'astronomy', 0, 'sunset', default='?')

        if max_uv := max((_safe(h, 'uvIndex', default='0') for h in hours), default='?'):
            try:
                uv = str(max(int(x) for x in [_safe(h, 'uvIndex', default='0') for h in hours if _safe(h, 'uvIndex', default='0') != '?']))
            except (ValueError, TypeError):
                uv = max_uv

        lines.append(f"📅 {date} | {tmin}°C ~ {tmax}°C | {day_txt} → {night_txt}")
        lines.append(f"  ☀️ UV: {uv} | 🌅 日出: {rise}  日落: {set_}")

        if show_hourly and hours:
            for h in hours:
                tm = h.get('time', '?')
                t_str = f"{tm[:2]}:{tm[2:]}" if len(tm) == 4 else tm
                tmp = _safe(h, 'tempC', default='?')
                cond = _safe(h, 'weatherDesc', 0, 'value', default='?')
                hh = _safe(h, 'humidity', default='?')
                wd = _safe(h, 'windspeedKmph', default='?')
                cr = _safe(h, 'chanceofrain', default='0')
                lines.append(f"  {t_str} | {tmp}°C {cond} | 湿{hh}% | 风{wd}km/h | 雨{cr}%")
        lines.append("")

    return '\n'.join(lines)


def main():
    location = None
    json_mode = False
    lang = 'zh'
    show_daily = False

    args = sys.argv[1:]
    for arg in args:
        if arg in ('--json', '-j'):
            json_mode = True
        elif arg.startswith('--lang='):
            lang = arg.split('=', 1)[1]
        elif arg in ('--today', '-t', '--forecast', '-f'):
            show_daily = True
        elif arg in ('--help', '-h'):
            print(__doc__)
            sys.exit(0)
        elif location is None:
            location = arg

    loc = location or ''
    url = f"{BASE_URL}/{quote(loc)}?format=j1" if loc else f"{BASE_URL}/?format=j1"

    data = http_get_json(url, lang=lang)
    if not data:
        print("❌ 无法获取天气数据，请稍后重试", file=sys.stderr)
        sys.exit(1)

    if json_mode:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    elif show_daily:
        print(format_now(data))
        print()
        print(format_daily(data, show_hourly=False))
    else:
        print(format_now(data))
        print()
        print(format_daily(data, show_hourly=True))


if __name__ == '__main__':
    main()
