#!/usr/bin/env python3
"""YH8.5 双引擎回测脚本 — 回测 ST/BB20 信号胜率/盈亏/回撤"""
import os, sys, argparse
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import ccxt
import numpy as np
import pandas as pd
from datetime import datetime, timezone, timedelta

from strategies.yh8_engine import YH8Engine
from strategies.playbook_manager import get_playbook


def load_historical_data(symbols, days, timeframe='30m'):
    """拉取历史 K线"""
    exchange = ccxt.binanceusdm({'enableRateLimit': True})
    data = {}
    since_ms = int((datetime.now(timezone.utc) - timedelta(days=days + 10)).timestamp() * 1000)
    for sym in symbols:
        try:
            ex_sym = sym.replace('/USDT', '/USDT:USDT')
            ohlcv = exchange.fetch_ohlcv(ex_sym, timeframe, since=since_ms, limit=2000)
            if len(ohlcv) < 100:
                continue
            df = pd.DataFrame(ohlcv, columns=['ts', 'open', 'high', 'low', 'close', 'volume'])
            df['ts'] = pd.to_datetime(df['ts'], unit='ms')
            df.set_index('ts', inplace=True)
            cutoff = df.index[-1] - timedelta(days=days)
            df = df[df.index >= cutoff]
            if len(df) >= 50:
                data[sym] = df
        except Exception as e:
            print(f"  ⚠️ {sym} 加载失败: {e}")
    return data


class PaperSimulator:
    """简单回测模拟器：TP/SL 固定百分比"""

    def __init__(self, tp_pct=0.02, sl_pct=0.015, max_hold_hours=24):
        self.tp_pct = tp_pct
        self.sl_pct = sl_pct
        self.max_hold_hours = max_hold_hours
        self.positions = []
        self.trades = []

    def open(self, sym, side, entry, ts, strategy):
        self.positions.append({'symbol': sym, 'side': side, 'entry': entry,
                               'open_ts': ts, 'strategy': strategy})

    def update(self, sym, bar_time, high, low, close):
        for pos in list(self.positions):
            if pos['symbol'] != sym:
                continue
            hold_h = (bar_time - pos['open_ts']) / 3600
            exit_p = None
            reason = None
            if pos['side'] == 'long':
                if high >= pos['entry'] * (1 + self.tp_pct):
                    exit_p, reason = pos['entry'] * (1 + self.tp_pct), 'tp'
                elif low <= pos['entry'] * (1 - self.sl_pct):
                    exit_p, reason = pos['entry'] * (1 - self.sl_pct), 'sl'
            else:
                if low <= pos['entry'] * (1 - self.tp_pct):
                    exit_p, reason = pos['entry'] * (1 - self.tp_pct), 'tp'
                elif high >= pos['entry'] * (1 + self.sl_pct):
                    exit_p, reason = pos['entry'] * (1 + self.sl_pct), 'sl'
            if reason is None and hold_h >= self.max_hold_hours:
                exit_p, reason = close, 'timeout'
            if reason:
                pnl_pct = (exit_p - pos['entry']) / pos['entry'] * 100
                if pos['side'] == 'short':
                    pnl_pct = -pnl_pct
                self.trades.append({'symbol': sym, 'side': pos['side'], 'strategy': pos['strategy'],
                                    'pnl_pct': pnl_pct, 'reason': reason})
                self.positions.remove(pos)

    def stats(self):
        if not self.trades:
            return {'trades': 0, 'win_rate': 0, 'avg_pnl': 0, 'total_pnl': 0}
        wins = [t for t in self.trades if t['pnl_pct'] > 0]
        pnls = [t['pnl_pct'] for t in self.trades]
        return {'trades': len(self.trades),
                'win_rate': round(len(wins) / len(self.trades) * 100, 1),
                'avg_pnl': round(sum(pnls) / len(pnls), 4),
                'total_pnl': round(sum(pnls), 2)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--days', type=int, default=30)
    ap.add_argument('--coins', type=str, default='BTC/USDT,ETH/USDT,XRP/USDT')
    ap.add_argument('--timeframe', type=str, default='30m')
    args = ap.parse_args()

    symbols = [s.strip() for s in args.coins.split(',') if s.strip()]
    pb = get_playbook()
    engine = YH8Engine()
    print(f"🔬 YH8.5 回测 | {args.days}天 | {len(symbols)}币")
    print("📥 加载历史数据...")
    data = load_historical_data(symbols, args.days, args.timeframe)
    if not data:
        print("❌ 无数据")
        return

    sim = PaperSimulator()
    signal_count = 0
    for sym, df in data.items():
        trend_sid = pb.data.get('coin_assignments', {}).get(sym, {}).get('trend')
        range_sid = pb.data.get('coin_assignments', {}).get(sym, {}).get('range')
        allowed = 'both' if (trend_sid and range_sid) else ('trend' if trend_sid else ('range' if range_sid else 'both'))
        bar_count = len(df)
        for i in range(200, bar_count, 5):
            window = df.iloc[:i + 1].copy()
            ts = df.index[i].timestamp()
            try:
                sig = engine.scan(sym, window, allowed=allowed)
            except Exception:
                continue
            if sig is None or not sig.get('entry'):
                continue
            signal_count += 1
            sim.open(sym, sig.get('side', 'long'), sig['entry'], ts, sig.get('strategy', 'unknown'))
        for pos in list(sim.positions):
            if pos['symbol'] != sym:
                continue
            lb = df.iloc[-1]
            sim.update(sym, df.index[-1].timestamp(), float(lb['high']), float(lb['low']), float(lb['close']))

    for pos in list(sim.positions):
        if pos['symbol'] in data:
            lb = data[pos['symbol']].iloc[-1]
            sim.update(pos['symbol'], data[pos['symbol']].index[-1].timestamp(),
                       float(lb['high']), float(lb['low']), float(lb['close']))

    s = sim.stats()
    print(f"\n📊 结果: 信号={signal_count} 交易={s['trades']} 胜率={s['win_rate']}% "
          f"平均PnL={s['avg_pnl']}% 累计={s['total_pnl']}%")


if __name__ == '__main__':
    main()
