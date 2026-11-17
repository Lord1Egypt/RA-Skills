#!/usr/bin/env python3
"""
研木 — 可比公司估值建模脚本
PE/PB/ROE/利润率雷达图对比 + 行业排名分析
"""
import json, sys, os, argparse
import urllib.request
from typing import Dict, List, Tuple
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['PingFang SC', 'Heiti SC', 'STHeiti', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


def _fetch_live_price(ticker: str, market: str):
    """从新浪财经获取实时股价，支持A股/港股/美股"""
    ticker_code = ticker.replace(".SH","").replace(".SZ","").replace(".HK","").replace(".US","")
    
    if market == "a-share":
        # A股: sh600519 / sz000858
        if ticker_code.startswith(("600","601","603","605","688")):
            prefix = "sh"
        elif ticker_code.startswith(("000","001","002","003","300","301")):
            prefix = "sz"
        else:
            return None
        url = f"https://hq.sinajs.cn/list={prefix}{ticker_code}"
    elif market == "hk":
        # 港股: rt_hk00700
        url = f"https://hq.sinajs.cn/list=rt_hk{ticker_code}"
    elif market == "us":
        # 美股: gb_nvda
        url = f"https://hq.sinajs.cn/list=gb_{ticker_code.lower()}"
    else:
        return None
    
    req = urllib.request.Request(url, headers={
        "Referer": "https://finance.sina.com.cn",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
    })
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            text = resp.read().decode("gbk")
        if "=" in text and '"' in text:
            data = text.split('"')[1].split(",")
            if market == "hk" and len(data) >= 7:
                # 港股格式: [0]=英文名 [1]=中文名 [2]=开盘 [3]=昨收 [4]=最高 [5]=最低 [6]=当前价
                p = float(data[6])
                if p > 0: return p
            elif market == "us" and len(data) >= 2:
                # 美股格式: [0]=中文名 [1]=当前价
                p = float(data[1])
                if p > 0: return p
            elif market == "a-share" and len(data) >= 4:
                # A股格式: [0]=名称 [1]=开盘 [2]=昨收 [3]=当前价
                p = float(data[3])
                if p > 0: return p
    except Exception:
        pass
    return None


FINANCIAL_DB = {
    "300750.SZ": {"name":"宁德时代","market":"a-share","shares_outstanding":46.27,"current_price":384.78,"market_cap":17803.77,"pe_ttm":22.4,"pb":5.41,"ps_est":4.2,"ev_ebitda":30.0,"roe":24.91,"gross_margin":26.27,"net_margin":17.05,"revenue_growth":17.04,"debt_ratio":61.94},
    "002594.SZ": {"name":"比亚迪","market":"a-share","market_cap":7907,"pe_ttm":28.7,"pb":3.41,"ps_est":0.98,"ev_ebitda":20.0,"roe":11.5,"gross_margin":20.2,"net_margin":5.3,"revenue_growth":26.0,"debt_ratio":62.3},
    "300014.SZ": {"name":"亿纬锂能","market":"a-share","market_cap":1265,"pe_ttm":29.7,"pb":3.08,"ps_est":2.06,"ev_ebitda":18.0,"roe":12.5,"gross_margin":18.5,"net_margin":8.2,"revenue_growth":22.0,"debt_ratio":58.0},
    "002074.SZ": {"name":"国轩高科","market":"a-share","market_cap":489,"pe_ttm":21.1,"pb":1.68,"ps_est":1.09,"ev_ebitda":12.0,"roe":8.5,"gross_margin":16.8,"net_margin":5.2,"revenue_growth":15.0,"debt_ratio":55.0},
    "002460.SZ": {"name":"赣锋锂业","market":"a-share","market_cap":1284,"pe_ttm":35.3,"pb":2.89,"ps_est":5.57,"ev_ebitda":22.0,"roe":8.0,"gross_margin":15.0,"net_margin":18.0,"revenue_growth":12.0,"debt_ratio":45.0},
    "600516.SH": {"name":"华友钴业","market":"a-share","market_cap":800,"pe_ttm":20.0,"pb":2.5,"ps_est":3.0,"ev_ebitda":15.0,"roe":12.0,"gross_margin":18.0,"net_margin":10.0,"revenue_growth":15.0,"debt_ratio":40.0},
    "600519.SH": {"name":"贵州茅台","market":"a-share","shares_outstanding":12.56,"current_price":1500.00,"market_cap":18840,"pe_ttm":21.5,"pb":7.8,"ps_est":10.5,"ev_ebitda":18.0,"roe":35.0,"gross_margin":91.8,"net_margin":50.0,"revenue_growth":7.5,"debt_ratio":20.0},
    "000858.SZ": {"name":"五粮液","market":"a-share","shares_outstanding":38.82,"current_price":150.00,"market_cap":5823,"pe_ttm":18.5,"pb":4.2,"ps_est":6.5,"ev_ebitda":15.0,"roe":24.0,"gross_margin":75.8,"net_margin":35.0,"revenue_growth":8.0,"debt_ratio":18.0},
    "000568.SZ": {"name":"泸州老窖","market":"a-share","shares_outstanding":14.72,"current_price":200.00,"market_cap":2944,"pe_ttm":19.0,"pb":5.5,"ps_est":8.0,"ev_ebitda":16.0,"roe":30.0,"gross_margin":85.0,"net_margin":42.0,"revenue_growth":12.0,"debt_ratio":22.0},
    "600809.SH": {"name":"山西汾酒","market":"a-share","shares_outstanding":12.20,"current_price":240.00,"market_cap":2928,"pe_ttm":24.0,"pb":6.0,"ps_est":7.0,"ev_ebitda":20.0,"roe":26.0,"gross_margin":75.0,"net_margin":30.0,"revenue_growth":15.0,"debt_ratio":25.0},
    "002304.SZ": {"name":"洋河股份","market":"a-share","shares_outstanding":15.06,"current_price":130.00,"market_cap":1958,"pe_ttm":15.0,"pb":2.8,"ps_est":4.5,"ev_ebitda":12.0,"roe":20.0,"gross_margin":70.0,"net_margin":32.0,"revenue_growth":5.0,"debt_ratio":20.0},
    "000596.SZ": {"name":"古井贡酒","market":"a-share","shares_outstanding":5.29,"current_price":280.00,"market_cap":1481,"pe_ttm":25.0,"pb":4.5,"ps_est":6.0,"ev_ebitda":22.0,"roe":18.0,"gross_margin":75.0,"net_margin":25.0,"revenue_growth":18.0,"debt_ratio":25.0},
    "00700.HK": {"name":"腾讯控股","market":"hk","shares_outstanding":92.5,"current_price":420.00,"market_cap":38850,"pe_ttm":22.9,"pb":5.8,"ps_est":5.2,"ev_ebitda":18.5,"roe":25.0,"gross_margin":50.2,"net_margin":26.4,"revenue_growth":10.5,"debt_ratio":40.0},
    "09988.HK": {"name":"阿里巴巴","market":"hk","shares_outstanding":200.0,"current_price":100.00,"market_cap":20000,"pe_ttm":15.0,"pb":2.0,"ps_est":2.5,"ev_ebitda":10.0,"roe":15.0,"gross_margin":38.0,"net_margin":15.0,"revenue_growth":8.0,"debt_ratio":25.0},
    "03690.HK": {"name":"美团","market":"hk","shares_outstanding":62.0,"current_price":150.00,"market_cap":9300,"pe_ttm":25.0,"pb":4.5,"ps_est":3.0,"ev_ebitda":20.0,"roe":18.0,"gross_margin":35.0,"net_margin":10.0,"revenue_growth":18.0,"debt_ratio":30.0},
    "09618.HK": {"name":"京东","market":"hk","shares_outstanding":31.0,"current_price":150.00,"market_cap":4650,"pe_ttm":12.0,"pb":1.8,"ps_est":0.5,"ev_ebitda":8.0,"roe":15.0,"gross_margin":15.0,"net_margin":3.5,"revenue_growth":8.0,"debt_ratio":60.0},
    "01024.HK": {"name":"快手","market":"hk","shares_outstanding":43.0,"current_price":60.00,"market_cap":2580,"pe_ttm":30.0,"pb":4.0,"ps_est":3.5,"ev_ebitda":22.0,"roe":12.0,"gross_margin":45.0,"net_margin":8.0,"revenue_growth":15.0,"debt_ratio":35.0},
    "PDD": {"name":"拼多多","market":"us","shares_outstanding":14.0,"current_price":120.00,"market_cap":1680,"pe_ttm":18.0,"pb":5.0,"ps_est":4.0,"ev_ebitda":15.0,"roe":28.0,"gross_margin":62.0,"net_margin":25.0,"revenue_growth":25.0,"debt_ratio":20.0},
    "NVDA": {"name":"NVIDIA","market":"us","shares_outstanding":25.0,"current_price":950.00,"market_cap":23750,"pe_ttm":32.5,"pb":25.0,"ps_est":15.8,"ev_ebitda":28.0,"roe":60.0,"gross_margin":73.0,"net_margin":56.7,"revenue_growth":15.0,"debt_ratio":25.0},
    "AMD": {"name":"AMD","market":"us","shares_outstanding":16.2,"current_price":120.00,"market_cap":1944,"pe_ttm":35.0,"pb":4.0,"ps_est":8.0,"ev_ebitda":30.0,"roe":12.0,"gross_margin":50.0,"net_margin":12.0,"revenue_growth":20.0,"debt_ratio":20.0},
    "INTC": {"name":"Intel","market":"us","shares_outstanding":42.0,"current_price":30.00,"market_cap":1260,"pe_ttm":25.0,"pb":1.2,"ps_est":2.0,"ev_ebitda":10.0,"roe":5.0,"gross_margin":40.0,"net_margin":8.0,"revenue_growth":5.0,"debt_ratio":30.0},
    "TSM": {"name":"台积电","market":"us","shares_outstanding":260.0,"current_price":180.00,"market_cap":46800,"pe_ttm":28.0,"pb":7.0,"ps_est":10.0,"ev_ebitda":22.0,"roe":28.0,"gross_margin":55.0,"net_margin":38.0,"revenue_growth":18.0,"debt_ratio":20.0},
    "AVGO": {"name":"博通","market":"us","shares_outstanding":5.0,"current_price":1800.00,"market_cap":9000,"pe_ttm":35.0,"pb":15.0,"ps_est":12.0,"ev_ebitda":30.0,"roe":40.0,"gross_margin":68.0,"net_margin":35.0,"revenue_growth":22.0,"debt_ratio":30.0},
    "QCOM": {"name":"高通","market":"us","shares_outstanding":11.0,"current_price":170.00,"market_cap":1870,"pe_ttm":22.0,"pb":6.0,"ps_est":4.5,"ev_ebitda":18.0,"roe":25.0,"gross_margin":55.0,"net_margin":22.0,"revenue_growth":12.0,"debt_ratio":35.0},
    "300308.SZ": {"name":"中际旭创","market":"a-share","market_cap":1273,"pe_ttm":44.9,"pb":8.5,"ps_est":7.5,"ev_ebitda":35.0,"roe":22.0,"gross_margin":35.0,"net_margin":20.0,"revenue_growth":30.0,"debt_ratio":25.0},
    "300502.SZ": {"name":"新易盛","market":"a-share","market_cap":680,"pe_ttm":38.5,"pb":7.2,"ps_est":6.8,"ev_ebitda":30.0,"roe":18.0,"gross_margin":32.0,"net_margin":18.0,"revenue_growth":28.0,"debt_ratio":20.0},
    "300394.SZ": {"name":"天孚通信","market":"a-share","market_cap":420,"pe_ttm":42.0,"pb":6.5,"ps_est":8.0,"ev_ebitda":32.0,"roe":15.0,"gross_margin":38.0,"net_margin":22.0,"revenue_growth":25.0,"debt_ratio":15.0},
    "002281.SZ": {"name":"光迅科技","market":"a-share","market_cap":350,"pe_ttm":55.0,"pb":4.8,"ps_est":3.5,"ev_ebitda":25.0,"roe":8.0,"gross_margin":22.0,"net_margin":6.0,"revenue_growth":15.0,"debt_ratio":30.0},
    "603083.SH": {"name":"剑桥科技","market":"a-share","market_cap":120,"pe_ttm":45.0,"pb":5.0,"ps_est":3.0,"ev_ebitda":28.0,"roe":10.0,"gross_margin":28.0,"net_margin":8.0,"revenue_growth":20.0,"debt_ratio":30.0},
    "301205.SZ": {"name":"联特科技","market":"a-share","market_cap":90,"pe_ttm":50.0,"pb":4.0,"ps_est":2.5,"ev_ebitda":30.0,"roe":8.0,"gross_margin":25.0,"net_margin":6.0,"revenue_growth":25.0,"debt_ratio":25.0},
}

def radar_chart(companies, labels, output_path):
    """生成多维度雷达图"""
    from math import pi
    metrics = ['PE(TTM)','PB','ROE(%)','毛利率(%)','净利率(%)']
    n = len(metrics)
    
    def normalize(vals, lower=True):
        a = np.array(vals, dtype=float)
        if lower: a = 1/a
        mn, mx = np.min(a), np.max(a)
        return ((a-mn)/(mx-mn) if mx>mn else np.ones_like(a)*0.5)*100
    
    pe = [c.get('pe_ttm',20) for c in companies]
    pb = [c.get('pb',2) for c in companies]
    roe = [c.get('roe',10) for c in companies]
    gm = [c.get('gross_margin',20) for c in companies]
    nm = [c.get('net_margin',10) for c in companies]
    
    dm = np.array([normalize(pe),normalize(pb),normalize(roe,False),normalize(gm,False),normalize(nm,False)])
    
    angles = [n*2*pi/5 for n in range(5)]; angles += angles[:1]
    fig, ax = plt.subplots(figsize=(10,10), subplot_kw=dict(polar=True))
    colors = plt.cm.Set1(np.linspace(0,1,len(companies)))
    for i, c in enumerate(companies):
        v = dm[:,i].tolist(); v += v[:1]
        ax.plot(angles, v, 'o-', linewidth=2, label=companies[i]['name'], color=colors[i])
        ax.fill(angles, v, alpha=0.1, color=colors[i])
    ax.set_xticks(angles[:-1]); ax.set_xticklabels(metrics, fontsize=12)
    ax.set_ylim(0,100); ax.set_title('可比公司多维度对比雷达图', fontsize=14, fontweight='bold', pad=20)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3,1.1))
    plt.tight_layout(); plt.savefig(output_path, dpi=200, bbox_inches='tight'); plt.close()

