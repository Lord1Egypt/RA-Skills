"""
Tomasini & Jaekle(2009) + Aronson(2006) 防过拟合 / 样本外检验 — 自写演示
=========================================================================
逻辑：
  - 参数稳定性扫描：在训练集扫描参数，观察最优值是否"孤立尖峰"（尖峰=过拟合信号）
  - 样本外衰减：训练集选最优参数，测试集检验绩效是否显著下降
用法：python backtest_guardrails.py
"""
import numpy as np
import pandas as pd


def _strategy_returns(price: pd.Series, fast: int) -> pd.Series:
    """极简双均线式信号：快线上穿慢线(=fast)持多，否则空仓。"""
    ma = price.rolling(fast).mean()
    pos = (price > ma).astype(int).shift(1).fillna(0)
    return pos * price.pct_change().fillna(0)


def sharpe(ret: pd.Series) -> float:
    if ret.std() == 0:
        return 0.0
    return float(ret.mean() / ret.std() * np.sqrt(252))


def select_best_param(train_ret: pd.Series, grid=range(5, 61)) -> int:
    best_p, best_s = None, -np.inf
    for p in grid:
        s = sharpe(_strategy_returns(train_ret, p))
        if s > best_s:
            best_s, best_p = s, p
    return best_p


if __name__ == "__main__":
    np.random.seed(3)
    # 模拟一段有趋势的价格（含噪声）
    n = 800
    trend = np.cumsum(np.random.normal(0.0004, 1, n) + np.r_[np.zeros(400), np.ones(400) * 0.05])
    price = pd.Series(100 * np.exp(trend / 100))

    split = int(n * 0.6)
    train, test = price.iloc[:split], price.iloc[split:]

    best_p = select_best_param(train, range(5, 61))
    train_sharpe = sharpe(_strategy_returns(train, best_p))
    test_sharpe = sharpe(_strategy_returns(test, best_p))

    print(f"训练集最优快线周期 = {best_p}")
    print(f"训练集 Sharpe = {train_sharpe:.2f}")
    print(f"样本外 Sharpe = {test_sharpe:.2f}")
    print(f"样本外衰减     = {train_sharpe - test_sharpe:.2f}")
    if (train_sharpe - test_sharpe) > 0.5:
        print("⚠️ 样本外衰减明显：参数可能依赖历史噪声，建议 widen 参数或简化模型。")
    else:
        print("✅ 样本外衰减可控，参数泛化较好。")
