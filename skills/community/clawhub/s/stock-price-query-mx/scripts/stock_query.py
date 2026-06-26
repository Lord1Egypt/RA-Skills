#!/usr/bin/env python3
"""
Stock Price Query Script v2 - 混合数据源版
查询 A 股（沪深）、港股、美股的实时行情数据。

数据源策略：
- A 股/美股：腾讯财经 API (qt.gtimg.cn)
- 港股：东方财富妙想数据服务（解决腾讯 API 港股延迟问题）

用法:
    python3 stock_query_v2.py <code1,code2,code3>
"""

import sys
import json
import re
import time
import urllib.request
import urllib.error
import os
from datetime import datetime

# 输入校验正则
VALID_CODE_PATTERN = re.compile(r'^\.?[A-Za-z0-9]{1,10}$')
VALID_MARKETS = {"sh", "sz", "hk", "us"}
HK_INDEX_CODES = {"HSI", "HSCEI", "HSTECH", "HSCCI"}


def validate_input(code: str, market: str | None) -> str | None:
    """校验输入参数"""
    if not VALID_CODE_PATTERN.match(code):
        return f"非法的股票代码 '{code}'。"
    if market is not None and market not in VALID_MARKETS:
        return f"非法的市场标识 '{market}'。"
    return None


def detect_market(code: str) -> str:
    """根据股票代码自动识别市场"""
    code = code.strip().upper()
    
    if code.startswith("SH"): return "sh"
    if code.startswith("SZ"): return "sz"
    if code.startswith("HK"): return "hk"
    if code.startswith("."): return "us"
    if code in HK_INDEX_CODES: return "hk"
    if re.match(r'^[A-Z]{1,5}$', code): return "us"
    
    digits = re.sub(r'[^0-9]', '', code)
    if len(digits) == 6:
        # A 股：6 开头沪市，0/3 开头深市，5/1 开头 ETF
        if digits.startswith('6') or digits.startswith('5'):
            return "sh"
        elif digits.startswith('0') or digits.startswith('3') or digits.startswith('1'):
            return "sz"
        else:
            return "sh"
    elif 1 <= len(digits) <= 5:
        return "hk"
    
    return "unknown"


def clean_code(code: str) -> str:
    """清理股票代码，去除市场前缀"""
    code = code.strip().upper()
    for prefix in ["SH", "SZ", "HK"]:
        if code.startswith(prefix):
            return code[len(prefix):]
    return code


def build_tencent_symbol(code: str, market: str) -> str:
    """构建腾讯财经 API 的股票符号"""
    code = clean_code(code)
    if market == "sh": return f"sh{code}"
    elif market == "sz": return f"sz{code}"
    elif market == "hk":
        if code.upper() in HK_INDEX_CODES:
            return f"hk{code.upper()}"
        return f"hk{code.zfill(5)}"
    elif market == "us":
        return f"us{code.upper()}"
    return code


def parse_stock(raw: str, code: str, market: str) -> dict:
    """解析腾讯财经 API 返回的行情数据"""
    parts = raw.split("~")
    if len(parts) < 35:
        return {"status": "error", "message": "数据解析失败"}

    name = parts[1].strip()
    if not name:
        return {"status": "error", "message": f"未找到股票 {clean_code(code)}"}

    current_price = float(parts[3]) if parts[3] else 0
    prev_close = float(parts[4]) if parts[4] else 0
    open_price = float(parts[5]) if parts[5] else 0
    volume_raw = parts[6].strip() if parts[6] else "0"
    volume = int(float(volume_raw))
    time_str = parts[30].strip() if len(parts) > 30 and parts[30] else ""
    change = float(parts[31]) if len(parts) > 31 and parts[31] else 0
    change_pct = float(parts[32]) if len(parts) > 32 and parts[32] else 0
    high = float(parts[33]) if len(parts) > 33 and parts[33] else 0
    low = float(parts[34]) if len(parts) > 34 and parts[34] else 0
    amount_raw = parts[37].strip() if len(parts) > 37 and parts[37] else "0"
    amount = float(amount_raw) if amount_raw else 0

    if market in ("sh", "sz"):
        volume = volume * 100
        amount = amount * 10000

    display_code = clean_code(code)
    if market == "hk":
        if display_code.upper() not in HK_INDEX_CODES:
            display_code = display_code.zfill(5)
        else:
            display_code = display_code.upper()
    elif market == "us":
        display_code = display_code.upper()

    return {
        "code": display_code,
        "name": name,
        "market": market,
        "current_price": current_price,
        "change": change,
        "change_percent": change_pct,
        "open": open_price,
        "high": high,
        "low": low,
        "prev_close": prev_close,
        "volume": volume,
        "amount": amount,
        "time": time_str,
        "status": "success",
    }