def bar_chart(companies, output_path):
    names = [c['name'] for c in companies]
    pe_vals = [c.get('pe_ttm',0) for c in companies]
    pb_vals = [c.get('pb',0) for c in companies]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    x = np.arange(len(names)); w = 0.5
    for ax, vals, ylabel, title in [(ax1,pe_vals,'PE (TTM)','市盈率对比'),(ax2,pb_vals,'PB','市净率对比')]:
        bars = ax.bar(x, vals, w, color=plt.cm.RdYlGn(np.array(vals)/max(vals)))
        ax.set_xticks(x); ax.set_xticklabels(names, rotation=45, ha='right', fontsize=10)
        ax.set_ylabel(ylabel, fontsize=12); ax.set_title(title, fontsize=13, fontweight='bold')
        for bar, val in zip(bars, vals):
            ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.5, f'{val:.1f}x', ha='center', va='bottom', fontsize=9)
    plt.tight_layout(); plt.savefig(output_path, dpi=200, bbox_inches='tight'); plt.close()

def format_report(target, comps, output_dir='.'):
    target_name, target_ticker = target['name'], target.get('ticker','')
    all_c = [target] + list(comps.values())
    
    lines = [
        f'━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━',
        f'  📊 可比公司估值 · {target_name} ({target_ticker})',
        f'━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n',
        f'━━━ 可比公司选取 ━━━',
    ]
    for c in all_c:
        prefix = '  ★ ' if c.get('ticker')==target_ticker else '    '
        lines.append(f"{prefix}{c['name']} ({c.get('ticker','')}) — 市值 ¥{c.get('market_cap',0):.0f}亿")
    
    lines.append(f'\n━━━ 估值倍数对比 ━━━')
    lines.append(f'  {"公司":<12} {"市值(亿)":<10} {"PE(TTM)":<10} {"PB":<8} {"PS":<8} {"ROE(%)":<8} {"毛利率":<8} {"净利率":<8}')
    lines.append(f'  {"─"*72}')
    
    for c in all_c:
        mk = '★ ' if c.get('ticker')==target_ticker else '  '
        lines.append(f'  {mk}{c["name"]:<10} ¥{c.get("market_cap",0):<8.0f} {c.get("pe_ttm","N/A"):<8} {c.get("pb","N/A"):<6.1f} {c.get("ps_est","N/A"):<6.1f} {c.get("roe","N/A"):<6.1f} {c.get("gross_margin","N/A"):<6.1f} {c.get("net_margin","N/A"):<6.1f}')
    
    pe_vals = [c.get('pe_ttm',0) for c in all_c if c.get('pe_ttm',0)>0]
    avg_pe = sum(pe_vals)/len(pe_vals) if pe_vals else 0
    roe_vals = [c.get('roe',0) for c in all_c if c.get('roe',0)>0]
    avg_roe = sum(roe_vals)/len(roe_vals) if roe_vals else 0
    tp = target.get('pe_ttm',0); tr = target.get('roe',0)
    
    lines.extend([
        f'\n━━━ 估值解读 ━━━\n',
        f'  PE视角:\n    {target_name} PE(TTM) = {tp:.1f}x vs 可比公司均值 = {avg_pe:.1f}x',
        f'    {"✅ PE低于同行均值，相对估值偏低" if tp < avg_pe else "📈 PE高于同行均值"}',
        f'\n  PB-ROE视角:\n    {target_name} ROE = {tr:.1f}% vs 同行均值 {avg_roe:.1f}%',
        f'    {"✅ ROE显著领先同行，PB溢价合理" if tr > avg_roe else "⚠️ ROE需关注"}',
        f'\n  盈利能力:\n    毛利率: {target.get("gross_margin",0):.1f}% | 净利率: {target.get("net_margin",0):.1f}%',
        f'\n━━━ 综合判断 ━━━',
        f'  {"📗 估值洼地 — PE低于同行，ROE高于同行" if tp < avg_pe and tr > avg_roe else "📘 优质溢价"}',
    ])
    
    try:
        rp = os.path.join(output_dir, f"{target_ticker.replace('.','_')}_comps_radar.png")
        radar_chart(all_c, [c['name'] for c in all_c], rp)
        lines.append(f'  📊 雷达图: {rp}')
        bp = os.path.join(output_dir, f"{target_ticker.replace('.','_')}_comps_bar.png")
        bar_chart(all_c, bp)
        lines.append(f'  📊 倍数对比图: {bp}')
    except Exception as e:
        lines.append(f'  ⚠️ 图表生成失败: {e}')
    
    lines.append(f'\n**免责声明**: 本报告仅供参考,不构成个人投资建议。')
    return '\n'.join(lines)

