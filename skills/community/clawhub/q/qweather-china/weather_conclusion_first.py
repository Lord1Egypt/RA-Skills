#!/usr/bin/env python3
"""
结论先行版天气回答
优化回答结构：结论 → 关键数据 → 详细分析 → 建议
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
            parts = value.split('-')
            return int(parts[0]) if parts[0].isdigit() else default
        return int(float(value)) if value else default
    except:
        return default

class ConclusionFirstWeather:
    """结论先行版天气回答"""
    
    def __init__(self, user_city="beijing"):
        self.client = QWeatherClient()
        self.loc_handler = LocationHandler()
        self.user_city = user_city
    
    def ask(self, question):
        """回答天气问题（结论先行）"""
        try:
            question = question.strip().lower()
            
            # 获取地点
            city = self._get_city(question)
            city_name = self.loc_handler.get_location_for_display(city)
            
            # 获取天气数据
            weather = self.client.get_weather_now(city.name)
            forecasts = self.client.get_weather_forecast(city.name, 1)
            today = forecasts[0] if forecasts else None
            
            # 修复数据类型
            weather = self._fix_data(weather)
            if today:
                today = self._fix_forecast(today)
            
            # 生成结论先行的回答
            return self._conclusion_first_reply(city, city_name, weather, today, question)
                
        except Exception as e:
            return f"查询失败：{str(e)[:80]}"
    
    def _get_city(self, question):
        """获取城市"""
        # 移除天气关键词
        text = question
        keywords = ['天气', '怎么样', '如何', '现在', '今天', '带伞', '冷不冷', '热不热', 
                   '下雨', '风大', '湿度', '详细', '预报', '温度', '吗', '？', '?']
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
        """修复数据类型"""
        weather.temp = safe_float(weather.temp)
        weather.feels_like = safe_float(getattr(weather, 'feels_like', weather.temp))
        weather.wind_scale = safe_int(getattr(weather, 'wind_scale', 0))
        weather.humidity = safe_int(getattr(weather, 'humidity', 0))
        weather.precip = safe_float(getattr(weather, 'precip', 0))
        return weather
    
    def _fix_forecast(self, forecast):
        """修复预报数据"""
        forecast.temp_min = safe_float(forecast.temp_min)
        forecast.temp_max = safe_float(forecast.temp_max)
        forecast.precip = safe_float(forecast.precip)
        forecast.humidity = safe_int(forecast.humidity)
        return forecast
    
    def _conclusion_first_reply(self, location, city_name, weather, today, question):
        """结论先行的回答"""
        # 地点说明
        if location.source == "memory":
            location_note = f"（您在{city_name}）"
        else:
            location_note = f"（{city_name}）"
        
        # 1. 生成核心结论
        conclusion = self._generate_conclusion(weather, today)
        
        # 2. 生成关键数据摘要
        summary = self._generate_summary(weather, today)
        
        # 3. 根据问题类型提供针对性信息
        details = self._generate_details(question, weather, today)
        
        # 4. 生成建议
        advice = self._generate_advice(weather, today)
        
        # 组合回答（结论先行）
        reply = f"{city_name}现在天气{location_note}：\n\n"
        
        # 结论（最重要，放最前面）
        reply += "💬 **结论**："
        reply += conclusion + "\n\n"
        
        # 关键数据
        reply += "📊 **关键数据**：\n"
        reply += summary + "\n\n"
        
        # 针对性信息（如果有）
        if details:
            reply += "🔍 **详细分析**：\n"
            reply += details + "\n\n"
        
        # 建议
        reply += "💡 **建议**：\n"
        reply += advice
        
        return reply
    
    def _generate_conclusion(self, weather, today):
        """生成核心结论"""
        conclusions = []
        
        # 天气结论
        if '晴' in weather.text or '多云' in weather.text:
            conclusions.append("天气很好")
        elif '雨' in weather.text:
            conclusions.append("有降水")
        elif '阴' in weather.text:
            conclusions.append("阴天")
        
        # 温度结论
        if weather.temp <= 5:
            conclusions.append("比较冷")
        elif weather.temp <= 15:
            conclusions.append("温度适宜")
        elif weather.temp <= 25:
            conclusions.append("比较温暖")
        else:
            conclusions.append("比较热")
        
        # 风力结论
        if weather.wind_scale >= 6:
            conclusions.append("风很大")
        elif weather.wind_scale >= 4:
            conclusions.append("有风")
        
        # 降水结论
        if weather.precip > 0:
            conclusions.append("有降水")
        
        # 综合结论
        if not conclusions:
            return "天气条件一般。"
        
        # 生成最终结论
        if '天气很好' in conclusions and '温度适宜' in conclusions:
            if weather.wind_scale < 4 and weather.precip == 0:
                return "今天天气很好，适合外出！☀️"
            else:
                return "天气不错，但有些因素需要注意。"
        elif '有降水' in conclusions:
            return "今天有降水，建议做好防雨准备。"
        elif '比较冷' in conclusions:
            return "今天比较冷，注意保暖。"
        elif '比较热' in conclusions:
            return "今天比较热，注意防暑。"
        else:
            return f"今天{''.join(conclusions[:2])}。"
    
    def _generate_summary(self, weather, today):
        """生成关键数据摘要"""
        summary = []
        
        # 当前天气
        summary.append(f"• {weather.text}，{weather.temp}°C")
        if weather.feels_like != weather.temp:
            summary[-1] += f"（体感{weather.feels_like}°C）"
        
        # 今天温度范围
        if today:
            summary.append(f"• 今天温度：{today.temp_min}°C ~ {today.temp_max}°C")
        
        # 风力
        summary.append(f"• 风力：{weather.wind_scale}级")
        if hasattr(weather, 'wind_dir') and weather.wind_dir:
            summary[-1] += f" {weather.wind_dir}"
        
        # 湿度
        summary.append(f"• 湿度：{weather.humidity}%")
        
        # 降水
        if weather.precip > 0:
            summary.append(f"• 降水：{weather.precip}mm")
        
        return "\n".join(summary)
    
    def _generate_details(self, question, weather, today):
        """生成针对性详细信息"""
        details = []
        
        # 根据问题关键词提供详细信息
        if '带伞' in question:
            if weather.precip > 0 or '雨' in weather.text:
                details.append("• 当前有降水，建议带伞")
            elif today and (today.precip > 0 or '雨' in today.text_day or '雨' in today.text_night):
                details.append("• 今天预报有雨，建议带伞")
            else:
                details.append("• 无降水，不用带伞")
        
        elif '冷不冷' in question or '冷' in question:
            feels_like = weather.feels_like
            if feels_like <= 0:
                details.append("• 体感温度≤0°C，非常冷")
            elif feels_like <= 10:
                details.append("• 体感温度≤10°C，有点冷")
            else:
                details.append("• 体感温度>10°C，不冷")
        
        elif '热不热' in question or '热' in question:
            feels_like = weather.feels_like
            if feels_like >= 30:
                details.append("• 体感温度≥30°C，非常热")
            elif feels_like >= 25:
                details.append("• 体感温度≥25°C，有点热")
            else:
                details.append("• 体感温度<25°C，不热")
        
        elif '下雨' in question:
            if '雨' in weather.text or weather.precip > 0:
                details.append(f"• 当前：{weather.text}，降水{weather.precip}mm")
            else:
                details.append("• 当前无降水")
        
        elif '风大' in question:
            if weather.wind_scale >= 6:
                details.append("• 风力≥6级，风很大")
            elif weather.wind_scale >= 4:
                details.append("• 风力≥4级，风有点大")
            else:
                details.append("• 风力<4级，风不大")
        
        elif '湿度' in question:
            if weather.humidity >= 80:
                details.append("• 湿度≥80%，非常潮湿")
            elif weather.humidity >= 60:
                details.append("• 湿度≥60%，湿度适中")
            elif weather.humidity >= 40:
                details.append("• 湿度≥40%，湿度适宜")
            else:
                details.append("• 湿度<40%，比较干燥")
        
        return "\n".join(details) if details else ""
    
    def _generate_advice(self, weather, today):
        """生成建议"""
        advice = []
        
        # 穿衣建议
        if weather.temp <= 5:
            advice.append("• 穿衣：比较冷，建议穿厚外套、戴手套")
        elif weather.temp <= 15:
            advice.append("• 穿衣：温度适宜，建议穿外套")
        elif weather.temp <= 25:
            advice.append("• 穿衣：比较温暖，建议穿长袖")
        else:
            advice.append("• 穿衣：比较热，建议穿短袖、注意防晒")
        
        # 雨伞建议
        if weather.precip > 0 or '雨' in weather.text:
            advice.append("• 雨伞：正在下雨，建议带伞")
        elif today and (today.precip > 0 or '雨' in today.text_day or '雨' in today.text_night):
            advice.append("• 雨伞：今天可能下雨，建议带伞")
        else:
            advice.append("• 雨伞：无降水，不用带伞")
        
        # 户外活动建议
        if '晴' in weather.text and weather.wind_scale < 4:
            advice.append("• 活动：天气晴朗，风力小，适合户外活动")
        elif '雨' in weather.text or weather.precip > 0:
            advice.append("• 活动：有降水，建议室内活动")
        
        # 特殊建议
        if today and abs(today.temp_max - today.temp_min) >= 10:
            advice.append("• 温差：今天温差较大，注意适时增减衣物")
        
        if weather.humidity >= 80:
            advice.append("• 湿度：湿度很高，可能感觉闷热")
        elif weather.humidity <= 40:
            advice.append("• 湿度：湿度较低，注意补水保湿")
        
        return "\n".join(advice)


# 测试
def test_conclusion_first():
    """测试结论先行版"""
    weather = ConclusionFirstWeather(user_city="beijing")
    
    tests = [
        "现在天气如何？",
        "天气怎么样？",
        "要不要带伞？",
        "冷不冷？",
        "热不热？",
        "下雨吗？",
        "风大吗？",
    ]
    
    safe_print("=" * 50)
    safe_print("结论先行版天气回答测试")
    safe_print("=" * 50)
    
    for test in tests:
        safe_print(f"\n问题：{test}")
        safe_print("-" * 40)
        answer = weather.ask(test)
        safe_print(answer)
        safe_print("-" * 40)
    
    safe_print("\n✅ 优化完成：结论先行，体验更佳！")

if __name__ == "__main__":
    test_conclusion_first()