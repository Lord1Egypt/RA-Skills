#!/usr/bin/env python3
"""
智能天气处理器 - 最终优化版
实现：
1. 智能地点记忆：优先使用记忆中的城市，兜底使用默认北京
2. 分级响应：简洁问题直接给结论，复杂问题提供完整信息
"""

import sys
import os
import re
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from encoding_utils import safe_print
from qweather import QWeatherClient
from location_handler import LocationHandler

class SmartWeatherHandler:
    """智能天气处理器"""
    
    def __init__(self, memory_city="beijing"):
        """
        初始化处理器
        memory_city: 从记忆中读取的用户所在城市，默认北京
        """
        self.client = QWeatherClient()
        self.location_handler = LocationHandler()
        
        # 设置默认城市（优先记忆，其次配置）
        self.memory_city = memory_city
        env_city = os.getenv("QWEATHER_DEFAULT_LOCATION", "beijing")
        self.default_city = memory_city if memory_city else env_city
        
        # 问题分类模式
        self.setup_patterns()
    
    def setup_patterns(self):
        """设置问题模式"""
        # 简洁回答模式（直接结论）
        self.brief_patterns = {
            # 不带地点
            r'^天气怎么样[？?]?$': ('weather_brief', True),
            r'^要不要带伞[？?]?$': ('umbrella_brief', True),
            r'^冷不冷[？?]?$': ('cold_brief', True),
            r'^热不热[？?]?$': ('hot_brief', True),
            r'^雨什么时候停[？?]?$': ('rain_stop_brief', True),
            r'^下雨吗[？?]?$': ('rain_brief', True),
            r'^风大吗[？?]?$': ('wind_brief', True),
            r'^湿度怎么样[？?]?$': ('humidity_brief', True),
            
            # 带地点
            r'^(.*?)天气怎么样[？?]?$': ('weather_brief', False),
            r'^(.*?)要不要带伞[？?]?$': ('umbrella_brief', False),
            r'^(.*?)冷不冷[？?]?$': ('cold_brief', False),
            r'^(.*?)热不热[？?]?$': ('hot_brief', False),
            r'^(.*?)下雨吗[？?]?$': ('rain_brief', False),
            r'^(.*?)风大吗[？?]?$': ('wind_brief', False),
        }
        
        # 详细回答模式
        self.detailed_patterns = {
            r'^详细说说(.*?)天气[？?]?$': 'weather_detailed',
            r'^(.*?)详细天气[？?]?$': 'weather_detailed',
            r'^全面报告(.*?)[？?]?$': 'full_report',
            r'^(.*?)完整天气[？?]?$': 'full_report',
            r'^(.*?)天气预报[？?]?$': 'weather_forecast',
        }
    
    def parse_query(self, query):
        """解析查询，返回(地点, 问题类型, 是否简洁)"""
        query = query.strip().lower()
        
        # 1. 检查简洁模式
        for pattern, (qtype, use_memory) in self.brief_patterns.items():
            match = re.match(pattern, query, re.IGNORECASE)
            if match:
                if use_memory:
                    # 使用记忆中的城市
                    location = self.location_handler.parse_input(self.memory_city)
                    location.source = "memory"
                else:
                    # 提取查询中的地点
                    location_text = match.group(1).strip()
                    if location_text:
                        location = self.location_handler.parse_input(location_text)
                    else:
                        location = self.location_handler.parse_input(self.memory_city)
                        location.source = "memory"
                return location, qtype, True
        
        # 2. 检查详细模式
        for pattern, qtype in self.detailed_patterns.items():
            match = re.match(pattern, query, re.IGNORECASE)
            if match:
                if match.lastindex and match.group(1):
                    location_text = match.group(1).strip()
                    location = self.location_handler.parse_input(location_text)
                else:
                    location = self.location_handler.parse_input(self.memory_city)
                    location.source = "memory"
                return location, qtype, False
        
        # 3. 默认：详细天气查询
        # 尝试提取地点
        location_text = query
        weather_keywords = ['天气', '预报', '温度', '气温', '下雨', '带伞', '冷不冷', '热不热', '风大', '湿度']
        for keyword in weather_keywords:
            location_text = location_text.replace(keyword, '')
        
        location_text = location_text.strip()
        
        if location_text:
            location = self.location_handler.parse_input(location_text)
        else:
            location = self.location_handler.parse_input(self.memory_city)
            location.source = "memory"
        
        return location, 'weather_full', False
    
    def handle(self, query):
        """处理天气查询"""
        try:
            # 解析查询
            location, qtype, is_brief = self.parse_query(query)
            display_name = self.location_handler.get_location_for_display(location)
            
            # 获取天气数据
            weather_now = self.client.get_weather_now(location.name)
            forecasts = self.client.get_weather_forecast(location.name, 1)
            today_forecast = forecasts[0] if forecasts else None
            
            # 生成响应
            if is_brief:
                return self.generate_brief_response(location, display_name, weather_now, today_forecast, qtype)
            else:
                return self.generate_detailed_response(location, display_name, weather_now, today_forecast, qtype)
                
        except Exception as e:
            return self.generate_error_response(e, location)
    
    def generate_brief_response(self, location, display_name, weather_now, today_forecast, qtype):
        """生成简洁响应"""
        # 地点说明
        location_note = self.get_location_note(location, display_name)
        
        # 根据问题类型生成回答
        if qtype == 'weather_brief':
            response = f"{display_name}现在天气{location_note}：\n"
            response += f"• {weather_now.text}，{weather_now.temp}°C（体感{weather_now.feels_like}°C）\n"
            if today_forecast:
                response += f"• 今天温度：{today_forecast.temp_min}°C ~ {today_forecast.temp_max}°C\n"
            response += f"• 风力：{weather_now.wind_scale}级 {weather_now.wind_dir}\n"
            
            # 简单建议
            advice = self.get_brief_advice(weather_now, today_forecast)
            if advice:
                response += f"• 建议：{advice}\n"
            
            return response
            
        elif qtype == 'umbrella_brief':
            needs_umbrella, reasons = self.check_umbrella_needed(weather_now, today_forecast)
            
            response = f"{display_name}今天{location_note}：\n"
            if needs_umbrella:
                response += "✅ 建议带伞！\n"
                for reason in reasons:
                    response += f"• {reason}\n"
            else:
                response += "❌ 不用带伞\n"
                response += f"• 当前：{weather_now.text}，降水{weather_now.precip}mm\n"
            
            return response
            
        elif qtype == 'cold_brief':
            feels_like = weather_now.feels_like
            
            response = f"{display_name}现在{location_note}：\n"
            response += f"• 温度：{weather_now.temp}°C（体感{feels_like}°C）\n"
            
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
            feels_like = weather_now.feels_like
            
            response = f"{display_name}现在{location_note}：\n"
            response += f"• 温度：{weather_now.temp}°C（体感{feels_like}°C）\n"
            
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
            response = f"{display_name}现在{location_note}：\n"
            response += f"• 风力：{weather_now.wind_scale}级（{weather_now.wind_speed}km/h）{weather_now.wind_dir}\n"
            
            if weather_now.wind_scale >= 6:
                response += "💨 风很大！注意安全\n"
            elif weather_now.wind_scale >= 4:
                response += "🌬️ 风有点大\n"
            elif weather_now.wind_scale >= 2:
                response += "🍃 微风，很舒适\n"
            else:
                response += "🌫️ 基本无风\n"
            
            return response
            
        elif qtype == 'humidity_brief':
            response = f"{display_name}现在{location_note}：\n"
            response += f"• 湿度：{weather_now.humidity}%\n"
            
            if weather_now.humidity >= 80:
                response += "💦 非常潮湿，可能感觉闷热\n"
            elif weather_now.humidity >= 60:
                response += "💧 湿度适中，比较舒适\n"
            elif weather_now.humidity >= 40:
                response += "😊 湿度适宜，很舒适\n"
            else:
                response += "🏜️ 比较干燥，注意补水\n"
            
            return response
        
        # 默认简洁回答
        return self.generate_default_brief(location, display_name, weather_now, today_forecast)
    
    def generate_detailed_response(self, location, display_name, weather_now, today_forecast, qtype):
        """生成详细响应"""
        location_note = self.get_location_note(location, display_name)
        
        response = f"{display_name}天气报告{location_note}\n"
        response += "=" * 50 + "\n\n"
        
        # 实时天气
        response += "📊 实时天气\n"
        response += "-" * 20 + "\n"
        response += f"• 观测时间：{weather_now.obs_time}\n"
        response += f"• 天气现象：{weather_now.text}\n"
        response += f"• 温度：{weather_now.temp}°C（体感{weather_now.feels_like}°C）\n"
        response += f"• 风力：{weather_now.wind_scale}级 {weather_now.wind_dir}\n"
        response += f"• 风速：{weather_now.wind_speed}km/h\n"
        response += f"• 湿度：{weather_now.humidity}%\n"
        response += f"• 降水量：{weather_now.precip}mm\n"
        response += f"• 气压：{weather_now.pressure}hPa\n"
        response += f"• 能见度：{weather_now.vis}公里\n"
        response += f"• 云量：{weather_now.cloud}%\n"
        response += f"• 露点温度：{weather_now.dew}°C\n\n"
        
        # 今天预报
        if today_forecast:
            response += "📅 今天预报\n"
            response += "-" * 20 + "\n"
            response += f"• 日期：{today_forecast.fx_date}\n"
            response += f"• 日出/日落：{today_forecast.sunrise} / {today_forecast.sunset}\n"
            response += f"• 温度范围：{today_forecast.temp_min}°C ~ {today_forecast.temp_max}°C\n"
            response += f"• 白天天气：{today_forecast.text_day}\n"
            response += f"• 夜间天气：{today_forecast.text_night}\n"
            response += f"• 白天风力：{today_forecast.wind_scale_day}级 {today_forecast.wind_dir_day}\n"
            response += f"• 夜间风力：{today_forecast.wind_scale_night}级 {today_forecast.wind_dir_night}\n"
            response += f"• 湿度：{today_forecast.humidity}%\n"
            response += f"• 降水量：{today_forecast.precip}mm\n"
            response += f"• 紫外线指数：{today_forecast.uv_index}级\n"
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
        
        # 温度相关建议
        if weather_now.temp <= 5:
            response += "• 保暖：温度较低，建议穿厚外套、戴手套\n"
        elif weather_now.temp >= 28:
            response += "• 防暑：温度较高，建议穿轻薄衣物、注意防晒\n"
        
        # 风力建议
        if weather_now.wind_scale >= 6:
            response += "• 防风：风较大，外出注意安全\n"
        elif weather_now.wind_scale >= 4:
            response += "• 防风：有风，建议固定好户外物品\n"
        
        # 湿度建议
        if weather_now.humidity >= 80:
            response += "• 除湿：湿度很高，可能感觉闷热不适\n"
        elif weather_now.humidity <= 40:
            response += "• 补水：湿度较低，注意皮肤保湿和补水\n"
        
        response += "\n" + "=" * 50 + "\n"
        
        # 总结
        summary = self.generate_summary(weather_now, today_forecast)
        response += f"💬 总结：{summary}\n"
        
        return response
    
    # 辅助方法
    def get_location_note(self, location, display_name):
        """获取地点说明"""
        if location.source == "memory":
            return f"（根据记忆，您在{display_name}）"
        elif location.source == "default" or location.source == "default_fallback":
            return f"（按默认地点{display_name}）"
        else:
            return f"（{display_name}）"
    
    def check_umbrella_needed(self, weather_now, today_forecast):
        """检查是否需要带伞"""
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
        
        if today_forecast and '雨' in today_forecast.text_day:
            needs_umbrella = True
            reasons.append(f"白天预报：{today_forecast.text_day}")
        
        if today_forecast and '雨' in today_forecast.text_night:
            needs_umbrella = True
            reasons.append(f"夜间预报：{today_forecast.text_night}")
        
        return needs