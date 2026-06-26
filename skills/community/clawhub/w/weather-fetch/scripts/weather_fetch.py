#!/usr/bin/env python3
from playwright.sync_api import sync_playwright
import re, sys, json

CITIES = {
    '苍南': {'id': '2333656', 'path': 'cangnan-county'},
    '梧州': {'id': '58361', 'path': 'wuzhou-city'}
}

def fetch_weather(city_name='苍南', partner='1000001049_hfaw'):
    info = CITIES.get(city_name, {})
    if not info:
        return {'error': f'未知城市: {city_name}'}
    
    url = f"https://m.weathercn.com/zh/cn/{info['path']}/{info['id']}/current-weather/{info['id']}?vivobrowser=1&partner={partner}"
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=['--no-sandbox'])
        context = browser.new_context(user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15')
        page = context.new_page()
        page.goto(url, timeout=30000)
        page.wait_for_timeout(5000)
        
        data = page.evaluate(r"""
            () => {
                const body = document.body.innerText;
                const r = {};
                
                // 城市
                const cityM = body.match(/(苍南县|梧州|钱库镇)/);
                r.city = cityM ? cityM[1] : '';
                
                // 当前温度
                const tempM = body.match(/(\d+)\s*℃/);
                r.temp = tempM ? tempM[1] : '';
                
                // 高低温：找4位数字（2618=26度高温18度低温）- 宽松匹配
                const fourM = body.match(/(\d{4})/);
                if (fourM && fourM[1].startsWith('2')) {  // 温度通常是20+
                    r.temp_high = fourM[1][0] + fourM[1][1];
                    r.temp_low = fourM[1][2] + fourM[1][3];
                }
                const lowM = body.match(/最低温?\s*(\d+)/);
                const highM = body.match(/最高温?\s*(\d+)/);
                if (lowM) r.temp_low = lowM[1];
                if (highM) r.temp_high = highM[1];
                
                // 天气
                const wM = body.match(/(晴|多云|阴|雾|小雨|中雨|大雨|阵雨|雷雨|暴雨)/);
                r.weather = wM ? wM[1] : '';
                
                // 湿度/体感/气压/能见度
                const humM = body.match(/湿度\s*(\d+)%/);
                r.humidity = humM ? humM[1] : '';
                const feelM = body.match(/体感\s*(\d+)℃/);
                r.feels_like = feelM ? feelM[1] : '';
                const presM = body.match(/气压\s*(\d+)/);
                r.pressure = presM ? presM[1] : '';
                const visM = body.match(/能见度\s*([\d.]+)\s*km/);
                r.visibility = visM ? visM[1] : '';
                
                // 风向风力
                const windM = body.match(/([东南西北]+)风(\d+)级/);
                if (windM) r.wind = windM[0];
                
                // 日出日落
                const srM = body.match(/日出\s*(\d+:\d+)/);
                const ssM = body.match(/日落\s*(\d+:\d+)/);
                r.sunrise = srM ? srM[1] : '';
                r.sunset = ssM ? ssM[1] : '';
                
                // AQI
                const aqiM = body.match(/空气质量[：:]?(\d+)(优|良)/);
                if (aqiM) { r.aqi = aqiM[1]; r.aqi_level = aqiM[2]; }
                
                return r;
            }
        """)
        browser.close()
        return data

def fmt(data):
    if 'error' in data:
        return f"获取失败: {data['error']}"
    return f"""{data.get('city', '')}
🌡️ {data.get('temp','')}°C（{data.get('temp_low','')}~{data.get('temp_high','')}°C）
🌤️ {data.get('weather','')}
💨 {data.get('wind','')}
🤒 体感 {data.get('feels_like','')}°C | 湿度 {data.get('humidity','')}%
👁️ 能见度 {data.get('visibility','')}km | 气压 {data.get('pressure','')}百帕
🌅 日出 {data.get('sunrise','')} / 日落 {data.get('sunset','')}
AQ: {data.get('aqi','')}{data.get('aqi_level','')}"""

if __name__ == '__main__':
    city = sys.argv[1] if len(sys.argv) > 1 else '苍南'
    data = fetch_weather(city)
    print(json.dumps(data, ensure_ascii=False, indent=2))
    print()
    print(fmt(data))
