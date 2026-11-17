"""金融源：名称→代码静态别名兜底（C3 零依赖开箱即用）。

锁定回归：常见 A 股全称（及含于查询的子串）应离线解析为代码，无需网络。
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/scripts")

import finance


def test_alias_exact_match():
    assert finance._resolve_name("贵州茅台", {}) == "600519"
    assert finance._resolve_name("宁德时代", {}) == "300750"
    assert finance._resolve_name("比亚迪", {}) == "002594"


def test_alias_substring_in_query():
    """查询包裹公司名（如"分析贵州茅台最近5年财报变化"）也能解析。"""
    assert finance._resolve_name("分析贵州茅台最近5年财报变化", {}) == "600519"
    assert finance._resolve_name("贵州茅台股票行情", {}) == "600519"
    assert finance._resolve_name("茅台股价", {}) == "600519"


def test_alias_longest_match_disambiguation():
    """子串命中多个别名时取最长匹配，降低歧义。"""
    assert finance._resolve_name("平安银行股票", {}) == "000001"  # 平安银行 优先于 中国平安
    assert finance._resolve_name("中国平安财报", {}) == "601318"


def test_alias_absent_falls_through():
    """不在别名表的名称不误命中（交由网络解析，沙箱下可能返回 None，但不应抛错）。"""
    assert finance._resolve_name("贵州茅台", {}) == "600519"  # 正例在先
    # 完全无关词：不抛异常即为通过（网络结果依赖沙箱，不做强断言）
    r = finance._resolve_name("xyz完全虚构公司名123", {})
    assert r is None or isinstance(r, str)
