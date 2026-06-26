#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
实时财经数据查询 - 新浪财经API + Yahoo Finance
支持A股、港股、美股、外汇、期货、指数
"""

import urllib.request
import urllib.parse
import json
import re
import sys

try:
    import yfinance as yf
    YFINANCE_AVAILABLE = True
except ImportError:
    YFINANCE_AVAILABLE = False
    print("⚠️  yfinance 未安装，美股数据将不可用")
    print("安装命令: pip3 install yfinance")

# ============ Yahoo Finance 数据获取 ============

def fetch_yahoo_data(symbol):
    """从Yahoo Finance获取数据"""
    if not YFINANCE_AVAILABLE:
        return None
    
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="1d", interval="1m")
        
        if data.empty:
            return None
        
        latest = data.iloc[-1]
        prev_close = ticker.info.get('previousClose', 0)
        
        change = latest['Close'] - prev_close if prev_close else 0
        change_pct = (change / prev_close * 100) if prev_close else 0
        
        return {
            "name": ticker.info.get('shortName', symbol),
            "price": round(latest['Close'], 2),
            "change": round(change, 2),
            "change_pct": round(change_pct, 2),
            "high": round(latest['High'], 2),
            "low": round(latest['Low'], 2),
            "open": round(latest['Open'], 2),
            "volume": int(latest['Volume']),
        }
    except Exception as e:
        return None

# ============ 新浪财经数据获取 ============

# 股票代码映射表
STOCK_MAP = {
    # 指数
    "上证指数": "sh000001", "上证": "sh000001",
    "深证成指": "sz399001", "深证": "sz399001",
    "创业板指": "sz399006", "创业板": "sz399006",
    "沪深300": "sh000300", "科创50": "sh000688",
    
    # 热门A股
    "贵州茅台": "sh600519", "茅台": "sh600519",
    "宁德时代": "sz300750",
    "比亚迪": "sz002594",
    "招商银行": "sh600036",
    "中国平安": "sh601318",
    "五粮液": "sz000858",
    "中芯国际": "sh688981",
    "隆基绿能": "sh601012", "隆基": "sh601012",
    "东方财富": "sz300059",
    "中信证券": "sh600030",
    "长江电力": "sh600900",
    "紫金矿业": "sh601899",
    "迈瑞医疗": "sz300760",
    "恒瑞医药": "sh600276",
    "药明康德": "sh603259",
    "伊利股份": "sh600887",
    "工业富联": "sh601138",
    "中国建筑": "sh601668",
    "中国石化": "sh600028",
    "中国石油": "sh601857",
    "牧原股份": "sz002714",
    "通威股份": "sh600438",
    
    # 港股
    "腾讯": "hk00700", "腾讯控股": "hk00700",
    "阿里巴巴": "hk09988", "阿里": "hk09988",
    "美团": "hk03690",
    "京东": "hk09618",
    "小米": "hk01810", "小米集团": "hk01810",
    "网易": "hk09999",
    "百度": "hk09888",
    "快手": "hk01024",
    "哔哩哔哩": "hk09626", "B站": "hk09626",
    "理想汽车": "hk02015",
    "蔚来": "hk09866",
    "小鹏汽车": "hk09868", "小鹏": "hk09868",
    "中国移动": "hk00941",
    "药明生物": "hk02269",
    
    # 美股（Yahoo Finance symbols）
    "苹果": "yah_AAPL", "AAPL": "yah_AAPL",
    "微软": "yah_MSFT", "MSFT": "yah_MSFT",
    "谷歌": "yah_GOOGL", "GOOGL": "yah_GOOGL",
    "亚马逊": "yah_AMZN", "AMZN": "yah_AMZN",
    "特斯拉": "yah_TSLA", "TSLA": "yah_TSLA",
    "英伟达": "yah_NVDA", "NVDA": "yah_NVDA",
    "Meta": "yah_META", "META": "yah_META",
    "伯克希尔": "yah_BRK-B", "BRK": "yah_BRK-B",
    "台积电": "yah_TSM", "TSM": "yah_TSM",
    "摩根大通": "yah_JPM", "JPM": "yah_JPM",
    "VISA": "yah_V", "V": "yah_V",
    "强生": "yah_JNJ", "JNJ": "yah_JNJ",
    "沃尔玛": "yah_WMT", "WMT": "yah_WMT",
    "联合健康": "yah_UNH", "UNH": "yah_UNH",
    "万事达卡": "yah_MA", "MA": "yah_MA",
    "博通": "yah_AVGO", "AVGO": "yah_AVGO",
    "甲骨文": "yah_ORCL", "ORCL": "yah_ORCL",
    
    # 美股中概股
    "阿里巴巴美股": "yah_BABA", "BABA": "yah_BABA",
    "拼多多": "yah_PDD", "PDD": "yah_PDD",
    "京东美股": "yah_JD", "JD": "yah_JD",
    "网易美股": "yah_NTES", "NTES": "yah_NTES",
    "百度美股": "yah_BIDU", "BIDU": "yah_BIDU",
    "蔚来美股": "yah_NIO", "NIO": "yah_NIO",
    "理想汽车美股": "yah_LI", "LI": "yah_LI",
    "小鹏汽车美股": "yah_XPEV", "XPEV": "yah_XPEV",
    "贝壳": "yah_BEKE", "BEKE": "yah_BEKE",
    "哔哩哔哩美股": "yah_BILI", "BILI": "yah_BILI",
    
    # 期货/大宗商品 (Yahoo Finance)
    "黄金": "yah_GC=F", "GC": "yah_GC=F",
    "白银": "yah_SI=F", "SI": "yah_SI=F",
    "原油": "yah_CL=F", "WTI原油": "yah_CL=F", "CL": "yah_CL=F",
    "布伦特原油": "yah_BZ=F", "BZ": "yah_BZ=F",
    "铜": "yah_HG=F", "HG": "yah_HG=F",
    "天然气": "yah_NG=F", "NG": "yah_NG=F",
    
    # 指数 (Yahoo Finance)
    "VIX": "yah_^VIX", "恐慌指数": "yah_^VIX",
    "道琼斯": "yah_^DJI", "道指": "yah_^DJI",
    "标普500": "yah_^GSPC",
    "纳斯达克": "yah_^IXIC", "纳指": "yah_^IXIC",
    "纳斯达克100": "yah_^NDX",
    "罗素2000": "yah_^RUT",
    
    # 美债收益率 (Yahoo Finance)
    "美债收益率": "yah_^TNX", "美债10年": "yah_^TNX", "TNX": "yah_^TNX",
    "美债2年": "yah_^FVX", "FVX": "yah_^FVX",
    "美债30年": "yah_^TYX", "TYX": "yah_^TYX",
    
    # 外汇 (Yahoo Finance)
    "美元兑人民币": "yah_USDCNY=X", "USDCNY": "yah_USDCNY=X",
    "美元人民币": "yah_USDCNY=X",
    "美元指数": "yah_DX-Y.NYB", "DXY": "yah_DX-Y.NYB",
    "欧元美元": "yah_EURUSD=X", "EURUSD": "yah_EURUSD=X",
    "英镑美元": "yah_GBPUSD=X", "GBPUSD": "yah_GBPUSD=X",
    "美元日元": "yah_USDJPY=X", "USDJPY": "yah_USDJPY=X",
    "离岸人民币": "yah_USDCNH=X", "USDCNH": "yah_USDCNH=X",
}

def normalize_code(code_or_name):
    """将股票名称或代码转换为API格式"""
    # 先查映射表
    if code_or_name in STOCK_MAP:
        return STOCK_MAP[code_or_name]
    
    # 处理纯数字代码（A股）
    if code_or_name.isdigit():
        code = code_or_name
        if code.startswith('6'):
            return f"sh{code}"
        elif code.startswith('0') or code.startswith('3'):
            return f"sz{code}"
        elif code.startswith('68'):
            return f"sh{code}"
        elif len(code) == 5:  # 港股
            return f"hk{code}"
    
    # 处理已带前缀的代码
    if code_or_name.startswith(('sh', 'sz', 'hk')):
        return code_or_name
    
    # 处理美股代码（纯字母）
    if code_or_name.isalpha():
        # 检查是否是大写股票代码
        if code_or_name.isupper() and len(code_or_name) <= 5:
            return f"yah_{code_or_name}"
    
    return None

def safe_float(s):
    """安全转换为float"""
    if not s or s.strip() == '' or ':' in s:
        return 0.0
    try:
        return float(s)
    except ValueError:
        return 0.0

def safe_int(s):
    """安全转换为int"""
    if not s or s.strip() == '':
        return 0
    try:
        return int(float(s))
    except ValueError:
        return 0

def fetch_sina_data(codes):
    """从新浪财经获取数据"""
    if isinstance(codes, str):
        codes = [codes]
    
    url = f"http://hq.sinajs.cn/list={','.join(codes)}"
    
    try:
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Referer': 'https://finance.sina.com.cn'
            }
        )
        
        with urllib.request.urlopen(req, timeout=10) as response:
            data = response.read().decode('gb2312', errors='ignore')
            return parse_sina_response(data)
    except Exception as e:
        return {"error": str(e)}

def parse_sina_response(data):
    """解析新浪返回的数据"""
    results = {}
    pattern = r'var hq_str_(\w+)="([^"]*)";'
    matches = re.findall(pattern, data)
    
    for code, content in matches:
        if not content:
            continue
            
        parts = content.split(',')
        
        if code.startswith('sh') or code.startswith('sz'):
            # A股
            if len(parts) >= 10:
                prev_close = safe_float(parts[2])
                price = safe_float(parts[3])
                results[code] = {
                    "name": parts[0],
                    "open": safe_float(parts[1]),
                    "prev_close": prev_close,
                    "price": price,
                    "high": safe_float(parts[4]),
                    "low": safe_float(parts[5]),
                    "bid": safe_float(parts[6]),
                    "ask": safe_float(parts[7]),
                    "volume": safe_int(parts[8]) // 100,
                    "amount": round(safe_float(parts[9]) / 10000, 2),
                    "change": round(price - prev_close, 2) if prev_close else 0,
                    "change_pct": round((price - prev_close) / prev_close * 100, 2) if prev_close else 0
                }
        
        elif code.startswith('hk'):
            # 港股
            if len(parts) >= 7:
                results[code] = {
                    "name": parts[1] if len(parts) > 1 and parts[1] else parts[0],
                    "price": safe_float(parts[6]),
                    "change": safe_float(parts[7]) if len(parts) > 7 else 0,
                    "change_pct": safe_float(parts[8]) if len(parts) > 8 else 0,
                    "high": safe_float(parts[4]) if len(parts) > 4 else 0,
                    "low": safe_float(parts[5]) if len(parts) > 5 else 0,
                }
    
    return results

def format_result(data):
    """格式化输出结果"""
    if "error" in data:
        return f"❌ 获取数据失败: {data['error']}"
    
    if not data:
        return "❌ 未找到数据"
    
    lines = []
    for code, info in data.items():
        name = info.get('name', code)
        price = info.get('price', 0)
        change = info.get('change', 0)
        change_pct = info.get('change_pct', 0)
        
        if price == 0:
            lines.append(f"⚪ **{name}** ({code}): 暂无数据")
            continue
        
        emoji = "🟢" if change >= 0 else "🔴"
        sign = "+" if change >= 0 else ""
        
        line = f"{emoji} **{name}** ({code}): {price:.2f} {sign}{change:.2f} ({sign}{change_pct:.2f}%)"
        
        if 'high' in info and info['high']:
            line += f" 高:{info['high']:.2f} 低:{info['low']:.2f}"
        if 'volume' in info and info['volume']:
            line += f" 量:{info['volume']/10000:.2f}万手"
        
        lines.append(line)
    
    return "\n".join(lines)

def main():
    if len(sys.argv) < 2:
        # 默认查询大盘
        codes = ["sh000001", "sz399001", "sz399006"]
        print("📊 A股主要指数：")
    else:
        query = " ".join(sys.argv[1:])
        codes = []
        yahoo_codes = []
        
        # 支持逗号或空格分隔
        items = re.split(r'[,，\s]+', query)
        
        for item in items:
            code = normalize_code(item.strip())
            if code:
                if code.startswith('yah_'):
                    yahoo_codes.append(code.replace('yah_', ''))
                else:
                    codes.append(code)
        
        if not codes and not yahoo_codes:
            print(f"❌ 无法识别: {query}")
            print("支持的格式：股票名称(如茅台)、代码(如600519)、美股代码(如AAPL)、指数(如VIX)")
            return
    
    # 获取新浪数据
    if codes:
        sina_data = fetch_sina_data(codes)
        print(format_result(sina_data))
    
    # 获取Yahoo Finance数据
    if yahoo_codes:
        if not YFINANCE_AVAILABLE:
            print("\n⚠️  yfinance 未安装，无法获取美股数据")
            print("安装命令: pip3 install yfinance")
            return
        
        print("\n📈 Yahoo Finance 数据：")
        for symbol in yahoo_codes:
            data = fetch_yahoo_data(symbol)
            if data:
                emoji = "🟢" if data['change'] >= 0 else "🔴"
                sign = "+" if data['change'] >= 0 else ""
                print(f"{emoji} **{data['name']}** ({symbol}): {data['price']:.2f} {sign}{data['change']:.2f} ({sign}{data['change_pct']:.2f}%)")
            else:
                print(f"⚪ **{symbol}**: 暂无数据")

if __name__ == "__main__":
    main()
