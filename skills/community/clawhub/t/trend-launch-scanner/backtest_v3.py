#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A股回测引擎 v3 - 基于趋势扫描系统的正确股票池
- 股票池: stock_pool_merged.py (309只精选股)
- 买入评分: score_v2.py (>=80分买入)
- 卖出评分: sell_signal.py (>=70分卖出)
- 回测期: 2026-03-01 至 2026-03-31
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import argparse, json, math, random, warnings
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, asdict, field
from datetime import datetime, timedelta
from pathlib import Path
from threading import Lock

import numpy as np
import pandas as pd
import requests
warnings.filterwarnings('ignore')

# ── 参数配置 ──────────────────────────────────────────────────────
BUY_TH   = 80   # 买入阈值
SELL_TH  = 70   # 卖出阈值
MAX_POS  = 10   # 最大持仓数
INIT_CASH = 40000.0  # 初始资金
STOP_LOSS = -0.10    # 止损线 -10%
MAX_HOLD  = 30       # 最大持有天数
POS_SIZE  = INIT_CASH / MAX_POS  # 每仓金额

# ── 路径配置 ──────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).parent
SKILL_DIR  = Path('C:/Users/Administrator/.qclaw/workspace-ag01/skills/trend-launch-scanner')
sys.path.insert(0, str(SKILL_DIR))

from stock_pool_merged import get_merged_stock_list as get_pool
from score_v2 import calc_score_v2

# ── 指标计算 ────────────────────────────────────────────────────────
def add_indicators(df):
    if df is None or len(df) < 20:
        return df
    df = df.copy()
    c = df['close']
    df['ma5']  = c.rolling(5).mean()
    df['ma10']  = c.rolling(10).mean()
    df['ma20']  = c.rolling(20).mean()
    delta = c.diff()
    gain = delta.clip(lower=0).rolling(14).mean()
    loss = (-delta.clip(upper=0)).rolling(14).mean()
    df['rsi'] = 100 - 100 / (1 + gain / loss.replace(0, 1e-9))
    ema12 = c.ewm(span=12, adjust=False).mean()
    ema26 = c.ewm(span=26, adjust=False).mean()
    df['dif']  = ema12 - ema26
    df['dea']  = df['dif'].ewm(span=9, adjust=False).mean()
    df['hist'] = (df['dif'] - df['dea']) * 2
    df['vol_ratio'] = df['volume'] / df['volume'].rolling(5).mean()
    df['boll_mid'] = c.rolling(20).mean()
    df['boll_std'] = c.rolling(20).std()
    df['boll_pos'] = (c - df['boll_mid']) / (df['boll_std'] * 2 + 1e-9)
    return df


# ── 卖出评分（来自 sell_signal.py） ────────────────────────────────
def calc_sell_score(df, buy_price=None, buy_date=None):
    """卖出评分，0-100分，越高分越该卖"""
    if df is None or len(df) < 20:
        return 0, []
    latest = df.iloc[-1]
    prev   = df.iloc[-2]
    c = latest['close']
    h = latest['high']
    macd_h     = latest.get('hist', 0)
    macd_h_p   = prev.get('hist', 0)
    rsi        = latest.get('rsi', 50)
    rsi_p      = prev.get('rsi', 50)
    ma5  = latest.get('ma5',  c)
    ma10 = latest.get('ma10', c)
    ma20 = latest.get('ma20', c)
    vol_ratio = latest.get('vol_ratio', 1.0)
    vol_ma5   = df['volume'].tail(5).mean() if len(df) >= 5 else latest.get('volume', 0)

    score = 0
    reasons = []

    # 1. MACD死叉
    if macd_h < 0 and macd_h_p > 0:
        score += 25; reasons.append('MACD死叉')
    elif macd_h < 0:
        score += 15; reasons.append('MACD柱负')

    # 2. 均线破位
    if c < ma20: score += 20; reasons.append('破MA20')
    elif c < ma10: score += 10; reasons.append('破MA10')
    elif c < ma5:  score += 5;  reasons.append('破MA5')

    # 3. RSI超买/回落
    if rsi > 80:               score += 15; reasons.append('RSI>80')
    elif rsi > 70 and rsi < rsi_p: score += 12; reasons.append('RSI回落')

    # 4. 量价背离
    if vol_ratio > 1.5 and abs(c - prev.get('close', c)) / prev.get('close', c) < 0.02:
        score += 12; reasons.append('放量滞涨')
    vol_recent = df['volume'].tail(3).mean()
    vol_early  = df['volume'].iloc[-5:-3].mean() if len(df) >= 5 else vol_recent
    if c > df['close'].iloc[-5] and vol_recent < vol_early * 0.7:
        score += 15; reasons.append('价涨量缩')

    # 5. 从高点回落
    high10 = df['high'].tail(10).max()
    high20 = df['high'].tail(20).max()
    if c < high20 * 0.90: score += 15; reasons.append(f'20日高点回落>10%')
    elif c < high10 * 0.95: score += 8; reasons.append('10日高点回落>5%')

    # 6. 持有收益
    if buy_price and buy_price > 0:
        profit = (c - buy_price) / buy_price
        if profit < -0.10:      score += 25; reasons.append(f'止损({profit*100:.1f}%)')
        elif profit > 0.20:     score += 10; reasons.append(f'止盈({profit*100:.1f}%)')
        elif profit > 0.15:     score += 5;  reasons.append(f'稳健({profit*100:.1f}%)')

    return min(score, 100), reasons


