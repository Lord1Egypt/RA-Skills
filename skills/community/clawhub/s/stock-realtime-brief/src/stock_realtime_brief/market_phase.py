#!/usr/bin/env python3
"""
v4.1 市场阶段判断器

四阶段:
  📊 1. 熊市底部/反弹     仓位 ≤ 20%
  📊 2. 牛市初期           仓位 30-40%
  📊 3. 牛市主升           仓位 50-60%
  📊 4. 牛市末期/鱼尾      仓位 ≤ 30%
"""
import urllib.request
import re
import json
from datetime import datetime


def fetch_quote(code):
    sym = code if code.startswith(('sh', 'sz')) else (
        'sz' + code if code.startswith(('0', '3', '1', '2')) else 'sh' + code
    )
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
        }
    except: return None


def fetch_kline(code, count=60):
    sym = code if code.startswith(('sh', 'sz')) else (
        'sz' + code if code.startswith(('0', '3')) else 'sh' + code
    )
    url = f"https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param={sym},day,,,{count},qfq"
    try:
        req = urllib.request.Request(url, headers={'Referer': 'https://gu.qq.com/'})
        with urllib.request.urlopen(req, timeout=15) as r:
            text = r.read().decode('utf-8', errors='ignore')
        text = re.sub(r'^[\s\S]*?=\s*', '', text).rstrip(';)')
        inner = json.loads(text).get('data', {}).get(sym, {})
        for k in ['qfqday', 'day']:
            if k in inner and inner[k]: return inner[k]
    except: pass
    return []


def calc_ma(values, n):
    if len(values) < n: return None
    return sum(values[-n:]) / n


def analyze_index(code, name):
    """分析单个指数"""
    quote = fetch_quote(code)
    kline = fetch_kline(code, 60)
    if not quote or not kline or len(kline) < 60:
        return None
    
    closes = [float(r[2]) for r in kline]
    cur = quote['price']
    
    ma5 = calc_ma(closes, 5)
    ma20 = calc_ma(closes, 20)
    ma60 = calc_ma(closes, 60)
    
    # 趋势判断
    multi_bull = ma5 and ma20 and ma60 and cur > ma5 > ma20 > ma60
    multi_bear = ma5 and ma20 and ma60 and cur < ma5 < ma20 < ma60
    
    # 5/20/60 日累计涨幅
    chg_5d = (cur - closes[-5]) / closes[-5] * 100 if closes[-5] > 0 else 0
    chg_20d = (cur - closes[-20]) / closes[-20] * 100 if closes[-20] > 0 else 0
    chg_60d = (cur - closes[-60]) / closes[-60] * 100 if closes[-60] > 0 else 0
    
    # 当前位于 60 日区间的什么位置
    high_60d = max(closes[-60:])
    low_60d = min(closes[-60:])
    pos = (cur - low_60d) / (high_60d - low_60d) * 100 if high_60d > low_60d else 50
    
    return {
        'name': name,
        'code': code,
        'price': cur,
        'change_pct': quote['change_pct'],
        'ma5': ma5, 'ma20': ma20, 'ma60': ma60,
        'chg_5d': round(chg_5d, 2),
        'chg_20d': round(chg_20d, 2),
        'chg_60d': round(chg_60d, 2),
        'pos_60d': round(pos, 1),
        'multi_bull': multi_bull,
        'multi_bear': multi_bear,
    }


def detect_phase():
    """市场阶段判断"""
    # 监控多个核心指数
    indices = [
        ('sh000001', '上证指数'),
        ('sz399001', '深证成指'),
        ('sz399006', '创业板指'),
        ('sh000688', '科创 50'),
    ]
    
    index_data = []
    for code, name in indices:
        analysis = analyze_index(code, name)
        if analysis:
            index_data.append(analysis)
    
    if not index_data:
        return None
    
    # 综合判断
    bull_count = sum(1 for d in index_data if d['multi_bull'])
    bear_count = sum(1 for d in index_data if d['multi_bear'])
    
    avg_60d = sum(d['chg_60d'] for d in index_data) / len(index_data)
    avg_20d = sum(d['chg_20d'] for d in index_data) / len(index_data)
    avg_pos = sum(d['pos_60d'] for d in index_data) / len(index_data)
    
    # 阶段判定逻辑
    phase = None
    confidence = 0
    
    # 熊市/反弹 (大盘多周期空头 / 接近 60 日低点)
    if bear_count >= 2 or avg_60d < -10:
        phase = 'bear_or_rebound'
        confidence = 80
    # 牛市初期 (大盘刚翻多 / 涨幅小)
    elif bull_count >= 1 and avg_20d < 5 and avg_60d > 0:
        phase = 'bull_early'
        confidence = 70
    # 牛市主升 (大盘强多头 / 高位但仍上涨)
    elif bull_count >= 3 and avg_20d > 5 and avg_pos > 60:
        phase = 'bull_main'
        confidence = 85
    # 牛市末期 (大盘高位 但开始震荡 / 60 日大涨 + 20 日转弱)
    elif avg_60d > 20 and avg_20d < 2 and avg_pos > 80:
        phase = 'bull_end'
        confidence = 75
    # 默认 - 震荡市
    else:
        phase = 'range_bound'
        confidence = 60
    
    return {
        'indices': index_data,
        'bull_count': bull_count,
        'bear_count': bear_count,
        'avg_chg_20d': round(avg_20d, 2),
        'avg_chg_60d': round(avg_60d, 2),
        'avg_pos_60d': round(avg_pos, 1),
        'phase': phase,
        'confidence': confidence,
    }


