"""
v2.6 多维分析模块
七个维度：基本面 / 估值面 / 技术面 / 情绪面 / 资金面 / 题材面 / 事件面

不依赖外部 SDK，纯 stdlib + TinyFish Search
"""
import urllib.parse, urllib.request, json, os, re
from datetime import datetime


def _key():
    """加载 TinyFish key"""
    try:
        with open('/home/work/.openclaw/secrets/tinyfish.env') as f:
            for line in f:
                if line.startswith('TINYFISH_API_KEY='):
                    return line.split('=', 1)[1].strip()
    except Exception:
        return None
    return None


def _search(query, top=5):
    """搜索 TinyFish"""
    key = _key()
    if not key:
        return []
    try:
        url = f'https://api.search.tinyfish.ai?query={urllib.parse.quote(query)}'
        req = urllib.request.Request(url, headers={'X-API-Key': key})
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read().decode('utf-8')).get('results', [])[:top]
    except Exception:
        return []


def _has(s, kws):
    """是否包含任一关键词"""
    return any(kw in s for kw in kws)


def scan_dimensions(code, name):
    """七维扫描，返回 dict"""
    out = {
        'fundamentals': [],
        'valuation': [],
        'sentiment': [],
        'capital_flow': [],
        'catalysts': [],
        'risk_events': [],
    }
    
    # 维度1: 基本面（业绩 / 营收 / 净利润）
    for q in [f'{name} 业绩 一季度', f'{name} 营收 净利润']:
        for r in _search(q, top=3):
            t, s = r.get('title', ''), r.get('snippet', '')
            if _has(t+s, ['亏损', '增亏', '下降', '减少', '业绩预减']):
                out['fundamentals'].append({'signal': 'bearish', 'text': t[:80], 'detail': s[:200]})
            elif _has(t+s, ['超预期', '大幅增长', '同比增', '净利润增长']):
                out['fundamentals'].append({'signal': 'bullish', 'text': t[:80], 'detail': s[:200]})
            if out['fundamentals']: break
    
    # 维度2: 估值
    for q in [f'{name} 估值 高', f'{name} PE 市盈率']:
        for r in _search(q, top=3):
            t, s = r.get('title', ''), r.get('snippet', '')
            if _has(t+s, ['估值高', '泡沫', '透支', '看不懂', '炒作', '断层']):
                out['valuation'].append({'signal': 'bearish', 'text': t[:80], 'detail': s[:200]})
                break
            elif _has(t+s, ['估值合理', '低估', '估值修复']):
                out['valuation'].append({'signal': 'bullish', 'text': t[:80], 'detail': s[:200]})
                break
    
    # 维度3: 情绪面（板块情绪、连板、龙虎榜）
    for q in [f'{name} 板块 龙头', f'{name} 涨停', f'{name} 龙虎榜']:
        for r in _search(q, top=3):
            t, s = r.get('title', ''), r.get('snippet', '')
            if _has(t+s, ['涨停', '主升', '走强', '板块龙头', '主力买入']):
                out['sentiment'].append({'signal': 'bullish', 'text': t[:80]})
            elif _has(t+s, ['杀跌', '回调', '冲高回落', '滞涨']):
                out['sentiment'].append({'signal': 'bearish', 'text': t[:80]})
            if out['sentiment']: break
    
    # 维度4: 资金面（主力 / 北上 / 机构）
    for q in [f'{name} 主力资金 流入', f'{name} 主力 净流出', f'{name} 北上 增持']:
        for r in _search(q, top=3):
            t, s = r.get('title', ''), r.get('snippet', '')
            if _has(t+s, ['净流出', '资金外逃', '抛压', '减持']):
                # 提取金额
                m = re.search(r'净流出[\D]*(\d+\.?\d*)[\D]*亿', s)
                amount = f"{m.group(1)}亿" if m else "未知"
                out['capital_flow'].append({'signal': 'bearish', 'text': t[:80], 'amount': amount, 'detail': s[:200]})
            elif _has(t+s, ['净流入', '增持', '加仓', '买入']):
                m = re.search(r'净流入[\D]*(\d+\.?\d*)[\D]*亿', s)
                amount = f"{m.group(1)}亿" if m else "未知"
                out['capital_flow'].append({'signal': 'bullish', 'text': t[:80], 'amount': amount, 'detail': s[:200]})
            if len(out['capital_flow']) >= 2: break
    
    # 维度5: 题材催化
    for q in [f'{name} 利好', f'{name} 订单', f'{name} 中标', f'{name} 机构调研']:
        for r in _search(q, top=2):
            t, s = r.get('title', ''), r.get('snippet', '')
            if _has(t+s, ['中标', '订单', '签约', '合同', '利好', '催化', '调研', '机构看好']):
                out['catalysts'].append({'signal': 'bullish', 'text': t[:80], 'detail': s[:150]})
                break
    
    # 维度6: 风险事件
    for q in [f'{name} 减持', f'{name} 解禁', f'{name} 处罚', f'{name} 立案']:
        for r in _search(q, top=2):
            t, s = r.get('title', ''), r.get('snippet', '')
            if _has(t+s, ['减持', '解禁', '处罚', '调查', '立案', '警示']):
                out['risk_events'].append({'signal': 'bearish', 'text': t[:80], 'detail': s[:150]})
                break
    
    return out


