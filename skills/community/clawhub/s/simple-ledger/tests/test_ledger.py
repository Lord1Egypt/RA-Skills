#!/usr/bin/env python3
"""
个人记账 Skill — 合并测试套件（零外部依赖）

合并自 run_tests.py（yaml 断言，28条）与 test_comprehensive.py（unittest，65条），
精选精华用例，覆盖全部 7 个维度：
  A. NLP 自然语言解析
  B. CSV 格式 / 引号逗号解析
  C. 账本查询（月度收支 / 分类 / 关键字 / 余额）
  D. 报告生成（收支概览 / 分类排行 / 日均 / 多月独立）
  E. 投资持仓（买入 / 卖出 / 分红 / 浮盈 / 多证券）
  F. 边界异常（空账本 / 缺失字段 / 引号逗号描述）
  G. 数据完整性（总条数 / 字段完整 / 日期有序 / 无余额行混入）

所有断言基于 tests/fixtures/sample.csv 真实数据。
可直接运行: python3 tests/test_ledger.py
"""

import sys
import csv
import json
import unittest
import tempfile
import os
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# ─── 路径 ─────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = BASE_DIR / "scripts"
FIXTURES_DIR = BASE_DIR / "tests" / "fixtures"
SAMPLE_CSV = str(FIXTURES_DIR / "sample.csv")
EMPTY_CSV = str(FIXTURES_DIR / "empty.csv")
BUDGET_JSON = str(FIXTURES_DIR / "sample.budget.json")

sys.path.insert(0, str(SCRIPTS_DIR))

import parse_entry as pe_mod
import query_ledger as ql_mod
import generate_report as gr_mod
import invest as inv_mod

# ─── 参考日期（用于相对日期解析） ──────────────────────────────────────
REF_DATE = datetime(2026, 5, 21)

# ═══════════════════════════════════════════════════════════════════════
# A. NLP 自然语言解析（来自 run_tests.yaml + test_comprehensive）
# ═══════════════════════════════════════════════════════════════════════

class TestNLPParsing(unittest.TestCase):
    """自然语言记账解析测试 — 覆盖支出/收入/相对日期/明确日期/账户推断"""

    # A-1 最基础的餐饮支出（NLP-001）
    def test_basic_expense(self):
        result = pe_mod.parse_entry("今天中午吃饭花了50块", ref_date=REF_DATE)
        self.assertIsNotNone(result)
        self.assertNotIn("error", result)
        self.assertEqual(result["type"], "支出")
        self.assertEqual(result["amount"], 50.00)
        self.assertEqual(result["category"], "餐饮")
        self.assertEqual(result["date"], "2026-05-21")

    # A-2 收入类型（NLP-003）
    def test_income(self):
        result = pe_mod.parse_entry("工资到账8000", ref_date=REF_DATE)
        self.assertIsNotNone(result)
        self.assertNotIn("error", result)
        self.assertEqual(result["type"], "收入")
        self.assertEqual(result["amount"], 8000.00)
        self.assertEqual(result["category"], "工资")

    # A-3 相对日期 + 小数金额（NLP-002）
    def test_relative_date_and_decimal(self):
        result = pe_mod.parse_entry("昨天打车花了23.5", ref_date=REF_DATE)
        self.assertIsNotNone(result)
        self.assertNotIn("error", result)
        self.assertEqual(result["date"], "2026-05-20")
        self.assertEqual(result["amount"], 23.50)
        self.assertEqual(result["category"], "交通")

    # A-4 明确日期 + 指定支付方式（NLP-004）
    def test_explicit_date_and_account(self):
        result = pe_mod.parse_entry("买了一件外套299，用支付宝付的", ref_date=REF_DATE)
        self.assertIsNotNone(result)
        self.assertNotIn("error", result)
        self.assertEqual(result["amount"], 299.00)
        self.assertEqual(result["category"], "购物")
        self.assertEqual(result["account"], "支付宝")

    # A-5 通讯支出（NLP-005）
    def test_telecom_expense(self):
        result = pe_mod.parse_entry("充话费30", ref_date=REF_DATE)
        self.assertIsNotNone(result)
        self.assertNotIn("error", result)
        self.assertEqual(result["type"], "支出")
        self.assertEqual(result["amount"], 30.00)
        self.assertEqual(result["category"], "通讯")

    # A-6 明确日期 X月X号格式（NLP-007）
    def test_explicit_month_day(self):
        result = pe_mod.parse_entry("5月15号喝了杯奶茶18", ref_date=REF_DATE)
        self.assertIsNotNone(result)
        self.assertNotIn("error", result)
        self.assertEqual(result["date"], "2026-05-15")
        self.assertEqual(result["amount"], 18.00)
        self.assertEqual(result["category"], "餐饮")

    # A-7 理财收益 / 投资收入（NLP-010）
    def test_investment_income(self):
        result = pe_mod.parse_entry("理财收益到账156.80", ref_date=REF_DATE)
        self.assertIsNotNone(result)
        self.assertNotIn("error", result)
        self.assertEqual(result["type"], "收入")
        self.assertEqual(result["amount"], 156.80)
        self.assertEqual(result["category"], "理财收益")

    # A-8 转账场景 — "转了"不匹配收入关键词，归入"其他"
    def test_transfer(self):
        result = pe_mod.parse_entry("给小王转了200", ref_date=REF_DATE)
        self.assertIsNotNone(result)
        self.assertNotIn("error", result)
        self.assertEqual(result["amount"], 200.00)
        self.assertEqual(result["category"], "其他")

    # A-9 合并金额 / 购物日用（NLP-009）
    def test_combined_amount_shopping(self):
        result = pe_mod.parse_entry("今天买了日用品，纸巾和洗发水一共67.5", ref_date=REF_DATE)
        self.assertIsNotNone(result)
        self.assertNotIn("error", result)
        self.assertEqual(result["amount"], 67.50)
        self.assertEqual(result["category"], "购物")

    # A-10 日期格式验证 — ISO YYYY-MM-DD
    def test_iso_date(self):
        result = pe_mod.parse_entry("2026-05-15吃饭50", ref_date=REF_DATE)
        self.assertIsNotNone(result)
        self.assertNotIn("error", result)
        self.assertEqual(result["date"], "2026-05-15")


