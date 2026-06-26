# -*- coding: utf-8 -*-
"""
持仓数据更新脚本（跨平台版）
支持 Windows / macOS / Linux
支持 AI 识别结果更新、手动更新持仓
"""
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# 跨平台路径
SKILL_ROOT = Path(__file__).parent.parent.resolve()
SKILL_DATA = SKILL_ROOT / 'data'
PORTFOLIO_PATH = SKILL_DATA / 'positions_portfolio.json'


def load_portfolio():
    """加载持仓数据"""
    if PORTFOLIO_PATH.exists():
        with open(PORTFOLIO_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {'last_updated': '', 'source': '', 'portfolio': []}


def save_portfolio(data, source='手动更新'):
    """保存持仓数据"""
    data['last_updated'] = datetime.now().strftime('%Y-%m-%d %H:%M')
    data['source'] = source
    os.makedirs(SKILL_DATA, exist_ok=True)
    with open(PORTFOLIO_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"[OK] 持仓已保存至 {PORTFOLIO_PATH}")


def update_from_ai_result(ai_recognized_list, source='微信截图识别'):
    """
    从 AI 识别结果更新持仓（覆盖式更新）
    
    ai_recognized_list: [
        {'name': '长电科技', 'code': '600584', 'quantity': 400, 'cost_price': 39.53},
        ...
    ]
    """
    data = {
        'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'source': source,
        'portfolio': []
    }
    
    for item in ai_recognized_list:
        entry = {
            'code': item.get('code', ''),
            'name': item.get('name', ''),
            'quantity': int(item.get('quantity', 0)),
            'cost_price': float(item.get('cost_price', 0)),
            'current_price': item.get('current_price'),  # 可选
            'market_value': item.get('market_value'),     # 可选
            'profit_pct': item.get('profit_pct'),         # 可选
            'asset_type': _detect_asset_type(item.get('code', ''))
        }
        data['portfolio'].append(entry)
        print(f"[ADD] {entry['name']}({entry['code']}): {entry['quantity']}股，成本{entry['cost_price']}")
    
    save_portfolio(data, source)
    return data


def _detect_asset_type(code):
    """根据代码判断资产类型"""
    if not code:
        return 'stock'
    # ETF 代码特征
    if code.startswith('51') or code.startswith('15') or code.startswith('16'):
        return 'etf'
    # 可转债
    if code.startswith('11') or code.startswith('12'):
        return 'bond'
    return 'stock'


def add_stock(code, name, quantity, cost_price, asset_type=None):
    """添加或更新单只持仓"""
    data = load_portfolio()
    portfolio = data.get('portfolio', [])
    
    if not asset_type:
        asset_type = _detect_asset_type(code)
    
    for item in portfolio:
        if item['code'] == code:
            item.update({
                'quantity': quantity,
                'cost_price': cost_price,
                'asset_type': asset_type
            })
            print(f"[UPDATE] {name}({code}): {quantity}股，成本{cost_price}")
            save_portfolio(data, '手动更新')
            return data
    
    portfolio.append({
        'code': code,
        'name': name,
        'quantity': quantity,
        'cost_price': cost_price,
        'current_price': None,
        'market_value': None,
        'profit_pct': None,
        'asset_type': asset_type
    })
    print(f"[ADD] {name}({code}): {quantity}股，成本{cost_price}")
    save_portfolio(data, '手动更新')
    return data


def remove_stock(code):
    """删除持仓"""
    data = load_portfolio()
    portfolio = data.get('portfolio', [])
    original_len = len(portfolio)
    data['portfolio'] = [item for item in portfolio if item['code'] != code]
    
    if len(data['portfolio']) < original_len:
        print(f"[REMOVE] 已删除 {code}")
        save_portfolio(data, '手动删除')
    else:
        print(f"[WARN] 未找到 {code}")
    return data


def clear_portfolio():
    """清空所有持仓"""
    data = {'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M'), 'source': '清空', 'portfolio': []}
    save_portfolio(data, '清空')
    print("[CLEAR] 所有持仓已清空")
    return data


def list_portfolio():
    """列出当前持仓"""
    data = load_portfolio()
    print(f"\n{'='*50}")
    print(f"当前持仓（{len(data.get('portfolio', []))}只）")
    print(f"{'='*50}")
    for i, item in enumerate(data.get('portfolio', []), 1):
        pct = item.get('profit_pct')
        pct_str = f"{pct:+.2f}%" if isinstance(pct, (int, float)) else "—"
        print(f"  {i}. {item['name']}({item['code']}) | "
              f"数量:{item['quantity']} | 成本:{item.get('cost_price','—')} | 盈亏:{pct_str}")
    print(f"\n更新时间: {data.get('last_updated', '从未更新')}")
    print(f"数据来源: {data.get('source', '—')}")
    return data


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='持仓管理工具（跨平台）')
    parser.add_argument('--list', action='store_true', help='列出当前持仓')
    parser.add_argument('--add', nargs=4, metavar=('CODE', 'NAME', 'QTY', 'COST'),
                        help='添加/更新持仓: --add 600584 长电科技 400 39.53')
    parser.add_argument('--remove', help='删除持仓: --remove 600584')
    parser.add_argument('--clear', action='store_true', help='清空所有持仓')
    parser.add_argument('--json', help='从JSON字符串更新持仓（AI识别结果）')
    parser.add_argument('--file', help='从JSON文件更新持仓')
    args = parser.parse_args()

    if args.list:
        list_portfolio()
    elif args.add:
        code, name, qty, cost = args.add
        add_stock(code, name, int(qty), float(cost))
    elif args.remove:
        remove_stock(args.remove)
    elif args.clear:
        clear_portfolio()
    elif args.json:
        items = json.loads(args.json)
        update_from_ai_result(items)
    elif args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            items = json.load(f)
        update_from_ai_result(items)
    else:
        list_portfolio()