def fetch_hk_stock_mx(code: str) -> dict | None:
    """使用妙想数据服务获取港股实时行情（解决腾讯 API 延迟问题）"""
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
        # 分两次查询：先获取最新价，再获取涨跌幅
        result = subprocess.run(
            ['python3', '/root/.openclaw/workspace/skills/mx-finance-data/scripts/get_data.py',
             '--query', f'{code}.HK 最新价'],
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
        
        first_col_name = str(df.columns[0])
        
        # 提取股票代码
        match = re.search(r'\((\d+)\.HK\)', first_col_name)
        code_from_file = match.group(1) if match else code
        
        # 解析最新价数据（单列实时数据格式）
        # 格式：第一列股票名，第二列最新价
        price = 0
        time_str = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        
        if len(df.columns) >= 2 and len(df) >= 1:
            try:
                price = float(df.iloc[0, 1])
            except:
                pass
        
        # 第二次查询：获取涨跌幅
        change_pct = 0
        try:
            result2 = subprocess.run(
                ['python3', '/root/.openclaw/workspace/skills/mx-finance-data/scripts/get_data.py',
                 '--query', f'{code}.HK 涨跌幅'],
                capture_output=True,
                text=True,
                timeout=30,
                env=env
            )
            
            xlsx_path2 = None
            for line in result2.stdout.split('\n'):
                if line.startswith('文件:'):
                    xlsx_path2 = line.replace('文件:', '').strip()
                    break
            
            if xlsx_path2:
                df2 = pd.read_excel(xlsx_path2)
                # 查找"涨跌幅"行
                for idx, row in df2.iterrows():
                    indicator = str(row.iloc[0]).strip() if len(row) > 0 else ''
                    value = str(row.iloc[1]).strip() if len(row) > 1 else '0'
                    
                    # 精确匹配"涨跌幅"（第一行通常是当日涨跌幅）
                    if indicator == '涨跌幅' and idx == 0:
                        try:
                            change_pct_str = value.replace('%', '')
                            change_pct = float(change_pct_str)
                        except:
                            pass
                        break
        except:
            pass
        
        # 计算涨跌额
        change = 0
        if change_pct != 0 and price != 0:
            prev_close = price / (1 + change_pct / 100)
            change = price - prev_close
        
        # 计算涨跌额
        if change_pct != 0 and price != 0:
            prev_close = price / (1 + change_pct / 100)
            change = price - prev_close
        
        return {
            'code': code_from_file,
            'current_price': price,
            'change_percent': change_pct,
            'change': change,
            'source': 'mx',
            'time': time_str
        }
    except Exception as e:
        print(f"妙想数据获取失败：{e}", file=sys.stderr)
        return None


def fetch_batch(codes: list[str]) -> list[dict]:
    """批量获取多只股票的实时行情（混合数据源：A 股用腾讯，港股用妙想）"""
    code_market_pairs = []
    symbol_list = []
    hk_codes = []
    
    for code in codes:
        market = detect_market(code)
        code_market_pairs.append((code, market))
        
        if market == "hk":
            hk_codes.append(code)
            symbol_list.append(None)
        elif market != "unknown":
            symbol_list.append(build_tencent_symbol(code, market))
        else:
            symbol_list.append(None)

    # 1. 先用腾讯 API 查询 A 股/美股
    tencent_results = {}
    valid_symbols = [s for s in symbol_list if s is not None]
    
    if valid_symbols:
        url = f"https://qt.gtimg.cn/q={','.join(valid_symbols)}"
        
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=15) as resp:
                raw = resp.read().decode("gbk", errors="ignore")
            
            response_map = {}
            for match in re.finditer(r'v_([a-zA-Z0-9.]+)="([^"]*)"', raw):
                resp_symbol = match.group(1)
                resp_data = match.group(2)
                response_map[resp_symbol.lower()] = resp_data
            
            for i, (code, market) in enumerate(code_market_pairs):
                if market in ("sh", "sz", "us") and symbol_list[i]:
                    resp_data = response_map.get(symbol_list[i].lower())
                    if resp_data:
                        tencent_results[code] = parse_stock(resp_data, code, market)
        except Exception as e:
            print(f"腾讯 API 查询失败：{e}", file=sys.stderr)
    
    # 2. 用妙想数据查询港股
    mx_results = {}
    for code in hk_codes:
        mx_data = fetch_hk_stock_mx(code)
        if mx_data:
            price = mx_data['current_price']
            change_pct = mx_data.get('change_percent', 0)
            change = mx_data.get('change', 0)
            prev_close = price - change if change != 0 else price
            
            mx_results[code] = {
                "code": mx_data['code'],
                "name": "港股",
                "market": "hk",
                "current_price": price,
                "change": change,
                "change_percent": change_pct,
                "open": price,
                "high": price,
                "low": price,
                "prev_close": prev_close,
                "volume": 0,
                "amount": 0,
                "time": mx_data.get('time', datetime.now().strftime("%Y/%m/%d %H:%M:%S")),
                "status": "success",
            }
    
    # 3. 合并结果，保持原始顺序
    results = []
    for code, market in code_market_pairs:
        if market == "unknown":
            results.append({
                "status": "error",
                "code": clean_code(code),
                "message": f"无法识别股票代码 {code}，请确认后重试。",
            })
        elif market == "hk" and code in mx_results:
            results.append(mx_results[code])
        elif code in tencent_results:
            results.append(tencent_results[code])
        else:
            results.append({
                "status": "error",
                "code": clean_code(code),
                "message": f"未找到股票 {clean_code(code)}，请检查代码是否正确",
            })
    
    return results


