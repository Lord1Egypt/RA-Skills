#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def round2(v: float) -> float:
    return round(float(v), 2)


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, obj: dict) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
        f.write("\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Update Beijing parameter file by year.")
    parser.add_argument("--params", default=str(Path(__file__).resolve().parents[1] / "data" / "beijing_params.json"))
    parser.add_argument("--year", type=int, required=True)

    parser.add_argument("--pension-base", type=float, help="养老金待遇计算基数（月）")
    parser.add_argument("--contrib-lower", type=float, help="缴费基数下限（月）")
    parser.add_argument("--contrib-upper", type=float, help="缴费基数上限（月）")
    parser.add_argument("--full-caliber-monthly", type=float, help="全口径城镇单位就业人员月平均工资")

    parser.add_argument("--flex-medical-fixed", type=float, help="灵活就业医保月固定额")
    parser.add_argument("--subsidy-pension", type=float, help="灵活就业补贴-养老")
    parser.add_argument("--subsidy-medical", type=float, help="灵活就业补贴-医疗")
    parser.add_argument("--subsidy-unemployment", type=float, help="灵活就业补贴-失业")

    parser.add_argument("--derive-full-caliber-from-lower", action="store_true", default=True)

    args = parser.parse_args()

    params_path = Path(args.params)
    obj = load_json(params_path)
    y = str(args.year)

    if args.pension_base is not None:
        obj.setdefault("pension_base_by_year", {})[y] = round2(args.pension_base)

    if args.contrib_lower is not None or args.contrib_upper is not None:
        obj.setdefault("contribution_limits_by_year", {})
        cur = obj["contribution_limits_by_year"].get(y, {})
        if args.contrib_lower is not None:
            cur["lower"] = round2(args.contrib_lower)
        if args.contrib_upper is not None:
            cur["upper"] = round2(args.contrib_upper)
        obj["contribution_limits_by_year"][y] = cur

    full_caliber = args.full_caliber_monthly
    if full_caliber is None and args.derive_full_caliber_from_lower and args.contrib_lower is not None:
        # 北京常用口径：下限=全口径月均*60%
        full_caliber = args.contrib_lower / 0.6

    if full_caliber is not None:
        full_caliber = round2(full_caliber)
        obj.setdefault("avg_wage_full_caliber_monthly_by_year", {})[y] = full_caliber
        obj.setdefault("avg_wage_monthly_for_index_by_year", {})[y] = full_caliber

    if args.flex_medical_fixed is not None:
        obj.setdefault("flexible_medical_fixed_by_year", {})[y] = round2(args.flex_medical_fixed)

    if args.subsidy_pension is not None:
        obj.setdefault("flexible_subsidy_standard_monthly", {})["pension"] = round2(args.subsidy_pension)
    if args.subsidy_medical is not None:
        obj.setdefault("flexible_subsidy_standard_monthly", {})["medical"] = round2(args.subsidy_medical)
    if args.subsidy_unemployment is not None:
        obj.setdefault("flexible_subsidy_standard_monthly", {})["unemployment"] = round2(args.subsidy_unemployment)

    obj.setdefault("metadata", {})["version"] = "2026-03-22"

    save_json(params_path, obj)

    print(json.dumps({
        "ok": True,
        "params": str(params_path),
        "year": args.year,
        "updated": {
            "pension_base": args.pension_base,
            "contrib_lower": args.contrib_lower,
            "contrib_upper": args.contrib_upper,
            "full_caliber_monthly": full_caliber,
            "flex_medical_fixed": args.flex_medical_fixed,
            "subsidy_pension": args.subsidy_pension,
            "subsidy_medical": args.subsidy_medical,
            "subsidy_unemployment": args.subsidy_unemployment,
        }
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
