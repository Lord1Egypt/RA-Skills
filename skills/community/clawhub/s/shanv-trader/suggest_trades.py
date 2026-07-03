#!/usr/bin/env python3
"""
Shanv Trader - 交易建议生成器
生成买入建议，等待大王确认
"""

import sys
import json
from datetime import datetime
from pathlib import Path

# 添加workspace到路径
sys.path.insert(0, str(Path.home() / '.openclaw/workspace'))

def load_portfolio():
    """加载当前持仓 - 从 holdings_latest.json"""
    holdings_file = Path.home() / '.openclaw/workspace/data/holdings_latest.json'
    if holdings_file.exists():
        with open(holdings_file) as f:
            data = json.load(f)
        return {
            'holdings': data.get('holdings', []),
            'cash': 0,  # 可用资金需要从平安证券获取
            'total_value': data.get('total_value', 0),
            'total_pl': data.get('total_pl', 0)
        }
    return {'holdings': [], 'cash': 0, 'total_value': 0, 'total_pl': 0}

def scan_chip_sector():
    """扫描芯片板块机会"""
    # 调用 unified_scanner.py --chip --top 5
    import subprocess
    result = subprocess.run(
        ['python3', 'scripts/unified_scanner.py', '--chip', '--top', '5'],
        cwd=Path.home() / '.openclaw/workspace',
        capture_output=True,
        text=True
    )
    return parse_scanner_output(result.stdout)

def parse_scanner_output(output):
    """解析扫描器输出"""
    # 简化实现
    return []

def calculate_position(signal_strength, price, cash_available):
    """计算建议仓位"""
    # 基础仓位
    base_position = 500  # 股
    
    # 根据信号强度调整
    multiplier = {
        '🟢强烈': 1.5,
        '🟡关注': 1.0,
        '⚪中性': 0.5,
        '🔴危险': 0
    }.get(signal_strength, 1.0)
    
    # 根据资金调整
    max_position_value = cash_available * 0.1  # 单股最多10%资金
    suggested_value = price * base_position * multiplier
    
    if suggested_value > max_position_value:
        return int(max_position_value / price / 100) * 100  # 取整百
    return int(base_position * multiplier / 100) * 100

def generate_trade_suggestion(stock_code, stock_name, signal_data):
    """生成交易建议卡片"""
    
    suggestion = {
        'timestamp': datetime.now().isoformat(),
        'stock_code': stock_code,
        'stock_name': stock_name,
        'current_price': signal_data.get('price', 0),
        'change_pct': signal_data.get('change', 0),
        'signal_strength': signal_data.get('signal', '⚪中性'),
        'reasons': signal_data.get('reasons', []),
        'suggested_quantity': signal_data.get('suggested_qty', 500),
        'suggested_value': 0,  # 计算
        'stop_loss': 0,  # 计算
        'risk_level': 'low',
        'status': 'pending',  # pending/confirmed/rejected
    }
    
    return suggestion

def format_suggestion_card(suggestion):
    """格式化交易建议卡片"""
    
    card = f"""
┌─────────────────────────────────────┐
│ 🎯 交易建议                           │
├─────────────────────────────────────┤
│ {suggestion['stock_name']}  {suggestion['stock_code']}
│ 现价: ¥{suggestion['current_price']:.2f}  ({suggestion['change_pct']:+.2f}%)
│ 信号强度: {suggestion['signal_strength']}
│                                      │
│ 📊 买入理由:"""
    
    for reason in suggestion['reasons'][:3]:
        card += f"\n│ • {reason}"
    
    card += f"""
│                                      │
│ 💰 建议仓位: {suggestion['suggested_quantity']}股
│ 🛡️ 风控: 止损位 ¥{suggestion['stop_loss']:.2f}
│                                      │
│ 回复: 【确认买入】或【取消】或【改数量:300】
└─────────────────────────────────────┘
"""
    return card

def main():
    """主函数"""
    print("🤖 Shanv Trader - 交易建议生成器")
    print("=" * 50)
    
    # 1. 加载持仓和资金
    portfolio = load_portfolio()
    print(f"💰 可用资金: ¥{portfolio['cash']:,.2f}")
    print(f"📊 当前持仓: {len(portfolio['holdings'])} 只")
    
    # 2. 扫描机会
    print("\n🔍 扫描芯片板块机会...")
    opportunities = scan_chip_sector()
    
    if not opportunities:
        print("⚠️ 暂无强烈信号，建议观望")
        return
    
    # 3. 生成建议
    print(f"\n🎯 发现 {len(opportunities)} 个机会:\n")
    
    suggestions = []
    for opp in opportunities[:3]:  # 只取TOP3
        suggestion = generate_trade_suggestion(
            opp['code'],
            opp['name'],
            opp
        )
        suggestions.append(suggestion)
        print(format_suggestion_card(suggestion))
    
    # 4. 保存建议到文件
    suggestions_file = Path(__file__).parent / 'data' / 'pending_suggestions.json'
    suggestions_file.parent.mkdir(exist_ok=True)
    with open(suggestions_file, 'w') as f:
        json.dump(suggestions, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 建议已保存，等待大王确认...")
    print(f"📁 文件: {suggestions_file}")

if __name__ == '__main__':
    main()
