#!/usr/bin/env python3
"""
QWeather China - 基于中国气象局数据的完整天气服务
和风天气API封装，提供实时天气、预报、生活指数等功能
跨平台兼容版本，自动处理编码问题
"""

import os
import json
import time
import jwt
import requests
import argparse
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

# 导入编码处理工具
from encoding_utils import safe_print, setup_encoding

# 配置常量 - 从环境变量或config.json加载
def load_config():
    """加载配置，优先从环境变量读取"""
    # 默认配置
    default_config = {
        "kid": "CGWFM979C7",
        "sub": "4FKRV2BREH",
        "api_host": "p54up4xhmm.re.qweatherapi.com",
        "private_key_path": os.path.expanduser("~/.config/qweather/private.pem"),
        "cache_dir": os.path.expanduser("~/.cache/qweather"),
        "cache_ttl": {
            "now": 600,      # 10分钟
            "forecast": 3600, # 1小时
            "indices": 10800, # 3小时
            "air": 1800,     # 30分钟
        }
    }
    
    # 从 config.json 加载（如果存在）
    CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            config_data = json.load(f)
        qweather_config = config_data.get("qweather", {})
        
        # 解析路径（支持 ~ 展开）
        def expand_path(path):
            if path:
                return os.path.expanduser(path)
            return path
        
        default_config.update({
            "kid": qweather_config.get("jwt", {}).get("kid", default_config["kid"]),
            "sub": qweather_config.get("jwt", {}).get("sub", default_config["sub"]),
            "api_host": qweather_config.get("api_host", default_config["api_host"]),
            "private_key_path": expand_path(qweather_config.get("jwt", {}).get("private_key_path", default_config["private_key_path"])),
            "cache_dir": expand_path(qweather_config.get("cache", {}).get("directory", default_config["cache_dir"])),
            "cache_ttl": qweather_config.get("cache", {}).get("ttl", default_config["cache_ttl"]),
        })
    
    # 环境变量覆盖
    default_config.update({
        "kid": os.getenv("QWEATHER_CREDENTIALS_ID", default_config["kid"]),
        "sub": os.getenv("QWEATHER_PROJECT_ID", default_config["sub"]),
        "api_host": os.getenv("QWEATHER_API_HOST", default_config["api_host"]),
        "private_key_path": os.path.expanduser(os.getenv("QWEATHER_PRIVATE_KEY_PATH", default_config["private_key_path"])),
        "cache_dir": os.path.expanduser(os.getenv("QWEATHER_CACHE_DIR", default_config["cache_dir"])),
    })
    
    return default_config

CONFIG = load_config()

# 常用城市代码
CITY_CODES = {
    "beijing": "101010100",
    "shanghai": "101020100",
    "guangzhou": "101280101",
    "shenzhen": "101280601",
    "hangzhou": "101210101",
    "chengdu": "101270101",
    "wuhan": "101200101",
    "nanjing": "101190101",
    "xian": "101110101",
    "chongqing": "101040100",
}

@dataclass
class WeatherNow:
    """实时天气数据"""
    obs_time: str
    temp: int
    feels_like: int
    text: str
    icon: str
    wind_speed: int
    wind_scale: str
    wind_dir: str
    humidity: int
    precip: float
    pressure: int
    vis: int
    cloud: int
    dew: int
    
    def format(self) -> str:
        """格式化显示"""
        return f"""
🌤️ 实时天气 ({self.obs_time})
🌡️ 温度: {self.temp}°C (体感: {self.feels_like}°C)
🌬️ 风力: {self.wind_scale}级 ({self.wind_speed}km/h) {self.wind_dir}
💧 湿度: {self.humidity}%
🌧️ 降水: {self.precip}mm
📊 气压: {self.pressure}hPa
👁️ 能见度: {self.vis}公里
☁️ 云量: {self.cloud}%
🌡️ 露点: {self.dew}°C
"""

