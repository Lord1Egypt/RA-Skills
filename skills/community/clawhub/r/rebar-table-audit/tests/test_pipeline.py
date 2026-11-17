"""抽取 + 规则核对的场景测试，全部用 make_fixtures.py 合成的 DXF（内存里的 ezdxf Drawing）。"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import make_fixtures as fx

from rebar_table_audit import extract, rules
from rebar_table_audit import tables as tables_mod
from rebar_table_audit.symbols import load_symbol_table


def run_pipeline(doc):
    extraction = extract.extract_all(doc)
    symtab = load_symbol_table()
    found = tables_mod.find_tables(extraction.texts, extraction.segments, symtab)
    findings, gaps = rules.run_all_rules(found)
    return found, findings, gaps, symtab


def _severities(findings, rule_id=None):
    return [f for f in findings if rule_id is None or f["rule_id"] == rule_id]


def test_clean_table_zero_findings():
    doc = fx.new_doc()
    msp = doc.modelspace()
    fx.build_table(msp, rows=fx.clean_table_rows(), totals_lines=fx.clean_table_totals())

    found, findings, gaps, _ = run_pipeline(doc)
    assert len(found) == 1
    t = found[0]
    assert len(t["rows"]) == 2
    assert re.match(r"^TEXT:\w+$", t["title_handle"])
    errors = [f for f in findings if f["severity"] == "error"]
    assert errors == [], errors
    assert gaps == [], gaps
    # 数值核实：编号1 diameter=12 total_length_m=25.0 weight=22.2
    row1 = next(r for r in t["rows"] if r["parsed"]["mark"] == "1")
    assert row1["parsed"]["diameter_mm"] == 12.0
    assert row1["parsed"]["grade"] == "HRB400"
    assert abs(row1["parsed"]["total_length_m"] - 25.0) < 1e-6
    assert abs(row1["parsed"]["weight_kg"] - 22.20) < 1e-6


def test_weight_digits_swapped_triggers_r001_and_r003():
    rows = fx.clean_table_rows()
    # 把编号2 的重量从 23.70 改成明显偏离（数字顺序颠倒）27.30，触发 R001；
    # 声明合计仍是原来两行之和 45.90，行和变成 22.20+27.30=49.50，触发 R003。
    rows[1][-1] = "27.30"
    doc = fx.new_doc()
    msp = doc.modelspace()
    fx.build_table(msp, rows=rows, totals_lines=fx.clean_table_totals())

    found, findings, gaps, _ = run_pipeline(doc)
    r001 = _severities(findings, "R001")
    r003 = _severities(findings, "R003")
    assert len(r001) == 1 and r001[0]["severity"] == "error" and r001[0]["row_mark"] == "2"
    assert len(r003) == 1 and r003[0]["severity"] == "error"
    assert any(f["severity"] == "error" for f in findings)


def test_duplicate_mark_triggers_r004_warning_only():
    rows = fx.clean_table_rows()
    rows[1][0] = "1"  # 编号重复
    doc = fx.new_doc()
    msp = doc.modelspace()
    fx.build_table(msp, rows=rows, totals_lines=["HRB400:45.90kg"])

    found, findings, gaps, _ = run_pipeline(doc)
    r004 = _severities(findings, "R004")
    assert len(r004) == 1
    assert r004[0]["severity"] == "warning"
    assert set(r004[0]["handles"])  # 至少带上重复行的证据
    assert not any(f["severity"] == "error" for f in findings)


def test_header_declares_cm_but_values_are_meters_triggers_r006():
    doc = fx.new_doc()
    msp = doc.modelspace()
    fx.build_table(msp, rows=fx.clean_table_rows(), totals_lines=fx.clean_table_totals(), header_total_unit="cm")

    found, findings, gaps, _ = run_pipeline(doc)
    r006 = _severities(findings, "R006")
    assert len(r006) == 1
    assert r006[0]["severity"] == "warning"
    assert r006[0]["expected"] == "cm"
    assert r006[0]["actual"] == "m"
    # R006 改判后 R001 不应再报错（用推断出的 m 计算重量恰好匹配）
    assert not any(f["rule_id"] == "R001" for f in findings)
    t = found[0]
    assert t["columns"][5]["unit_declared"] == "cm"
    assert t["columns"][5]["unit_inferred"] == "m"


def test_r006_majority_pass_isolates_the_one_wrong_row():
    """表头写 cm，数值实为 m；6 行里只有 1 行重量数字颠倒。多数通过（5/6）应反推为 m 并发
    1 条 R006，反推之后仅那一行本身的错误单独触发 1 条 R001，其余 5 行不应被牵连报错。"""
    rows = [
        ["1", "顶板", "%%13212", "10.000", "1", "10.000", "8.88"],
        ["2", "顶板", "%%13212", "20.000", "1", "20.000", "17.76"],
        ["3", "顶板", "%%13212", "30.000", "1", "30.000", "62.64"],  # 应为 26.64，数字颠倒
        ["4", "顶板", "%%13212", "40.000", "1", "40.000", "35.52"],
        ["5", "顶板", "%%13212", "50.000", "1", "50.000", "44.40"],
        ["6", "顶板", "%%13212", "60.000", "1", "60.000", "53.28"],
    ]
    doc = fx.new_doc()
    msp = doc.modelspace()
    fx.build_table(msp, rows=rows, totals_lines=[], header_total_unit="cm")

    found, findings, gaps, _ = run_pipeline(doc)
    t = found[0]
    r006 = _severities(findings, "R006")
    r001 = _severities(findings, "R001")
    assert len(r006) == 1
    assert r006[0]["expected"] == "cm"
    assert r006[0]["actual"] == "m"
    assert "0/6" in r006[0]["message"] and "5/6" in r006[0]["message"]
    assert len(r001) == 1
    assert r001[0]["row_mark"] == "3"
    assert t["columns"][5]["unit_inferred"] == "m"


def test_r006_tied_alternate_units_not_adopted():
    """两个候选单位（这里是 cm 与 m）核对通过数并列最高时，不采纳任何一个、不发 R006。"""
    rows = [
        ["1", "顶板", "%%13212", "1.000", "1", "1.000", "0.505"],
        ["2", "顶板", "%%13212", "1.000", "1", "1.000", "0.505"],
    ]
    doc = fx.new_doc()
    msp = doc.modelspace()
    fx.build_table(msp, rows=rows, totals_lines=[], header_total_unit="mm")

    found, findings, gaps, _ = run_pipeline(doc)
    t = found[0]
    r006 = _severities(findings, "R006")
    assert r006 == []
    # 未采纳时 unit_inferred 保持等于声明单位（未被 rules.py 改写）
    assert t["columns"][5]["unit_inferred"] == t["columns"][5]["unit_declared"] == "mm"


def test_r006_single_applicable_row_never_infers():
    """只有 1 个适用行时样本不足，不做单位反推，即使该单位下这一行核对失败也不发 R006。"""
    rows = fx.clean_table_rows()[:1]
    doc = fx.new_doc()
    msp = doc.modelspace()
    fx.build_table(msp, rows=rows, totals_lines=[], header_total_unit="cm")

    found, findings, gaps, _ = run_pipeline(doc)
    t = found[0]
    r006 = _severities(findings, "R006")
    assert r006 == []
    assert t["columns"][5]["unit_inferred"] == t["columns"][5]["unit_declared"] == "cm"


def test_unknown_symbol_logs_r005_gap_row_kept():
    rows = fx.clean_table_rows()
    rows[0][2] = "%%19912"  # 未知控制码，非默认映射表里的任何符号
    doc = fx.new_doc()
    msp = doc.modelspace()
    fx.build_table(msp, rows=rows, totals_lines=fx.clean_table_totals())

    found, findings, gaps, _ = run_pipeline(doc)
    t = found[0]
    assert len(t["rows"]) == 2  # 行没有被丢弃
    row1 = next(r for r in t["rows"] if r["parsed"]["mark"] == "1")
    assert row1["parsed"]["diameter_mm"] is None
    assert row1["parsed"]["grade"] is None
    r005 = [g for g in gaps if g["rule_id"] == "R005"]
    assert any("%%19912" in g["message"] or "未识别的符号编码" in g["message"] for g in r005)
    # 该行因缺直径无法核对 R001，不应算作 error
    assert not any(f["rule_id"] == "R001" and f["row_mark"] == "1" for f in findings)


def test_table_inside_scaled_translated_block():
    doc = fx.new_doc()
    block = doc.blocks.new("TBLK")
    fx.build_table(block, origin=(0.0, 0.0), rows=fx.clean_table_rows(), totals_lines=fx.clean_table_totals())
    msp = doc.modelspace()
    insert = msp.add_blockref("TBLK", (500.0, 500.0), dxfattribs={"xscale": 2.0, "yscale": 2.0, "zscale": 2.0})

    found, findings, gaps, _ = run_pipeline(doc)
    assert len(found) == 1
    t = found[0]
    assert t["title_handle"].startswith(f"INSERT:{insert.dxf.handle}>TEXT:")
    row1 = next(r for r in t["rows"] if r["parsed"]["mark"] == "1")
    assert abs(row1["parsed"]["weight_kg"] - 22.20) < 1e-6  # 数值内容不受几何缩放影响
    assert not any(f["severity"] == "error" for f in findings)


def test_declared_totals_split_across_two_text_objects():
    doc = fx.new_doc()
    msp = doc.modelspace()
    fx.build_table(
        msp,
        rows=[fx.clean_table_rows()[0]],
        totals_lines=["HRB400:22.20kg"],
        totals_split=[["HRB400:", "22.20kg"]],
    )
    found, findings, gaps, _ = run_pipeline(doc)
    t = found[0]
    assert len(t["declared_totals"]) == 1
    decl = t["declared_totals"][0]
    assert decl["grade"] == "HRB400"
    assert abs(decl["value_kg"] - 22.20) < 1e-6
    assert len(decl["handles"]) == 2  # 两个独立文字对象拼接而成
    assert not any(f["severity"] == "error" for f in findings)


def test_no_title_no_grid_returns_no_tables():
    doc = fx.new_doc()
    msp = doc.modelspace()
    msp.add_text("说明：本图仅供参考", dxfattribs={"height": 3.5, "insert": (0, 0)})
    msp.add_line((0, -5), (50, -5))

    found, findings, gaps, _ = run_pipeline(doc)
    assert found == []


def test_r002_single_length_times_count_mismatch():
    rows = fx.clean_table_rows()
    rows[0][4] = "8"  # 根数从 10 改成 8，但总长仍是 25.000（单根长 2.500），2.5*8=20 != 25
    doc = fx.new_doc()
    msp = doc.modelspace()
    fx.build_table(msp, rows=rows, totals_lines=fx.clean_table_totals())

    found, findings, gaps, _ = run_pipeline(doc)
    r002 = _severities(findings, "R002")
    assert len(r002) == 1
    assert r002[0]["row_mark"] == "1"
    assert abs(r002[0]["expected"] - 20.0) < 1e-6


def test_title_underline_and_scope_notes_do_not_fool_topline_search():
    """复现真实样图的版式：标题下方先是双下划线，再隔两行 scope_notes，再才是真网格。
    topline 选择必须跳过下划线（没有竖线相接），落到真正的网格上边框。"""
    doc = fx.new_doc()
    msp = doc.modelspace()
    fx.build_table(
        msp,
        rows=fx.clean_table_rows(),
        totals_lines=fx.clean_table_totals(),
        scope_notes=["(适用于C-C剖面)", "(每延米)"],
        title_underline=True,
    )

    found, findings, gaps, _ = run_pipeline(doc)
    assert len(found) == 1
    t = found[0]
    assert len(t["rows"]) == 2
    assert [n["text"] for n in t["scope_notes"]] == ["(适用于C-C剖面)", "(每延米)"] or \
        sorted(n["text"] for n in t["scope_notes"]) == sorted(["(适用于C-C剖面)", "(每延米)"])
    assert not any(g["rule_id"] == "R005" for g in gaps)
    assert not any(f["severity"] == "error" for f in findings)


def test_title_with_underline_but_no_grid_is_gap_not_crash():
    """标题下有下划线，但下划线之下根本没有表格网格——必须记 R005 gap，不能崩，也不能
    把下划线误判成表格（还原不出任何数据行）。"""
    doc = fx.new_doc()
    msp = doc.modelspace()
    fx.build_table(msp, title_underline=True, draw_grid=False)

    found, findings, gaps, _ = run_pipeline(doc)
    assert len(found) == 1
    t = found[0]
    assert len(t["rows"]) == 0
    assert len(t["columns"]) == 0
    r005 = [g for g in gaps if g["rule_id"] == "R005"]
    assert len(r005) == 1
    assert "合格" in r005[0]["message"] or "网格" in r005[0]["message"]


def test_grid_sanity_gate_rejects_runaway_column_flood():
    """模拟"上边框被延长、沿途一串刻度短竖线全被 flood 吸进来"的污染场景（现实里常见于
    尺寸标注/刻度线紧贴在表格顶线旁边），列数/包围盒会远超正常表格，必须判 gap 而不是
    吐出一张 75 列的垃圾表。"""
    doc = fx.new_doc()
    msp = doc.modelspace()
    info = fx.build_table(msp, rows=fx.clean_table_rows(), totals_lines=fx.clean_table_totals())
    x0, y_bottom, x1, y_top = info["bbox"]

    # 把上边框沿同一水平线向右延长很远，并在延长段上钉 25 根短竖线刻度——它们的端点都
    # 落在延长线上，flood fill 会顺着延长线把这些刻度全部吸进同一张"表"的网格。
    extension_end = x1 + 2000.0
    msp.add_line((x1, y_top), (extension_end, y_top))
    for i in range(25):
        tick_x = x1 + 50.0 + i * 50.0
        msp.add_line((tick_x, y_top), (tick_x, y_top - 5.0))

    found, findings, gaps, _ = run_pipeline(doc)
    assert len(found) == 1
    t = found[0]
    assert len(t["rows"]) == 0  # 没有吐出垃圾数据行
    assert len(t["columns"]) == 0
    r005 = [g for g in gaps if g["rule_id"] == "R005"]
    assert len(r005) == 1
    assert "异常" in r005[0]["message"]


def test_multi_scale_stray_large_text_does_not_break_normal_table():
    """同一图里混了一处大字号（远大于表格文字）的无关文字，正常表格的识别不应受影响。"""
    doc = fx.new_doc()
    msp = doc.modelspace()
    fx.build_table(msp, rows=fx.clean_table_rows(), totals_lines=fx.clean_table_totals())
    # 远离表格的一处巨大字号无关文字（比如另一张图的大标题），高度是表格文字的 ~20 倍
    msp.add_text("某某工程总平面图", dxfattribs={"height": fx.TEXT_HEIGHT * 20, "insert": (5000.0, 5000.0)})

    found, findings, gaps, _ = run_pipeline(doc)
    assert len(found) == 1
    t = found[0]
    assert len(t["rows"]) == 2
    row1 = next(r for r in t["rows"] if r["parsed"]["mark"] == "1")
    assert abs(row1["parsed"]["weight_kg"] - 22.20) < 1e-6
    assert not any(f["severity"] == "error" for f in findings)


def test_two_side_by_side_tables_same_topline_y_do_not_cross_contaminate():
    """两张同版式表左右并排、顶线在同一 y、间距约 1.3×表宽（对应真实样图的比例）。
    横向匹配容差收紧到 ≤1×标题字高后，各自应该只认领自己下方的网格和自己的
    scope_notes，不串到隔壁表；也不应出现"候选上边框已被占用"的 gap。"""
    doc = fx.new_doc()
    msp = doc.modelspace()
    table_width = len(fx.DEFAULT_HEADERS) * fx.COL_WIDTH
    gap = 1.3 * table_width
    fx.build_table(
        msp, origin=(0.0, 0.0), rows=fx.clean_table_rows(), totals_lines=fx.clean_table_totals(),
        scope_notes=["(左表注释)"],
    )
    fx.build_table(
        msp, origin=(table_width + gap, 0.0), rows=fx.clean_table_rows(), totals_lines=fx.clean_table_totals(),
        scope_notes=["(右表注释)"],
    )

    found, findings, gaps, _ = run_pipeline(doc)
    assert len(found) == 2
    seen_notes = set()
    for t in found:
        assert len(t["rows"]) == 2
        note_texts = tuple(n["text"] for n in t["scope_notes"])
        assert note_texts in (("(左表注释)",), ("(右表注释)",))
        seen_notes.add(note_texts)
    assert seen_notes == {("(左表注释)",), ("(右表注释)",)}  # 各表只看到自己的注释，没有串门
    assert not any("占用" in g["message"] for g in gaps)
    assert not any(f["severity"] == "error" for f in findings)


def test_spec_cell_encoding_variants_parse_to_identical_diameter_and_grade():
    """规格写成 ODA 风格（Ì25）、LibreDWG 的 \\U+XXXX 转义、以及孤立代理项三种形式，
    经归一化后必须解出完全一样的 (直径, 牌号)。"""
    symtab = load_symbol_table()
    variants = ["Ì25", "\\U+00CC25", "\udccc25"]
    results = []
    for raw in variants:
        normalized = extract.normalize_text(raw)
        gaps: list[dict] = []
        d, g, gs = tables_mod._parse_spec_cell(normalized, ["H1"], symtab, gaps)
        assert gaps == []
        results.append((d, g, gs))
    assert len(set(results)) == 1
    diameter, grade, grade_source = results[0]
    assert diameter == 25.0
    assert grade == "HRB400"


def test_diameter_only_symbol_with_zero_never_triggers_r001():
    """直径符号后跟不合理的 0（曾经会被解成 diameter=0.0，R001 用 0kg 当期望值假阳性）
    现在必须变成 diameter=None + gap，R001 对这一行整体跳过。"""
    rows = fx.clean_table_rows()
    rows[0][2] = "Φ0"
    doc = fx.new_doc()
    msp = doc.modelspace()
    fx.build_table(msp, rows=rows, totals_lines=fx.clean_table_totals())

    found, findings, gaps, _ = run_pipeline(doc)
    t = found[0]
    row1 = next(r for r in t["rows"] if r["parsed"]["mark"] == "1")
    assert row1["parsed"]["diameter_mm"] is None
    assert not any(f["rule_id"] == "R001" and f["row_mark"] == "1" for f in findings)
    assert any(g["rule_id"] == "R005" and "标准钢筋公称直径" in g["message"] for g in gaps)


def test_spec_cell_bare_known_grade_literal_not_parsed_as_diameter():
    """规格格子只写了牌号字面量"HRB400"（没有符号编码）——"400"绝不能被当成直径。"""
    rows = fx.clean_table_rows()
    rows[0][2] = "HRB400"
    doc = fx.new_doc()
    msp = doc.modelspace()
    fx.build_table(msp, rows=rows, totals_lines=fx.clean_table_totals())

    found, findings, gaps, _ = run_pipeline(doc)
    t = found[0]
    row1 = next(r for r in t["rows"] if r["parsed"]["mark"] == "1")
    assert row1["parsed"]["grade"] == "HRB400"
    assert row1["parsed"]["diameter_mm"] is None
    assert not any(f["rule_id"] == "R001" and f["row_mark"] == "1" for f in findings)


def test_spec_cell_unknown_grade_literal_logs_gap_not_guessed():
    """形似牌号（H[PR]B+三位数字）但不在已知牌号列表里的（如 HRB300）——记未知牌号 gap，
    原文照录，不猜测归入已知牌号。"""
    rows = fx.clean_table_rows()
    rows[0][2] = "HRB300"
    doc = fx.new_doc()
    msp = doc.modelspace()
    fx.build_table(msp, rows=rows, totals_lines=fx.clean_table_totals())

    found, findings, gaps, _ = run_pipeline(doc)
    t = found[0]
    row1 = next(r for r in t["rows"] if r["parsed"]["mark"] == "1")
    assert row1["parsed"]["grade"] is None
    assert row1["parsed"]["diameter_mm"] is None
    assert any(
        g["rule_id"] == "R005" and "未知牌号" in g["message"] and "HRB300" in g["message"]
        for g in gaps
    )


def test_no_mark_column_totals_row_ends_body_and_subtable_is_flagged():
    """没有编号列的表（比如"位置/规格/单位/数量"构件表）：含"合计"的行视为表体结束，
    声明合计要能从这一行里抓出来；合计之后又出现的类似表头的行判定为未识别子表，
    连同其下面的行都不当数据行、不静默混进本表明细。"""
    doc = fx.new_doc()
    msp = doc.modelspace()
    headers = [["位置"], ["规格"], ["单位"], ["数量"]]
    rows = [
        ["支护", "格栅拱架", "套", "12"],
        ["支护", "钢筋网", "m2", "340"],
        ["合计", "格栅拱架：HRB400,总重797.7Kg", "", ""],
        ["位置", "规格", "单位", "数量"],  # 疑似子表表头
        ["支护", "锚杆", "根", "88"],  # 子表数据，不应混进本表 rows
    ]
    fx.build_table(msp, headers=headers, rows=rows, totals_lines=[])

    found, findings, gaps, _ = run_pipeline(doc)
    assert len(found) == 1
    t = found[0]
    assert len(t["rows"]) == 2  # 只有合计行之前的两行算数据行
    assert [r["cells"][0]["text"] for r in t["rows"]] == ["支护", "支护"]
    decl = t["declared_totals"]
    assert len(decl) == 1
    assert decl[0]["grade"] == "HRB400"
    assert abs(decl[0]["value_kg"] - 797.7) < 1e-6
    subtable_gaps = [g for g in gaps if "未识别子表" in g["message"]]
    assert len(subtable_gaps) == 1
