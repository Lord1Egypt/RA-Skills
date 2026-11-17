"""塔吊吊装校核纯计算库（无 I/O、无 CAD 依赖）。

判据固定：
- 需求吊重 = 重量 × 动载系数 + 吊具重量（默认 1.1 / 0.3 t）
- 归属：仅在同分区塔吊中取幅度最小且 <= jib_m 的一台，不跨区
- 性能表线性插值；超表范围 out_of_range；无表 unknown_no_table
- 利用率 <=0.85 ok；(0.85,1.0] review；>1.0 insufficient
- 永远 final_check=false，结论等级默认 estimated
"""
from __future__ import annotations

import math
from datetime import datetime, timezone
from typing import Any, Iterable

from .model import Baseline, BaselineError, CapacityPoint, Crane, Fleet, Handoff, Member

SCHEMA = "crane-check/v1"

CONCLUSIONS = (
    "ok",
    "review",
    "insufficient",
    "blind",
    "unknown_no_table",
    "out_of_range",
    "unknown_no_weight",
)

CONCLUSION_LABELS = {
    "ok": "余量充足",
    "review": "需复核",
    "insufficient": "不合格",
    "blind": "盲区",
    "unknown_no_table": "无性能表",
    "out_of_range": "超幅度表范围",
    "unknown_no_weight": "缺重量",
}

GRADE_ESTIMATED = "estimated"
GRADE_CONFIRMED_INPUTS = "estimated_confirmed_inputs"


def interpolate_capacity(table: Iterable[CapacityPoint], radius_m: float) -> float | None:
    """按幅度线性插值；超出表范围返回 None（调用方判 out_of_range）。"""
    points = sorted(table, key=lambda p: p.radius_m)
    if not points:
        return None
    if radius_m < points[0].radius_m or radius_m > points[-1].radius_m:
        return None
    if len(points) == 1:
        return points[0].capacity_t if math.isclose(radius_m, points[0].radius_m) else None

    for left, right in zip(points, points[1:]):
        if radius_m <= right.radius_m:
            span = right.radius_m - left.radius_m
            if span <= 0:
                return right.capacity_t
            ratio = (radius_m - left.radius_m) / span
            return left.capacity_t + (right.capacity_t - left.capacity_t) * ratio
    return points[-1].capacity_t


def _distance(x1: float, y1: float, x2: float, y2: float) -> float:
    return math.hypot(x2 - x1, y2 - y1)


def select_crane(member: Member, cranes: Iterable[Crane]) -> tuple[Crane | None, float | None]:
    """同分区 + 幅度 <= jib 的塔吊中取幅度最小；不跨区。"""
    if not member.zone or not member.has_position:
        return None, None

    candidates: list[tuple[float, str, Crane]] = []
    for crane in cranes:
        if member.zone not in crane.zones:
            continue
        if not crane.has_position:
            continue
        radius = _distance(crane.x_m, crane.y_m, member.x_m, member.y_m)  # type: ignore[arg-type]
        if radius <= crane.jib_m + 1e-9:
            candidates.append((radius, crane.id, crane))

    if not candidates:
        return None, None
    candidates.sort(key=lambda item: (item[0], item[1]))
    radius, _, crane = candidates[0]
    return crane, radius


def _threshold(utilization: float) -> str:
    if utilization <= 0.85 + 1e-12:
        return "ok"
    if utilization <= 1.0 + 1e-12:
        return "review"
    return "insufficient"


