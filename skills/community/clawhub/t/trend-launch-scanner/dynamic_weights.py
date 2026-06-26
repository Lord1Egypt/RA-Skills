#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
动态权重系统
根据近期验证数据自动调整信号权重
"""
import json
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

DATA_DIR = Path("C:/Users/Administrator/.qclaw/workspace-ag01/data/trend_scan")
WEIGHTS_FILE = DATA_DIR / "signal_weights.json"

# 默认权重（基于对照组验证）
DEFAULT_WEIGHTS = {
    "macd_hist_pos": {"score": 25, "label": "MACD柱线为正", "base": 26},
    "above_ma20": {"score": 20, "label": "价格>MA20", "base": 21},
    "rsi_rising": {"score": 15, "label": "RSI上升", "base": 19},
    "rsi_above50": {"score": 15, "label": "RSI>50", "base": 18},
    "price_rising": {"score": 10, "label": "窗口内上升", "base": 18},
    "ma_bullish": {"score": 10, "label": "均线多头", "base": 16},
    "macd_hist_rising": {"score": 5, "label": "MACD柱线增大", "base": 15},
}


def load_weights():
    """加载权重设置"""
    if WEIGHTS_FILE.exists():
        with open(WEIGHTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return DEFAULT_WEIGHTS.copy()


def save_weights(weights):
    """保存权重设置"""
    WEIGHTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(WEIGHTS_FILE, "w", encoding="utf-8") as f:
        json.dump(weights, f, ensure_ascii=False, indent=2)


def update_weights_from_verification(performance_data):
    """
    根据验证数据更新权重
    
    performance_data: [{"signals": {...}, "gain_pct": +5.2}, ...]
    """
    weights = load_weights()
    
    # 统计每个信号在不同收益下的出现频率
    signal_performance = defaultdict(list)
    
    for record in performance_data:
        gain = record["gain_pct"]
        signals = record.get("signals", {})
        
        for sig_name, sig_value in signals.items():
            if sig_name in weights and sig_value:
                signal_performance[sig_name].append(gain)
    
    # 计算每个信号的平均收益贡献
    adjustments = {}
    for sig_name, gains in signal_performance.items():
        if gains:
            avg_gain = sum(gains) / len(gains)
            # 基础权重调整：收益越高，权重越高
            if avg_gain > 5:
                adjustments[sig_name] = 5  # +5分
            elif avg_gain > 2:
                adjustments[sig_name] = 0  # 不变
            elif avg_gain > 0:
                adjustments[sig_name] = -3  # -3分
            else:
                adjustments[sig_name] = -5  # -5分
    
    # 应用调整
    for sig_name, adjustment in adjustments.items():
        old_score = weights[sig_name]["score"]
        new_score = max(0, min(30, old_score + adjustment))
        weights[sig_name]["score"] = new_score
        weights[sig_name]["adjustment"] = adjustment
        weights[sig_name]["avg_gain"] = round(sum(signal_performance[sig_name]) / len(signal_performance[sig_name]), 2)
    
    # 归一化（确保总分=100）
    total = sum(w["score"] for w in weights.values())
    if total != 100 and total > 0:
        factor = 100 / total
        for w in weights.values():
            w["score"] = round(w["score"] * factor)
    
    save_weights(weights)
    return weights


def get_current_weights():
    """获取当前权重"""
    return load_weights()


def reset_weights():
    """重置为默认权重"""
    save_weights(DEFAULT_WEIGHTS.copy())
    return DEFAULT_WEIGHTS


def print_weights(weights):
    """打印权重设置"""
    print("=" * 50)
    print("当前信号权重（动态调整版）")
    print("=" * 50)
    print()
    print(f"{'信号':<15} {'分值':>5} {'近期收益':>8} {'调整':>5}")
    print("-" * 50)
    
    for sig_name, w in sorted(weights.items(), key=lambda x: x[1]["score"], reverse=True):
        adj = w.get("adjustment", 0)
        avg = w.get("avg_gain", "-")
        adj_str = f"{adj:+d}" if isinstance(adj, int) else "-"
        avg_str = f"{avg:+.1f}%" if isinstance(avg, float) else "-"
        print(f"{w['label']:<15} {w['score']:>5} {avg_str:>8} {adj_str:>5}")
    
    total = sum(w["score"] for w in weights.values())
    print("-" * 50)
    print(f"{'总分':<15} {total:>5}")
    print()


if __name__ == "__main__":
    # 测试
    print("动态权重系统测试")
    print()
    
    # 显示当前权重
    weights = get_current_weights()
    print_weights(weights)
    
    # 模拟验证数据
    test_data = [
        {"signals": {"macd_hist_pos": 1, "above_ma20": 1, "rsi_rising": 1, "rsi_above50": 1, "ma_bullish": 1}, "gain_pct": 8.5},
        {"signals": {"macd_hist_pos": 1, "above_ma20": 1, "rsi_rising": 1}, "gain_pct": 5.2},
        {"signals": {"macd_hist_pos": 1, "above_ma20": 1}, "gain_pct": 3.1},
        {"signals": {"macd_hist_pos": 1, "ma_bullish": 1}, "gain_pct": -2.3},
        {"signals": {"above_ma20": 1, "rsi_above50": 1}, "gain_pct": 1.5},
    ]
    
    print("\n模拟更新权重...")
    new_weights = update_weights_from_verification(test_data)
    print("\n更新后:")
    print_weights(new_weights)
