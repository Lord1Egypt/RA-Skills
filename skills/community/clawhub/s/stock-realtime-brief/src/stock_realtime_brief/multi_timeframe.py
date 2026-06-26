#!/usr/bin/env python3
"""
v2.9 多周期共振分析模块

核心原则（用户教诲）：
- 月 K → 定大趋势
- 周 K → 定波段
- 日 K → 定买卖点

依赖腾讯 K 线 API（https://web.ifzq.gtimg.cn/）
"""
import urllib.request, json, re
from typing import Optional


def _fetch_kline(code: str, period: str = 'day', count: int = 300) -> list:
    """拉腾讯多周期 K 线"""
    sym = ('sz' if code.startswith(('0', '3')) else 'sh') + code
    url = f"https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param={sym},{period},,,{count},qfq"
    try:
        req = urllib.request.Request(url, headers={'Referer': 'https://gu.qq.com/'})
        with urllib.request.urlopen(req, timeout=15) as r:
            text = r.read().decode('utf-8', errors='ignore')
        text = re.sub(r'^[\s\S]*?=\s*', '', text).rstrip(';)')
        data = json.loads(text)
        inner = data.get('data', {}).get(sym, {})
        for k in ['qfqday', 'qfqweek', 'qfqmonth', period, 'day', 'week', 'month']:
            if k in inner and inner[k]:
                return inner[k]
    except Exception:
        pass
    return []


def _calc_ma(closes: list, n: int) -> Optional[float]:
    if len(closes) < n:
        return None
    return round(sum(closes[-n:]) / n, 2)


def _calc_kdj(highs, lows, closes, n=9):
    """KDJ 计算"""
    if len(closes) < n:
        return None
    k_list, d_list, j_list = [], [], []
    k_prev, d_prev = 50.0, 50.0
    for i in range(n - 1, len(closes)):
        period_high = max(highs[i - n + 1:i + 1])
        period_low = min(lows[i - n + 1:i + 1])
        if period_high == period_low:
            rsv = 50
        else:
            rsv = (closes[i] - period_low) / (period_high - period_low) * 100
        k = 2/3 * k_prev + 1/3 * rsv
        d = 2/3 * d_prev + 1/3 * k
        j = 3 * k - 2 * d
        k_list.append(k)
        d_list.append(d)
        j_list.append(j)
        k_prev, d_prev = k, d
    return {
        'k': round(k_list[-1], 1),
        'd': round(d_list[-1], 1),
        'j': round(j_list[-1], 1),
    }


def _calc_macd(closes):
    """MACD 计算（EMA12-EMA26，DIF-DEA*2）"""
    if len(closes) < 35:
        return None
    
    def ema(values, n):
        k = 2 / (n + 1)
        result = [values[0]]
        for v in values[1:]:
            result.append(v * k + result[-1] * (1 - k))
        return result
    
    ema12 = ema(closes, 12)
    ema26 = ema(closes, 26)
    dif = [a - b for a, b in zip(ema12, ema26)]
    dea = ema(dif, 9)
    macd_hist = [(d - de) * 2 for d, de in zip(dif, dea)]
    
    return {
        'dif': round(dif[-1], 2),
        'dea': round(dea[-1], 2),
        'macd': round(macd_hist[-1], 2),
        'macd_prev': round(macd_hist[-2], 2) if len(macd_hist) >= 2 else 0,
        'trend': 'up' if dif[-1] > dea[-1] else 'down',
    }


