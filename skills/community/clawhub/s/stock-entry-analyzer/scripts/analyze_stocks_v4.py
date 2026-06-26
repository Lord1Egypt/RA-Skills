#!/usr/bin/env python3
"""
Stock Entry Analyzer v4 - 多指标股票入场分析（真实指标计算版）
基于乖离率 (BIAS) 为核心，结合多指标综合评分

数据源：
- 实时行情：stock-price-query v1.1.6
- 历史 K 线：腾讯财经 API（用于计算 MACD/RSI/KDJ）

修复内容：
1. 使用真实 EMA20 数据
2. 乖离率公式：ln(close) - ln(ema20) 【减法版】
3. 阈值：5%-15%
4. MACD/RSI/KDJ 使用真实计算
"""

import sys
import json
import subprocess
import os
import math
from datetime import datetime, timedelta

# 标的配置（26 只）
STOCKS = [
    {'name': '三花智控', 'code': '002050', 'type': 'A'},
    {'name': '绿的谐波', 'code': '688017', 'type': 'A'},
    {'name': '兆威机电', 'code': '003021', 'type': 'A'},
    {'name': '拓普集团', 'code': '601689', 'type': 'A'},
    {'name': '光伏 ETF', 'code': '515790', 'type': 'A'},
    {'name': '三安光电', 'code': '600703', 'type': 'A'},
    {'name': '中国东航', 'code': '600115', 'type': 'A'},
    {'name': '诺德股份', 'code': '600110', 'type': 'A'},
    {'name': '寒武纪', 'code': '688256', 'type': 'A'},
    {'name': '中科曙光', 'code': '603019', 'type': 'A'},
    {'name': '兆易创新', 'code': '603986', 'type': 'A'},
    {'name': '长电科技', 'code': '600584', 'type': 'A'},
    {'name': '大族激光', 'code': '002008', 'type': 'A'},
    {'name': '中国中免', 'code': '601888', 'type': 'A'},
    {'name': '科创芯片 ETF 嘉实', 'code': '588200', 'type': 'A'},
    {'name': '泡泡玛特', 'code': '09992', 'type': 'HK'},
    {'name': '宁德时代', 'code': '300750', 'type': 'A'},
    {'name': '恒瑞医药', 'code': '600276', 'type': 'A'},
    {'name': '腾讯控股', 'code': '00700', 'type': 'HK'},
    {'name': '双汇发展', 'code': '000895', 'type': 'A'},
    {'name': '贵州茅台', 'code': '600519', 'type': 'A'},
    {'name': '五粮液', 'code': '000858', 'type': 'A'},
    {'name': '中芯国际 (A)', 'code': '688981', 'type': 'A'},
    {'name': '比亚迪', 'code': '002594', 'type': 'A'},
    {'name': '立讯精密', 'code': '002475', 'type': 'A'},
    {'name': '天赐材料', 'code': '002709', 'type': 'A'},
    {'name': '恩捷股份', 'code': '002812', 'type': 'A'},
    {'name': '亿纬锂能', 'code': '300014', 'type': 'A'},
    {'name': '凯莱英', 'code': '002821', 'type': 'A'},
    {'name': '爱美客', 'code': '300896', 'type': 'A'},
    {'name': '通策医疗', 'code': '600763', 'type': 'A'},
    {'name': '中芯国际 (H)', 'code': '00981', 'type': 'HK'},
    {'name': '海光信息', 'code': '688041', 'type': 'A'},
    {'name': '阿里巴巴', 'code': '09988', 'type': 'HK'},
]


# ==================== 技术指标计算函数 ====================

def calc_ema(prices: list, period: int = 20) -> float | None:
    """计算指数移动平均 (EMA)"""
    if len(prices) < period:
        return None
    
    multiplier = 2 / (period + 1)
    ema = sum(prices[:period]) / period  # 初始 SMA
    
    for price in prices[period:]:
        ema = (price - ema) * multiplier + ema
    
    return ema


def calc_bias(close: float, ema20: float) -> float | None:
    """
    计算乖离率（减法版 - 刘晨明原文）
    公式：ln(close) - ln(ema20)
    """
    if ema20 is None or ema20 <= 0 or close <= 0:
        return None
    return math.log(close) - math.log(ema20)


