#!/usr/bin/env python3
"""
仓位计算器
Position Size Calculator

根据风险承受能力、信号置信度、止损位计算建议仓位

公式：
仓位大小 = (总资金 × 风险比例) / (入场价 - 止损价)
风险金额 = 总资金 × 风险比例
"""

import sys
from pathlib import Path
from datetime import datetime

# 加载配置
from config import load_config

config = load_config()

def calculate_position_size(
    total_capital: float,
    entry_price: float,
    stop_loss_price: float,
    risk_profile: str = "moderate",
    confidence: str = "medium",
    max_position_pct: float = None
) -> dict:
    """
    计算仓位大小
    
    Args:
        total_capital: 总资金 ($)
        entry_price: 入场价 ($)
        stop_loss_price: 止损价 ($)
        risk_profile: 风险偏好 (conservative/moderate/aggressive)
        confidence: 置信度 (low/medium/high)
        max_position_pct: 单只股票最大仓位 (%)
    
    Returns:
        {
            "shares": 100,           # 建议股数
            "position_value": 17500, # 仓位价值 ($)
            "position_pct": 17.5,    # 仓位占比 (%)
            "risk_amount": 1400,     # 风险金额 ($)
            "risk_pct": 2.0,         # 风险比例 (%)
            "stop_loss_pct": 8.0     # 止损幅度 (%)
        }
    """
    
    # 风险偏好对应的基础风险比例
    risk_profiles = {
        "conservative": 1.0,   # 保守：1% 风险
        "moderate": 2.0,       # 稳健：2% 风险
        "aggressive": 3.0      # 进取：3% 风险
    }
    
    base_risk_pct = risk_profiles.get(risk_profile, 2.0)
    
    # 根据置信度调整风险
    confidence_multipliers = {
        "high": 1.5,     # 高置信度：增加 50% 风险
        "medium": 1.0,   # 中置信度：基准
        "low": 0.5       # 低置信度：减少 50% 风险
    }
    
    confidence_mult = confidence_multipliers.get(confidence, 1.0)
    
    # 计算实际风险比例
    actual_risk_pct = base_risk_pct * confidence_mult
    
    # 计算风险金额
    risk_amount = total_capital * (actual_risk_pct / 100)
    
    # 计算止损幅度
    if entry_price > 0 and stop_loss_price > 0:
        stop_loss_pct = abs(entry_price - stop_loss_price) / entry_price * 100
    else:
        stop_loss_pct = 8.0  # 默认 8% 止损
    
    # 计算仓位大小
    # 仓位大小 = 风险金额 / 止损幅度
    if stop_loss_pct > 0 and entry_price > 0:
        position_value = risk_amount / (stop_loss_pct / 100)
        shares = int(position_value / entry_price)
        
        # 确保股数为正
        if shares <= 0:
            shares = 0
            position_value = 0
    else:
        shares = 0
        position_value = 0
    
    # 计算仓位占比
    position_pct = (position_value / total_capital * 100) if total_capital > 0 else 0
    
    # 应用最大仓位限制
    if max_position_pct is None:
        max_position_pct = config.get("technical_analysis", {}).get("position_sizing", {}).get("max_position_pct", 20.0)
    
    if position_pct > max_position_pct:
        # 超过最大仓位，调整
        position_pct = max_position_pct
        position_value = total_capital * (max_position_pct / 100)
        shares = int(position_value / entry_price)
        # 重新计算实际风险
        risk_amount = position_value * (stop_loss_pct / 100)
        actual_risk_pct = (risk_amount / total_capital * 100)
    
    return {
        "shares": shares,
        "position_value": round(position_value, 2),
        "position_pct": round(position_pct, 2),
        "risk_amount": round(risk_amount, 2),
        "risk_pct": round(actual_risk_pct, 2),
        "stop_loss_pct": round(stop_loss_pct, 2),
        "entry_price": entry_price,
        "stop_loss_price": stop_loss_price,
        "total_capital": total_capital,
        "risk_profile": risk_profile,
        "confidence": confidence
    }

def calculate_portfolio_allocation(
    total_capital: float,
    positions: list,
    risk_profile: str = "moderate"
) -> dict:
    """
    计算投资组合配置
    
    Args:
        total_capital: 总资金
        positions: 持仓列表 [{symbol, entry_price, stop_loss, confidence}, ...]
        risk_profile: 风险偏好
    
    Returns:
        {
            "allocations": [...],  # 每只股票的配置
            "total_invested": ..., # 总投资
            "total_risk": ...,     # 总风险
            "cash": ...,          # 剩余现金
            "cash_pct": ...       # 现金比例
        }
    """
    
    allocations = []
    total_invested = 0
    total_risk = 0
    
    for pos in positions:
        result = calculate_position_size(
            total_capital=total_capital,
            entry_price=pos["entry_price"],
            stop_loss_price=pos.get("stop_loss", pos["entry_price"] * 0.92),
            risk_profile=risk_profile,
            confidence=pos.get("confidence", "medium")
        )
        
        allocation = {
            "symbol": pos.get("symbol", "UNKNOWN"),
            **result
        }
        
        allocations.append(allocation)
        total_invested += result["position_value"]
        total_risk += result["risk_amount"]
    
    cash = total_capital - total_invested
    cash_pct = (cash / total_capital * 100) if total_capital > 0 else 0
    
    return {
        "allocations": allocations,
        "total_invested": round(total_invested, 2),
        "total_risk": round(total_risk, 2),
        "cash": round(cash, 2),
        "cash_pct": round(cash_pct, 2),
        "position_count": len(allocations),
        "timestamp": datetime.now().isoformat()
    }