def analyze_period(code: str, period: str = 'day', count: int = 200) -> dict:
    """分析单一周期"""
    arr = _fetch_kline(code, period, count)
    if not arr or len(arr) < 5:
        return {'error': '无数据'}
    
    # arr 格式：[date, open, close, high, low, volume]
    closes = [float(x[2]) for x in arr]
    highs = [float(x[3]) for x in arr]
    lows = [float(x[4]) for x in arr]
    opens = [float(x[1]) for x in arr]
    vols = [float(x[5]) if x[5] else 0 for x in arr]
    
    last_close = closes[-1]
    
    # 均线
    mas = {}
    for n in (5, 10, 20, 30, 60):
        v = _calc_ma(closes, n)
        if v:
            mas[f'ma{n}'] = v
    
    # 当前价相对均线
    above_ma5 = mas.get('ma5') and last_close > mas['ma5']
    above_ma10 = mas.get('ma10') and last_close > mas['ma10']
    above_ma20 = mas.get('ma20') and last_close > mas['ma20']
    above_ma60 = mas.get('ma60') and last_close > mas['ma60']
    
    # 多头排列
    multi_long = (mas.get('ma5') and mas.get('ma10') and mas.get('ma20') and
                  mas.get('ma60') and
                  mas['ma5'] > mas['ma10'] > mas['ma20'] > mas['ma60'])
    multi_short = (mas.get('ma5') and mas.get('ma10') and mas.get('ma20') and
                   mas.get('ma60') and
                   mas['ma5'] < mas['ma10'] < mas['ma20'] < mas['ma60'])
    
    # 趋势状态
    if multi_long:
        trend = 'bullish_strong'   # 强多
    elif above_ma20 and above_ma60:
        trend = 'bullish'           # 多头
    elif above_ma20 and not above_ma60:
        trend = 'bullish_weak'      # 弱多
    elif multi_short:
        trend = 'bearish_strong'    # 强空
    elif not above_ma20:
        trend = 'bearish'           # 空头
    else:
        trend = 'consolidation'     # 震荡
    
    # 高低点位置
    high_n = max(closes)
    low_n = min(closes)
    high_idx = closes.index(high_n)
    low_idx = closes.index(low_n)
    
    # 距高点距离
    drawdown_from_high = (high_n - last_close) / high_n * 100
    
    # 量价 - 最近 5 期均量 vs 历史均量
    recent_vol = sum(vols[-5:]) / 5
    hist_vol = sum(vols[-30:]) / 30 if len(vols) >= 30 else recent_vol
    vol_ratio = recent_vol / hist_vol if hist_vol > 0 else 1
    
    # 技术指标
    kdj = _calc_kdj(highs, lows, closes)
    macd = _calc_macd(closes)
    
    # 周期所处阶段（简单判断）
    if last_close >= high_n * 0.97:
        stage = '新高附近'
    elif drawdown_from_high < 10:
        stage = '高位回调'
    elif drawdown_from_high < 25:
        stage = '中位调整'
    elif drawdown_from_high < 50:
        stage = '深度调整'
    else:
        stage = '底部区域'
    
    return {
        'period': period,
        'count': len(arr),
        'last_close': round(last_close, 2),
        'last_date': arr[-1][0],
        **mas,
        'above_ma5': above_ma5,
        'above_ma10': above_ma10,
        'above_ma20': above_ma20,
        'above_ma60': above_ma60,
        'multi_long': multi_long,
        'multi_short': multi_short,
        'trend': trend,
        'stage': stage,
        'high_n': round(high_n, 2),
        'low_n': round(low_n, 2),
        'drawdown_from_high': round(drawdown_from_high, 1),
        'vol_ratio': round(vol_ratio, 2),
        'kdj': kdj,
        'macd': macd,
    }


def analyze_multi_timeframe(code: str) -> dict:
    """三周期共振分析（核心）"""
    daily = analyze_period(code, 'day', 200)
    weekly = analyze_period(code, 'week', 200)
    monthly = analyze_period(code, 'month', 100)
    
    if 'error' in daily or 'error' in weekly or 'error' in monthly:
        return {'error': '数据不全'}
    
    # 三周期共振判断
    resonance = _judge_resonance(daily, weekly, monthly)
    
    return {
        'code': code,
        'daily': daily,
        'weekly': weekly,
        'monthly': monthly,
        'resonance': resonance,
    }


def _judge_resonance(daily: dict, weekly: dict, monthly: dict) -> dict:
    """共振判断 - 核心决策矩阵"""
    
    # 各周期信号
    m_trend = monthly['trend']
    w_trend = weekly['trend']
    d_trend = daily['trend']
    
    # 信号分级
    def trend_score(t):
        return {
            'bullish_strong': 3,
            'bullish': 2,
            'bullish_weak': 1,
            'consolidation': 0,
            'bearish_weak': -1,
            'bearish': -2,
            'bearish_strong': -3,
        }.get(t, 0)
    
    m_score = trend_score(m_trend)
    w_score = trend_score(w_trend)
    d_score = trend_score(d_trend)
    
    # 加权综合分数（月线权重高）
    total = m_score * 3 + w_score * 2 + d_score * 1
    
    # 共振等级
    if m_score >= 2 and w_score >= 2 and d_score >= 2:
        resonance_type = '🚀🚀 三周期共振做多'
        action = '全力做多 / 重仓'
    elif m_score >= 2 and w_score >= 1 and d_score >= 0:
        resonance_type = '✅ 趋势内调整买入'
        action = '逢低买入 / 持有'
    elif m_score >= 2 and w_score >= 0 and d_score < 0:
        resonance_type = '⏸ 月线多头 / 短期回调'
        action = '不追高 / 等周线再起'
    elif m_score >= 1 and w_score <= -1:
        resonance_type = '⚠️ 长期向上但中期已转弱'
        action = '减仓观察 / 等周线企稳'
    elif m_score <= 0 and d_score >= 1:
        resonance_type = '🚨 月线已破 / 日线反弹'
        action = '🚨 逃命反弹 / 立即卖出'
    elif m_score <= -1 and w_score <= -1:
        resonance_type = '⛔ 中长期空头'
        action = '不碰 / 已持仓清仓'
    elif m_score >= 1 and w_score >= 1 and d_score == 0:
        resonance_type = '🟢 主升中继 / 短线震荡'
        action = '持仓 / 等突破再加'
    elif total >= 8:
        resonance_type = '✅ 多头主导'
        action = '可买入'
    elif total <= -8:
        resonance_type = '🚨 空头主导'
        action = '清仓 / 不碰'
    else:
        resonance_type = '⚖️ 多空不明'
        action = '观望 / 减仓等信号'
    
    return {
        'total_score': total,
        'monthly_score': m_score,
        'weekly_score': w_score,
        'daily_score': d_score,
        'monthly_trend': m_trend,
        'weekly_trend': w_trend,
        'daily_trend': d_trend,
        'resonance_type': resonance_type,
        'action': action,
    }


