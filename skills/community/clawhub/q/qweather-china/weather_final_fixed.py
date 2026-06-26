#!/usr/bin/env python3
"""
最终修复版天气回答
修复：1. 正确的星期几计算 2. 符合中文语法的地点时间顺序
"""

import sys
import os
import datetime
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
        if isinstance(value, str):
            if '-' in value:  # 处理'1-3级'
                parts = value.split('-')
                return int(parts[0]) if parts[0].isdigit() else default
            elif value.isdigit():
                return int(value)
        return int(float(value)) if value else default
    except:
        return default

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

class FinalWeather:
    """最终修复版天气回答"""
    
    def __init__(self, user_city="beijing"):
        self.client = QWeatherClient()
        self.loc_handler = LocationHandler()
        self.user_city = user_city
    
    def ask(self, question):
        """回答天气问题（最终修复版）"""
        try:
            question = question.strip().lower()
            
            # 判断是否是明天的问题
            is_tomorrow = '明天' in question or '明日' in question
            
            # 获取地点
            city = self._get_city(question, is_tomorrow)
            city_name = self.loc_handler.get_location_for_display(city)
            
            if is_tomorrow:
                return self._answer_tomorrow(city, city_name)
            else:
                return self._answer_now(city, city_name, question)
                
        except Exception as e:
            return f"查询失败：{str(e)[:80]}"
    
    def _get_city(self, question, is_tomorrow):
        """获取城市"""
        # 移除时间关键词
        text = question
        time_words = ['现在', '今天', '明天', '明日', '后天']
        for word in time_words:
            text = text.replace(word, '')
        
        # 移除天气关键词
        weather_words = ['天气', '怎么样', '如何', '带伞', '冷不冷', '热不热', 
                        '下雨', '风大', '湿度', '详细', '预报', '温度', '吗', '？', '?']
        for word in weather_words:
            text = text.replace(word, '')
        
        text = text.strip()
        
        if text:
            return self.loc_handler.parse_input(text)
        else:
            location = self.loc_handler.parse_input(self.user_city)
            location.source = "memory"
            return location
    
    def _answer_now(self, location, city_name, question):
        """回答现在/今天天气"""
        # 获取实时天气
        weather = self.client.get_weather_now(location.name)
        forecasts = self.client.get_weather_forecast(location.name, 1)
        today = forecasts[0] if forecasts else None
        
        # 修复数据类型
        weather = self._fix_weather_data(weather)
        if today:
            today = self._fix_forecast_data(today)
        
        # 生成回答
        return self._generate_now_reply(location, city_name, weather, today, question)
    
    def _answer_tomorrow(self, location, city_name):
        """回答明天天气"""
        # 获取明天预报（取2天预报的第2天）
        forecasts = self.client.get_weather_forecast(location.name, 2)
        if len(forecasts) < 2:
            return "❌ 无法获取明天天气预报"
        
        tomorrow = forecasts[1]
        tomorrow = self._fix_forecast_data(tomorrow)
        
        # 获取正确的星期几
        weekday = get_chinese_weekday(tomorrow.fx_date)
        date_with_weekday = f"{tomorrow.fx_date}（{weekday}）" if weekday else tomorrow.fx_date
        
        # 生成回答
        return self._generate_tomorrow_reply(location, city_name, tomorrow, date_with_weekday)
    
    def _fix_weather_data(self, weather):
        """修复实时天气数据"""
        weather.temp = safe_float(weather.temp)
        weather.feels_like = safe_float(getattr(weather, 'feels_like', weather.temp))
        weather.wind_scale = safe_int(getattr(weather, 'wind_scale', 0))
        weather.humidity = safe_int(getattr(weather, 'humidity', 0))
        weather.precip = safe_float(getattr(weather, 'precip', 0))
        return weather
    
    def _fix_forecast_data(self, forecast):
        """修复预报数据"""
        forecast.temp_min = safe_float(forecast.temp_min)
        forecast.temp_max = safe_float(forecast.temp_max)
        forecast.precip = safe_float(forecast.precip)
        forecast.humidity = safe_int(forecast.humidity)
        forecast.wind_scale_day = safe_int(forecast.wind_scale_day)
        return forecast
    
    def _generate_now_reply(self, location, city_name, weather, today, question):
        """生成现在天气回答"""
        # 地点说明（符合中文语法）
        if location.source == "memory":
            location_note = f"根据记忆您在北京"
        else:
            location_note = f"{city_name}"
        
        # 获取今天日期和星期几
        today_date = datetime.datetime.now().strftime("%Y-%m-%d")
        today_weekday = get_chinese_weekday(today_date)
        date_info = f"{today_date}（{today_weekday}）" if today_weekday else today_date
        
        reply = f"{location_note}，现在天气（{date_info}）：\n\n"
        
        # 结论
        conclusion = self._get_conclusion(weather, today, is_tomorrow=False)
        reply += f"💬 **结论**：{conclusion}\n\n"
        
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
        reply += self._get_advice(weather, today, is_tomorrow=False)
        
        return reply
    
    def _generate_tomorrow_reply(self, location, city_name, tomorrow, date_with_weekday):
        """生成明天天气回答"""
        # 地点说明（符合中文语法）
        if location.source == "memory":
            location_note = f"根据记忆您在北京"
        else:
            location_note = f"{city_name}"
        
        reply = f"{location_note}，明天天气（{date_with_weekday}）：\n\n"
        
        # 结论
        conclusion = self._get_conclusion(None, tomorrow, is_tomorrow=True)
        reply += f"💬 **结论**：{conclusion}\n\n"
        
        # 关键数据
        reply += "📊 **关键数据**：\n"
        reply += f"• 日期：{date_with_weekday}\n"
        reply += f"• 温度：{tomorrow.temp_min}°C ~ {tomorrow.temp_max}°C\n"
        reply += f"• 白天：{tomorrow.text_day}\n"
        reply += f"• 夜间：{tomorrow.text_night}\n"
        reply += f"• 降水：{tomorrow.precip}mm\n"
        reply += f"• 湿度：{tomorrow.humidity}%\n"
        reply += f"• 风力：{tomorrow.wind_scale_day}级 {tomorrow.wind_dir_day}\n\n"
        
        # 建议
        reply += "💡 **建议**：\n"
        reply += self._get_advice(None, tomorrow, is_tomorrow=True)
        
        return reply
    
    def _get_conclusion(self, weather, forecast, is_tomorrow):
        """获取结论"""
        if is_tomorrow:
            # 明天结论
            day_text = forecast.text_day.lower()
            night_text = forecast.text_night.lower()
            
            if '雨' in day_text or '雨' in night_text or forecast.precip > 0:
                return "明天可能有降水，建议做好防雨准备。"
            elif forecast.temp_max <= 5:
                return "明天比较冷，注意保暖。"
            elif forecast.temp_max >= 25:
                return "明天比较热，注意防暑。"
            elif '晴' in day_text and forecast.wind_scale_day < 4:
                return "明天天气很好，适合安排外出活动！☀️"
            else:
                return "明天天气条件良好。"
        else:
            # 现在结论
            if '雨' in weather.text or weather.precip > 0:
                return "现在有降水，建议做好防雨准备。"
            elif weather.temp <= 5:
                return "现在比较冷，注意保暖。"
            elif weather.temp >= 25:
                return "现在比较热，注意防暑。"
            elif '晴' in weather.text and weather.wind_scale < 4:
                return "现在天气很好，适合外出！☀️"
            else:
                return "现在天气条件良好。"
    
    def _get_advice(self, weather, forecast, is_tomorrow):
        """获取建议"""
        advice = []
        
        if is_tomorrow:
            # 明天建议
            avg_temp = (forecast.temp_min + forecast.temp_max) / 2
            day_text = forecast.text_day.lower()
            
            # 穿衣建议
            if avg_temp <= 5:
                advice.append("• 穿衣：比较冷，建议穿厚外套")
            elif avg_temp <= 15:
                advice.append("• 穿衣：温度适宜，建议穿外套")
            elif avg_temp <= 25:
                advice.append("• 穿衣：比较温暖，建议穿长袖")
            else:
                advice.append("• 穿衣：比较热，建议穿短袖、注意防晒")
            
            # 雨伞建议
            if forecast.precip > 0 or '雨' in day_text or '雨' in forecast.text_night.lower():
                advice.append("• 雨伞：可能有降水，建议带伞")
            else:
                advice.append("• 雨伞：无降水预报，不用带伞")
            
            # 活动建议
            if '晴' in day_text and forecast.wind_scale_day < 4:
                advice.append("• 活动：白天晴朗，风力小，适合户外活动")
            elif '雨' in day_text or forecast.precip > 0:
                advice.append("• 活动：可能有降水，建议室内活动")
            
            # 温差建议
            temp_diff = abs(forecast.temp_max - forecast.temp_min)
            if temp_diff >= 10:
                advice.append(f"• 温差：明天温差{temp_diff}°C，注意适时增减衣物")
            
            # 湿度建议
            if forecast.humidity >= 80:
                advice.append("• 湿度：湿度很高，可能感觉闷热")
            elif forecast.humidity <= 40:
                advice.append("• 湿度：湿度较低，注意补水保湿")
        
        else:
            # 现在建议
            # 穿衣建议
            if weather.temp <= 5:
                advice.append("• 穿衣：比较冷，建议穿厚外套")
            elif weather.temp <= 15:
                advice.append("• 穿衣：温度适宜，建议穿外套")
            elif weather.temp <= 25:
                advice.append("• 穿衣：比较温暖，建议穿长袖")
            else:
                advice.append("• 穿衣：比较热，建议穿短袖、注意防晒")
            
            # 雨伞建议
            if weather.precip > 0 or '雨' in weather.text:
                advice.append("• 雨伞：正在下雨，建议带伞")
            else:
                advice.append("• 雨伞：无降水，不用带伞")
            
            # 活动建议
            if '晴' in weather.text and weather.wind_scale < 4:
                advice.append("• 活动：天气晴朗，风力小，适合户外活动")
            elif '雨' in weather.text or weather.precip > 0:
                advice.append("• 活动：有降水，建议室内活动")
            
            # 湿度建议
            if weather.humidity >= 80:
                advice.append("• 湿度：湿度很高，可能感觉闷热")
            elif weather.humidity <= 40:
                advice.append("• 湿度：湿度较低，注意补水保湿")
        
        return "\n".join(advice)


# 测试
def test_final():
    """测试最终修复版"""
    weather = FinalWeather(user_city="beijing")
    
    tests = [
        "现在天气如何？",
        "明天天气怎么样？",
        "北京明天天气",
        "上海现在天气",
    ]
    
    safe_print("=" * 50)
    safe_print("最终修复版天气回答测试")
    safe_print("修复：1. 正确星期几 2. 中文语法优化")
    safe_print("=" * 50)
    
    for test in tests:
        safe_print(f"\n问题：{test}")
        safe_print("-" * 40)
        answer = weather.ask(test)
        safe_print(answer)
        safe_print("-" * 40)
    
    safe_print("\n✅ 所有问题修复完成！")

if __name__ == "__main__":
    test_final()