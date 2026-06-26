#!/usr/bin/env python3
"""
股票实时数据获取脚本 - 腾讯财经接口
支持A股、港股、美股实时行情获取
"""

import requests
import sys
import json
from typing import Dict, List, Optional

# 腾讯财经API基础URL
TENCENT_API = "https://qt.gtimg.cn/q={codes}"

def fetch_stock_data(codes: List[str]) -> Dict:
    """
    获取股票实时数据
    
    Args:
        codes: 股票代码列表，如 ['sh600919', 'sz159819']
              A股加 sh/sz 前缀，港股加 hk 前缀，美股直接代码
    
    Returns:
        Dict: 股票数据字典
    """
    if not codes:
        return {}
    
    try:
        url = TENCENT_API.format(codes=','.join(codes))
        resp = requests.get(url, timeout=10)
        resp.encoding = 'gbk'  # 腾讯接口使用GBK编码
        
        data = {}
        for line in resp.text.strip().split(';'):
            if not line.strip():
                continue
            
            try:
                parts = line.split('="')
                if len(parts) != 2:
                    continue
                
                code_key = parts[0].replace('v_', '')
                fields = parts[1].rstrip('"').split('~')
                
                if len(fields) < 35:
                    continue
                
                data[code_key] = {
                    'name': fields[1],
                    'code': fields[2],
                    'price': float(fields[3]) if fields[3] else 0.0,
                    'prev_close': float(fields[4]) if fields[4] else 0.0,
                    'open': float(fields[5]) if fields[5] else 0.0,
                    'volume': int(fields[6]) if fields[6] else 0,
                    'high': float(fields[33]) if fields[33] else 0.0,
                    'low': float(fields[34]) if fields[34] else 0.0,
                    'pe': float(fields[38]) if fields[38] else 0.0,
                }
                
                # 计算涨跌幅
                if data[code_key]['prev_close'] > 0:
                    data[code_key]['change_pct'] = round(
                        (data[code_key]['price'] - data[code_key]['prev_close']) 
                        / data[code_key]['prev_close'] * 100, 2
                    )
                else:
                    data[code_key]['change_pct'] = 0.0
                    
            except (IndexError, ValueError) as e:
                print(f"解析失败: {line[:50]}..., 错误: {e}", file=sys.stderr)
                continue
        
        return data
        
    except requests.RequestException as e:
        print(f"请求失败: {e}", file=sys.stderr)
        return {}


def calculate_position_pnl(position: Dict, current_price: float) -> Dict:
    """
    计算持仓盈亏
    
    Args:
        position: 持仓信息 {qty: 数量, cost: 成本价}
        current_price: 当前价格
    
    Returns:
        Dict: 盈亏信息
    """
    qty = position.get('qty', 0)
    cost = position.get('cost', 0)
    
    if qty <= 0 or cost <= 0:
        return {'pnl': 0, 'pnl_pct': 0, 'market_value': 0}
    
    pnl = (current_price - cost) * qty
    pnl_pct = round((current_price - cost) / cost * 100, 2) if cost > 0 else 0
    market_value = current_price * qty
    
    return {
        'pnl': round(pnl, 2),
        'pnl_pct': pnl_pct,
        'market_value': round(market_value, 2)
    }


def format_price_table(stock_data: Dict, positions: Optional[List[Dict]] = None) -> str:
    """
    格式化价格表格（Markdown格式）
    
    Args:
        stock_data: 股票数据字典
        positions: 持仓信息列表
    
    Returns:
        str: Markdown表格
    """
    lines = ["| 标的 | 代码 | 当前价 | 涨跌 | 状态 |", "|------|------|--------|------|------|"]
    
    for code, data in stock_data.items():
        change_emoji = "📈" if data.get('change_pct', 0) > 0 else "📉" if data.get('change_pct', 0) < 0 else "➖"
        lines.append(f"| {data.get('name', code)} | {code} | ¥{data.get('price', 0)} | {data.get('change_pct', 0)}% | {change_emoji} |")
    
    return '\n'.join(lines)


if __name__ == "__main__":
    # 命令行用法: python stock_fetcher.py sh600919 sz159819
    if len(sys.argv) < 2:
        print("Usage: python stock_fetcher.py <stock_code1> [stock_code2] ...")
        print("Example: python stock_fetcher.py sh600919 sz159819 hk00700")
        sys.exit(1)
    
    codes = sys.argv[1:]
    data = fetch_stock_data(codes)
    print(json.dumps(data, ensure_ascii=False, indent=2))
