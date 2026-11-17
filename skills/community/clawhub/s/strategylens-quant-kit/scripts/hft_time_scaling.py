"""
Dacorogna et al.(2001) 高频时间缩放/标度律 — 自写演示（非原书代码）
============================================================================
用模拟高频收益（带波动聚集）演示：
  - 将 tick 收益聚合到不同频率（1/5/15/60 分钟），观察波动率随聚合长度的缩放；
  - 高频收益典型呈「平方收益自相关」（波动聚集），聚合后减弱。
用法：python hft_time_scaling.py
"""
import numpy as np
import pandas as pd


def simulate_tick_returns(n, base_vol=0.001, cluster=0.98):
    """生成带波动聚集的高频收益（GARCH 类简化）。"""
    vol = base_vol
    out = []
    for _ in range(n):
        vol = cluster * vol + (1 - cluster) * base_vol + 0.0005 * abs(np.random.randn())
        out.append(np.random.randn() * vol)
    return pd.Series(out)


def aggregate_vol(returns, freqs):
    rows = []
    m = len(returns) // max(freqs) * max(freqs)
    arr = returns.values[:m]
    for f in freqs:
        k = m // f
        agg = arr[: k * f].reshape(k, f).sum(axis=1)
        # agg 是 f 个 tick 的累计收益，其 std 即「聚合 f ticks 的段波动率」，
        # 按 √Δt 规律应随 √f 增长（无需再乘 √f，否则会重复缩放）。
        rows.append((f, float(np.std(agg))))
    return rows


if __name__ == "__main__":
    np.random.seed(5)
    ticks = simulate_tick_returns(6000)
    print(f"模拟 tick 收益 {len(ticks)} 条，tick 波动率 ≈ {ticks.std():.4f}")
    print("不同聚合频率下的波动率（验证 √Δt 缩放规律）:")
    for f, v in aggregate_vol(ticks, [1, 5, 15, 60]):
        print(f"  聚合 {f:>2} ticks -> 波动率 ≈ {v:.4f}  (√{f} 倍 ≈ {np.sqrt(f):.2f})")

    sq = ticks ** 2
    ac1 = float(sq.autocorr(1))
    print(f"\n平方收益 1 阶自相关 ≈ {ac1:.3f} （>0 表示存在波动聚集，符合高频数据特征）")
    print("✅ 高频时间缩放/标度律演示完成（对应 Dacorogna 时间缩放）。")
