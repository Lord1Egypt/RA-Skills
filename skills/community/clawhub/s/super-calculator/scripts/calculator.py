#!/usr/bin/env python3
"""
全能超级计算器 - 核心计算函数库
支持：金融、统计、单位换算、日期、健康等各类计算
"""

import math
from datetime import datetime, date
from typing import List, Optional, Tuple


# ==================== 金融计算 ====================

def compound_interest(principal: float, rate: float, years: float, freq: int = 12) -> dict:
    """
    复利计算
    principal: 本金
    rate: 年利率（百分比，如 5 表示 5%）
    years: 年数
    freq: 复利频率（12=月复利, 4=季复利, 1=年复利）
    """
    r = rate / 100
    n = freq
    t = years
    future_value = principal * math.pow(1 + r/n, n*t)
    interest = future_value - principal
    return {
        "principal": principal,
        "rate": rate,
        "years": years,
        "future_value": round(future_value, 2),
        "total_interest": round(interest, 2),
        "multiplier": round(future_value / principal, 3)
    }

def simple_interest(principal: float, rate: float, years: float) -> dict:
    """单利计算"""
    r = rate / 100
    total_interest = principal * r * years
    future_value = principal + total_interest
    return {
        "principal": principal,
        "rate": rate,
        "years": years,
        "future_value": round(future_value, 2),
        "total_interest": round(total_interest, 2)
    }

def loan_monthly_payment(principal: float, annual_rate: float, years: int) -> dict:
    """
    贷款月供计算（等额本息）
    """
    r = annual_rate / 100 / 12  # 月利率
    n = years * 12              # 总月数
    
    if r == 0:
        monthly = principal / n
    else:
        monthly = principal * (r * math.pow(1 + r, n)) / (math.pow(1 + r, n) - 1)
    
    total_payment = monthly * n
    total_interest = total_payment - principal
    
    return {
        "principal": principal,
        "annual_rate": annual_rate,
        "years": years,
        "monthly_payment": round(monthly, 2),
        "total_payment": round(total_payment, 2),
        "total_interest": round(total_interest, 2)
    }

def investment_return(principal: float, final_value: float, years: float) -> dict:
    """计算年化收益率"""
    if principal <= 0 or years <= 0:
        return {"error": "本金和期限必须大于0"}
    total_return = (final_value - principal) / principal
    annual_return = (math.pow(final_value / principal, 1/years) - 1) * 100
    return {
        "principal": principal,
        "final_value": final_value,
        "years": years,
        "total_return_pct": round(total_return * 100, 2),
        "annual_return_pct": round(annual_return, 2)
    }


# ==================== 统计计算 ====================

