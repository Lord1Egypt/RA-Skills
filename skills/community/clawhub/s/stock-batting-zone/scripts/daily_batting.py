#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
每日击球区日报 - 五因子精准版
- 原始3股 + 四大行
- 因子: 股息率(30%) + PE分位(15%) + PB分位(15%) + ROE(20%) + 安全性(20%)
- 数据源: 新浪行情 / 小乐财报 / 东方财富
- 中国交易日历(chinese_calendar)
"""

import os
import sys
import io
import json
import logging
import argparse
import re
from datetime import datetime, date

os.environ.setdefault("PYTHONIOENCODING", "utf-8")
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

import requests
from chinese_calendar import is_workday

# ============== 股票配置 ==============
STOCKS = [
    {
        "code": "sh600900", "name": "长江电力", "api_code": "600900",
        "annual_div": 1.00, "leetab_code": "sh600900",
        "ex_div_date": "2026-02-12", "is_bank": False,
        "total_shares_billion": 24.47,  # 总股本(亿股)
    },
    {
        "code": "sh600887", "name": "伊利股份", "api_code": "600887",
        "annual_div": 1.38, "leetab_code": "sh600887",
        "ex_div_date": "2026-06-05", "is_bank": False,
        "total_shares_billion": 63.66,
    },
    {
        "code": "sz000651", "name": "格力电器", "api_code": "000651",
        "annual_div": 3.00, "leetab_code": "sz000651",
        "ex_div_date": "2026-01-23", "is_bank": False,
        "total_shares_billion": 5.60,
    },
    {
        "code": "sh601939", "name": "建设银行", "api_code": "601939",
        "annual_div": 0.3887, "leetab_code": "sh601939",
        "ex_div_date": None, "is_bank": True,
    },
    {
        "code": "sh600941", "name": "中国移动", "api_code": "600941",
        "annual_div": 4.7037, "leetab_code": "sh600941",
        "ex_div_date": "2026-06-05", "is_bank": False,
        "total_shares_billion": 214.7,
    },
]

DEFAULT_PE_PB = {
    "sh600900": {"pe": 18.44, "pe_pct": 2,  "pb": 2.92, "pb_pct": 14},
    "sh600887": {"pe": 12.98, "pe_pct": 9,  "pb": 2.91, "pb_pct": 5},
    "sz000651": {"pe": 7.16,  "pe_pct": 24, "pb": 1.37, "pb_pct": 0},
    "sh601939": {"pe": 6.0,   "pe_pct": 25, "pb": 0.7,  "pb_pct": 45},
    "sh600941": {"pe": 14.64, "pe_pct": 11, "pb": 1.44, "pb_pct": 3},
}

PUSH_SCRIPT = r"C:\Users\And19\.openclaw\workspace\skills\today-task\scripts\task_push.py"
SINA_URL = "https://hq.sinajs.cn/list={codes}"
SINA_REFERER = "https://finance.sina.com.cn"
LEETAB_PE_URL = "https://www.leetab.com/stock/{code}/pe"
LEETAB_PB_URL = "https://www.leetab.com/stock/{code}/pb"
EASTMONEY_DIV_URL = (
    "https://datacenter-web.eastmoney.com/api/data/v1/get?"
    "reportName=RPT_SHAREBONUS_DET"
    "&columns=SECURITY_CODE,PRETAX_BONUS_RMB,EX_DIVIDEND_DATE,ASSIGN_PROGRESS,REPORT_DATE"
    "&filter=(SECURITY_CODE%3D%22{code}%22)"
    "&pageNumber=1&pageSize=4&sortTypes=-1&sortColumns=PLAN_NOTICE_DATE"
)
TIMEOUT = 10

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
log = logging.getLogger("daily-report")


# ============== 数据抓取 ==============
def fetch_quotes():
    codes = ",".join(s["code"] for s in STOCKS)
    url = SINA_URL.format(codes=codes)
    try:
        r = requests.get(url, headers={"Referer": SINA_REFERER, "User-Agent": "Mozilla/5.0"}, timeout=TIMEOUT)
        r.encoding = "gbk"
        results = {}
        for line in r.text.strip().split("\n"):
            if '"' not in line: continue
            body = line.split('"')[1]
            if not body: continue
            fields = body.split(",")
            if len(fields) < 10: continue
            m = re.search(r'hq_str_(\w+)', line)
            if not m: continue
            raw_code = m.group(1)
            for s in STOCKS:
                if s["code"] == raw_code:
                    results[s["code"]] = {
                        "name": fields[0], "open": float(fields[1]),
                        "prev_close": float(fields[2]), "close": float(fields[3]),
                        "high": float(fields[4]), "low": float(fields[5]),
                        "date": fields[30] if len(fields) > 30 else "",
                    }
                    break
        return results
    except Exception as e:
        log.error(f"fetch_quotes failed: {e}")
        return {}


def fetch_leetab_pct(code):
    pe_data = pb_data = None
    try:
        r = requests.get(LEETAB_PE_URL.format(code=code), timeout=TIMEOUT)
        m = re.search(r'当前值\s*([\d.]+)', r.text)
        pe_val = float(m.group(1)) if m else None
        m = re.search(r'百分位[：:]\s*([\d.]+)%', r.text)
        pe_pct = float(m.group(1)) if m else None
        if pe_val and pe_pct is not None:
            pe_data = {"pe": pe_val, "pe_pct": pe_pct}
    except: pass
    try:
        r = requests.get(LEETAB_PB_URL.format(code=code), timeout=TIMEOUT)
        m = re.search(r'当前值\s*([\d.]+)', r.text)
        pb_val = float(m.group(1)) if m else None
        m = re.search(r'百分位[：:]\s*([\d.]+)%', r.text)
        pb_pct = float(m.group(1)) if m else None
        if pb_val and pb_pct is not None:
            pb_data = {"pb": pb_val, "pb_pct": pb_pct}
    except: pass
    result = {}
    if pe_data: result.update(pe_data)
    if pb_data: result.update(pb_data)
    return result


def get_pe_pb(code):
    fetched = fetch_leetab_pct(code)
    default = DEFAULT_PE_PB.get(code, {})
    return {**default, **fetched}


def fetch_ex_div_date(api_code):
    try:
        r = requests.get(EASTMONEY_DIV_URL.format(code=api_code), timeout=TIMEOUT)
        items = r.json().get("result", {}).get("data", [])
        for item in items:
            ex = item.get("EX_DIVIDEND_DATE")
            if ex: return ex[:10]
    except: pass
    return None


def get_ex_div_date(stock):
    fetched = fetch_ex_div_date(stock["api_code"])
    return fetched or stock.get("ex_div_date") or "待定"


EASTMONEY_FIN_URL = (
    "https://datacenter-web.eastmoney.com/api/data/v1/get?"
    "reportName=RPT_F10_FINANCE_MAINFINADATA"
    "&columns=SECURITY_CODE,ROEJQ,EPSJB,FCFF_FORWARD,PARENTNETPROFIT,ZCFZL"
    "&filter=(SECURITY_CODE%3D%22{code}%22)(REPORT_TYPE%3D%22年报%22)"
    "&pageNumber=1&pageSize=1&sortTypes=-1&sortColumns=REPORT_DATE"
)


def fetch_financials(api_code):
    """从东方财富抓 ROE、EPS、FCFF、净利润(年报)"""
    try:
        r = requests.get(EASTMONEY_FIN_URL.format(code=api_code), timeout=TIMEOUT)
        items = r.json().get("result", {}).get("data", [])
        if items:
            d = items[0]
            return {
                "roe": d.get("ROEJQ"),
                "eps": d.get("EPSJB"),
                "fcff": d.get("FCFF_FORWARD"),  # 元
                "net_profit": d.get("PARENTNETPROFIT"),  # 元
                "debt_ratio": d.get("ZCFZL"),
            }
    except Exception as e:
        log.warning(f"fetch_financials for {api_code} failed: {e}")
    return {}


def get_financials(stock):
    """获取财务数据并计算分红安全性指标"""
    fin = fetch_financials(stock["api_code"])
    result = {
        "roe": fin.get("roe"),
        "debt_ratio": fin.get("debt_ratio"),
    }
    eps = fin.get("eps")
    fcff = fin.get("fcff")
    net_profit = fin.get("net_profit")
    total_shares = stock.get("total_shares_billion")

    if stock.get("is_bank"):
        # 银行: 用派息率 = 年度分红 / EPS (越低越安全)
        if eps and eps > 0:
            payout_ratio = stock["annual_div"] / eps * 100
            result["payout_ratio"] = round(payout_ratio, 1)
        else:
            result["payout_ratio"] = None
        result["coverage"] = None
    else:
        # 非银行: 用分红覆盖率(FCFF / 总分红)
        if fcff and total_shares:
            total_div = stock["annual_div"] * total_shares * 1e8  # 元
            coverage = fcff / total_div if total_div > 0 else None
            result["coverage"] = round(coverage, 2) if coverage else None
        else:
            result["coverage"] = None
        result["payout_ratio"] = None

    return result


# ============== 五因子击球评分 ==============
def calc_batting_score(dy, pe_pct, pb_pct, roe, safety_val, is_bank):
    """
    击球意愿 = 股息率(30%) + PE低估(15%) + PB低估(15%) + ROE(20%) + 安全性(20%)

    各因子 0-100 分:
    - 股息率: 甜蜜区 3-6%, 线性映射; >6% 打八折; >8% 封顶 80
    - PE/PB: 100 - 分位(越低越便宜)
    - ROE: 线性映射, 25% = 100分
    - 安全性(非银行): 分红覆盖率, 2x=100, 1x=50, <0.5x=0
    - 安全性(银行): 派息率, <30%=100, 30-50%=70, 50-70%=40, >70%=20
    """
    # 1. 股息率得分
    if dy is None or dy <= 0:
        div_score = 0
    elif dy <= 6:
        div_score = min(dy / 6.0 * 100, 100)
    elif dy <= 8:
        div_score = 100 - (dy - 6) * 10  # 6%=100, 7%=90, 8%=80
    else:
        div_score = max(80 - (dy - 8) * 10, 50)  # 递减，最低50

    # 2. PE 低估得分
    pe_score = max(0, 100 - pe_pct) if pe_pct is not None else 50

    # 3. PB 低估得分
    pb_score = max(0, 100 - pb_pct) if pb_pct is not None else 50

    # 4. ROE 得分
    if roe is not None and roe > 0:
        roe_score = min(roe / 25.0 * 100, 100)
    else:
        roe_score = 50

    # 5. 安全性得分
    if is_bank:
        pr = safety_val  # 派息率
        if pr is None:
            safety_score = 50
        elif pr < 30:
            safety_score = 100
        elif pr < 50:
            safety_score = 70
        elif pr < 70:
            safety_score = 40
        else:
            safety_score = 20
    else:
        cov = safety_val  # 分红覆盖率
        if cov is None:
            safety_score = 50
        elif cov >= 2:
            safety_score = 100
        elif cov >= 1.5:
            safety_score = 80
        elif cov >= 1:
            safety_score = 60
        elif cov >= 0.5:
            safety_score = 30
        else:
            safety_score = 10

    score = (div_score * 0.30 + pe_score * 0.15 + pb_score * 0.15 +
             roe_score * 0.20 + safety_score * 0.20)
    return round(min(score, 100), 1)


# ============== 卡片生成 ==============
def build_card(quotes):
    today = datetime.now().strftime("%Y-%m-%d")
    rows = []

    for s in STOCKS:
        q = quotes.get(s["code"])
        if not q:
            rows.append(f"- {s['name']}: 数据缺失")
            continue

        dy = round(s["annual_div"] / q["close"] * 100, 2) if q["close"] > 0 else 0
        chg = (q["close"] - q["prev_close"]) / q["prev_close"] * 100 if q["prev_close"] else 0

        vp = get_pe_pb(s["code"])
        pe_pct = vp.get("pe_pct", "-")
        pb_pct = vp.get("pb_pct", "-")

        fin = get_financials(s)
        roe = fin.get("roe")
        safety_val = fin.get("payout_ratio") if s.get("is_bank") else fin.get("coverage")
        safety_label = f"派息率 {fin['payout_ratio']}%" if s.get("is_bank") else f"覆盖 {fin.get('coverage', '-')}x"

        batting = calc_batting_score(dy, vp.get("pe_pct"), vp.get("pb_pct"), roe, safety_val, s.get("is_bank", False))

        rows.append(
            f"- {s['name']}: {q['close']:.2f} ({chg:+.2f}%) | "
            f"股息 {dy}% | PE分位 {pe_pct}% | PB分位 {pb_pct}% | "
            f"ROE {roe}% | {safety_label} | "
            f"击球 {batting}%"
        )

    content = f"""# 每日击球区日报 - {today}

