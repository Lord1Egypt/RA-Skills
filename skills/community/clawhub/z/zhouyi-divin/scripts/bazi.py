#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
八字排盘模块 - 基于农历计算四柱八字
参考：《三命通会》《渊海子平》
"""

import math
from datetime import datetime, timedelta

# 天干地支
TIAN_GAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
DI_ZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

# 天干五行属性
GAN_WUXING = {
    "甲": "木阳", "乙": "木阴",
    "丙": "火阳", "丁": "火阴",
    "戊": "土阳", "己": "土阴",
    "庚": "金阳", "辛": "金阴",
    "壬": "水阳", "癸": "水阴"
}

# 地支五行属性
ZH_IWUXING = {
    "子": "水阳", "丑": "土阴", "寅": "木阳", "卯": "木阴",
    "辰": "土阳", "巳": "火阴", "午": "火阳", "未": "土阴",
    "申": "金阳", "酉": "金阴", "戌": "土阳", "亥": "水阴"
}

# 地支藏干
DIZHICHANGAN = {
    "子": ["癸"],
    "丑": ["己", "癸", "辛"],
    "寅": ["甲", "丙", "戊"],
    "卯": ["乙"],
    "辰": ["戊", "乙", "癸"],
    "巳": ["丙", "庚", "戊"],
    "午": ["丁", "己"],
    "未": ["己", "丁", "乙"],
    "申": ["庚", "壬", "戊"],
    "酉": ["辛"],
    "戌": ["戊", "辛", "丁"],
    "亥": ["壬", "甲"]
}

def is_leap_year(year):
    """判断闰年"""
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

def get_days_in_month(year, month):
    """获取月份天数"""
    days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if is_leap_year(year):
        days[1] = 29
    return days[month - 1]

def get_ganzhi_year(year):
    """计算年的干支"""
    year_offset = year - 4
    gan_idx = year_offset % 10
    zhi_idx = year_offset % 12
    return TIAN_GAN[gan_idx], DI_ZHI[zhi_idx]

def get_ganzhi_month(year, month, day):
    """
    计算月的干支（节气算法简化版）
    正月建寅，以立春为界
    """
    # 年的天干决定月干起始
    year_gan = TIAN_GAN[(year - 4) % 10]
    
    # 月干起始索引（根据年干推算）
    gan_start_map = {"甲": 2, "乙": 2, "丙": 4, "丁": 4, 
                     "戊": 6, "己": 6, "庚": 8, "辛": 8,
                     "壬": 0, "癸": 0}
    
    base_gan_idx = gan_start_map.get(year_gan, 2)
    
    # 月份转换（寅月开始，所以实际月份要减 2）
    month_zhi_idx = (month + 1) % 12  # 寅月是第 2 个月
    
    # 月干需要根据年份推算（五虎遁年上起月法）
    gan_idx = (base_gan_idx + month - 1) % 10
    
    return TIAN_GAN[gan_idx], DI_ZHI[month_zhi_idx]

def get_ganzhi_day(year, month, day):
    """
    计算日的干支
    使用一个已知基准日（2000 年 1 月 1 日是甲戌日）
    """
    base_date = datetime(2000, 1, 1)
    target_date = datetime(year, month, day)
    
    days_diff = (target_date - base_date).days
    
    # 处理负数情况
    if days_diff < 0:
        days_diff = days_diff % 60
    
    # 甲戌日是第 11 个干支组合（从甲子=0 算）
    base_idx = 11
    
    total_idx = (base_idx + days_diff) % 60
    
    gan_idx = total_idx % 10
    zhi_idx = total_idx % 12
    
    return TIAN_GAN[gan_idx], DI_ZHI[zhi_idx]

def get_ganzhi_hour(hour, day_gan):
    """
    计算时的干支
    根据日干推时干（五鼠遁日上起时法）
    """
    # 子时固定为 23:00-1:00，对应地支序号 0
    zhi_idx = (hour + 1) // 2 % 12
    
    # 根据日干确定时干起点
    start_map = {"甲": 0, "乙": 2, "丙": 4, "丁": 6, 
                 "戊": 8, "己": 10, "庚": 0, "辛": 2,
                 "壬": 4, "癸": 6}
    
    base_gan = start_map.get(day_gan, 0)
    gan_idx = (base_gan + zhi_idx) % 10
    
    return TIAN_GAN[gan_idx], DI_ZHI[zhi_idx]

def bazi_pandan(year, month, day, hour):
    """
    八字排盘主函数
    返回完整的四柱信息
    """
    year_gan, year_zhi = get_ganzhi_year(year)
    month_gan, month_zhi = get_ganzhi_month(year, month, day)
    day_gan, day_zhi = get_ganzhi_day(year, month, day)
    hour_gan, hour_zhi = get_ganzhi_hour(hour, day_gan)
    
    bazi = {
        "year": {"gan": year_gan, "zhi": year_zhi},
        "month": {"gan": month_gan, "zhi": month_zhi},
        "day": {"gan": day_gan, "zhi": day_zhi},
        "hour": {"gan": hour_gan, "zhi": hour_zhi},
        "raw": f"{year_gan}{year_zhi} {month_gan}{month_zhi} {day_gan}{day_zhi} {hour_gan}{hour_zhi}"
    }
    
    return bazi

def analyze_wuxing(bazi):
    """分析五行力量"""
    wuxing_count = {"金": 0, "木": 0, "水": 0, "火": 0, "土": 0}
    
    wuxing_map = {
        "金": ["庚", "辛", "申", "酉"],
        "木": ["甲", "乙", "寅", "卯"],
        "水": ["壬", "癸", "子", "亥"],
        "火": ["丙", "丁", "巳", "午"],
        "土": ["戊", "己", "辰", "戌", "丑", "未"]
    }
    
    all_gan_zhi = []
    for pillar in ["year", "month", "day", "hour"]:
        all_gan_zhi.append(bazi[pillar]["gan"])
        all_gan_zhi.append(bazi[pillar]["zhi"])
    
    for gz in all_gan_zhi:
        for wx, items in wuxing_map.items():
            if gz in items:
                wuxing_count[wx] += 1
                break
    
    return wuxing_count

def find_yongshen(wuxing_count, day_gan):
    """简单推断喜用神（简化版）"""
    # 日主强弱判断
    day_element = {
        "甲": "木", "乙": "木",
        "丙": "火", "丁": "火",
        "戊": "土", "己": "土",
        "庚": "金", "辛": "金",
        "壬": "水", "癸": "水"
    }.get(day_gan, "木")
    
    element_strength = wuxing_count.get(day_element, 0)
    
    recommendations = []
    
    if element_strength >= 3:
        # 身强，宜泄耗
        if day_element == "木":
            recommendations = ["火", "土", "金"]
        elif day_element == "火":
            recommendations = ["土", "金", "水"]
        elif day_element == "土":
            recommendations = ["金", "水", "木"]
        elif day_element == "金":
            recommendations = ["水", "木", "火"]
        elif day_element == "水":
            recommendations = ["木", "火", "土"]
    else:
        # 身弱，宜生扶
        sheng_wo_map = {"金": "土", "木": "水", "水": "金", "火": "木", "土": "火"}
        recommendations = [sheng_wo_map.get(day_element, "土"), day_element]
    
    return {
        "day_master": day_gan,
        "element": day_element,
        "strength": element_strength,
        "recommendations": recommendations
    }

def get_da_yun(bazi, gender="男"):
    """简易大运排法（每 10 年一大运）"""
    # 根据出生月和年推算起运岁数
    month_bazi = bazi["month"]["zhi"]
    
    # 简单的起运年龄计算（传统方法是三天=一岁）
    start_age = 3  # 默认 3 岁起运
    
    # 大运干支（简化的顺逆推算）
    current_gan_idx = TIAN_GAN.index(bazi["month"]["gan"])
    current_zhi_idx = DI_ZHI.index(month_bazi)
    
    da_yun_list = []
    for i in range(8):
        gan = TIAN_GAN[(current_gan_idx + i) % 10]
        zhi = DI_ZHI[(current_zhi_idx + i) % 12]
        start = start_age + i * 10
        end = start + 9
        
        da_yun_list.append({
            "age_start": start,
            "age_end": end,
            "gan": gan,
            "zhi": zhi
        })
    
    return da_yun_list

def generate_bazi_report(birth_info):
    """生成完整的八字报告"""
    year = birth_info["year"]
    month = birth_info["month"]
    day = birth_info["day"]
    hour = birth_info["hour"]
    gender = birth_info.get("gender", "男")
    
    # 排盘
    bazi = bazi_pandan(year, month, day, hour)
    
    # 五行分析
    wuxing_count = analyze_wuxing(bazi)
    yongshen = find_yongshen(wuxing_count, bazi["day"]["gan"])
    
    # 大运
    da_yun = get_da_yun(bazi, gender)
    
    # 当前大运
    current_year = datetime.now().year
    current_age = current_year - year
    current_da_yun = None
    for dy in da_yun:
        if dy["age_start"] <= current_age <= dy["age_end"]:
            current_da_yun = dy
            break
    
    report = {
        "birth": birth_info,
        "bazi": bazi,
        "wuxing": wuxing_count,
        "yongshen": yongshen,
        "da_yun": da_yun,
        "current_age": current_age,
        "current_da_yun": current_da_yun
    }
    
    return report

def print_bazi_report(report):
    """打印八字报告"""
    print("\n" + "=" * 50)
    print("📜 八字排盘报告")
    print("=" * 50)
    
    b = report["bazi"]
    print(f"\n👶 出生信息：{report['birth']['year']}年{report['birth']['month']}月{report['birth']['day']}日 {report['birth']['hour']}:00")
    
    print(f"\n🔮 四柱八字:")
    print(f"   年柱：{b['year']['gan']}{b['year']['zhi']}")
    print(f"   月柱：{b['month']['gan']}{b['month']['zhi']}")
    print(f"   日柱：{b['day']['gan']}{b['day']['zhi']} ← 日主")
    print(f"   时柱：{b['hour']['gan']}{b['hour']['zhi']}")
    
    print(f"\n⚖️  五行分布:")
    for k, v in report["wuxing"].items():
        bar = "█" * v
        print(f"   {k}: {bar} ({v})")
    
    y = report["yongshen"]
    print(f"\n💎 日主分析:")
    print(f"   日元：{y['day_master']} ({y['element']})")
    print(f"   强弱指数：{y['strength']}/8")
    if y['strength'] >= 3:
        print(f"   状态：🟢 身强")
    else:
        print(f"   状态：🟡 身弱")
    
    print(f"   建议用神：{', '.join(y['recommendations'])}")
    
    if report["current_da_yun"]:
        cd = report["current_da_yun"]
        print(f"\n️  当前大运：{cd['gan']}{cd['zhi']} ({cd['age_start']}-{cd['age_end']}岁)")
    
    print("\n" + "=" * 50)