@dataclass
class DailyForecast:
    """每日预报"""
    fx_date: str
    sunrise: str
    sunset: str
    temp_max: int
    temp_min: int
    text_day: str
    text_night: str
    icon_day: str
    icon_night: str
    wind_scale_day: str
    wind_dir_day: str
    precip: float
    humidity: int
    uv_index: str
    cloud: int
    
    def format(self) -> str:
        """格式化显示"""
        weekday = self._get_weekday()
        return f"""
{weekday} ({self.fx_date})
🌅 日出: {self.sunrise} | 🌇 日落: {self.sunset}
🌡️ 温度: {self.temp_min}°C ~ {self.temp_max}°C
☀️ 白天: {self.text_day}
🌙 夜间: {self.text_night}
🌬️ 风力: {self.wind_scale_day}级 {self.wind_dir_day}
💧 湿度: {self.humidity}%
🌧️ 降水: {self.precip}mm
☀️ 紫外线: {self.uv_index}级
☁️ 云量: {self.cloud}%
"""
    
    def _get_weekday(self) -> str:
        """获取星期几"""
        date_obj = datetime.strptime(self.fx_date, "%Y-%m-%d")
        weekdays = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
        return weekdays[date_obj.weekday()]

@dataclass
class LifeIndex:
    """生活指数"""
    date: str
    type: str
    name: str
    level: str
    category: str
    text: str
    
    def format(self) -> str:
        """格式化显示"""
        emoji = self._get_emoji()
        return f"{emoji} {self.name}: {self.level} - {self.text}"
    
    def _get_emoji(self) -> str:
        """获取对应的emoji"""
        emoji_map = {
            "穿衣": "👕", "洗车": "🚗", "运动": "🏃", "紫外线": "☀️",
            "感冒": "🤧", "空气污染": "😷", "钓鱼": "🎣", "旅游": "🧳",
            "舒适度": "😊", "晾晒": "👕", "交通": "🚦", "防晒": "🧴"
        }
        return emoji_map.get(self.name, "📊")

