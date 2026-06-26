#!/usr/bin/env python3
"""
退休规划计算器
计算退休时间和社保缴费总额
支持：职工社保、灵活就业社保
"""

import sys
import json
from datetime import datetime, timedelta
from typing import Dict, Tuple, Optional

# 中国延迟退休政策参数（2025年1月1日起实施）
RETIREMENT_POLICY = {
    "male": {
        "base_age": 60,  # 原退休年龄
        "target_age": 63,  # 目标退休年龄
        "transition_start": "2025-01-01",
        "transition_months": 36,  # 每4个月延迟1个月，总共36个月（3年）
    },
    "female_worker": {
        "base_age": 50,
        "target_age": 55,
        "transition_start": "2025-01-01",
        "transition_months": 60,  # 每2个月延迟1个月，总共60个月（5年）
    },
    "female_cadre": {
        "base_age": 55,
        "target_age": 58,
        "transition_start": "2025-01-01",
        "transition_months": 36,  # 每4个月延迟1个月，总共36个月（3年）
    }
}

# 职工社保缴费比例（有单位）
EMPLOYEE_RATES = {
    "pension": 0.08,       # 养老保险个人缴费比例 8%
    "medical": 0.02,       # 医疗保险个人缴费比例 2%
    "unemployment": 0.005, # 失业保险个人缴费比例 0.5%
    "housing_fund": 0.07,  # 住房公积金个人缴费比例 7%（范围5%-12%）
}

# 灵活就业缴费比例（无单位，自己缴纳）
FLEXIBLE_RATES = {
    "pension": 0.20,       # 养老保险 20%（8%进个人账户，12%进统筹）
    "medical": None,       # 医疗保险各地不同，见下方字典
    "unemployment": 0,     # 灵活就业没有失业保险
    "housing_fund": 0,     # 灵活就业一般没有公积金（可选，但很少交）
}

# 各城市灵活就业医疗保险缴费比例（各地差异较大）
CITY_FLEXIBLE_MEDICAL_RATES = {
    "北京": 0.065,    # 6.5%
    "上海": 0.11,     # 11%
    "广州": 0.08,     # 8%
    "深圳": 0.08,     # 8%
    "杭州": 0.095,    # 9.5%
    "成都": 0.088,    # 8.8%
    "武汉": 0.06,     # 6%
    "西安": 0.06,     # 6%
    "南京": 0.10,     # 10%
    "重庆": 0.10,     # 10%（分两档，这里取二档）
    "天津": 0.075,    # 7.5%
    "苏州": 0.10,     # 10%
    "其他城市": 0.08,  # 默认 8%
}

# 各城市2024年社保缴费基数上下限（单位：元）
CITY_SOCIAL_INSURANCE_BASE = {
    "北京": {"min": 6821, "max": 35283},
    "上海": {"min": 7384, "max": 36921},
    "广州": {"min": 5284, "max": 26421},
    "深圳": {"min": 4492, "max": 26421},
    "杭州": {"min": 4812, "max": 24930},
    "成都": {"min": 4246, "max": 21228},
    "武汉": {"min": 4224, "max": 21120},
    "西安": {"min": 4224, "max": 21120},
    "南京": {"min": 4494, "max": 24042},
    "重庆": {"min": 4118, "max": 20587},
    "天津": {"min": 5013, "max": 25065},
    "苏州": {"min": 4494, "max": 24042},
    "其他城市": {"min": 4000, "max": 20000},  # 默认值
}


