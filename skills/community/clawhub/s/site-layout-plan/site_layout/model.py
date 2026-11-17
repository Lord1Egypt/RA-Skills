"""site-layout-plan 场地/塔吊/柱 数据模型。

纯 stdlib，不读 DWG/DXF。所有坐标统一为米（m）；单位声明不是 m 时
直接抛 UnitError（CLI exit 4），避免 mm/cm 混用造成 10/1000 倍错误。
"""
from __future__ import annotations

import json
import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable


class SiteLayoutError(Exception):
    """输入错误（CLI exit 2）。"""

    exit_code = 2


class UnitError(SiteLayoutError):
    """坐标单位错误或不一致（CLI exit 4）。"""

    exit_code = 4


class BaselineError(SiteLayoutError):
    """口径未锁定或版本不一致（CLI exit 5）。"""

    exit_code = 5


UNIT_ALIASES = {
    "m": "m",
    "meter": "m",
    "meters": "m",
    "metre": "m",
    "metres": "m",
    "米": "m",
    "cm": "cm",
    "厘米": "cm",
    "公分": "cm",
    "mm": "mm",
    "毫米": "mm",
    "ft": "ft",
    "feet": "ft",
    "英尺": "ft",
}

UNIT_TEXT = {"cm": "厘米（cm）", "mm": "毫米（mm）", "ft": "英尺（ft）"}


def normalize_unit(value: Any) -> str:
    text = str(value).strip().lower()
    if text in UNIT_ALIASES:
        return UNIT_ALIASES[text]
    raise UnitError(f"无法识别坐标单位 {value!r}；只接受米（m）")


def _declared_unit(container: dict[str, Any]) -> str | None:
    for key in ("coord_unit", "unit", "units"):
        value = container.get(key)
        if value is not None and str(value).strip() != "":
            return normalize_unit(value)
    return None


def _number(value: Any, label: str, *, allow_none: bool = False) -> float | None:
    if value is None:
        if allow_none:
            return None
        raise SiteLayoutError(f"{label} 缺失")
    if isinstance(value, bool):
        raise SiteLayoutError(f"{label} 必须是数字，收到布尔值")
    try:
        result = float(value)
    except (TypeError, ValueError) as exc:
        raise SiteLayoutError(f"{label} 必须是数字，收到 {value!r}") from exc
    if not math.isfinite(result):
        raise SiteLayoutError(f"{label} 必须是有限数字，收到 {value!r}")
    return result


def _text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _xy_from(container: dict[str, Any], *, allow_bare_xy: bool) -> tuple[float | None, float | None]:
    """读取坐标。优先 x_m/y_m；其次 coord_m / position_m 二元组。

    裸 x/y 只有在该对象或顶层显式声明单位为 m 时才接受，避免把读者
    输出的 mm 值误当米。
    """
    if container.get("x_m") is not None or container.get("y_m") is not None:
        return (
            _number(container.get("x_m"), "x_m", allow_none=True),
            _number(container.get("y_m"), "y_m", allow_none=True),
        )

    for key in ("coord_m", "position_m", "center_m"):
        value = container.get(key)
        if isinstance(value, (list, tuple)) and len(value) == 2:
            return _number(value[0], f"{key}[0]"), _number(value[1], f"{key}[1]")

    for key in ("coord", "position", "center"):
        value = container.get(key)
        if isinstance(value, dict):
            if value.get("x_m") is not None or value.get("y_m") is not None:
                return (
                    _number(value.get("x_m"), f"{key}.x_m", allow_none=True),
                    _number(value.get("y_m"), f"{key}.y_m", allow_none=True),
                )
            if allow_bare_xy and (value.get("x") is not None or value.get("y") is not None):
                return (
                    _number(value.get("x"), f"{key}.x", allow_none=True),
                    _number(value.get("y"), f"{key}.y", allow_none=True),
                )

    if allow_bare_xy and (container.get("x") is not None or container.get("y") is not None):
        return (
            _number(container.get("x"), "x", allow_none=True),
            _number(container.get("y"), "y", allow_none=True),
        )
    return None, None


def _assert_metre(unit: str | None, where: str) -> None:
    if unit is None or unit == "m":
        return
    raise UnitError(
        f"{where} 的坐标单位是{UNIT_TEXT.get(unit, unit)}而非米（m）；"
        "请先换算为米再校核（拒绝按 10/1000 倍猜测）"
    )


@dataclass
class Member:
    id: str
    weight_t: float | None
    x_m: float | None
    y_m: float | None
    zone: str
    weight_basis: str
    coord_status: str
    raw: dict[str, Any] = field(default_factory=dict, repr=False)

    @property
    def has_position(self) -> bool:
        return self.x_m is not None and self.y_m is not None


@dataclass(frozen=True)
class CapacityPoint:
    radius_m: float
    capacity_t: float


