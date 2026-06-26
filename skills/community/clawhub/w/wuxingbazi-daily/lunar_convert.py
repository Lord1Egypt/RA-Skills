#!/usr/bin/env python3
"""
农历公历转换工具
支持1900-2100年的农历公历转换
"""

from datetime import datetime, timedelta

# 农历数据（1900-2100）
# 每个元素为16进制，表示该年的农历信息
# 0-3位：闰月月份（0表示无闰月）
# 4-15位：每月天数（大月30天，小月29天）
LUNAR_DATA = [
    0x04bd8, 0x04ae0, 0x0a570, 0x054d5, 0x0d260, 0x0d950, 0x16554, 0x056a0, 0x09ad0, 0x055d2,
    0x04ae0, 0x0a5b6, 0x0a4d0, 0x0d250, 0x1d255, 0x0b540, 0x0d6a0, 0x0ada2, 0x095b0, 0x14977,
    0x04970, 0x0a4b0, 0x0b4b5, 0x06a50, 0x06d40, 0x1ab54, 0x02b60, 0x09570, 0x052f2, 0x04970,
    0x06566, 0x0d4a0, 0x0ea50, 0x06e95, 0x05ad0, 0x02b60, 0x186e3, 0x092e0, 0x1c8d7, 0x0c950,
    0x0d4a0, 0x1d8a6, 0x0b550, 0x056a0, 0x1a5b4, 0x025d0, 0x092d0, 0x0d2b2, 0x0a950, 0x0b557,
    0x06ca0, 0x0b550, 0x15355, 0x04da0, 0x0a5d0, 0x14573, 0x052d0, 0x0a9a8, 0x0e950, 0x06aa0,
    0x0aea6, 0x0ab50, 0x04b60, 0x0aae4, 0x0a570, 0x05260, 0x0f263, 0x0d950, 0x05b57, 0x056a0,
    0x096d0, 0x04dd5, 0x04ad0, 0x0a4d0, 0x0d4d4, 0x0d250, 0x0d558, 0x0b540, 0x0b5a0, 0x195a6,
    0x095b0, 0x049b0, 0x0a974, 0x0a4b0, 0x0b27a, 0x06a50, 0x06d40, 0x0af46, 0x0ab60, 0x09570,
    0x04af5, 0x04970, 0x064b0, 0x074a3, 0x0ea50, 0x06b58, 0x055c0, 0x0ab60, 0x096d5, 0x092e0,
    0x0c960, 0x0d954, 0x0d4a0, 0x0da50, 0x07552, 0x056a0, 0x0abb7, 0x025d0, 0x092d0, 0x0cab5,
    0x0a950, 0x0b4a0, 0x0baa4, 0x0ad50, 0x055d9, 0x04ba0, 0x0a5b0, 0x15176, 0x052b0, 0x0a930,
    0x07954, 0x06aa0, 0x0ad50, 0x05b52, 0x04b60, 0x0a6e6, 0x0a4e0, 0x0d260, 0x0ea65, 0x0d530,
    0x05aa0, 0x076a3, 0x096d0, 0x04bd7, 0x04ad0, 0x0a4d0, 0x1d0b6, 0x0d250, 0x0d520, 0x0dd45,
    0x0b5a0, 0x056d0, 0x055b2, 0x049b0, 0x0a577, 0x0a4b0, 0x0aa50, 0x1b255, 0x06d20, 0x0ada0
]

# 天干
TIANGAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]

# 地支
DIZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

# 农历月份名称
LUNAR_MONTH_NAMES = ["正", "二", "三", "四", "五", "六", "七", "八", "九", "十", "冬", "腊"]

# 农历日期名称
LUNAR_DAY_NAMES = [
    "初一", "初二", "初三", "初四", "初五", "初六", "初七", "初八", "初九", "初十",
    "十一", "十二", "十三", "十四", "十五", "十六", "十七", "十八", "十九", "二十",
    "廿一", "廿二", "廿三", "廿四", "廿五", "廿六", "廿七", "廿八", "廿九", "三十"
]


def is_leap_month(year_data: int, month: int) -> bool:
    """判断某月是否为闰月"""
    return (year_data >> (16 - month)) & 1


def get_lunar_month_days(year_data: int, month: int) -> int:
    """获取某农历月的天数"""
    return 30 if (year_data >> (15 - month)) & 1 else 29