def format_multi_timeframe_report(result: dict, name: str = '') -> str:
    """格式化输出"""
    if 'error' in result:
        return f"❌ {result['error']}"
    
    lines = []
    lines.append(f"## 📊 多周期共振分析{f' · {name}' if name else ''}")
    lines.append("")
    
    res = result['resonance']
    lines.append(f"### 🎯 综合判断: {res['resonance_type']}")
    lines.append(f"### 💡 建议: **{res['action']}**")
    lines.append(f"")
    lines.append(f"| 周期 | 趋势 | 阶段 | 站上MA | 评分 |")
    lines.append(f"|:---:|---|---|:---:|:---:|")
    
    trend_emoji = {
        'bullish_strong': '🚀 强多头',
        'bullish': '✅ 多头',
        'bullish_weak': '🟢 弱多',
        'consolidation': '⚖️ 震荡',
        'bearish_weak': '🟡 弱空',
        'bearish': '🔴 空头',
        'bearish_strong': '⛔ 强空头',
    }
    
    for period_name, key in [('月线', 'monthly'), ('周线', 'weekly'), ('日线', 'daily')]:
        p = result[key]
        ma_count = sum([bool(p.get('above_ma5')), bool(p.get('above_ma10')), bool(p.get('above_ma20')), bool(p.get('above_ma60'))])
        lines.append(f"| {period_name} | {trend_emoji.get(p['trend'], p['trend'])} | {p['stage']} | {ma_count}/4 | {res[key + '_score'] if False else trend_score_str(p['trend'])} |")
    
    lines.append("")
    lines.append(f"### 📈 关键数据")
    lines.append(f"- 现价: ¥{result['daily']['last_close']}")
    
    monthly_high = result['monthly']['high_n']
    weekly_high = result['weekly']['high_n']
    lines.append(f"- 月线高点: ¥{monthly_high}（距高点 {result['monthly']['drawdown_from_high']}%）")
    lines.append(f"- 周线高点: ¥{weekly_high}（距高点 {result['weekly']['drawdown_from_high']}%）")
    lines.append(f"- 月线 MA20: ¥{result['monthly'].get('ma20', '-')}")
    lines.append(f"- 周线 MA20: ¥{result['weekly'].get('ma20', '-')}")
    lines.append(f"- 日线 MA20: ¥{result['daily'].get('ma20', '-')}")
    
    # MACD 状态
    lines.append("")
    lines.append(f"### 🌀 MACD 多周期")
    for period_name, key in [('月', 'monthly'), ('周', 'weekly'), ('日', 'daily')]:
        macd = result[key].get('macd')
        if macd:
            trend_str = '红柱↑' if macd['trend'] == 'up' else '绿柱↓'
            lines.append(f"- {period_name}: DIF={macd['dif']} DEA={macd['dea']} {trend_str}")
    
    return '\n'.join(lines)


def trend_score_str(trend):
    return {
        'bullish_strong': '+3',
        'bullish': '+2',
        'bullish_weak': '+1',
        'consolidation': '0',
        'bearish_weak': '-1',
        'bearish': '-2',
        'bearish_strong': '-3',
    }.get(trend, '0')


if __name__ == '__main__':
    import sys
    code = sys.argv[1] if len(sys.argv) > 1 else '300757'
    name = sys.argv[2] if len(sys.argv) > 2 else '罗博特科'
    
    print(f"\n{'='*60}")
    print(f"🎯 多周期共振分析: {name} ({code})")
    print(f"{'='*60}\n")
    result = analyze_multi_timeframe(code)
    print(format_multi_timeframe_report(result, name))
