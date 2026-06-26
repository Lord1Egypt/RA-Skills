#!/usr/bin/env python3
# 爬取中国天气网龙里县天气数据（零成本方案）
import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime

def fetch_longli_weather():
    """
    返回结构：
    {
        "date": "2026-03-15",
        "temp_range": "8℃～15℃",
        "weather": "多云转晴",
        "wind": "东北风 2级",
        "raw_html": "..."
    }
    若失败返回 None
    """
    url = "http://www.weather.com.cn/weather/101260408.shtml"  # 龙里县 ID
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        # 找今天天气（第一个 <li class="sky skyid lv...">）
        today = soup.find('li', class_=re.compile(r'sky skyid lv\d+'))
        if not today:
            return None
        
        # 温度
        temp = today.find('p', class_='tem')
        temp_range = temp.get_text(strip=True) if temp else ''
        
        # 天气现象
        wea = today.find('p', class_='wea')
        weather = wea.get_text(strip=True) if wea else ''
        
        # 风力
        wind = today.find('p', class_='win')
        wind_text = wind.get_text(strip=True) if wind else ''
        
        return {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "temp_range": temp_range,
            "weather": weather,
            "wind": wind_text,
            "raw_html": resp.text[:500]  # 留点日志
        }
    except Exception as e:
        print(f"爬取失败: {e}")
        return None

if __name__ == "__main__":
    data = fetch_longli_weather()
    if data:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print("{}")