@dataclass
class Crane:
    id: str
    model: str
    jib_m: float
    capacity_source: str
    capacity_table: list[CapacityPoint]
    hook_weight_t: float | None
    zones: list[str]
    x_m: float | None
    y_m: float | None
    table_invalid: bool = False
    table_note: str = ""
    raw: dict[str, Any] = field(default_factory=dict, repr=False)

    @property
    def has_position(self) -> bool:
        return self.x_m is not None and self.y_m is not None

    @property
    def has_table(self) -> bool:
        return (
            self.capacity_source != "missing"
            and not self.table_invalid
            and len(self.capacity_table) > 0
        )


@dataclass
class Baseline:
    project: str
    fleet_source: str
    fleet_version: str
    coverage_criteria: str
    locked_by: str
    locked_at: str

    def assert_locked(self) -> None:
        missing = [
            name
            for name, value in (
                ("project", self.project),
                ("fleet_source", self.fleet_source),
                ("fleet_version", self.fleet_version),
                ("coverage_criteria", self.coverage_criteria),
                ("locked_by", self.locked_by),
                ("locked_at", self.locked_at),
            )
            if not str(value or "").strip()
        ]
        if missing:
            raise BaselineError(f"baseline 缺少锁定字段：{', '.join(missing)}")
        if self.fleet_source not in ("schedule", "drawing"):
            raise BaselineError(
                f"fleet_source={self.fleet_source!r} 非法；只能是 schedule 或 drawing"
            )


@dataclass
class Handoff:
    project: str
    contract_id: str
    source_sha256: str
    members: list[Member]


@dataclass
class Fleet:
    project: str
    baseline_version: str
    cranes: list[Crane]


