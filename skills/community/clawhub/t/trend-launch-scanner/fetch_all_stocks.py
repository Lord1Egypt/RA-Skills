#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从东方财富API获取全A股股票列表"""
import requests
import json
from collections import Counter

def fetch_all_stocks_from_eastmoney():
    """从东方财富API获取完整A股列表"""
    stocks = []
    
    # 沪市主板 + 深市主板 + 创业板（合并查询）
    # fs参数说明：
    # m:1+t:2 = 沪市A股
    # m:0+t:6 = 深市A股
    # m:0+t:80 = 创业板
    
    queries = [
        ("沪市A股", "m:1+t:2,m:1+t:23"),
        ("深市A股", "m:0+t:6,m:0+t:13"),
        ("创业板", "m:0+t:80"),
    ]
    
    for name, fs in queries:
        print(f'获取{name}...', end=' ')
        url = f"http://82.push2.eastmoney.com/api/qt/clist/get?pn=1&pz=10000&po=1&np=1&fltt=2&invt=2&fid=f3&fs={fs}&fields=f12,f14"
        try:
            resp = requests.get(url, timeout=30)
            data = resp.json()
            count = 0
            if data.get('data') and data['data'].get('diff'):
                for item in data['data']['diff']:
                    code = item.get('f12', '')
                    name_str = item.get('f14', '')
                    if code and name_str:
                        stocks.append({'code': code, 'name': name_str})
                        count += 1
            print(f'{count}只')
        except Exception as e:
            print(f'失败: {e}')
    
    return stocks


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
        if any(kw in name for kw in ['白酒', '茅台', '五粮液', '汾酒', '泸州老窖', '洋河股份', '古井贡酒', '舍得酒业', '水井坊', '酒鬼酒', '今世缘', '迎驾贡酒', '口子窖', '金徽酒']):
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
        '"""股票池 - 全市场覆盖版（无行业配额限制）"""',
        '',
        'STOCK_POOL_FULL = [',
    ]
    
    for s in sorted(stocks, key=lambda x: x['code']):
        # 转义单引号
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
    stocks = fetch_all_stocks_from_eastmoney()
    print(f'\n总计: {len(stocks)}只')
    
    # 去重
    unique = {}
    for s in stocks:
        if s['code'] not in unique:
            unique[s['code']] = s
    print(f'去重后: {len(unique)}只')
    
    filtered = filter_stocks(list(unique.values()))
    save_pool(filtered)
