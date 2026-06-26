#!/usr/bin/env python3
"""
OpenClaw集成模块
将QWeather天气服务集成到OpenClaw中
支持智能地点处理和自然语言理解
"""

import re
import json
import os
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from qweather import QWeatherClient, WeatherNow, DailyForecast, LifeIndex
from location_handler import LocationHandler, LocationResult

class OpenClawWeatherHandler:
    """OpenClaw天气处理器"""
    
    def __init__(self):
        self.client = QWeatherClient()
        self.location_handler = LocationHandler(self.client)
        self.command_patterns = self._init_command_patterns()
        
    def _init_command_patterns(self) -> Dict:
        """初始化命令模式"""
        return {
            # 实时天气相关
            r"(.*?)天气(怎么样)?[？?]?$": self.handle_weather_now,
            r"(.*?)的?温度(是多少)?[？?]?$": self.handle_temperature,
            r"(.*?)现在天气[？?]?$": self.handle_weather_now,
            r"(.*?)当前天气[？?]?$": self.handle_weather_now,
            r"(.*?)实时天气[？?]?$": self.handle_weather_now,
            
            # 特定日期
            r"(.*?)(今天|明天|后天)天气[？?]?$": self.handle_specific_day,
            r"(今天|明天|后天)(.*?)天气[？?]?$": self.handle_specific_day_reverse,
            
            # 预报相关
            r"(.*?)未来(\d+)天?预报[？?]?$": self.handle_forecast_days,
            r"(.*?)预报[？?]?$": self.handle_forecast,
            r"(.*?)未来几天[？?]?$": self.handle_few_days,
            
            # 生活指数
            r"(.*?)生活指数[？?]?$": self.handle_life_indices,
            r"(.*?)指数[？?]?$": self.handle_life_indices,
            
            # 空气质量
            r"(.*?)空气质量[？?]?$": self.handle_air_quality,
            r"(.*?)AQI[？?]?$": self.handle_air_quality,
            
            # 建议类
            r"(.*?)需要带伞吗[？?]?$": self.handle_umbrella,
            r"(.*?)穿什么[？?]?$": self.handle_clothing,
            r"(.*?)穿衣建议[？?]?$": self.handle_clothing,
            
            # 帮助
            r"天气帮助[？?]?$": self.handle_help,
            r"weather help[？?]?$": self.handle_help,
        }
    
    def extract_location(self, text: str) -> Tuple[LocationResult, str]:
        """
        从文本中提取地点信息
        返回：(LocationResult, 原始文本中提取的地点部分)
        """
        # 移除常见查询词
        query_words = ["天气", "温度", "预报", "指数", "质量", "需要", "带伞", "穿什么", "穿衣"]
        location_text = text
        for word in query_words:
            location_text = location_text.replace(word, "")
        
        location_text = location_text.strip()
        
        # 使用智能地点处理器
        location = self.location_handler.parse_input(location_text)
        
        # 如果没有提供地点，使用默认地点并添加说明
        if location.source == "default" or location.source == "default_fallback":
            default_note = "（按默认地点查询）"
        else:
            default_note = ""
        
        return location, default_note
    
    def handle_query(self, query: str) -> str:
        """处理用户查询"""
        query = query.strip()
        
        # 遍历所有模式
        for pattern, handler in self.command_patterns.items():
            match = re.match(pattern, query, re.IGNORECASE)
            if match:
                return handler(query, match)
        
        # 默认处理
        return self.handle_default(query)
    
    def handle_weather_now(self, query: str, match) -> str:
        """处理实时天气查询"""
        location, default_note = self.extract_location(match.group(1))
        display_name = self.location_handler.get_location_for_display(location)
        
        try:
            weather = self.client.get_weather_now(location.name)
            dressing = self.client.get_dressing_advice(weather.temp)
            umbrella = self.client.get_umbrella_advice(weather.precip, weather.text)
            
            return f"""
🌤️ {display_name}当前天气{default_note} ({weather.obs_time})
📍 地点: {self.location_handler.format_location(location)}
🌡️ 温度: {weather.temp}°C (体感: {weather.feels_like}°C)
🌬️ 风力: {weather.wind_scale}级 ({weather.wind_speed}km/h) {weather.wind_dir}
💧 湿度: {weather.humidity}%
🌧️ 降水: {weather.precip}mm
📊 气压: {weather.pressure}hPa
👁️ 能见度: {weather.vis}公里
☁️ 云量: {weather.cloud}%

🎯 建议:
{dressing}
{umbrella}

📱 详细: {self.client.api_host}/weather/{location.name}
"""
        except Exception as e:
            error_msg = self._format_error(e, location)
            return error_msg
    
    def _format_error(self, error: Exception, location: LocationResult) -> str:
        """格式化错误信息"""
        error_str = str(error)
        display_name = self.location_handler.get_location_for_display(location)
        
        # 常见错误类型
        if "401" in error_str or "认证" in error_str:
            return f"""❌ 获取{display_name}天气失败: 认证错误

请检查以下环境变量配置：
1. QWEATHER_API_HOST: {os.getenv('QWEATHER_API_HOST', '未设置')}
2. QWEATHER_PROJECT_ID: {os.getenv('QWEATHER_PROJECT_ID', '未设置')}
3. QWEATHER_CREDENTIALS_ID: {os.getenv('QWEATHER_CREDENTIALS_ID', '未设置')}
4. QWEATHER_PRIVATE_KEY_PATH: {os.getenv('QWEATHER_PRIVATE_KEY_PATH', '未设置')}

或使用 QWEATHER_DEFAULT_LOCATION 设置默认查询地点"""
        
        elif "404" in error_str or "找不到" in error_str:
            return f"❌ 找不到地点: {display_name}，请确认城市名称是否正确"
        
        elif "429" in error_str or "频率" in error_str:
            return f"❌ 请求频率超限，请稍后再试查询{display_name}天气"
        
        elif "网络" in error_str or "连接" in error_str:
            return f"❌ 网络连接失败，请检查网络后重试查询{display_name}天气"
        
        else:
            return f"❌ 获取{display_name}天气失败: {error_str}"
    
    def handle_temperature(self, query: str, match) -> str:
        """处理温度查询"""
        location, default_note = self.extract_location(match.group(1))
        display_name = self.location_handler.get_location_for_display(location)
        
        try:
            weather = self.client.get_weather_now(location.name)
            return f"🌡️ {display_name}当前温度{default_note}: {weather.temp}°C (体感: {weather.feels_like}°C)"
        except Exception as e:
            error_msg = self._format_error(e, location)
            return error_msg
    
    def handle_specific_day(self, query: str, match) -> str:
        """处理特定日期天气 - 格式: [地点][今天/明天/后天]天气"""
        location_text = match.group(1)
        day = match.group(2)  # 今天、明天、后天
        
        location, default_note = self.extract_location(location_text)
        display_name = self.location_handler.get_location_for_display(location)
        
        # 天数映射
        day_map = {"今天": 1, "明天": 2, "后天": 3}
        if day not in day_map:
            return "❌ 请指定今天、明天或后天"
        
        days = day_map[day]
        
        try:
            forecasts = self.client.get_weather_forecast(location.name, days)
            if len(forecasts) < days:
                return f"❌ 无法获取{display_name}{day}的预报"
            
            # 只返回指定那天的预报
            target_day = forecasts[-1] if days > 1 else forecasts[0]
            
            return f"""
📅 {display_name}{day}天气{default_note}
📍 地点: {self.location_handler.format_location(location)}
{target_day.format()}
"""
        except Exception as e:
            error_msg = self._format_error(e, location)
            return error_msg
    
    def handle_specific_day_reverse(self, query: str, match) -> str:
        """处理特定日期天气 - 格式: [今天/明天/后天][地点]天气"""
        day = match.group(1)  # 今天、明天、后天
        location_text = match.group(2)
        
        location, default_note = self.extract_location(location_text)
        display_name = self.location_handler.get_location_for_display(location)
        
        # 天数映射
        day_map = {"今天": 1, "明天": 2, "后天": 3}
        if day not in day_map:
            return "❌ 请指定今天、明天或后天"
        
        days = day_map[day]
        
        try:
            forecasts = self.client.get_weather_forecast(location.name, days)
            if len(forecasts) < days:
                return f"❌ 无法获取{display_name}{day}的预报"
            
            # 只返回指定那天的预报
            target_day = forecasts[-1] if days > 1 else forecasts[0]
            
            return f"""
📅 {day}{display_name}天气{default_note}
📍 地点: {self.location_handler.format_location(location)}
{target_day.format()}
"""
        except Exception as e:
            error_msg = self._format_error(e, location)
            return error_msg
    
    def handle_few_days(self, query: str, match) -> str:
        """处理'未来几天'查询 - 默认3天"""
        location_text = match.group(1)
        location, default_note = self.extract_location(location_text)
        display_name = self.location_handler.get_location_for_display(location)
        
        # 默认查询3天
        days = 3
        
        try:
            forecasts = self.client.get_weather_forecast(location.name, days)
            
            result = f"📅 {display_name}未来{days}天预报{default_note}\n"
            result += f"📍 地点: {self.location_handler.format_location(location)}\n"
            result += "=" * 50 + "\n"
            
            for i, forecast in enumerate(forecasts):
                day_name = "今天" if i == 0 else f"第{i+1}天"
                result += f"\n{day_name}:\n"
                result += forecast.format() + "\n"
                result += "-" * 50 + "\n"
            
            return result
        except Exception as e:
            error_msg = self._format_error(e, location)
            return error_msg
    
    def handle_forecast_days(self, query: str, match) -> str:
        """处理指定天数预报"""
        city_en, city_cn = self.extract_city(query)
        
        try:
            days = int(match.group(2))
            if days < 1 or days > 7:
                return "❌ 预报天数请选择1-7天"
            
            forecasts = self.client.get_weather_forecast(city_en, days)
            result = f"📅 {city_cn}未来{days}天预报\n"
            result += "=" * 50 + "\n"
            
            for forecast in forecasts:
                result += forecast.format() + "\n"
                result += "-" * 50 + "\n"
            
            return result
        except Exception as e:
            return f"❌ 获取{city_cn}预报失败: {str(e)}"
    
    def handle_forecast(self, query: str, match) -> str:
        """处理天气预报（默认3天）"""
        city_en, city_cn = self.extract_city(query)
        
        try:
            forecasts = self.client.get_weather_forecast(city_en, 3)
            result = f"📅 {city_cn}未来3天预报\n"
            result += "=" * 50 + "\n"
            
            for forecast in forecasts:
                result += forecast.format() + "\n"
                result += "-" * 50 + "\n"
            
            return result
        except Exception as e:
            return f"❌ 获取{city_cn}预报失败: {str(e)}"
    
    def handle_life_indices(self, query: str, match) -> str:
        """处理生活指数查询"""
        city_en, city_cn = self.extract_city(query)
        
        try:
            indices = self.client.get_life_indices(city_en)
            result = f"📊 {city_cn}今日生活指数\n"
            result += "=" * 50 + "\n"
            
            # 分类显示
            categories = {}
            for index in indices:
                if index.category not in categories:
                    categories[index.category] = []
                categories[index.category].append(index)
            
            for category, cat_indices in categories.items():
                result += f"\n{category}:\n"
                for index in cat_indices[:3]:  # 每个类别显示前3个
                    result += f"  {index.format()}\n"
            
            return result
        except Exception as e:
            return f"❌ 获取{city_cn}生活指数失败: {str(e)}"
    
    def handle_air_quality(self, query: str, match) -> str:
        """处理空气质量查询"""
        city_en, city_cn = self.extract_city(query)
        
        try:
            air_data = self.client.get_air_quality(city_en)
            now = air_data["now"]
            
            return f"""
🌫️ {city_cn}空气质量
更新时间: {air_data['updateTime']}
AQI指数: {now['aqi']} ({now['category']})
主要污染物: {now['primary']}
PM2.5: {now['pm2p5']} μg/m³
PM10: {now['pm10']} μg/m³
二氧化硫: {now['so2']} μg/m³
二氧化氮: {now['no2']} μg/m³
臭氧: {now['o3']} μg/m³
一氧化碳: {now['co']} mg/m³

💡 建议: {self._get_air_quality_advice(now['category'])}
"""
        except Exception as e:
            return f"❌ 获取{city_cn}空气质量失败: {str(e)}"
    
    def _get_air_quality_advice(self, category: str) -> str:
        """获取空气质量建议"""
        advice_map = {
            "优": "空气质量非常好，适合户外活动",
            "良": "空气质量良好，基本适合户外活动",
            "轻度污染": "敏感人群减少户外活动",
            "中度污染": "减少户外活动，外出佩戴口罩",
            "重度污染": "避免户外活动，关闭门窗",
            "严重污染": "尽量避免外出，使用空气净化器"
        }
        return advice_map.get(category, "请参考官方空气质量建议")
    
    def handle_umbrella(self, query: str, match) -> str:
        """处理雨伞查询"""
        city_en, city_cn = self.extract_city(query)
        
        try:
            weather = self.client.get_weather_now(city_en)
            umbrella = self.client.get_umbrella_advice(weather.precip, weather.text)
            return f"🌂 {city_cn}{umbrella}"
        except Exception as e:
            return f"❌ 获取{city_cn}天气失败: {str(e)}"
    
    def handle_clothing(self, query: str, match) -> str:
        """处理穿衣查询"""
        city_en, city_cn = self.extract_city(query)
        
        try:
            weather = self.client.get_weather_now(city_en)
            dressing = self.client.get_dressing_advice(weather.temp)
            return f"👕 {city_cn}{dressing}"
        except Exception as e:
            return f"❌ 获取{city_cn}温度失败: {str(e)}"
    
    def handle_help(self, query: str, match) -> str:
        """处理帮助查询"""
        return """
🌤️ 天气查询帮助
==============

常用命令:
1. [城市]天气 - 查询实时天气 (例: 北京天气)
2. [城市]温度 - 查询当前温度
3. [城市]今天/明天/后天天气 - 查询特定日期
4. [城市]预报 - 查询3天预报
5. [城市]未来N天预报 - 查询N天预报
6. [城市]生活指数 - 查询生活指数
7. [城市]空气质量 - 查询空气质量
8. [城市]需要带伞吗 - 雨伞建议
9. [城市]穿什么 - 穿衣建议

支持城市:
北京、上海、广州、深圳、杭州、成都、武汉、南京、西安、重庆

数据来源: 中国气象局 · 和风天气
"""
    
    def handle_default(self, query: str) -> str:
        """默认处理"""
        return f"🤔 我不太明白你的意思。你可以问我关于天气的问题，比如:\n- 北京天气怎么样？\n- 上海未来3天预报\n- 广州生活指数\n\n输入'天气帮助'查看完整帮助。"

