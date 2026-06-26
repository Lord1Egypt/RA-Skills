"""portfolio 模块单元测试"""
import json
import os
import pytest
from pathlib import Path
from stock_realtime_brief.portfolio import (
    load_portfolio,
    calc_position_metrics,
    calc_guarantee_ratio,
    grade_guarantee_ratio,
    risk_rank_key,
    resolve_portfolio_path,
)


@pytest.fixture
def sample_portfolio(tmp_path):
    data = {
        "margin_debt": 100000,
        "positions": [
            {
                "symbol": "300750",
                "name": "宁德时代",
                "buy_price": 200.0,
                "amount": 500,
                "account": "普通",
            },
            {
                "symbol": "300750",  # 同一只票，融资账户
                "name": "宁德时代",
                "buy_price": 220.0,
                "amount": 100,
                "account": "融资",
            },
            {
                "symbol": "600519",
                "name": "贵州茅台",
                "buy_price": 1700.0,
                "amount": 100,
                "account": "普通",
            },
        ],
    }
    path = tmp_path / "test_portfolio.json"
    path.write_text(json.dumps(data, ensure_ascii=False))
    return path


def test_load_portfolio_merges_same_symbol(sample_portfolio):
    holdings, margin = load_portfolio(sample_portfolio)
    # 同一股票多笔应合并
    cosmik = [h for h in holdings if h["code"] == "300750"]
    assert len(cosmik) == 1
    # 加权平均成本: (500*200 + 100*220) / 600 = 203.33
    assert abs(cosmik[0]["cost"] - 203.33) < 0.05
    assert cosmik[0]["amount"] == 600
    assert cosmik[0]["has_margin"] is True
    assert margin == 100000


def test_load_portfolio_compatible_field_names(tmp_path):
    """支持 holdings/positions, code/symbol, cost/buy_price, shares/amount"""
    data = {
        "holdings": [{
            "code": "600519",
            "name": "贵州茅台",
            "cost": 1700,
            "shares": 100,
        }],
    }
    path = tmp_path / "alt_format.json"
    path.write_text(json.dumps(data))
    holdings, _ = load_portfolio(path)
    assert len(holdings) == 1
    assert holdings[0]["code"] == "600519"


def test_calc_position_metrics():
    holdings = [
        {"code": "300750", "cost": 200.0, "amount": 500, "has_margin": False, "name": "宁德", "sector": ""},
    ]
    rt_map = {"300750": {"price": 240.0}}
    holdings, total_mv = calc_position_metrics(holdings, rt_map)
    h = holdings[0]
    assert h["price"] == 240.0
    assert h["mv"] == 120000  # 240*500
    assert h["pnl"] == 20000  # (240-200)*500
    assert h["pnl_pct"] == 20.0
    assert total_mv == 120000


def test_guarantee_ratio_grade():
    assert "强平" in grade_guarantee_ratio(140)
    assert "强警告" in grade_guarantee_ratio(155)
    assert "警戒" in grade_guarantee_ratio(165)
    assert "可控" in grade_guarantee_ratio(180)
    assert "安全" in grade_guarantee_ratio(300)


def test_risk_rank_loss_margin_first():
    """亏损 + 融资的应排最前"""
    h_loss_margin = {"is_loss": True, "has_margin": True, "is_heavy": False, "hist": {}}
    h_normal = {"is_loss": False, "has_margin": False, "is_heavy": False, "hist": {}}
    h_heavy_loss = {"is_loss": True, "has_margin": False, "is_heavy": True, "hist": {}}

    holdings = [h_normal, h_loss_margin, h_heavy_loss]
    sorted_h = sorted(holdings, key=risk_rank_key)
    # 亏损融资分最高 → 排最前
    assert sorted_h[0] is h_loss_margin


def test_resolve_path_priority(tmp_path, monkeypatch):
    """三层路径优先级：参数 > env > cwd"""
    # 创建三个不同的文件
    arg_file = tmp_path / "arg.json"
    arg_file.write_text("{}")
    env_file = tmp_path / "env.json"
    env_file.write_text("{}")

    # 1. 参数优先
    monkeypatch.setenv("STOCK_BRIEF_PORTFOLIO", str(env_file))
    assert resolve_portfolio_path(str(arg_file)) == arg_file

    # 2. 没参数 → 环境变量
    assert resolve_portfolio_path() == env_file

    # 3. 都没 → 找 cwd
    monkeypatch.delenv("STOCK_BRIEF_PORTFOLIO")
    monkeypatch.chdir(tmp_path)
    cwd_file = tmp_path / "portfolio.json"
    cwd_file.write_text("{}")
    # 返回的是相对路径 portfolio.json，解析后应指向 cwd_file
    resolved = resolve_portfolio_path()
    assert resolved is not None
    assert resolved.resolve() == cwd_file.resolve()
