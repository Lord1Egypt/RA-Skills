#!/usr/bin/env python3
"""
v4.1 主线赛道识别引擎

铁律 1: 主线锁定原则
  • 板块指数持续创新高 + 回调小 + 修复快
  • 板块内批量翻倍股 + 龙头梯队
  • 消息面持续利好 + 行业景气度向上

输出:
  • 主线板块（置信度评分）
  • 龙头梯队（一/二/三线）
  • 支线板块（不重仓）
"""
import json
import urllib.request
import re
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent
UNIVERSE_PATH = ROOT / "configs" / "universe.json"


def fetch_quote(code):
    sym = ('sz' if code.startswith(('0', '3')) else 'sh') + code
    url = f"https://qt.gtimg.cn/q={sym}"
    try:
        req = urllib.request.Request(url, headers={'Referer': 'https://gu.qq.com/'})
        with urllib.request.urlopen(req, timeout=8) as r:
            text = r.read().decode('gbk', errors='ignore')
        p = text.split('~')
        if len(p) < 50: return None
        return {
            'name': p[1], 'price': float(p[3]), 'prev': float(p[4]),
            'change_pct': float(p[32]) if p[32] else 0,
            'turnover_rate': float(p[38]) if p[38] else 0,
            'vol_ratio': float(p[49]) if len(p) > 49 and p[49] else 0,
            'market_cap': float(p[44]) if p[44] else 0,
            'turnover_amount': float(p[37]) if p[37] else 0,
        }
    except: return None


def fetch_kline_recent(code, n=10):
    """拉最近 N 天 K 线，简化数据"""
    sym = ('sz' if code.startswith(('0', '3')) else 'sh') + code
    url = f"https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param={sym},day,,,{n+5},qfq"
    try:
        req = urllib.request.Request(url, headers={'Referer': 'https://gu.qq.com/'})
        with urllib.request.urlopen(req, timeout=10) as r:
            text = r.read().decode('utf-8', errors='ignore')
        text = re.sub(r'^[\s\S]*?=\s*', '', text).rstrip(';)')
        inner = json.loads(text).get('data', {}).get(sym, {})
        for k in ['qfqday', 'day']:
            if k in inner and inner[k]: return inner[k][-n:]
    except: pass
    return []


def analyze_board(stocks_in_board):
    """分析一个板块"""
    quotes = []
    for stock in stocks_in_board:
        q = fetch_quote(stock['code'])
        if not q: continue
        kline = fetch_kline_recent(stock['code'], 10)
        q['code'] = stock['code']
        q['tag'] = stock.get('tag', '')
        q['kline'] = kline
        quotes.append(q)
    
    if not quotes:
        return None
    
    # 板块指标计算
    n = len(quotes)
    avg_chg_today = sum(q['change_pct'] for q in quotes) / n
    
    # 计算 5 日累计涨幅
    chgs_5d = []
    new_high_count = 0  # 5 日内创新高个数
    big_gain_count = 0  # 5 日内 涨幅>15% 个数
    
    for q in quotes:
        if not q['kline'] or len(q['kline']) < 5:
            continue
        closes = [float(r[2]) for r in q['kline'][-5:]]
        if len(closes) >= 5:
            chg_5d = (closes[-1] - closes[0]) / closes[0] * 100
            chgs_5d.append(chg_5d)
            
            # 看是否 5 日内 创新高
            highs = [float(r[3]) for r in q['kline']]
            if len(highs) >= 10 and max(highs[-3:]) >= max(highs):
                new_high_count += 1
            
            # 大涨股
            if chg_5d > 15:
                big_gain_count += 1
    
    avg_chg_5d = sum(chgs_5d) / len(chgs_5d) if chgs_5d else 0
    
    # 龙头梯队识别 (按今日成交额 + 涨幅排序)
    sorted_quotes = sorted(quotes, key=lambda x: -(x.get('turnover_amount', 0)))
    leaders = sorted_quotes[:min(3, len(sorted_quotes))]
    
    return {
        'count': n,
        'avg_chg_today': round(avg_chg_today, 2),
        'avg_chg_5d': round(avg_chg_5d, 2),
        'new_high_count': new_high_count,
        'big_gain_count': big_gain_count,
        'leaders': leaders,
        'all_quotes': quotes,
    }