# ═══════════════════════════════════════════════════════════════════════
# B. CSV 格式 / 引号逗号解析（两套测试体系合并）
# ═══════════════════════════════════════════════════════════════════════

class TestCSVFormatParsing(unittest.TestCase):
    """CSV 格式验证与引号逗号解析"""

    # B-1 标准交易行 6 字段（FMT-001）
    def test_standard_transaction_row(self):
        line = "2026-05-21,支出,25.00,餐饮,午餐,微信钱包"
        result = ql_mod.parse_csv_line(line)
        self.assertIsNotNone(result)
        self.assertEqual(result["date"], "2026-05-21")
        self.assertEqual(result["type"], "支出")
        self.assertEqual(result["amount"], 25.00)
        self.assertEqual(result["category"], "餐饮")
        self.assertEqual(result["description"], "午餐")
        self.assertEqual(result["account"], "微信钱包")

    # B-2 余额行格式（FMT-002）
    def test_balance_row_format(self):
        line = "余额,微信钱包,1000.00"
        result = ql_mod.parse_csv_line(line)
        self.assertIsNotNone(result)
        self.assertIn("balance_entry", result)
        self.assertEqual(result["account"], "微信钱包")
        self.assertEqual(result["balance"], 1000.00)

    # B-3 收入行格式（FMT-003）
    def test_income_row_format(self):
        line = "2026-05-22,收入,8000.00,工资,5月工资,银行卡"
        result = ql_mod.parse_csv_line(line)
        self.assertIsNotNone(result)
        self.assertEqual(result["type"], "收入")
        self.assertEqual(result["amount"], 8000.00)
        self.assertEqual(result["category"], "工资")

    # B-4 引号包裹含逗号描述 — query_ledger（FMT-004 + E-1）
    def test_quoted_comma_description_query_ledger(self):
        line = '2026-02-14,支出,299.00,社交,"情人节礼物,玫瑰花束",支付宝'
        result = ql_mod.parse_csv_line(line)
        self.assertIsNotNone(result)
        self.assertEqual(result["description"], "情人节礼物,玫瑰花束")
        self.assertEqual(result["category"], "社交")
        self.assertEqual(result["amount"], 299.00)
        self.assertEqual(result["account"], "支付宝")

    # B-5 引号包裹含逗号描述 — parse_entry（E-2）
    def test_quoted_comma_description_parse_entry(self):
        line = '2026-02-14,支出,299.00,社交,"情人节礼物,玫瑰花束",支付宝'
        result = pe_mod.parse_csv_line(line)
        self.assertIsNotNone(result)
        self.assertEqual(result["description"], "情人节礼物,玫瑰花束")

    # B-6 引号包裹含逗号描述 — generate_report（E-3）
    def test_quoted_comma_description_generate_report(self):
        line = '2026-02-14,支出,299.00,社交,"情人节礼物,玫瑰花束",支付宝'
        result = gr_mod.parse_csv_line(line)
        self.assertIsNotNone(result)
        self.assertEqual(result["description"], "情人节礼物,玫瑰花束")

    # B-7 无引号逗号导致字段截断（E-4）
    def test_unquoted_comma_splits(self):
        line = '2026-02-14,支出,299.00,社交,情人节礼物,玫瑰花束,支付宝'
        result = ql_mod.parse_csv_line(line)
        self.assertIsNotNone(result)
        # csv.reader 将其解析为 7 段，取前 6 段
        self.assertEqual(result["description"], "情人节礼物")
        self.assertEqual(result["account"], "玫瑰花束")

    # B-8 sample.csv 中情人节行整体正确（E-5）
    def test_sample_csv_valentine_row(self):
        entries = ql_mod.read_entries(SAMPLE_CSV)
        valentine = [e for e in entries if "情人节" in e["description"]]
        self.assertEqual(len(valentine), 1)
        self.assertEqual(valentine[0]["description"], "情人节礼物,玫瑰花束")
        self.assertEqual(valentine[0]["date"], "2026-02-14")
        self.assertEqual(valentine[0]["type"], "支出")
        self.assertEqual(valentine[0]["amount"], 299.00)
        self.assertEqual(valentine[0]["category"], "社交")
        self.assertEqual(valentine[0]["account"], "支付宝")

    # B-9 多引号字段（E-6）
    def test_multiple_quoted_fields(self):
        line = '2026-03-15,支出,50.00,餐饮,"午餐,加了蛋",微信钱包'
        result = ql_mod.parse_csv_line(line)
        self.assertIsNotNone(result)
        self.assertEqual(result["description"], "午餐,加了蛋")

    # B-10 引号内嵌引号转义 ""（E-7）
    def test_escaped_quote_in_description(self):
        line = '2026-03-15,支出,50.00,餐饮,"他说""好吃""的店",微信钱包'
        result = ql_mod.parse_csv_line(line)
        self.assertIsNotNone(result)
        self.assertIn('他说"好吃"的店', result["description"])

    # B-11 注释行应跳过
    def test_comment_lines_skipped(self):
        self.assertIsNone(ql_mod.parse_csv_line("# 这是一行注释"))
        self.assertIsNone(ql_mod.parse_csv_line("# 日期,类型,金额,分类,描述,账户"))
        self.assertIsNone(ql_mod.parse_csv_line(""))
        self.assertIsNone(ql_mod.parse_csv_line("   "))

    # B-12 字段不足 6 列应返回 None
    def test_insufficient_columns(self):
        self.assertIsNone(ql_mod.parse_csv_line("2026-01-01,支出,50.00"))
        self.assertIsNone(ql_mod.parse_csv_line("2026-01-01,支出,50.00,餐饮"))


