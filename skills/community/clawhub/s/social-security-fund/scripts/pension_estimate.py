#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
退休金估算工具
根据缴费年限、缴费基数等参数，估算退休后每月可领取的养老金
"""

import argparse
import json
from city_rates import PENSION_PARAMS

def estimate_pension(
    years: int,
    avg_salary: float,
    local_avg_salary: float = 10000,
    personal_account_balance: float = None,
    retirement_age: int = 60
) -> dict:
    """
    估算退休金
    
    Args:
        years: 缴费年限
        avg_salary: 个人平均缴费工资
        local_avg_salary: 当地上年度社会平均工资
        personal_account_balance: 个人账户余额（None 则估算）
        retirement_age: 退休年龄
    
    Returns:
        估算结果字典
    """
    # 计发月数（根据退休年龄）
    if retirement_age <= 50:
        divisor = 195
    elif retirement_age <= 55:
        divisor = 170
    else:
        divisor = 139
    
    # 缴费指数
    contribution_index = avg_salary / local_avg_salary if local_avg_salary > 0 else 1
    
    # 基础养老金 = (当地社平工资 + 本人指数化工资) ÷ 2 × 缴费年限 × 1%
    indexed_salary = local_avg_salary * contribution_index
    base_pension = (local_avg_salary + indexed_salary) / 2 * years * PENSION_PARAMS["base_pension_rate"]
    
    # 个人账户养老金 = 个人账户余额 ÷ 计发月数
    if personal_account_balance is None:
        # 估算：假设按 8% 个人缴纳，年均增长 3%
        estimated_balance = avg_salary * 0.08 * 12 * years * 1.5  # 简化估算
        personal_account_balance = estimated_balance
    
    personal_pension = personal_account_balance / divisor
    
    # 总养老金
    total_pension = base_pension + personal_pension
    
    # 替代率（养老金/退休前工资）
    replacement_rate = total_pension / avg_salary if avg_salary > 0 else 0
    
    return {
        "years": years,
        "avg_salary": avg_salary,
        "local_avg_salary": local_avg_salary,
        "contribution_index": contribution_index,
        "personal_account_balance": personal_account_balance,
        "retirement_age": retirement_age,
        "pension": {
            "base": base_pension,
            "personal": personal_pension,
            "total": total_pension,
        },
        "replacement_rate": replacement_rate,
    }

def format_result(result: dict) -> str:
    """格式化输出结果"""
    lines = [
        f"👴 退休金估算结果",
        f"━━━━━━━━━━━━━━━━",
        f"📊 缴费年限：{result['years']} 年",
        f"💵 平均缴费工资：¥{result['avg_salary']:,.2f}",
        f"📍 当地社平工资：¥{result['local_avg_salary']:,.2f}",
        f"📈 缴费指数：{result['contribution_index']:.2f}",
        f"🏦 个人账户余额：¥{result['personal_account_balance']:,.2f}",
        f"🎂 退休年龄：{result['retirement_age']}岁",
        f"",
        f"💰 每月养老金：",
        f"   • 基础养老金：¥{result['pension']['base']:,.2f}",
        f"   • 个人账户养老金：¥{result['pension']['personal']:,.2f}",
        f"   ─────────────",
        f"   • 合计：¥{result['pension']['total']:,.2f}/月",
        f"",
        f"📉 养老金替代率：{result['replacement_rate']*100:.1f}%",
        f"",
        f"⚠️ 说明：",
        f"   • 以上结果为估算值，实际金额以社保局核算为准",
        f"   • 社平工资会逐年增长，实际养老金可能更高",
        f"   • 建议保持连续缴费，缴费年限越长养老金越高",
    ]
    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="退休金估算工具")
    parser.add_argument("--years", type=int, required=True, help="缴费年限")
    parser.add_argument("--avg-salary", type=float, required=True, help="平均缴费工资")
    parser.add_argument("--local-avg", type=float, default=10000, help="当地上年度社会平均工资")
    parser.add_argument("--balance", type=float, default=None, help="个人账户余额（可选）")
    parser.add_argument("--retirement-age", type=int, default=60, help="退休年龄")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")
    
    args = parser.parse_args()
    
    result = estimate_pension(
        args.years,
        args.avg_salary,
        args.local_avg,
        args.balance,
        args.retirement_age
    )
    
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(format_result(result))

if __name__ == "__main__":
    main()
