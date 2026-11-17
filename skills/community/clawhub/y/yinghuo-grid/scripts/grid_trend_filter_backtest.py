#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
手工网格 + ST趋势过滤器 回测 (2026-10-07)
==========================================
验证「趋势时暂停马丁加仓」能降多少回撤，供用户拍板是否挂上趋势过滤器。

对比两组（同一锚仓起点）：
  A. 无过滤器  —— 一直马丁加仓（现状）
  B. 有过滤器  —— close < EMA(趋势线) 时暂停加仓（趋势结束恢复）

核心逻辑对齐 manual_grid_atr.py：
  - 马丁加仓：跌 spacing 加一仓（前3格×1.5、第4格起×1.7，5格封顶）
  - 单格止盈：涨 spacing 减最近一格（LIFO）
  - 总止盈两档：浮盈20%减50%、30%全平
  - 总止损两档：浮亏15%减50%、25%全平

用法:
  venv/bin/python3 grid_trend_filter_backtest.py --days 90 --coins BTC/USDT,ETH/USDT,XRP/USDT
  venv/bin/python3 grid_trend_filter_backtest.py --days 90 --atr-mult 1.0
"""
import os, sys, argparse, time as _time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ccxt
import numpy as np
import pandas as pd
from datetime import datetime, timezone, timedelta


def load_recent_ohlcv(symbol, timeframe='1h', days=90):
    """分页拉取最近 days 天的完整 K线（覆盖最近的下跌/上涨周期）"""
    ex = ccxt.binanceusdm({'enableRateLimit': True})
    ex_sym = symbol.replace('/USDT', '/USDT:USDT')
    since_ms = int((datetime.now(timezone.utc) - timedelta(days=days)).timestamp() * 1000)
    bars = []
    cursor = since_ms
    while True:
        try:
            batch = ex.fetch_ohlcv(ex_sym, timeframe, since=cursor, limit=1000)
        except Exception as e:
            print(f"  ❌ {symbol} 拉取失败: {e}")
            break
        if not batch:
            break
        bars.extend(batch)
        last_ts = batch[-1][0]
        if last_ts <= cursor or len(batch) < 1000:
            break
        cursor = last_ts + 1
        _time.sleep(0.3)
    if not bars:
        return None
    bars = sorted(set(tuple(b) for b in bars))
    df = pd.DataFrame(bars, columns=['ts', 'open', 'high', 'low', 'close', 'volume'])
    df['ts'] = pd.to_datetime(df['ts'], unit='ms')
    df.set_index('ts', inplace=True)
    return df

# ── 参数（对齐 manual_grid_atr.py）──
ATR_PERIOD = 14
FIRST_NOTIONAL = 20.0
MARTINGALE_TIER1 = 1.5
MARTINGALE_TIER2 = 1.7
TIER1_LEVELS = 3
MAX_LEVELS = 5
TP_LEVELS = [(0.20, 0.50), (0.30, 1.00)]
SL_LEVELS = [(0.15, 0.50), (0.25, 1.00)]
ANCHOR_NOTIONAL = 100.0          # 锚仓固定名义（回测统一口径）
EMA_PERIOD = 453                 # 趋势线周期


def compute_atr(df, period=ATR_PERIOD):
    """Wilder ATR"""
    high, low, close = df['high'], df['low'], df['close']
    tr = np.maximum(high - low,
                    np.maximum((high - close.shift(1)).abs(), (low - close.shift(1)).abs()))
    atr = tr.ewm(alpha=1.0 / period, adjust=False).mean()
    return atr


def compute_ema(series, period):
    return series.ewm(span=period, adjust=False).mean()


class GridSim:
    """做多网格模拟器（锚仓 + 马丁加仓 + 单格止盈 + 总止盈止损）"""

    def __init__(self, atr_mult=1.0, trend_filter=False, ema_period=EMA_PERIOD):
        self.atr_mult = atr_mult
        self.trend_filter = trend_filter
        self.ema_period = ema_period
        self.reset()

    def reset(self):
        self.anchor_entry = None
        self.anchor_qty = 0.0
        self.levels = []            # [{entry, qty, notional}]
        self.realized = 0.0
        self.add_count = 0
        self.blocked_count = 0
        self.tp_stage = 0
        self.sl_stage = 0
        self.equity_curve = []

    def open_anchor(self, price):
        self.anchor_entry = price
        self.anchor_qty = ANCHOR_NOTIONAL / price

    def _notional_for_level(self, level_no):
        """第 level_no 格（1-based）的马丁名义"""
        if level_no <= TIER1_LEVELS:
            mult = MARTINGALE_TIER1 ** (level_no - 1)
        else:
            mult = (MARTINGALE_TIER1 ** (TIER1_LEVELS - 1)) * \
                   (MARTINGALE_TIER2 ** (level_no - TIER1_LEVELS))
        return FIRST_NOTIONAL * mult

    def _avg_entry(self):
        tq = self.anchor_qty + sum(l['qty'] for l in self.levels)
        if tq <= 0:
            return self.anchor_entry
        tc = self.anchor_qty * self.anchor_entry + sum(l['qty'] * l['entry'] for l in self.levels)
        return tc / tq

    def _last_ref(self):
        return self.levels[-1]['entry'] if self.levels else self.anchor_entry

    def _total_qty(self):
        return self.anchor_qty + sum(l['qty'] for l in self.levels)

    def _equity(self, price):
        avg = self._avg_entry()
        upnl = (price - avg) * self._total_qty()
        return self.realized + upnl

    def _spacing(self, atr, price):
        return max(self.atr_mult * atr, 0.003 * price)

    def _reduce_pct(self, price, pct):
        """减当前总仓位的 pct 比例，实现盈亏（LIFO 先减网格仓再减锚仓）"""
        total_qty = self._total_qty()
        if total_qty <= 0:
            return
        reduce_qty = total_qty * pct
        # LIFO：先减网格仓
        while reduce_qty > 1e-12 and self.levels:
            l = self.levels[-1]
            take = min(l['qty'], reduce_qty)
            self.realized += (price - l['entry']) * take
            l['qty'] -= take
            reduce_qty -= take
            if l['qty'] <= 1e-12:
                self.levels.pop()
        # 剩余减锚仓
        if reduce_qty > 1e-12:
            take = min(self.anchor_qty, reduce_qty)
            self.realized += (price - self.anchor_entry) * take
            self.anchor_qty -= take
            reduce_qty -= take

    def step(self, price, atr, trend_on):
        """处理一根 bar：总止盈止损 → 单格止盈 → 加仓"""
        if self.anchor_entry is None:
            return
        spacing = self._spacing(atr, price)
        avg = self._avg_entry()
        pnl_pct = (price - avg) / avg if avg > 0 else 0.0

        # 1. 总止盈止损（优先级最高）
        if pnl_pct >= 0:
            if pnl_pct >= TP_LEVELS[1][0] and self.tp_stage < 2:
                self._reduce_pct(price, TP_LEVELS[1][1])
                self.tp_stage = 2
                return
            if pnl_pct >= TP_LEVELS[0][0] and self.tp_stage < 1:
                self._reduce_pct(price, TP_LEVELS[0][1])
                self.tp_stage = 1
                return
        else:
            loss = -pnl_pct
            if loss >= SL_LEVELS[1][0] and self.sl_stage < 2:
                self._reduce_pct(price, SL_LEVELS[1][1])
                self.sl_stage = 2
                return
            if loss >= SL_LEVELS[0][0] and self.sl_stage < 1:
                self._reduce_pct(price, SL_LEVELS[0][1])
                self.sl_stage = 1
                return

        # 2. 单格止盈（涨 spacing 减最近一格）
        if self.levels:
            ref = self._last_ref()
            if price >= ref + spacing:
                l = self.levels[-1]
                self.realized += (price - l['entry']) * l['qty']
                self.levels.pop()
                return

        # 3. 马丁加仓（跌 spacing 加一格）
        if len(self.levels) >= MAX_LEVELS:
            return
        ref = self._last_ref()
        if price <= ref - spacing:
            if self.trend_filter and trend_on:
                self.blocked_count += 1
                return
            level_no = len(self.levels) + 1
            notional = self._notional_for_level(level_no)
            qty = notional / price
            self.levels.append({'entry': price, 'qty': qty, 'notional': notional})
            self.add_count += 1

    def run(self, df, warmup=500):
        """遍历回测。返回指标 dict"""
        self.reset()
        atr = compute_atr(df)
        ema = compute_ema(df['close'], self.ema_period)
        self.open_anchor(float(df['close'].iloc[warmup]))

        for i in range(warmup, len(df)):
            price = float(df['close'].iloc[i])
            a = atr.iloc[i]
            if pd.isna(a) or a <= 0:
                continue
            trend_on = False
            if self.trend_filter:
                e = ema.iloc[i]
                trend_on = not pd.isna(e) and price < float(e)  # close < EMA = 下跌趋势
            self.step(price, float(a), trend_on)
            self.equity_curve.append(self._equity(price))

        # 指标
        eq = np.array(self.equity_curve)
        max_dd_u = 0.0
        max_dd_pct = 0.0
        if len(eq) > 0:
            peak = np.maximum.accumulate(eq)
            dd_u = peak - eq  # 回撤金额（U）
            max_dd_u = float(dd_u.max())
            max_dd_pct = max_dd_u / ANCHOR_NOTIONAL * 100  # 相对锚仓名义
        final_eq = float(eq[-1]) if len(eq) else 0.0
        return {
            'final_equity': final_eq,
            'max_dd': max_dd_u,
            'max_dd_pct': max_dd_pct,
            'add_count': self.add_count,
            'blocked_count': self.blocked_count,
            'remaining_qty': self._total_qty(),
            'realized': self.realized,
        }


def _fmt(tag, s):
    return (f"  {tag}: 期末权益={s['final_equity']:+.2f}U 回撤={s['max_dd']:.2f}U({s['max_dd_pct']:.1f}%) "
            f"加仓={s['add_count']}次 拦截={s['blocked_count']}次 "
            f"已实现={s['realized']:+.2f}U 剩余仓={s['remaining_qty']:.4f}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--days', type=int, default=90)
    ap.add_argument('--coins', type=str, default='BTC/USDT,ETH/USDT,XRP/USDT,ZEN/USDT,DOT/USDT')
    ap.add_argument('--atr-mult', type=float, default=1.0)
    ap.add_argument('--ema-period', type=int, default=EMA_PERIOD)
    args = ap.parse_args()

    symbols = [s.strip() for s in args.coins.split(',') if s.strip()]
    print(f"🔬 手工网格 + 趋势过滤器 回测 | {args.days}天 | ATR乘数={args.atr_mult} | EMA{args.ema_period}")
    print(f"   币种: {', '.join(symbols)}")
    print()

    print("📥 加载历史数据...")
    data = {}
    for sym in symbols:
        df = load_recent_ohlcv(sym, timeframe='1h', days=args.days)
        if df is None or len(df) < 600:
            print(f"  ⚠️ {sym}: 数据不足")
            continue
        data[sym] = df
        print(f"  ✅ {sym}: {len(df)} bars, {df.index[0]} → {df.index[-1]}")
    if not data:
        print("❌ 无数据，终止")
        return
    print()

    print("=" * 64)
    print("逐币对比 (A=无过滤器/一直加仓 | B=有过滤器/趋势停加仓):")
    print("=" * 64)
    agg = {'A': {'dd': [], 'eq': [], 'add': 0, 'blocked': 0},
           'B': {'dd': [], 'eq': [], 'add': 0, 'blocked': 0}}
    for sym, df in data.items():
        simA = GridSim(atr_mult=args.atr_mult, trend_filter=False, ema_period=args.ema_period)
        rA = simA.run(df)
        simB = GridSim(atr_mult=args.atr_mult, trend_filter=True, ema_period=args.ema_period)
        rB = simB.run(df)
        print(f"\n【{sym}】{len(df)} bars")
        print(_fmt("A 无过滤", rA))
        print(_fmt("B 有过滤", rB))
        print(f"  → 回撤变化: {rA['max_dd']:.2f}U → {rB['max_dd']:.2f}U ({rB['max_dd'] - rA['max_dd']:+.2f}U)")
        print(f"  → 期末权益变化: {rA['final_equity']:+.2f} → {rB['final_equity']:+.2f}U ({rB['final_equity'] - rA['final_equity']:+.2f}U)")
        agg['A']['dd'].append(rA['max_dd']); agg['A']['eq'].append(rA['final_equity'])
        agg['A']['add'] += rA['add_count']; agg['A']['blocked'] += rA['blocked_count']
        agg['B']['dd'].append(rB['max_dd']); agg['B']['eq'].append(rB['final_equity'])
        agg['B']['add'] += rB['add_count']; agg['B']['blocked'] += rB['blocked_count']

    print("\n" + "=" * 64)
    print("汇总:")
    print(f"  A 无过滤: 平均回撤={np.mean(agg['A']['dd']):.2f}U 总期末权益={np.sum(agg['A']['eq']):+.2f}U 总加仓={agg['A']['add']}")
    print(f"  B 有过滤: 平均回撤={np.mean(agg['B']['dd']):.2f}U 总期末权益={np.sum(agg['B']['eq']):+.2f}U 总加仓={agg['B']['add']} (拦截{agg['B']['blocked']}次)")
    print(f"\n💡 结论：若 B 回撤明显更低且权益损失可控 → 建议挂趋势过滤器；否则维持现状。")


if __name__ == '__main__':
    main()
