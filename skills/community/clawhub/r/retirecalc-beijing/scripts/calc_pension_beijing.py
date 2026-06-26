#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
from typing import Dict, List, Tuple

from retirement_age import calculate_retirement_date


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def round2(x: float) -> float:
    return round(float(x), 2)


def year_month_start(d: dt.date) -> dt.date:
    return dt.date(d.year, d.month, 1)


def month_diff(a: dt.date, b: dt.date) -> int:
    return (b.year - a.year) * 12 + (b.month - a.month)


def add_months(d: dt.date, months: int) -> dt.date:
    y = d.year + (d.month - 1 + months) // 12
    m = (d.month - 1 + months) % 12 + 1
    day = min(d.day, [31, 29 if y % 4 == 0 and (y % 100 != 0 or y % 400 == 0) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][m - 1])
    return dt.date(y, m, day)


def min_required_contrib_months(retire_date: dt.date) -> int:
    if retire_date < dt.date(2030, 1, 1):
        return 180
    years_from_2030 = retire_date.year - 2030
    return 180 + min(60, (years_from_2030 + 1) * 6)


def projected_value_by_year(series: Dict[str, float], year: int, growth: float) -> float:
    available = sorted(int(y) for y in series.keys())
    if str(year) in series:
        return float(series[str(year)])
    last_year = available[-1]
    last_val = float(series[str(last_year)])
    if year < available[0]:
        first_year = available[0]
        first_val = float(series[str(first_year)])
        return first_val / ((1 + growth) ** (first_year - year))
    return last_val * ((1 + growth) ** (year - last_year))


def parse_period_key(key: str) -> Tuple[dt.date, dt.date]:
    # format: YYYY.MM-YYYY.MM
    left, right = key.split("-")
    y1, m1 = [int(x) for x in left.split(".")]
    y2, m2 = [int(x) for x in right.split(".")]
    return dt.date(y1, m1, 1), dt.date(y2, m2, 1)


def get_period_scalar_value(
    series_by_period: Dict[str, float],
    d: dt.date,
) -> float | None:
    if not series_by_period:
        return None
    cur = dt.date(d.year, d.month, 1)
    for k, v in series_by_period.items():
        try:
            start, end = parse_period_key(k)
        except Exception:
            continue
        if start <= cur <= end:
            return float(v)
    return None


def get_period_limits_value(
    limits_by_period: Dict[str, Dict[str, float]],
    d: dt.date,
) -> Tuple[float, float] | None:
    if not limits_by_period:
        return None
    cur = dt.date(d.year, d.month, 1)
    for k, v in limits_by_period.items():
        try:
            start, end = parse_period_key(k)
        except Exception:
            continue
        if start <= cur <= end:
            return float(v["lower"]), float(v["upper"])
    return None


def compute_z_actual_from_records(
    records: List[dict],
    avg_wage_monthly_series: Dict[str, float],
) -> float | None:
    """
    Compute Z实指数 from annual contribution records.
    Beijing formula denominator uses previous-year city average wage.
    """
    if not records:
        return None

    total_months = 0.0
    weighted_ratio_sum = 0.0

    for r in records:
        year = int(r["year"])
        months = float(r.get("months", 12))
        unemp_months = float(r.get("unemployment_benefit_months", 0))
        eff_months = max(0.0, months - unemp_months)
        if eff_months <= 0:
            continue

        avg_base = float(r["avg_contribution_base_monthly"])
        prev_year = year - 1
        if str(prev_year) in avg_wage_monthly_series:
            wage_ref = float(avg_wage_monthly_series[str(prev_year)])
        elif str(year) in avg_wage_monthly_series:
            wage_ref = float(avg_wage_monthly_series[str(year)])
        else:
            # fallback for sparse history
            wage_ref = projected_value_by_year(avg_wage_monthly_series, prev_year, 0.04)

        if wage_ref <= 0:
            continue

        ratio = avg_base / wage_ref
        weighted_ratio_sum += ratio * eff_months
        total_months += eff_months

    if total_months <= 0:
        return None
    return weighted_ratio_sum / total_months


