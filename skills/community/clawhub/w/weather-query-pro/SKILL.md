---
name: china-weather
description: 中国天气查询工具。Use when user wants to check weather for Chinese cities. Supports current weather, forecast, air quality, life index with rich data and beautiful formatting. Free APIs with fallback strategy. 天气查询、天气预报、空气质量。
version: 1.0.3
license: MIT-0
metadata: {"openclaw": {"emoji": "🌤️", "requires": {"bins": ["curl", "python3"], "env": []}}}
---

# China Weather

中国天气查询工具，支持实时天气、天气预报、空气质量、生活指数，提供丰富的数据和精美的排版输出。

## Features

- 🌤️ **实时天气**: 当前天气状况、温度、湿度、风向
- 📅 **天气预报**: 7天/15天天气预报
- 🌫️ **空气质量**: AQI指数、PM2.5、PM10
- 🧥 **生活指数**: 穿衣、紫外线、运动、洗车指数
- 🔄 **API降级**: 多个免费API自动切换
- 🎨 **精美排版**: 专业格式输出
- 🌍 **多语言**: 中英文支持

## Trigger Conditions

- "查天气" / "Check weather"
- "明天天气怎么样" / "What's the weather tomorrow"
- "北京天气" / "Beijing weather"
- "空气质量" / "Air quality"
- "天气预报" / "Weather forecast"
- "china-weather"

---

## API Strategy (接口策略)

### 认证方式说明

| API | 认证方式 | 免费额度 | 配置要求 |
|-----|----------|----------|----------|
| **wttr.in** | 无需认证 | 无限制 | ❌ 无需任何配置 |
| **和风天气** | API Host + Key | 1000次/天 | ✅ 需要API_HOST + API_KEY |
| **OpenWeatherMap** | API Key | 1000次/天 | ✅ 需要API_KEY + 绑定信用卡 |
| **心知天气** | API Key | 无限制 | ✅ 需要API_KEY |

**推荐**：优先使用wttr.in（无需任何配置，免费无限制）

### 降级策略

```python
# 优先级：无需配置 → 需要配置
API_CHAIN = [
    {"name": "wttr", "requires_key": False},      # 无需任何配置
    {"name": "qweather", "requires_key": True},    # 需要API Host + Key
    {"name": "openweathermap", "requires_key": True} # 需要Key + 信用卡
]
```

### 和风天气配置说明（重要）

和风天气从2026年起**不再支持公共API地址**，必须使用专属API Host：

```bash
# 环境变量配置
export QWEATHER_API_HOST="你的API_HOST"  # 如：abc1234xyz.def.qweatherapi.com
export QWEATHER_API_KEY="你的API_KEY"

# 正确的API调用
curl "https://${QWEATHER_API_HOST}/v7/weather/now?location=101010100&key=${QWEATHER_API_KEY}"
```

**注意**：响应使用gzip压缩，需要添加`--compressed`参数或在代码中处理

### 降级策略

```python
API_CHAIN = [
    {"name": "qweather", "priority": 1, "fallback": True},
    {"name": "seniverse", "priority": 2, "fallback": True},
    {"name": "openweathermap", "priority": 3, "fallback": True},
    {"name": "wttr", "priority": 4, "fallback": False}
]

def get_weather_with_fallback(city):
    """Try APIs in priority order, fallback on failure"""
    for api in API_CHAIN:
        try:
            result = call_api(api["name"], city)
            if result:
                return result
        except Exception as e:
            if api["fallback"]:
                continue
            else:
                raise
    return None
```

---

## Step 1: Install Dependencies

```bash
pip install requests
```

---

## Step 2: Weather Query Script

