"""site-layout-plan 0.7.2 · 派生 DXF/PNG 出图、图签与自检。

硬边界：
- 只读输入原图，永不写回；输出目录不得等于原图目录。
- 输出模型空间 1:1，单位 mm。
- contract_id 不一致或 final_check=false 时只出 DRAFT 草稿图。
- 自检有 fail 时仍保留已生成文件，但 CLI 返回 exit 5。
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
import os
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

try:  # 测试环境会先把 cad-file-reader/vendor 放进 sys.path
    import ezdxf  # type: ignore
except ImportError as exc:  # pragma: no cover - CLI 会先 bootstrap
    raise ImportError("缺少 ezdxf；请安装 ezdxf>=1.4 或设置 SITE_LAYOUT_VENDOR") from exc

from . import __version__
from .model import BaselineError, SiteLayoutError, UnitError, load_baseline, load_handoff, normalize_unit
from .prepare import validate_reader_contract, validate_reader_path

VERSION = __version__
SCHEMA = "layout-selfcheck/v1"
BASE_MAP_SCHEMA = "site-layout-base-map/v1"
TITLEBLOCK_SCHEMA = "layout-titleblock/v1"
LAYOUT_SCHEMA = "layout-result/v1"
DEFAULT_TITLEBLOCK = Path(__file__).resolve().parent.parent / "templates" / "titleblock.json"
REQUIRED_LAYERS: Tuple[Tuple[str, int, str, str], ...] = (
    ("BASE-底图", 8, "Continuous", "原图几何，灰显"),
    ("CRANE-塔吊", 1, "Continuous", "塔吊符号、型号、臂长、回转中心"),
    ("CRANE-覆盖", 5, "DASHED", "幅度圆，按塔吊分色"),
    ("LIFT-合格", 3, "Continuous", "逐柱着色：合格"),
    ("LIFT-超载", 1, "Continuous", "逐柱着色：超载/不合格"),
    ("LIFT-盲区", 2, "Continuous", "逐柱着色：盲区/待复核"),
    ("TEXT-结论", 7, "Continuous", "柱号、需求/额定、利用率"),
    ("META-图签", 7, "Continuous", "contract_id、版本、日期、免责声明、DRAFT"),
)
REQUIRED_LAYER_NAMES = tuple(row[0] for row in REQUIRED_LAYERS)
REDLINE_KEYWORDS = ("REDLINE", "BOUNDARY", "红线", "用地")
FENCE_KEYWORDS = ("FENCE", "HOARD", "围挡")
CRANE_COLORS = (1, 3, 5, 2, 6, 4, 7)
MEMBER_LAYER = {
    "ok": "LIFT-合格",
    "review": "LIFT-盲区",
    "insufficient": "LIFT-超载",
    "out_of_range": "LIFT-超载",
    "blind": "LIFT-盲区",
    "unknown_no_table": "LIFT-盲区",
    "unknown_no_weight": "LIFT-盲区",
}


class DrawGateError(SiteLayoutError):
    """出图闸门失败（CLI exit 5）。"""

    exit_code = 5


class FontError(SiteLayoutError):
    """字体不可用；允许显式降级，但必须写入图签与自检证据。"""


@dataclass
class CraneSpec:
    id: str
    model: str
    jib_mm: float
    x_mm: float
    y_mm: float


@dataclass
class SiteData:
    source_path: Path
    source_kind: str
    source_sha256: str
    source_units: str
    mm_per_unit: float
    contract_id: str
    contract_id_source: str
    contract_source_sha256: str = ""
    base_entities: List[Any] = field(default_factory=list)
    base_segments: List[Tuple[float, float, float, float]] = field(default_factory=list)
    redline_vertices: List[Tuple[float, float]] = field(default_factory=list)
    redline_segments: List[Tuple[float, float, float, float]] = field(default_factory=list)
    redline_closed: bool = False
    redline_gap_mm: Optional[float] = None
    fence_vertices: List[Tuple[float, float]] = field(default_factory=list)
    fence_segments: List[Tuple[float, float, float, float]] = field(default_factory=list)
    extents: Optional[Tuple[float, float, float, float]] = None
    warnings: List[str] = field(default_factory=list)


def _safe_text(value: Any, default: str = "") -> str:
    if value is None:
        return default
    text = str(value).strip()
    return text or default


def _number(value: Any, label: str) -> float:
    if isinstance(value, bool):
        raise SiteLayoutError(f"{label} 必须是数字，收到布尔值")
    try:
        result = float(value)
    except (TypeError, ValueError) as exc:
        raise SiteLayoutError(f"{label} 必须是数字，收到 {value!r}") from exc
    if not math.isfinite(result):
        raise SiteLayoutError(f"{label} 必须是有限数字，收到 {value!r}")
    return result


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _unit_factor(unit: str) -> Tuple[str, float]:
    normalized = normalize_unit(unit)
    if normalized == "mm":
        return "mm", 1.0
    if normalized == "m":
        return "m", 1000.0
    raise UnitError("出图只接受 mm 或 m 源坐标；请先换算为 mm 后再出图")


def _layer_matches(layer: str, keywords: Sequence[str]) -> bool:
    text = (layer or "").upper()
    return any(keyword.upper() in text for keyword in keywords)


def _entity_points(entity: Any, factor: float) -> List[Tuple[float, float]]:
    kind = entity.dxftype()
    points: List[Tuple[float, float]] = []
    try:
        if kind == "LINE":
            points = [
                (float(entity.dxf.start.x) * factor, float(entity.dxf.start.y) * factor),
                (float(entity.dxf.end.x) * factor, float(entity.dxf.end.y) * factor),
            ]
        elif kind == "LWPOLYLINE":
            points = [(float(x) * factor, float(y) * factor) for x, y, *_ in entity.get_points("xyseb")]
        elif kind == "POLYLINE":
            points = [
                (float(vertex.dxf.location.x) * factor, float(vertex.dxf.location.y) * factor)
                for vertex in entity.vertices
            ]
        elif kind in ("POINT",):
            loc = entity.dxf.location
            points = [(float(loc.x) * factor, float(loc.y) * factor)]
        elif kind in ("TEXT", "MTEXT", "INSERT"):
            loc = entity.dxf.insert
            points = [(float(loc.x) * factor, float(loc.y) * factor)]
        elif kind in ("CIRCLE", "ARC"):
            center = entity.dxf.center
            radius = float(entity.dxf.radius) * factor
            cx, cy = float(center.x) * factor, float(center.y) * factor
            points = [(cx - radius, cy - radius), (cx + radius, cy + radius), (cx, cy)]
        elif kind == "SOLID":
            for name in ("vtx0", "vtx1", "vtx2", "vtx3"):
                if entity.dxf.hasattr(name):
                    v = entity.dxf.get(name)
                    points.append((float(v.x) * factor, float(v.y) * factor))
    except Exception:
        return []
    return points


def _bbox_points(points: Iterable[Tuple[float, float]]) -> Optional[Tuple[float, float, float, float]]:
    data = list(points)
    if not data:
        return None
    xs = [p[0] for p in data]
    ys = [p[1] for p in data]
    return (min(xs), min(ys), max(xs), max(ys))


def _merge_bbox(
    left: Optional[Tuple[float, float, float, float]],
    right: Optional[Tuple[float, float, float, float]],
) -> Optional[Tuple[float, float, float, float]]:
    if left is None:
        return right
    if right is None:
        return left
    return (min(left[0], right[0]), min(left[1], right[1]), max(left[2], right[2]), max(left[3], right[3]))


def _distance(a: Tuple[float, float], b: Tuple[float, float]) -> float:
    return math.hypot(a[0] - b[0], a[1] - b[1])


def _polyline_area(points: Sequence[Tuple[float, float]]) -> float:
    if len(points) < 3:
        return 0.0
    return abs(sum(points[i][0] * points[(i + 1) % len(points)][1] - points[(i + 1) % len(points)][0] * points[i][1] for i in range(len(points))) / 2.0)


def _assemble_loop(
    segments: Sequence[Tuple[float, float, float, float]], tolerance_mm: float = 50.0
) -> Tuple[List[Tuple[float, float]], bool, Optional[float]]:
    """把线段按端点吸附串成闭合环；返回顶点、是否闭合、首尾缺口。"""
    usable = [seg for seg in segments if _distance((seg[0], seg[1]), (seg[2], seg[3])) > 1e-9]
    if not usable:
        return [], False, None
    remaining = list(usable)
    first = remaining.pop(0)
    points = [(first[0], first[1]), (first[2], first[3])]
    while remaining:
        tail = points[-1]
        best_index = -1
        best_reverse = False
        best_distance = tolerance_mm + 1e-9
        for index, seg in enumerate(remaining):
            d_start = _distance(tail, (seg[0], seg[1]))
            d_end = _distance(tail, (seg[2], seg[3]))
            if d_start <= best_distance:
                best_distance = d_start
                best_index = index
                best_reverse = False
            if d_end <= best_distance:
                best_distance = d_end
                best_index = index
                best_reverse = True
        if best_index < 0:
            break
        seg = remaining.pop(best_index)
        nxt = (seg[0], seg[1]) if best_reverse else (seg[2], seg[3])
        if _distance(points[-1], nxt) > 1e-9:
            points.append(nxt)
    gap = _distance(points[-1], points[0])
    closed = len(points) >= 4 and gap <= tolerance_mm + 1e-9
    if closed and _distance(points[-1], points[0]) <= 1e-9:
        points = points[:-1]
    return points, closed, gap


def _json_declared_unit(data: Dict[str, Any]) -> Optional[str]:
    for key in ("coord_unit", "units", "unit", "drawing_unit"):
        value = data.get(key)
        if value not in (None, ""):
            return _safe_text(value)
    audit = data.get("scale_unit_audit")
    if isinstance(audit, list):
        values: List[str] = []
        for row in audit:
            if not isinstance(row, dict):
                continue
            for key in ("units", "unit", "drawing_unit"):
                raw = row.get(key)
                if isinstance(raw, list):
                    values.extend(_safe_text(item) for item in raw if _safe_text(item))
                elif _safe_text(raw):
                    values.append(_safe_text(raw))
        unique = sorted({value.lower() for value in values})
        if len(unique) == 1:
            return unique[0]
    return None


def _load_site_json(path: Path) -> SiteData:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise SiteLayoutError(f"无法读取场地 JSON：{path}：{exc}") from exc
    if not isinstance(data, dict):
        raise SiteLayoutError("场地 JSON 顶层必须是对象")
    # 0.7.2 硬闸门：只接受 cad-file-reader 的 cad-site-geometry/v1，
    # 或 prepare_site 从该契约派生的 base-map；普通 JSON、手写底图一律拒绝。
    if _safe_text(data.get("schema")) == BASE_MAP_SCHEMA:
        validate_reader_path(path)
        if _safe_text(data.get("source_schema")) != "cad-site-geometry/v1":
            raise SiteLayoutError(
                "base-map 缺少 reader 来源：source_schema 必须是 cad-site-geometry/v1；"
                "请先走 lis-skill-bus → cad-file-reader → prepare_site.py"
            )
    else:
        validate_reader_contract(path, data)
    unit_text = _json_declared_unit(data)
    if not unit_text:
        raise UnitError("场地 JSON 未声明单位（coord_unit/units/drawing_unit），不能出图")
    source_units, factor = _unit_factor(unit_text)
    contract_id = _safe_text(data.get("contract_id") or (data.get("contract") or {}).get("contract_id"))
    contract_source = "json" if contract_id else "missing"
    base_segments: List[Tuple[float, float, float, float]] = []
    redline_segments: List[Tuple[float, float, float, float]] = []
    fence_segments: List[Tuple[float, float, float, float]] = []
    extents: Optional[Tuple[float, float, float, float]] = None
    rows = data.get("site_geometry") or []
    if isinstance(rows, list):
        for row in rows:
            if not isinstance(row, dict):
                continue
            geom = row.get("geometry")
            if not isinstance(geom, (list, tuple)) or len(geom) < 4:
                continue
            try:
                segment = (
                    float(geom[0]) * factor,
                    float(geom[1]) * factor,
                    float(geom[2]) * factor,
                    float(geom[3]) * factor,
                )
            except (TypeError, ValueError):
                continue
            base_segments.append(segment)
            extents = _merge_bbox(extents, _bbox_points([(segment[0], segment[1]), (segment[2], segment[3])]))
            layer = _safe_text(row.get("layer") or row.get("layer_name") or row.get("category"))
            if _layer_matches(layer, REDLINE_KEYWORDS):
                redline_segments.append(segment)
            if _layer_matches(layer, FENCE_KEYWORDS):
                fence_segments.append(segment)
    redline_vertices: List[Tuple[float, float]] = []
    redline_closed = False
    redline_gap: Optional[float] = None
    direct_poly = data.get("redline") or data.get("boundary")
    if isinstance(direct_poly, list) and len(direct_poly) >= 3:
        try:
            redline_vertices = [(float(p[0]) * factor, float(p[1]) * factor) for p in direct_poly]
            if len(redline_vertices) >= 2 and _distance(redline_vertices[0], redline_vertices[-1]) <= 1e-9:
                redline_vertices = redline_vertices[:-1]
            redline_closed = len(redline_vertices) >= 3
            redline_gap = 0.0 if redline_closed else None
        except (TypeError, ValueError, IndexError):
            redline_vertices = []
    if not redline_vertices and redline_segments:
        redline_vertices, redline_closed, redline_gap = _assemble_loop(redline_segments, 50.0)
    fence_vertices, _fc, _fg = _assemble_loop(fence_segments, 50.0) if fence_segments else ([], False, None)
    reader_contract = data.get("contract") if isinstance(data.get("contract"), dict) else {}
    return SiteData(
        source_path=path,
        source_kind="json",
        source_sha256=_sha256(path),
        source_units=source_units,
        mm_per_unit=factor,
        contract_id=contract_id,
        contract_id_source=contract_source,
        contract_source_sha256=_safe_text(reader_contract.get("source_sha256")),
        base_segments=base_segments,
        redline_vertices=redline_vertices,
        redline_segments=redline_segments,
        redline_closed=redline_closed,
        redline_gap_mm=redline_gap,
        fence_vertices=fence_vertices,
        fence_segments=fence_segments,
        extents=extents,
        warnings=["site JSON 的几何仅使用 site_geometry[] 线段；未做识图或重解析"],
    )


def load_site(path_value: str) -> SiteData:
    path = Path(path_value).expanduser()
    if not path.is_file():
        raise SiteLayoutError(f"找不到场地文件：{path}")
    # 0.7.2 硬闸门：出图也不得直读 CAD/PDF。识图只能走
    # DWG/DXF/PDF → lis-skill-bus → cad-file-reader → cad-contract/v1 → 本技能。
    validate_reader_path(path)
    if path.suffix.lower() != ".json":
        raise SiteLayoutError(
            "--site 只接受 cad-file-reader 的 cad-site-geometry/v1 JSON"
            "（或 prepare_site.py 从该契约派生的 base-map.json）；不直读 CAD/PDF"
        )
    return _load_site_json(path)


def _default_layout_path(site_path: Path) -> Optional[Path]:
    candidate = site_path.with_name(site_path.stem + ".layout.json")
    return candidate if candidate.is_file() else None


def load_layout(path_value: Optional[str], site_path: Path, check_data: Dict[str, Any]) -> Tuple[List[CraneSpec], str, Optional[str]]:
    path: Optional[Path] = Path(path_value).expanduser() if path_value else _default_layout_path(site_path)
    if path is not None and not path.is_file():
        raise SiteLayoutError(f"找不到布置结果 JSON：{path}")
    data: Dict[str, Any] = {}
    if path is not None:
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise SiteLayoutError(f"无法读取布置结果 JSON：{path}：{exc}") from exc
        if not isinstance(payload, dict):
            raise SiteLayoutError("布置结果 JSON 顶层必须是对象")
        data = payload
    raw_cranes = data.get("cranes") or data.get("crane_layout") or data.get("towers") or check_data.get("cranes")
    if not isinstance(raw_cranes, list) or not raw_cranes:
        raise SiteLayoutError("缺少布置结果 JSON 中的 cranes[]；请用 --layout 指定")

    # cad-file-reader 的 *.crane.json 用 center_xy_m / jib_length_m，且单位依据在 units.basis。
    # 若 reader 未显式声明图纸单位，center_xy_m 可能按默认 mm 误算，必须拒绝而不是猜。
    units = data.get("units") if isinstance(data.get("units"), dict) else {}
    unit_basis = _safe_text(units.get("basis"))
    if unit_basis and unit_basis != "explicit":
        for index, raw in enumerate(raw_cranes):
            if isinstance(raw, dict) and raw.get("center_xy_m"):
                raise UnitError(
                    f"塔吊识图未声明图纸单位（units.basis={unit_basis}），center_xy_m 不可信；"
                    "请先用 cad_crane_geometry --drawing-unit mm 重跑识图"
                )

    cranes: List[CraneSpec] = []
    seen: set = set()
    for index, raw in enumerate(raw_cranes):
        if not isinstance(raw, dict):
            raise SiteLayoutError(f"cranes[{index}] 必须是对象")
        crane_id = _safe_text(raw.get("id") or raw.get("crane_id"))
        if not crane_id:
            raise SiteLayoutError(f"cranes[{index}].id 缺失")
        if crane_id in seen:
            raise SiteLayoutError(f"cranes 存在重复 id：{crane_id}")
        seen.add(crane_id)
        if raw.get("jib_m") is not None:
            jib_mm = _number(raw.get("jib_m"), f"{crane_id}.jib_m") * 1000.0
        elif raw.get("jib_length_m") is not None:
            jib_mm = _number(raw.get("jib_length_m"), f"{crane_id}.jib_length_m") * 1000.0
        elif raw.get("jib_mm") is not None:
            jib_mm = _number(raw.get("jib_mm"), f"{crane_id}.jib_mm")
        else:
            raise SiteLayoutError(f"{crane_id}.jib 缺失；请给 jib_m / jib_length_m / jib_mm")
        if jib_mm <= 0:
            raise SiteLayoutError(f"{crane_id}.jib 必须大于 0")
        center = raw.get("center_xy_m")
        if raw.get("x_mm") is not None and raw.get("y_mm") is not None:
            x_mm = _number(raw.get("x_mm"), f"{crane_id}.x_mm")
            y_mm = _number(raw.get("y_mm"), f"{crane_id}.y_mm")
        elif raw.get("x_m") is not None and raw.get("y_m") is not None:
            x_mm = _number(raw.get("x_m"), f"{crane_id}.x_m") * 1000.0
            y_mm = _number(raw.get("y_m"), f"{crane_id}.y_m") * 1000.0
        elif isinstance(center, (list, tuple)) and len(center) >= 2 and center[0] is not None and center[1] is not None:
            status = _safe_text(raw.get("center_status"))
            if status and status != "insert_point":
                raise SiteLayoutError(
                    f"{crane_id} 回转中心不可用（center_status={status}）；"
                    "请用 DXF + 块基点重跑 cad_crane_geometry，不要伪造中心"
                )
            x_mm = _number(center[0], f"{crane_id}.center_xy_m[0]") * 1000.0
            y_mm = _number(center[1], f"{crane_id}.center_xy_m[1]") * 1000.0
        else:
            raise SiteLayoutError(
                f"{crane_id} 缺少回转中心：请给 x_m/y_m、x_mm/y_mm 或 reader 的 center_xy_m"
            )
        cranes.append(
            CraneSpec(
                id=crane_id,
                model=_safe_text(raw.get("model"), "未注明"),
                jib_mm=jib_mm,
                x_mm=x_mm,
                y_mm=y_mm,
            )
        )
    # 显式给了 layout 文件却没有 contract_id 时，必须返回空串而不是 None：
    # _check_contract_ids 要把 layout 计入"缺失"，未加 --draft 时 exit 5。
    contract_id = _safe_text(data.get("contract_id") or (data.get("contract") or {}).get("contract_id"))
    return cranes, (str(path) if path else "<check.cranes>"), (contract_id if path is not None else None)


def _load_json(path_value: str, label: str) -> Tuple[Dict[str, Any], Path, str]:
    path = Path(path_value).expanduser()
    if not path.is_file():
        raise SiteLayoutError(f"找不到 {label}：{path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise SiteLayoutError(f"无法读取 {label} JSON：{path}：{exc}") from exc
    if not isinstance(data, dict):
        raise SiteLayoutError(f"{label} JSON 顶层必须是对象")
    return data, path, _sha256(path)


def _check_contract_ids(site_id: str, handoff_id: str, check_id: str, layout_id: Optional[str], draft: bool) -> Tuple[bool, Dict[str, str], str]:
    """契约闸门：只要求"可追溯"，不再要求不同专业 payload 的 ID 相同。

    背景：cad-file-reader 的 contract_id = 源图哈希 + 业务内容摘要 + 图号/专业，
    同一张总平面图的 *.site.json 与 *.crane.json 内容不同，contract_id 必然不同。
    把它们判成"不一致"会逼着用户只能出草稿图。

    现在的口径：
    - 每个输入都应有 contract_id（缺失 → 不可追溯，未加 --draft 直接 exit 5）。
    - contract_id 不同但都存在 → 允许，图签分别列出各输入 ID，并标记
      contract_ids_differ=true 供人工核对是否同一版本。
    - 是否需要"同源"由上游 source_sha256 证明（见 siteplan 的 same_source 闸门）。
    """
    ids = {"site": site_id, "handoff": handoff_id, "check": check_id}
    # 空串代表"显式提供了 layout 文件但没有 contract_id"，必须计入缺失；
    # None 代表没有独立 layout 输入（塔吊数据来自 check），不参与闸门。
    if layout_id is not None:
        ids["layout"] = layout_id
    missing = [key for key, value in ids.items() if not _safe_text(value)]
    if missing and not draft:
        raise DrawGateError(
            "contract_id 缺失（{}）：无法追溯输入版本；补 contract_id，或加 --draft 出草稿图".format(
                ",".join(missing))
        )
    reason = "缺失：" + ",".join(missing) if missing else ""
    return bool(missing), ids, reason


def _draft_label(final_check: bool, mismatch: bool, requested: bool) -> str:
    if mismatch:
        return "DRAFT-CONTRACT-MISMATCH"
    if (not final_check) or requested:
        return "DRAFT"
    return ""


def _titleblock_params(template_path: Optional[str], overrides: Dict[str, Any]) -> Dict[str, Any]:
    path = Path(template_path).expanduser() if template_path else DEFAULT_TITLEBLOCK
    if not path.is_file():
        raise SiteLayoutError(f"找不到图签模板：{path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise SiteLayoutError(f"无法读取图签模板：{path}：{exc}") from exc
    if not isinstance(data, dict):
        raise SiteLayoutError("图签模板顶层必须是对象")
    for key, value in overrides.items():
        if value not in (None, ""):
            data[key] = value
    data.setdefault("title", "施工平面布置图")
    data.setdefault("drawing_no", "SLP-01")
    data.setdefault("scale", "1:500")
    data.setdefault("sheet_size", "A2")
    data.setdefault("revision", "0")
    data.setdefault("disclaimer", "本图为布置草案，须经项目技术负责人审核；不替代施工方案审批、设计签章和现场试吊。")
    data["_template_path"] = str(path)
    return data


def _ensure_safe_out_dir(out_value: str, site: SiteData) -> Path:
    out_dir = Path(out_value).expanduser().resolve()
    source = site.source_path.resolve()
    if out_dir == source.parent:
        raise DrawGateError("--out-dir 不能等于原图目录；请换到独立输出目录")
    if out_dir == source:
        raise DrawGateError("--out-dir 不能指向原图文件")
    return out_dir


def _create_doc() -> Any:
    doc = ezdxf.new("R2010", setup=True)
    doc.units = ezdxf.units.MM
    doc.header["$INSUNITS"] = 4
    doc.header["$MEASUREMENT"] = 1
    if not doc.styles.has_entry("LAYOUT-TEXT"):
        doc.styles.add("LAYOUT-TEXT", font="simsun.ttc")
    for name, color, linetype, _purpose in REQUIRED_LAYERS:
        if not doc.layers.has_entry(name):
            doc.layers.add(name, color=color, linetype=linetype)
    return doc


def finalize_doc_extents(doc: Any) -> bool:
    """写入图纸范围（0.6.7）。

    ezdxf 的 saveas -> update_all() 会用模型空间布局的 dxf.extmin/extmax 覆盖
    HEADER 的 $EXTMIN/$EXTMAX；只改 header 不生效，必须同时写 msp.dxf.extmin。
    默认值 1e+20 哨兵值会让部分看图软件（CAD快速看图等）按空图纸打开、只显黑屏。
    这里按模型空间实际包围盒写回布局范围与 HEADER，并留 1% 余量。
    """
    try:
        from ezdxf import bbox as ezbbox

        msp = doc.modelspace()
        box = ezbbox.extents(msp, fast=False)
        xmin, ymin = float(box.extmin.x), float(box.extmin.y)
        xmax, ymax = float(box.extmax.x), float(box.extmax.y)
    except Exception:
        return False
    if not all(math.isfinite(v) for v in (xmin, ymin, xmax, ymax)):
        return False
    if xmax <= xmin and ymax <= ymin:
        return False
    pad = max(xmax - xmin, ymax - ymin) * 0.01 or 1.0
    extmin = (xmin - pad, ymin - pad, 0.0)
    extmax = (xmax + pad, ymax + pad, 0.0)
    # 关键：布局 DXF 属性，saveas 时由 update_all() 回写 HEADER
    msp.dxf.extmin = extmin
    msp.dxf.extmax = extmax
    msp.dxf.limmin = (extmin[0], extmin[1])
    msp.dxf.limmax = (extmax[0], extmax[1])
    doc.header["$EXTMIN"] = extmin
    doc.header["$EXTMAX"] = extmax
    doc.header["$LIMMIN"] = (extmin[0], extmin[1])
    doc.header["$LIMMAX"] = (extmax[0], extmax[1])
    # 部分国产看图软件（CAD快速看图）打开后不执行 zoom-extents，
    # 只按 VPORT *Active 的中心/高度定位；不写就会出现“打开全黑/只看到一角”。
    try:
        entries = doc.viewports.get("*Active")
        if entries:
            vp = entries[0]
            width = extmax[0] - extmin[0]
            height = extmax[1] - extmin[1]
            aspect = 1.6
            view_height = max(height, width / aspect, 1.0) * 1.02
            vp.dxf.center = ((extmin[0] + extmax[0]) / 2.0,
                             (extmin[1] + extmax[1]) / 2.0)
            vp.dxf.height = view_height
            vp.dxf.aspect_ratio = aspect
            doc.header["$VIEWCTR"] = (vp.dxf.center[0], vp.dxf.center[1], 0.0)
            doc.header["$VIEWSIZE"] = view_height
    except Exception:
        pass
    return True


def _entity_anchor(entity: Any) -> List[float]:
    try:
        kind = entity.dxftype()
        if kind == "LINE":
            return [round(float(entity.dxf.start.x), 3), round(float(entity.dxf.start.y), 3)]
        if kind in ("LWPOLYLINE", "POLYLINE"):
            pts = _entity_points(entity, 1.0)
            return [round(pts[0][0], 3), round(pts[0][1], 3)] if pts else []
        if kind in ("CIRCLE", "ARC"):
            return [round(float(entity.dxf.center.x), 3), round(float(entity.dxf.center.y), 3)]
        if kind in ("TEXT", "MTEXT", "INSERT", "POINT"):
            loc = entity.dxf.insert if kind != "POINT" else entity.dxf.location
            return [round(float(loc.x), 3), round(float(loc.y), 3)]
    except Exception:
        return []
    return []


def _copy_base_geometry(doc: Any, site: SiteData) -> List[str]:
    msp = doc.modelspace()
    warnings: List[str] = []
    copied = 0
    for entity in site.base_entities:
        try:
            msp.add_foreign_entity(entity, copy=True)
            created = msp[-1]
            created.dxf.layer = "BASE-底图"
            created.dxf.color = 8
            copied += 1
        except Exception as exc:
            warnings.append(f"底图实体 {entity.dxftype()} 未复制：{exc}")
    if copied == 0:
        for x1, y1, x2, y2 in site.base_segments:
            msp.add_line((x1, y1), (x2, y2), dxfattribs={"layer": "BASE-底图", "color": 8})
            copied += 1
    if copied == 0:
        warnings.append("原图没有可绘制几何；BASE-底图 为空")
    return warnings


def _add_text(msp: Any, text: str, x: float, y: float, height: float, layer: str, color: int = 7) -> Any:
    return msp.add_text(
        text,
        height=height,
        dxfattribs={"layer": layer, "color": color, "style": "LAYOUT-TEXT"},
    ).set_placement((x, y))


def _frame_for(site: SiteData, cranes: Sequence[CraneSpec], titleblock_w: float, titleblock_h: float) -> Tuple[Tuple[float, float, float, float], Tuple[float, float, float, float]]:
    base = site.extents or (0.0, 0.0, 100000.0, 60000.0)
    points = [(base[0], base[1]), (base[2], base[3])]
    for crane in cranes:
        points.extend(
            [
                (crane.x_mm - crane.jib_mm, crane.y_mm - crane.jib_mm),
                (crane.x_mm + crane.jib_mm, crane.y_mm + crane.jib_mm),
            ]
        )
    bbox = _bbox_points(points) or (0.0, 0.0, 100000.0, 60000.0)
    margin = 25000.0
    x0, y0 = bbox[0] - margin, bbox[1] - margin
    x1, y1 = bbox[2] + margin, bbox[3] + margin
    if x1 - x0 < titleblock_w + 40000.0:
        x1 = x0 + titleblock_w + 40000.0
    if y1 - y0 < titleblock_h + 30000.0:
        y1 = y0 + titleblock_h + 30000.0
    tb_x = x1 - titleblock_w - 3000.0
    tb_y = y0 + 3000.0
    return (x0, y0, x1, y1), (tb_x, tb_y, tb_x + titleblock_w, tb_y + titleblock_h)


def _split_text(text: str, width: int) -> List[str]:
    if len(text) <= width:
        return [text]
    return [text[i : i + width] for i in range(0, len(text), width)]


def _draw_titleblock(msp: Any, titleblock: Dict[str, Any], bbox: Tuple[float, float, float, float], draft_label: str) -> None:
    x0, y0, x1, y1 = bbox
    msp.add_lwpolyline(
        [(x0, y0), (x1, y0), (x1, y1), (x0, y1)],
        close=True,
        dxfattribs={"layer": "META-图签", "color": 7},
    )
    width = x1 - x0
    height = y1 - y0
    _add_text(msp, _safe_text(titleblock.get("title"), "施工平面布置图"), x0 + 2000, y1 - 5000, 3200, "META-图签", 7)
    if draft_label:
        _add_text(msp, draft_label, x0 + 2000, y1 - 10000, 2400, "META-图签", 1)
    lines = [
        "图号 {}  比例 {}  图幅 {}  版本 {}".format(
            _safe_text(titleblock.get("drawing_no"), "—"),
            _safe_text(titleblock.get("scale"), "—"),
            _safe_text(titleblock.get("sheet_size"), "—"),
            _safe_text(titleblock.get("revision"), "—"),
        ),
        "contract_id: {}".format(_safe_text(titleblock.get("contract_id"), "缺失")),
        "技能版本 {}  日期 {}".format(_safe_text(titleblock.get("version"), VERSION), _safe_text(titleblock.get("date"), "")),
        "项目: {}".format(_safe_text(titleblock.get("project"), "—")),
    ]
    y = y1 - 13500
    for line in lines:
        _add_text(msp, line, x0 + 2000, y, 1700, "META-图签", 7)
        y -= 2600
    disclaimer = titleblock.get("disclaimer") or ""
    for line in _split_text(disclaimer, 38):
        _add_text(msp, line, x0 + 2000, max(y0 + 1500, y), 1400, "META-图签", 7)
        y -= 1900


def _draw_layout(doc: Any, site: SiteData, cranes: Sequence[CraneSpec], check_data: Dict[str, Any], frame: Tuple[float, float, float, float], titleblock_bbox: Tuple[float, float, float, float], titleblock: Dict[str, Any], draft_label: str) -> Dict[str, int]:
    msp = doc.modelspace()
    base_warnings = _copy_base_geometry(doc, site)
    site.warnings.extend(base_warnings)
    # 图框：不进入 layers.csv 的固定 8 层之外，仍放 META-图签。
    x0, y0, x1, y1 = frame
    msp.add_lwpolyline(
        [(x0, y0), (x1, y0), (x1, y1), (x0, y1)],
        close=True,
        dxfattribs={"layer": "META-图签", "color": 7},
    )
    drawn: Dict[str, int] = {name: 0 for name in REQUIRED_LAYER_NAMES}
    drawn["BASE-底图"] = len(msp.query('*[layer=="BASE-底图"]'))
    for index, crane in enumerate(cranes):
        color = CRANE_COLORS[index % len(CRANE_COLORS)]
        msp.add_circle(
            (crane.x_mm, crane.y_mm),
            crane.jib_mm,
            dxfattribs={"layer": "CRANE-覆盖", "color": color, "linetype": "DASHED"},
        )
        drawn["CRANE-覆盖"] += 1
        d = 3500.0
        msp.add_line((crane.x_mm - d, crane.y_mm), (crane.x_mm + d, crane.y_mm), dxfattribs={"layer": "CRANE-塔吊", "color": color})
        msp.add_line((crane.x_mm, crane.y_mm - d), (crane.x_mm, crane.y_mm + d), dxfattribs={"layer": "CRANE-塔吊", "color": color})
        msp.add_circle((crane.x_mm, crane.y_mm), 6200.0, dxfattribs={"layer": "CRANE-塔吊", "color": color})
        drawn["CRANE-塔吊"] += 3
        _add_text(msp, "{} {} 臂长{:.0f}m".format(crane.id, crane.model, crane.jib_mm / 1000.0), crane.x_mm + 7000.0, crane.y_mm + 7000.0, 2200, "CRANE-塔吊", color)
        drawn["CRANE-塔吊"] += 1

    members = check_data.get("members")
    if not isinstance(members, list):
        members = []
    for row in members:
        if not isinstance(row, dict):
            continue
        if row.get("x_m") is None or row.get("y_m") is None:
            continue
        x = float(row["x_m"]) * 1000.0
        y = float(row["y_m"]) * 1000.0
        conclusion = _safe_text(row.get("conclusion"), "unknown_no_table")
        layer = MEMBER_LAYER.get(conclusion, "LIFT-盲区")
        color = {"LIFT-合格": 3, "LIFT-超载": 1, "LIFT-盲区": 2}.get(layer, 7)
        msp.add_circle((x, y), 900.0, dxfattribs={"layer": layer, "color": color})
        drawn[layer] += 1
        demand = row.get("demand_t")
        capacity = row.get("capacity_t")
        utilization = row.get("utilization")
        label = "{} 需求/额定 {} / {} t  利用率 {}".format(
            _safe_text(row.get("id"), "—"),
            "—" if demand is None else "{:.2f}".format(float(demand)),
            "—" if capacity is None else "{:.2f}".format(float(capacity)),
            "—" if utilization is None else "{:.3f}".format(float(utilization)),
        )
        _add_text(msp, label, x + 1300.0, y + 1300.0, 1500, "TEXT-结论", 7)
        drawn["TEXT-结论"] += 1

    _draw_titleblock(msp, titleblock, titleblock_bbox, draft_label)
    drawn["META-图签"] = len(msp.query('*[layer=="META-图签"]'))
    return drawn


def _font_candidates() -> List[Path]:
    return [
        Path("/System/Library/Fonts/PingFang.ttc"),
        Path("/System/Library/Fonts/Hiragino Sans GB.ttc"),
        Path("/System/Library/Fonts/STHeiti Light.ttc"),
        Path("/System/Library/Fonts/Supplemental/Songti.ttc"),
        Path("/Library/Fonts/Arial Unicode.ttf"),
        Path("C:/Windows/Fonts/msyh.ttc"),
        Path("C:/Windows/Fonts/simsun.ttc"),
        Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"),
        Path("/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"),
    ]


def _pick_font(size: int) -> Tuple[Any, str, str]:
    from PIL import ImageFont

    for candidate in _font_candidates():
        if candidate.is_file():
            try:
                return ImageFont.truetype(str(candidate), size=size, index=0), "ok", str(candidate)
            except Exception:
                continue
    try:
        return ImageFont.load_default(size=size), "degraded", "Pillow default"
    except Exception:
        return ImageFont.load_default(), "degraded", "Pillow default"


def _png_safe(text: str, degraded: bool) -> str:
    if not degraded:
        return text
    return "".join(ch if ord(ch) < 128 else "?" for ch in text)


def _render_png(
    site: SiteData,
    cranes: Sequence[CraneSpec],
    check_data: Dict[str, Any],
    frame: Tuple[float, float, float, float],
    titleblock: Dict[str, Any],
    draft_label: str,
    path: Path,
) -> Dict[str, Any]:
    from PIL import Image, ImageDraw

    width, height = 2600, 1800
    map_bottom = 1270
    margin = 60
    x0, y0, x1, y1 = frame
    span_x = max(1.0, x1 - x0)
    span_y = max(1.0, y1 - y0)
    scale = min((width - 2 * margin) / span_x, (map_bottom - 2 * margin) / span_y)
    offset_x = margin + ((width - 2 * margin) - span_x * scale) / 2.0
    top_y = margin + ((map_bottom - 2 * margin) - span_y * scale) / 2.0

    def tx(x: float) -> float:
        return offset_x + (x - x0) * scale

    def ty(y: float) -> float:
        return top_y + (y1 - y) * scale

    image = Image.new("RGB", (width, height), "#f7f7f4")
    draw = ImageDraw.Draw(image)
    font_small, font_status, font_path = _pick_font(21)
    font_mid, _s, _p = _pick_font(28)
    font_title, _s, _p = _pick_font(48)
    font_draft, _s, _p = _pick_font(120)
    degraded = font_status == "degraded"

    if site.base_segments:
        for sx1, sy1, sx2, sy2 in site.base_segments:
            draw.line((tx(sx1), ty(sy1), tx(sx2), ty(sy2)), fill="#9a9a9a", width=2)
    if site.redline_vertices:
        pts = [(tx(x), ty(y)) for x, y in site.redline_vertices]
        if len(pts) >= 2:
            draw.line(pts + [pts[0]], fill="#c0392b", width=4)
    if site.fence_vertices:
        pts = [(tx(x), ty(y)) for x, y in site.fence_vertices]
        if len(pts) >= 2:
            draw.line(pts + [pts[0]], fill="#7f5a3a", width=3)

    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    odraw = ImageDraw.Draw(overlay)
    for index, crane in enumerate(cranes):
        color = (220, 50, 47) if index % 3 == 0 else ((46, 125, 50) if index % 3 == 1 else (33, 103, 184))
        box = (tx(crane.x_mm - crane.jib_mm), ty(crane.y_mm + crane.jib_mm), tx(crane.x_mm + crane.jib_mm), ty(crane.y_mm - crane.jib_mm))
        odraw.ellipse(box, fill=color + (30,), outline=color + (200,), width=3)
    image = Image.alpha_composite(image.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(image)

    for crane in cranes:
        cx, cy = tx(crane.x_mm), ty(crane.y_mm)
        draw.line((cx - 12, cy, cx + 12, cy), fill="#b71c1c", width=4)
        draw.line((cx, cy - 12, cx, cy + 12), fill="#b71c1c", width=4)
        draw.ellipse((cx - 16, cy - 16, cx + 16, cy + 16), outline="#b71c1c", width=3)
        draw.text((cx + 20, cy - 34), _png_safe("{} {}".format(crane.id, crane.model), degraded), fill="#b71c1c", font=font_mid)

    members = check_data.get("members") if isinstance(check_data.get("members"), list) else []
    for row in members:
        if not isinstance(row, dict) or row.get("x_m") is None or row.get("y_m") is None:
            continue
        x, y = tx(float(row["x_m"]) * 1000.0), ty(float(row["y_m"]) * 1000.0)
        conclusion = _safe_text(row.get("conclusion"), "unknown_no_table")
        fill = {"ok": "#2e7d32", "insufficient": "#c62828", "out_of_range": "#c62828"}.get(conclusion, "#f9a825")
        draw.ellipse((x - 7, y - 7, x + 7, y + 7), fill=fill, outline="#222222", width=1)
        label = "{} {}/{}t".format(
            _safe_text(row.get("id"), "—"),
            "—" if row.get("demand_t") is None else "{:.1f}".format(float(row["demand_t"])),
            "—" if row.get("capacity_t") is None else "{:.1f}".format(float(row["capacity_t"])),
        )
        draw.text((x + 10, y - 22), _png_safe(label, degraded), fill="#222222", font=font_small)

    if draft_label:
        draw.text((width - 700, 80), _png_safe("DRAFT", degraded), fill=(190, 30, 30, 100), font=font_draft)

    tb_top = 1300
    draw.rectangle((30, tb_top, width - 30, height - 30), outline="#222222", width=3, fill="#ffffff")
    draw.text((55, tb_top + 22), _png_safe(_safe_text(titleblock.get("title"), "施工平面布置图"), degraded), fill="#111111", font=font_title)
    if draft_label:
        draw.text((width - 850, tb_top + 28), _png_safe(draft_label, degraded), fill="#c62828", font=font_mid)
    info_lines = [
        "图号 {}    比例 {}    图幅 {}    版本 {}".format(
            _safe_text(titleblock.get("drawing_no"), "—"),
            _safe_text(titleblock.get("scale"), "—"),
            _safe_text(titleblock.get("sheet_size"), "—"),
            _safe_text(titleblock.get("revision"), "—"),
        ),
        "contract_id: {}    技能版本 {}    日期 {}".format(
            _safe_text(titleblock.get("contract_id"), "缺失"),
            _safe_text(titleblock.get("version"), VERSION),
            _safe_text(titleblock.get("date"), ""),
        ),
        "项目: {}    字体: {}".format(_safe_text(titleblock.get("project"), "—"), ("已找到" if not degraded else "降级")),
    ]
    y = tb_top + 95
    for line in info_lines:
        draw.text((55, y), _png_safe(line, degraded), fill="#222222", font=font_mid)
        y += 40
    disclaimer = _safe_text(titleblock.get("disclaimer"), "")
    for line in _split_text(disclaimer, 54):
        draw.text((55, y), _png_safe(line, degraded), fill="#555555", font=font_small)
        y += 26
    image.save(path, "PNG", dpi=(200, 200), optimize=True)
    return {"font_status": font_status, "font_path": font_path, "dpi": 200, "pixel_size": [width, height]}


def _text_bbox(entity: Any) -> Optional[Tuple[float, float, float, float]]:
    try:
        if entity.dxftype() == "TEXT":
            text = str(entity.dxf.text or "")
            height = float(entity.dxf.height)
            insert = entity.dxf.insert
            lines = text.splitlines() or [text]
        elif entity.dxftype() == "MTEXT":
            text = str(entity.text or "")
            height = float(entity.dxf.char_height)
            insert = entity.dxf.insert
            lines = text.splitlines() or [text]
        else:
            return None
        width_factor = 0.0
        for line in lines:
            width_factor = max(width_factor, sum(1.0 if ord(ch) > 127 else 0.62 for ch in line))
        width = max(0.1, width_factor) * height
        total_height = max(1, len(lines)) * height * 1.35
        x, y = float(insert.x), float(insert.y)
        return (x, y - height * 0.2, x + width, y + total_height)
    except Exception:
        return None


def _audit_doc(doc: Any) -> Dict[str, Any]:
    try:
        auditor = doc.audit()
        errors = [str(item) for item in auditor.errors]
        fixes = [str(item) for item in auditor.fixes]
        return {"errors": errors, "fixes": fixes, "error_count": len(errors), "fix_count": len(fixes)}
    except Exception as exc:
        return {"errors": [str(exc)], "fixes": [], "error_count": 1, "fix_count": 0}


def _point_in_polygon(point: Tuple[float, float], polygon: Sequence[Tuple[float, float]], tolerance_mm: float = 50.0) -> Tuple[bool, bool]:
    x, y = point
    inside = False
    on_boundary = False
    if len(polygon) < 3:
        return False, False
    for index, left in enumerate(polygon):
        right = polygon[(index + 1) % len(polygon)]
        if _distance_point_segment(point, left, right) <= tolerance_mm:
            on_boundary = True
        if (left[1] > y) != (right[1] > y):
            x_intersection = (right[0] - left[0]) * (y - left[1]) / (right[1] - left[1]) + left[0]
            if x < x_intersection:
                inside = not inside
    return inside or on_boundary, on_boundary


def _distance_point_segment(point: Tuple[float, float], left: Tuple[float, float], right: Tuple[float, float]) -> float:
    px, py = point
    x1, y1 = left
    x2, y2 = right
    dx, dy = x2 - x1, y2 - y1
    if dx == 0 and dy == 0:
        return math.hypot(px - x1, py - y1)
    t = max(0.0, min(1.0, ((px - x1) * dx + (py - y1) * dy) / (dx * dx + dy * dy)))
    return math.hypot(px - (x1 + t * dx), py - (y1 + t * dy))


def _segment_samples(vertices: Sequence[Tuple[float, float]]) -> List[Tuple[float, float, float, float]]:
    if len(vertices) < 2:
        return []
    segments = [(vertices[i][0], vertices[i][1], vertices[i + 1][0], vertices[i + 1][1]) for i in range(len(vertices) - 1)]
    if vertices[0] != vertices[-1]:
        segments.append((vertices[-1][0], vertices[-1][1], vertices[0][0], vertices[0][1]))
    return segments


def _circle_crossings(crane: CraneSpec, boundary: Sequence[Tuple[float, float]], name: str) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    if len(boundary) < 2:
        return rows
    for seg in _segment_samples(boundary):
        distance = _distance_point_segment((crane.x_mm, crane.y_mm), (seg[0], seg[1]), (seg[2], seg[3]))
        if distance < crane.jib_mm - 1e-6:
            rows.append({"boundary": name, "segment_mm": [round(v, 3) for v in seg], "distance_mm": round(distance, 3)})
    return rows


def _selfcheck_item(item_id: int, name: str, status: str, evidence: Dict[str, Any], message: str = "") -> Dict[str, Any]:
    return {"id": item_id, "name": name, "status": status, "message": message, "evidence": evidence}


def _build_selfcheck(
    site: SiteData,
    cranes: Sequence[CraneSpec],
    check_data: Dict[str, Any],
    dxf_path: Path,
    titleblock: Dict[str, Any],
    frame: Tuple[float, float, float, float],
    titleblock_bbox: Tuple[float, float, float, float],
    draft_label: str,
    drawn: Dict[str, int],
    png_info: Dict[str, Any],
) -> Dict[str, Any]:
    items: List[Dict[str, Any]] = []
    if len(site.redline_vertices) >= 3 and site.redline_closed:
        status = "pass"
    else:
        status = "fail"
    items.append(
        _selfcheck_item(
            1,
            "红线闭合（容差 50 mm）",
            status,
            {
                "coordinate_system": "mm",
                "tolerance_mm": 50.0,
                "closed": site.redline_closed,
                "gap_mm": None if site.redline_gap_mm is None else round(site.redline_gap_mm, 3),
                "vertex_count": len(site.redline_vertices),
                "vertices_mm": [[round(x, 3), round(y, 3)] for x, y in site.redline_vertices[:20]],
                "area_mm2": round(_polyline_area(site.redline_vertices), 3),
            },
        )
    )

    if not site.redline_vertices:
        status = "fail"
        outside: List[Dict[str, Any]] = []
    else:
        outside = []
        for crane in cranes:
            inside, on_boundary = _point_in_polygon((crane.x_mm, crane.y_mm), site.redline_vertices, 50.0)
            if not inside:
                outside.append({"crane_id": crane.id, "center_mm": [round(crane.x_mm, 3), round(crane.y_mm, 3)]})
            else:
                outside.append({"crane_id": crane.id, "center_mm": [round(crane.x_mm, 3), round(crane.y_mm, 3)], "inside": True, "on_boundary": on_boundary})
        status = "pass" if not any(not row.get("inside", False) for row in outside) else "fail"
    items.append(_selfcheck_item(2, "塔吊中心落在场地范围内", status, {"coordinate_system": "mm", "cranes": outside, "redline_bbox_mm": site.extents}))

    crossing_rows: List[Dict[str, Any]] = []
    for crane in cranes:
        row: Dict[str, Any] = {"crane_id": crane.id, "center_mm": [round(crane.x_mm, 3), round(crane.y_mm, 3)], "jib_mm": round(crane.jib_mm, 3)}
        row["redline_crossings"] = _circle_crossings(crane, site.redline_vertices, "redline") if site.redline_vertices else []
        row["fence_crossings"] = _circle_crossings(crane, site.fence_vertices, "fence") if site.fence_vertices else []
        crossing_rows.append(row)
    if not site.redline_vertices and not site.fence_vertices:
        status = "manual"
        cross_message = "缺少红线/围挡，无法判断幅度圆越界"
    elif any(row["redline_crossings"] or row["fence_crossings"] for row in crossing_rows):
        status = "manual"
        cross_message = "幅度圆越过红线/围挡；仅提示，不自动判违规"
    else:
        status = "pass"
        cross_message = ""
    items.append(_selfcheck_item(3, "幅度圆越过红线/围挡（提示）", status, {"coordinate_system": "mm", "cranes": crossing_rows}, cross_message))

    expected_blind = None
    try:
        expected_blind = int((check_data.get("summary") or {}).get("blind"))
    except (TypeError, ValueError):
        expected_blind = None
    blind_rows = [row for row in check_data.get("members", []) if isinstance(row, dict) and row.get("conclusion") == "blind"]
    blind_with_coords = [
        row for row in blind_rows if row.get("x_m") is not None and row.get("y_m") is not None
    ]
    drawn_blind = drawn.get("LIFT-盲区", 0)
    blind_consistent = expected_blind is not None and expected_blind == len(blind_rows)
    blind_drawn = drawn_blind >= len(blind_with_coords)
    status = "pass" if blind_consistent and blind_drawn else "fail"
    items.append(
        _selfcheck_item(
            4,
            "盲区柱数量与 crane_check 一致",
            status,
            {
                "coordinate_system": "mm",
                "expected_summary_blind": expected_blind,
                "check_blind_members": len(blind_rows),
                "drawn_LIFT_盲区_entities": drawn_blind,
                "blind_member_coords_mm": [
                    [round(float(row["x_m"]) * 1000.0, 3), round(float(row["y_m"]) * 1000.0, 3)]
                    for row in blind_rows
                    if row.get("x_m") is not None and row.get("y_m") is not None
                ],
            },
        )
    )

    out_doc = ezdxf.readfile(str(dxf_path))
    layer_names = {layer.dxf.name for layer in out_doc.layers}
    missing = [name for name in REQUIRED_LAYER_NAMES if name not in layer_names]
    msp = out_doc.modelspace()
    layer_evidence: Dict[str, Any] = {}
    for name in REQUIRED_LAYER_NAMES:
        entities = list(msp.query('*[layer=="{}"]'.format(name)))
        layer_evidence[name] = {
            "entity_count": len(entities),
            "sample_coord_mm": _entity_anchor(entities[0]) if entities else None,
        }
    audit = _audit_doc(out_doc)
    audit_ok = audit["error_count"] == 0
    status = "pass" if not missing and audit_ok else "fail"
    items.append(
        _selfcheck_item(
            5,
            "8 个必备图层齐全",
            status,
            {
                "required_layers": list(REQUIRED_LAYER_NAMES),
                "missing_layers": missing,
                "layers": layer_evidence,
                "frame_bbox_mm": [round(v, 3) for v in frame],
                "dxf_audit_errors": audit["error_count"],
            },
            "" if audit_ok else "DXF audit 存在错误",
        )
    )

    text_rows: List[Dict[str, Any]] = []
    overflow: List[Dict[str, Any]] = []
    for entity in msp.query("TEXT MTEXT"):
        if entity.dxf.layer not in ("TEXT-结论", "META-图签"):
            continue
        bbox = _text_bbox(entity)
        if bbox is None:
            continue
        x0, y0, x1, y1 = frame
        text_value = str(getattr(entity.dxf, "text", "")) if entity.dxftype() == "TEXT" else str(entity.text)
        outside = bbox[0] < x0 - 1 or bbox[1] < y0 - 1 or bbox[2] > x1 + 1 or bbox[3] > y1 + 1
        row = {"layer": entity.dxf.layer, "text": text_value[:80], "bbox_mm": [round(v, 3) for v in bbox]}
        text_rows.append(row)
        if outside:
            overflow.append(row)
    if overflow:
        text_status = "fail"
        text_message = "文字粗略包围盒超出图框"
    elif png_info.get("font_status") == "degraded":
        text_status = "manual"
        text_message = "中文字体缺失，PNG 已降级为 ASCII；DXF 中文仍在"
    else:
        text_status = "pass"
        text_message = ""
    items.append(
        _selfcheck_item(
            6,
            "文字不溢出图框（粗略包围盒）",
            text_status,
            {
                "coordinate_system": "mm",
                "frame_bbox_mm": [round(v, 3) for v in frame],
                "texts_checked": len(text_rows),
                "overflow_count": len(overflow),
                "overflow": overflow[:10],
                "font_status": png_info.get("font_status"),
                "font_path": png_info.get("font_path"),
            },
            text_message,
        )
    )

    try:
        out_insunits = int(out_doc.header.get("$INSUNITS", 0))
    except (TypeError, ValueError):
        out_insunits = 0
    unit_ok = out_insunits == 4 and site.source_units in ("mm", "m")
    items.append(
        _selfcheck_item(
            7,
            "单位一致性（mm）",
            "pass" if unit_ok else "fail",
            {
                "coordinate_system": "mm",
                "source_units": site.source_units,
                "mm_per_source_unit": site.mm_per_unit,
                "output_insunits": out_insunits,
                "output_expected_insunits": 4,
                "handoff_coord_unit": "m",
                "origin_mm": [0, 0],
            },
        )
    )

    final_check = bool(check_data.get("final_check"))
    expected_draft = bool(draft_label)
    actual_draft = bool(titleblock.get("draft"))
    status = "pass" if expected_draft == actual_draft and _safe_text(titleblock.get("draft_label")) == draft_label else "fail"
    items.append(
        _selfcheck_item(
            8,
            "DRAFT 标识与输入状态匹配",
            status,
            {
                "coordinate_system": "mm",
                "final_check": final_check,
                "input_contract_mismatch": bool(titleblock.get("contract_mismatch")),
                "expected_draft": expected_draft,
                "expected_label": draft_label,
                "titleblock_draft": actual_draft,
                "titleblock_label": titleblock.get("draft_label", ""),
                "titleblock_bbox_mm": [round(v, 3) for v in titleblock_bbox],
            },
        )
    )

    summary = {"pass": 0, "fail": 0, "manual": 0}
    for item in items:
        summary[item["status"]] += 1
    return {
        "schema": SCHEMA,
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "items": items,
        "summary": summary,
        "exit_code": 5 if summary["fail"] else 0,
    }


def _write_layers_csv(doc: Any, path: Path) -> None:
    msp = doc.modelspace()
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["图层", "颜色", "线型", "用途", "实体数", "样点坐标_mm"])
        for name, color, linetype, purpose in REQUIRED_LAYERS:
            entities = list(msp.query('*[layer=="{}"]'.format(name)))
            writer.writerow([name, color, linetype, purpose, len(entities), _entity_anchor(entities[0]) if entities else ""])


def _titleblock_payload(
    params: Dict[str, Any],
    site: SiteData,
    contract_ids: Dict[str, str],
    mismatch_reason: str,
    draft_label: str,
    check_data: Dict[str, Any],
    baseline: Any,
    check_path: Path,
    layout_path: str,
    source_before: str,
    source_after: str,
    png_info: Dict[str, Any],
) -> Dict[str, Any]:
    payload = {
        "schema": TITLEBLOCK_SCHEMA,
        "title": _safe_text(params.get("title"), "施工平面布置图"),
        "drawing_no": _safe_text(params.get("drawing_no"), "SLP-01"),
        "scale": _safe_text(params.get("scale"), "1:500"),
        "sheet_size": _safe_text(params.get("sheet_size"), "A2"),
        "revision": _safe_text(params.get("revision"), "0"),
        "date": _safe_text(params.get("date"), datetime.now().strftime("%Y-%m-%d")),
        "version": VERSION,
        "project": _safe_text(params.get("project")),
        "contract_id": contract_ids.get("site", ""),
        "contract_ids": contract_ids,
        "contract_ids_differ": len({v for v in contract_ids.values() if v}) > 1,
        "contract_mismatch": bool(mismatch_reason),
        "contract_mismatch_reason": mismatch_reason,
        "draft": bool(draft_label),
        "draft_label": draft_label,
        "final_check": bool(check_data.get("final_check")),
        "baseline": {
            "fleet_source": getattr(baseline, "fleet_source", ""),
            "fleet_version": getattr(baseline, "fleet_version", ""),
            "coverage_criteria": getattr(baseline, "coverage_criteria", ""),
            "locked_by": getattr(baseline, "locked_by", ""),
            "locked_at": getattr(baseline, "locked_at", ""),
        },
        "source_path": str(site.source_path),
        "source_kind": site.source_kind,
        "source_units": site.source_units,
        "mm_per_source_unit": site.mm_per_unit,
        "source_sha256_before": source_before,
        "source_sha256_after": source_after,
        "source_unchanged": source_before == source_after,
        "check_path": str(check_path),
        "layout_path": layout_path,
        "disclaimer": _safe_text(params.get("disclaimer")),
        "template_path": _safe_text(params.get("_template_path")),
        "font": png_info,
        "layers": [name for name, _c, _l, _p in REQUIRED_LAYERS],
    }
    return payload


def draw_layout(
    *,
    site_path: str,
    handoff_path: str,
    check_path: str,
    baseline_path: str,
    out_dir: str,
    layout_path: Optional[str] = None,
    titleblock_path: Optional[str] = None,
    draft: bool = False,
    title: Optional[str] = None,
    drawing_no: Optional[str] = None,
    scale: Optional[str] = None,
    date: Optional[str] = None,
    project: Optional[str] = None,
    revision: Optional[str] = None,
    site_contract_id: Optional[str] = None,
) -> Dict[str, Any]:
    baseline = load_baseline(baseline_path)
    baseline.assert_locked()
    handoff = load_handoff(handoff_path)
    check_data, check_file, _check_sha = _load_json(check_path, "crane_check")
    if _safe_text(check_data.get("schema")) != "crane-check/v1":
        raise SiteLayoutError("crane_check.schema 必须是 crane-check/v1")
    site = load_site(site_path)
    if not site.contract_id and site_contract_id:
        site.contract_id = _safe_text(site_contract_id)
        site.contract_id_source = "cli"
    cranes, resolved_layout_path, layout_contract = load_layout(layout_path, site.source_path, check_data)
    mismatch, contract_ids, mismatch_reason = _check_contract_ids(
        site.contract_id, handoff.contract_id, _safe_text((check_data.get("inputs") or {}).get("contract_id")), layout_contract, draft
    )
    label = _draft_label(bool(check_data.get("final_check")), mismatch, draft)
    out = _ensure_safe_out_dir(out_dir, site)
    out.mkdir(parents=True, exist_ok=True)
    dxf_path = out / "layout.dxf"
    png_path = out / "layout.png"
    csv_path = out / "layers.csv"
    title_path = out / "titleblock.json"
    selfcheck_path = out / "selfcheck.json"

    params = _titleblock_params(
        titleblock_path,
        {
            "title": title,
            "drawing_no": drawing_no,
            "scale": scale,
            "date": date or datetime.now().strftime("%Y-%m-%d"),
            "project": project or handoff.project,
            "revision": revision,
            "contract_id": site.contract_id,
            "version": VERSION,
            "draft_label": label,
        },
    )
    titleblock_w, titleblock_h = 90000.0, 30000.0
    frame, titleblock_bbox = _frame_for(site, cranes, titleblock_w, titleblock_h)
    doc = _create_doc()
    drawn = _draw_layout(doc, site, cranes, check_data, frame, titleblock_bbox, params, label)
    finalize_doc_extents(doc)
    doc.saveas(dxf_path)
    saved = ezdxf.readfile(str(dxf_path))
    audit = _audit_doc(saved)
    _write_layers_csv(saved, csv_path)
    png_info = _render_png(site, cranes, check_data, frame, params, label, png_path)
    source_after = _sha256(site.source_path)
    titleblock = _titleblock_payload(
        params,
        site,
        contract_ids,
        mismatch_reason,
        label,
        check_data,
        baseline,
        check_file,
        resolved_layout_path,
        site.source_sha256,
        source_after,
        png_info,
    )
    titleblock["dxf_audit"] = audit
    titleblock["titleblock_bbox_mm"] = [round(v, 3) for v in titleblock_bbox]
    titleblock["frame_bbox_mm"] = [round(v, 3) for v in frame]
    title_path.write_text(json.dumps(titleblock, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    selfcheck = _build_selfcheck(
        site, cranes, check_data, dxf_path, titleblock, frame, titleblock_bbox, label, drawn, png_info
    )
    selfcheck["source_sha256_before"] = site.source_sha256
    selfcheck["source_sha256_after"] = source_after
    selfcheck["source_unchanged"] = site.source_sha256 == source_after
    selfcheck["dxf_audit"] = audit
    selfcheck_path.write_text(json.dumps(selfcheck, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    exit_code = 5 if selfcheck["summary"]["fail"] or site.source_sha256 != source_after else 0
    selfcheck["exit_code"] = exit_code
    selfcheck_path.write_text(json.dumps(selfcheck, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {
        "out_dir": str(out),
        "dxf": str(dxf_path),
        "png": str(png_path),
        "layers_csv": str(csv_path),
        "titleblock": str(title_path),
        "selfcheck": str(selfcheck_path),
        "draft_label": label,
        "contract_mismatch": mismatch,
        "summary": selfcheck.get("summary", {}),
        "exit_code": exit_code,
        "source_sha256_before": site.source_sha256,
        "source_sha256_after": source_after,
    }
