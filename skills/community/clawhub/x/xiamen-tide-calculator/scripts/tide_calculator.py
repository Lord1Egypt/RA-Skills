#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
厦门潮汐计算器 - 增强版 v3.2
根据公历或农历日期计算厦门海域的潮汐时间，提供赶海评分和建议
支持公历自动转农历、当前日期自动识别、闰月处理
新功能：多窗口期分析、优缺点描述、推荐指数、整合窗口功能

版权信息：
    Copyright (c) 2026 柯英杰
    许可协议：MIT License
    
    作者：柯英杰
    创建日期：2026年4月2日
    最后更新：2026年4月3日
    版本：v3.2
    
    GitHub: https://github.com/kingwingshome/xiamen-tide-calculator
    
免责声明：
    本程序基于厦门海域标准潮汐计算公式，仅供参考。实际潮汐时间可能受
    天气、气压、地形等因素影响。赶海活动存在风险，请务必注意安全。
    使用本程序进行赶海活动，用户需自行承担风险。
"""

import argparse
import sys
import io
from datetime import datetime
import calendar

# 尝试导入农历转换库
try:
    import zhdate
    ZHDATE_AVAILABLE = True
except ImportError:
    ZHDATE_AVAILABLE = False

# 设置标准输出编码为UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def get_current_lunar_date():
    """
    获取当前日期的农历日期

    返回:
        (lunar_year, lunar_month, lunar_day, is_leap_month) 元组
    """
    if not ZHDATE_AVAILABLE:
        return None, None, None, False

    today = zhdate.ZhDate.today()
    return today.lunar_year, today.lunar_month, today.lunar_day, today.leap_month


def solar_to_lunar(solar_date_str):
    """
    公历日期转农历日期

    参数:
        solar_date_str: 公历日期字符串，格式为 YYYY-MM-DD

    返回:
        (lunar_year, lunar_month, lunar_day, is_leap_month) 元组
    """
    if not ZHDATE_AVAILABLE:
        print("错误：未找到农历转换库(zhdate)，无法进行公历转农历")
        print("请安装: pip install zhdate")
        return None, None, None, False

    try:
        # 使用datetime而不是date，避免类型兼容性问题
        solar_datetime = datetime.strptime(solar_date_str, "%Y-%m-%d")
        lunar_date = zhdate.ZhDate.from_datetime(solar_datetime)

        return lunar_date.lunar_year, lunar_date.lunar_month, lunar_date.lunar_day, lunar_date.leap_month

    except ValueError as e:
        print(f"错误：日期格式不正确，请使用 YYYY-MM-DD 格式")
        return None, None, None, False
    except Exception as e:
        print(f"错误：农历转换失败 - {str(e)}")
        return None, None, None, False


def get_season_info():
    """
    获取当前季节信息
    返回: (season_name, season_score, description)
    """
    month = datetime.now().month

    if month in [3, 4, 5]:
        return "春季", 10, "气候适宜，生物活跃，赶海最佳季节"
    elif month in [6, 7, 8]:
        return "夏季", 7, "天气炎热，建议早晚赶海，注意防晒"
    elif month in [9, 10, 11]:
        return "秋季", 10, "气候凉爽，生物丰富，赶海最佳季节"
    else:  # 冬季
        return "冬季", 4, "天气寒冷，生物活动少，不推荐赶海"


def calculate_beach_score(lunar_day, low1_h, low2_h, is_leap_month=False):
    """
    计算赶海评分（支持闰月）

    参数:
        lunar_day: 农历日期
        low1_h, low2_h: 两次低潮的小时数
        is_leap_month: 是否为闰月（默认为False）

    返回:
        (score, rating) 评分和等级
    """
    score = 0

    # 1. 潮汐大小评分（权重40%）
    # 闰月的潮汐可能与正常月份略有不同，这里暂时使用相同的判断逻辑
    tide_size = judge_tide_size(lunar_day, is_leap_month)
    if tide_size == "大潮":
        score += 4.0
    elif tide_size == "中潮":
        score += 2.4
    else:  # 小潮
        score += 0.8

    # 2. 赶海时间窗口评分（权重30%）
    # 评估窗口时长和时间段
    window_hours = 3  # 窗口时长3小时
    window_score = window_hours * 1.0  # 满分3分
    score += window_score

    # 3. 潮汐时间分布评分（权重20%）
    # 低潮在白天的加分
    day_low_count = 0
    for low_h in [low1_h, low2_h]:
        if 6 <= low_h < 18:  # 白天（6:00-18:00）
            day_low_count += 1

    if day_low_count == 2:
        score += 2.0
    elif day_low_count == 1:
        score += 1.0
    else:
        score += 0.0

    # 4. 季节因素评分（权重10%）
    _, season_score, _ = get_season_info()
    score += season_score * 0.1

    # 5. 闰月因素（额外调整）
    # 闰月期间，生物活动可能略有不同，给一个小的调整
    if is_leap_month:
        score += 0.2  # 闰月略有加分

    # 总分转换为整数
    final_score = round(score, 1)

    # 确定等级
    if final_score >= 8.0:
        rating = "强烈推荐"
    elif final_score >= 6.0:
        rating = "推荐"
    elif final_score >= 4.0:
        rating = "一般"
    else:
        rating = "不推荐"

    return final_score, rating


def get_location_recommendation(tide_size, is_leap_month=False):
    """
    根据潮汐大小和闰月推荐赶海地点

    返回: 推荐地点列表
    """
    locations = []

    if tide_size == "大潮":
        locations = [
            "五缘湾：潮差大，生物丰富",
            "翔安沿海：滩涂广，种类多",
            "环岛路沿线：交通便利，适合初学者"
        ]
    elif tide_size == "中潮":
        locations = [
            "环岛路沿线：交通便利",
            "集美鳌园：适合家庭赶海",
            "曾厝垵海滩：沙底松软"
        ]
    else:  # 小潮
        locations = [
            "建议等待大潮再赶海",
            "小潮期生物较少，收获有限"
        ]

    # 闰月期间的额外提示
    if is_leap_month:
        locations.append("注：闰月期间潮汐可能略有不同")

    return locations


def get_equipment_suggestion(season):
    """
    根据季节提供赶海装备建议

    返回: 装备建议字典
    """
    if season == "夏季":
        return {
            "必备": ["小铲子", "小桶", "防滑鞋", "手套"],
            "推荐": ["照明设备", "防晒帽", "防晒霜", "饮用水"],
            "特别提醒": "天气炎热，注意防暑降温"
        }
    elif season == "冬季":
        return {
            "必备": ["小铲子", "小桶", "防滑鞋", "手套"],
            "推荐": ["轻便外套", "保暖帽", "热水", "照明设备"],
            "特别提醒": "天气寒冷，注意保暖"
        }
    else:  # 春秋季
        return {
            "必备": ["小铲子", "小桶", "防滑鞋", "手套"],
            "推荐": ["照明设备", "轻便外套"],
            "特别提醒": "气候适宜，轻装上阵"
        }


def get_safety_warnings(low1_time, low2_time, beach_windows):
    """
    获取安全提醒

    返回: 安全提醒列表
    """
    warnings = []

    # 潮水上涨提醒
    for i, window in enumerate(beach_windows, 1):
        parts = window.split('-')
        if len(parts) == 2:
            end_time = parts[1].strip()
            warnings.append(f"赶海窗口{i}结束时间：{end_time}，之后潮水开始上涨，请及时撤离")

    # 通用安全提醒
    warnings.append("建议结伴同行，不要单独赶海")
    warnings.append("注意礁石区域，小心滑倒")
    warnings.append("穿戴防滑鞋，避免在湿滑区域摔倒")

    return warnings


def get_expected_harvest(tide_size):
    """
    根据潮汐大小预测赶海收获

    返回: 收获物列表
    """
    if tide_size == "大潮":
        return ["花蛤", "海螺", "小螃蟹", "海蛎子", "小虾"]
    elif tide_size == "中潮":
        return ["花蛤", "小螃蟹", "海蛎子"]
    else:  # 小潮
        return ["收获较少，不建议赶海"]


def format_decimal_time(decimal_hours):
    """
    将小数小时转换为 HH:MM 格式
    例如：6.4 → "06:24"
    """
    hours = int(decimal_hours)
    minutes = round((decimal_hours - hours) * 60)

    # 处理浮点精度问题
    if minutes >= 60:
        hours += 1
        minutes -= 60

    return f"{hours:02d}:{minutes:02d}"


def add_time(hh, mm, add_hours=0, add_minutes=0):
    """
    向时间添加小时和分钟
    """
    total_minutes = hh * 60 + mm + add_hours * 60 + add_minutes
    new_hh = total_minutes // 60
    new_mm = total_minutes % 60
    return new_hh, new_mm


def subtract_time(hh, mm, sub_hours=0, sub_minutes=0):
    """
    从时间减去小时和分钟
    """
    total_minutes = hh * 60 + mm - sub_hours * 60 - sub_minutes
    new_hh = total_minutes // 60
    new_mm = total_minutes % 60
    return new_hh, new_mm


def calculate_tide(lunar_day, is_leap_month=False):
    """
    根据农历日期计算潮汐时间（支持闰月）

    参数:
        lunar_day: 农历日期（1-30）
        is_leap_month: 是否为闰月（默认为False）

    返回:
        包含潮汐信息的字典
    """
    # 第一步：计算第一次高潮时间
    # 闰月对潮汐时间的影响较小，暂时使用相同的计算公式
    if lunar_day <= 15:
        high1_decimal = lunar_day * 0.8
    else:
        high1_decimal = (lunar_day - 15) * 0.8

    high1 = format_decimal_time(high1_decimal)
    high1_h = int(high1_decimal)
    high1_m = round((high1_decimal - high1_h) * 60)

    # 第二步：计算第二次高潮（第一次高潮 + 12小时24分）
    high2_h, high2_m = add_time(high1_h, high1_m, 12, 24)
    # 处理超过24小时的情况
    if high2_h >= 24:
        high2 = f"次日 {(high2_h - 24):02d}:{high2_m:02d}"
    else:
        high2 = f"{high2_h:02d}:{high2_m:02d}"

    # 第三步：计算两次低潮（高潮 - 6小时12分）
    low1_h, low1_m = subtract_time(high1_h, high1_m, 6, 12)
    # 处理负时间的情况（跨天）
    if low1_h < 0:
        low1 = f"前日 {(24 + low1_h):02d}:{low1_m:02d}"
    else:
        low1 = f"{low1_h:02d}:{low1_m:02d}"

    low2_h, low2_m = subtract_time(high2_h, high2_m, 6, 12)
    if low2_h >= 24:
        low2 = f"次日 {(low2_h - 24):02d}:{low2_m:02d}"
    elif low2_h < 0:
        low2 = f"前日 {(24 + low2_h):02d}:{low2_m:02d}"
    else:
        low2 = f"{low2_h:02d}:{low2_m:02d}"

    # 第四步：判断潮汐大小（支持闰月）
    tide_size = judge_tide_size(lunar_day, is_leap_month)

    # 第五步：计算赶海窗口（低潮前2小时到低潮后1小时）
    beach_windows = calculate_beach_windows(low1_h, low1_m, low2_h, low2_m)

    # 第六步：计算赶海评分（支持闰月）
    beach_score, beach_rating = calculate_beach_score(lunar_day, low1_h, low2_h, is_leap_month)

    return {
        'high1': high1,
        'high2': high2,
        'low1': low1,
        'low2': low2,
        'low1_h': low1_h,
        'low2_h': low2_h,
        'tide_size': tide_size,
        'beach_windows': beach_windows,
        'beach_score': beach_score,
        'beach_rating': beach_rating,
        'is_leap_month': is_leap_month
    }


def judge_tide_size(lunar_day, is_leap_month=False):
    """
    判断潮汐大小（支持闰月）

    参数:
        lunar_day: 农历日期（1-30）
        is_leap_month: 是否为闰月（默认为False）

    返回:
        "大潮"、"中潮" 或 "小潮"
    """
    # 闰月的潮汐判断可能与正常月份略有不同
    # 但目前科学数据表明，闰月对潮汐的影响较小
    # 暂时使用相同的判断逻辑
    # 可以在未来根据实际观测数据进行调整

    if lunar_day in [2, 3, 17, 18]:
        tide_size = "大潮"
    elif lunar_day in [8, 9, 23, 24]:
        tide_size = "小潮"
    else:
        tide_size = "中潮"

    # 闰月期间的额外标记
    if is_leap_month:
        tide_size += "（闰月）"

    return tide_size


def format_time_with_day(hh, mm):
    """
    格式化时间，处理跨天情况

    返回:
        格式化的时间字符串（如 "08:36" 或 "前日 22:12" 或 "次日 02:24"）
    """
    if hh >= 24:
        return f"次日 {(hh - 24):02d}:{mm:02d}"
    elif hh < 0:
        return f"前日 {(24 + hh):02d}:{mm:02d}"
    else:
        return f"{hh:02d}:{mm:02d}"


def get_time_period_type(hh, mm):
    """
    判断时间段类型（上午、下午、傍晚、清晨）

    参数:
        hh: 小时
        mm: 分钟

    返回:
        (period_type, period_name) 元组
        period_type: 0=跨天, 1=清晨, 2=上午, 3=下午, 4=傍晚, 5=夜间
    """
    total_minutes = hh * 60 + mm

    if hh >= 24:
        return 0, "次日"
    elif hh < 0:
        return 0, "前日"
    elif 4 <= total_minutes < 360:  # 4:00-6:00
        return 1, "清晨"
    elif 360 <= total_minutes < 720:  # 6:00-12:00
        return 2, "上午"
    elif 720 <= total_minutes < 1080:  # 12:00-18:00
        return 3, "下午"
    elif 1080 <= total_minutes < 1260:  # 18:00-21:00
        return 4, "傍晚"
    else:
        return 5, "夜间"


def get_window_advantages_disadvantages(period_name):
    """
    获取不同时间窗口的优缺点

    参数:
        period_name: 时间段名称（上午、下午、傍晚、清晨、夜间）

    返回:
        (advantages, disadvantages) 元组
    """
    advantages = []
    disadvantages = []

    if period_name == "上午":
        advantages = [
            "✅ 光线充足，视野清晰，安全性高",
            "✅ 气温适宜，赶海舒适度高",
            "✅ 潮水退潮彻底，生物活跃",
            "✅ 交通便利，适合所有人群",
            "✅ 收获丰富，海货种类多"
        ]
        disadvantages = [
            "❌ 需要早起，部分人群可能不适应"
        ]

    elif period_name == "下午":
        advantages = [
            "✅ 光线良好，视野清晰",
            "✅ 气温较高，适合不怕热的赶海者",
            "✅ 有充足的时间准备",
            "✅ 潮汐退潮程度较好"
        ]
        disadvantages = [
            "❌ 夏季可能较热，需注意防晒",
            "❌ 人体较疲劳，赶海效率可能降低",
            "❌ 可能需要配合晚间活动"
        ]

    elif period_name == "傍晚":
        advantages = [
            "✅ 气温凉爽，赶海舒适度高",
            "✅ 光线柔和，适合拍照",
            "✅ 退潮时间长，海货丰富",
            "✅ 工作时间后可前往，适合上班族"
        ]
        disadvantages = [
            "❌ 天色渐暗，视野受限",
            "❌ 潮水上涨较快，需注意安全",
            "❌ 后期可能需要照明设备",
            "❌ 时间较短，需要抓紧时间"
        ]

    elif period_name == "清晨":
        advantages = [
            "✅ 气温凉爽，赶海舒适度高",
            "✅ 潮水退潮程度最好，海货最多",
            "✅ 环境安静，赶海体验佳",
            "✅ 可以欣赏日出（时间合适时）"
        ]
        disadvantages = [
            "❌ 需要非常早起（3-4点）",
            "❌ 光线较暗，需要照明设备",
            "❌ 安全性较低，建议结伴同行",
            "❌ 气温较低，需注意保暖"
        ]

    elif period_name == "夜间":
        advantages = [
            "✅ 生物活跃度高，可能有意外收获",
            "✅ 退潮时间长，可以慢慢探索",
            "✅ 避开白天人群，体验独特"
        ]
        disadvantages = [
            "❌ 视野极差，必须携带照明设备",
            "❌ 安全性低，强烈建议结伴同行",
            "❌ 容易迷路或踩空，需特别小心",
            "❌ 不适合赶海新手"
        ]

    elif period_name in ["前日", "次日"]:
        advantages = ["该窗口不在当天范围内"]
        disadvantages = ["不属于当天赶海窗口"]

    return advantages, disadvantages


def calculate_beach_windows(low1_h, low1_m, low2_h, low2_m):
    """
    计算赶海最佳窗口（低潮前2小时到低潮后1小时）

    返回:
        两个赶海窗口的字符串列表
    """
    windows = []

    # 第一个赶海窗口
    start1_h, start1_m = add_time(low1_h, low1_m, -2, 0)
    end1_h, end1_m = add_time(low1_h, low1_m, 1, 0)
    start1 = format_time_with_day(start1_h, start1_m)
    end1 = format_time_with_day(end1_h, end1_m)
    windows.append(f"{start1}-{end1}")

    # 第二个赶海窗口
    start2_h, start2_m = add_time(low2_h, low2_m, -2, 0)
    end2_h, end2_m = add_time(low2_h, low2_m, 1, 0)
    start2 = format_time_with_day(start2_h, start2_m)
    end2 = format_time_with_day(end2_h, end2_m)
    windows.append(f"{start2}-{end2}")

    return windows


def get_integrated_windows(solar_date_str):
    """
    获取整合后的当日窗口（计算前后一天的窗口，整合出当天所有窗口）

    参数:
        solar_date_str: 公历日期字符串，格式为 YYYY-MM-DD

    返回:
        (windows, score, rating, tide_size) 整合后的窗口列表和评分
    """
    if not ZHDATE_AVAILABLE:
        return [], 0, 0, 0

    try:
        # 解析目标日期
        target_datetime = datetime.strptime(solar_date_str, "%Y-%m-%d")

        # 计算前一天、当天、后一天的日期
        from datetime import timedelta
        prev_datetime = target_datetime - timedelta(days=1)
        next_datetime = target_datetime + timedelta(days=1)

        prev_date_str = prev_datetime.strftime("%Y-%m-%d")
        next_date_str = next_datetime.strftime("%Y-%m-%d")

        # 计算三天的潮汐
        prev_lunar = solar_to_lunar(prev_date_str)
        curr_lunar = solar_to_lunar(solar_date_str)
        next_lunar = solar_to_lunar(next_date_str)

        if prev_lunar[0] is None or curr_lunar[0] is None or next_lunar[0] is None:
            return [], 0, 0, 0

        # 获取三天的潮汐信息
        prev_tide = calculate_tide(prev_lunar[2], prev_lunar[3])
        curr_tide = calculate_tide(curr_lunar[2], curr_lunar[3])
        next_tide = calculate_tide(next_lunar[2], next_lunar[3])

        # 提取所有窗口，判断哪些属于当天（0:00-24:00之间）
        all_windows = []

        # 前一天的窗口2（可能在当天）
        window_prev2 = prev_tide['beach_windows'][1]
        if "前日" not in window_prev2 and "次日" not in window_prev2:
            # 这个窗口完全在前一天，不包含
            pass
        else:
            # 这个窗口可能跨到当天
            parts = window_prev2.split('-')
            if len(parts) == 2:
                end_str = parts[1].strip()
                # 如果结束时间包含"前日"，说明还在前一天
                # 如果不包含"前日"，说明在当天
                if "前日" not in end_str:
                    # 提取开始和结束时间
                    start_parts = parts[0].strip().replace("次日 ", "").replace("前日 ", "").split(':')
                    end_parts = end_str.replace("次日 ", "").replace("前日 ", "").split(':')
                    if len(start_parts) == 2 and len(end_parts) == 2:
                        start_h = int(start_parts[0])
                        start_m = int(start_parts[1])
                        end_h = int(end_parts[0])
                        end_m = int(end_parts[1])
                        # 判断是否属于当天
                        if 0 <= start_h < 24 and 0 <= end_h < 24:
                            all_windows.append({
                                'time': f"{start_h:02d}:{start_m:02d}-{end_h:02d}:{end_m:02d}",
                                'low_time': prev_tide['low2'],
                                'source': '前一天窗口2'
                            })

        # 当天的窗口
        for i, window in enumerate(curr_tide['beach_windows'], 1):
            if "前日" not in window and "次日" not in window:
                parts = window.split('-')
                if len(parts) == 2:
                    start_parts = parts[0].split(':')
                    end_parts = parts[1].split(':')
                    if len(start_parts) == 2 and len(end_parts) == 2:
                        start_h = int(start_parts[0])
                        start_m = int(start_parts[1])
                        end_h = int(end_parts[0])
                        end_m = int(end_parts[1])
                        all_windows.append({
                            'time': f"{start_h:02d}:{start_m:02d}-{end_h:02d}:{end_m:02d}",
                            'low_time': curr_tide['low2'] if i == 2 else curr_tide['low1'],
                            'source': f'当天窗口{i}'
                        })

        # 后一天的窗口1（可能在当天傍晚）
        window_next1 = next_tide['beach_windows'][0]
        if "前日" not in window_next1 and "次日" not in window_next1:
            # 这个窗口完全在后一天，不包含
            pass
        else:
            # 这个窗口可能在当天傍晚
            parts = window_next1.split('-')
            if len(parts) == 2:
                start_str = parts[0].strip()
                # 如果开始时间包含"前日"，说明在当天
                if "前日" in start_str:
                    # 提取开始和结束时间
                    start_parts = start_str.replace("前日 ", "").split(':')
                    end_parts = parts[1].strip().replace("次日 ", "").replace("前日 ", "").split(':')
                    if len(start_parts) == 2 and len(end_parts) == 2:
                        start_h = int(start_parts[0])
                        start_m = int(start_parts[1])
                        end_h = int(end_parts[0])
                        end_m = int(end_parts[1])
                        # 判断是否属于当天
                        if 0 <= start_h < 24:
                            all_windows.append({
                                'time': f"{start_h:02d}:{start_m:02d}-{end_h:02d}:{end_m:02d}",
                                'low_time': next_tide['low1'],
                                'source': '后一天窗口1'
                            })

        # 按时间排序窗口
        def extract_start_time(window_info):
            time_str = window_info['time'].split('-')[0]
            parts = time_str.split(':')
            return int(parts[0]) * 60 + int(parts[1])

        all_windows.sort(key=extract_start_time)

        # 返回窗口列表和评分
        window_times = [w['time'] for w in all_windows]
        return window_times, curr_tide['beach_score'], curr_tide['beach_rating'], curr_tide['tide_size']

    except Exception as e:
        return [], 0, 0, 0


def format_standard_output(lunar_year, lunar_month, lunar_day, tide_info, is_leap_month=False):
    """
    格式化标准潮汐信息输出
    """
    output = []
    month_str = f"闰{lunar_month}月" if is_leap_month else f"{lunar_month}月"
    output.append(f"【厦门潮汐・农历{lunar_year}年{month_str}{lunar_day}日】")
    output.append(f"高潮 1：{tide_info['high1']}")
    output.append(f"高潮 2：{tide_info['high2']}")
    output.append(f"低潮 1：{tide_info['low1']}")
    output.append(f"低潮 2：{tide_info['low2']}")
    output.append(f"最佳赶海：{tide_info['beach_windows'][0]}（窗口1）、{tide_info['beach_windows'][1]}（窗口2）")
    output.append(f"潮汐大小：{tide_info['tide_size']}")
    output.append(f"赶海评分：{tide_info['beach_score']}分（{tide_info['beach_rating']}）")

    return '\n'.join(output)


def format_beach_output(lunar_year, lunar_month, lunar_day, tide_info, is_leap_month=False, integrated_windows=None):
    """
    格式化赶海专门模式输出（增强版：多窗口期优缺点分析）

    参数:
        lunar_year, lunar_month, lunar_day: 农历日期
        tide_info: 潮汐信息字典
        is_leap_month: 是否为闰月
        integrated_windows: 整合后的窗口列表（可选，如果提供则使用整合窗口）
    """
    output = []
    month_str = f"闰{lunar_month}月" if is_leap_month else f"{lunar_month}月"
    output.append(f"【厦门赶海建议・农历{lunar_year}年{month_str}{lunar_day}日】")
    output.append("")
    output.append(f"🌊 赶海评分：{tide_info['beach_score']}分（{tide_info['beach_rating']}）")
    output.append("")

    # 赶海时段（详细分析每个窗口）
    output.append("⏰ 最佳赶海时段：")

    # 使用整合窗口或原始窗口
    windows_to_analyze = integrated_windows if integrated_windows else tide_info['beach_windows']

    # 分析每个窗口
    for i, window in enumerate(windows_to_analyze, 1):
        output.append("")
        output.append(f"  【窗口{i}】{window}")

        # 解析窗口时间
        parts = window.split('-')
        if len(parts) == 2:
            start_str = parts[0].strip()
            end_str = parts[1].strip()

            # 提取开始时间的小时
            start_h = 0
            if "次日" in start_str:
                start_h = 24
            elif "前日" in start_str:
                start_h = -24

            # 提取时间数字
            time_parts = start_str.replace("次日 ", "").replace("前日 ", "").split(':')
            if len(time_parts) == 2:
                start_h += int(time_parts[0])
                start_m = int(time_parts[1])

                # 判断窗口类型
                period_type, period_name = get_time_period_type(start_h, start_m)

                # 判断是否为当天窗口
                is_same_day = (period_type != 0)  # 0表示跨天

                if is_same_day:
                    output.append(f"  └─ 时间类型：{period_name}")

                    # 获取优缺点
                    advantages, disadvantages = get_window_advantages_disadvantages(period_name)

                    # 优点
                    if advantages:
                        output.append(f"  └─ 优势：")
                        for adv in advantages[:3]:  # 只显示前3个优点
                            output.append(f"     {adv}")

                    # 缺点
                    if disadvantages:
                        output.append(f"  └─ 注意事项：")
                        for disadv in disadvantages[:2]:  # 只显示前2个缺点
                            output.append(f"     {disadv}")

                    # 判断是否推荐
                    if period_name == "上午" or period_name == "傍晚":
                        output.append(f"  └─ ⭐ 推荐指数：⭐⭐⭐⭐⭐")
                    elif period_name == "下午":
                        output.append(f"  └─ ⭐ 推荐指数：⭐⭐⭐⭐")
                    else:
                        output.append(f"  └─ ⭐ 推荐指数：⭐⭐⭐")
                else:
                    output.append(f"  └─ ⚠️ 该窗口不在当天范围内（{period_name}）")

    output.append("")

    # 推荐地点
    output.append("📍 推荐地点：")
    locations = get_location_recommendation(tide_info['tide_size'], is_leap_month)
    for loc in locations:
        output.append(f"  - {loc}")
    output.append("")

    # 预期收获
    output.append("🐟 预期收获：")
    harvest = get_expected_harvest(tide_info['tide_size'])
    output.append(f"  - {', '.join(harvest)}")
    output.append("")

    # 装备建议
    season_name, _, _ = get_season_info()
    equipment = get_equipment_suggestion(season_name)
    output.append("🧰 装备建议：")
    output.append(f"  - 必备：{', '.join(equipment['必备'])}")
    output.append(f"  - 推荐：{', '.join(equipment['推荐'])}")
    output.append(f"  - 特别提醒：{equipment['特别提醒']}")
    output.append("")

    # 安全提醒
    output.append("⚠️ 安全提醒：")
    warnings = get_safety_warnings(
        tide_info['low1'],
        tide_info['low2'],
        tide_info['beach_windows']
    )
    for warning in warnings:
        output.append(f"  - {warning}")
    output.append("")

    # 潮汐详细信息
    output.append("📊 潮汐信息：")
    output.append(f"  - 潮汐大小：{tide_info['tide_size']}")
    output.append(f"  - 低潮1：{tide_info['low1']}")
    output.append(f"  - 低潮2：{tide_info['low2']}")
    output.append(f"  - 高潮1：{tide_info['high1']}")
    output.append(f"  - 高潮2：{tide_info['high2']}")
    output.append("")

    # 季节信息
    season_name, season_score, season_desc = get_season_info()
    output.append("🌡️ 当前季节：")
    output.append(f"  - {season_name} - {season_desc}")
    output.append("")

    # 赶海提示
    output.append("💡 赶海提示：")
    output.append("  - 建议赶海窗口前1小时到达")
    output.append("  - 重点关注低潮前2小时的生物活跃期")
    output.append("  - 注意保护海洋生态，合理采撷")
    output.append("  - 不赶海时请带走垃圾，保护海洋环境")
    if is_leap_month:
        output.append("  - 闰月期间，潮汐可能略有不同，建议实地观察")

    return '\n'.join(output)


def main():
    # 设置标准输出编码为UTF-8
    if hasattr(sys.stdout, 'buffer'):
        sys.stdout.reconfigure(encoding='utf-8')

    parser = argparse.ArgumentParser(description='厦门潮汐计算器 v3.2')
    parser.add_argument('--lunar-day', type=int, help='农历日期（1-30）')
    parser.add_argument('--lunar-month', type=int, default=1, help='农历月份（1-12），默认为1月')
    parser.add_argument('--solar-date', type=str, help='公历日期（YYYY-MM-DD格式）')
    parser.add_argument('--today', action='store_true', help='使用当前日期')
    parser.add_argument('--beach-mode', action='store_true', help='赶海专门模式，提供详细赶海建议')
    parser.add_argument('--integrated', action='store_true', help='整合前后一天窗口，显示当天所有可用窗口')

    args = parser.parse_args()

    lunar_year = None
    lunar_month = args.lunar_month
    lunar_day = args.lunar_day
    is_leap_month = False

    # 处理公历日期
    if args.solar_date:
        lunar_year, lunar_month, lunar_day, is_leap_month = solar_to_lunar(args.solar_date)
        if lunar_day is None:
            return 1

    # 处理当前日期
    elif args.today:
        lunar_year, lunar_month, lunar_day, is_leap_month = get_current_lunar_date()
        if lunar_day is None:
            print("错误：无法获取当前农历日期，请使用 --lunar-day 和 --lunar-month 参数")
            return 1

    # 如果没有提供任何日期参数
    elif args.lunar_day is None:
        print("提示：未提供日期，将使用当前日期")
        lunar_year, lunar_month, lunar_day, is_leap_month = get_current_lunar_date()
        if lunar_day is None:
            print("错误：无法获取当前农历日期，请使用 --lunar-day 和 --lunar-month 参数")
            return 1

    # 验证农历日期
    if not 1 <= lunar_day <= 30:
        print("错误：农历日期必须在1-30之间")
        return 1

    if not 1 <= lunar_month <= 12:
        print("错误：农历月份必须在1-12之间")
        return 1

    # 如果没有提供年份，使用当前年份
    if lunar_year is None:
        lunar_year = datetime.now().year

    # 计算潮汐
    tide_info = calculate_tide(lunar_day, is_leap_month)

    # 格式化输出
    if args.beach_mode:
        # 如果启用整合窗口功能
        if args.integrated and args.solar_date:
            # 获取整合后的窗口
            integrated_windows, integrated_score, integrated_rating, integrated_tide_size = get_integrated_windows(args.solar_date)
            if integrated_windows:
                # 使用整合后的窗口和评分
                tide_info['beach_windows'] = integrated_windows
                tide_info['beach_score'] = integrated_score
                tide_info['beach_rating'] = integrated_rating
                tide_info['tide_size'] = integrated_tide_size
                output = format_beach_output(lunar_year, lunar_month, lunar_day, tide_info, is_leap_month, integrated_windows)
            else:
                # 整合失败，使用原始窗口
                output = format_beach_output(lunar_year, lunar_month, lunar_day, tide_info, is_leap_month)
        else:
            output = format_beach_output(lunar_year, lunar_month, lunar_day, tide_info, is_leap_month)
    else:
        output = format_standard_output(lunar_year, lunar_month, lunar_day, tide_info, is_leap_month)
    print(output)

    return 0


if __name__ == '__main__':
    sys.exit(main())
