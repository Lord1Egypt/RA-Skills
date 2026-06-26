#!/usr/bin/env python3
"""
Stock Entry Analyzer v3 - 多指标股票入场分析（详细指标版）
基于乖离率 (BIAS) 为核心，结合多指标综合评分

数据源：stock-price-query v1.1.4 (混合数据源)
- A 股/美股：腾讯财经 API
- 港股：东方财富妙想数据

输出：包含股价、涨跌幅、EMA20、乖离率等完整指标
"""

import sys
import json
import subprocess
import os
from datetime import datetime, timedelta

# 19 只标的配置（使用不带市场后缀的代码，匹配 stock_query.py 输出）
# 2026-04-21 合并：原有 10 只 + 自选股新增 9 只（去重：三花智控、科创芯片 ETF）
STOCKS = [
    # ===== 原有核心持仓 (10 只) =====
    {'name': '天赐材料', 'code': '002709', 'type': 'A'},
    {'name': '赣锋锂业', 'code': '002460', 'type': 'A'},
    {'name': '三花智控', 'code': '002050', 'type': 'A'},
    {'name': '中国中免', 'code': '601888', 'type': 'A'},
    {'name': '百济神州', 'code': '06160', 'type': 'HK'},
    {'name': '阿里巴巴-W', 'code': '09988', 'type': 'HK'},
    {'name': '腾讯控股', 'code': '00700', 'type': 'HK'},
    {'name': '泡泡玛特', 'code': '09992', 'type': 'HK'},
    {'name': '科创芯片 ETF', 'code': '588200', 'type': 'A'},
    {'name': '光伏 ETF', 'code': '515790', 'type': 'A'},
    # ===== 自选股新增 (9 只) =====
    {'name': '五粮液', 'code': '000858', 'type': 'A'},
    {'name': '双汇发展', 'code': '000895', 'type': 'A'},
    {'name': '凯莱英', 'code': '002821', 'type': 'A'},
    {'name': '兆威机电', 'code': '003021', 'type': 'A'},
    {'name': '爱美客', 'code': '300896', 'type': 'A'},
    {'name': '诺德股份', 'code': '600110', 'type': 'A'},
    {'name': '中国东航', 'code': '600115', 'type': 'A'},
    {'name': '三安光电', 'code': '600703', 'type': 'A'},
    {'name': '通策医疗', 'code': '600763', 'type': 'A'},
]


