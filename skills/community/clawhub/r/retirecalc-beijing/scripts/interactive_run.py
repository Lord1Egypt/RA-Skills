#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TMP = ROOT / "tmp" / "interactive"


def ask(prompt: str, default: str | None = None) -> str:
    suffix = f" [{default}]" if default is not None else ""
    v = input(f"{prompt}{suffix}: ").strip()
    return v if v else (default or "")


def ask_bool(prompt: str, default: bool = False) -> bool:
    d = "y" if default else "n"
    v = ask(prompt + " (y/n)", d).lower()
    return v in {"y", "yes", "1", "是"}


def ask_float(prompt: str, default: float) -> float:
    return float(ask(prompt, str(default)))


def ask_int(prompt: str, default: int) -> int:
    return int(float(ask(prompt, str(default))))


def main() -> None:
    print("\n北京退休金测算（交互式）\n")

    name = ask("姓名", "")
    birth_date = ask("出生日期(YYYY-MM-DD)")
    category = ask("退休类别: male_60 / female_55 / female_50", "male_60")

    as_of = ask("测算时点(YYYY-MM-DD)", "2026-03-01")
    actual_months = ask_int("实际缴费月数", 180)
    deemed_months = ask_int("视同缴费月数", 0)
    pre98_months = ask_int("1998-07前实际缴费月数", 0)
    account_balance = ask_float("个人账户累计储存额", 120000)
    use_annual_records = ask_bool("是否通过历年缴费数据自动计算Z实指数", True)
    annual_records = []
    if use_annual_records:
        n = ask_int("录入年度条数（建议近5-10年）", 5)
        for i in range(n):
            print(f"\n第{i+1}条年度记录:")
            y = ask_int("  年份", 2025 - i)
            m = ask_int("  该年缴费月数", 12)
            b = ask_float("  该年月均缴费基数", 12000)
            um = ask_int("  该年领取失业金月数(无则0)", 0)
            annual_records.append(
                {
                    "year": y,
                    "months": m,
                    "avg_contribution_base_monthly": b,
                    "unemployment_benefit_months": um,
                }
            )
        z_actual = 1.0
    else:
        z_actual = ask_float("当前Z实指数(手动)", 1.0)
    unemployment_months = ask_int("历史领取失业金月数", 0)

    employment_type = ask("就业类型: employee / flexible", "employee")
    is_4050 = ask_bool("是否符合4050/灵活就业补贴资格", False)
    subsidy_used = ask_int("4050已享补贴月数", 0) if is_4050 else 0
    subsidy_ins = ["pension", "medical", "unemployment"] if is_4050 else ["pension", "medical", "unemployment"]

    auto_growth = ask_bool("社平工资增长率是否用最近10年加权自动估算", True)
    if auto_growth:
        assumptions = {
            "avg_wage_growth_method": "weighted10y",
            "personal_account_bookkeeping_rate": 0.03,
            "personal_contribution_rate": 0.08,
        }
    else:
        assumptions = {
            "avg_wage_growth_rate": ask_float("手动输入年增长率(如0.04)", 0.04),
            "personal_account_bookkeeping_rate": ask_float("个人账户记账利率", 0.03),
            "personal_contribution_rate": ask_float("个人账户计入比例", 0.08),
        }

    strategy_raw = ask("未来缴费指数方案(逗号分隔)", "0.6,1.0,1.5,2.0,3.0")
    strategy = [float(x.strip()) for x in strategy_raw.split(",") if x.strip()]

    payload = {
        "person": {
            "name": name,
            "birth_date": birth_date,
            "category": category,
        },
        "current": {
            "as_of": as_of,
            "actual_contribution_months": actual_months,
            "deemed_contribution_months": deemed_months,
            "actual_pre_1998_07_months": pre98_months,
            "personal_account_balance": account_balance,
            "z_actual": z_actual,
            "annual_contribution_records": annual_records,
            "unemployment_benefit_months": unemployment_months,
            "employment_type": employment_type,
            "is_4050_eligible": is_4050,
            "subsidy_already_used_months": subsidy_used,
            "subsidy_insurances": subsidy_ins,
        },
        "assumptions": assumptions,
        "optimization": {
            "strategy_contribution_indices": strategy,
        },
    }

    TMP.mkdir(parents=True, exist_ok=True)
    in_path = TMP / "interactive_input.json"
    out_path = TMP / "result.json"
    in_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    cmd = ["python3", str(ROOT / "scripts" / "calc_pension_beijing.py"), "--input", str(in_path)]
    result = subprocess.check_output(cmd, text=True)
    out_path.write_text(result, encoding="utf-8")

    print("\n已完成测算")
    print(f"输入文件: {in_path}")
    print(f"结果文件: {out_path}\n")
    print(result)


if __name__ == "__main__":
    main()
