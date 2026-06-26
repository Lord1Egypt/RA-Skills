#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从新浪财经接口获取完整A股列表"""
import requests
import json
from collections import Counter

def fetch_all_stocks_sina():
    """从新浪财经接口获取A股列表"""
    all_stocks = []
    
    # 分页获取（新浪接口最多每页5000只）
    pages = [
        ('hs_a', '沪深A股'),
        ('sh_b', '沪市B股'),
        ('sz_b', '深市B股'),
    ]
    
    for node, name in pages:
        page = 1
        while True:
            url = f"http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page={page}&num=5000&sort=code&asc=1&node={node}&symbol=&_s_r_a=page"
            try:
                resp = requests.get(url, timeout=30)
                data = resp.json()
                if not data or len(data) == 0:
                    break
                for item in data:
                    code = item.get('code', '')
                    stock_name = item.get('name', '')
                    if code and stock_name:
                        all_stocks.append({'code': code, 'name': stock_name})
                print(f'{name} 第{page}页: {len(data)}只')
                if len(data) < 5000:
                    break
                page += 1
            except Exception as e:
                print(f'{name} 第{page}页失败: {e}')
                break
    
    return all_stocks


def filter_stocks(stocks):
    """过滤股票"""
    print(f'\n原始: {len(stocks)}只')
    
    filtered = []
    stats = Counter()
    
    for s in stocks:
        code = s['code']
        name = s['name']
        
        # 科创板
        if code.startswith('688'):
            stats['科创板'] += 1
            continue
        # 北交所
        if code.startswith('8') or code.startswith('4'):
            stats['北交所'] += 1
            continue
        # B股
        if code.endswith('B') or 'B' in name:
            stats['B股'] += 1
            continue
        # ST
        if 'ST' in name.upper() or '*' in name:
            stats['ST'] += 1
            continue
        # 退市
        if '退' in name:
            stats['退市'] += 1
            continue
        # 地产
        if '地产' in name:
            stats['地产'] += 1
            continue
        # 证券
        if '证券' in name:
            stats['证券'] += 1
            continue
        # 银行
        if '银行' in name:
            stats['银行'] += 1
            continue
        # 白酒
        if any(kw in name for kw in ['白酒', '茅台', '五粮液', '汾酒', '泸州老窖', '洋河股份', '古井贡酒', '舍得酒业', '水井坊', '酒鬼酒', '今世缘', '迎驾贡酒', '口子窖', '金徽酒', '伊力特', '老白干', '青青稞']):
            stats['白酒'] += 1
            continue
        
        filtered.append(s)
    
    print(f'过滤后: {len(filtered)}只')
    print('过滤统计:')
    for reason, cnt in stats.most_common():
        print(f'  {reason}: {cnt}')
    
    return filtered


def save_pool(stocks):
    """保存股票池"""
    output_path = r'C:\Users\Administrator\.qclaw\workspace-ag01\skills\trend-launch-scanner\stock_pool_full.py'
    
    lines = [
        '#!/usr/bin/env python3',
        '# -*- coding: utf-8 -*-',
        f'"""股票池 - 全市场覆盖版（{len(stocks)}只）"""',
        '',
        'STOCK_POOL_FULL = [',
    ]
    
    for s in sorted(stocks, key=lambda x: x['code']):
        name = s['name'].replace("'", "\\'")
        lines.append(f"    {{'code': '{s['code']}', 'name': '{name}'}},")
    
    lines.append(']')
    lines.append('')
    lines.append('def get_stock_pool_full():')
    lines.append('    return STOCK_POOL_FULL')
    lines.append('')
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    print(f'\n已保存到: {output_path}')


if __name__ == '__main__':
    stocks = fetch_all_stocks_sina()
    print(f'\n总计: {len(stocks)}只')
    
    # 去重
    unique = {}
    for s in stocks:
        if s['code'] not in unique:
            unique[s['code']] = s
    print(f'去重后: {len(unique)}只')
    
    filtered = filter_stocks(list(unique.values()))
    save_pool(filtered)