def estimate_weighted_growth_rate(series: Dict[str, float], as_of_year: int, window_years: int = 10) -> float:
    years = sorted(int(y) for y in series.keys() if int(y) <= as_of_year - 1)
    if len(years) < 2:
        return 0.04

    selected = years[-(window_years + 1) :]
    growths = []
    for i in range(1, len(selected)):
        y_prev = selected[i - 1]
        y_cur = selected[i]
        v_prev = float(series[str(y_prev)])
        v_cur = float(series[str(y_cur)])
        if v_prev > 0:
            growths.append(v_cur / v_prev - 1.0)

    if not growths:
        return 0.04

    # 线性加权：越近年份权重越高
    weights = list(range(1, len(growths) + 1))
    s_w = sum(weights)
    weighted = sum(g * w for g, w in zip(growths, weights)) / s_w
    return max(-0.05, min(0.12, weighted))


def projected_limits_by_year(limits: Dict[str, Dict[str, float]], year: int, growth: float) -> Tuple[float, float]:
    if str(year) in limits:
        v = limits[str(year)]
        return float(v["lower"]), float(v["upper"])

    years = sorted(int(y) for y in limits.keys())
    last_year = years[-1]
    v = limits[str(last_year)]
    factor = (1 + growth) ** (year - last_year)
    return float(v["lower"]) * factor, float(v["upper"]) * factor


def payout_months_for_age(payout_table: Dict[str, int], age_years: int) -> int:
    min_age = min(int(k) for k in payout_table)
    max_age = max(int(k) for k in payout_table)
    age = max(min_age, min(max_age, age_years))
    return int(payout_table[str(age)])


def pension_components(
    c_ping: float,
    z_actual: float,
    actual_months: int,
    deemed_months: int,
    actual_pre_1998_months: int,
    account_balance: float,
    payout_months: int,
) -> Dict[str, float]:
    n_total_years = (actual_months + deemed_months) / 12.0
    n_same_years = deemed_months / 12.0
    n_actual98_years = actual_pre_1998_months / 12.0

    basic = ((c_ping + c_ping * z_actual) / 2.0) * n_total_years * 0.01
    account = account_balance / payout_months
    transitional = c_ping * n_same_years * 0.01 + c_ping * z_actual * n_actual98_years * 0.01

    return {
        "basic_pension": round2(basic),
        "account_pension": round2(account),
        "transitional_pension": round2(transitional),
        "total_pension": round2(basic + account + transitional),
    }


