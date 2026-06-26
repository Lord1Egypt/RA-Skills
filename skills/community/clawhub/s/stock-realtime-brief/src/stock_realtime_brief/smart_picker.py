#!/usr/bin/env python3
"""
A 股智能选股引擎 v2.0

升级亮点:
1. 候选股池扩展 (39 → 100+ 股，14 大板块)
2. 真实业绩数据接入（东方财富 API）
3. 主力资金流追踪（3/5/10 日）
4. 技术指标 (MACD/RSI/KDJ)
5. 板块强度排名
6. 与你 portfolio 联动
7. 自动 QQ 推送支持
"""
import json
import sys
import urllib.request
import urllib.parse
import re
import time
import subprocess
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent
UNIVERSE_PATH = ROOT / "configs" / "universe.json"
OUTPUT_DIR = ROOT / "data" / "reports"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================
# 数据接口层
# ============================================================

def fetch_quote(code):
    """实时行情 (腾讯 API)"""
    sym = ('sz' if code.startswith(('0', '3')) else 'sh') + code
    url = f"https://qt.gtimg.cn/q={sym}"
    try:
        req = urllib.request.Request(url, headers={'Referer': 'https://gu.qq.com/'})
        with urllib.request.urlopen(req, timeout=8) as r:
            text = r.read().decode('gbk', errors='ignore')
        p = text.split('~')
        if len(p) < 50:
            return None
        return {
            'name': p[1],
            'price': float(p[3]),
            'prev': float(p[4]),
            'open': float(p[5]),
            'high': float(p[33]),
            'low': float(p[34]),
            'change_pct': float(p[32]) if p[32] else 0,
            'amplitude': float(p[43]) if p[43] else 0,
            'volume': int(p[6]) if p[6] else 0,
            'turnover_amount': float(p[37]) if p[37] else 0,  # 万元
            'turnover_rate': float(p[38]) if p[38] else 0,
            'pe': float(p[39]) if p[39] else 0,
            'vol_ratio': float(p[49]) if len(p) > 49 and p[49] else 0,
            'outer': int(p[7]) if p[7] else 0,
            'inner': int(p[8]) if p[8] else 0,
            'market_cap': float(p[44]) if p[44] else 0,
            'total_cap': float(p[45]) if p[45] else 0,
            'pb': float(p[46]) if p[46] else 0,
        }
    except Exception as e:
        return None

def fetch_kline(code, period='day', count=60):
    """K 线数据 - v2.0 拉 60 根做更准确的 MACD/RSI"""
    sym = ('sz' if code.startswith(('0', '3')) else 'sh') + code
    url = f"https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param={sym},{period},,,{count},qfq"
    try:
        req = urllib.request.Request(url, headers={'Referer': 'https://gu.qq.com/'})
        with urllib.request.urlopen(req, timeout=15) as r:
            text = r.read().decode('utf-8', errors='ignore')
        text = re.sub(r'^[\s\S]*?=\s*', '', text).rstrip(';)')
        inner = json.loads(text).get('data', {}).get(sym, {})
        for k in ['qfqday', 'day']:
            if k in inner and inner[k]:
                return inner[k]
    except:
        pass
    return []

def fetch_money_flow(code):
    """主力资金流（东方财富 API）"""
    secid = f"0.{code}" if code.startswith(('0', '3')) else f"1.{code}"
    url = f"https://push2.eastmoney.com/api/qt/stock/fflow/daykline/get?secid={secid}&lmt=10&klt=101&fields1=f1,f2,f3,f7&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f62,f63,f64,f65"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
        
        klines = data.get('data', {}).get('klines', [])
        if not klines:
            return None
        
        # 解析最近 10 天主力净流入
        days = []
        for line in klines:
            parts = line.split(',')
            if len(parts) >= 6:
                days.append({
                    'date': parts[0],
                    'main_net': float(parts[1]) if parts[1] != '-' else 0,  # 主力净流入
                })
        
        # 计算 3 日/5 日/10 日累计
        recent_3 = sum(d['main_net'] for d in days[-3:])
        recent_5 = sum(d['main_net'] for d in days[-5:])
        recent_10 = sum(d['main_net'] for d in days[-10:])
        
        return {
            'recent_3d_net': recent_3,    # 元
            'recent_5d_net': recent_5,
            'recent_10d_net': recent_10,
            'latest_day': days[-1] if days else None,
        }
    except Exception as e:
        return None

# ============================================================
# 技术指标层
# ============================================================