def calc_rsi(closes: list, window: int = 14) -> float | None:
    """
    计算 RSI（相对强弱指标）
    RSI = 100 - (100 / (1 + RS))
    RS = 平均涨幅 / 平均跌幅
    """
    if len(closes) < window + 1:
        return None
    
    # 计算每日涨跌幅
    deltas = [closes[i] - closes[i-1] for i in range(1, len(closes))]
    
    # 取最近 window 天
    recent = deltas[-window:]
    
    gains = [d for d in recent if d > 0]
    losses = [-d for d in recent if d < 0]
    
    if not losses:
        return 100.0  # 全部上涨
    if not gains:
        return 0.0  # 全部下跌
    
    avg_gain = sum(gains) / window
    avg_loss = sum(losses) / window
    
    if avg_loss == 0:
        return 100.0
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    
    return rsi


def calc_macd(closes: list, fast: int = 12, slow: int = 26, signal: int = 9) -> dict | None:
    """
    计算 MACD（指数平滑异同移动平均线）
    返回：macd, signal_line, histogram, is_golden_cross
    """
    if len(closes) < slow + signal:
        return None
    
    # 计算 EMA
    def ema(data, period):
        multiplier = 2 / (period + 1)
        result = [sum(data[:period]) / period]
        for val in data[period:]:
            result.append((val - result[-1]) * multiplier + result[-1])
        return result
    
    ema_fast = ema(closes, fast)
    ema_slow = ema(closes, slow)
    
    # MACD 线 = 快线 - 慢线
    macd_line = [ema_fast[i] - ema_slow[i] for i in range(len(ema_slow))]
    
    # 信号线 = MACD 的 EMA
    signal_line = ema(macd_line, signal)
    
    # 柱状图 = MACD 线 - 信号线
    histogram = [macd_line[i] - signal_line[i] for i in range(len(signal_line))]
    
    # 判断金叉/死叉（最近一天）
    is_golden_cross = histogram[-1] > 0 and histogram[-2] <= 0
    is_death_cross = histogram[-1] < 0 and histogram[-2] >= 0
    
    return {
        'macd': macd_line[-1],
        'signal': signal_line[-1],
        'histogram': histogram[-1],
        'golden_cross': is_golden_cross,
        'death_cross': is_death_cross
    }


def calc_kdj(highs: list, lows: list, closes: list, n: int = 9, m1: int = 3, m2: int = 3) -> dict | None:
    """
    计算 KDJ（随机指标）
    返回：K, D, J, is_golden_cross
    """
    if len(closes) < n + m1:
        return None
    
    # 计算 RSV
    rsv_list = []
    for i in range(n-1, len(closes)):
        lowest_n = min(lows[i-n+1:i+1])
        highest_n = max(highs[i-n+1:i+1])
        
        if highest_n == lowest_n:
            rsv = 50
        else:
            rsv = ((closes[i] - lowest_n) / (highest_n - lowest_n)) * 100
        
        rsv_list.append(rsv)
    
    # 计算 K 值（RSV 的 M1 日 SMA）
    k_list = []
    k = 50  # 初始值
    for rsv in rsv_list:
        k = (2/3) * k + (1/3) * rsv
        k_list.append(k)
    
    # 计算 D 值（K 的 M2 日 SMA）
    d_list = []
    d = 50  # 初始值
    for k in k_list:
        d = (2/3) * d + (1/3) * k
        d_list.append(d)
    
    # 计算 J 值
    j_list = [3 * k_list[i] - 2 * d_list[i] for i in range(len(k_list))]
    
    # 判断金叉/死叉
    is_golden_cross = k_list[-1] > d_list[-1] and k_list[-2] <= d_list[-2]
    is_death_cross = k_list[-1] < d_list[-1] and k_list[-2] >= d_list[-2]
    
    return {
        'k': k_list[-1],
        'd': d_list[-1],
        'j': j_list[-1],
        'golden_cross': is_golden_cross,
        'death_cross': is_death_cross
    }


# ==================== 数据获取函数 ====================

