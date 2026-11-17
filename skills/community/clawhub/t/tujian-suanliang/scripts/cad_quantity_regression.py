#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""算量回归比对：把统一报告与锁定基线逐键对账，量值一变就报错。

用途：改算法或并新证据脚本后，证明混凝土量、面积、计数没有漂。
只比标量叶节点（数值/字符串/布尔），默认忽略标题和时间戳；
数值用容差比较，其余必须全等。基线留在项目目录，不进技能发布包。
"""
from __future__ import annotations

try:
    import os as _boot_os, sys as _boot_sys
    _boot_sys.path.insert(0, _boot_os.path.dirname(_boot_os.path.abspath(__file__)))
    import pyboot as _boot_pyboot
    _boot_pyboot.ensure_utf8_io()
except Exception:
    pass



import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

SCHEMA = "cad-quantity-regression/v0.1"
DEFAULT_IGNORE = (r"(^|\.)title$|(^|\.)generated(_at)?$|(^|\.)timestamp$|"
                  r"(^|\.)updated_at$")
QUANTITY_KEY = re.compile(r"_m3$|_m2$|_count$|_ratio$|volume|area|total")


def flatten(value: Any, prefix: str = "") -> dict[str, Any]:
    out: dict[str, Any] = {}
    if isinstance(value, dict):
        for key, item in value.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            out.update(flatten(item, path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            out.update(flatten(item, f"{prefix}[{index}]"))
    else:
        out[prefix] = value
    return out


def comparable(leaves: dict[str, Any], ignore: re.Pattern,
               quantities_only: bool) -> dict[str, Any]:
    return {
        key: value for key, value in leaves.items()
        if not ignore.search(key)
        and (not quantities_only or bool(QUANTITY_KEY.search(key)))
    }


def compare(baseline: dict[str, Any], current: dict[str, Any],
            tolerance: float, ignore: re.Pattern,
            quantities_only: bool) -> dict[str, Any]:
    base = comparable(baseline, ignore, quantities_only)
    cur = comparable(current, ignore, quantities_only)
    drift: list[dict[str, Any]] = []
    missing: list[str] = []
    added: list[str] = []
    for key, value in base.items():
        if key not in cur:
            missing.append(key)
            continue
        new = cur[key]
        if isinstance(value, bool) or isinstance(new, bool):
            same = value == new
        elif isinstance(value, (int, float)) and isinstance(new, (int, float)):
            same = abs(float(value) - float(new)) <= tolerance
        else:
            same = value == new
        if not same:
            drift.append({"key": key, "baseline": value, "current": new})
    added = sorted(set(cur) - set(base))
    numeric_drift = [row for row in drift
                     if isinstance(row["baseline"], (int, float))
                     and not isinstance(row["baseline"], bool)]
    quantity_drift = [row for row in drift
                      if QUANTITY_KEY.search(row["key"])]
    return {
        "schema": SCHEMA,
        "compared_keys": len(base),
        "tolerance": tolerance,
        "quantities_only": quantities_only,
        "drift": sorted(drift, key=lambda row: row["key"]),
        "missing_keys": sorted(missing),
        "added_keys": added,
        "summary": {
            "drift_count": len(drift),
            "numeric_drift_count": len(numeric_drift),
            "quantity_drift_count": len(quantity_drift),
            "missing_count": len(missing),
            "added_count": len(added),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", required=True, help="锁定的基线报告 JSON")
    parser.add_argument("--report", required=True, help="本轮统一报告 JSON")
    parser.add_argument("--tolerance", type=float, default=1e-6,
                        help="数值容差，默认 1e-6")
    parser.add_argument("--quantities-only", action="store_true",
                        help="只比量值/计数/占比键")
    parser.add_argument("--ignore", default=DEFAULT_IGNORE,
                        help="忽略键的正则（作用在扁平化键路径上）")
    parser.add_argument("--update-baseline", action="store_true",
                        help="把本轮报告写成新基线（覆盖 --baseline 路径）")
    parser.add_argument("-o", "--output", help="比对结果 JSON")
    args = parser.parse_args()

    baseline_path = Path(args.baseline).expanduser().resolve()
    report_path = Path(args.report).expanduser().resolve()
    for path in (baseline_path, report_path):
        if not path.exists():
            print(f"文件不存在：{path}", file=sys.stderr)
            return 2
    if args.update_baseline:
        baseline_path.write_text(
            report_path.read_text(encoding="utf-8"), encoding="utf-8")
        print(f"已写入基线 {baseline_path}")
        return 0

    ignore = re.compile(args.ignore)
    result = compare(
        flatten(json.loads(baseline_path.read_text(encoding="utf-8"))),
        flatten(json.loads(report_path.read_text(encoding="utf-8"))),
        args.tolerance, ignore, args.quantities_only)
    result["baseline"] = str(baseline_path)
    result["report"] = str(report_path)
    verdict = not result["drift"] and not result["missing_keys"]
    if args.ignore != DEFAULT_IGNORE:
        verdict = verdict  # 自定义忽略只影响比较范围，不改判定口径
    result["verdict"] = "pass" if verdict else "fail"
    text = json.dumps(result, ensure_ascii=False, indent=1)
    if args.output:
        out = Path(args.output).expanduser().resolve()
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
    for row in result["drift"][:20]:
        print("漂移 %s: %s -> %s" % (row["key"], row["baseline"], row["current"]))
    for key in result["missing_keys"][:20]:
        print("基线键消失 %s" % key)
    print("回归判定 %s：比对 %d 键，漂移 %d（量值 %d），缺键 %d，新增 %d" % (
        result["verdict"], result["compared_keys"],
        result["summary"]["drift_count"],
        result["summary"]["quantity_drift_count"],
        result["summary"]["missing_count"], result["summary"]["added_count"]))
    return 0 if verdict else 1


if __name__ == "__main__":
    sys.exit(main())