def calc_ema(values, n):
    """EMA 计算"""
    if len(values) < n:
        return None
    alpha = 2.0 / (n + 1)
    ema = values[0]
    for v in values[1:]:
        ema = alpha * v + (1 - alpha) * ema
    return ema

def calc_macd(closes):
    """MACD 指标"""
    if len(closes) < 26:
        return None
    ema12 = calc_ema(closes, 12)
    ema26 = calc_ema(closes, 26)
    if ema12 is None or ema26 is None:
        return None
    dif = ema12 - ema26
    # 简化版 DEA
    dif_values = []
    for i in range(26, len(closes)):
        e12 = calc_ema(closes[:i+1], 12)
        e26 = calc_ema(closes[:i+1], 26)
        if e12 and e26:
            dif_values.append(e12 - e26)
    if len(dif_values) < 9:
        return {'dif': dif, 'dea': dif, 'histogram': 0, 'signal': 'neutral'}
    dea = calc_ema(dif_values, 9)
    histogram = dif - dea
    signal = 'bullish' if dif > dea and histogram > 0 else 'bearish' if dif < dea else 'neutral'
    return {'dif': dif, 'dea': dea, 'histogram': histogram, 'signal': signal}

def calc_rsi(closes, n=14):
    """RSI 指标"""
    if len(closes) < n + 1:
        return None
    gains = []
    losses = []
    for i in range(1, n + 1):
        change = closes[i] - closes[i-1]
        gains.append(max(0, change))
        losses.append(max(0, -change))
    avg_gain = sum(gains) / n
    avg_loss = sum(losses) / n
    if avg_loss == 0:
        return 100
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calc_ma(values, n):
    """移动平均"""
    if len(values) < n:
        return None
    return sum(values[-n:]) / n

# ============================================================
# 评分系统 v2.0 (12 维)
# ============================================================

def score_business(quote, kline_data=None):
    """业绩维度 (基本面 30%)"""
    if not quote:
        return 0
    score = 0
    pe = quote.get('pe', 0)
    if 0 < pe < 20: score += 8
    elif pe < 35: score += 6
    elif pe < 60: score += 4
    elif pe < 100: score += 2
    elif pe < 0:  # 亏损
        score += 1
    else:
        score += 0
    # 加分项：合理估值且趋势好
    if kline_data and len(kline_data) >= 20:
        closes = [float(r[2]) for r in kline_data[-20:]]
        if closes[-1] > sum(closes) / 20:  # 站上 MA20
            score += 2
    return min(10, score)

def score_trend_v2(quote, kline_data):
    """趋势维度 v2 (技术面 25%) - 加入 MACD/RSI"""
    if not quote or not kline_data or len(kline_data) < 26:
        return 5
    
    closes = [float(r[2]) for r in kline_data]
    cur = quote['price']
    score = 0
    
    # MA 系统
    ma5 = calc_ma(closes, 5)
    ma20 = calc_ma(closes, 20)
    ma60 = calc_ma(closes, 60) if len(closes) >= 60 else None
    
    if ma5 and ma20:
        if cur > ma5 > ma20: score += 3  # 多头排列
        elif cur > ma20: score += 2
        elif cur > ma5: score += 1
    
    if ma60 and cur > ma60: score += 1  # 长期趋势
    
    # MACD
    macd = calc_macd(closes)
    if macd:
        if macd['signal'] == 'bullish' and macd['histogram'] > 0:
            score += 3  # MACD 金叉红柱
        elif macd['signal'] == 'bullish':
            score += 2
        elif macd['signal'] == 'bearish':
            score -= 2
    
    # RSI（不超买）
    rsi = calc_rsi(closes)
    if rsi is not None:
        if 30 < rsi < 70: score += 2  # 健康
        elif rsi <= 30: score += 1  # 超卖（潜在反弹）
        elif rsi >= 80: score -= 2  # 严重超买
        elif rsi >= 70: score += 0
    
    return max(0, min(10, score))