def _load_json(path: str | Path, label: str) -> tuple[dict[str, Any], Path]:
    file_path = Path(path).expanduser()
    if not file_path.is_file():
        if label == "baseline":
            raise BaselineError(f"找不到 baseline 文件：{file_path}")
        raise SiteLayoutError(f"找不到 {label} 文件：{file_path}")
    try:
        data = json.loads(file_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise SiteLayoutError(f"无法读取 {label} JSON：{file_path}：{exc}") from exc
    if not isinstance(data, dict):
        raise SiteLayoutError(f"{label} 顶层必须是 JSON 对象")
    return data, file_path


def load_baseline(path: str | Path) -> Baseline:
    data, _ = _load_json(path, "baseline")
    baseline = Baseline(
        project=_text(data.get("project")),
        fleet_source=_text(data.get("fleet_source")),
        fleet_version=_text(data.get("fleet_version")),
        coverage_criteria=_text(data.get("coverage_criteria")),
        locked_by=_text(data.get("locked_by")),
        locked_at=_text(data.get("locked_at")),
    )
    baseline.assert_locked()
    return baseline


def load_handoff(path: str | Path) -> Handoff:
    data, _ = _load_json(path, "site_handoff")
    schema = _text(data.get("schema"))
    if schema != "site-handoff/v1":
        raise SiteLayoutError(
            f"site_handoff.schema={schema!r}，只接受 reader 的 site-handoff/v1；"
            "请先走 lis-skill-bus → cad-file-reader"
        )

    top_unit = _declared_unit(data)
    _assert_metre(top_unit, "site_handoff")

    raw_members = data.get("members")
    if not isinstance(raw_members, list) or not raw_members:
        raise SiteLayoutError("site_handoff.members 必须是非空数组")

    members: list[Member] = []
    seen: set[str] = set()
    for index, raw in enumerate(raw_members):
        if not isinstance(raw, dict):
            raise SiteLayoutError(f"members[{index}] 必须是对象")
        member_unit = _declared_unit(raw)
        _assert_metre(member_unit, f"members[{index}]")
        member_id = _text(raw.get("id"))
        if not member_id:
            raise SiteLayoutError(f"members[{index}].id 缺失")
        if member_id in seen:
            raise SiteLayoutError(f"members 存在重复 id：{member_id}")
        seen.add(member_id)

        allow_bare = top_unit == "m" or member_unit == "m"
        x_m, y_m = _xy_from(raw, allow_bare_xy=allow_bare)
        if (x_m is None) != (y_m is None):
            raise SiteLayoutError(f"members[{index}]（{member_id}）x/y 只给了一个")

        weight = _number(raw.get("weight_t"), f"{member_id}.weight_t", allow_none=True)
        if weight is not None and weight <= 0:
            raise SiteLayoutError(f"{member_id}.weight_t 必须大于 0")

        members.append(
            Member(
                id=member_id,
                weight_t=weight,
                x_m=x_m,
                y_m=y_m,
                zone=_text(raw.get("zone")),
                weight_basis=_text(raw.get("weight_basis")) or "unknown",
                coord_status=_text(raw.get("coord_status"))
                or ("confirmed" if x_m is not None and y_m is not None else "missing"),
                raw=raw,
            )
        )

    return Handoff(
        project=_text(data.get("project")),
        contract_id=_text(data.get("contract_id")),
        source_sha256=_text(data.get("source_sha256")),
        members=members,
    )


def _parse_capacity_table(crane_id: str, raw: Any) -> tuple[list[CapacityPoint], bool, str]:
    if raw is None:
        return [], False, ""
    if not isinstance(raw, list):
        return [], True, "capacity_table 不是数组"
    points: list[CapacityPoint] = []
    try:
        for item in raw:
            if not isinstance(item, dict):
                raise ValueError("表项不是对象")
            radius = _number(item.get("radius_m"), f"{crane_id}.capacity_table.radius_m")
            capacity = _number(item.get("capacity_t"), f"{crane_id}.capacity_table.capacity_t")
            if radius < 0:
                raise ValueError("幅度不能为负")
            if capacity <= 0:
                raise ValueError("额定起重量必须大于 0")
            points.append(CapacityPoint(radius_m=radius, capacity_t=capacity))
    except (SiteLayoutError, ValueError) as exc:
        return [], True, f"性能表无效：{exc}"

    points.sort(key=lambda p: (p.radius_m, p.capacity_t))
    deduped: list[CapacityPoint] = []
    for point in points:
        if deduped and math.isclose(point.radius_m, deduped[-1].radius_m):
            # 同一幅度出现两个额定值：取保守（较小）值
            if point.capacity_t < deduped[-1].capacity_t:
                deduped[-1] = point
            continue
        deduped.append(point)
    return deduped, False, ""


def load_fleet(path: str | Path) -> Fleet:
    data, _ = _load_json(path, "crane_fleet")
    top_unit = _declared_unit(data)
    _assert_metre(top_unit, "crane_fleet")

    raw_cranes = data.get("cranes")
    if not isinstance(raw_cranes, list) or not raw_cranes:
        raise SiteLayoutError("crane_fleet.cranes 必须是非空数组")

    cranes: list[Crane] = []
    seen: set[str] = set()
    for index, raw in enumerate(raw_cranes):
        if not isinstance(raw, dict):
            raise SiteLayoutError(f"cranes[{index}] 必须是对象")
        crane_unit = _declared_unit(raw)
        _assert_metre(crane_unit, f"cranes[{index}]")

        crane_id = _text(raw.get("id"))
        if not crane_id:
            raise SiteLayoutError(f"cranes[{index}].id 缺失")
        if crane_id in seen:
            raise SiteLayoutError(f"cranes 存在重复 id：{crane_id}")
        seen.add(crane_id)

        jib = _number(raw.get("jib_m"), f"{crane_id}.jib_m")
        if jib <= 0:
            raise SiteLayoutError(f"{crane_id}.jib_m 必须大于 0")

        source = _text(raw.get("capacity_source")).lower() or "missing"
        if source not in ("manufacturer", "estimated", "missing"):
            raise SiteLayoutError(
                f"{crane_id}.capacity_source={source!r}；只接受 manufacturer/estimated/missing"
            )

        hook = _number(raw.get("hook_weight_t"), f"{crane_id}.hook_weight_t", allow_none=True)
        if hook is not None and hook < 0:
            raise SiteLayoutError(f"{crane_id}.hook_weight_t 不能为负")

        zones_raw = raw.get("zones") or []
        if not isinstance(zones_raw, list):
            raise SiteLayoutError(f"{crane_id}.zones 必须是数组")
        zones = [_text(zone) for zone in zones_raw if _text(zone)]

        allow_bare = top_unit == "m" or crane_unit == "m"
        x_m, y_m = _xy_from(raw, allow_bare_xy=allow_bare)
        if (x_m is None) != (y_m is None):
            raise SiteLayoutError(f"{crane_id} 的 x/y 只给了一个")

        table, invalid, note = _parse_capacity_table(crane_id, raw.get("capacity_table"))
        if source == "missing" and table:
            # 来源声明缺失时，表只能作为参考，不能升级为可信输入
            note = note or "capacity_source=missing，性能表不作为可信依据"

        cranes.append(
            Crane(
                id=crane_id,
                model=_text(raw.get("model")),
                jib_m=jib,
                capacity_source=source,
                capacity_table=table,
                hook_weight_t=hook,
                zones=zones,
                x_m=x_m,
                y_m=y_m,
                table_invalid=invalid,
                table_note=note,
                raw=raw,
            )
        )

    return Fleet(
        project=_text(data.get("project")),
        baseline_version=_text(data.get("baseline_version")),
        cranes=cranes,
    )


def load_all(
    handoff_path: str | Path, fleet_path: str | Path, baseline_path: str | Path
) -> tuple[Handoff, Fleet, Baseline]:
    """按 baseline → handoff → fleet 顺序装载，baseline 缺失时最早失败。"""
    baseline = load_baseline(baseline_path)
    handoff = load_handoff(handoff_path)
    fleet = load_fleet(fleet_path)
    return handoff, fleet, baseline


def zone_members(members: Iterable[Member]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for member in members:
        key = member.zone or "（空）"
        counts[key] = counts.get(key, 0) + 1
    return counts
