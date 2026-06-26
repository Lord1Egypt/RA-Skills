#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///

import argparse
import json
import math
import sys
from typing import Literal


def calculate_retirement_age(
    birth_year: int, birth_month: int, role: Literal["男性", "女职工", "女干部"]
) -> dict:
    """
    Calculate the year in which the person will reach the retirement age.

    Args:
        birth_year (int): The year of birth of the person.
        birth_month (int): The month of birth of the person.
        role (Literal["男性", "女职工", "女干部"]): The role of the person.

    Returns:
        dict: The year in which the person will reach the retirement age and retirement time.
    """
    print(
        f"Calculating retirement age for birth year: {birth_year}, birth month: {birth_month}, role: {role}"
    )
    if role == "男性":
        base_age = 60
        if birth_year < 1965:
            return {
                "retirement_time": f"{birth_year + 60}年{birth_month}月",
                "retirement_age": "60岁",
            }
        elif birth_year > 1976 or (birth_year == 1976 and birth_month >= 9):
            return {
                "retirement_time": f"{birth_year + 63}年{birth_month}月",
                "retirement_age": "63岁",
            }
        else:
            # 过渡期年龄计算
            delay_month = math.ceil(((birth_year - 1965) * 12 + birth_month) / 4)
            retirement_age_year = 60 + delay_month // 12
            retirement_age_month = delay_month % 12
            retirement_time_year = (
                birth_year
                + retirement_age_year
                + (retirement_age_month + birth_month) // 12
            )
            retirement_time_month = (retirement_age_month + birth_month) % 12

            return {
                "retirement_time": f"{retirement_time_year}年{retirement_time_month}月",
                "retirement_age": f"{retirement_age_year}岁{retirement_age_month}个月",
            }
    elif role == "女职工":
        retirement_age = 50
        if birth_year < 1975:
            return {
                "retirement_time": f"{birth_year + 50}年{birth_month}月",
                "retirement_age": "50岁",
            }
        elif birth_year > 1984 or (birth_year == 1984 and birth_month >= 11):
            return {
                "retirement_time": f"{birth_year + 55}年{birth_month}月",
                "retirement_age": "55岁",
            }
        else:
            # 过渡期年龄计算
            delay_month = math.ceil(((birth_year - 1975) * 12 + birth_month) / 2)
            retirement_age_year = 50 + delay_month // 12
            retirement_age_month = delay_month % 12
            retirement_time_year = (
                birth_year
                + retirement_age_year
                + (retirement_age_month + birth_month) // 12
            )
            retirement_time_month = (retirement_age_month + birth_month) % 12
            return {
                "retirement_time": f"{retirement_time_year}年{retirement_time_month}月",
                "retirement_age": f"{retirement_age_year}岁{retirement_age_month}个月",
            }

    elif role == "女干部":
        retirement_age = 55
        if birth_year < 1970:
            return {
                "retirement_time": f"{birth_year + 55}年{birth_month}月",
                "retirement_age": "55岁",
            }
        elif birth_year > 1981 or (birth_year == 1981 and birth_month >= 9):
            return {
                "retirement_time": f"{birth_year + 58}年{birth_month}月",
                "retirement_age": "58岁",
            }
        else:
            # 过渡期年龄计算
            delay_month = math.ceil(((birth_year - 1970) * 12 + birth_month) / 4)
            retirement_age_year = 55 + delay_month // 12
            retirement_age_month = delay_month % 12
            retirement_time_year = (
                birth_year
                + retirement_age_year
                + (retirement_age_month + birth_month) // 12
            )
            retirement_time_month = (retirement_age_month + birth_month) % 12
            return {
                "retirement_time": f"{retirement_time_year}年{retirement_time_month}月",
                "retirement_age": f"{retirement_age_year}岁{retirement_age_month}个月",
            }
    else:
        raise ValueError("Invalid role")


def main():
    parser = argparse.ArgumentParser(description="计算退休时间和退休年龄")
    parser.add_argument(
        "--birth-year", type=int, required=True, help="出生年份（如 1970）"
    )
    parser.add_argument(
        "--birth-month", type=int, required=True, help="出生月份（1-12）"
    )
    parser.add_argument(
        "--role",
        required=True,
        choices=["男性", "女职工", "女干部"],
        help="职位类型：男性、女职工、女干部",
    )

    args = parser.parse_args()

    # 验证月份
    if not 1 <= args.birth_month <= 12:
        print("错误：出生月份必须在 1-12 之间", file=sys.stderr)
        sys.exit(1)

    # 验证年份
    if args.birth_year < 1900 or args.birth_year > 2100:
        print("错误：出生年份必须在 1900-2100 之间", file=sys.stderr)
        sys.exit(1)

    try:
        result = calculate_retirement_age(
            args.birth_year, args.birth_month, args.role
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except ValueError as e:
        print(f"错误：{e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()