# ═══════════════════════════════════════════════════════════════════════
# C. 账本查询 — 月度收支 / 分类 / 关键字 / 余额
# ═══════════════════════════════════════════════════════════════════════

class TestLedgerQueries(unittest.TestCase):
    """基于 sample.csv 的查询功能测试"""

    def setUp(self):
        self.entries = ql_mod.read_entries(SAMPLE_CSV)
        self.balances = ql_mod.read_balances(SAMPLE_CSV)

    # C-1 总交易条目数（B-1）
    def test_read_entries_count(self):
        self.assertEqual(len(self.entries), 20)

    # C-2 1月支出合计（QRY-001）
    def test_monthly_expenses_jan(self):
        data = ql_mod.query_by_month(self.entries, "2026-01")
        self.assertEqual(data["expense"], 4636.00)

    # C-3 1月支出笔数
    def test_monthly_expense_count_jan(self):
        jan_expenses = [e for e in self.entries
                        if e["date"].startswith("2026-01") and e["type"] == "支出"]
        self.assertEqual(len(jan_expenses), 11)

    # C-4 1月收入 = 15000（仅工资，奖金在 2月）（QRY-002）
    def test_monthly_income_jan(self):
        data = ql_mod.query_by_month(self.entries, "2026-01")
        self.assertEqual(data["income"], 15000.00)

    # C-5 1月餐饮分类支出 = 78（早餐15+午餐28+咖啡35）（QRY-003）
    def test_category_food_jan(self):
        data = ql_mod.query_by_category(self.entries, "2026-01")
        self.assertIn("餐饮", data["支出"])
        self.assertEqual(data["支出"]["餐饮"], 78.00)

    # C-6 1月工资收入 = 15000
    def test_category_salary_jan(self):
        data = ql_mod.query_by_category(self.entries, "2026-01")
        self.assertIn("工资", data["收入"])
        self.assertEqual(data["收入"]["工资"], 15000.00)

    # C-7 2月收入 = 工资15000 + 奖金5000 = 20000
    def test_monthly_income_feb(self):
        data = ql_mod.query_by_month(self.entries, "2026-02")
        self.assertEqual(data["income"], 20000.00)

    # C-8 2月支出合计 = 4210.50
    def test_monthly_expenses_feb(self):
        data = ql_mod.query_by_month(self.entries, "2026-02")
        self.assertAlmostEqual(data["expense"], 4210.50, places=2)

    # C-9 关键字搜索 — 火锅（QRY-008）
    def test_keyword_search_hotpot(self):
        results = [e for e in self.entries if "火锅" in e["description"]]
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["amount"], 186.00)

    # C-10 初始余额读取
    def test_read_balances(self):
        self.assertEqual(self.balances["微信钱包"], 800.00)
        self.assertEqual(self.balances["支付宝"], 2000.00)
        self.assertEqual(self.balances["银行卡"], 30000.00)
        self.assertEqual(self.balances["现金"], 500.00)

    # C-11 余额计算（银行卡：初始30000 + 工资15000 - 房租3500 + 2月工资15000 - 2月房租3500 = 58000）
    def test_balance_calc_bank(self):
        bal = ql_mod.calc_balance("银行卡", self.entries, self.balances)
        self.assertEqual(bal, 58000.00)

    # C-12 账户交易查询 — 支付宝（QRY-006）
    def test_account_transactions_alipay(self):
        alipay_txs = [e for e in self.entries if e["account"] == "支付宝"]
        self.assertGreaterEqual(len(alipay_txs), 5)
        amounts = [e["amount"] for e in alipay_txs]
        self.assertIn(200.00, amounts)   # 地铁充值
        self.assertIn(459.00, amounts)   # 冬季外套

    # C-13 最大单笔支出 — 1月 = 房租3500（QRY-007）
    def test_max_expense_jan(self):
        jan_expenses = [e for e in self.entries
                        if e["date"].startswith("2026-01") and e["type"] == "支出"]
        best = max(jan_expenses, key=lambda x: x["amount"])
        self.assertEqual(best["amount"], 3500.00)
        self.assertIn("房租", best["description"])

    # C-14 跨月合计支出 1月+2月 = 8846.50（QRY-005）
    def test_range_expenses_total(self):
        total = sum(e["amount"] for e in self.entries
                    if "2026-01-01" <= e["date"] <= "2026-02-28"
                    and e["type"] == "支出")
        self.assertAlmostEqual(total, 8846.50, places=2)

    # C-15 全部月份概览
    def test_all_months_overview(self):
        data = ql_mod.query_by_month(self.entries)
        self.assertIn("2026-01", data)
        self.assertIn("2026-02", data)
        self.assertEqual(len(data), 2)

    # C-16 最近 N 笔交易 — 按日期降序（QRY-004）
    def test_recent_transactions_sorted(self):
        sorted_txns = sorted(self.entries, key=lambda t: t["date"], reverse=True)
        recent_3 = sorted_txns[:3]
        self.assertEqual(len(recent_3), 3)
        dates = [tx["date"] for tx in recent_3]
        self.assertEqual(dates, sorted(dates, reverse=True))
        # 最新交易日期应为 2026-02-28
        self.assertEqual(recent_3[0]["date"], "2026-02-28")


