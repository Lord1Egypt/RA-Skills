#!/usr/bin/env python3
"""text_cleaner.py 单元测试"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from text_cleaner import clean_announcement_text, get_stats


class TestCleanAnnouncementText:
    """测试正文清洗功能"""

    def test_empty_input(self):
        """测试空输入"""
        assert clean_announcement_text("") == ""
        assert clean_announcement_text(None) == ""

    def test_normal_text(self):
        """测试正常文本（无模板文字）"""
        text = "这是一条正常的公告内容，没有模板文字。"
        result = clean_announcement_text(text)
        assert result == text

    def test_remove_stock_code_header(self):
        """测试移除股票代码表头"""
        text = "证券代码：600519 证券简称：贵州茅台 公告编号：2026-001\n这是正文内容"
        result = clean_announcement_text(text)
        assert "证券代码" not in result
        assert "证券简称" not in result
        assert "这是正文内容" in result

    def test_remove_board_disclaimer(self):
        """测试移除董事会免责声明"""
        text = "本公司及董事会全体成员保证信息披露的内容真实、准确、完整，没有虚假记载、误导性陈述或重大遗漏，并承担法律责任。这是正文内容"
        result = clean_announcement_text(text)
        assert "保证信息披露" not in result
        assert "虚假记载" not in result
        assert "这是正文内容" in result

    def test_remove_special_notice(self):
        """测试移除'特此公告'"""
        text = "这是正文内容\n特此公告\n贵州茅台董事会\n2026年6月14日"
        result = clean_announcement_text(text)
        assert "特此公告" not in result
        assert "这是正文内容" in result

    def test_remove_page_numbers(self):
        """测试移除页码"""
        text = "这是正文内容\n第1页 共3页\n更多内容"
        result = clean_announcement_text(text)
        assert "第1页" not in result
        assert "共3页" not in result
        assert "这是正文内容" in result
        assert "更多内容" in result

    def test_remove_stock_info_line(self):
        """测试移除股票信息行"""
        text = "股票简称：申万宏源 股票代码：000166\n这是正文内容"
        result = clean_announcement_text(text)
        assert "股票简称" not in result
        assert "股票代码" not in result
        assert "这是正文内容" in result

    def test_remove_empty_lines(self):
        """测试移除多余空行"""
        text = "这是第一行\n\n\n\n这是第二行"
        result = clean_announcement_text(text)
        assert "\n\n\n" not in result
        assert "这是第一行" in result
        assert "这是第二行" in result

    def test_preserve重要内容(self):
        """测试保留实质性内容"""
        text = "证券代码：600519 证券简称：贵州茅台\n本公司及董事会全体成员保证信息披露的内容真实、准确、完整。\n公司拟回购股份，金额不超过10亿元。"
        result = clean_announcement_text(text)
        assert "公司拟回购股份" in result
        assert "10亿元" in result

    def test_multiple_patterns(self):
        """测试同时存在多种模板文字"""
        text = """证券代码：600519 证券简称：贵州茅台 公告编号：2026-001
本公司及董事会全体成员保证信息披露的内容真实、准确、完整，没有虚假记载、误导性陈述或重大遗漏，并承担法律责任。
这是正文内容，包含重要信息。
特此公告
贵州茅台董事会
2026年6月14日"""
        result = clean_announcement_text(text)
        assert "证券代码" not in result
        assert "保证信息披露" not in result
        assert "特此公告" not in result
        assert "这是正文内容" in result
        assert "重要信息" in result


class TestGetStats:
    """测试统计功能"""

    def test_basic_stats(self):
        """测试基本统计"""
        original = "这是原始文本，包含一些内容。"
        cleaned = "这是清洗后文本。"
        stats = get_stats(original, cleaned)
        assert stats["original_chars"] == len(original)
        assert stats["cleaned_chars"] == len(cleaned)
        assert stats["saved_chars"] == len(original) - len(cleaned)
        assert stats["saved_pct"] > 0

    def test_empty_original(self):
        """测试空原始文本"""
        stats = get_stats("", "清洗后")
        assert stats["original_chars"] == 0
        assert stats["cleaned_chars"] == len("清洗后")
        assert stats["saved_pct"] == 0

    def test_identical_text(self):
        """测试相同文本"""
        text = "相同文本"
        stats = get_stats(text, text)
        assert stats["saved_chars"] == 0
        assert stats["saved_pct"] == 0
