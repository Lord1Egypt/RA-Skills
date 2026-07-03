#!/usr/bin/env python3
"""
Shanv Trader - 持仓实时监控
监控持仓盈亏、预警、风控
"""

import sys
import json
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path.home() / '.openclaw/workspace'))

# 大王铁律配置
RISK_CONFIG = {
    'stop_loss_pct': 0.08,      # 8% 强制止损
    'break_even_buffer': 0.02,  # 距成本2%预警
    'max_single_position': 0.2, # 单股最大20%仓位
    'max_total_positions': 10,  # 最大持仓数
}

def load_holdings():
    """加载当前持仓 - 从 holdings_latest.json"""
    holdings_file = Path.home() / '.openclaw/workspace/data/holdings_latest.json'
    if not holdings_file.exists():
        return []
    
    with open(holdings_file) as f:
        data = json.load(f)
    
    # 转换中文键名为英文，方便后续处理
    holdings = []
    for h in data.get('holdings', []):
        holdings.append({
            'code': h.get('代码', ''),
            'name': h.get('名称', ''),
            'quantity': h.get('股数', 0),
            'available': h.get('可用', 0),
            'cost': h.get('成本', 0),
            'price': h.get('现价', 0),
            'value': h.get('市值', 0),
            'pl': h.get('盈亏', 0),
            'pl_pct': h.get('盈亏%', 0)
        })
    
    return {
        'holdings': holdings,
        'total_cost': data.get('total_cost', 0),
        'total_value': data.get('total_value', 0),
        'total_pl': data.get('total_pl', 0),
        'total_pl_pct': data.get('total_pl_pct', 0),
        'account': data.get('account', '')
    }

def get_realtime_prices(codes):
    """获取实时价格"""
    # 调用 stock_price 或 unified_stock
    import subprocess
    code_str = ' '.join(codes)
    result = subprocess.run(
        f'cd ~/.openclaw/workspace && python3 bin/stock_price {code_str}',
        shell=True,
        capture_output=True,
        text=True
    )
    return parse_price_output(result.stdout)

def parse_price_output(output):
    """解析价格输出"""
    prices = {}
    # 简化实现
    return prices

def check_stop_loss(holding, current_price):
    """检查止损"""
    cost = holding.get('cost', 0)
    if cost == 0:
        return None
    
    loss_pct = (current_price - cost) / cost
    
    if loss_pct <= -RISK_CONFIG['stop_loss_pct']:
        return {
            'level': 'critical',
            'icon': '🚨',
            'message': f"已跌破止损线(-{RISK_CONFIG['stop_loss_pct']*100:.0f}%)，建议立即平仓",
            'action': 'sell'
        }
    
    if loss_pct <= -RISK_CONFIG['break_even_buffer']:
        return {
            'level': 'warning',
            'icon': '⚠️',
            'message': f"亏损{abs(loss_pct)*100:.1f}%，接近止损线",
            'action': 'watch'
        }
    
    return None

def check_break_even(holding, current_price):
    """检查保本线"""
    cost = holding.get('cost', 0)
    if cost == 0:
        return None
    
    # 从盈利转为亏损或接近成本
    profit_pct = (current_price - cost) / cost
    
    if profit_pct > 0 and profit_pct <= RISK_CONFIG['break_even_buffer']:
        return {
            'level': 'warning',
            'icon': '🚨',
            'message': f"盈利回撤至+{profit_pct*100:.1f}%，接近成本线，建议保本平仓",
            'action': 'sell'
        }
    
    return None

def format_position_card(holding, current_price, alerts):
    """格式化持仓卡片"""
    name = holding.get('name', '')
    code = holding.get('code', '')
    cost = holding.get('cost', 0)
    quantity = holding.get('quantity', 0)
    
    # 使用传入的current_price或holding中的price
    price = current_price if current_price > 0 else holding.get('price', 0)
    
    profit = (price - cost) * quantity
    profit_pct = (price - cost) / cost * 100 if cost > 0 else 0
    
    emoji = '🟢' if profit > 0 else '🔴' if profit < 0 else '⚪'
    
    card = f"""
{emoji} {name} ({code})
   成本: ¥{cost:.2f} × {quantity}股
   现价: ¥{price:.2f}
   盈亏: ¥{profit:,.2f} ({profit_pct:+.2f}%)"""
    
    for alert in alerts:
        card += f"\n   {alert['icon']} {alert['message']}"
    
    return card

def main():
    """主函数"""
    print("📊 Shanv Trader - 持仓实时监控")
    print("=" * 50)
    print(f"⏰ {datetime.now().strftime('%H:%M:%S')}")
    print()
    
    # 加载持仓
    data = load_holdings()
    holdings = data.get('holdings', [])
    
    if not holdings:
        print("⚠️ 暂无持仓")
        return
    
    print(f"📈 持仓 {len(holdings)} 只，账户: {data.get('account', '')}")
    print(f"💰 总市值: ¥{data.get('total_value', 0):,.2f}")
    print(f"📉 总盈亏: ¥{data.get('total_pl', 0):,.2f} ({data.get('total_pl_pct', 0):.2f}%)")
    print()
    
    # 获取实时价格 (简化：使用持仓中的现价)
    # 实际可调用 stock_price 更新
    
    # 检查每只持仓
    critical_alerts = []
    warning_alerts = []
    
    for holding in holdings:
        code = holding['code']
        current_price = holding.get('price', 0)
        
        # 风控检查
        alerts = []
        
        stop_loss = check_stop_loss(holding, current_price)
        if stop_loss:
            alerts.append(stop_loss)
            if stop_loss['level'] == 'critical':
                critical_alerts.append((holding, stop_loss))
            else:
                warning_alerts.append((holding, stop_loss))
        
        break_even = check_break_even(holding, current_price)
        if break_even:
            alerts.append(break_even)
            if (holding, break_even) not in warning_alerts:
                warning_alerts.append((holding, break_even))
        
        # 显示持仓卡片
        print(format_position_card(holding, current_price, alerts))
    
    # 汇总
    print(f"\n{'='*50}")
    
    # 预警汇总
    if critical_alerts:
        print(f"\n🚨 紧急预警 ({len(critical_alerts)}条):")
        for holding, alert in critical_alerts:
            print(f"   • {holding['name']}({holding['code']}): {alert['message']}")
            print(f"     回复【卖出 {holding['code']}】执行平仓")
    
    if warning_alerts:
        print(f"\n⚠️ 提醒 ({len(warning_alerts)}条):")
        for holding, alert in warning_alerts:
            print(f"   • {holding['name']}({holding['code']}): {alert['message']}")
    
    if not critical_alerts and not warning_alerts:
        print("\n✅ 所有持仓正常，无风险预警")

if __name__ == '__main__':
    main()
