#!/usr/bin/env python3
"""
🎯 持仓优化器 v1.0 (Markowitz 现代组合理论)

核心:
  • 计算 持仓 相关性
  • 板块 集中度 分析
  • 风险敞口 评估
  • 给出 优化 建议 (减仓 / 加仓 / 板块互补)

用法:
  python3 portfolio_optimizer.py                       # 全持仓 分析
  python3 portfolio_optimizer.py --days 60             # 60 天 相关性
"""

import argparse
import json
import re
import sys
import urllib.request
import math
from datetime import datetime


# 你 当前 持仓
HOLDINGS = {
    '600522': {'name': '中天科技', 'cost': 45.97, 'qty': 42200, 'sector': 'AI算力/海缆'},
    '000988': {'name': '华工科技', 'cost': 146.40, 'qty': 9400, 'sector': 'CPO/光通信'},
    '300757': {'name': '罗博特科', 'cost': 309.50, 'qty': 2500, 'sector': '半导体/CPO'},
    '688234': {'name': '天岳先进', 'cost': 182.35, 'qty': 2024, 'sector': '半导体/SiC'},
}

# 总资产 (起步 ¥380 万 + 浮盈)
TOTAL_ASSETS = 5500000  # 估算


def fetch_kline(code, days=60):
    """拿 N 天 收盘价"""
    if code.startswith(('0','3')): sym = 'sz' + code
    else: sym = 'sh' + code
    url = f"https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param={sym},day,,,{days+5},qfq"
    req = urllib.request.Request(url, headers={'Referer': 'https://gu.qq.com/'})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            text = r.read().decode('utf-8', errors='ignore')
        text = re.sub(r'^[\s\S]*?=\s*', '', text).rstrip(';)')
        inner = json.loads(text).get('data', {}).get(sym, {})
        for k in ['qfqday','day']:
            if k in inner and inner[k]:
                return [float(row[2]) for row in inner[k][-days:]]
    except: pass
    return []


def calc_returns(prices):
    """计算 日收益率"""
    return [(prices[i] - prices[i-1]) / prices[i-1] for i in range(1, len(prices))]


def calc_mean(arr):
    return sum(arr) / len(arr) if arr else 0


def calc_std(arr):
    if len(arr) < 2: return 0
    m = calc_mean(arr)
    var = sum((x - m) ** 2 for x in arr) / (len(arr) - 1)
    return math.sqrt(var)


def calc_corr(arr1, arr2):
    """计算 相关性"""
    if len(arr1) != len(arr2) or len(arr1) < 2: return 0
    m1, m2 = calc_mean(arr1), calc_mean(arr2)
    s1, s2 = calc_std(arr1), calc_std(arr2)
    if s1 == 0 or s2 == 0: return 0
    cov = sum((a - m1) * (b - m2) for a, b in zip(arr1, arr2)) / (len(arr1) - 1)
    return cov / (s1 * s2)