def main():
    parser = argparse.ArgumentParser(description='可比公司估值')
    parser.add_argument('--ticker','-t',required=True)
    parser.add_argument('--comps',required=True)
    parser.add_argument('--market','-m',default='a-share')
    parser.add_argument('--output-dir','-o',default='.')
    parser.add_argument('--format',choices=['text','json'],default='text')
    args = parser.parse_args()
    
    if args.ticker not in FINANCIAL_DB:
        print(f'❌ 股票 {args.ticker} 数据未收录'); sys.exit(1)
    
    target = FINANCIAL_DB[args.ticker].copy()
    
    # 实时股价覆盖
    live_price = _fetch_live_price(args.ticker, target.get("market", "a-share"))
    if live_price:
        old_p = target.get("current_price", 0)
        target["current_price"] = live_price
        shares = target.get("shares_outstanding", 0)
        if shares > 0:
            target["market_cap"] = round(live_price * shares, 2)
        print(f"✅ Comps: 实时股价 ¥{old_p} → ¥{live_price}", file=sys.stderr)

    target['ticker'] = args.ticker
    comps = {}
    for code in args.comps.split(','):
        code = code.strip()
        if code in FINANCIAL_DB:
            comps[code] = FINANCIAL_DB[code]
    
    os.makedirs(args.output_dir, exist_ok=True)
    
    if args.format == 'json':
        output = {'target': target, 'comps': comps}
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        print(format_report(target, comps, args.output_dir))

if __name__ == '__main__':
    main()
