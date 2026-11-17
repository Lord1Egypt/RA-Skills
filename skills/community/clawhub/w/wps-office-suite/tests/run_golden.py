#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NL2Formula 黄金集回归脚本 v5.5.0
==================================
逐条跑 tests/golden_formula.json 基准，断言 NL2Formula.convert() 返回的公式
包含预期关键子串，统计准确率。CI 可据退出码判定是否达标（默认阈值 85%）。

用法：
    python tests/run_golden.py                 # 跑全部，阈值 85%
    python tests/run_golden.py --threshold 0.9 # 自定义阈值
    python tests/run_golden.py --json          # JSON 输出（供流水线解析）

死规则合规：规则9 纯本地、规则14 自审数据、规则15 沙箱可跑。
"""
import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPTS = HERE.parent / "scripts"
sys.path.insert(0, str(SCRIPTS))


def load_golden():
    with (HERE / "golden_formula.json").open(encoding="utf-8") as f:
        return json.load(f)


def run(threshold: float = 0.85) -> dict:
    golden = load_golden()
    cases = golden.get("cases", [])
    try:
        from excel_analyzer import NL2Formula
        converter = NL2Formula()
    except Exception as e:
        return {"ok": False, "error": f"无法导入 NL2Formula: {e}", "accuracy": 0.0}

    passed, failed = [], []
    for case in cases:
        cid = case["id"]
        query = case["query"]
        expect = case["expect"]
        try:
            result = converter.convert(query)
            formula = str(result.get("formula", "")) if result.get("success") else ""
            hit = expect.lower() in formula.lower()
        except Exception as e:
            formula, hit = f"<异常: {e}>", False
        rec = {"id": cid, "query": query, "expect": expect,
               "formula": formula, "pass": hit}
        (passed if hit else failed).append(rec)

    total = len(cases)
    accuracy = round(len(passed) / total, 4) if total else 0.0
    return {
        "ok": accuracy >= threshold,
        "total": total,
        "passed": len(passed),
        "failed": len(failed),
        "accuracy": accuracy,
        "accuracy_pct": f"{accuracy * 100:.1f}%",
        "threshold": threshold,
        "failed_cases": failed,
        "golden_version": golden.get("version"),
    }


def main():
    ap = argparse.ArgumentParser(description="NL2Formula 黄金集回归 v5.5.0")
    ap.add_argument("--threshold", type=float, default=0.85, help="准确率阈值（默认 0.85）")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    args = ap.parse_args()

    r = run(args.threshold)
    if args.json:
        print(json.dumps(r, ensure_ascii=False, default=str))
    else:
        print("=" * 56)
        print("NL2Formula 黄金集回归 v5.5.0")
        print("=" * 56)
        print(f"基准总数 : {r.get('total')}")
        print(f"通过     : {r.get('passed')}")
        print(f"失败     : {r.get('failed')}")
        print(f"准确率   : {r.get('accuracy_pct')}  (阈值 {args.threshold * 100:.0f}%)")
        print(f"金集版本 : {r.get('golden_version')}")
        if r.get("failed_cases"):
            print("-" * 56)
            print("失败明细:")
            for c in r["failed_cases"]:
                print(f"  [{c['id']}] {c['query']}  expect={c['expect']}  got={c['formula']}")
        print("=" * 56)
        print("结论:", "达标 ✅" if r.get("ok") else "未达标 ❌")
    sys.exit(0 if r.get("ok") else 1)


if __name__ == "__main__":
    main()
