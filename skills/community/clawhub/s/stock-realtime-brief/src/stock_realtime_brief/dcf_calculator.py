#!/usr/bin/env python3
"""
DCF 内在价值 计算器 v1.0
基于 巴菲特 / 段永平 / 林奇 思想

核心: 区分 "好公司" 和 "好股票"
  好公司 = 强护城河 + 高 ROE + 真业绩
  好股票 = 好公司 + 好价格 (现价 < 内在价值 + 安全边际)

适用:
  ✅ 转型期 公司 (罗博 / 中天)
  ✅ 业绩 高增 公司 (华工 / 药明)
  ⚠️ 不适用 周期股 / 强波动 (天岳 SiC)
  ❌ 不适用 业绩持续亏损 / 无现金流公司

用法:
  python3 dcf_calculator.py
  python3 dcf_calculator.py --stock 600522 (中天) --custom
"""

import argparse
import json
import sys
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class DCFInput:
    """DCF 输入 参数"""
    name: str
    code: str
    current_price: float            # 当前股价
    total_shares: float             # 总股本 (亿股)
    
    # 基础数据
    last_year_revenue: float        # 上一年 营收 (亿元)
    last_year_net_profit: float     # 上一年 净利润 (亿元)
    last_year_fcf: Optional[float] = None  # 上一年 自由现金流 (亿元 / 没有用净利润代替)
    
    # 增长 预测
    growth_rate_1_5: float = 0.20   # 1-5 年 增长率 (默认 20%)
    growth_rate_6_10: float = 0.10  # 6-10 年 增长率 (默认 10%)
    terminal_growth: float = 0.03   # 永续增长率 (默认 3% / GDP)
    
    # 折现率
    discount_rate: float = 0.10     # 默认 10% (巴菲特 用 15%)
    
    # 安全边际 要求
    safety_margin: float = 0.30     # 默认 要求 30% 折扣
    
    def __post_init__(self):
        # 如果 没提供 自由现金流 / 用 净利润 * 0.85 估算
        if self.last_year_fcf is None:
            self.last_year_fcf = self.last_year_net_profit * 0.85


def calculate_dcf(inp: DCFInput) -> dict:
    """
    DCF 计算 - 三阶段 模型
    
    阶段 1: 1-5 年 高增长
    阶段 2: 6-10 年 中增长
    阶段 3: 11 年+ 永续 增长
    """
    # 阶段 1+2: 预测 10 年 现金流
    cash_flows = []
    current_fcf = inp.last_year_fcf
    
    # 1-5 年 高增长
    for year in range(1, 6):
        current_fcf = current_fcf * (1 + inp.growth_rate_1_5)
        cash_flows.append(current_fcf)
    
    # 6-10 年 中增长
    for year in range(6, 11):
        current_fcf = current_fcf * (1 + inp.growth_rate_6_10)
        cash_flows.append(current_fcf)
    
    # 阶段 3: 永续价值 (终值)
    terminal_value = (
        cash_flows[-1] * (1 + inp.terminal_growth) 
        / (inp.discount_rate - inp.terminal_growth)
    )
    
    # 折现 所有 现金流 到 现在
    discounted_cf = []
    for year, cf in enumerate(cash_flows, start=1):
        discount_factor = (1 + inp.discount_rate) ** year
        discounted_cf.append(cf / discount_factor)
    
    # 终值 也要 折现
    discounted_terminal = terminal_value / ((1 + inp.discount_rate) ** 10)
    
    # 总 内在价值 (亿元)
    total_intrinsic = sum(discounted_cf) + discounted_terminal
    
    # 每股 内在价值
    intrinsic_per_share = total_intrinsic / inp.total_shares
    
    # 安全 买入价
    safe_buy_price = intrinsic_per_share * (1 - inp.safety_margin)
    
    # 当前 安全边际 (现价 vs 内在价值)
    margin_now = (intrinsic_per_share - inp.current_price) / intrinsic_per_share
    
    # 评级
    if margin_now >= 0.5:
        rating = "🌟🌟🌟🌟🌟 极品 (严重低估 50%+)"
    elif margin_now >= 0.3:
        rating = "🌟🌟🌟🌟 优秀 (低估 30-50%)"
    elif margin_now >= 0.0:
        rating = "🌟🌟🌟 合理 (低估 0-30%)"
    elif margin_now >= -0.2:
        rating = "🟡 中性 (高估 0-20%)"
    elif margin_now >= -0.5:
        rating = "🔴 高估 (20-50%)"
    else:
        rating = "🚨 严重高估 (>50%)"
    
    return {
        'name': inp.name,
        'code': inp.code,
        'current_price': inp.current_price,
        'intrinsic_per_share': intrinsic_per_share,
        'safe_buy_price': safe_buy_price,
        'safety_margin_pct': margin_now * 100,
        'rating': rating,
        'total_intrinsic_yi': total_intrinsic,
        'cash_flows_5yr': cash_flows[:5],
        'cash_flows_10yr': cash_flows,
        'terminal_value': terminal_value,
        'discounted_cf_sum': sum(discounted_cf),
        'discounted_terminal': discounted_terminal,
        'inputs': {
            'last_fcf': inp.last_year_fcf,
            'g1_5': f"{inp.growth_rate_1_5*100:.1f}%",
            'g6_10': f"{inp.growth_rate_6_10*100:.1f}%",
            'terminal_g': f"{inp.terminal_growth*100:.1f}%",
            'discount': f"{inp.discount_rate*100:.1f}%",
            'safety_required': f"{inp.safety_margin*100:.1f}%",
        }
    }


