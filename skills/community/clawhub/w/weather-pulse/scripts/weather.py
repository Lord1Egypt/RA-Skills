#!/usr/bin/env python3
"""QWeather + WAQI 天气空气质量查询 - 发布版

QWeather 和风天气: now/3d/7d/10d/15d/30d/24h/72h/168h/indices
WAQI 空气质量: aqi (PM2.5/PM10/CO/NO2/O3/SO2/温湿度/气压/预报)

使用方法:
    python weather.py <location> [--endpoint ENDPOINT] [--json]

Location: CityId (101010100) / 经纬度 (116.41,39.92) / 城市名 (xinxiang)
Endpoints: now / 3d / 7d / 10d / 15d / 30d / 24h / 72h / 168h / indices / aqi

使用前配置:
    1. 设置 QW_HOST 和 QW_KEY (和风天气 API)
    2. 设置 WAQI_TOKEN (WAQI 空气质量 API)
    见下方 CONFIG 区域
"""

import argparse
import gzip
import io
import json
import sys
import os
import time
import urllib.error
import urllib.parse
import urllib.request

# ============================================================
# CONFIG - 使用前请填入你的 API 凭证
# ============================================================
# 和风天气: 注册 https://console.qweather.com
#   API Host: 控制台 -> 设置 -> API Host (格式: xxxxxxx.re.qweatherapi.com)
#   API Key : 控制台 -> 项目管理 -> 凭据 -> API KEY (32位字符串)
#   文档: https://dev.qweather.com/docs/start/
# ============================================================
# 免费额度: 50,000 次/月 (天气 + 指数)
# 环境变量名 → 内部变量名:
#   QWEATHER_API_HOST → QW_HOST
#   QWEATHER_API_KEY  → QW_KEY
# ============================================================
QW_HOST = os.environ.get("QWEATHER_API_HOST", "")
QW_KEY  = os.environ.get("QWEATHER_API_KEY", "")

# ============================================================
# 空气质量数据 (WAQI - World Air Quality Index)
#   Token: https://aqicn.org/data-platform/token/#/
#   免费额度: 1,000 次/小时
#   文档: https://aqicn.org/api/
# 环境变量名 → 内部变量名:
#   WAQI_API_TOKEN → WAQI_TOKEN
# ============================================================
WAQI_TOKEN = os.environ.get("WAQI_API_TOKEN", "")


# Windows console encoding fix
if sys.platform == 'win32':
    if hasattr(sys.stdout, 'buffer'):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


QW_ENDPOINTS = {
    'now':   'v7/weather/now',
    '3d':    'v7/weather/3d',
    '7d':    'v7/weather/7d',
    '10d':   'v7/weather/10d',
    '15d':   'v7/weather/15d',
    '30d':   'v7/weather/30d',
    '24h':   'v7/weather/24h',
    '72h':   'v7/weather/72h',
    '168h':  'v7/weather/168h',
}


def _check_config(endpoint_key):
    """检查该端点需要的配置是否填写。"""
    # aqi 端点只需要 WAQI_TOKEN
    if endpoint_key == 'aqi':
        if not WAQI_TOKEN:
            print("错误: WAQI 空气质量 API 需要 WAQI_TOKEN")
            print("请设置环境变量 WAQI_API_TOKEN 或在 CONFIG 区域填写 WAQI_TOKEN")
            print("获取 Token: https://aqicn.org/data-platform/token/#/")
            sys.exit(1)
        return
    # 其他端点（天气相关）只需要和风天气凭证
    if not QW_HOST:
        print("错误: 和风天气 API 需要 QWEATHER_API_HOST")
        print("请设置环境变量 QWEATHER_API_HOST 或在 CONFIG 区域填写 QW_HOST")
        print("获取 API Host+Key: https://console.qweather.com")
        sys.exit(1)
    if not QW_KEY:
        print("错误: 和风天气 API 需要 QWEATHER_API_KEY")
        print("请设置环境变量 QWEATHER_API_KEY 或在 CONFIG 区域填写 QW_KEY")
        sys.exit(1)


MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds


def _resolve_city_name(name):
    """通过 QWeather Geo API 将城市名解析为 CityId."""
    url = f'https://{QW_HOST}/geo/v2/city/lookup'
    params = {'key': QW_KEY, 'location': name}
    data = _json_fetch(url + '?' + urllib.parse.urlencode(params))
    if data.get('code') == '200' and data.get('location'):
        city_id = data['location'][0].get('id')
        if city_id:
            return city_id
    return None