# ── 数据获取 ────────────────────────────────────────────────────────
def fetch_kline_tencent(code, days=200):
    """使用腾讯API获取前复权日K线"""
    code = str(code).zfill(6)
    symbol = 'sh' + code if code.startswith('6') else 'sz' + code
    url = 'https://web.ifzq.gtimg.cn/appstock/app/fqkline/get'
    params = {
        '_var': 'kline_dayqfq',
        'param': f'{symbol},day,,,{days},qfq',
        'r': str(random.random())
    }
    try:
        r = requests.get(url, params=params, timeout=10)
        text = r.text
        if '=' not in text: return pd.DataFrame()
        json_str = text.split('=', 1)[1]
        data = json.loads(json_str)
        if data.get('code') != 0: return pd.DataFrame()
        kline = data.get('data', {}).get(symbol, {}).get('qfqday', [])
        if not kline: return pd.DataFrame()
        df = pd.DataFrame(kline, columns=['date','open','close','high','low','volume'])
        for col in ['open','close','high','low','volume']:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date').reset_index(drop=True)
        return df
    except:
        return pd.DataFrame()


def fetch_stock_batch(items):
    """并行获取多只股票K线"""
    code, name = items
    df = fetch_kline_tencent(code, 200)
    if not df.empty:
        df = add_indicators(df)
    return code, name, df


# ── 交易记录 ────────────────────────────────────────────────────────
@dataclass
class Position:
    code: str
    name: str
    buy_date: str
    buy_price: float
    qty: int
    buy_score: int

@dataclass
class Trade:
    code: str
    name: str
    buy_date: str
    buy_price: float
    sell_date: str
    sell_price: float
    buy_score: int
    sell_score: int
    ret_pct: float
    hold_days: int
    sell_reason: str


