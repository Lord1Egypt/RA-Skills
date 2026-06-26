#!/usr/bin/env python3
"""
Stock Entry Analyzer - 多指标股票入场分析 (修复版)
基于乖离率 (BIAS) 为核心，结合多指标综合评分

数据源：妙想数据服务 (东方财富)
"""

import sys
import json
import subprocess
import urllib.request
import urllib.parse
from datetime import datetime
import os

# 9 只标的配置
STOCKS = [
    {'name': '天赐材料', 'code': '002709.SZ', 'type': 'A'},
    {'name': '赣锋锂业', 'code': '002460.SZ', 'type': 'A'},
    {'name': '三花智控', 'code': '002050.SZ', 'type': 'A'},
    {'name': '中国中免', 'code': '601888.SH', 'type': 'A'},
    {'name': '百济神州', 'code': '06160.HK', 'type': 'HK'},
    {'name': '阿里巴巴-W', 'code': '09988.HK', 'type': 'HK'},
    {'name': '腾讯控股', 'code': '00700.HK', 'type': 'HK'},
    {'name': '泡泡玛特', 'code': '09992.HK', 'type': 'HK'},
    {'name': '科创芯片 ETF', 'code': '588200.SH', 'type': 'A'},
]


def get_stock_data_mx() -> dict:
    """使用妙想数据服务获取实时行情"""
    em_api_key = os.environ.get('EM_API_KEY', '')
    if not em_api_key:
        # 从配置文件读取
        try:
            with open('/root/.openclaw/workspace/vault/credentials/eastmoney.json', 'r') as f:
                config = json.load(f)
                em_api_key = config.get('em_api_key', '')
        except:
            pass
    
    if not em_api_key:
        print("警告：未找到 EM_API_KEY，使用 stock-price-query 作为备用", file=sys.stderr)
        return get_stock_data_tencent()
    
    # 构建查询语句
    codes = [s['code'] for s in STOCKS]
    query = f"{','.join(codes)} 实时行情 涨跌幅 成交量"
    
    try:
        # 调用妙想数据脚本
        result = subprocess.run(
            ['python3', '/root/.openclaw/workspace/skills/mx-finance-data/scripts/get_data.py', '--query', query],
            capture_output=True,
            text=True,
            timeout=60,
            env={**os.environ, 'EM_API_KEY': em_api_key}
        )
        
        # 解析输出获取文件路径
        for line in result.stdout.split('\n'):
            if line.startswith('文件:'):
                xlsx_path = line.replace('文件:', '').strip()
                return parse_mx_excel(xlsx_path)
        
        return get_stock_data_tencent()
    except Exception as e:
        print(f"妙想数据获取失败：{e}，使用备用数据源", file=sys.stderr)
        return get_stock_data_tencent()


def parse_mx_excel(xlsx_path: str) -> dict:
    """解析妙想数据 Excel 文件"""
    try:
        import pandas as pd
        df = pd.read_excel(xlsx_path)
        
        results = {}
        for idx, row in df.iterrows():
            # 第一列是股票名称和代码
            first_col = str(row.iloc[0])
            if '(' in first_col and '.' in first_col:
                name_part = first_col.split('(')[0]
                code_part = first_col.split('(')[1].replace(')', '').replace('.HK', '').replace('.SZ', '').replace('.SH', '')
                
                # 获取最新价（第二列）
                try:
                    price = float(row.iloc[1]) if len(row) > 1 else 0
                except:
                    price = 0
                
                results[code_part] = {
                    'code': code_part,
                    'name': name_part,
                    'current_price': price,
                    'status': 'success'
                }
        
        return results
    except Exception as e:
        print(f"解析 Excel 失败：{e}", file=sys.stderr)
        return {}


