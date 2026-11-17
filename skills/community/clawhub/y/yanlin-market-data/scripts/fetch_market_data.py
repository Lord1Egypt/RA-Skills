#!/usr/bin/env python3
"""
研林 · 市场数据采集脚本
采集A股大盘指数、行业板块排名、核心权重股行情
"""
import json, sys, re, urllib.request, urllib.error, time

def fetch_url(url, headers=None):
    """通用URL获取"""
    req = urllib.request.Request(url)
    if headers:
        for k, v in headers.items():
            req.add_header(k, v)
    req.add_header("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)")
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.read().decode('utf-8', errors='replace')
    except Exception as e:
        return None

def fetch_index_quotes():
    """获取指数行情"""
    codes = "sh000001,sz399001,sz399006,sh000688,sh000300,sh000016,sh000905,sh000852"
    url = f"https://hq.sinajs.cn/list={codes}"
    data = fetch_url(url, {"Referer": "https://finance.sina.com.cn"})
    if not data:
        return {}
    
    indices = {}
    name_map = {
        "sh000001": "上证指数", "sz399001": "深证成指", "sz399006": "创业板指",
        "sh000688": "科创50", "sh000300": "沪深300", "sh000016": "上证50",
        "sh000905": "中证500", "sh000852": "中证1000"
    }
    
    for line in data.strip().split('\n'):
        m = re.match(r'var hq_str_(\w+)="(.+)"', line)
        if m:
            code = m.group(1)
            fields = m.group(2).split(',')
            if len(fields) >= 4:
                name = fields[0] if fields[0] else name_map.get(code, code)
                try:
                    open_p = float(fields[1]) if fields[1] else 0
                    prev_close = float(fields[2]) if fields[2] else 0
                    current = float(fields[3]) if fields[3] else 0
                    high = float(fields[4]) if fields[4] else 0
                    low = float(fields[5]) if fields[5] else 0
                    change_pct = round((current - prev_close) / prev_close * 100, 2) if prev_close else 0
                    indices[code] = {
                        "name": name, "close": current, "open": open_p,
                        "high": high, "low": low, "prev_close": prev_close,
                        "change_pct": change_pct
                    }
                except:
                    pass
    return indices

def fetch_sector_rankings():
    """获取行业板块排名（同花顺）"""
    url = "http://q.10jqka.com.cn/thshy/"
    data = fetch_url(url)
    if not data:
        return {"top": [], "bottom": []}
    
    # 尝试不同编码
    for enc in ['gbk', 'gb2312', 'utf-8']:
        try:
            html = data.encode('latin1').decode(enc)
            break
        except:
            html = data
    
    sectors_top, sectors_bottom = [], []
    tables = re.findall(r'<table.*?</table>', html, re.DOTALL)
    
    for table in tables:
        rows = re.findall(r'<tr.*?</tr>', table, re.DOTALL)
        for row in rows:
            cells = re.findall(r'<td.*?>(.*?)</td>', row, re.DOTALL)
            if len(cells) >= 3:
                name = re.sub(r'<[^>]+>', '', cells[1]).strip()
                pct_str = re.sub(r'<[^>]+>', '', cells[2]).strip().replace('%', '')
                try:
                    pct = float(pct_str)
                except:
                    continue
                entry = {"name": name, "change_pct": pct}
                if len(sectors_top) < 15:
                    sectors_top.append(entry)
                else:
                    sectors_bottom.append(entry)
    
    return {"top": sectors_top, "bottom": sectors_bottom[-10:] if sectors_bottom else []}

def fetch_core_stocks():
    """获取核心权重股行情"""
    codes = "sh600519,sh600036,sh600030,sh601318,sh600900,sh601012,sh600585,sh600276,sh600887,sh600690,sh601899,sh600703,sh600171,sh601127,sz300750,sz000858,sz002475,sz002415,sz000333,sz000651,sz002230,sz300059,sz002714,sz300124,sz002129,sh601857,sh688981,sh600010,sz002594,sz300001"
    url = f"https://hq.sinajs.cn/list={codes}"
    data = fetch_url(url, {"Referer": "https://finance.sina.com.cn"})
    if not data:
        return {}
    
    stocks = {}
    for line in data.strip().split('\n'):
        m = re.match(r'var hq_str_(\w+)="(.+)"', line)
        if m:
            code = m.group(1)
            fields = m.group(2).split(',')
            if len(fields) >= 4 and fields[0]:
                try:
                    name = fields[0]
                    current = float(fields[3]) if fields[3] else 0
                    prev_close = float(fields[2]) if fields[2] else 0
                    high = float(fields[4]) if fields[4] else 0
                    low = float(fields[5]) if fields[5] else 0
                    change_pct = round((current - prev_close) / prev_close * 100, 2) if prev_close else 0
                    turnover = fields[8] if len(fields) > 8 else ""
                    stocks[code] = {
                        "name": name, "close": current, "change_pct": change_pct,
                        "high": high, "low": low
                    }
                except:
                    pass
    return stocks

def main():
    output_format = sys.argv[2] if len(sys.argv) > 2 and sys.argv[1] == '--output' else 'text'
    
    indices = fetch_index_quotes()
    sectors = fetch_sector_rankings()
    stocks = fetch_core_stocks()
    
    result = {
        "date": time.strftime("%Y-%m-%d"),
        "indices": indices,
        "sectors": sectors,
        "stocks": stocks
    }
    
    if output_format == 'json':
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"=== 指数行情 ({result['date']}) ===")
        for code, idx in indices.items():
            arrow = "🔴" if idx['change_pct'] < 0 else "🟢"
            print(f"{idx['name']:8s} {idx['close']:>8.2f}  {arrow} {idx['change_pct']:>+6.2f}%")
        
        print(f"\n=== 行业涨幅TOP10 ===")
        for s in sectors.get('top', [])[:10]:
            print(f"  {s['name']:10s}  {s['change_pct']:>+6.2f}%")
        
        print(f"\n=== 核心个股 ===")
        for code, st in list(stocks.items())[:15]:
            arrow = "🔴" if st['change_pct'] < 0 else "🟢"
            print(f"  {st['name']:8s}  {st['close']:>8.2f}  {arrow} {st['change_pct']:>+6.2f}%")

if __name__ == '__main__':
    main()
