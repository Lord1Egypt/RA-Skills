"""
v2.7 业绩深度分析模块（用户教训）

不能简单看"业绩亏损"就判 bearish
必须深挖：
1. 扣非净利 趋势
2. 亏损原因（结构性 vs 战略性）
3. 在手订单（持续大额订单 = 优先利好）
4. 客户质量
5. 业务结构变化

核心判断逻辑：
- 旧业务衰退 + 新业务订单堆积 + 顶级客户 = 切换期，可看多
- 旧业务衰退 + 新业务订单不足 = 结构性问题，看空
- 单纯研发投入大但订单跟上 = 战略性亏损，看多
"""
import urllib.parse, urllib.request, json, re

def _key():
    try:
        with open('/home/work/.openclaw/secrets/tinyfish.env') as f:
            for line in f:
                if line.startswith('TINYFISH_API_KEY='):
                    return line.split('=', 1)[1].strip()
    except:
        return None

def _search(query, top=5):
    key = _key()
    if not key: return []
    try:
        url = f'https://api.search.tinyfish.ai?query={urllib.parse.quote(query)}'
        req = urllib.request.Request(url, headers={'X-API-Key': key})
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read().decode('utf-8')).get('results', [])[:top]
    except:
        return []


def analyze_business_quality(code, name):
    """业绩质量深度分析"""
    result = {
        'revenue_trend': '',     # 营收趋势
        'profit_truth': '',      # 真实利润（扣非）
        'loss_reason': '',       # 亏损原因
        'orders': [],            # 在手订单 / 大额订单
        'customer_quality': [],  # 客户质量
        'business_structure': '', # 业务结构变化
        'verdict': '',           # 综合判断
        'score_adjustment': 0,   # 评分修正（-3 ~ +5）
    }
    
    # 1. 营收 + 扣非净利
    for q in [f'{name} 营收 扣非净利', f'{name} 扣非归母净利润']:
        for r in _search(q, top=3):
            s = r.get('snippet', '')
            # 营收同比
            m = re.search(r'营业?收入[^，。]*?(\d+\.?\d*)亿[^，。]*?同比(增长|增加|下滑|减少)?[\D]*?(\d+\.?\d*)%', s)
            if m:
                trend = '+' if m.group(2) in ('增长', '增加') else '-'
                result['revenue_trend'] = f"营收 {m.group(1)}亿 同比{trend}{m.group(3)}%"
            # 扣非
            m2 = re.search(r'扣非[^，。]*?(-?\d+\.?\d*)[万亿]', s)
            if m2:
                result['profit_truth'] = f"扣非净利 {m2.group(0)}"
            if result['revenue_trend'] and result['profit_truth']: break
        if result['revenue_trend']: break
    
    # 2. 亏损原因
    for q in [f'{name} 亏损 原因', f'{name} 业绩 下滑 原因']:
        for r in _search(q, top=3):
            s = r.get('snippet', '')[:500]
            # 战略性投入
            if any(k in s for k in ['研发投入', '加大投入', '战略转型', '并购整合', '业务切换']):
                result['loss_reason'] = '战略性投入'
                result['score_adjustment'] += 2  # 战略性亏损不扣分
            # 结构性问题
            elif any(k in s for k in ['毛利率下降', '订单减少', '行业下行', '需求萎缩', '产能过剩', '盈利能力弱']):
                result['loss_reason'] = '结构性问题'
                result['score_adjustment'] -= 3
            if result['loss_reason']: break
        if result['loss_reason']: break
    
    # 3. 在手订单（最重要）
    for q in [f'{name} 在手订单', f'{name} 累计 订单 亿', f'{name} 新签订单']:
        for r in _search(q, top=4):
            t = r.get('title', '')
            s = r.get('snippet', '')[:400]
            # 提取订单金额
            m = re.search(r'(订单|合同|签约)[^，。]*?(\d+\.?\d*)\s*(亿|万)\s*(元|欧元)', s)
            if m:
                result['orders'].append({
                    'amount': f"{m.group(2)}{m.group(3)}{m.group(4)}",
                    'source': t[:60]
                })
                result['score_adjustment'] += 1  # 每条大额订单 +1
        if len(result['orders']) >= 3: break
    
    # 4. 客户质量（顶级客户 = 大利好）
    top_customers = ['英伟达', '台积电', '英特尔', '博通', '微软', '苹果', '华为', '中芯国际', 
                     'NVIDIA', 'TSMC', 'Intel', 'Broadcom', 'Microsoft', 'Apple', 'Huawei',
                     '宁德时代', '比亚迪', '特斯拉']
    for q in [f'{name} 客户', f'{name} 大客户']:
        for r in _search(q, top=3):
            s = r.get('title', '') + r.get('snippet', '')
            for c in top_customers:
                if c in s and c not in [x.get('name') for x in result['customer_quality']]:
                    result['customer_quality'].append({'name': c, 'evidence': s[:150]})
                    result['score_adjustment'] += 1.5  # 顶级客户 +1.5
            if len(result['customer_quality']) >= 4: break
    
    # 5. 综合判断
    if result['loss_reason'] == '结构性问题' and not result['orders']:
        result['verdict'] = '❌ 结构性问题 + 无大订单 = 真正的烂公司'
    elif result['loss_reason'] == '结构性问题' and len(result['orders']) >= 2:
        result['verdict'] = '⚠️ 旧业务塌陷 + 新业务订单 = 切换期，关键看转化'
    elif result['loss_reason'] == '战略性投入' and len(result['orders']) >= 2:
        result['verdict'] = '✅ 战略性亏损 + 订单饱满 = 优质成长股'
    elif result['loss_reason'] == '战略性投入':
        result['verdict'] = '⚠️ 战略性投入但订单不明 = 看后续兑现'
    else:
        result['verdict'] = '➖ 信息不足，需要继续观察'
    
    return result


if __name__ == '__main__':
    import sys
    code = sys.argv[1] if len(sys.argv) > 1 else '300757'
    name = sys.argv[2] if len(sys.argv) > 2 else '罗博特科'
    
    print("="*60)
    print(f"📊 业绩质量深度分析: {name} ({code})")
    print("="*60)
    r = analyze_business_quality(code, name)
    print(f"\n营收趋势: {r['revenue_trend']}")
    print(f"真实利润: {r['profit_truth']}")
    print(f"亏损原因: {r['loss_reason']}")
    print(f"\n在手订单 ({len(r['orders'])}条):")
    for o in r['orders']:
        print(f"  ✅ {o['amount']}  来源: {o['source'][:50]}")
    print(f"\n顶级客户 ({len(r['customer_quality'])}个):")
    for c in r['customer_quality']:
        print(f"  ⭐ {c['name']}")
    print(f"\n综合判断: {r['verdict']}")
    print(f"评分修正: {r['score_adjustment']:+.1f}")
