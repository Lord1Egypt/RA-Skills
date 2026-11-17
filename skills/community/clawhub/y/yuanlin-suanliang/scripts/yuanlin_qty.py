#!/usr/bin/env python3
"""yuanlin-suanliang: 园林概算底稿（苗木统计 + 铺装面积）候选复算器。

输入：cad-file-reader landscape-geometry 输出 JSON + cad_scan --with-geom --with-geom-layer --detail-json。
口径：只出概算底稿与物资计划草稿；带使用边界、置信分层 P0-P3、证据坐标与需核对。
"""
from __future__ import annotations

try:
    import os as _boot_os, sys as _boot_sys
    _boot_sys.path.insert(0, _boot_os.path.dirname(_boot_os.path.abspath(__file__)))
    import pyboot as _boot_pyboot
    _boot_pyboot.ensure_utf8_io()
except Exception:
    pass


import argparse, copy, csv, json, math, os, re, subprocess, sys, tempfile

import i18n
import contract_support as cs
from contract_guard import GuardError
import entry_gate as eg
from pathlib import Path

SCHEMA = "yuanlin-suanliang/v0"
BOUNDARY = "只出概算底稿与物资计划草稿；不替代设计复核、放线、点树、竣工计量、对量、结算与正式报价；需核对项不自动默认。"

DEFAULT_RULES = {
    "confidence": {
        "direct": 0.95, "block_name": 0.9, "pattern": 0.78,
        "geometry_closure": 0.86, "geometry_summary": 0.7, "inferred": 0.6, "review": 0.4,
    },
    "dedupe_tolerance": 0.5,
    "geometry_close_tolerance": 50,
    "exclude_layers": [],
    "include_layers_regex": "",
    "exclude_frame_bbox": None,
    "paving_layer_tokens": ["景观铺地", "铺装", "铺地", "园路", "波打", "收边", "PAVING", "HARDSCAPE", "PAVE"],
    "scale_unit_hints": {"mm": 1, "毫米": 1, "m": 1000, "米": 1000},
    "plant_groundcover": ["地被", "草坪", "草皮", "麦冬", "鸢尾", "萱草", "阔叶麦冬", "金娃娃萱草", "玉簪", "葱兰", "沿阶草", "佛甲草", "景天", "三叶草", "结缕草", "黑麦草", "高羊茅", "百慕大", "马尼拉"],
    "plant_shrubs": ["紫薇", "月季", "女贞", "大叶女贞", "冬青", "黄杨", "大叶黄杨", "迎春", "连翘", "木槿", "紫荆", "腊梅", "丁香", "红叶石楠", "红叶小檗", "金叶女贞", "海桐", "卫矛", "锦带", "绣球", "蔷薇", "榆叶梅", "珍珠梅", "紫叶小檗", "枸骨", "棣棠", "金银木", "黄栌", "扶芳藤"],
    "plant_trees": ["国槐", "银杏", "白蜡", "栾树", "法桐", "悬铃木", "枣树", "柳树", "垂柳", "槐树", "樱花", "海棠", "玉兰", "桂花", "香樟", "红枫", "紫叶李", "枇杷", "雪松", "油松", "白皮松", "侧柏", "龙柏", "青桐", "水杉", "五角枫", "元宝枫", "云杉", "金枝槐", "火炬树", "合欢", "梧桐", "乌桕", "朴树", "榆树", "山楂树", "柿树", "紫叶矮樱", "石榴", "晚樱", "梅"],
    "plant_other": ["绿篱", "花镜", "花钵", "树池", "种植池", "花带", "模纹", "竹", "竹类", "紫竹", "刚竹", "石菖蒲", "再力花", "千屈菜", "荷花", "睡莲"],
}
CONF_P0, CONF_P1, CONF_P2, CONF_P3 = "P0", "P1", "P2", "P3"

# 参考库只做“中文名 → 大类”归组；规格、密度、苗价/综合单价一律不读、不推断。
PLANT_LIBRARY_SECTION_CATEGORY = (
    # 顺序敏感：先“地被”口径（“小灌木及地被”含“灌木”，必须先判地被），再灌木，再乔木。
    ("小灌木及地被", "地被"), ("水生", "地被"), ("草坪", "地被"), ("地被", "地被"), ("草花", "地被"),
    ("球类灌木", "灌木"), ("大灌木", "灌木"), ("灌木", "灌木"),
    ("常绿乔木", "乔木"), ("落叶乔木", "乔木"), ("乔木", "乔木"),
    ("藤本", "其他"), ("竹类", "其他"), ("竹", "其他"),
)
PLANT_LIBRARY_CATEGORY_KEYS = {"乔木": "plant_trees", "灌木": "plant_shrubs", "地被": "plant_groundcover", "其他": "plant_other"}
DEFAULT_PLANT_LIBRARY_DIR = Path(__file__).resolve().parent.parent / "rules"
DEFAULT_PLANT_LIBRARY = DEFAULT_PLANT_LIBRARY_DIR / "plant_library_常用园林植物.json"


def default_plant_libraries():
    """内置区域植物库：rules/plant_library_*.json 全部自动加载（按文件名稳定排序）。

    每个库都只提供“中文名 → 大类”，不含规格/密度/单价；多个库按顺序做“只补缺口”合并，
    先加载的库优先，后加载的库不覆盖既有分类。
    """
    try:
        files = sorted(DEFAULT_PLANT_LIBRARY_DIR.glob("plant_library_*.json"))
        # v2：rules/plant_library/<大区>/<城市>.json 两级库；按路径稳定排序，先加载者优先。
        files += sorted((DEFAULT_PLANT_LIBRARY_DIR / "plant_library").glob("*/*.json"))
    except Exception:
        files = []
    if DEFAULT_PLANT_LIBRARY.exists() and DEFAULT_PLANT_LIBRARY not in files:
        files = [DEFAULT_PLANT_LIBRARY] + files
    return files


# ---------- 通用输入读取（容忍多种 JSON 结构） ----------
def _num(v):
    try:
        f = float(v)
        return f if math.isfinite(f) else None
    except (TypeError, ValueError):
        return None


def iter_records(data):
    seen, n = set(), 0
    for key in ("records", "text_records", "text_items", "text", "items", "block_instances", "candidates"):
        for rec in (data.get(key) or []):
            if not isinstance(rec, dict):
                continue
            rec = dict(rec)
            h = rec.get("handle") or rec.get("id") or f"{key}-{n}"
            if h in seen:
                continue
            seen.add(h)
            n += 1
            rec["_key"] = key
            yield rec


def iter_geometry(data):
    """cad_scan --with-geom --with-geom-layer 格式：geometry_segments + geometry_layers。"""
    sfiles = data.get("geometry_segments") or []
    lfiles = data.get("geometry_layers") or []
    for fi, segs in enumerate(sfiles):
        layers = lfiles[fi] if fi < len(lfiles) else []
        for si, seg in enumerate(segs or []):
            if not (isinstance(seg, (list, tuple)) and len(seg) >= 4):
                continue
            layer = str(layers[si]) if si < len(layers) else ""
            sx = [_num(seg[0]), _num(seg[1]), _num(seg[2]), _num(seg[3])]
            if any(v is None for v in sx):
                continue
            yield {"fi": fi, "si": si, "layer": layer, "x1": sx[0], "y1": sx[1], "x2": sx[2], "y2": sx[3]}
    for rec in iter_records(data):
        sx = [_num(rec.get("x1")), _num(rec.get("y1")), _num(rec.get("x2")), _num(rec.get("y2"))]
        if all(v is not None for v in sx):
            yield {"layer": str(rec.get("layer") or ""), "x1": sx[0], "y1": sx[1], "x2": sx[2], "y2": sx[3], "source": "record"}


def find_text(data):
    out = []
    for rec in iter_records(data):
        t = rec.get("text")
        if isinstance(t, str) and t.strip():
            out.append({"text": t.strip(), "layer": str(rec.get("layer") or ""), "x": _num(rec.get("x")), "y": _num(rec.get("y")), "kind": str(rec.get("kind") or rec.get("type") or "TEXT")})
    return out


# ---------- 比例/单位检测 ----------
def detect_scale_unit(data, cfg, override_scale=None, override_mm=None):
    mm = float(override_mm) if override_mm else cfg.get("drawing_mm_per_unit")
    if not mm:
        mm = 1.0
    scale = float(override_scale) if override_scale else None
    text = " ".join(t["text"] for t in find_text(data)) + " " + json.dumps(data.get("text") or {}, ensure_ascii=False)[:4000]
    if not scale:
        from collections import Counter
        recs = find_text(data)
        ctx = Counter()
        for r in recs:
            t = r["text"]
            if any(k in t for k in ("平面图", "总平面", "种植", "景观", "铺装", "比例", "SCALE")):
                for x in re.findall(r"1\s*[:：]\s*(\d{2,4})", t):
                    if 20 <= int(x) <= 2000:
                        ctx[int(x)] += 1
        allr = Counter(int(x) for x in re.findall(r"1\s*[:：]\s*(\d{2,4})", text) if 20 <= int(x) <= 2000)
        pick = (ctx or allr)
        scale = float(pick.most_common(1)[0][0]) if pick else 1.0
    mm_source = "用户覆盖" if override_mm else ("规则配置" if cfg.get("drawing_mm_per_unit") else "默认")
    if not override_mm:
        low = text.lower()
        for k, v in cfg.get("scale_unit_hints", {}).items():
            if k in low:
                mm = v
                mm_source = "图纸文字"
                break
    scale_source = "用户覆盖" if override_scale else ("图纸文字" if not cfg.get("scale") else "规则配置")
    return {"scale": scale, "drawing_mm_per_unit": mm, "scale_source": scale_source, "drawing_unit_source": mm_source}


# ---------- 苗木统计 ----------
def _unique_pts(points, tol):
    pts, seen = [], set()
    for x, y in points:
        if x is None or y is None:
            continue
        key = (round(x / max(tol, 1e-6)), round(y / max(tol, 1e-6)))
        if key not in seen:
            seen.add(key)
            pts.append((x, y))
    return pts


CJK = lambda t: sum(1 for c in t if "\u4e00" <= c <= "\u9fff")
HEADER_WORDS = {"图例", "名称", "数量", "单位", "备注", "胸径(cm)", "胸径（cm）", "高度(m)", "高度（m）", "冠幅(m)", "冠幅（m）",
                "枝下高（m）", "枝下高(m)", "序号", "常绿树", "乔木", "花灌木、球类植物", "地被、绿篱", "规格", "种植密度", "株"}
SCHEDULE_NON_PLANT_WORDS = ("给排水", "上沙路", "出入口", "架空", "空调", "会签", "施工说明", "种植说明", "总平面", "道路沿", "规格(cm)", "数量(棵)", "二年生", "三年生", "丛生", "厕", "政府", "厂", "事务所", "公司", "设计", "审核", "绘图", "比例", "日期", "工种", "共张", "第张", "图号")
UNIT_TOKENS = ("株/m2", "株/㎡", "株/m²", "株", "棵", "m2", "㎡", "m²", "平方米", "丛", "袋", "芽")


def _is_plant_name(t):
    t = (t or "").strip()
    if not (2 <= len(t) <= 14) or t in HEADER_WORDS:
        return False
    if re.search(r"[0-9]", t) or "-" in t or "\\U+2265" in t:
        return False
    c = CJK(t)
    return c >= 2 and c >= len(t) * 0.6


def _is_plant_like(t, cfg, base=None):
    """中英文通用的植物名/块名过滤；优先信任底座分类，其次看植物词/图层。"""
    t = re.sub(r"\s+", " ", str(t or "").strip())
    if not t or len(t) > 120:
        return False
    if base and str(base.get("category") or "") in ("乔木", "灌木", "地被", "地被/绿篱", "其他"):
        return True
    if _is_plant_name(t):
        return True
    low = t.lower()
    layer = str((base or {}).get("layer") or "").lower()
    if re.match(r"^(structure|buildings?|legend|furniture|services?|annotation|dim|axis|[a-z]{1,2})\s*[-_/]", low):
        return False
    if any(k in low for k in ("苗木表", "苗木配置表", "总平面图", "平面图", "标题", "图框")):
        return False
    # 中英文植物块名与植物图层。Ornamental/Herb/Fern 等常见于欧美景观图；
    # 图层中明确出现 Plant/Ground cover/绿化/种植 时，也允许通用图例名进入候选。
    tokens = (
        "tree", "shrub", "perennial", "annual", "climber", "ground cover", "groundcover",
        "lawn", "grass", "bush", "plant", "pot", "rose", "ivy", "ornamental", "herbaceous",
        "herb", "fern", "wildflower", "meadow", "bulb", "vine", "conifer", "palm", "aquatic",
    )
    hay = low + " " + layer
    if any(re.search(rf"(?<![a-z]){re.escape(k)}(?![a-z])", hay) for k in tokens):
        return True
    if any(k in layer for k in ("plant -", "planting", "ground cover", "绿化", "种植", "苗木")):
        return True
    # 词库命中只接受“像名称”的短文本：参考库扩充后，避免把“...棕榈科植物...”这类
    # 设计说明整句误判成植物块/图例；长句与带句读的说明一律不进候选。
    if len(t) > 16 or re.search(r"[，。；：！？、,;:]", t):
        return False
    return any(str(x).strip().lower() in low for x in (cfg.get("plant_trees") or []) + (cfg.get("plant_shrubs") or []) + (cfg.get("plant_groundcover") or []) + (cfg.get("plant_other") or []) if str(x).strip())


def _is_number(t):
    t = (t or "").strip().replace(" ", "")
    return bool(re.fullmatch(r"\d+(?:\.\d+)?", t))


def _is_unit(t):
    t = (t or "").strip().replace(" ", "")
    tl = t.lower()
    return t in UNIT_TOKENS or tl in UNIT_TOKENS or tl.endswith("株/m2") or t.endswith("株/m²")


