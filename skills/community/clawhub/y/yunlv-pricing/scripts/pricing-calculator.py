#!/usr/bin/env python3
"""
云旅定价计算器 - Yunlv Pricing Calculator
FOB/CIF/CFR价格计算、同行定位分析、利润模拟

命令:
  fob   - 计算FOB价格
  cif   - 计算CIF价格
  cfr   - 计算CFR价格
  position - 同行定位分析
  simulate - 利润模拟
"""

import sys
import json
import argparse
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict

# ============ 数据模型 ============

@dataclass
class PriceCalculation:
    """价格计算结果"""
    base_cost: float      # 基础成本 (CNY)
    fob_price: float      # FOB价 (CNY)
    cif_price: float      # CIF价 (CNY)
    cfr_price: float      # CFR价 (CNY)
    exchange_rate: float  # 汇率
    profit_margin: float  # 利润率 %
    final_profit: float   # 最终利润 (CNY)

@dataclass
class CompetitorPosition:
    """同行定位分析"""
    your_price: float
    avg_market_price: float
    position_rank: str      # low/mid/high/leader
    price_gap_pct: float    # 价格差距百分比
    recommendation: str      # 建议

@dataclass
class ProfitSimulation:
    """利润模拟结果"""
    revenue: float
    total_cost: float
    export_rebate: float   # 出口退税
    net_profit: float
    profit_margin_pct: float
    roi: float             # 投资回报率
    break_even_price: float # 保本价格

# ============ 核心计算函数 ============

def calculate_fob(cost: float, profit_margin: float = 10.0) -> float:
    """计算FOB价格"""
    return cost * (1 + profit_margin / 100)

def calculate_cif(cost: float, freight: float, insurance: float = 0.0, profit_margin: float = 10.0) -> float:
    """计算CIF价格"""
    base_cost = cost + freight + insurance
    return base_cost * (1 + profit_margin / 100)

def calculate_cfr(cost: float, freight: float, profit_margin: float = 10.0) -> float:
    """计算CFR价格"""
    base_cost = cost + freight
    return base_cost * (1 + profit_margin / 100)

def analyze_competitor_position(your_price: float, market_prices: List[float]) -> Dict:
    """同行定位分析"""
    avg_price = sum(market_prices) / len(market_prices)
    min_price = min(market_prices)
    max_price = max(market_prices)
    gap_pct = ((your_price - avg_price) / avg_price) * 100
    
    if your_price <= min_price * 1.05:
        rank = "leader"
        recommendation = "您的价格具有较强竞争力，建议突出性价比优势"
    elif your_price <= avg_price:
        rank = "mid"
        recommendation = "价格处于中上水平，建议强调产品质量和服务的差异化"
    elif your_price <= max_price * 0.95:
        rank = "high"
        recommendation = "价格偏高，建议优化成本或强化产品价值主张"
    else:
        rank = "premium"
        recommendation = "高端定位，需确保产品和服务匹配高价格"
    
    return {
        "your_price": your_price,
        "avg_market_price": round(avg_price, 2),
        "min_market_price": min_price,
        "max_market_price": max_price,
        "position_rank": rank,
        "price_gap_pct": round(gap_pct, 2),
        "recommendation": recommendation
    }

def simulate_profit(
    cost: float,
    selling_price: float,
    exchange_rate: float,
    export_rebate_rate: float = 13.0,
    operation_cost: float = 0.0
) -> Dict:
    """利润模拟计算"""
    # 收入（转换为CNY）
    revenue = selling_price * exchange_rate
    # 总成本
    total_cost = cost + operation_cost
    # 出口退税（仅当成本不含税时适用，这里简化计算）
    rebate = cost * export_rebate_rate / 100
    # 净利润
    net_profit = revenue - total_cost + rebate
    # 利润率
    profit_margin = (net_profit / revenue * 100) if revenue > 0 else 0
    # ROI
    roi = (net_profit / total_cost * 100) if total_cost > 0 else 0
    # 保本价格
    break_even = (total_cost - rebate) / exchange_rate
    
    return {
        "revenue": round(revenue, 2),
        "total_cost": round(total_cost, 2),
        "export_rebate": round(rebate, 2),
        "net_profit": round(net_profit, 2),
        "profit_margin_pct": round(profit_margin, 2),
        "roi": round(roi, 2),
        "break_even_price": round(break_even, 2),
        "break_even_usd": round(break_even / exchange_rate, 4) if exchange_rate > 0 else 0
    }

# ============ 命令处理函数 ============

def cmd_fob(args) -> Dict:
    """FOB价格计算命令"""
    result = calculate_fob(args.cost, args.margin)
    return {
        "command": "fob",
        "input": {"cost": args.cost, "profit_margin": args.margin},
        "result": {
            "base_cost_cny": args.cost,
            "fob_price_cny": round(result, 2),
            "profit_amount_cny": round(result - args.cost, 2)
        }
    }