# ── 主回测 ─────────────────────────────────────────────────────────
def run_backtest(pool, start_date, end_date, buy_th, sell_th, max_pos, init_cash, max_hold):
    """执行回测"""

    # Step 1: 筛选回测区间交易日
    trade_dates = pd.bdate_range(start=start_date, end=end_date)
    trade_dates = [d for d in trade_dates if d.dayofweek < 5]  # 只工作日
    # 过滤节假日（简化处理）
    holidays = {pd.Timestamp('2026-03-04'), pd.Timestamp('2026-03-05'),
                pd.Timestamp('2026-03-09'), pd.Timestamp('2026-03-10'),
                pd.Timestamp('2026-03-16'), pd.Timestamp('2026-03-17'),
                pd.Timestamp('2026-03-20'), pd.Timestamp('2026-03-23'),
                pd.Timestamp('2026-03-30'), pd.Timestamp('2026-03-31')}
    trade_dates = [d for d in trade_dates if d not in holidays]
    print(f'  交易日: {len(trade_dates)} 天')
    print(f'  {trade_dates[0].date()} ~ {trade_dates[-1].date()}')

    # Step 2: 并行获取所有股票K线
    print(f'\n[Step 2] 并行获取 {len(pool)} 只股票K线...')
    kline_cache = {}
    lock = Lock()
    done = [0]

    with ThreadPoolExecutor(max_workers=30) as ex:
        futures = [ex.submit(fetch_stock_batch, (s['code'], s.get('name', s['code']))) for s in pool]
        for f in as_completed(futures):
            code, name, df = f.result()
            kline_cache[code] = df
            with lock:
                done[0] += 1
                if done[0] % 50 == 0:
                    print(f'  {done[0]}/{len(pool)}', flush=True)
    valid = sum(1 for df in kline_cache.values() if not df.empty)
    print(f'  有效数据: {valid}/{len(pool)} 只')

    # Step 3: 预计算每日评分矩阵
    print(f'\n[Step 3] 预计算评分矩阵...')
    score_rows = []
    for code, df in kline_cache.items():
        if df.empty: continue
        df_idx = df.set_index('date')
        for td in trade_dates:
            # 找到td日之前（含）最近的交易日
            avail = df_idx.index[df_idx.index <= td]
            if len(avail) < 30: continue
            di = len(avail) - 1
            df_day = df.iloc[:di+1].copy()
            s = calc_score_v2(df_day)
            if s and s.get('total', 0) > 0:
                score_rows.append({
                    'date': td,
                    'code': code,
                    'close': df_day['close'].iloc[-1],
                    'buy_score': s['total'],
                    'rsi': s.get('rsi', 50),
                    'boll_pos': s.get('boll_pos', 0),
                    'gain_5d': s.get('gain_5d', 0),
                    'macd_hist_pos': s.get('macd_hist_pos', 0),
                    'above_ma20': s.get('above_ma20', 0),
                    'ma_bullish': s.get('ma_bullish', 0),
                })
    scores_df = pd.DataFrame(score_rows)
    print(f'  评分矩阵: {len(scores_df)} 条')
    buy_cands = scores_df[scores_df['buy_score'] >= buy_th]
    print(f'  候选股(买分>={buy_th}): {len(buy_cands)} 条')
    if buy_cands.empty:
        print(f'  无候选股！TOP5买分:')
        top5 = scores_df.nlargest(5, 'buy_score')
        for _, r in top5.iterrows():
            print(f'    {r["code"]} 买分:{r["buy_score"]} 日期:{r["date"].date()}')

    # Step 4: 模拟交易
    print(f'\n[Step 4] 模拟交易...')
    positions = []   # list of Position
    cash = init_cash
    trades = []     # list of Trade
    portfolio_values = []
    day_stats = {}

    for td in trade_dates:
        day_scores = scores_df[scores_df['date'] == td].copy()
        day_scores = day_scores.sort_values('buy_score', ascending=False)

        # ── 卖出检查 ──
        sells_to_close = []
        for pos in positions:
            df = kline_cache.get(pos.code)
            if df.empty: continue
            avail = df[df['date'] <= td]
            if avail.empty: continue
            sell_score, reasons = calc_sell_score(avail, pos.buy_price, pos.buy_date)
            cur_price = avail['close'].iloc[-1]

            # 计算持有天数
            buy_dt = pd.to_datetime(pos.buy_date) if isinstance(pos.buy_date, str) else pos.buy_date
            hold_days = (td - buy_dt).days if buy_dt <= td else 0

            should_sell = False
            sell_reason = ''

            # 卖出条件: 评分≥阈值 或 止损 或 超持
            if sell_score >= sell_th:
                should_sell = True; sell_reason = f'卖出信号({sell_score}分)'
            elif hold_days > max_hold:
                should_sell = True; sell_reason = f'超持{max_hold}天'
            else:
                ret = (cur_price - pos.buy_price) / pos.buy_price
                if ret <= STOP_LOSS:
                    should_sell = True; sell_reason = f'止损({ret*100:.1f}%)'

            if should_sell:
                sells_to_close.append({
                    'pos': pos, 'sell_price': cur_price,
                    'sell_score': sell_score, 'sell_reason': sell_reason,
                    'hold_days': hold_days,
                })

        # 执行卖出
        for s in sells_to_close:
            pos = s['pos']
            ret_pct = (s['sell_price'] - pos.buy_price) / pos.buy_price * 100
            trades.append(Trade(
                code=pos.code, name=pos.name,
                buy_date=str(pos.buy_date)[:10],
                buy_price=pos.buy_price,
                sell_date=str(td.date()),
                sell_price=s['sell_price'],
                buy_score=pos.buy_score,
                sell_score=s['sell_score'],
                ret_pct=round(ret_pct, 2),
                hold_days=s['hold_days'],
                sell_reason=s['sell_reason'],
            ))
            cash += pos.qty * s['sell_price']
            positions.remove(pos)

        # ── 买入检查 ──
        if len(positions) < max_pos:
            slots = max_pos - len(positions)
            candidates = day_scores[~day_scores['code'].isin(p.code for p in positions)]
            for _, row in candidates.iterrows():
                if slots <= 0: break
                code = row['code']
                name = code  # 默认用code
                for s in pool:
                    if s['code'] == code:
                        name = s.get('name', code); break
                price = row['close']
                if price <= 0: continue
                qty = math.floor(POS_SIZE / price / 100) * 100
                if qty < 100: continue
                buy_cost = qty * price
                if buy_cost > cash: continue
                # 找对应持仓的K线算卖出评分（用于记录买分时的RSI等）
                positions.append(Position(
                    code=code, name=name,
                    buy_date=str(td.date()),
                    buy_price=price,
                    qty=qty,
                    buy_score=int(row['buy_score']),
                ))
                cash -= buy_cost
                slots -= 1

        # ── 当日账户价值 ──
        pos_value = sum(p.qty * kline_cache.get(p.code, pd.DataFrame()).iloc[-1]['close']
                        for p in positions
                        if not kline_cache.get(p.code, pd.DataFrame()).empty
                        and kline_cache.get(p.code)[kline_cache.get(p.code)['date'] <= td].shape[0] > 0)
        total_value = cash + pos_value
        portfolio_values.append({
            'date': str(td.date()),
            'cash': round(cash, 2),
            'pos_value': round(pos_value, 2),
            'total': round(total_value, 2),
            'ret_pct': round((total_value / init_cash - 1) * 100, 2),
            'n_pos': len(positions),
        })

    return trades, portfolio_values, positions


