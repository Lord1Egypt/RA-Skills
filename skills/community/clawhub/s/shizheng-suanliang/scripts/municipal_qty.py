#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""市政工程计划口径速算：管道延米 / 井类计数 / 道路面积带。

输入是 cad-file-reader `municipal-geometry` 识图包的产物 `*.municipal.json`
（schema cad-municipal-geometry/v1）。识图层只给证据（管道候选、井类构件、
道路中线几何段、宽度/管径标注），工程量在此按以下口径估算：

  管道延米
      图面口径——市政管道图层 geometry 段长合计（mm→m，按契约单位换算），
      按系统（雨水/污水/给水/再生水/热力/燃气/电力/通信）分组。
      管径只从 pipe_network[].pipe_size 文本提取（DN/De/d/Φ），按档计数，
      **不做管径×几何段的强配**：缺"哪段是哪根管"的配对依据，强配就是编造。
      输出估算带 = 图面段长 × [1.00, 1.15]（图面口径系统偏低）。
  井类计数
      components 里 category 命中 检查井/雨水口/跌水井/阀门井/泵站 的候选，
      按系统计数；connectivity.junction_candidates 只作交叉核对，不并入计数。
  道路面积带
      道路中线/边线图层段长 × labels 里提取的车道/红线宽度标注。
      缺宽度标注一律进缺项清单，面积 unavailable，**不默认宽度**。
  路面结构层
      materials 里的材料做法只列清单并标注层厚缺失，不做分层面积
      （厚度证据缺失，分层就是编造）。

缺依据的项一律进缺项清单并写明缺什么，绝不用默认值凑数。
输出为估算带（±15%），final_quantity=false，不替代清单编制、结算与竣工计量。

用法
  # 正式入口：只从 lis-skill-bus 按 contract_id 取契约
  python3 municipal_qty.py --from-contract <contract_id> --project 项目 --out-prefix 市政算量
  # 手工/文件降级：必须显式 --allow-manual，结果 final_quantity=false
  python3 municipal_qty.py --municipal 市政识图/xxx.municipal.json --allow-manual --out-prefix 市政算量

来源准入由 contract_guard.guard_contract 把关；缺 reader/bus 时先跑 --check-deps，
不得自行实现 DWG/DXF 解析或用其它解析器兜底。
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
import csv
import json
import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime
from io import StringIO
from pathlib import Path

from contract_guard import GuardError, guard_contract, stamp_result
import contract_support as cs
import entry_gate as eg

SCHEMA = "cad-municipal-qty/v0.1"
INPUT_SCHEMA = "cad-municipal-geometry/v1"
CONTRACT_SCHEMA = "cad-contract/v1"
SKILL_NAME = "shizheng-suanliang"
SKILL_VERSION_FALLBACK = "0.1.0"

PIPE_SYSTEMS = ("雨水", "污水", "给水", "再生水", "热力", "燃气", "电力", "通信", "排水")
WIDTH_RE = re.compile(r"(\d+(?:\.\d+)?)\s*(?:m|M|米)")
DIAMETER_RE = re.compile(
    r"(?<![A-Za-z])(?:DN|dn|De|DE|de|d|D|Φ|φ)\s*[=＝]?\s*(\d{2,4})(?:\s*[xX×*]\s*(\d{2,4}))?")

# ---- 真实识图契约（cad-municipal-geometry/v1）的英文枚举 → 中文系统名 ----
# 来源：cad-file-reader packs/municipal-geometry/rules.json 的
# system_rules / pipe_rules（system 字段是英文键，不是中文）。
SYSTEM_EN_TO_ZH = {
    "rainwater": "雨水", "sewage": "污水", "water_supply": "给水",
    "reclaimed_water": "再生水", "heating": "热力", "gas": "燃气",
    "power": "电力", "telecom": "通信", "drainage": "排水",
    "fire_protection": "消防", "sponge_city": "海绵城市",
    "road": "道路", "pavement": "路面", "earthwork": "土方",
    "bridge": "桥梁", "culvert": "涵洞", "tunnel": "隧道",
    "retaining_wall": "挡墙", "slope_protection": "边坡",
    "utility_tunnel": "综合管廊", "street_lighting": "照明", "traffic": "交通",
}
PIPE_SYSTEM_KEYS = frozenset({
    "rainwater", "sewage", "water_supply", "reclaimed_water", "heating",
    "gas", "power", "telecom", "drainage", "fire_protection",
})
# 真实契约 geometry 行 category 来自 component_rules（英文键）；管道图层
# 不命中 component_rules 时 category=unclassified_municipal、system=英文键。
PIPE_CATEGORY_ZH_RE = re.compile(r"管道|管线|管网|排水管|雨水管|污水管|给水管")
# 管线综合国标色系（GB/T 50106 及市政管线综合惯例；蓝标系列图示用）
SYSTEM_COLORS = {
    "雨水": "#4DA6E8", "排水": "#5DCAA5", "污水": "#8B5A2B",
    "给水": "#0070C0", "再生水": "#3C3489", "消防": "#1D9E75",
    "热力": "#E24B4A", "燃气": "#EF9F27", "电力": "#D85A30",
    "通信": "#639922", "道路": "#5F5E5A", "未分类": "#B4B2A9", "其他": "#888780",
}
DEFAULT_COLOR = "#888780"

ROAD_CENTERLINE_KEYS = frozenset({"road_centerline"})
ROAD_EDGE_KEYS = frozenset({"road_edge", "road_edge_line", "kerb", "kerb_line", "roadside"})
ROAD_EDGE_ZH_RE = re.compile(r"(道路边线|边线|路缘石|路缘)")
ROAD_CENTERLINE_ZH_RE = re.compile(r"道路中线|路线中线|中线")
WELL_CATEGORY_KEYS = frozenset({"manhole"})
WELL_SUBTYPE_RE = re.compile(r"(雨水口|跌水井|阀门井|泵站|检查井)")
WELL_ZH_RE = re.compile(r"检查井|雨水井|污水井|雨水口|跌水井|阀门井|集水井|井盖")

# 管径分档（mm）；表外档进 other，只计数不硬套
DIA_BANDS = (300, 400, 500, 600, 800, 1000, 1200, 1500)


def dia_band(dn: int) -> str:
    for band in DIA_BANDS:
        if dn <= band:
            return "DN≤%d" % band
    return "DN>1500"


def _skill_version() -> str:
    try:
        return pyboot_skill_version()
    except Exception:
        return SKILL_VERSION_FALLBACK


def pyboot_skill_version() -> str:
    import pyboot
    return pyboot.skill_version()


# ---------------------------------------------------------------- 输入装载
def _load_json(path: str) -> tuple[dict | None, str]:
    p = Path(path)
    if not p.is_file():
        return None, "文件不存在: %s" % path
    try:
        return json.loads(p.read_text(encoding="utf-8-sig")), ""
    except json.JSONDecodeError as exc:
        return None, "JSON 解析失败: %s（%s）" % (path, exc)


def _doc_unit(doc: dict) -> str:
    for getter in (
        lambda d: d.get("coordinate_unit"),
        lambda d: (d.get("units") or {}).get("coordinate"),
        lambda d: (d.get("contract") or {}).get("coordinate_unit"),
    ):
        try:
            value = getter(doc)
        except Exception:
            value = None
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def _doc_unit_scale(doc: dict):
    for raw in (doc.get("unit_scale"),
                (doc.get("units") or {}).get("scale") if isinstance(doc.get("units"), dict) else None):
        if isinstance(raw, bool) or raw is None:
            continue
        try:
            value = float(raw)
        except (TypeError, ValueError):
            continue
        if value > 0:
            return value
    return None


