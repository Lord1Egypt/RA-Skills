#!/usr/bin/env python3
"""
东方财富 F10 数据抓取脚本（browserless CDP 版本）

功能：
- 抓取商誉、净资产、质押率、现金流数据
- 使用 browserless CDP 渲染 JS 页面

数据源：
- 东方财富 F10: https://emdata.eastmoney.com/cwfx/{secid}.html

用法：
    python f10_scraper.py --code 002460
    python f10_scraper.py --code 002460 --json
"""

import argparse
import json
import re
import sys
import time
import urllib.parse
import urllib.request

# Browserless CDP URL
BROWSERLESS_URL = "http://192.168.3.120:3000"

# 东方财富 F10 页面模板
EM_F10_URL = "https://emdata.eastmoney.com/cwfx/{secid}.html"

# 东方财富财务分析 AJAX 接口
EM_FINANCE_AJAX = "https://emweb.eastmoney.com/PC_NewFinanceAnalysis/MainAssetsAjax"


def normalize_code(code):
    """标准化股票代码"""
    c = code.strip().upper().replace(" ", "")
    if c.startswith("SH"):
        c = c[2:]
    elif c.startswith("SZ"):
        c = c[2:]
    if "." in c:
        left, right = c.split(".", 1)
        if left.isdigit():
            c = left
    if not re.fullmatch(r"\d{6}", c):
        raise ValueError("Unsupported code: {}".format(code))
    return c


def code_to_secid(code6):
    """转换为东方财富 secid"""
    if code6.startswith("6"):
        return "1." + code6
    return "0." + code6


def fetch_financial_ajax(code6):
    """
    从东方财富 AJAX 接口获取财务数据（无需 JS）
    
    API: https://emweb.eastmoney.com/PC_NewFinanceAnalysis/MainAssetsAjax
    
    返回 JSON 格式的财务数据
    """
    secid = code_to_secid(code6)
    
    url = EM_FINANCE_AJAX + "?" + urllib.parse.urlencode({
        "type": "web",
        "code": secid,
        "cb": "",  # 不使用 JSONP
    })
    
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://emdata.eastmoney.com/",
    })
    
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            raw = resp.read().decode("utf-8-sig", "ignore")  # 使用 utf-8-sig 处理 BOM
            
            # 尝试解析 JSON（某些接口返回 JSONP）
            if raw.startswith("cb") or "(" in raw[:10]:
                # JSONP 格式：cb({...})
                json_str = re.search(r'\{.*\}', raw).group() if re.search(r'\{.*\}', raw) else "{}"
                obj = json.loads(json_str)
            else:
                obj = json.loads(raw)
            
            return obj
    except Exception as e:
        return {"error": str(e)}


def fetch_balance_sheet_ajax(code6):
    """
    获取资产负债表数据（商誉）
    
    API: https://emweb.eastmoney.com/PC_NewFinanceAnalysis/BalanceSheetAjax
    """
    secid = code_to_secid(code6)
    
    url = "https://emweb.eastmoney.com/PC_NewFinanceAnalysis/BalanceSheetAjax?" + urllib.parse.urlencode({
        "type": "web",
        "code": secid,
    })
    
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://emdata.eastmoney.com/",
    })
    
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            raw = resp.read().decode("utf-8-sig", "ignore")  # 使用 utf-8-sig 处理 BOM
            
            if raw.startswith("cb") or "(" in raw[:10]:
                json_str = re.search(r'\{.*\}', raw).group() if re.search(r'\{.*\}', raw) else "{}"
                obj = json.loads(json_str)
            else:
                obj = json.loads(raw)
            
            # 解析商誉数据
            # 数据结构: { "data": [ { "date": "2024-09-30", "商誉": "12345", ... }, ... ] }
            data = obj.get("data", [])
            
            if not data:
                return None
            
            # 最新一期的商誉
            latest = data[0] if isinstance(data, list) else data
            
            # 商誉字段名可能是中文或英文
            goodwill = None
            net_assets = None
            
            for key, val in latest.items():
                if "商誉" in key or "goodwill" in key.lower():
                    goodwill = val
                if "净资产" in key or "net_assets" in key.lower() or "股东权益" in key:
                    net_assets = val
            
            return {
                "goodwill": goodwill,
                "net_assets": net_assets,
                "date": latest.get("date") or latest.get("报告期"),
                "raw": latest,
            }
    
    except Exception as e:
        return {"error": str(e)}