def print_report(trades, portfolio_values, positions, buy_th, sell_th, start_date, end_date, init_cash):
    print(f'\n{"="*70}')
    print(f'  回测报告  |  买入>={buy_th}分  卖出>={sell_th}分  |  {start_date} ~ {end_date}')
    print(f'{"="*70}')

    if not trades:
        print('  ⚠️  无任何成交记录')
        return

    df_t = pd.DataFrame([asdict(t) for t in trades])
    wins  = df_t[df_t['ret_pct'] > 0]
    loss  = df_t[df_t['ret_pct'] <= 0]

    # ── 收益总览 ──
    if portfolio_values:
        pv = pd.DataFrame(portfolio_values)
        final = pv.iloc[-1]
        peak  = pv['total'].max()
        dd    = pv['total'].min()
        print(f'\n  [收益总览]')
        print(f'  初始资金:  {init_cash:>10,.0f} 元')
        print(f'  最终价值:  {final["total"]:>10,.2f} 元')
        print(f'  总收益率:  {(final["total"]/init_cash-1)*100:>+10.2f}%')
        print(f'  峰值资金:  {peak:>10,.2f} 元')
        print(f'  最大回撤:  {(dd/peak-1)*100:>+10.2f}%')
        if len(pv) > 1:
            daily_rets = pv['total'].pct_change().dropna()
            sharpe = daily_rets.mean()/daily_rets.std()*math.sqrt(252) if daily_rets.std() > 0 else 0
            print(f'  夏普比率:  {sharpe:>+10.2f}')

    # ── 交易统计 ──
    print(f'\n  [交易统计]')
    print(f'  总交易:    {len(trades):>6} 笔')
    print(f'  盈利交易:  {len(wins):>6} 笔  (胜率 {len(wins)/len(trades)*100:.1f}%)')
    print(f'  亏损交易:  {len(loss):>6} 笔')
    if not df_t.empty:
        print(f'  均收益:    {df_t["ret_pct"].mean():>+8.2f}%')
        print(f'  均盈利:    {wins["ret_pct"].mean() if not wins.empty else 0:>+8.2f}%')
        print(f'  均亏损:    {loss["ret_pct"].mean() if not loss.empty else 0:>+8.2f}%')
        print(f'  最大单笔:  {df_t["ret_pct"].max():>+8.2f}%')
        print(f'  最大亏损:  {df_t["ret_pct"].min():>+8.2f}%')

    # ── 月度收益 ──
    print(f'\n  [月度收益]')
    df_t['month'] = df_t['sell_date'].str[:7]
    monthly = df_t.groupby('month').agg(
        count=('ret_pct','count'),
        total_ret=('ret_pct','sum'),
        avg_ret=('ret_pct','mean'),
        wins=('ret_pct', lambda x: (x>0).sum()),
    )
    monthly['wr'] = (monthly['wins']/monthly['count']*100).round(1)
    for mo, row in monthly.iterrows():
        s = '+' if row['total_ret'] >= 0 else ''
        bar = '▓' * int(abs(row['total_ret'])/2) if row['total_ret'] >= 0 else '░' * int(abs(row['total_ret'])/2)
        print(f'    {mo}: {s}{row["total_ret"]:>+6.2f}%  交易:{int(row["count"])}笔  胜率:{row["wr"]}%  {bar}')

    # ── 卖出原因 ──
    print(f'\n  [卖出原因分布]')
    vc = df_t['sell_reason'].value_counts()
    for reason, cnt in vc.items():
        print(f'    {reason}: {cnt}笔')

    # ── TOP10盈利 ──
    print(f'\n  [TOP10 盈利交易]')
    print(f'    {"代码":<8} | {"名称":<8} | {"买日期":<12} | {"买价":>8} | {"卖日期":<12} | {"卖价":>8} | {"收益":>7} | {"天":>3}')
    print(f'    {"-"*8} | {"-"*8} | {"-"*12} | {"-"*8} | {"-"*12} | {"-"*8} | {"-"*7} | {"-"*3}')
    for _, t in df_t.nlargest(10, 'ret_pct').iterrows():
        s = '+' if t['ret_pct'] >= 0 else ''
        print(f'    {t["code"]:<8} | {t["name"]:<8} | {t["buy_date"]:<12} | {t["buy_price"]:>8.2f} | {t["sell_date"]:<12} | {t["sell_price"]:>8.2f} | {s}{t["ret_pct"]:>5.1f}% | {t["hold_days"]:>3}d')

    # ── TOP5亏损 ──
    print(f'\n  [TOP5 亏损交易]')
    for _, t in df_t.nsmallest(5, 'ret_pct').iterrows():
        s = '+' if t['ret_pct'] >= 0 else ''
        print(f'    {t["code"]:<8} | {t["name"]:<8} | {t["buy_date"]:<12} | {t["buy_price"]:>8.2f} | {t["sell_date"]:<12} | {t["sell_price"]:>8.2f} | {s}{t["ret_pct"]:>5.1f}% | {t["hold_days"]:>3}d  {t["sell_reason"]}')

    # ── 持仓 ──
    if positions:
        print(f'\n  [未平仓持仓 {len(positions)} 笔]')
        for p in positions:
            print(f'    {p.code} {p.name}  买于{p.buy_date} @ {p.buy_price}  买分:{p.buy_score}')

    print(f'\n{"="*70}')
    print(f'  ⚠️  回测结果仅供参考，不代表未来真实收益，不构成投资建议。')
    print(f'{"="*70}')