def _normalize_location(loc, endpoint_key):
    """智能标准化 location 输入。

    - "101020100" (纯数字) → CityId，直接返回
    - "116.41,39.92" (经纬度) → 对天气端点转为 CityId，对 AQI 端点转为 geo: 格式
    - "geo:39.92;116.41" (AQI 端点) → 对 AQI 直接返回
    - "Shanghai" (英文/中文城市名) → 对天气端点通过 Geo API 解析
      对 AQI 端点保留原名（WAQI 支持英文城市名）
    - "@5789" (AQI 站ID) → 保留原名
    - "here" (AQI 当前位置) → 保留原名
    """
    # 纯数字 → CityId
    if loc.isdigit():
        return loc

    # AQI 端点专有格式 (@ID, here)
    if endpoint_key == 'aqi':
        return loc  # WAQI 支持 "xinxiang", "@5789", "geo:39.92;116.41", "here"

    # 经纬度格式 "116.41,39.92" 或 "39.92,116.41"（自动检测顺序）
    parts = loc.split(',')
    if len(parts) == 2:
        try:
            v1 = float(parts[0].strip())
            v2 = float(parts[1].strip())
            # QWeather 要求 经度,纬度
            # 如果 v1 > 135 说明是纬度在前（纬度不可能>135），交换一下
            if v1 > 135:
                return f"{v2},{v1}"
            # 中国境内范围验证：经度 73-138，纬度 3-54
            if 73 <= v1 <= 138 and 3 <= v2 <= 54:
                return loc  # 已经是 经度,纬度
            if 3 <= v1 <= 54 and 73 <= v2 <= 138:
                return f"{v2},{v1}"  # 原来是 纬度,经度，交换
            return loc  # 其他区域，假设已经是 经度,纬度
        except ValueError:
            pass

    # geo: 格式 (经纬度另一种写法) → 转为逗号分隔 (经度,纬度)
    if loc.startswith('geo:'):
        geo = loc[4:].replace(';', ',')
        return geo

    # 城市名 → 通过 Geo API 解析为 CityId
    city_id = _resolve_city_name(loc)
    if city_id:
        return city_id

    # 解析失败 → 保持原样（让 API 自己报错）
    return loc


def _json_fetch(url, headers=None):
    """通用 JSON GET (gzip 解压)，支持自动重试 3 次。"""
    req = urllib.request.Request(url)
    req.add_header('Accept-Encoding', 'gzip, deflate')
    if headers:
        for k, v in headers.items():
            req.add_header(k, v)
    last_err = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                raw = resp.read()
                ce = resp.headers.get('Content-Encoding', '')
                if 'gzip' in ce:
                    raw = gzip.decompress(raw)
                return json.loads(raw.decode('utf-8'))
        except (TimeoutError, urllib.error.URLError) as e:
            last_err = str(e)
            if attempt < MAX_RETRIES:
                print(f"[警告] 请求失败 (尝试 {attempt}/{MAX_RETRIES})，{RETRY_DELAY}秒后重试... ({last_err})")
                time.sleep(RETRY_DELAY)
            else:
                print(f"[错误] 请求失败，已重试 {MAX_RETRIES} 次，放弃。({last_err})")
        except urllib.error.HTTPError as e:
            body = e.read().decode('utf-8', errors='replace')
            try:
                return {'error': json.loads(body)}
            except json.JSONDecodeError:
                return {'error': {'status': e.code, 'body': body}}
        except Exception as e:
            last_err = str(e)
            if attempt < MAX_RETRIES:
                print(f"[警告] 请求异常 (尝试 {attempt}/{MAX_RETRIES})，{RETRY_DELAY}秒后重试... ({last_err})")
                time.sleep(RETRY_DELAY)
            else:
                print(f"[错误] 请求异常，已重试 {MAX_RETRIES} 次，放弃。({last_err})")
    return {'error': {'status': 0, 'message': last_err}}


# ============================================================
# QWeather (和风天气) API
# ============================================================
def fetch_qweather(endpoint_key, location, lang='zh', unit='m'):
    """请求和风天气 API."""
    ep = QW_ENDPOINTS.get(endpoint_key, f'v7/{endpoint_key}')
    url = f'https://{QW_HOST}/{ep}'
    params = {'key': QW_KEY, 'location': location, 'lang': lang, 'unit': unit}
    return _json_fetch(url + '?' + urllib.parse.urlencode(params))


# ============================================================
# WAQI (世界空气质量) API
# ============================================================
def fetch_aqi(location):
    """请求 WAQI 空气质量 API.
    location: 城市名(xinxiang) / @ID(5789) / geo:35.30;113.92 / here
    """
    url = f'https://api.waqi.info/feed/{urllib.parse.quote(location)}/?token={WAQI_TOKEN}'
    return _json_fetch(url)