def calc_main_line_score(board_analysis):
    """计算主线置信度评分（0-100）
    
    三大标准:
      ① 板块指数持续创新高 + 回调小（30 分）
      ② 板块内批量翻倍/大涨股（30 分）
      ③ 龙头梯队 + 持续性（40 分）
    """
    if not board_analysis:
        return 0
    
    score = 0
    
    # 维度 1: 板块指数持续性（30 分）
    avg_5d = board_analysis['avg_chg_5d']
    if avg_5d > 15:
        score += 30
    elif avg_5d > 10:
        score += 25
    elif avg_5d > 5:
        score += 18
    elif avg_5d > 0:
        score += 10
    
    # 维度 2: 批量大涨股（30 分）
    big_gain = board_analysis['big_gain_count']
    total = board_analysis['count']
    big_gain_ratio = big_gain / total if total else 0
    if big_gain_ratio > 0.5:
        score += 30  # 一半以上大涨
    elif big_gain_ratio > 0.3:
        score += 22
    elif big_gain_ratio > 0.15:
        score += 15
    elif big_gain_ratio > 0:
        score += 8
    
    # 维度 3: 龙头梯队（40 分）
    new_high = board_analysis['new_high_count']
    new_high_ratio = new_high / total if total else 0
    if new_high_ratio > 0.5:
        score += 40
    elif new_high_ratio > 0.3:
        score += 30
    elif new_high_ratio > 0.15:
        score += 20
    elif new_high_ratio > 0:
        score += 10
    
    return score


def identify_dragon_tier(quotes_in_board):
    """龙头梯队识别"""
    if not quotes_in_board:
        return {}
    
    # 按 综合指标 排序
    # 综合指标 = 流通市值 + 今日成交额 + 5日涨幅
    scored = []
    for q in quotes_in_board:
        if not q.get('kline') or len(q['kline']) < 5:
            chg_5d = 0
        else:
            closes = [float(r[2]) for r in q['kline'][-5:]]
            chg_5d = (closes[-1] - closes[0]) / closes[0] * 100 if closes[0] > 0 else 0
        
        # 龙头分数
        leader_score = (
            q.get('turnover_amount', 0) / 1e8 * 1.0 +  # 成交额（亿）
            q.get('market_cap', 0) * 0.05 +           # 流通市值（亿）* 0.05
            chg_5d * 2                                 # 5 日涨幅 * 2
        )
        scored.append({**q, 'leader_score': leader_score, 'chg_5d': chg_5d})
    
    scored.sort(key=lambda x: -x['leader_score'])
    
    n = len(scored)
    tier1 = scored[:min(2, n)]  # 一线龙头 (前 2)
    tier2 = scored[2:min(5, n)]  # 二线 (3-5)
    tier3 = scored[5:]           # 三线 (6+)
    
    return {
        'tier1': tier1,
        'tier2': tier2,
        'tier3': tier3,
    }


def scan_main_lines():
    """扫描所有板块，识别主线"""
    with open(UNIVERSE_PATH, encoding='utf-8') as f:
        universe = json.load(f)
    
    results = []
    print(f"\n🔍 扫描 {len(universe['themes'])} 个板块...\n")
    
    for theme, theme_data in universe['themes'].items():
        analysis = analyze_board(theme_data['stocks'])
        if not analysis:
            continue
        
        score = calc_main_line_score(analysis)
        tier = identify_dragon_tier(analysis['all_quotes'])
        
        # 主线判定
        if score >= 70:
            classification = '🥇 主线'
        elif score >= 50:
            classification = '🥈 次主线'
        elif score >= 30:
            classification = '🟡 支线'
        else:
            classification = '❌ 冷门'
        
        results.append({
            'theme': theme,
            'weight': theme_data.get('weight', 1.0),
            'score': score,
            'classification': classification,
            'analysis': analysis,
            'tier': tier,
        })
        
        print(f"  ✅ {theme}: {classification} ({score} 分)")
    
    results.sort(key=lambda x: -x['score'])
    return results