def main():
    p = argparse.ArgumentParser(description='A股趋势扫描回测 v3')
    p.add_argument('--start', default='2026-03-01')
    p.add_argument('--end',   default='2026-03-31')
    p.add_argument('--buy-th',  type=int, default=80)
    p.add_argument('--sell-th', type=int, default=70)
    p.add_argument('--max-pos', type=int, default=10)
    p.add_argument('--cash',    type=float, default=40000)
    args = p.parse_args()

    print(f'{"="*70}')
    print(f'  A股趋势扫描回测  |  基于 stock_pool_merged + score_v2')
    print(f'{"="*70}')
    print(f'  回测期:   {args.start} ~ {args.end}')
    print(f'  买入阈值: >={args.buy_th}分')
    print(f'  卖出阈值: >={args.sell_th}分')
    print(f'  最大持仓: {args.max_pos} 仓')
    print(f'  初始资金: {args.cash:,.0f} 元')

    # 获取股票池
    print(f'\n[Step 1] 获取股票池...')
    pool = get_pool()
    print(f'  股票池: {len(pool)} 只')

    # 运行回测
    trades, portfolio_values, positions = run_backtest(
        pool=pool,
        start_date=args.start,
        end_date=args.end,
        buy_th=args.buy_th,
        sell_th=args.sell_th,
        max_pos=args.max_pos,
        init_cash=args.cash,
        max_hold=30,
    )

    # 输出报告
    print_report(trades, portfolio_values, positions,
                 args.buy_th, args.sell_th, args.start, args.end, args.cash)


if __name__ == '__main__':
    main()
