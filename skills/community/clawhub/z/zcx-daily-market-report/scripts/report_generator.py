#!/usr/bin/env python3
"""
Daily Market Report Generator for Chinese Futures

Provides:
- fetch_all_quotes()         — Bulk fetch major contracts from Sina
- calc_sector_averages()     — Aggregate sector-level data
- rank_by_change()           — Top gainers/losers
- detect_anomalies()         — Spot unusual moves
- generate_markdown_report() — Build full report
- export_pdf()               — Convert markdown to PDF (needs pandoc/weasyprint)
"""

import json
import time
import subprocess
from datetime import datetime
from pathlib import Path

# Sector definitions
SECTORS = {
    "金融股指": ["IF", "IC", "IH", "IM"],
    "贵金属": ["AU", "AG"],
    "有色金属": ["CU", "AL", "ZN", "PB", "NI", "SN"],
    "黑色系": ["I", "RB", "HC", "J", "JM"],
    "能源化工": ["SC", "LU", "MA", "TA", "SA", "EG", "PP", "L"],
    "农产品": ["C", "M", "Y", "P", "SR", "CF", "RM", "OI"],
    "航运": ["EC"],
}

CONTRACT_MULTIPLIERS = {
    "IF": 300, "IC": 200, "IH": 300, "IM": 200,
    "AU": 1000, "AG": 15, "CU": 5, "AL": 5,
    "I": 100, "RB": 10, "HC": 10, "J": 100, "JM": 60,
    "SC": 1000, "MA": 10, "TA": 5, "SA": 20,
    "C": 10, "M": 10, "Y": 10, "P": 10,
    "SR": 10, "CF": 5, "EC": 50,
}

def fetch_all_quotes(contracts=None):
    """Bulk fetch quotes via Sina Finance API.
    Returns dict of {prefix: {price, open, high, low, prev_close, volume, oi}}
    """
    if contracts is None:
        contracts = [prefix for sector in SECTORS.values() for prefix in sector]
    
    codes = ",".join(f"{c}0" for c in contracts)
    url = f"https://hq.sinajs.cn/list={codes}"
    
    # Use subprocess to call curl
    try:
        result = subprocess.run(
            ["curl", "-s", "-e", "https://finance.sina.com.cn", url],
            capture_output=True, text=True, timeout=10
        )
        data = {}
        for line in result.stdout.strip().split("\n"):
            if not line.strip():
                continue
            # Parse format: var hq_str_PREFIX0="name,...,"
            try:
                prefix = line.split("hq_str_")[1].split("0=")[0]
                fields = line.split('"')[1].split(",")
                if len(fields) >= 14:
                    data[prefix] = {
                        "name": fields[0],
                        "timestamp": fields[1] if len(fields) > 1 else "",
                        "prev_close": float(fields[2]),
                        "open": float(fields[3]),
                        "current": float(fields[4]),
                        "high": float(fields[5]),
                        "low": float(fields[6]),
                        "volume": int(fields[12]) if fields[12] else 0,
                        "oi": int(fields[13]) if fields[13] else 0,
                    }
            except (IndexError, ValueError):
                continue
        return data
    except subprocess.TimeoutExpired:
        print("[ERROR] Fetch timeout")
        return {}

def calc_sector_averages(data):
    """Calculate sector-level aggregates"""
    sector_data = {}
    for sector, prefixes in SECTORS.items():
        prices = []
        changes = []
        for p in prefixes:
            if p in data:
                d = data[p]
                if d["prev_close"] > 0:
                    change = (d["current"] - d["prev_close"]) / d["prev_close"] * 100
                    changes.append(change)
                    prices.append(d["current"])
        if changes:
            sector_data[sector] = {
                "avg_change": sum(changes) / len(changes),
                "advance": sum(1 for c in changes if c > 0),
                "decline": sum(1 for c in changes if c < 0),
            }
    return sector_data

def rank_by_change(data, top_n=5):
    """Returns top gainers and top losers"""
    items = [(p, d) for p, d in data.items() if d["prev_close"] > 0]
    for p, d in items:
        d["change_pct"] = (d["current"] - d["prev_close"]) / d["prev_close"] * 100
    
    sorted_items = sorted(items, key=lambda x: x[1]["change_pct"], reverse=True)
    gainers = [(p, d) for p, d in sorted_items[:top_n] if d["change_pct"] > 0]
    losers = [(p, d) for p, d in sorted_items[-top_n:] if d["change_pct"] < 0]
    losers.reverse()
    return gainers, losers

def generate_markdown_report(data, date_str=None):
    """Generate the full daily report markdown"""
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")
    
    gainers, losers = rank_by_change(data)
    sectors = calc_sector_averages(data)
    
    report = f"""---
# 中国期货市场每日行情报告
## {date_str}
"""

    # ... template building would go here
    
    return report

def export_pdf(markdown_path, pdf_path=None):
    """Convert markdown report to PDF"""
    if pdf_path is None:
        pdf_path = Path(markdown_path).with_suffix(".pdf")
    
    # Try pandoc
    try:
        subprocess.run(["pandoc", str(markdown_path), "-o", str(pdf_path), "--pdf-engine=wkhtmltopdf"], 
                      check=True, capture_output=True)
        print(f"[OK] PDF generated: {pdf_path}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    
    # Fallback: try weasyprint
    try:
        from weasyprint import HTML
        with open(markdown_path, "r", encoding="utf-8") as f:
            html = f"<html><body><pre>{f.read()}</pre></body></html>"
        HTML(string=html).write_pdf(str(pdf_path))
        print(f"[OK] PDF generated (weasyprint): {pdf_path}")
        return True
    except ImportError:
        print("[WARN] Neither pandoc nor weasyprint available. Report saved as markdown only.")
        return False

if __name__ == "__main__":
    print("Fetching quotes...")
    quotes = fetch_all_quotes()
    if quotes:
        gainers, losers = rank_by_change(quotes)
        print(f"\n📈 Gainers: {[p for p,_ in gainers]}")
        print(f"📉 Losers:  {[p for p,_ in losers]}")