def format_main_line_report(results):
    """格式化输出"""
    lines = []
    lines.append("=" * 75)
    lines.append(f"📊 主线赛道识别 · 北京时间 {datetime.now():%Y-%m-%d %H:%M}")
    lines.append("=" * 75)
    
    main_lines = [r for r in results if r['score'] >= 70]
    sub_lines = [r for r in results if 50 <= r['score'] < 70]
    branch_lines = [r for r in results if r['score'] < 50]
    
    # 主线
    if main_lines:
        lines.append("\n🥇 主线赛道 (锁定 + 重仓):")
        for r in main_lines:
            lines.append(f"\n  📊 {r['theme']} (置信度: {r['score']} 分)")
            lines.append(f"     今日 {r['analysis']['avg_chg_today']:+.2f}% / 5日 {r['analysis']['avg_chg_5d']:+.2f}%")
            lines.append(f"     大涨股 {r['analysis']['big_gain_count']} / 创新高 {r['analysis']['new_high_count']}")
            if r['tier'].get('tier1'):
                lines.append(f"     🥇 一线龙头: " + ", ".join([f"{q['name']}({q['change_pct']:+.1f}%)" for q in r['tier']['tier1']]))
            if r['tier'].get('tier2'):
                lines.append(f"     🥈 二线跟随: " + ", ".join([f"{q['name']}({q['change_pct']:+.1f}%)" for q in r['tier']['tier2']]))
    else:
        lines.append("\n🥇 主线赛道: 暂无（市场无明确主线）")
    
    # 次主线
    if sub_lines:
        lines.append("\n🥈 次主线 (轻仓参与):")
        for r in sub_lines[:5]:
            lines.append(f"  • {r['theme']} ({r['score']} 分) {r['analysis']['avg_chg_today']:+.2f}% / 5日 {r['analysis']['avg_chg_5d']:+.2f}%")
    
    # 支线
    if branch_lines:
        lines.append("\n🟡 支线/冷门 (不重仓):")
        for r in branch_lines[:5]:
            lines.append(f"  • {r['theme']} ({r['score']} 分)")
    
    # 操作建议
    lines.append("\n" + "=" * 75)
    lines.append("💡 操作建议（按金融博士铁律 1）:")
    if main_lines:
        lines.append(f"  ✅ 锁定主线: {', '.join([r['theme'] for r in main_lines])}")
        lines.append(f"  ✅ 围绕主线龙头 低吸布局")
        lines.append(f"  ❌ 非主线板块 不要重仓")
    else:
        lines.append(f"  ⚠️ 当前无明确主线 → 仓位 ≤ 30%")
    
    return "\n".join(lines)


def main():
    results = scan_main_lines()
    print()
    print(format_main_line_report(results))
    
    # 保存
    out_dir = ROOT / "data" / "reports"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"main_line_{datetime.now():%Y%m%d_%H%M}.json"
    with open(out_file, 'w', encoding='utf-8') as f:
        # 简化保存
        simplified = []
        for r in results:
            simplified.append({
                'theme': r['theme'],
                'score': r['score'],
                'classification': r['classification'],
                'avg_chg_today': r['analysis']['avg_chg_today'],
                'avg_chg_5d': r['analysis']['avg_chg_5d'],
                'big_gain_count': r['analysis']['big_gain_count'],
                'new_high_count': r['analysis']['new_high_count'],
                'tier1': [q['name'] for q in r['tier'].get('tier1', [])],
                'tier2': [q['name'] for q in r['tier'].get('tier2', [])],
            })
        json.dump(simplified, f, ensure_ascii=False, indent=2)
    
    return results


if __name__ == '__main__':
    main()
