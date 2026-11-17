"""确定性算术核对规则（ID 稳定，见任务卡）。

只产出「疑点 + 期望值 + 实际值 + 证据 handle」，不判定"设计错误"。
"""
from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Optional

DEFAULT_UNIT_WEIGHTS_PATH = Path(__file__).parent / "data" / "unit_weights.json"

LENGTH_UNIT_CANDIDATES = ["mm", "cm", "m"]
LENGTH_FACTORS = {"mm": 0.001, "cm": 0.01, "m": 1.0}

# R006 单位反推的"多数通过"阈值：既要求相对比例（>=60%，覆盖"表内混了少数几行真错"
# 这种典型场景，不会因为个别错行就把整表退回声明单位、连带把真错行也吃掉），也要求
# 绝对数量下限（>=2 行，排除样本量太小时 1 行偶然通过就被当成"多数"的误判）。
R006_MIN_PASS_RATIO = 0.6
R006_MIN_PASS_COUNT = 2


def load_unit_weights(path: Optional[Path] = None) -> dict:
    data = json.loads((path or DEFAULT_UNIT_WEIGHTS_PATH).read_text(encoding="utf-8"))
    return {float(k): v for k, v in data["weights_kg_per_m"].items()}


def _tol(expected: float, abs_floor: float, rel: float) -> float:
    return max(abs_floor, rel * abs(expected))


def _weight_candidates(diameter_mm: float, total_length_m: float, unit_weights: dict) -> list[tuple[float, str]]:
    candidates = []
    nominal = unit_weights.get(float(diameter_mm))
    if nominal is not None:
        candidates.append((nominal * total_length_m, f"GB 名义值 {nominal}kg/m × {total_length_m:.4f}m"))
    formula = 0.00617 * (diameter_mm ** 2)
    candidates.append((formula * total_length_m, f"0.00617×{diameter_mm}²={formula:.4f}kg/m × {total_length_m:.4f}m"))
    return candidates


def _row_weight_ok(diameter_mm, total_length_m, weight_kg, unit_weights) -> tuple[bool, list[tuple[float, str]]]:
    candidates = _weight_candidates(diameter_mm, total_length_m, unit_weights)
    ok = any(abs(weight_kg - exp) <= _tol(exp, 0.5, 0.005) for exp, _ in candidates)
    return ok, candidates


def check_r006_and_r001(table: dict, unit_weights: dict, findings: list[dict]) -> None:
    """先判 R006（总长单位声明是否与算术反推一致），再用（可能改判的）单位跑 R001。"""
    rows = table["rows"]
    applicable = [
        r for r in rows
        if r["parsed"]["diameter_mm"] is not None
        and r["parsed"]["total_length_raw"] is not None
        and r["parsed"]["weight_kg"] is not None
    ]

    inferred_unit = None
    if applicable and len(applicable) > 1:  # n=1 时样本不足，不做单位反推
        declared_unit = applicable[0]["parsed"]["total_length_unit"] or "m"
        n = len(applicable)

        def pass_count(unit):
            factor = LENGTH_FACTORS[unit]
            k = 0
            for r in applicable:
                p = r["parsed"]
                total_m = p["total_length_raw"] * factor
                ok, _ = _row_weight_ok(p["diameter_mm"], total_m, p["weight_kg"], unit_weights)
                if ok:
                    k += 1
            return k

        k_declared = pass_count(declared_unit)
        if k_declared < n:
            threshold = max(R006_MIN_PASS_COUNT, math.ceil(R006_MIN_PASS_RATIO * n))
            candidate_k = {
                unit: pass_count(unit)
                for unit in LENGTH_UNIT_CANDIDATES
                if unit != declared_unit
            }
            best_k = max(candidate_k.values()) if candidate_k else 0
            best_units = [u for u, k in candidate_k.items() if k == best_k]
            if best_k >= threshold and best_k > k_declared and len(best_units) == 1:
                inferred_unit = best_units[0]
                total_length_col = _col_index(table, "total_length")
                handles = []
                if total_length_col is not None:
                    for r in applicable:
                        handles.extend(r["cells"][total_length_col]["handles"])
                findings.append({
                    "rule_id": "R006",
                    "severity": "warning",
                    "table_id": table["id"],
                    "row_mark": None,
                    "message": f"总长列表头声明单位为 {declared_unit}，但按此单位仅 {k_declared}/{n} 行核对通过；按 {inferred_unit} 折算则 {best_k}/{n} 行通过，疑似表头单位标注与实际数值单位不一致",
                    "expected": declared_unit,
                    "actual": inferred_unit,
                    "handles": handles or [table["title_handle"]],
                })

    if inferred_unit is not None:
        col_idx = _col_index(table, "total_length")
        if col_idx is not None:
            table["columns"][col_idx]["unit_inferred"] = inferred_unit
        factor = LENGTH_FACTORS[inferred_unit]
        for r in rows:
            p = r["parsed"]
            if p["total_length_raw"] is not None:
                p["total_length_m"] = p["total_length_raw"] * factor

    # R001：用（可能已按 R006 改判的）total_length_m 逐行核对
    for r in rows:
        p = r["parsed"]
        if p["diameter_mm"] is None or p["total_length_m"] is None or p["weight_kg"] is None:
            continue
        ok, candidates = _row_weight_ok(p["diameter_mm"], p["total_length_m"], p["weight_kg"], unit_weights)
        if not ok:
            best_exp, basis = min(candidates, key=lambda c: abs(c[0] - p["weight_kg"]))
            findings.append({
                "rule_id": "R001",
                "severity": "error",
                "table_id": table["id"],
                "row_mark": p["mark"],
                "message": f"编号 {p['mark']} 重量与总长×单位理论重量不符（{basis}）",
                "expected": round(best_exp, 3),
                "actual": p["weight_kg"],
                "handles": _row_handles(r),
            })


