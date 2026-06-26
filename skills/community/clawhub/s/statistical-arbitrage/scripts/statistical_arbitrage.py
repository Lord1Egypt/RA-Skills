#!/usr/bin/env python3
# Statistical Arbitrage - Obfuscated Version
import pandas as _p0
import numpy as _n0
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as _p1
import yfinance as _y0
import statsmodels.api as _s0
from statsmodels.tsa.stattools import adfuller as _a0, coint as _c0
from datetime import datetime as _d0
import warnings as _w0
_w0.filterwarnings('ignore')

_p1.rcParams['font.family'] = ['Arial Unicode MS', 'Heiti TC', 'SimHei', 'sans-serif']
_p1.rcParams['axes.unicode_minus'] = False
_b0, _f0 = '#1a1a2e', 'white'

_c1 = {
    's1': '1398.HK', 's2': '0939.HK', 'd0': '2020-01-01', 'd1': '2026-12-31',
    'r0': 0.7, 'e0': 2.0, 'e1': 0.5, 's3': 3.5, 'w0': 60, 't0': 0.0015,
    'i0': 100000, 'p0': 0.5, 'o0': '/Users/houloi/Desktop/代碼/',
}

def _f1(_t0, _d2, _d3):
    _r0 = _y0.download(_t0, start=_d2, end=_d3, progress=False)
    if _r0.empty: raise ValueError(f"Error: {_t0}")
    if isinstance(_r0.columns, _p0.MultiIndex):
        _df = _r0.xs(_t0, axis=1, level='Ticker').copy()
    else:
        _df = _r0.copy()
    _b1 = len(_df)
    _df = _df[_df['Volume'] > 0].copy()
    _a1 = len(_df)
    if _b1 != _a1: print(f"  Filtered {_b1-_a1} invalid days for {_t0}")
    print(f"  {_t0}: {len(_df)} valid days")
    return _df

def _f2(_df, _c2, _b2):
    _p2 = (_df[_c2].shift(1) + _df[_b2].shift(1) + _df[_df.columns[3]].shift(1)) / 3
    _r1 = 2 * _p2 - _df[_b2].shift(1)
    _s4 = 2 * _p2 - _df[_c2].shift(1)
    return _p2, _r1, _s4