## 关键指标

{chr(10).join(rows)}

## 说明

- 股息率 = 2025 年度全年分红(中期+末期) / 当前股价
- PE/PB 分位: 小乐财报历史百分位(越低越便宜)
- ROE: 2025 年报加权净资产收益率
- 安全性(非银行): 分红覆盖率 = 自由现金流(FCFF) / 总分红, >=2x安全, 1-2x基本安全, <1x需关注
- 安全性(银行): 派息率 = 分红 / EPS, <30%安全, 30-50%适中, >50%偏高
- 击球意愿: 股息率30% + PE低估15% + PB低估15% + ROE20% + 安全性20%

---

*数据来源: 新浪财经 / 小乐财报 / 东方财富 / 公司公告*
*仅供研究参考，不构成投资建议*"""

    summary_parts = []
    for s in STOCKS:
        q = quotes.get(s["code"])
        if q:
            dy = round(s["annual_div"] / q["close"] * 100, 2)
            summary_parts.append(f"{s['name']} {q['close']:.2f} 股息{dy}%")
    summary = " | ".join(summary_parts)

    return {
        "task_id": f"daily_batting_{today.replace('-', '')}",
        "task_name": f"每日击球区日报 - {today}",
        "task_result": summary,
        "task_content": content,
        "schedule_task_id": "daily_batting_zone",
        "auth_code": read_auth_code(),
    }


def read_auth_code():
    try:
        with open(r"C:\Users\And19\.openclaw\openclaw.json", "r", encoding="utf-8") as f:
            cfg = json.load(f)
        code = cfg.get("skills", {}).get("entries", {}).get("today-task", {}).get("config", {}).get("authCode")
        if code: return code
    except: pass
    return "MISSING"


def push_to_neg1(card):
    import subprocess, tempfile
    tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, encoding="utf-8")
    json.dump(card, tmp, ensure_ascii=False, indent=2)
    tmp.close()
    try:
        result = subprocess.run(
            ["python", PUSH_SCRIPT, "--data", tmp.name],
            capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60,
        )
        log.info(f"push result: {result.stdout[-300:]}")
        return result.returncode == 0
    finally:
        try: os.unlink(tmp.name)
        except: pass


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    today = date.today()
    if not is_workday(today) and not args.dry_run:
        log.info(f"{today} 非交易日，跳过")
        return 0

    log.info("Fetching quotes...")
    quotes = fetch_quotes()
    if not quotes:
        log.error("No quotes fetched")
        return 1

    log.info("Fetching PE/PB percentiles...")
    for s in STOCKS:
        vp = get_pe_pb(s["code"])
        log.info(f"{s['name']}: PE={vp.get('pe','-')} ({vp.get('pe_pct','-')}%), PB={vp.get('pb','-')} ({vp.get('pb_pct','-')}%)")

    log.info("Fetching financials (ROE/FCFF/payout)...")
    for s in STOCKS:
        fin = get_financials(s)
        if s.get("is_bank"):
            log.info(f"{s['name']}: ROE={fin.get('roe','-')}%, 派息率={fin.get('payout_ratio','-')}%")
        else:
            log.info(f"{s['name']}: ROE={fin.get('roe','-')}%, 覆盖率={fin.get('coverage','-')}x")

    card = build_card(quotes)
    log.info(f"Summary: {card['task_result']}")

    if args.dry_run:
        with open("daily_dryrun.json", "w", encoding="utf-8") as f:
            json.dump(card, f, ensure_ascii=False, indent=2)
        log.info("[DRY-RUN] saved")
        return 0

    ok = push_to_neg1(card)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
