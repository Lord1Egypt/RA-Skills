"""
MacLean et al.(2011) / Kelly 资本增长 — 自写演示（非原书代码）
=============================================================
实现：给定策略的历史胜率 p 与盈亏比 b（赢时赚 b 倍下注额），
计算 Kelly 最优下注比例 f* = p - (1-p)/b，以及更稳健的半 Kelly (f*/2)。
同时给出基于收益序列估计 p、b 的简化方法。
用法：python kelly_position.py
"""
import numpy as np
import pandas as pd


def kelly_fraction(p, b):
    """p=胜率, b=净盈亏比(赢时赚b倍本金)。返回 Kelly 比例 f*。"""
    if b <= 0:
        return 0.0
    f = p - (1.0 - p) / b
    return float(np.clip(f, 0.0, 1.0))


def kelly_from_returns(returns: pd.Series):
    """从收益序列估计 p、b，再算 Kelly / 半 Kelly。"""
    wins = returns[returns > 0]
    losses = returns[returns < 0]
    if len(wins) == 0 or len(losses) == 0:
        return {"p": np.nan, "b": np.nan, "kelly": 0.0, "half_kelly": 0.0}
    p = len(wins) / len(returns)
    b = wins.mean() / abs(losses.mean())     # 平均盈利 / 平均亏损
    f = kelly_fraction(p, b)
    return {"p": p, "b": float(b), "kelly": f, "half_kelly": f / 2.0}


if __name__ == "__main__":
    np.random.seed(11)
    # 模拟一个策略的日收益：60% 天数小赚，40% 小亏
    n = 600
    r = np.where(np.random.rand(n) < 0.55,
                 np.random.normal(0.0012, 0.01, n),
                 np.random.normal(-0.0010, 0.012, n))
    ret = pd.Series(r)

    res = kelly_from_returns(ret)
    print(f"估计胜率 p = {res['p']:.3f}   盈亏比 b = {res['b']:.3f}")
    print(f"Kelly 最优下注比例 f*     = {res['kelly']:.3f}")
    print(f"半 Kelly（更稳健）f*/2   = {res['half_kelly']:.3f}")
    print("\n✅ Kelly/半 Kelly 仓位演示完成（对应 MacLean 资本增长理论）。"
          "实际常取半 Kelly 以控回撤。")