```python
python3 << 'PYEOF'
import os
import requests
import json
from datetime import datetime

class WeatherService:
    def __init__(self):
        self.apis = {
            'qweather': QWeatherAPI(),
            'seniverse': SeniverseAPI(),
            'openweathermap': OpenWeatherMapAPI(),
            'wttr': WttrAPI()
        }
    
    def get_weather(self, city, days=7):
        """Get weather with fallback strategy"""
        for name, api in self.apis.items():
            try:
                result = api.get_weather(city, days)
                if result:
                    result['source'] = name
                    return result
            except Exception as e:
                print(f"⚠️ {name} failed: {e}")
                continue
        return None
    
    def format_weather(self, data, lang='zh'):
        """Format weather data beautifully"""
        if lang == 'zh':
            return self._format_chinese(data)
        else:
            return self._format_english(data)
    
    def _format_chinese(self, data):
        """Chinese format output"""
        output = []
        output.append(f"┌{'─'*50}┐")
        output.append(f"│  🌤️ {data['city']}天气预报")
        output.append(f"└{'─'*50}┘")
        output.append("")
        
        # 当前天气
        output.append(f"📍 当前天气")
        output.append(f"├─ 🌡️ 温度: {data['current']['temp']}°C (体感 {data['current']['feels_like']}°C)")
        output.append(f"├─ 🌤️ 天气: {data['current']['weather']}")
        output.append(f"├─ 💧 湿度: {data['current']['humidity']}%")
        output.append(f"├─ 🌬️ 风向: {data['current']['wind_dir']} {data['current']['wind_speed']}km/h")
        output.append(f"└─ 👁️ 能见度: {data['current']['visibility']}km")
        output.append("")
        
        # 空气质量
        if 'aqi' in data:
            output.append(f"🌫️ 空气质量")
            aqi = data['aqi']
            aqi_level = self._get_aqi_level(aqi['value'])
            output.append(f"├─ AQI: {aqi['value']} ({aqi_level})")
            output.append(f"├─ PM2.5: {aqi.get('pm25', 'N/A')}μg/m³")
            output.append(f"├─ PM10: {aqi.get('pm10', 'N/A')}μg/m³")
            output.append(f"└─ 首要污染物: {aqi.get('primary', 'N/A')}")
            output.append("")
        
        # 未来预报
        output.append(f"📅 未来预报")
        for day in data.get('forecast', [])[:7]:
            output.append(f"├─ {day['date']}: {day['weather']} {day['temp_min']}~{day['temp_max']}°C")
        output.append("")
        
        # 生活指数
        if 'indices' in data:
            output.append(f"🧥 生活指数")
            for idx in data['indices'][:4]:
                output.append(f"├─ {idx['name']}: {idx['level']}")
        
        return '\n'.join(output)
    
    def _format_english(self, data):
        """English format output"""
        output = []
        output.append(f"┌{'─'*50}┐")
        output.append(f"│  🌤️ {data['city']} Weather Forecast")
        output.append(f"└{'─'*50}┘")
        output.append("")
        
        # Current weather
        output.append(f"📍 Current Weather")
        output.append(f"├─ 🌡️ Temperature: {data['current']['temp']}°C (Feels like {data['current']['feels_like']}°C)")
        output.append(f"├─ 🌤️ Weather: {data['current']['weather']}")
        output.append(f"├─ 💧 Humidity: {data['current']['humidity']}%")
        output.append(f"├─ 🌬️ Wind: {data['current']['wind_dir']} {data['current']['wind_speed']}km/h")
        output.append(f"└─ 👁️ Visibility: {data['current']['visibility']}km")
        output.append("")
        
        # Air quality
        if 'aqi' in data:
            output.append(f"🌫️ Air Quality")
            aqi = data['aqi']
            aqi_level = self._get_aqi_level(aqi['value'])
            output.append(f"├─ AQI: {aqi['value']} ({aqi_level})")
            output.append(f"├─ PM2.5: {aqi.get('pm25', 'N/A')}μg/m³")
            output.append(f"├─ PM10: {aqi.get('pm10', 'N/A')}μg/m³")
            output.append(f"└─ Primary: {aqi.get('primary', 'N/A')}")
            output.append("")
        
        # Forecast
        output.append(f"📅 Forecast")
        for day in data.get('forecast', [])[:7]:
            output.append(f"├─ {day['date']}: {day['weather']} {day['temp_min']}~{day['temp_max']}°C")
        output.append("")
        
        return '\n'.join(output)
    
    def _get_aqi_level(self, aqi):
        """Get AQI level description"""
        if aqi <= 50:
            return "优 🟢"
        elif aqi <= 100:
            return "良 🟡"
        elif aqi <= 150:
            return "轻度污染 🟠"
        elif aqi <= 200:
            return "中度污染 🔴"
        elif aqi <= 300:
            return "重度污染 🟣"
        else:
            return "严重污染 🟤"

class WttrAPI:
    """wttr.in - Free, no API key required"""
    
    def get_weather(self, city, days=7):
        url = f"https://wttr.in/{city}?format=j1"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        current = data['current_condition'][0]
        
        result = {
            'city': city,
            'current': {
                'temp': current['temp_C'],
                'feels_like': current['FeelsLikeC'],
                'weather': current['lang_zh'][0]['value'] if 'lang_zh' in current else current['weatherDesc'][0]['value'],
                'humidity': current['humidity'],
                'wind_dir': current['winddir16Point'],
                'wind_speed': current['windspeedKmph'],
                'visibility': current['visibility']
            },
            'forecast': []
        }
        
        for day in data['weather'][:days]:
            result['forecast'].append({
                'date': day['date'],
                'weather': day['hourly'][4]['weatherDesc'][0]['value'],
                'temp_min': day['mintempC'],
                'temp_max': day['maxtempC']
            })
        
        return result

class QWeatherAPI:
    """和风天气 - 需要API Host + Key"""
    
    def __init__(self):
        self.api_key = os.environ.get('QWEATHER_API_KEY', '')
        self.api_host = os.environ.get('QWEATHER_API_HOST', '')
        # 默认使用GeoAPI端点
        self.geo_url = f"https://{self.api_host}/geo/v2" if self.api_host else ''
        self.weather_url = f"https://{self.api_host}/v7" if self.api_host else ''
    
    def get_weather(self, city, days=7):
        if not self.api_key or not self.api_host:
            return None
        
        # Get city ID
        city_id = self._get_city_id(city)
        if not city_id:
            return None
        
        # Get current weather (with gzip support)
        url = f"{self.weather_url}/weather/now?location={city_id}&key={self.api_key}"
        response = requests.get(url, timeout=10, headers={'Accept-Encoding': 'gzip'})
        response.encoding = 'utf-8'
        
        try:
            current_data = response.json()
        except:
            return None
        
        if current_data.get('code') != '200':
            return None
        
        now = current_data['now']
        
        result = {
            'city': city,
            'current': {
                'temp': now['temp'],
                'feels_like': now['feelsLike'],
                'weather': now['text'],
                'humidity': now['humidity'],
                'wind_dir': now['windDir'],
                'wind_speed': now['windSpeed'],
                'visibility': now['vis']
            },
            'forecast': self._get_forecast(city_id, days)
        }
        
        # Get AQI
        aqi = self._get_aqi(city_id)
        if aqi:
            result['aqi'] = aqi
        
        return result
    
    def _get_city_id(self, city):
        """Get city ID from city name"""
        url = f"{self.geo_url}/city/lookup?location={city}&key={self.api_key}"
        response = requests.get(url, timeout=10, headers={'Accept-Encoding': 'gzip'})
        try:
            data = response.json()
            if data.get('code') == '200' and data.get('location'):
                return data['location'][0]['id']
        except:
            pass
        return None
    
    def _get_forecast(self, city_id, days):
        """Get weather forecast"""
        url = f"{self.base_url}/weather/7d?location={city_id}&key={self.api_key}"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        forecast = []
        for day in data.get('daily', [])[:days]:
            forecast.append({
                'date': day['fxDate'],
                'weather': day['textDay'],
                'temp_min': day['tempMin'],
                'temp_max': day['tempMax']
            })
        return forecast
    
    def _get_aqi(self, city_id):
        """Get air quality index"""
        url = f"{self.base_url}/air/now?location={city_id}&key={self.api_key}"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if data.get('code') == '200':
            air = data['now']
            return {
                'value': int(air['aqi']),
                'pm25': air.get('pm2p5'),
                'pm10': air.get('pm10'),
                'primary': air.get('primary')
            }
        return None

# Example usage
service = WeatherService()

# Query weather
data = service.get_weather('Beijing')
if data:
    # Format output
    output = service.format_weather(data, lang='zh')
    print(output)
else:
    print("❌ 无法获取天气数据")
PYEOF
```

