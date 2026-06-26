#!/usr/bin/env python3
"""
v4.1 鱼尾行情预警器

铁律 4: 主升浪聚焦原则
  • 80% 利润来自主升 / 20% 鱼尾是陷阱

鱼尾 2 大特征:
  ① 主线龙头高位放量滞涨 + 长上影线
  ② 低价垃圾股批量连板 + 全民炒股
"""
import urllib.request
import re
import json
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
            'name': p[1], 'price': float(p[3]),
            'open': float(p[5]), 'high': float(p[33]), 'low': float(p[34]),
            'change_pct': float(p[32]) if p[32] else 0,
            'amplitude': float(p[43]) if p[43] else 0,
            'turnover_rate': float(p[38]) if p[38] else 0,
            'vol_ratio': float(p[49]) if len(p) > 49 and p[49] else 0,
            'turnover_amount': float(p[37]) if p[37] else 0,
            'market_cap': float(p[44]) if p[44] else 0,
        }
    except: return None


def detect_long_upper_shadow(q):
    """检测长上影线
    
    定义: 上影线 > 实体 2 倍
    """
    if not q: return False
    upper_shadow = q['high'] - max(q['open'], q['price'])
    body = abs(q['price'] - q['open'])
    if body < 0.01: body = 0.01
    return upper_shadow / body > 2.0


def detect_high_volume_stagnation(q):
    """检测高位放量滞涨
    
    定义: 涨幅 < 2% 但 量比 > 1.5 + 振幅 > 4%
    """
    if not q: return False
    return q['change_pct'] < 2 and q['vol_ratio'] > 1.5 and q['amplitude'] > 4


def scan_main_line_warning():
    """扫描主线龙头警示信号"""
    with open(UNIVERSE_PATH, encoding='utf-8') as f:
        universe = json.load(f)
    
    warnings = []
    
    for theme, theme_data in universe['themes'].items():
        for stock in theme_data.get('stocks', [])[:3]:  # 只看每个板块前 3 只
            q = fetch_quote(stock['code'])
            if not q: continue
            q['code'] = stock['code']
            q['theme'] = theme
            
            # 长上影线
            if detect_long_upper_shadow(q):
                warnings.append({
                    'type': '长上影线',
                    'name': q['name'],
                    'code': q['code'],
                    'theme': theme,
                    'price': q['price'],
                    'change_pct': q['change_pct'],
                    'signal': f"上影线 ¥{q['high']-max(q['open'],q['price']):.2f} / 实体 ¥{abs(q['price']-q['open']):.2f}",
                })
            
            # 高位放量滞涨
            if detect_high_volume_stagnation(q):
                warnings.append({
                    'type': '高位放量滞涨',
                    'name': q['name'],
                    'code': q['code'],
                    'theme': theme,
                    'price': q['price'],
                    'change_pct': q['change_pct'],
                    'signal': f"涨幅 {q['change_pct']:+.2f}% / 量比 {q['vol_ratio']} / 振幅 {q['amplitude']}%",
                })
    
    return warnings


def detect_garbage_stock_rally():
    """检测垃圾股普涨
    
    定义: 流通市值 < 50 亿 + 涨幅 > 5% 的股票数量
    """
    # 简化版: 用 universe 中的小市值股票来代表
    # 真实版需要 接入 全市场扫描接口
    with open(UNIVERSE_PATH, encoding='utf-8') as f:
        universe = json.load(f)
    
    small_cap_count = 0
    small_cap_big_gain = 0
    
    for theme, theme_data in universe['themes'].items():
        for stock in theme_data.get('stocks', []):
            q = fetch_quote(stock['code'])
            if not q: continue
            
            if q.get('market_cap', 0) < 50:  # 小于 50 亿流通市值
                small_cap_count += 1
                if q['change_pct'] > 5:
                    small_cap_big_gain += 1
    
    ratio = small_cap_big_gain / small_cap_count if small_cap_count > 0 else 0
    
    return {
        'small_cap_count': small_cap_count,
        'small_cap_big_gain': small_cap_big_gain,
        'ratio': ratio,
        'is_warning': ratio > 0.4,  # 40% 以上小市值大涨 = 鱼尾信号
    }


