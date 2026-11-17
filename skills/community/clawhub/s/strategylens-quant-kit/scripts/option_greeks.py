"""
Sinclair(2020) / Hilpisch(2015) 期权定价与 Greeks — 自写演示（非原书代码）
=========================================================================
用最基础的 Black-Scholes 公式自写看涨/看跌定价与主要 Greeks
（delta/gamma/vega/theta/rho）。仅依赖标准库 math 与 numpy，
不依赖任何期权库，也不复制原书代码。
用法：python option_greeks.py
"""
import math
import numpy as np


def _norm_cdf(x):
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def _norm_pdf(x):
    return math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)


def bs_price(S, K, T, r, sigma, kind="call"):
    if T <= 0 or sigma <= 0:
        return max(0.0, S - K) if kind == "call" else max(0.0, K - S)
    d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    if kind == "call":
        return S * _norm_cdf(d1) - K * math.exp(-r * T) * _norm_cdf(d2)
    return K * math.exp(-r * T) * _norm_cdf(-d2) - S * _norm_cdf(-d1)


def bs_greeks(S, K, T, r, sigma, kind="call"):
    if T <= 0 or sigma <= 0:
        return {"delta": 0.0, "gamma": 0.0, "vega": 0.0, "theta": 0.0, "rho": 0.0}
    d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    nd1 = _norm_pdf(d1)
    sqrtT = math.sqrt(T)
    gamma = nd1 / (S * sigma * sqrtT)
    vega = S * nd1 * sqrtT / 100.0          # 每 1 vol 点
    if kind == "call":
        delta = _norm_cdf(d1)
        theta = (-S * nd1 * sigma / (2 * sqrtT)
                 - r * K * math.exp(-r * T) * _norm_cdf(d2)) / 100.0
        rho = K * T * math.exp(-r * T) * _norm_cdf(d2) / 100.0
    else:
        delta = _norm_cdf(d1) - 1.0
        theta = (-S * nd1 * sigma / (2 * sqrtT)
                 + r * K * math.exp(-r * T) * _norm_cdf(-d2)) / 100.0
        rho = -K * T * math.exp(-r * T) * _norm_cdf(-d2) / 100.0
    return {"delta": delta, "gamma": gamma, "vega": vega, "theta": theta, "rho": rho}


if __name__ == "__main__":
    S, K, T, r, sigma = 100.0, 100.0, 0.5, 0.02, 0.20
    print(f"标的 S={S} 行权 K={K} 期限 T={T}年 无风险 r={r} 波动率 σ={sigma}")
    for kind in ("call", "put"):
        p = bs_price(S, K, T, r, sigma, kind)
        g = bs_greeks(S, K, T, r, sigma, kind)
        print(f"\n{kind.upper()} 价格 = {p:.4f}")
        print("  Greeks:", {k: round(v, 4) for k, v in g.items()})
    print("\n✅ 自写 Black-Scholes 定价与 Greeks 演示完成"
          "（对应 Sinclair 头寸 Greeks / Hilpisch 定价）。")
