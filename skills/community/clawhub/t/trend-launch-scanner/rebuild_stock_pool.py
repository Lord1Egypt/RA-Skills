#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
重建股票池 - 行业均衡分布
从全市场5000只股票中筛选300-350只，每行业最多15-20只
"""
import baostock as bs
import pandas as pd
import requests
import json
import random
import time
from collections import Counter, defaultdict
from pathlib import Path

OUTPUT_PATH = Path("C:/Users/Administrator/.qclaw/workspace-ag01/skills/trend-launch-scanner/stock_pool_v2.py")

# 行业关键词映射
SECTOR_KEYWORDS = {
    '医药生物': ['制药', '药业', '医药', '生物', '医疗', '健康', '康', '中药', '胶囊', '注射', '药房', '医科', '医', '药', '诊断', '器械', '基因', '疫苗'],
    '食品饮料': ['食品', '乳业', '牛奶', '饮料', '调味', '肉制', '罐头', '零食', '酒', '白酒', '茅台', '五粮', '汾酒', '青岛', '燕京', '洋河', '泸州', '古井', '舍得', '水井'],
    '电子': ['电子', '光电', '面板', 'LED', '半导体', '芯片', '集成电路', '显示', '光学'],
    '计算机': ['软件', '系统', '网络', '云', '数据', '信息', '智控', '智造', '科技', '数码', '互联'],
    '化工': ['化工', '化学', '新材', '材料', '塑', '橡胶', '纤维'],
    '机械设备': ['机械', '重工', '装备', '机床', '仪器', '泵', '阀', '轴承', '齿轮'],
    '汽车': ['汽车', '车企', '部件', '发动机', '座椅', '轮胎', '轮毂'],
    '家用电器': ['家电', '电器', '空调', '冰箱', '洗衣机', '厨电', '小家电'],
    '电力设备': ['电力', '电气', '电池', '储能', '光伏', '风电', '核电', '电网', '发电'],
    '有色金属': ['有色', '铜业', '铝业', '稀土', '矿业', '矿产', '金属', '锂', '钴'],
    '房地产': ['地产', '房地产', '万科', '保利', '金地', '华侨城', '招商蛇口'],
    '银行': ['银行'],
    '非银金融': ['证券', '保险', '信托', '基金', '资本', '投资'],
    '国防军工': ['军工', '航空', '航天', '国防', '雷达'],
    '传媒': ['传媒', '影视', '文化', '游戏', '出版', '广告', '娱乐'],
    '交通运输': ['航空', '机场', '航运', '港口', '物流', '快递', '高速', '铁路'],
    '建筑材料': ['建材', '水泥', '钢铁', '螺纹', '玻璃', '陶瓷'],
    '纺织服装': ['纺织', '服装', '鞋', '家纺', '服饰', '布'],
    '轻工制造': ['轻工', '造纸', '包装', '印刷', '家居'],
    '公用事业': ['水务', '燃气', '供热', '环保', '环境'],
    '农林牧渔': ['农业', '畜牧', '养殖', '饲料', '种业', '渔业', '农产品'],
    '商贸零售': ['零售', '超市', '百货', '商贸', '贸易', '商业'],
    '煤炭': ['煤炭', '煤业', '焦煤'],
    '石油石化': ['石油', '油气', '石化', '炼化'],
    '建筑装饰': ['装饰', '装修', '幕墙', '园林', '建设'],
    '通信': ['通信', '通讯', '5G', '基站', '光纤', '光缆'],
    '钢铁': ['钢铁', '钢', '特钢'],
    '基础化工': ['氯碱', '纯碱', '尿素', '磷肥', '钾肥'],
}

# 排除的行业（不纳入股票池）
EXCLUDE_SECTORS = ['银行']  # 银行股波动小，不适合短线

# 每行业最多选多少只
MAX_PER_SECTOR = 15


def guess_sector(name):
    """根据名称关键词猜测行业"""
    for sector, keywords in SECTOR_KEYWORDS.items():
        for kw in keywords:
            if kw in name:
                return sector
    return '其他'


def fetch_all_stocks():
    """从baostock获取全市场股票列表"""
    print('获取全市场股票列表...', flush=True)
    bs.login()
    rs = bs.query_stock_basic(code_name='')
    stocks = []
    while rs.next():
        r = rs.get_row_data()
        if r and len(r) >= 3 and r[0] and r[1]:
            # r: [code, code_name, ipoDate, outDate, type, status]
            # code格式: sh.600000 或 sz.000001 或直接是代码
            code_full = r[0]
            name = r[1]
            
            # 解析代码
            if '.' in code_full:
                market, code = code_full.split('.')
            else:
                code = code_full
                market = 'sh' if code.startswith('6') else 'sz'
            
            # 只要沪深主板+创业板，排除科创板(688)、北交所(8)
            if code.startswith('688') or code.startswith('8') or code.startswith('4'):
                continue
            
            # 排除指数和基金
            if code.startswith('00') and len(code) == 6 and code[2] in ['0', '1', '2', '3']:
                pass  # 正常股票
            elif code.startswith('60') or code.startswith('00'):
                pass  # 正常股票
            else:
                continue
            
            stocks.append({
                'code': code,
                'name': name,
                'sector': guess_sector(name)
            })
    bs.logout()
    return stocks


def filter_stocks(stocks):
    """筛选股票"""
    print(f'原始股票数: {len(stocks)}', flush=True)
    
    # 1. 排除ST和*
    clean = [s for s in stocks if 'ST' not in s['name'] and '*' not in s['name'] and '退' not in s['name']]
    print(f'排除ST后: {len(clean)}', flush=True)
    
    # 2. 排除指定行业
    clean = [s for s in clean if s['sector'] not in EXCLUDE_SECTORS]
    print(f'排除银行后: {len(clean)}', flush=True)
    
    # 3. 行业分布统计
    sector_count = Counter(s['sector'] for s in clean)
    print('\n当前行业分布:')
    for sec, cnt in sector_count.most_common(15):
        print(f'  {sec}: {cnt}')
    print(f'  ... 共{len(sector_count)}个行业')
    
    return clean


def select_balanced(stocks):
    """按行业均衡选股，排除指数和基金"""
    # 排除指数、基金、债券等
    clean = []
    exclude_keywords = [
        '指数', 'ETF', 'LOF', '基金', '分级', 'B股', '创业板',
        '380', '主题', '沪投', '消费', '能源', '材料', '工业',
        '可选', '金融', '信息', '电信', '公用', '持续', '等权',
        '成长', '价值', 'R成长', 'R价值', '细分', '医药生物',
        '债', '转债', '债券', '水泥'
    ]
    for s in stocks:
        name = s['name']
        code = s['code']
        
        # 排除包含排除关键词的
        if any(e in name for e in exclude_keywords):
            continue
        
        # 排除0000开头的指数代码
        if code.startswith('0000') or code.startswith('399'):
            continue
        
        # 排除0001开头的指数（如000102-000121）
        if code.startswith('0001') and len(code) == 6:
            try:
                num = int(code)
                if 102 <= num <= 200:  # 指数代码范围
                    continue
            except:
                pass
        
        clean.append(s)
    
    # 按行业分组
    by_sector = defaultdict(list)
    for s in clean:
        by_sector[s['sector']].append(s)
    
    # 每行业按代码排序
    for sec in by_sector:
        by_sector[sec].sort(key=lambda x: x['code'])
    
    # 每行业最多选MAX_PER_SECTOR只
    selected = []
    for sec, stocks_in_sec in by_sector.items():
        n = min(len(stocks_in_sec), MAX_PER_SECTOR)
        selected.extend(stocks_in_sec[:n])
    
    # 去重：按代码去重，保留第一个
    seen_codes = set()
    unique_selected = []
    for s in selected:
        if s['code'] not in seen_codes:
            seen_codes.add(s['code'])
            unique_selected.append(s)
    
    return unique_selected


def save_pool(stocks):
    """保存为新股票池文件"""
    lines = [
        '#!/usr/bin/env python3',
        '# -*- coding: utf-8 -*-',
        '"""股票池 v2 - 行业均衡分布"""',
        '',
        'STOCK_POOL_V2 = [',
    ]
    
    for s in sorted(stocks, key=lambda x: x['code']):
        lines.append(f"    {{'code': '{s['code']}', 'name': '{s['name']}'}},")
    
    lines.append(']')
    lines.append('')
    lines.append('def get_stock_pool_v2():')
    lines.append('    return STOCK_POOL_V2')
    lines.append('')
    
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    print(f'\n已保存到: {OUTPUT_PATH}', flush=True)


def main():
    # 1. 获取全市场股票
    all_stocks = fetch_all_stocks()
    
    # 2. 筛选
    clean = filter_stocks(all_stocks)
    
    # 3. 行业均衡选股
    selected = select_balanced(clean)
    
    # 4. 统计结果
    final_count = Counter(s['sector'] for s in selected)
    print(f'\n最终股票池: {len(selected)}只')
    print('行业分布:')
    for sec, cnt in sorted(final_count.items(), key=lambda x: -x[1]):
        print(f'  {sec}: {cnt}')
    
    # 5. 保存
    save_pool(selected)
    
    return selected


if __name__ == '__main__':
    main()
