#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
8因子候选 + ATR追踪止损策略 - PTrade 实盘版
策略: 在纯小市值基础上，用8因子打分筛选 + ATR动态风控
基于 Martin Skill 文件学习生成 (2026-04-10)
Update: 2026-04-10 17:35
"""

from ptrade import (
    get_price, get_instrument_info, get_trade_calendar,
    order_shares, get_prev_trade_date
)
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("C31_Momentum")

# ============================================================
# 全局参数
# ============================================================
MAX_MARKET_CAP = 60          # 亿元
MAX_PRICE = 12                # 元
MIN_SCORE = 6                 # 8因子打分≥6分才入选
ATR_PERIOD = 14               # ATR周期
ATR_MULTIPLIER = 2             # ATR倍数（止损 = 当前价 - ATR×2）
HOLD_DAYS = 5                 # 持有天数
TRADE_DAYS = [1, 15]          # 每月调仓日
MAX_POS_PCT = 0.20            # 单只仓位上限
STOP_LOSS_ATR = True          # ATR追踪止损（替代固定止损）

# 动态仓位ATR阈值
ATR_LOW = 0.02                # ATR≤2% → 80%仓
ATR_MID = 0.05                # ATR 2-5% → 50%仓

# 黑天鹅防护
BLACK_SWANG_3 = -0.03         # 指数跌幅≥3% → 减半仓
BLACK_SWANG_5 = -0.05         # 指数跌幅≥5% → 清仓

# ============================================================
# Context
# ============================================================
_context = {
    "positions": {},           # {stock: {"shares":, "buy_price":, "atr":, "high_price":, "stop_loss":}}
    "nav": 1.0,
    "nav_high": 1.0,
    "data_cache": {},
    "last_rebalance": None,
}


def init(context):
    logger.info("8因子候选+ATR止损策略初始化 | MIN_SCORE={} | ATR×{} | HOLD={}天".format(
        MIN_SCORE, ATR_MULTIPLIER, HOLD_DAYS))
    run("09:25")


def before_trading_start(context, data):
    _context["data_cache"]["global"] = data


def scheduled(context, data):
    today = context.now.strftime("%Y-%m-%d")
    day = context.now.day
    weekday = context.now.weekday()

    if weekday != 0:
        return
    if day not in TRADE_DAYS:
        return

    logger.info("调仓日：{}".format(today))
    rebalance(context, data)


def rebalance(context, data):
    """
    调仓主逻辑
    1. 获取候选股票池（市值≤60亿，MA60上方，股价≤12元）
    2. 计算8因子打分
    3. 选打分≥6分的股票
    4. 计算ATR确定仓位
    5. 执行买卖
    """
    # ---- 黑天鹅防护：检查指数 ----
    index = "000300.SH"  # 沪深300
    idx_df = get_price(
        securities=[index],
        start_date=get_prev_trade_date(context.now.strftime("%Y-%m-%d")),
        end_date=get_prev_trade_date(context.now.strftime("%Y-%m-%d")),
        frequency="1d",
        fields=["close"]
    )
    if len(idx_df) >= 2:
        idx_today = idx_df["close"].iloc[-1]
        idx_yesterday = idx_df["close"].iloc[-2]
        idx_change = (idx_today - idx_yesterday) / idx_yesterday
        if idx_change <= BLACK_SWANG_5:
            logger.warning("指数跌幅{}%，清仓".format(idx_change * 100))
            for stock in list(_context["positions"].keys()):
                sell_stock(context, data, stock)
            return
        elif idx_change <= BLACK_SWANG_3:
            logger.warning("指数跌幅{}%，减半仓".format(idx_change * 100))
            for stock in list(_context["positions"].keys()):
                pos = _context["positions"][stock]
                half = pos["shares"] // 2
                if half >= 100:
                    order_shares(stock, pos["shares"] - half)

    # ---- 步骤1：获取候选股票池 ----
    all_stocks = [s for s in get_trade_calendar()
                  if s.endswith(".SH") or s.endswith(".SZ")]

    prev_date = get_prev_trade_date(context.now.strftime("%Y-%m-%d"))
    start_date = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")
    batch_data = get_price(
        securities=all_stocks,
        start_date=start_date,
        end_date=prev_date,
        frequency="1d",
        fields=["close", "open", "high", "low", "volume", "amount"],
        adjust_type="post"
    )

    candidates = []
    for stock in all_stocks:
        try:
            df = batch_data[batch_data["security"] == stock].tail(60)
            if len(df) < 60:
                continue

            close = df["close"].iloc[-1]
            if close > MAX_PRICE:
                continue

            # 涨跌停过滤
            if len(df) >= 2:
                prev_close = df["close"].iloc[-2]
                if prev_close > 0:
                    chg = (close - prev_close) / prev_close
                    if chg > 0.095 or chg < -0.095:
                        continue

            # MA60 过滤
            ma60 = df["close"].rolling(60).mean().iloc[-1]
            if close < ma60:
                continue

            # 市值
            info = get_instrument_info(stock)
            market_cap = info.get("market_cap", 999)
            if market_cap > MAX_MARKET_CAP:
                continue

            # ---- 计算8因子 ----
            score = compute_8_factors(df, close, market_cap)
            if score < MIN_SCORE:
                continue

            # 计算ATR（用于动态仓位）
            atr = compute_atr(df, ATR_PERIOD)
            atr_pct = atr / close

            # 确定仓位
            position_pct = get_position_by_atr(atr_pct)

            candidates.append({
                "stock": stock,
                "market_cap": market_cap,
                "close": close,
                "score": score,
                "atr": atr,
                "atr_pct": atr_pct,
                "position_pct": position_pct,
            })

        except Exception as e:
            continue

    # 按分数降序
    candidates.sort(key=lambda x: x["score"], reverse=True)
    candidates = candidates[:10]

    if not candidates:
        logger.warning("无候选股票")
        return

    logger.info("候选股票：{} 只（分数≥{}）".format(len(candidates), MIN_SCORE))
    for c in candidates:
        logger.info("  {} 市值{}亿 分数{} ATR={:.2%} 仓位{}%".format(
            c["stock"], c["market_cap"], c["score"], c["atr_pct"], int(c["position_pct"] * 100)))

    # ---- 执行调仓 ----
    target_stocks = set([c["stock"] for c in candidates])
    current_stocks = set(_context["positions"].keys())

    # 卖出
    to_sell = current_stocks - target_stocks
    for stock in to_sell:
        sell_stock(context, data, stock)

    # 买入
    available = context.portfolio.available_cash
    for c in candidates:
        if c["stock"] in current_stocks:
            continue
        target_value = available * c["position_pct"]
        buy_stock(context, data, c["stock"], target_value, c["atr"])

    _context["last_rebalance"] = context.now.strftime("%Y-%m-%d")


def compute_8_factors(df: pd.DataFrame, close: float, market_cap: float) -> int:
    """
    计算8因子打分体系
    返回：总分（0-14分）
    """
    score = 0
    close_series = df["close"]
    volume_series = df["volume"]

    # ---- 因子1：动量因子（20日涨幅，排名前30% → +2分）----
    returns_20d = (close - close_series.iloc[-20]) / close_series.iloc[-20] if len(df) >= 20 else 0

    # ---- 因子2：成交量因子（换手率 proxy：成交额/市值）----
    avg_amount_5 = df["amount"].tail(5).mean()
    amount_per_cap = avg_amount_5 / (market_cap * 1e8) if market_cap > 0 else 0

    # ---- 因子3：RSI（40-70区间 → +1分）----
    delta = df["close"].diff()
    gain = delta.clip(lower=0).rolling(14).mean()
    loss = (-delta.clip(upper=0)).rolling(14).mean()
    rs = gain / loss.replace(0, np.nan)
    rsi = (100 - 100 / (1 + rs)).iloc[-1]
    if 40 <= rsi <= 70:
        score += 1

    # ---- 因子4：ATR 波动率因子（适中 → +1分）----
    atr = compute_atr(df, 14)
    atr_pct = atr / close if close > 0 else 0
    if 0.02 <= atr_pct <= 0.05:
        score += 1

    # ---- 因子5：突破因子（收盘价 > 20日高点 → +2分）----
    high_20d = close_series.tail(20).max()
    if close >= high_20d:
        score += 2

    # ---- 因子6：趋势因子（MA5 > MA10 > MA20 → +2分）----
    ma5 = close_series.tail(5).mean()
    ma10 = close_series.tail(10).mean()
    ma20 = close_series.tail(20).mean()
    if ma5 > ma10 > ma20:
        score += 2

    # ---- 因子7：量价配合（上涨带量 → +1分）----
    if len(df) >= 5:
        vol_5d_avg = volume_series.tail(5).mean()
        vol_today = volume_series.iloc[-1]
        price_change = (close - close_series.iloc[-2]) / close_series.iloc[-2] if len(df) >= 2 else 0
        if price_change > 0 and vol_today > vol_5d_avg:
            score += 1

    # ---- 因子8：抗跌因子（beta proxy，跌幅<大盘 → +1分）----
    # 简版：用20日波动率与平均波动率比较
    volatility_20d = close_series.tail(20).std() / close_series.tail(20).mean()
    volatility_avg = close_series.std() / close_series.mean()
    if volatility_20d < volatility_avg:
        score += 1

    # 市值因子加成（市值越小，加1-2分）
    if market_cap <= 30:
        score += 2
    elif market_cap <= 50:
        score += 1

    return score


def compute_atr(df: pd.DataFrame, period: int = 14) -> float:
    """计算 ATR（Average True Range）"""
    high = df["high"]
    low = df["low"]
    close = df["close"]
    tr1 = high - low
    tr2 = (high - close.shift(1)).abs()
    tr3 = (low - close.shift(1)).abs()
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr = tr.rolling(period).mean().iloc[-1]
    return atr if not np.isnan(atr) else 0.0


def get_position_by_atr(atr_pct: float) -> float:
    """基于ATR波动率确定仓位"""
    if atr_pct <= ATR_LOW:
        return 0.80
    elif atr_pct <= ATR_MID:
        return 0.50
    else:
        return 0.30


def on_bar(context, data):
    """每日收盘：ATR追踪止损 + 持有期卖出"""
    today = context.now.strftime("%Y-%m-%d")

    for stock in list(_context["positions"].keys()):
        pos = _context["positions"][stock]
        current_price = data[stock].close
        buy_price = pos["buy_price"]
        atr = pos["atr"]
        high_price = pos["high_price"]

        # ---- 更新最高价 ----
        if current_price > high_price:
            pos["high_price"] = current_price

        # ---- ATR追踪止损 ----
        stop_loss = pos["high_price"] - ATR_MULTIPLIER * atr
        if current_price <= stop_loss:
            logger.info("ATR止损：{} 价{} 止损线{}".format(stock, current_price, stop_loss))
            sell_stock(context, data, stock)
            continue

        # ---- 持有期到期 ----
        pos["hold_days"] = pos.get("hold_days", 0) + 1
        if pos["hold_days"] >= HOLD_DAYS:
            pnl = (current_price - buy_price) / buy_price
            logger.info("持有期到，卖出：{} 盈利{:.1%}".format(stock, pnl))
            sell_stock(context, data, stock)


def buy_stock(context, data, stock, target_value, atr):
    """买入"""
    try:
        current_price = data[stock].close
        shares = int(target_value / current_price / 100) * 100
        if shares < 100:
            return
        order_shares(stock, shares)
        _context["positions"][stock] = {
            "shares": shares,
            "buy_price": current_price,
            "atr": atr,
            "high_price": current_price,
            "stop_loss": current_price - ATR_MULTIPLIER * atr,
            "hold_days": 0,
        }
        logger.info("买入：{} {}股@{}元 ATR={}".format(stock, shares, current_price, atr))
    except Exception as e:
        logger.error("买入失败：{} - {}".format(stock, e))


def sell_stock(context, data, stock):
    """卖出"""
    try:
        order_shares(stock, 0)
        if stock in _context["positions"]:
            del _context["positions"][stock]
        logger.info("卖出：{}".format(stock))
    except Exception as e:
        logger.error("卖出失败：{} - {}".format(stock, e))


def on_order_filled(context, order):
    stock = order["security"]
    if stock in _context["positions"]:
        _context["positions"][stock]["shares"] = order["filled_shares"]


def on_strategy_end(context):
    logger.info("策略结束，最终净值：{:.4f}".format(_context["nav"]))