def get_lunar_year_days(year: int) -> int:
    """获取某农历年的总天数"""
    year_data = LUNAR_DATA[year - 1900]
    days = 0
    for month in range(12):
        days += get_lunar_month_days(year_data, month)
    # 如果有闰月
    leap_month = year_data >> 16
    if leap_month > 0:
        days += get_lunar_month_days(year_data, 12)  # 闰月使用第13位
    return days


def solar_to_lunar(solar_date: datetime) -> dict:
    """
    公历转农历
    返回：{
        'year': 农历年,
        'month': 农历月（1-12）,
        'day': 农历日,
        'is_leap': 是否闰月,
        'ganzhi_year': 年干支,
        'animal': 生肖
    }
    """
    # 1900年春节是1月31日
    base_date = datetime(1900, 1, 31)
    
    if solar_date < base_date:
        raise ValueError("不支持1900年1月31日之前的日期")
    
    # 计算从1900年1月31日到目标日期的天数
    days_diff = (solar_date - base_date).days
    
    # 逐年累加，确定农历年
    lunar_year = 1900
    while days_diff >= get_lunar_year_days(lunar_year):
        days_diff -= get_lunar_year_days(lunar_year)
        lunar_year += 1
    
    # 确定农历月和日
    year_data = LUNAR_DATA[lunar_year - 1900]
    leap_month = year_data >> 16
    
    lunar_month = 1
    is_leap = False
    
    for month in range(1, 14):
        month_days = get_lunar_month_days(year_data, month - 1)
        if days_diff < month_days:
            lunar_month = month if month <= 12 else leap_month
            if month == 13 or (leap_month > 0 and month == leap_month + 1):
                is_leap = True
            break
        days_diff -= month_days
    
    lunar_day = int(days_diff) + 1
    
    # 计算年干支
    ganzhi_offset = (lunar_year - 1900) % 60
    gan = TIANGAN[ganzhi_offset % 10]
    zhi = DIZHI[ganzhi_offset % 12]
    ganzhi_year = gan + zhi
    
    # 生肖
    animals = ["鼠", "牛", "虎", "兔", "龙", "蛇", "马", "羊", "猴", "鸡", "狗", "猪"]
    animal = animals[(lunar_year - 1900) % 12]
    
    return {
        'year': lunar_year,
        'month': lunar_month,
        'day': lunar_day,
        'is_leap': is_leap,
        'ganzhi_year': ganzhi_year,
        'animal': animal,
        'month_name': LUNAR_MONTH_NAMES[lunar_month - 1],
        'day_name': LUNAR_DAY_NAMES[lunar_day - 1]
    }


def lunar_to_solar(lunar_year: int, lunar_month: int, lunar_day: int, is_leap: bool = False) -> datetime:
    """
    农历转公历
    """
    if lunar_year < 1900 or lunar_year > 2100:
        raise ValueError("只支持1900-2100年的农历")
    
    base_date = datetime(1900, 1, 31)
    
    # 计算从1900年到目标年的天数
    days = 0
    for year in range(1900, lunar_year):
        days += get_lunar_year_days(year)
    
    # 计算目标年内的天数
    year_data = LUNAR_DATA[lunar_year - 1900]
    leap_month = year_data >> 16
    
    for month in range(1, lunar_month):
        days += get_lunar_month_days(year_data, month - 1)
    
    # 处理闰月
    if is_leap and leap_month > 0 and lunar_month == leap_month:
        days += get_lunar_month_days(year_data, lunar_month - 1)
    elif leap_month > 0 and lunar_month > leap_month:
        days += get_lunar_month_days(year_data, 12)  # 闰月天数
    
    days += lunar_day - 1
    
    return base_date + timedelta(days=days)


def format_lunar_date(lunar_info: dict) -> str:
    """格式化农历日期输出"""
    leap_str = "闰" if lunar_info['is_leap'] else ""
    return f"{lunar_info['year']}年{leap_str}{lunar_info['month_name']}月{lunar_info['day_name']} {lunar_info['ganzhi_year']}年 [{lunar_info['animal']}]"


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) >= 4:
        # 公历转农历
        year = int(sys.argv[1])
        month = int(sys.argv[2])
        day = int(sys.argv[3])
        
        solar_date = datetime(year, month, day)
        lunar_info = solar_to_lunar(solar_date)
        print(format_lunar_date(lunar_info))
    else:
        # 显示今天的农历
        today = datetime.now()
        lunar_info = solar_to_lunar(today)
        print(f"今天是：{today.strftime('%Y年%m月%d日')}")
        print(f"农历：{format_lunar_date(lunar_info)}")
