#!/usr/bin/env python3
"""
持仓管理脚本
支持添加/修改/删除持仓，计算收益，设置预警
"""

import sys
import os
import json
import argparse
from datetime import datetime
from pathlib import Path

# 数据目录
DATA_DIR = Path(__file__).parent.parent / 'data'
HOLDINGS_FILE = DATA_DIR / 'holdings.json'
ALERTS_FILE = DATA_DIR / 'alerts.json'

# 确保数据目录存在
DATA_DIR.mkdir(parents=True, exist_ok=True)


def load_json(filepath, default=None):
    """加载 JSON 文件"""
    if default is None:
        default = {}
    try:
        if filepath.exists():
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
    except (json.JSONDecodeError, IOError):
        pass
    return default


def save_json(filepath, data):
    """保存 JSON 文件"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_holdings():
    """加载持仓数据"""
    return load_json(HOLDINGS_FILE, {'holdings': []})


def save_holdings(data):
    """保存持仓数据"""
    save_json(HOLDINGS_FILE, data)


def load_alerts():
    """加载预警数据"""
    return load_json(ALERTS_FILE, {'alerts': []})


def save_alerts(data):
    """保存预警数据"""
    save_json(ALERTS_FILE, data)


def add_holding(symbol, price, shares, name=None):
    """添加持仓记录"""
    data = load_holdings()
    
    # 检查是否已存在同一股票的持仓
    existing = None
    for h in data['holdings']:
        if h['symbol'].upper() == symbol.upper():
            existing = h
            break
    
    if existing:
        # 加仓：计算平均成本
        old_shares = existing['shares']
        old_price = existing['avg_price']
        new_shares = shares
        
        total_cost = old_price * old_shares + price * new_shares
        total_shares = old_shares + new_shares
        avg_price = total_cost / total_shares if total_shares > 0 else 0
        
        existing['avg_price'] = round(avg_price, 4)
        existing['shares'] = total_shares
        existing['last_updated'] = datetime.now().isoformat()
        if name:
            existing['name'] = name
        
        msg = f"✅ 加仓 {name or symbol}: {new_shares} 股 @ ¥{price:.2f}"
        msg += f"\n   新持仓：{total_shares} 股，平均成本 ¥{avg_price:.4f}"
    else:
        # 新建持仓
        holding = {
            'symbol': symbol.upper(),
            'name': name or symbol,
            'shares': shares,
            'avg_price': price,
            'created_at': datetime.now().isoformat(),
            'last_updated': datetime.now().isoformat()
        }
        data['holdings'].append(holding)
        
        msg = f"✅ 新建持仓 {name or symbol}: {shares} 股 @ ¥{price:.2f}"
    
    save_holdings(data)
    return msg


def remove_holding(symbol):
    """删除持仓记录"""
    data = load_holdings()
    symbol = symbol.upper()
    
    for i, h in enumerate(data['holdings']):
        if h['symbol'] == symbol:
            removed = data['holdings'].pop(i)
            save_holdings(data)
            return f"✅ 已删除持仓：{removed['name']} ({removed['symbol']})"
    
    return f"❌ 未找到持仓：{symbol}"


def list_holdings():
    """列出所有持仓"""
    data = load_holdings()
    
    if not data['holdings']:
        return "📭 暂无持仓记录"
    
    lines = ["## 📊 持仓列表\n"]
    lines.append("| 股票 | 名称 | 持仓 | 成本价 | 更新日期 |")
    lines.append("|------|------|------|--------|----------|")
    
    for h in data['holdings']:
        date = h['last_updated'][:10] if 'last_updated' in h else '-'
        lines.append(f"| {h['symbol']} | {h['name']} | {h['shares']} | ¥{h['avg_price']:.4f} | {date} |")
    
    return "\n".join(lines)


def calculate_summary():
    """计算持仓汇总（需要获取实时股价）"""
    data = load_holdings()
    
    if not data['holdings']:
        return "📭 暂无持仓记录"
    
    # 导入行情查询
    sys.path.insert(0, str(Path(__file__).parent))
    from stock_fetch import fetch_stock_price
    
    lines = ["## 💼 持仓收益汇总\n"]
    lines.append("| 股票 | 持仓 | 成本价 | 现价 | 市值 | 盈亏 | 盈亏率 |")
    lines.append("|------|------|--------|------|------|------|--------|")
    
    total_cost = 0
    total_value = 0
    
    for h in data['holdings']:
        # 获取实时股价
        price_data = fetch_stock_price(h['symbol'])
        
        if 'error' in price_data:
            current = h['avg_price']  # 使用成本价作为占位
            change_str = "数据获取失败"
        else:
            current = price_data['current']
            change_str = f"{price_data['change']:+.2f} ({price_data['change_pct']:+.2f}%)"
        
        cost = h['avg_price'] * h['shares']
        value = current * h['shares']
        profit = value - cost
        profit_pct = (profit / cost * 100) if cost > 0 else 0
        
        total_cost += cost
        total_value += value
        
        # 颜色符号
        if profit > 0:
            symbol = "📈"
        elif profit < 0:
            symbol = "📉"
        else:
            symbol = "➖"
        
        lines.append(f"| {h['symbol']} | {h['shares']} | ¥{h['avg_price']:.2f} | ¥{current:.2f} | ¥{value:,.0f} | {symbol}¥{profit:,.0f} | {profit_pct:+.2f}% |")
    
    # 汇总行
    total_profit = total_value - total_cost
    total_profit_pct = (total_profit / total_cost * 100) if total_cost > 0 else 0
    
    lines.append("")
    lines.append(f"**总投入**: ¥{total_cost:,.0f}  |  **总市值**: ¥{total_value:,.0f}  |  **总盈亏**: {'📈' if total_profit > 0 else '📉' if total_profit < 0 else '➖'}¥{total_profit:,.0f} ({total_profit_pct:+.2f}%)")
    
    return "\n".join(lines)


def set_alert(symbol, target_price=None, change_pct=None):
    """设置价格预警"""
    data = load_alerts()
    symbol = symbol.upper()
    
    alert = {
        'symbol': symbol,
        'target_price': target_price,
        'change_pct': change_pct,
        'created_at': datetime.now().isoformat()
    }
    
    # 检查是否已存在
    existing_idx = None
    for i, a in enumerate(data['alerts']):
        if a['symbol'] == symbol:
            existing_idx = i
            break
    
    if existing_idx is not None:
        data['alerts'][existing_idx] = alert
        msg = f"✅ 更新预警：{symbol}"
    else:
        data['alerts'].append(alert)
        msg = f"✅ 新建预警：{symbol}"
    
    if target_price:
        msg += f" 目标价 ¥{target_price}"
    if change_pct:
        msg += f" 涨跌幅 {change_pct:+.1f}%"
    
    save_alerts(data)
    return msg


def list_alerts():
    """列出所有预警"""
    data = load_alerts()
    
    if not data['alerts']:
        return "🔔 暂无预警设置"
    
    lines = ["## 🔔 预警列表\n"]
    lines.append("| 股票 | 目标价 | 涨跌幅 | 创建时间 |")
    lines.append("|------|--------|--------|----------|")
    
    for a in data['alerts']:
        target = f"¥{a['target_price']}" if a.get('target_price') else "-"
        change = f"{a['change_pct']:+.1f}%" if a.get('change_pct') else "-"
        date = a['created_at'][:10] if 'created_at' in a else '-'
        lines.append(f"| {a['symbol']} | {target} | {change} | {date} |")
    
    return "\n".join(lines)


def remove_alert(symbol):
    """删除预警"""
    data = load_alerts()
    symbol = symbol.upper()
    
    for i, a in enumerate(data['alerts']):
        if a['symbol'] == symbol:
            removed = data['alerts'].pop(i)
            save_alerts(data)
            return f"✅ 已删除预警：{removed['symbol']}"
    
    return f"❌ 未找到预警：{symbol}"


def check_alerts():
    """检查预警条件"""
    alerts_data = load_alerts()
    
    if not alerts_data['alerts']:
        return "🔔 暂无预警需要检查"
    
    # 导入行情查询
    sys.path.insert(0, str(Path(__file__).parent))
    from stock_fetch import fetch_stock_price
    
    triggered = []
    
    for alert in alerts_data['alerts']:
        price_data = fetch_stock_price(alert['symbol'])
        
        if 'error' in price_data:
            continue
        
        current = price_data['current']
        change_pct = price_data['change_pct']
        
        # 检查目标价
        if alert.get('target_price'):
            target = alert['target_price']
            if current >= target:
                triggered.append(f"🎯 {alert['symbol']} 达到目标价 ¥{target} (当前 ¥{current:.2f})")
        
        # 检查涨跌幅
        if alert.get('change_pct'):
            threshold = alert['change_pct']
            if abs(change_pct) >= abs(threshold):
                triggered.append(f"📊 {alert['symbol']} 涨跌幅 {change_pct:+.2f}% (阈值 {threshold:+.1f}%)")
    
    if triggered:
        return "⚠️ 预警触发:\n\n" + "\n".join(triggered)
    else:
        return "✅ 所有预警条件未触发"


def main():
    parser = argparse.ArgumentParser(description='股票持仓管理工具')
    subparsers = parser.add_subparsers(dest='command', help='命令')
    
    # add 命令
    add_parser = subparsers.add_parser('add', help='添加持仓')
    add_parser.add_argument('--symbol', required=True, help='股票代码')
    add_parser.add_argument('--price', type=float, required=True, help='买入价格')
    add_parser.add_argument('--shares', type=int, required=True, help='股数')
    add_parser.add_argument('--name', help='股票名称')
    
    # remove 命令
    remove_parser = subparsers.add_parser('remove', help='删除持仓')
    remove_parser.add_argument('--symbol', required=True, help='股票代码')
    
    # list 命令
    subparsers.add_parser('list', help='列出持仓')
    
    # summary 命令
    subparsers.add_parser('summary', help='持仓汇总')
    
    # alert 命令
    alert_parser = subparsers.add_parser('alert', help='设置预警')
    alert_parser.add_argument('--symbol', required=True, help='股票代码')
    alert_parser.add_argument('--target', type=float, help='目标价格')
    alert_parser.add_argument('--change', type=float, help='涨跌幅阈值')
    
    # alerts 命令
    subparsers.add_parser('alerts', help='列出预警')
    
    # remove-alert 命令
    remove_alert_parser = subparsers.add_parser('remove-alert', help='删除预警')
    remove_alert_parser.add_argument('--symbol', required=True, help='股票代码')
    
    # check-alerts 命令
    subparsers.add_parser('check-alerts', help='检查预警')
    
    args = parser.parse_args()
    
    if args.command == 'add':
        print(add_holding(args.symbol, args.price, args.shares, args.name))
    elif args.command == 'remove':
        print(remove_holding(args.symbol))
    elif args.command == 'list':
        print(list_holdings())
    elif args.command == 'summary':
        print(calculate_summary())
    elif args.command == 'alert':
        print(set_alert(args.symbol, args.target, args.change))
    elif args.command == 'alerts':
        print(list_alerts())
    elif args.command == 'remove-alert':
        print(remove_alert(args.symbol))
    elif args.command == 'check-alerts':
        print(check_alerts())
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
