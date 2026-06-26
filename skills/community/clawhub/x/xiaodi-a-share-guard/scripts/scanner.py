#!/usr/bin/env python3
"""
A股避雷针 - 量化扫描器
整合 a_share_snapshot.py + 新雷达指标

雷达指标：
1. 商誉占比（Goodwill Ratio）
2. 大股东质押率（Major Shareholder Pledge Ratio）
3. 经营性现金流净额（Operating Cash Flow）

数据源：
- 东方财富 F10（财务数据）
- 腾讯/东方财富 API（行情数据）
"""

import argparse
import datetime as dt
import json
import re
import urllib.parse
import urllib.request


# ========== API 配置 ==========
EM_QUOTE_API = "https://push2.eastmoney.com/api/qt/ulist.np/get"
EM_F10_API = "https://emweb.eastmoney.com/PC_HSF10/NewFinanceAnalysis/Index"
TX_KLINE_API = "https://web.ifzq.gtimg.cn/appstock/app/fqkline/get"


# ========== 工具函数 ==========
def _http_get_json(url, timeout=15):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8", "ignore"))


def normalize_code(code):
    c = code.strip().upper().replace(" ", "")
    if c.startswith("SH") and len(c) == 8 and c[2:].isdigit():
        c = c[2:]
    elif c.startswith("SZ") and len(c) == 8 and c[2:].isdigit():
        c = c[2:]
    if "." in c:
        left, right = c.split(".", 1)
        if left.isdigit() and right in {"SH", "SS", "SZ"}:
            c = left
    if not re.fullmatch(r"\d{6}", c):
        raise ValueError("Unsupported code format: {}".format(code))
    return c


def code_to_secid(code6):
    if code6.startswith("6"):
        return "1." + code6
    return "0." + code6


def code_to_tencent_symbol(code6):
    if code6.startswith("6"):
        return "sh" + code6
    return "sz" + code6


# ========== 行情数据（继承 a_share_snapshot）==========
def fetch_quotes(codes):
    """获取实时行情快照"""
    secids = [code_to_secid(c) for c in codes]
    fields = "f12,f14,f2,f3,f4,f5,f6,f7,f8,f9,f10,f15,f16,f17,f18"
    url = EM_QUOTE_API + "?" + urllib.parse.urlencode({
        "fltt": "2",
        "invt": "2",
        "fields": fields,
        "secids": ",".join(secids),
    })
    obj = _http_get_json(url)
    diff = obj.get("data", {}).get("diff", [])
    
    out = []
    for it in diff:
        out.append({
            "code": str(it.get("f12", "")),
            "name": it.get("f14"),
            "last": it.get("f2"),
            "pct": it.get("f3"),
            "chg": it.get("f4"),
            "volume": it.get("f5"),
            "amount": it.get("f6"),
            "amplitude": it.get("f7"),
            "turnover": it.get("f8"),
            "pe_ttm": it.get("f9"),
            "volume_ratio": it.get("f10"),
            "high": it.get("f15"),
            "low": it.get("f16"),
            "open": it.get("f17"),
            "prev_close": it.get("f18"),
        })
    
    order = dict((c, i) for i, c in enumerate(codes))
    out.sort(key=lambda x: order.get(x.get("code"), 9999))
    return out


# ========== 新增：雷达指标 ==========
def fetch_goodwill_ratio(code6):
    """
    商誉占比 = 商誉 / 总资产
    雷点阈值：>30%
    
    数据源：东方财富 F10（需要 browserless 抓取）
    """
    # 简化版：返回模拟数据（实际需要 browserless 抓取 F10 页面）
    # TODO: 实现 browserless CDP 抓取
    return {
        "goodwill": None,  # 商誉（亿元）
        "total_assets": None,  # 总资产（亿元）
        "ratio": None,  # 商誉占比
        "status": "pending",  # pending / safe / warning / danger
        "source": "东方财富F10",
    }


def fetch_pledge_ratio(code6):
    """
    大股东质押率
    雷点阈值：>50%
    
    数据源：东方财富 F10
    """
    # 简化版：返回模拟数据
    # TODO: 实现 browserless 抓取质押数据
    return {
        "pledge_ratio": None,  # 质押率
        "pledge_amount": None,  # 质押股数
        "status": "pending",
        "source": "东方财富F10",
    }


