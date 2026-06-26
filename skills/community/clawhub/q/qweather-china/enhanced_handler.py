#!/usr/bin/env python3
"""
增强版天气处理器
实现智能地点记忆和分级响应
"""

import sys
import os
import re
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from encoding_utils import safe_print, setup_encoding
from qweather import QWeatherClient
from location_handler import LocationHandler

class EnhancedWeatherHandler:
    """增强版天气处理器"""
    
    def __init__(self, memory_city=None):
        """
        初始化处理器
        memory_city: 从记忆中读取的用户所在城市
        """
        self.client = QWeatherClient()
        self.location_handler = LocationHandler()
        
        # 优先使用记忆中的城市，其次使用默认城市
        if memory_city:
            self.default_city = memory_city
            self.default_source = "memory"
        else:
            # 从环境变量或配置中获取默认城市
            env_city = os.getenv("QWEATHER_DEFAULT_LOCATION", "beijing")
            self.default_city = env_city
            self.default_source = "config"
        
        # 问题类型分类
        self.simple_patterns = {
            # 简洁回答类型
            r'^天气怎么样[？?]?$': 'weather_brief',
            r'^要不要带伞[？?]?$': 'umbrella_brief',
            r'^冷不冷[？?]?$': 'cold_brief',
            r'^热不热[？?]?$': 'hot_brief',
            r'^雨什么时候停[？?]?$': 'rain_stop_brief',
            r'^下雨吗[？?]?$': 'rain_brief',
            r'^风大吗[？?]?$': 'wind_brief',
            r'^湿度怎么样[？?]?$': 'humidity_brief',
            
            # 带地点的简洁问题
            r'^(.*?)天气怎么样[？?]?$': 'weather_brief_with_city',
            r'^(.*?)要不要带伞[？?]?$': 'umbrella_brief_with_city',
            r'^(.*?)冷不冷[？?]?$': 'cold_brief_with_city',
            r'^(.*?)热不热[？?]?$': 'hot_brief_with_city',
            r'^(.*?)下雨吗[？?]?$': 'rain_brief_with_city',
        }
        
        self.detailed_patterns = {
            # 详细回答类型
            r'^详细说说(.*?)天气[？?]?$': 'weather_detailed',
            r'^(.*?)详细天气[？?]?$': 'weather_detailed',
            r'^全面报告(.*?)[？?]?$': 'full_report',
            r'^(.*?)完整天气[？?]?$': 'full_report',
        }
    
    def get_user_city_from_memory(self):
        """从记忆中获取用户所在城市（模拟函数）"""
        # 这里应该从MEMORY.md或其他记忆文件中读取
        # 暂时返回从初始化参数传入的城市
        return self.default_city
    
    def parse_query(self, query):
        """解析用户查询，返回(地点, 问题类型, 响应级别)"""
        query = query.strip()
        
        # 1. 检查是否是简洁问题
        for pattern, qtype in self.simple_patterns.items():
            match = re.match(pattern, query, re.IGNORECASE)
            if match:
                if 'with_city' in qtype:
                    # 带地点的问题
                    location_text = match.group(1).strip()
                    if location_text:
                        location = self.location_handler.parse_input(location_text)
                        return location, qtype.replace('_with_city', ''), 'brief'
                else:
                    # 不带地点的问题，使用记忆中的城市
                    memory_city = self.get_user_city_from_memory()
                    location = self.location_handler.parse_input(memory_city)
                    return location, qtype, 'brief'
        
        # 2. 检查是否是详细问题
        for pattern, qtype in self.detailed_patterns.items():
            match = re.match(pattern, query, re.IGNORECASE)
            if match:
                if match.lastindex and match.group(1):
                    location_text = match.group(1).strip()
                    location = self.location_handler.parse_input(location_text)
                else:
                    memory_city = self.get_user_city_from_memory()
                    location = self.location_handler.parse_input(memory_city)
                return location, qtype, 'detailed'
        
        # 3. 默认：按完整天气查询处理
        # 尝试提取地点
        location_text = query
        # 移除常见天气关键词
        weather_keywords = ['天气', '预报', '温度', '气温', '下雨', '带伞', '冷不冷', '热不热']
        for keyword in weather_keywords:
            location_text = location_text.replace(keyword, '')
        
        location_text = location_text.strip()
        
        if location_text:
            location = self.location_handler.parse_input(location_text)
        else:
            memory_city = self.get_user_city_from_memory()
            location = self.location_handler.parse_input(memory_city)
        
        return location, 'weather_full', 'detailed'
    
    def handle_query(self, query):
        """处理用户查询"""
        # 解析查询
        location, qtype, response_level = self.parse_query(query)
        display_name = self.location_handler.get_location_for_display(location)
        
        # 获取天气数据
        try:
            # 实时天气
            weather_now = self.client.get_weather_now(location.name)
            
            # 今天预报
            forecasts = self.client.get_weather_forecast(location.name, 1)
            today_forecast = forecasts[0] if forecasts else None
            
            # 根据响应级别生成回答
            if response_level == 'brief':
                return self.generate_brief_response(
                    location, display_name, weather_now, today_forecast, qtype
                )
            else:
                return self.generate_detailed_response(
                    location, display_name, weather_now, today_forecast, qtype
                )
                
        except Exception as e:
            return self.generate_error_response(e, location, display_name)
    
    def generate_brief_response(self, location, display_name, weather_now, today_forecast, qtype):
        """生成简洁回答"""
        # 地点说明
        if location.source == "memory":
            location_note = f"（根据记忆，您在{display_name}）"
        elif location.source == "default" or location.source == "default_fallback":
            location_note = f"（按默认地点{display_name}）"
        else:
            location_note = f"（{display_name}）"
        
        # 根据问题类型生成回答
        if qtype == 'weather_brief':
            response = f"{display_name}今天天气{location_note}：\n"
            response += f"• {weather_now.text}，{weather_now.temp}°C（体感{weather_now.feels_like}°C）\n"
            if today_forecast:
                response += f"• 温度：{today_forecast.temp_min}°C ~ {today_forecast.temp_max}°C\n"
            response += f"• 风力：{weather_now.wind_scale}级 {weather_now.wind_dir}\n"
            
            # 简单建议
            if weather_now.precip > 0 or '雨' in weather_now.text:
                response += "• 建议：可能会下雨，建议带伞\n"
            elif weather_now.temp <= 5:
                response += "• 建议：比较冷，注意保暖\n"
            elif weather_now.temp >= 25:
                response += "• 建议：比较热，注意防暑\n"
            
            return response
            
        elif qtype == 'umbrella_brief':
            needs_umbrella = False
            reasons = []
            
            if weather_now.precip > 0:
                needs_umbrella = True
                reasons.append(f"当前有降水（{weather_now.precip}mm）")
            
            if '雨' in weather_now.text:
                needs_umbrella = True
                reasons.append(f"天气描述：{weather_now.text}")
            
            if today_forecast and today_forecast.precip > 0:
                needs_umbrella = True
                reasons.append(f"今天预报有降水")
            
            response = f"{display_name}今天{location_note}：\n"
            
            if needs_umbrella:
                response += "✅ 建议带伞！\n"
                for reason in reasons:
                    response += f"• {reason}\n"
            else:
                response += "❌ 不用带伞\n"
                response += f"• 当前天气：{weather_now.text}\n"
                response += f"• 降水：{weather_now.precip}mm\n"
            
            return response
            
        elif qtype == 'cold_brief':
            temp = weather_now.temp
            feels_like = weather_now.feels_like
            
            response = f"{display_name}现在{location_note}：\n"
            response += f"• 温度：{temp}°C（体感{feels_like}°C）\n"
            
            if feels_like <= 0:
                response += "❄️ 非常冷！注意防寒保暖\n"
            elif feels_like <= 10:
                response += "🥶 有点冷，建议穿外套\n"
            elif feels_like <= 20:
                response += "😊 温度适宜，不冷不热\n"
            else:
                response += "😅 不冷，挺暖和的\n"
            
            if today_forecast:
                response += f"• 今天温度范围：{today_forecast.temp_min}°C ~ {today_forecast.temp_max}°C\n"
            
            return response
            
        elif qtype == 'hot_brief':
            temp = weather_now.temp
            feels_like = weather_now.feels_like
            
            response = f"{display_name}现在{location_note}：\n"
            response += f"• 温度：{temp}°C（体感{feels_like}°C）\n"
            
            if feels_like >= 30:
                response += "🔥 非常热！注意防暑降温\n"
            elif feels_like >= 25:
                response += "🥵 有点热，注意防晒\n"
            elif feels_like >= 20:
                response += "😊 温度适宜，不冷不热\n"
            else:
                response += "😌 不热，挺凉快的\n"
            
            if today_forecast:
                response += f"• 今天温度范围：{today_forecast.temp_min}°C ~ {today_forecast.temp_max}°C\n"
            
            return response
            
        elif qtype == 'rain_stop_brief':
            response = f"{display_name}{location_note}：\n"
            
            if '雨' not in weather_now.text and weather_now.precip == 0:
                response += "✅ 现在没有下雨\n"
            else:
                response += f"• 当前：{weather_now.text}，降水{weather_now.precip}mm\n"
                response += "• 建议关注天气预报，雨停时间不确定\n"
            
            return response
            
        elif qtype == 'rain_brief':
            response = f"{display_name}现在{location_note}：\n"
            
            if '雨' in weather_now.text or weather_now.precip > 0:
                response += "🌧️ 正在下雨\n"
                response += f"• 天气：{weather_now.text}\n"
                response += f"• 降水：{weather_now.precip}mm\n"
                response += "✅ 建议带伞\n"
            else:
                response += "☀️ 没有下雨\n"
                response += f"• 天气：{weather_now.text}\n"
                response += "❌ 不用带伞\n"
            
            return response
            
        elif qtype == 'wind_brief':
            wind_scale = weather_now.wind_scale
            wind_speed = weather_now.wind_speed
            
            response = f"{display_name}现在{location_note}：\n"
            response += f"• 风力：{wind_scale}级（{wind_speed}km/h）{weather_now.wind_dir}\n"
            
            if wind_scale >= 6:
                response += "💨 风很大！注意安全\n"
            elif wind_scale >= 4:
                response += "🌬️ 风有点大\n"
            elif wind_scale >= 2:
                response += "🍃 微风，很舒适\n"
            else:
                response += "🌫️ 基本无风\n"
            
            return response
            
        elif qtype == 'humidity_brief':
            humidity = weather_now.humidity
            
            response = f"{display_name}现在{location_note}：\n"
            response += f"• 湿度：{humidity}%\n"
            
            if humidity >= 80:
                response += "💦 非常潮湿，可能感觉闷热\n"
            elif humidity >= 60:
                response += "💧 湿度适中，比较舒适\n"
            elif humidity >= 40:
                response += "😊 湿度适宜，很舒适\n"
            else:
                response += "🏜️ 比较干燥，注意补水\n"
            
            return response
        
        # 默认简洁回答
        response = f"{display_name}现在天气{location_note}：\n"
        response += f"• {weather_now.text}，{weather_now.temp}°C\n"
        response += f"• 风力：{weather_now.wind_scale}级\n"
        response += f"• 湿度：{weather_now.humidity}%\n"
        
        return response
    
    def generate_detailed_response(self, location, display_name, weather_now, today_forecast, qtype):
        """生成详细回答"""
        # 地点说明
        if location.source == "memory":
            location_note = f"（根据记忆，您在{display_name}）"
        elif location.source == "default" or location.source == "default_fallback":
            location_note = f"（按默认地点{display_name}）"
        else:
            location_note = f"（{display_name}）"
        
        response = f"{display_name}天气报告{location_note}\n"
        response += "=" * 40 + "\n\n"
        
        # 实时天气
        response += "📊 实时天气\n"
        response += "-" * 20 + "\n"
        response += f"• 时间：{weather_now.obs_time}\n"
        response += f"• 天气：{weather_now.text}\n"
        response += f"• 温度：{weather_now.temp}°C（体感{weather_now.feels_like}°C）\n"
        response += f"• 风力：{weather_now.wind_scale}级 {weather_now.wind_dir}（{weather_now.wind_speed}km/h）\n"
        response += f"• 湿度：{weather_now.humidity}%\n"
        response += f"• 降水：{weather_now.precip}mm\n"
        response += f"• 气压：{weather_now.pressure}hPa\n"
        response += f"• 能见度：{weather_now.vis}公里\n"
        response += f"• 云量：{weather_now.cloud}%\n"
        response += f"• 露点：{weather_now.dew}°C\n\n"
        
        # 今天预报
        if today_forecast:
            response += "📅 今天预报\n"
            response += "-" * 20 + "\n"
            response += f"• 日期：{today_forecast.fx_date}\n"
            response += f"• 日出：{today_forecast.sunrise} | 日落：{today_forecast.sunset}\n"
            response += f"• 温度：{today_forecast.temp_min}°C ~ {today_forecast.temp_max}°C\n"
            response += f"• 白天：{today_forecast.text_day}\n"
            response += f"• 夜间：{today_forecast.text_night}\n"
            response += f"• 风力：{today_forecast.wind_scale_day}级 {today_forecast.wind_dir_day}\n"
            response += f"• 湿度：{today_forecast.humidity}%\n"
            response += f"• 降水：{today_forecast.precip}mm\n"
            response += f"• 紫外线：{today_forecast.uv_index}级\n"
            response += f"• 降水概率：{today_forecast.pop}%\n\n"
        
        # 生活建议
        response += "💡 生活建议\n"
        response += "-" * 20 + "\n"
        
        # 穿衣建议
        dressing = self.client.get_dressing_advice(weather_now.temp)
        response += f"• 穿衣：{dressing}\n"
        
        # 雨伞建议
        umbrella = self.client.get_umbrella_advice(weather_now.precip, weather_now.text)
        response += f"• 雨伞：{umbrella}\n"
        
        # 温度建议
        if weather_now.temp <= 5:
            response += "• 保暖：温度较低，注意防寒保暖\n"
        elif weather_now.temp >= 28:
            response += "• 防暑：温度较高，注意防暑降温\n"
        
        # 风力建议
        if weather_now.wind_scale >= 6:
            response += "• 防风：风较大，注意安全\n"
        
        # 湿度建议
        if weather_now.humidity >= 80:
            response += "• 除湿：湿度较高，可能感觉闷热\n"
        elif weather_now.h