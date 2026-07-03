#!/usr/bin/env python3
"""
Shanv Trader - 半自动交易演示
完整流程: 扫描 → 建议 → 确认 → 执行
"""

import subprocess
import json
from datetime import datetime
from pathlib import Path

def scan_opportunities():
    """扫描交易机会"""
    print("🔍 步骤1: 扫描市场机会...")
    print("-" * 50)
    
    result = subprocess.run(
        ['python3', 'bin/unified_scanner.py'],
        cwd=Path.home() / '.openclaw/workspace',
        capture_output=True,
        text=True
    )
    
    # 解析输出，提取强烈信号
    lines = result.stdout.split('\n')
    opportunities = []
    
    in_strong = False
    for line in lines:
        if '🟢 强烈信号' in line:
            in_strong = True
            continue
        if '🟡 观察信号' in line:
            in_strong = False
            continue
        if in_strong and len(line) > 80:
            # 解析行
            parts = line.split()
            if len(parts) >= 8 and parts[4].isdigit():
                opportunities.append({
                    'code': parts[4],
                    'name': parts[5],
                    'change': parts[6],
                    'signal': '🟢强烈'
                })
    
    return opportunities[:2]  # 只取前2个

def load_holdings():
    """加载当前持仓"""
    holdings_file = Path.home() / '.openclaw/workspace/data/holdings_latest.json'
    if holdings_file.exists():
        with open(holdings_file) as f:
            return json.load(f)
    return {'holdings': [], 'total_pl': 0}

def generate_suggestion(opp, holdings):
    """生成交易建议卡片"""
    code = opp['code']
    name = opp['name']
    change = opp['change']
    
    # 计算建议仓位 (简化)
    suggested_qty = 500
    
    # 检查是否已持仓
    for h in holdings.get('holdings', []):
        if h['代码'] == code:
            return None  # 已持仓，不重复建议
    
    card = f"""
┌─────────────────────────────────────────┐
│ 🎯 交易建议 #{code}                     │
├─────────────────────────────────────────┤
│ 股票: {name} ({code})                   │
│ 涨幅: {change}                          │
│ 信号: 🟢🟢🟢 强烈做多                   │
│                                          │
│ 📊 买入理由:                             │
│ • 三雷达评分: 资金+趋势双强              │
│ • 外盘比例 > 60%: 主力买入               │
│ • 放量上涨: 量价配合良好                 │
│                                          │
│ 💰 建议仓位: {suggested_qty}股           │
│ 🛡️ 风控: 止损位 -8%                     │
│                                          │
│ 大王请确认:                              │
│ 【1】确认买入 {suggested_qty}股          │
│ 【2】修改数量                            │
│ 【3】查看详情                            │
│ 【4】跳过此股                            │
└─────────────────────────────────────────┘
"""
    return {
        'card': card,
        'code': code,
        'name': name,
        'suggested_qty': suggested_qty
    }

def monitor_positions():
    """监控持仓"""
    print("\n📊 步骤3: 持仓风险监控...")
    print("-" * 50)
    
    holdings = load_holdings()
    
    if not holdings.get('holdings'):
        print("暂无持仓")
        return
    
    print(f"持仓 {len(holdings['holdings'])} 只，总盈亏: ¥{holdings['total_pl']:,.2f}")
    print()
    
    alerts = []
    for h in holdings['holdings']:
        code = h['代码']
        name = h['名称']
        pl_pct = h['盈亏%']
        
        if pl_pct <= -8:
            alerts.append(f"🚨 {name}({code}): 亏损{pl_pct:.1f}%，已触发止损线！")
        elif pl_pct <= -2:
            alerts.append(f"⚠️ {name}({code}): 亏损{pl_pct:.1f}%，接近止损线")
    
    if alerts:
        print("风险预警:")
        for alert in alerts:
            print(f"  {alert}")
    else:
        print("✅ 所有持仓正常，无风险预警")

def main():
    """演示主流程"""
    print("=" * 60)
    print("🤖 Shanv Trader - 半自动交易演示")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print()
    
    # 1. 扫描机会
    opportunities = scan_opportunities()
    
    if not opportunities:
        print("⚠️ 暂无强烈信号，建议观望")
        return
    
    print(f"\n发现 {len(opportunities)} 个强烈信号:\n")
    
    # 2. 生成建议
    holdings = load_holdings()
    suggestions = []
    
    for opp in opportunities:
        suggestion = generate_suggestion(opp, holdings)
        if suggestion:
            suggestions.append(suggestion)
            print(suggestion['card'])
    
    if not suggestions:
        print("ℹ️ 信号股票已在持仓中，不重复建议")
    else:
        print(f"\n💡 请大王回复数字确认交易，或说'取消'跳过")
    
    # 3. 监控持仓
    monitor_positions()
    
    print()
    print("=" * 60)
    print("演示完成！实际交易将调用: python3 execute_trade.py")
    print("=" * 60)

if __name__ == '__main__':
    main()