def print_position_result(result: dict):
    """打印仓位计算结果"""
    
    print(f"\n{'='*60}")
    print(f"💰 仓位计算结果")
    print(f"{'='*60}")
    
    print(f"\n📊 基本信息:")
    print(f"  总资金：${result['total_capital']:,.2f}")
    print(f"  风险偏好：{result['risk_profile']}")
    print(f"  置信度：{result['confidence']}")
    
    print(f"\n💵 仓位详情:")
    print(f"  股数：{result['shares']} 股")
    print(f"  入场价：${result['entry_price']:.2f}")
    print(f"  止损价：${result['stop_loss_price']:.2f}")
    print(f"  仓位价值：${result['position_value']:,.2f}")
    print(f"  仓位占比：{result['position_pct']:.1f}%")
    
    print(f"\n⚠️ 风险控制:")
    print(f"  风险金额：${result['risk_amount']:,.2f}")
    print(f"  风险比例：{result['risk_pct']:.1f}%")
    print(f"  止损幅度：{result['stop_loss_pct']:.1f}%")
    
    # 风险收益比
    if result['risk_amount'] > 0:
        # 假设止盈位为入场价 + 2 倍风险
        take_profit = result['entry_price'] * (1 + result['stop_loss_pct'] / 100 * 2)
        potential_profit = (take_profit - result['entry_price']) * result['shares']
        risk_reward_ratio = potential_profit / result['risk_amount']
        
        print(f"\n🎯 风险收益比:")
        print(f"  止盈价：${take_profit:.2f}")
        print(f"  潜在收益：${potential_profit:,.2f}")
        print(f"  风险收益比：1:{risk_reward_ratio:.1f}")
    
    print(f"{'='*60}\n")

def print_portfolio_result(result: dict):
    """打印投资组合配置结果"""
    
    print(f"\n{'='*60}")
    print(f"📊 投资组合配置")
    print(f"{'='*60}")
    
    print(f"\n📈 持仓概览:")
    print(f"  持仓数量：{result['position_count']} 只")
    print(f"  总投资：${result['total_invested']:,.2f}")
    print(f"  总风险：${result['total_risk']:,.2f}")
    print(f"  现金：${result['cash']:,.2f} ({result['cash_pct']:.1f}%)")
    
    print(f"\n💼 详细配置:")
    print(f"  {'股票':<8} {'股数':>8} {'仓位价值':>12} {'仓位%':>8} {'风险$':>10}")
    print(f"  {'-'*50}")
    
    for alloc in result["allocations"]:
        print(f"  {alloc['symbol']:<8} {alloc['shares']:>8} ${alloc['position_value']:>10,.2f} {alloc['position_pct']:>7.1f}% ${alloc['risk_amount']:>8,.2f}")
    
    print(f"  {'-'*50}")
    print(f"  {'总计':<8} {'':>8} ${result['total_invested']:>10,.2f} {'':>8} ${result['total_risk']:>8,.2f}")
    
    print(f"{'='*60}\n")

if __name__ == "__main__":
    # 测试
    print("🔧 仓位计算器测试")
    print("=" * 60)
    
    # 测试 1: 单个股票仓位计算
    print("\n📝 测试 1: 单个股票仓位计算")
    
    test_cases = [
        {
            "name": "稳健型 + 中置信度",
            "capital": 100000,
            "entry": 175.64,
            "stop_loss": 165.00,
            "risk_profile": "moderate",
            "confidence": "medium"
        },
        {
            "name": "保守型 + 高置信度",
            "capital": 100000,
            "entry": 175.64,
            "stop_loss": 165.00,
            "risk_profile": "conservative",
            "confidence": "high"
        },
        {
            "name": "进取型 + 低置信度",
            "capital": 100000,
            "entry": 175.64,
            "stop_loss": 165.00,
            "risk_profile": "aggressive",
            "confidence": "low"
        }
    ]
    
    for test in test_cases:
        print(f"\n  测试：{test['name']}")
        result = calculate_position_size(
            total_capital=test["capital"],
            entry_price=test["entry"],
            stop_loss_price=test["stop_loss"],
            risk_profile=test["risk_profile"],
            confidence=test["confidence"]
        )
        print_position_result(result)
    
    # 测试 2: 投资组合配置
    print("\n📝 测试 2: 投资组合配置")
    
    positions = [
        {"symbol": "NVDA", "entry_price": 175.64, "stop_loss": 165.00, "confidence": "medium"},
        {"symbol": "AAPL", "entry_price": 251.49, "stop_loss": 240.00, "confidence": "high"},
        {"symbol": "SPY", "entry_price": 580.00, "stop_loss": 560.00, "confidence": "medium"},
        {"symbol": "TSLA", "entry_price": 350.00, "stop_loss": 320.00, "confidence": "low"}
    ]
    
    portfolio = calculate_portfolio_allocation(
        total_capital=100000,
        positions=positions,
        risk_profile="moderate"
    )
    
    print_portfolio_result(portfolio)
    
    print("✅ 测试完成！")