def _max_coord_abs(payload: dict) -> float:
    """契约几何坐标的最大绝对值，用于量级推断单位。"""
    biggest = 0.0
    for key in ("municipal_geometry", "components"):
        for row in payload.get(key) or []:
            if not isinstance(row, dict):
                continue
            values = row.get("geometry") if key == "municipal_geometry" else None
            if not isinstance(values, (list, tuple)):
                x, y = row.get("x"), row.get("y")
                values = (x, y)
            for v in values:
                try:
                    biggest = max(biggest, abs(float(v)))
                except (TypeError, ValueError):
                    continue
    return biggest


def _infer_unit(payload: dict, warnings: list) -> str:
    """真实识图契约常缺 coordinate_unit：audit 证据 -> 坐标量级 -> 停算。

    推断结论一律带警告并标注来源，绝不静默。
    """
    audit = payload.get("scale_unit_audit")
    units: list[str] = []
    if isinstance(audit, list):
        for item in audit:
            if isinstance(item, dict):
                for u in item.get("units") or []:
                    if isinstance(u, str) and u.strip():
                        units.append(u.strip().lower())
    unit_set = {u for u in units if u in ("m", "mm")}
    if len(unit_set) == 1:
        inferred = unit_set.pop()
        warnings.append(
            "契约未声明 coordinate_unit，按 scale_unit_audit 文字证据推断为 %s；算量前请核对。" % inferred)
        return inferred

    biggest = _max_coord_abs(payload)
    if biggest >= 1e5:
        warnings.append(
            "契约未声明 coordinate_unit，audit 文字证据混合（%s）；按坐标量级 %.0f 推断为测量坐标 m。"
            "算量前请核对。" % ("/".join(sorted(unit_set)) if unit_set else "无", biggest))
        return "m"
    if 0 < biggest <= 1e4:
        warnings.append(
            "契约未声明 coordinate_unit，audit 文字证据混合（%s）；按坐标量级 %.0f 推断为图面 mm。"
            "算量前请核对。" % ("/".join(sorted(unit_set)) if unit_set else "无", biggest))
        return "mm"
    raise GuardError(4,
                     "坐标单位无法判定：契约未声明 coordinate_unit，audit 证据混合且坐标量级 %.0f "
                     "在 m/mm 歧义区（1e4~1e5），拒绝猜测。已停止长度/面积计算。" % biggest,
                     hint="用 --unit-scale 手工指定换算系数（m 图 1000，mm 图 1），或在契约顶层补 coordinate_unit。")


def _to_mm_factor(payload: dict, warnings: list, unit_scale_override: float | None = None) -> float:
    """坐标→毫米系数：unit=mm → 1；unit=m → 1000（单位定义）；其余需显式 unit_scale。"""
    if unit_scale_override is not None:
        warnings.append("使用 --unit-scale=%g 手工指定换算系数，覆盖契约单位声明。" % unit_scale_override)
        return float(unit_scale_override)
    unit = _doc_unit(payload)
    if not unit:
        unit = _infer_unit(payload, warnings)
    if unit.lower() == "mm":
        return 1.0
    if unit.lower() in ("m", "meter", "meters"):
        declared = _doc_unit_scale(payload)
        if declared is not None and declared != 1000.0:
            warnings.append("契约声明 unit_scale=%g，与 m 的固有换算 1m=1000mm 不一致，以 1000 为准。" % declared)
        warnings.append("坐标单位 m，按 1m=1000mm 换算；延米结果即为 m 口径，算量前请核对。")
        return 1000.0
    scale = _doc_unit_scale(payload)
    if scale is None:
        raise GuardError(4,
                         "坐标单位 %r 不是 mm，且未给 unit_scale（换算到 mm 的系数），已停止。"
                         "只出计数与缺项清单，不出长度/面积。" % unit,
                         hint="在契约顶层补 unit_scale（如 m 图给 1000）后重跑。")
    warnings.append("坐标单位 %r，按 unit_scale=%s 换算为 mm；算量前务必核对。" % (unit, scale))
    return float(scale)


def _validate_contract(data) -> dict:
    """结构不合法 -> SystemExit(2)；完全空证据 -> SystemExit(5)。"""
    if not isinstance(data, dict):
        print("❌ 契约顶层必须是 JSON 对象，实际是 %s" % type(data).__name__, file=sys.stderr)
        raise SystemExit(2)
    schema = str(data.get("schema") or "").strip()
    if schema != INPUT_SCHEMA:
        print("❌ 非契约输入：schema 必须是 %s，当前为 %s"
              % (INPUT_SCHEMA, schema or "<missing>"), file=sys.stderr)
        raise SystemExit(2)
    for key in ("components", "pipe_network", "municipal_geometry"):
        if key not in data or not isinstance(data[key], list):
            print("❌ 契约缺必需数组 %s（识图层产物损坏），请回到 cad-file-reader 重新生成。"
                  % key, file=sys.stderr)
            raise SystemExit(2)
    evidence = (len(data["components"]) + len(data["pipe_network"])
                + len(data["municipal_geometry"]) + len(data.get("labels") or []))
    if evidence == 0:
        print("❌ 空输入：契约里没有任何构件/管道/几何/标注证据，禁止输出估算。"
              "请回 cad-file-reader 确认识图范围。", file=sys.stderr)
        raise SystemExit("空输入：契约里没有任何构件/管道/几何/标注证据")
    return data


def _validated_payload(data) -> dict:
    """结构不合法 -> exit 2；空证据 -> exit 5（数据不足）。"""
    try:
        return _validate_contract(data)
    except SystemExit as exc:
        message = str(exc)
        code = 5 if "空输入" in message else 2
        print(message, file=sys.stderr)
        raise SystemExit(code) from None


# ---------------------------------------------------------------- 证据提取
def _seg_len_mm(row: dict) -> float:
    """优先用识图包现成的 length_drawing_units；缺了再按 geometry 四元组算。"""
    value = row.get("length_drawing_units")
    if isinstance(value, (int, float)) and value > 0 and not isinstance(value, bool):
        return float(value)
    geom = row.get("geometry")
    if not isinstance(geom, (list, tuple)) or len(geom) < 4:
        return 0.0
    try:
        x1, y1, x2, y2 = (float(v) for v in geom[:4])
    except (TypeError, ValueError):
        return 0.0
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5


def _system_zh(row: dict, extra_text: str = "") -> str:
    """系统名：先吃真实契约的英文 system 键，再回退中文文本匹配。"""
    system_key = str(row.get("system") or "").strip().lower()
    if system_key in SYSTEM_EN_TO_ZH:
        return SYSTEM_EN_TO_ZH[system_key]
    for name in PIPE_SYSTEMS:
        if name in extra_text:
            return name
    return "其他"


def _is_pipe_geometry(row: dict) -> bool:
    """管道几何判定：英文 system 键命中管道系统，或中文文本回退。"""
    system_key = str(row.get("system") or "").strip().lower()
    if system_key in PIPE_SYSTEM_KEYS:
        return True
    text = " ".join(str(row.get(k) or "") for k in ("category", "system", "layer"))
    return bool(PIPE_CATEGORY_ZH_RE.search(text))


