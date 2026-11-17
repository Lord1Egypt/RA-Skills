"""
Carver(2017) 简化风险平价（对角近似）— 自写演示（非原书代码）
=============================================================
说明：风险平价的"精确版"是等风险贡献(ERC)，需迭代求解协方差非对角项，
      实现较复杂且对数值敏感。此处采用文献中最常用的**简化（对角近似）**：
      按各资产年化波动反比配权（w_i ∝ 1/σ_i）。当资产间相关性较低时，
      该权重非常接近等风险贡献，且永远稳定、权重非负。
      若要精确 ERC，参考 Carver(2017) 或 Roncalli 的风险预算框架。
用法：python risk_parity.py
"""
import numpy as np
import pandas as pd


def risk_parity_weights(returns: pd.DataFrame) -> pd.Series:
    ann_vol = (returns.std() * np.sqrt(252)).replace(0, np.nan)
    inv_vol = 1.0 / ann_vol
    w = inv_vol / inv_vol.sum()
    return w.fillna(0.0)


if __name__ == "__main__":
    np.random.seed(2)
    # 模拟 4 个相关性较低的资产收益（B、D 波动更低）
    n = 500
    a = np.random.normal(0.0003, 0.015, n)
    b = np.random.normal(0.0002, 0.010, n)
    c = np.random.normal(0.0004, 0.020, n)
    d = np.random.normal(0.0001, 0.008, n)
    ret = pd.DataFrame({"AST_A": a, "AST_B": b, "AST_C": c, "AST_D": d})

    w = risk_parity_weights(ret)
    print("简化风险平价（逆波动）权重：")
    for k, wi in w.round(3).items():
        print(f"  {k}: 年化波动≈{ret[k].std()*np.sqrt(252):.3f} | 权重={wi}")
    print("\n✅ 波动越低的资产权重越高（B、D 应高于 A、C），符合风险平价直觉。")
