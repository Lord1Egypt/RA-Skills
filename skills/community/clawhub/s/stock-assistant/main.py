#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
炒股助手 - CLI 入口
"""

import sys
import argparse
import os
import json

# 确保当前目录在 Python 路径中
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fetcher import StockFetcher
from trader import StockTrader


def cmd_quote(args):
    """行情查询"""
    fetcher = StockFetcher()
    result = fetcher.get_quote(args.code)
    print(fetcher.format_quote(result))


def cmd_positions(args):
    """查看持仓"""
    trader = StockTrader()
    positions = trader.get_positions()
    
    if not positions:
        print("暂无持仓")
        return
    
    print("\n【当前持仓】")
    print("-" * 60)
    print(f"{'代码':<10} {'名称':<10} {'数量':<10} {'成本价':<12} {'总成本':<15}")
    print("-" * 60)
    
    total_market_value = 0
    total_cost = 0
    
    for pos in positions:
        print(f"{pos.code:<10} {pos.name:<10} {pos.quantity:<10} {pos.avg_cost:<12.4f} {pos.total_cost:<15.2f}")
        total_cost += pos.total_cost
    
    print("-" * 60)
    print(f"总成本: {total_cost:.2f}")


def cmd_pnl(args):
    """盈亏计算"""
    trader = StockTrader()
    
    try:
        if args.price:
            # 使用指定价格
            pnl = trader.calculate_pnl(args.code, args.price)
        else:
            # 获取实时价格
            pnl = trader.get_pnl_with_live_price(args.code)
        
        if not pnl:
            print(f"未找到股票 {args.code} 的持仓")
            return
        
        print(f"\n【{pnl.name} ({pnl.code})】")
        print("-" * 40)
        print(f"持仓数量: {pnl.quantity} 股")
        print(f"成本均价: {pnl.avg_cost:.4f} 元")
        print(f"当前价格: {pnl.current_price:.4f} 元")
        print(f"市值: {pnl.market_value:.2f} 元")
        print(f"盈亏: {pnl.profit:+.2f} 元 ({pnl.profit_pct:+.2f}%)")
        
    except ValueError as e:
        print(f"错误: {e}")


def cmd_list(args):
    """列出交易记录"""
    trader = StockTrader()
    trades = trader.list_trades(args.code)
    
    if not trades:
        print("暂无交易记录")
        return
    
    print(f"\n【交易记录】{' (筛选: ' + args.code + ')' if args.code else ''}")
    print("-" * 80)
    print(f"{'日期':<12} {'代码':<10} {'名称':<10} {'方向':<6} {'数量':<8} {'价格':<10} {'金额':<12}")
    print("-" * 80)
    
    for trade in trades:
        print(f"{trade.trade_date:<12} {trade.code:<10} {trade.name:<10} {trade.direction:<6} "
              f"{trade.quantity:<8} {trade.price:<10.4f} {trade.amount:<12.2f}")
    
    print("-" * 80)
    print(f"共 {len(trades)} 条记录")


def cmd_import(args):
    """导入CSV"""
    if not os.path.exists(args.file):
        print(f"文件不存在: {args.file}")
        return
    
    trader = StockTrader()
    try:
        count = trader.import_csv(args.file)
        print(f"成功导入 {count} 条交易记录")
    except Exception as e:
        print(f"导入失败: {e}")


def cmd_export(args):
    """导出CSV"""
    trader = StockTrader()
    try:
        count = trader.export_csv(args.output, args.code)
        print(f"成功导出 {count} 条记录到 {args.output}")
    except Exception as e:
        print(f"导出失败: {e}")


def cmd_add(args):
    """手动添加交易"""
    trader = StockTrader()
    
    trade_data = {
        'date': args.date,
        'time': args.time or '',
        'code': args.code,
        'name': args.name or '',
        'direction': '买入' if args.type == 'buy' else '卖出',
        'quantity': args.quantity,
        'price': args.price,
        'amount': args.quantity * args.price,
    }
    
    try:
        trade_id = trader.add_trade(trade_data)
        print(f"成功添加交易记录 (ID: {trade_id})")
    except Exception as e:
        print(f"添加失败: {e}")


def cmd_delete(args):
    """删除交易记录"""
    trader = StockTrader()
    
    if trader.delete_trade(args.id):
        print(f"已删除交易记录 ID: {args.id}")
    else:
        print(f"删除失败，记录不存在")


def cmd_notify(args):
    """推送股价到飞书"""
    from fetcher import StockFetcher, send_feishu, send_feishu_private
    from trader import StockTrader
    import json
    
    codes = args.codes.split(',') if args.codes else [args.code]
    fetcher = StockFetcher()
    trader = StockTrader()
    
    messages = []
    
    for code in codes:
        code = code.strip()
        if not code:
            continue
        
        # 获取行情
        result = fetcher.get_quote(code)
        
        # 获取持仓
        position = trader.get_position(code)
        
        # 生成卡片（带持仓信息）
        message = fetcher.format_table(result, position)
        messages.append(message)
    
    # 合并多张卡片
    full_message = messages[0] if len(messages) == 1 else json.dumps({
        'config': {'wide_screen_mode': True},
        'header': {'title': {'tag': 'plain_text', 'content': '📊 多只股票行情'}, 'template': 'blue'},
        'elements': [{'tag': 'div', 'text': {'tag': 'lark_md', 'content': m}} for m in messages]
    })
    
    if args.webhook:
        # 发送到飞书 Webhook (群机器人) - 需要转文本
        text_content = "\n\n---\n\n".join([json.loads(m).get('elements', [])[0].get('text', {}).get('content', '') if m.startswith('{') else m for m in messages])
        success = send_feishu(args.webhook, text_content)
        if success:
            print("✅ 已发送到飞书群")
        else:
            print("❌ 发送失败")
    elif args.app_id and args.app_secret and args.receive_id:
        # 发送到飞书私聊 - 使用卡片格式
        success = send_feishu_private(full_message, args.app_id, args.app_secret, args.receive_id, is_card=True)
        if success:
            print("✅ 已发送到飞书私聊")
        else:
            print("❌ 发送失败")
    else:
        # 只输出
        print(full_message)


def main():
    parser = argparse.ArgumentParser(
        description='炒股助手 - A股交易辅助工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  python main.py quote 600016              查询行情
  python main.py positions                 查看持仓
  python main.py pnl 600016                 查看盈亏(实时价格)
  python main.py pnl 600016 --price 4.15    查看盈亏(指定价格)
  python main.py import trades.csv          导入CSV
  python main.py add --code 600016 --type buy --quantity 1000 --price 3.90
  python main.py notify 600016              查询并输出行情(多数据源备用)
  python main.py notify --codes 600016,000001 --webhook https://xxx  推送到飞书
        '''
    )
    
    subparsers = parser.add_subparsers(dest='command', help='子命令')
    
    # 行情查询
    p_quote = subparsers.add_parser('quote', help='查询股票行情')
    p_quote.add_argument('code', help='股票代码')
    p_quote.set_defaults(func=cmd_quote)
    
    # 持仓
    p_pos = subparsers.add_parser('positions', help='查看当前持仓')
    p_pos.set_defaults(func=cmd_positions)
    
    # 盈亏
    p_pnl = subparsers.add_parser('pnl', help='计算盈亏')
    p_pnl.add_argument('code', help='股票代码')
    p_pnl.add_argument('--price', type=float, help='指定价格(不指定则获取实时价格)')
    p_pnl.set_defaults(func=cmd_pnl)
    
    # 交易记录
    p_list = subparsers.add_parser('list', help='列出交易记录')
    p_list.add_argument('--code', help='筛选股票代码')
    p_list.set_defaults(func=cmd_list)
    
    # 导入
    p_import = subparsers.add_parser('import', help='导入CSV文件')
    p_import.add_argument('file', help='CSV文件路径')
    p_import.set_defaults(func=cmd_import)
    
    # 导出
    p_export = subparsers.add_parser('export', help='导出CSV文件')
    p_export.add_argument('--output', default='trades.csv', help='输出文件路径')
    p_export.add_argument('--code', help='筛选股票代码')
    p_export.set_defaults(func=cmd_export)
    
    # 添加
    p_add = subparsers.add_parser('add', help='手动添加交易')
    p_add.add_argument('--code', required=True, help='股票代码')
    p_add.add_argument('--name', help='股票名称')
    p_add.add_argument('--type', choices=['buy', 'sell'], required=True, help='买入/卖出')
    p_add.add_argument('--quantity', type=int, required=True, help='数量')
    p_add.add_argument('--price', type=float, required=True, help='价格')
    p_add.add_argument('--date', default='', help='交易日期(默认今天)')
    p_add.add_argument('--time', help='交易时间')
    p_add.set_defaults(func=cmd_add)
    
    # 删除
    p_del = subparsers.add_parser('delete', help='删除交易记录')
    p_del.add_argument('id', type=int, help='交易记录ID')
    p_del.set_defaults(func=cmd_delete)
    
    # 推送
    p_notify = subparsers.add_parser('notify', help='推送股价到飞书(定时任务用)')
    p_notify.add_argument('code', nargs='?', help='股票代码(可省略，配合 --codes 使用)')
    p_notify.add_argument('--codes', help='多个股票代码，用逗号分隔')
    p_notify.add_argument('--webhook', help='飞书 Webhook URL (群机器人)')
    p_notify.add_argument('--app-id', dest='app_id', help='飞书应用 App ID (私聊)')
    p_notify.add_argument('--app-secret', dest='app_secret', help='飞书应用 App Secret (私聊)')
    p_notify.add_argument('--receive-id', dest='receive_id', help='接收者 ID (私聊)')
    p_notify.set_defaults(func=cmd_notify)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # 设置默认日期
    if hasattr(args, 'date') and args.date == '':
        from datetime import datetime
        args.date = datetime.now().strftime('%Y-%m-%d')
    
    args.func(args)


if __name__ == '__main__':
    main()