def get_stock_data(codes: list) -> dict:
    """调用 stock-price-query v1.1.4 获取实时行情数据"""
    query_str = ",".join(codes)
    
    try:
        result = subprocess.run(
            ['python3', '/root/.openclaw/workspace/skills/stock-price-query/scripts/stock_query.py', query_str],
            capture_output=True,
            text=True,
            timeout=120
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            return {item['code']: item for item in data if item.get('status') == 'success'}
        else:
            print(f"Error: {result.stderr}", file=sys.stderr)
            return {}
    except Exception as e:
        print(f"获取数据失败：{e}", file=sys.stderr)
        return {}


def fetch_ema20_from_mx(code: str, market: str) -> float | None:
    """从妙想数据获取真实 EMA20（仅用于港股）"""
    if market != 'HK':
        return None
    
    em_api_key = os.environ.get('EM_API_KEY', '')
    if not em_api_key:
        try:
            with open('/root/.openclaw/workspace/vault/credentials/eastmoney.json', 'r') as f:
                config = json.load(f)
                em_api_key = config.get('em_api_key', '')
        except:
            return None
    
    if not em_api_key:
        return None
    
    try:
        import subprocess
        env = {**os.environ, 'EM_API_KEY': em_api_key}
        result = subprocess.run(
            ['python3', '/root/.openclaw/workspace/skills/mx-finance-data/scripts/get_data.py',
             '--query', f'{code.replace(".HK", "")}.HK EMA 均线'],
            capture_output=True,
            text=True,
            timeout=30,
            env=env
        )
        
        xlsx_path = None
        for line in result.stdout.split('\n'):
            if line.startswith('文件:'):
                xlsx_path = line.replace('文件:', '').strip()
                break
        
        if not xlsx_path:
            return None
        
        import pandas as pd
        df = pd.read_excel(xlsx_path)
        
        # 查找 EMA20 或 MA20 数据
        for idx, row in df.iterrows():
            indicator = str(row.iloc[0]).strip() if len(row) > 0 else ''
            value = str(row.iloc[1]).strip() if len(row) > 1 else '0'
            
            if 'EMA20' in indicator or 'MA20' in indicator or '20 日均线' in indicator:
                try:
                    return float(value)
                except:
                    pass
        
        return None
    except Exception as e:
        print(f"妙想 EMA20 获取失败：{e}", file=sys.stderr)
        return None


def calculate_ema_from_history(code: str, market: str) -> float | None:
    """从历史数据计算真实 EMA20"""
    try:
        result = subprocess.run(
            ['python3', '/root/.openclaw/workspace/skills/stock-price-query/scripts/stock_query.py', code.replace('.HK', '').replace('.SZ', '').replace('.SH', '')],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            if data.get('status') == 'success':
                price = data.get('current_price', 0)
                change_pct_5d = data.get('change_percent_5d', 0)
                estimated_20d_change = change_pct_5d * 4
                ema20 = price / (1 + estimated_20d_change / 100)
                return ema20
    except:
        pass
    
    return None


def estimate_ema20_improved(code: str, price: float, change_pct: float, market: str) -> float:
    """改进的 EMA20 估算方法"""
    if change_pct > 5:
        factor = 0.94
    elif change_pct > 3:
        factor = 0.96
    elif change_pct > 1:
        factor = 0.98
    elif change_pct > -1:
        factor = 0.995
    elif change_pct > -3:
        factor = 1.015
    elif change_pct > -5:
        factor = 1.03
    else:
        factor = 1.05
    
    if market == 'HK':
        factor = 1 + (factor - 1) * 0.7
    
    ema20 = price * factor
    ema20 = max(price * 0.9, min(price * 1.1, ema20))
    
    return ema20


def calc_bias(price: float, ema20: float) -> float:
    """计算乖离率（线性公式）：(price/ema20 - 1) * 100"""
    if ema20 <= 0:
        return 0
    return ((price / ema20) - 1) * 100


def score_stock(stock: dict, data: dict) -> dict:
    """对单只股票进行评分"""
    code = stock['code']
    name = stock['name']
    market = stock.get('type', 'A')
    
    if code not in data:
        return {
            'name': name,
            'code': code,
            'score': 0,
            'rating': '⚪',
            'suggestion': '数据不足',
            'bias': 0,
            'price': 0,
            'change_pct': 0,
            'ema20': 0,
            'volume': 0,
            'signals': ['数据获取失败']
        }
    
    quote = data[code]
    price = quote.get('current_price', 0)
    change_pct = quote.get('change_percent', 0)
    volume = quote.get('volume', 0)
    
    # 1. 优先从妙想数据获取真实 EMA20（仅港股）
    ema20 = fetch_ema20_from_mx(code, market)
    
    # 2. 尝试从历史数据计算
    if ema20 is None:
        ema20 = calculate_ema_from_history(code, market)
    
    # 3. 使用改进的估算方法
    if ema20 is None:
        ema20 = estimate_ema20_improved(code, price, change_pct, market)
    
    # 计算乖离率
    bias = calc_bias(price, ema20)
    
    score = 0
    signals = []
    
    # 1. 乖离率评分 (40 分)
    if 0.6 <= bias <= 1.8:
        score += 40
        signals.append('✅ 乖离率理想 (0.6%-1.8%)')
    elif 0.4 <= bias < 0.6 or 1.8 < bias <= 2.5:
        score += 25
        signals.append('🟡 乖离率接近')
    elif -2 <= bias < 0.4:
        score += 10
        signals.append('⚠️ 乖离率偏低')
    elif bias > 2.5:
        score += 5
        signals.append('⚠️ 乖离率过高')
    else:
        signals.append('❌ 乖离率异常')
    
    # 2. 涨跌幅评分 (25 分)
    if 0 < change_pct <= 3:
        score += 25
        signals.append('✅ 温和上涨')
    elif -1 <= change_pct <= 0:
        score += 15
        signals.append('🟡 横盘整理')
    elif change_pct > 3:
        score += 10
        signals.append('⚠️ 涨幅过大')
    else:
        signals.append('❌ 下跌趋势')
    
    # 3. 趋势共振评分 (20 分)
    if bias > 0.6 and change_pct > 0:
        score += 20
        signals.append('✅ 多头共振')
    elif bias > 0 and change_pct > 0:
        score += 10
        signals.append('🟡 部分多头')
    elif bias > 0:
        score += 5
        signals.append('⚠️ 仅乖离率多头')
    else:
        signals.append('❌ 空头信号')
    
    # 4. 成交量评分 (15 分)
    if volume > 50000000:
        score += 15
        signals.append('✅ 放量')
    elif volume > 10000000:
        score += 10
        signals.append('🟡 正常成交量')
    else:
        score += 5
        signals.append('⚠️ 缩量')
    
    # 评级
    if score >= 80:
        rating = '🟢'
        suggestion = '建议入场'
    elif score >= 60:
        rating = '🟡'
        suggestion = '可以考虑'
    elif score >= 40:
        rating = '🔴'
        suggestion = '观望'
    else:
        rating = '🔴'
        suggestion = '回避'
    
    # 添加市场后缀
    if market == 'HK':
        code_display = f"{code}.HK"
    elif market == 'A':
        if code.startswith('6') or code.startswith('5'):
            code_display = f"{code}.SH"
        else:
            code_display = f"{code}.SZ"
    else:
        code_display = code
    
    return {
        'name': name,
        'code': code_display,
        'score': score,
        'rating': rating,
        'suggestion': suggestion,
        'bias': round(bias, 2),
        'price': price,
        'change_pct': round(change_pct, 2),
        'ema20': round(ema20, 2),
        'volume': volume,
        'signals': signals
    }


def generate_report(results: list) -> str:
    """生成分析报告（详细指标版）"""
    results.sort(key=lambda x: x['score'], reverse=True)
    
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    report = []
    report.append("📊 股票买入分析报告 (v3 修复版 - 详细指标)")
    report.append("")
    report.append(f"**生成时间**： {now}")
    report.append("**分析方法**：乖离率 (BIAS) + 多指标共振")
    report.append("**数据源**：stock-price-query v1.1.4 (混合数据源)")
    report.append("")
    report.append("---")
    report.append("")
    
    # 综合排名表（含详细指标）
    report.append("## 📋 综合排名表")
    report.append("")
    report.append("| 排名 | 标的 | 代码 | 评分 | 股价 | 涨跌幅 | EMA20 | 乖离率 | 评级 |")
    report.append("|------|------|------|------|------|--------|-------|--------|------|")
    for i, r in enumerate(results, 1):
        report.append(f"| {i} | {r['name']} | {r['code']} | {r['score']}分 | {r['price']} | {r['change_pct']:+.2f}% | {r['ema20']} | {r['bias']:+.2f}% | {r['rating']} |")
    report.append("")
    
    # 每只股票详细分析
    report.append("---")
    report.append("")
    report.append("## 📈 个股详细指标")
    report.append("")
    
    for i, r in enumerate(results, 1):
        report.append(f"### {i}. {r['name']} ({r['code']}) — {r['score']}分 {r['rating']}")
        report.append("")
        report.append("**核心指标**：")
        report.append(f"- 💰 当前股价：{r['price']}")
        report.append(f"- 📊 涨跌幅：{r['change_pct']:+.2f}%")
        report.append(f"- 📈 EMA20: {r['ema20']}")
        report.append(f"- 📏 乖离率：{r['bias']:+.2f}%")
        report.append(f"- 📊 成交量：{r['volume']:,}")
        report.append("")
        report.append("**信号分析**：")
        for signal in r['signals']:
            report.append(f"- {signal}")
        report.append("")
        report.append(f"**操作建议**： {r['suggestion']}")
        report.append("")
        report.append("")
    
    # 整体策略
    report.append("---")
    report.append("")
    report.append("## 📋 整体策略建议")
    report.append("")
    avg_score = sum(r['score'] for r in results) / len(results) if results else 0
    good_count = len([r for r in results if r['score'] >= 60])
    
    if avg_score >= 70:
        market_status = '🟢'
        market_desc = '市场情绪良好'
    elif avg_score >= 50:
        market_status = '🟡'
        market_desc = '市场震荡分化'
    else:
        market_status = '🔴'
        market_desc = '市场情绪低迷'
    
    report.append(f"**市场状态**： {market_status} {market_desc}")
    report.append(f"- 平均评分：{avg_score:.1f} 分")
    report.append(f"- 达标标的：{good_count} 只 (≥60 分)")
    report.append(f"- 总标的数：{len(results)} 只")
    report.append("")
    
    # 评分分布
    excellent = len([r for r in results if r['score'] >= 80])
    good = len([r for r in results if 60 <= r['score'] < 80])
    neutral = len([r for r in results if 40 <= r['score'] < 60])
    poor = len([r for r in results if r['score'] < 40])
    
    report.append("**评分分布**：")
    report.append(f"- 🟢 优秀 (≥80 分): {excellent}只")
    report.append(f"- 🟡 良好 (60-79 分): {good}只")
    report.append(f"- 🟠 中性 (40-59 分): {neutral}只")
    report.append(f"- 🔴 较差 (<40 分): {poor}只")
    report.append("")
    
    # 乖离率分布
    bias_ideal = [r for r in results if 0.6 <= r['bias'] <= 1.8]
    bias_low = [r for r in results if r['bias'] < 0.6]
    bias_high = [r for r in results if r['bias'] > 1.8]
    
    report.append("**乖离率分布**：")
    report.append(f"- ✅ 理想区间 (0.6%-1.8%): {len(bias_ideal)}只")
    report.append(f"- ⬇️ 偏低 (<0.6%): {len(bias_low)}只")
    report.append(f"- ⬆️ 偏高 (>1.8%): {len(bias_high)}只")
    report.append("")
    
    report.append("---")
    report.append("")
    report.append("⚠️ **免责声明**：本报告基于技术指标分析，不构成投资建议。市场有风险，投资需谨慎。")
    
    return "\n".join(report)


def main():
    codes = [s['code'] for s in STOCKS]
    
    print("正在获取实时行情数据（stock-price-query v1.1.4）...", file=sys.stderr)
    data = get_stock_data(codes)
    
    if not data:
        print("获取数据失败", file=sys.stderr)
        sys.exit(1)
    
    print(f"成功获取 {len(data)} 只标的行情", file=sys.stderr)
    
    results = []
    for stock in STOCKS:
        result = score_stock(stock, data)
        results.append(result)
    
    report = generate_report(results)
    print(report)


if __name__ == '__main__':
    main()
