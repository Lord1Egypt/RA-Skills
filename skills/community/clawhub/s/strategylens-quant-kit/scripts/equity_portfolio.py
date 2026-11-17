"""
Chincarini & Kim(2009) 量化权益组合 — 自写演示（非原书代码）
==============================================================
用最简方式演示：因子暴露（这里用单一动量因子）+ 组合优化（最大化
预期收益/波动比，带长仓约束）。对应书中 factor model / optimization 的入门思路。
精确实现需更多因子与约束求解器，此处用自包含 numpy 演示核心逻辑。
用法：python equity_portfolio.py
"""
import numpy as np
import pandas as pd


def simple_momentum(returns: pd.DataFrame, lookback=60):
    """用过去 lookback 期累计收益作为动量因子得分。"""
    return returns.rolling(lookback).sum().iloc[-1]


def long_only_max_sharpe(returns: pd.DataFrame, top_n=3):
    """在动量得分最高的 top_n 只里，按波动反比配权（简化 max-Sharpe）。"""
    score = simple_momentum(returns)
    top = score.nlargest(top_n).index.tolist()
    sub = returns[top]
    inv_vol = 1.0 / (sub.std() * np.sqrt(252)).replace(0, np.nan)
    w = inv_vol / inv_vol.sum()
    port_ret = (sub * w).sum(axis=1)
    sharpe = port_ret.mean() / port_ret.std() * np.sqrt(252)
    return top, w.round(3), float(sharpe)


if __name__ == "__main__":
    np.random.seed(13)
    assets = [f"EQ{i:02d}" for i in range(8)]
    n = 400
    px = pd.DataFrame(
        {a: 100 * np.cumprod(1 + np.random.normal(0.0004, 0.015, n)) for a in assets}
    )
    ret = px.pct_change().dropna()

    top, w, sharpe = long_only_max_sharpe(ret, top_n=3)
    print(f"动量得分最高的 {len(top)} 只: {top}")
    print("波动率目标化组合权重:")
    for a, wi in w.items():
        print(f"  {a}: {wi}")
    print(f"\n组合年化 Sharpe ≈ {sharpe:.2f}")
    print("\n✅ 量化权益组合（动量因子+优化配权）演示完成"
          "（对应 Chincarini & Kim 因子模型/优化思路）。")