def fetch_cashflow_ajax(code6):
    """
    获取现金流数据
    
    API: https://emweb.eastmoney.com/PC_NewFinanceAnalysis/CashFlowAjax
    """
    secid = code_to_secid(code6)
    
    url = "https://emweb.eastmoney.com/PC_NewFinanceAnalysis/CashFlowAjax?" + urllib.parse.urlencode({
        "type": "web",
        "code": secid,
    })
    
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://emdata.eastmoney.com/",
    })
    
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            raw = resp.read().decode("utf-8-sig", "ignore")  # 使用 utf-8-sig 处理 BOM
            
            if raw.startswith("cb") or "(" in raw[:10]:
                json_str = re.search(r'\{.*\}', raw).group() if re.search(r'\{.*\}', raw) else "{}"
                obj = json.loads(json_str)
            else:
                obj = json.loads(raw)
            
            data = obj.get("data", [])
            
            if not data:
                return None
            
            # 解析经营性现金流
            cashflow_values = []
            
            for item in data[:4]:  # 最近4期
                for key, val in item.items():
                    if "经营" in key and "现金流" in key:
                        try:
                            cashflow_values.append(float(val) if val else 0)
                        except:
                            pass
            
            # 计算连续负值次数
            negative_count = 0
            for cf in cashflow_values:
                if cf < 0:
                    negative_count += 1
                else:
                    break  # 中断连续计数
            
            return {
                "cashflow_recent": cashflow_values[:4],
                "cashflow_negative_count": negative_count,
                "raw": data[:4] if isinstance(data, list) else data,
            }
    
    except Exception as e:
        return {"error": str(e)}


def fetch_pledge_data(code6):
    """
    获取质押数据（需要 JS 渲染）
    
    暂时返回占位数据，实际需要 browserless
    """
    # 东方财富质押页面
    # https://data.eastmoney.com/gp/gplist.html
    
    return {
        "pledge_ratio": None,
        "status": "pending",
        "note": "质押数据需 browserless JS 渲染",
    }


def scrape_f10_data(code6):
    """
    综合抓取 F10 数据
    
    返回：商誉、净资产、质押率、现金流
    """
    result = {
        "code": code6,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    
    # 1. 资产负债表（商誉）
    balance = fetch_balance_sheet_ajax(code6)
    result["balance_sheet"] = balance
    
    if balance and not balance.get("error"):
        goodwill = balance.get("goodwill")
        net_assets = balance.get("net_assets")
        
        # 计算商誉占比
        if goodwill and net_assets:
            try:
                gw = float(goodwill)
                na = float(net_assets)
                if na > 0:
                    result["goodwill_ratio"] = round(gw / na * 100, 2)
            except:
                pass
    
    # 2. 现金流
    cashflow = fetch_cashflow_ajax(code6)
    result["cashflow"] = cashflow
    
    if cashflow and not cashflow.get("error"):
        result["cashflow_negative_count"] = cashflow.get("cashflow_negative_count", 0)
    
    # 3. 质押（占位）
    pledge = fetch_pledge_data(code6)
    result["pledge"] = pledge
    
    return result


def main():
    parser = argparse.ArgumentParser(description="东方财富 F10 数据抓取")
    parser.add_argument("--code", required=True, help="股票代码")
    parser.add_argument("--json", action="store_true", help="输出 JSON")
    args = parser.parse_args()
    
    code6 = normalize_code(args.code)
    result = scrape_f10_data(code6)
    
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"\n📊 {code6} F10 数据")
        
        if result.get("goodwill_ratio"):
            print(f"商誉占比: {result['goodwill_ratio']}%")
        else:
            print("商誉占比: N/A")
        
        print(f"现金流负值连续: {result.get('cashflow_negative_count', 0)}季度")
        print(f"质押率: {result.get('pledge', {}).get('pledge_ratio') or 'N/A'}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())