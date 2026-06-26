#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票实时行情查询脚本
支持 A股 和 港股 的实时行情获取

使用方法:
    python stock_query.py --codes 03690.HK,300413.SZ,300251.SZ
    python stock_query.py --names 美团,芒果超媒,光线传媒
"""

import argparse
import sys
import time

def check_akshare():
    """检查 akshare 是否安装"""
    try:
        import akshare as ak
        return ak
    except ImportError:
        print("❌ akshare 未安装，请运行: pip install akshare")
        sys.exit(1)

def parse_code(code):
    """解析股票代码，返回 (市场, 纯代码)"""
    if '.' in code:
        parts = code.split('.')
        return parts[1], parts[0]  # (市场, 代码)
    else:
        # 默认 A股
        return 'SZ', code

def get_a_stock_price(ak, code):
    """获取 A股 实时行情"""
    try:
        # 获取 A股 实时行情
        df = ak.stock_zh_a_spot_em()
        
        # 查找目标股票
        row = df[df['代码'] == code]
        if row.empty:
            return None
        
        row = row.iloc[0]
        return {
            'code': code,
            'market': 'SZ' if code.startswith('0') or code.startswith('3') else 'SH',
            'name': row['名称'],
            'price': float(row['最新价']),
            'change_pct': float(row['涨跌幅']),
            'volume': float(row['成交量']),
            'amount': float(row['成交额']),
            'high': float(row['最高']),
            'low': float(row['最低']),
            'open': float(row['今开']),
            'prev_close': float(row['昨收']),
        }
    except Exception as e:
        print(f"❌ 获取 A股 {code} 失败: {e}")
        return None

def get_hk_stock_price(ak, code):
    """获取港股实时行情"""
    try:
        # 获取港股实时行情
        df = ak.stock_hk_spot_em()
        
        # 查找目标股票（港股代码格式：03690）
        row = df[df['代码'] == code]
        if row.empty:
            return None
        
        row = row.iloc[0]
        return {
            'code': code,
            'market': 'HK',
            'name': row['名称'],
            'price': float(row['最新价']),
            'change_pct': float(row['涨跌幅']),
            'volume': float(row['成交量']) if '成交量' in row else 0,
            'amount': float(row['成交额']) if '成交额' in row else 0,
            'high': float(row['最高']) if '最高' in row else 0,
            'low': float(row['最低']) if '最低' in row else 0,
        }
    except Exception as e:
        print(f"❌ 获取港股 {code} 失败: {e}")
        return None

def format_price(data):
    """格式化价格显示"""
    if data is None:
        return "❌ 数据获取失败"
    
    market_symbol = {
        'SZ': '¥',
        'SH': '¥',
        'HK': 'HK$',
    }.get(data['market'], '$')
    
    change_symbol = '🔴' if data['change_pct'] < 0 else '🟢' if data['change_pct'] > 0 else '⚪'
    
    return f"{data['name']}({data['code']}.{data['market']}): {market_symbol}{data['price']:.2f} ({change_symbol}{data['change_pct']:+.2f}%)"

def main():
    parser = argparse.ArgumentParser(description='股票实时行情查询')
    parser.add_argument('--codes', type=str, help='股票代码，逗号分隔，如 03690.HK,300413.SZ')
    parser.add_argument('--names', type=str, help='股票名称，逗号分隔（暂不支持）')
    args = parser.parse_args()
    
    if not args.codes and not args.names:
        parser.print_help()
        return
    
    ak = check_akshare()
    
    codes = []
    if args.codes:
        codes = [c.strip() for c in args.codes.split(',')]
    
    print(f"\n📊 正在查询 {len(codes)} 只股票...\n")
    
    results = []
    for code in codes:
        market, pure_code = parse_code(code)
        
        if market == 'HK':
            data = get_hk_stock_price(ak, pure_code)
        else:
            data = get_a_stock_price(ak, pure_code)
        
        if data:
            results.append(data)
            print(format_price(data))
        
        # 避免请求过快
        time.sleep(0.5)
    
    print(f"\n✅ 成功获取 {len(results)}/{len(codes)} 只股票数据")
    
    return results

if __name__ == '__main__':
    main()
