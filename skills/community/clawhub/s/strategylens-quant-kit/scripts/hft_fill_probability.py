"""
Lehalle & Laruelle(2018) / 微观结构 — 限价单成交概率（自写演示，非原书代码）
=================================================================================
用最简单模型演示：被动限价单的成交概率随「队列位置」衰减。
假设队首成交概率最高，越靠后越低（指数衰减）。仅为教学示意，
真实模型需 tick/Level-2 数据与更复杂的动态。
用法：python hft_fill_probability.py
"""
import numpy as np


def fill_prob(queue_pos, lam=0.3):
    """队列位置 queue_pos(0=队首) 处的成交概率，指数衰减。"""
    return float(np.exp(-lam * queue_pos))


if __name__ == "__main__":
    print("限价单成交概率随队列位置衰减（λ=0.3）:")
    for q in range(0, 8):
        print(f"  队列位置 {q}: 成交概率 ≈ {fill_prob(q, 0.3):.3f}")
    front_orders = 12
    p = fill_prob(front_orders, lam=0.3)
    print(f"\n前方有 {front_orders} 笔挂单时，本单成交概率 ≈ {p:.3f}")
    print("✅ 限价单排队成交概率演示完成（对应微观结构订单簿/成交概率建模）。")