def assess_end_wave():
    """综合评估是否进入鱼尾行情"""
    main_line_warnings = scan_main_line_warning()
    garbage_check = detect_garbage_stock_rally()
    
    # 评分
    score = 0
    reasons = []
    
    # 主线龙头长上影
    long_shadow_count = sum(1 for w in main_line_warnings if w['type'] == '长上影线')
    if long_shadow_count >= 3:
        score += 40
        reasons.append(f"主线 {long_shadow_count} 只龙头 出现长上影线")
    elif long_shadow_count >= 1:
        score += 20
        reasons.append(f"主线 {long_shadow_count} 只龙头 出现长上影")
    
    # 高位放量滞涨
    stagnation_count = sum(1 for w in main_line_warnings if w['type'] == '高位放量滞涨')
    if stagnation_count >= 2:
        score += 30
        reasons.append(f"{stagnation_count} 只主线龙头 高位放量滞涨")
    
    # 垃圾股普涨
    if garbage_check['is_warning']:
        score += 30
        reasons.append(f"小市值股大涨比例 {garbage_check['ratio']*100:.0f}% > 40%")
    
    # 鱼尾判定
    if score >= 70:
        verdict = '🚨 强烈鱼尾信号'
        risk = '极高'
        action = '🔴 立刻减仓 60-70% / 现金为王'
    elif score >= 50:
        verdict = '⚠️ 鱼尾预警'
        risk = '高'
        action = '⚠️ 减仓 30-50% / 不开新仓'
    elif score >= 30:
        verdict = '🟡 部分鱼尾迹象'
        risk = '中'
        action = '🟡 警惕主升龙头 / 浮盈减半'
    else:
        verdict = '✅ 主升正常'
        risk = '低'
        action = '✅ 继续持有 / 按计划操作'
    
    return {
        'score': score,
        'verdict': verdict,
        'risk_level': risk,
        'action': action,
        'reasons': reasons,
        'warnings': main_line_warnings,
        'garbage_check': garbage_check,
    }


def format_end_wave_report(result):
    """格式化鱼尾报告"""
    lines = []
    lines.append("=" * 70)
    lines.append(f"📊 鱼尾行情预警 · 北京时间 {datetime.now():%Y-%m-%d %H:%M}")
    lines.append("=" * 70)
    
    lines.append(f"\n🎯 综合评估: {result['verdict']}")
    lines.append(f"   鱼尾评分: {result['score']}/100")
    lines.append(f"   风险等级: {result['risk_level']}")
    lines.append(f"\n💡 操作建议:")
    lines.append(f"   {result['action']}")
    
    if result['reasons']:
        lines.append(f"\n📋 触发原因:")
        for r in result['reasons']:
            lines.append(f"   • {r}")
    
    if result['warnings']:
        lines.append(f"\n⚠️ 主线龙头警示信号:")
        for w in result['warnings'][:8]:
            lines.append(f"   • {w['name']}({w['code']}) [{w['theme']}] - {w['type']}")
            lines.append(f"     现价 ¥{w['price']:.2f} ({w['change_pct']:+.2f}%) | {w['signal']}")
    
    g = result['garbage_check']
    lines.append(f"\n📊 小市值股普涨情况:")
    lines.append(f"   小市值总数: {g['small_cap_count']}")
    lines.append(f"   大涨数量: {g['small_cap_big_gain']}")
    lines.append(f"   普涨比例: {g['ratio']*100:.1f}%")
    
    return "\n".join(lines)


def main():
    print("\n🚀 鱼尾行情预警扫描...")
    result = assess_end_wave()
    print(format_end_wave_report(result))
    return result


if __name__ == '__main__':
    main()