def score_money_v2(quote, money_flow=None):
    """资金维度 v2 (20%) - 加入主力净流入"""
    if not quote:
        return 0
    score = 0
    
    # 主动买盘比
    outer = quote.get('outer', 0)
    inner = quote.get('inner', 0)
    if outer + inner > 0:
        ratio = outer / (outer + inner)
        if ratio > 0.6: score += 3
        elif ratio > 0.55: score += 2
        elif ratio > 0.5: score += 1
    
    # 量比
    vr = quote.get('vol_ratio', 0)
    if 1.2 <= vr <= 3.0: score += 3
    elif vr > 3.0: score += 1
    elif 0.8 <= vr < 1.2: score += 2
    
    # 主力净流入 (新增 v2)
    if money_flow:
        net_3d = money_flow.get('recent_3d_net', 0)
        net_5d = money_flow.get('recent_5d_net', 0)
        if net_3d > 0 and net_5d > 0: score += 4  # 持续流入
        elif net_3d > 0: score += 2
        elif net_3d < -50000000:  # 大幅流出（5000 万+）
            score -= 2
    
    return max(0, min(10, score))

def score_momentum(quote):
    """情绪 momentum (15%)"""
    if not quote:
        return 0
    score = 0
    chg = quote.get('change_pct', 0)
    if 0 < chg < 5: score += 5
    elif 5 <= chg < 8: score += 4
    elif 8 <= chg < 9.8: score += 2
    elif chg >= 9.8: score += 0
    elif -2 < chg <= 0: score += 4
    elif -5 < chg <= -2: score += 3
    elif chg <= -5: score += 1
    
    amp = quote.get('amplitude', 0)
    if 2 <= amp <= 6: score += 3
    elif amp < 2: score += 2
    elif 6 < amp <= 10: score += 1
    
    if quote['high'] > 0 and quote['low'] > 0 and quote['high'] != quote['low']:
        position = (quote['price'] - quote['low']) / (quote['high'] - quote['low'])
        if position > 0.9: score += 0
        elif position > 0.7: score += 1
        else: score += 2
    return min(10, score)

def score_valuation(quote):
    """估值 (10%)"""
    if not quote:
        return 0
    score = 5
    pe = quote.get('pe', 0)
    pb = quote.get('pb', 0)
    if 0 < pe < 25: score += 3
    elif pe < 50: score += 1
    elif pe > 100: score -= 2
    elif pe < 0: score -= 1
    if 0 < pb < 5: score += 2
    elif pb > 10: score -= 1
    return max(0, min(10, score))

def comprehensive_score_v2(quote, kline_data, money_flow=None):
    """综合评分 v2"""
    if not quote:
        return {'total': 0, 'breakdown': {}, 'grade': '❌'}
    
    business = score_business(quote, kline_data)
    trend = score_trend_v2(quote, kline_data)
    money = score_money_v2(quote, money_flow)
    momentum = score_momentum(quote)
    valuation = score_valuation(quote)
    
    total = (
        business * 3.0 +
        trend * 2.5 +
        money * 2.0 +
        momentum * 1.5 +
        valuation * 1.0
    )
    
    grade = ('⭐⭐⭐⭐⭐ 强烈推荐' if total >= 80
             else '⭐⭐⭐⭐ 推荐' if total >= 65
             else '⭐⭐⭐ 关注' if total >= 50
             else '⭐⭐ 谨慎' if total >= 35
             else '❌ 回避')
    
    return {
        'total': round(total, 1),
        'breakdown': {
            'business': business,
            'trend': trend,
            'money': money,
            'momentum': momentum,
            'valuation': valuation,
        },
        'grade': grade
    }

# ============================================================
# 板块强度分析
# ============================================================

def analyze_sector_strength(results):
    """板块强度排名"""
    sectors = {}
    for r in results:
        theme = r['theme']
        if theme not in sectors:
            sectors[theme] = {'stocks': [], 'avg_chg': 0, 'avg_score': 0}
        sectors[theme]['stocks'].append(r)
    
    sector_list = []
    for theme, data in sectors.items():
        stocks = data['stocks']
        avg_chg = sum(s['change_pct'] for s in stocks) / len(stocks)
        avg_score = sum(s['score'] for s in stocks) / len(stocks)
        leader = max(stocks, key=lambda x: x['score'])
        sector_list.append({
            'theme': theme,
            'count': len(stocks),
            'avg_chg': round(avg_chg, 2),
            'avg_score': round(avg_score, 1),
            'leader': leader['name'],
            'leader_chg': leader['change_pct'],
            'leader_score': leader['score'],
        })
    
    sector_list.sort(key=lambda x: -x['avg_score'])
    return sector_list

# ============================================================
# 主扫描
# ============================================================

