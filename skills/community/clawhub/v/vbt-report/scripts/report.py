#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
VectorBT Backtest HTML Report Generator (vbt-report)
数据层 v2: XDXR精确复权 | 4层网络fallback | 腾讯API | 北交所支持

Usage:
    python report.py 688387
    python report.py 688387 --output ./688387_report.html
    python report.py 600519 --data-dir "D:\\new_tdx64"
"""
import sys, os, json, warnings, io, argparse, datetime

# 仅在独立运行时设置 stdout（被 import 时不干扰子进程的 stdout）
if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
warnings.filterwarnings('ignore')

import pandas as pd
import numpy as np
import vectorbt as vbt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from mootdx.reader import Reader


# ==============================================================================
# Data Loading (v2: XDXR复权 + 4层fallback)
# ==============================================================================

def detect_exchange(symbol):
    """自动判断交易所后缀"""
    if symbol.startswith('6') or symbol.startswith('5'):
        return 'SH', 'sh'
    elif symbol.startswith('0') or symbol.startswith('3'):
        return 'SZ', 'sz'
    elif symbol.startswith('4') or symbol.startswith('8') or symbol.startswith('92'):
        return 'BJ', 'bj'
    else:
        return 'SZ', 'sz'


def fetch_bj_local_daily(symbol, tdxdir):
    """读取北交所本地日线二进制文件"""
    import struct
    filepath = os.path.join(tdxdir, 'vipdoc', 'bj', 'lday', f'bj{symbol}.day')
    if not os.path.exists(filepath):
        return None
    records = []
    with open(filepath, 'rb') as f:
        while True:
            chunk = f.read(32)
            if len(chunk) < 32:
                break
            date, open_p, high_p, low_p, close_p, amount, vol, _ = \
                struct.unpack('=iffffif8x', chunk)
            year = date // 10000
            month = (date % 10000) // 100
            day = date % 100
            try:
                dt = pd.Timestamp(year=year, month=month, day=day)
            except Exception:
                continue
            records.append({
                'date': dt, 'open': open_p, 'high': high_p,
                'low': low_p, 'close': close_p, 'volume': vol
            })
    if not records:
        return None
    df = pd.DataFrame(records).set_index('date').sort_index()
    return df


def apply_forward_adjustment(df, xdxr_raw):
    """基于XDXR的前复权处理"""
    if xdxr_raw is None or len(xdxr_raw) == 0:
        return df

    fq_events = []
    for d in xdxr_raw:
        if d.get('category') == 1:
            dt = datetime.datetime(d['year'], d['month'], d['day'])
            cash = (d.get('fenhong') or 0) / 10.0
            stock = (d.get('songzhuangu') or 0) / 10.0
            ration = (d.get('peigu') or 0) / 10.0
            ration_price = (d.get('peigujia') or 0) / 10.0
            fq_events.append({
                'date': dt, 'cash': cash, 'stock': stock,
                'ration': ration, 'ration_price': ration_price
            })

    if not fq_events:
        return df

    fq_events.sort(key=lambda x: x['date'])
    df = df.copy()
    df['adj_factor'] = 1.0
    for ev in reversed(fq_events):
        dt = ev['date']
        mask_before = df.index < dt
        if mask_before.sum() < 1:
            continue
        close_before = float(df.loc[mask_before, 'close'].iloc[-1])
        denom = 1.0
        if ev['stock'] > 0:
            denom += ev['stock']
        if ev['ration'] > 0:
            denom += ev['ration']
        ex_right_price = (close_before - ev['cash'] + ev['ration'] * ev['ration_price']) / denom
        if close_before > 0:
            ev_factor = ex_right_price / close_before
            df.loc[mask_before, 'adj_factor'] *= ev_factor

    for col in ['open', 'high', 'low', 'close']:
        df[col] = df[col] * df['adj_factor']
    df = df.drop(columns=['adj_factor'])
    print(f"  [INFO] 前复权完成: {len(fq_events)}个除权事件, {len(df)}条记录")
    return df


def fetch_local_data(symbol, tdxdir):
    """本地通达信日线读取"""
    if not os.path.exists(tdxdir):
        print(f"  [WARN] 本地TDX目录不存在: {tdxdir}")
        return None

    try:
        from mootdx.reader import StdReader
        reader = StdReader(tdxdir=tdxdir)

        if symbol.startswith('4') or symbol.startswith('8') or symbol.startswith('92'):
            df = fetch_bj_local_daily(symbol, tdxdir)
            src = "BJ本地文件"
        else:
            df = reader.daily(symbol=symbol)
            src = "mootdx本地(通达信)"

        if df is not None and len(df) > 0:
            df.columns = [c.lower() for c in df.columns]
            print(f"  [OK] {src}读取成功: {len(df)}条")
            if hasattr(df.index, 'strftime'):
                print(f"  本地范围: {df.index[0].strftime('%Y-%m-%d')} ~ {df.index[-1].strftime('%Y-%m-%d')}")
            return df
    except ImportError:
        print(f"  [WARN] mootdx 未安装")
    except Exception as e:
        print(f"  [WARN] mootdx读取失败: {e}")

    return None


def fetch_xdxr_info(symbol):
    """通达信服务器获取除权除息信息"""
    try:
        from tdxpy.hq import TdxHq_API
        candidates = [1, 0]
        for mkt in candidates:
            try:
                api = TdxHq_API()
                api.connect(ip='110.41.147.114', port=7709, time_out=5)
                xdxr_raw = api.get_xdxr_info(mkt, symbol)
                api.disconnect()
                if xdxr_raw and len(xdxr_raw) > 0:
                    return xdxr_raw
            except Exception:
                try:
                    api.disconnect()
                except Exception:
                    pass
                continue
    except ImportError:
        print(f"  [WARN] tdxpy 未安装，跳过前复权")
    except Exception as e:
        print(f"  [WARN] 获取除权除息信息失败: {e}")
    return None


def fetch_tdx_server_daily(symbol):
    """通达信服务器直连日K线"""
    try:
        from tdxpy.hq import TdxHq_API

        if symbol.startswith('68'):
            candidates = [1]
        elif symbol.startswith('6') or symbol.startswith('5'):
            candidates = [0, 1]
        else:
            candidates = [1]

        for market_id in candidates:
            try:
                api = TdxHq_API()
                api.connect(ip='110.41.147.114', port=7709, time_out=5)
                data = api.get_security_bars(9, market_id, symbol, 0, 800)
                api.disconnect()
                if data and len(data) > 0:
                    rows = []
                    for item in data:
                        if isinstance(item, dict):
                            dt = str(item.get('datetime', item.get('date', '')))[:10]
                            rows.append({
                                'date': dt,
                                'open': float(item.get('open', 0)),
                                'close': float(item.get('close', 0)),
                                'high': float(item.get('high', 0)),
                                'low': float(item.get('low', 0)),
                                'volume': float(item.get('vol', 0))
                            })
                    if rows:
                        df = pd.DataFrame(rows)
                        df['date'] = pd.to_datetime(df['date'], errors='coerce')
                        df = df.dropna().set_index('date')
                        if len(df) > 0:
                            return df
            except Exception:
                try:
                    api.disconnect()
                except Exception:
                    pass
                continue
        return None
    except ImportError:
        return None
    except Exception:
        return None


def fetch_tencent_daily(symbol):
    """腾讯财经API日K线（无需token，A股最稳定源）"""
    try:
        import requests
        _, mkt = detect_exchange(symbol)
        url = "https://web.ifzq.gtimg.cn/appstock/app/fqkline/get"
        params = {'param': f"{mkt}{symbol},day,,,800,qfq"}
        resp = requests.get(url, params=params,
                          headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        jdata = resp.json()
        tencent_code = f"{mkt}{symbol}"
        kline_data = jdata['data'][tencent_code]['qfqday']
        if not kline_data or len(kline_data) < 2:
            return None
        rows = [{'date': r[0], 'open': float(r[1]), 'close': float(r[2]),
                 'high': float(r[3]), 'low': float(r[4]), 'volume': float(r[5])}
                for r in kline_data]
        df = pd.DataFrame(rows)
        df['date'] = pd.to_datetime(df['date'])
        df = df.dropna().set_index('date')
        return df
    except Exception:
        return None


def fetch_akshare_daily(symbol, start, end):
    """AKShare兜底获取历史日线"""
    try:
        import akshare as ak
        df = ak.stock_zh_a_hist(
            symbol=symbol, period="daily",
            start_date=start.replace('-', ''),
            end_date=end.replace('-', ''),
            adjust="qfq"
        )
        if df is None or df.empty:
            return None
        col_map = {}
        for c in df.columns:
            cl = c.strip()
            if cl in ('日期',):
                col_map[c] = 'date'
            elif cl in ('开盘',):
                col_map[c] = 'open'
            elif cl in ('最高',):
                col_map[c] = 'high'
            elif cl in ('最低',):
                col_map[c] = 'low'
            elif cl in ('收盘',):
                col_map[c] = 'close'
            elif cl in ('成交量',):
                col_map[c] = 'volume'
        df = df.rename(columns=col_map)
        required = {'date', 'open', 'high', 'low', 'close'}
        if not required.issubset(set(df.columns)):
            return None
        df['date'] = pd.to_datetime(df['date'])
        for col in ['open', 'high', 'low', 'close', 'volume']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        df = df.set_index('date').sort_index().dropna(subset=['close'])
        return df
    except Exception:
        return None


def fuse_data(local_df, network_df):
    """融合本地和网络数据，本地优先"""
    combined = local_df.copy()
    common_dates = combined.index.intersection(network_df.index)
    for dt in common_dates:
        combined.loc[dt] = network_df.loc[dt]
    new_dates = network_df.index.difference(combined.index)
    if len(new_dates) > 0:
        combined = pd.concat([combined, network_df.loc[new_dates]])
    combined = combined.sort_index()
    return combined


def get_data(symbol, tdxdir, start='20200101', end='20260531'):
    """统一数据入口：本地TDX → XDXR复权 → 网络补全"""
    print(f"  [INFO] 获取数据: {symbol}")

    # Phase 1: 本地数据
    local_df = fetch_local_data(symbol, tdxdir)

    # Phase 1.5: XDXR前复权
    if local_df is not None and len(local_df) > 100:
        try:
            xdxr_raw = fetch_xdxr_info(symbol)
            if xdxr_raw:
                local_df = apply_forward_adjustment(local_df, xdxr_raw)
        except Exception as e:
            print(f"  [WARN] 前复权处理异常: {e}")

    # 判断是否需要网络补全
    need_fill = False
    if local_df is None or len(local_df) < 50:
        need_fill = True
    elif hasattr(local_df.index, 'strftime'):
        local_end = local_df.index[-1]
        days_gap = (pd.Timestamp.now() - local_end).days
        if days_gap > 4:
            need_fill = True
            print(f"  [网络补全] 本地数据截止 {local_end.strftime('%Y-%m-%d')}, 尝试网络数据源...")

    # Phase 2: 网络补丁
    network_df = None
    if need_fill:
        network_sources = [
            ('TDX直连', fetch_tdx_server_daily(symbol)),
            ('腾讯财经', fetch_tencent_daily(symbol)),
            ('AKShare', fetch_akshare_daily(symbol, start, end)),
        ]
        for src_name, src_df in network_sources:
            if src_df is not None and len(src_df) > 0:
                network_df = src_df
                print(f"  [OK] 网络数据源({src_name})获取成功，{len(network_df)}条记录")
                break

    # Phase 3: 融合
    if local_df is not None and len(local_df) > 0:
        if network_df is not None and len(network_df) > 0:
            df = fuse_data(local_df, network_df)
            print(f"  [OK] 数据融合完成，{len(df)}条记录")
        else:
            df = local_df
            print(f"  [OK] 仅使用本地数据，{len(df)}条记录")
    elif network_df is not None and len(network_df) > 0:
        df = network_df
        print(f"  [OK] 仅使用网络数据，{len(df)}条记录")
    else:
        raise RuntimeError(f"无法获取 {symbol} 的数据，请检查代码和日期范围")

    # 重命名为大写列名（BacktestEngine/HTML要求）
    df = df.rename(columns={
        'open': 'Open', 'high': 'High', 'low': 'Low',
        'close': 'Close', 'volume': 'Volume', 'amount': 'Amount'
    })
    if 'Amount' not in df.columns:
        df['Amount'] = df['Volume'] * (df['Open'] + df['Close']) / 2

    print(f"数据: {df.index[0].date()} ~ {df.index[-1].date()}, {len(df)}个交易日")
    return df


def guess_stock_name(ticker):
    """通过AKShare获取股票中文简称"""
    try:
        import akshare as ak
        info = ak.stock_individual_info_em(symbol=ticker)
        row = info[info['item'] == '股票简称']
        if not row.empty:
            return str(row['value'].iloc[0])
    except Exception:
        pass
    return ''


# ==============================================================================
# KDJ Calculation
# ==============================================================================
def calc_kdj(hi, lo, cl, n=9, m1=3, m2=3):
    lo_n = lo.rolling(n).min(); hi_n = hi.rolling(n).max()
    rsv = (cl - lo_n) / (hi_n - lo_n) * 100
    k = rsv.ewm(alpha=1/m1, adjust=False).mean()
    d = k.ewm(alpha=1/m2, adjust=False).mean()
    j = 3*k - 2*d
    return k, d, j


# ==============================================================================
# Backtest Engine
# ==============================================================================
class BacktestEngine:
    def __init__(self, price, high, low, init_cash=1_000_000):
        self.price = price; self.high = high; self.low = low
        self.IC = init_cash; self.results = []; self.all_pfs = {}
        vbt.settings.array_wrapper.freq = '1D'

    def _record(self, name, pf, cat):
        t = pf.trades; avg_ret = 0.0
        if t.count() > 0:
            try: avg_ret = float(t.returns.mean() if hasattr(t.returns,'mean') else np.mean(t.returns))
            except: pass
        self.results.append({
            'name': name, 'cat': cat,
            'ret': float(pf.total_return()),
            'wr': float(t.win_rate()) if t.count()>0 else 0,
            'sharpe': float(pf.sharpe_ratio()) if pf.sharpe_ratio() is not None and not np.isnan(float(pf.sharpe_ratio())) else 0,
            'mdd': float(pf.max_drawdown()),
            'nt': int(t.count()),
            'pf_val': float(t.profit_factor()) if t.count()>0 else 0,
            'avg_ret': avg_ret
        })
        self.all_pfs[name] = (pf, cat)

    def run_ma_cross(self, fast=[5,10,15,20], slow=[30,50,60,100]):
        for f in fast:
            for s in slow:
                if f >= s: continue
                en = vbt.MA.run(self.price, f).ma_crossed_above(vbt.MA.run(self.price, s))
                ex = vbt.MA.run(self.price, f).ma_crossed_below(vbt.MA.run(self.price, s))
                self._record(f"MA({f},{s})", vbt.Portfolio.from_signals(self.price, en, ex, init_cash=self.IC, freq='1D'), "趋势跟踪")

    def run_rsi(self, periods=[7,14,21], osold=30, obought=70):
        for p in periods:
            r = vbt.RSI.run(self.price, p)
            self._record(f"RSI({p})", vbt.Portfolio.from_signals(self.price, r.rsi_crossed_below(osold), r.rsi_crossed_above(obought), init_cash=self.IC, freq='1D'), "反转策略")

    def run_macd(self):
        m = vbt.MACD.run(self.price)
        self._record("MACD金叉死叉", vbt.Portfolio.from_signals(self.price, m.macd_crossed_above(m.signal), m.macd_crossed_below(m.signal), init_cash=self.IC, freq='1D'), "趋势跟踪")

    def run_bollinger(self, period=20, std=2):
        b = vbt.BBANDS.run(self.price, period, std)
        bl = self.price < b.lower; am = self.price > b.middle
        en = bl & ~bl.shift(1).fillna(False); ex = am & ~am.shift(1).fillna(False)
        self._record("布林带突破", vbt.Portfolio.from_signals(self.price, en, ex, init_cash=self.IC, freq='1D'), "反转策略")

    def run_kdj(self):
        k, d, _ = calc_kdj(self.high, self.low, self.price)
        en = (k < 20) & (k > d); ex = k > 80
        self._record("KDJ超买超卖", vbt.Portfolio.from_signals(self.price, en, ex, init_cash=self.IC, freq='1D'), "反转策略")

    def run_momentum(self, periods=[20,40,60], th=0.05):
        for mp in periods:
            momo = self.price.pct_change(mp)
            self._record(f"动量({mp}日)", vbt.Portfolio.from_signals(self.price, (momo>th)&(momo.shift(1)<=th), (momo<-th)&(momo.shift(1)>=-th), init_cash=self.IC, freq='1D'), "趋势跟踪")

    def run_combo(self):
        s = vbt.MA.run(self.price, 10); l = vbt.MA.run(self.price, 50)
        r = vbt.RSI.run(self.price, 14)
        en = s.ma_crossed_above(l) & r.rsi_crossed_below(30)
        self._record("MA金叉+RSI超卖", vbt.Portfolio.from_signals(self.price, en, s.ma_crossed_below(l), init_cash=self.IC, freq='1D'), "组合策略")

    def run_buy_hold(self):
        en = pd.Series(True, index=self.price.index); en.iloc[0] = True
        ex = pd.Series(False, index=self.price.index)
        self._record("买入持有(基准)", vbt.Portfolio.from_signals(self.price, en, ex, init_cash=self.IC, freq='1D'), "基准策略")

    def run_ma_atr_stop(self, ma_period=20, atr_period=14, atr_mult=2.0):
        ma = vbt.MA.run(self.price, ma_period)
        en = ma.ma_crossed_above(self.price) | (self.price > ma.ma)
        atr = vbt.ATR.run(self.high, self.low, self.price, atr_period).atr
        stop_level = ma.ma - atr * atr_mult
        ex = self.price < stop_level
        first_ma_cross = ma.ma_crossed_above(self.price)
        en = first_ma_cross | (self.price > ma.ma)
        self._record(f"MA({ma_period})+ATR止损", vbt.Portfolio.from_signals(self.price, en, ex, init_cash=self.IC, freq='1D'), "趋势跟踪")

    def run_all(self):
        self.run_ma_cross(); self.run_rsi(); self.run_macd()
        self.run_bollinger(); self.run_kdj(); self.run_momentum(); self.run_combo()
        self.run_buy_hold(); self.run_ma_atr_stop()
        self.results.sort(key=lambda x: x['ret'], reverse=True)
        return self.results


# ==============================================================================
# Chart Generation
# ==============================================================================
def make_portfolio_chart(pf, name, price, IC):
    try:
        eq = pf.value()
    except:
        try: eq = pf.cumulative_returns(); eq = eq * IC
        except:
            try: eq = pf.portfolio_value()
            except: return '<div>Chart error</div>'

    dates = eq.index if hasattr(eq,'index') else price.index
    vals = [float(x) for x in eq]
    cm = pd.Series(vals).cummax()
    dd = (pd.Series(vals) - cm) / cm * 100

    fig = make_subplots(rows=3, cols=1, shared_xaxes=True, row_heights=[0.5,0.3,0.2], vertical_spacing=0.05,
                        subplot_titles=(f'{name} - 净值 Curve', '最新价', '回撤'))
    fig.add_trace(go.Scatter(x=dates, y=vals, mode='lines', name='净值', line=dict(color='#3fb950', width=1.5)), row=1, col=1)
    fig.add_hline(y=IC, line_dash="dash", line_color="#8b949e", row=1, col=1)
    fig.add_trace(go.Scatter(x=price.index, y=price, mode='lines', name='最新价', line=dict(color='#58a6ff', width=1.5)), row=2, col=1)
    fig.add_trace(go.Scatter(x=dates, y=dd, mode='lines', fill='tozeroy', name='回撤', line=dict(color='#f85149', width=1), fillcolor='rgba(248,81,73,0.15)'), row=3, col=1)
    fig.add_hline(y=-20, line_dash="dash", line_color="#d29922", row=3, col=1)
    fig.update_layout(template='plotly_dark', height=600, margin=dict(l=40,r=40,t=40,b=40), paper_bgcolor='#161b22', plot_bgcolor='#161b22', font=dict(color='#c9d1d9',size=11), showlegend=False, hovermode='x unified')
    fig.update_xaxes(gridcolor='#30363d'); fig.update_yaxes(gridcolor='#30363d')
    return fig.to_html(include_plotlyjs='cdn', full_html=False)


def make_top5_chart(results, all_pfs, price):
    top5 = results[:min(5, len(results))]
    fig = go.Figure(); colors = ['#3fb950','#58a6ff','#bc8cff','#d29922','#f0883e']
    for i, r in enumerate(top5):
        pf_i, _ = all_pfs[r['name']]
        try: eq_i = pf_i.value()
        except:
            try: eq_i = pf_i.cumulative_returns() * 1_000_000
            except:
                try: eq_i = pf_i.portfolio_value()
                except: continue
        fig.add_trace(go.Scatter(x=eq_i.index, y=[float(x) for x in eq_i], mode='lines', name=f"#{i+1} {r['name']} ({r['ret']*100:+.2f}%)", line=dict(color=colors[i], width=1.5)))
    fig.update_layout(template='plotly_dark', height=450, margin=dict(l=40,r=40,t=30,b=40), paper_bgcolor='#161b22', plot_bgcolor='#161b22', font=dict(color='#c9d1d9',size=11), hovermode='x unified', title=dict(text='TOP5 策略净值对比', font=dict(color='#f0f6fc',size=15)))
    fig.update_xaxes(gridcolor='#30363d'); fig.update_yaxes(gridcolor='#30363d')
    return fig.to_html(include_plotlyjs=False, full_html=False)


# ==============================================================================
# HTML Report Generator
# ==============================================================================
def generate_report(ticker, stock_name, df, results, all_pfs, out_path):
    price = df['Close'].astype(float)
    high = df['High'].astype(float)
    low = df['Low'].astype(float)

    cp = float(price.iloc[-1])
    ma5 = float(price.rolling(5).mean().iloc[-1])
    ma10 = float(price.rolling(10).mean().iloc[-1])
    ma20 = float(price.rolling(20).mean().iloc[-1])
    ma60 = float(price.rolling(60).mean().iloc[-1])
    chg = (cp - float(price.iloc[-2])) / float(price.iloc[-2]) * 100

    rsi_val = float(vbt.RSI.run(price, 14).rsi.iloc[-1])
    m = vbt.MACD.run(price)
    md, ms, mh = float(m.macd.iloc[-1]), float(m.signal.iloc[-1]), float(m.hist.iloc[-1])
    m_stat = "看多" if md > ms else "看空"
    bb = vbt.BBANDS.run(price, 20, 2)
    bb_pos = (cp - float(bb.lower.iloc[-1])) / (float(bb.upper.iloc[-1]) - float(bb.lower.iloc[-1]))
    k, d, j = [float(x.iloc[-1]) for x in calc_kdj(high, low, price)]

    price_min = float(price.min()); price_max = float(price.max())
    p_min_d = price.idxmin().strftime('%Y-%m-%d'); p_max_d = price.idxmax().strftime('%Y-%m-%d')
    price_drop = (price_min - price_max) / price_max * 100

    now = pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')
    label = f"{ticker} {stock_name}" if stock_name else ticker
    updown = f"+{chg:.2f}%" if chg >= 0 else f"{chg:.2f}%"
    ucol = "up" if chg >= 0 else "down"
    dr = f"{df.index[0].strftime('%Y-%m-%d')} ~ {df.index[-1].strftime('%Y-%m-%d')}"

    best = results[0]
    avg_ret = np.mean([r['ret'] for r in results])
    overall = "green" if avg_ret > 0.1 else "yellow" if avg_ret > -0.1 else "red"
    overall_t = "看多" if avg_ret>0.1 else "中性区间" if avg_ret>-0.1 else "看空"

    tbl = ""
    for i, x in enumerate(results):
        rk = i+1; star = "⭐ " if rk == 1 else ""
        be = "class='best'" if rk == 1 else ""
        bg = {"趋势跟踪":"badge-trend","反转策略":"badge-reverse","组合策略":"badge-combo","基准策略":"badge-benchmark"}.get(x['cat'],"badge-trend")
        def c(v, t=0): return "green" if v>=t else "red"
        def c2(v): return "green" if v>=0.5 else "red"
        def c3(v): return "red" if v<=-0.15 else "yellow" if v<=-0.05 else "green"
        def c4(v): return "green" if v>=1.5 else "yellow" if v>=1 else "red"
        cc = "color:var(--green);font-weight:700" if rk==1 else "color:var(--text-dim)"
        tbl += f"""    <tr{be}>
      <td style="{cc}">{rk}</td>
      <td><strong>{star}{x['name']}</strong></td>
      <td><span class="badge {bg}">{x['cat']}</span></td>
      <td class="{c(x['ret'])}">{x['ret']*100:+.2f}%</td>
      <td class="{c2(x['wr'])}">{x['wr']*100:.1f}%</td>
      <td class="{c(x['sharpe'])}">{x['sharpe']:+.2f}</td>
      <td class="{c3(x['mdd'])}">{x['mdd']*100:.1f}%</td>
      <td>{x['nt']}</td>
      <td class="{c4(x['pf_val'])}">{x['pf_val']:.2f}</td>
      <td class="{c(x['avg_ret'])}">{x['avg_ret']*100:+.2f}%</td>
    </tr>