def _schedule_header_type(t):
    h = str(t or "").strip().replace(" ", "").lower().replace("（", "(").replace("）", ")")
    if (h in ("名称", "苗木名称", "植物名称", "品种", "品名", "中文名称", "中文名", "苗木中文名", "植物中文名", "中文植物名称")
            or h.startswith("名称") or h.endswith("中文名称") or "中文名称" in h
            or h in ("图例编号", "图例号", "序号")):
        return "name"
    if h in ("数量", "株数", "工程量") or re.fullmatch(r"数量\((?:株|棵|丛|袋|m2|㎡|m²)\)", h):
        return "qty"
    if h == "单位":
        return "unit"
    if h in ("规格", "规格及单位", "规格说明") or h.startswith("规格("):
        return "spec"
    return ""


def _schedule_header_qty_unit(t):
    """数量表头中的单位是证据；没有显式单位时不得默认为株。"""
    h = str(t or "").strip().replace(" ", "").lower().replace("（", "(").replace("）", ")")
    m = re.fullmatch(r"数量\((株|棵|丛|袋|m2|㎡|m²)\)", h)
    if not m:
        return None
    return {"m2": "m²", "㎡": "m²"}.get(m.group(1), m.group(1))


def _schedule_title_type(t):
    """识别图纸苗木表标题；长说明句不作为表区锚点。"""
    h = re.sub(r"\s+", "", str(t or "")).lower()
    if not h or len(h) > 20 or "种植苗木表" in h:
        return ""
    for kind in ("苗木配置表", "苗木规格总表", "苗木图例表", "苗木表", "植物表"):
        if kind in h:
            return kind
    return ""


def _implicit_schedule_titles(tr, explicit_titles):
    """无标题苗木表兜底：同一排同时出现“名称类表头 + 数量/单位表头”即视为表区锚点。

    只认表头组合、不靠内容猜表；已有显式标题覆盖的表区不重复建锚点（保守，避免重复计数）。
    """
    out, seen = [], set()
    for r in tr:
        if _schedule_header_type(r["text"]) != "name":
            continue
        y, sheet = float(r["y"]), r.get("sheet")
        key = (sheet, round(y, 1))
        if key in seen:
            continue
        seen.add(key)
        # 实测图纸里同一张表可能被版面切分标到不同 sheet（如 sheet1/sheet6 共用一套坐标），
        # 因此按“同一排坐标”而不是按 sheet 判表头组合。
        same_row = [q for q in tr if abs(float(q["y"]) - y) < 1500.0
                    and abs(float(q["x"]) - float(r["x"])) < 260000.0
                    and _schedule_header_type(q["text"]) in ("qty", "unit")]
        if not same_row:
            continue
        covered = any(0.0 <= (float(t["y"]) - y) < 4000
                      and abs(float(t["x"]) - float(r["x"])) < 80000 for t in explicit_titles)
        if covered:
            continue
        out.append({"text": "苗木表(表头自识别)", "x": float(r["x"]), "y": y, "sheet": sheet,
                    "_implicit": True})
    return out


def _schedule_header_sets(headers, title_rec):
    """按数量列配对实际名称列；序号/图例编号只在无实际名称列时兜底。"""
    by_type = {k: [r for r in headers if _schedule_header_type(r["text"]) == k] for k in ("name", "qty", "unit", "spec")}
    actual_names = [r for r in by_type.get("name") or [] if str(r["text"]).replace(" ", "") not in ("图例编号", "图例号", "序号")]
    fallback_names = [r for r in by_type.get("name") or [] if str(r["text"]).replace(" ", "") in ("图例编号", "图例号", "序号")]
    out = []
    for qty in by_type.get("qty") or []:
        names = actual_names or fallback_names
        name = min(names, key=lambda r: abs(float(r["x"]) - float(qty["x"])) + 0.2 * abs(float(r["y"]) - float(qty["y"])), default=None)
        if not name:
            continue
        qx, qy = float(qty["x"]), float(qty["y"])
        unit = min(by_type.get("unit") or [], key=lambda r: abs(float(r["x"]) - qx) + 0.2 * abs(float(r["y"]) - qy), default=None)
        spec = min(by_type.get("spec") or [], key=lambda r: abs(float(r["x"]) - qx) + 0.2 * abs(float(r["y"]) - qy), default=None)
        out.append({"name": name, "qty": qty, "unit": unit, "spec": spec,
                    "distance": abs(float(name["x"]) - float(title_rec["x"]))})
    return sorted(out, key=lambda h: (h["distance"], float(h["name"]["x"])))


def _selected_schedule_header_sets(headers, title_rec):
    """只解析标题最近的表组；邻近表组按距离倍数放行，避免误读旁边的灯具/材料表。"""
    groups = _schedule_header_sets(headers, title_rec)
    if not groups:
        return []
    base = max(groups[0]["distance"], 1.0)
    return [g for g in groups if g["distance"] <= max(base * 5.0, base + 1000.0)]


def _split_schedule_name_spec(t):
    """兼容“银杏 φ10-12”“1 银杏”等合并/编号写法；只拆名称与规格证据，不猜规格。"""
    raw = str(t or "").strip()
    if not raw:
        return "", ""
    # 图例编号列常见 “1 银杏 / A01 银杏”，取首个空格后的内容；纯编号保留原编号。
    m = re.match(r"^[\dA-Za-z]{1,6}[\s　]+([^\d][\s\S]*)$", raw)
    if m:
        raw = m.group(1).strip()
    m = re.match(r"^([\u4e00-\u9fff]{2,14})(?:[\s　:：,，]+([\s\S]+))?$", raw)
    if m:
        return m.group(1).strip(), (m.group(2) or "").strip()
    return raw, ""