def format_report(result: dict) -> str:
    """格式化 DCF 报告"""
    r = result
    inp = r['inputs']
    
    margin = r['safety_margin_pct']
    margin_str = f"+{margin:.1f}%" if margin > 0 else f"{margin:.1f}%"
    
    report = f"""
╔══════════════════════════════════════════════════════════╗
║  💰 DCF 内在价值 计算 - {r['name']} ({r['code']})
╚══════════════════════════════════════════════════════════╝

📊 当前 估值:
  • 现价:         ¥{r['current_price']:.2f}
  • 内在价值:     ¥{r['intrinsic_per_share']:.2f} / 股
  • 安全买入价:   ¥{r['safe_buy_price']:.2f} (要求 {inp['safety_required']} 安全边际)
  • 当前 安全边际: {margin_str}

🎯 评级: {r['rating']}

📈 输入 假设:
  • 上一年 FCF:    ¥{inp['last_fcf']:.2f} 亿
  • 1-5 年 增速:   {inp['g1_5']}
  • 6-10 年 增速:  {inp['g6_10']}
  • 永续增速:      {inp['terminal_g']}
  • 折现率:        {inp['discount']}

🔍 计算 明细:
  • 1-10 年 折现 现金流 合计:  ¥{r['discounted_cf_sum']:.1f} 亿
  • 终值 (折现后):             ¥{r['discounted_terminal']:.1f} 亿
  • 总 内在价值:               ¥{r['total_intrinsic_yi']:.1f} 亿

📉 10 年 预测 自由现金流 (亿元):
"""
    for i, cf in enumerate(r['cash_flows_10yr'], 1):
        marker = '⭐' if i <= 5 else ' '
        report += f"  Year {i:>2}: ¥{cf:>8.2f} 亿 {marker}\n"
    
    report += f"\n  Year 终值: ¥{r['terminal_value']:>8.1f} 亿 (永续)\n"
    
    report += """
💎 决策 建议:
"""
    if margin >= 30:
        report += "  ✅ 当前 估值 极有 吸引力 / 可重仓 (单股 ≤ 30%)\n"
        report += "  ✅ 满足 巴菲特 / 段永平 安全边际 要求\n"
    elif margin >= 0:
        report += "  🟢 当前 估值 合理 / 可建仓 (单股 ≤ 20%)\n"
        report += f"  💡 等回调 到 ¥{r['safe_buy_price']:.2f} 时 重仓\n"
    elif margin >= -20:
        report += "  🟡 当前 估值 偏高 / 不建议 加仓\n"
        report += f"  💡 等回调 到 ¥{r['intrinsic_per_share']:.2f} 以下\n"
    else:
        report += "  🚨 当前 估值 严重高估 / 持有 可 / 不建议 新进\n"
        report += "  🚨 不要 因为 涨势 追涨\n"
    
    return report


