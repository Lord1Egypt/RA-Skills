#!/usr/bin/env python3
"""
智能天气处理器 - 简洁完整版
实现两个核心优化：
1. 智能地点记忆：优先记忆城市，兜底默认北京
2. 分级响应：简洁问题直接结论，复杂问题完整信息
"""

import sys
import os
import re
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from encoding_utils import safe_print
from qweather import QWeatherClient
from location_handler import LocationHandler

class SmartWeather:
    """智能天气处理器"""
    
    def __init__(self, memory_city="beijing"):
        """初始化，memory_city从记忆中读取的用户城市"""
        self.client = QWeatherClient()
        self.loc_handler = LocationHandler()
        self.memory_city = memory_city  # 从MEMORY.md读取的北京
    
    def answer(self, question):
        """回答天气问题"""
        question = question.strip()
        
        # 1. 确定地点
        location = self._get_location(question)
        city_display = self.loc_handler.get_location_for_display(location)
        
        # 2. 判断问题类型
        is_simple = self._is_simple_question(question)
        
        try:
            # 获取天气数据
            weather_now = self.client.get_weather_now(location.name)
            forecasts = self.client.get_weather_forecast(location.name, 1)
            today = forecasts[0] if forecasts else None
            
            # 生成回答
            if is_simple:
                return self._simple_answer(question, location, city_display, weather_now, today)
            else:
                return self._detailed_answer(location, city_display, weather_now, today)
                
        except Exception as e:
            return f"❌ 查询失败：{str(e)}"
    
    def _get_location(self, question):
        """智能获取地点"""
        # 尝试从问题中提取地点
        location_text = question
        # 移除天气相关词
        weather_words = ['天气', '怎么样', '要不要', '带伞', '冷不冷', '热不热', '下雨', '风大', '湿度', '详细', '预报']
        for word in weather_words:
            location_text = location_text.replace(word, '')
        
        location_text = location_text.strip()
        
        if location_text:
            # 问题中指定了地点
            return self.loc_handler.parse_input(location_text)
        else:
            # 没有指定地点，使用记忆中的城市
            location = self.loc_handler.parse_input(self.memory_city)
            location.source = "memory"  # 标记为来自记忆
            return location
    
    def _is_simple_question(self, question):
        """判断是否是简单问题"""
        simple_patterns = [
            r'^天气怎么样[？?]?$',
            r'^要不要带伞[？?]?$',
            r'^冷不冷[？?]?$',
            r'^热不热[？?]?$',
            r'^下雨吗[？?]?$',
            r'^风大吗[？?]?$',
            r'^湿度怎么样[？?]?$',
            r'^雨什么时候停[？?]?$',
        ]
        
        for pattern in simple_patterns:
            if re.match(pattern, question, re.IGNORECASE):
                return True
        
        # 检查是否以这些词开头
        simple_starts = ['天气怎么样', '要不要带伞', '冷不冷', '热不热', '下雨吗', '风大吗']
        for start in simple_starts:
            if question.startswith(start):
                return True
        
        return False
    
    def _simple_answer(self, question, location, city_display, weather_now, today):
        """生成简洁回答"""
        # 地点说明
        if location.source == "memory":
            location_note = f"（您在{city_display}）"
        else:
            location_note = f"（{city_display}）"
        
        # 根据问题类型回答
        if '天气怎么样' in question:
            response = f"{city_display}现在天气{location_note}：\n"
            response += f"• {weather_now.text}，{weather_now.temp}°C（体感{weather_now.feels_like}°C）\n"
            if today:
                response += f"• 今天温度：{today.temp_min}°C ~ {today.temp_max}°C\n"
            response += f"• 风力：{weather_now.wind_scale}级 {weather_now.wind_dir}\n"
            
            # 简单建议
            if weather_now.precip > 0 or '雨' in weather_now.text:
                response += "• 建议：可能会下雨，带伞\n"
            elif weather_now.temp <= 5:
                response += "• 建议：比较冷，注意保暖\n"
            elif weather_now.temp >= 25:
                response += "• 建议：比较热，注意防暑\n"
            
            return response
            
        elif '要不要带伞' in question:
            needs_umbrella = False
            if weather_now.precip > 0 or '雨' in weather_now.text:
                needs_umbrella = True
            if today and (today.precip > 0 or '雨' in today.text_day or '雨' in today.text_night):
                needs_umbrella = True
            
            response = f"{city_display}今天{location_note}：\n"
            if needs_umbrella:
                response += "✅ 建议带伞！\n"
                response += f"• 当前：{weather_now.text}，降水{weather_now.precip}mm\n"
            else:
                response += "❌ 不用带伞\n"
                response += f"• 当前：{weather_now.text}，无降水\n"
            
            return response
            
        elif '冷不冷' in question:
            feels_like = weather_now.feels_like
            
            response = f"{city_display}现在{location_note}：\n"
            response += f"• 温度：{weather_now.temp}°C（体感{feels_like}°C）\n"
            
            if feels_like <= 0:
                response += "❄️ 非常冷！注意防寒\n"
            elif feels_like <= 10:
                response += "🥶 有点冷，穿外套\n"
            elif feels_like <= 20:
                response += "😊 温度适宜\n"
            else:
                response += "😅 不冷，暖和\n"
            
            if today:
                response += f"• 今天：{today.temp_min}°C ~ {today.temp_max}°C\n"
            
            return response
            
        elif '热不热' in question:
            feels_like = weather_now.feels_like
            
            response = f"{city_display}现在{location_note}：\n"
            response += f"• 温度：{weather_now.temp}°C（体感{feels_like}°C）\n"
            
            if feels_like >= 30:
                response += "🔥 非常热！注意防暑\n"
            elif feels_like >= 25:
                response += "🥵 有点热，注意防晒\n"
            elif feels_like >= 20:
                response += "😊 温度适宜\n"
            else:
                response += "😌 不热，凉快\n"
            
            if today:
                response += f"• 今天：{today.temp_min}°C ~ {today.temp_max}°C\n"
            
            return response
            
        elif '下雨吗' in question or '雨什么时候停' in question:
            response = f"{city_display}现在{location_note}：\n"
            
            if '雨' in weather_now.text or weather_now.precip > 0:
                response += "🌧️ 正在下雨\n"
                response += f"• 天气：{weather_now.text}\n"
                response += f"• 降水：{weather_now.precip}mm\n"
                if '雨什么时候停' in question:
                    response += "• 雨停时间：请关注天气预报\n"
            else:
                response += "☀️ 没有下雨\n"
                response += f"• 天气：{weather_now.text}\n"
            
            return response
            
        elif '风大吗' in question:
            response = f"{city_display}现在{location_note}：\n"
            response += f"• 风力：{weather_now.wind_scale}级 {weather_now.wind_dir}\n"
            
            if weather_now.wind_scale >= 6:
                response += "💨 风很大！注意安全\n"
            elif weather_now.wind_scale >= 4:
                response += "🌬️ 风有点大\n"
            else:
                response += "🍃 微风或基本无风\n"
            
            return response
            
        elif '湿度怎么样' in question:
            response = f"{city_display}现在{location_note}：\n"
            response += f"• 湿度：{weather_now.humidity}%\n"
            
            if weather_now.humidity >= 80:
                response += "💦 非常潮湿\n"
            elif weather_now.humidity >= 60:
                response += "💧 湿度适中\n"
            elif weather_now.humidity >= 40:
                response += "😊 湿度适宜\n"
            else:
                response += "🏜️ 比较干燥\n"
            
            return response
        
        # 默认简洁回答
        return self._default_simple_answer(location, city_display, weather_now, today)
    
    def _detailed_answer(self, location, city_display, weather_now, today):
        """生成详细回答"""
        if location.source == "memory":
            location_note = f"（您在{city_display}）"
        else:
            location_note = f"（{city_display}）"
        
        response = f"{city_display}天气报告{location_note}\n"
        response += "=" * 50 + "\n\n"
        
        # 实时天气
        response += "📊 实时天气\n"
        response += "-" * 20 + "\n"
        response += f"• 时间：{weather_now.obs_time}\n"
        response += f"• 天气：{weather_now.text}\n"
        response += f"• 温度：{weather_now.temp}°C（体感{weather_now.feels_like}°C）\n"
        response += f"• 风力：{weather_now.wind_scale}级 {weather_now.wind_dir}\n"
        response += f"• 湿度：{weather_now.humidity}%\n"
        response += f"• 降水：{weather_now.precip}mm\n"
        response += f"• 气压：{weather_now.pressure}hPa\n"
        response += f"• 能见度：{weather_now.vis}公里\n\n"
        
        # 今天预报
        if today:
            response += "📅 今天预报\n"
            response += "-" * 20 + "\n"
            response += f"• 日期：{today.fx_date}\n"
            response += f"• 温度：{today.temp_min}°C ~ {today.temp_max}°C\n"
            response += f"• 白天：{today.text_day}\n"
            response += f"• 夜间：{today.text_night}\n"
            response += f"• 风力：{today.wind_scale_day}级 {today.wind_dir_day}\n"
            response += f"• 湿度：{today.humidity}%\n"
            response += f"• 降水：{today.precip}mm\n"
            response += f"• 紫外线：{today.uv_index}级\n\n"
        
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
            response += "• 保暖：温度较低，注意防寒\n"
        elif weather_now.temp >= 28:
            response += "• 防暑：温度较高，注意防晒\n"
        
        # 风力建议
        if weather_now.wind_scale >= 6:
            response += "• 防风：风较大，注意安全\n"
        
        # 湿度建议
        if weather_now.humidity >= 80:
            response += "• 除湿：湿度很高，可能闷热\n"
        elif weather_now.humidity <= 40:
            response += "• 补水：湿度较低，注意保湿\n"
        
        response += "\n" + "=" * 50 + "\n"
        
        # 总结
        summary = []
        if '雨' in weather_now.text or weather_now.precip > 0:
            summary.append("有降水")
        if weather_now.temp <= 10:
            summary.append("温度较低")
        elif weather_now.temp >= 25:
            summary.append("温度较高")
        
        if summary:
            response += f"💬 总结：今天{'、'.join(summary)}。"
        else:
            response += "💬 总结：今天天气条件良好。"
        
        return response
    
    def _default_simple_answer(self, location, city_display, weather_now, today):
        """默认简洁回答"""
        if location.source == "memory":
            location_note = f"（您在{city_display}）"
        else:
            location_note = f"（{city_display}）"
        
        response = f"{city_display}现在天气{location_note}：\n"
        response += f"• {weather_now.text}，{weather_now.temp}°C\n"
        response += f"• 风力：{weather_now.wind_scale}级\n"
        response += f"• 湿度：{weather_now.humidity}%\n"
        
        if today:
            response += f"• 今天温度：{today.temp_min}°C ~ {today.temp_max}°C\n"
        
        return response


# 测试函数
def test_smart_weather():
    """测试智能天气处理器"""
    # 从MEMORY.md知道用户在北京
    weather = SmartWeather(memory_city="beijing")
    
    test_cases = [
        "天气怎么样？",
        "要不要带伞？",
        "冷不冷？",
        "热不热？",
        "下雨吗？",
        "风大吗？",
        "湿度怎么样？",
        "北京天气怎么样？",
        "上海要不要带伞？",
        "详细说说天气",
        "今天天气怎么样？",
    ]
    
    safe_print("=" * 60)
    safe_print("智能天气处理器测试")
    safe_print("=" * 60)
    
    for question in test_cases:
        safe_print(f"\n问题：{question}")
        safe_print("-" * 40)
        answer = weather.answer(question)
        safe_print(answer)
        safe_print("-" * 40)
    
    safe_print("\n✅ 测试完成！")
    safe_print("优化功能：")
    safe_print("  1. ✅ 智能地点记忆：优先使用记忆中的北京")
    safe_print("  2. ✅ 分级响应：简洁问题直接结论，复杂问题完整信息")

if __name__ == "__main__":
    test_smart_weather()