def _f3(_d4, _z0, _b3):
    _c3 = _c1['i0']
    _p3 = 0
    _p4 = _c1['p0']
    _c4 = _c1['t0']
    _t1 = []
    _e2 = [_c3]
    _n1 = _n2 = 0
    _e3 = _e4 = 0.0
    _e5 = _b2 = 1.0
    
    for _i in range(1, len(_d4)):
        _dt = _d4.index[_i]
        _z = _d4[_z0].iloc[_i]
        _p5 = _d4['s1'].iloc[_i]
        _p6 = _d4['s2'].iloc[_i]
        
        if isinstance(_b3, _p0.Series):
            _b2 = _b3.loc[_dt] if _dt in _b3.index else _b2
        else:
            _b2 = _b3
        
        if _p3 == 0:
            _a2 = _c3 * _p4
            if _z < -_c1['e0']:
                _p3 = 1
                _n1 = _a2 / 2 / _p5
                _n2 = _a2 / 2 * _b2 / _p6
                _e3, _e4, _e5 = _p5, _p6, _b2
                _c3 -= _a2 * _c4
                _t1.append({'date': _dt, 'type': 'ENTRY_LONG', 'z': _z, 'price1': _p5, 'price2': _p6, 'pnl': 0})
            elif _z > _c1['e0']:
                _p3 = -1
                _n1 = _a2 / 2 / _p5
                _n2 = _a2 / 2 * _b2 / _p6
                _e3, _e4, _e5 = _p5, _p6, _b2
                _c3 -= _a2 * _c4
                _t1.append({'date': _dt, 'type': 'ENTRY_SHORT', 'z': _z, 'price1': _p5, 'price2': _p6, 'pnl': 0})
        
        elif _p3 == 1:
            _t2 = _z > -_c1['e1']
            _t3 = _z < -_c1['s3']
            if _t2 or _t3:
                _p7 = _n1*(_p5-_e3) - _n2*(_p6-_e4) - (_n1*_p5+_n2*_p6)*_c4
                _c3 += _p7
                _p3 = 0
                _t1.append({'date': _dt, 'type': 'EXIT_LONG', 'z': _z, 'price1': _p5, 'price2': _p6, 'pnl': _p7, 'reason': 'TP' if _t2 else 'SL'})
        
        elif _p3 == -1:
            _t2 = _z < _c1['e1']
            _t3 = _z > _c1['s3']
            if _t2 or _t3:
                _p7 = -_n1*(_p5-_e3) + _n2*(_p6-_e4) - (_n1*_p5+_n2*_p6)*_c4
                _c3 += _p7
                _p3 = 0
                _t1.append({'date': _dt, 'type': 'EXIT_SHORT', 'z': _z, 'price1': _p5, 'price2': _p6, 'pnl': _p7, 'reason': 'TP' if _t2 else 'SL'})
        
        _e2.append(_c3)
    
    if _p3 != 0:
        _p5f, _p6f = _d4['s1'].iloc[-1], _d4['s2'].iloc[-1]
        _p7 = (_n1*(_p5f-_e3) - _n2*(_p6f-_e4) if _p3==1 else -_n1*(_p5f-_e3) + _n2*(_p6f-_e4))
        _p7 -= (_n1*_p5f + _n2*_p6f) * _c4
        _c3 += _p7
        _t1.append({'date': _d4.index[-1], 'type': f'EXIT_{"LONG" if _p3==1 else "SHORT"}', 'z': _d4[_z0].iloc[-1], 'price1': _p5f, 'price2': _p6f, 'pnl': _p7, 'reason': 'FINAL'})
        _e2[-1] = _c3
    
    return _p0.DataFrame(_t1), _p0.Series(_e2, index=_d4.index)

def _f4(_e2, _t1, _l0):
    _r1 = _e2.pct_change().dropna()
    _t4 = (_e2.iloc[-1]/_e2.iloc[0] - 1) * 100
    _a3 = ((_e2.iloc[-1]/_e2.iloc[0]) ** (252/len(_e2)) - 1) * 100
    _v0 = _r1.std() * _n0.sqrt(252) * 100
    _s5 = (_r1.mean() / _r1.std()) * _n0.sqrt(252) if _r1.std() > 0 else 0
    _d5 = ((_e2 - _e2.cummax()) / _e2.cummax()).min() * 100
    _c5 = _a3 / abs(_d5) if _d5 != 0 else 0
    
    _e5 = _t1[_t1['type'].str.startswith('EXIT')] if len(_t1) else _p0.DataFrame()
    _w1 = (_e5['pnl'] > 0).mean() * 100 if len(_e5) else 0
    _a4 = _e5['pnl'].mean() if len(_e5) else 0
    _p8 = (_e5[_e5['pnl']>0]['pnl'].sum() / abs(_e5[_e5['pnl']<0]['pnl'].sum())) if len(_e5[_e5['pnl']<0]) > 0 else float('inf')
    
    print(f"\n{'─'*55}")
    print(f"  {_l0}")
    print(f"{'─'*55}")
    print(f"  Total: {_t4:+.2f}%  |  Ann: {_a3:+.2f}%  |  Vol: {_v0:.2f}%")
    print(f"  Sharpe: {_s5:.3f}  |  Calmar: {_c5:.3f}  |  MaxDD: {_d5:.2f}%")
    print(f"  Trades: {len(_e5)}  |  Win%: {_w1:.1f}%  |  Avg: ${_a4:.2f}")
    return dict(total=_t4, ann=_a3, vol=_v0, sharpe=_s5, dd=_d5, calmar=_c5, win_rate=_w1, trades=len(_e5))

