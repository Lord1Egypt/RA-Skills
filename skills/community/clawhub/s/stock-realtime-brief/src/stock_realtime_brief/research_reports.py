#!/usr/bin/env python3
"""
v2.8 研报抓取模块

支持：
- 机构评级（买入/增持/中性/减持/卖出）
- 目标价（均值/最高/最低）
- 分析师 + 所属机构
- 业绩预测
- 评级一致性 / 变化趋势
"""
import urllib.parse, urllib.request, json, re, os
from datetime import datetime


def _key():
    try:
        with open('/home/work/.openclaw/secrets/tinyfish.env') as f:
            for line in f:
                if line.startswith('TINYFISH_API_KEY='):
                    return line.split('=', 1)[1].strip()
    except:
        return None


def _search(query, top=8):
    key = _key()
    if not key: return []
    try:
        url = f'https://api.search.tinyfish.ai?query={urllib.parse.quote(query)}'
        req = urllib.request.Request(url, headers={'X-API-Key': key})
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read().decode('utf-8')).get('results', [])[:top]
    except:
        return []


# 评级关键词分级
RATING_BULLISH = ['买入', '强烈推荐', '推荐', '强力买入']
RATING_NEUTRAL_POSITIVE = ['增持', '审慎推荐']
RATING_NEUTRAL = ['中性', '持有', '观望']
RATING_BEARISH = ['减持', '回避', '卖出', '强烈卖出']

# 主流券商列表
MAJOR_BROKERS = [
    '中信证券', '国泰君安', '海通证券', '招商证券', '广发证券', '中信建投',
    '华泰证券', '兴业证券', '申万宏源', '国信证券', '光大证券', '东兴证券',
    '东方证券', '东吴证券', '国金证券', '安信证券', '华西证券', '中金公司',
    '华鑫证券', '财通证券', '方正证券', '西南证券', '天风证券', '民生证券',
    '中泰证券', '长江证券', '银河证券', '海通国际', '德邦证券',
]