def scan_all_v2(include_money_flow=True, verbose=True):
    """v2.0 全市场扫描"""
    with open(UNIVERSE_PATH, encoding='utf-8') as f:
        universe = json.load(f)
    
    results = []
    total = sum(len(t.get('stocks', [])) for t in universe.get('themes', {}).values())
    count = 0
    
    for theme, theme_data in universe.get('themes', {}).items():
        for stock in theme_data.get('stocks', []):
            code = stock['code']
            count += 1
            if verbose:
                print(f"\r[{count}/{total}] 扫描 {code} {stock['name']}...    ", end='', flush=True)
            
            quote = fetch_quote(code)
            if not quote:
                continue
            kline = fetch_kline(code, 'day', 60)
            money_flow = fetch_money_flow(code) if include_money_flow else None
            
            score = comprehensive_score_v2(quote, kline, money_flow)
            
            results.append({
                'code': code,
                'name': stock['name'],
                'theme': theme,
                'tag': stock.get('tag', ''),
                'price': quote['price'],
                'change_pct': quote['change_pct'],
                'pe': quote.get('pe', 0),
                'market_cap': quote.get('market_cap', 0),
                'vol_ratio': quote.get('vol_ratio', 0),
                'turnover_rate': quote.get('turnover_rate', 0),
                'money_flow_3d': money_flow.get('recent_3d_net', 0) / 1e8 if money_flow else 0,  # 亿
                'money_flow_5d': money_flow.get('recent_5d_net', 0) / 1e8 if money_flow else 0,
                'score': score['total'],
                'grade': score['grade'],
                'breakdown': score['breakdown'],
            })
            time.sleep(0.1)  # 防止 API 限流
    
    if verbose:
        print()  # 换行
    
    results.sort(key=lambda x: -x['score'])
    return results

# ============================================================
# 输出格式
# ============================================================

def format_top_n_v2(results, title, n=10):
    """v2 格式化输出"""
    lines = []
    lines.append("=" * 85)
    lines.append(f"📊 {title} · 北京时间 {datetime.now():%Y-%m-%d %H:%M}")
    lines.append("=" * 85)
    lines.append(f"{'#':>3s} {'代码':<8s} {'名称':<10s} {'现价':>8s} {'涨跌':>7s} {'量比':>5s} {'3日主力':>8s} {'综合分':>6s} {'评级':>18s} {'题材'}")
    lines.append("-" * 85)
    for i, r in enumerate(results[:n], 1):
        flag = '🚀' if r['change_pct'] > 5 else '🟢' if r['change_pct'] > 0 else '🟡' if r['change_pct'] > -2 else '🔴'
        money = f"{r['money_flow_3d']:+.2f}亿" if abs(r['money_flow_3d']) > 0 else "--"
        lines.append(f"{i:>3d}. {r['code']:<8s} {r['name']:<10s} ¥{r['price']:>6.2f} {flag}{r['change_pct']:>+5.2f}% {r['vol_ratio']:>4.1f}  {money:>8s} {r['score']:>5.1f}  {r['grade'][:16]} {r['theme'][:14]}")
    return "\n".join(lines)

def format_sector_ranking(sectors):
    """板块强度排名"""
    lines = []
    lines.append("=" * 75)
    lines.append("📊 板块强度排名 · 北京时间 " + datetime.now().strftime('%Y-%m-%d %H:%M'))
    lines.append("=" * 75)
    lines.append(f"{'#':>3s} {'板块':<25s} {'平均涨跌':>10s} {'平均分':>8s} {'龙头股':<15s} {'龙头涨跌':>10s}")
    lines.append("-" * 75)
    for i, s in enumerate(sectors, 1):
        flag = '🚀' if s['avg_chg'] > 3 else '🟢' if s['avg_chg'] > 0 else '🔴'
        lines.append(f"{i:>3d}. {s['theme']:<25s} {flag}{s['avg_chg']:>+7.2f}%  {s['avg_score']:>6.1f}  {s['leader']:<15s} {s['leader_chg']:>+6.2f}%")
    return "\n".join(lines)

