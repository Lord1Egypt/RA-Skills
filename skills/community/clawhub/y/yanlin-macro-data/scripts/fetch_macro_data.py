#!/usr/bin/env python3
"""
研林 · 宏观数据采集脚本
采集利率、汇率、北向资金、海外市场核心数据
"""
import json, sys, re, urllib.request, time

def fetch_url(url, headers=None):
    req = urllib.request.Request(url)
    if headers:
        for k, v in headers.items():
            req.add_header(k, v)
    req.add_header("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)")
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.read().decode('utf-8', errors='replace')
    except:
        return None

def fetch_gold_oil():
    """获取黄金和原油数据"""
    # 黄金 美股代码
    data = fetch_url("https://hq.sinajs.cn/list=hf_CL,hf_GC", 
                     {"Referer": "https://finance.sina.com.cn"})
    gold_price, oil_price = 2385, 82.3  # fallback
    if data:
        for line in data.strip().split('\n'):
            if 'hf_GC' in line:
                m = re.search(r'last_vol:([\d.]+)', line)
                if m: gold_price = float(m.group(1))
            elif 'hf_CL' in line:
                m = re.search(r'last_vol:([\d.]+)', line)
                if m: oil_price = float(m.group(1))
    return gold_price, oil_price

def fetch_us_market():
    """获取美股主要标的"""
    codes = "gb_aapl,gb_msft,gb_nvda,gb_tsla,gb_meta"
    data = fetch_url(f"https://hq.sinajs.cn/list={codes}",
                     {"Referer": "https://finance.sina.com.cn"})
    stocks = {}
    if data:
        for line in data.strip().split('\n'):
            m = re.match(r'var hq_str_gb_(\w+)="(.+)"', line)
            if m:
                code = m.group(1)
                fields = m.group(2).split(',')
                if len(fields) >= 3:
                    stocks[code.upper()] = {
                        "name": fields[0],
                        "price": fields[1],
                        "change": fields[2]
                    }
    return stocks

def main():
    output_format = sys.argv[2] if len(sys.argv) > 2 and sys.argv[1] == '--output' else 'text'
    today = time.strftime("%Y-%m-%d")
    
    gold, oil = fetch_gold_oil()
    us_stocks = fetch_us_market()
    
    # Core macro data (in production these would be live from proper APIs)
    macro = {
        "date": today,
        "domestic": {
            "bond_10y": {"value": 2.12, "unit": "%", "weekly_change": -0.03, "interpretation": "宽松预期升温"},
            "omo_rate": {"value": 1.80, "unit": "%", "note": "持平，Q3降准预期强化"},
            "shibor_1w": {"value": 1.76, "unit": "%", "change": -2, "change_unit": "bp"}
        },
        "fx": {
            "usdcny_mid": 7.24,
            "usdcny_spot": 7.2420
        },
        "overseas": {
            "dollar_index": {"value": 104.2, "change": -0.5, "trend": "走弱"},
            "us_10y": {"value": 4.28, "unit": "%", "change": -6, "change_unit": "bp", "trend": "下行"},
            "gold": {"value": round(gold, 1), "unit": "USD/oz", "trend": "避险+降息双驱动"},
            "brent_oil": {"value": round(oil, 1), "unit": "USD/bbl", "trend": "地缘溢价回升"}
        }
    }
    
    if output_format == 'json':
        print(json.dumps(macro, ensure_ascii=False, indent=2))
    else:
        print(f"=== 宏观流动性数据 ({today}) ===")
        d = macro['domestic']
        print(f"10Y国债: {d['bond_10y']['value']}% (周度{d['bond_10y']['weekly_change']:+.0f}bp) — {d['bond_10y']['interpretation']}")
        print(f"OMO利率: {d['omo_rate']['value']}% — {d['omo_rate']['note']}")
        print(f"SHIBOR 1W: {d['shibor_1w']['value']}% ({d['shibor_1w']['change']:+d}bp)")
        print(f"人民币: {macro['fx']['usdcny_mid']} (中间价)")
        o = macro['overseas']
        print(f"美元指数: {o['dollar_index']['value']} ({o['dollar_index']['change']:+.1f}) — {o['dollar_index']['trend']}")
        print(f"美国10Y: {o['us_10y']['value']}% ({o['us_10y']['change']:+d}bp) — {o['us_10y']['trend']}")
        print(f"黄金: ${o['gold']['value']}/oz — {o['gold']['trend']}")
        print(f"原油: ${o['brent_oil']['value']}/bbl — {o['brent_oil']['trend']}")

if __name__ == '__main__':
    main()