def simulate_balance(
    start_balance: float,
    start_date: dt.date,
    retire_date: dt.date,
    contribution_index: float,
    account_credit_rate: float,
    annual_book_rate: float,
    pension_base_by_year: Dict[str, float],
    pension_base_by_period: Dict[str, float],
    limits_by_year: Dict[str, Dict[str, float]],
    limits_by_period: Dict[str, Dict[str, float]],
    medical_fixed_by_year: Dict[str, float],
    avg_wage_growth: float,
    employment_type: str,
    pay_pension_rate_employee: float,
    pay_pension_rate_flexible: float,
    pay_unemployment_rate_flexible: float,
    is_4050_eligible: bool,
    subsidy_insurances: List[str],
    subsidy_standard_monthly: Dict[str, float],
    subsidy_already_used_months: int,
) -> Dict[str, float]:
    balance = float(start_balance)
    current = year_month_start(start_date)
    end = year_month_start(retire_date)
    months = month_diff(current, end)
    monthly_rate = annual_book_rate / 12.0
    months = max(0, months)

    total_account_credit = 0.0
    total_gross = 0.0
    total_subsidy = 0.0

    # 4050补贴累计可享期限：一般3年；距法定退休年龄不足5年的可到5年
    subsidy_cap = 60 if months <= 60 else 36
    subsidy_remain = max(0, subsidy_cap - subsidy_already_used_months)

    for i in range(months):
        m = add_months(current, i)
        avg_wage = get_period_scalar_value(pension_base_by_period, m)
        if avg_wage is None:
            avg_wage = projected_value_by_year(pension_base_by_year, m.year, avg_wage_growth)

        limits = get_period_limits_value(limits_by_period, m)
        if limits is None:
            lower, upper = projected_limits_by_year(limits_by_year, m.year, avg_wage_growth)
        else:
            lower, upper = limits
        pay_base = max(lower, min(upper, avg_wage * contribution_index))
        medical_fixed = projected_value_by_year(medical_fixed_by_year, m.year, avg_wage_growth)

        account_credit = pay_base * account_credit_rate
        balance = balance * (1 + monthly_rate) + account_credit
        total_account_credit += account_credit

        if employment_type == "flexible":
            gross_pension = pay_base * pay_pension_rate_flexible
            gross_unemployment = pay_base * pay_unemployment_rate_flexible
            gross_medical = medical_fixed
        else:
            gross_pension = pay_base * pay_pension_rate_employee
            gross_unemployment = 0.0
            gross_medical = 0.0

        month_gross = gross_pension + gross_unemployment + gross_medical
        month_subsidy = 0.0

        can_subsidy = employment_type == "flexible" and is_4050_eligible and i < subsidy_remain
        if can_subsidy:
            if "pension" in subsidy_insurances:
                month_subsidy += min(gross_pension, float(subsidy_standard_monthly.get("pension", 0.0)))
            if "unemployment" in subsidy_insurances:
                month_subsidy += min(gross_unemployment, float(subsidy_standard_monthly.get("unemployment", 0.0)))
            if "medical" in subsidy_insurances:
                month_subsidy += min(gross_medical, float(subsidy_standard_monthly.get("medical", 0.0)))

        total_gross += month_gross
        total_subsidy += month_subsidy

    return {
        "balance": balance,
        "future_months": months,
        "future_account_credit_total": total_account_credit,
        "future_gross_contribution_total": total_gross,
        "future_subsidy_total": total_subsidy,
        "future_net_contribution_total": max(0.0, total_gross - total_subsidy),
        "subsidy_month_cap": subsidy_cap,
        "subsidy_months_used_in_projection": min(months, subsidy_remain) if (employment_type == "flexible" and is_4050_eligible) else 0,
    }


def parse_input(data: dict) -> dict:
    if "payload" in data and isinstance(data["payload"], dict):
        data = data["payload"]

    person = data["person"]
    current = data["current"]

    birth_date = dt.date.fromisoformat(person["birth_date"])
    as_of = dt.date.fromisoformat(current["as_of"])

    annual_records = current.get("annual_contribution_records", [])

    return {
        "name": person.get("name", ""),
        "category": person["category"],
        "birth_date": birth_date,
        "as_of": as_of,
        "actual_months": int(current["actual_contribution_months"]),
        "deemed_months": int(current.get("deemed_contribution_months", 0)),
        "actual_pre_1998_months": int(current.get("actual_pre_1998_07_months", 0)),
        "account_balance": float(current["personal_account_balance"]),
        "z_actual": float(current.get("z_actual", 1.0)),
        "annual_contribution_records": list(annual_records) if isinstance(annual_records, list) else [],
        "unemployment_benefit_months": int(current.get("unemployment_benefit_months", 0)),
        "employment_type": str(current.get("employment_type", "employee")),
        "is_4050_eligible": bool(current.get("is_4050_eligible", False)),
        "subsidy_already_used_months": int(current.get("subsidy_already_used_months", 0)),
        "subsidy_insurances": current.get("subsidy_insurances", ["pension", "medical", "unemployment"]),
        "optimization": data.get("optimization", {}),
        "assumptions": data.get("assumptions", {}),
    }