def score_dimension(items, weight_bullish=1, weight_bearish=-1):
    """单维度评分：+ 看多 / - 看空"""
    score = 0
    for it in items:
        if it.get('signal') == 'bullish':
            score += weight_bullish
        elif it.get('signal') == 'bearish':
            score += weight_bearish
    return score


def assess_stock(code, name):
    """综合评估，返回评分 + 建议"""
    dims = scan_dimensions(code, name)
    
    # 各维度评分
    scores = {
        'fundamentals': score_dimension(dims['fundamentals']) * 2,  # 基本面权重高
        'valuation': score_dimension(dims['valuation']) * 1.5,
        'sentiment': score_dimension(dims['sentiment']),
        'capital_flow': score_dimension(dims['capital_flow']) * 2,  # 资金面权重高
        'catalysts': score_dimension(dims['catalysts']),
        'risk_events': score_dimension(dims['risk_events']) * 1.5,  # 风险事件权重高
    }
    
    total = sum(scores.values())
    
    # 建议
    if total >= 3:
        rec = '🚀 强买 / 加仓'
    elif total >= 1:
        rec = '✅ 持有 / 观察'
    elif total >= -2:
        rec = '⚠️ 谨慎 / 减仓部分'
    elif total >= -5:
        rec = '🚨 强减 / 减仓 50%+'
    else:
        rec = '🚨🚨 立刻清仓'
    
    return {
        'code': code,
        'name': name,
        'scores': scores,
        'total': total,
        'recommendation': rec,
        'details': dims,
    }


if __name__ == '__main__':
    import sys
    if len(sys.argv) >= 3:
        result = assess_stock(sys.argv[1], sys.argv[2])
    else:
        # demo: 罗博特科
        result = assess_stock('300757', '罗博特科')
    
    print(f"\n{'='*60}")
    print(f"📊 多维分析: {result['name']} ({result['code']})")
    print(f"{'='*60}")
    print(f"\n各维度评分:")
    for dim, score in result['scores'].items():
        bar = '█' * abs(int(score)) if score != 0 else ''
        sign = '+' if score >= 0 else ''
        print(f"  {dim:<20} {sign}{score:>+.1f}  {bar}")
    print(f"\n  {'总评分':<20} {result['total']:+.1f}")
    print(f"\n📋 建议: {result['recommendation']}")
    print(f"\n详细信息:")
    for dim, items in result['details'].items():
        if items:
            print(f"\n  📍 {dim}:")
            for it in items[:2]:
                sig = '🟢' if it.get('signal')=='bullish' else '🔴'
                print(f"    {sig} {it.get('text', '')[:70]}")
                if it.get('detail'):
                    print(f"       {it['detail'][:120]}")
