#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 cad-file-reader 测量候选 / 装饰识图中间数据转成装饰算量输入表草稿。

CAD 导入行只作待核对输入：做法编号保持为空，需核对固定为“是”。
面积/长度换算、扣减、做法映射、损耗和材料台账仍由 zhuangshi-suanliang 处理。
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
import subprocess
import sys
from pathlib import Path
from typing import Any

HEADERS = [
    "楼层", "区域", "房间", "部位类型", "做法编号", "做法名称", "做法类型",
    "节点编号", "节点详图", "长_m", "宽_m", "高_m", "周长_m",
    "门窗洞口面积_m2", "洞口侧壁增加_m2", "扣减长度_m", "直接面积_m2",
    "直接长度_m", "防水上翻高度_m", "附加层面积_m2", "附加层长度_m",
    "附加层宽度_m", "搭接宽度_mm", "卷材幅宽_mm", "涂膜厚度_mm",
    "防水道数", "间数", "说明", "依据", "需核对",
]


def fmt(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (int, float)):
        return f"{value:.6f}".rstrip("0").rstrip(".")
    return str(value)


def room_name(row: dict[str, Any]) -> str:
    rooms = row.get("rooms")
    if isinstance(rooms, list) and rooms:
        return "、".join(str(value) for value in rooms if value)
    return str(row.get("source_id") or "CAD识图候选")


def blank() -> dict[str, str]:
    return {header: "" for header in HEADERS}


class ValidationUnavailable(RuntimeError):
    """默认 --validate 需要 cad-file-reader 的校验器；缺失或不可执行时不再静默跳过。"""


def cad_validate(input_path: Path) -> dict[str, Any]:
    """用 cad-file-reader 的 cad_validate.sh 校验交接 JSON。

    默认校验路径不再返回 None 静默跳过：底座/校验器缺失直接抛
    ValidationUnavailable，由 main 退出 1；仅显式 --no-validate 才跳过。
    """
    base = os.environ.get("CAD_SKILL_DIR")
    if not base:
        for d in (Path(__file__).resolve().parent.parent.parent / "cad-file-reader",
                  *sorted(Path.home().glob(".workbuddy/skills/*/cad-file-reader")),
                  Path.home() / ".claude/skills/cad-file-reader",
                  Path.home() / ".codex/skills/cad-file-reader"):
            if d.is_dir():
                base = str(d)
                break
    if not base:
        raise ValidationUnavailable(
            "找不到 cad-file-reader，无法执行 --validate。"
            "安装：skillhub install cad-file-reader --namespace user_43faedd6；"
            "确有离线交付需要时显式加 --no-validate，并在输出标 validation=skipped。")
    validator = Path(base) / "scripts" / "cad_validate.sh"
    if not validator.exists():
        raise ValidationUnavailable(
            f"cad-file-reader 缺少校验器：{validator}。请升级到 >=0.41.0；"
            "确有离线交付需要时显式加 --no-validate。")
    try:
        r = subprocess.run(
            ["bash", str(validator), str(input_path)],
            capture_output=True, text=True, timeout=120,
        )
    except Exception as exc:
        return {"ok": False, "errors": [f"{type(exc).__name__}: {exc}"], "exit": None}
    lines = [ln for ln in r.stdout.splitlines() if ln.strip()]
    errors: list[str] = []
    for ln in lines:
        try:
            rec = json.loads(ln)
            errors.extend(rec.get("errors") or [])
        except Exception:
            continue
    if r.returncode != 0 and not errors:
        tail = (r.stderr or r.stdout or "").strip().splitlines()[-3:]
        errors.append("cad_validate exit %d：%s" % (r.returncode, " | ".join(tail)))
    return {"ok": r.returncode == 0 and not errors, "errors": errors[:20],
            "exit": r.returncode}


def measurement_row(row: dict[str, Any], floor: str, zone: str) -> dict[str, str] | None:
    kind = str(row.get("kind") or "")
    if kind not in {"length", "area"}:
        return None
    value = row.get("value")
    if value is None:
        detail = (
            f"未换算：图面值 {fmt(row.get('value_drawing_units'))} {row.get('drawing_unit') or ''}；"
            f"{row.get('review_reason') or '缺比例或单位'}"
        )
    else:
        detail = f"{row.get('formula') or ''}；{row.get('review_reason') or ''}".strip("；")
    output = blank()
    output.update({
        "楼层": floor,
        "区域": zone,
        "房间": room_name(row),
        "部位类型": "待确认-面积" if kind == "area" else "待确认-长度",
        "做法名称": "CAD识图测量候选（需绑定做法）",
        "做法类型": "通用",
        "间数": "1",
        "说明": f"{detail}；final_quantity=false",
        "依据": f"cad-file-reader:{row.get('source_schema') or ''}:{row.get('source_id') or ''}",
        "需核对": "是",
    })
    if kind == "area" and value is not None:
        output["直接面积_m2"] = fmt(value)
    elif kind == "length" and value is not None:
        output["直接长度_m"] = fmt(value)
    return output


