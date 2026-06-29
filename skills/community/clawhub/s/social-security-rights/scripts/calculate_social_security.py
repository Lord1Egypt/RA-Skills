# 社保补缴金额计算工具
# 用于计算用人单位应补缴的社保费用及滞纳金

import argparse
import json
import os
from datetime import datetime, date

def parse_args():
    parser = argparse.ArgumentParser(description="社保补缴金额计算工具")
    parser.add_argument("--config", type=str, help="案件信息JSON文件路径")
    parser.add_argument("--output-dir", type=str, default=".", help="输出目录")
    parser.add_argument("--monthly-salary", type=float, help="月工资")
    parser.add_argument("--base-salary", type=float, default=None, help="社保缴费基数（如低于实际工资）")
    parser.add_argument("--start-date", type=str, help="应缴起始日期 YYYY-MM")
    parser.add_argument("--end-date", type=str, help="应缴结束日期 YYYY-MM")
    parser.add_argument("--city", type=str, default="北京", help="所在城市")
    parser.add_argument("--actual-base", type=float, default=None, help="用人单位实际缴纳基数（0表示未缴）")
    return parser.parse_args()

def load_config(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_city_rates(city):
    """各城市社保费率（单位+个人）"""
    rates = {
        "北京": {"pension_e": 0.16, "pension_p": 0.08, "medical_e": 0.09, "medical_p": 0.02,
                  "unemploy_e": 0.005, "unemploy_p": 0.005, "injury_e": 0.005, "maternity_e": 0.008},
        "上海": {"pension_e": 0.16, "pension_p": 0.08, "medical_e": 0.10, "medical_p": 0.02,
                  "unemploy_e": 0.005, "unemploy_p": 0.005, "injury_e": 0.003, "maternity_e": 0.01},
        "深圳": {"pension_e": 0.14, "pension_p": 0.08, "medical_e": 0.052, "medical_p": 0.02,
                  "unemploy_e": 0.007, "unemploy_p": 0.003, "injury_e": 0.003, "maternity_e": 0.0045},
        "广州": {"pension_e": 0.14, "pension_p": 0.08, "medical_e": 0.055, "medical_p": 0.02,
                  "unemploy_e": 0.008, "unemploy_p": 0.002, "injury_e": 0.005, "maternity_e": 0.0085},
        "杭州": {"pension_e": 0.14, "pension_p": 0.08, "medical_e": 0.099, "medical_p": 0.02,
                  "unemploy_e": 0.005, "unemploy_p": 0.005, "injury_e": 0.005, "maternity_e": 0.012},
    }
    return rates.get(city, rates["北京"])

def months_between(start, end):
    """计算月数差"""
    sy, sm = map(int, start.split("-"))
    ey, em = map(int, end.split("-"))
    return (ey - sy) * 12 + (em - sm) + 1

def calculate_late_fee(principal, days):
    """计算滞纳金：每日万分之五"""
    return principal * 0.0005 * days

def generate_report(config):
    city = config.get("city", "北京")
    salary = config["monthly_salary"]
    actual_base = config.get("actual_base", 0)
    should_base = config.get("base_salary", salary)
    start = config["start_date"]
    end = config["end_date"]
    
    rates = get_city_rates(city)
    months = months_between(start, end)
    
    today = date.today()
    end_date = datetime.strptime(end + "-01", "%Y-%m-%d").date()
    late_days = (today - end_date).days
    if late_days < 0:
        late_days = 0
    
    items = []
    total_employer = 0
    total_personal = 0
    total_late = 0
    
    rate_items = [
        ("养老保险", "pension_e", "pension_p"),
        ("医疗保险", "medical_e", "medical_p"),
        ("失业保险", "unemploy_e", "unemploy_p"),
        ("工伤保险", "injury_e", None),
        ("生育保险", "maternity_e", None),
    ]
    
    for name, e_key, p_key in rate_items:
        e_rate = rates[e_key]
        e_amount = (should_base - actual_base) * e_rate * months
        p_amount = 0
        if p_key:
            p_rate = rates[p_key]
            p_amount = (should_base - actual_base) * p_rate * months
        late_fee = calculate_late_fee(e_amount, late_days)
        
        items.append({
            "name": name,
            "employer_rate": f"{e_rate*100:.1f}%",
            "employer_amount": round(e_amount, 2),
            "personal_rate": f"{p_rate*100:.1f}%" if p_key else "0%",
            "personal_amount": round(p_amount, 2),
            "late_fee": round(late_fee, 2),
        })
        total_employer += e_amount
        total_personal += p_amount
        total_late += late_fee
    
    return {
        "city": city,
        "monthly_salary": salary,
        "should_base": should_base,
        "actual_base": actual_base,
        "start": start,
        "end": end,
        "months": months,
        "late_days": late_days,
        "items": items,
        "total_employer": round(total_employer, 2),
        "total_personal": round(total_personal, 2),
        "total_late": round(total_late, 2),
        "total_all": round(total_employer + total_personal + total_late, 2),
    }

def write_report(result, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    today = datetime.now().strftime("%Y年%m月%d日")
    
    md = f"""# 社保补缴金额计算表

所在地区：{result['city']}

生成日期：{today}

---

## 基础信息

| 项目 | 内容 |
|------|------|
| 月工资标准 | ¥{result['monthly_salary']:,.0f} |
| 应缴基数 | ¥{result['should_base']:,.0f} |
| 实际缴纳基数 | ¥{result['actual_base']:,.0f} |
| 应缴期间 | {result['start']} 至 {result['end']} |
| 欠缴月数 | {result['months']}个月 |
| 滞纳金计算天数 | {result['late_days']}天 |

## 各险种补缴明细

| 序号 | 险种 | 单位费率 | 单位应补(元) | 个人费率 | 个人应补(元) | 滞纳金(元) |
|------|------|---------|------------|---------|------------|-----------|
"""
    for i, item in enumerate(result["items"], 1):
        md += f"| {i} | {item['name']} | {item['employer_rate']} | {item['employer_amount']:,.2f} | {item['personal_rate']} | {item['personal_amount']:,.2f} | {item['late_fee']:,.2f} |\n"
    
    md += f"""| **合计** | | | **{result['total_employer']:,.2f}** | | **{result['total_personal']:,.2f}** | **{result['total_late']:,.2f}** |

## 补缴总金额

| 项目 | 金额(元) |
|------|---------|
| 用人单位应补 | {result['total_employer']:,.2f} |
| 个人应补 | {result['total_personal']:,.2f} |
| 滞纳金 | {result['total_late']:,.2f} |
| **合计** | **{result['total_all']:,.2f}** |

## 计算说明

1. **应缴基数**：职工上年度月平均工资，在社平工资60%-300%之间
2. **滞纳金**：按《社会保险法》第86条，每日万分之五
3. **工伤保险和生育保险**：由用人单位全额缴纳，个人不缴费
4. **实际缴纳金额以社保经办机构核定为准**

> **注意：** 以上计算基于参考费率，各地费率可能微调。实际补缴金额以当地社保经办机构核定为准。
"""
    
    path = os.path.join(output_dir, "社保补缴计算表.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"社保补缴计算表已生成：{path}")
    print(f"补缴总金额：¥{result['total_all']:,.2f}")

def main():
    args = parse_args()
    
    if args.config:
        config = load_config(args.config)
    else:
        config = {
            "monthly_salary": args.monthly_salary,
            "base_salary": args.base_salary or args.monthly_salary,
            "actual_base": args.actual_base or 0,
            "start_date": args.start_date,
            "end_date": args.end_date,
            "city": args.city,
        }
    
    result = generate_report(config)
    write_report(result, args.output_dir)

if __name__ == "__main__":
    main()