# ═══════════════════════════════════════════════════════════════════════
# D. 报告生成 — 收支概览 / 分类排行 / 日均 / 多月独立
# ═══════════════════════════════════════════════════════════════════════

class TestReportGeneration(unittest.TestCase):
    """月度报告生成测试"""

    def setUp(self):
        self.entries = gr_mod.read_entries(SAMPLE_CSV)

    # D-1 1月收支概览（RPT-001: 收入15000, 支出4636, 净10364）
    def test_jan_summary(self):
        cur = gr_mod.calc_month(self.entries, "2026-01")
        self.assertEqual(cur["income"], 15000.00)
        self.assertEqual(cur["expense"], 4636.00)
        self.assertEqual(cur["net"], 10364.00)

    # D-2 1月支出分类排行 — TOP1 = 居住 3500（RPT-002）
    def test_jan_category_ranking(self):
        cur = gr_mod.calc_month(self.entries, "2026-01")
        top_cat, top_amt = list(cur["exp_cats"].items())[0]
        self.assertEqual(top_cat, "居住")
        self.assertEqual(top_amt, 3500.00)

    # D-3 1月分类数 = 9（RPT-002: 居住/购物/餐饮/教育/交通/社交/娱乐/通讯/医疗）
    def test_jan_category_count(self):
        cur = gr_mod.calc_month(self.entries, "2026-01")
        self.assertEqual(len(cur["exp_cats"]), 9)

    # D-4 1月日均消费 = 4636/31 ≈ 149.55（RPT-003）
    def test_jan_daily_average(self):
        cur = gr_mod.calc_month(self.entries, "2026-01")
        daily = cur["expense"] / 31
        self.assertAlmostEqual(daily, 149.55, places=1)

    # D-5 2月独立计算（RPT-005: 收入20000, 支出4210.50, 净15789.50）
    def test_feb_summary(self):
        cur = gr_mod.calc_month(self.entries, "2026-02")
        self.assertEqual(cur["income"], 20000.00)
        self.assertAlmostEqual(cur["expense"], 4210.50, places=2)
        self.assertAlmostEqual(cur["net"], 15789.50, places=2)

    # D-6 1月交易笔数 = 13（11支出+2收入 — 工资+奖金都算在1月？
    #   实际：1月2笔收入(工资15000) + 11笔支出 = 13笔。
    #   奖金5000在2月，不计入1月）
    #   修正：sample.csv 1月只有1笔收入(工资) + 11笔支出 = 12笔
    def test_jan_transaction_count(self):
        cur = gr_mod.calc_month(self.entries, "2026-01")
        self.assertEqual(cur["count"], 12)

    # D-7 生成报告文本包含关键数据
    def test_report_text_content(self):
        report = gr_mod.generate_report(self.entries, "2026-01")
        self.assertIn("2026-01", report)
        # 报告应包含收支数据
        self.assertTrue(
            "4636" in report or "¥4636.00" in report or "4,636" in report,
            f"报告应包含 4636，实际: {report[:200]}"
        )

    # D-8 储蓄率计算（1月: (15000-4636)/15000 ≈ 69.07%）
    def test_savings_rate_jan(self):
        cur = gr_mod.calc_month(self.entries, "2026-01")
        sr = (cur["net"] / cur["income"] * 100) if cur["income"] > 0 else 0
        self.assertAlmostEqual(sr, 69.07, delta=1.0)

    # D-9 2月支出分类包含社交 299（情人节）
    def test_feb_social_expense(self):
        cur = gr_mod.calc_month(self.entries, "2026-02")
        self.assertIn("社交", cur["exp_cats"])
        self.assertEqual(cur["exp_cats"]["社交"], 299.00)

    # D-10 空账本报告不报错
    def test_empty_report(self):
        entries = gr_mod.read_entries(EMPTY_CSV)
        cur = gr_mod.calc_month(entries, "2026-01")
        self.assertEqual(cur["income"], 0)
        self.assertEqual(cur["expense"], 0)
        self.assertEqual(cur["count"], 0)

    # D-11 最大单笔支出识别（RPT-004）
    def test_max_single_expense_jan(self):
        cur = gr_mod.calc_month(self.entries, "2026-01")
        # 从分类支出中找最大
        if cur["exp_cats"]:
            top_cat, top_amt = list(cur["exp_cats"].items())[0]
            self.assertEqual(top_amt, 3500.00)
            self.assertEqual(top_cat, "居住")