def descriptive_rows(payload: dict[str, Any], floor: str, zone: str) -> list[dict[str, str]]:
    """把 cad-descriptive-geometry 中间数据转成待核对输入行。

    房间/墙段/吊顶/洞口/做法索引只作装饰算量前的地图与草表，不直接出量；
    做法编号尽量从做法/节点详情带出，但必须先人工核对。
    """
    rows: list[dict[str, str]] = []

    def sid(item: dict[str, Any]) -> str:
        return str(item.get("source_id") or item.get("id") or "CAD装饰候选")

    def review_reason(item: dict[str, Any]) -> str:
        return str(item.get("review_reason") or "")

    for item in payload.get("room_boundaries") or []:
        if not isinstance(item, dict):
            continue
        row = blank()
        row.update({
            "楼层": floor, "区域": zone, "房间": room_name(item),
            "部位类型": "待确认-房间",
            "做法名称": "CAD房间边界（待核对/绑定做法）", "做法类型": "通用",
            "间数": "1",
            "说明": f"闭合房间边界；bbox={item.get('bbox') or ''}；{review_reason(item)}".rstrip("；"),
            "依据": f"cad-file-reader:cad-descriptive-geometry:{sid(item)}",
            "需核对": "是",
        })
        rows.append(row)

    for item in payload.get("wall_segments") or []:
        if not isinstance(item, dict):
            continue
        seg = item.get("segment") or ()
        row = blank()
        seg_kind = item.get("segment_kind") or item.get("status") or "待确认"
        row.update({
            "楼层": floor, "区域": zone,
            "房间": "、".join(str(v) for v in item.get("rooms") or []) or room_name(item),
            "部位类型": "待确认-墙面" if seg_kind == "clear" else "待确认-墙面洞口",
            "做法名称": "CAD墙段（clear/opening）", "做法类型": "通用",
            "门窗洞口面积_m2": "", "扣减长度_m": fmt(item.get("opening_width_mm")),
            "直接长度_m": "",
            "高_m": fmt(item.get("height_m")),
            "说明": f"墙段={list(seg)}；{review_reason(item)}".rstrip("；"),
            "依据": f"cad-file-reader:cad-descriptive-geometry:{sid(item)}",
            "需核对": "是",
        })
        rows.append(row)

    for item in payload.get("ceiling_zones") or []:
        if not isinstance(item, dict):
            continue
        row = blank()
        zone_kind = item.get("zone_kind") or "吊顶"
        row.update({
            "楼层": floor, "区域": zone, "房间": room_name(item),
            "部位类型": "待确认-顶棚",
            "做法名称": f"CAD吊顶分区({zone_kind})", "做法类型": "通用",
            "间数": "1",
            "说明": f"吊顶标高={fmt(item.get('elevation_m'))}m；{review_reason(item)}".rstrip("；"),
            "依据": f"cad-file-reader:cad-descriptive-geometry:{sid(item)}",
            "需核对": "是",
        })
        rows.append(row)

    for item in payload.get("openings") or []:
        if not isinstance(item, dict):
            continue
        geo = item.get("geometry") or {}
        row = blank()
        row.update({
            "楼层": floor, "区域": zone,
            "房间": "、".join(str(v) for v in item.get("rooms") or geo.get("room_candidates") or []) or old_rooms(item),
            "部位类型": "待确认-门窗洞口",
            "做法名称": "CAD门窗洞口（需核对尺寸/扣减）", "做法类型": "通用",
            "门窗洞口面积_m2": "",
            "说明": f"洞口编号={item.get('code') or item.get('door_code') or ''}；{review_reason(item)}".rstrip("；"),
            "依据": f"cad-file-reader:cad-descriptive-geometry:{sid(item)}",
            "需核对": "是",
        })
        rows.append(row)

    for item in payload.get("node_detail_index") or []:
        if not isinstance(item, dict):
            continue
        row = blank()
        codes = "、".join(str(v) for v in (item.get("practice_codes") or []))
        nodes = "、".join(str(v) for v in (item.get("node_codes") or []))
        row.update({
            "楼层": floor, "区域": zone, "房间": room_name(item),
            "部位类型": "待确认-做法",
            "做法编号": codes, "做法名称": "CAD做法→节点索引", "做法类型": "通用",
            "节点编号": nodes, "节点详图": str(geo_file(item) or ""),
            "说明": f"做法编号={codes or '未识别'}；{review_reason(item)}".rstrip("；"),
            "依据": f"cad-file-reader:cad-descriptive-geometry:{sid(item)}",
            "需核对": "是",
        })
        rows.append(row)
    return rows