def _extract(payload: dict, mm_factor: float) -> dict:
    """从契约载荷提取全部证据；只读，不改契约。

    兼容真实识图契约（英文枚举 category/system/label_type）与中文文本回退。
    对 municipal_geometry 做同段去重（layer+sheet+几何四元组相同视为重复，
    识图层去重失效或人工拼接契约时防止双计）。
    """
    warnings: list[str] = []

    # ---- municipal_geometry 同段去重（layer+图幅+几何四元组一致视为重复）----
    geometry_rows: list[dict] = []
    seen_geom: set[tuple] = set()
    dup_count = 0
    for row in payload.get("municipal_geometry") or []:
        if not isinstance(row, dict):
            continue
        geom = row.get("geometry")
        geom_key = (str(row.get("layer") or ""), str(row.get("sheet") or ""),
                    tuple(round(float(v), 3) for v in geom)
                    if isinstance(geom, (list, tuple)) and len(geom) >= 4 else None)
        if geom_key in seen_geom:
            dup_count += 1
            continue
        seen_geom.add(geom_key)
        geometry_rows.append(row)
    if dup_count:
        warnings.append("municipal_geometry 有 %d 条完全重复段（layer+图幅+几何一致）已去重，"
                        "防止双计。" % dup_count)

    # ---- 管道几何段长（按系统）----
    pipe_len_mm: dict[str, float] = {}
    pipe_seg_count: dict[str, int] = {}
    pipe_review_mm = 0.0
    for row in geometry_rows:
        if not _is_pipe_geometry(row):
            continue
        length = _seg_len_mm(row) * mm_factor
        if length <= 0:
            continue
        system = _system_zh(row, " ".join(str(row.get(k) or "")
                                          for k in ("category", "system", "layer")))
        if system == "其他":
            system = "未分类"
            warnings.append("有管道几何段无法映射到系统（图层未分类），单独归入「未分类」，不硬套系统。")
        pipe_len_mm[system] = pipe_len_mm.get(system, 0.0) + length
        pipe_seg_count[system] = pipe_seg_count.get(system, 0) + 1
        if str(row.get("status") or "") == "review":
            pipe_review_mm += length
    if pipe_review_mm > 0:
        warnings.append("管道几何段中 %.1f m 为识图层 review 状态（市政图层未映射到构件类别），"
                        "已按 system 归类计入延米，建议人工核对。" % (pipe_review_mm / 1000.0))
    if dup_count:
        warnings.append("municipal_geometry 有 %d 条完全重复段（layer+图幅+几何一致）已去重，"
                        "防止双计。" % dup_count)

    # ---- 管径分档计数（只计数，不做段长强配）----
    dia_counts: dict[str, int] = {}
    dia_unparsed = 0
    for row in payload.get("pipe_network") or []:
        if not isinstance(row, dict):
            continue
        text = " ".join(str(row.get(k) or "") for k in ("pipe_size", "raw", "system"))
        match = DIAMETER_RE.search(text)
        if not match:
            dia_unparsed += 1
            continue
        dn = int(match.group(1))
        band = dia_band(dn)
        dia_counts[band] = dia_counts.get(band, 0) + 1
    if dia_unparsed:
        warnings.append("管道候选 %d 条未提取到管径（DN/De/d/Φ），只计数不进管径分档。" % dia_unparsed)

    # ---- 井类计数（真实契约 category=manhole 英文键；子类从 raw 原文细分）----
    wells: dict[str, dict[str, int]] = {}
    well_specs: dict[str, dict[str, int]] = {}
    well_unmapped = 0
    for row in payload.get("components") or []:
        if not isinstance(row, dict):
            continue
        category = str(row.get("category") or "")
        raw = str(row.get("raw") or "")
        is_well = (category.lower() in WELL_CATEGORY_KEYS
                   or WELL_ZH_RE.search(category))
        if not is_well:
            continue
        subtype_match = WELL_SUBTYPE_RE.search(raw) or WELL_SUBTYPE_RE.search(category)
        subtype = subtype_match.group(1) if subtype_match else "检查井"
        system = _system_zh(row, category + " " + raw + " " + str(row.get("layer") or ""))
        wells.setdefault(system, {})
        wells[system][subtype] = wells[system].get(subtype, 0) + 1
        # B2: 井规格分档（φ/DN/纯数字 600~3000），表外规格只计数不归档
        spec_match = re.search(r"(?:[Φφ]|DN|D)?\s*[=＝]?\s*(\d{3,4})(?:\s*[xX×*]\s*(\d{2,4}))?", raw)
        if spec_match:
            spec = "φ%s" % spec_match.group(1)
            if spec_match.group(2):
                spec += "x%s" % spec_match.group(2)
            well_specs.setdefault(system, {})
            well_specs[system][spec] = well_specs[system].get(spec, 0) + 1
        well_unmapped += 1 if system == "其他" else 0
    if well_unmapped:
        warnings.append("井类候选 %d 个无法映射到系统，归入「其他」。" % well_unmapped)

    # ---- 道路中线段长（真实契约英文键 road_centerline + 中文回退 + review 弧段按 system=road 归类）----
    road_len_mm = 0.0
    road_seg_count = 0
    road_review_len_mm = 0.0
    for row in geometry_rows:
        category = str(row.get("category") or "")
        is_centerline = (category.lower() in ROAD_CENTERLINE_KEYS
                         or bool(ROAD_CENTERLINE_ZH_RE.search(category)))
        # 仅弧段行做 review 归类：弧段来自 ARC 实体、几何确定是道路中心线的一部分；
        # unclassified 直线段可能是边线/红线，不能当中线，不归类。
        if not is_centerline and row.get("arc") and (
                category == "unclassified_municipal"
                and str(row.get("system") or "").strip().lower() == "road"):
            is_centerline = True
            review_flag = True
        else:
            review_flag = False
        if not is_centerline:
            continue
        length = _seg_len_mm(row) * mm_factor
        if length > 0:
            road_len_mm += length
            road_seg_count += 1
            if review_flag:
                road_review_len_mm += length
    if road_review_len_mm > 0:
        warnings.append(
            "道路几何段中 %.1f m 为识图层 review 状态（system=road 未映射构件类别，含弧段），"
            "已按道路口径计入，建议人工核对。" % (road_review_len_mm / 1000.0))

    # B5: 道路边线段长（双口径交叉核对用）
    road_edge_len_mm = 0.0
    road_edge_seg_count = 0
    for row in geometry_rows:
        category = str(row.get("category") or "")
        is_edge = (category.lower() in ROAD_EDGE_KEYS
                   or bool(ROAD_EDGE_ZH_RE.search(category)))
        if not is_edge:
            continue
        length = _seg_len_mm(row) * mm_factor
        if length > 0:
            road_edge_len_mm += length
            road_edge_seg_count += 1

    # B3: 图层级聚合——同 layer 的管道几何段长 × 同 layer 管径候选（弱配对参考口径）
    layer_len_mm: dict[str, float] = {}
    for row in geometry_rows:
        if not _is_pipe_geometry(row):
            continue
        length = _seg_len_mm(row) * mm_factor
        if length > 0:
            key = str(row.get("layer") or "").strip() or "<无图层>"
            layer_len_mm[key] = layer_len_mm.get(key, 0.0) + length
    layer_dias: dict[str, set[str]] = {}
    for row in payload.get("pipe_network") or []:
        if not isinstance(row, dict):
            continue
        text = " ".join(str(row.get(k) or "") for k in ("pipe_size", "raw"))
        match = DIAMETER_RE.search(text)
        layer = str(row.get("layer") or "").strip() or "<无图层>"
        if match:
            layer_dias.setdefault(layer, set()).add(match.group(0).strip())

    # ---- B4: 桩号/标高/坡度复核表（透传，不算量）----
    survey_rows = []
    for row in payload.get("labels") or []:
        if not isinstance(row, dict):
            continue
        ltype = str(row.get("label_type") or "").lower()
        if ltype in ("station", "elevation", "slope"):
            survey_rows.append({"label_type": ltype,
                                "value": str(row.get("value") or row.get("raw") or ""),
                                "layer": str(row.get("layer") or "")})

    # ---- 宽度标注（真实契约无 width 类型：查 dimension 标注原文，回退全部 labels）----
    widths: list[float] = []
    for row in payload.get("labels") or []:
        if not isinstance(row, dict):
            continue
        text = " ".join([str(row.get("value") or ""), str(row.get("raw") or "")])
        if not re.search(r"宽|车道|红线|断面", text):
            continue
        match = WIDTH_RE.search(text)
        if match:
            value = float(match.group(1))
            if 2.0 <= value <= 100.0:
                widths.append(value)
    road_width_m = None
    if widths:
        counts: dict[float, int] = {}
        for value in widths:
            counts[value] = counts.get(value, 0) + 1
        road_width_m = max(counts, key=lambda k: counts[k])

    # ---- 材料/做法清单 ----
    materials = []
    for row in payload.get("materials") or []:
        if isinstance(row, dict):
            materials.append({
                "category": str(row.get("category") or ""),
                "value": str(row.get("value") or ""),
                "layer": str(row.get("layer") or ""),
            })

    # ---- 连通性交叉核对 ----
    connectivity = {}
    conn = payload.get("connectivity")
    if isinstance(conn, dict):
        conn_sum = conn.get("summary")
        if isinstance(conn_sum, dict):
            connectivity = {
                "open_endpoints": conn_sum.get("open_endpoints"),
                "junction_candidates": conn_sum.get("junction_candidates"),
            }

    # ---- 待复核项透传 ----
    review = []
    for row in payload.get("review") or []:
        if isinstance(row, dict):
            review.append({"type": str(row.get("type") or ""),
                           "reason": str(row.get("reason") or "")})

    return {
        "warnings": warnings,
        "pipe_len_mm": pipe_len_mm,
        "pipe_seg_count": pipe_seg_count,
        "dia_counts": dia_counts,
        "road_len_mm": road_len_mm,
        "road_seg_count": road_seg_count,
        "road_edge_len_mm": road_edge_len_mm,
        "road_edge_seg_count": road_edge_seg_count,
        "road_width_m": road_width_m,
        "wells": wells,
        "wells_specs": well_specs,
        "layer_len_mm": layer_len_mm,
        "layer_dias": {k: sorted(v) for k, v in layer_dias.items()},
        "survey_rows": survey_rows,
        "materials": materials,
        "connectivity": connectivity,
        "review": review,
    }


