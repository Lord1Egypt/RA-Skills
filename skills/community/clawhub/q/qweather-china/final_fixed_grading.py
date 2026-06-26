#!/usr/bin/env python3
"""
最终修复版分级响应
修复：确保所有含义相同的简单问题都得到简洁回答
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from encoding_utils import safe_print
from qweather import QWeatherClient
from location_handler import LocationHandler

class FixedGradingWeather:
    """修复版分级响应的天气回答"""
    
    def __init__(self, user_city="beijing"):
        self.client = QWeatherClient()
        self.loc_handler = LocationHandler()
        self.user_city = user_city
        
        # 更全面的简单问题模式
        self.simple_patterns = {
            'weather': ['天气', '天气怎么样', '天气如何', '天气情况', '现在天气'],
            'umbrella': ['伞', '带伞', '雨伞', '要不要带伞', '需要带伞', '带伞吗'],
            'cold': ['冷', '冷不冷', '冷吗', '外面冷不冷', '现在冷不冷', '温度冷'],
            'hot': ['热', '热不热', '热吗', '外面热不热', '现在热不热', '温度热'],
            'rain': ['雨', '下雨', '有雨', '下雨吗', '有雨吗', '会下雨吗'],
            'wind': ['风', '风力', '风大', '风大吗', '风力大吗', '风大不大'],
            'humidity': ['湿度', '湿度怎么样', '湿度如何', '湿度情况', '潮湿'],
            'temperature': ['温度', '多少度', '温度多少', '现在温度', '当前温度'],
        }
        
        # 详细问题模式
        self.detailed_patterns = ['详细', '完整', '全面', '报告', '预报', '天气报告']
    
    def ask(self, question):
        """回答天气问题（修复版）"""
        try:
            question = question.strip()
            
            # 判断问题类型
            question_type = self._get_question_type(question)
            
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
            
            # 生成回答
            if question_type == 'simple':
                return self._simple_answer(question, city, city_name, weather, today)
            else:
                return self._detailed_answer(city, city_name, weather, today)
                
        except Exception as e:
            return f"查询失败：{str(e)[:80]}"
    
    def _get_question_type(self, question):
        """判断问题类型（修复版）"""
        q = question.lower()
        
        # 检查是否是详细问题
        for pattern in self.detailed_patterns:
            if pattern in q:
                return 'detailed'
        
        # 检查是否是简单问题（更宽松的判断）
        for category, patterns in self.simple_patterns.items():
            for pattern in patterns:
                if pattern in q:
                    return 'simple'
        
        # 默认：如果问题很短，认为是简单问题
        if len(q) <= 10:
            return 'simple'
        else:
            return 'detailed'
    
    def _get_city(self, question):
        """获取城市"""
        # 移除所有可能的关键词
        text = question.lower()
        
        # 收集所有关键词
        all_keywords = []
        for patterns in self.simple_patterns.values():
            all_keywords.extend(patterns)
        all_keywords.extend(self.detailed_patterns)
        all_keywords.extend(['现在', '今天', '外面', '吗', '？', '?', '呢', '啊', '呀'])
        
        # 按长度排序，先移除长关键词
        all_keywords.sort(key=len, reverse=True)
        
        for keyword in all_keywords:
            text = text.replace(keyword, '')
        
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
        
        # 根据关键词判断问题类型
        for category, patterns in self.simple_patterns.items():
            for pattern in patterns:
                if pattern in q:
                    # 找到匹配的关键词，调用对应的回答函数
                    if category == 'weather':
                        return self._answer_weather_simple(location_note, weather, today)
                    elif category == 'umbrella':
                        return self._answer_umbrella_simple(location_note, weather, today)
                    elif category == 'cold':
                        return self._answer_cold_simple(location_note, weather, today)
                    elif category == 'hot':
                        return self._answer_hot_simple(location_note, weather, today)
                    elif category == 'rain':
                        return self._answer_rain_simple(location_note, weather, today)
                    elif category == 'wind':
                        return self._answer_wind_simple(location_note, weather)
                    elif category == 'humidity':
                        return self._answer_humidity_simple(location_note, weather)
                    elif category == 'temperature':
                        return self._answer_temperature_simple(location_note, weather, today)
        
        # 默认：天气怎么样
        return self._answer_weather_simple(location_note, weather, today)
    
    def _answer_weather_simple(self, location_note, weather, today):
        """简洁：天气怎么样"""
        reply = f"{location_note}现在：{weather.text}，{weather.temp}°C"
        
        if weather.feels_like != weather.temp:
            reply += f"（体感{weather.feels_like}°C）"
        
        reply += f"，{weather.wind_scale}级风"
        
        if today:
            reply += f"，今天{today.temp_min}°C~{today.temp_max}°C"
        
        # 简单建议
        if weather.precip > 0 or '雨' in weather.text:
            reply += "。建议带伞"
        elif weather.temp <= 5:
            reply += "。比较冷，注意保暖"
        elif weather.temp >= 25:
            reply += "。比较热，注意防暑"
        
        return reply
    
    def _answer_umbrella_simple(self, location_note, weather, today):
        """简洁：要不要带伞"""
        needs_umbrella = False
        if weather.precip > 0 or '雨' in weather.text:
            needs_umbrella = True
        if today and (today.precip > 0 or '雨' in today.text_day or '雨' in today.text_night):
            needs_umbrella = True
        
        if needs_umbrella:
            return f"{location_note}：建议带伞！当前{weather.text}，降水{weather.precip}mm"
        else:
            return f"{location_note}：不用带伞。当前{weather.text}，无降水"
    
    def _answer_cold_simple(self, location_note, weather, today):
        """简洁：冷不冷"""
        feels_like = weather.feels_like
        
        if feels_like <= 0:
            reply = f"{location_note}：非常冷！❄️ 体感{feels_like}°C"
        elif feels_like <= 5:
            reply = f"{location_note}：比较冷 🥶 体感{feels_like}°C"
        elif feels_like <= 10:
            reply = f"{location_note}：有点冷 🧥 体感{feels_like}°C"
        elif feels_like <= 15:
            reply = f"{location_note}：微凉 😌 体感{feels_like}°C"
        elif feels_like <= 20:
            reply = f"{location_note}：温度适宜 😊 体感{feels_like}°C"
        else:
            reply = f"{location_note}：不冷 😅 体感{feels_like}°C"
        
        if today:
            reply += f"，今天{today.temp_min}°C~{today.temp_max}°C"
        
        return reply
    
    def _answer_hot_simple(self, location_note, weather, today):
        """简洁：热不热"""
        feels_like = weather.feels_like
        
        if feels_like >= 35:
            reply = f"{location_note}：非常热！🔥 体感{feels_like}°C"
        elif feels_like >= 30:
            reply = f"{location_note}：很热 🥵 体感{feels_like}°C"
        elif feels_like >= 28:
            reply = f"{location_note}：有点热 😓 体感{feels_like}°C"
        elif feels_like >= 25:
            reply = f"{location_note}：温暖 😌 体感{feels_like}°C"
        elif feels_like >= 20:
            reply = f"{location_note}：温度适宜 😊 体感{feels_like}°C"
        else:
            reply = f"{location_note}：不热 🍃 体感{feels_like}°C"
        
        if today:
            reply += f"，今天最高{today.temp_max}°C"
        
        return reply
    
    def _answer_rain_simple(self, location_note, weather, today):
        """简洁：下雨吗"""
        if '雨' in weather.text or weather.precip > 0:
            return f"{location_note}：正在下雨 🌧️ {weather.text}，降水{weather.precip}mm"
        else:
            return f"{location_note}：没有下雨 ☀️ {weather.text}，无降水"
    
    def _answer_wind_simple(self, location_note, weather):
        """简洁：风大吗"""
        if weather.wind_scale >= 6:
            return f"{location_note}：风很大！💨 {weather.wind_scale}级"
        elif weather.wind_scale >= 4:
            return f"{location_note}：风有点大 🌬️ {weather.wind_scale}级"
        elif weather.wind_scale >= 2:
            return f"{location_note}：微风 🍃 {weather.wind_scale}级"
        else:
            return f"{location_note}：基本无风 🌫️ {weather.wind_scale}级"
    
    def _answer_humidity_simple(self, location_note, weather):
        """简洁：湿度怎么样"""
        if weather.humidity >= 80:
            return f"{location_note}：非常潮湿 💦 {weather.humidity}%"
        elif weather.humidity >= 60:
            return f"{location_note}：湿度适中 💧 {weather.humidity}%"
        elif weather.humidity >= 40:
            return f"{location_note}：湿度适宜 😊 {weather.humidity}%"
        else:
            return f"{location_note}：比较干燥 🏜️ {weather.humidity}%"
    
    def _answer_temperature_simple(self, location_note, weather, today):
        """简洁：温度多少"""
        reply = f"{location_note}：{weather.temp}°C"
        
        if weather.feels_like != weather.temp:
            reply += f"（体感{weather.feels_like}°C）"
        
        if today:
            reply += f"，今天{today.temp_min}°C~{today.temp_max}°C"
        
        return reply
    
    def _detailed_answer(self, location, city_name, weather, today):
        """详细回答（完整信息）"""
        if location.source == "memory":
            location_note = "根据记忆您在北京"
        else:
            location_note = city_name
        
        reply = f"{location_note}，现在天气：\n\n"
        
        # 结论
        if '晴' in weather.text and weather.wind_scale < 4:
            reply += "💬 **结论**：现在天气很好，适合外出！☀️\n\n"
        elif '雨' in weather.text or weather.precip > 0:
            reply += "💬 **结论**：现在有降水，建议做好防雨准备。\n\n"
        elif weather.temp <= 5:
            reply += "💬 **结论**：现在比较冷，注意保暖。\n\n"
        elif weather.temp >= 25:
            reply += "💬 **结论**：现在比较热，注意防暑。\n\n"
        else:
            reply += "💬 **结论**：现在天气条件良好。\n\n"
        
        # 关键数据
        reply += "📊 **关键数据**：\n"
        reply += f"• 天气：{weather.text}\n"
        reply += f"• 温度：{weather.temp}°C（体感{weather.feels_like}°C）\n"
        
        if today:
            reply += f"• 今天温度：{today.temp_min}°C ~ {today.temp_max}°C\n"
        
        reply += f"• 风力：{weather.wind_scale}级"
        if hasattr(weather, 'wind_dir') and weather.wind_dir:
            reply += f" {weather.wind_dir}\n"
        else:
            reply += "\n"
        
        reply += f"• 湿度：{weather.humidity}%\n"
        
        if weather.precip > 0:
            reply += f"• 降水：{weather.precip}mm\n"
        
        reply += "\n"
        
        # 建议
        reply += "💡 **建议**：\n"
        
        if weather.temp <= 5:
            reply += "• 穿衣：比较冷，建议穿厚外套\n"
        elif weather.temp <= 15:
            reply += "• 穿衣：温度适宜，建议穿外套\n"
        elif weather.temp <= 25:
            reply += "• 穿衣：比较温暖，建议穿长袖\n"
        else:
            reply += "• 穿衣：比较热，建议穿短袖\n"
        
        if weather.precip > 0 or '雨' in weather.text:
            reply += "• 雨伞：正在下雨，建议带伞\n"
        else:
            reply += "• 雨伞：无降水，不用带伞\n"
        
        if weather.humidity >= 80:
            reply += "• 湿度：湿度很高，可能感觉闷热\n"
        elif weather.humidity <= 40:
            reply += "• 湿度：湿度较低，注意补水保湿\n"
        
        if today and abs(today.temp_max - today.temp_min) >= 10:
            reply += "• 温差：今天温差较大，注意适时增减衣物\n"
        
        return reply


# 测试
def test_fixed_grading():
    """测试修复版分级响应"""
    weather = FixedGradingWeather(user_city="beijing")
    
    # 测试含义相同但问法不同的问题
    test_cases = [
        ("现在外面冷不冷？", "冷不冷？"),
        ("天气怎么样？", "天气如何？"),
        ("风大吗？", "风力大吗？"),
        ("热不热？", "外面热不热？"),
        ("要不要带伞？", "需要带伞吗？"),
        ("下雨吗？", "有雨吗？"),
        ("湿度怎么样？", "湿度如何？"),
        ("温度多少？", "现在多少度？"),
        ("详细说说天气", "给我完整的天气报告"),
    ]
    
    safe_print("=" * 60)
    safe_print("修复版分级响应测试")
    safe_print("确保含义相同的问题都得到简洁回答")
    safe_print("=" * 60)
    
    all_passed = True
    
    for q1, q2 in test_cases:
