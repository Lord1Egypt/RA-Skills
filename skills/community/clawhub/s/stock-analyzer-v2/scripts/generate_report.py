#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票分析报告生成脚本

整合实时行情和基本面数据，生成 Markdown 格式分析报告。

使用方法:
    python scripts/generate_report.py --codes 03690.HK,300413.SZ --output report.md
    python scripts/generate_report.py --codes 600519.SH --output茅台分析.md --title "贵州茅台深度分析"
"""

import argparse
import os
import sys
import time
from datetime import datetime

def check_akshare():
    """检查并返回 akshare 模块"""
    try:
        import akshare as ak
        return ak
    except ImportError:
        print("❌ akshare 未安装，请运行: pip install akshare")
        sys.exit(1)

def check_jqdata():
    """检查聚宽配置，返回 jq 模块或 None"""
    phone = os.environ.get('JQDATA_PHONE')
    password = os.environ.get('JQDATA_PASSWORD')
    if not phone or not password:
        return None
    try:
        import jqdatasdk as jq
        jq.auth(phone, password)
        return jq
    except:
        return None

def parse_code(code):
    """解析股票代码"""
    if '.' in code:
        parts = code.split('.')
        return parts[1].upper(), parts[0]  # (市场, 纯代码)
    return 'SZ', code

def get_a_stock_price(ak, code):
    """获取 A股 实时行情"""
    try:
        df = ak.stock_zh_a_spot_em()
        row = df[df['代码'] == code]
        if row.empty:
            return None
        r = row.iloc[0]
        return {
            'code': code,
            'name': r['名称'],
            'price': float(r['最新价']),
            'change_pct': float(r['涨跌幅']),
            'volume': float(r['成交量']),
            'amount': float(r['成交额']),
            'high': float(r['最高']),
            'low': float(r['最低']),
            'open': float(r['今开']),
            'prev_close': float(r['昨收']),
        }
    except Exception as e:
        return {'code': code, 'error': str(e)}

def get_hk_stock_price(ak, code):
    """获取港股实时行情"""
    try:
        df = ak.stock_hk_spot_em()
        row = df[df['代码'] == code]
        if row.empty:
            return None
        r = row.iloc[0]
        return {
            'code': code,
            'name': r['名称'],
            'price': float(r['最新价']),
            'change_pct': float(r['涨跌幅']),
            'volume': float(r.get('成交量', 0)),
            'amount': float(r.get('成交额', 0)),
            'high': float(r.get('最高', 0)),
            'low': float(r.get('最低', 0)),
        }
    except Exception as e:
        return {'code': code, 'error': str(e)}

def get_fundamentals(jq, code):
    """获取基本面数据"""
    if jq is None:
        return None
    try:
        # 标准化代码
        market, pure = parse_code(code)
        if '.' not in code:
            if pure == 'HK':
                jq_code = f'{pure}{code}'  # 港股格式
            elif pure in ('SZ', 'XSHE'):
                jq_code = f'{code}.XSHE'
            elif pure in ('SH', 'XSHG'):
                jq_code = f'{code}.XSHG'
            else:
                jq_code = code
        else:
            jq_code = code
        
        val = jq.get_valuation(jq_code)
        if val is not None and len(val) > 0:
            row = val.iloc[-1]
            return {
                'market_cap': row.get('market_cap'),
                'pe_ratio': row.get('pe_ratio'),
                'pb_ratio': row.get('pb_ratio'),
                'roe': row.get('roe'),
                'date': str(val.index[-1].date()) if hasattr(val.index[-1], 'date') else str(val.index[-1]),
            }
    except:
        pass
    return None

def format_change_pct(pct):
    """格式化涨跌幅"""
    if pct is None:
        return "N/A"
    symbol = "🔴" if pct < 0 else "🟢" if pct > 0 else "⚪"
    return f"{symbol}{pct:+.2f}%"

def generate_report(codes, title=None, output_path='report.md'):
    """生成分析报告"""
    ak = check_akshare()
    jq = check_jqdata()
    
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    print(f"\n📊 正在生成股票分析报告...")
    print(f"股票数量: {len(codes)}")
    print()
    
    # 获取行情数据
    prices = {}
    for code in codes:
        market, pure = parse_code(code)
        print(f"获取 {code} 行情...")
        if market == 'HK':
            prices[code] = get_hk_stock_price(ak, pure)
        else:
            prices[code] = get_a_stock_price(ak, pure)
        time.sleep(0.3)
    
    # 获取基本面数据
    fundamentals = {}
    if jq:
        print("\n获取基本面数据（需聚宽配置）...")
        for code in codes:
            print(f"获取 {code} 基本面...")
            fundamentals[code] = get_fundamentals(jq, code)
            time.sleep(0.3)
    else:
        print("\n⚠️ 未配置聚宽，跳过基本面数据（运行 jq_login.py 可启用）")
    
    # 构建 Markdown 报告
    lines = []
    
    # 标题
    if title:
        lines.append(f"# {title}\n")
    else:
        stock_names = [prices.get(c, {}).get('name', c) for c in codes]
        lines.append(f"# 股票分析报告 | {', '.join(stock_names)}\n")
    
    lines.append(f"**生成时间**: {now}\n")
    lines.append(f"**数据来源**: AkShare（实时行情）" + 
                 ("、聚宽 JQData（基本面）" if jq else "（基本面数据未配置）") + "\n")
    lines.append("---\n")
    
    # 行情速览
    lines.append("## 📊 行情速览\n")
    lines.append("| 代码 | 名称 | 最新价 | 涨跌幅 | 成交额 |")
    lines.append("|------|------|--------|--------|--------|")
    
    for code in codes:
        p = prices.get(code, {})
        if p and 'error' not in p:
            amt = p.get('amount', 0)
            amt_str = f"{amt/1e8:.2f}亿" if amt > 0 else "N/A"
            lines.append(f"| {code} | {p.get('name', 'N/A')} | {p.get('price', 'N/A')} | "
                        f"{format_change_pct(p.get('change_pct'))} | {amt_str} |")
        else:
            lines.append(f"| {code} | ❌ 获取失败 | - | - | - |")
    
    lines.append("\n")
    
    # 基本面数据
    if fundamentals and any(fundamentals.values()):
        lines.append("## 📈 基本面数据\n")
        lines.append("| 代码 | 总市值(亿) | PE | PB | ROE | 数据日期 |")
        lines.append("|------|-----------|----|----|-----|----------|")
        
        for code in codes:
            f = fundamentals.get(code)
            if f:
                mc = f"{f['market_cap']:.2f}" if f.get('market_cap') else "N/A"
                pe = f"{f['pe_ratio']:.2f}" if f.get('pe_ratio') else "N/A"
                pb = f"{f['pb_ratio']:.2f}" if f.get('pb_ratio') else "N/A"
                roe = f"{f['roe']:.2f}%" if f.get('roe') else "N/A"
                lines.append(f"| {code} | {mc} | {pe} | {pb} | {roe} | {f.get('date', 'N/A')} |")
            else:
                lines.append(f"| {code} | N/A | N/A | N/A | N/A | - |")
        lines.append("\n")
    
    # 操作建议（基于涨跌幅的简单建议）
    lines.append("## 💡 操作建议\n")
    for code in codes:
        p = prices.get(code, {})
        if p and 'error' not in p:
            pct = p.get('change_pct', 0)
            name = p.get('name', code)
            
            if pct < -3:
                rating = "**关注**"
                note = "跌幅较大，谨慎观望"
            elif pct < 0:
                rating = "**持有**"
                note = "小幅回调，趋势未破"
            elif pct < 3:
                rating = "**持有**"
                note = "稳步上涨，趋势良好"
            else:
                rating = "**谨慎**"
                note = "涨幅过大，注意风险"
            
            lines.append(f"- **{name}**({code}): {rating} — {note}\n")
    
    lines.append("---\n")
    lines.append(f"*本报告由 Stock Analyzer 自动生成 | {now}*\n")
    
    # 写入文件
    content = '\n'.join(lines)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n✅ 报告已生成: {output_path}")
    return output_path

def main():
    parser = argparse.ArgumentParser(description='生成股票分析报告')
    parser.add_argument('--codes', type=str, required=True, 
                       help='股票代码，逗号分隔，如 03690.HK,300413.SZ')
    parser.add_argument('--output', type=str, default='report.md',
                       help='输出文件路径（默认: report.md）')
    parser.add_argument('--title', type=str,
                       help='报告标题（可选）')
    args = parser.parse_args()
    
    codes = [c.strip() for c in args.codes.split(',')]
    generate_report(codes, title=args.title, output_path=args.output)

if __name__ == '__main__':
    main()
