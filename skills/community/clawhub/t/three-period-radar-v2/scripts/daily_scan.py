#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日三周期雷达扫描
15:30收盘后自动运行，覆盖持仓+关注标的+板块ETF
"""

import sys
import os
import time
from datetime import datetime, timedelta

# 添加 radar.py 所在目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

import akshare as ak
import pandas as pd
from radar import three_period_radar

# ------------------------------------------------------------------ 扫描列表

HOLDINGS = [
    ("sz300731", "科创新源"),
    ("sz002975", "博杰股份"),
    ("sh605133", "嵘泰股份"),
    ("sz300580", "贝斯特"),
    ("sh603616", "韩建河山"),
    ("sz300363", "博腾股份"),
]

WATCHLIST = [
    ("sh601985", "中国核电"),
    ("sh600406", "国电南瑞"),
    ("sh600875", "东方电气"),
    ("sh603308", "应流股份"),
]

ETFS = [
    ("sh510300", "沪深300ETF"),
    ("sh510500", "中证500ETF"),
    ("sh588000", "科创50ETF"),
]

ALL_TICKERS = HOLDINGS + WATCHLIST + ETFS

# ------------------------------------------------------------------ 数据拉取

def fetch_stock(prefix, name):
    """拉取单票日线数据"""
    try:
        end = datetime.now().strftime('%Y%m%d')
        start = (datetime.now() - timedelta(days=400)).strftime('%Y%m%d')
        df = ak.stock_zh_a_daily(symbol=prefix, start_date=start, end_date=end)
        df = df.reset_index(drop=True)
        df_out = df[['date', 'open', 'high', 'low', 'close', 'volume']].copy()
        df_out.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
        df_out['Date'] = pd.to_datetime(df_out['Date'])
        df_out = df_out.sort_values('Date').reset_index(drop=True)
        return df_out
    except Exception as e:
        print(f"✗ {name}({prefix}): {e}", file=sys.stderr)
        return None


def fetch_etf(prefix, name):
    """拉取ETF日线数据"""
    try:
        code = prefix[2:]  # 去掉 sh/sz 前缀
        df = ak.fund_etf_hist_sina(symbol=prefix)
        df.columns = [c.lower() for c in df.columns]
        df['date'] = pd.to_datetime(df['date'])
        start = pd.to_datetime((datetime.now() - timedelta(days=400)).strftime('%Y%m%d'))
        df = df[df['date'] >= start].copy()
        df = df.sort_values('date').reset_index(drop=True)
        df_out = df[['date', 'open', 'high', 'low', 'close', 'volume']].copy()
        df_out.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
        return df_out
    except Exception as e:
        print(f"✗ {name}({prefix}): {e}", file=sys.stderr)
        return None

# ------------------------------------------------------------------ 报告生成

def generate_report(results):
    """生成飞书友好的 Markdown 报告"""
    lines = []
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    lines.append(f"# 📊 每日三周期雷达 ({now})")
    lines.append("")
    
    # 按分组排序
    holdings_results = [r for r in results if any(t[1] == r['name'] for t in HOLDINGS)]
    watch_results = [r for r in results if any(t[1] == r['name'] for t in WATCHLIST)]
    etf_results = [r for r in results if any(t[1] == r['name'] for t in ETFS)]
    
    # 持仓
    if holdings_results:
        lines.append("## 🎯 持仓扫描")
        lines.append("")
        lines.append(f"{'标的':<10}{'评分':>6}{'标签':<8}{'三周期状态':<28}{'近20日':>8}")
        lines.append("-" * 60)
        for r in sorted(holdings_results, key=lambda x: x['score'], reverse=True):
            s = r['state']
            chg = f"{r['change_20']:+.1f}%" if r['change_20'] is not None else '—'
            lines.append(f"{r['name']:<10}{r['score']:>6}{r['label']:<8}月{s['M']}/周{s['W']}/日{s['D']:<16}{chg:>8}")
        lines.append("")
    
    # 关注池
    if watch_results:
        lines.append("## 👁️ 关注池")
        lines.append("")
        lines.append(f"{'标的':<10}{'评分':>6}{'标签':<8}{'三周期状态':<28}{'近20日':>8}")
        lines.append("-" * 60)
        for r in sorted(watch_results, key=lambda x: x['score'], reverse=True):
            s = r['state']
            chg = f"{r['change_20']:+.1f}%" if r['change_20'] is not None else '—'
            lines.append(f"{r['name']:<10}{r['score']:>6}{r['label']:<8}月{s['M']}/周{s['W']}/日{s['D']:<16}{chg:>8}")
        lines.append("")
    
    # ETF
    if etf_results:
        lines.append("## 📈 板块ETF")
        lines.append("")
        lines.append(f"{'ETF':<12}{'评分':>6}{'标签':<8}{'三周期状态':<28}{'近20日':>8}")
        lines.append("-" * 60)
        for r in sorted(etf_results, key=lambda x: x['score'], reverse=True):
            s = r['state']
            chg = f"{r['change_20']:+.1f}%" if r['change_20'] is not None else '—'
            lines.append(f"{r['name']:<12}{r['score']:>6}{r['label']:<8}月{s['M']}/周{s['W']}/日{s['D']:<16}{chg:>8}")
        lines.append("")
    
    # 特别关注
    checklist_pass = [r for r in results if r['checklist_pass']]
    high_score = [r for r in results if r['score'] >= 35 and not r['checklist_pass']]
    
    lines.append("## ⚡ 特别关注")
    lines.append("")
    
    if checklist_pass:
        lines.append(f"✅ **checklist 通过 ({len(checklist_pass)}只):**")
        for r in checklist_pass:
            lines.append(f"  • {r['name']}: 评分{r['score']} | 月{r['state']['M']}/周{r['state']['W']}/日{r['state']['D']}")
        lines.append("")
    
    if high_score:
        lines.append(f"🟡 **高分观察 ({len(high_score)}只):**")
        for r in high_score:
            lines.append(f"  • {r['name']}: 评分{r['score']} | 月{r['state']['M']}/周{r['state']['W']}/日{r['state']['D']}")
        lines.append("")
    
    if not checklist_pass and not high_score:
        lines.append("⚠️ 本次扫描无 checklist 通过标的，无高分观察标的")
        lines.append("")
    
    # 大盘环境判断
    etf_300 = next((r for r in etf_results if '沪深300' in r['name']), None)
    if etf_300:
        s = etf_300['state']
        lines.append(f"**大盘环境**: 沪深300ETF 评分{etf_300['score']} | 月{s['M']}/周{s['W']}/日{s['D']}")
        if etf_300['score'] < 15:
            lines.append("🔴 大盘弱势，控制仓位")
        elif etf_300['score'] < 30:
            lines.append("🟡 大盘震荡，谨慎操作")
        else:
            lines.append("🟢 大盘偏强，可积极参与")
        lines.append("")
    
    lines.append("---")
    lines.append("*数据来源: akshare | 三周期雷达 v2.0*")
    
    return "\n".join(lines)

# ------------------------------------------------------------------ 主函数

def main():
    print(f"🚀 每日三周期雷达扫描启动 ({datetime.now().strftime('%Y-%m-%d %H:%M')})")
    print(f"扫描标的: {len(ALL_TICKERS)} 只")
    print("")
    
    results = []
    
    # 拉取股票数据
    for prefix, name in HOLDINGS + WATCHLIST:
        df = fetch_stock(prefix, name)
        if df is not None and len(df) >= 60:
            result = three_period_radar(df, name)
            results.append(result)
            print(f"✓ {name}: {len(df)}条, 评分{result['score']}")
        time.sleep(0.8)
    
    # 拉取ETF数据
    for prefix, name in ETFS:
        df = fetch_etf(prefix, name)
        if df is not None and len(df) >= 60:
            result = three_period_radar(df, name)
            results.append(result)
            print(f"✓ {name}: {len(df)}条, 评分{result['score']}")
        time.sleep(0.8)
    
    if not results:
        print("✗ 无数据可用", file=sys.stderr)
        return 1
    
    # 生成报告
    report = generate_report(results)
    
    # 保存报告
    report_path = '/tmp/daily_radar_report.md'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    # 同时保存JSON供程序解析
    import json
    json_path = '/tmp/daily_radar_report.json'
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump([{
            'name': r['name'],
            'score': r['score'],
            'checklist_pass': r['checklist_pass'],
            'label': r['label'],
            'state': r['state'],
            'close': float(r['close']),
            'change_20': float(r['change_20']) if r['change_20'] is not None else None,
            'signals': r['signals'],
            'data_end': r['data_end'],
        } for r in results], f, ensure_ascii=False, indent=2)
    
    print(f"\n📄 报告已保存: {report_path}")
    print(f"📄 JSON已保存: {json_path}")
    print(f"\n扫描完成: {len(results)} 只标的")
    
    # 打印摘要到stdout
    print("\n" + "=" * 60)
    print(report)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