def fetch_research_reports(code, name):
    """抓取个股研报数据
    
    返回:
        {
            'avg_target_price': 平均目标价,
            'max_target': 最高,
            'min_target': 最低,
            'analyst_count': 覆盖分析师数,
            'rating_summary': 评级分布,
            'consensus': 综合评级,
            'upside_pct': 上涨空间%,
            'recent_reports': [研报清单],
            'brokers': [覆盖券商],
            'has_recent_downgrade': 是否有近期降级,
            'has_recent_upgrade': 是否有近期升级,
        }
    """
    result = {
        'avg_target_price': None,
        'max_target': None,
        'min_target': None,
        'analyst_count': 0,
        'rating_summary': {},
        'consensus': None,
        'upside_pct': None,
        'recent_reports': [],
        'brokers': set(),
        'has_recent_downgrade': False,
        'has_recent_upgrade': False,
    }
    
    queries = [
        f'{name} 研报 评级',
        f'{name} 目标价 券商',
        f'{name} 研报 2026',
        f'{code} 研究报告',
        f'{name} 买入评级 机构',
        f'{name} 高盛 目标价',           # v2.8: 找外资大行
        f'{name} 中信 国君 海通 评级',   # v2.8: 找头部券商
    ]
    
    all_results = []
    for q in queries:
        all_results.extend(_search(q, top=5))
    
    # 去重
    seen_urls = set()
    unique_results = []
    for r in all_results:
        u = r.get('url', '')
        if u and u not in seen_urls:
            seen_urls.add(u)
            unique_results.append(r)
    
    # 解析
    for r in unique_results:
        title = r.get('title', '')
        snippet = r.get('snippet', '')
        url = r.get('url', '')
        combined = title + ' ' + snippet
        
        # 1. 提取目标价（v2.8 优化：多模式 + 合理验证）
        target_prices_found = []
        for pattern in [
            # "目标价688 元" / "目标价 ¥688" / "目标价：688"
            r'目标价[^,。\d]{0,20}?(\d{2,5}\.?\d*)\s*元',
            r'目标价[^,。\d]{0,5}?(?:CNY|￥|¥)?\s*(\d{2,5}\.?\d*)\s*(?:[,，。\s元])',
            # "688 元目标价"  (前置数字)
            r'(\d{2,5}\.?\d*)\s*元\s*目标价',
            # "12 个月平均目标价为 CNY688"
            r'12.个月\s*平均\s*目标价[\s\S]{0,15}?(?:CNY|￥|¥)?\s*(\d{2,5}\.?\d*)',
            # "买入，目标价688 元"
            r'(?:买入|增持|强买)[，,]\s*目标价[^,。\d]{0,5}(\d{2,5}\.?\d*)',
            # "看高至 688" / "估值 688"
            r'(?:看高至|看至|估值)\s*(?:CNY|￥|¥)?\s*(\d{2,5}\.?\d*)',
            # 列出多个目标价 "有688、710、888"
            r'(?:有|含|为)\s*(\d{2,5}\.?\d*)[、，,]',
        ]:
            for m in re.finditer(pattern, combined):
                try:
                    price = float(m.group(1))
                    if 30 <= price <= 3000:
                        target_prices_found.append(price)
                except:
                    pass
        
        # 汇总目标价：取众数/中位数防止异常值
        if target_prices_found:
            # 去重 + 排序
            unique_prices = sorted(set(target_prices_found))
            for p in unique_prices:
                if not result['avg_target_price']:
                    result['avg_target_price'] = p
                if not result['max_target'] or p > result['max_target']:
                    result['max_target'] = p
                if not result['min_target'] or p < result['min_target']:
                    result['min_target'] = p
            # 平均价取中位数（防极端值）
            mid = unique_prices[len(unique_prices)//2]
            result['avg_target_price'] = mid
        
        # 2. 提取分析师数
        m = re.search(r'(\d+)\s*名?\s*分析师', combined)
        if m:
            n = int(m.group(1))
            if n > result['analyst_count']:
                result['analyst_count'] = n
        
        # 3. 评级分布
        for kw in RATING_BULLISH:
            if kw in combined:
                result['rating_summary'][kw] = result['rating_summary'].get(kw, 0) + 1
        for kw in RATING_NEUTRAL_POSITIVE:
            if kw in combined:
                result['rating_summary'][kw] = result['rating_summary'].get(kw, 0) + 1
        for kw in RATING_NEUTRAL:
            if kw in combined:
                result['rating_summary'][kw] = result['rating_summary'].get(kw, 0) + 1
        for kw in RATING_BEARISH:
            if kw in combined:
                result['rating_summary'][kw] = result['rating_summary'].get(kw, 0) + 1
        
        # 4. 覆盖券商
        for broker in MAJOR_BROKERS:
            if broker in combined:
                result['brokers'].add(broker)
        
        # 5. 综合评级
        m = re.search(r'整体评级[^,，。]*?(强力买入|买入|增持|中性|持有|减持|卖出)', combined)
        if m:
            result['consensus'] = m.group(1)
        
        # 6. 上涨空间
        m = re.search(r'(?:具有|预期)[+\-]?\s*(\d+\.?\d*)%?\s*(?:看涨|上涨|空间|潜力)', combined)
        if m:
            result['upside_pct'] = float(m.group(1))
        
        # 7. 升降级信号
        if '下调' in combined and ('目标价' in combined or '评级' in combined):
            result['has_recent_downgrade'] = True
        if ('上调' in combined or '调高') in combined and ('目标价' in combined or '评级' in combined):
            result['has_recent_upgrade'] = True
        
        # 8. 收集研报清单（前 5 条）
        if len(result['recent_reports']) < 5:
            if any(kw in combined for kw in ['研报', '研究报告', '评级', '目标价']):
                result['recent_reports'].append({
                    'title': title[:80],
                    'source': r.get('site_name', ''),
                    'url': url[:100],
                    'snippet': snippet[:200],
                })
    
    # 综合评级（如果没识别到，按计数推断）
    if not result['consensus'] and result['rating_summary']:
        bullish = sum(v for k, v in result['rating_summary'].items() if k in RATING_BULLISH)
        bearish = sum(v for k, v in result['rating_summary'].items() if k in RATING_BEARISH)
        if bullish > bearish * 2:
            result['consensus'] = '买入'
        elif bullish > bearish:
            result['consensus'] = '增持'
        elif bearish > bullish:
            result['consensus'] = '减持'
        else:
            result['consensus'] = '中性'
    
    result['brokers'] = sorted(result['brokers'])
    return result


def format_report_summary(result, current_price=None):
    """格式化输出"""
    lines = []
    lines.append("## 📊 机构研报观点")
    lines.append("")
    
    if result.get('avg_target_price'):
        tgt = result['avg_target_price']
        space = ''
        if current_price:
            pct = (tgt - current_price) / current_price * 100
            arrow = '↑' if pct > 0 else '↓'
            space = f" ({arrow}{abs(pct):.1f}%)"
        lines.append(f"- 🎯 **目标价**: ¥{tgt:.0f}{space}")
        if result.get('max_target') and result.get('min_target') and result['max_target'] != result['min_target']:
            lines.append(f"  - 区间: ¥{result['min_target']:.0f} ~ ¥{result['max_target']:.0f}")
    
    if result.get('consensus'):
        cmap = {
            '强力买入': '🚀 强力买入', '买入': '✅ 买入', '增持': '🟢 增持',
            '中性': '⚖️ 中性', '持有': '🟡 持有', '减持': '⚠️ 减持',
            '卖出': '🔴 卖出',
        }
        lines.append(f"- 综合评级: **{cmap.get(result['consensus'], result['consensus'])}**")
    
    if result.get('analyst_count'):
        lines.append(f"- 分析师覆盖: **{result['analyst_count']}** 名")
    
    if result.get('upside_pct'):
        lines.append(f"- 上涨空间: **+{result['upside_pct']:.1f}%**")
    
    if result.get('brokers'):
        lines.append(f"- 覆盖券商 ({len(result['brokers'])}家): {', '.join(result['brokers'][:5])}{'...' if len(result['brokers']) > 5 else ''}")
    
    if result.get('rating_summary'):
        rs = result['rating_summary']
        items = [f"{k}×{v}" for k, v in sorted(rs.items(), key=lambda x: -x[1])][:4]
        if items:
            lines.append(f"- 评级分布: {' | '.join(items)}")
    
    if result.get('has_recent_downgrade'):
        lines.append(f"- ⚠️ **检测到近期评级/目标价下调**")
    if result.get('has_recent_upgrade'):
        lines.append(f"- ✅ **检测到近期评级/目标价上调**")
    
    if result.get('recent_reports'):
        lines.append(f"")
        lines.append(f"### 近期研报")
        for r in result['recent_reports'][:3]:
            lines.append(f"- 📰 {r['title']}")
            if r.get('snippet'):
                lines.append(f"  > {r['snippet'][:120]}")
    
    return '\n'.join(lines)


if __name__ == '__main__':
    import sys
    code = sys.argv[1] if len(sys.argv) > 1 else '300757'
    name = sys.argv[2] if len(sys.argv) > 2 else '罗博特科'
    price = float(sys.argv[3]) if len(sys.argv) > 3 else None
    
    print(f"\n{'='*60}")
    print(f"📊 研报扫描: {name} ({code})")
    print(f"{'='*60}\n")
    r = fetch_research_reports(code, name)
    print(format_report_summary(r, current_price=price))