# ---------------------------------------------------------------- 口径计算
def build(payload_path: str, out_prefix: str, *, payload: dict | None = None,
          guard: dict | None = None, run_manifest: dict | None = None,
          unit_scale_override: float | None = None,
          road_width_override: float | None = None) -> Path:
    guard = guard or {}
    if payload is None:
        data, err = _load_json(payload_path)
        if err:
            raise GuardError(2, err)
        payload = _validated_payload(data)
    warnings: list[str] = list(payload.get("warnings") if isinstance(payload.get("warnings"), list) else [])
    evidence = _extract(payload, _to_mm_factor(payload, warnings, unit_scale_override))
    # 提取层警告（review 状态提示、管径未提取、未分类段等）必须并入最终输出，
    # 不能只留在 evidence 里——否则用户看不到口径警示。
    for message in evidence["warnings"]:
        if message not in warnings:
            warnings.append(message)

    # ---- 井密度交叉核对：工程口径污水/雨水管每 30~40m 一座井 ----
    total_len_m = sum(evidence.get("pipe_len_mm", {}).values()) / 1000.0
    wells_total = sum(sum(cats.values()) for cats in evidence.get("wells", {}).values())
    if wells_total == 0 and total_len_m > 0:
        warnings.append(
            "管道 %.0f m 但未识别到任何井类构件：识图层漏检可能性大（井常用图块表示），"
            "井计数不可直接使用，请人工清点或回识图层扩大构件规则。" % total_len_m)
    elif wells_total > 0 and total_len_m / wells_total > 100:
        warnings.append(
            "井密度 %.0f m/座（管道 %.0f m / 井 %d 座），远超工程常规 30~40 m/座："
            "识图层很可能漏检井类图块，井计数仅作下限参考。" % (total_len_m / wells_total, total_len_m, wells_total))

    missing: list[str] = []
    # ---- 管道延米带 ----
    pipes = []
    for system, length_mm in sorted(evidence["pipe_len_mm"].items()):
        length_m = length_mm / 1000.0
        segs = evidence["pipe_seg_count"].get(system, 0)
        pipes.append({
            "system": system,
            "length_m_estimate_low": round(length_m, 1),
            "length_m_estimate_high": round(length_m * 1.15, 1),
            "basis": "图面几何段长 × %d 段" % segs,
            "final_quantity": False,
        })
    if not pipes:
        missing.append("管道延米：市政管道图层无几何段（缺 municipal_geometry 管道段证据）")

    # ---- 管径分档 ----
    diameters = [{"band": band, "count": count}
                 for band, count in sorted(evidence["dia_counts"].items())]
    if not diameters:
        missing.append("管径分档：pipe_network 无可解析管径文本（DN/De/d/Φ）")

    # ---- 井类计数 ----
    wells = []
    well_total = 0
    system_len_m = {s: v / 1000.0 for s, v in evidence["pipe_len_mm"].items()}
    for system, cats in sorted(evidence["wells"].items()):
        subtotal = sum(cats.values())
        well_total += subtotal
        pipe_len_m = system_len_m.get(system, 0.0)
        density = round(subtotal / (pipe_len_m / 100.0), 2) if pipe_len_m > 0 else None
        for category, count in sorted(cats.items()):
            wells.append({"system": system, "category": category,
                          "count": count, "final_quantity": False})
        if density is not None:
            wells.append({"system": system, "category": "井密度（座/百米）",
                          "count": density, "final_quantity": False,
                          "note": "井 %d 座 / 管道 %.0f m，工程常规 30~40 m/座即 2.5~3.3 座/百米"
                                  % (subtotal, pipe_len_m)})
    # B2: 井规格分档（表外规格只计数）
    for system, specs in sorted(evidence["wells_specs"].items()):
        for spec, count in sorted(specs.items()):
            wells.append({"system": system, "category": "井规格 %s" % spec,
                          "count": count, "final_quantity": False,
                          "note": "规格从井 raw 文本提取，仅计数"})
    if not wells:
        missing.append("井类计数：components 无检查井/雨水口/跌水井/阀门井/泵站候选")

    # ---- 道路面积带（B5: 双口径交叉核对；--road-width 显式传参不默认）----
    road = None
    road_width = road_width_override if road_width_override is not None else evidence["road_width_m"]
    width_basis = "--road-width 显式传参" if road_width_override is not None else "labels 宽度标注多数档"
    if evidence["road_len_mm"] > 0 and road_width is not None:
        road_len_m = evidence["road_len_mm"] / 1000.0
        area = road_len_m * road_width
        road = {
            "centerline_length_m": round(road_len_m, 1),
            "width_m": road_width,
            "width_basis": width_basis,
            "area_m2_estimate_low": round(area, 1),
            "area_m2_estimate_high": round(area * 1.15, 1),
            "segment_count": evidence["road_seg_count"],
            "final_quantity": False,
        }
        if evidence["road_seg_count"] == 0:
            road["note"] = "宽度有标注但中线段长为 0，请核对道路中线图层分类"
        # B5: 边线口径交叉核对（边线段长/2 ≈ 中线段长，偏差>10% 警告）
        if evidence["road_edge_len_mm"] > 0:
            edge_len_m = evidence["road_edge_len_mm"] / 1000.0
            edge_area = edge_len_m / 2.0 * road_width
            road["edge_crosscheck"] = {
                "edge_length_m": round(edge_len_m, 1),
                "edge_area_m2_estimate": round(edge_area, 1),
                "deviation_percent": round(abs(edge_area - area) / area * 100, 1) if area > 0 else None,
                "evidence_grade": "weak",
            }
            if area > 0 and abs(edge_area - area) / area > 0.10:
                warnings.append(
                    "道路面积双口径偏差 %.1f%%（中线口径 %.0f m² vs 边线/2 口径 %.0f m²），"
                    "超 10%% 阈值：道路图层可能混入非道路线段，请人工核对。"
                    % (abs(edge_area - area) / area * 100, area, edge_area))
    else:
        if evidence["road_len_mm"] <= 0:
            missing.append("道路面积：道路中线/边线图层无几何段")
        if road_width is None:
            missing.append("道路面积：labels 无宽度标注（车道/红线宽），不默认宽度，面积 unavailable；"
                           "如有设计宽度可用 --road-width 显式传参")

    # ---- B3: 管径×图层级弱配对参考口径（不进主口径）----
    pipe_layer_ref = []
    for layer, len_mm in sorted(evidence["layer_len_mm"].items()):
        dias = evidence["layer_dias"].get(layer) or []
        pipe_layer_ref.append({
            "layer": layer,
            "length_m_estimate": round(len_mm / 1000.0, 1),
            "diameter_candidates_on_layer": dias,
            "evidence_grade": "weak",
            "note": "同图层级段长与管径候选的弱配对，仅供参考，不作为工程量依据",
            "final_quantity": False,
        })

    # ---- B4: 桩号/标高/坡度复核表（透传不算量）----
    survey_table = evidence["survey_rows"]

    # ---- 结构层清单（不算量）----
    pavement_layers = evidence["materials"]

    # ---- 连通性复核提示 ----
    connectivity = evidence["connectivity"]
    if connectivity.get("open_endpoints"):
        warnings.append("管网开放端点 %s 个：管道不连通处（断头/图幅边界），延米可能偏少，需人工核对。"
                        % connectivity["open_endpoints"])

    out = {
        "schema": SCHEMA,
        "skill": SKILL_NAME,
        "skill_version": _skill_version(),
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "source_file": str(payload_path),
        "input_schema": INPUT_SCHEMA,
        "run_manifest": run_manifest or {},
        "summary": {
            "pipe_systems": len(pipes),
            "pipe_length_m_low": round(sum(p["length_m_estimate_low"] for p in pipes), 1),
            "pipe_length_m_high": round(sum(p["length_m_estimate_high"] for p in pipes), 1),
            "diameter_bands": len(diameters),
            "wells_total": well_total,
            "road_area_m2_low": (road or {}).get("area_m2_estimate_low"),
            "road_area_m2_high": (road or {}).get("area_m2_estimate_high"),
            "missing_items": len(missing),
            "review_items": len(evidence["review"]),
            "final_quantity": False,
        },
        "pipes_length_estimate": pipes,
        "diameter_bands": diameters,
        "wells_count": wells,
        "pipe_length_by_layer_ref": pipe_layer_ref,
        "survey_review_table": survey_table,
        "road_area_estimate": road,
        "pavement_material_list": pavement_layers,
        "connectivity_crosscheck": connectivity,
        "missing_items": missing,
        "review_passthrough": evidence["review"][:80],
        "warnings": warnings,
        "boundary": "计划口径毛量估算带（±15%），final_quantity=false；"
                    "不替代工程量清单编制、竣工计量、结算与报价。",
    }
    stamp_result(out, guard)
    if out.get("contract_mode") == "manual" and not out.get("provenance"):
        # 契约没写 provenance 时 guard 按 manual 处理但不回填；结果必须显式 manual。
        out["provenance"] = "manual"

    cs.write_json(Path(str(out_prefix) + ".json"), out)
    _write_markdown(out, Path(str(out_prefix) + ".md"))
    _write_csv(out, Path(str(out_prefix) + ".csv"))
    _write_svg_legend(out, Path(str(out_prefix) + ".svg"))
    handoff_members = [
        cs.handoff_member("pipe-%s" % p["system"], length_m=p["length_m_estimate_low"],
                          zone=p["system"], weight_basis="unknown")
        for p in pipes
    ]
    cs.write_handoff(Path(str(out_prefix)).resolve().parent, "",
                     "市政", guard, handoff_members)
    return Path(str(out_prefix) + ".csv")


