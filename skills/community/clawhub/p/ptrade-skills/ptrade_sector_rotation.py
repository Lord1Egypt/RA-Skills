#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
热点行业轮动 + 移动止损策略 - PTrade 实盘版
策略: 每月初选最强赛道ETF，8%移动止损兜底
基于 Skill 文件学习生成 (2026-04-10)
Update: 2026-04-10 17:40
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
logger = logging.getLogger("SectorRotation")

# ============================================================
# 全局参数
# ============================================================
# 5大核心赛道 ETF（高弹性、流动性充裕）
SECTOR_ETFS = [
    "512760.SH",   # 半导体ETF
    "515790.SH",   # 光伏ETF
    "512880.SH",   # 证券ETF
    "512010.SH",   # 医药ETF
    "159915.SZ",   # 创业板ETF
]

MOMENTUM_WINDOW = 20         # 动量回看天数（20天）
TRAILING_STOP_PCT = 0.08     # 移动止损：从最高点回撤8%清仓
TRADE_DAYS = [1]             # 每月1日调仓（月初）
LOOKBACK_PERIOD = 60         # 数据回看天数


_context = {
    "position": None,         # 当前持仓ETF
    "entry_price": 0.0,       # 买入价
    "high_price": 0.0,        # 持仓期间最高价
    "entry_date": None,       # 买入日期
    "nav": 1.0,
    "nav_high": 1.0,
    "data_cache": {},
}


def init(context):
    logger.info("热点行业轮动+移动止损策略初始化 | ETF池：{} | 动量窗口{}天 | 移动止损{}%".format(
        len(SECTOR_ETFS), MOMENTUM_WINDOW, int(TRAILING_STOP_PCT * 100)))
    run("09:25")


def before_trading_start(context, data):
    _context["data_cache"]["global"] = data


def scheduled(context, data):
    """每月1日调仓"""
    day = context.now.day
    weekday = context.now.weekday()

    if day not in TRADE_DAYS:
        return

    logger.info("月初调仓日：{}".format(context.now.strftime("%Y-%m-%d")))
    rebalance(context, data)


def rebalance(context, data):
    """
    调仓逻辑
    1. 获取5只ETF的20日动量
    2. 选涨幅最强的ETF（全仓）
    3. 如果持仓中已有这只ETF，跳过（不重复买卖）
    4. 切换赛道：先卖后买
    """
    prev_date = get_prev_trade_date(context.now.strftime("%Y-%m-%d"))
    start_date = (datetime.now() - timedelta(days=LOOKBACK_PERIOD)).strftime("%Y-%m-%d")

    # 批量获取数据
    df_all = get_price(
        securities=SECTOR_ETFS,
        start_date=start_date,
        end_date=prev_date,
        frequency="1d",
        fields=["close"],
        adjust_type="post"
    )

    momentum_scores = []
    for etf in SECTOR_ETFS:
        df_etf = df_all[df_all["security"] == etf].tail(MOMENTUM_WINDOW + 1)
        if len(df_etf) < MOMENTUM_WINDOW + 1:
            continue
        price_start = df_etf["close"].iloc[0]
        price_end = df_etf["close"].iloc[-1]
        if price_start > 0:
            momentum = (price_end - price_start) / price_start
            momentum_scores.append({
                "etf": etf,
                "momentum": momentum,
                "price": price_end,
            })
            logger.info("  {} 20日动量：{:.2%}".format(etf, momentum))

    if not momentum_scores:
        logger.warning("无有效ETF数据")
        return

    # 选动量最强的ETF
    momentum_scores.sort(key=lambda x: x["momentum"], reverse=True)
    best = momentum_scores[0]

    logger.info("最强赛道：{} 动量{:.2%}".format(best["etf"], best["momentum"]))

    # 如果当前持仓就是这只，不动
    if _context["position"] == best["etf"]:
        logger.info("持仓不变：{}".format(best["etf"]))
        return

    # ---- 切换：先卖后买 ----
    # 卖出
    if _context["position"] is not None:
        sell_etf(context, data, _context["position"])

    # 买入
    buy_etf(context, data, best["etf"], best["price"])


def on_bar(context, data):
    """每日收盘：移动止损检查"""
    if _context["position"] is None:
        return

    current_price = data[_context["position"]].close

    # 更新最高价
    if current_price > _context["high_price"]:
        _context["high_price"] = current_price
        logger.info("新高：{} @ {}".format(_context["position"], current_price))

    # 移动止损检查
    trailing_stop = _context["high_price"] * (1 - TRAILING_STOP_PCT)
    drawdown = (current_price - _context["high_price"]) / _context["high_price"]

    if current_price <= trailing_stop:
        pnl = (current_price - _context["entry_price"]) / _context["entry_price"]
        logger.info("移动止损出局：{} 回撤{:.1%} 盈亏{:.1%}".format(
            _context["position"], drawdown, pnl))
        sell_etf(context, data, _context["position"])
        return

    # 指数黑天鹅检查（如果持仓的是宽基ETF）
    check_black_swan(context, data)


def check_black_swan(context, data):
    """黑天鹅检查：指数跌幅≥3%减仓，≥5%清仓"""
    # 用沪深300作为大盘代表
    index = "000300.SH"
    prev_date = get_prev_trade_date(context.now.strftime("%Y-%m-%d"))

    idx_df = get_price(
        securities=[index],
        start_date=prev_date,
        end_date=prev_date,
        frequency="1d",
        fields=["close"]
    )
    if len(idx_df) < 2:
        return

    idx_today = idx_df["close"].iloc[-1]
    idx_prev = idx_df["close"].iloc[-2]
    idx_change = (idx_today - idx_prev) / idx_prev

    if idx_change <= -0.05:
        logger.warning("大盘暴跌{}%，清仓".format(idx_change * 100))
        sell_etf(context, data, _context["position"])
    elif idx_change <= -0.03:
        logger.warning("大盘下跌{}%，减半仓".format(idx_change * 100))
        pos = _context.get("shares", 0)
        if pos > 0:
            half = pos // 2
            order_shares(_context["position"], half)


def buy_etf(context, data, etf, price):
    """全仓买入ETF"""
    try:
        available = context.portfolio.available_cash
        shares = int(available / price / 100) * 100
        if shares < 100:
            logger.warning("资金不足，无法买入")
            return
        order_shares(etf, shares)
        _context["position"] = etf
        _context["entry_price"] = price
        _context["high_price"] = price
        _context["entry_date"] = context.now.strftime("%Y-%m-%d")
        _context["shares"] = shares
        logger.info("买入：{} {}股@{}元".format(etf, shares, price))
    except Exception as e:
        logger.error("买入失败：{} - {}".format(etf, e))


def sell_etf(context, data, etf):
    """清仓ETF"""
    try:
        order_shares(etf, 0)
        logger.info("卖出：{}".format(etf))
        _context["position"] = None
        _context["entry_price"] = 0.0
        _context["high_price"] = 0.0
        _context["entry_date"] = None
        _context["shares"] = 0
    except Exception as e:
        logger.error("卖出失败：{} - {}".format(etf, e))


def on_order_filled(context, order):
    if _context["position"] == order["security"]:
        _context["shares"] = order["filled_shares"]


def on_strategy_end(context):
    logger.info("策略结束，最终净值：{:.4f}".format(_context["nav"]))