def interior_finish_rows(payload: dict[str, Any], floor: str, zone: str) -> list[dict[str, str]]:
    """把 cad-interior-finish-geometry 中间数据转成待核对装饰输入行。

    只搬运识图候选和做法/做法表证据；不把候选面积当正式量，做法编号仍须人工核对。
    """
    rows: list[dict[str, str]] = []
    part_by_system = {
        "floor": "待确认-地面",
        "wall": "待确认-墙面",
        "ceiling": "待确认-顶棚",
        "skirting": "待确认-踢脚",
        "waterproof": "待确认-防水",
        "insulation": "待确认-保温",
        "furniture": "待确认-固定家具",
    }
    def evidence_text(item: dict[str, Any]) -> str:
        ev = (item.get("evidence") or [{}])[0] if isinstance(item.get("evidence"), list) else {}
        bits = []
        for key in ("text", "layer", "file", "sheet", "kind", "space"):
            value = ev.get(key) if isinstance(ev, dict) else None
            if value not in (None, ""):
                bits.append(f"{key}={value}")
        coord = ev.get("coord") if isinstance(ev, dict) else None
        if coord:
            bits.append(f"coord={coord}")
        return "；".join(bits)

    for item in payload.get("components") or []:
        if not isinstance(item, dict):
            continue
        system = str(item.get("system") or "")
        category = str(item.get("category") or "")
        if system not in part_by_system and category not in {"floor_layer", "wall_finish", "ceiling_finish", "skirting", "waterproof", "insulation"}:
            continue
        row = blank()
        row.update({
            "楼层": floor,
            "区域": zone,
            "房间": room_name(item) or f"CAD{item.get('file') or item.get('source_id') or '装饰候选'}",
            "部位类型": part_by_system.get(system, "待确认-装饰"),
            "做法名称": str(item.get("raw") or category or "CAD装饰做法候选")[:120],
            "做法类型": "通用",
            "间数": "1",
            "说明": f"cad-interior-finish:{category or system}；{evidence_text(item)}；final_quantity=false",
            "依据": f"cad-file-reader:cad-interior-finish-geometry:{item.get('source_id') or item.get('file') or ''}",
            "需核对": "是",
        })
        rows.append(row)

    for item in payload.get("references") or []:
        if not isinstance(item, dict):
            continue
        ref_type = str(item.get("reference_type") or "")
        code = str(item.get("value") or "")
        if ref_type == "finish_code" or (code and any(code.upper().startswith(x) for x in ("DM", "QM", "WM", "CM", "JM"))):
            row = blank()
            row.update({
                "楼层": floor, "区域": zone, "房间": room_name(item) or "CAD做法编号候选",
                "部位类型": "待确认-做法", "做法编号": code,
                "做法名称": str(item.get("raw") or "CAD做法编号候选")[:120], "做法类型": "通用",
                "间数": "1", "说明": f"做法编号候选；{evidence_text(item)}；须与建筑说明/做法表人工核对",
                "依据": f"cad-file-reader:cad-interior-finish-geometry:{item.get('source_id') or item.get('file') or ''}",
                "需核对": "是",
            })
            rows.append(row)
    return rows


def notes_text_rows(text_paths: list[str], floor: str, zone: str) -> list[dict[str, str]]:
    """把本地图纸说明/OCR 文本中的做法证据转成待核对装饰输入行。

    只搬运原文证据，不解析厚度/面积/材料消耗，不自动绑定做法编号。
    """
    part_keywords = [
        ("待确认-保温", ("保温", "岩棉", "挤塑", "聚苯板", "燃烧性能", "传热系数")),
        ("待确认-防水", ("防水", "防潮", "卷材", "涂膜", "止水")),
        ("待确认-屋面", ("屋面", "屋面板", "排水坡")),
        ("待确认-外墙", ("外墙", "外保温", "外饰面")),
        ("待确认-墙面", ("墙面", "内墙", "乳胶漆", "壁纸", "石材")),
        ("待确认-地面", ("地面", "楼面", "铺装", "地坪")),
        ("待确认-顶棚", ("顶棚", "吊顶", "天花")),
        ("待确认-踢脚", ("踢脚", "脚线")),
    ]
    rows: list[dict[str, str]] = []
    for raw_path in text_paths:
        path = Path(raw_path).expanduser().resolve()
        if not path.exists() or not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for line_no, line in enumerate(text.splitlines(), 1):
            text_line = " ".join(line.split()).strip()
            if len(text_line) < 4:
                continue
            part = ""
            for candidate, keywords in part_keywords:
                if any(k.lower() in text_line.lower() for k in keywords):
                    part = candidate
                    break
            if not part:
                continue
            row = blank()
            row.update({
                "楼层": floor,
                "区域": zone,
                "房间": f"文字证据-{path.stem}",
                "部位类型": part,
                "做法名称": text_line[:120],
                "做法类型": "通用",
                "间数": "1",
                "说明": f"本地说明/OCR 文本证据；{path.name}:{line_no}；仅作做法与部位定位，厚度、面积、损耗和材料量须人工核对；final_quantity=false",
                "依据": f"local-text:{path}:{line_no}",
                "需核对": "是",
            })
            rows.append(row)
    return rows