def check_member(
    member: Member,
    cranes: Iterable[Crane],
    *,
    dynamic_factor: float = 1.1,
    default_hook_t: float = 0.3,
    grade: str = GRADE_ESTIMATED,
) -> dict[str, Any]:
    crane, radius = select_crane(member, cranes)

    hook_t = crane.hook_weight_t if crane and crane.hook_weight_t is not None else default_hook_t
    demand_t: float | None = None
    if member.weight_t is not None:
        demand_t = member.weight_t * dynamic_factor + hook_t

    capacity_t: float | None = None
    utilization: float | None = None
    reason = ""

    if crane is None:
        conclusion = "blind"
        if not member.zone:
            reason = "分区为空，无法按分区归属；不跨区就近分配"
        elif not member.has_position:
            reason = f"柱坐标缺失，无法计算到「{member.zone}」区塔吊的幅度"
        else:
            reason = (
                f"分区「{member.zone}」内无幅度 <= jib_m 的同区塔吊；"
                "不跨区就近分配"
            )
        crane_id = None
    else:
        crane_id = crane.id
        if not crane.has_table:
            conclusion = "unknown_no_table"
            if crane.capacity_source == "missing":
                reason = "capacity_source=missing，无厂家性能表"
            elif crane.table_invalid:
                reason = crane.table_note or "性能表无效"
            else:
                reason = "capacity_table 为空，无法确定额定起重量"
        elif member.weight_t is None:
            conclusion = "unknown_no_weight"
            reason = "weight_t 缺失，无法计算需求吊重"
        else:
            assert radius is not None and demand_t is not None
            capacity_t = interpolate_capacity(crane.capacity_table, radius)
            if capacity_t is None:
                conclusion = "out_of_range"
                low = crane.capacity_table[0].radius_m
                high = crane.capacity_table[-1].radius_m
                reason = f"幅度 {radius:.2f} m 超出性能表范围 {low:g}-{high:g} m"
            elif capacity_t <= 0:
                conclusion = "insufficient"
                reason = "插值额定起重量 <= 0，按不合格处理"
                utilization = math.inf
            else:
                utilization = demand_t / capacity_t
                conclusion = _threshold(utilization)
                reason = f"利用率 {utilization:.3f}"

    return {
        "id": member.id,
        "weight_t": _round(member.weight_t),
        "x_m": _round(member.x_m),
        "y_m": _round(member.y_m),
        "zone": member.zone,
        "coord_status": member.coord_status,
        "weight_basis": member.weight_basis,
        "crane_id": crane_id,
        "crane_model": crane.model if crane else None,
        "capacity_source": crane.capacity_source if crane else None,
        "jib_m": _round(crane.jib_m) if crane else None,
        "radius_m": _round(radius, 4),
        "capacity_t": _round(capacity_t, 4),
        "hook_weight_t": _round(hook_t, 4),
        "demand_t": _round(demand_t, 4),
        "utilization": _round(utilization, 6),
        "conclusion": conclusion,
        "confidence": grade,
        "reason": reason,
    }


def _round(value: float | None, digits: int = 3) -> float | None:
    if value is None:
        return None
    if not math.isfinite(value):
        return None
    return round(value, digits)


def _grade(fleet: Fleet) -> str:
    if fleet.cranes and all(
        crane.capacity_source == "manufacturer" and crane.has_table for crane in fleet.cranes
    ):
        return GRADE_CONFIRMED_INPUTS
    return GRADE_ESTIMATED


def run_check(
    handoff: Handoff,
    fleet: Fleet,
    baseline: Baseline,
    *,
    dynamic_factor: float = 1.1,
    default_hook_t: float = 0.3,
) -> dict[str, Any]:
    baseline.assert_locked()
    if fleet.baseline_version and fleet.baseline_version != baseline.fleet_version:
        raise BaselineError(
            "设备清单版本与口径锁不一致："
            f"fleet.baseline_version={fleet.baseline_version!r}，"
            f"baseline.fleet_version={baseline.fleet_version!r}"
        )

    warnings: list[str] = []
    if handoff.project and fleet.project and handoff.project != fleet.project:
        warnings.append(
            f"项目名不一致：site_handoff={handoff.project!r}，crane_fleet={fleet.project!r}"
        )
    if baseline.project and fleet.project and baseline.project != fleet.project:
        warnings.append(
            f"项目名不一致：baseline={baseline.project!r}，crane_fleet={fleet.project!r}"
        )

    grade = _grade(fleet)
    details = [
        check_member(
            member,
            fleet.cranes,
            dynamic_factor=dynamic_factor,
            default_hook_t=default_hook_t,
            grade=grade,
        )
        for member in handoff.members
    ]

    summary: dict[str, int] = {"total": len(details)}
    for key in CONCLUSIONS:
        summary[key] = sum(1 for row in details if row["conclusion"] == key)

    return {
        "schema": SCHEMA,
        "project": handoff.project or fleet.project or baseline.project,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "final_check": False,
        "conclusion_grade": grade,
        "inputs": {
            "contract_id": handoff.contract_id,
            "source_sha256": handoff.source_sha256,
            "baseline": {
                "fleet_source": baseline.fleet_source,
                "fleet_version": baseline.fleet_version,
                "coverage_criteria": baseline.coverage_criteria,
                "locked_by": baseline.locked_by,
                "locked_at": baseline.locked_at,
            },
            "fleet_baseline_version": fleet.baseline_version,
            "dynamic_factor": dynamic_factor,
            "default_hook_t": default_hook_t,
            "crane_count": len(fleet.cranes),
        },
        "warnings": warnings,
        "summary": summary,
        "members": details,
    }


