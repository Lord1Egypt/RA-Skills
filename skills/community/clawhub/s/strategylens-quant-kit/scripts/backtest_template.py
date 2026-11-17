"""通用回测模板（仅供研究，非投资建议）
========================================
数据接入（二选一）：
  1) 用配套 MCP 的 get_price_history 取数后，构造
     df = pd.DataFrame(result['data'])  # 含 date/open/high/low/close/volume
  2) 读取本地 CSV：
     df = pd.read_csv('price.csv', parse_dates=['date'])

所有策略返回带 'strat'（策略日收益）列的 DataFrame，
再由 performance() 计算累计收益 / 年化 / Sharpe / 最大回撤。
"""

import numpy as np
import pandas as pd


# ---------------- 策略函数（与 references/strategies.md 对应） ----------------

def ma_crossover(df, short=5, long=20):
    df = df.copy()
    df['ma_s'] = df['close'].rolling(short).mean()
    df['ma_l'] = df['close'].rolling(long).mean()
    df['signal'] = 0
    df.loc[df['ma_s'] > df['ma_l'], 'signal'] = 1
    df.loc[df['ma_s'] < df['ma_l'], 'signal'] = -1
    df['position'] = df['signal'].shift(1).fillna(0)
    df['ret'] = df['close'].pct_change()
    df['strat'] = df['position'] * df['ret']
    return df


def turtle(df, entry=20, exit_n=10, atr_n=20):
    df = df.copy()
    df['hh'] = df['high'].rolling(entry).max().shift(1)
    df['ll'] = df['low'].rolling(exit_n).min().shift(1)
    df['tr'] = (df['high'] - df['low']).rolling(atr_n).mean()
    df['signal'] = 0
    df.loc[df['close'] > df['hh'], 'signal'] = 1
    df.loc[df['close'] < df['ll'], 'signal'] = -1
    df['position'] = df['signal'].shift(1).fillna(0)
    df['ret'] = df['close'].pct_change()
    df['strat'] = df['position'] * df['ret']
    return df


def bollinger_reversion(df, period=20, k=2):
    df = df.copy()
    mid = df['close'].rolling(period).mean()
    std = df['close'].rolling(period).std()
    df['upper'] = mid + k * std
    df['lower'] = mid - k * std
    df['signal'] = 0
    df.loc[df['close'] < df['lower'], 'signal'] = 1
    df.loc[df['close'] > df['upper'], 'signal'] = -1
    df['position'] = df['signal'].shift(1).fillna(0)
    df['ret'] = df['close'].pct_change()
    df['strat'] = df['position'] * df['ret']
    return df


def momentum(df, window=90):
    df = df.copy()
    df['mom'] = df['close'].pct_change(window)
    df['signal'] = 0
    df.loc[df['mom'] > 0, 'signal'] = 1
    df.loc[df['mom'] < 0, 'signal'] = -1
    df['position'] = df['signal'].shift(1).fillna(0)
    df['ret'] = df['close'].pct_change()
    df['strat'] = df['position'] * df['ret']
    return df


def calendar_spread(near, far, window=20, z=2):
    spread = near['close'] - far['close']
    zscore = (spread - spread.rolling(window).mean()) / spread.rolling(window).std()
    signal = -((zscore > z).astype(int) - (zscore < -z).astype(int))
    out = pd.DataFrame({'spread': spread, 'zscore': zscore, 'signal': signal})
    out['position'] = out['signal'].shift(1).fillna(0)
    out['ret'] = spread.pct_change()
    out['strat'] = out['position'] * out['ret']
    return out


def pair_trade(a, b, window=30, z=2):
    ratio = a['close'] / b['close']
    zscore = (ratio - ratio.rolling(window).mean()) / ratio.rolling(window).std()
    signal_a = -(zscore > z).astype(int) + (zscore < -z).astype(int)
    out = pd.DataFrame({'ratio': ratio, 'zscore': zscore, 'signal_a': signal_a})
    return out


# ---------------- 绩效统计 ----------------

def performance(df, col='strat'):
    """输入含 strat 列的 df，返回绩效字典。"""
    s = df[col].fillna(0)
    cum = (1 + s).cumprod()
    n = len(s)
    ann = cum.iloc[-1] ** (252.0 / max(n, 2)) - 1 if n > 1 else 0
    sharpe = np.sqrt(252) * s.mean() / (s.std() + 1e-9)
    peak = cum.cummax()
    mdd = (cum - peak) / peak
    return {
        "final_equity": round(float(cum.iloc[-1]), 4),
        "ann_return": round(float(ann), 4),
        "sharpe": round(float(sharpe), 3),
        "max_drawdown": round(float(mdd.min()), 4),
    }


if __name__ == "__main__":
    # 演示：用随机游走数据测试 ma_crossover（不联网）
    np.random.seed(0)
    dates = pd.date_range("2025-01-01", periods=300)
    price = 100 + np.cumsum(np.random.randn(300))
    df = pd.DataFrame({
        "date": dates,
        "close": price,
        "open": price,
        "high": price + 0.5,
        "low": price - 0.5,
        "volume": 1000,
    })
    out = ma_crossover(df, short=5, long=20)
    print("[演示] 双均线回测绩效（随机数据，仅验证代码）:", performance(out))
    print("⚠️ 仅供研究，非投资建议。实盘请用真实行情并做样本外检验。")