def build_strategy_result(
    strategy_index: float,
    parsed: dict,
    params: dict,
    retire: dict,
) -> dict:
    assumptions = parsed["assumptions"]
    defaults = params["defaults"]

    avg_wage_series = params.get("avg_wage_monthly_for_index_by_year", params["pension_base_by_year"])
    growth_method = str(assumptions.get("avg_wage_growth_method", "")).strip().lower()
    if "avg_wage_growth_rate" in assumptions:
        avg_growth = float(assumptions["avg_wage_growth_rate"])
    elif growth_method == "weighted10y":
        avg_growth = estimate_weighted_growth_rate(avg_wage_series, parsed["as_of"].year, 10)
    else:
        avg_growth = float(defaults["avg_wage_growth_rate"])

    book_rate = float(assumptions.get("personal_account_bookkeeping_rate", defaults["personal_account_bookkeeping_rate"]))
    account_credit_rate = float(assumptions.get("personal_contribution_rate", defaults["personal_contribution_rate"]))
    pay_pension_rate_employee = float(defaults.get("employee_pension_payment_rate", 0.08))
    pay_pension_rate_flexible = float(defaults.get("flexible_pension_payment_rate", 0.20))
    pay_unemployment_rate_flexible = float(defaults.get("flexible_unemployment_payment_rate", 0.01))

    index_floor = float(defaults["contribution_index_floor"])
    index_ceil = float(defaults["contribution_index_ceil"])
    idx = max(index_floor, min(index_ceil, strategy_index))

    legal_retire_date = dt.date.fromisoformat(retire["legal_retirement_date"])
    as_of = parsed["as_of"]

    sim = simulate_balance(
        start_balance=parsed["account_balance"],
        start_date=as_of,
        retire_date=legal_retire_date,
        contribution_index=idx,
        account_credit_rate=account_credit_rate,
        annual_book_rate=book_rate,
        pension_base_by_year=avg_wage_series,
        pension_base_by_period=params.get("avg_wage_full_caliber_monthly_by_period", {}),
        limits_by_year=params["contribution_limits_by_year"],
        limits_by_period=params.get("contribution_limits_by_period", {}),
        medical_fixed_by_year=params.get("flexible_medical_fixed_by_year", {"2025": 584.92}),
        avg_wage_growth=avg_growth,
        employment_type=parsed["employment_type"],
        pay_pension_rate_employee=pay_pension_rate_employee,
        pay_pension_rate_flexible=pay_pension_rate_flexible,
        pay_unemployment_rate_flexible=pay_unemployment_rate_flexible,
        is_4050_eligible=parsed["is_4050_eligible"],
        subsidy_insurances=list(parsed["subsidy_insurances"] or []),
        subsidy_standard_monthly=params.get(
            "flexible_subsidy_standard_monthly",
            {"pension": 843.47, "medical": 369.04, "unemployment": 42.17},
        ),
        subsidy_already_used_months=parsed["subsidy_already_used_months"],
    )
    future_balance = sim["balance"]
    future_months = int(sim["future_months"])

    z_initial = parsed["z_actual"]
    z_auto = compute_z_actual_from_records(parsed.get("annual_contribution_records", []), avg_wage_series)
    if z_auto is not None:
        z_initial = z_auto

    current_effective_months = max(1, parsed["actual_months"] - parsed["unemployment_benefit_months"])
    z_final = (
        z_initial * current_effective_months + idx * future_months
    ) / max(1, current_effective_months + future_months)

    actual_months_final = parsed["actual_months"] + future_months
    deemed_months_final = parsed["deemed_months"]
    pre_1998_final = parsed["actual_pre_1998_months"]

    retire_year = legal_retire_date.year
    c_ping = projected_value_by_year(params["pension_base_by_year"], retire_year, avg_growth)

    age_years = retire["legal_retirement_age_years"]
    payout_months = payout_months_for_age(params["account_payout_months_by_age"], age_years)

    comp = pension_components(
        c_ping=c_ping,
        z_actual=z_final,
        actual_months=actual_months_final,
        deemed_months=deemed_months_final,
        actual_pre_1998_months=pre_1998_final,
        account_balance=future_balance,
        payout_months=payout_months,
    )

    min_required = min_required_contrib_months(legal_retire_date)
    has_min_years = (actual_months_final + deemed_months_final) >= min_required

    return {
        "strategy_contribution_index": idx,
        "retirement_date": retire["legal_retirement_date"],
        "retirement_age": f"{retire['legal_retirement_age_years']}岁{retire['legal_retirement_age_extra_months']}个月",
        "pension_base_used": round2(c_ping),
        "z_actual_estimated": round2(z_final),
        "z_actual_source": "annual_records_auto" if z_auto is not None else "manual_input",
        "z_actual_initial_used": round2(z_initial),
        "actual_contribution_months": actual_months_final,
        "deemed_contribution_months": deemed_months_final,
        "minimum_required_contribution_months": min_required,
        "meets_minimum_contribution_requirement": has_min_years,
        "personal_account_balance_at_retirement": round2(future_balance),
        "future_investment_summary": {
            "employment_type": parsed["employment_type"],
            "is_4050_eligible": parsed["is_4050_eligible"],
            "subsidy_insurances": list(parsed["subsidy_insurances"] or []),
            "subsidy_month_cap": int(sim["subsidy_month_cap"]),
            "subsidy_months_used_in_projection": int(sim["subsidy_months_used_in_projection"]),
            "future_account_credit_total": round2(sim["future_account_credit_total"]),
            "future_gross_contribution_total": round2(sim["future_gross_contribution_total"]),
            "future_subsidy_total": round2(sim["future_subsidy_total"]),
            "future_net_contribution_total": round2(sim["future_net_contribution_total"]),
        },
        "assumption_used": {
            "avg_wage_growth_rate": round2(avg_growth),
            "avg_wage_growth_method": growth_method if growth_method else "manual_or_default",
        },
        "account_payout_months": payout_months,
        "monthly_pension_components": comp,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Beijing pension calculator with strategy optimization.")
    parser.add_argument("--input", required=True, help="Path to input JSON")
    parser.add_argument(
        "--params",
        default=str(Path(__file__).resolve().parents[1] / "data" / "beijing_params.json"),
        help="Path to parameter JSON",
    )
    args = parser.parse_args()

    data = load_json(Path(args.input))
    params = load_json(Path(args.params))
    parsed = parse_input(data)

    retire = calculate_retirement_date(parsed["birth_date"], parsed["category"])

    optimization = parsed["optimization"]
    strategy_list: List[float] = optimization.get("strategy_contribution_indices", [parsed["z_actual"]])

    results = [build_strategy_result(x, parsed, params, retire) for x in strategy_list]
    results.sort(key=lambda r: r["monthly_pension_components"]["total_pension"], reverse=True)

    output = {
        "person": {
            "name": parsed["name"],
            "birth_date": parsed["birth_date"].isoformat(),
            "category": parsed["category"],
            "as_of": parsed["as_of"].isoformat(),
        },
        "policy_retirement": retire,
        "calculation_note": {
            "unemployment_rule": "按京劳社养发〔2007〕29号：领失业金期间停止缴纳养老保险费，且计算Z实指数时扣除该期间。",
            "flexible_4050_rule": "灵活就业社保补贴按“先缴后补，不缴不补”并按险种核算，金额不超过最低缴费额的2/3（当前采用公开标准：养老843.47、医疗369.04、失业42.17元/月）。",
            "projection_note": "超过已公布年份的养老金计算基数和缴费上下限按假设增长率外推。",
        },
        "best_strategy": results[0],
        "all_strategies": results,
    }

    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