def _cell(value: Any) -> str:
    if value is None:
        return ""
    text = str(value).replace("|", "／").replace("\n", " ").strip()
    return text


def _fmt(value: float | None, digits: int = 2) -> str:
    return "" if value is None else f"{value:.{digits}f}"


def render_markdown(result: dict[str, Any]) -> str:
    summary = result["summary"]
    members = result["members"]
    baseline = result["inputs"]["baseline"]

    lines: list[str] = []
    lines.append(f"# 塔吊吊装校核报告 · {_cell(result.get('project')) or '未命名项目'}")
    lines.append("")
    lines.append(
        "> 本报告为**估算校核**，`final_check=false`，"
        f"结论等级 `{result['conclusion_grade']}`；不替代施工方案审批、"
        "厂家性能表核验与现场试吊。"
    )
    lines.append("")
    lines.append("## 0. 口径与计数")
    lines.append("")
    lines.append(
        f"- 设备清单来源：`{_cell(baseline['fleet_source'])}`，"
        f"版本 `{_cell(baseline['fleet_version'])}`，"
        f"锁定人 `{_cell(baseline['locked_by'])}`，锁定日期 `{_cell(baseline['locked_at'])}`"
    )
    lines.append(f"- 覆盖判据：{_cell(baseline['coverage_criteria'])}")
    lines.append(
        f"- 动载系数：{result['inputs']['dynamic_factor']:g}；"
        f"默认吊具：{result['inputs']['default_hook_t']:g} t；"
        f"塔吊台数：{result['inputs']['crane_count']}"
    )
    lines.append("")
    lines.append("| 总数 | ok | review | insufficient | blind | unknown_no_table | out_of_range | unknown_no_weight |")
    lines.append("|---:|---:|---:|---:|---:|---:|---:|---:|")
    lines.append(
        "| {total} | {ok} | {review} | {insufficient} | {blind} | "
        "{unknown_no_table} | {out_of_range} | {unknown_no_weight} |".format(**summary)
    )
    lines.append("")

    def section(title: str, keys: tuple[str, ...]) -> None:
        rows = [row for row in members if row["conclusion"] in keys]
        lines.append(f"## {title}")
        lines.append("")
        if not rows:
            lines.append("- 无")
            lines.append("")
            return
        lines.append("| 柱号 | 分区 | 塔吊 | 幅度 m | 额定 t | 需求 t | 利用率 | 结论 | 说明 |")
        lines.append("|---|---|---|---:|---:|---:|---:|---|---|")
        for row in rows:
            lines.append(
                "| {id} | {zone} | {crane} | {radius} | {capacity} | {demand} | "
                "{util} | {conclusion} | {reason} |".format(
                    id=_cell(row["id"]),
                    zone=_cell(row["zone"]),
                    crane=_cell(row["crane_id"]) or "—",
                    radius=_fmt(row["radius_m"]),
                    capacity=_fmt(row["capacity_t"]),
                    demand=_fmt(row["demand_t"]),
                    util=_fmt(row["utilization"], 3),
                    conclusion=row["conclusion"],
                    reason=_cell(row["reason"]),
                )
            )
        lines.append("")

    section("1. 不合格（insufficient）", ("insufficient",))
    section("2. 盲区（blind）", ("blind",))
    section("3. 无性能表（unknown_no_table）", ("unknown_no_table",))
    section("4. 超幅度表范围（out_of_range）", ("out_of_range",))
    section("5. 缺重量（unknown_no_weight）", ("unknown_no_weight",))

    estimated = [row for row in members if row["confidence"] == GRADE_ESTIMATED]
    lines.append("## 6. 估算项（confidence=estimated）")
    lines.append("")
    if not estimated:
        lines.append("- 无：本次全部为厂家性能表输入，但仍为 `final_check=false`。")
    else:
        lines.append(
            f"- 共 {len(estimated)} 根："
            + "、".join(_cell(row["id"]) for row in estimated)
        )
        lines.append("- 这些柱的结论不能作为正式签认；需补厂家性能表后复核。")
    lines.append("")

    lines.append("## 7. 逐柱明细")
    lines.append("")
    lines.append("| 柱号 | 重量 t | x m | y m | 分区 | 塔吊 | 幅度 m | 额定 t | 需求 t | 利用率 | 结论 | 置信度 | 说明 |")
    lines.append("|---|---:|---:|---:|---|---|---:|---:|---:|---:|---|---|---|")
    for row in members:
        lines.append(
            "| {id} | {weight} | {x} | {y} | {zone} | {crane} | {radius} | "
            "{capacity} | {demand} | {util} | {conclusion} | {confidence} | {reason} |".format(
                id=_cell(row["id"]),
                weight=_fmt(row["weight_t"], 3),
                x=_fmt(row["x_m"]),
                y=_fmt(row["y_m"]),
                zone=_cell(row["zone"]),
                crane=_cell(row["crane_id"]) or "—",
                radius=_fmt(row["radius_m"]),
                capacity=_fmt(row["capacity_t"]),
                demand=_fmt(row["demand_t"]),
                util=_fmt(row["utilization"], 3),
                conclusion=row["conclusion"],
                confidence=row["confidence"],
                reason=_cell(row["reason"]),
            )
        )
    lines.append("")

    lines.append("## 8. 输入告警")
    lines.append("")
    if result.get("warnings"):
        for warning in result["warnings"]:
            lines.append(f"- {_cell(warning)}")
    else:
        lines.append("- 无")
    lines.append("")

    lines.append("## 9. 边界")
    lines.append("")
    lines.append("- 只做吊装覆盖与额定起重量校核；不做塔吊选型、基础/附着验算、群塔碰撞。")
    lines.append("- 归属只按同分区最小幅度，不做多机比选；无同区塔吊即判 blind，不跨区凑数。")
    lines.append("- 无厂家性能表一律 `unknown_no_table`，不输出肯定结论。")
    lines.append("- 坐标只接受米（m）；cm/mm/ft 输入直接拒绝，需先换算。")
    lines.append("")
    return "\n".join(lines)


CSV_HEADERS = [
    "柱号",
    "重量_t",
    "x_m",
    "y_m",
    "分区",
    "归属塔吊",
    "幅度_m",
    "额定_t",
    "需求_t",
    "利用率",
    "结论",
    "置信度",
    "说明",
]


def csv_rows(result: dict[str, Any]) -> list[list[Any]]:
    rows: list[list[Any]] = [CSV_HEADERS]
    for row in result["members"]:
        rows.append(
            [
                row["id"],
                _fmt(row["weight_t"], 3),
                _fmt(row["x_m"]),
                _fmt(row["y_m"]),
                row["zone"],
                row["crane_id"] or "",
                _fmt(row["radius_m"]),
                _fmt(row["capacity_t"]),
                _fmt(row["demand_t"]),
                _fmt(row["utilization"], 4),
                row["conclusion"],
                row["confidence"],
                row["reason"],
            ]
        )
    return rows
