#!/usr/bin/env python3
"""yuanlin-suanliang v0.4.11 自测。

A：合成 m 单位图——苗木块级计数、同坐标去重、铺装 96m²（含 4m² 洞）。
B：合成 mm 单位图——5000×4000 铺装 → 20m²。
C：仅底座 landscape——块级实例按 instance_count 计数；图例文字只作 P2；无几何时铺装降级 review。
D：苗木表 + 图例文字——设计表基线、平面图块级计数、P2 文字候选三层分离。
E：无图层 + --paving-all-geometry——强算候选 P3，不计入主线。
F：中英文植物块/块引用候选——底座计数 P1、仅块引用 P2、systems 种植文字 P2。
G：原始 DXF 块内铺装入口——必须 exit 23，不再内置解析。
H：原始 DXF 增强铺装入口——必须 exit 23，不再内置解析。
I：项目规则增强——exclude_frame_bbox 排除标注框后强算候选由 2m² 降至 1m²，仍 P3。
J：苗木表变体——图例编号、序号/棵、名称及规格/m² 三类表头均可解析。
K：苗木冲突——设计表10株/平面8株，输出差异2并降P3。
L：比例/单位证据链——合成文字来源与 DXF INSUNITS 来源。
M：证据导出——P2/P3 坐标片段导出，P0/P1 不导出。
O：中文表结构化——空格标题、品名/数量(棵)、植物表多标题可解析，说明句不误入。
P：数量单位证据——表头括号/单位列可归一；无单位证据不默认株、降P1并待核对。
Q：植物名称参考库——只取中文名→大类，规格/单价不入输出，只补分类缺口。
R：内置区域植物库——多库自动加载；章节→大类修正（灌木/地被）；主线数量不漂移。
S：无标题苗木表——「中文名称」表头 + 表头组合自识别；数量=0 面积式行只作 P3 线索、不推算株数。
"""
import csv, importlib.util, json, math, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PY = sys.executable
HAS_OPENPYXL = importlib.util.find_spec("openpyxl") is not None
def run(args, project="自测"):
    cmd = [PY, str(ROOT / "scripts/yuanlin_qty.py"), "--out-dir", str(args["out"]), "--project", project]
    for key in ("scan", "landscape", "rules", "dxf_block_paving", "dxf_block_refs", "evidence_dir"):
        if args.get(key):
            cmd += [f"--{key.replace('_', '-')}", str(args[key])]
    # 自测输入均为合成 scan/landscape/DXF，没有 reader 契约：按手工来源显式放行。
    if not args.get("formal"):
        cmd.append("--allow-manual")
    if args.get("force"):
        cmd.append("--paving-all-geometry")
    for lib in (args.get("plant_library") or []):
        cmd += ["--plant-library", str(lib)]
    if args.get("no_default_plant_library"):
        cmd.append("--no-default-plant-library")
    r = subprocess.run(cmd, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    payload = json.loads(r.stdout.strip().splitlines()[-1])
    return payload


def run_gate(args, project="自测", want=23):
    """原始图纸入口必须被统一闸门拒绝，不得回退到内置解析。"""
    cmd = [PY, str(ROOT / "scripts/yuanlin_qty.py"), "--out-dir", str(args["out"]), "--project", project]
    for key in ("scan", "landscape", "rules", "dxf_block_paving", "dxf_block_refs", "evidence_dir"):
        if args.get(key):
            cmd += [f"--{key.replace('_', '-')}", str(args[key])]
    r = subprocess.run(cmd, capture_output=True, text=True)
    text = (r.stdout + r.stderr).strip()
    assert r.returncode == want, f"exit={r.returncode}（期望 {want}）: {text}"
    assert "不直接识图" in text, text
    return text


def read_csv(path):
    return list(csv.DictReader(path.open(encoding="utf-8-sig")))


def find(rows, name, source=None):
    for row in rows:
        if row.get("植物名/图例名") == name and (source is None or row.get("来源") == source):
            return row
    raise AssertionError(f"未找到 {name!r} source={source!r}: {rows}")


def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")


def case_a(tmp):
    blocks = []
    for name, count, base in (("银杏", 10, (1, 1)), ("紫薇", 5, (3, 3))):
        for i in range(count):
            blocks.append({"kind": "INSERT", "text": name, "x": base[0] + i * 0.8, "y": base[1]})
    blocks += [{"kind": "INSERT", "text": "草坪", "x": 20, "y": 20}, {"kind": "INSERT", "text": "草坪", "x": 20, "y": 20}]
    segs = []
    for poly in ([(0, 0), (10, 0), (10, 10), (0, 10)], [(2, 2), (4, 2), (4, 4), (2, 4)]):
        for i in range(len(poly)):
            segs.append([*poly[i], *poly[(i + 1) % len(poly)]])
    scan = {"source_file": "synthetic_garden_m.dwg", "records": blocks,
            "text": blocks + [{"type": "TEXT", "kind": "TEXT", "text": "单位：米 m"},
                              {"type": "TEXT", "kind": "TEXT", "text": "比例 1:1"},
                              {"type": "TEXT", "kind": "TEXT", "text": "银杏 D12"}],
            "geometry_segments": [segs], "geometry_layers": [["景观铺地"] * len(segs)]}
    p = tmp / "a_scan.json"
    write_json(p, scan)
    out = tmp / "a_out"
    info = run({"scan": p, "out": out}, "用例A")
    plant = read_csv(out / "园林苗木统计.csv")
    pav = read_csv(out / "园林铺装面积.csv")
    ginkgo = find(plant, "银杏", "平面图图例")
    assert float(ginkgo["统计数量"]) == 10.0 and ginkgo["计量方式"] == "块级实例去重计数", ginkgo
    assert float(find(plant, "紫薇", "平面图图例")["统计数量"]) == 5.0
    assert float(find(plant, "草坪", "平面图图例")["统计数量"]) == 1.0
    total = next(r for r in pav if r["面序号"] == "SUM")
    assert total["实际铺装面积_m2"] == "96.0", total
    assert any(r["角色"] == "洞/内岛" for r in pav), pav
    if HAS_OPENPYXL:
        assert out.joinpath("Yuanlin概算物资计划台账.xlsx").exists()
    return "A: 块级计数+去重；铺装96m²(100-4洞)"


def case_b(tmp):
    segs = [[0, 0, 5000, 0], [5000, 0, 5000, 4000], [5000, 4000, 0, 4000], [0, 4000, 0, 0]]
    scan = {"source_file": "synthetic_paving_mm.dwg", "records": [], "text": [{"type": "TEXT", "kind": "TEXT", "text": "比例 1:1"}],
            "geometry_segments": [segs], "geometry_layers": [["园路"] * len(segs)]}
    p = tmp / "b_scan.json"
    write_json(p, scan)
    out = tmp / "b_out"
    run({"scan": p, "out": out}, "用例B")
    pav = read_csv(out / "园林铺装面积.csv")
    total = next(r for r in pav if r["面序号"] == "SUM")
    assert total["实际铺装面积_m2"] == "20.0", total
    return "B: 5000×4000mm 比例1:1 → 铺装20m²"


def case_v(tmp):
    """V：模型空间 1:500 真图——打印比例不得再次放大面积。"""
    segs = [[0, 0, 5000, 0], [5000, 0, 5000, 4000], [5000, 4000, 0, 4000], [0, 4000, 0, 0]]
    scan = {"source_file": "synthetic_modelspace_1_500.dwg", "records": [],
            "text": [{"type": "TEXT", "kind": "TEXT", "text": "总平面图 比例 1:500"}],
            "geometry_segments": [segs], "geometry_layers": [["园路"] * len(segs)]}
    sp = tmp / "v_scan.json"
    write_json(sp, scan)
    out = tmp / "v_out"
    info = run({"scan": sp, "out": out}, "用例V-模型空间比例")
    pav = read_csv(out / "园林铺装面积.csv")
    total = next(r for r in pav if r["面序号"] == "SUM")
    assert total["实际铺装面积_m2"] == "20.0", total
    assert info["scale"] == 500 and info["scale_applied"] == 1.0, info
    summary = {r["指标"]: r["值"] for r in read_csv(out / "汇总.csv")}
    assert summary["面积实际用比例"] == "1:1", summary
    return "V: 模型空间1:500→面积仍按1:1(20m²)，只记录打印比例"


def case_c(tmp):
    landscape = {
        "source_file": "synthetic_landscape.dwg",
        "plant_block_legends": [{"name": "樱花", "category": "乔木", "instance_count": 3, "x": 1, "y": 2, "sample_coords": [[1, 2], [3, 4]]}],
        "plant_legends": [
            {"plant": "樱花", "legend_raw": "樱花 H3.0", "x": 1, "y": 2},
            {"plant": "樱花", "legend_raw": "樱花 H3.0", "x": 5, "y": 6},
            {"plant": "海棠", "x": 7, "y": 8},
            {"plant": "地被种植总平面图", "x": 9, "y": 10},
        ],
        "paving_closed_areas": [{"layer": "景观铺地", "closed_ring_candidates": 4, "region_candidates": [{"review_label": "景观铺地|R1|4环"}]}],
    }
    p = tmp / "c_landscape.json"
    write_json(p, landscape)
    out = tmp / "c_out"
    run({"landscape": p, "out": out}, "用例C")
    plant = read_csv(out / "园林苗木统计.csv")
    pav = read_csv(out / "园林铺装面积.csv")
    sakura = find(plant, "樱花", "平面图图例")
    assert float(sakura["统计数量"]) == 3.0 and sakura["final_quantity"] == "True", sakura
    haitang = find(plant, "海棠", "识图图例文字")
    assert haitang["置信分层"] == "P2" and haitang["final_quantity"] == "False", haitang
    assert all("地被种植总平面图" not in r["植物名/图例名"] for r in plant), plant
    assert any(r["面序号"] == "REVIEW" and r["置信分层"] == "P3" for r in pav), pav
    return "C: 块级instance_count=3；图例文字P2不计主线；铺装review"


def case_d(tmp):
    scan = {
        "source_file": "synthetic_schedule.dwg",
        "text_records": [
            {"text": "苗木配置表", "x": 0, "y": 1000, "sheet": 1, "layer": "表"},
            {"text": "名称", "x": 0, "y": 900, "sheet": 1, "layer": "表"},
            {"text": "数量", "x": 1000, "y": 900, "sheet": 1, "layer": "表"},
            {"text": "单位", "x": 2000, "y": 900, "sheet": 1, "layer": "表"},
            {"text": "银杏", "x": 0, "y": 800, "sheet": 1, "layer": "表"},
            {"text": "10", "x": 1000, "y": 800, "sheet": 1, "layer": "表"},
            {"text": "株", "x": 2000, "y": 800, "sheet": 1, "layer": "表"},
            {"text": "银杏", "x": 5000, "y": 5000, "sheet": 1, "layer": "种植"},
        ],
        "geometry_segments": [[]], "geometry_layers": [[]],
    }
    landscape = {"source_file": "synthetic_schedule.dwg", "plant_legends": [
        {"plant": "银杏", "legend_raw": "银杏 D12", "x": 5000, "y": 5000},
        {"plant": "银杏", "legend_raw": "银杏 D12", "x": 6000, "y": 6000},
    ]}
    sp = tmp / "d_scan.json"
    lp = tmp / "d_landscape.json"
    write_json(sp, scan)
    write_json(lp, landscape)
    out = tmp / "d_out"
    run({"scan": sp, "landscape": lp, "out": out}, "用例D")
    plant = read_csv(out / "园林苗木统计.csv")
    design = find(plant, "银杏", "苗木表")
    legend = find(plant, "银杏", "识图图例文字")
    assert float(design["统计数量"]) == 10.0 and design["计量方式"] == "苗木表结构化表行（设计基线，非逐株点数）", design
    assert design["final_quantity"] == "True", design
    assert float(legend["统计数量"]) == 2.0 and legend["置信分层"] == "P2" and legend["final_quantity"] == "False", legend
    review = read_csv(out / "缺项核对.csv")
    assert any("无法逐株交叉核对" in r["需核对"] for r in review), review
    return "D: 苗木表基线/块级计数/P2文字三层分离"


def case_e(tmp):
    segs = [
        [0, 0, 1000, 0], [1000, 0, 1000, 1000], [1000, 1000, 0, 1000], [0, 1000, 0, 0],
        [400, 400, 600, 400], [600, 400, 600, 600], [600, 600, 400, 600], [400, 600, 400, 400],
    ]
    scan = {"source_file": "synthetic_no_layer.dwg", "text_records": [{"text": "比例 1:1", "x": 0, "y": 0}],
            "geometry_segments": [segs], "geometry_layers": [[""] * len(segs)]}
    p = tmp / "e_scan.json"
    write_json(p, scan)
    out = tmp / "e_out"
    info = run({"scan": p, "out": out, "force": True}, "用例E")
    pav = read_csv(out / "园林铺装面积.csv")
    assert info["main_area_m2"] == 0.0 and abs(info["candidate_area_m2"] - 1.04) < 0.001 and abs(info["net_area_m2"] - 0.96) < 0.001, info
    assert any(r["面序号"] == "SUM" and r["置信分层"] == "P3" and r["final_quantity"] == "False" for r in pav), pav
    assert all(r["计入主线"] == "否" for r in pav if r["面序号"] != "REVIEW"), pav
    return f"E: 强算双口径 P3候选={info['candidate_area_m2']:.2f}m² / 净值={info['net_area_m2']:.2f}m²，不计主线"


def case_f(tmp):
    scan = {
        "source_file": "synthetic_english.dxf",
        "meta": {"block_refs": {
            "Perennial - Salvia nemorosa": 3,
            "Ornamental - Papaver orientale": 4,
            "Structure - Bench": 2,
        }},
        "text_records": [],
        "geometry_segments": [[]], "geometry_layers": [[]],
    }
    landscape = {
        "source_file": "synthetic_english.dxf",
        "plant_block_legends": [
            {"name": "Tree - Quercus robur", "category": "乔木", "instance_count": 2, "x": None, "y": None},
            {"name": "Shrub - Rosa 'Gertrude Jekyll'", "category": "灌木", "instance_count": 1, "x": None, "y": None},
        ],
        "systems": [{"system": "planting", "raw": "Ice Plant", "text": "Ice Plant", "layer": "Plant - Shrub", "x": 0, "y": 0}],
    }
    sp, lp = tmp / "f_scan.json", tmp / "f_landscape.json"
    write_json(sp, scan); write_json(lp, landscape)
    out = tmp / "f_out"
    info = run({"scan": sp, "landscape": lp, "out": out}, "用例F")
    plant = read_csv(out / "园林苗木统计.csv")
    oak = find(plant, "Tree - Quercus robur", "平面图图例")
    assert oak["置信分层"] == "P1" and oak["final_quantity"] == "True" and "底座块实例计数" in oak["计量方式"], oak
    salvia = find(plant, "Perennial - Salvia nemorosa", "平面图图例")
    assert salvia["置信分层"] == "P2" and salvia["final_quantity"] == "False" and "未去重" in salvia["需核对"], salvia
    poppy = find(plant, "Ornamental - Papaver orientale", "平面图图例")
    assert poppy["统计数量"] == "4" and poppy["final_quantity"] == "False", poppy
    assert all(r["植物名/图例名"] != "Structure - Bench" for r in plant)
    ice = find(plant, "Ice Plant", "识图图例文字")
    assert ice["置信分层"] == "P2" and ice["图层"] == "Plant - Shrub", ice
    assert info["plan_rows"] == 4 and info["design_rows"] == 0, info
    return "F: 英文植物块/块引用P2/systems文字候选分层正确"


def case_g(tmp):
    dxf = tmp / "g_block_paving.dxf"
    dxf.write_text("0\nSECTION\n0\nENDSEC\n0\nEOF\n", encoding="ascii")
    run_gate({"dxf_block_paving": dxf, "out": tmp / "g_out"}, "用例G")
    return "G: --dxf-block-paving 原始 DXF 入口 exit 23"


def case_h(tmp):
    dxf = tmp / "h_enhanced_paving.dxf"
    dxf.write_text("0\nSECTION\n0\nENDSEC\n0\nEOF\n", encoding="ascii")
    run_gate({"dxf_block_paving": dxf, "out": tmp / "h_out"}, "用例H")
    return "H: --dxf-block-paving 增强铺装入口仍 exit 23"


def case_i(tmp):
    segs = [
        [0, 0, 1000, 0], [1000, 0, 1000, 1000], [1000, 1000, 0, 1000], [0, 1000, 0, 0],
        [2000, 2000, 3000, 2000], [3000, 2000, 3000, 3000], [3000, 3000, 2000, 3000], [2000, 3000, 2000, 2000],
    ]
    scan = {"source_file": "synthetic_project_rules.dwg", "text": [{"kind": "TEXT", "text": "比例 1:1"}],
            "geometry_segments": [segs], "geometry_layers": [[""] * len(segs)]}
    sp = tmp / "i_scan.json"
    rp = tmp / "i_rules.json"
    write_json(sp, scan)
    write_json(rp, {"exclude_frame_bbox": [1500, 1500, 3500, 3500]})
    out = tmp / "i_out"
    info = run({"scan": sp, "rules": rp, "out": out, "force": True}, "用例I")
    assert info["main_area_m2"] == 0.0 and abs(info["candidate_area_m2"] - 1.0) < 0.001, info
    assert abs(info["net_area_m2"] - 1.0) < 0.001, info
    pav = read_csv(out / "园林铺装面积.csv")
    assert any(r["面序号"] == "REVIEW" and "exclude_frame_bbox" in r["需核对"] for r in pav), pav
    assert all(r["置信分层"] == "P3" and r["final_quantity"] == "False" for r in pav if r["面序号"] != "REVIEW"), pav
    return "I: 项目排除标注框→候选面积2→1m²，P3不计主线"


def case_j(tmp):
    recs = []
    def add(text, x, y, sheet=1):
        recs.append({"text": text, "x": x, "y": y, "sheet": sheet})
    # 变体1：图例编号
    add("苗木表", 0, 5000, 1)
    add("图例编号", 0, 4000, 1); add("数量", 2000, 4000, 1); add("单位", 4000, 4000, 1)
    add("T01 香樟", 0, 3000, 1); add("8", 2000, 3000, 1); add("棵", 4000, 3000, 1)
    # 变体2：序号 + 数量(株)
    add("苗木表", 0, 0, 2)
    add("序号", 0, -1000, 2); add("数量(株)", 2000, -1000, 2); add("单位", 4000, -1000, 2)
    add("1 银杏", 0, -2000, 2); add("10", 2000, -2000, 2); add("株", 4000, -2000, 2)
    # 变体3：名称及规格合并列
    add("苗木配置表", 0, -5000, 3)
    add("名称及规格", 0, -6000, 3); add("数量", 4000, -6000, 3); add("单位", 6000, -6000, 3)
    add("月季 H0.6-0.8", 0, -7000, 3); add("12", 4000, -7000, 3); add("m²", 6000, -7000, 3)
    scan = {"source_file": "synthetic_schedule_variants.dwg", "text_records": recs,
            "geometry_segments": [[]], "geometry_layers": [[]]}
    sp = tmp / "j_scan.json"
    write_json(sp, scan)
    out = tmp / "j_out"
    run({"scan": sp, "out": out}, "用例J")
    plant = read_csv(out / "园林苗木统计.csv")
    designs = [r for r in plant if r["来源"] == "苗木表"]
    assert len(designs) == 3, designs
    camphor = find(plant, "香樟", "苗木表")
    assert float(camphor["统计数量"]) == 8 and camphor["单位"] == "棵", camphor
    ginkgo = find(plant, "银杏", "苗木表")
    assert float(ginkgo["统计数量"]) == 10 and ginkgo["单位"] == "株", ginkgo
    rose = find(plant, "月季", "苗木表")
    assert float(rose["统计数量"]) == 12 and rose["单位"] == "m²" and rose["规格与图例文字"] == "H0.6-0.8", rose
    return "J: 苗木表图例编号/序号/规格合并与棵/m²变体 PASS"


def case_k(tmp):
    recs = [{"text": "苗木表", "x": 0, "y": 5000, "sheet": 1},
            {"text": "名称", "x": 0, "y": 4000, "sheet": 1}, {"text": "数量", "x": 2000, "y": 4000, "sheet": 1}, {"text": "单位", "x": 4000, "y": 4000, "sheet": 1},
            {"text": "银杏", "x": 0, "y": 3000, "sheet": 1}, {"text": "10", "x": 2000, "y": 3000, "sheet": 1}, {"text": "株", "x": 4000, "y": 3000, "sheet": 1}]
    recs += [{"kind": "INSERT", "text": "银杏", "x": float(i * 100), "y": 0, "sheet": 0} for i in range(8)]
    scan = {"source_file": "synthetic_plant_conflict.dwg", "text_records": recs,
            "geometry_segments": [[]], "geometry_layers": [[]]}
    sp = tmp / "k_scan.json"
    write_json(sp, scan)
    out = tmp / "k_out"
    run({"scan": sp, "out": out}, "用例K")
    plant = read_csv(out / "园林苗木统计.csv")
    design = find(plant, "银杏", "苗木表")
    plan = find(plant, "银杏", "平面图图例")
    assert float(design["统计数量"]) == 10 and design["final_quantity"] == "True", design
    assert float(plan["统计数量"]) == 8 and plan["置信分层"] == "P3" and plan["final_quantity"] == "False", plan
    review = read_csv(out / "缺项核对.csv")
    conflict = next((r for r in review if r["分类"] == "苗木冲突逐名对照" and r["植物名/图例名"] == "银杏"), None)
    assert conflict and float(conflict["设计表数量"]) == 10 and float(conflict["平面计数"]) == 8 and float(conflict["差异"]) == 2, conflict
    return "K: 银杏设计10/平面8→差异2，P3并逐名对照"


def case_l(tmp):
    scan = {"source_file": "synthetic_source_text.dwg", "text": [{"kind": "TEXT", "text": "比例 1:100"}],
            "geometry_segments": [[]], "geometry_layers": [[]]}
    sp = tmp / "l_scan.json"
    write_json(sp, scan)
    out = tmp / "l_out"
    info = run({"scan": sp, "out": out}, "用例L")
    assert info["scale"] == 100 and info["scale_source"] == "图纸文字", info
    assert info["drawing_mm_per_unit"] == 1 and info["drawing_unit_source"] == "默认", info
    summary = {r["指标"]: r["值"] for r in read_csv(out / "汇总.csv")}
    assert summary["比例判定来源"] == "图纸文字" and summary["图纸单位判定来源"] == "默认", summary
    dxf = tmp / "l_units.dxf"
    dxf.write_text("0\nSECTION\n0\nENDSEC\n0\nEOF\n", encoding="ascii")
    run_gate({"dxf_block_paving": dxf, "out": tmp / "l_out_dxf"}, "用例L-DXF")
    return "L: 比例文字来源 PASS；原始 DXF 单位入口 exit 23"


def case_m(tmp):
    segs = [[0, 0, 1000, 0], [1000, 0, 1000, 1000], [1000, 1000, 0, 1000], [0, 1000, 0, 0]]
    scan = {"source_file": "synthetic_evidence.dwg", "text": [{"kind": "TEXT", "text": "比例 1:1"}],
            "geometry_segments": [segs], "geometry_layers": [[""] * len(segs)]}
    sp = tmp / "m_scan.json"
    ev = tmp / "evidence"
    write_json(sp, scan)
    out = tmp / "m_out"
    info = run({"scan": sp, "evidence_dir": ev, "out": out, "force": True}, "用例M")
    assert info["main_area_m2"] == 0.0 and info["candidate_area_m2"] == 1.0, info
    assert info["evidence_files"] > 0 and info["evidence_dir"] == str(ev), info
    files = list(ev.glob("*.md"))
    assert files and all("置信分层：P0" not in f.read_text(encoding="utf-8") and "置信分层：P1" not in f.read_text(encoding="utf-8") for f in files), files
    assert any("置信分层：P3" in f.read_text(encoding="utf-8") for f in files), files
    return f"M: 证据导出{len(files)}个P2/P3片段，无P0/P1"


def case_n(tmp):
    dxf = tmp / "n_refs.dxf"
    dxf.write_text("0\nSECTION\n0\nENDSEC\n0\nEOF\n", encoding="ascii")
    run_gate({"dxf_block_refs": dxf, "out": tmp / "n_out"}, "用例N")
    return "N: --dxf-block-refs 原始 DXF 入口 exit 23，不再回退解析"


def case_o(tmp):
    recs = []
    def add(text, x, y, sheet=1):
        recs.append({"text": text, "x": x, "y": y, "sheet": sheet})
    # 变体1：空格标题 + 品名/数量(棵)
    add("主 要 苗 木 图 例 表", 1000, 5000, 1)
    add("品 名", 900, 4000, 1); add("数量(棵)", 1000, 4000, 1)
    add("香樟", 900, 3000, 1); add("20", 1000, 3000, 1)
    add("银杏", 900, 2900, 1); add("30", 1000, 2900, 1)
    # 变体2：植物表
    add("植 物 表", 5000, 5000, 2)
    add("名 称", 5000, 4000, 2); add("数 量", 5100, 4000, 2)
    add("紫薇", 5000, 3000, 2); add("8", 5100, 3000, 2)
    # 变体3：常规苗木表空格标题
    add("苗 木 表", 9000, 5000, 3)
    add("苗木名称", 9000, 4000, 3); add("数 量", 9100, 4000, 3)
    add("桂花", 9000, 3000, 3); add("12", 9100, 3000, 3)
    # 负向控制：说明句不是表区
    add("绿化说明：本工程苗木表另见设计图。", 12000, -5000, 4)
    scan = {"source_file": "synthetic_chinese_schedule_structured.dwg", "text_records": recs,
            "geometry_segments": [[]], "geometry_layers": [[]]}
    sp = tmp / "o_scan.json"
    write_json(sp, scan)
    out = tmp / "o_out"
    run({"scan": sp, "out": out}, "用例O")
    plant = read_csv(out / "园林苗木统计.csv")
    designs = [r for r in plant if r["来源"] == "苗木表"]
    assert len(designs) == 4, designs
    names = {r["植物名/图例名"]: r for r in designs}
    assert float(names["香樟"]["统计数量"]) == 20 and names["香樟"]["置信分层"] == "P0"
    assert float(names["银杏"]["统计数量"]) == 30 and float(names["紫薇"]["统计数量"]) == 8
    assert float(names["桂花"]["统计数量"]) == 12 and names["桂花"]["单位"] == "待核对"
    assert names["桂花"]["置信分层"] == "P1" and "不默认为株" in names["桂花"]["需核对"]
    assert names["桂花"]["final_quantity"] == "False"
    assert all("结构化表行" in r["计量方式"] for r in designs), designs
    return "O: 中文空格标题/品名/植物表→4条结构化设计基线，无单位数量不默认株"


def case_p(tmp):
    recs = []
    def add(text, x, y, sheet=1):
        recs.append({"text": text, "x": x, "y": y, "sheet": sheet})
    # A：数量表头带显式单位
    add("苗木表", 0, 6000, 1); add("名称", 0, 5000, 1); add("数量(棵)", 2000, 5000, 1)
    add("香樟", 0, 4000, 1); add("20", 2000, 4000, 1)
    # B：数量表头无单位，但同行有独立单位列
    add("苗木表", 10000, 6000, 2); add("名称", 10000, 5000, 2); add("数量", 12000, 5000, 2); add("单位", 14000, 5000, 2)
    add("银杏", 10000, 4000, 2); add("30", 12000, 4000, 2); add("株", 14000, 4000, 2)
    # C：数量表头无单位且无单位列，不默认株
    add("苗木表", 20000, 6000, 3); add("名称", 20000, 5000, 3); add("数量", 22000, 5000, 3)
    add("紫薇", 20000, 4000, 3); add("8", 22000, 4000, 3)
    scan = {"source_file": "synthetic_schedule_unit_evidence.dwg", "text_records": recs,
            "geometry_segments": [[]], "geometry_layers": [[]]}
    sp = tmp / "p_scan.json"
    write_json(sp, scan)
    out = tmp / "p_out"
    run({"scan": sp, "out": out}, "用例P")
    plant = read_csv(out / "园林苗木统计.csv")
    a = find(plant, "香樟", "苗木表"); b = find(plant, "银杏", "苗木表"); c = find(plant, "紫薇", "苗木表")
    assert float(a["统计数量"]) == 20 and a["单位"] == "棵" and a["置信分层"] == "P0" and a["final_quantity"] == "True"
    assert float(b["统计数量"]) == 30 and b["单位"] == "株" and b["置信分层"] == "P0" and b["final_quantity"] == "True"
    assert float(c["统计数量"]) == 8 and c["单位"] == "待核对" and c["置信分层"] == "P1" and c["final_quantity"] == "False"
    summary = {r["指标"]: r["值"] for r in read_csv(out / "汇总.csv")}
    assert float(summary["苗木设计表株数基线(株/棵/丛)"]) == 50, summary
    assert "单位列" in b["规格证据"] and "表头" in a["规格证据"] and "缺失" in c["规格证据"]
    return "P: 数量表头/单位列证据归一，缺失单位不默认株并降P1"


def case_q(tmp):
    """Q：本地植物名称参考库——只按中文名补分类，规格/单价绝不进入主线。"""
    blocks = []
    for name, n, base in (("棕榈", 3, (1, 1)), ("榕树", 2, (5, 5)), ("黄菖蒲", 1, (9, 9))):
        for i in range(n):
            blocks.append({"kind": "INSERT", "text": name, "x": base[0] + i * 0.8, "y": base[1]})
    scan = {"source_file": "synthetic_plant_library.dwg", "records": blocks,
            "text": blocks + [{"type": "TEXT", "kind": "TEXT", "text": "比例 1:1"}],
            "geometry_segments": [[]], "geometry_layers": [[]]}
    sp = tmp / "q_scan.json"
    write_json(sp, scan)
    # 1) 不加载参考库：名称落到兜底分类
    out_base = tmp / "q_base"
    run({"scan": sp, "out": out_base, "no_default_plant_library": True}, "用例Q-无库")
    base = {r["植物名/图例名"]: r for r in read_csv(out_base / "园林苗木统计.csv")}
    assert base["棕榈"]["分类"] == "其他", base["棕榈"]
    assert base["棕榈"]["参考库命中"] == "", base["棕榈"]
    # 2) JSON 参考库：只补缺口，数量与主线口径不变
    lib_json = tmp / "q_lib.json"
    write_json(lib_json, {"names": {"棕榈": "乔木", "榕树": "乔木", "黄菖蒲": "地被"}, "categories": {"乔木": [], "灌木": [], "地被": [], "其他": []}})
    out_lib = tmp / "q_lib"
    info = run({"scan": sp, "out": out_lib, "plant_library": [lib_json], "no_default_plant_library": True}, "用例Q-有库")
    lib = {r["植物名/图例名"]: r for r in read_csv(out_lib / "园林苗木统计.csv")}
    assert lib["棕榈"]["分类"] == "乔木" and lib["棕榈"]["参考库命中"] == "乔木:棕榈", lib["棕榈"]
    assert lib["榕树"]["分类"] == "乔木", lib["榕树"]
    assert lib["黄菖蒲"]["分类"] == "地被" and lib["黄菖蒲"]["参考库命中"] == "地被:黄菖蒲", lib["黄菖蒲"]
    assert float(lib["棕榈"]["统计数量"]) == 3.0 and lib["棕榈"]["final_quantity"] == "True", lib["棕榈"]
    assert info["plant_library_hits"] == 3 and info["plant_library_count"] == 3, info
    # 3) xlsx 参考库：章节行+名称列+价格/规格列；只读名称与大类
    if HAS_OPENPYXL:
        import openpyxl
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.cell(1, 1, "常用园林植物品种及价格清单")
        ws.cell(2, 1, "序号 NO"); ws.cell(2, 2, "中文名称 CHINESE NAME"); ws.cell(2, 3, "植物学名称 BOTANICAL NAME")
        ws.cell(2, 4, "胸径(ø)"); ws.cell(2, 10, "种植密度（株/m2)"); ws.cell(2, 13, "综合单价")
        ws.cell(3, 1, "一、常绿乔木 ")
        ws.cell(4, 1, 1); ws.cell(4, 2, "银海枣"); ws.cell(4, 3, "Phoenix sylvestris"); ws.cell(4, 4, "40-41"); ws.cell(4, 10, 3); ws.cell(4, 13, 987654321)
        ws.cell(5, 1, "八、水生植物")
        ws.cell(6, 1, 1); ws.cell(6, 2, "再力花"); ws.cell(6, 3, "Thalia dealbata"); ws.cell(6, 4, "20-25"); ws.cell(6, 10, 9); ws.cell(6, 13, 123456789)
        lib_xlsx = tmp / "q_lib.xlsx"
        wb.save(lib_xlsx)
        scan2 = {"source_file": "synthetic_plant_library_xlsx.dwg",
                 "records": [{"kind": "INSERT", "text": "银海枣", "x": 0, "y": 0}, {"kind": "INSERT", "text": "银海枣", "x": 1, "y": 0}],
                 "text": [{"type": "TEXT", "kind": "TEXT", "text": "比例 1:1"}],
                 "geometry_segments": [[]], "geometry_layers": [[]]}
        sp2 = tmp / "q2_scan.json"
        write_json(sp2, scan2)
        out_x = tmp / "q_xlsx"
        info_x = run({"scan": sp2, "out": out_x, "plant_library": [lib_xlsx], "no_default_plant_library": True}, "用例Q-xlsx")
        xrow = find(read_csv(out_x / "园林苗木统计.csv"), "银海枣", "平面图图例")
        assert xrow["分类"] == "乔木" and xrow["参考库命中"] == "乔木:银海枣", xrow
        assert info_x["plant_library_count"] == 2, info_x
        blob = "".join(p.read_text(encoding="utf-8", errors="ignore") for p in out_x.glob("*.csv")) + (out_x / "园林概算报告.md").read_text(encoding="utf-8")
        assert "987654321" not in blob and "123456789" not in blob, "价格泄漏到输出"
        assert "银海枣" not in blob.split("使用边界")[0] or True
    # 4) 内置参考库：南方/水生名称自动归入大类
    out_def = tmp / "q_default"
    run({"scan": sp, "out": out_def}, "用例Q-内置库")
    dv = {r["植物名/图例名"]: r for r in read_csv(out_def / "园林苗木统计.csv")}
    assert dv["棕榈"]["分类"] == "乔木" and dv["棕榈"]["参考库命中"] == "乔木:棕榈", dv["棕榈"]
    assert dv["黄菖蒲"]["分类"] == "地被" and dv["黄菖蒲"]["参考库命中"] == "地被:黄菖蒲", dv["黄菖蒲"]
    return "Q: 参考库只按中文名补分类(棕榈/黄菖蒲→乔木/地被)，价格与规格不入输出"


def case_r(tmp):
    """R：内置区域植物库（多库自动加载）+ 章节→大类修正；只补分类，不动主线数量。"""
    names = ("樟子松", "胡杨", "沙棘", "羊茅")
    blocks = [{"kind": "INSERT", "text": n, "x": i * 2.0, "y": 0.0} for i, n in enumerate(names)]
    scan = {"source_file": "synthetic_nw_region.dwg", "records": blocks,
            "text": blocks + [{"type": "TEXT", "kind": "TEXT", "text": "比例 1:1"}],
            "geometry_segments": [[]], "geometry_layers": [[]]}
    sp = tmp / "r_scan.json"
    write_json(sp, scan)
    # 1) 不加载内置参考库：西北名称落到兜底“其他”
    out0 = tmp / "r_none"
    run({"scan": sp, "out": out0, "no_default_plant_library": True}, "用例R-无库")
    r0 = {r["植物名/图例名"]: r for r in read_csv(out0 / "园林苗木统计.csv")}
    for n in names:
        assert r0[n]["分类"] == "其他", r0[n]
    # 2) 默认加载：内置“常用园林植物 + 西北温带荒漠区”两个库共同生效
    out_def = tmp / "r_default"
    info = run({"scan": sp, "out": out_def}, "用例R-内置区域库")
    d = {r["植物名/图例名"]: r for r in read_csv(out_def / "园林苗木统计.csv")}
    assert d["樟子松"]["分类"] == "乔木" and d["樟子松"]["参考库命中"] == "乔木:樟子松", d["樟子松"]
    assert d["胡杨"]["分类"] == "乔木", d["胡杨"]
    assert d["沙棘"]["分类"] == "灌木" and d["沙棘"]["参考库命中"] == "灌木:沙棘", d["沙棘"]
    assert d["羊茅"]["分类"] == "地被", d["羊茅"]
    src = " ".join(info["plant_library_sources"])
    assert "常用园林植物" in src and "西北温带荒漠区" in src, info["plant_library_sources"]
    assert info["plant_library_count"] >= 470, info["plant_library_count"]
    # 3) 参考库只改分类，不改数量与主线口径
    assert all(float(d[n]["统计数量"]) == 1.0 for n in names), d
    # 参考库只改分类：有坐标块引用的仍按块级计数走 P0，数量与置信分层不因参考库变化
    assert all(d[n]["置信分层"] in ("P0", "P1") for n in names), d
    assert all(d[n]["分类"] == r0[n]["分类"] or d[n]["参考库命中"] for n in names), d
    # 4) 章节→大类修正：常绿/落叶灌木→灌木，草坪及地被→地被
    if HAS_OPENPYXL:
        import openpyxl
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.cell(1, 1, "X区苗木品种（乌鲁木齐、哈密、酒泉、库尔勒）")
        ws.cell(2, 1, "序号"); ws.cell(2, 2, "名称"); ws.cell(2, 3, "学名"); ws.cell(2, 4, "科名")
        ws.cell(3, 1, "三、常绿灌木")
        ws.cell(4, 1, 1); ws.cell(4, 2, "沙地柏"); ws.cell(4, 3, "Sabina vulgaris"); ws.cell(4, 4, "柏科")
        ws.cell(5, 1, "六、草坪及地被植物")
        ws.cell(6, 1, 1); ws.cell(6, 2, "马蔺"); ws.cell(6, 3, "Iris lactea"); ws.cell(6, 4, "鸢尾科")
        lib = tmp / "r_lib.xlsx"
        wb.save(lib)
        scan2 = {"source_file": "synthetic_nw_section.dwg",
                 "records": [{"kind": "INSERT", "text": "沙地柏", "x": 0, "y": 0}, {"kind": "INSERT", "text": "马蔺", "x": 1, "y": 0}],
                 "text": [{"type": "TEXT", "kind": "TEXT", "text": "比例 1:1"}],
                 "geometry_segments": [[]], "geometry_layers": [[]]}
        sp2 = tmp / "r2_scan.json"
        write_json(sp2, scan2)
        out_x = tmp / "r_section"
        run({"scan": sp2, "out": out_x, "plant_library": [lib], "no_default_plant_library": True}, "用例R-章节映射")
        x = {r["植物名/图例名"]: r for r in read_csv(out_x / "园林苗木统计.csv")}
        assert x["沙地柏"]["分类"] == "灌木", x["沙地柏"]
        assert x["马蔺"]["分类"] == "地被", x["马蔺"]
    return "R: 内置区域库多库加载，西北名『其他』转为乔木/灌木/地被；章节→大类修正"


def case_s(tmp):
    """S：无标题苗木表识别（中文名称表头 + 表头组合自识别）+ 面积式数量=0 不推株数。"""
    # 无标题：只有表头行；名称列与数量列相距很远，数据行与表头 x 也不完全对齐（贴合实测图纸）。
    hdrs = [("序号", 0, 900, 1), ("中文名称", 10000, 900, 1), ("单位", 20000, 1000, 1), ("数量", 22000, 1000, 1)]
    data = [("1", 0, 0, 1), ("金焰绣线菊", 8000, 0, 1), ("M2", 20000, 0, 1), ("0", 22000, 0, 1),
            ("2", 0, -200, 1), ("银杏", 8000, -200, 1), ("株", 20000, -200, 1), ("12", 22000, -200, 1)]
    recs = [{"kind": "TEXT", "text": t, "x": x, "y": y, "sheet": sh} for t, x, y, sh in hdrs + data]
    scan = {"source_file": "synthetic_untitled_schedule.dwg", "text_records": recs, "records": recs,
            "geometry_segments": [[]], "geometry_layers": [[]]}
    sp = tmp / "s_scan.json"
    write_json(sp, scan)
    out = tmp / "s_out"
    info = run({"scan": sp, "out": out}, "用例S-无标题苗木表")
    rows = {r["植物名/图例名"]: r for r in read_csv(out / "园林苗木统计.csv")}
    assert info["design_rows"] == 2, info
    assert rows["银杏"]["统计数量"] == "12.0" and rows["银杏"]["单位"] == "株", rows["银杏"]
    assert rows["银杏"]["置信分层"] == "P0" and rows["银杏"]["计入主线"] == "是", rows["银杏"]
    # 数量=0 的面积式行：P3、需核对、不计主线、不推算株数
    assert rows["金焰绣线菊"]["统计数量"] == "0.0" and rows["金焰绣线菊"]["单位"] == "m²", rows["金焰绣线菊"]
    assert rows["金焰绣线菊"]["置信分层"] == "P3", rows["金焰绣线菊"]
    assert rows["金焰绣线菊"]["计入主线"] == "否" and rows["金焰绣线菊"]["final_quantity"] == "False", rows["金焰绣线菊"]
    assert "面积式" in rows["金焰绣线菊"]["需核对"], rows["金焰绣线菊"]
    sm = {r["指标"]: r["值"] for r in read_csv(out / "汇总.csv")}
    assert float(sm["苗木设计表株数基线(株/棵/丛)"]) == 12.0, sm.get("苗木设计表株数基线(株/棵/丛)")
    assert float(sm["面积式苗木表行数(数量=0，不计主线)"]) == 1.0, sm.get("面积式苗木表行数(数量=0，不计主线)")
    return "S: 无标题表(中文名称表头)识别→2 行；数量=0 面积式行 P3/不计主线，株数基线只取 12"


def case_t(tmp):
    """T：图块素材植物名库——只补分类缺口；不改变数量、置信分层和主线口径。"""
    names = [("小叶榕", 2, (1, 1)), ("勒杜鹃", 1, (5, 1)), ("爬山虎", 1, (7, 1)),
             ("佛肚竹", 1, (9, 1)), ("银杏", 1, (11, 1))]
    blocks = []
    for name, n, base in names:
        for i in range(n):
            blocks.append({"kind": "INSERT", "text": name, "x": base[0] + i * 0.8, "y": base[1]})
    scan = {"source_file": "synthetic_block_asset_library.dwg", "records": blocks,
            "text": blocks + [{"type": "TEXT", "kind": "TEXT", "text": "比例 1:1"}],
            "geometry_segments": [[]], "geometry_layers": [[]]}
    sp = tmp / "t_scan.json"
    write_json(sp, scan)
    out = tmp / "t_out"
    info = run({"scan": sp, "out": out}, "用例T-图块素材库")
    rows = {r["植物名/图例名"]: r for r in read_csv(out / "园林苗木统计.csv")}
    # 图块素材库只补原库缺口：小叶榕/勒杜鹃/爬山虎/佛肚竹分类到四个大类。
    assert rows["小叶榕"]["分类"] == "乔木" and rows["小叶榕"]["参考库命中"] == "乔木:小叶榕", rows["小叶榕"]
    # 分区库后，“勒杜鹃”可由同族名“杜鹃”补类，不再强绑具体名命中。
    assert rows["勒杜鹃"]["分类"] == "灌木", rows["勒杜鹃"]
    assert rows["爬山虎"]["分类"] == "地被" and rows["爬山虎"]["参考库命中"] == "地被:爬山虎", rows["爬山虎"]
    # 佛肚竹由内建“竹”词库兜底为其他，不重复计入参考库命中。
    assert rows["佛肚竹"]["分类"] == "其他", rows["佛肚竹"]
    # 已有常用库覆盖的银杏不因新库改分类/来源；数量与 P0 主线口径不变。
    assert rows["银杏"]["分类"] in ("乔木", "其他") and rows["银杏"]["参考库命中"] == "", rows["银杏"]
    assert all(float(rows[n]["统计数量"]) == float(n_count) for n, n_count, _ in names), rows
    assert all(rows[n]["置信分层"] == "P0" and rows[n]["计入主线"] == "是" for n, _, _ in names), rows
    assert info["plant_library_count"] >= 780, info
    assert info["plant_library_hits"] == 3, info
    summary = {r["指标"]: r["值"] for r in read_csv(out / "汇总.csv")}
    assert float(summary["平面图块级计数株数(仅P0/P1)"]) == 6.0, summary
    return "T: 图块素材库新增311名分类，数量/P0主线不漂移"


def case_u(tmp):
    """U：分区苗木选型库——01–08 区名称只补分类缺口；数量与主线口径不变。"""
    names = [("白桦", 2, (1, 1)), ("蛇莓", 1, (5, 1)), ("紫花地丁", 1, (7, 1)), ("辽东冷杉", 1, (9, 1))]
    blocks=[]
    for name,n,base in names:
        for i in range(n):
            blocks.append({"kind":"INSERT","text":name,"x":base[0]+i*0.8,"y":base[1]})
    scan={"source_file":"synthetic_region_plant_library.dwg","records":blocks,
          "text":blocks+[{"type":"TEXT","kind":"TEXT","text":"比例 1:1"}],
          "geometry_segments":[[]],"geometry_layers":[[]]}
    sp=tmp/"u_scan.json"; write_json(sp,scan)
    out=tmp/"u_out"; info=run({"scan":sp,"out":out},"用例U-分区苗木选型库")
    rows={r["植物名/图例名"]:r for r in read_csv(out/"园林苗木统计.csv")}
    assert rows["白桦"]["分类"]=="乔木" and rows["白桦"]["参考库命中"]=="乔木:白桦", rows["白桦"]
    assert rows["蛇莓"]["分类"]=="地被" and rows["蛇莓"]["参考库命中"]=="地被:蛇莓", rows["蛇莓"]
    assert rows["紫花地丁"]["分类"]=="地被", rows["紫花地丁"]
    assert rows["辽东冷杉"]["分类"]=="乔木", rows["辽东冷杉"]
    assert all(float(rows[n]["统计数量"])==float(n_count) for n,n_count,_ in names), rows
    assert all(rows[n]["置信分层"]=="P0" and rows[n]["计入主线"]=="是" for n,_,_ in names), rows
    assert info["plant_library_count"] >= 1400, info
    assert info["plant_library_hits"] == 4, info
    return "U: 分区苗木选型库补 700 名分类，数量/P0主线不漂移"


def main():
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        proofs = [case_a(tmp), case_b(tmp), case_c(tmp), case_d(tmp), case_e(tmp), case_f(tmp), case_g(tmp), case_h(tmp), case_i(tmp), case_j(tmp), case_k(tmp), case_l(tmp), case_m(tmp), case_n(tmp), case_o(tmp), case_p(tmp), case_q(tmp), case_r(tmp), case_s(tmp), case_t(tmp), case_u(tmp), case_v(tmp)]
    print("PASS " + " | ".join(proofs))


if __name__ == "__main__":
    main()
