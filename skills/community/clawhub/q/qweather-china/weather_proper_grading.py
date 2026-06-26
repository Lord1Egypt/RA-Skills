#!/usr/bin/env python3
"""
正确实现分级响应的天气回答
严格按照优化约定：
- 简单问题：直接结论
- 复杂问题：完整信息
"""

import sys
import os
import datetime
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from encoding_utils import safe_print
from qweather import QWeatherClient
from location_handler import LocationHandler

def get_chinese_weekday(date_str):
    """获取中文星期几"""
    try:
        year, month, day = map(int, date_str.split('-'))
        date_obj = datetime.date(year, month, day)
        weekday_num = date_obj.weekday()  # 0=周一, 1=周二, ..., 6=周日
        weekdays = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
        return weekdays[weekday_num]
    except:
        return ""

class ProperGradingWeather:
    """正确分级响应的天气回答"""
    
    def __init__(self, user_city="beijing"):
        self.client = QWeatherClient()
        self.loc_handler = LocationHandler()
        self.user_city = user_city
        
        # 简单问题模式（直接结论）
        self.simple_questions = {
            'weather_brief': ['天气怎么样', '天气如何', '天气'],
            'umbrella_brief': ['要不要带伞', '带伞', '雨伞'],
            'cold_brief': ['冷不冷', '冷吗'],
            'hot_brief': ['热不热', '热吗'],
            'rain_brief': ['下雨吗', '下雨', '有雨吗'],
            'wind_brief': ['风大吗', '风大', '风力'],
            'humidity_brief': ['湿度怎么样', '湿度'],
            'temperature_brief': ['温度多少', '多少度', '温度'],
        }
        
        # 详细问题模式（完整信息）
        self.detailed_questions = ['详细说说', '详细天气', '完整天气', '全面报告', '天气预报']
    
    def ask(self, question):
        """回答天气问题（正确分级）"""
        try:
            question = question.strip().lower()
            
            # 1. 判断问题类型
            question_type = self._get_question_type(question)
            
            # 2. 获取地点
            city = self._get_city(question)
            city_name = self.loc_handler.get_location_for_display(city)
            
            # 3. 获取天气数据
            weather = self.client.get_weather_now(city.name)
            forecasts = self.client.get_weather_forecast(city.name, 1)
            today = forecasts[0] if forecasts else None
            
            # 4. 安全转换数据
            weather = self._fix_data(weather)
            if today:
                today = self._fix_forecast(today)
            
            # 5. 根据问题类型生成回答
            if question_type == 'simple':
                return self._simple_answer(question, city, city_name, weather, today)
            else:
                return self._detailed_answer(city, city_name, weather, today)
                
        except Exception as e:
            return f"查询失败：{str(e)[:80]}"
    
    def _get_question_type(self, question):
        """判断问题类型"""
        q = question.lower()
        
        # 检查是否是详细问题
        for pattern in self.detailed_questions:
            if pattern in q:
                return 'detailed'
        
        # 检查是否是简单问题
        for category, patterns in self.simple_questions.items():
            for pattern in patterns:
                if pattern in q:
                    return 'simple'
        
        # 默认：简单问题（如果问题很短）
        if len(question) <= 8:
            return 'simple'
        else:
            return 'detailed'
    
    def _get_city(self, question):
        """获取城市"""
        # 移除常见关键词
        text = question
        all_keywords = []
        for patterns in self.simple_questions.values():
            all_keywords.extend(patterns)
        all_keywords.extend(self.detailed_questions)
        all_keywords.extend(['现在', '今天', '明天', '外面', '吗', '？', '?'])
        
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
        
        def safe_int(v):
            try:
                return int(float(v)) if v else 0
            except:
                return 0
        
        forecast.temp_min = safe_float(forecast.temp_min)
        forecast.temp_max = safe_float(forecast.temp_max)
        forecast.precip = safe_float(forecast.precip)
        forecast.humidity = safe_int(forecast.humidity)
        return forecast
    
    def _simple_answer(self, question, location, city_name, weather, today):
        """简洁回答（直接结论）"""
        q = question.lower()
        
        # 地点说明
        if location.source == "memory":
            location_note = "您在北京"
        else:
            location_note = city_name
        
        # 根据问题类型生成简洁回答
        if '天气怎么样' in q or '天气如何' in q or '天气' == q.strip():
            return self._simple_weather(location_note, weather, today)
        
        elif '带伞' in q or '雨伞' in q:
            return self._simple_umbrella(location_note, weather, today)
        
        elif '冷不冷' in q or '冷吗' in q:
            return self._simple_cold(location_note, weather, today)
        
        elif '热不热' in q or '热吗' in q:
            return self._simple_hot(location_note, weather, today)
        
        elif '下雨' in q:
            return self._simple_rain(location_note, weather, today)
        
        elif '风大' in q or '风力' in q:
            return self._simple_wind(location_note, weather)
        
        elif '湿度' in q:
            return self._simple_humidity(location_note, weather)
        
        elif '温度' in q or '多少度' in q:
            return self._simple_temperature(location_note, weather, today)
        
        # 默认简洁回答
        return self._simple_weather(location_note, weather, today)
    
    def _simple_weather(self, location_note, weather, today):
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
    
    def _simple_umbrella(self, location_note, weather, today):
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
    
    def _simple_cold(self, location_note, weather, today):
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
    
    def _simple_hot(self, location_note, weather, today):
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
    
    def _simple_rain(self, location_note, weather, today):
        """简洁：下雨吗"""
        if '雨' in weather.text or weather.precip > 0:
            return f"{location_note}：正在下雨 🌧️ {weather.text}，降水{weather.precip}mm"
        else:
            return f"{location_note}：没有下雨 ☀️ {weather.text}，无降水"
    
    def _simple_wind(self, location_note, weather):
        """简洁：风大吗"""
        if weather.wind_scale >= 6:
            return f"{location_note}：风很大！💨 {weather.wind_scale}级"
        elif weather.wind_scale >= 4:
            return f"{location_note}：风有点大 🌬️ {weather.wind_scale}级"
        elif weather.wind_scale >= 2:
            return f"{location_note}：微风 🍃 {weather.wind_scale}级"
        else:
            return f"{location_note}：基本无风 🌫️ {weather.wind_scale}级"
    
    def _simple_humidity(self, location_note, weather):
        """简洁：湿度怎么样"""
        if weather.humidity >= 80:
            return f"{location_note}：非常潮湿 💦 {weather.humidity}%"
        elif weather.humidity >= 60:
            return f"{location_note}：湿度适中 💧 {weather.humidity}%"
        elif weather.humidity >= 40:
            return f"{location_note}：湿度适宜 😊 {weather.humidity}%"
        else:
            return f"{location_note}：比较干燥 🏜️ {weather.humidity}%"
    
    def _simple_temperature(self, location_note, weather, today):
        """简洁：温度多少"""
        reply = f"{location_note}：{weather.temp}°C"
        
        if weather.feels_like != weather.temp:
            reply += f"（体感{weather.feels_like}°C）"
        
        if today:
            reply += f"，今天{today.temp_min}°C~{today.temp_max}°C"
        
        return reply
    
    def _detailed_answer(self, location, city_name, weather, today):
        """详细回答（完整信息）"""
        # 使用现有的FinalWeather的详细回答逻辑
        if location.source == "memory":
            location_note = f"根据记忆您在北京"
        else:
            location_note = f"{city_name}"
        
        today_date = datetime.datetime.now().strftime("%Y-%m-%d")
        today_weekday = get_chinese_weekday(today_date)
        date_info = f"{today_date}（{today_weekday}）" if today_weekday else today_date
        
        reply = f"{location_note}，现在天气（{date_info}）：\n\n"
        
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
        reply += f"• 温度：{weather.temp}°C"
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
        
        reply += f"• 湿度：{weather.humidity}%\n"
        
        if weather.precip > 0:
            reply += f"• 降水：{weather.precip}mm\n"
        
        reply += "\n"
        
        # 建议
        reply += "💡 **建议**：\n"
        
        # 穿衣建议
        if weather.temp <= 5:
            reply += "• 穿衣：比较冷，建议穿厚外套\n"
        elif weather.temp <= 15:
            reply += "• 穿衣：温度适宜，建议穿外套\n"
        elif weather.temp <= 25:
            reply += "• 穿衣：比较温暖，建议穿长袖\n"
        else:
            reply += "• 穿衣：比较热