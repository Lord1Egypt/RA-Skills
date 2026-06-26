#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
天气查询脚本 - 从中国天气网获取天气信息
Usage: python weather_query.py <city_code>
Example: python weather_query.py 101010100  # 北京
"""

import sys
import os

# 确保标准输出使用 UTF-8 编码
if sys.stdout.encoding != 'utf-8':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
if sys.stderr.encoding != 'utf-8':
    import io
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

import urllib.request
import urllib.error
import re
import json
from html import unescape


def fetch_weather_page(city_code: str) -> str:
    """获取天气网页面内容"""
    url = f"http://www.weather.com.cn/weather/{city_code}.shtml"
    
    try:
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            }
        )
        with urllib.request.urlopen(req, timeout=15) as response:
            return response.read().decode('utf-8')
    except urllib.error.URLError as e:
        print(f"错误：无法连接天气网 - {e}")
        sys.exit(1)
    except Exception as e:
        print(f"错误：{e}")
        sys.exit(1)


def parse_weather_info(html: str) -> dict:
    """解析天气信息"""
    result = {
        'city': '',
        'today': {},
        'forecast': []
    }
    
    # 提取城市名 - 从 title 标签
    city_match = re.search(r'<title>\s*([^\s,]+)\s*天气预报', html)
    if city_match:
        result['city'] = city_match.group(1).strip()
    
    # 提取今日天气 - 从 hidden_title (新格式)
    hidden_title = re.search(r'<input type="hidden" id="hidden_title" value="([^"]+)"', html)
    if hidden_title:
        # 解析：03 月 07 日 20 时 周六  阴转晴  -1/13°C
        hidden_value = hidden_title.group(1)
        parts = hidden_value.split()
        
        # 提取日期
        if len(parts) >= 3:
            result['today']['date'] = parts[0] + parts[1] + parts[2]
        
        # 提取天气（中间部分）
        for i, part in enumerate(parts):
            if '晴' in part or '阴' in part or '雨' in part or '雪' in part or '多云' in part or '雾' in part:
                result['today']['weather'] = part
                break
        
        # 提取温度（最后一部分）
        if parts:
            temp_part = parts[-1]
            if '°C' in temp_part:
                result['today']['temp'] = temp_part.replace('°C', '')
    
    # 备用方案：查找天气现象（旧格式）
    if 'weather' not in result['today']:
        weather_matches = re.findall(r'<p class="wea">([^<]+)</p>', html)
        if weather_matches:
            result['today']['weather'] = weather_matches[0].strip()
    
    # 备用方案：查找温度（旧格式）
    if 'temp' not in result['today']:
        temp_matches = re.findall(r'<p class="tem">([^<]+)</p>', html)
        if temp_matches:
            result['today']['temp'] = temp_matches[0].strip()
    
    # 查找风力（旧格式）
    if 'wind' not in result['today']:
        wind_matches = re.findall(r'<p class="win"><i></i>([^<]+)</p>', html)
        if not wind_matches:
            wind_matches = re.findall(r'<p class="win">([^<]+)</p>', html)
        if wind_matches:
            result['today']['wind'] = wind_matches[0].strip()
    
    # 查找生活指数
    indices = []
    # 尝试匹配生活指数列表
    index_blocks = re.findall(r'<li>\s*<span class="title">([^<]+)</span>\s*<span class="level">([^<]+)</span>\s*<p>([^<]+)</p>', html, re.DOTALL)
    
    for title, level, desc in index_blocks[:6]:
        indices.append({
            'name': unescape(title.strip()),
            'level': unescape(level.strip()),
            'desc': unescape(desc.strip())[:50]
        })
    
    # 如果没找到，尝试另一种格式
    if not indices:
        index_matches = re.findall(r'<dt>([^<]+)</dt>\s*<dd[^>]*>([^<]+)</dd>', html)
        for title, desc in index_matches[:6]:
            indices.append({
                'name': unescape(title.strip()),
                'level': '',
                'desc': unescape(desc.strip())[:50]
            })
    
    result['today']['indices'] = indices
    
    return result


def get_clothing_advice(temp_range: str, weather: str) -> str:
    """根据温度范围和天气给出穿衣建议"""
    # 解析温度
    temps = re.findall(r'-?\d+', temp_range)
    if len(temps) >= 2:
        low = int(temps[0])
        high = int(temps[1])
        avg = (low + high) / 2
    else:
        avg = 15  # 默认
    
    advice = []
    
    # 根据温度给建议
    if avg >= 28:
        advice.append("建议穿短袖、短裤、裙子等夏季服装")
    elif avg >= 22:
        advice.append("建议穿薄衬衫、T 恤、薄外套等春秋服装")
    elif avg >= 15:
        advice.append("建议穿外套、毛衣、薄夹克等服装")
    elif avg >= 8:
        advice.append("建议穿厚外套、毛衣、风衣等保暖服装")
    elif avg >= 0:
        advice.append("建议穿厚羽绒服、棉衣、保暖内衣等冬季服装")
    else:
        advice.append("建议穿厚羽绒服、棉衣、保暖内衣，戴帽子围巾手套等隆冬装备")
    
    # 根据天气补充建议
    if '雨' in weather or '雪' in weather:
        advice.append("有降水，请携带雨具，穿防滑防水的鞋子")
    if '雪' in weather and avg < 0:
        advice.append("路面可能结冰，注意防滑")
    if '雾' in weather or '霾' in weather:
        advice.append("能见度较低，外出注意交通安全，敏感人群佩戴口罩")
    if '多云' in weather or '晴' in weather:
        advice.append("天气较好，适宜户外活动")
    
    return "；".join(advice)


def format_output(data: dict) -> str:
    """格式化输出"""
    lines = []
    
    if data['city']:
        lines.append(f"📍 城市：{data['city']}")
        lines.append("")
    
    if data['today']:
        lines.append("📅 今日天气")
        weather = data['today'].get('weather', '未知')
        temp = data['today'].get('temp', '未知')
        wind = data['today'].get('wind', '')
        
        lines.append(f"   天气：{weather}")
        lines.append(f"   温度：{temp}")
        if wind:
            lines.append(f"   风力：{wind}")
        lines.append("")
        
        # 穿衣建议
        if temp != '未知':
            advice = get_clothing_advice(temp, weather)
            lines.append("👕 穿衣建议")
            lines.append(f"   {advice}")
            lines.append("")
    
    if data['today'].get('indices'):
        lines.append("📊 生活指数")
        for idx in data['today']['indices']:
            level_str = f": {idx['level']}" if idx['level'] else ""
            lines.append(f"   • {idx['name']}{level_str} - {idx['desc']}")
    
    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("用法：python weather_query.py <city_code>")
        print("示例：python weather_query.py 101010100  # 北京")
        print("\n常见城市代码：")
        print("  北京：101010100")
        print("  上海：101020100")
        print("  广州：101280101")
        print("  深圳：101280601")
        print("  武汉：101200101")
        print("  黄冈：101200401")
        sys.exit(1)
    
    city_code = sys.argv[1]
    print(f"正在查询城市代码 {city_code} 的天气...", file=sys.stderr)
    html = fetch_weather_page(city_code)
    data = parse_weather_info(html)
    output = format_output(data)
    print(output)


if __name__ == '__main__':
    main()