def check_r002(table: dict, findings: list[dict]) -> None:
    for r in table["rows"]:
        p = r["parsed"]
        if p["single_length_m"] is None or p["count"] is None or p["total_length_m"] is None:
            continue
        expected = p["single_length_m"] * p["count"]
        tol = _tol(expected, 0.05, 0.005)
        if abs(p["total_length_m"] - expected) > tol:
            findings.append({
                "rule_id": "R002",
                "severity": "error",
                "table_id": table["id"],
                "row_mark": p["mark"],
                "message": f"编号 {p['mark']} 总长与 单根长×根数 不符",
                "expected": round(expected, 4),
                "actual": p["total_length_m"],
                "handles": _row_handles(r),
            })


def check_r003(table: dict, findings: list[dict]) -> None:
    sums: dict[str, float] = {}
    handles_by_grade: dict[str, list[str]] = {}
    for r in table["rows"]:
        p = r["parsed"]
        if p["grade"] and p["weight_kg"] is not None:
            sums[p["grade"]] = sums.get(p["grade"], 0.0) + p["weight_kg"]
            handles_by_grade.setdefault(p["grade"], []).extend(_row_handles(r))
    for decl in table["declared_totals"]:
        grade, declared_value = decl["grade"], decl["value_kg"]
        if grade not in sums:
            continue
        actual_sum = sums[grade]
        tol = _tol(declared_value, 0.2, 0.001)
        if abs(actual_sum - declared_value) > tol:
            findings.append({
                "rule_id": "R003",
                "severity": "error",
                "table_id": table["id"],
                "row_mark": None,
                "message": f"牌号 {grade} 行重量之和与表内声明合计不符",
                "expected": declared_value,
                "actual": round(actual_sum, 3),
                "handles": list(decl["handles"]) + handles_by_grade.get(grade, []),
            })


def check_r004(table: dict, findings: list[dict]) -> None:
    by_mark: dict[str, list[dict]] = {}
    for r in table["rows"]:
        mark = r["parsed"]["mark"]
        if mark:
            by_mark.setdefault(mark, []).append(r)
    for mark, rs in by_mark.items():
        if len(rs) > 1:
            handles = []
            for r in rs:
                handles.extend(_row_handles(r))
            findings.append({
                "rule_id": "R004",
                "severity": "warning",
                "table_id": table["id"],
                "row_mark": mark,
                "message": f"编号 {mark} 在本表中重复出现 {len(rs)} 次",
                "expected": 1,
                "actual": len(rs),
                "handles": handles,
            })


def _row_handles(row: dict) -> list[str]:
    handles = []
    for cell in row["cells"]:
        handles.extend(cell["handles"])
    return handles


def _col_index(table: dict, key: str) -> Optional[int]:
    for i, c in enumerate(table["columns"]):
        if c["key"] == key:
            return i
    return None


def run_all_rules(tables: list[dict], unit_weights: Optional[dict] = None) -> tuple[list[dict], list[dict]]:
    """对每张表跑 R001-R006，返回 (findings, gaps)。gaps 汇总各表在抽取阶段记的 R005。"""
    if unit_weights is None:
        unit_weights = load_unit_weights()
    findings: list[dict] = []
    gaps: list[dict] = []
    for table in tables:
        check_r006_and_r001(table, unit_weights, findings)
        check_r002(table, findings)
        check_r003(table, findings)
        check_r004(table, findings)
        for g in table["gaps"]:
            gaps.append({**g, "table_id": table["id"]})
    return findings, gaps
