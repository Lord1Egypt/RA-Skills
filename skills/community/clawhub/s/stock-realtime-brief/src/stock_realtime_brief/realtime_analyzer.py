#!/usr/bin/env python3
"""
v3.0 盘中实时量价分析模块

核心方法论（用户指导）：
- 盘中实时 ≠ 周期分析
- 重点落在量价关系
- 维度：技术、资金、板块、量价

不谈月/周线趋势，只谈当下盘面的状态、可能趋势、立刻可做的策略
"""
import urllib.request, json, re
from typing import Optional


def fetch_realtime_full(code: str) -> dict:
    """从腾讯拉完整盘口数据（含五档买卖、内外盘、量比等）"""
    sym = ('sz' if code.startswith(('0', '3')) else 'sh') + code
    url = f"https://qt.gtimg.cn/q={sym}"
    try:
        req = urllib.request.Request(url, headers={'Referer': 'https://gu.qq.com/'})
        with urllib.request.urlopen(req, timeout=10) as r:
            text = r.read().decode('gbk', errors='ignore')
        parts = text.split('~')
        if len(parts) < 50:
            return None
        return {
            'name': parts[1],
            'code': parts[2],
            'price': float(parts[3]),
            'prev_close': float(parts[4]),
            'open': float(parts[5]),
            'volume': int(parts[6]) if parts[6] else 0,
            'outer': int(parts[7]) if parts[7] else 0,
            'inner': int(parts[8]) if parts[8] else 0,
            'bid1_price': float(parts[9]), 'bid1_qty': int(parts[10]),
            'bid2_price': float(parts[11]), 'bid2_qty': int(parts[12]),
            'bid3_price': float(parts[13]), 'bid3_qty': int(parts[14]),
            'bid4_price': float(parts[15]), 'bid4_qty': int(parts[16]),
            'bid5_price': float(parts[17]), 'bid5_qty': int(parts[18]),
            'ask1_price': float(parts[19]), 'ask1_qty': int(parts[20]),
            'ask2_price': float(parts[21]), 'ask2_qty': int(parts[22]),
            'ask3_price': float(parts[23]), 'ask3_qty': int(parts[24]),
            'ask4_price': float(parts[25]), 'ask4_qty': int(parts[26]),
            'ask5_price': float(parts[27]), 'ask5_qty': int(parts[28]),
            'time': parts[30],
            'change': float(parts[31]) if parts[31] else 0,
            'change_pct': float(parts[32]) if parts[32] else 0,
            'high': float(parts[33]),
            'low': float(parts[34]),
            'turnover_wan': float(parts[37]) if parts[37] else 0,  # 万元
            'turnover_rate': float(parts[38]) if parts[38] else 0,  # %
            'amplitude': float(parts[43]) if parts[43] else 0,
            'circ_market_cap_yi': float(parts[44]) if parts[44] else 0,
            'total_market_cap_yi': float(parts[45]) if parts[45] else 0,
            'vol_ratio': float(parts[49]) if len(parts) > 49 and parts[49] else 0,
        }
    except Exception:
        return None


def fetch_intraday_kline(code: str, n: int = 240) -> list:
    """拉 1 分钟分时数据（最多 240 分钟 = 全天）"""
    sym = ('sz' if code.startswith(('0', '3')) else 'sh') + code
    url = f"https://web.ifzq.gtimg.cn/appstock/app/kline/mkline?param={sym},m1,,{n}"
    try:
        req = urllib.request.Request(url, headers={'Referer': 'https://gu.qq.com/'})
        with urllib.request.urlopen(req, timeout=10) as r:
            text = r.read().decode('utf-8', errors='ignore')
        text = re.sub(r'^[\s\S]*?=\s*', '', text).rstrip(';)')
        data = json.loads(text)
        inner = data.get('data', {}).get(sym, {})
        return inner.get('m1', [])
    except Exception:
        return []