def plant_schedule_rows(scan, cfg):
    """从图纸文字里的苗木表解析设计给定数量；兼容表头变体与规格合并列。"""
    if not scan:
        return [], []
    tr = [r for r in iter_records(scan) if isinstance(r.get("text"), str) and r.get("x") is not None and r.get("y") is not None]
    rows, meta = [], []
    titles = [r for r in tr if _schedule_title_type(r["text"])]
    titles = titles + _implicit_schedule_titles(tr, titles)
    seen = set()
    for t0 in titles:
        x0, y0, sheet = float(t0["x"]), float(t0["y"]), t0.get("sheet")
        # 表区横向窗口：默认锚点 ±20000；若锚点同一排就是表头行（无标题表），按表头跨度放宽，
        # 否则“名称列—数量列”很宽的表会取不到数量列。
        lo, hi = x0 - 20000, x0 + 20000
        same_row_headers = [r for r in tr if abs(float(r["y"]) - y0) < 1500
                            and _schedule_header_type(r["text"])]
        if len(same_row_headers) >= 2:
            hxs = [float(r["x"]) for r in same_row_headers]
            lo, hi = min(lo, min(hxs) - 6000), max(hi, max(hxs) + 6000)
        if t0.get("_implicit"):
            # 表头自识别：表被切到多个 sheet 时仍按坐标取行；y 窗口稍放宽以容纳双层表头。
            near = [r for r in tr if lo <= float(r["x"]) <= hi and (y0 - 45000) < float(r["y"]) < (y0 + 4000)]
        else:
            near = [r for r in tr if r.get("sheet") == sheet and lo <= float(r["x"]) <= hi and (y0 - 45000) < float(r["y"]) < (y0 + 2000)]
        headers = [r for r in near if _schedule_header_type(r["text"])]
        header_groups = _selected_schedule_header_sets(headers, t0)
        if not header_groups:
            continue
        title_kind = _schedule_title_type(t0["text"])
        # 表头自识别时，用表头行里相邻表头列的间距推名称列容差（数据往往不与表头严格同 x）。
        row_hdr_xs = sorted({round(float(r["x"]), 3) for r in near
                             if abs(float(r["y"]) - y0) < 1500 and _schedule_header_type(r["text"])}) if t0.get("_implicit") else []
        # 名称列容差避免把单位/数量列文字当作图例；表组按标题距离过滤后逐组解析。
        for hmap in header_groups:
            nx = float(hmap["name"]["x"])
            qx = float(hmap["qty"]["x"])
            ux = float(hmap["unit"]["x"]) if hmap.get("unit") else x0
            sx = float(hmap["spec"]["x"]) if hmap.get("spec") else None
            xmin, xmax = min(nx, sx if sx is not None else nx) - 4000, max(qx, ux, sx if sx is not None else qx) + 3500
            win = [r for r in near if xmin <= float(r["x"]) <= xmax]
            name_anchors = []
            is_name_header = str(hmap["name"]["text"]).strip() in ("名称", "苗木名称", "植物名称", "品种", "品名",
                                                                 "中文名称", "中文名", "苗木中文名", "植物中文名", "中文植物名称")
            other_name_xs = [float(g["name"]["x"]) for g in header_groups if g is not hmap]
            name_gap = min([abs(nx - x) for x in other_name_xs if abs(nx - x) > 1], default=None)
            name_x_tol = min(1200.0, name_gap / 2.0) if name_gap else 1200.0
            if row_hdr_xs:
                col_gap = min([abs(nx - x) for x in row_hdr_xs if abs(nx - x) > 50.0], default=None)
                if col_gap:
                    name_x_tol = min(3000.0, max(name_x_tol, col_gap / 2.0))
            for r in win:
                name, spec0 = _split_schedule_name_spec(r["text"])
                if abs(float(r["x"]) - nx) >= name_x_tol or not name:
                    continue
                # 表行在名称表头下方（CAD y 向上时更小）；不把标题上方的图名/专业栏当植物。
                if float(r["y"]) >= float(hmap["name"]["y"]):
                    continue
                if name in HEADER_WORDS or name in ("种植苗木表",):
                    continue
                clean = re.sub(r"\s+", "", name)
                if any(w in clean for w in SCHEDULE_NON_PLANT_WORDS):
                    continue
                if is_name_header and not _is_plant_name(name):
                    continue
                if not is_name_header and _is_number(name):
                    continue
                name_anchors.append((r, name, spec0))
            # 连续表行聚类：表头下方第一段密集行为苗木表；大间隔后的构造大样/说明文字不解析。
            below = sorted([a for a in name_anchors if float(a[0]["y"]) < float(hmap["name"]["y"])],
                           key=lambda a: float(a[0]["y"]), reverse=True)
            if below:
                ys = [float(a[0]["y"]) for a in below]
                gaps = [a - b for a, b in zip(ys, ys[1:]) if a - b > 1e-6]
                if gaps:
                    med_gap = sorted(gaps)[len(gaps) // 2]
                    break_gap = max(50.0, med_gap * 5.0)
                    keep = [below[0]]
                    for a in below[1:]:
                        if keep[-1] and float(a[0]["y"]) < float(keep[-1][0]["y"]) - break_gap:
                            break
                        keep.append(a)
                    name_anchors = keep
            for name_rec, plant_name, merged_spec in name_anchors:
                y = float(name_rec["y"])
                # 行距自适应：窄行表不能把上下行数量串行；常规表仍允许表头分层。
                row_ys = sorted({round(float(a[0]["y"]), 3) for a in name_anchors})
                row_gaps = [b - a for a, b in zip(row_ys, row_ys[1:]) if 1e-6 < b - a < 100000]
                y_tol = max(2.0, min(420.0, (min(row_gaps) / 3.0) if row_gaps else 420.0))
                band = [r for r in win if abs(float(r["y"]) - y) < y_tol]
                qty = min([r for r in band if _is_number(r["text"]) and abs(float(r["x"]) - qx) < 4000],
                          key=lambda r: abs(float(r["x"]) - qx), default=None)
                if not qty:
                    continue
                unit = min([r for r in band if _is_unit(r["text"])], key=lambda r: abs(float(r["x"]) - ux), default=None)
                spec = merged_spec
                if sx is not None and not spec:
                    spec_rec = min([r for r in band if abs(float(r["x"]) - sx) < 4000 and r["text"].strip()],
                                   key=lambda r: abs(float(r["x"]) - sx), default=None)
                    spec = (spec_rec or {}).get("text", "").strip()
                raw_unit = (unit or {}).get("text", "").strip().replace(" ", "")
                unit_alias = {"平方米": "m²", "M2": "m²", "M²": "m²", "㎡": "m²"}
                explicit_header_unit = _schedule_header_qty_unit(hmap["qty"]["text"])
                if explicit_header_unit:
                    unit_txt = explicit_header_unit
                else:
                    unit_txt = unit_alias.get(raw_unit, raw_unit)
                unit_evidence = bool(unit_txt)
                if not unit_txt:
                    unit_txt = "待核对"
                key = (plant_name, unit_txt)
                if key in seen:
                    continue
                seen.add(key)
                category, cls_token = classify(plant_name, cfg, unit_txt)
                # 数量=0 的设计表行不是可用基线（多为面积式/密度式种植），只作复核线索，不推算株数。
                zero_qty = float(qty["text"]) == 0.0
                if zero_qty:
                    conf_layer, final_qty, in_main = CONF_P3, False, "否"
                    review = "是；设计表数量=0（面积式/待定），需按图纸面积×种植密度折算，不自动推算株数"
                    basis_txt = "苗木表结构化表行（数量=0，面积式线索，不计主线）"
                else:
                    conf_layer, final_qty, in_main = (CONF_P0 if unit_evidence else CONF_P1), unit_evidence, "是"
                    review = "否" if unit_evidence else "是；数量单位无表头/单位列证据，不默认为株"
                    basis_txt = "苗木表结构化表行（设计基线，非逐株点数）"
                rows.append({"分类": category, "来源": "苗木表", "植物名/图例名": plant_name, "规格与图例文字": spec,
                             "统计数量": float(qty["text"]), "单位": unit_txt,
                             "计量方式": basis_txt, "平面图文字标记数": "",
                             "口径": "苗木表设计给定数量（概算底稿基线）" if not zero_qty else "苗木表数量=0（面积式/待定，仅复核线索）",
                             "置信分层": conf_layer,
                             "置信度": cfg["confidence"]["direct"] if unit_evidence else cfg["confidence"]["block_name"],
                             "需核对": review,
                             "证据坐标": f"x={float(name_rec['x']):.0f},y={float(name_rec['y']):.0f}",
                             "规格证据": f"表区sheet={sheet};标题={t0['text']};标题类型={title_kind};表头={hmap['name']['text']}/{hmap['qty']['text']};数量单位证据={'表头' if explicit_header_unit else ('单位列' if unit_evidence else '缺失')}" + (f";规格={spec}" if spec else ""),
                             "文件": str(scan.get("source_file") or ""),
                             "图层": str(t0.get("layer") or ""), "分类依据": f"植物类别={category};命中={cls_token or '单位/默认'}" + (f";参考库={_library_hit(cfg, cls_token)}" if _library_hit(cfg, cls_token) else ""),
                             "参考库命中": _library_hit(cfg, cls_token),
                             "依据": "图纸苗木表结构化文字解析", "计入主线": in_main, "final_quantity": final_qty, "使用边界": BOUNDARY})
                meta.append({"kind": "plant_schedule", "name": plant_name, "qty": float(qty["text"]), "unit": unit_txt,
                             "unit_evidence": unit_evidence,
                             "sheet": sheet, "category": category, "title": t0["text"], "title_kind": title_kind})

    return rows, meta


def _library_name_variants(name):
    """参考库名称归一：保留原名，并追加去掉括号备注后的基础名。"""
    base = re.sub(r"\s+", "", str(name or ""))
    out = [base] if base else []
    stripped = re.sub(r"[（(][^）)]*[）)]", "", base).strip()
    if stripped and stripped != base and 2 <= len(stripped) <= 20:
        out.append(stripped)
    return out


def _library_section_category(section):
    sec = re.sub(r"\s+", "", str(section or ""))
    for token, cat in PLANT_LIBRARY_SECTION_CATEGORY:
        if token and token in sec:
            return cat
    return None


def load_plant_library(path):
    """读取本地植物名称参考库（.json/.csv/.xlsx/.xlsm）。

    只取“中文名称 → 大类”，显式忽略规格、种植密度、苗价/综合单价等列；
    参考库只用于分类与图例识别，绝不用于自动推断规格或报价。
    """
    path = Path(path)
    source = str(path)
    empty = {"names": {}, "sections": {}, "source": source, "warnings": [], "count": 0}
    if not path.exists():
        empty["warnings"] = [f"参考库不存在：{path}"]
        return empty
    names, sections, warnings = {}, {}, []
    suffix = path.suffix.lower()
    try:
        if suffix == ".json":
            data = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(data, dict) and str(data.get("schema") or "").endswith("plant-library-index/v2"):
                # v2 索引只描述分区结构，条目在 rules/plant_library/<大区>/<城市>.json，不算空库告警。
                return empty
            if isinstance(data, dict) and isinstance(data.get("names"), dict):
                for nm, cat in data["names"].items():
                    if cat in PLANT_LIBRARY_CATEGORY_KEYS and str(nm).strip():
                        names.setdefault(str(nm).strip(), cat)
            if isinstance(data, dict) and isinstance(data.get("categories"), dict):
                for cat, lst in data["categories"].items():
                    if cat in PLANT_LIBRARY_CATEGORY_KEYS and isinstance(lst, (list, tuple)):
                        for nm in lst:
                            nm = str(nm).strip()
                            if nm:
                                names.setdefault(nm, cat)
            if isinstance(data, dict) and isinstance(data.get("plants"), list):
                for it in data["plants"]:
                    if not isinstance(it, dict):
                        continue
                    nm = str(it.get("name") or it.get("中文名称") or it.get("名称") or "").strip()
                    cat = str(it.get("category") or it.get("分类") or it.get("类别") or "").strip()
                    if nm and cat in PLANT_LIBRARY_CATEGORY_KEYS:
                        names.setdefault(nm, cat)
            if isinstance(data, list):
                for it in data:
                    if not isinstance(it, dict):
                        continue
                    nm = str(it.get("name") or it.get("中文名称") or it.get("名称") or "").strip()
                    cat = str(it.get("category") or it.get("分类") or it.get("类别") or "").strip()
                    if nm and cat in PLANT_LIBRARY_CATEGORY_KEYS:
                        names.setdefault(nm, cat)
        elif suffix == ".csv":
            with path.open(encoding="utf-8-sig", newline="") as fh:
                for row in csv.DictReader(fh):
                    nm = str(row.get("中文名称") or row.get("名称") or row.get("植物名") or row.get("name") or "").strip()
                    cat = str(row.get("分类") or row.get("类别") or row.get("category") or "").strip()
                    if not nm:
                        continue
                    if cat not in PLANT_LIBRARY_CATEGORY_KEYS:
                        cat = _library_section_category(row.get("章节") or row.get("section") or "") or ""
                    if cat:
                        for cand in _library_name_variants(nm):
                            names.setdefault(cand, cat)
        elif suffix in (".xlsx", ".xlsm"):
            try:
                import openpyxl  # type: ignore
            except Exception as exc:
                empty["warnings"] = [f"openpyxl 不可用，无法读取 xlsx 参考库：{exc}"]
                return empty
            wb = openpyxl.load_workbook(str(path), data_only=True)
            for ws in wb.worksheets:
                name_col, header_row = None, None
                max_r = int(ws.max_row or 0)
                max_c = min(int(ws.max_column or 0), 30)
                for r in range(1, min(max_r, 40) + 1):
                    for c in range(1, max_c + 1):
                        v = ws.cell(r, c).value
                        if isinstance(v, str) and any(k in re.sub(r"\s+", "", v) for k in ("中文名称", "植物名称", "苗木名称", "名称")):
                            name_col, header_row = c, r
                            break
                    if name_col:
                        break
                if name_col is None:
                    continue  # 无名称列的工作表跳过（空表/纯价格表一律不读）
                cur = None
                for r in range(1, max_r + 1):
                    a = ws.cell(r, 1).value
                    if isinstance(a, str):
                        sec = _library_section_category(a)
                        if sec and not str(ws.cell(r, name_col).value or "").strip():
                            cur = sec
                            sections[a.strip()] = sections.get(a.strip(), 0) + 1
                            continue
                    nm = ws.cell(r, name_col).value
                    if not isinstance(nm, str) or not nm.strip():
                        continue
                    cat = _library_section_category(nm) or cur
                    if not cat:
                        continue
                    for cand in _library_name_variants(nm):
                        if 2 <= len(cand) <= 20:
                            names.setdefault(cand, cat)
            wb.close()
        else:
            empty["warnings"] = [f"不支持的参考库格式：{suffix or '无扩展名'}"]
            return empty
    except Exception as exc:
        empty["warnings"] = [f"参考库读取失败：{exc}"]
        return empty
    if not names:
        empty["warnings"] = [f"参考库未解析到可用植物名：{path}"]
        return empty
    return {"names": names, "sections": sections, "source": source, "warnings": warnings, "count": len(names)}


def merge_plant_library(cfg, library):
    """把参考库名称并入植物词库；只补现有词库尚未覆盖的名称，不改动既有分类。"""
    names = (library or {}).get("names") or {}
    builtin = []
    for key in PLANT_LIBRARY_CATEGORY_KEYS.values():
        for tok in cfg.get(key) or []:
            tok = str(tok).strip()
            if tok:
                builtin.append(tok.lower())
    lib_map = dict(cfg.get("plant_library") or {})
    added, added_names = {}, set()
    for nm, cat in names.items():
        nm = str(nm).strip()
        key = PLANT_LIBRARY_CATEGORY_KEYS.get(cat)
        if not nm or not key:
            continue
        lib_map.setdefault(nm, cat)
        # 已被内建/项目词库覆盖的名称保持原分类，参考库只填缺口。
        if any(tok in nm.lower() for tok in builtin):
            continue
        cfg.setdefault(key, []).append(nm)
        added.setdefault(cat, []).append(nm)
        added_names.add(nm)
    cfg["plant_library"] = lib_map
    cfg["plant_library_added"] = set(cfg.get("plant_library_added") or set()) | added_names
    return added


def _library_hit(cfg, token):
    """只有“参考库真正补进来的名称”才算参考库命中；内建/项目词库已覆盖的不算。"""
    lib = cfg.get("plant_library") or {}
    added = cfg.get("plant_library_added") or set()
    tok = str(token or "").strip()
    if tok and tok in added and tok in lib:
        return f"{lib[tok]}:{tok}"
    return ""


def classify(name, cfg, unit=""):
    """按项目词库给植物名做弱分类；只用于分组，不改变数量口径。"""
    name = (name or "").strip()
    low = name.lower()
    groups = (
        ("地被", "plant_groundcover"),
        ("灌木", "plant_shrubs"),
        ("乔木", "plant_trees"),
        ("其他", "plant_other"),
    )
    # 最长命中优先：避免短名（如“含笑”）盖过更具体的植物名（如“乐昌含笑”）；
    # 同长度仍按 地被>灌木>乔木>其他 的原判定顺序，保持既有分类不倒退。
    best = None
    for gi, (label, key) in enumerate(groups):
        for token in cfg.get(key) or []:
            token = str(token).strip()
            if not token:
                continue
            if token.lower() in low or token in name:
                cand = (len(token), -gi, label, token)
                if best is None or cand > best:
                    best = cand
    if best:
        return best[2], best[3]
    # 兜底词：不依赖完整词库也能把常见图例归入可用大类。
    fallback = (("草", "地被"), ("地被", "地被"), ("灌", "灌木"), ("球", "灌木"),
                ("绿篱", "灌木"), ("篱", "灌木"), ("乔", "乔木"), ("树", "乔木"),
                ("竹", "其他"), ("conifer", "乔木"), ("palm", "乔木"), ("tree", "乔木"),
                ("shrub", "灌木"), ("bush", "灌木"), ("perennial", "地被"), ("annual", "地被"),
                ("ground cover", "地被"), ("groundcover", "地被"), ("grass", "地被"),
                ("lawn", "地被"), ("herbaceous", "地被"), ("herb", "地被"), ("fern", "地被"),
                ("wildflower", "地被"), ("meadow", "地被"), ("bulb", "地被"), ("aquatic", "地被"),
                ("climber", "其他"), ("vine", "其他"), ("pot", "其他"), ("ornamental", "其他"))
    for token, label in fallback:
        if token in low or token in name:
            return label, token
    u = (unit or "").strip().lower().replace(" ", "")
    if u in ("m2", "㎡", "m²", "平方米") or "株/m2" in u or "株/㎡" in u or "株/m²" in u:
        return "地被/绿篱", "单位面积"
    return "其他", ""


def _plant_legend_records(landscape):
    """合并 plant_legends 与 systems 中的种植文字候选，兼容欧美图和底座新结构。"""
    if not landscape:
        return []
    out, seen = [], set()

    def add(r):
        if not isinstance(r, dict):
            return
        nm = str(r.get("plant") or r.get("name") or r.get("raw") or r.get("legend_raw") or r.get("text") or "").strip()
        if not nm:
            return
        key = (nm, str(r.get("layer") or ""), _num(r.get("x")), _num(r.get("y")))
        if key in seen:
            return
        seen.add(key)
        rr = dict(r)
        rr.setdefault("plant", nm)
        out.append(rr)

    for r in landscape.get("plant_legends") or []:
        add(r)
    plant_systems = {"planting", "plant", "landscape", "landscape_planting", "绿化", "种植"}
    for r in landscape.get("systems") or []:
        if not isinstance(r, dict):
            continue
        system = str(r.get("system") or "").strip().lower()
        layer = str(r.get("layer") or "").lower()
        if system not in plant_systems and not any(k in layer for k in ("plant -", "ground cover", "绿化", "种植", "苗木")):
            continue
        rr = dict(r)
        if not (rr.get("plant") or rr.get("name") or rr.get("raw") or rr.get("legend_raw")):
            rr["plant"] = rr.get("text")
        add(rr)
    return out


def plant_rows(landscape, scan, cfg):
    rows, meta = [], {"by_name": {}, "review": [], "evidence": [], "warnings": [], "conflicts": []}
    # 底座块图例候选
    blk_rows = {}
    if landscape:
        blk_rows = {str(r.get("name") or r.get("plant") or ""): r for r in (landscape.get("plant_block_legends") or []) if isinstance(r, dict) and str(r.get("name") or r.get("plant") or "").strip()}
    # cad_scan 的 DXF 块引用计数不依赖块坐标，可补齐底座只输出部分植物块的场景。
    ref_counts = {}
    if scan:
        for nm, cnt in ((scan.get("meta") or {}).get("block_refs") or {}).items():
            n = _num(cnt)
            if n is not None and n > 0:
                ref_counts[str(nm).strip()] = int(n)
    # 从 scan 提取 INSERT 实例坐标（块引用文本/名称）
    instances = {}
    for rec in iter_records(scan) if scan else []:
        if str(rec.get("kind") or rec.get("type") or "").upper() not in ("INSERT", "MINSERT", "BLOCK"):
            continue
        nm = str(rec.get("text") or rec.get("name") or rec.get("block_name") or "").strip()
        if not nm:
            continue
        instances.setdefault(nm, []).append((_num(rec.get("x")), _num(rec.get("y"))))
        if rec.get("x") is not None and rec.get("y") is not None:
            blk_rows.setdefault(nm, {})
    # 图例文字（植物名/规格证据）；plant_legends 是主来源，systems 只补种植系统候选。
    legend_records = _plant_legend_records(landscape)
    legends = {}
    for r in legend_records:
        text = str(r.get("plant") or r.get("name") or r.get("raw") or r.get("legend_raw") or r.get("text") or "").strip()
        if text:
            legends.setdefault(text, r)

    sched, smeta = plant_schedule_rows(scan, cfg)
    sched_names = {r["植物名/图例名"] for r in sched}
    sched_by_name = {}
    for r in sched:
        sched_by_name.setdefault(r["植物名/图例名"], r)
    sched_sheets = {m.get("sheet") for m in smeta}
    # 平面图文字标记数：只作“有没有/备查”证据，绝不能当株数。
    text_counts = {}
    for rec in iter_records(scan) if scan else []:
        if rec.get("sheet") in sched_sheets:
            continue
        t = str(rec.get("text") or "").strip()
        if not t or not sched_names:
            continue
        if any(n and (n in t or t in n) for n in sched_names):
            text_counts[t] = text_counts.get(t, 0) + 1

    def mark_count(name):
        return sum(v for t, v in text_counts.items() if name and (name in t or t in name))

    names = set(blk_rows) | set(instances) | set(ref_counts)
    for name in sorted(names):
        if not name:
            continue
        base = blk_rows.get(name) or {}
        if name not in sched_names and not _is_plant_like(name, cfg, base):
            continue  # 过滤轴线、门窗、图框等非植物块名；中英文植物块名均保留
        raw_instances = instances.get(name) or []
        ref_count = ref_counts.get(name)
        has_instance_points = any(x is not None and y is not None for x, y in raw_instances)
        pts = list(raw_instances)
        if not pts:
            pts = [(p[0], p[1]) for p in ((base.get("x"), base.get("y")),) if p[0] is not None and p[1] is not None]
        try:
            smp = base.get("sample_coords") or base.get("evidence") and base.get("evidence")[0].get("sample_coords")
        except Exception:
            smp = None
        if pts:
            pts.extend([(p[0], p[1]) for p in (smp or []) if p and p[0] is not None and p[1] is not None])
        uq = _unique_pts(pts, float(cfg.get("dedupe_tolerance") or 0.5))
        base_count = _num(base.get("instance_count"))
        # 计数口径分层：有坐标才去重；只有底座/块引用计数时保留总数但标明未逐点去重。
        if has_instance_points:
            count = len(uq)
            method = "块级实例去重计数"
            tier, conf = CONF_P0, cfg["confidence"]["block_name"]
            need_check = ""
        elif raw_instances:
            count = len(raw_instances)
            method = "块引用记录（无坐标，未去重）"
            tier, conf = CONF_P2, cfg["confidence"]["inferred"]
            need_check = "是；有块引用记录但无坐标，未逐点去重；需人工核对"
        elif base_count is not None:
            count = int(base_count)
            method = "底座块实例计数（无坐标，未逐点去重）"
            tier, conf = CONF_P1, cfg["confidence"]["pattern"]
            need_check = ""
        elif ref_count is not None:
            count = ref_count
            method = "块引用总数（无坐标，未去重）"
            tier, conf = CONF_P2, cfg["confidence"]["inferred"]
            need_check = "是；仅有块引用总数，无坐标/底座候选，未去重；需人工核对"
        else:
            count = len(uq)
            method = "无可靠计数"
            tier, conf = CONF_P2, cfg["confidence"]["inferred"]
            need_check = "是；无坐标或块引用计数，需人工核对"
        if count <= 0:
            continue
        have_coords = bool(uq)
        category = str(base.get("category") or base.get("type") or "")
        cls_token = ""
        if category not in ("乔木", "灌木", "地被", "地被/绿篱", "其他"):
            category, cls_token = classify(name, cfg, str(base.get("unit") or ""))
        # 规格证据：图例文字含块名时取整条文字
        spec, spec_hit = "", ""
        for t, r in legends.items():
            if t and (name in t or t in name):
                spec = t[:200]
                spec_hit = str(r.get("file") or "") + "|" + str(r.get("layer") or "") + "|" + str(r.get("x") or "") + "," + str(r.get("y") or "")
                break
        # 苗木表回溯交叉核对（尽力读取，缺失不报错）
        schedule = landscape.get("plant_schedule_links") or [] if landscape else []
        exp = None
        for link in schedule if isinstance(schedule, list) else []:
            if not isinstance(link, dict):
                continue
            nm_l = str(link.get("plant") or link.get("name") or link.get("block_name") or "")
            if nm_l and (nm_l == name or nm_l in name or name in nm_l):
                for k in ("qty", "count", "数量", "expected_qty", "expected_quantity"):
                    v = _num(link.get(k))
                    if v is not None:
                        exp = v
                        break
                if exp:
                    break
        if exp is None and name in sched_by_name:
            exp = _num(sched_by_name[name].get("统计数量"))
        if exp is not None and abs(exp - count) > 1e-6:
            need_check = f"苗木表={exp:g} 与平面块级计数={count:g} 不一致"
            tier, conf = CONF_P3, cfg["confidence"]["review"]
        if base and (base.get("status") == "review" or base.get("review_reason") or base.get("review_reasons")):
            if not need_check:
                need_check = f"底座{base.get('review_reason') or '缺复核'}：{base.get('status')}"
            if tier != CONF_P3:
                tier, conf = CONF_P2, cfg["confidence"]["inferred"]

        coord_ev = "; ".join(f"{x:g},{y:g}" for x, y in uq[:20]) or f"无坐标；块计数={count}"
        need_txt = need_check or ("否" if tier not in (CONF_P2, CONF_P3) else "是")
        final = tier in (CONF_P0, CONF_P1) and need_txt == "否"
        rows.append({
            "分类": category, "来源": "平面图图例", "植物名/图例名": name, "规格与图例文字": spec,
            "统计数量": count, "单位": "株", "计量方式": method,
            "平面图文字标记数": mark_count(name), "口径": "按图例分类计数（概算草稿）",
            "置信分层": tier, "置信度": round(conf, 3), "需核对": need_txt,
            "证据坐标": coord_ev, "规格证据": spec_hit[:200], "文件": str(base.get("file") or "") or str((scan or {}).get("source_file") or ""),
            "图层": str(base.get("layer") or ";".join(sorted({str(r.get("layer")) for r in ((landscape or {}).get("plant_block_legends") or []) if isinstance(r, dict) and str(r.get("name") or r.get("plant"))==name}))) or "",
            "分类依据": f"植物类别={category};命中={cls_token or '块名/词库'}" + (f";参考库={_library_hit(cfg, cls_token)}" if _library_hit(cfg, cls_token) else ""),
            "参考库命中": _library_hit(cfg, cls_token),
            "依据": "cad-file-reader plant_block_legends/block INSERT 实例",
            "计入主线": "是" if final else "否", "final_quantity": final, "使用边界": BOUNDARY,
        })
        if exp is not None and abs(exp - count) > 1e-6:
            meta["conflicts"].append({"名称": name, "设计表数量": exp, "平面计数": count,
                                      "差异": round(exp - count, 4),
                                      "冲突原因": "同名设计表与平面块级计数不一致；平面行已降P3退出主线"})
        meta["by_name"][name] = {"category": category, "count": count, "tier": tier}
        meta["evidence"].append({"kind": "plant_block_legends", "name": name, "category": category, "instance_count": count, "coords": uq[:60], "tier": tier})

    block_names = {r["植物名/图例名"] for r in rows if r.get("来源") == "平面图图例"}
    # 底座图例文字次数始终作为 P2 候选保留；即使与苗木表同名，也不改动设计基线。
    if landscape:
        legend_groups = {}
        skip_tokens = ("苗木表", "苗木配置表", "总平面图", "平面图", "地被、绿篱", "播种/草坪卷")
        for r in legend_records:
            if not isinstance(r, dict):
                continue
            nm = str(r.get("plant") or r.get("name") or r.get("raw") or r.get("legend_raw") or "").strip()
            if not _is_plant_like(nm, cfg, r):
                continue
            if "/" in nm or "\\" in nm or any(k in nm for k in skip_tokens):
                continue
            legend_groups.setdefault(nm, []).append(r)
        for nm, items in sorted(legend_groups.items()):
            if nm in block_names:
                continue
            cnt = len(items)
            first = items[0]
            category = str(first.get("category") or "")
            cls_token = ""
            if category not in ("乔木", "灌木", "地被", "地被/绿篱", "其他"):
                category, cls_token = classify(nm, cfg, "")
            coords = []
            for it in items[:20]:
                x, y = _num(it.get("x")), _num(it.get("y"))
                if x is not None and y is not None:
                    coords.append(f"{x:g},{y:g}")
            spec = str(first.get("spec") or first.get("legend_raw") or "")[:200]
            same_schedule = "；与苗木表同名，不改设计基线" if nm in sched_names else ""
            rows.append({"分类": category, "来源": "识图图例文字", "植物名/图例名": nm, "规格与图例文字": spec,
                         "统计数量": cnt, "单位": "文字次数", "计量方式": "文字出现次数（非株数）", "平面图文字标记数": cnt,
                         "口径": "底座图例文字出现次数，不进入主线", "置信分层": CONF_P2, "置信度": cfg["confidence"]["inferred"],
                         "需核对": f"是；图例文字次数不能当株数，需人工按图点数{same_schedule}", "证据坐标": "; ".join(coords), "规格证据": spec,
                         "文件": str(first.get("file") or landscape.get("source_file") or ""), "图层": str(first.get("layer") or ""),
                         "分类依据": f"植物类别={category};命中={cls_token or '文字'}" + (f";参考库={_library_hit(cfg, cls_token)}" if _library_hit(cfg, cls_token) else ""), "参考库命中": _library_hit(cfg, cls_token), "依据": "cad-file-reader plant_legends（文字标记，非株数）",
                         "计入主线": "否", "final_quantity": False, "使用边界": BOUNDARY})
        if legend_groups:
            meta["warnings"].append({"分类": "复核提示", "植物名/图例名": "苗木统计", "统计数量": "", "实际铺装面积_m2": "",
                                     "需核对": f"底座提供 {len(legend_groups)} 类、共 {sum(len(v) for v in legend_groups.values())} 条图例文字标记；文字次数不等于株数，已作 P2 候选，未计入主线",
                                     "证据坐标": "", "计算式": "缺可靠块级实例计数；需人工按图点数或结合苗木表核对"})

    # 合并苗木表解析结果：有块计数则交叉核对，无则用苗木表作为设计给定数量。
    for sr in sched:
        nm = sr["植物名/图例名"]
        marks = mark_count(nm)
        if nm in block_names:
            for r in rows:
                if r["来源"] == "平面图图例" and r["植物名/图例名"] == nm and _num(r.get("统计数量")) is not None:
                    if abs(_num(r["统计数量"]) - _num(sr["统计数量"])) > 1e-6:
                        r["需核对"] = f'苗木表={sr["统计数量"]:g} 与平面图点数={r["统计数量"]:g} 不一致'
                        r["置信分层"] = CONF_P3; r["置信度"] = cfg["confidence"]["review"]; r["final_quantity"] = False; r["计入主线"] = "否"
                    r["规格证据"] = (r.get("规格证据") or "") + f';苗木表单位={sr["单位"]}'
                    break
        else:
            if marks:
                sr["规格证据"] = (sr.get("规格证据") or "") + f";平面图文字标记={marks}（标记数非株数）"
        # 设计表行始终保留为设计基线；平面块级行单独分层，冲突不覆盖基线。
        sr["平面图文字标记数"] = marks
        rows.append(sr)

    has_block_plan = any(r.get("来源") == "平面图图例" for r in rows)
    if sched and not has_block_plan:
        meta["warnings"].append({"分类": "复核提示", "植物名/图例名": "苗木统计", "统计数量": "", "实际铺装面积_m2": "",
                                 "需核对": f"已解析苗木表 {len(sched)} 项；但平面图块名/图层不可用，无法逐株交叉核对，苗木表数量仅作设计基线",
                                 "证据坐标": "", "计算式": "块名/图层缺失时不得把苗木表数量冒充平面图点数"})
    if not rows:
        meta["warnings"].append({"分类": "复核提示", "植物名/图例名": "苗木统计", "统计数量": "", "实际铺装面积_m2": "",
                                 "需核对": "没有可用的苗木表、块级实例或图例文字输入，未输出苗木数量",
                                 "证据坐标": "", "计算式": "需要 cad-file-reader 园林识图或图纸苗木表"})
    meta["schedule"] = smeta
    meta["evidence"].extend(smeta)
    return rows, meta


# ---------- 铺装面积 ----------
def _poly_area(poly):
    s = 0.0
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        s += x1 * y2 - x2 * y1
    return s / 2.0


def _point_in_poly(x, y, poly):
    inside = False
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
            inside = not inside
    return inside


def _faces(segs, tol):
    """轻量环面提取：把线段端点吸附成图，按逆时针邻接追踪边界，去重取多边形（面积可正可负）。"""
    key = lambda x, y: (round(x / max(tol, 1e-9)), round(y / max(tol, 1e-9)))
    nodes, edges = {}, []
    for s in segs:
        x1, y1, x2, y2 = s
        a, b = key(x1, y1), key(x2, y2)
        if a == b:
            continue
        nodes.setdefault(a, (x1, y1))
        nodes.setdefault(b, (x2, y2))
        edges.append((a, b))
    if not nodes:
        return []
    pts, idx = nodes, list(nodes)
    pidx = {p: i for i, p in enumerate(idx)}
    adj = [[] for _ in idx]
    edges = {(pidx[a], pidx[b]) for a, b in edges}
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    for i in range(len(idx)):
        adj[i].sort(key=lambda j: math.atan2(pts[idx[j]][1] - pts[idx[i]][1], pts[idx[j]][0] - pts[idx[i]][0]))
    pos = {}
    for i in range(len(idx)):
        for k, j in enumerate(adj[i]):
            pos[i, j] = k
    used, out = set(), []
    guard_max = len(idx) ** 2 + 8
    for a in range(len(idx)):
        for b in list(adj[a]):
            if (a, b) in used:
                continue
            path, cur, nx, guard = [], a, b, 0
            while (cur, nx) not in used and guard < guard_max:
                used.add((cur, nx))
                path.append(cur)
                guard += 1
                ns = adj[nx]
                k = pos.get((nx, cur))
                if k is None:
                    break
                nxt = ns[(k + 1) % len(ns)]
                cur, nx = nx, nxt
            if cur == a and nxt == b and len(path) >= 3 and len(set(path)) == len(path):
                poly = [pts[idx[i]] for i in path] + [pts[idx[a]]]
                ar = _poly_area(poly)
                if abs(ar) > 1e-6:
                    out.append((poly, ar))
    # 去重：同一边界正反追踪只保留一条（面积取绝对值由调用方处理）
    seen, res = set(), []
    for poly, ar in out:
        s = _poly_key(poly)
        if s in seen:
            continue
        seen.add(s)
        res.append((poly, ar))
    return res


def _bbox(poly):
    xs = [p[0] for p in poly]
    ys = [p[1] for p in poly]
    return [min(xs), min(ys), max(xs), max(ys)]


def _centroid(poly):
    return (sum(p[0] for p in poly) / len(poly), sum(p[1] for p in poly) / len(poly))


def _poly_key(poly, digits=6):
    """闭合环去重键：忽略起点和方向，只保留吸附后的点集。"""
    pts = [(round(float(x), digits), round(float(y), digits)) for x, y in poly]
    if len(pts) > 1 and pts[0] == pts[-1]:
        pts = pts[:-1]
    return tuple(sorted(pts))


def _project_exclusion_bboxes(value):
    """解析项目规则中的排除框；支持单个 [x1,y1,x2,y2] 或多框数组。"""
    if not value:
        return []
    boxes = []

    def add(v):
        if isinstance(v, dict):
            xs = [_num(v.get("x1")), _num(v.get("y1")), _num(v.get("x2")), _num(v.get("y2"))]
        elif isinstance(v, (list, tuple)) and len(v) >= 4:
            xs = [_num(v[0]), _num(v[1]), _num(v[2]), _num(v[3])]
        else:
            return
        if all(x is not None for x in xs) and xs[0] <= xs[2] and xs[1] <= xs[3]:
            boxes.append(tuple(xs))

    if isinstance(value, (list, tuple)) and value and isinstance(value[0], (list, tuple, dict)):
        for v in value:
            add(v)
    else:
        add(value)
    return boxes


def _point_in_project_boxes(x, y, boxes):
    return any(x1 <= x <= x2 and y1 <= y <= y2 for x1, y1, x2, y2 in boxes)


def _layer_allowed(layer, cfg):
    layer = str(layer or "").strip()
    low = layer.lower()
    if any(str(layer).strip().lower() == str(x).strip().lower() for x in (cfg.get("exclude_layers") or [])):
        return False
    rx = str(cfg.get("include_layers_regex") or "").strip()
    if rx:
        try:
            if not re.search(rx, layer, re.IGNORECASE):
                return False
        except re.error:
            return False
    return True


def _cad_reader_script():
    """定位 cad-file-reader 的园林几何入口；找不到返回 None。"""
    candidates = []
    for env in ("CAD_FILE_READER_HOME", "CAD_SKILL_DIR"):
        base = os.environ.get(env)
        if base:
            candidates.append(Path(base) / "scripts" / "cad_landscape_geometry.sh")
    candidates.append(Path.home() / ".codex" / "skills" / "cad-file-reader" / "scripts" / "cad_landscape_geometry.sh")
    for path in candidates:
        if path.is_file():
            return path
    return None


def _run_landscape_geometry(dxf_paving, dxf_refs):
    """转调 cad-file-reader 的 cad_landscape_geometry.sh；本技能不再自带 DXF 解析。

    返回 segments/layers/block_refs/units/warnings；reader 缺失或失败直接
    SystemExit(1)，不回退到本技能内部解析。
    """
    script = _cad_reader_script()
    if script is None:
        sys.stderr.write(
            "[yuanlin] 未找到 cad-file-reader：需要 cad-file-reader>=0.41.0 的 "
            "scripts/cad_landscape_geometry.sh。\n"
            "安装：skillhub install cad-file-reader --namespace user_43faedd6\n")
        raise SystemExit(1)
    out_dir = Path(tempfile.mkdtemp(prefix="yuanlin-landscape-"))
    cmd = ["bash", str(script), "--out-dir", str(out_dir)]
    if dxf_paving:
        cmd += ["--block-paving", str(dxf_paving)]
    if dxf_refs:
        cmd += ["--block-refs", str(dxf_refs)]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    except Exception as exc:
        sys.stderr.write(f"[yuanlin] cad_landscape_geometry 调用失败：{exc}\n")
        raise SystemExit(1) from None
    if proc.returncode != 0:
        tail = (proc.stderr or proc.stdout or "").strip().splitlines()[-5:]
        sys.stderr.write("[yuanlin] cad_landscape_geometry 失败 exit %d：%s\n"
                         % (proc.returncode, " | ".join(tail)))
        raise SystemExit(1)
    payloads = []
    for path in sorted(out_dir.glob("*.landscape.json")):
        try:
            doc = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            sys.stderr.write(f"[yuanlin] 无法解析 reader 输出 {path}：{exc}\n")
            raise SystemExit(1) from None
        contract = doc.get("contract") if isinstance(doc.get("contract"), dict) else {}
        if not _is_reader_contract(contract):
            sys.stderr.write(f"[yuanlin] reader 输出缺 cad-contract/v1 契约块：{path}\n")
            raise SystemExit(1)
        payloads.append(doc)
    if not payloads:
        sys.stderr.write("[yuanlin] cad_landscape_geometry 未生成 *.landscape.json\n")
        raise SystemExit(1)

    segments, layers, block_refs, warnings = [], [], [], []
    mm_per_unit = None
    for doc in payloads:
        units = doc.get("units") if isinstance(doc.get("units"), dict) else {}
        if units.get("drawing_mm_per_unit") and mm_per_unit is None:
            mm_per_unit = float(units["drawing_mm_per_unit"])
        for ring in doc.get("paving_rings") or []:
            if not isinstance(ring, dict):
                continue
            label = str(ring.get("layer_label") or ring.get("layer") or "未知铺装图层")
            if not label.startswith("（DXF"):
                label = "（DXF回退）" + label
            clean = []
            for point in ring.get("points") or []:
                try:
                    x, y = float(point[0]), float(point[1])
                except Exception:
                    continue
                if clean and abs(clean[-1][0] - x) < 1e-12 and abs(clean[-1][1] - y) < 1e-12:
                    continue
                clean.append((x, y))
            while len(clean) > 1 and abs(clean[0][0] - clean[-1][0]) < 1e-12 and abs(clean[0][1] - clean[-1][1]) < 1e-12:
                clean.pop()
            if len(clean) < 3:
                continue
            for i, (x1, y1) in enumerate(clean):
                x2, y2 = clean[(i + 1) % len(clean)]
                segments.append([x1, y1, x2, y2])
                layers.append(label)
        for ref in doc.get("block_refs") or []:
            if not isinstance(ref, dict):
                continue
            name = str(ref.get("block_name") or ref.get("name") or "").strip()
            if not name:
                continue
            block_refs.append({
                "kind": "INSERT", "text": name,
                "x": _num(ref.get("x")), "y": _num(ref.get("y")),
                "layer": str(ref.get("layer") or ""), "source": "dxf_block_ref",
            })
        for item in doc.get("review") or []:
            reason = str((item or {}).get("reason") or "")
            if any(k in reason for k in ("失败", "不可用", "超过安全上限", "未读到")):
                warnings.append(reason)
    # 只清理本次 reader 临时产物；保留目录本身失败时忽略。
    for path in out_dir.glob("*.landscape.*"):
        try:
            path.unlink()
        except OSError:
            pass
    try:
        out_dir.rmdir()
    except OSError:
        pass
    return {"segments": segments, "layers": layers, "block_refs": block_refs,
            "insert_count": len(block_refs), "mm_per_unit": mm_per_unit,
            "warnings": warnings}


FORMAL_YUANLIN_PROVENANCE = {"reader", "bus"}


def _is_reader_contract(contract):
    """reader 契约块版本判断：兼容 contract_version（cad-file-reader/v0 外壳）
    与老式顶层 schema=cad-contract/v1。"""
    if not isinstance(contract, dict):
        return False
    version = str(contract.get("contract_version") or contract.get("schema") or "").strip()
    return version == "cad-contract/v1" and bool(str(contract.get("contract_id") or "").strip())


def _doc_provenance(doc):
    """取识图输入的来源；reader 产物可能只有 contract 块、没有顶层 provenance。"""
    if not isinstance(doc, dict):
        return "manual"
    prov = str(doc.get("provenance") or "").strip().lower()
    if prov:
        return prov
    contract = doc.get("contract") if isinstance(doc.get("contract"), dict) else {}
    prov = str(contract.get("provenance") or "").strip().lower()
    if prov:
        return prov
    if _is_reader_contract(contract):
        return "reader"
    if str(doc.get("schema") or "") == "cad-contract/v1" and str(doc.get("contract_id") or "").strip():
        return "reader"
    # cad_scan 详情：无 schema、无 contract，但带 text_records/layers/geometry_segments，
    # 是本机 reader 直接产出的识图证据，不是手工表。
    if all(k in doc for k in ("text_records", "layers", "geometry_segments")):
        return "reader"
    return "manual"


def _doc_contract_id(doc):
    if not isinstance(doc, dict):
        return ""
    return str(doc.get("contract_id") or (doc.get("contract") or {}).get("contract_id") or "").strip()


def unwrap_bus_contract(data):
    """bus 外壳 {schema:cad-contract/v1, contract:{...}} → 内层园林 payload。"""
    if isinstance(data, dict) and data.get("schema") == "cad-contract/v1":
        inner = data.get("contract")
        if isinstance(inner, dict):
            # 内层可能还嵌一层 cad-contract/v1；只取带园林数组的那层。
            for cand in (inner, inner.get("contract")):
                if isinstance(cand, dict) and any(k in cand for k in (
                        "plant_legends", "plant_block_legends", "paving_closed_areas", "hardscape")):
                    return cand
    return data


def guard_yuanlin_sources(landscape, scan, has_raw_dxf, allow_manual):
    """按输入 provenance 判定来源；raw DXF 回退按手工来源，必须显式 --allow-manual。"""
    docs = [("--landscape", landscape), ("--scan", scan)]
    docs = [(label, doc) for label, doc in docs if isinstance(doc, dict)]
    if has_raw_dxf:
        docs.append(("--dxf-block-*", {"provenance": "manual"}))
    if not docs:
        raise GuardError(5, "没有可用输入。",
                         hint="至少提供 --landscape / --scan / --dxf-block-paving / --dxf-block-refs 之一。")
    provs, ids, shas, rvs, warnings = [], [], [], [], []
    for label, doc in docs:
        prov = _doc_provenance(doc)
        # cad_scan 详情是识图证据、不是契约，本身不带 provenance；
        # 只要 schema 标了 cad-file-reader/v0，就按 reader 证据处理，避免被误判成手工。
        if not prov and str(doc.get("schema") or "") == "cad-file-reader/v0":
            prov = "reader"
            warnings.append("%s 无 provenance，按 cad-file-reader 识图证据处理。" % label)
        provs.append(prov)
        if prov not in FORMAL_YUANLIN_PROVENANCE:
            warnings.append("%s 的 provenance=%s，按手工来源处理。" % (label, prov or "缺失"))
        cid = _doc_contract_id(doc)
        if cid:
            ids.append(cid)
        contract = doc.get("contract") if isinstance(doc.get("contract"), dict) else {}
        sha = str(doc.get("source_sha256") or contract.get("source_sha256") or "").strip()
        if sha:
            shas.append(sha)
        rv = str(doc.get("reader_version") or contract.get("reader_version") or "").strip()
        if rv:
            rvs.append(rv)
    formal = all(p in FORMAL_YUANLIN_PROVENANCE for p in provs)
    if not formal and not allow_manual:
        raise GuardError(3, "输入 provenance=%s，不是 reader/bus，拒入正式链路。"
                          % "、".join(sorted(set(provs))),
                         hint="确认是手工/旧识图结果后加 --allow-manual；结果强制 final_quantity=false。")
    return {
        "mode": "formal" if formal else "manual",
        "provenance": "reader" if formal else "manual",
        "contract_id": ",".join(dict.fromkeys(ids)),
        "source_sha256": ",".join(dict.fromkeys(shas)),
        "contract_sha256": "",
        "reader_version": rvs[0] if rvs else "",
        "formal_ledger_eligible": bool(formal),
        "warnings": warnings,
    }


def paving_area_implausible(raw_area: float, frame_m2: float,
                            cap_m2: float = 1e8, ratio_limit: float = 3.0) -> tuple[bool, str]:
    """铺装强算候选面积的合理性判据（真图驱动，0.4.33）。

    真图教训：sample-road种植总图图层名解码失败，--paving-all-geometry 对全几何做闭环，
    把图框线、苗木表表格线、种植符号一并闭成"假环"，算出 74 亿 m²（真实铺装应为万级）。
    判据一（绝对上限）：没有任何单体景观/园林工程的铺装能到 cap_m2（默认 100 km²）；
    判据二（相对图幅）：仅当图幅外接面积本身可信（<cap_m2）时才用——多图框 DWG 的
    总 bbox 会被撑大（该图实测 375 亿 m²），此时相对判据不可用，只靠绝对上限。
    """
    bad_neg = raw_area < 0
    bad_cap = raw_area > cap_m2
    bad_ratio = frame_m2 > 0 and frame_m2 < cap_m2 and raw_area > frame_m2 * ratio_limit
    if bad_neg:
        return True, f"强算候选 {raw_area:,.0f} m² 为负，判定不可信"
    if bad_cap:
        return True, f"强算候选 {raw_area:,.0f} m² 超过可信上限 {cap_m2:,.0f} m²"
    if bad_ratio:
        return True, (f"强算候选 {raw_area:,.0f} m² 达图幅外接面积 {frame_m2:,.0f} m² 的 "
                      f"{raw_area / frame_m2:,.1f} 倍（阈值 {ratio_limit:g} 倍）")
    return False, ""


def paving_rows(landscape, scan, cfg, scale_unit, all_geometry=False):
    rows, review = [], []
    segs_by_layer, blank_layer_segs = {}, []
    has_geometry = False
    forced_mode = False
    paving_tokens = [str(t).upper() for t in (cfg.get("paving_layer_tokens") or []) if str(t).strip()]
    ex_boxes = _project_exclusion_bboxes(cfg.get("exclude_frame_bbox"))
    excluded_segments = 0
    if scan:
        for g in iter_geometry(scan):
            has_geometry = True
            layer = g["layer"]
            up = layer.upper()
            if not up:
                if _point_in_project_boxes(g["x1"], g["y1"], ex_boxes) and _point_in_project_boxes(g["x2"], g["y2"], ex_boxes):
                    excluded_segments += 1
                    continue
                blank_layer_segs.append((g["x1"], g["y1"], g["x2"], g["y2"]))
            if not any(t in up for t in paving_tokens):
                continue
            if not _layer_allowed(layer, cfg):
                continue
            if _point_in_project_boxes(g["x1"], g["y1"], ex_boxes) and _point_in_project_boxes(g["x2"], g["y2"], ex_boxes):
                excluded_segments += 1
                continue
            segs_by_layer.setdefault(layer, []).append((g["x1"], g["y1"], g["x2"], g["y2"]))
        if excluded_segments and len(review) < 50:
            review.append({"layer": "（项目规则排除）", "reason": f"项目规则 exclude_frame_bbox 排除 {excluded_segments} 段完全位于排除框内的铺装图层几何", "evidence": f"excluded_segments={excluded_segments}, boxes={ex_boxes}", "confidence": cfg["confidence"]["review"]})
        if not segs_by_layer:
            if blank_layer_segs and all_geometry:
                forced_mode = True
                segs_by_layer["（无图层，全几何候选）"] = blank_layer_segs
                review.append({"layer": "（无图层，全几何候选）", "reason": "图层名缺失，按全部几何做闭环候选；仅作 P3 证据，不计入主线面积", "evidence": f"blank_layer_segments={len(blank_layer_segs)}", "confidence": cfg["confidence"]["review"]})
            elif blank_layer_segs:
                review.append({"layer": "（图层名缺失）", "reason": f"几何有 {len(blank_layer_segs)} 段但无图层名，无法区分铺装；如需生成 P3 候选请加 --paving-all-geometry 并人工复核", "evidence": f"blank_layer_segments={len(blank_layer_segs)}", "confidence": cfg["confidence"]["review"]})
            else:
                review.append({"layer": "（未命中铺装图层）", "reason": "有几何但未命中铺装图层 token，无法确认铺装范围；面积未计算", "evidence": f"geometry_segments={sum(len(x or []) for x in (scan.get('geometry_segments') or []))}", "confidence": cfg["confidence"]["review"]})
    scale = float(scale_unit["scale"])
    mm = float(scale_unit["drawing_mm_per_unit"])
    # 模型空间几何按实际尺寸绘制，图纸文字里的 1:500/1:100 只是打印比例，
    # 不能再乘一次；只有非模型空间（如图纸单位本身就是纸面单位）才应用比例。
    geom_scale = 1.0 if has_geometry else scale
    scale_basis = "模型空间1:1（打印比例不参与面积）" if has_geometry else "图纸比例"
    # 闭合容差按图纸单位归一：默认 50 视作毫米，图纸单位为米时换算成 0.05 图纸单位。
    tol = float(cfg.get("geometry_close_tolerance") or 50) / max(mm, 1e-9)
    layers = sorted(segs_by_layer)
    if not layers and landscape and landscape.get("paving_closed_areas"):
        for r in landscape.get("paving_closed_areas") or []:
            if not isinstance(r, dict):
                continue
            layer = str(r.get("layer") or "未知铺装图层")
            review.append({"layer": layer, "reason": "缺 geometry_segments/geometry_layers，底座仅给闭合环候选，降级不计算面积", "evidence": json.dumps({"closed_ring_candidates": r.get("closed_ring_candidates"), "region_candidates": r.get("region_candidates")}, ensure_ascii=False)[:400], "confidence": cfg["confidence"]["review"]})
    if not layers and not review:
        review.append({"layer": "（无铺装几何）", "reason": "没有可用的 scan/geometry_segments，面积未计算", "evidence": "geometry=0", "confidence": cfg["confidence"]["review"]})

    main_area, candidate_area, net_candidate_area = 0.0, 0.0, 0.0
    for layer in layers:
        forced_layer = forced_mode or layer.startswith("（无图层") or layer.startswith("（DXF块内铺装）") or layer.startswith("（DXF回退）")
        segs = segs_by_layer[layer]
        faces = _faces(segs, tol)
        _seen_b, _uniq = set(), []
        for poly, ar in faces:
            xs = [p[0] for p in poly]
            ys = [p[1] for p in poly]
            kk = (round(abs(ar), 6), tuple(round(v, 6) for v in (min(xs), min(ys), max(xs), max(ys))))
            if kk in _seen_b:
                continue
            _seen_b.add(kk)
            _uniq.append((poly, ar))
        faces = _uniq
        cands = []
        for poly, ar in faces:
            abs_ar = abs(ar)
            if abs_ar < 1e-6:
                continue
            cx, cy = _centroid(poly)
            depth = 0
            for q, a2 in faces:
                if q is poly:
                    continue
                if abs(a2) > abs_ar and _point_in_poly(cx, cy, q):
                    depth += 1
            role = "洞/内岛" if depth % 2 == 1 else "外轮廓"
            cands.append({"poly": poly, "area_drawing2": round(abs_ar, 6), "depth": depth, "role": role, "bbox": _bbox(poly),
                          "center": (round(cx, 3), round(cy, 3))})
        cands.sort(key=lambda c: -c["area_drawing2"])
        net = 0.0
        for c in cands:
            if c["role"] == "外轮廓":
                net += c["area_drawing2"]
            else:
                net -= c["area_drawing2"]
        solid = sum(c["area_drawing2"] for c in cands) if forced_layer else net
        area_factor = (mm * geom_scale) ** 2 / 1e6
        area_m2 = solid * area_factor
        net_area_m2 = net * area_factor
        if forced_layer:
            tier, conf = CONF_P3, cfg["confidence"]["review"]
            need = "是；DXF回退铺装候选，边界/块变换/嵌套关系需复核，不计入主线" if layer.startswith("（DXF") else "是；全几何强算候选，不计入主线"
            final = False
        else:
            tier = CONF_P0 if cands and not any(c["depth"] > 0 for c in cands) else (CONF_P1 if cands else CONF_P3)
            conf = cfg["confidence"]["geometry_closure"] if tier == CONF_P0 else (cfg["confidence"]["geometry_summary"] if tier == CONF_P1 else cfg["confidence"]["review"])
            need = ""
            if not cands:
                need = "无法成环，面积未计算"
            elif any(c["depth"] > 0 for c in cands):
                need = "含洞/内岛，按深度奇偶扣减，需复核"
            elif len(cands) > 50:
                need = "闭环候选过多，疑似重复环/文字几何混入，需复核"
            final = bool(cands) and tier in (CONF_P0, CONF_P1) and not need
        for i, c in enumerate(cands):
            rows.append({
                "图层": layer, "面序号": f"SP{i+1}", "区域": f"{layer}|P{i+1}",
                "绘制单位面积": c["area_drawing2"], "实际铺装面积_m2": round(c["area_drawing2"] * area_factor, 4),
                "候选环面积_m2": round(c["area_drawing2"] * area_factor, 4) if forced_layer else "",
                "奇偶扣减净值_m2": "",
                "角色": ("候选" + c["role"] if forced_layer else c["role"]), "嵌套深度": c["depth"],
                "置信分层": tier, "置信度": round(conf, 3), "需核对": need,
                "证据坐标": f"bbox={c['bbox']} center={c['center']}",
                "计算式": f"鞋带面积(dwg²)*({mm:g}mm/单位*1:{scale:g})²/1e6",
                "依据": "cad_scan --with-geom --with-geom-layer 几何闭环检测",
                "计入主线": "是" if final else "否", "final_quantity": final, "使用边界": BOUNDARY,
            })
        sum_role = "候选环面积合计(不判断洞/内岛，不计入主线)" if forced_layer else "合计(含洞扣减)"
        sum_need = need if forced_layer else (need or ("否" if cands else "是"))
        sum_final = False if forced_layer else bool(cands) and not need
        rows.append({
            "图层": layer, "面序号": "SUM", "区域": f"{layer}|合计",
            "绘制单位面积": round(solid, 6), "实际铺装面积_m2": round(area_m2, 4),
            "候选环面积_m2": round(area_m2, 4), "奇偶扣减净值_m2": round(net_area_m2, 4),
            "角色": sum_role, "嵌套深度": "",
            "置信分层": CONF_P3 if forced_layer else (CONF_P1 if any(c["depth"] > 0 for c in cands) else (CONF_P0 if cands else CONF_P3)),
            "置信度": round(cfg["confidence"]["review"] if forced_layer else conf, 3), "需核对": sum_need,
            "证据坐标": "", "计算式": f"Σ候选环面积 ×({mm:g}mm/单位×{scale:g})²/1e6" if forced_layer else f"Σ外轮廓-Σ洞 ×({mm:g}mm/单位×{scale:g})²/1e6",
            "依据": "加权鞋带面积", "计入主线": "是" if sum_final else "否", "final_quantity": sum_final, "使用边界": BOUNDARY,
        })
        if forced_layer:
            net_candidate_area += net_area_m2
        if sum_final:
            main_area += area_m2
        else:
            candidate_area += area_m2
    # 合理性护栏（真图教训：图层名解码失败时全几何闭环会算出天文数字，如 74 亿 m²）
    implausible_note = ""
    if forced_mode and blank_layer_segs:
        xs = [p for s in blank_layer_segs for p in (s[0], s[2])]
        ys = [p for s in blank_layer_segs for p in (s[1], s[3])]
        k = mm * geom_scale / 1000.0  # 图纸单位 → 米
        frame_m2 = max(max(xs) - min(xs), 0.0) * max(max(ys) - min(ys), 0.0) * k * k
        raw_area = net_candidate_area or candidate_area
        bad, why = paving_area_implausible(
            raw_area, frame_m2,
            cap_m2=float(cfg.get("paving_area_plausibility_cap_m2") or 1e8),
            ratio_limit=float(cfg.get("paving_area_plausibility_ratio") or 3.0))
        if bad:
            ratio = (raw_area / frame_m2) if frame_m2 > 0 else 0.0
            implausible_note = (why + "；图层名缺失下全几何闭环会把图框、表格线、"
                               "苗木符号一并闭成假环；本轮不出面积，只留证据（真图教训："
                               "sample-road种植总图曾算出 74 亿 m²）")
            review.append({"layer": "（无图层，全几何候选）",
                           "reason": implausible_note,
                           "evidence": f"raw_candidate_m2={raw_area:.2f}, frame_m2={frame_m2:.2f}, ratio={ratio:.1f}",
                           "confidence": cfg["confidence"]["review"]})
            candidate_area = 0.0
            net_candidate_area = 0.0
    for r in review:
        rows.append({"图层": r["layer"], "面序号": "REVIEW", "区域": f"{r['layer']}|降级", "绘制单位面积": "", "实际铺装面积_m2": "",
                     "角色": "未计算", "嵌套深度": "", "置信分层": CONF_P3, "置信度": cfg["confidence"]["review"],
                     "需核对": "是；" + r["reason"], "证据坐标": str(r.get("evidence") or ""), "计算式": r["reason"],
                     "依据": "cad-file-reader paving_closed_areas / geometry_layers 降级复核",
                     "计入主线": "否", "final_quantity": False, "使用边界": BOUNDARY})
    return rows, {"layers": layers, "review": review, "solid": {l: None for l in layers},
                  "main_area_m2": round(main_area, 4), "candidate_area_m2": round(candidate_area, 4),
                  "net_area_m2": round(net_candidate_area, 4), "forced_mode": forced_mode,
                  "scale_detected": scale, "scale_applied": geom_scale, "scale_basis": scale_basis,
                  "area_implausible": bool(implausible_note), "area_implausible_note": implausible_note,
                  "has_geometry": has_geometry}


def _safe_evidence_name(v):
    text = re.sub(r"\s+", "_", str(v or "").strip())
    text = re.sub(r"[^\w\u4e00-\u9fff-]+", "", text, flags=re.UNICODE)
    return (text[:48] or "unnamed")


def export_p23_evidence(rows, evidence_dir, source=""):
    """为 P2/P3 输出本机坐标片段；P0/P1 不导出，避免把主线结果重复成文件。"""
    evidence_dir.mkdir(parents=True, exist_ok=True)
    written = []
    for i, r in enumerate(rows, 1):
        tier = str(r.get("置信分层") or "")
        if tier not in (CONF_P2, CONF_P3):
            continue
        name = str(r.get("植物名/图例名") or r.get("区域") or r.get("图层") or f"row{i}")
        kind = "plant" if r.get("来源") in ("苗木表", "平面图图例", "识图图例文字") else "paving"
        fname = f"{i:04d}_{kind}_{tier}_{_safe_evidence_name(name)}.md"
        lines = ["# P2/P3 证据片段", "", f"- 行号：{i}", f"- 类型：{kind}", f"- 名称：{name}",
                 f"- 置信分层：{tier}", f"- 来源：{r.get('来源') or r.get('分类') or ''}",
                 f"- 数量/面积：{r.get('统计数量', r.get('实际铺装面积_m2', ''))}",
                 f"- 单位：{r.get('单位', '')}", f"- 需核对：{r.get('需核对', '')}",
                 f"- 证据坐标：{r.get('证据坐标') or '无坐标'}",
                 f"- 图层：{r.get('图层') or ''}", f"- 源文件：{source}", f"- 使用边界：{BOUNDARY}"]
        (evidence_dir / fname).write_text("\n".join(lines) + "\n", encoding="utf-8")
        written.append(fname)
    return written

# ---------- 落盘 ----------
# 公式注入防护：图纸/候选文本里的单元格若以 = + - @ 或制表符/换行开头，
# 写 CSV/XLSX 时统一加前导单引号，避免 Excel 把不可信内容当公式执行；仅对报告落盘生效。
_FORMULA_PREFIXES = ("=", "+", "-", "@", "\t", "\r", "\n")


def _safe_cell(v):
    s = str(v)
    if s and s[0] in _FORMULA_PREFIXES:
        return "'" + s + ""
    return v


def write_csv(path, fieldnames, rows):
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow({k: _safe_cell(r.get(k, "")) for k in fieldnames})


def write_xlsx(path, sheets):
    try:
        from openpyxl import Workbook
    except Exception:
        return False
    wb = Workbook()
    wb.remove(wb.active)
    for name, headers, rows in sheets:
        ws = wb.create_sheet(name)
        ws.append(headers)
        for r in rows:
            ws.append([_safe_cell(r.get(k, "")) for k in headers])
    wb.save(path)
    return True


def _skill_version() -> str:
    try:
        return str(json.loads((Path(__file__).resolve().parents[1] / "manifest.json")
                              .read_text(encoding="utf-8")).get("version") or "")
    except Exception:
        return ""


def main(argv=None):
    raw = list(sys.argv[1:] if argv is None else argv)
    lang = i18n.argv_lang(raw)
    # 必须在其它检查之前拦下：--check-deps 只做依赖体检，不要求输入文件。
    if "--check-deps" in raw:
        status = cs.check_deps()
        print(cs.format_deps(status))
        raise SystemExit(eg.dependency_exit_code())
    ap = argparse.ArgumentParser(description="Yuanlin QTO (plants + paving) budget-candidate recomputer." if lang == "en" else "园林概算底稿候选复算器")
    i18n.add_lang_arg(ap, default=lang)
    ap.add_argument("--landscape", type=Path, help="cad-file-reader landscape-geometry JSON" if lang == "en" else "cad-file-reader landscape-geometry 输出 JSON")
    ap.add_argument("--scan", type=Path, help="cad_scan --with-geom --with-geom-layer --detail-json JSON" if lang == "en" else "cad_scan --with-geom --with-geom-layer --detail-json JSON")
    ap.add_argument("--rules", type=Path, help="project rules JSON" if lang == "en" else "项目规则 JSON")
    ap.add_argument("--out-dir", type=Path, default=Path("./outputs"))
    ap.add_argument("--project", default="")
    ap.add_argument("--scale", type=float, help="drawing scale 1:S (overrides autodetect)" if lang == "en" else "图纸比例 1:S，覆盖自动检测")
    ap.add_argument("--drawing-mm-per-unit", type=float, help="drawing mm per unit (default autodetect: mm=1/m=1000)" if lang == "en" else "图纸单位对应毫米数，默认自动检测(mm=1/m=1000)")
    ap.add_argument("--dedupe-tolerance", type=float)
    ap.add_argument("--paving-all-geometry", action="store_true", help="closure candidates over all geometry when layer names are missing (review-only)" if lang == "en" else "图层名缺失时对全部几何做闭环候选（只能作需核对）")
    ap.add_argument("--dxf-block-paving", type=Path, help="DISABLED: raw DXF input is rejected with exit 23; use cad-file-reader contract JSON" if lang == "en" else "已停用：传原始 DXF 会 exit 23；请先用 cad-file-reader 生成契约 JSON")
    ap.add_argument("--dxf-block-refs", type=Path, help="DISABLED: raw DXF input is rejected with exit 23; use cad-file-reader contract JSON" if lang == "en" else "已停用：传原始 DXF 会 exit 23；请先用 cad-file-reader 生成契约 JSON")
    ap.add_argument("--evidence-dir", type=Path, help="optional: export local coordinate snippets for P2/P3 (not for P0/P1)" if lang == "en" else "可选：为每条 P2/P3 导出本机坐标片段；P0/P1 不导出")
    ap.add_argument("--plant-library", type=Path, action="append", help="optional: local plant-name library (.json/.csv/.xlsx), name->category only; repeatable" if lang == "en" else "可选：本地植物名称参考库（.json/.csv/.xlsx），只取中文名→大类，忽略规格与单价；可重复指定")
    ap.add_argument("--no-default-plant-library", action="store_true", help="do not load the built-in common plant-name library" if lang == "en" else "不加载内置常用园林植物名称参考库")
    ap.add_argument("--allow-manual", action="store_true",
                    help="allow manual scan/landscape/DXF input; result forced final_quantity=false" if lang == "en"
                    else "允许消费无 reader 溯源的手工/旧扫描 JSON；结果强制 final_quantity=false（图纸仍 exit 23）")
    ap.add_argument("--check-deps", action="store_true",
                    help="only check cad-file-reader / lis-skill-bus / Python; exit 20/21 when missing" if lang == "en"
                    else "只检查 cad-file-reader / lis-skill-bus / Python 前置；缺 reader=20、缺 bus=21")
    args = ap.parse_args(argv)

    # 入口闸门：原始 DXF 路径一律 23；直接传图纸一律 23；缺 reader=20、缺 bus=21。
    try:
        if args.dxf_block_paving or args.dxf_block_refs:
            raise eg.GateError(
                23, eg.DRAWING_REJECT_MESSAGE,
                "本技能不接受原始 DXF；请先用 cad-file-reader 生成契约 JSON（cad_landscape_geometry 产物），再传入 --landscape。")
        eg.reject_drawing_input(args.landscape, args.scan)
        eg.require_reader()
        eg.require_bus()
    except eg.GateError as exc:
        raise SystemExit(eg.print_gate_error(exc))
    cfg = json.loads(Path(__file__).parent.parent.joinpath("rules", "rules.json").read_text(encoding="utf-8")) if Path(__file__).parent.parent.joinpath("rules", "rules.json").exists() else {}
    merged = copy.deepcopy(DEFAULT_RULES)
    if cfg.get("confidence"):
        merged["confidence"].update(cfg["confidence"])
    for k in ("dedupe_tolerance", "geometry_close_tolerance", "paving_layer_tokens", "scale_unit_hints", "drawing_mm_per_unit",
              "plant_groundcover", "plant_shrubs", "plant_trees", "plant_other"):
        if cfg.get(k) is not None:
            merged[k] = cfg[k]
    if args.rules and args.rules.exists():
        proj = json.loads(args.rules.read_text(encoding="utf-8"))
        if proj.get("confidence"):
            merged["confidence"].update(proj["confidence"])
        for k in ("dedupe_tolerance", "geometry_close_tolerance", "paving_layer_tokens", "scale_unit_hints", "drawing_mm_per_unit",
                  "plant_groundcover", "plant_shrubs", "plant_trees", "plant_other", "exclude_layers",
                  "include_layers_regex", "exclude_frame_bbox"):
            if proj.get(k) is not None:
                merged[k] = proj[k]
    if args.dedupe_tolerance:
        merged["dedupe_tolerance"] = args.dedupe_tolerance
    library_sources, library_added = [], {}
    if not args.no_default_plant_library:
        for lib_path in default_plant_libraries():
            lib = load_plant_library(lib_path)
            for w in lib.get("warnings") or []:
                library_sources.append(f"警告:{w}")
            if lib.get("names"):
                added = merge_plant_library(merged, lib)
                for cat, lst in added.items():
                    library_added.setdefault(cat, []).extend(lst)
                library_sources.append(f"{lib_path.name}({lib['count']})")
    for lib_path in (args.plant_library or []):
        lib = load_plant_library(lib_path)
        for w in lib.get("warnings") or []:
            library_sources.append(f"警告:{w}")
        if lib.get("names"):
            added = merge_plant_library(merged, lib)
            for cat, lst in added.items():
                library_added.setdefault(cat, []).extend(lst)
            library_sources.append(f"{lib_path.name}({lib['count']})")
    landscape = unwrap_bus_contract(json.loads(args.landscape.read_text(encoding="utf-8"))) if args.landscape else None
    scan = unwrap_bus_contract(json.loads(args.scan.read_text(encoding="utf-8"))) if args.scan else None
    if not landscape and not scan and not args.dxf_block_paving and not args.dxf_block_refs:
        ap.error("provide at least one of --landscape, --scan, --dxf-block-paving or --dxf-block-refs"
                 if lang == "en" else "至少提供 --landscape / --scan / --dxf-block-paving / --dxf-block-refs 之一")
    try:
        guard = guard_yuanlin_sources(landscape, scan,
                                      bool(args.dxf_block_paving or args.dxf_block_refs),
                                      allow_manual=bool(args.allow_manual))
    except GuardError as exc:
        sys.stderr.write("[GuardError %d] %s\n" % (exc.code, exc.message))
        if exc.hint:
            sys.stderr.write("修复: %s\n" % exc.hint)
        raise SystemExit(exc.code) from None
    args.out_dir.mkdir(parents=True, exist_ok=True)
    dxf_info = None
    block_ref_info = None
    if args.dxf_block_paving or args.dxf_block_refs:
        reader_info = _run_landscape_geometry(args.dxf_block_paving, args.dxf_block_refs)
        if scan is None:
            scan = {"source_file": str(args.dxf_block_paving or args.dxf_block_refs),
                    "geometry_segments": [], "geometry_layers": []}
        if args.dxf_block_paving and reader_info.get("segments"):
            scan.setdefault("geometry_segments", []).append(reader_info["segments"])
            scan.setdefault("geometry_layers", []).append(reader_info["layers"])
            dxf_info = {"segments": reader_info["segments"],
                        "warnings": [] if not any(x in " ".join(reader_info.get("warnings") or []) for x in ("失败", "不可用")) else reader_info["warnings"],
                        "mm_per_unit": reader_info.get("mm_per_unit")}
            scan["_dxf_block_paving"] = {"source": str(args.dxf_block_paving),
                                         "ring_segments": len(reader_info.get("segments") or []),
                                         "warnings": dxf_info["warnings"]}
        if args.dxf_block_refs and reader_info.get("block_refs"):
            scan.setdefault("text_records", []).extend(reader_info["block_refs"])
            block_ref_info = {"records": reader_info["block_refs"],
                              "insert_count": reader_info.get("insert_count") or 0,
                              "warnings": reader_info.get("warnings") or []}
            scan["_dxf_block_refs"] = {"source": str(args.dxf_block_refs),
                                       "insert_count": block_ref_info["insert_count"],
                                       "warnings": block_ref_info["warnings"]}
        if args.dxf_block_paving and not dxf_info:
            dxf_info = {"segments": [], "warnings": reader_info.get("warnings") or [],
                        "mm_per_unit": reader_info.get("mm_per_unit")}
            scan["_dxf_block_paving"] = {"source": str(args.dxf_block_paving),
                                         "ring_segments": 0, "warnings": dxf_info["warnings"]}
        if args.dxf_block_refs and not block_ref_info:
            block_ref_info = {"records": [], "insert_count": 0, "warnings": reader_info.get("warnings") or []}
            scan["_dxf_block_refs"] = {"source": str(args.dxf_block_refs),
                                       "insert_count": 0, "warnings": block_ref_info["warnings"]}
    su = detect_scale_unit(scan or landscape or {}, merged, args.scale, args.drawing_mm_per_unit)
    if dxf_info and dxf_info.get("mm_per_unit") and not args.drawing_mm_per_unit:
        su["drawing_mm_per_unit"] = float(dxf_info["mm_per_unit"])
        su["drawing_unit_source"] = "DXF INSUNITS"
    plants, pmeta = plant_rows(landscape, scan, merged)
    for warning in (dxf_info or {}).get("warnings") or []:
        pmeta.setdefault("warnings", []).append({"分类": "复核提示", "植物名/图例名": "DXF块铺装回退", "统计数量": "", "实际铺装面积_m2": "", "需核对": warning, "证据坐标": "", "计算式": "dxf_block_paving"})
    for warning in [s[3:] for s in library_sources if s.startswith("警告:")]:
        pmeta.setdefault("warnings", []).append({"分类": "复核提示", "植物名/图例名": "植物参考库", "统计数量": "", "实际铺装面积_m2": "", "需核对": warning, "证据坐标": "", "计算式": "plant_library", "参考库命中": ""})
    for warning in (block_ref_info or {}).get("warnings") or []:
        pmeta.setdefault("warnings", []).append({"分类": "复核提示", "植物名/图例名": "DXF块引用回退", "统计数量": "", "实际铺装面积_m2": "", "需核对": warning, "证据坐标": "", "计算式": "dxf_block_refs"})
    pav, vmeta = paving_rows(landscape, scan, merged, su, all_geometry=bool(args.paving_all_geometry))

    def qty_sum(rows, units=None):
        total = 0.0
        for r in rows:
            if units is not None and str(r.get("单位") or "") not in units:
                continue
            v = _num(r.get("统计数量"))
            if v is not None:
                total += v
        return round(total, 4)

    review = list(pmeta.get("warnings", []))
    review += [r for r in plants if "是" in str(r.get("需核对") or "")]
    review += [r for r in pav if r.get("面序号") == "REVIEW"]
    for conflict in pmeta.get("conflicts") or []:
        review.append({"分类": "苗木冲突逐名对照", "植物名/图例名": conflict.get("名称"), "统计数量": conflict.get("平面计数"),
                       "实际铺装面积_m2": "", "需核对": f"设计表数量={conflict.get('设计表数量')};平面计数={conflict.get('平面计数')};差异={conflict.get('差异')};{conflict.get('冲突原因')}",
                       "证据坐标": "", "计算式": "设计表数量-平面计数", "设计表数量": conflict.get("设计表数量"),
                       "平面计数": conflict.get("平面计数"), "差异": conflict.get("差异"), "冲突原因": conflict.get("冲突原因")})

    evidence_files = []
    if args.evidence_dir:
        evidence_files = export_p23_evidence(plants + pav + review, args.evidence_dir, str(args.scan or args.landscape or ""))

    design_rows = [r for r in plants if r.get("来源") == "苗木表"]
    plan_rows = [r for r in plants if r.get("来源") == "平面图图例"]
    legend_rows = [r for r in plants if r.get("来源") == "识图图例文字"]
    plan_main_rows = [r for r in plan_rows if r.get("final_quantity")]
    plan_ref_rows = [r for r in plan_rows if r.get("置信分层") == "P2" and "块引用" in str(r.get("计量方式") or "")]
    main_area = float(vmeta.get("main_area_m2") or 0)
    candidate_area = float(vmeta.get("candidate_area_m2") or 0)
    net_area = float(vmeta.get("net_area_m2") or 0)
    sum_rows = [
        {"指标": "苗木设计表条目数", "值": len(design_rows), "口径": "图纸苗木表逐行解析，按名称+单位去重"},
        {"指标": "苗木设计表株数基线(株/棵/丛)", "值": qty_sum(design_rows, {"株", "棵", "丛"}), "口径": "设计给定数量，只作概算基线，不等同平面图逐株点数"},
        {"指标": "苗木设计表面积基线(m²/㎡)", "值": qty_sum(design_rows, {"m2", "㎡", "m²", "平方米"}), "口径": "设计给定面积，只作概算基线"},
        {"指标": "面积式苗木表行数(数量=0，不计主线)", "值": sum(1 for r in design_rows if float(r.get("统计数量") or 0) == 0.0), "口径": "设计表数量=0（面积式/密度式种植），只作复核线索，不按株数推算、不计入主线"},
        {"指标": "平面图块级计数条数", "值": len(plan_rows), "口径": "有块名/坐标可复算的植物图例条数"},
        {"指标": "平面图块级计数株数(仅P0/P1)", "值": qty_sum(plan_main_rows, {"株", "棵", "丛"}), "口径": "有坐标时去重，无坐标底座计数按 P1 保留并标明未逐点去重；P2/P3不进入主线"},
        {"指标": "平面图块引用候选条数(仅P2)", "值": len(plan_ref_rows), "口径": "只有块引用总数、无坐标的植物图例条数"},
        {"指标": "平面图块引用候选数量(仅P2)", "值": qty_sum(plan_ref_rows, {"株", "棵", "丛"}), "口径": "块引用总数未去重，只作复核线索"},
        {"指标": "平面图文字标记候选条数(仅P2)", "值": len(legend_rows), "口径": "底座 plant_legends/systems 种植文字分组条数，文字次数不等于株数"},
        {"指标": "平面图文字标记出现次数(仅P2)", "值": qty_sum(legend_rows), "口径": "底座图例文字出现次数，只作人工复核线索"},
        {"指标": "铺装面积合计(m²,仅计入主线)", "值": round(main_area, 4), "口径": "只累计 final_quantity=true 的闭环面积"},
        {"指标": "铺装强算候选面积(m²,不计入主线)", "值": round(candidate_area, 4), "口径": "--paving-all-geometry 候选环面积合计与DXF回退候选合计，强制P3"},
        {"指标": "铺装强算奇偶扣减净值(m²,P3)", "值": round(net_area, 4), "口径": "强制P3；外轮廓减洞/内岛的净值，仅作复核线索，不计入主线"},
        {"指标": "比例判定来源", "值": su.get("scale_source") or "默认", "口径": "用户覆盖/图纸文字/规则配置/默认"},
        {"指标": "面积实际用比例", "值": f"1:{vmeta.get('scale_applied', su['scale']):g}", "口径": f"{vmeta.get('scale_basis','')}；检测值 1:{su['scale']:g} 仅记录"},
        {"指标": "图纸单位判定来源", "值": su.get("drawing_unit_source") or "默认", "口径": "用户覆盖/DXF INSUNITS/图纸文字/规则配置/默认"},
        {"指标": "铺装图层数", "值": len(vmeta.get("layers") or []), "口径": "命中铺装图层 token 或全几何候选层"},
        {"指标": "苗木逐株交叉核对状态", "值": "已执行" if plan_main_rows else "不可用/需人工", "口径": "没有可靠块级计数时，苗木表不能冒充平面图点数"},
        {"指标": "需核对条数", "值": len(review), "口径": "苗木复核提示+铺装降级/候选复核，不含每个 SP 候选行"},
        {"指标": "P2/P3证据文件数", "值": len(evidence_files), "口径": "--evidence-dir 启用时导出的坐标片段数；P0/P1不导出"},
        {"指标": "植物名称参考库条目数", "值": len(merged.get("plant_library") or {}), "口径": "只含中文名→大类映射；不含规格/密度/苗价/综合单价，来源：" + (";".join(library_sources) or "未加载")},
        {"指标": "参考库命中分类条数", "值": sum(1 for r in plants if str(r.get("参考库命中") or "").strip()), "口径": "参考库只补充原有词库未覆盖的名称，不改变内建/项目词库既有分类"},
    ]
    base_rows = [{"项目": "使用边界声明", "依据文本": BOUNDARY},
                 {"项目": "比例/单位检测", "依据文本": f"scale=1:{su['scale']:g}, drawing_mm_per_unit={su['drawing_mm_per_unit']:g}, 比例来源={su.get('scale_source','默认')}, 单位来源={su.get('drawing_unit_source','默认')}"},
                 {"项目": "苗木", "依据文本": "cad-file-reader plant_block_legends/plant_legends/systems/block INSERT 实例 + 图纸苗木表文字解析"},
                 {"项目": "植物名称参考库", "依据文本": ("参考库：" + ";".join(library_sources or ["未加载"])) + "；（" + "，".join(f"{k}+{len(v)}" for k, v in library_added.items()) + "）只用于名称分类，不读规格/密度/单价，不自动推断规格或报价"},
                 {"项目": "铺装", "依据文本": "cad_scan --with-geom --with-geom-layer 几何闭环；可选 --dxf-block-paving 展开块内 POLYLINE/LWPOLYLINE；块内与全几何强算只出 P3 候选"},
                 {"项目": "计算式", "依据文本": "面积m² = 鞋带面积(dwg²)×(mm/单位×比例)²/1e6"}]
    plant_headers = ["分类", "来源", "植物名/图例名", "规格与图例文字", "统计数量", "单位", "计量方式", "平面图文字标记数",
                     "口径", "置信分层", "置信度", "需核对", "证据坐标", "规格证据", "文件", "图层", "分类依据", "参考库命中", "依据",
                     "计入主线", "final_quantity", "使用边界"]
    paving_headers = ["图层", "面序号", "区域", "绘制单位面积", "实际铺装面积_m2", "候选环面积_m2", "奇偶扣减净值_m2", "角色", "嵌套深度", "置信分层", "置信度",
                      "需核对", "证据坐标", "计算式", "依据", "计入主线", "final_quantity", "使用边界"]
    review_headers = ["分类", "植物名/图例名", "统计数量", "实际铺装面积_m2", "需核对", "证据坐标", "计算式", "设计表数量", "平面计数", "差异", "冲突原因"]
    write_csv(args.out_dir / "园林苗木统计.csv", plant_headers, plants)
    write_csv(args.out_dir / "园林铺装面积.csv", paving_headers, pav)
    write_csv(args.out_dir / "缺项核对.csv", review_headers, review)
    write_csv(args.out_dir / "汇总.csv", ["指标", "值", "口径"], sum_rows)
    write_csv(args.out_dir / "依据.csv", ["项目", "依据文本"], base_rows)
    xlsx = write_xlsx(args.out_dir / "Yuanlin概算物资计划台账.xlsx",
                      [("使用边界", ["使用边界声明"], [{"使用边界声明": BOUNDARY}]),
                       ("苗木统计", plant_headers, plants),
                       ("铺装面积", paving_headers, pav),
                       ("缺项核对", review_headers, review),
                       ("汇总", ["指标", "值", "口径"], sum_rows),
                       ("依据", ["项目", "依据文本"], base_rows)])
    lines = [f"# 园林概算底稿报告 {args.project}", "", f"源：landscape={args.landscape or '-'} scan={args.scan or '-'}",
             f"比例/单位：scale=1:{su['scale']:g}，drawing_mm_per_unit={su['drawing_mm_per_unit']:g}",
             f"苗木：设计表 {len(design_rows)} 行；平面图块级计数 {len(plan_rows)} 行；图例文字P2候选 {len(legend_rows)} 类；逐株交叉核对={'已执行' if plan_main_rows else '不可用/需人工'}",
             f"铺装：计入主线 {main_area:.4f} m²；P3 强算候选 {candidate_area:.4f} m²；奇偶扣减净值 {net_area:.4f} m²",
             "", "## 苗木统计", "", "| 分类 | 来源 | 植物名/图例名 | 数量 | 单位 | 计量方式 | 置信 | 需核对 | 证据坐标 |", "|---|---|---|---|---|---|---|---|---|"]
    for r in plants[:80]:
        lines.append(f"| {r['分类']} | {r.get('来源','')} | {r['植物名/图例名']} | {r['统计数量']} | {r.get('单位','')} | {r.get('计量方式','')} | {r['置信分层']} | {r['需核对']} | {str(r.get('证据坐标',''))[:60]} |")
    if len(plants) > 80:
        lines.append(f"| ... | ... | 其余 {len(plants)-80} 行见 CSV/xlsx | ... | ... | ... | ... | ... | ... |")
    lines += ["", "## 铺装面积", "", "| 图层 | 区域 | 角色 | 面积m² | 置信 | 需核对 | 计入主线 | 计算式 |", "|---|---|---|---|---|---|---|---|"]
    for r in pav[:200]:
        lines.append(f"| {r['图层']} | {r['区域']} | {r['角色']} | {r.get('实际铺装面积_m2','')} | {r['置信分层']} | {r['需核对']} | {r.get('计入主线','')} | {r['计算式']} |")
    if len(pav) > 200:
        lines.append(f"| ... | ... | 其余 {len(pav)-200} 行见 CSV/xlsx | ... | ... | ... | ... | ... |")
    lines += ["", "## 使用边界", "", BOUNDARY]
    (args.out_dir / "园林概算报告.md").write_text("\n".join(lines), encoding="utf-8")

    def _coord(value):
        try:
            parts = str(value or "").replace("，", ",").split(",")
            if len(parts) >= 2:
                return float(parts[0]), float(parts[1])
        except Exception:
            pass
        return None, None

    def _clean(value):
        s = str(value if value is not None else "").strip()
        return "" if s.lower() in ("none", "nan", "null") else s

    members = []
    n = 0
    for r in plants:
        qty = _num(r.get("统计数量"))
        unit = str(r.get("单位") or "")
        if not qty or unit not in ("株", "棵", "丛", "m2", "㎡", "m²"):
            continue
        if r.get("置信分层") not in ("P0", "P1"):
            continue
        n += 1
        x, y = _coord(r.get("证据坐标"))
        members.append(cs.handoff_member(
            "YUANLIN-%04d" % n, weight_t=None, length_m=None,
            section=_clean(r.get("植物名/图例名")), grade="",
            x_m=x, y_m=y, z_m=None, zone=_clean(r.get("图层")),
            weight_basis="unknown",
            coord_status=("estimated" if x is not None and y is not None else "missing"),
            kind="plant", quantity=qty, unit=unit,
            confidence=str(r.get("置信分层") or "")))
    for r in pav:
        area = _num(r.get("实际铺装面积_m2"))
        if not area or r.get("面序号") == "SUM":
            continue
        n += 1
        members.append(cs.handoff_member(
            "YUANLIN-%04d" % n, weight_t=None, length_m=None,
            section=_clean(r.get("图层")), grade="",
            weight_basis="unknown", coord_status="missing",
            kind="paving", area_m2=area,
            confidence=str(r.get("置信分层") or "")))
    provenance = cs.provenance_fields(guard)
    provenance["mode"] = guard.get("mode") or "manual"
    cs.write_json(args.out_dir / "provenance.json", provenance)
    manifest = cs.run_manifest("yuanlin-suanliang", _skill_version(), guard, argv=raw)
    cs.write_json(args.out_dir / "run.json", manifest)
    cs.write_handoff(args.out_dir, args.project, "landscape", guard, members)
    if guard.get("mode") != "formal":
        sys.stderr.write("[yuanlin] 手工来源（provenance=manual）：final_quantity=false，不得报正式量。\n")
    print(json.dumps({"status": "ok", "ok": True,
                      "message": ("generated" if lang == "en" else "已生成"), "schema": SCHEMA, "project": args.project,
                      "plants": len(plants), "design_rows": len(design_rows), "plan_rows": len(plan_rows),
                      "paving_rows": len(pav), "review_rows": len(review), "main_area_m2": round(main_area, 4),
                      "candidate_area_m2": round(candidate_area, 4), "net_area_m2": round(net_area, 4), "xlsx": bool(xlsx),
                      "scale": su["scale"], "scale_applied": vmeta.get("scale_applied", su["scale"]), "scale_basis": vmeta.get("scale_basis", ""), "drawing_mm_per_unit": su["drawing_mm_per_unit"], "scale_source": su.get("scale_source", "默认"), "drawing_unit_source": su.get("drawing_unit_source", "默认"),
                      "evidence_files": len(evidence_files), "evidence_dir": str(args.evidence_dir or ""),
                      "plant_library_count": len(merged.get("plant_library") or {}),
                      "plant_library_added": {k: len(v) for k, v in library_added.items()},
                      "plant_library_hits": sum(1 for r in plants if str(r.get("参考库命中") or "").strip()),
                      "plant_library_sources": library_sources,
                      "provenance": provenance.get("provenance"),
                      "contract_id": provenance.get("contract_id") or "",
                      "final_quantity": bool(provenance.get("final_quantity")),
                      "formal_ledger_eligible": bool(provenance.get("formal_ledger_eligible")),
                      "handoff_members": len(members),
                      "out_dir": str(args.out_dir)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