if __name__ == '__main__':
    print("═" * 65)
    print("  Pair Trading Analysis")
    print(f"  {_c1['s1']} vs {_c1['s2']}")
    print("═" * 65)
    
    print("\nDownloading data...")
    _d6 = _f1(_c1['s1'], _c1['d0'], _c1['d1'])
    _d7 = _f1(_c1['s2'], _c1['d0'], _c1['d1'])
    
    _c6 = _p0.DataFrame({
        's1': _d6['Close'], 's2': _d7['Close'],
        'h1': _d6['High'], 'l1': _d6['Low'],
        'h2': _d7['High'], 'l2': _d7['Low'],
    }).dropna()
    print(f"  Common days: {len(_c6)}")
    
    _c6['log1'] = _n0.log(_c6['s1'])
    _c6['log2'] = _n0.log(_c6['s2'])
    
    _s6 = int(len(_c6) * _c1['r0'])
    _t5 = _c6.iloc[:_s6].copy()
    _t6 = _c6.iloc[_s6:].copy()
    print(f"\nTrain: {_t5.index[0].date()} -> {_t5.index[-1].date()} ({len(_t5)} days)")
    print(f"Test: {_t6.index[0].date()} -> {_t6.index[-1].date()} ({len(_t6)} days)")
    
    print("\nCointegration test (train)...")
    _c7, _p9, _c8 = _c0(_t5['log1'], _t5['log2'], autolag='AIC')
    print(f"  Stat: {_c7:.4f}  |  p: {_p9:.6f}  |  5%: {_c8[1]:.4f}")
    print(f"  {'Significant' if _p9 < 0.05 else 'Not significant'}")
    
    _x0 = _s0.add_constant(_t5['log2'])
    _m0 = _s0.OLS(_t5['log1'], _x0).fit()
    _a5 = _m0.params.iloc[0]
    _b4 = _m0.params.iloc[1]
    print(f"\nHedge ratio: alpha={_a5:.6f} beta={_b4:.6f} R2={_m0.rsquared:.4f}")
    
    _c6['spread'] = _c6['log1'] - _b4 * _c6['log2']
    _s7 = _c6['spread'].iloc[:_s6].mean()
    _s8 = _c6['spread'].iloc[:_s6].std()
    _c6['z'] = (_c6['spread'] - _s7) / _s8
    
    _a6 = _a0(_c6['spread'].iloc[:_s6], autolag='AIC')
    print(f"\nADF test: stat={_a6[0]:.4f} p={_a6[1]:.6f} {'Stationary' if _a6[1]<0.05 else 'Non-stationary'}")
    
    _z1 = _c6['z'].iloc[-1]
    print(f"\nCurrent Z-Score: {_z1:.2f}")
    if abs(_z1) > _c1['e0']:
        _sig = 'Long spread' if _z1 < 0 else 'Short spread'
        print(f"  Signal: {_sig}")
    else:
        print(f"  No signal (Z within ±{_c1['e0']})")
    
    print("\nRunning backtest...")
    _t7, _e6 = _f3(_c6.iloc[:_s6], 'z', _b4)
    _t8, _e7 = _f3(_c6.iloc[_s6:], 'z', _b4)
    
    _m1 = _f4(_e6, _t7, "Train")
    _m2 = _f4(_e7, _t8, "Test")
    
    print(f"\n{'═'*65}")
    print("  Summary")
    print(f"{'═'*65}")
    print(f"  Pair: {_c1['s1']} vs {_c1['s2']}")
    print(f"  Coint p: {_p9:.4f} ({'Significant' if _p9<0.05 else 'Not'})")
    print(f"  Beta: {_b4:.4f}")
    print(f"  Current Z: {_z1:.2f}")
    print(f"  Test: Ann {_m2['ann']:+.1f}%  Sharpe {_m2['sharpe']:.2f}  MaxDD {_m2['dd']:.1f}%")
    print(f"{'═'*65}")
