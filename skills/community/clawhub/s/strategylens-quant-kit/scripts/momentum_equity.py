"""
Clenow(2015) 股票动量策略 — 自写演示（非原书代码）
=================================================
逻辑：
  1) 动量信号：价格是否接近 N 日新高（rolling max * pct）
  2) 波动率目标化配权：按各股波动反比配权，把组合波动压到 target_vol
用法：python momentum_equity.py
（真实回测时把 px 替换为 MCP 拉取的真实行情即可）
"""
import numpy as np
import pandas as pd


def momentum_signal(price: pd.Series, lookback: int = 200, pct: float = 0.95) -> bool:
    return bool(price.iloc[-1] >= price.rolling(lookback).max().iloc[-1] * pct)


def vol_target_weights(returns: pd.DataFrame, target_vol: float = 0.20) -> pd.Series:
    ann_vol = (returns.std() * np.sqrt(252)).replace(0, np.nan)
    inv_vol = 1.0 / ann_vol
    w = inv_vol / inv_vol.sum()
    return w.fillna(0.0)


if __name__ == "__main__":
    np.random.seed(1)
    assets = ["STK_A", "STK_B", "STK_C", "STK_D"]
    px = pd.DataFrame(
        {a: 100 * np.cumprod(1 + np.random.normal(0.0004, 0.02, 600)) for a in assets}
    )
    ret = px.pct_change().dropna()

    print("=== 动量信号（接近 200 日新高？）===")
    sig = {a: momentum_signal(px[a], 200, 0.95) for a in assets}
    for a, s in sig.items():
        print(f"  {a}: {'入选' if s else '未入选'}")

    w = vol_target_weights(ret, target_vol=0.20)
    print("\n=== 波动率目标化组合权重（仅示例，未过滤未入选）===")
    for a, wi in w.round(3).items():
        print(f"  {a}: {wi}")

    # 仅对入选股票配权
    selected = [a for a, s in sig.items() if s]
    if selected:
        w_sel = vol_target_weights(ret[selected], 0.20)
        print(f"\n=== 入选组合权重（{selected}）===")
        for a, wi in w_sel.round(3).items():
            print(f"  {a}: {wi}")
