#!/usr/bin/env python3
"""
修复：确保所有含义相同的简单问题都得到简洁回答
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from encoding_utils import safe_print
from qweather import QWeatherClient
from location_handler import LocationHandler

class FixedSimpleWeather:
    """修复版：确保含义相同的问题都简洁回答"""
    
    def __init__(self, user_city="beijing"):
        self.client = QWeatherClient()
        self.loc_handler = LocationHandler()
        self.user_city = user_city
    
    def ask(self, question):
        """回答天气问题（修复版）"""
        try:
            question = question.strip()
            
            # 获取地点
            city = self._get_city(question)
            city_name = self.loc_handler.get_location_for_display(city)
            
            # 获取天气数据
            weather = self.client.get_weather_now(city.name)
            forecasts = self.client.get_weather_forecast(city.name, 1)
            today = forecasts[0] if forecasts else None
            
            # 安全转换
            weather = self._fix_data(weather)
            if today:
                today = self._fix_forecast(today)
            
            # 判断是否是简单问题
            if self._is_simple_question(question):
                return self._simple_answer(question, city, city_name, weather, today)
            else:
                return self._detailed_answer(city, city_name, weather, today)
                
        except Exception as e:
            return f"查询失败：{str(e)[:80]}"
    
    def _is_simple_question(self, question):
        """判断是否是简单问题（修复版）"""
        q = question.lower()
        
        # 详细问题关键词
        detailed_keywords = ['详细', '完整', '全面', '报告', '预报']
        for keyword in detailed_keywords:
            if keyword in q:
                return False
        
        # 简单问题关键词（更全面的列表）
        simple_keywords = [
            # 天气相关
            '天气', '天气怎么样', '天气如何',
            # 温度相关
            '冷', '热', '冷不冷', '热不热', '冷吗', '热吗',
            '温度', '多少度', '温度多少',
            # 降水相关
            '伞', '带伞', '雨伞', '下雨', '有雨',
            # 风力相关
            '风', '风力', '风大',
            # 湿度相关
            '湿度', '潮湿',
            # 简短问题
            '吗', '呢', '呀', '啊'
        ]
        
        # 检查是否包含简单关键词
        for keyword in simple_keywords:
            if keyword in q:
                return True
        
        # 默认：如果问题很短，认为是简单问题
        return len(q) <= 12
    
    def _get_city(self, question):
        """获取城市"""
        # 简单移除关键词
        text = question.lower()
        keywords = ['现在', '外面', '今天', '吗', '？', '?', '呢', '呀', '啊']
        
        for word in keywords:
            text = text.replace(word, '')
        
        text = text.strip()
        
        if text:
            return self.loc_handler.parse_input(text)
        else:
            location = self.loc_handler.parse_input(self.user_city)
            location.source = "memory"
            return location
    
    def _fix_data(self, weather):
        """修复数据"""
        def safe_float(v):
            try:
                return float(v) if v else 0
            except:
                return 0
        
        def safe_int(v):
            try:
                if isinstance(v, str) and '-' in v:
                    return int(v.split('-')[0]) if v.split('-')[0].isdigit() else 0
                return int(float(v)) if v else 0
            except:
                return 0
        
        weather.temp = safe_float(weather.temp)
        weather.feels_like = safe_float(getattr(weather, 'feels_like', weather.temp))
        weather.wind_scale = safe_int(getattr(weather, 'wind_scale', 0))
        weather.humidity = safe_int(getattr(weather, 'humidity', 0))
        weather.precip = safe_float(getattr(weather, 'precip', 0))
        return weather
    
    def _fix_forecast(self, forecast):
        """修复预报数据"""
        def safe_float(v):
            try:
                return float(v) if v else 0
            except:
                return 0
        
        forecast.temp_min = safe_float(forecast.temp_min)
        forecast.temp_max = safe_float(forecast.temp_max)
        forecast.precip = safe_float(forecast.precip)
        return forecast
    
    def _simple_answer(self, question, location, city_name, weather, today):
        """简洁回答（修复版）"""
        q = question.lower()
        
        # 地点说明
        if location.source == "memory":
            location_note = "您在北京"
        else:
            location_note = city_name
        
        # 根据问题内容判断回答类型
        if '带伞' in q or '伞' in q:
            return self._answer_umbrella(location_note, weather, today)
        elif '冷' in q:
            return self._answer_cold(location_note, weather, today)
        elif '热' in q:
            return self._answer_hot(location_note, weather, today)
        elif '下雨' in q or '有雨' in q:
            return self._answer_rain(location_note, weather, today)
        elif '风' in q:
            return self._answer_wind(location_note, weather)
        elif '湿度' in q:
            return self._answer_humidity(location_note, weather)
        elif '温度' in q or '多少度' in q:
            return self._answer_temperature(location_note, weather, today)
        else:
            # 默认：天气怎么样
            return self._answer_weather(location_note, weather, today)
    
    def _answer_weather(self, location_note, weather, today):
        """简洁：天气怎么样"""
        reply = f"{location_note}现在：{weather.text}，{weather.temp}°C"
        
        if weather.feels_like != weather.temp:
            reply += f"（体感{weather.feels_like}°C）"
        
        reply += f"，{weather.wind_scale}级风"
        
        if today:
            reply += f"，今天{today.temp_min}°C~{today.temp_max}°C"
        
        return reply
    
    def _answer_umbrella(self, location_note, weather, today):
        """简洁：要不要带伞"""
        if weather.precip > 0 or '雨' in weather.text:
            return f"{location_note}：建议带伞！当前{weather.text}，降水{weather.precip}mm"
        else:
            return f"{location_note}：不用带伞。当前{weather.text}，无降水"
    
    def _answer_cold(self, location_note, weather, today):
        """简洁：冷不冷"""
        feels_like = weather.feels_like
        
        if feels_like <= 5:
            reply = f"{location_note}：比较冷 🥶 体感{feels_like}°C"
        elif feels_like <= 10:
            reply = f"{location_note}：有点冷 🧥 体感{feels_like}°C"
        elif feels_like <= 15:
            reply = f"{location_note}：微凉 😌 体感{feels_like}°C"
        else:
            reply = f"{location_note}：不冷 😊 体感{feels_like}°C"
        
        if today:
            reply += f"，今天{today.temp_min}°C~{today.temp_max}°C"
        
        return reply
    
    def _answer_hot(self, location_note, weather, today):
        """简洁：热不热"""
        feels_like = weather.feels_like
        
        if feels_like >= 30:
            reply = f"{location_note}：很热 🥵 体感{feels_like}°C"
        elif feels_like >= 25:
            reply = f"{location_note}：有点热 😓 体感{feels_like}°C"
        else:
            reply = f"{location_note}：不热 😊 体感{feels_like}°C"
        
        if today:
            reply += f"，今天最高{today.temp_max}°C"
        
        return reply
    
    def _answer_rain(self, location_note, weather, today):
        """简洁：下雨吗"""
        if '雨' in weather.text or weather.precip > 0:
            return f"{location_note}：正在下雨 🌧️ {weather.text}"
        else:
            return f"{location_note}：没有下雨 ☀️ {weather.text}"
    
    def _answer_wind(self, location_note, weather):
        """简洁：风大吗"""
        if weather.wind_scale >= 4:
            return f"{location_note}：风有点大 🌬️ {weather.wind_scale}级"
        elif weather.wind_scale >= 2:
            return f"{location_note}：微风 🍃 {weather.wind_scale}级"
        else:
            return f"{location_note}：基本无风 🌫️ {weather.wind_scale}级"
    
    def _answer_humidity(self, location_note, weather):
        """简洁：湿度怎么样"""
        if weather.humidity >= 80:
            return f"{location_note}：非常潮湿 💦 {weather.humidity}%"
        elif weather.humidity >= 60:
            return f"{location_note}：湿度适中 💧 {weather.humidity}%"
        elif weather.humidity >= 40:
            return f"{location_note}：湿度适宜 😊 {weather.humidity}%"
        else:
            return f"{location_note}：比较干燥 🏜️ {weather.humidity}%"
    
    def _answer_temperature(self, location_note, weather, today):
        """简洁：温度多少"""
        reply = f"{location_note}：{weather.temp}°C"
        
        if weather.feels_like != weather.temp:
            reply += f"（体感{weather.feels_like}°C）"
        
        if today:
            reply += f"，今天{today.temp_min}°C~{today.temp_max}°C"
        
        return reply
    
    def _detailed_answer(self, location, city_name, weather, today):
        """详细回答"""
        if location.source == "memory":
            location_note = "根据记忆您在北京"
        else:
            location_note = city_name
        
        reply = f"{location_note}，现在天气：\n\n"
        reply += f"天气：{weather.text}\n"
        reply += f"温度：{weather.temp}°C（体感{weather.feels_like}°C）\n"
        
        if today:
            reply += f"今天温度：{today.temp_min}°C ~ {today.temp_max}°C\n"
        
        reply += f"风力：{weather.wind_scale}级\n"
        reply += f"湿度：{weather.humidity}%\n"
        
        if weather.precip > 0:
            reply += f"降水：{weather.precip}mm\n"
        
        return reply


# 测试
def test_fixed():
    """测试修复版"""
    weather = FixedSimpleWeather(user_city="beijing")
    
    # 测试含义相同的问题
    test_questions = [
        "现在外面冷不冷？",
        "冷不冷？", 
        "天气怎么样？",
        "天气如何？",
        "风大吗？",
        "风力大吗？",
        "热不热？",
        "外面热不热？",
        "要不要带伞？",
        "需要带伞吗？",
        "下雨吗？",
        "有雨吗？",
        "湿度怎么样？",
        "湿度如何？",
        "温度多少？",
        "现在多少度？",
    ]
    
    safe_print("测试含义相同的问题是否都得到简洁回答：")
    safe_print("=" * 50)
    
    for question in test_questions:
        safe_print(f"\n问题：{question}")
        answer = weather.ask(question)
        safe_print(f"回答：{answer}")
        
        # 检查是否是简洁回答
        if len(answer.split('\n')) == 1:
            safe_print("✅ 简洁回答")
        else:
            safe_print("⚠️ 可能不是简洁回答")
    
    safe_print("\n" + "=" * 50)
    safe_print("修复完成！")

if __name__ == "__main__":
    test_fixed()