def get_realtime_data(codes: list) -> dict:
    """调用 stock-price-query v1.1.6 获取实时行情数据"""
    all_data = {}
    batch_size = 20
    
    for i in range(0, len(codes), batch_size):
        batch = codes[i:i + batch_size]
        query_str = ",".join(batch)
        
        try:
            result = subprocess.run(
                ['python3', '/root/.openclaw/workspace/skills/stock-price-query/scripts/stock_query.py', query_str],
                capture_output=True,
                text=True,
                timeout=90
            )
            if result.returncode == 0:
                data = json.loads(result.stdout)
                batch_data = {item['code']: item for item in data if item.get('status') == 'success'}
                all_data.update(batch_data)
        except Exception as e:
            print(f"获取实时数据失败 (batch {i//batch_size + 1}): {e}", file=sys.stderr)
    
    return all_data


def get_history_data(code: str, market: str, days: int = 60) -> list | None:
    """获取历史 K 线数据用于技术指标计算"""
    try:
        result = subprocess.run(
            ['python3', '/root/.openclaw/workspace/skills/stock-price-query/scripts/stock_query.py', code, '--history', str(days)],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            if data.get('status') == 'success':
                return data.get('data', [])
    except Exception as e:
        print(f"获取历史数据失败 {code}: {e}", file=sys.stderr)
    
    return None


# ==================== 分析函数 ====================

def analyze_stock(stock: dict, realtime_data: dict) -> dict | None:
    """分析单只股票"""
    code = stock['code']
    name = stock['name']
    market_type = stock['type']
    
    # 获取实时数据
    real_data = realtime_data.get(code)
    if not real_data or real_data.get('status') != 'success':
        return None
    
    current_price = real_data.get('current_price', 0)
    change_pct = real_data.get('change_percent', 0)
    volume = real_data.get('volume', 0)
    
    # 获取历史数据
    history = get_history_data(code, market_type, days=60)
    if not history or len(history) < 30:
        # 历史数据不足，使用简化分析
        return analyze_stock_simple(stock, real_data)
    
    # 提取价格序列
    closes = [item['close'] for item in history]
    highs = [item['high'] for item in history]
    lows = [item['low'] for item in history]
    
    # 计算 EMA20
    ema20 = calc_ema(closes, 20)
    if ema20 is None:
        return analyze_stock_simple(stock, real_data)
    
    # 计算乖离率（减法版）
    bias = calc_bias(current_price, ema20)
    bias_pct = bias * 100 if bias else 0
    
    # 计算 RSI
    rsi = calc_rsi(closes, 14)
    
    # 计算 MACD
    macd_data = calc_macd(closes)
    
    # 计算 KDJ
    kdj_data = calc_kdj(highs, lows, closes)
    
    # 判断均线状态
    ma_trend = 'bullish' if bias and bias > 0 else 'bearish'
    
    # 评分计算
    score = 0
    checks = []
    
    # 1. 乖离率评分（权重 30%）
    if bias is not None:
        if 5.0 <= bias_pct <= 15.0:
            score += 30
            checks.append({'name': '乖离率', 'value': f'{bias_pct:+.2f}%', 'pass': True, 'desc': '最佳区间'})
        elif 0 < bias_pct < 5.0:
            score += 15
            checks.append({'name': '乖离率', 'value': f'{bias_pct:+.2f}%', 'pass': False, 'desc': '偏离度不足'})
        elif bias_pct > 15.0:
            score += 5
            checks.append({'name': '乖离率', 'value': f'{bias_pct:+.2f}%', 'pass': False, 'desc': '偏高警惕'})
        elif -5.0 <= bias_pct <= 0:
            score += 10
            checks.append({'name': '乖离率', 'value': f'{bias_pct:+.2f}%', 'pass': False, 'desc': '坚守区间'})
        else:
            checks.append({'name': '乖离率', 'value': f'{bias_pct:+.2f}%', 'pass': False, 'desc': '离场信号'})
    
    # 2. 均线系统（权重 15%）
    if ma_trend == 'bullish':
        score += 15
        checks.append({'name': '均线', 'value': '多头', 'pass': True})
    else:
        checks.append({'name': '均线', 'value': '空头', 'pass': False})
    
    # 3. MACD（权重 15%）
    if macd_data:
        if macd_data['golden_cross'] or macd_data['histogram'] > 0:
            score += 15
            checks.append({'name': 'MACD', 'value': '金叉' if macd_data['golden_cross'] else '红柱', 'pass': True})
        else:
            checks.append({'name': 'MACD', 'value': '死叉/绿柱', 'pass': False})
    else:
        checks.append({'name': 'MACD', 'value': 'N/A', 'pass': False})
    
    # 4. RSI（权重 10%）
    if rsi is not None:
        if 40 <= rsi <= 60:
            score += 10
            checks.append({'name': 'RSI', 'value': f'{rsi:.1f}', 'pass': True, 'desc': '中性区'})
        elif 60 < rsi < 70:
            score += 5
            checks.append({'name': 'RSI', 'value': f'{rsi:.1f}', 'pass': False, 'desc': '偏强'})
        elif rsi >= 70:
            checks.append({'name': 'RSI', 'value': f'{rsi:.1f}', 'pass': False, 'desc': '超买'})
        elif 30 <= rsi < 40:
            score += 5
            checks.append({'name': 'RSI', 'value': f'{rsi:.1f}', 'pass': False, 'desc': '偏弱'})
        else:
            checks.append({'name': 'RSI', 'value': f'{rsi:.1f}', 'pass': False, 'desc': '超卖'})
    else:
        checks.append({'name': 'RSI', 'value': 'N/A', 'pass': False})
    
    # 5. KDJ（权重 10%）
    if kdj_data:
        if kdj_data['golden_cross'] or (kdj_data['k'] > kdj_data['d']):
            score += 10
            checks.append({'name': 'KDJ', 'value': '金叉' if kdj_data['golden_cross'] else 'K>D', 'pass': True})
        else:
            checks.append({'name': 'KDJ', 'value': '死叉/K<D', 'pass': False})
    else:
        checks.append({'name': 'KDJ', 'value': 'N/A', 'pass': False})
    
    # 6. 量比（权重 10%）- 简化：用成交量判断
    if volume > 50000000:
        score += 10
        checks.append({'name': '成交量', 'value': '放量', 'pass': True})
    else:
        checks.append({'name': '成交量', 'value': '缩量', 'pass': False})
    
    # 7. 主力流向（权重 10%）- 简化：用涨跌幅判断
    if change_pct > 0:
        score += 10
        checks.append({'name': '主力', 'value': '净流入', 'pass': True})
    else:
        checks.append({'name': '主力', 'value': '净流出', 'pass': False})
    
    # 操作建议
    if score >= 80:
        action = '🟢 入场 20-30%'
    elif score >= 60:
        action = '🟡 考虑 10-20%'
    elif score >= 40:
        action = '🔴 观望'
    else:
        action = '🔴 回避'
    
    return {
        'name': name,
        'code': code,
        'score': score,
        'price': current_price,
        'change_pct': change_pct,
        'ema20': ema20,
        'bias': bias_pct,
        'rsi': rsi,
        'macd': macd_data,
        'kdj': kdj_data,
        'ma_trend': ma_trend,
        'volume': volume,
        'checks': checks,
        'action': action,
        'uses_real_indicators': True
    }


def analyze_stock_simple(stock: dict, real_data: dict) -> dict:
    """简化分析（当历史数据不足时）"""
    code = stock['code']
    name = stock['name']
    
    current_price = real_data.get('current_price', 0)
    change_pct = real_data.get('change_percent', 0)
    volume = real_data.get('volume', 0)
    
    # 简化：仅基于涨跌幅和成交量
    score = 50
    if change_pct > 2:
        score += 20
    elif change_pct > 0:
        score += 10
    elif change_pct < -2:
        score -= 20
    elif change_pct < 0:
        score -= 10
    
    if volume > 50000000:
        score += 10
    
    score = max(0, min(100, score))
    
    return {
        'name': name,
        'code': code,
        'score': score,
        'price': current_price,
        'change_pct': change_pct,
        'ema20': current_price,  # 估算
        'bias': 0,
        'rsi': 50,  # 中性
        'macd': {'golden_cross': change_pct > 0, 'histogram': change_pct},
        'kdj': {'golden_cross': change_pct > 0, 'k': 50, 'd': 50},
        'ma_trend': 'bullish' if change_pct > 0 else 'bearish',
        'volume': volume,
        'checks': [],
        'action': '🔴 观望' if score < 60 else '🟡 考虑',
        'uses_real_indicators': False
    }


# ==================== 报告生成 ====================

def generate_report(results: list) -> str:
    """生成 Markdown 格式报告"""
    report = []
    
    report.append("# 📊 股票买入分析报告")
    report.append("")
    report.append(f"**生成时间：** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    report.append(f"**分析方法：** 乖离率 (BIAS) + 多指标共振（真实计算）")
    report.append(f"**分析标的：** {len(results)} 只")
    
    avg_score = sum(r['score'] for r in results) / len(results) if results else 0
    good_count = len([r for r in results if r['score'] >= 60])
    
    report.append(f"**平均评分：** {avg_score:.1f} 分")
    report.append(f"**达标标的：** {good_count} 只 (≥60 分)")
    report.append("")
    report.append("---")
    report.append("")
    
    # 综合排名表
    report.append("## 📋 综合排名表")
    report.append("")
    report.append("| 排名 | 标的 | 代码 | 评分 | 股价 | 涨跌幅 | EMA20 | 乖离率 | RSI | MACD | KDJ | 操作建议 |")
    report.append("|------|------|------|------|------|--------|-------|--------|-----|------|-----|----------|")
    
    # 按评分排序
    sorted_results = sorted(results, key=lambda x: x['score'], reverse=True)
    
    for i, r in enumerate(sorted_results, 1):
        code = r['code']
        price_prefix = 'HK$' if '.HK' in code or r.get('market') == 'HK' else '¥'
        
        macd_status = '✅' if r['macd'] and r['macd'].get('golden_cross') else '🟡' if r['macd'] else '❌'
        kdj_status = '✅' if r['kdj'] and r['kdj'].get('golden_cross') else '🟡' if r['kdj'] else '❌'
        
        rsi_status = f"{r['rsi']:.0f}" if r['rsi'] else 'N/A'
        
        report.append(
            f"| {i} | {r['name']} | {code} | {r['score']}分 | {price_prefix}{r['price']:.2f} | "
            f"{r['change_pct']:+.2f}% | {price_prefix}{r['ema20']:.2f} | {r['bias']:+.2f}% | "
            f"{rsi_status} | {macd_status} | {kdj_status} | {r['action']} |"
        )
    
    report.append("")
    report.append("---")
    report.append("")
    
    # 重点关注标的（评分≥60 分）
    good_stocks = [r for r in sorted_results if r['score'] >= 60]
    if good_stocks:
        report.append("## ⭐ 重点关注标的 (评分≥60 分)")
        report.append("")
        
        for r in good_stocks[:5]:  # 最多展示 5 只
            report.append(f"### {r['name']} ({r['code']}) — {r['score']}分")
            report.append("")
            report.append(f"**操作建议：** {r['action']}")
            report.append("")
            
            if r['checks']:
                report.append("**检查清单：**")
                for check in r['checks']:
                    status = '✅' if check['pass'] else '❌'
                    desc = check.get('desc', '')
                    report.append(f"- {status} {check['name']}: {check['value']} {desc}")
                report.append("")
    
    # 整体策略
    report.append("## 📋 整体策略建议")
    report.append("")
    
    if avg_score >= 70:
        market_status = '🟢'
        market_desc = '市场情绪良好，可积极布局'
    elif avg_score >= 50:
        market_status = '🟡'
        market_desc = '市场震荡分化，精选个股'
    else:
        market_status = '🔴'
        market_desc = '市场整体偏弱，保持观望'
    
    report.append(f"**市场状态：** {market_status} {market_desc}")
    report.append("")
    report.append(f"- 平均评分：{avg_score:.1f}分")
    report.append(f"- 达标标的：{good_count}只")
    report.append(f"- 最高评分：{sorted_results[0]['score']}分 ({sorted_results[0]['name']})")
    report.append("")
    report.append("---")
    report.append("")
    report.append("*风险提示：本报告基于技术指标分析，不构成投资建议。市场有风险，投资需谨慎。*")
    
    return '\n'.join(report)


def generate_wechat_message(results: list) -> str:
    """生成微信消息（简化版表格）"""
    lines = []
    lines.append("📊 股票买入分析报告")
    lines.append("")
    lines.append(f"**分析标的：** {len(results)} 只")
    
    avg_score = sum(r['score'] for r in results) / len(results) if results else 0
    good_count = len([r for r in results if r['score'] >= 60])
    
    lines.append(f"**平均评分：** {avg_score:.1f} 分")
    lines.append(f"**达标标的：** {good_count} 只 (≥60 分)")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("| 标的 | 评分 | 股价 | 涨跌幅 | EMA20 | 乖离率 | RSI | MACD | KDJ | 操作建议 |")
    lines.append("|------|------|------|--------|-------|--------|-----|------|-----|----------|")
    
    sorted_results = sorted(results, key=lambda x: x['score'], reverse=True)
    
    for r in sorted_results[:25]:  # 最多 25 只
        code = r['code']
        price_prefix = 'HK$' if '.HK' in code or r.get('market') == 'HK' else '¥'
        
        macd_status = '✅' if r['macd'] and r['macd'].get('golden_cross') else '🟡' if r['macd'] else '❌'
        kdj_status = '✅' if r['kdj'] and r['kdj'].get('golden_cross') else '🟡' if r['kdj'] else '❌'
        
        rsi_status = f"{r['rsi']:.0f}" if r['rsi'] else 'N/A'
        
        lines.append(
            f"| {r['name']} | {r['score']}分 | {price_prefix}{r['price']:.2f} | "
            f"{r['change_pct']:+.2f}% | {r['ema20']:.2f} | {r['bias']:+.2f}% | "
            f"{rsi_status} | {macd_status} | {kdj_status} | {r['action']} |"
        )
    
    lines.append("")
    lines.append(f"*完整报告共 {len(results)} 只股票*")
    lines.append("")
    lines.append("【数据源】✅ stock-price-query v1.1.6 + stock-entry-analyzer v4.0.0 (真实指标计算)")
    
    return '\n'.join(lines)


# ==================== 主函数 ====================

def main():
    print(f"开始执行股票监控任务 (v4.0.0 真实指标计算版)...", file=sys.stderr)
    
    # 获取实时数据
    codes = [s['code'] for s in STOCKS]
    print(f"正在获取 {len(codes)} 只股票的实时数据...", file=sys.stderr)
    realtime_data = get_realtime_data(codes)
    print(f"✅ 获取到 {len(realtime_data)} 只股票实时数据", file=sys.stderr)
    
    # 分析每只股票
    results = []
    for i, stock in enumerate(STOCKS, 1):
        print(f"[{i}/{len(STOCKS)}] 分析 {stock['name']}...", file=sys.stderr)
        result = analyze_stock(stock, realtime_data)
        if result:
            results.append(result)
    
    print(f"✅ 完成 {len(results)} 只股票分析", file=sys.stderr)
    print(f"   平均评分：{sum(r['score'] for r in results)/len(results):.1f}分", file=sys.stderr)
    print(f"   ≥60 分：{len([r for r in results if r['score'] >= 60])}只", file=sys.stderr)
    
    # 生成报告
    report_md = generate_report(results)
    wechat_msg = generate_wechat_message(results)
    
    # 保存报告
    timestamp = datetime.now().strftime('%Y%m%d_%H%M')
    report_path = f"/root/.openclaw/workspace/stock_analysis_report_{timestamp}.md"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_md)
    print(f"✅ 报告已保存：{report_path}", file=sys.stderr)
    
    # 输出 JSON（供自动化脚本使用）
    output = {
        'status': 'success',
        'timestamp': timestamp,
        'message': wechat_msg,
        'report_path': report_path,
        'data_count': len(results),
        'avg_score': sum(r['score'] for r in results) / len(results) if results else 0,
        'count_above_60': len([r for r in results if r['score'] >= 60]),
        'results': results
    }
    
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