def old_rooms(item: dict[str, Any]) -> str:
    return str(item.get("source_id") or "CAD门窗候选")


def geo_file(item: dict[str, Any]) -> Any:
    return item.get("file") or item.get("file_name")


def convert(payload: dict[str, Any], floor: str, zone: str,
            descriptive: dict[str, Any] | None = None,
            interior_finish: dict[str, Any] | None = None,
            notes_text: list[str] | None = None) -> tuple[list[dict[str, str]], int]:
    measurements = payload.get("measurements")
    if measurements is None and interior_finish is None:
        raise ValueError("输入 JSON 缺少 measurements 数组")
    if not isinstance(measurements, list):
        measurements = []
    rows: list[dict[str, str]] = []
    skipped = 0
    for item in measurements:
        if not isinstance(item, dict):
            skipped += 1
            continue
        row = measurement_row(item, floor, zone)
        if row is None:
            skipped += 1
            continue
        rows.append(row)
    if descriptive:
        rows.extend(descriptive_rows(descriptive, floor, zone))
    if interior_finish:
        rows.extend(interior_finish_rows(interior_finish, floor, zone))
    if notes_text:
        rows.extend(notes_text_rows(notes_text, floor, zone))
    return rows, skipped


def main() -> int:
    parser = argparse.ArgumentParser(description="cad-file-reader 识别/测量候选 → 装饰算量输入表草稿（全部需核对）")
    parser.add_argument("--measurements", help="cad-measurement-candidates.json（与 --interior-finish 至少提供一个）")
    parser.add_argument("--out", required=True, help="输出 CSV")
    parser.add_argument("--floor", default="", help="统一填写楼层")
    parser.add_argument("--zone", default="CAD识图候选", help="区域名称")
    parser.add_argument("--descriptive", default=None,
                        help="可选：cad-descriptive-geometry 中间数据 JSON（房间/墙段/吊顶/洞口/做法索引）")
    parser.add_argument("--interior-finish", default=None,
                        help="可选：cad-interior-finish-geometry 中间数据 JSON（装饰/保温做法候选）")
    parser.add_argument("--notes-text", action="append", default=[],
                        help="可选：本地建筑说明/PDF OCR 文本；可重复传入，只生成待核对做法证据行")
    parser.add_argument("--validate", dest="validate", action=argparse.BooleanOptionalAction,
                        default=True,
                        help="导入前用 cad-file-reader 校验交接 JSON；缺底座/校验器 exit 1。"
                             "仅显式 --no-validate 才跳过并标 validation=skipped")
    args = parser.parse_args()

    source = Path(args.measurements).expanduser().resolve() if args.measurements else None
    target = Path(args.out).expanduser().resolve()
    payload = json.loads(source.read_text(encoding="utf-8")) if source else {}
    descriptive = None
    if args.descriptive:
        descriptive = json.loads(Path(args.descriptive).expanduser().resolve().read_text(encoding="utf-8"))
    interior_finish = None
    if args.interior_finish:
        interior_finish = json.loads(Path(args.interior_finish).expanduser().resolve().read_text(encoding="utf-8"))
    rows, skipped = convert(payload, args.floor, args.zone, descriptive, interior_finish, args.notes_text)

    validation: dict[str, Any] | str | None = None
    if args.validate:
        if source is not None:
            try:
                validation = cad_validate(source)
            except ValidationUnavailable as exc:
                print(f"❌ {exc}", file=sys.stderr)
                return 1
            if not validation.get("ok"):
                print("❌ CAD交接校验未通过：" + "；".join(validation.get("errors") or []), file=sys.stderr)
                return 1
        else:
            validation = {"ok": True, "skipped": True, "reason": "未提供 --measurements，无需校验"}
    else:
        validation = "skipped"
        for row in rows:
            row["需核对"] = "是"
            row["说明"] = "未执行 CAD交接校验（--no-validate）；" + row["说明"]

    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(rows)
    print(json.dumps({
        "source": str(source) if source else "",
        "descriptive": args.descriptive,
        "interior_finish": args.interior_finish,
        "notes_text": args.notes_text,
        "output": str(target),
        "rows": len(rows),
        "skipped": skipped,
        "review_required": True,
        "validation": validation,
        "note": "做法编号保持为空或仅作待核对候选；面积/长度、扣减、损耗和材料量仍由装饰算量技能处理",
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