def _write_markdown(out: dict, path: Path) -> None:
    s = out["summary"]
    lines = [
        "# 市政工程计划口径速算（估算带）", "",
        "- 契约：`%s`（%s）" % (out["source_file"], out.get("contract_mode") or "-"),
        "- contract_id：%s" % (out.get("contract_id") or "-"),
        "- final_quantity：**false**（计划口径估算，不进正式台账）", "",
        "## 管道延米（按系统）", "",
    ]
    if out["pipes_length_estimate"]:
        lines += ["| 系统 | 估算带（m） | 依据 |", "|---|---|---|"]
        for row in out["pipes_length_estimate"]:
            lines.append("| %s | %.1f ~ %.1f | %s |"
                         % (row["system"], row["length_m_estimate_low"],
                            row["length_m_estimate_high"], row["basis"]))
        lines += ["", "合计：%.1f ~ %.1f m" % (s["pipe_length_m_low"], s["pipe_length_m_high"])]
    else:
        lines.append("无几何证据")
    lines += ["", "## 管径分档（只计数，不做段长强配）", ""]
    if out["diameter_bands"]:
        lines += ["| 管径档 | 数量 |", "|---|---|"]
        for row in out["diameter_bands"]:
            lines.append("| %s | %d |" % (row["band"], row["count"]))
    else:
        lines.append("无")
    lines += ["", "## 井类计数", ""]
    if out["wells_count"]:
        lines += ["| 系统 | 类别 | 数量 |", "|---|---|---|"]
        for row in out["wells_count"]:
            lines.append("| %s | %s | %d |" % (row["system"], row["category"], row["count"]))
    else:
        lines.append("无")
    lines += ["", "## 道路面积带", ""]
    road = out["road_area_estimate"]
    if road:
        lines += [
            "- 中线长度：%.1f m（%d 段）" % (road["centerline_length_m"], road["segment_count"]),
            "- 宽度：%.1f m（%s）" % (road["width_m"], road["width_basis"]),
            "- 面积估算带：**%.1f ~ %.1f m²**" % (road["area_m2_estimate_low"], road["area_m2_estimate_high"]),
        ]
        if road.get("note"):
            lines.append("- 提示：%s" % road["note"])
    else:
        lines.append("unavailable（见缺项清单）")
    lines += ["", "## 路面材料/做法清单（只列清单，不算分层面积）", ""]
    if out["pavement_material_list"]:
        lines += ["| 类别 | 做法 | 图层 |", "|---|---|---|"]
        for row in out["pavement_material_list"][:60]:
            lines.append("| %s | %s | %s |" % (row["category"], row["value"], row["layer"]))
    else:
        lines.append("无")
    lines += ["", "## 缺项清单", ""]
    if out["missing_items"]:
        for item in out["missing_items"]:
            lines.append("- %s" % item)
    else:
        lines.append("无")
    conn = out["connectivity_crosscheck"]
    if conn:
        lines += ["", "## 连通性交叉核对", "",
                  "- 开放端点：%s" % (conn.get("open_endpoints") or 0),
                  "- 汇聚节点：%s" % (conn.get("junction_candidates") or 0)]
    # 蓝标系列图例（国标管线色系，SVG 图示同前缀 .svg）
    lines += ["", "## 系统色标图例（蓝标系列）", "",
              "| 色标 | 系统 | 估算带 |", "|---|---|---|"]
    for item in out.get("pipes_length_estimate") or []:
        color = SYSTEM_COLORS.get(str(item["system"]), DEFAULT_COLOR)
        lines.append("| ■ `%s` | %s | %s ~ %s m |" % (color, item["system"],
                    item["length_m_estimate_low"], item["length_m_estimate_high"]))
    road = out.get("road_area_estimate")
    if road:
        color = SYSTEM_COLORS["道路"]
        lines.append("| ■ `%s` | 道路 | 面积 %s ~ %s m² |" % (color,
                    road.get("area_m2_estimate_low"), road.get("area_m2_estimate_high")))
    lines.append("")
    lines.append("> 色系参照管线综合国标惯例；配套 SVG 图示：`%s.svg`。图例仅辅助读图，不构成工程量依据。" % Path(out["source_file"]).stem)

    lines += ["", "## 警告", ""]
    if out["warnings"]:
        for warning in out["warnings"]:
            lines.append("- %s" % warning)
    else:
        lines.append("无")
    lines += ["", "> %s" % out["boundary"], ""]
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_svg_legend(out: dict, path: Path) -> None:
    """蓝标系列图示：按国标管线色系输出 SVG 图例（系统色标 + 延米估算带）。"""
    rows = []
    for item in out.get("pipes_length_estimate") or []:
        rows.append({"name": item["system"], "kind": "pipe",
                     "value": "%s ~ %s m" % (item["length_m_estimate_low"], item["length_m_estimate_high"])})
    road = out.get("road_area_estimate")
    if road:
        rows.append({"name": "道路", "kind": "road",
                     "value": "面积 %s ~ %s m²" % (road.get("area_m2_estimate_low"), road.get("area_m2_estimate_high"))})
    if not rows:
        path.write_text('<svg xmlns="http://www.w3.org/2000/svg" width="420" height="60">'
                        '<text x="16" y="32" font-size="14" fill="#888780">本图无市政系统量</text></svg>',
                        encoding="utf-8")
        return
    h = 40 + len(rows) * 34 + 24
    parts = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 680 %d" width="100%%">' % h,
             '<text x="40" y="30" font-size="15" font-weight="500" fill="#444441">市政系统色标图例（估算带，final_quantity=false）</text>']
    y = 58
    for i, row in enumerate(rows, 1):
        color = SYSTEM_COLORS.get(str(row["name"]), DEFAULT_COLOR)
        parts.append('<rect x="40" y="%d" width="26" height="18" rx="3" fill="%s"/>' % (y - 14, color))
        parts.append('<text x="78" y="%d" font-size="13" fill="#2C2C2A">%d. %s</text>' % (y, i, row["name"]))
        parts.append('<text x="240" y="%d" font-size="13" fill="#5F5E5A">%s</text>' % (y, row["value"]))
        y += 34
    parts.append('<text x="40" y="%d" font-size="11" fill="#888780">色系参照管线综合国标惯例；蓝标图例仅辅助读图，不构成工程量依据。</text>' % (h - 14))
    parts.append('</svg>')
    path.write_text("\n".join(parts), encoding="utf-8")