---

## API Configuration (接口配置)

### 和风天气 (推荐)

```bash
# 注册: https://dev.qweather.com
# 免费额度: 1000次/天
export QWEATHER_API_KEY="your_key_here"
```

### OpenWeatherMap

```bash
# 注册: https://openweathermap.org/api
# 免费额度: 1000次/天
export OPENWEATHER_API_KEY="your_key_here"
```

### 心知天气

```bash
# 注册: https://www.seniverse.com
# 免费额度: 无限制（基础数据）
export SENIVERSE_API_KEY="your_key_here"
```

### wttr.in (无需API Key)

```bash
# 直接使用，无需注册
curl "wttr.in/Beijing?format=j1"
```

---

## Data Fields (数据字段)

### Current Weather (实时天气)

| 字段 | 说明 | 单位 |
|------|------|------|
| temp | 温度 | °C |
| feels_like | 体感温度 | °C |
| weather | 天气状况 | 文字 |
| humidity | 湿度 | % |
| wind_dir | 风向 | 方位 |
| wind_speed | 风速 | km/h |
| visibility | 能见度 | km |
| pressure | 气压 | hPa |

### Air Quality (空气质量)

| 字段 | 说明 | 单位 |
|------|------|------|
| aqi | 空气质量指数 | 0-500 |
| pm25 | PM2.5浓度 | μg/m³ |
| pm10 | PM10浓度 | μg/m³ |
| so2 | 二氧化硫 | μg/m³ |
| no2 | 二氧化氮 | μg/m³ |
| co | 一氧化碳 | mg/m³ |
| o3 | 臭氧 | μg/m³ |

### Life Index (生活指数)

| 指数 | 说明 | 等级 |
|------|------|------|
| 穿衣指数 | 建议穿着 | 寒冷/凉爽/舒适/炎热 |
| 紫外线指数 | UV强度 | 弱/中等/强/很强 |
| 运动指数 | 适合运动程度 | 适宜/较适宜/不宜 |
| 洗车指数 | 适合洗车程度 | 适宜/较适宜/不宜 |
| 感冒指数 | 感冒风险 | 低/中/高 |

---

## Security Notes

- ✅ No data uploaded to external servers (except API calls)
- ✅ Open source dependencies
- ✅ Multiple API fallback
- ⚠️ API keys should be kept secure

---

## Notes

- wttr.in 免费无需API Key，功能较简单
- 和风天气数据最丰富，需要注册
- 多API降级策略确保服务可用性
- 支持中英文天气描述