class QWeatherClient:
    """和风天气API客户端"""
    
    def __init__(self):
        self.kid = CONFIG["kid"]
        self.sub = CONFIG["sub"]
        self.api_host = CONFIG["api_host"]
        self.private_key = self._load_private_key()
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "OpenClaw-QWeather/1.0"
        })
        
        # 创建缓存目录
        os.makedirs(CONFIG["cache_dir"], exist_ok=True)
    
    def _load_private_key(self):
        """加载私钥"""
        with open(CONFIG["private_key_path"], 'r') as f:
            private_key_pem = f.read()
        
        return serialization.load_pem_private_key(
            private_key_pem.encode(),
            password=None,
            backend=default_backend()
        )
    
    def _generate_jwt(self) -> str:
        """生成JWT token"""
        current_time = int(time.time())
        payload = {
            "sub": self.sub,
            "iat": current_time,
            "exp": current_time + 3600
        }
        
        headers = {
            "alg": "EdDSA",
            "typ": "JWT",
            "kid": self.kid
        }
        
        return jwt.encode(
            payload,
            self.private_key,
            algorithm="EdDSA",
            headers=headers
        )
    
    def _get_cached_data(self, cache_key: str, ttl: int) -> Optional[Dict]:
        """获取缓存数据"""
        cache_file = os.path.join(CONFIG["cache_dir"], f"{cache_key}.json")
        
        if os.path.exists(cache_file):
            mtime = os.path.getmtime(cache_file)
            if time.time() - mtime < ttl:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        
        return None
    
    def _save_to_cache(self, cache_key: str, data: Dict):
        """保存到缓存"""
        cache_file = os.path.join(CONFIG["cache_dir"], f"{cache_key}.json")
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def _make_request(self, endpoint: str, params: Dict = None) -> Dict:
        """发送API请求"""
        # 生成JWT token
        token = self._generate_jwt()
        
        # 构建URL
        url = f"https://{self.api_host}{endpoint}"
        
        # 设置headers
        headers = {
            "Authorization": f"Bearer {token}"
        }
        
        # 发送请求
        response = self.session.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        
        return response.json()
    
    def get_city_code(self, city_name: str) -> str:
        """获取城市代码"""
        city_name_lower = city_name.lower()
        
        # 首先检查已知城市
        if city_name_lower in CITY_CODES:
            return CITY_CODES[city_name_lower]
        
        # 如果是数字，直接返回
        if city_name.isdigit():
            return city_name
        
        # 默认返回北京
        return CITY_CODES["beijing"]
    
    def get_weather_now(self, city: str) -> WeatherNow:
        """获取实时天气"""
        cache_key = f"now_{city}"
        
        # 检查缓存
        cached = self._get_cached_data(cache_key, CONFIG["cache_ttl"]["now"])
        if cached:
            data = cached
        else:
            city_code = self.get_city_code(city)
            data = self._make_request("/v7/weather/now", {"location": city_code})
            self._save_to_cache(cache_key, data)
        
        now_data = data["now"]
        return WeatherNow(
            obs_time=now_data["obsTime"],
            temp=int(now_data["temp"]),
            feels_like=int(now_data["feelsLike"]),
            text=now_data["text"],
            icon=now_data["icon"],
            wind_speed=int(now_data["windSpeed"]),
            wind_scale=now_data["windScale"],
            wind_dir=now_data["windDir"],
            humidity=int(now_data["humidity"]),
            precip=float(now_data["precip"]),
            pressure=int(now_data["pressure"]),
            vis=int(now_data["vis"]),
            cloud=int(now_data["cloud"]),
            dew=int(now_data["dew"])
        )
    
    def get_weather_forecast(self, city: str, days: int = 3) -> List[DailyForecast]:
        """获取天气预报"""
        cache_key = f"forecast_{city}_{days}"
        
        # 检查缓存
        cached = self._get_cached_data(cache_key, CONFIG["cache_ttl"]["forecast"])
        if cached:
            data = cached
        else:
            city_code = self.get_city_code(city)
            endpoint = "/v7/weather/7d" if days > 3 else "/v7/weather/3d"
            data = self._make_request(endpoint, {"location": city_code})
            self._save_to_cache(cache_key, data)
        
        forecasts = []
        for daily_data in data["daily"][:days]:
            forecast = DailyForecast(
                fx_date=daily_data["fxDate"],
                sunrise=daily_data["sunrise"],
                sunset=daily_data["sunset"],
                temp_max=int(daily_data["tempMax"]),
                temp_min=int(daily_data["tempMin"]),
                text_day=daily_data["textDay"],
                text_night=daily_data["textNight"],
                icon_day=daily_data["iconDay"],
                icon_night=daily_data["iconNight"],
                wind_scale_day=daily_data["windScaleDay"],
                wind_dir_day=daily_data["windDirDay"],
                precip=float(daily_data["precip"]),
                humidity=int(daily_data["humidity"]),
                uv_index=daily_data["uvIndex"],
                cloud=int(daily_data["cloud"])
            )
            forecasts.append(forecast)
        
        return forecasts
    
    def get_life_indices(self, city: str, date: str = None) -> List[LifeIndex]:
        """获取生活指数"""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        cache_key = f"indices_{city}_{date}"
        
        # 检查缓存
        cached = self._get_cached_data(cache_key, CONFIG["cache_ttl"]["indices"])
        if cached:
            data = cached
        else:
            city_code = self.get_city_code(city)
            data = self._make_request("/v7/indices/1d", {
                "location": city_code,
                "type": "0"  # 获取所有类型
            })
            self._save_to_cache(cache_key, data)
        
        indices = []
        for index_data in data["daily"]:
            index = LifeIndex(
                date=index_data["date"],
                type=index_data["type"],
                name=index_data["name"],
                level=index_data["level"],
                category=index_data["category"],
                text=index_data["text"]
            )
            indices.append(index)
        
        return indices
    
    def get_air_quality(self, city: str) -> Dict:
        """获取空气质量"""
        cache_key = f"air_{city}"
        
        # 检查缓存
        cached = self._get_cached_data(cache_key, CONFIG["cache_ttl"]["air"])
        if cached:
            return cached
        
        city_code = self.get_city_code(city)
        data = self._make_request("/v7/air/now", {"location": city_code})
        self._save_to_cache(cache_key, data)
        
        return data
    
    def get_dressing_advice(self, temp: int) -> str:
        """根据温度提供穿衣建议"""
        if temp >= 28:
            return "👕 短袖、短裤、裙子，注意防晒"
        elif temp >= 23:
            return "👕 短袖、薄外套，早晚可加衣"
        elif temp >= 18:
            return "👕 长袖、薄外套，舒适温度"
        elif temp >= 10:
            return "🧥 外套、长裤，注意保暖"
        elif temp >= 0:
            return "🧥 厚外套、毛衣，建议穿秋裤"
        else:
            return "🧥 羽绒服、厚毛衣，注意防寒保暖"
    
    def get_umbrella_advice(self, precip: float, text: str) -> str:
        """根据降水提供雨伞建议"""
        if precip > 5 or "雨" in text:
            return "🌂 需要带雨伞，可能有中到大雨"
        elif precip > 0.1 or "小雨" in text:
            return "🌂 建议带雨伞，可能有小雨"
        else:
            return "☀️ 不需要带雨伞"

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="QWeather China - 中国气象局天气服务")
    parser.add_argument("command", choices=["now", "forecast", "indices", "air", "full"],
                       help="命令: now(实时天气), forecast(预报), indices(生活指数), air(空气质量), full(完整报告)")
    parser.add_argument("--city", default="beijing", help="城市名称或代码，默认: beijing")
    parser.add_argument("--days", type=int, default=3, help="预报天数，默认: 3")
    parser.add_argument("--no-cache", action="store_true", help="不使用缓存")
    
    args = parser.parse_args()
    
    # 创建客户端
    client = QWeatherClient()
    
    try:
        if args.command == "now":
            # 实时天气
            weather = client.get_weather_now(args.city)
            safe_print(weather.format())
            
            # 穿衣建议
            dressing = client.get_dressing_advice(weather.temp)
            safe_print(f"👕 穿衣建议: {dressing}")
            
            # 雨伞建议
            umbrella = client.get_umbrella_advice(weather.precip, weather.text)
            safe_print(f"🌂 雨伞建议: {umbrella}")
            
        elif args.command == "forecast":
            # 天气预报
            forecasts = client.get_weather_forecast(args.city, args.days)
            safe_print(f"📅 {args.city.capitalize()} {args.days}天天气预报")
            safe_print("=" * 50)
            
            for forecast in forecasts:
                safe_print(forecast.format())
                safe_print("-" * 50)
            
        elif args.command == "indices":
            # 生活指数
            indices = client.get_life_indices(args.city)
            safe_print(f"📊 {args.city.capitalize()} 今日生活指数")
            safe_print("=" * 50)
            
            for index in indices[:10]:  # 显示前10个
                safe_print(index.format())
            
        elif args.command == "air":
            # 空气质量
            air_data = client.get_air_quality(args.city)
            now = air_data["now"]
            safe_print(f"🌫️ {args.city.capitalize()} 空气质量")
            safe_print("=" * 50)
            safe_print(f"更新时间: {air_data['updateTime']}")
            safe_print(f"AQI: {now['aqi']} ({now['category']})")
            safe_print(f"主要污染物: {now['primary']}")
            safe_print(f"PM2.5: {now['pm2p5']} μg/m³")
            safe_print(f"PM10: {now['pm10']} μg/m³")
            safe_print(f"二氧化硫: {now['so2']} μg/m³")
            safe_print(f"二氧化氮: {now['no2']} μg/m³")
            safe_print(f"臭氧: {now['o3']} μg/m³")
            safe_print(f"一氧化碳: {now['co']} mg/m³")
            
        elif args.command == "full":
            # 完整报告
            safe_print(f"📋 {args.city.capitalize()} 天气完整报告")
            safe_print("=" * 60)
            
            # 实时天气
            weather = client.get_weather_now(args.city)
            safe_print("🌤️ 实时天气")
            safe_print(weather.format())
            
            # 穿衣和雨伞建议
            dressing = client.get_dressing_advice(weather.temp)
            umbrella = client.get_umbrella_advice(weather.precip, weather.text)
            safe_print(f"👕 穿衣建议: {dressing}")
            safe_print(f"🌂 雨伞建议: {umbrella}")
            safe_print()
            
            # 3天预报
            safe_print("📅 3天天气预报")
            safe_print("-" * 50)
            forecasts = client.get_weather_forecast(args.city, 3)
            for forecast in forecasts:
                safe_print(forecast.format())
            
            # 生活指数
            safe_print("📊 今日生活指数")
            safe_print("-" * 50)
            indices = client.get_life_indices(args.city)
            for index in indices[:8]:  # 显示前8个重要指数
                safe_print(index.format())
            
            # 空气质量
            safe_print("🌫️ 空气质量")
            safe_print("-" * 50)
            try:
                air_data = client.get_air_quality(args.city)
                now = air_data["now"]
                safe_print(f"AQI: {now['aqi']} ({now['category']})")
                safe_print(f"主要污染物: {now['primary']}")
                safe_print(f"PM2.5: {now['pm2p5']} μg/m³")
            except Exception as e:
                safe_print(f"空气质量数据暂时不可用: {e}")
            
            safe_print()
            safe_print("=" * 60)
            safe_print("数据来源: 中国气象局 · 和风天气")
            safe_print(f"报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    except Exception as e:
        safe_print(f"❌ 错误: {e}")
        safe_print("请检查网络连接或API配置")

if __name__ == "__main__":
    main()