def analyze_volume_price(realtime: dict, intraday: list = None) -> dict:
    """量价关系分析（核心）"""
    if not realtime:
        return None
    
    result = {}
    
    # 1. 价格状态
    price = realtime['price']
    prev = realtime['prev_close']
    open_p = realtime['open']
    high = realtime['high']
    low = realtime['low']
    
    # 高开/低开/平开
    open_pct = (open_p - prev) / prev * 100
    if open_pct > 2:
        open_type = '🚀 大幅高开'
    elif open_pct > 0.5:
        open_type = '✅ 高开'
    elif open_pct > -0.5:
        open_type = '⚖️ 平开'
    elif open_pct > -2:
        open_type = '🟡 低开'
    else:
        open_type = '🔴 大幅低开'
    
    # 当前位置（在今日高低区间的位置）
    if high > low:
        position_in_day = (price - low) / (high - low) * 100
    else:
        position_in_day = 50
    
    if position_in_day > 80:
        position_type = '📈 接近高点'
    elif position_in_day > 60:
        position_type = '✅ 上半区'
    elif position_in_day > 40:
        position_type = '⚖️ 中位'
    elif position_in_day > 20:
        position_type = '🟡 下半区'
    else:
        position_type = '📉 接近低点'
    
    # 冲高回落判断
    high_pct = (high - prev) / prev * 100
    price_pct = realtime['change_pct']
    pullback_from_high = (high - price) / high * 100 if high > 0 else 0
    
    if high_pct > 2 and pullback_from_high > 1.5:
        intraday_pattern = '🚨 冲高回落'
    elif high_pct > 1 and pullback_from_high > 0.8 and position_in_day < 50:
        intraday_pattern = '⚠️ 高位回落'
    elif position_in_day > 80 and price_pct > 1:
        intraday_pattern = '🚀 强势上攻'
    elif position_in_day < 30 and price_pct < -1:
        intraday_pattern = '🔴 弱势杀跌'
    elif abs(price_pct) < 0.5 and realtime['amplitude'] < 1.5:
        intraday_pattern = '⚖️ 横盘震荡'
    else:
        intraday_pattern = '🟢 正常波动'
    
    # 2. 量能分析
    vol_ratio = realtime['vol_ratio']
    if vol_ratio >= 3:
        vol_signal = '🚀 巨量放大'
    elif vol_ratio >= 2:
        vol_signal = '✅ 明显放量'
    elif vol_ratio >= 1.5:
        vol_signal = '🟢 温和放量'
    elif vol_ratio >= 0.8:
        vol_signal = '⚖️ 正常量'
    else:
        vol_signal = '🟡 缩量'
    
    # 3. 内外盘（主动买卖盘）
    outer = realtime['outer']
    inner = realtime['inner']
    if inner + outer > 0:
        outer_ratio = outer / (inner + outer)
    else:
        outer_ratio = 0.5
    
    if outer_ratio > 0.6:
        flow_signal = '✅ 主动买盘强'
    elif outer_ratio > 0.55:
        flow_signal = '🟢 主动买盘略多'
    elif outer_ratio > 0.45:
        flow_signal = '⚖️ 多空均衡'
    elif outer_ratio > 0.4:
        flow_signal = '🟡 主动卖盘略多'
    else:
        flow_signal = '🔴 主动卖盘强'
    
    # 4. 五档盘口厚度
    bid_total = sum([realtime[f'bid{i}_qty'] for i in range(1, 6)])
    ask_total = sum([realtime[f'ask{i}_qty'] for i in range(1, 6)])
    
    if ask_total + bid_total > 0:
        bid_ask_ratio = bid_total / (bid_total + ask_total)
    else:
        bid_ask_ratio = 0.5
    
    if bid_ask_ratio > 0.65:
        depth_signal = '✅ 买盘厚'
    elif bid_ask_ratio > 0.55:
        depth_signal = '🟢 买盘略厚'
    elif bid_ask_ratio > 0.45:
        depth_signal = '⚖️ 均衡'
    elif bid_ask_ratio > 0.35:
        depth_signal = '🟡 卖盘略厚'
    else:
        depth_signal = '🔴 卖盘厚'
    
    # 5. 量价配合（最重要）
    if price_pct > 2 and vol_ratio >= 1.5 and outer_ratio > 0.55:
        vp_match = '🚀 量价齐升（健康）'
    elif price_pct > 2 and vol_ratio < 1:
        vp_match = '⚠️ 价升量缩（警惕滞涨）'
    elif price_pct > 2 and outer_ratio < 0.45:
        vp_match = '🚨 价升但主动卖（顶部信号）'
    elif price_pct < -2 and vol_ratio >= 2:
        vp_match = '🚨 量价齐跌（杀跌中）'
    elif price_pct < -2 and vol_ratio < 1:
        vp_match = '🟢 价跌量缩（恐慌减弱）'
    elif abs(price_pct) < 0.5 and vol_ratio > 1.5:
        vp_match = '🟡 放量震荡（多空分歧）'
    else:
        vp_match = '⚖️ 量价正常'
    
    # 综合
    result.update({
        'open_pct': round(open_pct, 2),
        'open_type': open_type,
        'position_in_day': round(position_in_day, 1),
        'position_type': position_type,
        'pullback_from_high': round(pullback_from_high, 2),
        'intraday_pattern': intraday_pattern,
        'vol_ratio': vol_ratio,
        'vol_signal': vol_signal,
        'outer_ratio': round(outer_ratio, 2),
        'flow_signal': flow_signal,
        'bid_ask_ratio': round(bid_ask_ratio, 2),
        'depth_signal': depth_signal,
        'vp_match': vp_match,
    })
    
    return result