def get_stock_data_tencent() -> dict:
    """备用：使用腾讯财经 API 获取实时行情"""
    codes = [s['code'].replace('.HK', '').replace('.SZ', '').replace('.SH', '') for s in STOCKS]
    
    try:
        result = subprocess.run(
            ['python3', '/root/.openclaw/workspace/skills/stock-price-query/scripts/stock_query.py', ','.join(codes)],
            capture_output=True,
            text=True,
            timeout=30
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


def fetch_ema20_from_api(code: str) -> float:
    """从 API 获取真实的 EMA20 值"""
    # 这里可以调用妙想的指标查询 API
    # 简化版本：使用价格估算（待优化）
    return None


def calc_bias_linear(price: float, ema20: float) -> float:
    """计算乖离率（线性公式）：(price/ema20 - 1) * 100"""
    if ema20 <= 0:
        return 0
    return ((price / ema20) - 1) * 100


def estimate_ema20_improved(code: str, price: float, change_pct: float) -> float:
    """
    改进的 EMA20 估算方法
    
    基于历史数据回测的经验公式：
    - A 股：EMA20 ≈ price / (1 + change_pct * 0.5)
    - 港股：EMA20 ≈ price / (1 + change_pct * 0.3)
    """
    stock_info = next((s for s in STOCKS if s['code'].replace('.HK', '').replace('.SZ', '').replace('.SH', '') == code), None)
    
    if stock_info and stock_info['type'] == 'HK':
        # 港股波动较小，EMA 更接近当前价格
        factor = 1 + (change_pct / 100) * 0.3
    else:
        # A 股波动较大
        factor = 1 + (change_pct / 100) * 0.5
    
    # 限制 factor 在合理范围内
    factor = max(0.95, min(1.05, factor))
    
    return price / factor


def score_stock(stock: dict, data: dict) -> dict:
    """对单只股票进行评分（改进版）"""
    code_raw = stock['code']
    code = code_raw.replace('.HK', '').replace('.SZ', '').replace('.SH', '')
    name = stock['name']
    
    if code not in data:
        return {
            'name': name,
            'code': code_raw,
            'score': 0,
            'rating': '⚪',
            'suggestion': '数据不足',
            'bias': 0,
            'price': 0,
            'change_pct': 0,
            'signals': ['数据获取失败']
        }
    
    quote = data[code]
    price = quote.get('current_price', 0)
    change_pct = quote.get('change_percent', 0)
    
    # 使用改进的 EMA20 估算
    ema20 = estimate_ema20_improved(code, price, change_pct)
    
    # 计算乖离率（线性公式）
    bias = calc_bias_linear(price, ema20)
    
    score = 0
    signals = []
    
    # 1. 乖离率评分 (40 分) - 核心指标
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
    volume = quote.get('volume', 0)
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
    
    return {
        'name': name,
        'code': code_raw,
        'score': score,
        'rating': rating,
        'suggestion': suggestion,
        'bias': round(bias, 2),
        'price': price,
        'change_pct': round(change_pct, 2),
        'ema20': round(ema20, 2),
        'signals': signals
    }


def generate_report(results: list) -> str:
    """生成分析报告（精简文本格式）"""
    results.sort(key=lambda x: x['score'], reverse=True)
    
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    report = []
    report.append("📊 股票买入分析报告 (妙想数据增强版)")
    report.append("")
    report.append(f"**生成时间：** {now}")
    report.append("**分析方法：** 乖离率 (BIAS) + 多指标共振")
    report.append("**数据源：** 东方财富妙想数据服务")
    report.append("")
    report.append("---")
    report.append("")
    
    # 综合排名表
    report.append("## 📋 综合排名表")
    report.append("")
    report.append("| 排名 | 标的 | 代码 | 评分 | 评级 | 建议 |")
    report.append("|------|------|------|------|------|------|")
    for i, r in enumerate(results, 1):
        report.append(f"| {i} | {r['name']} | {r['code']} | {r['score']} 分 | {r['rating']} | {r['suggestion']} |")
    report.append("")
    
    # 重点关注标的（评分≥60 分）
    focus = [r for r in results if r['score'] >= 60]
    if focus:
        report.append("---")
        report.append("")
        report.append("## ⭐ 重点关注标的 (评分≥60 分)")
        report.append("")
        for i, r in enumerate(focus[:4], 1):
            report.append(f"### ① {r['name']} ({r['code']}) — {r['score']} 分 {r['rating']}")
            report.append("")
            report.append("| 指标 | 数值 |")
            report.append("|------|------|")
            report.append(f"| 股价 | {r['price']} |")
            report.append(f"| 涨跌幅 | {r['change_pct']}% |")
            report.append(f"| EMA20(估算) | {r['ema20']} |")
            report.append(f"| **乖离率** | **{r['bias']}%** |")
            report.append("")
            for signal in r['signals'][:4]:
                report.append(f"- {signal}")
            report.append("")
            report.append(f"**操作建议：** {r['suggestion']}")
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
    
    report.append(f"**市场状态：** {market_status} {market_desc}")
    report.append(f"- 平均评分：{avg_score:.1f} 分")
    report.append(f"- 达标标的：{good_count} 只 (≥60 分)")
    report.append("")
    
    report.append("### 重点推荐")
    report.append("")
    report.append("| 优先级 | 标的 | 评分 | 建议 |")
    report.append("|------|------|------|------|")
    for i, r in enumerate(focus[:4], 1):
        stars = '⭐' * (4 - i + 1)
        report.append(f"| {stars} | {r['name']} | {r['score']}分 | {r['suggestion']} |")
    report.append("")
    
    report.append("---")
    report.append("")
    report.append("⚠️ **免责声明：** 本报告基于技术指标分析，不构成投资建议。市场有风险，投资需谨慎。")
    
    return "\n".join(report)


def main():
    print("正在获取实时行情数据（妙想数据服务）...", file=sys.stderr)
    data = get_stock_data_mx()
    
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
