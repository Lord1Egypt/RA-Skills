#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""尝试使用AKShare获取A股列表"""

try:
    import akshare as ak
    print('AKShare已安装')
    
    # 获取A股列表
    df = ak.stock_info_a_code_name()
    print(f'\nA股总数: {len(df)}')
    print(df.head(10))
    
    # 保存
    output_path = r'C:\Users\Administrator\.qclaw\workspace-ag01\skills\trend-launch-scanner\stock_pool_full.py'
    
    # 过滤
    filtered = []
    from collections import Counter
    stats = Counter()
    
    for _, row in df.iterrows():
        code = str(row['code']).zfill(6)
        name = row['name']
        
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
        if any(kw in name for kw in ['白酒', '茅台', '五粮液', '汾酒', '泸州老窖', '洋河股份', '古井贡酒', '舍得酒业', '水井坊', '酒鬼酒', '今世缘', '迎驾贡酒', '口子窖', '金徽酒', '伊力特', '老白干', '青青稞']):
            stats['白酒'] += 1
            continue
        
        filtered.append({'code': code, 'name': name})
    
    print(f'\n过滤后: {len(filtered)}只')
    print('过滤统计:')
    for reason, cnt in stats.most_common():
        print(f'  {reason}: {cnt}')
    
    # 保存
    lines = [
        '#!/usr/bin/env python3',
        '# -*- coding: utf-8 -*-',
        f'"""股票池 - 全市场覆盖版（{len(filtered)}只，来自AKShare）"""',
        '',
        'STOCK_POOL_FULL = [',
    ]
    
    for s in sorted(filtered, key=lambda x: x['code']):
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
    
except ImportError:
    print('AKShare未安装')
    print('安装命令: pip install akshare')