PHASE_CONFIG = {
    'bear_or_rebound': {
        'name': '🔴 熊市底部/反弹阶段',
        'position_max': 20,
        'position_recommended': '10-20%',
        'single_stock_max': 20,
        'strategy': '防御为主 / 大量持币 / 仅试探主线龙头',
        'risk_warning': '⚠️ 市场风险高，避免大幅加仓'
    },
    'bull_early': {
        'name': '🟢 牛市初期',
        'position_max': 40,
        'position_recommended': '30-40%',
        'single_stock_max': 30,
        'strategy': '试错布局主线龙头 / 确认趋势再加仓',
        'risk_warning': '✅ 谨慎乐观，逐步加仓'
    },
    'bull_main': {
        'name': '🚀 牛市主升阶段',
        'position_max': 70,
        'position_recommended': '50-70%',
        'single_stock_max': 50,
        'strategy': '集中主线 2-3 只龙头 / 持有为王',
        'risk_warning': '✅ 顺势重仓，不要随意切换'
    },
    'bull_end': {
        'name': '⚠️ 牛市末期/鱼尾阶段',
        'position_max': 30,
        'position_recommended': '≤ 30%',
        'single_stock_max': 20,
        'strategy': '现金为王 / 不开新仓 / 主升盈利 ≥ 50% 立即减半',
        'risk_warning': '🚨 危险区域！避免接最后一棒'
    },
    'range_bound': {
        'name': '⚖️ 震荡市',
        'position_max': 50,
        'position_recommended': '30-50%',
        'single_stock_max': 30,
        'strategy': '高抛低吸 / 主题轮动 / 不重仓',
        'risk_warning': '⚖️ 中性，需选股能力'
    },
}


def format_phase_report(data):
    """格式化阶段报告"""
    if not data:
        return "❌ 数据获取失败"
    
    lines = []
    lines.append("=" * 70)
    lines.append(f"📊 市场阶段判断 · 北京时间 {datetime.now():%Y-%m-%d %H:%M}")
    lines.append("=" * 70)
    
    # 各指数状态
    lines.append("\n📈 主要指数:")
    for idx in data['indices']:
        flag = '🚀' if idx['multi_bull'] else '🔴' if idx['multi_bear'] else '🟡'
        lines.append(f"  {flag} {idx['name']:<10s} {idx['price']:>8.2f} ({idx['change_pct']:+.2f}%) | 20日 {idx['chg_20d']:+.2f}% | 60日 {idx['chg_60d']:+.2f}% | 60日位置 {idx['pos_60d']}%")
    
    lines.append(f"\n📊 综合指标:")
    lines.append(f"  多头共振指数: {data['bull_count']}/4")
    lines.append(f"  空头共振指数: {data['bear_count']}/4")
    lines.append(f"  平均 20 日涨幅: {data['avg_chg_20d']:+.2f}%")
    lines.append(f"  平均 60 日涨幅: {data['avg_chg_60d']:+.2f}%")
    lines.append(f"  平均 60 日区间位置: {data['avg_pos_60d']}%")
    
    # 阶段判定
    cfg = PHASE_CONFIG[data['phase']]
    lines.append(f"\n🎯 当前阶段: {cfg['name']}")
    lines.append(f"   置信度: {data['confidence']}%")
    
    lines.append(f"\n💡 仓位建议:")
    lines.append(f"  • 总仓位上限: {cfg['position_max']}%")
    lines.append(f"  • 推荐仓位: {cfg['position_recommended']}")
    lines.append(f"  • 单股上限: {cfg['single_stock_max']}%")
    
    lines.append(f"\n📋 操作策略:")
    lines.append(f"  {cfg['strategy']}")
    
    lines.append(f"\n{cfg['risk_warning']}")
    
    return "\n".join(lines)


def main():
    print("\n🚀 市场阶段判断启动...")
    data = detect_phase()
    print(format_phase_report(data))
    return data


if __name__ == '__main__':
    main()
