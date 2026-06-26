#!/usr/bin/env python3
"""
温度专注版天气回答
专门优化温度相关问题的回答：冷不冷、热不热、温度多少等
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

class TemperatureFocusedWeather:
    """温度专注版天气回答"""
    
    def __init__(self, user_city="beijing"):
        self.client = QWeatherClient()
        self.loc_handler = LocationHandler()
        self.user_city = user_city
    
    def ask(self, question):
        """回答温度相关问题"""
        try:
            question = question.strip().lower()
            
            # 判断问题类型
            if '冷不冷' in question or '冷' in question:
                return self._answer_cold(question)
            elif '热不热' in question or '热' in question:
                return self._answer_hot(question)
            elif '温度' in question or '多少度' in question:
                return self._answer_temperature(question)
            else:
                return self._answer_general(question)
                
        except Exception as e:
            return f"查询失败：{str(e)[:80]}"
    
    def _answer_cold(self, question):
        """回答'冷不冷'"""
        # 获取地点
        city = self._get_city(question)
        city_name = self.loc_handler.get_location_for_display(city)
        
        # 获取天气数据
        weather = self.client.get_weather_now(city.name)
        
        # 安全转换温度
        def safe_float(v):
            try:
                return float(v) if v else 0
            except:
                return 0
        
        current_temp = safe_float(weather.temp)
        feels_like = safe_float(getattr(weather, 'feels_like', current_temp))
        
        # 获取今天预报
        forecasts = self.client.get_weather_forecast(city.name, 1)
        today = forecasts[0] if forecasts else None
        if today:
            today_min = safe_float(today.temp_min)
            today_max = safe_float(today.temp_max)
        
        # 生成回答
        reply = ""
        
        # 地点和时间
        if city.source == "memory":
            location_note = f"根据记忆您在北京"
        else:
            location_note = f"{city_name}"
        
        today_date = datetime.datetime.now().strftime("%Y-%m-%d")
        today_weekday = get_chinese_weekday(today_date)
        date_info = f"{today_date}（{today_weekday}）" if today_weekday else today_date
        
        reply += f"{location_note}，现在温度情况（{date_info}）：\n\n"
        
        # 核心结论（针对冷不冷）
        if feels_like <= 0:
            reply += "💬 **结论**：非常冷！❄️ 体感温度≤0°C，注意防寒保暖\n\n"
        elif feels_like <= 5:
            reply += "💬 **结论**：比较冷 🥶 体感温度≤5°C，建议穿厚外套\n\n"
        elif feels_like <= 10:
            reply += "💬 **结论**：有点冷 🧥 体感温度≤10°C，建议穿外套\n\n"
        elif feels_like <= 15:
            reply += "💬 **结论**：微凉 😌 体感温度≤15°C，穿薄外套即可\n\n"
        elif feels_like <= 20:
            reply += "💬 **结论**：温度适宜 😊 体感温度≤20°C，不冷不热\n\n"
        else:
            reply += "💬 **结论**：不冷 😅 体感温度>20°C，挺暖和的\n\n"
        
        # 详细温度数据
        reply += "📊 **温度数据**：\n"
        reply += f"• 当前温度：{current_temp}°C\n"
        reply += f"• 体感温度：{feels_like}°C\n"
        
        if today:
            reply += f"• 今天温度范围：{today_min}°C ~ {today_max}°C\n"
            temp_diff = today_max - today_min
            if temp_diff >= 10:
                reply += f"• 昼夜温差：{temp_diff}°C（温差较大）\n"
        
        reply += f"• 当前天气：{weather.text}\n"
        
        # 针对性建议
        reply += "\n💡 **针对性建议**：\n"
        
        if feels_like <= 0:
            reply += "• 防寒：穿羽绒服、戴手套围巾\n"
            reply += "• 室内：注意取暖，防止感冒\n"
            reply += "• 外出：尽量减少户外停留时间\n"
        elif feels_like <= 5:
            reply += "• 穿衣：厚外套、毛衣、保暖内衣\n"
            reply += "• 头部：建议戴帽子\n"
            reply += "• 手脚：注意手脚保暖\n"
        elif feels_like <= 10:
            reply += "• 穿衣：外套、长袖、长裤\n"
            reply += "• 层次：建议洋葱式穿搭\n"
            reply += "• 活动：户外活动注意保暖\n"
        elif feels_like <= 15:
            reply += "• 穿衣：薄外套或长袖即可\n"
            reply += "• 舒适：这个温度比较舒适\n"
            reply += "• 活动：适合各种户外活动\n"
        else:
            reply += "• 穿衣：短袖或薄长袖即可\n"
            reply += "• 舒适：温度很舒适\n"
            reply += "• 活动：非常适合户外活动\n"
        
        # 特殊提醒
        if today and today_min <= 5:
            reply += "• 提醒：今晚最低温度较低，注意夜间保暖\n"
        
        return reply
    
    def _answer_hot(self, question):
        """回答'热不热'"""
        # 获取地点
        city = self._get_city(question)
        city_name = self.loc_handler.get_location_for_display(city)
        
        # 获取天气数据
        weather = self.client.get_weather_now(city.name)
        
        # 安全转换温度
        def safe_float(v):
            try:
                return float(v) if v else 0
            except:
                return 0
        
        current_temp = safe_float(weather.temp)
        feels_like = safe_float(getattr(weather, 'feels_like', current_temp))
        
        # 获取今天预报
        forecasts = self.client.get_weather_forecast(city.name, 1)
        today = forecasts[0] if forecasts else None
        if today:
            today_max = safe_float(today.temp_max)
        
        # 生成回答
        reply = ""
        
        # 地点和时间
        if city.source == "memory":
            location_note = f"根据记忆您在北京"
        else:
            location_note = f"{city_name}"
        
        today_date = datetime.datetime.now().strftime("%Y-%m-%d")
        today_weekday = get_chinese_weekday(today_date)
        date_info = f"{today_date}（{today_weekday}）" if today_weekday else today_date
        
        reply += f"{location_note}，现在温度情况（{date_info}）：\n\n"
        
        # 核心结论（针对热不热）
        if feels_like >= 35:
            reply += "💬 **结论**：非常热！🔥 体感温度≥35°C，注意防暑降温\n\n"
        elif feels_like >= 30:
            reply += "💬 **结论**：很热 🥵 体感温度≥30°C，注意防晒避暑\n\n"
        elif feels_like >= 28:
            reply += "💬 **结论**：有点热 😓 体感温度≥28°C，注意防暑\n\n"
        elif feels_like >= 25:
            reply += "💬 **结论**：温暖 😌 体感温度≥25°C，比较舒适\n\n"
        elif feels_like >= 20:
            reply += "💬 **结论**：温度适宜 😊 体感温度≥20°C，不冷不热\n\n"
        else:
            reply += "💬 **结论**：不热 🍃 体感温度<20°C，挺凉快的\n\n"
        
        # 详细温度数据
        reply += "📊 **温度数据**：\n"
        reply += f"• 当前温度：{current_temp}°C\n"
        reply += f"• 体感温度：{feels_like}°C\n"
        
        if today:
            reply += f"• 今天最高温度：{today_max}°C\n"
        
        reply += f"• 当前天气：{weather.text}\n"
        reply += f"• 当前湿度：{getattr(weather, 'humidity', '未知')}%\n"
        
        # 针对性建议
        reply += "\n💡 **针对性建议**：\n"
        
        if feels_like >= 35:
            reply += "• 防暑：避免在高温时段外出\n"
            reply += "• 补水：及时补充水分，防止中暑\n"
            reply += "• 防晒：使用防晒霜，戴遮阳帽\n"
        elif feels_like >= 30:
            reply += "• 防晒：使用防晒霜，避免暴晒\n"
            reply += "• 补水：多喝水，保持水分\n"
            reply += "• 衣着：穿轻薄、透气的衣物\n"
        elif feels_like >= 28:
            reply += "• 防晒：注意防晒，避免长时间暴晒\n"
            reply += "• 补水：适当增加饮水量\n"
            reply += "• 衣着：建议穿短袖或薄长袖\n"
        elif feels_like >= 25:
            reply += "• 舒适：这个温度比较舒适\n"
            reply += "• 衣着：短袖或薄长袖即可\n"
            reply += "• 活动：适合各种户外活动\n"
        else:
            reply += "• 舒适：温度很舒适，不热\n"
            reply += "• 衣着：长袖或薄外套即可\n"
            reply += "• 活动：非常适合户外活动\n"
        
        # 湿度相关建议
        humidity = getattr(weather, 'humidity', 0)
        try:
            humidity = int(humidity) if humidity else 0
            if humidity >= 80 and feels_like >= 25:
                reply += "• 湿度：湿度很高，可能感觉闷热\n"
            elif humidity <= 40 and feels_like >= 28:
                reply += "• 湿度：湿度较低，注意补水保湿\n"
        except:
            pass
        
        return reply
    
    def _answer_temperature(self, question):
        """回答温度相关问题"""
        return self._answer_cold(question)  # 暂时复用冷热回答
    
    def _answer_general(self, question):
        """回答一般天气问题"""
        from weather_final_fixed import FinalWeather
        weather = FinalWeather(user_city=self.user_city)
        return weather.ask(question)
    
    def _get_city(self, question):
        """获取城市"""
        # 移除关键词
        text = question
        keywords = ['现在', '外面', '冷不冷', '热不热', '温度', '多少度', '吗', '？', '?']
        for word in keywords:
            text = text.replace(word, '')
        
        text = text.strip()
        
        if text:
            return self.loc_handler.parse_input(text)
        else:
            location = self.loc_handler.parse_input(self.user_city)
            location.source = "memory"
            return location


# 测试
def test_temperature():
    """测试温度专注版"""
    weather = TemperatureFocusedWeather(user_city="beijing")
    
    tests = [
        "现在外面冷不冷？",
        "热不热？",
        "温度多少？",
        "北京冷不冷？",
        "上海热不热？",
    ]
    
    safe_print("=" * 50)
    safe_print("温度专注版天气回答测试")
    safe_print("专门优化：冷不冷、热不热、温度多少等问题")
    safe_print("=" * 50)
    
    for test in tests:
        safe_print(f"\n问题：{test}")
        safe_print("-" * 40)
        answer = weather.ask(test)
        safe_print(answer)
        safe_print("-" * 40)
    
    safe_print("\n✅ 温度问题优化完成！")

if __name__ == "__main__":
    test_temperature()