# OpenClaw技能接口
class QWeatherSkill:
    """QWeather OpenClaw技能"""
    
    def __init__(self):
        self.handler = OpenClawWeatherHandler()
        self.name = "qweather-china"
        self.version = "1.0.0"
        self.description = "基于中国气象局数据的天气服务"
    
    def process(self, message: str, context: Dict = None) -> str:
        """处理消息"""
        try:
            response = self.handler.handle_query(message)
            return response
        except Exception as e:
            return f"❌ 天气服务暂时不可用: {str(e)}"
    
    def get_capabilities(self) -> List[str]:
        """获取技能能力"""
        return [
            "实时天气查询",
            "天气预报",
            "生活指数",
            "空气质量",
            "穿衣建议",
            "雨伞建议"
        ]
    
    def get_supported_cities(self) -> List[str]:
        """获取支持的城市"""
        return [
            "北京", "上海", "广州", "深圳", "杭州",
            "成都", "武汉", "南京", "西安", "重庆"
        ]

# 测试函数
def test_integration():
    """测试集成"""
    safe_print("测试OpenClaw天气集成...")
    safe_print("=" * 60)
    
    skill = QWeatherSkill()
    handler = OpenClawWeatherHandler()
    
    test_queries = [
        "北京天气怎么样？",
        "上海温度",
        "广州明天天气",
        "深圳未来3天预报",
        "杭州生活指数",
        "成都空气质量",
        "武汉需要带伞吗",
        "南京穿什么",
        "天气帮助",
        "随机查询"
    ]
    
    for query in test_queries:
        safe_print(f"\n📝 查询: {query}")
        safe_print(f"🤖 回复: {handler.handle_query(query)}")
        safe_print("-" * 60)

if __name__ == "__main__":
    test_integration()