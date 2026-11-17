"""
Danielsson(2011) 风险预测简化演示 — 自写（非原书代码）
=====================================================
用自包含方法演示：
  - EWMA(RiskMetrics) 波动率预测
  - 历史模拟法 VaR 与 ES(期望短缺)
精确 GARCH(1,1) 与极值理论 EVT 需 arch 等包，此处用简化版演示思路。
用法：python risk_forecast.py
"""
import math
import numpy as np
import pandas as pd


def ewma_vol(returns, lam=0.94):
    v = float(returns.var())
    out = []
    for r in returns.values:
        v = lam * v + (1.0 - lam) * r * r
        out.append(math.sqrt(v))
    return pd.Series(out, index=returns.index)


def historical_var_es(returns, alpha=0.05):
    q = np.percentile(returns.values, alpha * 100)
    var = -q
    tail = returns[returns <= q]
    es = -tail.mean() if len(tail) > 0 else var
    return float(var), float(es)


if __name__ == "__main__":
    np.random.seed(7)
    n = 1000
    ret = pd.Series(np.random.normal(0, 0.01, n))
    ret.iloc[-1] = -0.06                  # 人为加入一个尾部极端负收益

    ev = ewma_vol(ret, lam=0.94)
    print(f"EWMA 最新日波动预测 = {ev.iloc[-1]:.4f}  (年化≈{ev.iloc[-1]*math.sqrt(252):.3f})")
    var, es = historical_var_es(ret, alpha=0.05)
    print(f"历史模拟 VaR(95%) = {var:.4f}   ES(95%) = {es:.4f}")
    print("\n✅ 风险预测简化演示完成（对应 Danielsson 波动预测/VaR/ES）。"
          "精确 GARCH/EVT 需 arch 包。")
