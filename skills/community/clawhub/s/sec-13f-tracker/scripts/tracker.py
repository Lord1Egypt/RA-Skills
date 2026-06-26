#!/usr/bin/env python3
"""
SEC 13F 大佬持仓追踪器
从 SEC EDGAR 抓取知名基金的 13F 持仓数据，解析并生成中文报告
"""
from __future__ import annotations

import json
import os
import sys
import time
import xml.etree.ElementTree as ET
from datetime import datetime, date
from pathlib import Path
from collections import defaultdict

# Clear proxy env vars that may interfere with direct connections
for _proxy_var in ["ALL_PROXY", "all_proxy", "HTTPS_PROXY", "https_proxy", "HTTP_PROXY", "http_proxy"]:
    os.environ.pop(_proxy_var, None)

import requests

# === 配置 ===
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = BASE_DIR / "reports"

EDGAR_BASE = "https://efts.sec.gov/LATEST/search-index"
EDGAR_FILINGS = "https://www.sec.gov/cgi-bin/browse-edgar"
EDGAR_FULL_TEXT = "https://efts.sec.gov/LATEST/search-index"

# SEC EDGAR API endpoints
SUBMISSIONS_URL = "https://data.sec.gov/submissions/CIK{cik}.json"
FILING_INDEX_URL = "https://www.sec.gov/Archives/edgar/data/{cik_int}/{accession}/"

USER_AGENT = "OpenClaw Research Tool research@openclaw.com"

HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept-Encoding": "gzip, deflate",
}

# 追踪的基金
FUNDS = {
    "0001067983": {"name": "Berkshire Hathaway", "manager": "Warren Buffett"},
    "0001350694": {"name": "Bridgewater Associates", "manager": "Ray Dalio"},
    "0001336528": {"name": "Pershing Square", "manager": "Bill Ackman"},
    "0001029160": {"name": "Soros Fund Management", "manager": "George Soros"},
    "0001697748": {"name": "ARK Invest", "manager": "Cathie Wood"},
}

# XML namespaces for 13F
NS_13F = {
    "ns": "http://www.sec.gov/document/thirteenf-2024q1",  # will be detected dynamically
}


def rate_limit():
    """SEC EDGAR rate limit: max 10 req/sec"""
    time.sleep(0.15)


