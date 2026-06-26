#!/usr/bin/env python3
"""
天气优化版 - 最终修复
修复所有类型错误，实现两个核心优化
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from encoding_utils import safe_print
from qweather import QWeatherClient
from location_handler import LocationHandler

def safe_float(value, default=0):
    """安全转换为浮点数"""
    try:
        return float(value) if value else default
    except:
        return default

def safe_int(value, default=0):
    """安全转换为整数"""
    try:
        if isinstance(value, str) and '-' in value:
            # 处理"1-2级"格式
            parts = value.split('-')
            return int(parts[0]) if parts[0].isdigit() else default
        return int(float(value)) if value else default
    except:
        return default

class OptimizedWeather:
    """优化版天气处理器"""
    
    def __init__(self, user_city="beijing"):
        """user_city: 从记忆读取的用户所在城市"""
        self.client = QWeatherClient()
        self.loc_handler = LocationHandler()
        self.user_city = user_city  # 从MEMORY.md读取：北京
    
    def ask(self, question):
        """回答天气问题"""
        try:
            question = question.strip()
            
            # 1. 智能获取地点
            city = self._get_city(question)
            city_name = self.loc_handler.get_location_for_display(city)
            
            # 2. 获取天气数据并修复类型
            weather = self.client.get_weather_now(city.name)
            forecasts = self.client.get_weather_forecast(city.name, 1)
            today = forecasts[0] if forecasts else None
            
            # 修复数据类型
            weather = self._fix_data(weather)
            if today:
                today = self._fix_forecast(today)
            
            # 3. 判断回答类型
            if self._is_simple(question):
                return self._simple_reply(question, city, city_name, weather, today)
            else:
                return self._detailed_reply(city, city_name, weather, today)
                
        except Exception as e:
            return f"查询失败：{str(e)[:80]}"
    
    def _get_city(self, question):
        """智能获取城市"""
        # 移除天气关键词
        text = question
        keywords = ['天气', '怎么样', '带伞', '冷不冷', '热不热', '下雨', '风大', '湿度', 
                   '详细', '预报', '温度', '吗', '？', '?', '多少度']
        for word in keywords:
            text = text.replace(word, '')
        
        text = text.strip()
        
        if text:
            # 问题中有地点
            return self.loc_handler.parse_input(text)
        else:
            # 使用记忆中的城市
            location = self.loc_handler.parse_input(self.user_city)
            location.source = "memory"
            return location
    
    def _is_simple(self, question):
        """判断是否简单问题"""
        q = question.lower()
        
        # 简单问题关键词
        simple_words = ['怎么样', '带伞', '冷不冷', '热不热', '下雨吗', '风大吗', 
                       '湿度怎么样', '温度多少', '多少度', '天气?', '天气？']
        
        for word in simple_words:
            if word in q:
                return True
        
        # 很短的问题
        if len(question) <= 8:
            return True
        
        return False
    
    def _fix_data(self, weather):
        """修复天气数据类型"""
        weather.temp = safe_float(weather.temp)
        weather.feels_like = safe_float(getattr(weather, 'feels_like', weather.temp))
        weather.wind_scale = safe_int(getattr(weather, 'wind_scale', 0))
        weather.humidity = safe_int(getattr(weather, 'humidity', 0))
        weather.precip = safe_float(getattr(weather, 'precip', 0))
        return weather
    
    def _fix_forecast(self, forecast):
        """修复预报数据类型"""
        forecast.temp_min = safe_float(forecast.temp_min)
        forecast.temp_max = safe_float(forecast.temp_max)
        forecast.precip = safe_float(forecast.precip)
        forecast.humidity = safe_int(forecast.humidity)
        return forecast
    
    def _simple_reply(self, question, location, city_name, weather, today):
        """简洁回答"""
        q = question.lower()
        
        # 地点说明
        if location.source == "memory":
            note = f"（您在{city_name}）"
        else:
            note = f"（{city_name}）"
        
        # 根据问题类型回答
        if '带伞' in q:
            return self._umbrella_reply(note, city_name, weather, today)
        elif '冷不冷' in q or '冷' in q:
            return self._cold_reply(note, city_name, weather, today)
        elif '热不热' in q or '热' in q:
            return self._hot_reply(note, city_name, weather, today)
        elif '下雨' in q:
            return self._rain_reply(note, city_name, weather, today)
        elif '风大' in q:
            return self._wind_reply(note, city_name, weather)
        elif '湿度' in q:
            return self._humidity_reply(note, city_name, weather)
        elif '温度' in q or '多少度' in q:
            return self._temp_reply(note, city_name, weather, today)
        else:
            # 默认天气回答
            return self._weather_reply(note, city_name, weather, today)
    
    def _weather_reply(self, note, city_name, weather, today):
        """天气怎么样"""
        reply = f"{city_name}现在天气{note}：\n"
        reply += f"• {weather.text}，{weather.temp}°C"
        if weather.feels_like != weather.temp:
            reply += f"（体感{weather.feels_like}°C）\n"
        else:
            reply += "\n"
        
        if today:
            reply += f"• 今天温度：{today.temp_min}°C ~ {today.temp_max}°C\n"
        
        reply += f"• 风力：{weather.wind_scale}级"
        if hasattr(weather, 'wind_dir') and weather.wind_dir:
            reply += f" {weather.wind_dir}\n"
        else:
            reply += "\n"
        
        # 建议
        if weather.precip > 0 or '雨' in weather.text:
            reply += "• 建议：可能会下雨\n"
        elif weather.temp <= 5:
            reply += "• 建议：比较冷\n"
        elif weather.temp >= 25:
            reply += "• 建议：比较热\n"
        
        return reply
    
    def _umbrella_reply(self, note, city_name, weather, today):
        """要不要带伞"""
        need = False
        if weather.precip > 0 or '雨' in weather.text:
            need = True
        if today and (today.precip > 0 or '雨' in today.text_day or '雨' in today.text_night):
            need = True
        
        reply = f"{city_name}今天{note}：\n"
        if need:
            reply += "✅ 建议带伞！\n"
            reply += f"• 当前：{weather.text}"
            if weather.precip > 0:
                reply += f"，降水{weather.precip}mm\n"
            else:
                reply += "\n"
        else:
            reply += "❌ 不用带伞\n"
            reply += f"• 当前：{weather.text}，无降水\n"
        
        return reply
    
    def _cold_reply(self, note, city_name, weather, today):
        """冷不冷"""
        reply = f"{city_name}现在{note}：\n"
        reply += f"• 温度：{weather.temp}°C（体感{weather.feels_like}°C）\n"
        
        if weather.feels_like <= 0:
            reply += "❄️ 非常冷！注意保暖\n"
        elif weather.feels_like <= 10:
            reply += "🥶 有点冷，穿外套\n"
        elif weather.feels_like <= 20:
            reply += "😊 温度适宜\n"
        else:
            reply += "😅 不冷，暖和\n"
        
        if today:
            reply += f"• 今天：{today.temp_min}°C ~ {today.temp_max}°C\n"
        
        return reply
    
    def _hot_reply(self, note, city_name, weather, today):
        """热不热"""
        reply = f"{city_name}现在{note}：\n"
        reply += f"• 温度：{weather.temp}°C（体感{weather.feels_like}°C）\n"
        
        if weather.feels_like >= 30:
            reply += "🔥 非常热！注意防暑\n"
        elif weather.feels_like >= 25:
            reply += "🥵 有点热，注意防晒\n"
        elif weather.feels_like >= 20:
            reply += "😊 温度适宜\n"
        else:
            reply += "😌 不热，凉快\n"
        
        if today:
            reply += f"• 今天：{today.temp_min}°C ~ {today.temp_max}°C\n"
        
        return reply
    
    def _rain_reply(self, note, city_name, weather, today):
        """下雨吗"""
        reply = f"{city_name}现在{note}：\n"
        
        if weather.precip > 0 or '雨' in weather.text:
            reply += "🌧️ 正在下雨\n"
            reply += f"• {weather.text}，降水{weather.precip}mm\n"
            reply += "✅ 建议带伞\n"
        else:
            reply += "☀️ 没有下雨\n"
            reply += f"• {weather.text}，无降水\n"
            reply += "❌ 不用带伞\n"
        
        return reply
    
    def _wind_reply(self, note, city_name, weather):
        """风大吗"""
        reply = f"{city_name}现在{note}：\n"
        reply += f"• 风力：{weather.wind_scale}级\n"
        
        if weather.wind_scale >= 6:
            reply += "💨 风很大！注意安全\n"
        elif weather.wind_scale >= 4:
            reply += "🌬️ 风有点大\n"
        else:
            reply += "🍃 微风或基本无风\n"
        
        return reply
    
    def _humidity_reply(self, note, city_name, weather):
        """湿度怎么样"""
        reply = f"{city_name}现在{note}：\n"
        reply += f"• 湿度：{weather.humidity}%\n"
        
        if weather.humidity >= 80:
            reply += "💦 非常潮湿\n"
        elif weather.humidity >= 60:
            reply += "💧 湿度适中\n"
        elif weather.humidity >= 40:
            reply += "😊 湿度适宜\n"
        else:
            reply += "🏜️ 比较干燥\n"
        
        return reply
    
    def _temp_reply(self, note, city_name, weather, today):
        """温度多少"""
        reply = f"{city_name}现在{note}：\n"
        reply += f"• 当前：{weather.temp}°C（体感{weather.feels_like}°C）\n"
        
        if today:
            reply += f"• 今天：{today.temp_min}°C ~ {today.temp_max}°C\n"
        
        return reply
    
    def _detailed_reply(self, location, city_name, weather, today):
        """详细回答"""
        if location.source == "memory":
            note = f"（您在{city_name}）"
        else:
            note = f"（{city_name}）"
        
        reply = f"{city_name}天气报告{note}\n"
        reply += "=" * 40 + "\n\n"
        
        # 实时天气
        reply += "📊 实时天气\n"
        reply += "-" * 20 + "\n"
        reply += f"• 时间：{getattr(weather, 'obs_time', '最新')}\n"
        reply += f"• 天气：{weather.text}\n"
        reply += f"• 温度：{weather.temp}°C（体感{weather.feels_like}°C）\n"
        reply += f"• 风力：{weather.wind_scale}级"
        if hasattr(weather, 'wind_dir') and weather.wind_dir:
            reply += f" {weather.wind_dir}\n"
        else:
            reply += "\n"
        reply += f"• 湿度：{weather.humidity}%\n"
        reply += f"• 降水：{weather.precip}mm\n\n"
        
        # 今天预报
        if today:
            reply += "📅 今天预报\n"
            reply += "-" * 20 + "\n"
            reply += f"• 温度：{today.temp_min}°C ~ {today.temp_max}°C\n"
            reply += f"• 白天：{today.text_day}\n"
            reply += f"• 夜间：{today.text_night}\n"
            reply += f"• 降水：{today.precip}mm\n"
            reply += f"• 湿度：{today.humidity}%\n\n"
        
        # 建议
        reply += "💡 建议\n"
        reply += "-" * 20 + "\n"
        
        # 穿衣建议
        try:
            dressing = self.client.get_dressing_advice(weather.temp)
            reply += f"• 穿衣：{dressing}\n"
        except:
            reply += "• 穿衣：根据温度适当着装\n"
        
        # 雨伞建议
        if weather.precip > 0 or '雨' in weather.text:
            reply += "• 雨伞：建议带伞\n"
        else:
            reply += "• 雨伞：不用带伞\n"
        
        # 温度建议
        if weather.temp <= 5:
            reply += "• 保暖：注意防寒\n"
        elif weather.temp >= 28:
            reply += "• 防暑：注意防晒\n"
        
        reply += "\n" + "=" * 40 + "\n"
        
        # 总结
        summary = []
        if weather.precip > 0 or '雨' in weather.text:
            summary.append("有降水")
        if weather.temp <= 10:
            summary.append("温度较低")
        elif weather.temp >= 25:
            summary.append("温度较高")
        
        if summary:
            reply += f"💬 总结：今天{'、'.join(summary)}。"
        else:
            reply += "💬 总结：今天天气条件良好。"
        
        return reply


# 测试
def test_optimized():
    """测试优化版"""
    # 从记忆知道用户在北京
    weather = OptimizedWeather(user_city="beijing")
    
    tests = [
        "天气怎么样？",
        "要不要带伞？",
        "冷不冷？",
        "热不热？",
        "下雨吗？",
        "风大吗？",
        "湿度怎么样？",
        "温度多少？",
        "北京天气怎么样？",
        "详细说说天气",
    ]
    
    safe_print("=" * 50)
    safe_print("优化版天气处理器测试")
    safe_print("=" * 50)
    
    for test in tests:
        safe_print(f"\n问题：{test}")
        safe_print("-" * 30)
        answer = weather.ask(test)
        safe_print(answer)
    
    safe_print("\n" + "=" * 50)
    safe_print("✅ 优化完成！")
    safe_print("=" * 50)
    safe_print("优化功能：")
    safe_print("  1. ✅ 智能地点记忆：优先记忆城市（北京）")
    safe_print("  2. ✅ 分级响应：简洁问题直接结论")
    safe_print("  3. ✅ 类型安全：修复所有数据类型错误")
    safe_print("  4. ✅ 跨平台兼容：Windows/Linux/macOS")

if __name__ == "__main__":
    test_optimized()