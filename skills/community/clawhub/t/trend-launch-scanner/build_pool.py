import baostock as bs
import pandas as pd
from collections import Counter

bs.login()
rs = bs.query_stock_basic(code_name='')
stocks = []
while rs.next():
    r = rs.get_row_data()
    if r and len(r) >= 4 and r[1] and r[2]:
        if r[4] in ['1','2']:
            stocks.append({'code': r[1].split('.')[1], 'name': r[2]})
bs.logout()

print(f'全市场股票总数: {len(stocks)}')

st_stocks = [s for s in stocks if 'ST' in s['name'] or '*' in s['name']]
print(f'ST股: {len(st_stocks)}只')

clean = [s for s in stocks if 'ST' not in s['name'] and '*' not in s['name']]
print(f'非ST股: {len(clean)}只')

# 用关键词识别行业
SECTOR_KEYWORDS = {
    '医药生物': ['制药','药业','医药','生物','医疗','健康','康','中药','胶囊','注射','药房','医科'],
    '食品饮料': ['食品','乳业','牛奶','饮料','调味','肉制','罐头','零食','酒','白酒','茅台','五粮','汾酒','青岛','燕京'],
    '电子': ['电子','光电','面板','LED','半导体','芯片','集成电路'],
    '计算机': ['软件','系统','网络','云','数据','信息','智控','智造'],
    '化工': ['化工','化学','新材','材料'],
    '机械设备': ['机械','重工','装备','机床','仪器'],
    '汽车': ['汽车','车企','部件','发动机','座椅'],
    '家用电器': ['家电','电器','空调','冰箱','洗衣机','厨电'],
    '电力设备': ['电力','电气','电池','储能','光伏','风电','核电'],
    '有色金属': ['有色','铜业','铝业','稀土','矿业','矿产'],
    '房地产': ['地产','房地产','万科','保利','金地','华侨城'],
    '银行': ['银行'],
    '非银金融': ['证券','保险','信托','基金'],
    '军工': ['军工','航空','航天','军工','国防'],
    '传媒': ['传媒','影视','文化','游戏','出版','广告'],
    '交通运输': ['航空','机场','航运','港口','物流','快递'],
    '建筑材料': ['建材','水泥','钢铁','螺纹'],
    '纺织服装': ['纺织','服装','鞋','家纺'],
    '轻工制造': ['轻工','造纸','包装','印刷'],
    '公用事业': ['水务','燃气','供热','环保'],
    '农林牧渔': ['农业','畜牧','养殖','饲料','种业','渔业'],
    '商贸零售': ['零售','超市','百货','商贸','贸易'],
    '煤炭': ['煤炭','煤业'],
    '石油': ['石油','油气'],
    '汽车服务': ['汽车服务','经销商'],
}

def guess_industry(name):
    for sector, kws in SECTOR_KEYWORDS.items():
        for kw in kws:
            if kw in name:
                return sector
    return '其他'

ind_count = Counter(guess_industry(s['name']) for s in clean)
print('\n全市场非ST股行业分布:')
for ind, cnt in ind_count.most_common():
    print(f'  {ind}: {cnt}只 ({cnt/len(clean)*100:.0f}%)')

# 筛选策略：每行业最多N只
MAX_PER_SECTOR = 15
selected = []
sector_used = Counter()
for s in clean:
    ind = guess_industry(s['name'])
    if sector_used[ind] < MAX_PER_SECTOR:
        selected.append(s)
        sector_used[ind] += 1

print(f'\n行业均衡筛选结果: {len(selected)}只')
for ind, cnt in sorted(sector_used.items()):
    print(f'  {ind}: {cnt}只')
