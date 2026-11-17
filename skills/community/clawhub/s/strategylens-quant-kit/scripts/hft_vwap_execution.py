"""
Lehalle & Laruelle(2018) 执行算法 — VWAP/TWAP 拆单（自写演示，非原书代码）
=================================================================================
把一笔大单拆成若干子单：TWAP(均匀) vs VWAP(按日内成交量轮廓)。
用模拟的 U 形成交量曲线演示，比较两者对成交量轮廓的跟踪误差。
用法：python hft_vwap_execution.py
"""
import numpy as np


def vwap_weights(n_slices, shape="u"):
    """生成 n_slices 段的成交量权重。shape='u' 为 U 形(开盘/收盘重)，'flat' 为均匀。"""
    if shape == "flat":
        w = np.ones(n_slices)
    else:
        t = np.linspace(0, 1, n_slices)
        w = 0.5 + 0.5 * np.cos(2 * np.pi * (t - 0.5))   # U 形：两端高中间低
        w = np.clip(w, 0.01, None)
    return w / w.sum()


def execute(total_qty, n_slices, shape):
    return vwap_weights(n_slices, shape) * total_qty


if __name__ == "__main__":
    total, n = 100000, 10
    twap = execute(total, n, "flat")
    vwap = execute(total, n, "u")
    print(f"大单总量={total}, 拆成 {n} 段")
    print("TWAP(均匀) 每段:", np.round(twap).astype(int).tolist())
    print("VWAP(U形)   每段:", np.round(vwap).astype(int).tolist())

    true_curve = vwap_weights(n, "u")
    twap_curve = vwap_weights(n, "flat")
    mse_twap = float(((twap_curve - true_curve) ** 2).mean())
    mse_vwap = float(((vwap_weights(n, "u") - true_curve) ** 2).mean())
    print(f"\nTWAP 与真实成交量轮廓的均方误差 = {mse_twap:.4f}")
    print(f"VWAP 与真实成交量轮廓的均方误差 = {mse_vwap:.4f}")
    print("✅ VWAP/TWAP 拆单执行演示完成（对应 Lehalle 执行优化）。")