def get_submissions(cik: str) -> dict:
    """获取 CIK 的所有提交记录"""
    url = SUBMISSIONS_URL.format(cik=cik)
    rate_limit()
    resp = requests.get(url, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    return resp.json()


def find_13f_filings(submissions: dict, limit: int = 2) -> list:
    """从提交记录中找到最近的 13F-HR 文件"""
    recent = submissions.get("filings", {}).get("recent", {})
    forms = recent.get("form", [])
    accessions = recent.get("accessionNumber", [])
    dates = recent.get("filingDate", [])
    primary_docs = recent.get("primaryDocument", [])
    report_dates = recent.get("reportDate", [])

    filings = []
    for i, form in enumerate(forms):
        if form in ("13F-HR", "13F-HR/A"):
            filings.append({
                "form": form,
                "accession": accessions[i],
                "filing_date": dates[i],
                "primary_doc": primary_docs[i] if i < len(primary_docs) else "",
                "report_date": report_dates[i] if i < len(report_dates) else "",
            })
            if len(filings) >= limit:
                break
    return filings


def find_infotable_url(cik: str, accession: str) -> str:
    """通过 filing index.json 找到 information table XML 文件的 URL"""
    cik_int = str(int(cik))
    acc_clean = accession.replace("-", "")
    base_url = f"https://www.sec.gov/Archives/edgar/data/{cik_int}/{acc_clean}/"

    # Use JSON index for reliable file discovery
    index_url = base_url + "index.json"
    rate_limit()
    resp = requests.get(index_url, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    items = data.get("directory", {}).get("item", [])
    xml_files = [item["name"] for item in items if item["name"].endswith(".xml")]

    # Priority: infotable.xml > any XML that's not primary_doc.xml
    for name in xml_files:
        lower = name.lower()
        if "infotable" in lower or "information" in lower:
            return base_url + name

    for name in xml_files:
        lower = name.lower()
        if "primary" not in lower and "cover" not in lower and "index" not in lower:
            return base_url + name

    return None


def parse_13f_xml(xml_text: str) -> list:
    """解析 13F information table XML"""
    holdings = []
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        print("  [WARN] XML parse error, trying to clean up...")
        # Sometimes there's junk before the XML
        idx = xml_text.find("<?xml")
        if idx > 0:
            xml_text = xml_text[idx:]
        root = ET.fromstring(xml_text)

    # Detect namespace
    tag = root.tag
    ns = ""
    if "{" in tag:
        ns = tag.split("}")[0] + "}"

    # Find all infoTable entries
    for entry in root.iter():
        if entry.tag.endswith("infoTable"):
            holding = {}
            for child in entry:
                local_tag = child.tag.split("}")[-1] if "}" in child.tag else child.tag

                if local_tag == "nameOfIssuer":
                    holding["name"] = child.text.strip() if child.text else ""
                elif local_tag == "titleOfClass":
                    holding["class"] = child.text.strip() if child.text else ""
                elif local_tag == "cusip":
                    holding["cusip"] = child.text.strip() if child.text else ""
                elif local_tag == "value":
                    holding["value"] = int(child.text.strip()) if child.text else 0  # in dollars (new XML schema)
                elif local_tag == "sshPrnamt":
                    holding["shares"] = int(child.text.strip()) if child.text else 0
                elif local_tag == "sshPrnamtType":
                    holding["share_type"] = child.text.strip() if child.text else "SH"
                elif local_tag == "putCall":
                    holding["put_call"] = child.text.strip() if child.text else ""
                elif local_tag == "investmentDiscretion":
                    holding["discretion"] = child.text.strip() if child.text else ""
                elif local_tag == "shrsOrPrnAmt":
                    for sub in child:
                        sub_tag = sub.tag.split("}")[-1] if "}" in sub.tag else sub.tag
                        if sub_tag == "sshPrnamt":
                            holding["shares"] = int(sub.text.strip()) if sub.text else 0
                        elif sub_tag == "sshPrnamtType":
                            holding["share_type"] = sub.text.strip() if sub.text else "SH"

            if holding.get("name"):
                holdings.append(holding)

    return holdings


def fetch_13f_holdings(cik: str, filing: dict) -> list:
    """获取并解析一个 13F filing 的持仓数据"""
    # Find infotable XML via index.json
    infotable_url = find_infotable_url(cik, filing["accession"])
    if not infotable_url:
        print(f"  [WARN] Could not find infotable XML for {filing['accession']}")
        return []

    print(f"  Fetching infotable: {infotable_url}")
    rate_limit()
    resp = requests.get(infotable_url, headers=HEADERS, timeout=60)
    resp.raise_for_status()

    holdings = parse_13f_xml(resp.text)
    print(f"  Parsed {len(holdings)} holdings")
    return holdings


def holdings_to_dict(holdings: list) -> dict:
    """将持仓列表转换为以 CUSIP 为 key 的字典，合并同 CUSIP 的持仓"""
    result = {}
    for h in holdings:
        cusip = h.get("cusip", "")
        key = cusip
        if h.get("put_call"):
            key = f"{cusip}_{h['put_call']}"

        if key in result:
            result[key]["value"] += h.get("value", 0)
            result[key]["shares"] += h.get("shares", 0)
        else:
            result[key] = {
                "name": h.get("name", ""),
                "cusip": cusip,
                "class": h.get("class", ""),
                "value": h.get("value", 0),
                "shares": h.get("shares", 0),
                "share_type": h.get("share_type", "SH"),
                "put_call": h.get("put_call", ""),
            }
    return result


def compare_holdings(current: dict, previous: dict) -> dict:
    """对比两期持仓，返回变化"""
    changes = {
        "new": [],       # 新建仓
        "increased": [], # 加仓
        "decreased": [], # 减仓
        "closed": [],    # 清仓
        "unchanged": [], # 不变
    }

    all_keys = set(list(current.keys()) + list(previous.keys()))

    for key in all_keys:
        curr = current.get(key)
        prev = previous.get(key)

        if curr and not prev:
            changes["new"].append({
                **curr,
                "change_pct": None,
                "share_change": curr["shares"],
            })
        elif prev and not curr:
            changes["closed"].append({
                **prev,
                "change_pct": -100,
                "share_change": -prev["shares"],
            })
        elif curr and prev:
            if curr["shares"] == prev["shares"]:
                changes["unchanged"].append(curr)
            else:
                pct = ((curr["shares"] - prev["shares"]) / prev["shares"] * 100) if prev["shares"] > 0 else 0
                entry = {
                    **curr,
                    "prev_shares": prev["shares"],
                    "prev_value": prev["value"],
                    "change_pct": round(pct, 1),
                    "share_change": curr["shares"] - prev["shares"],
                }
                if pct > 0:
                    changes["increased"].append(entry)
                else:
                    changes["decreased"].append(entry)

    # Sort by value (largest first)
    for cat in changes:
        changes[cat].sort(key=lambda x: x.get("value", 0), reverse=True)

    return changes


def format_value(val_dollars: int) -> str:
    """格式化市值（输入单位：美元）"""
    val = val_dollars
    if val >= 1e12:
        return f"${val/1e12:.1f}T"
    elif val >= 1e9:
        return f"${val/1e9:.1f}B"
    elif val >= 1e6:
        return f"${val/1e6:.1f}M"
    else:
        return f"${val:,.0f}"


def format_shares(shares: int) -> str:
    """格式化股数"""
    if shares >= 1e6:
        return f"{shares/1e6:.1f}M"
    elif shares >= 1e3:
        return f"{shares/1e3:.1f}K"
    return str(shares)


def report_date_to_quarter(report_date: str) -> str:
    """将报告日期转换为季度表示"""
    if not report_date:
        return "Unknown"
    try:
        d = datetime.strptime(report_date, "%Y-%m-%d")
        q = (d.month - 1) // 3 + 1
        return f"{d.year}-Q{q}"
    except ValueError:
        return report_date


def generate_report(all_fund_data: list) -> str:
    """生成 Markdown 报告"""
    today = date.today().strftime("%Y-%m-%d")
    lines = [f"# 🏦 13F 大佬持仓追踪 - {today}\n"]
    lines.append(f"> 数据来源：SEC EDGAR | 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}\n")

    # Track cross-fund holdings for insights
    all_new = defaultdict(list)
    all_increased = defaultdict(list)
    all_closed = defaultdict(list)

    for fund_data in all_fund_data:
        info = fund_data["info"]
        current_filing = fund_data.get("current_filing", {})
        changes = fund_data.get("changes")
        current_holdings = fund_data.get("current_holdings", {})
        error = fund_data.get("error")

        lines.append(f"\n---\n")
        lines.append(f"## {info['manager']} ({info['name']})\n")

        if error:
            lines.append(f"⚠️ 数据获取失败：{error}\n")
            continue

        quarter = report_date_to_quarter(current_filing.get("report_date", ""))
        filing_date = current_filing.get("filing_date", "Unknown")
        total_value = sum(h.get("value", 0) for h in current_holdings.values())
        num_holdings = len(current_holdings)

        lines.append(f"- **报告期**：{quarter}")
        lines.append(f"- **提交日期**：{filing_date}")
        lines.append(f"- **总持仓市值**：{format_value(total_value)}")
        lines.append(f"- **持仓数量**：{num_holdings} 只\n")

        if not changes:
            lines.append("_（无上季度数据可对比）_\n")
            # Show top 10 holdings
            lines.append("### 前 10 大持仓\n")
            lines.append("| 排名 | 股票 | 市值 | 股数 |")
            lines.append("|------|------|------|------|")
            sorted_h = sorted(current_holdings.values(), key=lambda x: x["value"], reverse=True)
            for i, h in enumerate(sorted_h[:10], 1):
                pc = f" ({h['put_call']})" if h.get("put_call") else ""
                lines.append(f"| {i} | {h['name']}{pc} | {format_value(h['value'])} | {format_shares(h['shares'])} |")
            lines.append("")
            continue

        # New positions
        if changes["new"]:
            lines.append(f"### 🆕 新建仓 ({len(changes['new'])} 只)\n")
            lines.append("| 股票 | 市值 | 股数 |")
            lines.append("|------|------|------|")
            for h in changes["new"][:15]:
                pc = f" ({h['put_call']})" if h.get("put_call") else ""
                lines.append(f"| {h['name']}{pc} | {format_value(h['value'])} | {format_shares(h['shares'])} |")
                if info["manager"] not in all_new[h["name"]]:
                    all_new[h["name"]].append(info["manager"])
            if len(changes["new"]) > 15:
                lines.append(f"| ... 及其他 {len(changes['new'])-15} 只 | | |")
            lines.append("")

        # Increased positions
        if changes["increased"]:
            lines.append(f"### 📈 加仓 ({len(changes['increased'])} 只)\n")
            lines.append("| 股票 | 市值 | 变化 |")
            lines.append("|------|------|------|")
            for h in changes["increased"][:15]:
                pc = f" ({h['put_call']})" if h.get("put_call") else ""
                lines.append(f"| {h['name']}{pc} | {format_value(h['value'])} | +{h['change_pct']}% |")
                if info["manager"] not in all_increased[h["name"]]:
                    all_increased[h["name"]].append(info["manager"])
            if len(changes["increased"]) > 15:
                lines.append(f"| ... 及其他 {len(changes['increased'])-15} 只 | | |")
            lines.append("")

        # Decreased positions
        if changes["decreased"]:
            lines.append(f"### 📉 减仓 ({len(changes['decreased'])} 只)\n")
            lines.append("| 股票 | 市值 | 变化 |")
            lines.append("|------|------|------|")
            for h in changes["decreased"][:15]:
                pc = f" ({h['put_call']})" if h.get("put_call") else ""
                lines.append(f"| {h['name']}{pc} | {format_value(h['value'])} | {h['change_pct']}% |")
            if len(changes["decreased"]) > 15:
                lines.append(f"| ... 及其他 {len(changes['decreased'])-15} 只 | | |")
            lines.append("")

        # Closed positions
        if changes["closed"]:
            lines.append(f"### 🚫 清仓 ({len(changes['closed'])} 只)\n")
            lines.append("| 股票 | 上期市值 | 上期股数 |")
            lines.append("|------|----------|----------|")
            for h in changes["closed"][:15]:
                pc = f" ({h['put_call']})" if h.get("put_call") else ""
                lines.append(f"| {h['name']}{pc} | {format_value(h['value'])} | {format_shares(h['shares'])} |")
                if info["manager"] not in all_closed[h["name"]]:
                    all_closed[h["name"]].append(info["manager"])
            if len(changes["closed"]) > 15:
                lines.append(f"| ... 及其他 {len(changes['closed'])-15} 只 | | |")
            lines.append("")

        # Summary
        lines.append(f"**变动概要**：新建仓 {len(changes['new'])} | 加仓 {len(changes['increased'])} | 减仓 {len(changes['decreased'])} | 清仓 {len(changes['closed'])} | 不变 {len(changes['unchanged'])}\n")

    # === 关键洞察 ===
    lines.append("\n---\n")
    lines.append("## 💡 关键洞察\n")

    # Multi-fund convergence
    multi_new = {k: v for k, v in all_new.items() if len(v) >= 2}
    multi_inc = {k: v for k, v in all_increased.items() if len(v) >= 2}
    multi_closed = {k: v for k, v in all_closed.items() if len(v) >= 2}

    if multi_new or multi_inc:
        lines.append("### 🎯 多个大佬同时看好\n")
        for name, managers in {**multi_new, **multi_inc}.items():
            action = "新建仓" if name in multi_new else "加仓"
            lines.append(f"- **{name}**：{', '.join(managers)} 同时{action}")
        lines.append("")

    if multi_closed:
        lines.append("### ⚠️ 多个大佬同时退出\n")
        for name, managers in multi_closed.items():
            lines.append(f"- **{name}**：{', '.join(managers)} 同时清仓")
        lines.append("")

    if not multi_new and not multi_inc and not multi_closed:
        lines.append("- 本期各大佬操作分化，无明显共识标的\n")

    lines.append("\n---\n")
    lines.append(f"_报告自动生成 by SEC 13F Tracker | {datetime.now().strftime('%Y-%m-%d %H:%M')}_\n")

    return "\n".join(lines)


def process_fund(cik: str, info: dict) -> dict:
    """处理单个基金的完整流程"""
    print(f"\n{'='*60}")
    print(f"Processing: {info['manager']} ({info['name']}) - CIK: {cik}")
    print(f"{'='*60}")

    result = {"cik": cik, "info": info}

    try:
        # 1. Get submissions
        print("  Fetching submissions...")
        submissions = get_submissions(cik)

        # 2. Find 13F filings (latest 2)
        filings = find_13f_filings(submissions, limit=2)
        if not filings:
            result["error"] = "No 13F filings found"
            return result

        print(f"  Found {len(filings)} recent 13F filings:")
        for f in filings:
            print(f"    - {f['form']} filed {f['filing_date']} (report date: {f['report_date']})")

        # 3. Fetch current quarter holdings
        current_filing = filings[0]
        result["current_filing"] = current_filing
        print(f"\n  Fetching current quarter ({current_filing['report_date']})...")
        current_raw = fetch_13f_holdings(cik, current_filing)
        current_holdings = holdings_to_dict(current_raw)
        result["current_holdings"] = current_holdings

        # Save current data
        save_path = DATA_DIR / f"{cik}_{current_filing['report_date']}.json"
        with open(save_path, "w") as f:
            json.dump({
                "cik": cik,
                "info": info,
                "filing": current_filing,
                "holdings": current_holdings,
                "fetched_at": datetime.now().isoformat(),
            }, f, indent=2)
        print(f"  Saved to {save_path}")

        # 4. Fetch previous quarter for comparison
        if len(filings) >= 2:
            prev_filing = filings[1]
            print(f"\n  Fetching previous quarter ({prev_filing['report_date']})...")

            # Check if we already have this data
            prev_path = DATA_DIR / f"{cik}_{prev_filing['report_date']}.json"
            if prev_path.exists():
                print(f"  Using cached data from {prev_path}")
                with open(prev_path) as f:
                    prev_data = json.load(f)
                prev_holdings = prev_data["holdings"]
            else:
                prev_raw = fetch_13f_holdings(cik, prev_filing)
                prev_holdings = holdings_to_dict(prev_raw)
                with open(prev_path, "w") as f:
                    json.dump({
                        "cik": cik,
                        "info": info,
                        "filing": prev_filing,
                        "holdings": prev_holdings,
                        "fetched_at": datetime.now().isoformat(),
                    }, f, indent=2)

            # 5. Compare
            print("  Comparing quarters...")
            changes = compare_holdings(current_holdings, prev_holdings)
            result["changes"] = changes
            print(f"  New: {len(changes['new'])}, Increased: {len(changes['increased'])}, "
                  f"Decreased: {len(changes['decreased'])}, Closed: {len(changes['closed'])}, "
                  f"Unchanged: {len(changes['unchanged'])}")
        else:
            result["changes"] = None

    except Exception as e:
        result["error"] = str(e)
        import traceback
        traceback.print_exc()

    return result


def main():
    print("=" * 60)
    print("  SEC 13F 大佬持仓追踪器")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)

    # Process all funds
    all_results = []
    for cik, info in FUNDS.items():
        result = process_fund(cik, info)
        all_results.append(result)
        time.sleep(1)  # Extra delay between funds

    # Generate report
    print("\n\n" + "=" * 60)
    print("  Generating report...")
    print("=" * 60)

    report = generate_report(all_results)

    # Save report
    report_filename = f"13f-report-{date.today().strftime('%Y-%m-%d')}.md"
    report_path = REPORTS_DIR / report_filename
    with open(report_path, "w") as f:
        f.write(report)
    print(f"\n  Report saved to: {report_path}")

    # Also save as latest
    latest_path = REPORTS_DIR / "latest.md"
    with open(latest_path, "w") as f:
        f.write(report)
    print(f"  Also saved as: {latest_path}")

    # Print summary
    print("\n" + "=" * 60)
    print("  DONE!")
    print("=" * 60)

    return report_path


if __name__ == "__main__":
    main()