def main():
    if len(sys.argv) < 2:
        print(json.dumps(
            {"status": "error", "message": "用法：python3 stock_query_v2.py <code1,code2,code3>"},
            ensure_ascii=False,
        ))
        sys.exit(1)

    raw_input = sys.argv[1].strip()

    if "," in raw_input:
        codes = [c.strip() for c in raw_input.split(",") if c.strip()]
        if len(codes) > 20:
            print(json.dumps(
                {"status": "error", "message": "批量查询最多支持 20 只股票"},
                ensure_ascii=False,
            ))
            sys.exit(1)

        for c in codes:
            validation_error = validate_input(c, None)
            if validation_error:
                print(json.dumps(
                    {"status": "error", "message": f"股票代码 '{c}' 校验失败：{validation_error}"},
                    ensure_ascii=False,
                ))
                sys.exit(1)

        results = fetch_batch(codes)
        print(json.dumps(results, ensure_ascii=False, indent=2))

        if all(r.get("status") != "success" for r in results):
            sys.exit(1)
    else:
        code = raw_input
        market = sys.argv[2].strip().lower() if len(sys.argv) > 2 else None

        validation_error = validate_input(code, market)
        if validation_error:
            print(json.dumps(
                {"status": "error", "message": validation_error},
                ensure_ascii=False,
            ))
            sys.exit(1)

        if not market:
            market = detect_market(code)

        if market == "unknown":
            print(json.dumps(
                {"status": "error", "message": "无法识别该股票代码"},
                ensure_ascii=False,
            ))
            sys.exit(1)

        # 单只查询：港股用妙想，其他用腾讯
        if market == "hk":
            mx_data = fetch_hk_stock_mx(code)
            if mx_data:
                result = {
                    "code": mx_data['code'],
                    "name": "港股",
                    "market": "hk",
                    "current_price": mx_data['current_price'],
                    "change": 0,
                    "change_percent": 0,
                    "open": mx_data['current_price'],
                    "high": mx_data['current_price'],
                    "low": mx_data['current_price'],
                    "prev_close": mx_data['current_price'],
                    "volume": 0,
                    "amount": 0,
                    "time": mx_data.get('time', ''),
                    "status": "success",
                }
                print(json.dumps(result, ensure_ascii=False, indent=2))
                return
        
        # 非港股或妙想失败，用腾讯 API
        result = parse_tencent_single(code, market)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        if result.get("status") != "success":
            sys.exit(1)


def parse_tencent_single(code: str, market: str) -> dict:
    """单只股票查询（腾讯 API）"""
    symbol = build_tencent_symbol(code, market)
    url = f"https://qt.gtimg.cn/q={symbol}"

    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=10) as resp:
            raw = resp.read().decode("gbk", errors="ignore")

        if '=""' in raw or not raw.strip():
            return {"status": "error", "message": f"未找到股票 {clean_code(code)}"}

        return parse_stock(raw, code, market)
    except Exception as e:
        return {"status": "error", "message": f"查询异常：{str(e)}"}


if __name__ == "__main__":
    main()
