#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从腾讯API获取A股股票列表"""
import requests
import json
import re
from collections import Counter

def get_stock_list_from_tencent():
    """从腾讯股票API获取A股列表"""
    # 腾讯股票列表API
    url = "https://qt.gtimg.cn/q="
    
    # 先获取沪深A股列表
    # 沪市主板: 600000-684000
    # 深市主板: 000001-002999
    # 创业板: 300001-301999
    
    stocks = []
    
    # 尝试从另一个API获取完整列表
    # 使用东方财富股票列表API
    try:
        # 沪市A股
        print('获取沪市A股...')
        url_sh = "http://82.push2.eastmoney.com/api/qt/clist/get?pn=1&pz=5000&po=1&np=1&fltt=2&invt=2&fid=f3&fs=m:1+t:2,m:1+t:23&fields=f12,f14"
        resp = requests.get(url_sh, timeout=30)
        data = resp.json()
        if data.get('data') and data['data'].get('diff'):
            for item in data['data']['diff']:
                code = item.get('f12', '')
                name = item.get('f14', '')
                if code and name:
                    stocks.append({'code': code, 'name': name})
        print(f'沪市A股: {len(stocks)}只')
        
        # 深市A股（主板+中小板）
        print('获取深市A股...')
        url_sz = "http://82.push2.eastmoney.com/api/qt/clist/get?pn=1&pz=5000&po=1&np=1&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:80&fields=f12,f14"
        resp = requests.get(url_sz, timeout=30)
        data = resp.json()
        sh_count = len(stocks)
        if data.get('data') and data['data'].get('diff'):
            for item in data['data']['diff']:
                code = item.get('f12', '')
                name = item.get('f14', '')
                if code and name:
                    stocks.append({'code': code, 'name': name})
        print(f'深市A股: {len(stocks) - sh_count}只')
        
        # 创业板
        print('获取创业板...')
        url_cy = "http://82.push2.eastmoney.com/api/qt/clist/get?pn=1&pz=5000&po=1&np=1&fltt=2&invt=2&fid=f3&fs=m:0+t:80&fields=f12,f14"
        resp = requests.get(url_cy, timeout=30)
        data = resp.json()
        prev_count = len(stocks)
        if data.get('data') and data['data'].get('diff'):
            for item in data['data']['diff']:
                code = item.get('f12', '')
                name = item.get('f14', '')
                if code and name:
                    stocks.append({'code': code, 'name': name})
        print(f'创业板: {len(stocks) - prev_count}只')
        
    except Exception as e:
        print(f'API调用失败: {e}')
    
    return stocks


def filter_stocks(stocks):
    """过滤股票"""
    print(f'\n原始股票数: {len(stocks)}')
    
    filtered = []
    stats = Counter()
    
    for s in stocks:
        code = s['code']
        name = s['name']
        reason = None
        
        # 科创板
        if code.startswith('688'):
            reason = '科创板'
        # 北交所
        elif code.startswith('8') or code.startswith('4'):
            reason = '北交所'
        # ST
        elif 'ST' in name.upper() or '*' in name:
            reason = 'ST'
        # 退市
        elif '退' in name:
            reason = '退市'
        # 地产
        elif '地产' in name:
            reason = '地产'
        # 证券
        elif '证券' in name:
            reason = '证券'
        # 银行
        elif '银行' in name:
            reason = '银行'
        # 白酒
        elif any(kw in name for kw in ['白酒', '茅台', '五粮液', '汾酒', '泸州老窖', '洋河', '古井贡', '舍得', '水井坊', '酒鬼酒']):
            reason = '白酒'
        
        if reason:
            stats[reason] += 1
        else:
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
        lines.append(f"    {{'code': '{s['code']}', 'name': '{s['name']}'}},")
    
    lines.append(']')
    lines.append('')
    lines.append('def get_stock_pool_full():')
    lines.append('    return STOCK_POOL_FULL')
    lines.append('')
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    print(f'\n已保存到: {output_path}')


if __name__ == '__main__':
    stocks = get_stock_list_from_tencent()
    if stocks:
        filtered = filter_stocks(stocks)
        save_pool(filtered)
    else:
        print('获取股票列表失败')