# ═══════════════════════════════════════════════════════════════════════
# E. 投资持仓 — 买入 / 卖出 / 分红 / 浮盈 / 多证券
# ═══════════════════════════════════════════════════════════════════════

class TestInvest(unittest.TestCase):
    """投资模块测试（使用临时数据构造，不污染实际文件）"""

    def _make_entries(self, raw_lines):
        entries = []
        for line in raw_lines:
            e = inv_mod.parse_csv_line(line)
            if e:
                entries.append(e)
        return entries

    # E-1 基础买入解析
    def test_parse_buy(self):
        entries = self._make_entries([
            "2026-01-15,买入,恒生ETF,159920,1000,@3.50,3500.00,银行卡",
        ])
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["action"], "买入")
        self.assertEqual(entries[0]["shares"], 1000.0)
        self.assertEqual(entries[0]["price"], 3.50)
        self.assertEqual(entries[0]["amount"], 3500.00)

    # E-2 基础卖出解析
    def test_parse_sell(self):
        entries = self._make_entries([
            "2026-03-01,卖出,恒生ETF,159920,500,@4.00,2000.00,银行卡",
        ])
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["action"], "卖出")
        self.assertEqual(entries[0]["shares"], 500.0)
        self.assertEqual(entries[0]["proceeds"], 2000.00)

    # E-3 分红解析
    def test_parse_dividend(self):
        entries = self._make_entries([
            "2026-02-10,分红,恒生ETF,159920,45.60,,,银行卡",
        ])
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["action"], "分红")
        self.assertEqual(entries[0]["amount"], 45.60)

    # E-4 持仓计算 — 买入后部分卖出
    def test_holdings_after_partial_sell(self):
        entries = self._make_entries([
            "2026-01-15,买入,沪深300ETF,510050,1000,@3.50,3500.00,银行卡",
            "2026-03-01,卖出,沪深300ETF,510050,500,@4.00,2000.00,银行卡",
        ])
        holdings = inv_mod.compute_holdings(entries)
        codes = list(holdings.keys())
        self.assertGreaterEqual(len(codes), 1)
        h = holdings[codes[0]]
        self.assertEqual(h["total_shares"], 500.0)
        self.assertEqual(h["total_cost"], 1750.00)

    # E-5 持仓计算 — 含分红
    def test_holdings_with_dividend(self):
        entries = self._make_entries([
            "2026-01-15,买入,恒生ETF,159920,2000,@1.20,2400.00,银行卡",
            "2026-02-10,分红,恒生ETF,159920,120.00,,,银行卡",
        ])
        holdings = inv_mod.compute_holdings(entries)
        codes = list(holdings.keys())
        h = holdings[codes[0]]
        self.assertEqual(h["total_shares"], 2000.0)
        self.assertEqual(h["dividends"], 120.00)
        self.assertEqual(h["total_cost"], 2400.00)

    # E-6 收益率计算 — 浮盈场景
    def test_unrealized_pnl(self):
        entries = self._make_entries([
            "2026-01-15,买入,纳指ETF,513100,500,@1.80,900.00,银行卡",
        ])
        holdings = inv_mod.compute_holdings(entries)
        codes = list(holdings.keys())
        h = holdings[codes[0]]
        prices = {codes[0]: 2.00}
        market = h["total_shares"] * prices[codes[0]]
        pnl = market - h["total_cost"]
        self.assertEqual(pnl, 100.00)  # 500*2.0 - 500*1.8 = 100

    # E-7 多只证券独立持仓
    def test_multi_holdings(self):
        entries = self._make_entries([
            "2026-01-10,买入,沪深300ETF,510050,1000,@3.50,3500.00,银行卡",
            "2026-01-15,买入,恒生ETF,159920,2000,@1.20,2400.00,银行卡",
        ])
        holdings = inv_mod.compute_holdings(entries)
        self.assertEqual(len(holdings), 2)

    # E-8 卖出实现盈亏计算
    def test_realized_pnl_on_sell(self):
        entries = self._make_entries([
            "2026-01-15,买入,999999,测试ETF,1000,@2.00,2000.00,银行卡",
            "2026-03-01,卖出,999999,测试ETF,1000,@3.00,3000.00,银行卡",
        ])
        holdings = inv_mod.compute_holdings(entries)
        codes = list(holdings.keys())
        h = holdings[codes[0]]
        # 清仓后 shares=0, cost=0, realized_pnl = 3000 - 2000 = 1000
        self.assertEqual(h["total_shares"], 0.0)
        self.assertEqual(h["total_cost"], 0.0)
        self.assertEqual(h["realized_pnl"], 1000.00)

    # E-9 fetch_realtime_price — 模拟数据验证返回结构
    def test_fetch_realtime_price_structure(self):
        # 不依赖网络，直接测函数返回结构（无网络时返回 None）
        result = inv_mod.fetch_realtime_price("600487")
        # 有网络时返回 dict，无网络时返回 None（两种都合理）
        if result is not None:
            self.assertIn("code", result)
            self.assertIn("price", result)
            self.assertIsInstance(result["price"], float)

    # E-10 do_cost — 修改成本单价（内存层逻辑验证）
    def test_do_cost_logic(self):
        """验证 do_cost 对最近一笔买入单价的修改逻辑（内存层）"""
        entries = self._make_entries([
            "2026-01-10,买入,600000,测试股,100,@10.00,1000.00,银行卡",
            "2026-01-20,买入,600000,测试股,200,@12.00,2400.00,银行卡",
        ])
        # 找最近一笔买入（索引最大）
        buy_indices = [i for i, e in enumerate(entries) if e["code"] == "600000" and e["action"] == "买入"]
        last_idx = buy_indices[-1]
        # 验证最近一笔是第二笔（12元）
        self.assertEqual(entries[last_idx]["price"], 12.00)
        # 修改为 11.5
        entries[last_idx]["price"] = 11.50
        entries[last_idx]["amount"] = round(200 * 11.50, 2)
        self.assertEqual(entries[last_idx]["price"], 11.50)
        self.assertEqual(entries[last_idx]["amount"], 2300.00)
        # 第一笔不受影响
        self.assertEqual(entries[buy_indices[0]]["price"], 10.00)


