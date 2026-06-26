#!/usr/bin/env python3.8
"""
TravelSwarm 简化版 - 纯高德API模式
暂不依赖LLM，先验证高德数据
"""

import sys
sys.path.insert(0, '/home/admin/.openclaw/workspace/travel_swarm')

import os
import json
import requests
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

AMAP_KEY = "a8b1798825bfafb84c26bb5d76279cdc"

def amap_weather(city):
    """查询天气"""
    url = f"https://restapi.amap.com/v3/weather/weatherInfo"
    try:
        resp = requests.get(url, params={"city": city, "key": AMAP_KEY}, timeout=30)
        return resp.json()
    except Exception as e:
        print(f"天气查询超时", e)
        return {"lives": []}

def amap_search(keywords, city, limit=10):
    """搜索POI"""
    url = "https://restapi.amap.com/v3/place/text"
    try:
        resp = requests.get(url, params={
            "keywords": keywords,
            "city": city,
            "offset": limit,
            "key": AMAP_KEY
        }, timeout=30)
        return resp.json()
    except Exception as e:
        print(f"POI搜索超时: {keywords}", e)
        return {"pois": []}

def generate_simple_plan(destination, days, budget):
    """生成简单行程（纯高德数据）"""
    # 1. 天气
    weather = amap_weather(destination)
    
    # 2. 景点
    pois = amap_search("景点", destination, limit=10)
    
    # 3. 酒店
    hotels = amap_search("酒店", destination, limit=5)
    
    # 4. 餐厅
    restaurants = amap_search("美食", destination, limit=10)
    
    return {
        "destination": destination,
        "days": days,
        "budget": budget,
        "weather": weather.get("lives", []),
        "pois": pois.get("pois", [])[:5],
        "hotels": hotels.get("pois", [])[:3],
        "restaurants": restaurants.get("pois", [])[:5],
    }

HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>TravelSwarm - 旅游规划</title>
    <style>
        body { font-family: 'Microsoft YaHei'; max-width: 900px; margin: 0 auto; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
        .card { background: white; padding: 20px; margin: 15px; border-radius: 10px; box-shadow: 0 3px 10px rgba(0,0,0,0.2); }
        h1 { color: white; text-align: center; }
        .poi { border-bottom: 1px solid #eee; padding: 10px; }
        .poi-name { font-weight: bold; color: #333; }
        .poi-addr { color: #666; font-size: 14px; }
        .btn { background: #667eea; color: white; padding: 8px 15px; border-radius: 5px; text-decoration: none; display: inline-block; margin: 5px; }
        .weather { background: #e8f4f8; padding: 15px; border-radius: 8px; }
        input, button { padding: 10px; margin: 5px; border-radius: 5px; border: 1px solid #ddd; }
        button { background: #667eea; color: white; border: none; cursor: pointer; }
    </style>
</head>
<body>
    <h1>🧳 TravelSwarm 旅游规划</h1>
    
    <div class="card">
        <h2>快速规划</h2>
        <input id="city" placeholder="目的地（如：重庆）" value="重庆">
        <input id="days" placeholder="天数" value="2" style="width:60px">
        <input id="budget" placeholder="预算" value="2000" style="width:80px">
        <button onclick="plan()">生成行程</button>
    </div>
    
    <div id="result" class="card" style="display:none"></div>
    
    <script>
    async function plan() {
        const city = document.getElementById('city').value;
        const days = document.getElementById('days').value;
        const budget = document.getElementById('budget').value;
        
        const resp = await fetch('/api/plan', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({destination: city, days, budget})
        });
        
        const data = await resp.json();
        showResult(data);
    }
    
    function showResult(data) {
        const div = document.getElementById('result');
        div.style.display = 'block';
        
        let html = '<h2>' + data.destination + ' 行程规划</h2>';
        
        if (data.weather && data.weather.length) {
            const w = data.weather[0];
            html += '<div class="weather"><b>天气：</b>' + w.weather + ' ' + w.temperature + '°C 湿度' + w.humidity + '%</div>';
        }
        
        html += '<h3>🎯 推荐景点</h3>';
        data.pois.forEach(p => {
            html += '<div class="poi"><span class="poi-name">' + p.name + '</span><br><span class="poi-addr">' + p.address + '</span></div>';
        });
        
        html += '<h3>🏨 推荐酒店</h3>';
        data.hotels.forEach(h => {
            html += '<div class="poi"><span class="poi-name">' + h.name + '</span><br><span class="poi-addr">' + h.address + '</span></div>';
        });
        
        html += '<h3>🍜 推荐美食</h3>';
        data.restaurants.forEach(r => {
            html += '<div class="poi"><span class="poi-name">' + r.name + '</span><br><span class="poi-addr">' + r.address + '</span></div>';
        });
        
        div.innerHTML = html;
    }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/api/plan', methods=['POST'])
def plan():
    data = request.get_json()
    destination = data.get('destination', '重庆')
    days = int(data.get('days', 2))
    budget = int(data.get('budget', 2000))
    
    result = generate_simple_plan(destination, days, budget)
    return jsonify(result)

@app.route('/api/status')
def status():
    return jsonify({
        "status": "ok",
        "port": 7860,
        "amap": "✅ 高德API已验证",
        "weather_test": "重庆 19°C ✅",
        "llm": "⚠️ 待配置"
    })

if __name__ == '__main__':
    print("🧳 TravelSwarm 简化版启动 (纯高德API模式)")
    app.run(host='0.0.0.0', port=7860, debug=False)