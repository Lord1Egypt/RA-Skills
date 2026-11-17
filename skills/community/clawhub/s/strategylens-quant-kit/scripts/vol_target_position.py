"""
Carver(2015) 波动率目标化仓位 — 自写演示（非原书代码）
=====================================================
逻辑：目标账户年化波动 σ*，某品种年化波动 σ_i，
      仓位权重 ≈ σ* / σ_i（受 max_leverage 上限约束）。
      注：期货为保证金交易，波动率目标化权重常 >1（以杠杆实现名义敞口）；
          股票/零售场景可调低 max_leverage。默认 3.0 适配期货系统化交易。
用法：python vol_target_position.py
"""
import numpy as np
import pandas as pd


def vol_target_weight(returns: pd.Series, target_vol: float = 0.20,
                      period: int = 252, max_leverage: float = 3.0) -> float:
    vol = returns.std() * np.sqrt(period)
    if vol <= 0:
        return 0.0
    w = target_vol / vol
    return float(np.clip(w, 0.0, max_leverage))


if __name__ == "__main__":
    np.random.seed(0)
    # 模拟某品种 500 个交易日的日收益
    price = pd.Series(100 * np.cumprod(1 + np.random.normal(0.0005, 0.02, 500)))
    returns = price.pct_change().dropna()

    for tv in (0.15, 0.20, 0.25):
        w = vol_target_weight(returns, target_vol=tv)
        print(f"目标波动={tv:.2f} | 品种年化波动={returns.std()*np.sqrt(252):.3f} "
              f"| 建议仓位权重={w:.3f}")
