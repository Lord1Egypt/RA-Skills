"""indicators 模块单元测试"""
import pytest
from stock_realtime_brief.indicators import (
    calc_ma,
    calc_all_mas,
    derive_stop_loss,
    calc_composite_score,
    judge_stance,
)


# ====== MA 测试 ======

def test_calc_ma_basic():
    closes = [100, 102, 104, 103, 105]
    assert calc_ma(closes, 5) == 102.8


def test_calc_ma_insufficient_data():
    assert calc_ma([100, 102], 5) is None


def test_calc_all_mas():
    closes = list(range(1, 31))  # 1..30
    mas = calc_all_mas(closes)
    assert mas["ma5"] == 28.0
    assert mas["ma10"] == 25.5
    assert mas["ma20"] == 20.5
    assert mas["ma30"] == 15.5


# ====== 止损位测试 ======

def test_stop_loss_basic():
    rt = {"price": 100}
    hist = {"ma5": 98, "ma10": 95, "ma20": 90}
    sl = derive_stop_loss(rt, hist, cost=80)
    assert sl is not None
    assert sl["warn_line"] is not None
    assert sl["risk_line"] is not None


def test_stop_loss_profit_lock():
    """盈利 > 30% 应有利润保护位"""
    rt = {"price": 150}
    hist = {"ma5": 140, "ma10": 130, "ma20": 120}
    sl = derive_stop_loss(rt, hist, cost=100)  # 盈利 50%
    assert sl["profit_lock"] is not None
    # 利润保护位 = 现价 - 25% 利润 = 150 - 12.5 = 137.5
    assert sl["profit_lock"] == 137.5


def test_stop_loss_loss_state():
    """亏损股清仓线 = 成本 -25%"""
    rt = {"price": 80}
    hist = {"ma5": 82, "ma10": 85, "ma20": 90}
    sl = derive_stop_loss(rt, hist, cost=100)  # 亏 20%
    assert sl["cut_line"] == 75.0  # 100 * 0.75


def test_stop_loss_margin_uplift():
    """融资股止损位上提 3%"""
    rt = {"price": 100}
    hist = {"ma5": 95, "ma10": 90, "ma20": 85}
    sl_normal = derive_stop_loss(rt, hist)
    sl_margin = derive_stop_loss(rt, hist, has_margin=True)
    assert sl_margin["risk_line"] > sl_normal["risk_line"]


def test_stop_loss_no_data():
    assert derive_stop_loss(None, None) is None
    assert derive_stop_loss({}, {}) is None


# ====== 综合评分测试 ======

def test_composite_score_strong():
    rt = {"price": 110, "pct_change": 5, "volume": 1500000}
    hist = {"last": 110, "ma5": 100, "ma20": 90, "avg_vol5": 1000000}
    score = calc_composite_score(rt, hist)
    assert score > 5  # 应为强势分


def test_composite_score_weak():
    rt = {"price": 90, "pct_change": -5, "volume": 1500000}
    hist = {"last": 90, "ma5": 100, "ma20": 110, "avg_vol5": 1000000}
    score = calc_composite_score(rt, hist)
    assert score < -5  # 应为弱势分


def test_composite_score_no_data():
    assert calc_composite_score(None, None) == 0


# ====== 态势速判 ======

def test_judge_stance_bullish():
    rt = {"price": 110, "pct_change": 2}
    hist = {"ma5": 105, "ma10": 100, "ma20": 95}
    assert "多头" in judge_stance(rt, hist) or "上攻" in judge_stance(rt, hist)


def test_judge_stance_bearish():
    rt = {"price": 90, "pct_change": -2}
    hist = {"ma5": 95, "ma10": 100, "ma20": 105}
    assert "空头" in judge_stance(rt, hist) or "下跌" in judge_stance(rt, hist)


def test_judge_stance_no_data():
    assert "数据不足" in judge_stance(None, None) or "数据不全" in judge_stance(None, None)