# ============ 预设案例 (你的持仓) ============

PRESETS = {
    '中天科技': DCFInput(
        name='中天科技', code='600522',
        current_price=68.10,
        total_shares=34.13,  # 总股本 34 亿股
        last_year_revenue=485,  # 2025 营收估
        last_year_net_profit=32,  # 2025 净利润估
        growth_rate_1_5=0.25,  # AI算力+海缆 高增
        growth_rate_6_10=0.12,
        discount_rate=0.10,
    ),
    '华工科技': DCFInput(
        name='华工科技', code='000988',
        current_price=173.58,
        total_shares=10.0,
        last_year_revenue=170,  # 2025 营收估 +44%
        last_year_net_profit=18,  # 2025 净利估
        growth_rate_1_5=0.30,  # CPO 主升
        growth_rate_6_10=0.15,
        discount_rate=0.10,
    ),
    '罗博特科': DCFInput(
        name='罗博特科', code='300757',
        current_price=647.00,
        total_shares=1.5,
        last_year_revenue=11,  # 2025 营收 (光伏拖累)
        last_year_net_profit=2,  # 业务转型期 / 预期 业绩拐点
        growth_rate_1_5=0.80,  # 业务转型 + 英伟达 + ¥11亿在手订单 / 高增预期
        growth_rate_6_10=0.30,
        discount_rate=0.12,  # 转型期 风险 / 折现率高
    ),
    '天岳先进': DCFInput(
        name='天岳先进', code='688234',
        current_price=172.28,
        total_shares=4.3,
        last_year_revenue=15,
        last_year_net_profit=1.5,  # 行业周期 + 初步盈利
        growth_rate_1_5=0.50,  # SiC 主升
        growth_rate_6_10=0.20,
        discount_rate=0.12,  # 周期股 折现率高
    ),
    '药明康德': DCFInput(
        name='药明康德', code='603259',
        current_price=118.18,
        total_shares=29.0,
        last_year_revenue=440,  # 2025 营收
        last_year_net_profit=100,  # 2025 净利润估
        growth_rate_1_5=0.20,
        growth_rate_6_10=0.10,
        discount_rate=0.12,  # 美国 政治风险 高 / 折现率高
    ),
}


def main():
    parser = argparse.ArgumentParser(description='DCF 内在价值 计算器 v1.0')
    parser.add_argument('--stock', help='预设股票代码 (中天/华工/罗博/天岳/药明)')
    parser.add_argument('--all', action='store_true', help='计算所有 预设股票')
    args = parser.parse_args()
    
    if args.all or not args.stock:
        print("🌟 你 4 只持仓 + watchlist DCF 完整分析\n")
        results = []
        for name, inp in PRESETS.items():
            result = calculate_dcf(inp)
            results.append(result)
            print(format_report(result))
            print()
        
        # 汇总
        print("\n" + "=" * 60)
        print("📊 DCF 汇总 对比")
        print("=" * 60)
        print(f"{'股票':<10s} {'现价':>8s} {'内在价值':>10s} {'安全买入':>10s} {'当前边际':>10s} 评级")
        print("-" * 70)
        for r in results:
            margin_str = f"{r['safety_margin_pct']:+.1f}%"
            short_rating = r['rating'].split(' ')[0]  # 仅 取 emoji
            print(f"  {r['name']:<8s} ¥{r['current_price']:>5.2f}  ¥{r['intrinsic_per_share']:>7.2f}  ¥{r['safe_buy_price']:>7.2f}  {margin_str:>9s}  {short_rating}")
    
    elif args.stock in PRESETS:
        result = calculate_dcf(PRESETS[args.stock])
        print(format_report(result))
    else:
        print(f"❌ 未知股票: {args.stock}")
        print(f"可选: {', '.join(PRESETS.keys())}")
        sys.exit(1)


if __name__ == '__main__':
    main()