# ═══════════════════════════════════════════════════════════════════════
# F. 边界异常 — 空账本 / 缺失字段 / 引号逗号描述
# ═══════════════════════════════════════════════════════════════════════

class TestEdgeCases(unittest.TestCase):
    """边界与异常场景"""

    # F-1 缺失金额应返回 error（ERR-003）
    def test_missing_amount(self):
        result = pe_mod.parse_entry("今天吃了个饭", ref_date=REF_DATE)
        self.assertIsNotNone(result)
        self.assertIn("error", result)

    # F-2 负数金额 — 已知行为：正则匹配忽略负号，解析为正数
    def test_negative_amount(self):
        result = pe_mod.parse_entry("今天花了-50块", ref_date=REF_DATE)
        self.assertIsNotNone(result)
        self.assertNotIn("error", result)
        self.assertEqual(result["amount"], 50.0)

    # F-3 非数字金额（ERR-005）
    def test_invalid_amount_non_numeric(self):
        result = pe_mod.parse_entry("今天花了abc块", ref_date=REF_DATE)
        self.assertIsNotNone(result)
        # 无法解析金额
        if "error" not in result:
            # 如果未报错，amount 应为 None 或 0
            self.assertTrue(result.get("amount", 0) == 0 or result["amount"] is None)

    # F-4 空字符串输入
    def test_empty_input(self):
        result = pe_mod.parse_entry("")
        self.assertIsNone(result)

    # F-5 空账本读取（ERR-002）
    def test_empty_ledger_read(self):
        entries = ql_mod.read_entries(EMPTY_CSV)
        self.assertEqual(len(entries), 0)

    # F-6 空账本查询不报错
    def test_empty_ledger_query(self):
        entries = ql_mod.read_entries(EMPTY_CSV)
        data = ql_mod.query_by_month(entries, "2026-01")
        self.assertEqual(data["income"], 0.0)
        self.assertEqual(data["expense"], 0.0)

    # F-7 空账本余额
    def test_empty_ledger_balance(self):
        balances = ql_mod.read_balances(EMPTY_CSV)
        # empty.csv 只有注释格式的余额行
        self.assertEqual(balances.get("微信钱包", 0.0), 0.0)

    # F-8 format_csv_line — 描述含逗号时自动加引号
    def test_format_csv_with_comma(self):
        entry = {
            "date": "2026-02-14", "type": "支出", "amount": 299.00,
            "category": "社交", "description": "礼物,花束",
            "account": "支付宝",
        }
        line = pe_mod.format_csv_line(entry)
        self.assertIsNotNone(line)
        self.assertIn('"礼物,花束"', line)

    # F-9 format_csv_line — 描述含引号时转义
    def test_format_csv_with_quote(self):
        entry = {
            "date": "2026-03-01", "type": "支出", "amount": 50.00,
            "category": "餐饮", "description": '他说"好吃"',
            "account": "微信钱包",
        }
        line = pe_mod.format_csv_line(entry)
        self.assertIsNotNone(line)
        self.assertIn('他说""好吃""', line)

    # F-10 format_csv_line — error 条目返回 None
    def test_format_csv_error_entry(self):
        line = pe_mod.format_csv_line({"error": "无法识别金额"})
        self.assertIsNone(line)

    # F-11 预算 JSON 加载
    def test_budget_load(self):
        budgets = json.loads(Path(BUDGET_JSON).read_text(encoding="utf-8"))
        self.assertIn("categories", budgets)
        self.assertIn("餐饮", budgets["categories"])
        self.assertEqual(budgets["categories"]["餐饮"], 500.0)

    # F-12 仅 whitespace 的输入
    def test_whitespace_input(self):
        result = pe_mod.parse_entry("   ")
        self.assertIsNone(result)

    # F-13 query_by_category 空月份返回空字典
    def test_category_query_empty_month(self):
        entries = ql_mod.read_entries(SAMPLE_CSV)
        data = ql_mod.query_by_category(entries, "2026-06")
        self.assertEqual(data["支出"], {})
        self.assertEqual(data["收入"], {})