# ============================================================
# 格式化输出
# ============================================================
def format_now(d):
    """实况天气."""
    if 'error' in d:
        return f"Error: {json.dumps(d['error'], ensure_ascii=False)}"
    if d.get('code') != '200':
        return f"API Error: code={d.get('code')} {d.get('status', '')}"
    n = d.get('now', {})
    cloud = n.get('cloud', '?')
    dew = n.get('dew', '?')
    cloud_str = f"  Cloud: {cloud}%" if cloud != '?' else ""
    dew_str = f"  Dew: {dew}C" if dew != '?' else ""
    return (
        f"Obs: {n.get('obsTime', '?')}\n"
        f"Temp: {n.get('temp', '?')}C  Feels: {n.get('feelsLike', '?')}C\n"
        f"Weather: {n.get('text', '?')} [{n.get('icon', '?')}]\n"
        f"Wind: {n.get('windDir', '?')} {n.get('windScale', '?')}  {n.get('windSpeed', '?')}km/h ({n.get('wind360', '?')}deg)\n"
        f"Humidity: {n.get('humidity', '?')}%\n"
        f"Precip(1h): {n.get('precip', '?')}mm\n"
        f"Pressure: {n.get('pressure', '?')}hPa\n"
        f"Visibility: {n.get('vis', '?')}km{cloud_str}{dew_str}"
    )


def format_daily(d):
    """逐日预报."""
    if 'error' in d:
        return f"Error: {json.dumps(d['error'], ensure_ascii=False)}"
    if d.get('code') != '200':
        return f"API Error: code={d.get('code')}"
    lines = []
    for day in d.get('daily', []):
        t_range = f"{day.get('tempMin', '?')} ~ {day.get('tempMax', '?')}C"
        day_w = f"{day.get('textDay', '?')} -> {day.get('textNight', '?')}"
        wind = f"{day.get('windDirDay', '?')}{day.get('windScaleDay', '?')} / {day.get('windDirNight', '?')}{day.get('windScaleNight', '?')}"
        moon = day.get('moonPhase', '')
        moon_str = f"  Moon: {moon}" if moon else ""
        lines.append(
            f"  {day.get('fxDate', '?')} | {t_range} | {day_w} "
            f"| Hum {day.get('humidity', '?')}% | UV {day.get('uvIndex', '?')} "
            f"| Precip {day.get('precip', '?')}mm | {wind} "
            f"| Rise {day.get('sunrise', '?')} Set {day.get('sunset', '?')}{moon_str}"
        )
    return '\n'.join(lines)


def format_hourly(d):
    """逐小时预报."""
    if 'error' in d:
        return f"Error: {json.dumps(d['error'], ensure_ascii=False)}"
    if d.get('code') != '200':
        return f"API Error: code={d.get('code')}"
    lines = []
    for h in d.get('hourly', []):
        fx = h.get('fxTime', '?')
        t = fx[11:16] if 'T' in fx else fx
        lines.append(
            f"  {t} | {h.get('temp', '?')}C | {h.get('text', '?')} "
            f"| Hum {h.get('humidity', '?')}% | {h.get('windDir', '?')}{h.get('windScale', '?')} "
            f"| Pop {h.get('pop', '0')}%  Precip {h.get('precip', '0')}mm"
        )
    return '\n'.join(lines)


def format_indices(d):
    """天气生活指数."""
    if 'error' in d:
        return f"Error: {json.dumps(d['error'], ensure_ascii=False)}"
    if d.get('code') != '200':
        return f"API Error: code={d.get('code')}"
    lines = []
    seen = set()
    for item in d.get('daily', []):
        key = item.get('type')
        if key not in seen:
            seen.add(key)
            name = item.get('name', '?')
            cat = item.get('category', '?')
            txt = item.get('text', '')
            lines.append(f"  {name}: [{cat}] {txt}" if txt else f"  {name}: [{cat}]")
    return '\n'.join(lines)


def _aqi_level(score):
    """AQI 等级."""
    try:
        v = int(score)
    except (ValueError, TypeError):
        return "?"
    if v <= 50:
        return "优"
    elif v <= 100:
        return "良"
    elif v <= 150:
        return "轻度污染"
    elif v <= 200:
        return "中度污染"
    elif v <= 300:
        return "重度污染"
    else:
        return "严重污染"


