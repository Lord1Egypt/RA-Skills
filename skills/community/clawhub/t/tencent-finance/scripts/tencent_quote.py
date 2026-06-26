#!/usr/bin/env python3
"""
腾讯财经行情接口 - 实时行情查询工具
用法：
  python3 tencent_quote.py [代码列表]
  python3 tencent_quote.py sh000001 sz399001 hkHSI
  python3 tencent_quote.py --list 预设常用指数
"""

import sys
import requests
import json
from datetime import datetime

BASE_URL = "https://qt.gtimg.cn/q="

# 预设代码列表
PRESET_CODES = {
    "A股指数": ["sh000001", "sz399001", "sz399006", "sh000300", "sh000688"],
    "港股指数": ["hkHSI", "hkHSTECH"],
    "A股个股": ["sh600519", "sz300750", "sz002594", "sh600036", "sh560860"],
    "港股个股": ["hk00700", "hk09988", "hk03690", "hk01810"],
    "商品外汇": ["hf_GC", "hf_CL", "fx_usr"],
}

def parse_quote(raw_data, code):
    """解析腾讯行情原始数据"""
    try:
        # 格式: v_xxx="1~名称~代码~现价~昨收~今开~...~涨跌额~涨跌幅~最高~最低~..."
        content = raw_data.strip()
        if '="1~' not in content and '="v_' not in content:
            return None
        
        inner = content.split('="')[1].strip().strip('";')
        fields = inner.split('~')
        
        if len(fields) < 35:
            return None
        
        return {
            "code": code,
            "name": fields[1] if fields[1] else code,
            "price": fields[3] if len(fields) > 3 else "-",
            "yesterday_close": fields[4] if len(fields) > 4 else "-",
            "open": fields[5] if len(fields) > 5 else "-",
            "change": fields[31] if len(fields) > 31 and fields[31] else "0",
            "change_pct": fields[32] if len(fields) > 32 and fields[32] else "0",
            "high": fields[33] if len(fields) > 33 and fields[33] else "-",
            "low": fields[34] if len(fields) > 34 and fields[34] else "-",
            "volume": fields[36] if len(fields) > 36 and fields[36] else "-",
            "turnover": fields[37] if len(fields) > 37 and fields[37] else "-",
            "turnover_rate": fields[38] if len(fields) > 38 and fields[38] else "-",
            "pe": fields[39] if len(fields) > 39 and fields[39] else "-",
            "amplitude": fields[43] if len(fields) > 43 and fields[43] else "-",
            "mkt_cap_cir": fields[44] if len(fields) > 44 and fields[44] else "-",
            "mkt_cap_total": fields[45] if len(fields) > 45 and fields[45] else "-",
        }
    except Exception as e:
        return {"code": code, "error": str(e)}


def get_quotes(codes):
    """批量获取行情数据"""
    if not codes:
        return []
    
    url = BASE_URL + ",".join(codes)
    try:
        resp = requests.get(url, timeout=10)
        # 不强制指定编码，腾讯返回的是GBK，但requests默认能处理
        text = resp.text
        
        results = []
        for code in codes:
            # 查找包含该代码的数据行
            search_patterns = [f'"{code}~"', f'~{code}~']
            for line in text.split('\n'):
                if any(p in line for p in search_patterns):
                    quote = parse_quote(line, code)
                    if quote and 'error' not in quote:
                        results.append(quote)
                    break
        
        return results
    except Exception as e:
        print(f"请求失败: {e}", file=sys.stderr)
        return []


def format_quote(q):
    """格式化输出单条行情"""
    try:
        change = float(q.get("change", 0))
        change_pct = float(q.get("change_pct", 0))
        arrow = "▲" if change >= 0 else "▼"
        sign = "+" if change >= 0 else ""
        
        output = [
            f"{q['name']} ({q['code']})",
            f"  价格: {q['price']}  {arrow} {sign}{change} ({sign}{change_pct}%)",
            f"  今开: {q['open']}  最高: {q['high']}  最低: {q['low']}",
        ]
        
        if q.get("volume") and q["volume"] != "-":
            vol = int(float(q["volume"]))
            output.append(f"  成交量: {vol:,} 手")
        
        if q.get("turnover_rate") and q["turnover_rate"] != "-":
            output.append(f"  换手率: {q['turnover_rate']}%")
        
        if q.get("pe") and q["pe"] not in ["-", ""]:
            output.append(f"  市盈率: {q['pe']}")
        
        return "\n".join(output)
    except:
        return f"{q['name']} ({q['code']}): 解析失败"


def main():
    if len(sys.argv) < 2:
        # 默认显示A股主要指数
        codes = ["sh000001", "sz399001", "sz399006", "sh000300", "hkHSI", "hkHSTECH"]
        print(f"【{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 行情快照】\n")
    elif sys.argv[1] == "--list":
        print("可用预设组合：")
        for name in PRESET_CODES:
            print(f"  {name}: {', '.join(PRESET_CODES[name])}")
        return
    else:
        codes = sys.argv[1:]

    quotes = get_quotes(codes)
    
    if not quotes:
        print("未获取到数据，请检查代码是否正确")
        return
    
    for q in quotes:
        print(format_quote(q))
        print()


if __name__ == "__main__":
    main()