def get_current_price(code):
    if code.startswith(('0','3')): sym = 'sz' + code
    else: sym = 'sh' + code
    url = f"https://qt.gtimg.cn/q={sym}"
    req = urllib.request.Request(url, headers={'Referer': 'https://gu.qq.com/'})
    try:
        with urllib.request.urlopen(req, timeout=5) as r:
            text = r.read().decode('gbk', errors='ignore')
        return float(text.split('~')[3])
    except: return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--days', type=int, default=60, help='相关性 计算天数')
    args = parser.parse_args()
    
    print(f"🎯 持仓优化器 v1.0 (Markowitz)  /  {datetime.now():%Y-%m-%d %H:%M}")
    print()
    
    # 1. 拿 收盘价 + 收益率
    data = {}
    print("📊 抓取 持仓 数据 + 计算 日收益率...")
    for code, h in HOLDINGS.items():
        prices = fetch_kline(code, args.days)
        if len(prices) < 20:
            print(f"  ⚠️ {h['name']} 数据 不足")
            continue
        cur = get_current_price(code)
        if not cur: continue
        returns = calc_returns(prices)
        market_value = cur * h['qty']
        data[code] = {
            'name': h['name'],
            'sector': h['sector'],
            'cost': h['cost'],
            'qty': h['qty'],
            'current': cur,
            'mv': market_value,
            'returns': returns,
            'mean_ret': calc_mean(returns) * 100,  # 日均
            'std_ret': calc_std(returns) * 100,    # 日波动
            'annual_ret': calc_mean(returns) * 250 * 100,  # 年化
            'annual_vol': calc_std(returns) * math.sqrt(250) * 100,  # 年波动
        }
    
    if not data:
        print("❌ 数据不足")
        return
    
    # 2. 持仓 基础数据
    print()
    print("=" * 70)
    print("💎 持仓 基础数据 + 风险收益 特征")
    print("=" * 70)
    print(f"{'股票':<10s} {'市值':>10s} {'权重':>7s} {'年化收益':>9s} {'年化波动':>9s} {'夏普(简)':>9s}")
    print("-" * 65)
    
    total_mv = sum(d['mv'] for d in data.values())
    for code, d in data.items():
        weight = d['mv'] / total_mv * 100
        sharpe = (d['annual_ret'] - 3) / d['annual_vol'] if d['annual_vol'] > 0 else 0  # 无风险=3%
        flag = '✅' if sharpe > 1 else '🟡' if sharpe > 0 else '🔴'
        print(f"  {d['name']:<8s} ¥{d['mv']/10000:>5.1f}万 {weight:>5.1f}% {d['annual_ret']:>+7.1f}% {d['annual_vol']:>7.1f}% {flag}{sharpe:>+6.2f}")
    
    # 3. 相关性 矩阵
    print()
    print("=" * 70)
    print("🔗 持仓 相关性 矩阵 (60 天 日收益)")
    print("=" * 70)
    codes = list(data.keys())
    names = [data[c]['name'] for c in codes]
    
    # 表头
    print(f"\n{'':<10s}", end='')
    for n in names:
        print(f"{n[:5]:>8s}", end='')
    print()
    print('-' * (10 + 8 * len(codes)))
    
    corr_pairs = []
    for i, c1 in enumerate(codes):
        print(f"  {names[i][:5]:<8s}", end='')
        for j, c2 in enumerate(codes):
            if i == j:
                corr = 1.0
            else:
                corr = calc_corr(data[c1]['returns'], data[c2]['returns'])
                if i < j:
                    corr_pairs.append((names[i], names[j], corr))
            flag = '🔴' if corr > 0.7 else '🟡' if corr > 0.4 else '🟢' if corr > 0 else '⚪'
            print(f"  {flag}{corr:>+5.2f}", end='')
        print()
    
    # 4. 板块 集中度
    print()
    print("=" * 70)
    print("📊 板块 集中度 分析")
    print("=" * 70)
    
    sectors = {}
    for code, d in data.items():
        # 主要 板块 (取 sector 第一段)
        main_sec = d['sector'].split('/')[0]
        if main_sec not in sectors: sectors[main_sec] = 0
        sectors[main_sec] += d['mv']
    
    print()
    for sec, mv in sorted(sectors.items(), key=lambda x: -x[1]):
        pct = mv / total_mv * 100
        flag = '🔴 过集中' if pct > 60 else '⚠️ 集中' if pct > 40 else '🟢 健康'
        print(f"  {sec:<14s}  ¥{mv/10000:>5.1f}万  {pct:>5.1f}%  {flag}")
    
    # 含 半导体 / AI / CPO 重合 板块
    semi_keywords = ['半导体', 'CPO', 'AI', '光通信', 'SiC']
    semi_mv = sum(d['mv'] for d in data.values() if any(kw in d['sector'] for kw in semi_keywords))
    semi_pct = semi_mv / total_mv * 100
    print(f"\n  🌐 半导体 / CPO / AI 算力 总占比: {semi_pct:.1f}%")
    if semi_pct > 80:
        print(f"     🚨 严重 过度集中 / 系统性 板块风险")
    elif semi_pct > 60:
        print(f"     ⚠️ 集中度 高 / 单板块 大跌 全军覆没")
    
    # 5. 高 相关 对 警示
    print()
    print("=" * 70)
    print("⚠️ 高相关 持仓 对")
    print("=" * 70)
    
    high_corr_pairs = sorted([p for p in corr_pairs if p[2] > 0.6], key=lambda x: -x[2])
    if high_corr_pairs:
        print()
        for n1, n2, c in high_corr_pairs:
            level = '🔴 极高' if c > 0.8 else '🟡 高'
            print(f"  {level}  {n1} ↔ {n2}: 相关性 {c:+.2f}")
            print(f"      → 二者 同涨同跌 / 没有 分散 风险")
    else:
        print("\n  ✅ 无 极高相关 持仓 对 (>0.6)")
    
    # 6. 优化 建议
    print()
    print("=" * 70)
    print("💡 优化 建议")
    print("=" * 70)
    
    print()
    
    # 单股 仓位 检查
    for code, d in data.items():
        weight = d['mv'] / total_mv * 100
        if weight > 50:
            print(f"  🚨 {d['name']} 单股 {weight:.1f}% > 50% / 必须 减仓")
        elif weight > 35:
            print(f"  ⚠️ {d['name']} 单股 {weight:.1f}% > 35% / 建议 减仓")
    
    # 板块 集中度
    if semi_pct > 70:
        print(f"\n  🚨 半导体链 集中度 {semi_pct:.1f}% 过高")
        print(f"     建议: 减 1-2 只 + 增配 不同板块 (医药 / 消费 / 新能源)")
    
    # 相关性
    if any(c > 0.8 for _, _, c in corr_pairs):
        print(f"\n  ⚠️ 部分 持仓 相关性 >0.8 / 分散 效果 接近 0")
        print(f"     建议: 减仓 1 个 同方向标的 / 选 不同周期 行业")
    
    # 投资组合 整体 指标
    print()
    print("=" * 70)
    print("📈 组合 整体 表现")
    print("=" * 70)
    
    # 加权 年化收益 / 波动
    portfolio_ret = sum(d['annual_ret'] * (d['mv']/total_mv) for d in data.values())
    portfolio_vol = math.sqrt(sum((d['annual_vol'] * (d['mv']/total_mv)) ** 2 for d in data.values()))  # 简化 (忽略协方差)
    portfolio_sharpe = (portfolio_ret - 3) / portfolio_vol if portfolio_vol > 0 else 0
    
    print(f"\n  📊 加权 年化 收益: {portfolio_ret:+.1f}%")
    print(f"  📊 加权 年化 波动: {portfolio_vol:.1f}%")
    print(f"  📊 组合 夏普比: {portfolio_sharpe:+.2f}")
    
    if portfolio_sharpe > 1.5:
        print(f"\n  🌟 组合 优秀 (夏普 >1.5)")
    elif portfolio_sharpe > 1.0:
        print(f"\n  🟢 组合 良好 (夏普 1.0-1.5)")
    elif portfolio_sharpe > 0:
        print(f"\n  🟡 组合 中性 (夏普 0-1.0)")
    else:
        print(f"\n  🔴 组合 不佳 (夏普 ≤ 0)")
    
    # 理想 配置 vs 当前
    print()
    print("=" * 70)
    print("🎯 理想 vs 当前 持仓")
    print("=" * 70)
    print(f"\n{'股票':<10s} {'当前':>7s} {'建议':>7s} {'差异':>8s}")
    print('-' * 40)
    
    # 简化 等权 + 风险 调整
    n = len(data)
    base_weight = 100 / n
    
    for code, d in data.items():
        cur_weight = d['mv'] / total_mv * 100
        # 推荐: 单股 ≤ 30% / 等权偏好
        if cur_weight > 35:
            target = 30
        elif cur_weight < 5:
            target = 10
        else:
            target = base_weight
        
        diff = target - cur_weight
        if abs(diff) < 5:
            action = '✅ 维持'
        elif diff > 5:
            action = f'🟢 加 {diff:.0f}%'
        else:
            action = f'🔴 减 {abs(diff):.0f}%'
        
        print(f"  {d['name']:<8s} {cur_weight:>5.1f}% {target:>5.0f}% {action:>15s}")
    
    print()
    print("=" * 70)
    print("💎 v5.0 + Markowitz 综合 决策")
    print("=" * 70)
    print("""
  ✅ 当前 组合 是 主升浪 + 主线集中型 (高风险高收益)
  ✅ 适合 牛市 / 不适合 大盘 转弱
  
  📋 优化 路径:
    1. 减仓 单股 仓位 >35% 的 票 → 单股 ≤ 30%
    2. 半导体链 占比 >70% → 减到 ≤ 50%
    3. 增配 不同 板块 (医药 / 消费 / 新能源 / 银行)
    4. 设 整体 净敞口 ≤ 80% (留 20% 现金)
    
  🎯 行动:
    • 现金 弹药 ≥ 15%
    • 5 只持仓 / 板块 互补
    • 单股 ≤ 30%
    • 同方向标的 ≤ 2 只
""")


if __name__ == '__main__':
    main()
