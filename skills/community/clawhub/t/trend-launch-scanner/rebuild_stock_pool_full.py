#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
重建股票池 - 全市场覆盖版
去掉行业配额限制，只做基础过滤
"""
import baostock as bs
import json
from pathlib import Path
from collections import Counter, defaultdict

OUTPUT_PATH = Path("C:/Users/Administrator/.qclaw/workspace-ag01/skills/trend-launch-scanner/stock_pool_full.py")

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

# 排除的行业
EXCLUDE_SECTORS = ['银行', '非银金融']  # 银行、证券都排除

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
            code_full = r[0]
            name = r[1]
            
            if '.' in code_full:
                market, code = code_full.split('.')
            else:
                code = code_full
                market = 'sh' if code.startswith('6') else 'sz'
            
            # 只要沪深主板+创业板，排除科创板(688)、北交所(8/4)
            if code.startswith('688') or code.startswith('8') or code.startswith('4'):
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
    
    # 1. 排除ST、*、退
    clean = [s for s in stocks if 'ST' not in s['name'] and '*' not in s['name'] and '退' not in s['name']]
    print(f'排除ST后: {len(clean)}', flush=True)
    
    # 2. 排除指定行业（银行、证券）
    clean = [s for s in clean if s['sector'] not in EXCLUDE_SECTORS]
    print(f'排除银行/证券后: {len(clean)}', flush=True)
    
    # 3. 排除指数、基金等
    exclude_keywords = [
        '指数', 'ETF', 'LOF', '基金', '分级', 'B股', '创业板',
        '380', '主题', '沪投', '消费', '能源', '材料', '工业',
        '可选', '金融', '信息', '电信', '公用', '持续', '等权',
        '成长', '价值', 'R成长', 'R价值', '细分', '医药生物',
        '债', '转债', '债券', '水泥'
    ]
    clean = [s for s in clean if not any(e in s['name'] for e in exclude_keywords)]
    print(f'排除指数/基金后: {len(clean)}', flush=True)
    
    # 4. 排除指数代码
    clean = [s for s in clean if not (s['code'].startswith('0000') or s['code'].startswith('399'))]
    print(f'排除指数代码后: {len(clean)}', flush=True)
    
    # 5. 排除名字含"地产""证券"的
    clean = [s for s in clean if '地产' not in s['name'] and '证券' not in s['name']]
    print(f'排除地产/证券后: {len(clean)}', flush=True)
    
    # 6. 排除白酒
    clean = [s for s in clean if '白酒' not in s['sector'] and '酒' not in s['name'] and '茅台' not in s['name'] and '五粮' not in s['name']]
    print(f'排除白酒后: {len(clean)}', flush=True)
    
    return clean


def main():
    # 1. 获取全市场股票
    all_stocks = fetch_all_stocks()
    
    # 2. 筛选（不限制行业配额）
    clean = filter_stocks(all_stocks)
    
    # 3. 统计
    sector_count = Counter(s['sector'] for s in clean)
    print(f'\n最终股票池: {len(clean)}只')
    print('行业分布:')
    for sec, cnt in sector_count.most_common():
        print(f'  {sec}: {cnt}')
    
    # 4. 保存为Python文件
    lines = [
        '#!/usr/bin/env python3',
        '# -*- coding: utf-8 -*-',
        '"""股票池 - 全市场覆盖版（无行业配额限制）"""',
        '',
        'STOCK_POOL_FULL = [',
    ]
    
    for s in sorted(clean, key=lambda x: x['code']):
        lines.append(f"    {{'code': '{s['code']}', 'name': '{s['name']}'}},")
    
    lines.append(']')
    lines.append('')
    lines.append('def get_stock_pool_full():')
    lines.append('    return STOCK_POOL_FULL')
    lines.append('')
    
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    print(f'\n已保存到: {OUTPUT_PATH}', flush=True)
    
    return clean


if __name__ == '__main__':
    main()
