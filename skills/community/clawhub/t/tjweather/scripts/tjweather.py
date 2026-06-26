#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import json
import os
import urllib.parse
import urllib.request
from datetime import datetime, timedelta

def get_weather_data(lon, lat, fcst_days=3, tz=8):
    """调用 TJWeather API 获取天气数据"""
    api_key = os.environ.get('TJWEATHER_API_KEY')
    
    # 兜底：如果环境变量未注入，尝试从同级目录的 .env 文件加载
    if not api_key:
        env_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env')
        try:
            with open(env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('TJWEATHER_API_KEY='):
                        api_key = line.split('=', 1)[1].strip()
                        break
        except FileNotFoundError:
            pass
    
    if not api_key:
        print("❌ 错误: 未找到 TJWEATHER_API_KEY，请在 openclaw.json 或 .env 中配置", file=sys.stderr)
        return None

    fields = "t2m,ws10m,wd10m,psz,tp,rh2m"
    # 注意：API 参数 tz 允许用户获取对应时区的时间戳
    # TJWeather 经度格式为 0-360，将 WGS84 负数经度（西半球）自动转换
    lon_val = float(lon)
    if lon_val < 0:
        lon_val = lon_val + 360
    url = f"https://api.tjweather.com/beta?loc={lon_val},{lat}&key={api_key}&fields={fields}&fcst_days={fcst_days}&tz={tz}"
    
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode('utf-8'))
            
        code = str(data.get('code', '200'))
        if code == '200':
            return data
        
        # 简化错误码解析
        msg = data.get('message', 'Unknown error')
        print(f'❌ API 错误 (代码: {code}): {msg}', file=sys.stderr)
        return None
    except Exception as e:
        print(f"❌ 天气查询请求失败: {e}", file=sys.stderr)
        return None

def get_wind_direction_16(degree):
    """将角度转换为16方位风向"""
    names = ["北风", "北东北风", "东北风", "东东北风", "东风", "东东南风", "东南风", "南东南风",
             "南风", "南西南风", "西南风", "西南西风", "西风", "西西北风", "西北风", "北西北风"]
    idx = int((degree + 11.25) // 22.5) % 16
    return names[idx]

def format_weather_output(weather_data, lon, lat, name, original_query):
    """根据当地时区日期统计格式化输出"""
    records = weather_data.get('data', {}).get('data', [])
    if not records:
        return "❌ 未获取到有效天气数据。"

    # 按当地日期分组
    daily_groups = {}
    for r in records:
        time_str = r.get('time', '') # 预期格式: 2026-03-24T19:00+08:00
        if not time_str:
            continue
        try:
            # 提取日期 (T 之前的部分)
            date_part = time_str.split('T')[0]
            # 提取小时用于判断 00-23
            time_part = time_str.split('T')[1]
            hour_part = int(time_part.split(':')[0])
            
            # 由于 API 已经按照传入的 tz 处理了 time 字符串，
            # 我们直接使用该字符串作为“当地日期”。
            if 0 <= hour_part <= 23:
                if date_part not in daily_groups:
                    daily_groups[date_part] = []
                daily_groups[date_part].append(r)
        except (IndexError, ValueError):
            continue
    
    sorted_dates = sorted(daily_groups.keys())
    # 按照预定的格式要求
    header = f"您查询的 {original_query} 匹配到 {name}，经度：{lon}, 纬度：{lat}"
    lines = [header]
    
    for date_str in sorted_dates:
        day_records = daily_groups[date_str]
        t2ms = [r['t2m'] for r in day_records if 't2m' in r]
        wss = [r['ws10m'] for r in day_records if 'ws10m' in r]
        wds = [r['wd10m'] for r in day_records if 'wd10m' in r]
        tps = [r['tp'] for r in day_records if 'tp' in r]
        rhs = [r['rh2m'] for r in day_records if 'rh2m' in r]
        
        if not t2ms: continue
        
        t_max, t_min = max(t2ms), min(t2ms)
        ws_avg = sum(wss) / len(wss) if wss else 0
        tp_sum = sum(tps) if tps else 0
        rh_avg = sum(rhs) / len(rhs) if rhs else 0
        
        dominant_wd = "无数据"
        if wds:
            wd_names = [get_wind_direction_16(deg) for deg in wds]
            dominant_wd = max(set(wd_names), key=wd_names.count)
        
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        weekdays = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
        
        lines.append(f"\n📅 {dt.year}年{dt.month}月{dt.day}日 {weekdays[dt.weekday()]}")
        lines.append(f"🌡️ 气温: {t_min:.1f}°C ~ {t_max:.1f}°C")
        lines.append(f"💨 平均风速: {ws_avg:.1f} 米/秒 / 主风向: {dominant_wd}")
        lines.append(f"🌧️ 降水: {f'日累积降水 {tp_sum:.1f} 毫米' if tp_sum > 0 else '无'}")
        lines.append(f"💧 日平均相对湿度: {rh_avg:.1f}%")

    return "\n".join(lines)

def main():
    # 参数: lon, lat, name, original_query, fcst_days, tz
    if len(sys.argv) < 7:
        print("用法: python3 tjweather.py <lon> <lat> <name> <original_query> <fcst_days> <tz>", file=sys.stderr)
        sys.exit(1)
        
    try:
        lon = sys.argv[1]
        lat = sys.argv[2]
        name = sys.argv[3]
        original_query = sys.argv[4]
        fcst_days = int(sys.argv[5])
        tz = int(sys.argv[6])
        
        # 预报天数限制逻辑
        if fcst_days > 10:
            print(f"⚠️ 注意：由于测试版本限制，目前仅提供最长 10 天预报（原请求 {fcst_days} 天）。", file=sys.stderr)
            print("💡 如需更长预报天数，请联系 tjweather.com 获取商业授权。", file=sys.stderr)
            fcst_days = 10
            
    except ValueError:
        print("❌ 参数格式错误", file=sys.stderr)
        sys.exit(1)
            
    # 查询天气
    weather_result = get_weather_data(lon, lat, fcst_days, tz)
    
    if not weather_result:
        sys.exit(1)
        
    # 统计并格式化输出
    formatted_output = format_weather_output(weather_result, lon, lat, name, original_query)
    print(formatted_output)

if __name__ == "__main__":
    main()
