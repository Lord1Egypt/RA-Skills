"""
日历工具：处理传统节日和节气
"""

from datetime import datetime, date
from typing import Optional, List, Tuple
import calendar


class CalendarUtils:
    """日历事件工具类"""
    
    # 24 节气（简化版，实际需要精确计算）
    SOLAR_TERMS_ZH = [
        "立春", "雨水", "惊蛰", "春分", "清明", "谷雨",
        "立夏", "小满", "芒种", "夏至", "小暑", "大暑",
        "立秋", "处暑", "白露", "秋分", "寒露", "霜降",
        "立冬", "小雪", "大雪", "冬至", "小寒", "大寒"
    ]
    
    # 中国传统节日（简化版，使用农历日期）
    TRADITIONAL_FESTIVALS_ZH = {
        (1, 1): "春节",
        (1, 15): "元宵节",
        (5, 5): "端午节",
        (7, 7): "七夕节",
        (8, 15): "中秋节",
        (9, 9): "重阳节",
        (12, 30): "除夕"
    }
    
    # 通用节日（公历）
    COMMON_FESTIVALS = {
        (1, 1): "New Year's Day",
        (2, 14): "Valentine's Day",
        (3, 8): "International Women's Day",
        (4, 1): "April Fool's Day",
        (5, 1): "Labor Day",
        (6, 1): "Children's Day",
        (10, 31): "Halloween",
        (12, 25): "Christmas"
    }
    
    @staticmethod
    def get_today_festival(language: str = "zh") -> Optional[str]:
        """
        获取今天的节日
        返回节日名称，如果没有则返回 None
        """
        today = date.today()
        month_day = (today.month, today.day)
        
        if language == "zh":
            # Check traditional festivals (simplified here, actual implementation needs lunar conversion)
            # Temporarily only check Gregorian calendar festivals
            return CalendarUtils.COMMON_FESTIVALS.get(month_day)
        else:
            return CalendarUtils.COMMON_FESTIVALS.get(month_day)
    
    @staticmethod
    def get_today_solar_term() -> Optional[str]:
        """
        Get today's solar term (simplified version)
        Actual implementation requires precise solar term calculation algorithm
        """
        # Returns None here, actual implementation needs precise solar term calculation
        # Can use third-party libraries like zhdate for calculation
        return None
    
    @staticmethod
    def should_trigger_calendar_greeting(language: str = "zh") -> Optional[str]:
        """
        Check if calendar greeting should be triggered
        Returns greeting message, or None if not needed
        """
        festival = CalendarUtils.get_today_festival(language)
        if festival:
            if language == "zh":
                return f"今天是{festival}，祝你节日快乐！"
            else:
                return f"Today is {festival}, wish you a happy holiday!"
        
        # 检查节气（仅中文）
        if language == "zh":
            solar_term = CalendarUtils.get_today_solar_term()
            if solar_term:
                return f"今天是{solar_term}，注意天气变化哦～"
        
        return None
