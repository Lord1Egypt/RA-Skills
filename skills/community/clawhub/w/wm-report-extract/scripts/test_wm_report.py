#!/usr/bin/env python3
"""test_wm_report.py — wm_report.py 纯函数单测（不依赖 docling/pymupdf）。"""
from __future__ import annotations

import json
import re
import contextlib
import io
import tempfile
import unittest
from pathlib import Path

import wm_report as w


class TestEmitMarkdown(unittest.TestCase):
    def test_page_markers_and_stats(self):
        md, pages = w.emit_markdown([
            {"kind": "text", "label": "section_header", "page": 1, "text": "第一章 公司简介"},
            {"kind": "text", "label": "text", "page": 1, "text": "正文段落"},
            {"kind": "table", "label": "table", "page": 2, "text": "| a | b |\n|---|---|\n| 1 | 2 |"},
            {"kind": "picture", "label": "picture", "page": 2, "text": ""},
        ])
        self.assertIn("<!-- page:1 -->", md)
        self.assertIn("<!-- page:2 -->", md)
        self.assertIn("## 第一章 公司简介", md)
        self.assertEqual(len(pages), 2)
        self.assertEqual(pages[0]["headings"], ["第一章 公司简介"])
        self.assertEqual(pages[1]["tables"], 1)
        self.assertEqual(pages[1]["pictures"], 1)

    def test_nfkc_and_header_skip(self):
        md, pages = w.emit_markdown([
            {"kind": "text", "label": "text", "page": 1, "text": "⼈民币"},  # 康熙部首
            {"kind": "text", "label": "page_header", "page": 1, "text": "年度报告"},
        ])
        self.assertIn("人民币", md)
        self.assertNotIn("年度报告", md)

    def test_list_item(self):
        md, _ = w.emit_markdown([
            {"kind": "text", "label": "list_item", "page": 1, "text": "重大风险提示"},
        ])
        self.assertIn("- 重大风险提示", md)


class TestFindChapters(unittest.TestCase):
    def test_jie_and_zhang_variants(self):
        md_lines = [
            "<!-- page:1 -->", "", "## 第一节 释义", "",
            "<!-- page:5 -->", "", "## 第二节 公司简介和主要财务指标", "",
            "<!-- page:20 -->", "", "## 第十节 财务报告", "",
        ]
        ch = w.find_chapters(md_lines)
        self.assertEqual([c["num"] for c in ch], [1, 2, 10])
        self.assertEqual(ch[1]["page"], 5)
        self.assertEqual(ch[1]["page_end"], 20)

    def test_zhang_chapter_and_toc_dedup(self):
        md_lines = [
            "<!-- page:2 -->", "- 10 第一章 公司简介", "- 18 第三章 管理层讨论与分析",
            "<!-- page:10 -->", "", "## 第一章 公司简介", "",
            "<!-- page:18 -->", "", "## 第三章 管理层讨论与分析", "",
        ]
        ch = w.find_chapters(md_lines)
        # 目录行（- 开头）不构成章节标题；正文标题去重
        self.assertEqual([c["num"] for c in ch], [1, 3])
        self.assertEqual(ch[0]["page"], 10)

    def test_kangxi_normalized(self):
        md_lines = ["<!-- page:3 -->", "", "## 第⼗节 财务报告", ""]
        ch = w.find_chapters(md_lines)
        self.assertEqual(len(ch), 1)
        self.assertEqual(ch[0]["title"], "财务报告")

    def test_toc_fallback_when_no_body_headings(self):
        md_lines = [
            "<!-- page:2 -->", "- 10 第一章 公司简介", "- 13 第二章 会计数据和财务指标摘要",
            "<!-- page:12 -->", "1.1 公司简介正文（数字编号版式，无章标题）",
        ]
        ch = w.find_chapters(md_lines)
        self.assertEqual([c["num"] for c in ch], [1, 2])
        self.assertTrue(all(c["source"] == "toc" and c["printed_page"] for c in ch))
        self.assertEqual(ch[0]["page"], 10)


class TestFindSections(unittest.TestCase):
    def test_toc_fallback_flagged(self):
        md_lines = [
            "<!-- page:2 -->", "- 13 第二章 会计数据和财务指标摘要", "",
            "<!-- page:13 -->", "", "## 主要会计数据和财务指标", "",
        ]
        secs = w.find_sections(md_lines)
        kf = [s for s in secs if s["key"] == "key_financials"]
        self.assertEqual(len(kf), 1)
        self.assertEqual(kf[0]["page"], 13)
        self.assertFalse(kf[0]["from_toc"])

    def test_toc_only_hit(self):
        md_lines = ["<!-- page:2 -->", "- 30 第十节 财务报告", "- 45 审计报告"]
        secs = w.find_sections(md_lines)
        audit = [s for s in secs if s["key"] == "audit_report"]
        self.assertEqual(len(audit), 1)
        self.assertTrue(audit[0]["from_toc"])

    def test_statement_heading_anchored(self):
        md_lines = [
            "<!-- page:120 -->", "", "## 合并资产负债表", "（除特别注明外，金额单位：人民币元）",
            "<!-- page:150 -->", "", "## 合并利润表", "",
        ]
        secs = w.find_sections(md_lines)
        keys = {s["key"] for s in secs}
        self.assertIn("balance_sheet", keys)
        self.assertIn("income_stmt", keys)

    def test_outlook_skips_disclaimer_prefers_mda_chapter(self):
        md_lines = [
            "<!-- page:2 -->", "", "## 重要提示",
            "本报告中所涉及的未来计划、发展战略等前瞻性描述不构成公司对投资者的实质承诺,敬请投资者注意投资风险。",
            "## 六、 前瞻性陈述的风险声明",
            "## 十、 重大风险提示",
            "<!-- page:13 -->", "", "## 第三节 董事长致辞", "", "## 未来展望:",
            "<!-- page:15 -->", "", "## 第四节 管理层讨论与分析",
            "## 2. 经营模式",
            "## 二、报告期内公司所处行业情况",
            "<!-- page:16 -->", "", "## 三、经营情况讨论与分析",
            "<!-- page:39 -->", "", "## 六、公司关于公司未来发展的讨论与分析",
            "## 未来展望",
            "## ( 四 ) 可能面对的风险",
            "<!-- page:41 -->", "", "## 第五节 董事会报告",
        ]
        ch = w.find_chapters(md_lines)
        secs = {s["key"]: s for s in w.find_sections(md_lines, ch)}
        self.assertEqual(secs["mda_outlook"]["page"], 39)
        self.assertIn("未来发展", secs["mda_outlook"]["matched"])
        self.assertEqual(secs["risk_factors"]["page"], 39)
        self.assertIn("可能面对的风险", secs["risk_factors"]["matched"])
        self.assertEqual(secs["mda_business"]["page"], 15)
        self.assertEqual(secs["mda_industry"]["page"], 15)
        self.assertEqual(secs["mda_overview"]["page"], 16)

    def test_bank_outlook_prospect_heading_inside_mda(self):
        md_lines = [
            "<!-- page:2 -->",
            "这些陈述是基于现行计划,故不构成本集团的实质承诺,投资者应注意投资风险。",
            "<!-- page:18 -->", "", "## 第三章 管理层讨论与分析",
            "## 3.1 总体经营情况分析",
            "<!-- page:67 -->", "", "## 3.13 前景展望与应对措施",
            "<!-- page:70 -->", "", "## 第四章 环境、社会与治理",
        ]
        ch = w.find_chapters(md_lines)
        secs = {s["key"]: s for s in w.find_sections(md_lines, ch)}
        self.assertEqual(secs["mda_outlook"]["page"], 67)
        self.assertIn("前景展望", secs["mda_outlook"]["matched"])
        self.assertEqual(secs["mda_overview"]["page"], 18)


class TestFindTables(unittest.TestCase):
    def test_signature_and_structural_typing(self):
        key_fin = "\n".join([
            "| （人民币百万元） | 2025年 | 增减(%) |",
            "|---|---|---|",
            "| 营业收入 | 100 | 5 |",
            "| 基本每股收益 | 1.2 | 3 |",
        ])
        bal = "\n".join([  # 银行版资产负债表：无货币资金行，靠结构性判定（资产总计+负债合计）
            "| 项目 | 期末 | 期初 |",
            "|---|---|---|",
            "| 现金及存放中央银行款项 | 1 | 2 |",
            "| 资产总计 | 99 | 88 |",
            "| 负债合计 | 90 | 80 |",
        ])
        md_lines = ("<!-- page:10 -->\n\n" + key_fin + "\n\n<!-- page:20 -->\n\n" + bal).split("\n")
        tables = w.find_tables(md_lines)
        self.assertEqual([t["type"] for t in tables], ["key_financials", "balance_sheet"])
        self.assertEqual(tables[0]["page"], 10)
        self.assertEqual(tables[1]["page"], 20)
        # schema 解析
        self.assertEqual(tables[1]["sample_labels"], ["现金及存放中央银行款项", "资产总计", "负债合计"])
        self.assertIn("期末", tables[1]["periods"].values())

    def test_manufacturing_balance_sheet_structural(self):
        bal = "\n".join([
            "| 项目 | 附注 | 期末余额 | 期初余额 |",
            "|---|---|---|---|",
            "| 货币资金 | 六、1 | 100 | 90 |",
            "| 资产总计 | | 900 | 800 |",
            "| 负债和所有者权益总计 | | 900 | 800 |",
        ])
        md_lines = ("<!-- page:80 -->\n\n" + bal).split("\n")
        tables = w.find_tables(md_lines)
        self.assertEqual(tables[0]["type"], "balance_sheet")  # 负债和所有者权益总计 也是结构证据

    def test_variance_reasons_and_segments_and_ratios(self):
        expense = "\n".join([
            "| 项目名称 | 2025 年度 | 2024 年度 | 变动幅度 | 原因说明 |",
            "|---|---|---|---|---|",
            "| 销售费用 | 11,273 | 7,832 | 43.93 | 主要系报告期公司加速构建直连用户的新渠道模式所致 |",
            "| 财务费用 | -1,969 | 99 | -2083.65 | 主要系报告期内汇兑收益增加所致 |",
        ])
        asset = "\n".join([
            "| 项目名称 | 本期期末数 | 变动比例 | 情况说明 |",
            "|---|---|---|---|",
            "| 长期借款 | 1,068 | -83.63 | 长期借款变动主要系报告期偿还银行长期借款所致 |",
        ])
        seg = "\n".join([
            "| 分地区 | 营业收入 | 营业成本 | 毛利率 ( % ) |",
            "|---|---|---|---|",
            "| 国内 | 128,467 | 104,562 | 18.61 |",
            "| 国外 | 91,488 | 76,210 | 16.70 |",
        ])
        ratios = "\n".join([
            "| 项目 | 2025 | 2024 |",
            "|---|---|---|",
            "| 毛利率 (%) | 18.04 | 19.51 |",
            "| 销售费用占营业收入比例 (%) | 5.06 | 3.87 |",
        ])
        prod = "\n".join([
            "| 主要产品 | 单位 | 生产量 | 销售量 | 库存量 |",
            "|---|---|---|---|---|",
            "| SUV | 辆 | 958,920 | 1,033,097 | 80,775 |",
        ])
        md_lines = (
            "<!-- page:16 -->\n\n" + ratios
            + "\n\n<!-- page:28 -->\n\n" + seg
            + "\n\n" + prod
            + "\n\n<!-- page:31 -->\n\n" + expense
            + "\n\n<!-- page:33 -->\n\n" + asset
        ).split("\n")
        tables = w.find_tables(md_lines)
        types = [t["type"] for t in tables]
        self.assertEqual(types, ["mda_ratios", "segments", "production_sales", "variance_reasons", "variance_reasons"])
        recs = w.build_records(md_lines, tables)
        by_label = {r["label_norm"]: r for r in recs if r.get("type") == "variance_reasons"}
        sell = by_label["销售费用"]
        reason = next(v["value"] for v in sell["values"] if "原因" in (v.get("header") or ""))
        self.assertIn("直连用户", reason)
        yoy = next(v["value"] for v in sell["values"] if "变动" in (v.get("header") or ""))
        self.assertEqual(yoy, "43.93")
        region = [r for r in recs if r.get("type") == "segments"]
        labels = {r["label_norm"] for r in region}
        self.assertIn("国内", labels)
        self.assertIn("国外", labels)

    def test_build_records_tolerates_empty_first_column(self):
        # fitz 长格报表首列空、科目在 col1——不得整行丢弃（地产年报三大报表实证）
        md = "\n".join([
            "<!-- page:152 -->", "",
            "|  |  |  | 附注 |  | 本年年末余额 |  | 上年年末余额 |",
            "|---|---|---|---|---|---|---|---|",
            "|  | 货币资金 |  | (五)1 |  | 67,240,949,734.90 |  | 88,162,865,022.03 |",
            "|  | 交易性金融资产 |  | (五)2 |  | 68,016,700.87 |  | 51,200,000.00 |",
            "|  | 资产总计 |  |  |  | 1,500,000,000,000 |  | 1,400,000,000,000 |",
        ]).split("\n")
        tables = [{"index": 0, "page": 152, "line": 2, "line_end": 6,
                   "type": "balance_sheet", "rows": 3}]
        recs = w.build_records(md, tables)
        labels = {r["label_norm"] for r in recs}
        self.assertIn("货币资金", labels)
        self.assertIn("资产总计", labels)
        cash = next(r for r in recs if r["label_norm"] == "货币资金")
        vals = [v["value"] for v in cash["values"]]
        self.assertIn("67,240,949,734.90", vals)

    def test_variance_signature_does_not_steal_income_stmt(self):
        inc = "\n".join([
            "| 项目 | 2025 年度 | 2024 年度 |",
            "|---|---|---|",
            "| 营业收入 | 100 | 90 |",
            "| 净利润 | 10 | 12 |",
        ])
        md_lines = ("<!-- page:140 -->\n\n" + inc).split("\n")
        tables = w.find_tables(md_lines)
        self.assertEqual(tables[0]["type"], "income_stmt")

    def test_synonym_expansion(self):
        vs = w.expand_need_keywords("股东权益合计")
        self.assertIn("所有者权益合计", vs)
        self.assertIn("归属于母公司股东的净利润", w.expand_need_keywords("归属于上市公司股东的净利润"))
        self.assertIn("资产总计", w.expand_need_keywords("资产合计"))
        # 原简繁变体不受迁移影响
        self.assertIn("存貨", w.expand_need_keywords("存货"))

    def test_continued_table_merge(self):
        part1 = "\n".join([
            "| 科目 | 2025 | 2024 |",
            "|---|---|---|",
            "| 营业收入 | 1 | 2 |",
        ])
        part2 = "\n".join([  # 次页续表：同列数、空壳表头
            "| | | |",
            "|---|---|---|",
            "| 净利润 | 3 | 4 |",
        ])
        md_lines = ("<!-- page:10 -->\n\n" + part1 + "\n\n<!-- page:11 -->\n\n" + part2).split("\n")
        tables = w.find_tables(md_lines)
        self.assertEqual(len(tables), 2)
        self.assertTrue(tables[1].get("continued"))
        self.assertEqual(tables[0].get("continued_by"), [1])

    def test_clean_header_new_table_not_merged_as_continuation(self):
        # 恒瑞附表3→附表4/5：同列数、页距 1、前表长——前片表头是「列名+数据」粘连长格（fitz），
        # 本片带纯列名干净表头 → 同构新表，不得并入
        part1 = "\n".join([
            "| 报告期进展NDA受理 (15项) | 药品名称/代号舒地胰岛素 | 靶点胰岛素 | 单药/联合 |",
            "|---|---|---|---|",
        ] + [f"| 报告期进展NDA受理 (15项) | 药{i}号yyy | PD-L{i} | II 期 |" for i in range(16)])
        part2 = "\n".join([
            "| 治疗领域 | 药品名称 | 靶点 | 阶段 |",
            "|---|---|---|---|",
            "| 肿瘤 | 新药A | T1 | III 期 |",
        ])
        # 间隔文本带「后续」字样（附表4 标题词）——单字「续」曾误触发续表合并
        between = "附表4-已上市创新药后续主要临床研发管线(截至2026年2月28日)"
        md_lines = ("<!-- page:28 -->\n\n" + part1 + "\n\n" + between + "\n\n"
                    + "<!-- page:29 -->\n\n" + part2).split("\n")
        tables = w.find_tables(md_lines)
        self.assertFalse(tables[1].get("continued"))

    def test_explicit_continuation_marker_still_merges(self):
        # 「（续）」标记的续表不受收紧影响
        part1 = "\n".join([
            "| 科目 | 2025 | 2024 | 备注 |",
            "|---|---|---|---|",
            "| 营业收入 | 1 | 2 | x |",
        ])
        part2 = "\n".join([
            "| 净利润 | 3 | 4 | y |",
            "|---|---|---|---|",
            "| 扣非净利润 | 5 | 6 | z |",
        ])
        md_lines = ("<!-- page:10 -->\n\n" + part1 + "\n\n合并资产负债表（续）\n\n<!-- page:11 -->\n\n"
                    + part2).split("\n")
        tables = w.find_tables(md_lines)
        self.assertTrue(tables[1].get("continued"))

    def test_fragment_detection(self):
        frag = "| a |\n|---|\n| 1 |"
        md_lines = ("<!-- page:5 -->\n\n" + frag).split("\n")
        tables = w.find_tables(md_lines)
        self.assertEqual(tables[0]["cols"], 1)