def basic_statistics(numbers: List[float]) -> dict:
    """基础统计：均值、方差、标准差、中位数、众数"""
    if not numbers:
        return {"error": "数据列表为空"}
    
    n = len(numbers)
    mean = sum(numbers) / n
    variance = sum((x - mean) ** 2 for x in numbers) / n
    std_dev = math.sqrt(variance)
    sorted_nums = sorted(numbers)
    
    # 中位数
    if n % 2 == 0:
        median = (sorted_nums[n//2 - 1] + sorted_nums[n//2]) / 2
    else:
        median = sorted_nums[n//2]
    
    # 众数
    from collections import Counter
    counter = Counter(numbers)
    max_count = max(counter.values())
    modes = [k for k, v in counter.items() if v == max_count]
    
    return {
        "count": n,
        "mean": round(mean, 4),
        "variance": round(variance, 4),
        "std_dev": round(std_dev, 4),
        "median": round(median, 4),
        "mode": modes if len(modes) < n else "无众数",
        "min": min(numbers),
        "max": max(numbers),
        "range": round(max(numbers) - min(numbers), 4)
    }


# ==================== 单位换算 ====================

UNIT_CONVERSIONS = {
    # 长度 (to meters)
    "m": 1, "meter": 1, "米": 1,
    "km": 1000, "kilometer": 1000, "公里": 1000,
    "cm": 0.01, "centimeter": 0.01, "厘米": 0.01,
    "mm": 0.001, "millimeter": 0.001, "毫米": 0.001,
    "inch": 0.0254, "in": 0.0254, "英寸": 0.0254,
    "ft": 0.3048, "foot": 0.3048, "英尺": 0.3048,
    "yd": 0.9144, "yard": 0.9144, "码": 0.9144,
    "mi": 1609.344, "mile": 1609.344, "英里": 1609.344,
    
    # 重量 (to kg)
    "kg": 1, "kilogram": 1, "公斤": 1,
    "g": 0.001, "gram": 0.001, "克": 0.001,
    "lb": 0.453592, "lbs": 0.453592, "磅": 0.453592,
    "oz": 0.0283495, "ounce": 0.0283495, "盎司": 0.0283495,
    "t": 1000, "ton": 1000, "吨": 1000,
    
    # 面积 (to sq meters)
    "m2": 1, "sqm": 1, "平方米": 1,
    "km2": 1_000_000, "sqkm": 1_000_000, "平方公里": 1_000_000,
    "acre": 4046.8564224, "英亩": 4046.8564224,
    "亩": 666.667,
    
    # 温度（特殊处理）
    "c": "celsius", "celsius": "celsius", "摄氏度": "celsius",
    "f": "fahrenheit", "fahrenheit": "fahrenheit", "华氏度": "fahrenheit",
}

def convert_unit(value: float, from_unit: str, to_unit: str) -> dict:
    """单位换算"""
    fu = from_unit.lower().strip()
    tu = to_unit.lower().strip()
    
    # 温度特殊处理
    if fu in ["c", "celsius", "摄氏度"] and tu in ["f", "fahrenheit", "华氏度"]:
        result = value * 9/5 + 32
        return {"from": f"{value}°C", "to": f"{round(result, 2)}°F", "result": round(result, 2)}
    if fu in ["f", "fahrenheit", "华氏度"] and tu in ["c", "celsius", "摄氏度"]:
        result = (value - 32) * 5/9
        return {"from": f"{value}°F", "to": f"{round(result, 2)}°C", "result": round(result, 2)}
    
    if fu not in UNIT_CONVERSIONS or tu not in UNIT_CONVERSIONS:
        return {"error": f"不支持的单位换算: {from_unit} → {to_unit}"}
    
    base_from = UNIT_CONVERSIONS[fu]
    base_to = UNIT_CONVERSIONS[tu]
    base_value = value * base_from
    result = base_value / base_to
    
    return {
        "from": f"{value} {from_unit}",
        "to": f"{round(result, 6)} {to_unit}",
        "result": round(result, 6)
    }


# ==================== 日期计算 ====================

def age_calculator(birth_date: str, ref_date: Optional[str] = None) -> dict:
    """计算年龄"""
    fmt = "%Y-%m-%d"
    try:
        birth = datetime.strptime(birth_date, fmt)
    except ValueError:
        try:
            birth = datetime.strptime(birth_date, "%Y年%m月%d日")
        except ValueError:
            return {"error": "日期格式不支持，请使用 YYYY-MM-DD 格式"}
    
    if ref_date:
        ref = datetime.strptime(ref_date, fmt)
    else:
        ref = datetime.now()
    
    years = ref.year - birth.year
    months = ref.month - birth.month
    days = ref.day - birth.day
    
    if days < 0:
        months -= 1
        # 获取上个月的天数
        prev_month = ref.month - 1 if ref.month > 1 else 12
        prev_year = ref.year if ref.month > 1 else ref.year - 1
        import calendar
        days += calendar.monthrange(prev_year, prev_month)[1]
    
    if months < 0:
        years -= 1
        months += 12
    
    total_days = (ref - birth).days
    
    return {
        "birth_date": birth_date,
        "age_years": years,
        "age_months": months,
        "age_days": days,
        "total_days": total_days,
        "total_months": total_days // 30,
        "description": f"{years}岁{months}个月{days}天"
    }

def date_diff(start_date: str, end_date: str) -> dict:
    """计算日期间隔"""
    fmt = "%Y-%m-%d"
    try:
        start = datetime.strptime(start_date, fmt)
    except ValueError:
        try:
            start = datetime.strptime(start_date, "%Y年%m月%d日")
            fmt = "%Y年%m月%d日"
        except ValueError:
            return {"error": "日期格式不支持"}
    
    try:
        end = datetime.strptime(end_date, fmt)
    except ValueError:
        try:
            end = datetime.strptime(end_date, "%Y年%m月%d日")
        except ValueError:
            return {"error": "日期格式不支持"}
    
    diff = end - start
    days = diff.days
    
    return {
        "start": start_date,
        "end": end_date,
        "days": abs(days),
        "months": abs(days) // 30,
        "years": round(abs(days) / 365.25, 2),
        "weeks": round(abs(days) / 7, 2)
    }


# ==================== 健康计算 ====================

def bmi(height_cm: float, weight_kg: float) -> dict:
    """计算BMI"""
    height_m = height_cm / 100
    bmi_val = weight_kg / (height_m ** 2)
    
    if bmi_val < 18.5:
        category = "偏瘦"
        color = "偏蓝色"
    elif bmi_val < 24:
        category = "正常"
        color = "绿色"
    elif bmi_val < 28:
        category = "偏胖"
        color = "黄色"
    else:
        category = "肥胖"
        color = "红色"
    
    # 标准体重
    ideal_low = 18.5 * (height_m ** 2)
    ideal_high = 24 * (height_m ** 2)
    
    return {
        "height_cm": height_cm,
        "weight_kg": weight_kg,
        "bmi": round(bmi_val, 1),
        "category": category,
        "ideal_weight_range": f"{round(ideal_low, 1)}-{round(ideal_high, 1)} kg",
        "description": f"BMI {round(bmi_val, 1)}，属于{category}范围"
    }

def bmr(height_cm: float, weight_kg: float, age: int, gender: str = "男") -> dict:
    """基础代谢率（BMR）"""
    if gender in ["男", "male", "m"]:
        bmr_val = 13.7 * weight_kg + 5 * height_cm - 6.8 * age + 66
    else:
        bmr_val = 9.5 * weight_kg + 1.9 * height_cm - 4.7 * age + 655
    
    # 每日所需热量
    tdee = {
        "久坐": bmr_val * 1.2,
        "轻度活动": bmr_val * 1.375,
        "中度活动": bmr_val * 1.55,
        "重度活动": bmr_val * 1.725,
        "运动员": bmr_val * 1.9
    }
    
    return {
        "gender": gender,
        "age": age,
        "bmr": round(bmr_val, 0),
        "daily_calories": {k: round(v, 0) for k, v in tdee.items()}
    }


# ==================== 方程求解 ====================

def solve_linear(a: float, b: float) -> dict:
    """一元一次方程 ax + b = 0"""
    if a == 0:
        if b == 0:
            return {"equation": f"{a}x + {b} = 0", "solution": "无穷多解"}
        return {"equation": f"{a}x + {b} = 0", "solution": "无解"}
    x = -b / a
    return {"equation": f"{a}x + {b} = 0", "solution": f"x = {round(x, 6)}"}

def solve_quadratic(a: float, b: float, c: float) -> dict:
    """一元二次方程 ax² + bx + c = 0"""
    if a == 0:
        return solve_linear(b, c)
    
    discriminant = b**2 - 4*a*c
    eq = f"{a}x² + {b}x + {c} = 0"
    
    if discriminant < 0:
        real = -b / (2*a)
        imag = math.sqrt(-discriminant) / (2*a)
        return {
            "equation": eq,
            "type": "无实数解（有两个共轭复根）",
            "x1": f"{round(real, 4)} + {round(imag, 4)}i",
            "x2": f"{round(real, 4)} - {round(imag, 4)}i"
        }
    elif discriminant == 0:
        x = -b / (2*a)
        return {"equation": eq, "type": "重根", "x": round(x, 6)}
    else:
        x1 = (-b + math.sqrt(discriminant)) / (2*a)
        x2 = (-b - math.sqrt(discriminant)) / (2*a)
        return {"equation": eq, "type": "两个不等实根", "x1": round(x1, 6), "x2": round(x2, 6)}


if __name__ == "__main__":
    print("=== 复利测试 ===")
    print(compound_interest(100000, 5, 20))
    
    print("\n=== 贷款月供测试 ===")
    print(loan_monthly_payment(2000000, 4.9, 20))
    
    print("\n=== 统计测试 ===")
    print(basic_statistics([2, 4, 4, 4, 5, 5, 7, 9]))
    
    print("\n=== BMI测试 ===")
    print(bmi(175, 70))
    
    print("\n=== 年龄测试 ===")
    print(age_calculator("1988-07-01"))