def judge_intraday_state(realtime: dict, analysis: dict) -> dict:
    """综合判断当下状态 + 可能趋势 + 立刻策略"""
    price_pct = realtime['change_pct']
    
    # 评分（盘中维度，不看长期）
    score = 0
    reasons = []
    
    # 量价
    if '齐升' in analysis['vp_match']:
        score += 3; reasons.append('量价齐升')
    elif '滞涨' in analysis['vp_match']:
        score -= 2; reasons.append('价升量缩(滞涨)')
    elif '顶部' in analysis['vp_match']:
        score -= 4; reasons.append('价升主动卖(顶部信号)')
    elif '齐跌' in analysis['vp_match']:
        score -= 3; reasons.append('量价齐跌')
    elif '放量震荡' in analysis['vp_match']:
        score -= 1; reasons.append('放量震荡')
    
    # 内外盘
    if analysis['outer_ratio'] > 0.55:
        score += 2; reasons.append(f'外盘 {analysis["outer_ratio"]} 占优')
    elif analysis['outer_ratio'] < 0.45:
        score -= 2; reasons.append(f'内盘 {1-analysis["outer_ratio"]:.2f} 占优')
    
    # 盘口厚度
    if analysis['bid_ask_ratio'] > 0.6:
        score += 1; reasons.append('买盘厚')
    elif analysis['bid_ask_ratio'] < 0.4:
        score -= 1; reasons.append('卖盘厚')
    
    # 位置
    if '冲高回落' in analysis['intraday_pattern']:
        score -= 3; reasons.append('冲高回落')
    elif '强势上攻' in analysis['intraday_pattern']:
        score += 2; reasons.append('强势上攻')
    elif '弱势杀跌' in analysis['intraday_pattern']:
        score -= 3; reasons.append('弱势杀跌')
    
    # 量比
    if analysis['vol_ratio'] > 2.5 and price_pct > 1:
        score += 2; reasons.append(f'量比 {analysis["vol_ratio"]} 放大')
    elif analysis['vol_ratio'] < 1 and price_pct > 1:
        score -= 1; reasons.append(f'量比 {analysis["vol_ratio"]} 偏低')
    
    # 状态
    if score >= 5:
        state = '🚀 强势'
        trend = '继续上行概率大'
        strategy = '持有 / 可加仓'
    elif score >= 2:
        state = '✅ 偏强'
        trend = '震荡偏上'
        strategy = '持有'
    elif score >= -1:
        state = '⚖️ 中性'
        trend = '震荡待方向'
        strategy = '观望 / 不动'
    elif score >= -3:
        state = '⚠️ 偏弱'
        trend = '调整概率大'
        strategy = '减仓 / 设止损'
    else:
        state = '🚨 弱势'
        trend = '下跌风险高'
        strategy = '立即减仓'
    
    return {
        'score': score,
        'state': state,
        'trend': trend,
        'strategy': strategy,
        'reasons': reasons,
    }


