#!/usr/bin/env python3
"""
智能天气处理器 - 修复版
修复类型错误，确保稳定运行
"""

import sys
import os
import re
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from encoding_utils import safe_print
from qweather import QWeatherClient
from location_handler import LocationHandler

class SmartWeather:
    """智能天气处理器（修复类型错误）"""
    
    def __init__(self, memory_city="beijing"):
        self.client = QWeatherClient()
        self.loc_handler = LocationHandler()
        self.memory_city = memory_city
    
    def answer(self, question):
        """回答天气问题（带错误处理）"""
        try:
            question = question.strip()
            
            # 1. 确定地点
            location = self._get_location(question)
            city_display = self.loc_handler.get_location_for_display(location)
            
            # 2. 获取天气数据
            weather_now = self.client.get_weather_now(location.name)
            forecasts = self.client.get_weather_forecast(location.name, 1)
            today = forecasts[0] if forecasts else None
            
            # 3. 确保数据类型正确
            weather_now = self._fix_weather_data_types(weather_now)
            if today:
                today = self._fix_forecast_data_types(today)
            
            # 4. 判断问题类型并回答
            if self._is_simple_question(question):
                return self._simple_answer(question, location, city_display, weather_now, today)
            else:
                return self._detailed_answer(location, city_display, weather_now, today)
                
        except Exception as e:
            return f"❌ 查询失败：{str(e)[:100]}"
    
    def _fix_weather_data_types(self, weather):
        """修复实时天气数据类型"""
        # 确保数值字段是数字
        if hasattr(weather, 'temp'):
            weather.temp = float(weather.temp) if weather.temp else 0
        if hasattr(weather, 'feels_like'):
            weather.feels_like = float(weather.feels_like) if weather.feels_like else 0
        if hasattr(weather, 'wind_scale'):
            try:
                weather.wind_scale = int(weather.wind_scale) if weather.wind_scale else 0
            except:
                # 处理"1-2级"这样的格式
                if isinstance(weather.wind_scale, str) and '-' in weather.wind_scale:
                    parts = weather.wind_scale.split('-')
                    if parts:
                        weather.wind_scale = int(parts[0]) if parts[0].isdigit() else 0
                else:
                    weather.wind_scale = 0
        if hasattr(weather, 'humidity'):
            weather.humidity = int(weather.humidity) if weather.humidity else 0
        if hasattr(weather, 'precip'):
            weather.precip = float(weather.precip) if weather.precip else 0
        
        return weather
    
    def _fix_forecast_data_types(self, forecast):
        """修复预报数据类型"""
        if hasattr(forecast, 'temp_min'):
            forecast.temp_min = float(forecast.temp_min) if forecast.temp_min else 0
        if hasattr(forecast, 'temp_max'):
            forecast.temp_max = float(forecast.temp_max) if forecast.temp_max else 0
        if hasattr(forecast, 'precip'):
            forecast.precip = float(forecast.precip) if forecast.precip else 0
        if hasattr(forecast, 'humidity'):
            forecast.humidity = int(forecast.humidity) if forecast.humidity else 0
        if hasattr(forecast, 'uv_index'):
            try:
                forecast.uv_index = int(forecast.uv_index) if forecast.uv_index else 0
            except:
                forecast.uv_index = 0
        
        return forecast
    
    def _get_location(self, question):
        """智能获取地点"""
        # 尝试从问题中提取地点
        location_text = question
        
        # 移除常见天气词（但不移除城市名）
        weather_words = ['怎么样', '要不要', '带伞', '冷不冷', '热不热', '下雨', '风大', '湿度', 
                        '详细', '预报', '天气', '吗', '？', '?']
        for word in weather_words:
            location_text = location_text.replace(word, '')
        
        location_text = location_text.strip()
        
        if location_text:
            # 问题中指定了地点
            return self.loc_handler.parse_input(location_text)
        else:
            # 没有指定地点，使用记忆中的城市
            location = self.loc_handler.parse_input(self.memory_city)
            location.source = "memory"
            return location
    
    def _is_simple_question(self, question):
        """判断是否是简单问题"""
        question_lower = question.lower()
        
        # 简单问题模式
        simple_patterns = [
            r'^天气怎么样',
            r'^要不要带伞',
            r'^冷不冷',
            r'^热不热',
            r'^下雨吗',
            r'^风大吗',
            r'^湿度怎么样',
            r'^雨什么时候停',
            r'^温度多少',
            r'^多少度',
        ]
        
        for pattern in simple_patterns:
            if re.search(pattern, question_lower):
                return True
        
        # 检查简短问题
        if len(question) <= 10:  # 很短的问题通常是简单问题
            simple_words = ['天气', '带伞', '冷不', '热不', '下雨', '风大', '湿度', '温度']
            for word in simple_words:
                if word in question:
                    return True
        
        return False
    
    def _simple_answer(self, question, location, city_display, weather_now, today):
        """生成简洁回答"""
        question_lower = question.lower()
        
        # 地点说明
        if location.source == "memory":
            location_note = f"（您在{city_display}）"
        else:
            location_note = f"（{city_display}）"
        
        # 根据问题关键词回答
        if '天气怎么样' in question_lower or '天气' == question.strip():
            return self._answer_weather_brief(location_note, city_display, weather_now, today)
        
        elif '带伞' in question_lower:
            return self._answer_umbrella_brief(location_note, city_display, weather_now, today)
        
        elif '冷不冷' in question_lower or '冷' in question_lower:
            return self._answer_cold_brief(location_note, city_display, weather_now, today)
        
        elif '热不热' in question_lower or '热' in question_lower:
            return self._answer_hot_brief(location_note, city_display, weather_now, today)
        
        elif '下雨' in question_lower:
            return self._answer_rain_brief(location_note, city_display, weather_now, today)
        
        elif '风大' in question_lower:
            return self._answer_wind_brief(location_note, city_display, weather_now)
        
        elif '湿度' in question_lower:
            return self._answer_humidity_brief(location_note, city_display, weather_now)
        
        elif '温度' in question_lower or '多少度' in question_lower:
            return self._answer_temperature_brief(location_note, city_display, weather_now, today)
        
        # 默认简洁回答
        return self._default_brief_answer(location_note, city_display, weather_now, today)
    
    def _answer_weather_brief(self, location_note, city_display, weather_now, today):
        """回答'天气怎么样'"""
        response = f"{city_display}现在天气{location_note}：\n"
        response += f"• {weather_now.text}，{weather_now.temp}°C"
        if hasattr(weather_now, 'feels_like'):
            response += f"（体感{weather_now.feels_like}°C）\n"
        else:
            response += "\n"
        
        if today:
            response += f"• 今天温度：{today.temp_min}°C ~ {today.temp_max}°C\n"
        
        response += f"• 风力：{weather_now.wind_scale}级"
        if hasattr(weather_now, 'wind_dir') and weather_now.wind_dir:
            response += f" {weather_now.wind_dir}\n"
        else:
            response += "\n"
        
        # 简单建议
        advice = []
        if hasattr(weather_now, 'precip') and weather_now.precip > 0:
            advice.append("有降水")
        elif '雨' in weather_now.text:
            advice.append("可能下雨")
        
        if hasattr(weather_now, 'temp'):
            if weather_now.temp <= 5:
                advice.append("较冷")
            elif weather_now.temp >= 25:
                advice.append("较热")
        
        if advice:
            response += f"• 建议：{'，'.join(advice)}\n"
        
        return response
    
    def _answer_umbrella_brief(self, location_note, city_display, weather_now, today):
        """回答'要不要带伞'"""
        needs_umbrella = False
        reasons = []
        
        if hasattr(weather_now, 'precip') and weather_now.precip > 0:
            needs_umbrella = True
            reasons.append(f"当前降水{weather_now.precip}mm")
        
        if '雨' in weather_now.text:
            needs_umbrella = True
            reasons.append(f"天气：{weather_now.text}")
        
        if today:
            if hasattr(today, 'precip') and today.precip > 0:
                needs_umbrella = True
                reasons.append("今天预报有降水")
            if '雨' in today.text_day or '雨' in today.text_night:
                needs_umbrella = True
                reasons.append("预报有雨")
        
        response = f"{city_display}今天{location_note}：\n"
        
        if needs_umbrella:
            response += "✅ 建议带伞！\n"
            for reason in reasons[:2]:  # 最多显示2个原因
                response += f"• {reason}\n"
        else:
            response += "❌ 不用带伞\n"
            response += f"• 当前：{weather_now.text}"
            if hasattr(weather_now, 'precip'):
                response += f"，降水{weather_now.precip}mm\n"
            else:
                response += "\n"
        
        return response
    
    def _answer_cold_brief(self, location_note, city_display, weather_now, today):
        """回答'冷不冷'"""
        temp = weather_now.temp
        feels_like = getattr(weather_now, 'feels_like', temp)
        
        response = f"{city_display}现在{location_note}：\n"
        response += f"• 温度：{temp}°C"
        if feels_like != temp:
            response += f"（体感{feels_like}°C）\n"
        else:
            response += "\n"
        
        if feels_like <= 0:
            response += "❄️ 非常冷！注意防寒保暖\n"
        elif feels_like <= 10:
            response += "🥶 有点冷，建议穿外套\n"
        elif feels_like <= 20:
            response += "😊 温度适宜，不冷不热\n"
        else:
            response += "😅 不冷，挺暖和的\n"
        
        if today:
            response += f"• 今天温度：{today.temp_min}°C ~ {today.temp_max}°C\n"
        
        return response
    
    def _answer_hot_brief(self, location_note, city_display, weather_now, today):
        """回答'热不热'"""
        temp = weather_now.temp
        feels_like = getattr(weather_now, 'feels_like', temp)
        
        response = f"{city_display}现在{location_note}：\n"
        response += f"• 温度：{temp}°C"
        if feels_like != temp:
            response += f"（体感{feels_like}°C）\n"
        else:
            response += "\n"
        
        if feels_like >= 30:
            response += "🔥 非常热！注意防暑降温\n"
        elif feels_like >= 25:
            response += "🥵 有点热，注意防晒\n"
        elif feels_like >= 20:
            response += "😊 温度适宜，不冷不热\n"
        else:
            response += "😌 不热，挺凉快的\n"
        
        if today:
            response += f"• 今天温度：{today.temp_min}°C ~ {today.temp_max}°C\n"
        
        return response
    
    def _answer_rain_brief(self, location_note, city_display, weather_now, today):
        """回答'下雨吗'"""
        response = f"{city_display}现在{location_note}：\n"
        
        is_raining = ('雨' in weather_now.text or 
                     (hasattr(weather_now, 'precip') and weather_now.precip > 0))
        
        if is_raining:
            response += "🌧️ 正在下雨\n"
            response += f"• 天气：{weather_now.text}\n"
            if hasattr(weather_now, 'precip'):
                response += f"• 降水：{weather_now.precip}mm\n"
            response += "✅ 建议带伞\n"
        else:
            response += "☀️ 没有下雨\n"
            response += f"• 天气：{weather_now.text}\n"
            if hasattr(weather_now, 'precip'):
                response += f"• 降水：{weather_now.precip}mm\n"
            response += "❌ 不用带伞\n"
        
        return response
    
    def _answer_wind_brief(self, location_note, city_display, weather_now):
        """回答'风大吗'"""
        wind_scale = weather_now.wind_scale
        
        response = f"{city_display}现在{location_note}：\n"
        response += f"• 风力：{wind_scale}级"
        if hasattr(weather_now, 'wind_dir') and weather_now.wind_dir:
            response += f" {weather_now.wind_dir}\n"
        else:
            response += "\n"
        
        if wind_scale >= 6:
            response += "💨 风很大！注意安全\n"
        elif wind_scale >= 4:
            response += "🌬️ 风有点大\n"
        elif wind_scale >= 2:
            response += "🍃 微风，很舒适\n"
        else:
            response += "🌫️ 基本无风\n"
        
        return response
    
    def _answer_humidity_brief(self, location_note, city_display, weather_now):
        """回答'湿度怎么样'"""
        humidity = weather_now.humidity
        
        response = f"{city_display}现在{location_note}：\n"
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
    
    def _answer_temperature_brief(self, location_note, city_display, weather_now, today):
        """回答温度相关问题"""
        response = f"{city_display}现在{location_note}：\n"
        response += f"• 当前温度：{weather_now.temp}°C\n"
        
        if hasattr(weather_now, 'feels_like'):
            response += f"• 体感温度：{weather_now.feels_like}°C\n"
        
        if today:
            response += f"• 今天温度范围：{today.temp_min}°C ~ {today.temp_max}°C\n"
        
        return response
    
    def _default_brief_answer(self, location_note, city_display, weather_now, today):
        """默认简洁回答"""
        response = f"{city_display}现在天气{location_note}：\n"
        response += f"• {weather_now.text}，{weather_now.temp}°C\n"
        response += f"• 风力：{weather_now.wind_scale}级\n"
        response += f"• 湿度：{weather_now.humidity}%\n"
        
        if today:
            response += f"• 今天温度：{today.temp_min}°C ~ {today.temp_max}°C\n"
        
        return response
    
    def _detailed_answer(self, location, city_display, weather_now, today):
        """生成详细回答"""
        if location.source == "memory":
            location_note = f"（您在{city_display}）"
        else:
            location_n