def fetch_operating_cashflow(code6, quarters=4):
    """
    经营性现金流净额（最近N季度）
    雷点阈值：连续2季度负值
    
    数据源：东方财富财务分析
    """
    # 简化版：返回模拟数据
    # TODO: 实现财务数据抓取
    return {
        "recent_quarters": [],  # 最近N季度现金流
        "negative_count": 0,  # 负值季度数
        "status": "pending",
        "source": "东方财富财务分析",
    }


# ========== 风险阈值（红线指标）==========
RED_LINE_THRESHOLDS = {
    "goodwill_ratio": 30,      # 商誉/净资产 > 30% → CRITICAL_RISK
    "pledge_ratio": 50,        # 大股东质押 > 50% → CRITICAL_RISK
    "cashflow_negative_count": 2,  # 连续2季度现金流负 → WARNING
}


# ========== 风险评分 ==========
def calculate_risk_score(radar_data):
    """
    计算综合风险评分（0-100）
    
    红线指标（触发直接预警）：
    - 商誉占比 >30% → +30分 + CRITICAL_RISK
    - 质押率 >50% → +25分 + CRITICAL_RISK
    
    其他指标：
    - 现金流连续负值 → +35分
    - PE-TTM >100 → +10分
    """
    score = 0
    reasons = []
    signal = "SAFE"
    
    # 红线检查：商誉占比
    gw = radar_data.get("goodwill", {})
    gw_ratio = gw.get("ratio")
    if gw_ratio and gw_ratio > RED_LINE_THRESHOLDS["goodwill_ratio"]:
        score += 30
        reasons.append(f"商誉占比过高（{gw_ratio}% > 30%）")
        signal = "CRITICAL_RISK"
    
    # 红线检查：质押率
    pl = radar_data.get("pledge", {})
    pl_ratio = pl.get("pledge_ratio")
    if pl_ratio and pl_ratio > RED_LINE_THRESHOLDS["pledge_ratio"]:
        score += 25
        reasons.append(f"大股东质押率高（{pl_ratio}% > 50%）")
        signal = "CRITICAL_RISK"
    
    # 现金流检查
    cf = radar_data.get("cashflow", {})
    cf_neg = cf.get("negative_count", 0)
    if cf_neg >= RED_LINE_THRESHOLDS["cashflow_negative_count"]:
        score += 35
        reasons.append(f"现金流连续{cf_neg}季度负值")
        if signal == "SAFE":
            signal = "WARNING"
    
    # PE-TTM
    quote = radar_data.get("quote", {})
    if quote.get("pe_ttm") and quote["pe_ttm"] > 100:
        score += 10
        reasons.append(f"PE-TTM过高（{quote['pe_ttm']}）")
    
    # 评级
    if score >= 70:
        level = "高危"
    elif score >= 50:
        level = "预警"
    elif score >= 30:
        level = "观察"
    else:
        level = "安全"
    
    # 如果触犯红线，强制升级为 CRITICAL_RISK
    if signal == "CRITICAL_RISK":
        level = "高危"
    
    return {
        "score": score,
        "level": level,
        "reasons": reasons,
        "signal": signal,  # SAFE / WARNING / CRITICAL_RISK
    }


# ========== 主扫描函数 ==========
def scan_stock(code6):
    """扫描单只股票"""
    result = {
        "timestamp": dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "code": code6,
    }
    
    # 1. 行情数据
    try:
        quotes = fetch_quotes([code6])
        result["quote"] = quotes[0] if quotes else None
    except Exception as e:
        result["quote"] = {"error": str(e)}
    
    # 2. 雷达指标
    result["goodwill"] = fetch_goodwill_ratio(code6)
    result["pledge"] = fetch_pledge_ratio(code6)
    result["cashflow"] = fetch_operating_cashflow(code6)
    
    # 3. 风险评分
    result["risk"] = calculate_risk_score(result)
    
    return result


def main():
    parser = argparse.ArgumentParser(description="A股避雷针 - 量化扫描器")
    parser.add_argument("--codes", required=True, help="股票代码（逗号分隔）")
    parser.add_argument("--pretty", action="store_true", help="美化输出")
    args = parser.parse_args()
    
    codes = [normalize_code(c) for c in args.codes.split(",")]
    
    results = []
    for c in codes:
        try:
            r = scan_stock(c)
            results.append(r)
        except Exception as e:
            results.append({"code": c, "error": str(e)})
    
    output = {
        "timestamp": dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "codes": codes,
        "results": results,
    }
    
    print(json.dumps(output, ensure_ascii=False, indent=2 if args.pretty else None))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())