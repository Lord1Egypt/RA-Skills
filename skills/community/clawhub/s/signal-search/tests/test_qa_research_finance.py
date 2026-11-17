"""研究编排层：金融意图 schema 适配（C2）。

锁定回归：research() 对含"财报/营收"等金融意图的查询，应生成金融分析维度
（营业收入/归母净利润/每股收益/ROE/同比变动）而非通用百科模板，且能拿到金融来源。
不依赖抖动网络（monkeypatch finance.fetch）。
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/scripts")

import finance
import research


def _fake_finance_fetch(query, cfg=None, web_fetch=None):
    """模拟金融源返回一份多年财报 doc（含布局所需关键词）。"""
    text = (
        "# 东方财富 f10 财报（业绩报表）：贵州茅台(600519)\n"
        "最新报告期: 2025-03-31\n"
        "营业收入: 514.43 亿元（同比 10.67%）\n"
        "归母净利润: 268.47 亿元（同比 11.56%）\n"
        "基本每股收益: 21.38 元  加权平均ROE: 13.63%\n"
        "近年年度业绩：\n"
        "- 2024-12-31：营收 1741.44 亿元（同比 15.66%） | 归母净利润 862.28 亿元 | EPS 68.64 | ROE 34.46%\n"
    )
    return [
        {
            "url": "https://emweb.securities.eastmoney.com/PC_HSF10/NewFinanceAnalysis/Index?"
            "type=web&code=S600519",
            "text": text,
            "snippet": text[:240],
            "engine": "eastmoney-f10",
            "source_type": "finance_report",
            "landing_resolved": True,
            "secid": "1.600519",
            "code": "600519",
            "name": "贵州茅台",
            "citation": {
                "key": "eastmoney-f10-600519",
                "stock_code": "600519",
                "name": "贵州茅台",
                "source": "eastmoney-f10",
            },
        }
    ], []


_FINANCE_SCHEMA = ["营业收入", "归母净利润", "每股收益", "ROE", "同比变动"]


def test_research_finance_schema_adaptation(monkeypatch):
    monkeypatch.setattr(finance, "fetch", _fake_finance_fetch)
    res = research.research("分析贵州茅台最近5年财报变化", cfg={})
    names = [d["name"] for d in res["schema"]]
    assert names == _FINANCE_SCHEMA, f"金融意图应套用金融维度模板，实际 {names}"
    assert len(res["sources"]) >= 1, "应拿到金融来源"
    assert any(s.get("source_type") == "finance_report" for s in res["sources"])
    # 编排层合成 findings 应把金融维度铺开（而非"无来源"空壳）
    assert "营业收入" in res["findings"] and "归母净利润" in res["findings"]


def test_research_nonfinance_keeps_default_schema(monkeypatch):
    """非金融查询仍用通用百科模板（对照组）。"""
    monkeypatch.setattr(finance, "fetch", _fake_finance_fetch)
    res = research.research("分析量子纠缠的物理原理", cfg={})
    names = [d["name"] for d in res["schema"]]
    assert "定义与概念" in names, f"通用查询应保留百科模板，实际 {names}"
    assert "营业收入" not in names, "通用查询不应套金融维度"