def calculate_retirement_age(birth_date: str, gender: str, job_type: str = "worker") -> Tuple[int, int]:
    """
    计算退休年龄和延迟月数
    
    Args:
        birth_date: 出生日期，格式 "YYYY-MM-DD"
        gender: "male" 或 "female"
        job_type: 女性需要区分 "worker" (工人) 或 "cadre" (干部)
    
    Returns:
        (退休年龄, 延迟月数)
    """
    birth = datetime.strptime(birth_date, "%Y-%m-%d")
    policy_key = "male" if gender == "male" else f"female_{job_type}"
    policy = RETIREMENT_POLICY[policy_key]
    
    transition_start = datetime.strptime(policy["transition_start"], "%Y-%m-%d")
    
    # 计算原退休日期
    original_retirement_year = birth.year + policy["base_age"]
    original_retirement_date = datetime(original_retirement_year, birth.month, 1)
    
    # 如果原退休日期在过渡期开始之前，不延迟
    if original_retirement_date <= transition_start:
        return policy["base_age"], 0
    
    # 计算过渡期经过的月数
    months_since_transition = (original_retirement_date.year - transition_start.year) * 12 + \
                              (original_retirement_date.month - transition_start.month)
    
    # 计算延迟月数
    if policy_key == "male" or policy_key == "female_cadre":
        # 每4个月延迟1个月
        delay_months = min(months_since_transition // 4, policy["transition_months"])
    else:  # female_worker
        # 每2个月延迟1个月
        delay_months = min(months_since_transition // 2, policy["transition_months"])
    
    retirement_age = policy["base_age"] + (delay_months / 12)
    
    return retirement_age, delay_months


def calculate_retirement_date(birth_date: str, gender: str, job_type: str = "worker") -> Dict:
    """
    计算退休日期
    
    Returns:
        包含退休日期详细信息的字典
    """
    birth = datetime.strptime(birth_date, "%Y-%m-%d")
    retirement_age, delay_months = calculate_retirement_age(birth_date, gender, job_type)
    
    # 计算退休日期
    retirement_year = birth.year + int(retirement_age)
    retirement_month = birth.month + int((retirement_age % 1) * 12)
    
    # 处理月份溢出
    if retirement_month > 12:
        retirement_year += retirement_month // 12
        retirement_month = retirement_month % 12
    
    retirement_date = datetime(retirement_year, retirement_month, 1)
    
    # 计算距离退休还有多少个月
    today = datetime.now()
    months_until_retirement = (retirement_year - today.year) * 12 + (retirement_month - today.month)
    
    return {
        "birth_date": birth_date,
        "gender": "男性" if gender == "male" else "女性",
        "job_type": "工人" if job_type == "worker" else "干部" if gender == "female" else "",
        "retirement_age": retirement_age,
        "delay_months": delay_months,
        "retirement_year": retirement_year,
        "retirement_month": retirement_month,
        "retirement_date": f"{retirement_year}年{retirement_month}月",
        "months_until_retirement": max(0, months_until_retirement),
        "years_until_retirement": round(max(0, months_until_retirement) / 12, 1),
    }


def calculate_social_insurance_employee(
    base: float,
    months_until_retirement: int,
    include_housing_fund: bool = True
) -> Dict:
    """
    计算职工社保缴费（有单位）
    """
    # 计算各项社保费用（个人缴纳部分）
    pension = base * EMPLOYEE_RATES["pension"]
    medical = base * EMPLOYEE_RATES["medical"]
    unemployment = base * EMPLOYEE_RATES["unemployment"]
    
    monthly_total = pension + medical + unemployment
    
    if include_housing_fund:
        housing_fund = base * EMPLOYEE_RATES["housing_fund"]
        monthly_total += housing_fund
    else:
        housing_fund = 0
    
    # 计算总额
    total = monthly_total * months_until_retirement
    
    return {
        "employment_type": "employee",
        "employment_type_name": "职工社保（单位代缴）",
        "monthly_payments": {
            "pension": round(pension, 2),
            "medical": round(medical, 2),
            "unemployment": round(unemployment, 2),
            "housing_fund": round(housing_fund, 2) if include_housing_fund else 0,
            "total": round(monthly_total, 2),
        },
        "total_payments": {
            "pension": round(pension * months_until_retirement, 2),
            "medical": round(medical * months_until_retirement, 2),
            "unemployment": round(unemployment * months_until_retirement, 2),
            "housing_fund": round(housing_fund * months_until_retirement, 2) if include_housing_fund else 0,
            "total": round(total, 2),
        },
    }


def calculate_social_insurance_flexible(
    base: float,
    city: str,
    months_until_retirement: int
) -> Dict:
    """
    计算灵活就业社保（无单位，自己缴纳）
    """
    # 获取该城市医疗保险比例
    medical_rate = CITY_FLEXIBLE_MEDICAL_RATES.get(city, CITY_FLEXIBLE_MEDICAL_RATES["其他城市"])
    
    # 计算各项社保费用（全部自己承担）
    pension = base * FLEXIBLE_RATES["pension"]  # 20%
    medical = base * medical_rate  # 各地不同，约6%-11%
    unemployment = 0  # 灵活就业没有失业保险
    housing_fund = 0  # 灵活就业一般没有公积金
    
    monthly_total = pension + medical
    
    # 计算总额
    total = monthly_total * months_until_retirement
    
    return {
        "employment_type": "flexible",
        "employment_type_name": "灵活就业（个人缴纳）",
        "monthly_payments": {
            "pension": round(pension, 2),
            "medical": round(medical, 2),
            "unemployment": 0,
            "housing_fund": 0,
            "total": round(monthly_total, 2),
        },
        "total_payments": {
            "pension": round(pension * months_until_retirement, 2),
            "medical": round(medical * months_until_retirement, 2),
            "unemployment": 0,
            "housing_fund": 0,
            "total": round(total, 2),
        },
        "notes": "灵活就业养老保险20%中只有8%进个人账户，12%进统筹账户",
    }


def calculate_social_insurance(
    monthly_salary: float,
    city: str,
    months_until_retirement: int,
    employment_type: str = "employee",
    include_housing_fund: bool = True
) -> Dict:
    """
    计算社保缴费总额
    
    Args:
        monthly_salary: 月工资（元）
        city: 城市名称
        months_until_retirement: 距离退休的月数
        employment_type: "employee" 职工社保 或 "flexible" 灵活就业
        include_housing_fund: 是否包含住房公积金（仅职工社保有效）
    
    Returns:
        社保缴费详情
    """
    # 获取城市缴费基数
    city_base = CITY_SOCIAL_INSURANCE_BASE.get(city, CITY_SOCIAL_INSURANCE_BASE["其他城市"])
    
    # 确定缴费基数（在上下限之间）
    base = max(city_base["min"], min(monthly_salary, city_base["max"]))
    
    # 根据就业类型计算
    if employment_type == "flexible":
        insurance_details = calculate_social_insurance_flexible(base, city, months_until_retirement)
    else:
        insurance_details = calculate_social_insurance_employee(base, months_until_retirement, include_housing_fund)
    
    return {
        "city": city,
        "monthly_salary": monthly_salary,
        "social_insurance_base": base,
        "months_until_retirement": months_until_retirement,
        "years_until_retirement": round(months_until_retirement / 12, 1),
        **insurance_details,
    }


def compare_employment_types(
    monthly_salary: float,
    city: str,
    months_until_retirement: int,
    include_housing_fund: bool = True
) -> Dict:
    """
    对比职工社保和灵活就业的缴费差异
    """
    employee = calculate_social_insurance(monthly_salary, city, months_until_retirement, "employee", include_housing_fund)
    flexible = calculate_social_insurance(monthly_salary, city, months_until_retirement, "flexible")
    
    employee_monthly = employee["monthly_payments"]["total"]
    flexible_monthly = flexible["monthly_payments"]["total"]
    employee_total = employee["total_payments"]["total"]
    flexible_total = flexible["total_payments"]["total"]
    
    return {
        "employee": employee,
        "flexible": flexible,
        "comparison": {
            "monthly_difference": round(flexible_monthly - employee_monthly, 2),
            "total_difference": round(flexible_total - employee_total, 2),
            "flexible_more_expensive_by": round((flexible_monthly / employee_monthly - 1) * 100, 1) if employee_monthly > 0 else 0,
        }
    }


def main():
    """主函数"""
    if len(sys.argv) < 5:
        print("Usage: python calculate_retirement.py <birth_date> <gender> <job_type> <monthly_salary> [city] [employment_type] [include_housing_fund]")
        print("")
        print("参数说明:")
        print("  birth_date:       出生日期，格式 YYYY-MM-DD，如 1985-06-15")
        print("  gender:           male 或 female")
        print("  job_type:         worker（工人）或 cadre（干部），女性需要填写")
        print("  monthly_salary:   月工资，如 15000")
        print("  city:             城市名称，如 北京、上海，默认为其他城市")
        print("  employment_type:  employee（职工社保）或 flexible（灵活就业），默认为 employee")
        print("  include_housing_fund: 是否含公积金，true 或 false，默认为 true")
        print("")
        print("示例:")
        print("  职工社保: python calculate_retirement.py 1985-06-15 male worker 15000 北京 employee true")
        print("  灵活就业: python calculate_retirement.py 1985-06-15 male worker 15000 北京 flexible")
        sys.exit(1)
    
    birth_date = sys.argv[1]
    gender = sys.argv[2]  # male or female
    job_type = sys.argv[3]  # worker or cadre
    monthly_salary = float(sys.argv[4])
    city = sys.argv[5] if len(sys.argv) > 5 else "其他城市"
    employment_type = sys.argv[6] if len(sys.argv) > 6 else "employee"
    include_housing_fund = sys.argv[7].lower() == "true" if len(sys.argv) > 7 else True
    
    # 计算退休信息
    retirement_info = calculate_retirement_date(birth_date, gender, job_type)
    
    # 计算社保
    insurance_info = calculate_social_insurance(
        monthly_salary,
        city,
        retirement_info["months_until_retirement"],
        employment_type,
        include_housing_fund
    )
    
    # 如果是对比模式，也计算另一种方式
    comparison = None
    if employment_type == "employee":
        flexible_info = calculate_social_insurance(
            monthly_salary, city, retirement_info["months_until_retirement"], "flexible"
        )
        comparison = {
            "flexible_alternative": flexible_info,
            "note": f"如选择灵活就业，每月需多缴 ¥{round(flexible_info['monthly_payments']['total'] - insurance_info['monthly_payments']['total'], 2)}，退休前总计多缴 ¥{round(flexible_info['total_payments']['total'] - insurance_info['total_payments']['total'], 2)}"
        }
    
    # 合并结果
    result = {
        "retirement": retirement_info,
        "social_insurance": insurance_info,
    }
    
    if comparison:
        result["comparison"] = comparison
    
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