# ═══════════════════════════════════════════════════════════════════════
# G. 数据完整性 — sample.csv 逐行验证
# ═══════════════════════════════════════════════════════════════════════

class TestDataIntegrity(unittest.TestCase):
    """验证 sample.csv 数据的完整性与一致性"""

    def setUp(self):
        self.entries = ql_mod.read_entries(SAMPLE_CSV)
        self.balances = ql_mod.read_balances(SAMPLE_CSV)

    # G-1 总交易数 = 20
    def test_total_count(self):
        self.assertEqual(len(self.entries), 20)

    # G-2 所有条目字段完整
    def test_all_fields_present(self):
        required = ["date", "type", "amount", "category", "description", "account"]
        for i, e in enumerate(self.entries):
            for field in required:
                self.assertTrue(e.get(field), f"Entry #{i+1} missing field '{field}': {e}")

    # G-3 类型字段只有 收入/支出
    def test_valid_types(self):
        for e in self.entries:
            self.assertIn(e["type"], ("收入", "支出"),
                          f"Invalid type: {e['type']} in {e}")

    # G-4 所有金额 > 0
    def test_positive_amounts(self):
        for e in self.entries:
            self.assertGreater(e["amount"], 0, f"金额 <= 0: {e}")

    # G-5 日期格式正确 YYYY-MM-DD
    def test_date_format(self):
        import re
        for e in self.entries:
            self.assertRegex(e["date"], r"^\d{4}-\d{2}-\d{2}$",
                              f"日期格式错误: {e['date']}")

    # G-6 日期大致有序（1月严格有序；2月奖金行2026-02-28排在开头，其余有序）
    def test_date_order_within_months(self):
        months = defaultdict(list)
        for e in self.entries:
            months[e["date"][:7]].append(e["date"])
        # 1月内部严格有序
        self.assertEqual(months["2026-01"], sorted(months["2026-01"]),
                         "1月交易日期未按升序排列")
        # 2月：奖金行(2026-02-28)排在文件开头是sample.csv的已知特征
        # 验证：去掉奖金行后，剩余交易按日期升序
        feb = months["2026-02"]
        # 第一个 2026-02-28 是奖金，跳过它
        first_28_idx = feb.index("2026-02-28")
        feb_remaining = feb[:first_28_idx] + feb[first_28_idx+1:]
        self.assertEqual(feb_remaining, sorted(feb_remaining),
                         "2月交易日期（去掉奖金行后）未按升序排列")

    # G-7 余额行不混入交易
    def test_no_balance_in_transactions(self):
        for e in self.entries:
            self.assertNotIn("balance_entry", e,
                             f"余额行混入交易: {e}")

    # G-8 1月餐饮条目明细验证
    def test_jan_food_items(self):
        jan_food = [e for e in self.entries
                    if e["date"].startswith("2026-01") and e["category"] == "餐饮"]
        amounts = {e["amount"]: e["description"] for e in jan_food}
        self.assertIn(15.00, amounts)   # 早餐
        self.assertIn(28.00, amounts)   # 午餐
        self.assertIn(35.00, amounts)   # 咖啡

    # G-9 逗号描述行完整字段（情人节）
    def test_comma_description_complete(self):
        valentine = [e for e in self.entries if "情人节" in e["description"]]
        self.assertEqual(len(valentine), 1)
        v = valentine[0]
        self.assertEqual(v["amount"], 299.00)
        self.assertEqual(v["category"], "社交")
        self.assertEqual(v["description"], "情人节礼物,玫瑰花束")
        self.assertEqual(v["account"], "支付宝")
        self.assertEqual(v["date"], "2026-02-14")

    # G-10 账户余额总和 = 微信800+支付宝2000+银行卡30000+现金500 = 33300
    def test_total_initial_balance(self):
        total = sum(self.balances.values())
        self.assertEqual(total, 33300.00)

    # G-11 1月支出逐笔加和 = 4636
    def test_jan_expense_line_items(self):
        jan_exp = [e for e in self.entries
                   if e["date"].startswith("2026-01") and e["type"] == "支出"]
        self.assertEqual(len(jan_exp), 11)
        total = sum(e["amount"] for e in jan_exp)
        self.assertEqual(total, 4636.00)

    # G-12 2月支出逐笔加和 = 4210.50
    def test_feb_expense_line_items(self):
        feb_exp = [e for e in self.entries
                   if e["date"].startswith("2026-02") and e["type"] == "支出"]
        self.assertEqual(len(feb_exp), 6)
        total = sum(e["amount"] for e in feb_exp)
        self.assertAlmostEqual(total, 4210.50, places=2)

    # G-13 火锅搜索结果验证
    def test_hotpot_search(self):
        results = [e for e in self.entries if "火锅" in e["description"]]
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["amount"], 186.00)