class TestIndustryHint(unittest.TestCase):
    def test_bank(self):
        h = w.detect_industry("吸收存款 1000 发放贷款和垫款 资本充足率 不良贷款率 净息差 拨备覆盖率 客户存款")
        self.assertEqual(h["industry"], "bank")
        self.assertGreaterEqual(h["confidence"], 0.7)

    def test_building_materials(self):
        # 北新样式：品类词多词共现 + 标题「建材」——稳压财务公司附注带来的 bank 弱命中
        h = w.detect_industry(
            "石膏板销量全球第一 轻钢龙骨 防水卷材 防水材料 防水工程 涂料 玻璃纤维 家装渠道 "
            "吸收存款 发放贷款和垫款 客户存款 客户贷款",
            title="北新建材2025年报")
        self.assertEqual(h["industry"], "building_materials")

    def test_machinery(self):
        # 盾安样式：制冷设备 6 词共现压过 automobile 的热管理弱命中（新能源/汽车/整车）
        h = w.detect_industry(
            "制冷元器件全球领先 阀件 压缩机 换热器 冷水机组 冷链 新能源 汽车 整车 销量",
            title="盾安环境:2025年年度报告")
        self.assertEqual(h["industry"], "machinery")

    def test_automobile_traditional_chinese(self):
        # 港股繁体招股书：automobile 简繁并收后整车厂不再被智驾宣传词误判 auto_electronics
        h = w.detect_industry(
            "汽車銷量 整車 乘用車 新能源 分車型 發動機 自動駕駛 輔助駕駛 智能駕駛 域控 ADAS",
            title="奇瑞汽车全球發售招股章程")
        self.assertEqual(h["industry"], "automobile")

    def test_bank_shortdoc_financial_company_note_cleanup(self):
        # 季报（短文档）：集团财务公司附注的存贷款词不得把非金融公司判成 bank
        h = w.detect_industry("货币资金 应收账款 客户存款 客户贷款 吸收存款 发放贷款和垫款",
                              title="北新建材2026年一季度报告", pages=20)
        self.assertNotEqual(h["industry"], "bank")

    def test_low_confidence_returns_none(self):
        # 单个弱词命中（季报仅「合同负债」）不得输出误导行业标签
        h = w.detect_industry("营业收入 合同负债 货币资金", title="宇通客车:2026年第一季度报告", pages=12)
        self.assertIsNone(h["industry"])

    def test_bank_type_hints(self):
        md = "\n".join([
            "<!-- page:40 -->",
            "| 指标 | 核心一级资本充足率 | 资本充足率 |",
            "|---|---|---|",
            "| 本行 | 13% | 16% |",
            "<!-- page:41 -->",
            "| 指标 | 不良贷款率 | 拨备覆盖率 |",
            "|---|---|---|",
            "| 本行 | 0.9% | 400% |",
            "<!-- page:42 -->",
            "| 指标 | 净息差 | 净利差 |",
            "|---|---|---|",
            "| 本行 | 2.0% | 2.1% |",
            "<!-- page:43 -->",
            "| 项目 | 吸收存款 | 发放贷款和垫款 |",
            "|---|---|---|",
            "| 余额 | 1000 | 800 |",
        ]).split("\n")
        hints = {t.get("type_hint") for t in w.find_tables(md)}
        self.assertTrue(
            {"capital_adequacy", "asset_quality", "nim_spread", "deposit_loan"} <= hints
        )

    def test_bank_annual_narratives_and_required_gaps(self):
        with tempfile.TemporaryDirectory() as td:
            import os
            os.environ[w.CACHE_ENV] = td
            try:
                sha = "bankannual01"
                d = w.entry_dir(sha)
                d.mkdir(parents=True, exist_ok=True)
                meta = {
                    "source": {"title": "某银行股份有限公司2025年年度报告"},
                    "filing_kind": "annual",
                    "industry_hint": {"industry": "bank"},
                    "doc": {"pages": 300},
                    "tables": [],
                }
                (d / "meta.json").write_text(json.dumps(meta, ensure_ascii=False), encoding="utf-8")
                (d / "records.json").write_text(json.dumps([{
                    "table": 0, "page": 1, "type": "key_financials", "row_label": "营业收入",
                    "values": [{"col": 1, "value": "100", "header": "本期"}],
                }], ensure_ascii=False), encoding="utf-8")
                w.materialize_tables(sha, out_name="result-BANK", force=True)
                narr = w.read_json(d / "result-BANK" / "manifest.json", {}).get("catalog", {}).get("narratives", [])
                ids = {n["id"] for n in narr if n.get("group") == "X_bank"}
                self.assertEqual(ids, {"nim_drivers"})
                gaps = w.read_json(d / "result-BANK" / "gaps.json", [])
                gap_ids = {g["id"] for g in gaps if g.get("status") == "required"}
                self.assertTrue({"cost_income_ratio", "retail_aum"} <= gap_ids)
            finally:
                os.environ.pop(w.CACHE_ENV, None)

    def test_narrative_kpi_gate_flags_found_without_quote(self):
        with tempfile.TemporaryDirectory() as td:
            rd = Path(td) / "result-N"
            (rd / "narratives").mkdir(parents=True)
            bad = {
                "narrative_id": "power_price",
                "bullets": [
                    {"label": "电价", "text": "上涨", "status": "found", "quote": "", "page": None},
                    {"label": "未披露项", "status": "not_disclosed"},
                ],
            }
            (rd / "narratives" / "power_price.json").write_text(
                json.dumps(bad, ensure_ascii=False), encoding="utf-8"
            )
            findings = w.validate_narrative_kpi_gate(rd)
            self.assertTrue(any(f.get("reason") == "narrative_kpi_gate" for f in findings))
            good_dir = Path(td) / "result-G"
            (good_dir / "narratives").mkdir(parents=True)
            good = {
                "narrative_id": "power_price",
                "bullets": [
                    {"label": "电价", "text": "上涨", "status": "found",
                     "quote": "平均上网电价 0.3 元/千瓦时", "page": 18},
                ],
            }
            (good_dir / "narratives" / "power_price.json").write_text(
                json.dumps(good, ensure_ascii=False), encoding="utf-8"
            )
            self.assertEqual(w.validate_narrative_kpi_gate(good_dir), [])

    def test_automobile_beats_generic(self):
        h = w.detect_industry("整车产量 分车型销量 新能源 汽车 皮卡 研发投入 产销量")
        self.assertEqual(h["industry"], "automobile")

    def test_quarter_title_beats_bank_noise(self):
        text = "吸收存款 发放贷款和垫款 资本充足率 客户存款"
        h = w.detect_industry(
            text,
            title="长城汽车:长城汽车股份有限公司2026年第一季度报告",
            pages=15,
        )
        self.assertEqual(h["industry"], "automobile")

    def test_gh_table_signatures(self):
        exec_tbl = "\n".join([
            "| 姓名 | 职务 | 性别 | 年龄 | 任期 | 报酬（万元） |",
            "|---|---|---|---|---|---|",
            "| 张三 | 董事长 | 男 | 55 | 2023-2026 | 120 |",
        ])
        rd_tbl = "\n".join([
            "| 项目 | 2025年度 | 2024年度 | 变动幅度 |",
            "|---|---|---|---|",
            "| 研发投入 | 5,000 | 4,000 | 25.00 |",
            "| 研发投入占营业收入比例(%) | 4.5 | 4.0 | 0.5 |",
        ])
        md_lines = ("<!-- page:50 -->\n\n" + exec_tbl + "\n\n<!-- page:60 -->\n\n" + rd_tbl).split("\n")
        tables = w.find_tables(md_lines)
        types = [t["type"] for t in tables]
        self.assertIn("executives", types)
        rd = [t for t in tables if "研发投入" in " ".join(t.get("sample_labels") or [])]
        self.assertTrue(rd)
        self.assertIsNone(rd[0]["type"])
        self.assertEqual(rd[0].get("type_hint"), "rd_investment")

    def test_meeting_minutes_not_equity_incentive(self):
        meeting = "\n".join([
            "| 会议 | 召开日期 | 审议事项 |",
            "|---|---|---|",
            "| 第八届监事会第九次会议 | 2024 年 1 月 19 日 | 审议通过关于 2023 年限制性股票激励计划与股票期权激励计划的议案 |",
        ])
        md_lines = ("<!-- page:49 -->\n\n" + meeting).split("\n")
        tables = w.find_tables(md_lines)
        self.assertIsNone(tables[0]["type"])
        self.assertNotEqual(tables[0].get("type_hint"), "equity_incentive")

    def test_subsidiary_table_not_income_stmt(self):
        sub = "\n".join([
            "| 公司名称 | 业务性质 | 注册资本 | 持股比例 ( % ) | 本年营业收入 | 本年净利润 |",
            "|---|---|---|---|---|---|",
            "| 某零部件公司 | 汽车零部件制造 | 100 | 100 | 8,447 | 1,726 |",
        ])
        md_lines = ("<!-- page:39 -->\n\n" + sub).split("\n")
        tables = w.find_tables(md_lines)
        self.assertNotEqual(tables[0]["type"], "income_stmt")

    def test_entity_kpi_wide_table_not_income_stmt(self):
        """主体列 × 本期发生额营业收入/净利润 列式不得定型为利润表（泛化，虚构主体）。"""
        wide = "\n".join([
            "| 子公司名称 | 本期发生额营业收入 | 本期发生额净利润 | 本期发生额综合收益总额 |",
            "|---|---|---|---|",
            "| 甲乙丙科技股份有限公司 | 1,000.00 | 100.00 | 100.00 |",
        ])
        md_lines = ("<!-- page:200 -->\n\n" + wide).split("\n")
        tables = w.find_tables(md_lines)
        self.assertNotEqual(tables[0].get("type"), "income_stmt")

    def test_subsidiary_name_rows_not_income_stmt(self):
        """行首为『子公司名称』+ 实体名单，即使表体含营业收入/净利润也不得定型利润表。"""
        body = "\n".join([
            "| | 2025 年度 | 2024 年度 |",
            "|---|---|---|",
            "| 子公司名称 | 营业收入 | 营业收入 |",
            "| 准格尔能源 | 100 | 90 |",
            "| 宝日希勒能源 | 80 | 70 |",
            "| 净利润合计 | 10 | 9 |",
        ])
        typ, _, _ = w.infer_table_type(
            body, title="", headers=["", "2025 年度", "2024 年度"],
            sample_labels=["子公司名称", "准格尔能源", "宝日希勒能源"],
        )
        self.assertNotEqual(typ, "income_stmt")

    def test_financial_indicator_mash_not_income_stmt(self):
        """『表2 财务指标』摘要表头堆砌营收/净利润，不得 STRUCTURAL 定型利润表。"""
        hdr = ("表2 财务指标2024年 变化 2025年 营业收入 百万元 294,916 "
               "利润总额 百万元 79,339 归属于本公司股东的净利润 百万元 52,849")
        typ, _, _ = w.infer_table_type(
            f"| {hdr} |\n|---|",
            title="",
            headers=[hdr],
            sample_labels=["表2 财务指标"],
        )
        self.assertNotEqual(typ, "income_stmt")

    def test_title_anchored_cashflow_investing_continuation(self):
        """现金流量表续页仅有投资/筹资活动行时仍可标题锚定定型。"""
        typ, _, hint = w.infer_table_type(
            "| 项目 | 本期 |\n| 二、投资活动产生的现金流量 | |\n| 收回投资收到的现金 | 1 |\n",
            title="合并现金流量表 ( 续 )",
            headers=["项目", "本期"],
            sample_labels=["二、投资活动产生的现金流量", "收回投资收到的现金"],
        )
        self.assertEqual(typ, "cashflow_stmt")
        self.assertIsNone(hint)
    def test_title_anchored_income_fragment_without_net_profit(self):
        """标题为合并利润表且有营业总收入行，即使本片无净利润也可定型。"""
        frag = "\n".join([
            "| 项目 | 2025 年度 | 2024 年度 |",
            "|---|---|---|",
            "| 一、营业总收入 | 100 | 90 |",
            "| 其中:营业收入 | 100 | 90 |",
            "| 利息收入 | 0.00 | 0.00 |",
            "| 已赚保费 | 0.00 | 0.00 |",
            "| 二、营业总成本 | 80 | 70 |",
        ])
        md_lines = ("<!-- page:90 -->\n\n## 3、合并利润表\n\n" + frag).split("\n")
        tables = w.find_tables(md_lines)
        self.assertEqual(tables[0].get("type"), "income_stmt")
        self.assertNotEqual(tables[0].get("type_hint"), "claims_payout")

    def test_cas_income_template_not_claims_hint(self):
        typ, _, hint = w.infer_table_type(
            "| 项目 | 本期 |\n| 一、营业总收入 | 1 |\n| 赔付支出净额 | 0 |\n| 退保金 | 0 |\n",
            title="合并利润表",
            headers=["项目", "本期"],
            sample_labels=["一、营业总收入", "赔付支出净额", "退保金"],
        )
        self.assertEqual(typ, "income_stmt")
        self.assertIsNone(hint)

    def test_title_anchored_cashflow_variant_without_net_amount(self):
        """标题为现金流量表；行文无「净额」且含空格/斜杠变体时仍定型，且不 hint 存贷款。"""
        frag = "\n".join([
            "| 项目 | 2025 年度 | 2024 年度 |",
            "|---|---|---|",
            "| 一、经营活动产生 /( 使用 ) 的现金流量 | | |",
            "| 销售商品、提供劳务收到的现金 | 100 | 90 |",
            "| 发放贷款及垫款净减少额 | 0.00 | 0.00 |",
            "| 吸收存款和同业存放款项净增加额 | 0.00 | 0.00 |",
            "| 二、投资活动产生的现金流量 | | |",
            "| 三、筹资活动产生的现金流量 | | |",
        ])
        md_lines = ("<!-- page:137 -->\n\n## 合并现金流量表\n\n" + frag).split("\n")
        tables = w.find_tables(md_lines)
        self.assertEqual(tables[0].get("type"), "cashflow_stmt")
        self.assertNotEqual(tables[0].get("type_hint"), "deposit_loan")

    def test_cas_cashflow_template_not_deposit_hint(self):
        typ, _, hint = w.infer_table_type(
            "| 项目 | 本期 |\n| 一、经营活动产生/(使用)的现金流量 | |\n"
            "| 销售商品、提供劳务收到的现金 | 1 |\n"
            "| 发放贷款及垫款净减少额 | 0 |\n| 投资活动 | |\n| 筹资活动 | |\n",
            title="合并及公司现金流量表",
            headers=["项目", "本期"],
            sample_labels=[
                "一、经营活动产生 /( 使用 ) 的现金流量",
                "销售商品、提供劳务收到的现金",
                "发放贷款及垫款净减少额",
                "投资活动产生的现金流量",
                "筹资活动产生的现金流量",
            ],
        )
        self.assertEqual(typ, "cashflow_stmt")
        self.assertIsNone(hint)

    def test_furniture_title_does_not_block_income_stmt(self):
        """签字行当 nearby_title 时，仍可按科目结构定型利润表。"""
        body = "\n".join([
            "| 项目 | 本期金额 | 上期金额 |",
            "|---|---|---|",
            "| 一、营业总收入 | 100 | 90 |",
            "| 其中:营业收入 | 100 | 90 |",
            "| 二、营业总成本 | 80 | 70 |",
            "| 三、营业利润(亏损以“—”号填列) | 20 | 20 |",
            "| 四、利润总额(亏损总额以“—”号填列) | 20 | 20 |",
            "| 五、净利润(净亏损以“—”号填列) | 15 | 15 |",
        ])
        typ, _, hint = w.infer_table_type(
            body,
            title="会计机构负责人:张三",
            headers=["项目", "本期金额", "上期金额"],
            sample_labels=["一、营业总收入", "二、营业总成本", "五、净利润(净亏损以“—”号填列)"],
        )
        self.assertEqual(typ, "income_stmt")
        self.assertIsNone(hint)

    def test_income_stmt_subject_continuation_across_pages(self):
        """利润表科目序跨页粘链：首片营业总收入 + 次片税金及附加/净利润。"""
        p1 = "\n".join([
            "| 项目 | 本期 | 上期 |",
            "|---|---|---|",
            "| 一、营业总收入 | 100 | 90 |",
            "| 其中:营业收入 | 100 | 90 |",
            "| 二、营业总成本 | 80 | 70 |",
        ])
        p2 = "\n".join([
            "| 项目 | 本期 | 上期 |",
            "|---|---|---|",
            "| 税金及附加 | 1 | 1 |",
            "| 销售费用 | 2 | 2 |",
            "| 五、净利润(净亏损以“-”号填列) | 10 | 9 |",
        ])
        md_lines = (
            "<!-- page:10 -->\n\n## 合并利润表\n\n" + p1
            + "\n\n<!-- page:11 -->\n\n" + p2
        ).split("\n")
        tables = w.find_tables(md_lines)
        self.assertGreaterEqual(len(tables), 2)
        head = next(t for t in tables if not t.get("continued"))
        self.assertEqual(head.get("type"), "income_stmt")
        self.assertTrue(head.get("continued_by"))

    def test_variance_prior_not_pct_column(self):
        asset = "\n".join([
            "| 项目名称 | 本期期末数 | 占总资产比例(%) | 变动比例 | 情况说明 |",
            "|---|---|---|---|---|",
            "| 交易性金融资产 | 14,181,400,741.40 | 6.53 | 244.85 | 主要系购买理财产品增加 |",
        ])
        md_lines = ("<!-- page:32 -->\n\n" + asset).split("\n")
        tables = w.find_tables(md_lines)
        recs = w.build_records(md_lines, tables)
        row = w._build_variance_row(recs[0])
        self.assertEqual(row["value_current"], "14,181,400,741.40")
        self.assertNotEqual(row["value_prior"], "6.53")
        self.assertEqual(row["yoy_pct"], "244.85")

    def test_variance_signature_does_not_steal_rd_table(self):
        rd = "\n".join([
            "| 项目 | 2025 年度 | 2024 年度 | 变动幅度 | 原因说明 |",
            "|---|---|---|---|---|",
            "| 研发投入 | 100 | 90 | 11.11 | 主要系加大新技术投入 |",
        ])
        md_lines = ("<!-- page:20 -->\n\n" + rd).split("\n")
        tables = w.find_tables(md_lines)
        self.assertEqual(tables[0]["type"], "variance_reasons")

    def test_infer_filing_kind(self):
        self.assertEqual(w.infer_filing_kind({"title": "2026年第一季度报告"}, 15), "q1")
        self.assertEqual(w.infer_filing_kind({"title": "北新建材2026一季报"}, 15), "q1")
        self.assertEqual(w.infer_filing_kind({"title": "2026年第三季度报告"}, 25), "q3")
        self.assertEqual(w.infer_filing_kind({"title": "某某2026三季报"}, 20), "q3")
        self.assertEqual(w.infer_filing_kind({"title": "2026年第二季度报告"}, 25), "quarter")
        self.assertEqual(w.infer_filing_kind({"title": "2024年年度报告"}, 330), "annual")
        # 港股（0.6.0）：招股书 prospectus / 繁体中期报告 semi / 本地 convert 无 title 走正文头部兜底
        self.assertEqual(w.infer_filing_kind({"title": "全球發售"}, 701), "prospectus")
        self.assertEqual(w.infer_filing_kind({"title": "2025中期報告"}, 94), "semi")
        self.assertEqual(w.infer_filing_kind({"title": "吉利汽车 2026年中期业绩"}, 74), "semi")
        self.assertEqual(w.infer_filing_kind({"title": "截至2026年6月30日止六个月中期业绩公告"}, 28), "semi")
        self.assertEqual(w.infer_filing_kind({}, 701, "地平線機器人 全球發售 聯席保薦人 發售價"), "prospectus")
        self.assertEqual(w.infer_filing_kind({}, 94, "2025 中期報告 簡明合併財務報表"), "semi")
        self.assertEqual(w.infer_filing_kind({}, 248, "2025 年報 合併損益表"), "annual")

    def test_hk_statement_signatures(self):
        # 港式 IFRS 报表定型（地平线年报实测措辞）
        typ, _, _ = w.infer_table_type(
            "", title="合併損益表", headers=["附註", "2025年 人民幣千元"],
            sample_labels=["來自客戶合同的收入", "毛利", "年內虧損"])
        self.assertEqual(typ, "income_stmt")
        typ, _, _ = w.infer_table_type(
            "", title="合併財務狀況表", headers=["附註", "2025年 人民幣千元"],
            sample_labels=["物業、廠房及設備", "資產總值", "負債總額", "權益總額"])
        self.assertEqual(typ, "balance_sheet")
        typ, _, _ = w.infer_table_type(
            "", title="合併現金流量表", headers=["附註", "2025年 人民幣千元"],
            sample_labels=["經營活動產生的現金流量", "投資活動", "融資活動"])
        self.assertEqual(typ, "cashflow_stmt")

    def test_hk_dual_caption_income(self):
        # 港式双写法「年內 (虧損) ╱利潤」：正负号跨期翻转时利润行以斜杠双写
        typ, _, _ = w.infer_table_type(
            "| 年內 (虧損) ╱利潤 | | (10,469,366) | 2,346,508 |\n| 年內全面 (虧損) ╱收益總額 | | (10,464,177) | 2,074,644 |",
            title="合併損益表", headers=["附註", "2025年 人民幣千元"],
            sample_labels=["來自客戶合同的收入"])
        self.assertEqual(typ, "income_stmt")
        # 反序双写法「年內利潤╱ (虧損)」（盈利年，利润在前）
        typ, _, _ = w.infer_table_type(
            "| 年內利潤╱ (虧損) | | 2,346,508 | (6,739,053) |",
            title="合併損益表", headers=["附註", "2024年 人民幣千元"],
            sample_labels=["來自客戶合同的收入"])
        self.assertEqual(typ, "income_stmt")

    def test_auto_electronics_industry(self):
        # 智驾方案商：汽车/新能源属客户语境词，专属词（ADAS/域控/流片/SoC/車規…）须胜出
        supplier = ("我們的自動駕駛及輔助駕駛解決方案 域控制器 ADAS 車規級 處理硬件 流片 "
                    "算力 SoC 智能駕駛 智能汽車解決方案 汽车 新能源 销量")
        out = w.detect_industry(supplier)
        self.assertEqual(out["industry"], "auto_electronics")
        # 整车厂：整车专属词（整车/分车型/皮卡）≥2 时反向压制 auto_electronics
        oem = "整车 分车型 新能源 销量 汽车 皮卡 自动驾驶 智能驾驶 ADAS 算力 车规"
        out = w.detect_industry(oem)
        self.assertEqual(out["industry"], "automobile")

    def test_quarter_narratives_not_applicable(self):
        with tempfile.TemporaryDirectory() as td:
            import os

            os.environ[w.CACHE_ENV] = td
            try:
                sha = "q1test123456"
                d = w.entry_dir(sha)
                d.mkdir(parents=True, exist_ok=True)
                meta = {
                    "source": {"title": "某公司2026年第一季度报告", "report_date": "2026-03-31"},
                    "filing_kind": "q1",
                    "industry_hint": {"industry": "automobile"},
                    "doc": {"pages": 15},
                    "tables": [],
                }
                (d / "meta.json").write_text(json.dumps(meta, ensure_ascii=False), encoding="utf-8")
                (d / "records.json").write_text(json.dumps([{
                    "table": 0, "page": 1, "type": "key_financials", "row_label": "营业收入",
                    "values": [{"col": 1, "value": "100", "header": "本期"}],
                }], ensure_ascii=False), encoding="utf-8")
                w.materialize_tables(sha, out_name="result-Q1", force=True)
                gaps = w.read_json(d / "result-Q1" / "gaps.json", [])
                mda_gaps = [g for g in gaps if g.get("group") == "D_mda"]
                self.assertTrue(mda_gaps)
                self.assertTrue(all(g["status"] == "not_applicable" for g in mda_gaps))
                narr = w.read_json(d / "result-Q1" / "manifest.json", {}).get("catalog", {}).get("narratives", [])
                auto_narr = [n for n in narr if n.get("group") == "X_automobile"]
                self.assertEqual(auto_narr, [])
            finally:
                os.environ.pop(w.CACHE_ENV, None)

    def test_current_quarter_keeps_pending_narratives(self):
        with tempfile.TemporaryDirectory() as td:
            import os

            os.environ[w.CACHE_ENV] = td
            try:
                sha = "q2test123456"
                d = w.entry_dir(sha)
                d.mkdir(parents=True, exist_ok=True)
                meta = {
                    "source": {"title": "某公司2026年第二季度报告", "report_date": "2026-06-30"},
                    "filing_kind": "quarter",
                    "industry_hint": {"industry": "nonferrous"},
                    "doc": {"pages": 28},
                    "tables": [],
                }
                (d / "meta.json").write_text(json.dumps(meta, ensure_ascii=False), encoding="utf-8")
                (d / "records.json").write_text(json.dumps([{
                    "table": 0, "page": 1, "type": "key_financials", "row_label": "营业收入",
                    "values": [{"col": 1, "value": "100", "header": "本期"}],
                }], ensure_ascii=False), encoding="utf-8")
                w.materialize_tables(sha, out_name="result-Q2", force=True)
                gaps = w.read_json(d / "result-Q2" / "gaps.json", [])
                mda_gaps = [g for g in gaps if g.get("group") == "D_mda"]
                self.assertTrue(mda_gaps)
                self.assertTrue(all(g["status"] == "pending" for g in mda_gaps))
                narr = w.read_json(d / "result-Q2" / "manifest.json", {}).get("catalog", {}).get("narratives", [])
                nf_ids = {n["id"] for n in narr if n.get("group") == "X_nonferrous"}
                self.assertEqual(nf_ids, {"project_progress", "unit_cost"})
            finally:
                os.environ.pop(w.CACHE_ENV, None)

    def test_build_meta_includes_document_profile(self):
        md_text = "\n".join([
            "<!-- page:1 -->",
            "## 2025中期報告",
            "## 合併財務狀況表",
            "| 項目 | 2025年 | 2024年 |",
            "|---|---|---|",
            "| 資產總值 | 100 | 90 |",
        ])
        meta = w.build_meta(
            "metaprofile1",
            md_text,
            [{"page": 1, "line_start": 0, "line_end": 5, "chars": 40, "headings": [], "tables": 1, "pictures": 0}],
            {"pdf": {"pages": 1}},
            {"title": "某公司2025中期報告"},
        )
        profile = meta.get("document_profile") or {}
        self.assertEqual(profile.get("market"), "hk")
        self.assertEqual(profile.get("script"), "zh_hant")
        self.assertEqual(profile.get("accounting"), "ifrs_hk")
        self.assertEqual(profile.get("filing_kind"), "semi")
        self.assertIn("convert_health", profile)

    def test_adapt_plan_null_industry_stays_base_only(self):
        with tempfile.TemporaryDirectory() as td:
            import os

            os.environ[w.CACHE_ENV] = td
            try:
                sha = "adaptnull1234"
                d = w.entry_dir(sha)
                d.mkdir(parents=True, exist_ok=True)
                meta = {
                    "cache_id": sha,
                    "source": {"title": "某公司2026年第三季度报告", "report_date": "2026-09-30"},
                    "filing_kind": "q3",
                    "industry_hint": {"industry": None, "confidence": 0.1},
                    "document_profile": {
                        "market": "a_share",
                        "script": "zh_hans",
                        "accounting": "cas",
                        "filing_kind": "q3",
                        "industry": None,
                        "industry_confidence": 0.1,
                        "convert_health": {"low_text_ratio": 0.0, "garbled_pages": 0},
                        "novelty": True,
                        "novelty_reasons": ["industry_unknown"],
                    },
                    "doc": {"pages": 20},
                    "tables": [],
                    "anomalies": [],
                }
                (d / "meta.json").write_text(json.dumps(meta, ensure_ascii=False), encoding="utf-8")
                (d / "records.json").write_text(json.dumps([{
                    "table": 0, "page": 1, "type": "key_financials", "row_label": "营业收入",
                    "values": [{"col": 1, "value": "100", "header": "本期"}],
                }], ensure_ascii=False), encoding="utf-8")
                w.cmd_adapt_plan([sha, "--result", "result-ADAPT"])
                plan = w.read_json(d / "result-ADAPT" / "adapt_plan.json", {})
                self.assertTrue(plan.get("coverage_groups"))
                self.assertFalse(any(str(g).startswith("X_") for g in plan["coverage_groups"]))
                narr = {n["id"]: n for n in plan.get("narratives") or []}
                self.assertEqual(narr["mda_business"]["status"], "not_applicable")
                self.assertIn("promote_priority", plan)
                self.assertIn("observed_signals", plan)
            finally:
                os.environ.pop(w.CACHE_ENV, None)

    def test_adapt_plan_content_signals_from_report_md(self):
        with tempfile.TemporaryDirectory() as td:
            import os

            os.environ[w.CACHE_ENV] = td
            try:
                sha = "adaptcnt12345"
                d = w.entry_dir(sha)
                d.mkdir(parents=True, exist_ok=True)
                meta = {
                    "cache_id": sha,
                    "source": {"title": "某建材2025年年度报告", "report_date": "2025-12-31"},
                    "filing_kind": "annual",
                    "industry_hint": {"industry": "building_materials", "confidence": 0.9},
                    "document_profile": {
                        "market": "a_share", "script": "zh_hans", "accounting": "cas",
                        "filing_kind": "annual", "industry": "building_materials",
                        "industry_confidence": 0.9,
                        "convert_health": {"low_text_ratio": 0.0, "garbled_pages": 0},
                        "novelty": False, "novelty_reasons": [],
                    },
                    "doc": {"pages": 300},
                    "tables": [],
                    "anomalies": [],
                }
                (d / "meta.json").write_text(json.dumps(meta, ensure_ascii=False), encoding="utf-8")
                (d / "report.md").write_text(
                    "<!-- page:80 -->\n# 合并资产负债表\n货币资金 100\n资产总计 200\n负债合计 50\n"
                    "<!-- page:90 -->\n# 合并利润表\n营业总收入 10\n净利润 1\n"
                    "<!-- page:100 -->\n# 合并现金流量表\n经营活动产生的现金流量净额 2\n投资活动 3\n筹资活动 4\n",
                    encoding="utf-8",
                )
                (d / "result-ADAPT").mkdir(parents=True, exist_ok=True)
                (d / "result-ADAPT" / "manifest.json").write_text(
                    json.dumps({"catalog": {"tables": [], "narratives": [], "fields": [], "derived": []}},
                               ensure_ascii=False), encoding="utf-8")
                plan = w.build_adapt_plan(meta, "result-ADAPT", sha12=sha)
                types = {o["type"] for o in plan.get("observed_signals") or []}
                self.assertIn("balance_sheet", types)
                self.assertIn("income_stmt", types)
                self.assertIn("cashflow_stmt", types)
                self.assertTrue(plan.get("promote_priority"))
                self.assertEqual(plan["promote_priority"][0], "balance_sheet")
                for stmt in ("balance_sheet", "income_stmt", "cashflow_stmt"):
                    self.assertIn(stmt, plan.get("expected_but_missing") or [])
            finally:
                os.environ.pop(w.CACHE_ENV, None)

    def test_review_annual_missing_statements_hard_fail(self):
        with tempfile.TemporaryDirectory() as td:
            import os

            os.environ[w.CACHE_ENV] = td
            try:
                sha = "revhard123456"
                d = w.entry_dir(sha)
                result = d / "result-REV"
                (result / "tables").mkdir(parents=True, exist_ok=True)
                (result / "derived").mkdir(parents=True, exist_ok=True)
                meta = {
                    "cache_id": sha,
                    "source": {"title": "某公司2025年年度报告"},
                    "filing_kind": "annual",
                    "industry_hint": {"industry": "building_materials", "confidence": 1.0},
                    "document_profile": {
                        "market": "a_share", "filing_kind": "annual",
                        "industry": "building_materials", "industry_confidence": 1.0,
                        "novelty": False, "novelty_reasons": [],
                    },
                    "doc": {"pages": 200},
                }
                (d / "meta.json").write_text(json.dumps(meta, ensure_ascii=False), encoding="utf-8")
                (d / "report.md").write_text("资产负债表 货币资金 资产总计\n", encoding="utf-8")
                (result / "manifest.json").write_text(json.dumps({
                    "catalog": {"tables": [], "narratives": [], "fields": [], "derived": []},
                }, ensure_ascii=False), encoding="utf-8")
                (result / "quality.json").write_text(json.dumps({"status": "pass", "tables": []}, ensure_ascii=False), encoding="utf-8")
                (result / "gaps.json").write_text("[]", encoding="utf-8")
                (result / "promote_candidates.json").write_text(json.dumps({
                    "candidates": [{"table_id": "generic_table_p001_i001", "type_hint": "claims_payout", "title": "签章"}]
                }, ensure_ascii=False), encoding="utf-8")
                (result / "adapt_plan.json").write_text(json.dumps({
                    "required_gaps": [],
                    "observed_signals": [{"type": "balance_sheet", "strength": "strong", "evidence": ["货币资金"]}],
                    "expected_but_missing": ["balance_sheet", "income_stmt", "cashflow_stmt"],
                }, ensure_ascii=False), encoding="utf-8")
                out = w.review_extract(sha, result_name="result-REV")
                self.assertEqual(out["status"], "fail")
                hard_ids = [h.get("id") for h in out.get("hard_failures") or []]
                self.assertIn("statement_signature_gap", hard_ids)
                prop = w.read_json(result / "derived" / "evolution_proposal.json", {})
                self.assertTrue((prop.get("suggestions") or {}).get("actions"))
                self.assertTrue((prop.get("suggestions") or {}).get("missing_type_signatures"))
                noise = (prop.get("suggestions") or {}).get("noise_type_hints") or []
                self.assertTrue(any(n.get("type_hint") == "claims_payout" for n in noise))
            finally:
                os.environ.pop(w.CACHE_ENV, None)

    def test_review_q1_missing_income_is_warning_only(self):
        with tempfile.TemporaryDirectory() as td:
            import os

            os.environ[w.CACHE_ENV] = td
            try:
                sha = "revq1warn1234"
                d = w.entry_dir(sha)
                result = d / "result-Q1"
                (result / "tables").mkdir(parents=True, exist_ok=True)
                (result / "derived").mkdir(parents=True, exist_ok=True)
                meta = {
                    "cache_id": sha,
                    "source": {"title": "某公司2026一季报"},
                    "filing_kind": "q1",
                    "industry_hint": {"industry": "building_materials", "confidence": 0.5},
                    "document_profile": {
                        "market": "a_share", "filing_kind": "q1",
                        "industry": "building_materials", "industry_confidence": 0.5,
                        "novelty": False, "novelty_reasons": [],
                    },
                    "doc": {"pages": 15},
                }
                (d / "meta.json").write_text(json.dumps(meta, ensure_ascii=False), encoding="utf-8")
                (d / "report.md").write_text("page\n", encoding="utf-8")
                (result / "manifest.json").write_text(json.dumps({
                    "catalog": {
                        "tables": [
                            {"id": "balance_sheet", "file": "tables/balance_sheet.json", "group": "A"},
                            {"id": "cashflow_stmt", "file": "tables/cashflow_stmt.json", "group": "A"},
                        ],
                        "narratives": [
                            {"id": "mda_business", "file": "narratives/mda_business.json",
                             "group": "D_mda", "status": "not_applicable"},
                        ],
                        "fields": [], "derived": [],
                    },
                }, ensure_ascii=False), encoding="utf-8")
                (result / "quality.json").write_text(json.dumps({"status": "pass", "tables": []}, ensure_ascii=False), encoding="utf-8")
                (result / "gaps.json").write_text("[]", encoding="utf-8")
                (result / "promote_candidates.json").write_text(json.dumps({"candidates": []}, ensure_ascii=False), encoding="utf-8")
                (result / "adapt_plan.json").write_text(json.dumps({
                    "required_gaps": [], "observed_signals": [], "expected_but_missing": [],
                }, ensure_ascii=False), encoding="utf-8")
                out = w.review_extract(sha, result_name="result-Q1")
                self.assertEqual(out["status"], "pass")
                warn_ids = [x.get("id") for x in out.get("warnings") or []]
                self.assertIn("statement_signature_gap", warn_ids)
                hard_ids = [h.get("id") for h in out.get("hard_failures") or []]
                self.assertNotIn("statement_signature_gap", hard_ids)
            finally:
                os.environ.pop(w.CACHE_ENV, None)

    def test_qa_demotes_junk_income_stmt(self):
        with tempfile.TemporaryDirectory() as td:
            import os

            os.environ[w.CACHE_ENV] = td
            try:
                sha = "qajunkinc1234"
                d = w.entry_dir(sha)
                result = d / "result-QA"
                (result / "tables").mkdir(parents=True, exist_ok=True)
                payload = {
                    "table_id": "income_stmt",
                    "record_type": "income_stmt",
                    "title": "利润表",
                    "rows": [{"item": "北新嘉宝莉涂料集团股份有限公司", "c1": "1,000"}],
                    "row_count": 1,
                    "schema": {"columns": [{"label": "项目"}, {"label": "本期"}]},
                    "provenance": {"pages": [1], "tables": [1]},
                }
                (result / "tables" / "income_stmt.json").write_text(
                    json.dumps(payload, ensure_ascii=False), encoding="utf-8")
                (result / "manifest.json").write_text(json.dumps({
                    "catalog": {"tables": [
                        {"id": "income_stmt", "file": "tables/income_stmt.json", "group": "A",
                         "record_type": "income_stmt"},
                    ], "narratives": [], "fields": [], "derived": []},
                }, ensure_ascii=False), encoding="utf-8")
                findings = w.python_qa_findings(result, pdf_path=None)
                dem = [f for f in findings if f.get("verdict") == "demote"
                       and f.get("reason") == "statement_row_labels_invalid"]
                self.assertTrue(dem)
            finally:
                os.environ.pop(w.CACHE_ENV, None)

    def test_review_extract_writes_review_and_evolution_proposal(self):
        with tempfile.TemporaryDirectory() as td:
            import os

            os.environ[w.CACHE_ENV] = td
            try:
                sha = "review123456"
                d = w.entry_dir(sha)
                result = d / "result-REVIEW"
                (result / "tables").mkdir(parents=True, exist_ok=True)
                (result / "narratives").mkdir(parents=True, exist_ok=True)
                (result / "derived").mkdir(parents=True, exist_ok=True)
                meta = {
                    "cache_id": sha,
                    "source": {"title": "Unknown Holdings 2026 Annual Report", "report_date": "2026-12-31"},
                    "filing_kind": "annual",
                    "industry_hint": {"industry": None, "confidence": 0.0},
                    "document_profile": {
                        "market": "unknown",
                        "script": "en",
                        "accounting": "unknown",
                        "filing_kind": "annual",
                        "industry": None,
                        "industry_confidence": 0.0,
                        "convert_health": {"low_text_ratio": 0.0, "garbled_pages": 0},
                        "novelty": True,
                        "novelty_reasons": ["industry_unknown", "language_unsupported"],
                    },
                    "doc": {"pages": 100},
                }
                (d / "meta.json").write_text(json.dumps(meta, ensure_ascii=False), encoding="utf-8")
                (d / "report.md").write_text("<!-- page:1 -->\nBusiness outlook remains stable.\n", encoding="utf-8")
                manifest = {
                    "cache_id": sha,
                    "source": {"title": meta["source"]["title"], "report_date": meta["source"]["report_date"], "filing_kind": "annual"},
                    "catalog": {
                        "tables": [],
                        "narratives": [{"id": "mda_business", "file": "narratives/mda_business.json", "group": "D_mda", "status": "not_found"}],
                        "fields": [],
                        "derived": [],
                    },
                }
                (result / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")
                (result / "quality.json").write_text(json.dumps({"status": "pass", "tables": []}, ensure_ascii=False), encoding="utf-8")
                (result / "gaps.json").write_text(json.dumps([], ensure_ascii=False), encoding="utf-8")
                (result / "promote_candidates.json").write_text(json.dumps({
                    "candidates": [{"table_id": "generic_table_p001_i001", "type_hint": "customer_concentration", "title": "主要客户"}]
                }, ensure_ascii=False), encoding="utf-8")
                (result / "narratives" / "mda_business.json").write_text(json.dumps({
                    "id": "mda_business", "status": "not_found"
                }, ensure_ascii=False), encoding="utf-8")
                out = w.review_extract(sha, result_name="result-REVIEW")
                # 年报缺三表 → hard fail，但仍写 evolution_proposal
                self.assertEqual(out["status"], "fail")
                self.assertTrue(any(h.get("id") == "statement_signature_gap" for h in out.get("hard_failures") or []))
                self.assertTrue(out["novelty"])
                self.assertTrue((result / "review.json").is_file())
                self.assertTrue((result / "derived" / "evolution_proposal.json").is_file())
                prop = w.read_json(result / "derived" / "evolution_proposal.json", {})
                self.assertTrue((prop.get("suggestions") or {}).get("actions"))
                man = w.read_json(result / "manifest.json", {})
                self.assertTrue(any(d.get("id") == "evolution_proposal" for d in man["catalog"]["derived"]))
            finally:
                os.environ.pop(w.CACHE_ENV, None)

    def test_none(self):
        self.assertIsNone(w.detect_industry("普通文本")["industry"])

    def test_nonferrous_beats_manufacturing(self):
        text = ("主要产品产量 矿产铜 107 万吨，产销量 同比增长，产能利用率 提升；"
                "冶炼 选矿 精矿 保有储量 资源量 金属量")
        h = w.detect_industry(text)
        self.assertEqual(h["industry"], "nonferrous")
        self.assertIn("nonferrous", h["matched"])

    def test_nonferrous_title_boost(self):
        h = w.detect_industry("阴极铜 产量 销量", title="某铜业股份有限公司2025年年度报告", pages=300)
        self.assertEqual(h["industry"], "nonferrous")

    def test_jewelry_retail_not_nonferrous(self):
        text = "珠宝首饰 零售 加盟店 门店 黄金饰品 销售额"
        h = w.detect_industry(text, title="某黄金珠宝集团股份有限公司2025年年度报告", pages=200)
        self.assertNotEqual(h["industry"], "nonferrous")

    def test_nonferrous_type_hint_signatures(self):
        resv_tbl = "\n".join([
            "| 矿山 | 矿石量（万吨） | 品位（%） | 金属量（万吨） |",
            "|---|---|---|---|",
            "| 某铜矿 | 10,000 | 0.45 | 45 |",
        ])
        constr_tbl = "\n".join([
            "| 项目名称 | 预算数 | 本期增加 | 工程累计投入占预算比例(%) | 工程进度(%) |",
            "|---|---|---|---|---|",
            "| 某扩建工程 | 500,000 | 12,000 | 60 | 65 |",
        ])
        hedge_tbl = "\n".join([
            "| 衍生品投资类型 | 期初投资金额 | 期末投资金额 | 报告期实际损益金额 |",
            "|---|---|---|---|",
            "| 铜期货合约 | 1,000 | 1,200 | 150 |",
        ])
        md_lines = ("<!-- page:55 -->\n\n" + resv_tbl + "\n\n<!-- page:180 -->\n\n" + constr_tbl
                    + "\n\n<!-- page:190 -->\n\n" + hedge_tbl).split("\n")
        tables = w.find_tables(md_lines)
        hints = {t["index"]: t.get("type_hint") for t in tables}
        self.assertEqual(hints[0], "reserves")
        self.assertEqual(hints[1], "construction_projects")
        self.assertEqual(hints[2], "hedging")
        self.assertTrue(all(t["type"] is None for t in tables))

    def test_nonferrous_annual_narratives_registered(self):
        with tempfile.TemporaryDirectory() as td:
            import os

            os.environ[w.CACHE_ENV] = td
            try:
                sha = "nfannual1234"
                d = w.entry_dir(sha)
                d.mkdir(parents=True, exist_ok=True)
                meta = {
                    "source": {"title": "某矿业公司2025年年度报告", "report_date": "2025-12-31"},
                    "filing_kind": "annual",
                    "industry_hint": {"industry": "nonferrous"},
                    "doc": {"pages": 300},
                    "tables": [],
                }
                (d / "meta.json").write_text(json.dumps(meta, ensure_ascii=False), encoding="utf-8")
                (d / "records.json").write_text(json.dumps([{
                    "table": 0, "page": 1, "type": "key_financials", "row_label": "营业收入",
                    "values": [{"col": 1, "value": "100", "header": "本期"}],
                }], ensure_ascii=False), encoding="utf-8")
                w.materialize_tables(sha, out_name="result-NF", force=True)
                narr = w.read_json(d / "result-NF" / "manifest.json", {}).get("catalog", {}).get("narratives", [])
                nf_ids = {n["id"] for n in narr if n.get("group") == "X_nonferrous"}
                self.assertEqual(nf_ids, {"project_progress", "unit_cost"})
            finally:
                os.environ.pop(w.CACHE_ENV, None)

    def test_nonferrous_quarter_narratives_not_registered(self):
        with tempfile.TemporaryDirectory() as td:
            import os

            os.environ[w.CACHE_ENV] = td
            try:
                sha = "nfquarter123"
                d = w.entry_dir(sha)
                d.mkdir(parents=True, exist_ok=True)
                meta = {
                    "source": {"title": "某矿业公司2026年第一季度报告", "report_date": "2026-03-31"},
                    "filing_kind": "q1",
                    "industry_hint": {"industry": "nonferrous"},
                    "doc": {"pages": 15},
                    "tables": [],
                }
                (d / "meta.json").write_text(json.dumps(meta, ensure_ascii=False), encoding="utf-8")
                (d / "records.json").write_text(json.dumps([{
                    "table": 0, "page": 1, "type": "key_financials", "row_label": "营业收入",
                    "values": [{"col": 1, "value": "100", "header": "本期"}],
                }], ensure_ascii=False), encoding="utf-8")
                w.materialize_tables(sha, out_name="result-NFQ", force=True)
                narr = w.read_json(d / "result-NFQ" / "manifest.json", {}).get("catalog", {}).get("narratives", [])
                nf_narr = [n for n in narr if n.get("group") == "X_nonferrous"]
                self.assertEqual(nf_narr, [])
            finally:
                os.environ.pop(w.CACHE_ENV, None)

    def test_nonferrous_reserves_promotion(self):
        with tempfile.TemporaryDirectory() as td:
            import os

            os.environ[w.CACHE_ENV] = td
            try:
                sha = "nfpromo12345"
                d = w.entry_dir(sha)
                d.mkdir(parents=True, exist_ok=True)
                meta = {
                    "source": {"title": "某矿业公司2025年年度报告", "report_date": "2025-12-31"},
                    "filing_kind": "annual",
                    "industry_hint": {"industry": "nonferrous"},
                    "tables": [
                        {"index": 1, "page": 55, "line": 0, "line_end": 5, "type": None,
                         "headers": ["矿山", "矿石量", "品位", "金属量"], "rows": 3,
                         "type_hint": "reserves"},
                    ],
                }
                md = "\n".join([
                    "<!-- page:55 -->", "## 资源储量",
                    "| 矿山 | 矿石量 | 品位 | 金属量 |",
                    "|---|---|---|---|",
                    "| 某铜矿 | 10,000 | 0.45 | 45 |",
                    "| 某金矿 | 5,000 | 1.20 | 6 |",
                    "| 某锌矿 | 8,000 | 3.10 | 25 |",
                ])
                (d / "report.md").write_text(md, encoding="utf-8")
                (d / "meta.json").write_text(json.dumps(meta, ensure_ascii=False), encoding="utf-8")
                (d / "records.json").write_text(json.dumps([
                    {"table": 1, "page": 55, "type": None, "row_label": "某铜矿",
                     "values": [{"col": 1, "value": "10,000", "header": "矿石量"}]},
                ], ensure_ascii=False), encoding="utf-8")
                w.materialize_tables(sha, out_name="result-NFP", force=True)
                generic_id = "generic_table_p055_i001"
                w.apply_promotions(sha, [{
                    "table_file": f"tables/{generic_id}.json",
                    "promote_to": "reserves",
                    "confidence": "high",
                    "reason": "表头含矿石量/品位/金属量",
                }], result_name="result-NFP")
                man = w.read_json(d / "result-NFP" / "manifest.json", {})
                ids = {t["id"] for t in man["catalog"]["tables"]}
                self.assertIn("reserves", ids)
                tbl = w.read_json(d / "result-NFP" / "tables" / "reserves.json", {})
                self.assertEqual(tbl.get("group"), "X_nonferrous")
            finally:
                os.environ.pop(w.CACHE_ENV, None)


    def test_schema_has_no_company_brand_names(self):
        root = Path(__file__).resolve().parents[1]
        blob = (root / "scripts" / "wm_report.py").read_text(encoding="utf-8")
        blob += (root / "references" / "coverage-checklist.md").read_text(encoding="utf-8")
        for p in (root / "scripts" / "domain").glob("*.py"):
            blob += p.read_text(encoding="utf-8")
        for name in ("哈弗", "魏牌", "欧拉", "坦克", "中国平安", "中信证券", "万科", "华能"):
            self.assertNotIn(name, blob)

    def test_insurance_beats_bank(self):
        text = ("原保险保费收入 上升，赔付支出 与 退保金 披露；"
                "综合偿付能力充足率 与 核心偿付能力充足率 达标；已赚保费 承保利润。"
                "吸收存款 偶见于托管描述。")
        h = w.detect_industry(text, title="某人寿保险股份有限公司2025年年度报告", pages=300)
        self.assertEqual(h["industry"], "insurance")

    def test_insurance_type_hints(self):
        md = "\n".join([
            "<!-- page:40 -->",
            "| 项目 | 原保险保费收入 | 保险业务收入 |",
            "|---|---|---|",
            "| 寿险 | 100 | 100 |",
            "<!-- page:41 -->",
            "| 项目 | 赔付支出 | 退保金 |",
            "|---|---|---|",
            "| 合计 | 50 | 10 |",
            "<!-- page:42 -->",
            "| 指标 | 综合偿付能力充足率 | 核心偿付能力充足率 |",
            "|---|---|---|",
            "| 本公司 | 220% | 180% |",
            "<!-- page:43 -->",
            "| 指标 | 新业务价值 | 内含价值 |",
            "|---|---|---|",
            "| 寿险 | 200 | 8000 |",
            "<!-- page:44 -->",
            "| 渠道 | 个险 | 银保 |",
            "|---|---|---|",
            "| 保费 | 60 | 40 |",
        ]).split("\n")
        hints = {t.get("type_hint") for t in w.find_tables(md)}
        self.assertTrue({"premium_income", "claims_payout", "solvency", "nbv_ev", "channel_mix"} <= hints)

    def test_insurance_annual_narratives(self):
        with tempfile.TemporaryDirectory() as td:
            import os
            os.environ[w.CACHE_ENV] = td
            try:
                sha = "insannual001"
                d = w.entry_dir(sha)
                d.mkdir(parents=True, exist_ok=True)
                meta = {
                    "source": {"title": "某保险公司2025年年度报告"},
                    "filing_kind": "annual",
                    "industry_hint": {"industry": "insurance"},
                    "doc": {"pages": 280},
                    "tables": [],
                }
                (d / "meta.json").write_text(json.dumps(meta, ensure_ascii=False), encoding="utf-8")
                (d / "records.json").write_text(json.dumps([{
                    "table": 0, "page": 1, "type": "key_financials", "row_label": "营业收入",
                    "values": [{"col": 1, "value": "100", "header": "本期"}],
                }], ensure_ascii=False), encoding="utf-8")
                w.materialize_tables(sha, out_name="result-INS", force=True)
                narr = w.read_json(d / "result-INS" / "manifest.json", {}).get("catalog", {}).get("narratives", [])
                ids = {n["id"] for n in narr if n.get("group") == "X_insurance"}
                self.assertEqual(ids, {"underwriting_profit", "spread_income"})
                gaps = w.read_json(d / "result-INS" / "gaps.json", [])
                gap_ids = {g["id"] for g in gaps if g.get("status") == "required"}
                self.assertTrue({"ifrs17_csm", "persistency_surrender_rate"} <= gap_ids)
            finally:
                os.environ.pop(w.CACHE_ENV, None)

    def test_broker_beats_bank(self):
        text = ("经纪业务 手续费及佣金 上升；投行业务 承销；资产管理业务 管理费；"
                "净资本 与 风险覆盖率 达标；代理买卖证券 两融 客户保证金。")
        h = w.detect_industry(text, title="某证券股份有限公司2025年年度报告", pages=300)
        self.assertEqual(h["industry"], "broker")

    def test_bank_group_subsidiaries_do_not_flip_to_broker(self):
        # 招行式：银行集团必含投行/资管/两融子公司词（招银国际/招银理财），
        # 银行强词充分 + 银行标题时不得误判 broker
        text = ("吸收存款 与 发放贷款和垫款 稳步增长；资本充足率 不良贷款 双改善；"
                "净息差 拨备覆盖率 保持同业前列；客户贷款 客户存款 结构优化。"
                "子公司投行业务 投资银行业务 发展；资产管理业务 稳健；融资融券 余额上升。")
        h = w.detect_industry(text, title="招商银行股份有限公司2025年年度报告", pages=350)
        self.assertEqual(h["industry"], "bank")

    def test_broker_type_hints(self):
        md = "\n".join([
            "<!-- page:50 -->",
            "| 业务 | 经纪业务 | 手续费及佣金 |",
            "|---|---|---|",
            "| 代理买卖 | 10 | 10 |",
            "<!-- page:51 -->",
            "| 指标 | 净资本 | 风险覆盖率 |",
            "|---|---|---|",
            "| 本公司 | 500 | 200% |",
            "<!-- page:52 -->",
            "| 项目 | 融资融券 | 两融余额 |",
            "|---|---|---|",
            "| 合计 | 100 | 100 |",
            "<!-- page:53 -->",
            "| 项目 | 自营业务 | 投资收益 |",
            "|---|---|---|",
            "| 权益 | 20 | 5 |",
        ]).split("\n")
        hints = {t.get("type_hint") for t in w.find_tables(md)}
        self.assertTrue({"brokerage_income", "risk_indicators", "margin_trading", "prop_trading"} <= hints)

    def test_broker_annual_narratives(self):
        with tempfile.TemporaryDirectory() as td:
            import os
            os.environ[w.CACHE_ENV] = td
            try:
                sha = "brkannual001"
                d = w.entry_dir(sha)
                d.mkdir(parents=True, exist_ok=True)
                meta = {
                    "source": {"title": "某证券公司2025年年度报告"},
                    "filing_kind": "annual",
                    "industry_hint": {"industry": "broker"},
                    "doc": {"pages": 250},
                    "tables": [],
                }
                (d / "meta.json").write_text(json.dumps(meta, ensure_ascii=False), encoding="utf-8")
                (d / "records.json").write_text(json.dumps([{
                    "table": 0, "page": 1, "type": "key_financials", "row_label": "营业收入",
                    "values": [{"col": 1, "value": "100", "header": "本期"}],
                }], ensure_ascii=False), encoding="utf-8")
                w.materialize_tables(sha, out_name="result-BRK", force=True)
                narr = w.read_json(d / "result-BRK" / "manifest.json", {}).get("catalog", {}).get("narratives", [])
                ids = {n["id"] for n in narr if n.get("group") == "X_broker"}
                self.assertEqual(ids, {"trading_volume_drivers"})
            finally:
                os.environ.pop(w.CACHE_ENV, None)

    def test_real_estate_beats_manufacturing(self):
        text = ("签约金额 与 签约面积 增长；土地储备 权益面积；竣工面积 交付；"
                "去化 预售 房地产项目。产销量 产能利用率 亦提及。")
        h = w.detect_industry(text, title="某置业股份有限公司2025年年度报告", pages=280)
        self.assertEqual(h["industry"], "real_estate")

    def test_real_estate_type_hints(self):
        md = "\n".join([
            "<!-- page:30 -->",
            "| 地区 | 签约金额 | 签约面积 |",
            "|---|---|---|",
            "| 华东 | 100 | 50 |",
            "<!-- page:31 -->",
            "| 项目 | 土地储备 | 总建筑面积 |",
            "|---|---|---|",
            "| 合计 | 200 | 400 |",
            "<!-- page:32 -->",
            "| 项目 | 竣工面积 | 交付面积 |",
            "|---|---|---|",
            "| 合计 | 80 | 70 |",
            "<!-- page:33 -->",
            "| 项目 | 合同负债 | 预收账款 |",
            "|---|---|---|",
            "| 合计 | 300 | 0 |",
            "<!-- page:34 -->",
            "| 指标 | 净负债率 | 现金短债比 |",
            "|---|---|---|",
            "| 集团 | 80% | 1.5 |",
        ]).split("\n")
        hints = {t.get("type_hint") for t in w.find_tables(md)}
        self.assertTrue(
            {"contracted_sales", "land_bank", "delivery_completion",
             "contract_liabilities", "three_red_lines"} <= hints
        )

    def test_real_estate_annual_narratives(self):
        with tempfile.TemporaryDirectory() as td:
            import os
            os.environ[w.CACHE_ENV] = td
            try:
                sha = "reannual0001"
                d = w.entry_dir(sha)
                d.mkdir(parents=True, exist_ok=True)
                meta = {
                    "source": {"title": "某地产公司2025年年度报告"},
                    "filing_kind": "annual",
                    "industry_hint": {"industry": "real_estate"},
                    "doc": {"pages": 260},
                    "tables": [],
                }
                (d / "meta.json").write_text(json.dumps(meta, ensure_ascii=False), encoding="utf-8")
                (d / "records.json").write_text(json.dumps([{
                    "table": 0, "page": 1, "type": "key_financials", "row_label": "营业收入",
                    "values": [{"col": 1, "value": "100", "header": "本期"}],
                }], ensure_ascii=False), encoding="utf-8")
                w.materialize_tables(sha, out_name="result-RE", force=True)
                narr = w.read_json(d / "result-RE" / "manifest.json", {}).get("catalog", {}).get("narratives", [])
                ids = {n["id"] for n in narr if n.get("group") == "X_real_estate"}
                self.assertEqual(ids, {"sell_through", "project_financing"})
            finally:
                os.environ.pop(w.CACHE_ENV, None)

    def test_energy_beats_manufacturing(self):
        text = ("装机容量 增加；发电量 与 上网电量 上升；售电量 稳定；"
                "平均利用小时 改善。产量 产销量 产能利用率 亦有。")
        h = w.detect_industry(text, title="某电力股份有限公司2025年年度报告", pages=240)
        self.assertEqual(h["industry"], "energy")

    def test_nonferrous_beats_energy_captive_power(self):
        """电投能源式：电解铝+自备电厂，标题含「能源」也不应判 energy。"""
        text = ("有色金属 电解铝 氧化铝 冶炼 矿山 资源量；"
                "装机容量 发电量 售电量 上网电量 利用小时 千瓦时。产量 产销量。")
        h = w.detect_industry(text, title="某能源股份有限公司2025年年度报告", pages=293)
        self.assertEqual(h["industry"], "nonferrous")

    def test_quarter_building_materials_not_insurance(self):
        """季报短文常含保险合同准则附注词，无保险标题不得定型 insurance。"""
        text = ("营业收入 增长。附注提及 赔付支出 退保金 原保险合同 已赚保费；"
                "另有 代理买卖证券 融资融券 吸收存款 发放贷款和垫款。产能利用率 产量。")
        h = w.detect_industry(text, title="某建材股份有限公司2026年第一季度报告", pages=11)
        self.assertNotEqual(h["industry"], "insurance")
        self.assertNotEqual(h["industry"], "broker")

    def test_energy_type_hints(self):
        md = "\n".join([
            "<!-- page:20 -->",
            "| 电源 | 装机容量 | 兆瓦 |",
            "|---|---|---|",
            "| 火电 | 1000 | 1000 |",
            "<!-- page:21 -->",
            "| 项目 | 发电量 | 上网电量 |",
            "|---|---|---|",
            "| 合计 | 50 | 48 |",
            "<!-- page:22 -->",
            "| 项目 | 利用小时 | 平均利用小时 |",
            "|---|---|---|",
            "| 火电 | 4000 | 4000 |",
            "<!-- page:23 -->",
            "| 指标 | 来水 | 水库 |",
            "|---|---|---|",
            "| 本期 | 偏丰 | 正常 |",
            "<!-- page:24 -->",
            "| 类型 | 中长期 | 现货 |",
            "|---|---|---|",
            "| 电量占比 | 70% | 30% |",
        ]).split("\n")
        hints = {t.get("type_hint") for t in w.find_tables(md)}
        self.assertTrue(
            {"installed_capacity", "power_generation", "utilization_hours",
             "hydrology", "power_price_mix"} <= hints
        )

    def test_energy_annual_narratives(self):
        with tempfile.TemporaryDirectory() as td:
            import os
            os.environ[w.CACHE_ENV] = td
            try:
                sha = "enannual0001"
                d = w.entry_dir(sha)
                d.mkdir(parents=True, exist_ok=True)
                meta = {
                    "source": {"title": "某能源公司2025年年度报告"},
                    "filing_kind": "annual",
                    "industry_hint": {"industry": "energy"},
                    "doc": {"pages": 220},
                    "tables": [],
                }
                (d / "meta.json").write_text(json.dumps(meta, ensure_ascii=False), encoding="utf-8")
                (d / "records.json").write_text(json.dumps([{
                    "table": 0, "page": 1, "type": "key_financials", "row_label": "营业收入",
                    "values": [{"col": 1, "value": "100", "header": "本期"}],
                }], ensure_ascii=False), encoding="utf-8")
                w.materialize_tables(sha, out_name="result-EN", force=True)
                narr = w.read_json(d / "result-EN" / "manifest.json", {}).get("catalog", {}).get("narratives", [])
                ids = {n["id"] for n in narr if n.get("group") == "X_energy"}
                self.assertEqual(ids, {"power_price", "fuel_cost"})
            finally:
                os.environ.pop(w.CACHE_ENV, None)

    def test_insurance_premium_promotion(self):
        with tempfile.TemporaryDirectory() as td:
            import os
            os.environ[w.CACHE_ENV] = td
            try:
                sha = "inspromo0001"
                d = w.entry_dir(sha)
                d.mkdir(parents=True, exist_ok=True)
                meta = {
                    "source": {"title": "某保险公司2025年年度报告"},
                    "filing_kind": "annual",
                    "industry_hint": {"industry": "insurance"},
                    "tables": [
                        {"index": 1, "page": 40, "line": 0, "line_end": 5, "type": None,
                         "headers": ["项目", "原保险保费收入", "保险业务收入"], "rows": 3,
                         "type_hint": "premium_income"},
                    ],
                }
                md = "\n".join([
                    "<!-- page:40 -->", "## 保费收入",
                    "| 项目 | 原保险保费收入 | 保险业务收入 |",
                    "|---|---|---|",
                    "| 寿险 | 100 | 100 |",
                    "| 财险 | 80 | 80 |",
                    "| 合计 | 180 | 180 |",
                ])
                (d / "report.md").write_text(md, encoding="utf-8")
                (d / "meta.json").write_text(json.dumps(meta, ensure_ascii=False), encoding="utf-8")
                (d / "records.json").write_text(json.dumps([
                    {"table": 1, "page": 40, "type": None, "row_label": "寿险",
                     "values": [{"col": 1, "value": "100", "header": "原保险保费收入"}]},
                    {"table": 1, "page": 40, "type": None, "row_label": "财险",
                     "values": [{"col": 1, "value": "80", "header": "原保险保费收入"}]},
                    {"table": 1, "page": 40, "type": None, "row_label": "合计",
                     "values": [{"col": 1, "value": "180", "header": "原保险保费收入"}]},
                ], ensure_ascii=False), encoding="utf-8")
                w.materialize_tables(sha, out_name="result-INSP", force=True)
                generic_id = "generic_table_p040_i001"
                w.apply_promotions(sha, [{
                    "table_file": f"tables/{generic_id}.json",
                    "promote_to": "premium_income",
                    "confidence": "high",
                    "reason": "表头含原保险保费收入",
                }], result_name="result-INSP")
                man = w.read_json(d / "result-INSP" / "manifest.json", {})
                ids = {t["id"] for t in man["catalog"]["tables"]}
                self.assertIn("premium_income", ids)
                tbl = w.read_json(d / "result-INSP" / "tables" / "premium_income.json", {})
                self.assertEqual(tbl.get("group"), "X_insurance")
            finally:
                os.environ.pop(w.CACHE_ENV, None)


class TestBuildRecords(unittest.TestCase):
    def test_records_with_provenance(self):
        tbl = "\n".join([
            "| （人民币百万元） | 2025年 | 2024年 |",
            "|---|---|---|",
            "| 营业收入 | 337,532 | 337,488 |",
            "| 资产总计 | 130,000 | 120,000 |",
            "| 说明行（无数值） | — 略 | |",
        ])
        md_lines = ("<!-- page:14 -->\n\n" + tbl).split("\n")
        tables = w.find_tables(md_lines)
        recs = w.build_records(md_lines, tables)
        self.assertEqual(len(recs), 2)  # 无数值的说明行被过滤
        r0 = recs[0]
        self.assertEqual(r0["row_label"], "营业收入")
        self.assertEqual(r0["page"], 14)
        self.assertEqual(r0["values"][0]["value"], "337,532")
        self.assertIn("2025", r0["values"][0]["period"] or r0["values"][0]["header"])
        self.assertEqual(r0["unit"], "人民币百万元")


class TestAnomalies(unittest.TestCase):
    def _meta(self, pages, tables, chapters, conv, md="x" * 100):
        return w.detect_anomalies(pages, tables, chapters, conv, md)

    def test_blockers(self):
        a = self._meta([], [], [], {"error": "boom", "pdf": {"bookmarks": []}}, "")
        codes = {x["code"]: x for x in a}
        self.assertEqual(codes["convert_failed"]["severity"], "blocker")
        self.assertIn("missing_chapter_anchors", codes)
        self.assertIn("no_bookmarks", codes)

    def test_low_text_and_long_table(self):
        pages = [{"page": 9, "chars": 3, "tables": 0}]
        tables = [{"page": 30, "rows": 90, "cols": 5, "type": "balance_sheet"}]
        a = self._meta(pages, tables, [{"num": 1, "page": 1, "page_end": None}],
                       {"pdf": {"bookmarks": [["x", 1, "目录"]], "pages": 300, "encrypted": False}}, "y" * 100)
        codes = {x["code"] for x in a}
        self.assertIn("low_text_page", codes)
        self.assertIn("long_table", codes)
        self.assertNotIn("convert_failed", codes)

    def test_kangxi_flag(self):
        a = self._meta([], [], [], {"pdf": {"bookmarks": [1], "encrypted": False},
                                    "kangxi_pages": [3, 7]}, "z" * 100)
        codes = {x["code"]: x for x in a}
        self.assertEqual(codes["kangxi_compat"]["pages"], [3, 7])

    def test_convert_missing(self):
        a = self._meta([], [], [], {}, "")
        self.assertEqual(a[0]["code"], "convert_missing")
        self.assertEqual(a[0]["severity"], "blocker")


class TestLocate(unittest.TestCase):
    def test_page_of_line(self):
        md_lines = ["<!-- page:1 -->", "甲", "<!-- page:2 -->", "乙", "丙"]
        self.assertEqual(w.page_of_line(md_lines, 2), 2)
        self.assertEqual(w.page_of_line(md_lines, 1), 1)


class TestCacheRoundtrip(unittest.TestCase):
    def test_index_upsert_and_load(self):
        with tempfile.TemporaryDirectory() as td:
            import os

            os.environ[w.CACHE_ENV] = td
            try:
                w.index_upsert("abc123def456", symbol="600036", title="招商银行年报")
                idx = w.index_load()
                ent = idx["entries"]["abc123def456"]
                self.assertEqual(ent["symbol"], "600036")
                # fetch→scan 产物落盘可读
                d = w.entry_dir("abc123def456")
                d.mkdir(parents=True)
                (d / "fetch_meta.json").write_text(
                    json.dumps({"source": {"symbol": "600036"}}, ensure_ascii=False), encoding="utf-8")
                self.assertEqual(w.read_json(d / "fetch_meta.json")["source"]["symbol"], "600036")
            finally:
                os.environ.pop(w.CACHE_ENV, None)

    def test_cmd_cache_info_derives_latest_result_and_quality(self):
        with tempfile.TemporaryDirectory() as td:
            import os

            os.environ[w.CACHE_ENV] = td
            try:
                sha = "abc123def456"
                d = w.entry_dir(sha)
                d.mkdir(parents=True, exist_ok=True)

                result_name = "result-UT"
                result_dir = d / result_name
                result_dir.mkdir(parents=True, exist_ok=True)

                (result_dir / "manifest.json").write_text(
                    json.dumps({
                        "version": "0.4.1",
                        "layout": "split_tables",
                        "cache_id": sha,
                        "catalog": {"tables": [{"id": "key_financials", "file": "tables/key_financials.json"}], "narratives": [], "fields": [], "derived": []},
                    }, ensure_ascii=False),
                    encoding="utf-8",
                )
                (result_dir / "quality.json").write_text(
                    json.dumps({"status": "pass", "tables": [{"id": "key_financials", "verdict": "pass"}]}, ensure_ascii=False),
                    encoding="utf-8",
                )

                buf = io.StringIO()
                with contextlib.redirect_stdout(buf):
                    w.cmd_cache(["info", sha])
                out = json.loads(buf.getvalue())

                self.assertEqual(out.get("latest_result"), result_name)
                self.assertEqual(out.get("quality_status"), "pass")
                self.assertEqual(out.get("catalog_summary", {}).get("tables"), 1)
                self.assertEqual(out.get("catalog_summary", {}).get("fields"), 0)
                self.assertEqual(out.get("typed_pass_tables"), 1)
            finally:
                os.environ.pop(w.CACHE_ENV, None)


class TestMaterializeTables(unittest.TestCase):
    def test_materialize_split_tables_and_manifest(self):
        with tempfile.TemporaryDirectory() as td:
            import os

            os.environ[w.CACHE_ENV] = td
            try:
                sha = "abc123def456"
                d = w.entry_dir(sha)
                d.mkdir(parents=True, exist_ok=True)
                meta = {
                    "source": {"title": "长城汽车2025年报", "symbol": "601633", "report_date": "2025-12-31"},
                    "industry_hint": {"industry": "automobile"},
                    "tables": [
                        {"index": 1, "type": "segments", "headers": ["分地区", "营业收入", "营业成本"], "periods": {1: "2025", 2: "2025"}},
                        {"index": 2, "type": "variance_reasons", "headers": ["项目名称", "2025年度", "2024年度", "变动幅度", "原因说明"]},
                    ],
                }
                records = [
                    {"table": 1, "page": 28, "type": "segments", "row_label": "国内", "values": [
                        {"col": 1, "value": "128,467", "header": "营业收入"},
                        {"col": 2, "value": "104,562", "header": "营业成本"},
                    ]},
                    {"table": 2, "page": 31, "type": "variance_reasons", "row_label": "销售费用", "values": [
                        {"col": 1, "value": "11,273", "header": "2025年度"},
                        {"col": 2, "value": "7,832", "header": "2024年度"},
                        {"col": 3, "value": "43.93", "header": "变动幅度"},
                        {"col": 4, "value": "主要系渠道建设", "header": "原因说明"},
                    ]},
                ]
                (d / "meta.json").write_text(json.dumps(meta, ensure_ascii=False), encoding="utf-8")
                (d / "records.json").write_text(json.dumps(records, ensure_ascii=False), encoding="utf-8")
                out = w.materialize_tables(sha, out_name="result-UT", force=True)
                self.assertEqual(out["tables"], 2)
                manifest = w.read_json(d / "result-UT" / "manifest.json", {})
                self.assertEqual(manifest.get("layout"), "split_tables")
                self.assertEqual(manifest.get("version"), "0.4.1")
                table_ids = {x["id"] for x in manifest.get("catalog", {}).get("tables", [])}
                self.assertIn("segments_by_region", table_ids)
                self.assertIn("variance_reasons", table_ids)
                seg = w.read_json(d / "result-UT" / "tables" / "segments_by_region.json", {})
                self.assertEqual(seg.get("schema", {}).get("columns", [])[1]["label"], "营业收入")
                self.assertEqual(seg.get("rows", [])[0]["c1"], "128,467")
                varf = w.read_json(d / "result-UT" / "tables" / "variance_reasons.json", {})
                self.assertEqual(varf.get("rows", [])[0]["yoy_pct"], "43.93")
                self.assertIn("渠道建设", varf.get("rows", [])[0]["reason"])
            finally:
                os.environ.pop(w.CACHE_ENV, None)

    def test_materialize_generic_table_and_variance_gap(self):
        with tempfile.TemporaryDirectory() as td:
            import os

            os.environ[w.CACHE_ENV] = td
            try:
                sha = "fff111eee222"
                d = w.entry_dir(sha)
                d.mkdir(parents=True, exist_ok=True)
                md = "\n".join([
                    "<!-- page:31 -->", "",
                    "## 经营情况讨论与分析",
                    "| 项目名称 | 2025年度 | 2024年度 | 变动幅度 |",
                    "|---|---|---|---|",
                    "| 管理费用 | 10 | 9 | 11.11 |",
                    "",
                    "<!-- page:40 -->", "",
                    "## 其他表",
                    "| 自定义列 | 值1 | 值2 |",
                    "|---|---|---|",
                    "| 行A | 1 | 2 |",
                    "| 行B | 3 | 4 |",
                    "| 行C | 5 | 6 |",
                ])
                meta = {
                    "source": {"title": "测试年报", "symbol": "000001", "report_date": "2025-12-31"},
                    "industry_hint": {"industry": "automobile"},
                    "sections": [{"key": "mda_overview", "page": 31}],
                    "tables": [
                        {"index": 1, "page": 31, "line": 3, "line_end": 5, "type": "variance_reasons",
                         "headers": ["项目名称", "2025年度", "2024年度", "变动幅度"], "rows": 1},
                        {"index": 2, "page": 40, "line": 9, "line_end": 13, "type": None,
                         "headers": ["自定义列", "值1", "值2"], "rows": 3},
                    ],
                }
                records = [
                    {"table": 1, "page": 31, "type": "variance_reasons", "row_label": "管理费用", "values": [
                        {"col": 1, "value": "10", "header": "2025年度"},
                        {"col": 2, "value": "9", "header": "2024年度"},
                        {"col": 3, "value": "11.11", "header": "变动幅度"},
                    ]},
                ]
                (d / "report.md").write_text(md, encoding="utf-8")
                (d / "meta.json").write_text(json.dumps(meta, ensure_ascii=False), encoding="utf-8")
                (d / "records.json").write_text(json.dumps(records, ensure_ascii=False), encoding="utf-8")
                out = w.materialize_tables(sha, out_name="result-UT2", force=True)
                manifest = w.read_json(d / "result-UT2" / "manifest.json", {})
                table_ids = {x["id"] for x in manifest.get("catalog", {}).get("tables", [])}
                generic = [tid for tid in table_ids if tid.startswith("generic_table_p040")]
                self.assertTrue(generic)
                gaps = w.read_json(d / "result-UT2" / "gaps.json", [])
                gap_ids = {g["id"] for g in gaps}
                self.assertIn("variance_reason::管理费用", gap_ids)
                generic_tbl = w.read_json(d / "result-UT2" / "tables" / f"{generic[0]}.json", {})
                self.assertEqual(generic_tbl.get("source_type"), "generic_table")
                self.assertEqual(generic_tbl.get("rows", [])[0]["c1"], "1")
                self.assertEqual(out["tables"], len(manifest.get("catalog", {}).get("tables", [])))
            finally:
                os.environ.pop(w.CACHE_ENV, None)

    def test_materialize_hinted_two_row_table_enters_candidates(self):
        with tempfile.TemporaryDirectory() as td:
            import os

            os.environ[w.CACHE_ENV] = td
            try:
                sha = "hint2row12345"
                d = w.entry_dir(sha)
                d.mkdir(parents=True, exist_ok=True)
                md = "\n".join([
                    "<!-- page:64 -->", "",
                    "## 新药情况",
                    "| 细分行业 | 药品名称 | 是否纳入国家医保目录 |",
                    "|---|---|---|",
                    "| 化学制药 | B药 | 是 |",
                    "",
                    "<!-- page:70 -->", "",
                    "## 其他小表",
                    "| 列甲 | 列乙 |",
                    "|---|---|",
                    "| x | y |",
                ])
                meta = {
                    "source": {"title": "测试年报", "symbol": "600276", "report_date": "2025-12-31"},
                    "industry_hint": {"industry": "pharma"},
                    "sections": [],
                    "tables": [
                        # 跨页续表首片：物理 rows=2 但带 regulatory_milestones hint → 应进候选
                        {"index": 1, "page": 64, "line": 3, "line_end": 5, "type": None,
                         "headers": ["细分行业", "药品名称", "是否纳入国家医保目录"], "rows": 2,
                         "type_hint": "regulatory_milestones"},
                        # 无 hint 的 2 行表 → 仍是噪声，不进候选
                        {"index": 2, "page": 70, "line": 10, "line_end": 12, "type": None,
                         "headers": ["列甲", "列乙"], "rows": 2, "type_hint": None},
                    ],
                }
                (d / "report.md").write_text(md, encoding="utf-8")
                (d / "meta.json").write_text(json.dumps(meta, ensure_ascii=False), encoding="utf-8")
                # type=None 的记录不进 typed 分组，仅满足 materialize 的非空检查
                (d / "records.json").write_text(
                    json.dumps([{"table": 1, "page": 64, "type": None, "row_label": "化学制药", "values": []}],
                               ensure_ascii=False), encoding="utf-8")
                w.materialize_tables(sha, out_name="result-UT3", force=True)
                cand = w.read_json(d / "result-UT3" / "promote_candidates.json", {})
                cand_ids = {c.get("table_id") for c in cand.get("candidates") or []}
                self.assertIn("generic_table_p064_i001", cand_ids)
                self.assertNotIn("generic_table_p070_i002", cand_ids)
            finally:
                os.environ.pop(w.CACHE_ENV, None)

    def test_materialize_excludes_toc_and_glossary_candidates(self):
        with tempfile.TemporaryDirectory() as td:
            import os

            os.environ[w.CACHE_ENV] = td
            try:
                sha = "tocgloss12345"
                d = w.entry_dir(sha)
                d.mkdir(parents=True, exist_ok=True)
                md = "\n".join([
                    "<!-- page:3 -->", "",
                    "## 目录",
                    "| 术语 | 释义 ....... |",
                    "|---|---|",
                    "| 第一节 | 释义 ....... 3 |",
                    "| 第二节 | 释义 ....... 8 |",
                    "<!-- page:4 -->", "",
                    "## 释义",
                    "| 词语 | 指 | 含义 |",
                    "|---|---|---|",
                    "| 公司或本公司 | 指 | 江苏某药业股份有限公司 |",
                    "| 报告期 | 指 | 2025 年度 |",
                    "<!-- page:40 -->", "",
                    "## 经营表",
                    "| 指标 | 值1 | 值2 |",
                    "|---|---|---|",
                    "| 行A | 1 | 2 |",
                    "| 行B | 3 | 4 |",
                    "| 行C | 5 | 6 |",
                ])
                meta = {
                    "source": {"title": "测试年报", "symbol": "600276", "report_date": "2025-12-31"},
                    "industry_hint": {"industry": "pharma"},
                    "sections": [],
                    "tables": [
                        {"index": 0, "page": 3, "line": 3, "line_end": 6, "type": None,
                         "headers": ["术语", "释义"], "rows": 3, "nearby_title": "目录"},
                        {"index": 1, "page": 4, "line": 10, "line_end": 13, "type": None,
                         "headers": ["词语", "指", "含义"], "rows": 3, "nearby_title": "释义"},
                        {"index": 2, "page": 40, "line": 17, "line_end": 21, "type": None,
                         "headers": ["指标", "值1", "值2"], "rows": 4},
                    ],
                }
                (d / "report.md").write_text(md, encoding="utf-8")
                (d / "meta.json").write_text(json.dumps(meta, ensure_ascii=False), encoding="utf-8")
                (d / "records.json").write_text(json.dumps(
                    [{"table": 2, "page": 40, "type": None, "row_label": "行A", "values": []}],
                    ensure_ascii=False), encoding="utf-8")
                w.materialize_tables(sha, out_name="result-TOC", force=True)
                cand = w.read_json(d / "result-TOC" / "promote_candidates.json", {})
                cand_ids = {c.get("table_id") for c in cand.get("candidates") or []}
                self.assertNotIn("generic_table_p003_i000", cand_ids)  # 目录点线表
                self.assertNotIn("generic_table_p004_i001", cand_ids)  # 术语释义表
                self.assertIn("generic_table_p040_i002", cand_ids)
            finally:
                os.environ.pop(w.CACHE_ENV, None)

    def test_materialize_hint_contagion_and_merge(self):
        # 恒瑞新药注册表形态：首片带 hint、续片表头被数据吞掉 hint 丢失 → 传染 + 相邻片合并
        with tempfile.TemporaryDirectory() as td:
            import os

            os.environ[w.CACHE_ENV] = td
            try:
                sha = "contagion1234"
                d = w.entry_dir(sha)
                d.mkdir(parents=True, exist_ok=True)
                md = "\n".join([
                    "<!-- page:64 -->", "",
                    "| 细分行业 | 药品名称 | 是否纳入国家医保目录 |",
                    "|---|---|---|",
                    "| 化学制药 | 药A | 是 |",
                    "<!-- page:65 -->", "",
                    "| 化学制药 | 药B | 否 |",
                    "|---|---|---|",
                    "| 化学制药 | 药C | 是 |",
                    "<!-- page:66 -->", "",
                    "| 化学制药 | 药D | 是 |",
                    "|---|---|---|",
                    "| 生物制药 | 药E | 否 |",
                ])
                meta = {
                    "source": {"title": "测试年报", "symbol": "600276", "report_date": "2025-12-31"},
                    "industry_hint": {"industry": "pharma"},
                    "sections": [],
                    "tables": [
                        {"index": 0, "page": 64, "line": 2, "line_end": 4, "type": None,
                         "headers": ["细分行业", "药品名称", "是否纳入国家医保目录"], "rows": 2,
                         "type_hint": "regulatory_milestones"},
                        {"index": 1, "page": 65, "line": 7, "line_end": 9, "type": None,
                         "headers": ["化学制药", "药B", "否"], "rows": 2, "type_hint": None},
                        {"index": 2, "page": 66, "line": 12, "line_end": 14, "type": None,
                         "headers": ["化学制药", "药D", "是"], "rows": 2, "type_hint": None},
                    ],
                }
                (d / "report.md").write_text(md, encoding="utf-8")
                (d / "meta.json").write_text(json.dumps(meta, ensure_ascii=False), encoding="utf-8")
                (d / "records.json").write_text(json.dumps(
                    [{"table": 0, "page": 64, "type": None, "row_label": "药A", "values": []}],
                    ensure_ascii=False), encoding="utf-8")
                w.materialize_tables(sha, out_name="result-CT", force=True)
                cand = w.read_json(d / "result-CT" / "promote_candidates.json", {})
                first = next(c for c in cand.get("candidates") or []
                             if c.get("type_hint") == "regulatory_milestones")
                self.assertTrue(first["table_id"].startswith("generic_merged_regulatory_milestones_"))
                self.assertEqual(first["row_count"], 5)  # 药A~E 全部行
                merged = w.read_json(d / "result-CT" / "tables" / f"{first['table_id']}.json", {})
                self.assertEqual(merged.get("method"), "merge_fragments")
                self.assertEqual(sorted(merged.get("provenance", {}).get("pages") or []), [64, 65, 66])
                self.assertEqual(len(merged.get("merged_from") or []), 3)
            finally:
                os.environ.pop(w.CACHE_ENV, None)

    def test_materialize_header_echo_not_recovered(self):
        # 表头回声护栏：传染片首行与簇首片表头高度重叠（逐页重复同款表头，如担保明细）
        # 不得被回收为数据行——只回收真正的数据首行（上例药B 形态）
        with tempfile.TemporaryDirectory() as td:
            import os
            os.environ[w.CACHE_ENV] = td
            try:
                sha = "headerecho12"
                d = w.entry_dir(sha)
                d.mkdir(parents=True, exist_ok=True)
                md = "\n".join([
                    "<!-- page:10 -->", "",
                    "| 担保对象 | 担保金额 |",
                    "|---|---|",
                    "| 甲公司 | 100 |",
                    "<!-- page:11 -->", "",
                    "| 担保对象 | 担保金额 |",
                    "|---|---|",
                    "| 乙公司 | 200 |",
                ])
                meta = {
                    "source": {"title": "测试年报", "symbol": "000002", "report_date": "2025-12-31"},
                    "industry_hint": {"industry": "real_estate"},
                    "sections": [],
                    "tables": [
                        {"index": 0, "page": 10, "line": 2, "line_end": 4, "type": None,
                         "headers": ["担保对象", "担保金额"], "rows": 2, "type_hint": "guarantees"},
                        {"index": 1, "page": 11, "line": 7, "line_end": 9, "type": None,
                         "headers": ["担保对象", "担保金额"], "rows": 2, "type_hint": None},
                    ],
                }
                (d / "report.md").write_text(md, encoding="utf-8")
                (d / "meta.json").write_text(json.dumps(meta, ensure_ascii=False), encoding="utf-8")
                (d / "records.json").write_text(json.dumps(
                    [{"table": 0, "page": 10, "type": None, "row_label": "甲公司", "values": []}],
                    ensure_ascii=False), encoding="utf-8")
                w.materialize_tables(sha, out_name="result-HE", force=True)
                cand = w.read_json(d / "result-HE" / "promote_candidates.json", {})
                first = next(c for c in cand.get("candidates") or []
                             if c.get("type_hint") == "guarantees")
                merged = w.read_json(d / "result-HE" / "tables" / f'{first["table_id"]}.json', {})
                items = [r.get("item") for r in merged.get("rows") or []]
                self.assertNotIn("担保对象", items)  # 表头回声不得混入数据行
                self.assertIn("乙公司", items)
            finally:
                os.environ.pop(w.CACHE_ENV, None)

    def test_materialize_force_preserves_manual_overrides(self):
        with tempfile.TemporaryDirectory() as td:
            import os

            os.environ[w.CACHE_ENV] = td
            try:
                sha = "override12345"
                d = w.entry_dir(sha)
                d.mkdir(parents=True, exist_ok=True)
                md = "\n".join([
                    "<!-- page:31 -->", "",
                    "## 其他表",
                    "| 自定义列 | 值1 |",
                    "|---|---|",
                    "| 行A | 1 |",
                    "| 行B | 2 |",
                    "| 行C | 3 |",
                ])
                meta = {
                    "source": {"title": "测试年报", "symbol": "000001", "report_date": "2025-12-31"},
                    "industry_hint": {"industry": "pharma"},
                    "sections": [],
                    "tables": [
                        {"index": 1, "page": 31, "line": 3, "line_end": 7, "type": None,
                         "headers": ["自定义列", "值1"], "rows": 4},
                    ],
                }
                (d / "report.md").write_text(md, encoding="utf-8")
                (d / "meta.json").write_text(json.dumps(meta, ensure_ascii=False), encoding="utf-8")
                (d / "records.json").write_text(json.dumps(
                    [{"table": 1, "page": 31, "type": None, "row_label": "行A", "values": []}],
                    ensure_ascii=False), encoding="utf-8")
                w.materialize_tables(sha, out_name="result-OV", force=True)
                rd = d / "result-OV"
                # 模拟 Agent 手工闭环：narrative 落盘 + gaps 显式判定 + manifest 回填
                (rd / "narratives" / "pipeline_progress.json").write_text(json.dumps({
                    "narrative_id": "pipeline_progress", "status": "found",
                    "quote": "附表：报告期 3 项获批", "page": 31}, ensure_ascii=False), encoding="utf-8")
                gaps = json.loads((rd / "gaps.json").read_text(encoding="utf-8"))
                for g in gaps:
                    if g.get("id") == "pipeline_progress":
                        g.update({"status": "found", "evidence": "narratives/pipeline_progress.json"})
                    if g.get("id") == "cdmo_order_visibility":
                        g.update({"status": "not_applicable", "reason": "非 CDMO 业务"})
                (rd / "gaps.json").write_text(json.dumps(gaps, ensure_ascii=False), encoding="utf-8")
                man = json.loads((rd / "manifest.json").read_text(encoding="utf-8"))
                for n in man["catalog"]["narratives"]:
                    if n.get("id") == "pipeline_progress":
                        n["status"] = "found"
                (rd / "manifest.json").write_text(json.dumps(man, ensure_ascii=False), encoding="utf-8")
                # --force 重建：手工层应幸存
                w.materialize_tables(sha, out_name="result-OV", force=True)
                ov = json.loads((rd / "narratives" / "pipeline_progress.json").read_text(encoding="utf-8"))
                self.assertEqual(ov.get("status"), "found")
                gaps2 = json.loads((rd / "gaps.json").read_text(encoding="utf-8"))
                by_id = {g.get("id"): g for g in gaps2}
                self.assertEqual(by_id["pipeline_progress"]["status"], "found")
                self.assertIn("evidence", by_id["pipeline_progress"])
                self.assertEqual(by_id["cdmo_order_visibility"]["status"], "not_applicable")
                # 无手工版的条目回到机器初始态
                self.assertEqual(by_id["mda_business"]["status"], "pending")
                man2 = json.loads((rd / "manifest.json").read_text(encoding="utf-8"))
                pn = {n.get("id"): n for n in man2["catalog"]["narratives"]}
                self.assertEqual(pn["pipeline_progress"]["status"], "found")
                self.assertTrue(pn["pipeline_progress"].get("replayed_override"))
            finally:
                os.environ.pop(w.CACHE_ENV, None)

    def test_shareholder_nature_not_top_holders(self):
        notes = "\n".join([
            "| 公司名称 | 股东性质 | 持股比例 |",
            "|---|---|---|",
            "| 某子公司 | 境内非国有法人 | 100 |",
            "| 另一子公司 | 境内非国有法人 | 80 |",
        ])
        md_lines = ("<!-- page:149 -->\n\n" + notes).split("\n")
        tables = w.find_tables(md_lines)
        self.assertNotEqual(tables[0]["type"], "top_holders")

    def test_apply_promotions_and_qa_demote(self):
        with tempfile.TemporaryDirectory() as td:
            import os

            os.environ[w.CACHE_ENV] = td
            try:
                sha = "promoqa123456"
                d = w.entry_dir(sha)
                d.mkdir(parents=True, exist_ok=True)
                meta = {
                    "source": {"title": "某公司2024年年度报告", "report_date": "2024-12-31"},
                    "filing_kind": "annual",
                    "industry_hint": {"industry": "automobile"},
                    "tables": [
                        {"index": 1, "page": 36, "line": 0, "line_end": 4, "type": None,
                         "headers": ["车型", "销量", "产量"], "rows": 3, "type_hint": "nev_sales"},
                    ],
                }
                md = "\n".join([
                    "<!-- page:36 -->", "## 新能源销量",
                    "| 车型 | 销量 | 产量 |",
                    "|---|---|---|",
                    "| 新能源车 | 322202 | 325389 |",
                    "| 采购产品 | 2620603 | 609 |",
                    "| 行C | 1 | 2 |",
                ])
                (d / "report.md").write_text(md, encoding="utf-8")
                (d / "meta.json").write_text(json.dumps(meta, ensure_ascii=False), encoding="utf-8")
                (d / "records.json").write_text(json.dumps([
                    {"table": 1, "page": 36, "type": None, "row_label": "新能源车",
                     "values": [{"col": 1, "value": "322202", "header": "销量"}]},
                ], ensure_ascii=False), encoding="utf-8")
                w.materialize_tables(sha, out_name="result-QA", force=True)
                generic_id = "generic_table_p036_i001"
                w.apply_promotions(sha, [{
                    "table_file": f"tables/{generic_id}.json",
                    "promote_to": "nev_sales",
                    "confidence": "high",
                    "reason": "表头为销量/产量，行标签含新能源车",
                }], result_name="result-QA")
                man = w.read_json(d / "result-QA" / "manifest.json", {})
                ids = {t["id"] for t in man["catalog"]["tables"]}
                self.assertIn("nev_sales", ids)
                w.apply_qa(sha, [{"id": "nev_sales", "verdict": "demote", "reason": "row_mix_unrelated"}],
                           result_name="result-QA")
                man2 = w.read_json(d / "result-QA" / "manifest.json", {})
                ids2 = {t["id"] for t in man2["catalog"]["tables"]}
                self.assertNotIn("nev_sales", ids2)
                q = w.read_json(d / "result-QA" / "quality.json", {})
                self.assertEqual(q.get("status"), "fail")
                self.assertTrue(any(t.get("verdict") == "demote" for t in q.get("tables") or []))
            finally:
                os.environ.pop(w.CACHE_ENV, None)

    def test_apply_promotions_unique_ids_and_skip_low(self):
        with tempfile.TemporaryDirectory() as td:
            import os

            os.environ[w.CACHE_ENV] = td
            try:
                sha = "promouniq1234"
                d = w.entry_dir(sha)
                d.mkdir(parents=True, exist_ok=True)
                meta = {
                    "source": {"title": "某公司2024年年度报告"},
                    "filing_kind": "annual",
                    "tables": [
                        {"index": 10, "page": 90, "line": 2, "line_end": 6, "type": None,
                         "headers": ["关联交易内容", "2024年度"], "rows": 3, "type_hint": "related_txn"},
                        {"index": 11, "page": 91, "line": 8, "line_end": 12, "type": None,
                         "headers": ["关联交易内容", "2024年度"], "rows": 3, "type_hint": "related_txn"},
                        {"index": 12, "page": 49, "line": 14, "line_end": 18, "type": None,
                         "headers": ["会议", "审议事项"], "rows": 3},
                    ],
                }
                md = "\n".join([
                    "<!-- page:90 -->",
                    "| 关联交易内容 | 2024年度 |",
                    "|---|---|",
                    "| 采购商品 | 1 |",
                    "| 销售商品 | 2 |",
                    "| 合计 | 3 |",
                    "<!-- page:91 -->",
                    "| 关联交易内容 | 2024年度 |",
                    "|---|---|",
                    "| 提供劳务 | 4 |",
                    "| 接受劳务 | 5 |",
                    "| 合计 | 9 |",
                    "<!-- page:49 -->",
                    "| 会议 | 审议事项 |",
                    "|---|---|",
                    "| 监事会 | 限制性股票激励计划 |",
                    "| 董事会 | 公告 |",
                    "| 股东大会 | 议案 |",
                ])
                (d / "report.md").write_text(md, encoding="utf-8")
                (d / "meta.json").write_text(json.dumps(meta, ensure_ascii=False), encoding="utf-8")
                (d / "records.json").write_text(json.dumps([
                    {"table": 99, "page": 1, "type": None, "row_label": "placeholder",
                     "values": [{"col": 1, "value": "0", "header": "x"}]},
                ], ensure_ascii=False), encoding="utf-8")
                w.materialize_tables(sha, out_name="result-UNIQ", force=True)
                out = w.apply_promotions(sha, [
                    {"table_file": "tables/generic_table_p090_i010.json", "promote_to": "related_txn",
                     "confidence": "high", "reason": "关联交易内容与年度金额"},
                    {"table_file": "tables/generic_table_p091_i011.json", "promote_to": "related_txn",
                     "confidence": "high", "reason": "关联交易内容与年度金额"},
                    {"table_file": "tables/generic_table_p049_i012.json", "promote_to": "equity_incentive",
                     "confidence": "low", "reason": "会议议程含激励字样，不晋升"},
                ], result_name="result-UNIQ")
                self.assertEqual(out["applied"], 2)
                self.assertEqual(out["skipped"], 1)
                man = w.read_json(d / "result-UNIQ" / "manifest.json", {})
                ids = [t["id"] for t in man["catalog"]["tables"]]
                self.assertEqual(len(ids), len(set(ids)))
                self.assertIn("related_txn", ids)
                self.assertTrue(any(i.startswith("related_txn_p091") for i in ids))
                self.assertNotIn("equity_incentive", ids)
                self.assertTrue((d / "result-UNIQ" / "tables" / "generic_table_p049_i012.json").is_file())
            finally:
                os.environ.pop(w.CACHE_ENV, None)

    def test_apply_promotions_merges_history(self):
        with tempfile.TemporaryDirectory() as td:
            import os

            os.environ[w.CACHE_ENV] = td
            try:
                sha = "promohist1234"
                d = w.entry_dir(sha)
                d.mkdir(parents=True, exist_ok=True)
                meta = {
                    "source": {"title": "某公司2024年年度报告"},
                    "filing_kind": "annual",
                    "tables": [
                        {"index": 10, "page": 90, "line": 2, "line_end": 6, "type": None,
                         "headers": ["关联交易内容", "2024年度"], "rows": 3, "type_hint": "related_txn"},
                        {"index": 11, "page": 91, "line": 8, "line_end": 12, "type": None,
                         "headers": ["关联交易内容", "2024年度"], "rows": 3, "type_hint": "related_txn"},
                    ],
                }
                md = "\n".join([
                    "<!-- page:90 -->",
                    "| 关联交易内容 | 2024年度 |",
                    "|---|---|",
                    "| 采购商品 | 1 |",
                    "| 销售商品 | 2 |",
                    "| 合计 | 3 |",
                    "<!-- page:91 -->",
                    "| 关联交易内容 | 2024年度 |",
                    "|---|---|",
                    "| 提供劳务 | 4 |",
                    "| 接受劳务 | 5 |",
                    "| 合计 | 9 |",
                ])
                (d / "report.md").write_text(md, encoding="utf-8")
                (d / "meta.json").write_text(json.dumps(meta, ensure_ascii=False), encoding="utf-8")
                (d / "records.json").write_text(json.dumps([
                    {"table": 99, "page": 1, "type": None, "row_label": "placeholder",
                     "values": [{"col": 1, "value": "0", "header": "x"}]},
                ], ensure_ascii=False), encoding="utf-8")
                w.materialize_tables(sha, out_name="result-HIST", force=True)
                # 补晋升分多次调用：第二次不得覆写第一次的 applied 记录
                w.apply_promotions(sha, [
                    {"table_file": "tables/generic_table_p090_i010.json", "promote_to": "related_txn",
                     "confidence": "high", "reason": "第一次"},
                ], result_name="result-HIST")
                w.apply_promotions(sha, [
                    {"table_file": "tables/generic_table_p091_i011.json", "promote_to": "related_txn",
                     "confidence": "high", "reason": "第二次"},
                ], result_name="result-HIST")
                hist = w.read_json(d / "result-HIST" / "promotions_applied.json", {})
                self.assertEqual(len(hist.get("applied") or []), 2)
                # 重复执行已晋升项：src 已删 → skipped，applied 不重复
                w.apply_promotions(sha, [
                    {"table_file": "tables/generic_table_p090_i010.json", "promote_to": "related_txn",
                     "confidence": "high", "reason": "重复"},
                ], result_name="result-HIST")
                hist2 = w.read_json(d / "result-HIST" / "promotions_applied.json", {})
                self.assertEqual(len(hist2.get("applied") or []), 2)
                self.assertTrue(hist2.get("skipped"))
            finally:
                os.environ.pop(w.CACHE_ENV, None)

    def test_subsidiary_table_no_channel_hint(self):
        # 永辉实况：子公司情况表表体含「物流配送/零售」，曾误命中 sales_channel_mix
        md = "\n".join([
            "<!-- page:36 -->",
            "## 主要子公司情况",
            "| 公司名称 | 公司类型 | 主要业务 | 注册资本 | 总资产 |",
            "|---|---|---|---|---|",
            "| 甲子公司 | 子公司 | 物流配送与零售 | 10000 | 20000 |",
            "| 乙子公司 | 孙公司 | 商业配送 | 5000 | 8000 |",
            "<!-- page:37 -->",
            "| 续片 | 注册资本 | 业务性质 |",
            "|---|---|---|",
            "| 丙公司 | 3000 | 医院配送 |",
        ]).split("\n")
        hints = {t.get("type_hint") for t in w.find_tables(md)}
        self.assertNotIn("sales_channel_mix", hints)

    def test_qa_split_keeps_typed_and_fails_status(self):
        with tempfile.TemporaryDirectory() as td:
            import os

            os.environ[w.CACHE_ENV] = td
            try:
                sha = "qasplit123456"
                d = w.entry_dir(sha)
                d.mkdir(parents=True, exist_ok=True)
                result = d / "result-SPLIT"
                (result / "tables").mkdir(parents=True)
                payload = {
                    "table_id": "non_recurring",
                    "record_type": "non_recurring",
                    "unit_default": "元",
                    "schema": {"columns": [{"key": "item", "label": "项目"}]},
                    "rows": [
                        {"item": "政府补助", "c1": "1"},
                        {"item": "使用权资产", "c1": "2"},
                    ],
                    "row_count": 2,
                    "provenance": {"pages": [8], "tables": [3]},
                }
                w.write_json(result / "tables" / "non_recurring.json", payload)
                w.write_json(result / "manifest.json", {
                    "version": "0.3.2", "layout": "split_tables",
                    "catalog": {"tables": [
                        {"id": "non_recurring", "file": "tables/non_recurring.json", "group": "A"},
                    ]},
                })
                out = w.apply_qa(sha, [{
                    "id": "non_recurring", "verdict": "split",
                    "keep_items": ["政府补助"],
                    "reason": "去掉串味行",
                }], result_name="result-SPLIT")
                self.assertEqual(out["status"], "fail")
                kept = w.read_json(result / "tables" / "non_recurring.json", {})
                self.assertEqual(kept.get("row_count"), 1)
                self.assertEqual(kept["rows"][0]["item"], "政府补助")
                man = w.read_json(result / "manifest.json", {})
                ids = {t["id"] for t in man["catalog"]["tables"]}
                self.assertIn("non_recurring", ids)
                dropped = [t for t in man["catalog"]["tables"] if str(t.get("id") or "").startswith("generic_")]
                self.assertTrue(dropped)
                drop_obj = w.read_json(result / dropped[0]["file"], {})
                self.assertEqual(drop_obj["rows"][0]["item"], "使用权资产")
            finally:
                os.environ.pop(w.CACHE_ENV, None)

    def test_python_qa_variance_misaligned_demote(self):
        with tempfile.TemporaryDirectory() as td:
            import os

            os.environ[w.CACHE_ENV] = td
            try:
                sha = "qamisalign12"
                d = w.entry_dir(sha)
                d.mkdir(parents=True, exist_ok=True)
                result = d / "result-MIS"
                (result / "tables").mkdir(parents=True)
                w.write_json(result / "tables" / "variance_reasons.json", {
                    "table_id": "variance_reasons",
                    "record_type": "variance_reasons",
                    "rows": [
                        {"item": "货币资金", "value_current": "14181400741.40", "value_prior": "6.53"},
                        {"item": "存货", "value_current": "20000000000.00", "value_prior": "1.20"},
                    ],
                    "row_count": 2,
                    "provenance": {"pages": [32], "tables": [5]},
                })
                w.write_json(result / "manifest.json", {
                    "catalog": {"tables": [
                        {"id": "variance_reasons", "file": "tables/variance_reasons.json"},
                    ]},
                })
                findings = w.python_qa_findings(result)
                self.assertTrue(any(f.get("verdict") == "demote" and f.get("id") == "variance_reasons"
                                    for f in findings))
                w.apply_qa(sha, [], result_name="result-MIS")
                man = w.read_json(result / "manifest.json", {})
                ids = {t["id"] for t in man["catalog"]["tables"]}
                self.assertNotIn("variance_reasons", ids)
            finally:
                os.environ.pop(w.CACHE_ENV, None)

    def test_python_degraded_keeps_typed_pass(self):
        with tempfile.TemporaryDirectory() as td:
            import os

            os.environ[w.CACHE_ENV] = td
            try:
                sha = "qadegrade1234"
                d = w.entry_dir(sha)
                result = d / "result-DEG"
                (result / "tables").mkdir(parents=True)
                w.write_json(result / "tables" / "key_financials.json", {
                    "table_id": "key_financials",
                    "record_type": "key_financials",
                    "unit_default": "",
                    "rows": [{"item": "营业收入", "c1": "1"}],
                    "row_count": 1,
                    "schema": {"columns": [{"key": "item", "label": "项目"}]},
                    "provenance": {"pages": [3], "tables": [1]},
                })
                w.write_json(result / "manifest.json", {
                    "catalog": {"tables": [
                        {"id": "key_financials", "file": "tables/key_financials.json"},
                    ]},
                })
                out = w.apply_qa(sha, [], result_name="result-DEG")
                self.assertEqual(out["status"], "pass")
                man = w.read_json(result / "manifest.json", {})
                ids = {t["id"] for t in man["catalog"]["tables"]}
                self.assertIn("key_financials", ids)
                q = w.read_json(result / "quality.json", {})
                self.assertTrue(any(f.get("reason") == "missing_unit" for f in q.get("python_findings") or []))
                self.assertTrue(any(t.get("id") == "key_financials" and t.get("verdict") == "pass"
                                    for t in q.get("tables") or []))
            finally:
                os.environ.pop(w.CACHE_ENV, None)


class TestMetaSummary(unittest.TestCase):
    def test_summary_render(self):
        meta = {
            "cache_id": "x", "source": {"title": "T", "symbol": "S", "report_date": "2025-12-31"},
            "doc": {"pages": 10, "table_count": 3},
            "chapters": [{"anchor": "第二节 公司简介", "page": 5, "page_end": 9}],
            "sections": [{"key": "dividend", "page": 7}],
            "tables": [{"type": "dividend"}],
            "anomalies": [{"code": "no_bookmarks", "severity": "info"}],
        }
        s = w.meta_summary_text(meta)
        self.assertIn("cache_id: x", s)
        self.assertIn("第二节 公司简介(p5~9)", s)
        self.assertIn("dividend(p7)", s)
        self.assertIn("no_bookmarks[info]", s)


class TestLiveCacheRegression(unittest.TestCase):
    """本地缓存双线回归（CI 无缓存则跳过）。"""

    def _load_md(self, sha: str) -> list[str] | None:
        p = Path.home() / ".cache" / "wm-report-extract" / sha / "report.md"
        if not p.is_file():
            return None
        return p.read_text(encoding="utf-8").split("\n")

    def test_gwm_mda_outlook_and_variance_tables(self):
        md = self._load_md("5f1ef188878a")
        if md is None:
            self.skipTest("长城汽车 cache 不存在")
        ch = w.find_chapters(md)
        mda = next(c for c in ch if "管理层讨论" in (c.get("title") or ""))
        secs = {s["key"]: s for s in w.find_sections(md, ch)}
        self.assertGreaterEqual(secs["mda_outlook"]["page"], mda["page"])
        self.assertLessEqual(secs["mda_outlook"]["page"], mda.get("page_end") or 10**9)
        self.assertNotEqual(secs["mda_outlook"]["page"], 2)
        self.assertGreaterEqual(secs["risk_factors"]["page"], mda["page"])
        tables = w.find_tables(md)
        vr = [t for t in tables if t.get("type") == "variance_reasons"]
        self.assertGreaterEqual(len(vr), 2)
        recs = w.build_records(md, tables)
        segs = [r for r in recs if r.get("type") == "segments"]
        labels = {r["label_norm"] for r in segs}
        self.assertTrue({"国内", "国外"} & labels or {"销售汽车", "汽车行业"} & labels)
        sell = next((r for r in recs if r.get("label_norm") == "销售费用" and r.get("type") == "variance_reasons"), None)
        self.assertIsNotNone(sell)
        reason = " ".join(v["value"] for v in sell["values"] if "原因" in (v.get("header") or "") or "说明" in (v.get("header") or ""))
        self.assertIn("直连用户", reason)

    def test_zijin_nonferrous_live(self):
        sha = "01819e1c7daa"
        md = self._load_md(sha)
        if md is None:
            self.skipTest("紫金矿业 2025 年报 cache 不存在")
        meta_p = Path.home() / ".cache" / "wm-report-extract" / sha / "meta.json"
        if not meta_p.is_file():
            self.skipTest("紫金矿业 meta.json 不存在")
        meta = json.loads(meta_p.read_text(encoding="utf-8"))
        src = meta.get("source") or {}
        industry = w.detect_industry(
            "\n".join(md),
            title=src.get("title") or "",
            pages=(meta.get("doc") or {}).get("pages") or 0,
        )
        self.assertEqual(industry["industry"], "nonferrous")
        hints = {t.get("type_hint") for t in meta.get("tables") or []}
        self.assertIn("reserves", hints)
        self.assertIn("construction_projects", hints)

    def _latest_quality_result(self, sha: str) -> Path | None:
        d = Path.home() / ".cache" / "wm-report-extract" / sha
        if not d.is_dir():
            return None
        dirs = sorted(
            [p for p in d.glob("result-*") if (p / "quality.json").is_file()],
            key=lambda p: p.name,
        )
        # 实验目录（smoke/extract/bnbm）不抢正式产物，避免本地试跑污染断言
        formal = [p for p in dirs if not any(tag in p.name for tag in ("smoke", "extract", "bnbm"))]
        pool = formal or dirs
        return pool[-1] if pool else None

    def _typed_ids(self, result: Path) -> list[str]:
        man = json.loads((result / "manifest.json").read_text(encoding="utf-8"))
        return [
            t["id"] for t in (man.get("catalog") or {}).get("tables") or []
            if not str(t.get("id") or "").startswith("generic")
        ]

    def test_hk_horizon_adapt_and_review_live(self):
        sha = "89ca26806258"
        cache_dir = Path.home() / ".cache" / "wm-report-extract" / sha
        if not cache_dir.is_dir():
            self.skipTest("地平线 HK cache 不存在")
        meta = json.loads((cache_dir / "meta.json").read_text(encoding="utf-8"))
        result_name = "result-20260824T075500Z"
        result = cache_dir / result_name
        if not result.is_dir():
            self.skipTest("地平线 adapt/review result 不存在")
        plan = json.loads((result / "adapt_plan.json").read_text(encoding="utf-8"))
        review = json.loads((result / "review.json").read_text(encoding="utf-8"))
        self.assertEqual(w.infer_filing_kind(meta.get("source") or {}, (meta.get("doc") or {}).get("pages") or 0), "semi")
        self.assertEqual(plan["document_profile"]["market"], "hk")
        self.assertEqual(plan["document_profile"]["filing_kind"], "semi")
        self.assertEqual(review["status"], "pass")
        self.assertTrue((result / "derived" / "evolution_proposal.json").is_file())

    def test_hk_geely_adapt_and_review_live(self):
        sha = "a5ad04213e52"
        cache_dir = Path.home() / ".cache" / "wm-report-extract" / sha
        if not cache_dir.is_dir():
            self.skipTest("吉利 HK cache 不存在")
        meta = json.loads((cache_dir / "meta.json").read_text(encoding="utf-8"))
        result_name = "result-20260824T075600Z"
        result = cache_dir / result_name
        if not result.is_dir():
            self.skipTest("吉利 adapt/review result 不存在")
        plan = json.loads((result / "adapt_plan.json").read_text(encoding="utf-8"))
        review = json.loads((result / "review.json").read_text(encoding="utf-8"))
        self.assertEqual(w.infer_filing_kind(meta.get("source") or {}, (meta.get("doc") or {}).get("pages") or 0), "semi")
        self.assertEqual(plan["document_profile"]["market"], "hk")
        self.assertEqual(plan["document_profile"]["filing_kind"], "semi")
        self.assertEqual(review["status"], "pass")
        self.assertTrue((result / "derived" / "evolution_proposal.json").is_file())

    def test_gwm_2024_promote_and_qa(self):
        md = self._load_md("da4a2d594878")
        if md is None:
            self.skipTest("长城 2024 年报 cache 不存在")
        tables = w.find_tables(md)
        py_types = {t.get("type") for t in tables if t.get("type")}
        self.assertIn("executives", py_types)
        self.assertNotIn("equity_incentive", py_types)
        self.assertNotIn("overseas_ops", py_types)
        hints = {t.get("type_hint") for t in tables if t.get("type_hint")}
        self.assertTrue(hints & {"employees", "rd_investment", "related_txn", "nev_sales"})
        result = self._latest_quality_result("da4a2d594878")
        if result is None:
            self.skipTest("长城 2024 年报 quality 产物不存在")
        typed = self._typed_ids(result)
        self.assertIn("executives", typed)
        self.assertTrue(
            any(i == "rd_investment" or i.startswith("rd_investment_") for i in typed)
            or any(i == "related_txn" or i.startswith("related_txn_") for i in typed)
            or any(i == "nev_sales" or i.startswith("nev_sales_") for i in typed)
        )
        th = next((i for i in typed if i == "top_holders" or str(i).startswith("top_holders_")), None)
        if th:
            # 0.4.1 起真股东表合法定型（17 行级别）；污染时代曾 451 条误标
            obj = json.loads((result / "tables" / f"{th}.json").read_text(encoding="utf-8"))
            self.assertLessEqual(obj.get("row_count") or 0, 40)
        for tid in typed:
            if not str(tid).startswith("equity_incentive"):
                continue
            obj = json.loads((result / "tables" / f"{tid}.json").read_text(encoding="utf-8"))
            self.assertLess(obj.get("row_count") or 0, 80)

    def test_gwm_2025_promote_and_qa(self):
        md = self._load_md("5f1ef188878a")
        if md is None:
            self.skipTest("长城 2025 年报 cache 不存在")
        py_types = {t.get("type") for t in w.find_tables(md) if t.get("type")}
        self.assertIn("executives", py_types)
        self.assertNotIn("equity_incentive", py_types)
        self.assertNotIn("overseas_ops", py_types)
        result = self._latest_quality_result("5f1ef188878a")
        if result is None:
            self.skipTest("长城 2025 年报 quality 产物不存在")
        typed = self._typed_ids(result)
        self.assertIn("executives", typed)
        self.assertTrue(
            any(i == "rd_investment" or i.startswith("rd_investment_") for i in typed)
            or any(i == "related_txn" or i.startswith("related_txn_") for i in typed)
        )
        th = next((i for i in typed if i == "top_holders" or str(i).startswith("top_holders_")), None)
        if th:
            # 0.4.1 起真股东表合法定型；污染时代曾数百条误标
            obj = json.loads((result / "tables" / f"{th}.json").read_text(encoding="utf-8"))
            self.assertLessEqual(obj.get("row_count") or 0, 40)
        self.assertTrue((result / "quality.json").is_file())

    def test_gwm_q1_qa_no_fake_typed(self):
        md = self._load_md("869cab8eb833")
        if md is None:
            self.skipTest("长城 2026 Q1 cache 不存在")
        py_types = {t.get("type") for t in w.find_tables(md) if t.get("type")}
        self.assertNotIn("overseas_ops", py_types)
        self.assertNotIn("equity_incentive", py_types)
        result = self._latest_quality_result("869cab8eb833")
        if result is None:
            self.skipTest("长城 2026 Q1 quality 产物不存在")
        typed = self._typed_ids(result)
        self.assertFalse(any(i == "overseas_ops" or str(i).startswith("overseas_ops_") for i in typed))
        self.assertFalse(any(i == "equity_incentive" or str(i).startswith("equity_incentive_") for i in typed))
        nr = result / "tables" / "non_recurring.json"
        if nr.is_file():
            obj = json.loads(nr.read_text(encoding="utf-8"))
            self.assertLessEqual(obj.get("row_count") or 0, 20)

    def test_gwm_q1_automobile_not_bank(self):
        meta_path = Path.home() / ".cache" / "wm-report-extract" / "869cab8eb833" / "meta.json"
        if not meta_path.is_file():
            self.skipTest("长城 2026 Q1 cache 不存在")
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        src = meta.get("source") or {}
        industry = w.detect_industry(
            "\n".join(self._load_md("869cab8eb833") or []),
            title=src.get("title") or "",
            pages=(meta.get("doc") or {}).get("pages") or 0,
        )
        self.assertEqual(industry["industry"], "automobile")
        self.assertEqual(w.infer_filing_kind(src, 15), "q1")

    def test_cmb_outlook_not_disclaimer_and_no_auto_fields(self):
        md = self._load_md("abe612a27346")
        if md is None:
            self.skipTest("招行 cache 不存在")
        ch = w.find_chapters(md)
        secs = {s["key"]: s for s in w.find_sections(md, ch)}
        self.assertIn("mda_outlook", secs)
        self.assertNotIn("实质承诺", secs["mda_outlook"]["matched"])
        self.assertGreaterEqual(secs["mda_outlook"]["page"], 18)
        auto_names = ("哈弗", "魏牌", "欧拉", "坦克")
        blob = json.dumps(w.PRIORITY_GROUPS_BASE, ensure_ascii=False) + json.dumps(w.INDUSTRY_EXT_GROUPS, ensure_ascii=False)
        for name in auto_names:
            self.assertNotIn(name, blob)

    def test_industry_ext_groups_cover_shallow_industries(self):
        for key in ("insurance", "broker", "real_estate", "energy", "bank",
                    "pharma", "consumer", "transport_infrastructure", "fossil_energy",
                    "auto_electronics"):
            self.assertIn(key, w.INDUSTRY_EXT_GROUPS)
            ext = w.INDUSTRY_EXT_GROUPS[key]
            self.assertTrue(ext.get("tables"))
            self.assertTrue(ext.get("group", "").startswith("X_"))
            self.assertTrue(ext.get("required_gaps"), f"{key} must declare required_gaps")
            for tid in ext["tables"]:
                self.assertIn(tid, w.TABLE_SPEC_BY_ID)

    def test_pharma_beats_manufacturing(self):
        text = ("药品注册 一致性评价 带量采购 集中采购 创新药 仿制药 "
                "临床试验 适应症 原料药 制剂。产量 产销量 产能利用率。")
        h = w.detect_industry(text, title="某制药股份有限公司2025年年度报告", pages=220)
        self.assertEqual(h["industry"], "pharma")

    def test_device_title_not_pharma(self):
        text = ("产能利用率 产量。器械注册 体外诊断。")
        h = w.detect_industry(text, title="某医疗器械股份有限公司2025年年度报告", pages=180)
        self.assertNotEqual(h["industry"], "pharma")

    def test_consumer_beats_insurance_footnote_pollution(self):
        """年报附注常含保险合同准则词；有消费标题+渠道词时应定型 consumer。"""
        text = ("经销商 分销渠道 渠道结构 出厂价 基酒 酿造 商超。"
                "附注提及 赔付支出 退保金 原保险合同 已赚保费。产量 产销量。")
        h = w.detect_industry(text, title="某酒业股份有限公司2025年年度报告", pages=160)
        self.assertEqual(h["industry"], "consumer")

    def test_jewelry_title_not_consumer(self):
        text = ("产量 产能利用率。黄金 首饰。")
        h = w.detect_industry(text, title="某黄金珠宝有限公司2025年年度报告", pages=120)
        self.assertNotEqual(h["industry"], "consumer")

    def test_transport_highway_segment(self):
        text = ("车流量 通行费 收费公路 收费里程 通行量。房地产项目 合同负债 偶发。")
        h = w.detect_industry(text, title="某高速公路股份有限公司2025年年度报告", pages=240)
        self.assertEqual(h["industry"], "transport_infrastructure")
        self.assertEqual(h.get("transport_segment"), "highway")

    def test_transport_port_segment(self):
        text = ("货物吞吐量 集装箱吞吐量 TEU 泊位 港区 装卸。")
        h = w.detect_industry(text, title="某港口股份有限公司2025年年度报告", pages=260)
        self.assertEqual(h["industry"], "transport_infrastructure")
        self.assertEqual(h.get("transport_segment"), "port")

    def test_epc_not_transport(self):
        text = ("工程承包 施工 EPC 项目。产能利用率。")
        h = w.detect_industry(text, title="某工程建设股份有限公司2025年年度报告", pages=200)
        self.assertNotEqual(h["industry"], "transport_infrastructure")

    def test_fossil_beats_energy(self):
        text = ("原煤产量 商品煤 煤炭销量 吨煤成本 洗选 长协 市场煤。"
                "装机容量 发电量 售电量 利用小时。")
        h = w.detect_industry(text, title="某煤业股份有限公司2025年年度报告", pages=260)
        self.assertEqual(h["industry"], "fossil_energy")

    def test_nonferrous_beats_fossil(self):
        text = ("有色金属 矿产铜 电解铝 冶炼 保有储量 资源量 精矿 矿山。"
                "原煤产量 商品煤。产量 产销量。")
        h = w.detect_industry(text, title="某铜业股份有限公司2025年年度报告", pages=250)
        self.assertEqual(h["industry"], "nonferrous")

    def test_pharma_type_hints(self):
        md = "\n".join([
            "<!-- page:20 -->",
            "## 在研项目",
            "| 项目 | 适应症 | 临床阶段 |",
            "|---|---|---|",
            "| A药 | 肿瘤 | III期 |",
            "<!-- page:21 -->",
            "## 注册进展",
            "| 品种 | 一致性评价 | 通过 |",
            "|---|---|---|",
            "| B药 | 一致性评价 | 通过 |",
            "<!-- page:22 -->",
            "## 销售渠道",
            "| 渠道 | 医院 | 占比 |",
            "|---|---|---|",
            "| 医院 | 100 | 60 |",
            "<!-- page:23 -->",
            "## GMP 产能",
            "| 基地 | GMP | 生产基地 |",
            "|---|---|---|",
            "| 一厂 | GMP | 生产基地 |",
            # 恒瑞附表5 式表头：无「在研项目」，靠 药品名称+靶点+适应症 命中
            "<!-- page:24 -->",
            "| 治疗领域 | 药品名称 | 靶点 | 适应症 | I 期 |",
            "|---|---|---|---|---|",
            "| 肿瘤 | A单抗 | PD-L1 | 二线NSCLC | III 期 |",
        ]).split("\n")
        hints = {t.get("type_hint") for t in w.find_tables(md)}
        self.assertTrue({"rd_pipeline", "regulatory_milestones", "sales_channel_mix", "capacity_gmp"} <= hints)

    def test_consumer_type_hints(self):
        md = "\n".join([
            "<!-- page:30 -->",
            "| 渠道 | 销售收入 | 占比 |",
            "|---|---|---|",
            "| 直营 | 100 | 40% |",
            "<!-- page:31 -->",
            "| 区域 | 经销商 | 数量 |",
            "|---|---|---|",
            "| 华东 | 经销商 | 数量 |",
            "<!-- page:32 -->",
            "| 指标 | 门店 | 新开 |",
            "|---|---|---|",
            "| 本期 | 门店 | 新开 |",
            "<!-- page:33 -->",
            "| 指标 | 同店 | 增长 |",
            "|---|---|---|",
            "| 超市 | 同店 | 增长 |",
        ]).split("\n")
        hints = {t.get("type_hint") for t in w.find_tables(md)}
        self.assertTrue(
            {"retail_channel_mix", "dealer_network", "store_operations", "same_store_sales"} <= hints
        )

    def test_transport_type_hints(self):
        md = "\n".join([
            "<!-- page:40 -->",
            "| 路段 | 通行量 | 通行费 |",
            "|---|---|---|",
            "| 沪宁 | 100 | 50 |",
            "<!-- page:41 -->",
            "| 项目 | 收费公路里程 | 特许经营权 |",
            "|---|---|---|",
            "| 合计 | 1000 | 特许经营权 |",
            "<!-- page:42 -->",
            "| 港区 | 货物吞吐量 | 集装箱 |",
            "|---|---|---|",
            "| 洋山 | 100 | 50 |",
            "<!-- page:43 -->",
            "| 港区 | 泊位 | 港区 |",
            "|---|---|---|",
            "| 外高桥 | 泊位 | 港区 |",
        ]).split("\n")
        hints = {t.get("type_hint") for t in w.find_tables(md)}
        self.assertTrue(
            {"highway_toll_traffic", "concession_network_assets",
             "port_throughput", "port_berth_assets"} <= hints
        )

    def test_fossil_type_hints(self):
        md = "\n".join([
            "<!-- page:50 -->",
            "## 煤炭产销",
            "| 项目 | 原煤产量 | 商品煤 |",
            "|---|---|---|",
            "| 合计 | 100 | 80 |",
            "<!-- page:51 -->",
            "## 储量",
            "| 矿井 | 煤炭资源量 | 可采储量 |",
            "|---|---|---|",
            "| A矿 | 100 | 50 |",
            "<!-- page:52 -->",
            "## 吨煤成本",
            "| 项目 | 吨煤 | 完全成本 |",
            "|---|---|---|",
            "| 现金 | 吨煤 | 完全成本 |",
            "<!-- page:53 -->",
            "## 油气产量",
            "| 项目 | 原油产量 | 天然气 |",
            "|---|---|---|",
            "| 合计 | 100 | 50 |",
            "<!-- page:54 -->",
            "## 储量分级",
            "| 项目 | 证实储量 | 探明 |",
            "|---|---|---|",
            "| 原油 | 证实储量 | 探明 |",
            "<!-- page:55 -->",
            "## 单位成本",
            "| 项目 | 桶油 | 成本 |",
            "|---|---|---|",
            "| 操作 | 桶油 | 成本 |",
        ]).split("\n")
        hints = {t.get("type_hint") for t in w.find_tables(md)}
        self.assertTrue(
            {"coal_production", "coal_reserves", "coal_cost_price",
             "hydrocarbon_production", "hydrocarbon_reserves", "lifting_cost"} <= hints
        )

    def test_pharma_annual_narratives_and_gaps(self):
        with tempfile.TemporaryDirectory() as td:
            import os
            os.environ[w.CACHE_ENV] = td
            try:
                sha = "phannual0001"
                d = w.entry_dir(sha)
                d.mkdir(parents=True, exist_ok=True)
                meta = {
                    "source": {"title": "某制药公司2025年年度报告"},
                    "filing_kind": "annual",
                    "industry_hint": {"industry": "pharma"},
                    "doc": {"pages": 220},
                    "tables": [],
                }
                (d / "meta.json").write_text(json.dumps(meta, ensure_ascii=False), encoding="utf-8")
                (d / "records.json").write_text(json.dumps([{
                    "table": 0, "page": 1, "type": "key_financials", "row_label": "营业收入",
                    "values": [{"col": 1, "value": "100", "header": "本期"}],
                }], ensure_ascii=False), encoding="utf-8")
                w.materialize_tables(sha, out_name="result-PH", force=True)
                man = w.read_json(d / "result-PH" / "manifest.json", {})
                narr = {n["id"] for n in man.get("catalog", {}).get("narratives", [])
                        if n.get("group") == "X_pharma"}
                self.assertEqual(narr, {"pipeline_progress", "vbp_policy_impact"})
                gaps = w.read_json(d / "result-PH" / "gaps.json", [])
                gids = {g["id"] for g in gaps if g.get("status") == "required"}
                self.assertTrue(
                    {"key_product_pricing", "market_share_estimate", "sales_force_scale",
                     "innovative_vs_generic_mix", "cdmo_order_visibility"} <= gids
                )
            finally:
                os.environ.pop(w.CACHE_ENV, None)

    def test_transport_segment_gaps(self):
        with tempfile.TemporaryDirectory() as td:
            import os
            os.environ[w.CACHE_ENV] = td
            try:
                sha = "trannual0001"
                d = w.entry_dir(sha)
                d.mkdir(parents=True, exist_ok=True)
                meta = {
                    "source": {"title": "某高速公路公司2025年年度报告"},
                    "filing_kind": "annual",
                    "industry_hint": {"industry": "transport_infrastructure",
                                      "transport_segment": "highway"},
                    "doc": {"pages": 240},
                    "tables": [],
                }
                (d / "meta.json").write_text(json.dumps(meta, ensure_ascii=False), encoding="utf-8")
                (d / "records.json").write_text(json.dumps([{
                    "table": 0, "page": 1, "type": "key_financials", "row_label": "营业收入",
                    "values": [{"col": 1, "value": "100", "header": "本期"}],
                }], ensure_ascii=False), encoding="utf-8")
                w.materialize_tables(sha, out_name="result-TR", force=True)
                gaps = w.read_json(d / "result-TR" / "gaps.json", [])
                by_id = {g["id"]: g for g in gaps}
                self.assertEqual(by_id["etc_traffic_mix"]["status"], "required")
                self.assertEqual(by_id["toll_per_vehicle_text"]["status"], "required")
                self.assertEqual(by_id["berth_utilization"]["status"], "not_applicable")
                self.assertEqual(by_id["hinterland_economy"]["status"], "not_applicable")
            finally:
                os.environ.pop(w.CACHE_ENV, None)

    def test_consumer_promotion(self):
        with tempfile.TemporaryDirectory() as td:
            import os
            os.environ[w.CACHE_ENV] = td
            try:
                sha = "cspromo0001"
                d = w.entry_dir(sha)
                d.mkdir(parents=True, exist_ok=True)
                meta = {
                    "source": {"title": "某消费公司2025年年度报告"},
                    "filing_kind": "annual",
                    "industry_hint": {"industry": "consumer"},
                    "tables": [
                        {"index": 1, "page": 40, "line": 0, "line_end": 6, "type": None,
                         "headers": ["渠道", "销售收入", "占比"], "rows": 3,
                         "type_hint": "retail_channel_mix"},
                    ],
                }
                md = "\n".join([
                    "<!-- page:40 -->", "## 渠道结构",
                    "| 渠道 | 销售收入 | 占比 |",
                    "|---|---|---|",
                    "| 直营 | 100 | 40% |",
                    "| 经销 | 150 | 60% |",
                    "| 合计 | 250 | 100% |",
                ])
                (d / "report.md").write_text(md, encoding="utf-8")
                (d / "meta.json").write_text(json.dumps(meta, ensure_ascii=False), encoding="utf-8")
                (d / "records.json").write_text(json.dumps([
                    {"table": 1, "page": 40, "type": None, "row_label": "直营",
                     "values": [{"col": 1, "value": "100", "header": "销售收入"}]},
                    {"table": 1, "page": 40, "type": None, "row_label": "经销",
                     "values": [{"col": 1, "value": "150", "header": "销售收入"}]},
                    {"table": 1, "page": 40, "type": None, "row_label": "合计",
                     "values": [{"col": 1, "value": "250", "header": "销售收入"}]},
                ], ensure_ascii=False), encoding="utf-8")
                w.materialize_tables(sha, out_name="result-CS", force=True)
                generic_id = "generic_table_p040_i001"
                w.apply_promotions(sha, [{
                    "table_file": f"tables/{generic_id}.json",
                    "promote_to": "retail_channel_mix",
                    "confidence": "high",
                    "reason": "表头含销售收入与渠道",
                }], result_name="result-CS")
                man = w.read_json(d / "result-CS" / "manifest.json", {})
                ids = {t["id"] for t in man["catalog"]["tables"]}
                self.assertIn("retail_channel_mix", ids)
            finally:
                os.environ.pop(w.CACHE_ENV, None)

    def _detect_cache(self, sha: str):
        d = Path.home() / ".cache" / "wm-report-extract" / sha
        meta_p = d / "meta.json"
        fetch_p = d / "fetch_meta.json"
        pdf = d / "report.pdf"
        md_p = d / "report.md"
        if md_p.is_file():
            meta = json.loads(meta_p.read_text(encoding="utf-8")) if meta_p.is_file() else {}
            src = meta.get("source") or {}
            if fetch_p.is_file() and not src:
                src = (json.loads(fetch_p.read_text(encoding="utf-8")).get("source") or {})
            pages = (meta.get("doc") or {}).get("pages") or 0
            text = md_p.read_text(encoding="utf-8", errors="ignore")
            if len(text) > 120_000:
                text = text[:80_000] + text[-40_000:]
            return w.detect_industry(text, title=src.get("title") or "", pages=pages)
        if not pdf.is_file():
            return None
        import fitz
        fm = json.loads(fetch_p.read_text(encoding="utf-8")) if fetch_p.is_file() else {}
        title = (fm.get("source") or {}).get("title") or ""
        doc = fitz.open(pdf)
        pages = doc.page_count
        idxs = list(range(min(40, pages))) + list(range(max(0, pages // 2), min(pages, pages // 2 + 20)))
        text = "\n".join(doc.load_page(i).get_text("text") for i in sorted(set(idxs)))
        doc.close()
        return w.detect_industry(text, title=title, pages=pages)

    def test_dianmei_stays_nonferrous_not_energy(self):
        h = self._detect_cache("d68752f707d0")
        if h is None:
            self.skipTest("电投能源 cache 不存在")
        self.assertEqual(h["industry"], "nonferrous")

    def test_pingan_insurance_live(self):
        h = self._detect_cache("860c455bbad9")
        if h is None:
            self.skipTest("中国平安 2025 年报 cache 不存在")
        self.assertEqual(h["industry"], "insurance")

    def test_citic_broker_live(self):
        h = self._detect_cache("438f2a53dcf4")
        if h is None:
            self.skipTest("中信证券 2025 年报 cache 不存在")
        self.assertEqual(h["industry"], "broker")

    def test_vanke_real_estate_live(self):
        h = self._detect_cache("b2befc9da2a9")
        if h is None:
            self.skipTest("万科A 2025 年报 cache 不存在")
        self.assertEqual(h["industry"], "real_estate")

    def test_cyjdl_energy_live(self):
        h = self._detect_cache("aa0cdb92e3aa")
        if h is None:
            self.skipTest("长江电力 2025 年报 cache 不存在")
        self.assertEqual(h["industry"], "energy")

    def test_dunan_machinery_live(self):
        sha = "b8dd4f1f0f15"
        h = self._detect_cache(sha)
        if h is None:
            self.skipTest("盾安环境 2025 年报 cache 不存在")
        self.assertEqual(h["industry"], "machinery")
        meta_p = Path.home() / ".cache" / "wm-report-extract" / sha / "meta.json"
        meta = json.loads(meta_p.read_text(encoding="utf-8"))
        hints = {t.get("type_hint") for t in (meta.get("tables") or []) if t.get("type_hint")}
        for req in ("employees", "rd_investment", "related_txn"):
            self.assertIn(req, hints, msg=f"missing scan type_hint {req}")

    def test_dunan_closure_live(self):
        sha = "b8dd4f1f0f15"
        result = Path.home() / ".cache" / "wm-report-extract" / sha / "result-DA"
        if not result.is_dir():
            self.skipTest("盾安 result-DA 不存在")
        gaps = json.loads((result / "gaps.json").read_text(encoding="utf-8"))
        for g in gaps:
            self.assertEqual(g.get("status"), "found", msg=g.get("id"))
        quality = json.loads((result / "quality.json").read_text(encoding="utf-8"))
        self.assertEqual(quality.get("status"), "pass")
        self.assertEqual(quality.get("narrative_kpi_findings") or [], [])
        promos = json.loads((result / "promotions_applied.json").read_text(encoding="utf-8"))
        applied_types = {a.get("type") for a in (promos.get("applied") or [])}
        for req in ("employees", "rd_investment", "related_txn"):
            self.assertIn(req, applied_types)
        for tid in ("employees", "rd_investment", "related_txn"):
            self.assertTrue((result / "tables" / f"{tid}.json").is_file())

    def test_shenhuo_nonferrous_live(self):
        sha = "a666703bc261"
        h = self._detect_cache(sha)
        if h is None:
            self.skipTest("神火股份 2025 年报 cache 不存在")
        self.assertEqual(h["industry"], "nonferrous")
        meta_p = Path.home() / ".cache" / "wm-report-extract" / sha / "meta.json"
        meta = json.loads(meta_p.read_text(encoding="utf-8"))
        hints = {t.get("type_hint") for t in (meta.get("tables") or []) if t.get("type_hint")}
        for req in ("employees", "rd_investment", "related_txn", "construction_projects", "hedging"):
            self.assertIn(req, hints, msg=f"missing scan type_hint {req}")

    def test_shenhuo_closure_live(self):
        sha = "a666703bc261"
        result = Path.home() / ".cache" / "wm-report-extract" / sha / "result-SH"
        if not result.is_dir():
            self.skipTest("神火 result-SH 不存在")
        gaps = json.loads((result / "gaps.json").read_text(encoding="utf-8"))
        for g in gaps:
            self.assertEqual(g.get("status"), "found", msg=g.get("id"))
        quality = json.loads((result / "quality.json").read_text(encoding="utf-8"))
        self.assertEqual(quality.get("status"), "pass")
        self.assertEqual(quality.get("narrative_kpi_findings") or [], [])
        promos = json.loads((result / "promotions_applied.json").read_text(encoding="utf-8"))
        applied_types = {a.get("type") for a in (promos.get("applied") or [])}
        for req in ("employees", "rd_investment", "related_txn", "construction_projects", "hedging"):
            self.assertIn(req, applied_types)
        for tid in ("employees", "rd_investment", "related_txn", "construction_projects", "hedging"):
            self.assertTrue((result / "tables" / f"{tid}.json").is_file())

    def test_gwm_l2_resolve_contract_liabilities(self):
        sha = "5f1ef188878a"
        result = self._latest_quality_result(sha)
        if result is None:
            self.skipTest("长城 2025 年报 quality 产物不存在")

        w.cmd_resolve([
            sha,
            "--need", "合同负债",
            "--result", result.name,
            "--write-fields",
            "--max-hits", "10",
        ])

        field_id = w._field_id_from_need("合同负债")
        field_path = result / "fields" / f"{field_id}.json"
        self.assertTrue(field_path.is_file())
        field_obj = json.loads(field_path.read_text(encoding="utf-8"))
        self.assertEqual(field_obj.get("status"), "found")
        self.assertIn("合同负债", field_obj.get("label") or "")
        self.assertIsNotNone((field_obj.get("source") or {}).get("quote"))

        # 0.5.0 baseline：长城 2025 年报合并资产负债表合同负债期末 = 13,157,259,156.48 元 ≈ 131.57 亿
        expected_yi = 131.57
        raw_val = (field_obj.get("value") or "").replace(",", "").strip()
        actual = float(raw_val) if raw_val else 0.0
        actual_yi = actual / 1e8 if abs(actual) > 1e6 else actual
        self.assertAlmostEqual(actual_yi, expected_yi, delta=max(0.2, expected_yi * 0.005))


class TestFitzTrack(unittest.TestCase):
    """①b fitz 轨道：矩阵转 md、签名行过滤、合并路由、ACCURATE 精修选页。"""

    def test_matrix_to_md_col0_fill_and_sep(self):
        matrix = [
            ["项目", "2024年", None],
            ["货币资金", "1,234.56", "789.00"],
            [None, "10.00", "20.00"],
        ]
        md, bboxes = w.fitz_matrix_to_md(matrix, [[0, 0, 10, 5], [0, 5, 10, 8], None])
        lines = [ln for ln in md.splitlines() if ln.startswith("|")]
        self.assertEqual(len(lines), 4)  # 表头 + 分隔 + 2 数据行
        self.assertIn("- ", lines[1])
        self.assertTrue(lines[2].startswith("| 货币资金 |"))
        self.assertTrue(lines[3].startswith("| 货币资金 |"))  # 首列跨行合并下填
        self.assertEqual(bboxes[0], [0, 0, 10, 5])
        self.assertIsNone(bboxes[2])

    def test_matrix_to_md_header_stack_and_right_fill(self):
        matrix = [
            ["项目", "2024年12月31日", None],
            ["附注", "期末余额", "期初余额"],
            ["货币资金", "100.00", "200.00"],
        ]
        md, bboxes = w.fitz_matrix_to_md(matrix, [[0, 0, 10, 5], [0, 5, 10, 8], [0, 8, 10, 11]])
        header = md.splitlines()[0]
        self.assertIn("2024年12月31日期末余额", header)
        self.assertIn("2024年12月31日期初余额", header)  # 列跨右填充后堆叠
        self.assertEqual(len(bboxes), 2)  # 两行表头堆叠为一行

    def test_matrix_to_md_signature_filter(self):
        matrix = [
            ["项目", "金额"],
            ["营业收入", "100"],
            ["", "财务负责人：张三　董事会秘书：李四"],
        ]
        md, _ = w.fitz_matrix_to_md(matrix)
        self.assertNotIn("财务负责人", md)
        self.assertIn("营业收入", md)

    def test_strip_signature_rows_md(self):
        md = "| 项目 | 金额 |\n| --- | --- |\n| 收入 | 100 |\n|  | 财务负责人：张三 |"
        out = w.strip_signature_rows(md)
        self.assertNotIn("财务负责人", out)
        self.assertIn("| 收入 | 100 |", out)

    def test_merge_fitz_track_replace_keep_add(self):
        events = [
            {"kind": "text", "label": "text", "page": 1, "text": "正文"},
            {"kind": "table", "label": "table", "page": 1,
             "text": "| a | b |\n| --- | --- |\n| 100.00 | 200.00 |"},
            {"kind": "table", "label": "table", "page": 2,
             "text": "| x | y |\n| --- | --- |\n| 300.00 | 400.00 |\n| 500.00 | 600.00 |"},
            {"kind": "text", "label": "text", "page": 3, "text": "docling 漏检页"},
        ]
        fitz_tables = {
            1: [{"matrix": [["a", "b"], ["100.00", "200.00"], ["999.00", "888.00"]],
                 "bbox": [1, 2, 3, 4], "row_bboxes": [], "rows": 3, "cols": 2}],
            2: [{"matrix": [["x", "y"], ["300.00", "400.00"]],
                 "bbox": [1, 2, 3, 4], "row_bboxes": [], "rows": 2, "cols": 2}],
            3: [{"matrix": [["m", "n"], ["700.00", "800.00"], ["900.00", "950.00"]],
                 "bbox": [5, 6, 7, 8], "row_bboxes": [], "rows": 3, "cols": 2}],
        }
        new_events, manifest, stats = w.merge_fitz_track(events, fitz_tables)
        self.assertEqual(stats["replaced"], 1)
        self.assertEqual(stats["kept_docling_richer"], 1)  # fitz 缺 500/600 → 不替换
        self.assertEqual(stats["fitz_added"], 1)
        texts = [ev["text"] for ev in new_events if ev.get("kind") == "table"]
        self.assertTrue(any("999.00" in t for t in texts))          # 页1 用 fitz 版
        self.assertTrue(any("500.00" in t for t in texts))          # 页2 保留 docling 版
        self.assertTrue(any("700.00" in t for t in texts))          # 页3 fitz 新增
        pages = manifest["pages"]
        self.assertEqual(pages["1"][0]["order"], 0)
        self.assertEqual(pages["1"][0]["source"], "replace")
        self.assertEqual(pages["3"][0]["order"], 0)
        self.assertEqual(pages["3"][0]["source"], "added")
        self.assertNotIn("2", pages)

    def _tbl(self, page, n_rows, text_prefix="科目"):
        rows = [f"| {text_prefix} | 金额 |", "| --- | --- |"]
        rows += [f"| 行{i} | {100 + i}.00 |" for i in range(n_rows)]
        return {"kind": "table", "label": "table", "page": page, "text": "\n".join(rows)}

    def test_pick_refine_pages(self):
        events = [
            {"kind": "text", "label": "section_header", "page": 10, "text": "## 合并资产负债表"},
            self._tbl(10, 4),
            self._tbl(11, 4),                    # 续页（无标题）
            dict(self._tbl(12, 4), _fitz_table=True),  # fitz 已接管 → 排除
            self._tbl(20, 2),                    # 行数不足 → 排除
            {"kind": "text", "label": "text", "page": 30, "text": "普通页"},
            {"kind": "table", "label": "table", "page": 30,
             "text": "| 项目 | 金额 |\n| --- | --- |\n| 资产总计 | 1,000.00 |\n| 存货 | 100.00 |\n"
                     "| 负债合计 | 900.00 |\n| 货币资金 | 50.00 |"},  # 结构词命中
        ]
        self.assertEqual(w.pick_refine_pages(events), [10, 11, 30])


class TestQaV2(unittest.TestCase):
    """⑥ qa-tables v2：勾稽 / 数值存在性 / quote 回验。"""

    def test_parse_num_variants(self):
        self.assertEqual(w._parse_num("1,234.56"), 1234.56)
        self.assertEqual(w._parse_num("（1,234）"), -1234.0)
        self.assertEqual(w._parse_num("-12.5%"), -12.5)
        self.assertIsNone(w._parse_num("不适用"))

    def _bs_obj(self, total_val, eq_val=None):
        return {
            "record_type": "balance_sheet",
            "schema": {"columns": [{"key": "item"}, {"key": "c1", "label": "期末余额"}]},
            "rows": [
                {"item": "货币资金", "c1": "100.00"},
                {"item": "应收账款", "c1": "200.00"},
                {"item": "资产总计", "c1": total_val},
                {"item": "负债合计", "c1": "150.00"},
                {"item": "所有者权益合计", "c1": "150.00"},
                {"item": "负债和所有者权益总计", "c1": eq_val if eq_val is not None else total_val},
            ],
        }

    def test_crossfoot_pass(self):
        self.assertEqual(w.crossfoot_findings(self._bs_obj("300.00"), "t", "f.json"), [])

    def test_crossfoot_subtotal_and_identity_mismatch(self):
        f = w.crossfoot_findings(self._bs_obj("500.00", eq_val="400.00"), "t", "f.json")
        reasons = {x["reason"] for x in f}
        self.assertIn("subtotal_mismatch", reasons)
        self.assertIn("identity_mismatch", reasons)

    def test_crossfoot_jian_and_qizhong(self):
        obj = {
            "record_type": "income_stmt",
            "schema": {"columns": [{"key": "item"}, {"key": "c1", "label": "本期"}]},
            "rows": [
                {"item": "营业收入", "c1": "300.00"},
                {"item": "减：营业成本", "c1": "100.00"},
                {"item": "其中：直接材料", "c1": "999.00"},  # 其中项跳过
                {"item": "营业利润", "c1": "200.00"},
            ],
        }
        self.assertEqual(w.crossfoot_findings(obj, "t", "f.json"), [])

    def test_crossfoot_yoy(self):
        base = {"record_type": "variance_reasons", "schema": {"columns": []}, "rows": [
            {"item": "营业收入", "value_current": "110.00", "value_prior": "100.00", "yoy_pct": "10.00"}]}
        self.assertEqual(w.crossfoot_findings(base, "t", "f.json"), [])
        bad = {"record_type": "variance_reasons", "schema": {"columns": []}, "rows": [
            {"item": "营业收入", "value_current": "110.00", "value_prior": "100.00", "yoy_pct": "25.00"}]}
        f = w.crossfoot_findings(bad, "t", "f.json")
        self.assertEqual(f[0]["reason"], "yoy_mismatch")

    def test_crossfoot_roll_forward(self):
        obj = {
            "record_type": None, "promoted_to_type": None, "id": "generic",
            "schema": {"columns": [{"key": "item"}, {"key": "c1", "label": "期初"},
                                   {"key": "c2", "label": "增减"}, {"key": "c3", "label": "期末"}]},
            "rows": [
                {"item": "存货", "c1": "100.00", "c2": "50.00", "c3": "150.00"},
                {"item": "应收", "c1": "100.00", "c2": "50.00", "c3": "999.00"},
            ],
        }
        f = w.crossfoot_findings(obj, "t", "f.json")
        self.assertEqual(f[0]["reason"], "roll_mismatch")

    def test_value_existence(self):
        obj = {
            "provenance": {"pages": [1]},
            "schema": {"columns": [{"key": "item"}, {"key": "c1"}]},
            "rows": [{"item": "货币资金", "c1": "100.00"}, {"item": "坏账", "c1": "999.99"}],
        }
        tokens = {1: set(w._numeric_tokens("100.00 200.00"))}  # 页集须与表值同构归一（含小数点合并）
        f = w.value_existence_findings(obj, "t", "f.json", tokens)
        self.assertEqual(f[0]["reason"], "value_not_on_page")
        self.assertEqual(f[0]["verdict"], "demote")  # 1/2 = 50% > 30% 阈值
        obj_mild = {"provenance": {"pages": [1]}, "schema": {"columns": [{"key": "item"}, {"key": "c1"}]},
                    "rows": [{"item": f"r{i}", "c1": "100.00"} for i in range(4)]
                            + [{"item": "坏账", "c1": "888.88"}]}
        f1 = w.value_existence_findings(obj_mild, "t", "f.json", tokens)
        self.assertEqual(f1[0]["verdict"], "degraded")  # 1/5 = 20%
        obj_many = {"provenance": {"pages": [1]}, "schema": {"columns": [{"key": "item"}, {"key": "c1"}]},
                    "rows": [{"item": f"r{i}", "c1": "888.88"} for i in range(5)]}
        f2 = w.value_existence_findings(obj_many, "t", "f.json", tokens)
        self.assertEqual(f2[0]["verdict"], "demote")

    def test_quote_verify(self):
        obj = {"rows": [
            {"item": "货币资金", "source": {"page": 1, "quote": "货币资金 10,000"}},
            {"item": "存货", "source": {"page": 1, "quote": "页面上不存在的引文"}},
        ]}
        tokens = {1: {"10000", "200"}}
        normtext = {1: "货币资金10000元存货200"}
        f = w.quote_verify_findings(obj, "t", "f.json", tokens, normtext)
        self.assertEqual(len(f), 1)
        self.assertEqual(f[0]["reason"], "quote_unverified")
        self.assertIn("存货", f[0]["samples"][0])

    def test_quote_verify_tolerates_interleaved_columns(self):
        # 页面列序为 标签|附注|本期|上年，quote 只拼了 标签+本期+上年——逐 token 校验应通过
        obj = {"rows": [{"item": "货币资金",
                         "source": {"page": 1, "quote": "货币资金 10,000 20,000"}}]}
        tokens = {1: {"1", "10000", "20000"}}
        normtext = {1: "货币资金11000020000"}
        self.assertEqual(w.quote_verify_findings(obj, "t", "f.json", tokens, normtext), [])

    def test_quote_verify_tolerates_dash_placeholder(self):
        # docling 把页上 en dash 空值占位（–）转成 '-'：双侧经 _seg_norm 统一 dash 家族后应通过
        obj = {"rows": [{"item": "存放同业和其他金融机构款项净减少额",
                         "source": {"page": 1, "quote": "7,383 -"}}]}
        tokens = {1: {"7383"}}
        normtext = {1: w._seg_norm("存放同业和其他金融机构款项净减少额 7,383 –")}
        self.assertEqual(w.quote_verify_findings(obj, "t", "f.json", tokens, normtext), [])
        self.assertEqual(w._seg_norm("–"), "-")

    def test_seg_norm_symmetry_unicode_variants(self):
        # docling↔fitz 常见字符变体双侧同构：任一变体归一后必须等价（防 dash 家族式不对称复发）
        pairs = [
            ("-", "–"), ("-", "—"), ("-", "－"), ("-", "−"),  # dash 家族
            ("-", "‐"), ("-", "‑"), ("-", "‒"), ("-", "―"),
        ]
        for ascii_form, variant in pairs:
            self.assertEqual(w._seg_norm(ascii_form), w._seg_norm(variant),
                             f"{variant!r} 未与 '-' 同构")
        # 空白/全半角标点在两侧归一后同样等价
        for a, b in [("1,000", "1，000"), ("50%", "50％"), ("（注）", "(注)")]:
            self.assertEqual(w._seg_norm(a), w._seg_norm(b))

    def test_value_existence_reports_unique_prefix_repair(self):
        # 残片（缺尾位）在页 token 集有唯一前缀候选时附 repair_candidates 诊断（不回填）
        obj = {"provenance": {"pages": [1]},
               "rows": [{"item": "川宁生物", "c1": "549,059,47",
                         "source": {"page": 1, "quote": ""}}]}
        tokens = {1: {"549059474", "100"}}
        f = w.value_existence_findings(obj, "t", "f.json", tokens)
        self.assertEqual(f[0]["reason"], "value_not_on_page")
        self.assertEqual(f[0]["repair_candidates"], {"54905947": "549059474"})
        # 多候选/零候选 → 不给诊断提示
        tokens2 = {1: {"549059474", "549059477", "100"}}
        f2 = w.value_existence_findings(obj, "t", "f.json", tokens2)
        self.assertNotIn("repair_candidates", f2[0])
        # 全文级巨型 token（整行数值粘连）不得淹没唯一性
        tokens3 = {1: {"549059478", "5490594785758307743140035022014002508821791067276"}}
        f3 = w.value_existence_findings(obj, "t", "f.json", tokens3)
        self.assertEqual(f3[0]["repair_candidates"], {"54905947": "549059478"})

    def test_clip_quote_never_splits_number(self):
        # 截断点落在数值中间 → 回退到数值段前；数值恰在边界完整 → 保留；短串 → 原样
        s = "激励对象授予105,005,100 股上港集团A 股限制性股票,授予的限制性股票满36 个月后分批解除限售"
        clipped = w._clip_quote(s, 20)
        self.assertNotIn("105", clipped.split()[-1])  # 尾段不得是数值残片
        self.assertTrue(clipped.endswith("激励对象授予") or not w.re.search(r"\d[\d,，.]*$", clipped))
        # 数值恰在截断边界完整结束（下一字符非数字）→ 保留完整数值
        s2 = "营业收入 30,015,354 元"
        self.assertEqual(w._clip_quote(s2, 20), "营业收入 30,015,354 元"[:20])
        # 短串原样
        self.assertEqual(w._clip_quote("短串"), "短串")

    def test_warn_stale_cache(self):
        import io
        with tempfile.TemporaryDirectory() as td:
            import os
            os.environ[w.CACHE_ENV] = td
            try:
                sha = "stalecache01"
                d = w.entry_dir(sha)
                d.mkdir(parents=True, exist_ok=True)
                # 无版本戳（旧缓存）→ 提醒
                (d / "convert_meta.json").write_text("{}", encoding="utf-8")
                buf = io.StringIO()
                with contextlib.redirect_stderr(buf):
                    w.warn_stale_cache(sha)
                self.assertIn("无版本戳", buf.getvalue())
                # 旧版本 → 提醒
                (d / "convert_meta.json").write_text(
                    json.dumps({"pipeline_version": "0.5.0"}), encoding="utf-8")
                buf = io.StringIO()
                with contextlib.redirect_stderr(buf):
                    w.warn_stale_cache(sha)
                self.assertIn("0.5.0", buf.getvalue())
                # 当前版本 → 静默
                (d / "convert_meta.json").write_text(
                    json.dumps({"pipeline_version": w.PIPELINE_VERSION}), encoding="utf-8")
                buf = io.StringIO()
                with contextlib.redirect_stderr(buf):
                    w.warn_stale_cache(sha)
                self.assertEqual(buf.getvalue(), "")
            finally:
                os.environ.pop(w.CACHE_ENV, None)


class TestAnnotateTracks(unittest.TestCase):
    def test_track_annotation(self):
        tables = [
            {"index": 0, "page": 3, "line": 10},
            {"index": 1, "page": 3, "line": 30},
            {"index": 2, "page": 4, "line": 50},
        ]
        manifest = {"pages": {"3": [{"order": 1, "bbox": [1, 2, 3, 4]}]}}
        w.annotate_table_tracks(tables, manifest)
        self.assertEqual(tables[0]["track"], "docling")
        self.assertEqual(tables[1]["track"], "fitz")  # 页3 第2张表为 fitz
        self.assertEqual(tables[2]["track"], "docling")


class TestMaterializeBBox(unittest.TestCase):
    def test_generic_row_bbox(self):
        md_lines = ["<!-- page:3 -->", "", "| 项目 | 数量 |", "| --- | --- |",
                    "| 甲 | 1 |", "| 乙 | 2 |"]
        table_meta = {"index": 0, "page": 3, "line": 2, "line_end": 5, "rows": 2, "cols": 2, "type": None}
        entry = {"row_bboxes": [[0, 0, 10, 1], [0, 1, 10, 2], [0, 2, 10, 3]]}
        payload = w._materialize_generic_table(md_lines, table_meta, fitz_entry=entry)
        self.assertEqual(payload["rows"][0]["source"]["bbox"], [0, 1, 10, 2])
        self.assertEqual(payload["rows"][1]["source"]["bbox"], [0, 2, 10, 3])
        self.assertEqual(payload["rows"][0]["source"]["page"], 3)


class TestExtractQuery(unittest.TestCase):
    def test_expand_need_keywords_inventory(self):
        kws = w.expand_need_keywords("存货")
        self.assertIn("存貨", kws)

    def test_split_and_slice_pages(self):
        md = [
            "<!-- page:1 -->", "AAA",
            "<!-- page:2 -->", "合同负债 12.3",
            "<!-- page:3 -->", "BBB",
        ]
        pages = w.split_md_pages(md)
        self.assertEqual(set(pages), {1, 2, 3})
        sliced = w.slice_pages(pages, [2], pad=1)
        self.assertEqual(set(sliced), {1, 2, 3})

    def test_status_not_in_pdf(self):
        self.assertEqual(w.classify_extract_status([], []), "not_in_pdf")

    def test_status_ambiguous_many_md_pages(self):
        md_hits = [{"page": i, "text": "x"} for i in range(1, 12)]
        self.assertEqual(w.classify_extract_status([], md_hits), "ambiguous")

    def test_build_item_from_records(self):
        rec = [{"page": 5, "row_label": "合同负债", "unit": "千元",
                "values": [{"value": "123", "period": "2025"}]}]
        page_texts = {5: "合同负债 123 千元"}
        item = w.build_extract_query_item("合同负债", rec, [], page_texts)
        self.assertEqual(item["status"], "found")
        self.assertEqual(item["page"], 5)
        self.assertIn("合同负债", item["quote"])
        self.assertEqual(item["value"], "123")

    def test_extract_query_cli_writes_adhoc(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            sha = "aaaaaaaaaaaa"
            d = root / sha
            d.mkdir()
            (d / "report.md").write_text(
                "<!-- page:1 -->\n存货 100\n<!-- page:2 -->\n合同负债 50\n",
                encoding="utf-8",
            )
            old = w.cache_root
            w.cache_root = lambda: root  # type: ignore[method-assign]
            try:
                w.cmd_extract_query([sha, "--need", "合同负债", "--need", "不存在科目XYZ"])
            finally:
                w.cache_root = old  # type: ignore[method-assign]
            adhoc_dirs = list(d.glob("adhoc-*/adhoc.json"))
            self.assertEqual(len(adhoc_dirs), 1)
            payload = json.loads(adhoc_dirs[0].read_text(encoding="utf-8"))
            by_q = {it["query"]: it["status"] for it in payload["items"]}
            self.assertEqual(by_q["合同负债"], "found")
            self.assertEqual(by_q["不存在科目XYZ"], "not_in_pdf")


class TestResolveFields(unittest.TestCase):
    def test_cmd_resolve_l1_writes_field_record(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            sha = "aaaaaaaaaaaa"
            cache_dir = root / sha
            cache_dir.mkdir(parents=True, exist_ok=True)

            # report.md：用于 quote_on_page 回验
            (cache_dir / "report.md").write_text(
                "<!-- page:2 -->\n合同负债 50 千元\n",
                encoding="utf-8",
            )

            # records.json：用于 L1 typed row → records 精确取值
            records = [{
                "table": 10,
                "page": 2,
                "type": "balance_sheet",
                "row_label": "合同负债",
                "label_norm": "合同负债",
                "values": [{"value": "50", "period": "2025年度", "header": "期末余额"}],
                "unit": "千元",
                "headers": ["科目/项目", "期末余额"],
            }]
            (cache_dir / "records.json").write_text(
                json.dumps(records, ensure_ascii=False),
                encoding="utf-8",
            )

            # result 产物：typed table + quality pass + manifest
            result_name = "result-20260818T000000Z"
            result_dir = cache_dir / result_name
            (result_dir / "tables").mkdir(parents=True, exist_ok=True)

            table_payload = {
                "table_id": "balance_sheet",
                "record_type": "balance_sheet",
                "schema": {"columns": [
                    {"key": "item", "label": "科目/项目", "type": "string", "description": ""},
                    {"key": "c1", "label": "期末余额", "type": "string", "description": ""},
                ]},
                "rows": [{
                    "item": "合同负债",
                    "c1": "50",
                    "source": {"page": 2, "table": 10, "quote": "合同负债 50"},
                }],
                "provenance": {"pages": [2], "tables": [10]},
            }
            (result_dir / "tables" / "balance_sheet.json").write_text(
                json.dumps(table_payload, ensure_ascii=False),
                encoding="utf-8",
                )

            manifest = {
                "version": "0.4.1",
                "layout": "split_tables",
                "cache_id": sha,
                "catalog": {
                    "tables": [{"id": "balance_sheet", "file": "tables/balance_sheet.json"}],
                    "narratives": [],
                    "derived": [],
                    "fields": [],
                },
                "gaps_file": "gaps.json",
                "quality_file": "quality.json",
                "promote_candidates_file": "promote_candidates.json",
            }
            (result_dir / "manifest.json").write_text(
                json.dumps(manifest, ensure_ascii=False),
                encoding="utf-8",
            )

            quality = {
                "status": "pass",
                "tables": [{"id": "balance_sheet", "verdict": "pass"}],
                "python_findings": [],
            }
            (result_dir / "quality.json").write_text(
                json.dumps(quality, ensure_ascii=False),
                encoding="utf-8",
            )

            old = w.cache_root
            w.cache_root = lambda: root  # type: ignore[method-assign]
            try:
                w.cmd_resolve([sha, "--need", "合同负债", "--result", result_name, "--write-fields"])
            finally:
                w.cache_root = old  # type: ignore[method-assign]

            fields_dir = result_dir / "fields"
            self.assertTrue(fields_dir.is_dir())
            json_files = [p for p in fields_dir.glob("field_*.json")]
            self.assertEqual(len(json_files), 1)
            field_obj = json.loads(json_files[0].read_text(encoding="utf-8"))
            self.assertEqual(field_obj["field_id"], json_files[0].stem)
            self.assertEqual(field_obj["value"], "50")
            self.assertEqual(field_obj["status"], "found")
            self.assertEqual(field_obj["source"]["page"], 2)
            self.assertEqual(field_obj["source"]["table"], 10)

    def test_cmd_extract_needs_from_request_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            sha = "aaaaaaaaaaaa"
            cache_dir = root / sha
            cache_dir.mkdir(parents=True, exist_ok=True)

            (cache_dir / "report.md").write_text(
                "<!-- page:2 -->\n合同负债 50 千元\n",
                encoding="utf-8",
            )
            records = [{
                "table": 10,
                "page": 2,
                "type": "balance_sheet",
                "row_label": "合同负债",
                "label_norm": "合同负债",
                "values": [{"value": "50", "period": "2025年度", "header": "期末余额"}],
                "unit": "千元",
                "headers": ["科目/项目", "期末余额"],
            }]
            (cache_dir / "records.json").write_text(
                json.dumps(records, ensure_ascii=False),
                encoding="utf-8",
            )

            result_name = "result-20260818T000000Z"
            result_dir = cache_dir / result_name
            (result_dir / "tables").mkdir(parents=True, exist_ok=True)

            table_payload = {
                "table_id": "balance_sheet",
                "record_type": "balance_sheet",
                "schema": {"columns": [
                    {"key": "item", "label": "科目/项目", "type": "string", "description": ""},
                    {"key": "c1", "label": "期末余额", "type": "string", "description": ""},
                ]},
                "rows": [{
                    "item": "合同负债",
                    "c1": "50",
                    "source": {"page": 2, "table": 10, "quote": "合同负债 50"},
                }],
                "provenance": {"pages": [2], "tables": [10]},
            }
            (result_dir / "tables" / "balance_sheet.json").write_text(
                json.dumps(table_payload, ensure_ascii=False),
                encoding="utf-8",
            )

            manifest = {
                "version": "0.4.1",
                "layout": "split_tables",
                "cache_id": sha,
                "catalog": {
                    "tables": [{"id": "balance_sheet", "file": "tables/balance_sheet.json"}],
                    "narratives": [],
                    "derived": [],
                    "fields": [],
                },
                "gaps_file": "gaps.json",
                "quality_file": "quality.json",
                "promote_candidates_file": "promote_candidates.json",
            }
            (result_dir / "manifest.json").write_text(
                json.dumps(manifest, ensure_ascii=False),
                encoding="utf-8",
            )
            quality = {
                "status": "pass",
                "tables": [{"id": "balance_sheet", "verdict": "pass"}],
                "python_findings": [],
            }
            (result_dir / "quality.json").write_text(
                json.dumps(quality, ensure_ascii=False),
                encoding="utf-8",
            )

            # request file: fields[]
            req_path = root / "request.json"
            req_path.write_text(json.dumps({"fields": ["合同负债"]}, ensure_ascii=False), encoding="utf-8")

            old = w.cache_root
            w.cache_root = lambda: root  # type: ignore[method-assign]
            try:
                w.cmd_extract_needs([sha, "--file", str(req_path), "--result", result_name])
            finally:
                w.cache_root = old  # type: ignore[method-assign]

            fields_dir = result_dir / "fields"
            json_files = [p for p in fields_dir.glob("field_*.json")]
            self.assertEqual(len(json_files), 1)
            field_obj = json.loads(json_files[0].read_text(encoding="utf-8"))
            self.assertEqual(field_obj["value"], "50")


class TestFixes041(unittest.TestCase):
    """0.4.1：文本表去重 / 链内类型继承 / 附注编号阻断 / 标题否决 / 按链分组 / 堆叠包含。"""

    def test_stack_header_cells_containment(self):
        self.assertEqual(w._stack_header_cells("何平", "何平"), "何平")
        self.assertEqual(w._stack_header_cells("公司注册地址", "公司注册地址的历史变更情况"),
                         "公司注册地址的历史变更情况")
        self.assertEqual(w._stack_header_cells("2024年12月31日期初余额", "期初余额"),
                         "2024年12月31日期初余额")
        self.assertEqual(w._stack_header_cells("2024年", "期末余额"), "2024年期末余额")

    def test_merge_text_dedup_suppresses_duplicate(self):
        events = [
            {"kind": "table", "label": "table", "page": 1,
             "text": "| 姓名 | 职务 |\n| --- | --- |\n| 张三 | 董事 |"},
            {"kind": "table", "label": "table", "page": 2,
             "text": "| 数字表 | 金额 |\n| --- | --- |\n| 甲 | 100 |\n| 乙 | 200 |"},
        ]
        fitz_tables = {
            1: [{"matrix": [["姓名国籍", "职务"], ["张三中国", "董事"]],
                 "bbox": [1, 2, 3, 4], "row_bboxes": [], "rows": 2, "cols": 2}],
            2: [{"matrix": [["完全不同的内容", "说明"], ["业务概述", "无关文本行"]],
                 "bbox": [1, 2, 3, 4], "row_bboxes": [], "rows": 2, "cols": 2}],
        }
        new_events, manifest, stats = w.merge_fitz_track(events, fitz_tables)
        self.assertEqual(stats["suppressed_duplicate"], 1)  # 页1 文本重复 → 抑制，保留 docling
        self.assertEqual(stats["fitz_added"], 1)            # 页2 无重复 → 正常补插
        texts = "\n".join(ev.get("text", "") for ev in new_events)
        self.assertNotIn("张三中国", texts)
        self.assertIn("完全不同的内容", texts)
        self.assertNotIn("1", manifest["pages"])  # 抑制表不进 manifest

    def test_chain_local_inheritance_no_global_infection(self):
        head = "\n".join([
            "| 项目 | 期末 | 期初 |",
            "|---|---|---|",
            "| 资产总计 | 900 | 800 |",
            "| 负债合计 | 500 | 400 |",
        ])
        piece = "\n".join([  # 同列数、空壳表头的续片
            "| | | |",
            "|---|---|---|",
            "| 所有者权益合计 | 400 | 400 |",
        ])
        far = "\n".join([
            "| 摘要 | 甲 | 乙 |",
            "|---|---|---|",
            "| 事项 | 1 | 2 |",
        ])
        md_lines = ("<!-- page:10 -->\n\n" + head + "\n\n" + piece
                    + "\n\n<!-- page:13 -->\n\n" + far).split("\n")
        tables = w.find_tables(md_lines)
        recs = w.build_records(md_lines, tables)
        by_label = {r["row_label"]: r for r in recs}
        self.assertEqual(by_label["资产总计"]["type"], "balance_sheet")
        self.assertEqual(by_label["所有者权益合计"]["type"], "balance_sheet")  # 链内继承
        self.assertIsNone(by_label["事项"]["type"])  # 跨链不再传染（旧全局 last_type 行为）

    def test_note_numbering_blocks_continuation(self):
        a = "\n".join(["| 项目 | 本期 | 上期 |", "|---|---|---|", "| 甲 | 1 | 2 |"])
        b = "\n".join(["| 项目 | 本期 | 上期 |", "|---|---|---|", "| 乙 | 3 | 4 |"])
        md_lines = ("<!-- page:20 -->\n\n" + a + "\n\n（三）应收账款\n\n" + b).split("\n")
        tables = w.find_tables(md_lines)
        self.assertFalse(tables[1].get("continued"))
        md_lines2 = ("<!-- page:20 -->\n\n" + a + "\n\n续上表\n\n" + b).split("\n")
        tables2 = w.find_tables(md_lines2)
        self.assertTrue(tables2[1].get("continued"))  # 真续表信号不受影响

    def test_title_veto_for_structural_stmt(self):
        labels = ["资产总计", "负债合计"]
        self.assertEqual(w.infer_table_type("", title="合并范围调整",
                                            headers=["项目", "期末"], sample_labels=labels),
                         (None, [], None))  # 有标题但不含报表名 → 否决
        self.assertEqual(w.infer_table_type("", title="合并资产负债表",
                                            headers=["项目", "期末"], sample_labels=labels),
                         ("balance_sheet", ["资产总计", "负债合计"], None))
        self.assertEqual(w.infer_table_type("", title="",
                                            headers=["项目", "期末"], sample_labels=labels),
                         ("balance_sheet", ["资产总计", "负债合计"], None))  # 无标题 → 结构证据生效

    def test_materialize_per_chain_grouping(self):
        import os

        with tempfile.TemporaryDirectory() as td:
            os.environ[w.CACHE_ENV] = td
            try:
                sha = "bba421aa0411"
                d = w.entry_dir(sha)
                d.mkdir(parents=True, exist_ok=True)
                md = "\n".join([
                    "<!-- page:100 -->", "", "## 合并资产负债表",
                    "| 项目 | 期末 |", "|---|---|", "| 资产总计 | 900 |", "| 负债合计 | 500 |",
                    "<!-- page:200 -->", "", "## 其他同形表",
                    "| 项目 | 期末 |", "|---|---|", "| 资产合计 | 9 |",
                ])
                (d / "report.md").write_text(md, encoding="utf-8")
                meta = {
                    "source": {"title": "测试年报", "symbol": "000001", "report_date": "2025-12-31"},
                    "tables": [
                        {"index": 5, "type": "balance_sheet", "page": 100, "line": 3, "line_end": 6,
                         "headers": ["项目", "期末"], "nearby_title": "合并资产负债表"},
                        {"index": 9, "type": "balance_sheet", "page": 200, "line": 10, "line_end": 13,
                         "headers": ["项目", "期末"], "nearby_title": "其他同形表"},
                    ],
                }
                records = [
                    {"table": 5, "page": 100, "type": "balance_sheet", "row_label": "资产总计",
                     "values": [{"col": 1, "value": "900", "header": "期末"}], "unit": "元", "headers": ["项目", "期末"]},
                    {"table": 5, "page": 100, "type": "balance_sheet", "row_label": "负债合计",
                     "values": [{"col": 1, "value": "500", "header": "期末"}], "unit": "元", "headers": ["项目", "期末"]},
                    {"table": 9, "page": 200, "type": "balance_sheet", "row_label": "资产合计",
                     "values": [{"col": 1, "value": "9", "header": "期末"}], "unit": "元", "headers": ["项目", "期末"]},
                ]
                (d / "meta.json").write_text(json.dumps(meta, ensure_ascii=False), encoding="utf-8")
                (d / "records.json").write_text(json.dumps(records, ensure_ascii=False), encoding="utf-8")
                out = w.materialize_tables(sha, out_name="result-UT", force=True)
                manifest = w.read_json(d / "result-UT" / "manifest.json", {})
                ids = {x["id"] for x in manifest.get("catalog", {}).get("tables", [])}
                self.assertIn("balance_sheet", ids)                       # 结构分最高链拿 canonical
                self.assertIn("balance_sheet_p200_i009", ids)             # 独立链独立文件，不混源拼接
                canon = w.read_json(d / "result-UT" / "tables" / "balance_sheet.json", {})
                labels = {r["item"] for r in canon.get("rows", [])}
                self.assertEqual(labels, {"资产总计", "负债合计"})          # 不再混入另一物理表
                other = w.read_json(d / "result-UT" / "tables" / "balance_sheet_p200_i009.json", {})
                self.assertEqual(other["rows"][0]["item"], "资产合计")
                self.assertEqual(other["title"], "资产负债表")             # 沿用基名目录元数据
            finally:
                os.environ.pop(w.CACHE_ENV, None)


    def test_guess_title_skips_unit_annotation(self):
        md_lines = ["<!-- page:142 -->", "", "## 合并资产负债表", "",
                    "（除特别注明外，金额单位人民币千元）", "", "| 项目 | 期末 |"]
        self.assertEqual(w._guess_table_title(md_lines, 6), "合并资产负债表")
        md_lines2 = ["<!-- page:1 -->", "", "## 人民币元", "", "| 项目 | 期末 |"]  # Docling 把单位行误标成标题
        self.assertEqual(w._guess_table_title(md_lines2, 4), "")
        md_lines3 = ["<!-- page:1 -->", "", "人民币元", "", "| 项目 | 期末 |"]
        self.assertEqual(w._guess_table_title(md_lines3, 4), "")  # 只有单位行 → 无标题
        md_lines4 = ["<!-- page:1 -->", "", "主要会计数据", "", "| 项目 | 期末 |"]
        self.assertEqual(w._guess_table_title(md_lines4, 4), "主要会计数据")  # 普通短行仍是标题


    def test_apply_hf_offline_default(self):
        import os

        saved = {k: os.environ.get(k) for k in ("HF_HOME", "HF_HUB_OFFLINE", "TRANSFORMERS_OFFLINE")}
        try:
            with tempfile.TemporaryDirectory() as td:
                # 场景1：本地有 docling 模型缓存 → 默认离线
                (Path(td) / "hub" / "models--docling-project--test").mkdir(parents=True)
                os.environ["HF_HOME"] = td
                os.environ.pop("HF_HUB_OFFLINE", None)
                os.environ.pop("TRANSFORMERS_OFFLINE", None)
                w.apply_hf_offline_default()
                self.assertEqual(os.environ.get("HF_HUB_OFFLINE"), "1")
                self.assertEqual(os.environ.get("TRANSFORMERS_OFFLINE"), "1")
                # 场景2：用户显式设置 → 不覆盖
                os.environ["HF_HUB_OFFLINE"] = "0"
                os.environ.pop("TRANSFORMERS_OFFLINE", None)
                w.apply_hf_offline_default()
                self.assertEqual(os.environ.get("HF_HUB_OFFLINE"), "0")
                # 场景3：无缓存目录 → 不设离线
                os.environ["HF_HOME"] = str(Path(td) / "none")
                os.environ.pop("HF_HUB_OFFLINE", None)
                os.environ.pop("TRANSFORMERS_OFFLINE", None)
                w.apply_hf_offline_default()
                self.assertIsNone(os.environ.get("HF_HUB_OFFLINE"))
        finally:
            for k, v in saved.items():
                if v is None:
                    os.environ.pop(k, None)
                else:
                    os.environ[k] = v


class TestFixes050(unittest.TestCase):
    """0.5.0：fetch --convert 不再把空串占位传给 convert（argparse 报 unrecognized arguments）。"""

    def test_fetch_convert_argv_no_empty_placeholders(self):
        import argparse

        args = argparse.Namespace(accurate=False, ocr=False, force=False, threads=8, device="cpu")
        argv = w._fetch_convert_argv(args, "abc123def456")
        self.assertEqual(argv, ["abc123def456", "--threads", "8", "--device", "cpu"])
        self.assertNotIn("", argv)
        args2 = argparse.Namespace(accurate=True, ocr=True, force=True, threads=4, device="mps")
        argv2 = w._fetch_convert_argv(args2, "abc123def456")
        self.assertIn("--accurate", argv2)
        self.assertIn("--ocr", argv2)
        self.assertIn("--force", argv2)



class TestRenderHtml(unittest.TestCase):
    """render-html：仅嵌入 quality=pass 表；产出自包含 HTML。"""

    def test_render_html_pass_only_and_hero(self):
        import os
        import render_html as rh

        with tempfile.TemporaryDirectory() as td:
            os.environ[w.CACHE_ENV] = td
            try:
                sha = "html0000test1"
                d = w.entry_dir(sha)
                result = d / "result-HTML"
                (result / "tables").mkdir(parents=True)
                manifest = {
                    "cache_id": sha,
                    "source": {
                        "title": "测试能源2025年报",
                        "symbol": "601088",
                        "report_date": "2025-12-31",
                        "filing_kind": "annual",
                        "industry_hint": "fossil_energy",
                    },
                    "coverage_groups": ["B_statements", "C_segments"],
                    "catalog": {
                        "tables": [
                            {"id": "balance_sheet", "file": "tables/balance_sheet.json",
                             "group": "B_statements", "method": "record_map", "row_count": 1},
                            {"id": "income_stmt_bad", "file": "tables/income_stmt_bad.json",
                             "group": "B_statements", "method": "record_map", "row_count": 1},
                            {"id": "segments_by_industry", "file": "tables/segments_by_industry.json",
                             "group": "C_segments", "method": "record_map", "row_count": 1},
                        ],
                        "narratives": [],
                        "fields": [],
                    },
                }
                quality = {
                    "status": "pass",
                    "tables": [
                        {"id": "balance_sheet", "verdict": "pass"},
                        {"id": "income_stmt_bad", "verdict": "demote"},
                        {"id": "segments_by_industry", "verdict": "pass"},
                    ],
                    "python_findings": [],
                }
                review = {
                    "status": "pass",
                    "hard_failures": [],
                    "warnings": [],
                    "document_profile": {"filing_kind": "annual", "industry": "fossil_energy"},
                }
                gaps = [
                    {"id": "coal_washing_yield", "group": "X_fossil_energy",
                     "status": "not_disclosed", "reason": "未披露入洗量"},
                ]
                bs = {
                    "table_id": "balance_sheet", "title": "资产负债表", "group": "B_statements",
                    "description": "", "method": "record_map", "unit_default": "",
                    "schema": {"columns": [
                        {"key": "item", "label": "科目/项目"},
                        {"key": "c1", "label": "2025"},
                    ]},
                    "rows": [{"item": "货币资金", "c1": "100",
                              "source": {"page": 10, "table": 1, "quote": "货币资金 100"}}],
                    "row_count": 1, "provenance": {"pages": [10]},
                }
                bad = {
                    "table_id": "income_stmt_bad", "title": "假利润表", "group": "B_statements",
                    "schema": {"columns": [{"key": "item", "label": "科目/项目"}]},
                    "rows": [{"item": "子公司名称", "source": {"page": 1, "quote": "x"}}],
                    "row_count": 1,
                }
                seg = {
                    "table_id": "segments_by_industry", "title": "分行业", "group": "C_segments",
                    "schema": {"columns": [
                        {"key": "item", "label": "科目/项目"},
                        {"key": "c1", "label": "收入"},
                    ]},
                    "rows": [{"item": "煤炭", "c1": "1",
                              "source": {"page": 20, "table": 2, "quote": "煤炭 1"}}],
                    "row_count": 1,
                }
                (result / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")
                (result / "quality.json").write_text(json.dumps(quality, ensure_ascii=False), encoding="utf-8")
                (result / "review.json").write_text(json.dumps(review, ensure_ascii=False), encoding="utf-8")
                (result / "gaps.json").write_text(json.dumps(gaps, ensure_ascii=False), encoding="utf-8")
                (result / "tables" / "balance_sheet.json").write_text(
                    json.dumps(bs, ensure_ascii=False), encoding="utf-8")
                (result / "tables" / "income_stmt_bad.json").write_text(
                    json.dumps(bad, ensure_ascii=False), encoding="utf-8")
                (result / "tables" / "segments_by_industry.json").write_text(
                    json.dumps(seg, ensure_ascii=False), encoding="utf-8")

                payload = rh.build_html_payload(result, cache_id=sha)
                self.assertEqual(payload["meta"]["source"]["title"], "测试能源2025年报")
                self.assertEqual(payload["meta"]["quality_status"], "pass")
                self.assertEqual(payload["meta"]["review_status"], "pass")
                self.assertIn("balance_sheet", payload["tables"])
                self.assertIn("segments_by_industry", payload["tables"])
                self.assertNotIn("income_stmt_bad", payload["tables"])
                self.assertEqual(payload["meta"]["pass_table_count"], 2)
                self.assertTrue(any(g.get("id") == "coal_washing_yield" for g in payload["gaps"]))

                dest = rh.write_html_report(result, cache_id=sha)
                self.assertTrue(dest.is_file())
                text = dest.read_text(encoding="utf-8")
                self.assertIn("测试能源2025年报", text)
                self.assertIn("balance_sheet", text)
                self.assertNotIn("假利润表", text)
                self.assertIn("coal_washing_yield", text)
                self.assertIn('id="payload"', text)

                buf = io.StringIO()
                with contextlib.redirect_stdout(buf):
                    w.cmd_render_html([sha, "--result", "result-HTML"])
                out = json.loads(buf.getvalue())
                self.assertEqual(out["cache_id"], sha)
                self.assertTrue(Path(out["html"]).is_file())
            finally:
                os.environ.pop(w.CACHE_ENV, None)


class TestCrossIndustryFixes(unittest.TestCase):
    """0.6.1 跨行业修复回归：粘链/勾稽/定型 veto/行业继承/auto-heal 协议。"""

    def test_footer_title_echo_chains(self):
        # 神华 p147→p148：页脚重印不带「续」的同名标题不得阻断粘链
        md = "\n".join([
            "<!-- page:147 -->",
            "| 项目 | 附注 | 2025 | 2024 |",
            "|---|---|---|---|",
            "| 货币资金 | 1 | 96,772 | 143,845 |",
            "| 应收票据 | 2 | 5,618 | 3,036 |",
            "| 流动资产合计 | | 102,390 | 146,881 |",
            "| 长期股权投资 | 3 | 62,044 | 59,842 |",
            "| 其他权益工具投资 | 4 | 3,175 | 2,787 |",
            "| 非流动资产合计 | | 65,219 | 62,629 |",
            "| 资产总计 | | 167,609 | 209,510 |",
            "| 负债合计 | | 90,000 | 100,000 |",
            "| 负债和股东权益总计 | | 167,609 | 209,510 |",
            "",
            "中国神华能源股份有限公司 合并资产负债表 2025 年 12 月 31 日 ( 金额单位:人民币百万元 )",
            "",
            "<!-- page:148 -->",
            "## 中国神华能源股份有限公司 合并资产负债表 ( 续 ) 2025 年 12 月 31 日",
            "| 项目 | 附注 | 2025 | 2024 |",
            "|---|---|---|---|",
            "| 短期借款 | 5 | 1,000 | 2,000 |",
            "| 应付账款 | 6 | 3,000 | 4,000 |",
            "| 流动负债合计 | | 4,000 | 6,000 |",
        ]).split("\n")
        tables = w.find_tables(md)
        self.assertEqual(tables[0].get("continued_by"), [1])
        self.assertEqual(tables[0].get("type"), "balance_sheet")

    def test_same_heading_echo_chains(self):
        # 平安：每页页首重印同一 ## 标题（无「续」），同款标题不阻断
        md = "\n".join([
            "<!-- page:187 -->",
            "## 合并资产负债表",
            "2025 年 12 月 31 日 (除特别注明外,金额单位为人民币百万元)",
            "| 项目 | 2025 | 2024 |",
            "|---|---|---|",
            "| 货币资金 | 100 | 200 |",
            "| 应收账款 | 300 | 400 |",
            "| 流动资产合计 | 400 | 600 |",
            "| 长期借款 | 50 | 60 |",
            "| 负债合计 | 350 | 380 |",
            "| 负债和股东权益总计 | 900 | 1,200 |",
            "| 资产总计 | 900 | 1,200 |",
            "| 股东权益合计 | 550 | 820 |",
            "",
            "<!-- page:188 -->",
            "## 合并资产负债表",
            "| 项目 | 2025 | 2024 |",
            "|---|---|---|",
            "| 股本 | 300 | 300 |",
            "| 资本公积 | 100 | 100 |",
            "| 未分配利润 | 150 | 420 |",
        ]).split("\n")
        tables = w.find_tables(md)
        self.assertEqual(tables[0].get("continued_by"), [1])

    def test_sparse_section_col_alignment_chains(self):
        # 平安 IS 续片带稀疏节号前置列（col0 仅 三、四、）：剔除后对齐续链
        md = "\n".join([
            "<!-- page:1 -->",
            "| 项目 | 附注 | 2025 | 2024 |",
            "|---|---|---|---|",
            "| 一、营业总收入 | | 1,000 | 900 |",
            "| 营业收入 | 1 | 1,000 | 900 |",
            "| 二、营业总成本 | | 800 | 750 |",
            "| 营业成本 | 2 | 700 | 660 |",
            "| 三、营业利润 | | 200 | 150 |",
            "| 净利润 | 3 | 180 | 140 |",
            "",
            "<!-- page:2 -->",
            "| | 项目 | 附注 | 2025 | 2024 |",
            "|---|---|---|---|---|",
            "| 五、 | 其他综合收益 | 4 | 20 | 15 |",
            "| | 综合收益总额 | | 200 | 155 |",
            "| | 每股收益 | | 0.5 | 0.4 |",
            "| | 基本每股收益 | 5 | 0.5 | 0.4 |",
            "| | 稀释每股收益 | 6 | 0.5 | 0.4 |",
            "| | 其他财务指标 | | 1 | 1 |",
        ]).split("\n")
        tables = w.find_tables(md)
        self.assertEqual(tables[0].get("cols"), 4)
        self.assertEqual(tables[0].get("continued_by"), [1])

    def test_identity_column_aligned(self):
        obj = {"record_type": "balance_sheet", "rows": [
            {"item": "流动资产合计", "c2": "146,969", "c3": "207,139"},
            {"item": "非流动资产合计", "c2": "480,792", "c3": "460,883"},
            {"item": "资产总计", "c2": "627,761", "c3": "668,022"},
            {"item": "负债和股东权益总计", "c2": "627,761", "c3": "668,022"},
        ]}
        self.assertEqual(w.crossfoot_findings(obj, "bs", "tables/bs.json"), [])

    def test_identity_detects_real_mismatch_per_column(self):
        obj = {"record_type": "balance_sheet", "rows": [
            {"item": "资产总计", "c2": "627,761", "c3": "668,022"},
            {"item": "负债和股东权益总计", "c2": "617,761", "c3": "668,022"},
        ]}
        findings = w.crossfoot_findings(obj, "bs", "tables/bs.json")
        self.assertTrue(any(f.get("reason") == "identity_mismatch" for f in findings))

    def test_subtotal_minus_paren_negative(self):
        # 减:库存股 (8,151,117)：值已为负，不得再取负（美的 BS 实证）
        obj = {"record_type": "balance_sheet", "rows": [
            {"item": "股本", "c2": "7,597,145"},
            {"item": "资本公积", "c2": "45,350,720"},
            {"item": "减:库存股", "c2": "(8,151,117)"},
            {"item": "未分配利润", "c2": "167,228,020"},
            {"item": "归属于母公司股东权益合计", "c2": "212,024,768"},
        ]}
        self.assertEqual(w.crossfoot_findings(obj, "bs", "tables/bs.json"), [])

    def test_subtotal_cf_section_result_not_polluting(self):
        # CF 净额行是节结果，不得污染下一节小计
        obj = {"record_type": "cashflow_stmt", "rows": [
            {"item": "销售商品、提供劳务收到的现金", "c2": "100"},
            {"item": "收到的税费返还", "c2": "20"},
            {"item": "经营活动现金流入小计", "c2": "120"},
            {"item": "购买商品支付的现金", "c2": "(50)"},
            {"item": "经营活动现金流出小计", "c2": "(50)"},
            {"item": "经营活动产生的现金流量净额", "c2": "70"},
            {"item": "收回投资收到的现金", "c2": "30"},
            {"item": "取得投资收益收到的现金", "c2": "10"},
            {"item": "投资活动现金流入小计", "c2": "40"},
        ]}
        self.assertEqual(w.crossfoot_findings(obj, "cf", "tables/cf.json"), [])

    def test_subtotal_unmarked_sibling_reconciled(self):
        # 未标注其中兄弟子项（长电 应收股利）：单行剔除后勾稽即豁免
        obj = {"record_type": "balance_sheet", "rows": [
            {"item": "货币资金", "c2": "833"},
            {"item": "其他应收款", "c2": "3,994"},
            {"item": "应收股利", "c2": "3,991"},
            {"item": "流动资产合计", "c2": "836"},
        ]}
        self.assertEqual(w.crossfoot_findings(obj, "bs", "tables/bs.json"), [])

    def test_parse_num_multi_token_glue(self):
        # 粘连多值单元格不得拼接成天文数字（美的 CF 1.6e15 实证）
        self.assertIsNone(w._parse_num("(164,904,908) (6,155,136)"))
        self.assertIsNone(w._parse_num("(158,573,072) (64,957,779)"))
        self.assertEqual(w._parse_num("96,772 7"), 96772.0)  # 短附注号容忍
        self.assertEqual(w._parse_num("(8,151,117)"), -8151117.0)

    def test_analysis_title_veto(self):
        # 「利润表及现金流量表主要项目变动分析」不得定型为报表（神华 p020 实证）
        md = "\n".join([
            "- 利润表及现金流量表主要项目变动分析",
            "| 项目 | 2025 年 | 2024 年(已重述) | 变化(%) |",
            "|---|---|---|---|",
            "| 营业收入 | 294,916 | 339,788 | (13.2) |",
            "| 营业成本 | 233,429 | 270,100 | (13.6) |",
            "| 经营活动产生的现金流量净额 | 75,059 | 91,086 | (17.6) |",
            "| 投资活动产生的现金流量净额 | (22,913) | (13,138) | 74.4 |",
        ]).split("\n")
        tables = w.find_tables(md)
        self.assertNotIn("cashflow_stmt", {t.get("type") for t in tables})
        self.assertIn("variance_reasons", {t.get("type_hint") for t in tables})

    def test_insurance_income_stmt_typed(self):
        md = "\n".join([
            "## 合并利润表",
            "| 项目 | 附注 | 2025 | 2024 |",
            "|---|---|---|---|",
            "| 保险业务收入 | 1 | 90,000 | 85,000 |",
            "| 保险服务费用 | 2 | (70,000) | (66,000) |",
            "| 净利润 | 3 | 12,000 | 11,000 |",
        ]).split("\n")
        tables = w.find_tables(md)
        self.assertIn("income_stmt", {t.get("type") for t in tables})

    def test_inherit_industry_from_cache(self):
        import os
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            os.environ[w.CACHE_ENV] = td
            try:
                ann = w.entry_dir("aaaa00000001")
                ann.mkdir(parents=True)
                w.write_json(ann / "meta.json", {
                    "filing_kind": "annual",
                    "source": {"symbol": "600066", "title": "宇通客车2025年报"},
                    "industry_hint": {"industry": "automobile", "confidence": 0.9},
                })
                w.index_upsert("aaaa00000001", symbol="600066",
                               title="宇通客车2025年报")
                meta = {
                    "filing_kind": "q1",
                    "source": {"symbol": "600066", "title": "宇通客车2026Q1"},
                    "industry_hint": {"industry": None, "confidence": 0.0},
                    "document_profile": {},
                }
                out = w.inherit_industry_from_cache("aaaa00000002", meta)
                ih = out["industry_hint"]
                self.assertEqual(ih.get("industry"), "automobile")
                self.assertEqual(ih.get("confidence"), 0.3)
                self.assertEqual(ih.get("inherited_from", {}).get("cache_id"), "aaaa00000001")
                # 年报不继承（未适配行业应显式 null + review 警示）
                meta2 = {
                    "filing_kind": "annual",
                    "source": {"symbol": "600066"},
                    "industry_hint": {"industry": None, "confidence": 0.0},
                }
                out2 = w.inherit_industry_from_cache("aaaa00000002", meta2)
                self.assertIsNone(out2["industry_hint"].get("industry"))
            finally:
                os.environ.pop(w.CACHE_ENV, None)

    def test_agent_apply_validates_and_lands(self):
        import os
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            os.environ[w.CACHE_ENV] = td
            try:
                d = w.entry_dir("bbbb00000001")
                (d / "result-x" / "agent_tasks_done").mkdir(parents=True)
                (d / "result-x" / "agent_tasks").mkdir(parents=True)
                md = "\n".join([
                    "<!-- page:3 -->",
                    "黄骅港完成装船量 217.0 百万吨( 2024 年: 214.4 百万吨)。",
                ])
                (d / "report.md").write_text(md, encoding="utf-8")
                w.write_json(d / "result-x" / "manifest.json", {
                    "catalog": {"narratives": [
                        {"id": "mda_business", "group": "D_mda", "status": "pending"}],
                        "tables": []}})
                w.write_json(d / "result-x" / "gaps.json", [
                    {"id": "mda_business", "group": "D_mda", "status": "pending"},
                    {"id": "railway_port_shipment", "group": "X_fossil_energy",
                     "status": "required"}])
                w.write_json(d / "result-x" / "quality.json", {
                    "python_findings": [
                        {"id": "balance_sheet", "verdict": "degraded",
                         "reason": "subtotal_mismatch", "detail": "x"}]})
                done = d / "result-x" / "agent_tasks_done"
                # found：页码错误 → 拒；not_disclosed：无 reason → 拒
                w.write_json(done / "gap-bad.json", {
                    "task": "narrative_close", "id": "railway_port_shipment",
                    "status": "found", "quote": "黄骅港完成装船量 217.0 百万吨",
                    "page": 9})
                w.write_json(done / "gap-bad2.json", {
                    "task": "narrative_close", "id": "mda_business",
                    "status": "not_disclosed", "reason": ""})
                out = w.agent_apply("bbbb00000001", result_name="result-x")
                self.assertEqual(len(out["rejected"]), 2)
                gaps = w.read_json(d / "result-x" / "gaps.json", [])
                by_id = {g["id"]: g for g in gaps}
                self.assertEqual(by_id["mda_business"]["status"], "pending")
                self.assertEqual(by_id["railway_port_shipment"]["status"], "required")
                # 正确 found + 仲裁 → 落地（坏任务已由 Agent 修正删除）
                (done / "gap-bad.json").unlink()
                (done / "gap-bad2.json").unlink()
                w.write_json(done / "gap-ok.json", {
                    "task": "narrative_close", "id": "railway_port_shipment",
                    "status": "found", "quote": "黄骅港完成装船量 217.0 百万吨",
                    "page": 3})
                w.write_json(done / "adj.json", {
                    "task": "qa_adjudication", "id": "balance_sheet",
                    "reason_kind": "subtotal_mismatch",
                    "adjudication": "rule_limitation", "rationale": "准则口径差异"})
                out2 = w.agent_apply("bbbb00000001", result_name="result-x")
                self.assertEqual(len(out2["rejected"]), 0)
                gaps2 = w.read_json(d / "result-x" / "gaps.json", [])
                gp = {g["id"]: g for g in gaps2}["railway_port_shipment"]
                self.assertEqual(gp["status"], "found")
                self.assertEqual(gp["page"], 3)
                q = w.read_json(d / "result-x" / "quality.json", {})
                self.assertEqual(
                    q["python_findings"][0].get("adjudicated"), "rule_limitation")
            finally:
                os.environ.pop(w.CACHE_ENV, None)


class TestCloseFixes061(unittest.TestCase):
    def test_statement_row_qa_scans_full_row(self):
        import os
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            os.environ[w.CACHE_ENV] = td
            try:
                sha = "qaseclabel01"
                d = w.entry_dir(sha)
                result = d / "result-QA2"
                (result / "tables").mkdir(parents=True, exist_ok=True)
                # 盾安 2025 年报版式：item 列为节标签（流动资产:），科目在 c1
                payload = {
                    "table_id": "balance_sheet",
                    "record_type": "balance_sheet",
                    "title": "资产负债表",
                    "rows": [
                        {"item": "流动资产:", "c1": "货币资金", "c3": "3,468,523,464.53"},
                        {"item": "流动资产:", "c1": "应收账款", "c3": "2,423,636,132.44"},
                        {"item": "流动资产:", "c1": "存货", "c3": "1,334,572,497.50"},
                        {"item": "流动资产:", "c1": "合同资产", "c3": "264,056,643.50"},
                        {"item": "流动资产:", "c1": "流动资产合计", "c3": "9,000,000,000.00"},
                    ],
                    "row_count": 4,
                    "schema": {"columns": [{"label": "项目"}]},
                    "provenance": {"pages": [77], "tables": [99]},
                }
                (result / "tables" / "balance_sheet.json").write_text(
                    json.dumps(payload, ensure_ascii=False), encoding="utf-8")
                (result / "manifest.json").write_text(json.dumps({
                    "catalog": {"tables": [
                        {"id": "balance_sheet", "file": "tables/balance_sheet.json",
                         "group": "B", "record_type": "balance_sheet"},
                    ], "narratives": [], "fields": [], "derived": []},
                }, ensure_ascii=False), encoding="utf-8")
                findings = w.python_qa_findings(result, pdf_path=None)
                dem = [f for f in findings if f.get("verdict") == "demote"
                       and f.get("reason") == "statement_row_labels_invalid"]
                self.assertEqual(dem, [])
            finally:
                os.environ.pop(w.CACHE_ENV, None)

    def test_narrative_scan_skips_qa_snapshot_gaps(self):
        import os
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            os.environ[w.CACHE_ENV] = td
            try:
                sha = "qaskip0000001"
                d = w.entry_dir(sha)
                result = d / "result-NS"
                result.mkdir(parents=True, exist_ok=True)
                (d / "report.md").write_text(
                    "<!-- page:1 -->\n正文。\n<!-- page:2 -->\n结尾。\n", encoding="utf-8")
                w.write_json(d / "meta.json", {
                    "cache_id": sha,
                    "source": {"title": "Sample 2025 Annual Report", "report_date": "2025-12-31"},
                })
                w.write_json(result / "manifest.json", {
                    "catalog": {"narratives": [], "tables": []}})
                w.write_json(result / "gaps.json", [
                    {"id": "qa::top_holders", "group": "Z_qa", "status": "suspect"},
                    {"id": "some_plain_gap", "group": "X_machinery", "status": "pending"},
                ])
                w.narrative_scan(sha, result_name="result-NS")
                tasks = {p.name for p in (result / "agent_tasks").glob("*.json")}
                self.assertNotIn("gap-qa::top_holders.json", tasks)
                self.assertIn("gap-some_plain_gap.json", tasks)
            finally:
                os.environ.pop(w.CACHE_ENV, None)


if __name__ == "__main__":
    unittest.main()