"""

    best_pf, _ = all_pfs[best['name']]
    best_chart = make_portfolio_chart(best_pf, best['name'], price, 1_000_000)
    top5_chart = make_top5_chart(results, all_pfs, price)

    rsi_s = "超卖区(偏低)" if rsi_val<30 else "超买区(偏高)" if rsi_val>70 else "中性区间"
    bb_s = "上轨附近(压力位)" if bb_pos>0.8 else "下轨附近(支撑位)" if bb_pos<0.2 else "中性区间"
    k_s = "超卖区(偏低)(K<20)" if k<20 else "超买区(偏高)(K>80)" if k>80 else "中性区间"
    hist_s = "看多" if mh>0 else "看空"

    r = results
    ov = overall
    ov_c = {'green':'63,185,80','yellow':'210,153,34','red':'248,81,73'}

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{label} - VectorBT 向量化回测分析报告</title>
<style>
  :root {{ --bg:#0d1117;--card:#161b22;--border:#30363d;--text:#c9d1d9;--text-dim:#8b949e;--text-bright:#f0f6fc;
    --green:#3fb950;--red:#f85149;--yellow:#d29922;--blue:#58a6ff;--purple:#bc8cff; }}
  * {{ margin:0;padding:0;box-sizing:border-box; }}
  body {{ background:var(--bg);color:var(--text);font-family:-apple-system,'Segoe UI',sans-serif;padding:20px;max-width:1200px;margin:0 auto; }}
  .header {{ text-align:center;padding:30px 0;border-bottom:1px solid var(--border);margin-bottom:30px; }}
  .header h1 {{ font-size:28px;color:var(--text-bright); }}
  .header .price {{ font-size:48px;font-weight:700;margin:16px 0; }}
  .card {{ background:var(--card);border:1px solid var(--border);border-radius:12px;padding:24px;margin-bottom:20px; }}
  .card h2 {{ font-size:16px;color:var(--text-bright);margin-bottom:16px;padding-bottom:10px;border-bottom:1px solid var(--border); }}
  table {{ width:100%;border-collapse:collapse;font-size:13px; }}
  th,td {{ padding:8px 10px;border-bottom:1px solid rgba(48,54,61,0.5);text-align:left; }}
  th {{ color:var(--text-dim);font-weight:500;font-size:12px; }}
  tr:hover {{ background:rgba(255,255,255,0.02); }}
  .up,.green {{ color:var(--green); }} .down,.red {{ color:var(--red); }} .yellow {{ color:var(--yellow); }}
  .best {{ background:rgba(63,185,80,0.08)!important; }}
  .badge {{ display:inline-block;padding:2px 8px;border-radius:4px;font-size:11px;font-weight:600; }}
  .badge-trend {{ background:rgba(88,166,255,0.12);color:var(--blue); }}
  .badge-reverse {{ background:rgba(188,140,255,0.12);color:var(--purple); }}
  .badge-combo {{ background:rgba(210,153,34,0.12);color:var(--yellow); }}
  .badge-benchmark {{ background:rgba(139,148,158,0.12);color:var(--text-dim); }}
  .grid {{ display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:12px;margin:16px 0; }}
  .grid-item {{ background:rgba(255,255,255,0.03);border-radius:8px;padding:14px;text-align:center; }}
  .grid-item .gl {{ font-size:11px;color:var(--text-dim);margin-bottom:4px; }}
  .grid-item .gv {{ font-size:22px;font-weight:700; }}
  .footer {{ text-align:center;padding:30px 0;color:var(--text-dim);font-size:12px;border-top:1px solid var(--border);margin-top:30px; }}
  .stat-row {{ display:flex;gap:24px;flex-wrap:wrap;background:rgba(255,255,255,0.02);border-radius:8px;padding:14px 18px;margin-bottom:16px; }}
  .chart-container {{ border-radius:8px;overflow:hidden;margin:16px 0; }}
  .status-bar {{ display:flex;justify-content:space-between;align-items:center;padding:14px 18px;margin:0 0 20px;border-radius:10px;background:rgba({ov_c[ov]},0.06);border:1px solid rgba({ov_c[ov]},0.15); }}
  .status-label {{ font-size:20px;font-weight:600; }}
</style>
</head>
<body>

<div class="header">
  <h1>{label} - VectorBT 向量化回测分析报告</h1>
  <div class="price" style="color:var(--{ucol})">{cp:.2f}</div>
  <div style="color:var(--{ucol});font-size:18px;margin-top:4px">{updown}</div>
  <div class="meta" style="margin-top:14px">
    <span>{now}</span><span>VectorBT v2.2.0 | TDX</span><span>{dr} ({len(df)})</span>
  </div>
</div>

<div class="status-bar">
  <span>综合判定 ({len(results)} 个策略)</span>
  <span class="status-label" style="color:var(--{ov})">{overall_t}</span>
  <span style="color:var(--text-dim);font-size:13px">均值={avg_ret*100:+.2f}% | 最佳={best['name']}</span>
</div>

<div class="card">
  <h2>当前行情</h2>
  <div class="grid">
    <div class="grid-item"><div class="gl">最新价</div><div class="gv" style="color:var(--{ucol})">{cp:.2f}</div></div>
    <div class="grid-item"><div class="gl">涨跌幅</div><div class="gv" style="color:var(--{ucol})">{updown}</div></div>
    <div class="grid-item"><div class="gl">MA5</div><div class="gv" style="color:{'var(--green)' if cp>=ma5 else 'var(--red)'}">{ma5:.2f}</div></div>
    <div class="grid-item"><div class="gl">MA10</div><div class="gv" style="color:{'var(--green)' if cp>=ma10 else 'var(--red)'}">{ma10:.2f}</div></div>
    <div class="grid-item"><div class="gl">MA20</div><div class="gv" style="color:{'var(--green)' if cp>=ma20 else 'var(--red)'}">{ma20:.2f}</div></div>
    <div class="grid-item"><div class="gl">MA60</div><div class="gv" style="color:{'var(--green)' if cp>=ma60 else 'var(--red)'}">{ma60:.2f}</div></div>
    <div class="grid-item"><div class="gl">RSI(14)</div><div class="gv" style="color:var(--{'green' if rsi_val<30 else 'red' if rsi_val>70 else 'yellow'})">{rsi_val:.1f}</div></div>
    <div class="grid-item"><div class="gl">MACD {m_stat}</div><div class="gv" style="font-size:16px;color:{'var(--green)' if md>0 else 'var(--red)'}">{md:.3f}</div></div>
    <div class="grid-item"><div class="gl">布林位置</div><div class="gv">{bb_pos:.2f}</div></div>
    <div class="grid-item"><div class="gl">KDJ(K/D/J)</div><div class="gv" style="font-size:16px">{k:.0f}/{d:.0f}/{j:.0f}</div></div>
  </div>
</div>

<div class="card">
  <h2>最佳策略净值曲线 — {best['name']}</h2>
  <div class="stat-row">
    <div><div class="gl">总收益</div><div class="gv" style="font-size:20px;color:var(--{'green' if best['ret']>=0 else 'red'})">{best['ret']*100:+.2f}%</div></div>
    <div><div class="gl">胜率</div><div class="gv" style="font-size:20px;color:var(--{'green' if best['wr']>=0.5 else 'red'})">{best['wr']*100:.1f}%</div></div>
    <div><div class="gl">夏普比率</div><div class="gv" style="font-size:20px;color:var(--{'green' if best['sharpe']>=0.5 else 'yellow'})">{best['sharpe']:+.2f}</div></div>
    <div><div class="gl">最大回撤</div><div class="gv" style="font-size:20px;color:var(--{'red' if best['mdd']<=-0.15 else 'yellow' if best['mdd']<=-0.05 else 'green'})">{best['mdd']*100:.1f}%</div></div>
    <div><div class="gl">交易次数</div><div class="gv" style="font-size:20px">{best['nt']}</div></div>
    <div><div class="gl">盈亏比</div><div class="gv" style="font-size:20px;color:var(--{'green' if best['pf_val']>=1.5 else 'yellow' if best['pf_val']>=1 else 'red'})">{best['pf_val']:.2f}</div></div>
  </div>
  <div class="chart-container">{best_chart}</div>
</div>

<div class="card">
  <h2>TOP5 策略净值对比</h2>
  <div class="chart-container">{top5_chart}</div>
</div>

<div class="card">
  <h2>策略回测排名 ({len(results)} 个策略)</h2>
  <table>
    <tr><th>#</th><th>策略名称</th><th>类型</th><th>总收益</th><th>胜率</th><th>夏普比率</th><th>最大回撤</th><th>交易次数</th><th>盈亏比</th><th>平均收益</th></tr>
{tbl}
  </table>
</div>

<div class="card">
  <h2>技术指标明细</h2>
  <table>
    <tr><th>指标名称</th><th>数值</th><th>评判</th></tr>
    <tr><td>RSI(14)</td><td>{rsi_val:.1f}</td><td>{rsi_s}</td></tr>
    <tr><td>MACD DIF</td><td>{md:.3f}</td><td>{m_stat}</td></tr>
    <tr><td>MACD Hist</td><td>{mh:+.4f}</td><td>{hist_s}</td></tr>
    <tr><td>布林位置 Pos</td><td>{bb_pos:.2f}</td><td>{bb_s}</td></tr>
    <tr><td>KDJ K</td><td>{k:.1f}</td><td>{k_s}</td></tr>
  </table>
</div>

<div class="footer">
  <p>{ticker} {stock_name} | 报告生成: {now} | VectorBT v2.2.0 | 数据源: 通达信/网络</p>
  <p style="margin-top:8px;color:var(--text-dim);font-size:12px">⚠️ 本报告仅供参考，不构成投资建议。回测结果不代表未来收益。</p>
</div>

</body>
</html>"""

    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"\nReport generated: {out_path} ({len(html)} bytes)")


# ==============================================================================
# Main
# ==============================================================================
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='VectorBT HuiCe BaoGao ShengChengQi')
    parser.add_argument('ticker', help='Agu 6Wei DaiMa')
    parser.add_argument('--data-dir', default=r'F:\new_tdx64', help='TDX ShuJu MuLu')
    parser.add_argument('--output', default=None, help='HTML BaoGao LuJing')
    args = parser.parse_args()

    # 获取数据（新数据层：XDXR复权 + 4层fallback）
    df = get_data(args.ticker, args.data_dir)
    price = df['Close'].astype(float)
    high = df['High'].astype(float)
    low = df['Low'].astype(float)

    be = BacktestEngine(price, high, low)
    results = be.run_all()

    # 获取中文名称
    try:
        import akshare as ak
        info = ak.stock_individual_info_em(symbol=args.ticker)
        row = info[info['item'] == '股票简称']
        stock_name = str(row['value'].iloc[0]) if not row.empty else ''
    except Exception:
        stock_name = ''

    out_path = args.output or os.path.join(os.getcwd(), f"{args.ticker}_vbt_report.html")
    generate_report(args.ticker, stock_name, df, results, be.all_pfs, out_path)