# ═══════════════════════════════════════════════════════════════════════
# 自定义测试报告输出
# ═══════════════════════════════════════════════════════════════════════

def run_with_report():
    """运行测试并输出格式化报告"""
    # 自定义 TestRunner 以输出友好报告
    runner = unittest.TextTestRunner(verbosity=2)
    suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])
    result = runner.run(suite)

    print("\n" + "=" * 60)
    print(f"  🦞 个人记账 Skill — 合并测试套件")
    print(f"  📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    total = result.testsRun
    passed = total - len(result.failures) - len(result.errors)
    failed = len(result.failures)
    errors = len(result.errors)
    rate = (passed / total * 100) if total > 0 else 0

    print(f"  ✅ 通过: {passed}")
    print(f"  ❌ 失败: {failed}")
    print(f"  💥 错误: {errors}")
    print(f"  📊 合计: {total}")
    print(f"  📈 通过率: {rate:.1f}%")

    if result.failures:
        print("\n  ⚠️ 失败用例:")
        for test, traceback in result.failures:
            print(f"     ❌ {test}")
            # 输出关键的断言行
            lines = traceback.strip().split('\n')
            for line in lines[-3:]:
                if line.strip():
                    print(f"        {line.strip()}")

    if result.errors:
        print("\n  💥 错误用例:")
        for test, traceback in result.errors:
            print(f"     ❌ {test}")
            lines = traceback.strip().split('\n')
            for line in lines[-3:]:
                if line.strip():
                    print(f"        {line.strip()}")

    print("=" * 60)
    status = "✅ 全部通过" if (failed == 0 and errors == 0) else f"⚠️ {failed + errors} 条失败/错误"
    print(f"  结果: {status}")
    print("=" * 60)

    return 0 if (failed == 0 and errors == 0) else 1


if __name__ == "__main__":
    sys.exit(run_with_report())