def _write_csv(out: dict, path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8-sig") as fh:
        writer = csv.writer(fh)
        writer.writerow(["item_type", "system", "category", "quantity_low",
                         "quantity_high", "unit", "basis", "final_quantity"])
        for row in out["pipes_length_estimate"]:
            writer.writerow(["pipe_length", row["system"], "", row["length_m_estimate_low"],
                             row["length_m_estimate_high"], "m", row["basis"], False])
        for row in out["diameter_bands"]:
            writer.writerow(["diameter_count", "", row["band"], row["count"], row["count"],
                             "处", "pipe_network 文本提取", False])
        for row in out["wells_count"]:
            writer.writerow(["well_count", row["system"], row["category"], row["count"],
                             row["count"], "座", "components 计数", False])
        road = out["road_area_estimate"]
        if road:
            writer.writerow(["road_area", "道路", "", road["area_m2_estimate_low"],
                             road["area_m2_estimate_high"], "m2",
                             "中线 %s m × 宽 %s m" % (road["centerline_length_m"], road["width_m"]),
                             False])


# ---------------------------------------------------------------- bus 接线
def _bus_client_path():
    for cand in (os.environ.get("SKILLBUS_CLIENT"),
                 Path.home() / ".codex" / "skills" / "lis-skill-bus" / "skillbus_client.py"):
        if cand and Path(str(cand)).is_file():
            return Path(str(cand))
    return None


def _bus_pull(project: str, contract_id: str) -> tuple[dict | None, str]:
    client = _bus_client_path()
    if client is None:
        return None, ("找不到 lis-skill-bus/skillbus_client.py。安装："
                      "bash ${CODEX_HOME:-$HOME/.codex}/skills/lis-skill-bus/install_skillbus.sh --apply")
    cmd = [sys.executable, str(client), "pull", "--project", project,
           "--entry-id", contract_id]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return None, "bus pull 执行失败：%s" % exc
    if proc.returncode != 0:
        return None, "bus pull 失败 rc=%d：%s" % (proc.returncode, (proc.stderr or "").strip()[-300:])
    try:
        data = json.loads(proc.stdout)
    except json.JSONDecodeError:
        return None, "bus pull 输出不是 JSON：%s" % (proc.stdout or "")[:200]
    entry = data.get("entry")
    if not data.get("hit") or not isinstance(entry, dict):
        return None, str(data.get("reason") or "bus 中未找到契约 %s" % contract_id)
    return entry, ""


def _pick_nested(payload: dict, key: str) -> str:
    """多级查找：顶层、camelCase、嵌套 contract/meta/_provenance（对齐真实识图契约）。"""
    candidates = (
        payload.get(key),
        payload.get("contractId") if key == "contract_id" else None,
        (payload.get("contract") or {}).get(key) if isinstance(payload.get("contract"), dict) else None,
        (payload.get("meta") or {}).get(key) if isinstance(payload.get("meta"), dict) else None,
        (payload.get("_provenance") or {}).get(key) if isinstance(payload.get("_provenance"), dict) else None,
    )
    for value in candidates:
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def _synthetic_guard_doc(payload: dict) -> dict:
    provenance = _pick_nested(payload, "provenance")
    contract_id = _pick_nested(payload, "contract_id")
    doc = {
        "schema": CONTRACT_SCHEMA,
        "provenance": provenance,
        "contract_id": contract_id,
        "coordinate_unit": _doc_unit(payload),
        "contract": payload,
    }
    if isinstance(payload.get("scale_unit_audit"), list) and payload.get("scale_unit_audit"):
        doc["scale_unit_audit"] = payload.get("scale_unit_audit")
    if isinstance(payload.get("source"), dict):
        doc["source"] = payload.get("source")
    return doc


def _guard_from_dict(doc: dict, *, allow_manual: bool, label: str = "<契约>") -> dict:
    with tempfile.TemporaryDirectory(prefix="municipal_contract_") as tmp:
        path = Path(tmp) / "contract.json"
        path.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
        try:
            return guard_contract(path, allow_manual=allow_manual, require_hash=False)
        except GuardError as exc:
            raise GuardError(exc.code,
                             exc.message.replace(str(path), label),
                             exc.hint.replace(str(path), label)) from None


def _guard_file_manual(path: str) -> tuple[dict, dict]:
    data, err = _load_json(path)
    if err:
        raise GuardError(2, err, hint="先确认路径：ls -l %s" % path)
    if not isinstance(data, dict):
        raise GuardError(2, "契约顶层必须是 JSON 对象", hint="检查文件开头")
    schema = str(data.get("schema") or "").strip()
    if schema == INPUT_SCHEMA:
        guard = _guard_from_dict(_synthetic_guard_doc(data), allow_manual=True, label=path)
        payload = data
    else:
        guard = guard_contract(path, allow_manual=True)
        payload = data.get("contract") if (
            schema == CONTRACT_SCHEMA and isinstance(data.get("contract"), dict)) else data
    if guard.get("mode") == "formal":
        guard = dict(guard)
        guard["mode"] = "manual"
        guard["provenance"] = "manual"
        guard["formal_ledger_eligible"] = False
        guard["warnings"] = list(guard.get("warnings") or []) + [
            "来源是文件路径而不是 bus，已按 manual 降级；正式量请用 --from-contract。"]
    return guard, payload


def _run_manifest(guard: dict) -> dict:
    return cs.run_manifest(SKILL_NAME, _skill_version(), guard, argv=sys.argv[1:])


def _print_guard_error(exc: GuardError) -> None:
    print("[GuardError %d] %s" % (exc.code, exc.message), file=sys.stderr)
    if exc.hint:
        print("修复: %s" % exc.hint, file=sys.stderr)


def _guard_exit_code(exc: GuardError) -> int:
    """guard 1-4 -> 22（契约无效），guard 5 -> 24（证据不足）；对齐 SKILL.md 退出码表。"""
    return 24 if exc.code == 5 else 22


# ---------------------------------------------------------------- self-test
def _self_test() -> int:
    """内置 10 项自检（合成数据、临时目录，不依赖 tests/fixtures）。"""
    checks: list[tuple[str, bool, str]] = []

    def record(name, ok, detail=""):
        checks.append((name, bool(ok), str(detail)))

    def expect_exit(name, fn, want_code):
        try:
            fn()
        except SystemExit as exc:
            got = int(exc.code or 0)
            record(name, got == want_code, "exit=%d（期望 %d）" % (got, want_code))
        except Exception as exc:
            record(name, False, "%s: %s" % (type(exc).__name__, exc))
        else:
            record(name, False, "未退出（期望 exit=%d）" % want_code)

    import tempfile

    def real_payload(**kw):
        base = {
            "schema": INPUT_SCHEMA, "source_file": "selftest.dwg",
            "coordinate_unit": "mm",
            "components": [
                {"category": "manhole", "system": "rainwater", "raw": "雨水检查井 φ1000",
                 "layer": "GS-SS", "x": 0, "y": 0, "status": "candidate"},
                {"category": "manhole", "system": "rainwater", "raw": "偏沟式雨水口",
                 "layer": "GS-YSK", "x": 1, "y": 1, "status": "candidate"},
            ],
            "pipe_network": [
                {"system": "rainwater", "pipe_size": "d800", "raw": "d800雨水管",
                 "layer": "DIM_雨水", "x": 0, "y": 0, "status": "candidate"},
            ],
            "materials": [{"category": "asphalt", "value": "沥青面层 4cm", "layer": "TEXT"}],
            "references": [],
            "labels": [{"label_type": "dimension", "value": "40", "raw": "红线宽 40m",
                        "layer": "TEXT"}],
            "municipal_geometry": [
                {"category": "unclassified_municipal", "system": "rainwater",
                 "layer": "DIM_雨水", "sheet": "PS-01",
                 "geometry": [0, 0, 120000, 0], "length_drawing_units": 120000.0,
                 "status": "review"},
                {"category": "road_centerline", "system": "road", "layer": "道路中线",
                 "sheet": "DL-01", "geometry": [0, 0, 0, 80000],
                 "length_drawing_units": 80000.0, "status": "candidate"},
            ],
            "entities": [],
            "connectivity": {"summary": {"open_endpoints": 1, "junction_candidates": 2}},
            "review": [],
        }
        base.update(kw)
        return base

    try:
        with tempfile.TemporaryDirectory(prefix="municipal_selftest_") as tmp:
            tmpdir = Path(tmp)

            def write(name, doc):
                path = tmpdir / name
                path.write_text(json.dumps(doc, ensure_ascii=False), encoding="utf-8")
                return str(path)

            # 1 validate 通过
            good = write("good.json", real_payload())
            data, err = _load_json(good)
            try:
                _validated_payload(data)
                record("1 validate 真实契约通过", err == "")
            except SystemExit:
                record("1 validate 真实契约通过", False)

            # 2 schema 错 -> 2
            expect_exit("2 schema 错误 -> 2",
                        lambda: _validated_payload(real_payload(schema="cad-contract/v0")), 2)

            # 3 空证据 -> 5
            expect_exit("3 空证据 -> 5",
                        lambda: _validated_payload(real_payload(
                            components=[], pipe_network=[],
                            municipal_geometry=[], labels=[])), 5)

            # 4 管道延米
            ev = _extract(real_payload(), 1.0)
            record("4 管道延米 120m",
                   abs(ev["pipe_len_mm"].get("雨水", 0) - 120000.0) < 1e-6)

            # 5 井类子类细分
            record("5 井类 检查井1+雨水口1",
                   ev["wells"].get("雨水", {}).get("检查井") == 1
                   and ev["wells"].get("雨水", {}).get("雨水口") == 1)

            # 6 管径分档
            record("6 管径档 DN≤800", ev["dia_counts"].get("DN≤800") == 1)

            # 7 宽度脏值过滤 + 多数档
            widths_payload = real_payload(labels=[
                {"label_type": "dimension", "value": "40", "raw": "红线宽 40m"},
                {"label_type": "dimension", "value": "40", "raw": "断面宽 40m"},
                {"label_type": "dimension", "value": "300", "raw": "宽 300m"},
            ])
            ev7 = _extract(widths_payload, 1.0)
            record("7 宽度多数档 40（300 过滤）", ev7["road_width_m"] == 40.0)

            # 8 m 单位 unit_scale 换算
            m_payload = real_payload(
                coordinate_unit="m", unit_scale=1000,
                municipal_geometry=[
                    {"category": "unclassified_municipal", "system": "rainwater",
                     "layer": "DIM_雨水", "geometry": [0, 0, 120, 0],
                     "length_drawing_units": 120.0, "status": "candidate"}])
            ev8 = _extract(m_payload, _to_mm_factor(m_payload, []))
            record("8 m 图 unit_scale=1000 -> 120m",
                   abs(ev8["pipe_len_mm"].get("雨水", 0) - 120000.0) < 1e-6)

            # 9 非 mm 且非 m 的单位缺 unit_scale -> GuardError(4)
            try:
                _to_mm_factor(real_payload(coordinate_unit="cm"), [])
                record("9 cm 缺 unit_scale 拒算", False, "未抛 GuardError")
            except GuardError as exc:
                record("9 cm 缺 unit_scale 拒算", exc.code == 4, "code=%d" % exc.code)

            # 10 端到端：manual build -> final_quantity=false + 三件套落盘
            path = write("e2e.json", real_payload())
            guard = _guard_from_dict(_synthetic_guard_doc(real_payload()),
                                     allow_manual=True, label=path)
            payload = _validated_payload(real_payload())
            out_csv = mq_build_e2e(tmpdir, path, payload, guard)
            out_json = Path(str(out_csv).replace(".csv", ".json"))
            ok = out_csv.is_file() and out_json.is_file()
            if ok:
                doc = json.loads(out_json.read_text(encoding="utf-8"))
                ok = (doc.get("final_quantity") is False
                      and doc.get("contract_mode") == "manual"
                      and doc.get("summary", {}).get("wells_total") == 2)
            record("10 端到端 manual build", ok)
    except Exception as exc:  # noqa: BLE001
        record("self-test 异常", False, "%s: %s" % (type(exc).__name__, exc))

    passed = sum(1 for _n, ok, _d in checks if ok)
    for name, ok, detail in checks:
        print("  %s  %s%s" % ("PASS" if ok else "FAIL", name,
                              (" (%s)" % detail if detail else "")))
    print("self-test: %d/%d PASS" % (passed, len(checks)))
    return 0 if passed == len(checks) else 1


def mq_build_e2e(tmpdir: Path, source: str, payload: dict, guard: dict) -> Path:
    return build(source, str(tmpdir / "e2e"), payload=payload, guard=guard,
                 run_manifest={"schema": "run-manifest/v1"})


# ---------------------------------------------------------------- CLI
def main() -> None:
    ap = argparse.ArgumentParser(
        description="Municipal quantity estimate from cad_municipal_geometry output")
    ap.add_argument("contract", nargs="?",
                    help="契约 JSON 路径（文件路径算量/mode=manual）")
    ap.add_argument("--municipal",
                    help="cad_municipal_geometry 产物 *.municipal.json（文件路径算量，必须配 --allow-manual）")
    ap.add_argument("--from-contract", metavar="CONTRACT_ID",
                    help="按 contract_id 从 lis-skill-bus 取正式契约（bus-only 入口）")
    ap.add_argument("--project", default="",
                    help="--from-contract 使用的 bus 项目标识")
    ap.add_argument("--unit-scale", type=float, default=None, metavar="FACTOR",
                    help="手工指定坐标→mm 换算系数（m 图 1000，mm 图 1），覆盖契约单位声明")
    ap.add_argument("--road-width", type=float, default=None, metavar="M",
                    help="人工指定道路红线宽（m），缺标注时显式传参，不默认")
    ap.add_argument("--allow-manual", action="store_true",
                    help="显式允许手工/文件契约；结果 provenance=manual、final_quantity=false")
    ap.add_argument("--out-prefix", help="输出前缀（计算模式必填）")
    ap.add_argument("--validate", action="store_true",
                    help="只体检输入契约：schema、必需数组、证据量；不出量")
    ap.add_argument("--self-test", action="store_true",
                    help="跑内置 10 项自检（合成数据，不读 fixtures）")
    ap.add_argument("--check-deps", action="store_true",
                    help="检查正式识图链路前置；缺 reader=20、缺 bus=21")
    a = ap.parse_args()

    if a.self_test:
        raise SystemExit(_self_test())

    if a.check_deps:
        status = cs.check_deps()
        print(cs.format_deps(status))
        raise SystemExit(eg.dependency_exit_code())

    try:
        eg.require_reader()
        eg.require_bus()
        eg.reject_drawing_input(a.contract, a.municipal)
    except eg.GateError as exc:
        raise SystemExit(eg.print_gate_error(exc)) from None

    source = a.municipal or a.contract
    if a.validate:
        if not source:
            ap.error("--validate 需要契约路径：--municipal 路径 或 直接放位置参数")
        data, err = _load_json(source)
        if err:
            print("❌ %s" % err, file=sys.stderr)
            raise SystemExit(2)
        try:
            _validated_payload(data)
        except SystemExit as exc:
            raise SystemExit(int(exc.code or 2)) from None
        print("体检通过：%s（schema=%s，证据就绪）" % (source, data.get("schema")))
        raise SystemExit(0)

    if not a.out_prefix:
        ap.error("计算模式需要 --out-prefix；只体检请用 --validate")

    if a.from_contract and source:
        print("WARN: 位置参数与 --from-contract 同时出现，"
              "已忽略位置参数，以 --from-contract=%s 为准。" % a.from_contract, file=sys.stderr)
        source = None

    if a.from_contract:
        entry, err = _bus_pull(a.project, a.from_contract)
        if entry is None:
            print("❌ 未取到契约 %s：%s" % (a.from_contract, err), file=sys.stderr)
            print("拉取命令（复制执行）：python3 ${CODEX_HOME:-$HOME/.codex}/skills/lis-skill-bus/"
                  "skillbus_client.py pull --project %s --entry-id %s"
                  % (a.project or "<项目>", a.from_contract), file=sys.stderr)
            raise SystemExit(1)
        schema = str(entry.get("schema") or "").strip()
        payload = entry.get("contract") if (schema == CONTRACT_SCHEMA
                                            and isinstance(entry.get("contract"), dict)) else entry
        provenance = str(entry.get("provenance") or "bus").strip()
        contract_id = _pick_nested(entry, "contract_id") or str(a.from_contract).strip()
        guard_doc = _synthetic_guard_doc(payload if isinstance(payload, dict) else entry)
        guard_doc["provenance"] = provenance or "bus"
        guard_doc["contract_id"] = contract_id
        if not _doc_unit(guard_doc.get("contract") or {}) and not _doc_unit(payload if isinstance(payload, dict) else {}):
            guard_doc["coordinate_unit"] = "mm"
        try:
            guard = _guard_from_dict(guard_doc, allow_manual=False, label="bus:%s" % a.from_contract)
        except GuardError as exc:
            _print_guard_error(exc)
            raise SystemExit(_guard_exit_code(exc)) from None
        if guard.get("mode") != "formal":
            print("❌ 契约来源不是 reader/bus，不能进正式算量。", file=sys.stderr)
            raise SystemExit(3)
        guard["reader_version"] = ""
        payload = _validated_payload(payload)
        safe_id = re.sub(r"[^0-9A-Za-z._-]+", "-", a.from_contract)[:64] or "contract"
        build("bus-" + safe_id, a.out_prefix, payload=payload,
              unit_scale_override=a.unit_scale, road_width_override=a.road_width,
              guard=guard, run_manifest=_run_manifest(guard))
        return

    if not source:
        ap.error("计算模式需要 --from-contract 或 --municipal/位置参数 + --out-prefix；"
                 "只体检请用 --validate")

    if not a.allow_manual:
        print("❌ 来源未授权：--municipal/位置参数是文件契约，必须同时给 --allow-manual。",
              file=sys.stderr)
        print("正式量请用 --from-contract <contract_id> --project <项目>；"
              "手工降级请加 --allow-manual（结果 final_quantity=false）。", file=sys.stderr)
        raise SystemExit(3)

    try:
        guard, payload = _guard_file_manual(source)
    except GuardError as exc:
        _print_guard_error(exc)
        raise SystemExit(_guard_exit_code(exc)) from None
    guard["reader_version"] = ""
    payload = _validated_payload(payload)
    build(source, a.out_prefix, payload=payload, unit_scale_override=a.unit_scale,
          road_width_override=a.road_width, guard=guard, run_manifest=_run_manifest(guard))


if __name__ == "__main__":
    main()