def format_realtime_report(realtime: dict, analysis: dict, judgment: dict, name: str = '') -> str:
    """格式化盘中报告"""
    if not realtime:
        return "❌ 无数据"
    
    lines = []
    lines.append(f"### 🎯 {name or realtime['name']} {realtime['code']}")
    lines.append("")
    
    # 标题行
    chg = realtime['change_pct']
    chg_emoji = '🚀' if chg > 3 else '✅' if chg > 0 else '🔴' if chg < -3 else '🟡'
    lines.append(f"**现价 ¥{realtime['price']} {chg_emoji} {chg:+.2f}%** · 换手 {realtime['turnover_rate']}% · 成交 ¥{realtime['turnover_wan']/10000:.1f}亿")
    lines.append("")
    
    # 综合判断
    lines.append(f"**{judgment['state']}** · 趋势预判：**{judgment['trend']}** · 策略：**{judgment['strategy']}**")
    lines.append("")
    
    # 量价四维
    lines.append("| 维度 | 信号 |")
    lines.append("|---|---|")
    lines.append(f"| 🎯 量价配合 | {analysis['vp_match']} |")
    lines.append(f"| 📊 量比 | {analysis['vol_ratio']} ({analysis['vol_signal']}) |")
    lines.append(f"| 💰 内外盘 | {analysis['outer_ratio']:.2f} ({analysis['flow_signal']}) |")
    lines.append(f"| 📋 盘口厚度 | {analysis['bid_ask_ratio']:.2f} ({analysis['depth_signal']}) |")
    lines.append(f"| 📈 盘中形态 | {analysis['intraday_pattern']} |")
    lines.append(f"| 🎚️ 日内位置 | {analysis['position_type']} ({analysis['position_in_day']}%) |")
    lines.append("")
    
    # 信号清单
    if judgment['reasons']:
        lines.append(f"**核心信号**：{' · '.join(judgment['reasons'][:6])}")
        lines.append("")
    
    # 五档盘口
    lines.append(f"**五档盘口**：")
    lines.append(f"```")
    for i in range(5, 0, -1):
        lines.append(f"卖{i}  {realtime[f'ask{i}_price']:>7.2f}  ×{realtime[f'ask{i}_qty']}")
    lines.append(f"---  ¥{realtime['price']:>7.2f}  ---")
    for i in range(1, 6):
        lines.append(f"买{i}  {realtime[f'bid{i}_price']:>7.2f}  ×{realtime[f'bid{i}_qty']}")
    lines.append(f"```")
    
    return '\n'.join(lines)


def analyze_intraday(code: str, name: str = '') -> dict:
    """主入口：完整盘中分析"""
    realtime = fetch_realtime_full(code)
    if not realtime:
        return {'error': '无法获取实时数据'}
    
    analysis = analyze_volume_price(realtime)
    judgment = judge_intraday_state(realtime, analysis)
    
    return {
        'code': code,
        'name': name or realtime['name'],
        'realtime': realtime,
        'analysis': analysis,
        'judgment': judgment,
        'report': format_realtime_report(realtime, analysis, judgment, name),
    }


def analyze_portfolio_intraday(positions: list) -> str:
    """组合的盘中分析（多只票）"""
    lines = []
    from datetime import datetime
    lines.append(f"# 📊 盘中实时量价分析")
    lines.append(f"")
    lines.append(f"> ⏰ 时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"> 📍 方法：量价 + 资金 + 技术 + 板块（不谈周期）")
    lines.append("")
    
    # 总览表
    lines.append("## 一、全局速览")
    lines.append("")
    lines.append("| 票 | 现价 | 涨幅 | 量比 | 内外盘 | 状态 | 策略 |")
    lines.append("|---|---:|:---:|:---:|:---:|---|---|")
    
    results = []
    for p in positions:
        r = analyze_intraday(p['code'], p.get('name', ''))
        if 'error' not in r:
            results.append(r)
            rt = r['realtime']
            a = r['analysis']
            j = r['judgment']
            lines.append(f"| {r['name']} {p['code']} | ¥{rt['price']} | {rt['change_pct']:+.2f}% | {a['vol_ratio']} | {a['outer_ratio']:.2f} | {j['state']} | {j['strategy']} |")
    
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # 逐票详细分析
    lines.append("## 二、逐票实时量价分析")
    lines.append("")
    for r in results:
        lines.append(r['report'])
        lines.append("")
        lines.append("---")
        lines.append("")
    
    return '\n'.join(lines)


if __name__ == '__main__':
    import sys
    import json as json_lib
    if len(sys.argv) >= 3 and sys.argv[1] == '--portfolio':
        # 持仓模式
        with open(sys.argv[2]) as f:
            pf = json_lib.load(f)
        positions = pf.get('positions', [])
        # 去重
        seen = set()
        unique = []
        for p in positions:
            if p['symbol'] not in seen:
                seen.add(p['symbol'])
                unique.append({'code': p['symbol'], 'name': p.get('name', '')})
        print(analyze_portfolio_intraday(unique))
    else:
        code = sys.argv[1] if len(sys.argv) > 1 else '300757'
        name = sys.argv[2] if len(sys.argv) > 2 else ''
        result = analyze_intraday(code, name)
        print(result.get('report', result.get('error', '?')))