def cmd_cif(args) -> Dict:
    """CIF价格计算命令"""
    result = calculate_cif(args.cost, args.freight, args.insurance, args.margin)
    return {
        "command": "cif",
        "input": {
            "cost": args.cost,
            "freight": args.freight,
            "insurance": args.insurance,
            "profit_margin": args.margin
        },
        "result": {
            "base_cost_cny": args.cost,
            "freight_cny": args.freight,
            "insurance_cny": args.insurance,
            "cif_price_cny": round(result, 2),
            "cif_price_usd": round(result / args.exchange_rate, 2) if args.exchange_rate > 0 else 0
        }
    }

def cmd_cfr(args) -> Dict:
    """CFR价格计算命令"""
    result = calculate_cfr(args.cost, args.freight, args.margin)
    return {
        "command": "cfr",
        "input": {
            "cost": args.cost,
            "freight": args.freight,
            "profit_margin": args.margin
        },
        "result": {
            "base_cost_cny": args.cost,
            "freight_cny": args.freight,
            "cfr_price_cny": round(result, 2),
            "cfr_price_usd": round(result / args.exchange_rate, 2) if args.exchange_rate > 0 else 0
        }
    }

def cmd_position(args) -> Dict:
    """同行定位分析命令"""
    market_prices = [float(x) for x in args.prices.split(',')]
    result = analyze_competitor_position(float(args.your_price), market_prices)
    return {
        "command": "position",
        "input": {"your_price": args.your_price, "market_prices": market_prices},
        "result": result
    }

def cmd_simulate(args) -> Dict:
    """利润模拟命令"""
    result = simulate_profit(
        cost=args.cost,
        selling_price=args.selling_price,
        exchange_rate=args.exchange_rate,
        export_rebate_rate=args.rebate_rate,
        operation_cost=args.operation_cost
    )
    return {
        "command": "simulate",
        "input": {
            "cost": args.cost,
            "selling_price_usd": args.selling_price,
            "exchange_rate": args.exchange_rate,
            "export_rebate_rate": args.rebate_rate,
            "operation_cost": args.operation_cost
        },
        "result": result
    }

# ============ CLI 入口 ============

def main():
    parser = argparse.ArgumentParser(
        description="云旅定价计算器 - 出口报价与利润分析工具"
    )
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # FOB命令
    p_fob = subparsers.add_parser('fob', help='计算FOB价格')
    p_fob.add_argument('--cost', type=float, required=True, help='基础成本(CNY)')
    p_fob.add_argument('--margin', type=float, default=10.0, help='利润率(%%), 默认10')
    
    # CIF命令
    p_cif = subparsers.add_parser('cif', help='计算CIF价格')
    p_cif.add_argument('--cost', type=float, required=True, help='基础成本(CNY)')
    p_cif.add_argument('--freight', type=float, required=True, help='运费(CNY)')
    p_cif.add_argument('--insurance', type=float, default=0.0, help='保险费(CNY)')
    p_cif.add_argument('--margin', type=float, default=10.0, help='利润率(%%), 默认10')
    p_cif.add_argument('--exchange-rate', type=float, default=7.2, help='汇率, 默认7.2')
    
    # CFR命令
    p_cfr = subparsers.add_parser('cfr', help='计算CFR价格')
    p_cfr.add_argument('--cost', type=float, required=True, help='基础成本(CNY)')
    p_cfr.add_argument('--freight', type=float, required=True, help='运费(CNY)')
    p_cfr.add_argument('--margin', type=float, default=10.0, help='利润率(%%), 默认10')
    p_cfr.add_argument('--exchange-rate', type=float, default=7.2, help='汇率, 默认7.2')
    
    # Position命令
    p_pos = subparsers.add_parser('position', help='同行定位分析')
    p_pos.add_argument('--your-price', required=True, help='您的价格')
    p_pos.add_argument('--prices', required=True, help='同行价格(逗号分隔)')
    
    # Simulate命令
    p_sim = subparsers.add_parser('simulate', help='利润模拟')
    p_sim.add_argument('--cost', type=float, required=True, help='总成本(CNY)')
    p_sim.add_argument('--selling-price', type=float, required=True, help='售价(USD)')
    p_sim.add_argument('--exchange-rate', type=float, default=7.2, help='汇率, 默认7.2')
    p_sim.add_argument('--rebate-rate', type=float, default=13.0, help='退税率(%%), 默认13')
    p_sim.add_argument('--operation-cost', type=float, default=0.0, help='运营成本(CNY)')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # 根据命令执行
    if args.command == 'fob':
        result = cmd_fob(args)
    elif args.command == 'cif':
        result = cmd_cif(args)
    elif args.command == 'cfr':
        result = cmd_cfr(args)
    elif args.command == 'position':
        result = cmd_position(args)
    elif args.command == 'simulate':
        result = cmd_simulate(args)
    else:
        print(f"未知命令: {args.command}")
        return
    
    # 输出结果
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