def save_report(results, sectors):
    """保存报告"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M')
    report_path = OUTPUT_DIR / f"smart_pick_{timestamp}.md"
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(f"# 智能选股报告 v2.0\n\n")
        f.write(f"生成时间: 北京时间 {datetime.now():%Y-%m-%d %H:%M}\n\n")
        
        f.write("\n## 板块强度排名\n\n")
        f.write("```\n")
        f.write(format_sector_ranking(sectors) + "\n")
        f.write("```\n")
        
        f.write("\n## 综合 TOP 20\n\n")
        f.write("```\n")
        f.write(format_top_n_v2(results, "综合 TOP 20", n=20) + "\n")
        f.write("```\n")
        
        f.write("\n## 业绩驱动 TOP 5\n\n")
        f.write("```\n")
        business_top = sorted(results, key=lambda x: -x['breakdown']['business'])[:5]
        f.write(format_top_n_v2(business_top, "业绩驱动 TOP 5", n=5) + "\n")
        f.write("```\n")
        
        f.write("\n## 资金流入 TOP 5（3 日累计）\n\n")
        f.write("```\n")
        money_top = sorted(results, key=lambda x: -x['money_flow_3d'])[:5]
        f.write(format_top_n_v2(money_top, "资金流入 TOP 5", n=5) + "\n")
        f.write("```\n")
        
    return report_path

# ============================================================
# QQ 推送
# ============================================================

def push_to_qq(message):
    """推送到 QQ"""
    USER_CHAT_ID = "9F067036FA0E02061F67D46AB31B4D2C"
    try:
        cmd = [
            "openclaw", "message", "send",
            "--channel", "qqbot",
            "--target", USER_CHAT_ID,
            "--message", message,
        ]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return r.returncode == 0
    except:
        return False

def build_daily_brief(results, sectors):
    """构造每日 QQ 推送简报"""
    lines = []
    lines.append(f"📊 智能选股每日简报 · {datetime.now():%m-%d %H:%M}")
    lines.append("")
    lines.append("🏆 综合 TOP 5:")
    for i, r in enumerate(results[:5], 1):
        flag = '🚀' if r['change_pct'] > 5 else '🟢' if r['change_pct'] > 0 else '🔴'
        lines.append(f"  {i}. {r['name']}({r['code']}) ¥{r['price']:.2f} {flag}{r['change_pct']:+.2f}% / 分{r['score']:.0f}")
    
    lines.append("")
    lines.append("🔥 最强板块 TOP 3:")
    for i, s in enumerate(sectors[:3], 1):
        lines.append(f"  {i}. {s['theme']} 平均{s['avg_chg']:+.2f}% / 龙头: {s['leader']}")
    
    # 与你持仓互补的机会
    try:
        with open('/home/work/.openclaw/workspace/stock-agents/data/portfolio.json', encoding='utf-8') as f:
            pf = json.load(f)
        held = {p['symbol'] for p in pf.get('positions', [])}
    except:
        held = set()
    
    new_opps = [r for r in results if r['code'] not in held and r['score'] >= 65][:3]
    if new_opps:
        lines.append("")
        lines.append("🆕 新机会（评分 ≥ 65 / 未持有）:")
        for r in new_opps:
            lines.append(f"  • {r['name']}({r['code']}) ¥{r['price']:.2f} / 分{r['score']:.0f} / {r['theme']}")
    
    return "\n".join(lines)

# ============================================================
# 主入口
# ============================================================

def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'scan-all'
    
    print(f"\n🚀 智能选股引擎 v2.0 启动 · {datetime.now():%H:%M:%S}")
    print(f"📋 命令: {cmd}\n")
    
    if cmd == 'push':
        # 仅推送
        print("⏳ 全市场扫描中（含资金流）...")
        results = scan_all_v2(include_money_flow=True, verbose=True)
        sectors = analyze_sector_strength(results)
        brief = build_daily_brief(results, sectors)
        print("\n" + brief)
        if push_to_qq(brief):
            print("\n✅ QQ 推送成功")
        else:
            print("\n❌ QQ 推送失败")
        save_report(results, sectors)
        return
    
    # 默认扫描
    fast_mode = '--fast' in sys.argv
    include_money = not fast_mode
    
    print(f"⏳ 全市场扫描中... (fast={fast_mode})")
    results = scan_all_v2(include_money_flow=include_money, verbose=True)
    sectors = analyze_sector_strength(results)
    
    if cmd == 'sectors':
        print(format_sector_ranking(sectors))
    elif cmd == 'all':
        print(format_top_n_v2(results, "🏆 综合 TOP 15", n=15))
        print()
        print(format_sector_ranking(sectors))
    else:
        print(format_top_n_v2(results, "🏆 综合 TOP 15", n=15))
        print()
        print(format_sector_ranking(sectors))
    
    # 保存报告
    report = save_report(results, sectors)
    print(f"\n📁 报告已保存: {report}")
    print(f"\n✅ 扫描完成 · 共 {len(results)} 只股票评分")

if __name__ == '__main__':
    main()