def format_aqi(d):
    """空气质量 - WAQI."""
    if 'error' in d:
        return f"Error: {json.dumps(d['error'], ensure_ascii=False)}"
    if d.get('status') != 'ok':
        return f"API Error: status={d.get('status')}"
    data = d.get('data', {})
    if not data:
        return "No AQI data"
    aqi = data.get('aqi', '?')
    city = data.get('city', {}).get('name', '?')
    dom = data.get('dominentpol', '?').upper()
    t = data.get('time', {}).get('s', '?')
    ia = data.get('iaqi', {})

    def iq(k):
        """安全获取 iaqi 值."""
        return ia.get(k, {}).get('v', '?')

    lines = [
        f"\n{'='*40}",
        f"AQI: {aqi} [{_aqi_level(aqi)}]  主要污染物: {dom}",
        f"City: {city}",
        f"Time: {t}",
        f"{'-'*40}",
        f"  PM2.5: {iq('pm25')}  PM10: {iq('pm10')}",
        f"  CO: {iq('co')}  NO2: {iq('no2')}  O3: {iq('o3')}  SO2: {iq('so2')}",
        f"  Temp: {iq('t')}C  Hum: {iq('h')}%",
        f"  Pressure: {iq('p')}hPa  Wind: {iq('w')}km/h",
        f"{'='*40}",
    ]

    # Forecast
    fc = data.get('forecast', {}).get('daily', {})
    if fc.get('pm25'):
        lines.append("\nPM2.5 预报:")
        for day in fc['pm25']:
            lines.append(f"  {day.get('day', '?')}: avg={day.get('avg', '?')}  min={day.get('min', '?')}  max={day.get('max', '?')}")
    if fc.get('pm10'):
        lines.append("\nPM10 预报:")
        for day in fc['pm10']:
            lines.append(f"  {day.get('day', '?')}: avg={day.get('avg', '?')}  min={day.get('min', '?')}  max={day.get('max', '?')}")
    if fc.get('uvi') or fc.get('uv') or fc.get('uvi'):
        uv_key = 'uvi' if 'uvi' in fc else 'uv'
        if fc.get(uv_key):
            lines.append(f"\nUV 预报:")
            for day in fc[uv_key]:
                lines.append(f"  {day.get('day', '?')}: avg={day.get('avg', '?')}  max={day.get('max', '?')}")

    return '\n'.join(lines)


# ============================================================
# 主入口
# ============================================================
def main():
    parser = argparse.ArgumentParser(
        description='QWeather + WAQI 天气空气质量查询',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # 新乡实况天气
  python weather.py 101180301

  # 7天预报
  python weather.py 101180301 --endpoint 7d

  # 24小时逐小时
  python weather.py 101180301 --endpoint 24h

  # 15天预报 (经纬度)
  python weather.py 113.92,35.30 --endpoint 15d

  # 天气指数 (感冒/穿衣/紫外线)
  python weather.py 101180301 --endpoint indices

  # 空气质量
  python weather.py xinxiang --endpoint aqi

  # 空气质量 (经纬度)
  python weather.py "geo:35.30;113.92" --endpoint aqi

  # 原始 JSON 输出
  python weather.py 101180301 --json
"""
    )
    parser.add_argument('location',
                        help='位置: CityId (101180301) / 经纬度 (113.92,35.30) / 城市名 (xinxiang, aqi端点可)')
    parser.add_argument('--endpoint', default='now',
                        help='端点: now/3d/7d/10d/15d/30d/24h/72h/168h/indices/aqi (默认: now)')
    parser.add_argument('--lang', default='zh', help='语言: zh/en/ja')
    parser.add_argument('--unit', default='m', help='单位: m(公制)/i(英制)')
    parser.add_argument('--json', action='store_true', help='原始 JSON 输出')
    args = parser.parse_args()

    ep = args.endpoint

    # 检查该端点需要的配置
    _check_config(ep)

    # 智能解析 location（天气端点：英文/中文城市名 → CityId；AQI 端点：保持原样）
    resolved_location = _normalize_location(args.location, ep)

    # 调用 API
    if ep == 'aqi':
        data = fetch_aqi(resolved_location)
    elif ep == 'indices':
        url = f'https://{QW_HOST}/v7/indices/1d'
        params = {'key': QW_KEY, 'location': resolved_location,
                  'lang': args.lang, 'unit': args.unit, 'type': '0'}
        data = _json_fetch(url + '?' + urllib.parse.urlencode(params))
    else:
        data = fetch_qweather(ep, resolved_location, args.lang, args.unit)

    # 输出
    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return

    fmt_map = {
        'now':   format_now,
        '3d':    format_daily, '7d': format_daily, '10d': format_daily,
        '15d':   format_daily, '30d': format_daily,
        '24h':   format_hourly, '72h': format_hourly, '168h': format_hourly,
        'indices': format_indices,
        'aqi':   format_aqi,
    }
    formatter = fmt_map.get(ep)
    if formatter:
        print(formatter(data))
    else:
        print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
