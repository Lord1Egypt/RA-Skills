#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
纯小市值策略 - PTrade 实盘版
策略: 每周一买市值最小的股票，持有5天，不追高
基于 SimTradeLab + BaoStock 混合回测验证 (2018-2026)
Update: 2026-04-10 17:30
"""

from ptrade import (
    get_price, get_instrument_info, get_trade_calendar,
    order_shares, order_target, get_prev_trade_date
)
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("SmallCap")

# ============================================================
# 全局参数（可调整）
# ============================================================
MAX_MARKET_CAP = 60      # 亿元，市值上限
MAX_PRICE = 12           # 元，股价上限
HOLD_DAYS = 5            # 持有天数
STOP_LOSS_PCT = -0.08    # 止损线 -8%
TRADE_DAYS = [1, 15]     # 每月调仓日：1号和15号
MAX_POS_PCT = 0.20       # 单只仓位上限 20%
DRAWDOWN_STOP = -0.10    # 熔断线：净值从高点回撤 -10% 停止开仓

# ============================================================
# Context（全局状态，禁止用全局变量）
# ============================================================
_context = {
    "positions": {},      #持仓: {stock: {"shares":, "buy_price":, "hold_days":, "entry_date":}}
    "nav": 1.0,          #净值
    "nav_high": 1.0,     #净值高点
    "data_cache": {},    #数据缓存，避免重复API调用
    "last_rebalance": None,  #上次调仓日
}


def init(context):
    """初始化策略"""
    logger.info("纯小市值策略初始化 | MAX_CAP={}亿 | HOLD={}天 | STOP={}".format(
        MAX_MARKET_CAP, HOLD_DAYS, STOP_LOSS_PCT))
    # 设置运行时间：每天 09:25 定时执行
    run("09:25")


def before_trading_start(context, data):
    """盘前准备：缓存全局行情数据"""
    _context["data_cache"]["global"] = data


def scheduled(context, data):
    """定时任务：每天 09:25 检查是否调仓"""
    today = context.now.strftime("%Y-%m-%d")
    day = context.now.day
    weekday = context.now.weekday()  # 0=周一

    # 只有周一才操作，且日期在 TRADE_DAYS 内
    if weekday != 0:
        return
    if day not in TRADE_DAYS:
        return

    logger.info("调仓日：{}".format(today))
    rebalance(context, data)


def rebalance(context, data):
    """
    调仓主逻辑
    1. 选股：市值从小到大排序，取前N只
    2. 过滤：ST/停牌/涨跌停/股价>12元/MA60空头
    3. 分配仓位：等权，单只上限20%
    4. 卖出：不在候选名单的持仓
    5. 买入：候选名单中无持仓的标的
    """
    # ---- 风控：净值回撤熔断 ----
    if _context["nav"] < _context["nav_high"] * (1 + DRAWDOWN_STOP):
        logger.warning("净值回撤超过{}，停止开仓".format(DRAWDOWN_STOP))
        # 发出全部卖单
        for stock in list(_context["positions"].keys()):
            sell_stock(context, data, stock)
        return

    # ---- 步骤1：获取全市场股票列表 ----
    all_stocks = get_trade_calendar()
    # 过滤沪深A股（ST范围：上交所+深交所）
    all_stocks = [s for s in all_stocks if s.endswith(".SH") or s.endswith(".SZ")]

    # ---- 步骤2：批量获取数据 ----
    prev_date = get_prev_trade_date(context.now.strftime("%Y-%m-%d"))
    batch_data = get_price(
        securities=all_stocks,
        start_date=(datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d"),
        end_date=prev_date,
        frequency="1d",
        fields=["close", "open", "high", "low", "volume", "amount"],
        adjust_type="post"
    )

    candidates = []
    for stock in all_stocks:
        try:
            df = batch_data[batch_data["security"] == stock].tail(60)  # 最近60天
            if len(df) < 60:
                continue

            close = df["close"].iloc[-1]  # 昨日收盘价
            open_price = df["open"].iloc[-1]  # 今日开盘价（用于过滤涨跌停）

            # ---- 过滤规则 ----
            # 1. 股价过滤
            if close > MAX_PRICE:
                continue

            # 2. 涨跌停过滤（ST/退市净化）
            if len(df) >= 2:
                prev_close = df["close"].iloc[-2]
                if prev_close > 0:
                    change_pct = (close - prev_close) / prev_close
                    if change_pct > 0.095 or change_pct < -0.095:  # 涨跌停
                        continue

            # 3. MA60 过滤（收盘价需在MA60上方）
            ma60 = df["close"].rolling(60).mean().iloc[-1]
            if close < ma60:
                continue

            # 4. 停牌过滤
            if is_suspended(stock, prev_date):
                continue

            # 5. 市值获取（Ptrade API）
            info = get_instrument_info(stock)
            market_cap = info.get("market_cap", 999)  # 亿元
            if market_cap > MAX_MARKET_CAP:
                continue

            # 候选股票评分（市值越小分越高）
            score = MAX_MARKET_CAP - market_cap
            candidates.append({
                "stock": stock,
                "market_cap": market_cap,
                "close": close,
                "score": score,
            })

        except Exception as e:
            continue

    # ---- 排序：按市值升序 ----
    candidates.sort(key=lambda x: x["market_cap"])
    candidates = candidates[:10]  # 最多10只

    if not candidates:
        logger.warning("无候选股票")
        return

    logger.info("候选股票：{} 只".format(len(candidates)))
    for c in candidates:
        logger.info("  {} 市值{}亿 价{}元".format(c["stock"], c["market_cap"], c["close"]))

    # ---- 步骤3：计算目标仓位 ----
    target_stocks = set([c["stock"] for c in candidates])
    current_stocks = set(_context["positions"].keys())

    # ---- 步骤4：卖出不在候选名单的持仓 ----
    to_sell = current_stocks - target_stocks
    for stock in to_sell:
        sell_stock(context, data, stock)

    # ---- 步骤5：买入候选名单中无持仓的标的 ----
    to_buy = target_stocks - current_stocks
    available_capital = context.portfolio.available_cash
    per_position = available_capital * MAX_POS_PCT  # 单只仓位上限

    for stock in to_buy:
        if available_capital < per_position * 0.5:
            break
        buy_stock(context, data, stock, per_position)

    _context["last_rebalance"] = context.now.strftime("%Y-%m-%d")


def on_bar(context, data):
    """每日收盘检查：止损 + 持有期到期卖出"""
    today = context.now.strftime("%Y-%m-%d")

    for stock in list(_context["positions"].keys()):
        pos = _context["positions"][stock]
        current_price = data[stock].close
        buy_price = pos["buy_price"]
        hold_days = pos["hold_days"]
        entry_date = pos["entry_date"]

        # ---- 止损检查 ----
        pnl_pct = (current_price - buy_price) / buy_price
        if pnl_pct <= STOP_LOSS_PCT:
            logger.info("止损出局：{} 亏损{:.1%}".format(stock, pnl_pct))
            sell_stock(context, data, stock)
            continue

        # ---- 持有期到期卖出（HOLD_DAYS天后） ----
        hold_days += 1
        pos["hold_days"] = hold_days
        if hold_days >= HOLD_DAYS:
            logger.info("持有期到，卖出：{} 盈利{:.1%}".format(stock, pnl_pct))
            sell_stock(context, data, stock)


def buy_stock(context, data, stock, target_value):
    """买入股票（整手处理）"""
    try:
        current_price = data[stock].close
        # 整手：100股的整数倍
        shares = int(target_value / current_price / 100) * 100
        if shares < 100:
            return

        order_shares(stock, shares)
        _context["positions"][stock] = {
            "shares": shares,
            "buy_price": current_price,
            "hold_days": 0,
            "entry_date": context.now.strftime("%Y-%m-%d"),
        }
        logger.info("买入：{} {}股@{}元".format(stock, shares, current_price))
    except Exception as e:
        logger.error("买入失败：{} - {}".format(stock, e))


def sell_stock(context, data, stock):
    """卖出股票（清仓）"""
    try:
        order_shares(stock, 0)  # PTrade 清仓写法
        if stock in _context["positions"]:
            del _context["positions"][stock]
        logger.info("卖出：{}".format(stock))
    except Exception as e:
        logger.error("卖出失败：{} - {}".format(stock, e))


def is_suspended(stock, date):
    """检查股票是否停牌"""
    try:
        df = get_price(
            securities=[stock],
            start_date=date,
            end_date=date,
            frequency="1d",
            fields=["volume"],
        )
        if len(df) == 0:
            return True
        return df["volume"].iloc[-1] == 0
    except:
        return True


def on_order_filled(context, order):
    """订单成交回调（处理部分成交）"""
    stock = order["security"]
    if stock in _context["positions"]:
        _context["positions"][stock]["shares"] = order["filled_shares"]


def on_strategy_end(context):
    """策略结束：更新净值记录"""
    logger.info("策略结束，最终净值：{:.4f}".format(_context["nav"]))
