#!/usr/bin/env python3
"""
SEC Finance - 从 SEC XBRL 获取全面的财务数据并生成 PDF 报表

功能:
- 资产负债表数据
- 利润表数据
- 现金流量表数据
- 每股指标
- PDF 报表生成
"""

import argparse
import json
import os
import re
import ssl
import sys
import textwrap
import time
import urllib.parse
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Any

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)
XBRL_BASE = "https://data.sec.gov/api/xbrl"
EDGAR_BASE = "https://www.sec.gov/cgi-bin/browse-edgar"
ISSUERS_FILE = Path(__file__).resolve().parent.parent / "references" / "issuers.json"

# ============ 财务指标定义 (中英文双语) ============
BALANCE_SHEET_CONCEPTS = {
    "Total Assets": ["Assets"],
    "Current Assets": ["AssetsCurrent"],
    "Non-current Assets": ["AssetsNoncurrent"],
    "Cash & Equivalents": ["CashAndCashEquivalentsAtCarryingValue", "CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents"],
    "Accounts Receivable": ["AccountsReceivableNetCurrent"],
    "Inventory": ["InventoryNet", "Inventory"],
    "Property & Equipment": ["PropertyPlantAndEquipmentNet"],
    "Goodwill": ["Goodwill"],
    "Total Liabilities": ["Liabilities"],
    "Current Liabilities": ["LiabilitiesCurrent"],
    "Non-current Liabilities": ["LiabilitiesNoncurrent"],
    "Accounts Payable": ["AccountsPayableCurrent"],
    "Short-term Debt": ["ShortTermBorrowings"],
    "Long-term Debt": ["LongTermDebt", "LongTermDebtNoncurrent"],
    "Shareholders Equity": ["StockholdersEquity", "StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest"],
    "Retained Earnings": ["RetainedEarningsAccumulatedDeficit"],
}

INCOME_STATEMENT_CONCEPTS = {
    "Revenue": ["RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues", "SalesRevenueNet"],
    "Cost of Revenue": ["CostOfGoodsAndServicesSold", "CostOfRevenue", "CostOfGoodsSold"],
    "Gross Profit": ["GrossProfit"],
    "R&D Expense": ["ResearchAndDevelopmentExpense"],
    "SG&A Expense": ["SellingGeneralAndAdministrativeExpense"],
    "Operating Income": ["OperatingIncomeLoss"],
    "Interest Expense": ["InterestExpense"],
    "Pre-tax Income": ["IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest"],
    "Income Tax": ["IncomeTaxExpenseBenefit"],
    "Net Income": ["NetIncomeLossAvailableToCommonStockholdersBasic", "NetIncomeLoss", "ProfitLoss"],
}

CASH_FLOW_CONCEPTS = {
    "Operating Cash Flow": ["NetCashProvidedByUsedInOperatingActivities"],
    "Investing Cash Flow": ["NetCashProvidedByUsedInInvestingActivities"],
    "Financing Cash Flow": ["NetCashProvidedByUsedInFinancingActivities"],
    "CapEx": ["PaymentsToAcquirePropertyPlantAndEquipment"],
    "Acquisitions": ["PaymentsToAcquireBusinessesNetOfCashAcquired"],
}

PER_SHARE_CONCEPTS = {
    "Basic EPS": ["EarningsPerShareBasic"],
    "Diluted EPS": ["EarningsPerShareDiluted"],
    "Dividend/Share": ["CommonStockDividendsPerShareCashPaid"],
}


def load_issuers() -> list:
    if not ISSUERS_FILE.exists():
        return []
    return json.loads(ISSUERS_FILE.read_text())


ISSUERS = load_issuers()
ALIAS_MAP = {}
for issuer in ISSUERS:
    for alias in issuer.get("aliases", []):
        ALIAS_MAP[alias.lower()] = issuer
    if issuer.get("name"):
        ALIAS_MAP[issuer["name"].lower()] = issuer
    if issuer.get("ticker"):
        ALIAS_MAP[issuer["ticker"].lower()] = issuer


def _secure_ctx() -> ssl.SSLContext:
    return ssl.create_default_context()


def _fallback_insecure_ctx() -> ssl.SSLContext:
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx


def _get_json(url: str, timeout: int = 20, retries: int = 2) -> dict:
    parsed = urllib.parse.urlparse(url)
    last_error = None
    for attempt in range(retries + 1):
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": USER_AGENT,
                "Accept": "application/json",
                "Host": parsed.netloc,
            },
        )
        for ctx_factory in (_secure_ctx, _fallback_insecure_ctx):
            try:
                with urllib.request.urlopen(req, timeout=timeout, context=ctx_factory()) as resp:
                    return json.loads(resp.read())
            except ssl.SSLError as e:
                last_error = e
                continue
            except urllib.error.HTTPError as e:
                if e.code == 429 and attempt < retries:
                    time.sleep(3 * (attempt + 1))
                    last_error = e
                    break
                if e.code == 404:
                    raise ValueError(f"CIK or resource not found: {url}") from e
                raise ValueError(f"HTTP {e.code} fetching {url}: {e.reason}") from e
            except urllib.error.URLError as e:
                last_error = e
                continue
        if attempt < retries:
            time.sleep(1.5 ** attempt)
    raise ConnectionError(f"Network/SSL error fetching {url}: {last_error}")


def _get_text(url: str, timeout: int = 20) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    last_error = None
    for ctx_factory in (_secure_ctx, _fallback_insecure_ctx):
        try:
            with urllib.request.urlopen(req, timeout=timeout, context=ctx_factory()) as resp:
                return resp.read().decode("utf-8", errors="replace")
        except Exception as e:
            last_error = e
    raise ConnectionError(f"Failed to fetch {url}: {last_error}")


def cik_from_name(company_name: str) -> Optional[dict]:
    key = company_name.strip().lower()
    if key in ALIAS_MAP and ALIAS_MAP[key].get("cik"):
        issuer = ALIAS_MAP[key]
        return {
            "name": issuer["name"],
            "cik": issuer["cik"],
            "ticker": issuer.get("ticker"),
            "exchange": issuer.get("exchange"),
        }

    encoded = urllib.parse.quote(company_name)
    url = f"{EDGAR_BASE}?action=getcompany&company={encoded}&owner=include&count=10"
    html = _get_text(url, timeout=15)
    ciks = list(dict.fromkeys(re.findall(r"CIK=(\d+)", html)))
    if not ciks:
        raise ValueError(f"No SEC results found for company: {company_name}")
    cik = ciks[0].zfill(10)
    name_match = re.search(r"companyName>([^<]+)<", html)
    name = name_match.group(1).strip() if name_match else company_name
    return {"name": name, "cik": cik}


def fetch_company_facts(cik: str) -> dict:
    return _get_json(f"{XBRL_BASE}/companyfacts/CIK{cik.zfill(10)}.json")


def _extract_metric(facts: dict, concept_list: List[str], period_type: str = "annual") -> List[Dict]:
    """提取指定指标的数据"""
    results = []
    
    for concept in concept_list:
        concept_data = facts.get(concept)
        if not concept_data:
            continue
        
        units = concept_data.get("units", {})
        if not units:
            continue
        
        # 选择货币单位
        currency_order = ["CNY", "USD", "HKD"]
        currency = None
        for c in currency_order:
            if c in units:
                currency = c
                break
        if not currency:
            currency = next(iter(units.keys()), None)
        if not currency:
            continue
        
        for entry in units[currency]:
            form = entry.get("form", "").upper()
            
            # 判断是年报还是季报
            is_annual = any(x in form for x in ("20-F", "10-K", "40-F"))
            is_quarterly = any(x in form for x in ("10-Q", "6-K"))
            
            if period_type == "annual" and not is_annual:
                continue
            if period_type == "quarterly" and not is_quarterly:
                continue
            
            results.append({
                "end": entry.get("end", ""),
                "start": entry.get("start", ""),
                "val": entry.get("val"),
                "form": entry.get("form", ""),
                "filed": entry.get("filed", ""),
                "currency": currency,
                "concept": concept,
            })
        
        if results:
            break  # 找到数据就停止
    
    # 按日期排序，去重，显示最新的数据
    seen = set()
    unique = []
    for r in sorted(results, key=lambda x: x["end"], reverse=True):
        end_date = r.get("end", "")
        if end_date and end_date not in seen:
            seen.add(end_date)
            unique.append(r)
    
    return unique[:5]  # 最多返回5条（最近的数据）


def fetch_comprehensive_financials(cik: str, period: str = "annual") -> Dict:
    """获取全面的财务数据"""
    facts = fetch_company_facts(cik)
    us_gaap = facts.get("facts", {}).get("us-gaap", {})
    ifrs = facts.get("facts", {}).get("ifrs-full", {})
    
    # 合并数据源，优先 IFRS
    all_facts = {**us_gaap, **ifrs}
    
    result = {
        "cik": cik.zfill(10),
        "company_name": facts.get("entityName", ""),
        "data_updated": facts.get("lastModified", ""),
        "period_type": period,
        "balance_sheet": {},
        "income_statement": {},
        "cash_flow": {},
        "per_share": {},
    }
    
    # 提取资产负债表
    for name, concepts in BALANCE_SHEET_CONCEPTS.items():
        data = _extract_metric(all_facts, concepts, period)
        if data:
            result["balance_sheet"][name] = data
    
    # 提取利润表
    for name, concepts in INCOME_STATEMENT_CONCEPTS.items():
        data = _extract_metric(all_facts, concepts, period)
        if data:
            result["income_statement"][name] = data
    
    # 提取现金流量表
    for name, concepts in CASH_FLOW_CONCEPTS.items():
        data = _extract_metric(all_facts, concepts, period)
        if data:
            result["cash_flow"][name] = data
    
    # 提取每股指标
    for name, concepts in PER_SHARE_CONCEPTS.items():
        data = _extract_metric(all_facts, concepts, period)
        if data:
            result["per_share"][name] = data
    
    return result


def _fmt_money(val, currency: str = "CNY") -> str:
    """格式化金额"""
    symbols = {"CNY": "¥", "USD": "$", "HKD": "HK$"}
    symbol = symbols.get(currency, currency + " ")
    
    if val is None:
        return "N/A"
    if not isinstance(val, (int, float)):
        return str(val)
    
    abs_val = abs(val)
    sign = "-" if val < 0 else ""
    
    if abs_val >= 1_000_000_000:
        return f"{sign}{symbol}{abs_val / 1_000_000_000:.2f}B"
    if abs_val >= 1_000_000:
        return f"{sign}{symbol}{abs_val / 1_000_000:.2f}M"
    return f"{sign}{symbol}{val:,.0f}"


def format_comprehensive_table(data: Dict) -> str:
    """格式化为表格输出"""
    lines = []
    width = 90
    
    lines.append(f"\n{'═' * width}")
    lines.append(f"  {data.get('company_name', 'N/A')}  |  CIK: {data.get('cik')}  |  {data.get('period_type', '').upper()}")
    lines.append(f"{'═' * width}")
    
    def print_section(title: str, section_data: Dict):
        if not section_data:
            return
        lines.append(f"\n  【{title}】")
        lines.append(f"  {'─' * 80}")
        
        # 获取所有日期
        all_dates = set()
        for metric_data in section_data.values():
            for item in metric_data:
                all_dates.add(item.get("end", ""))
        
        dates = sorted(all_dates, reverse=True)[:5]
        
        # 打印表头
        header = f"  {'指标':<20}"
        for d in dates:
            header += f" {d[-7:]:>12}"
        lines.append(header)
        lines.append(f"  {'─' * 80}")
        
        # 打印每个指标
        for metric_name, metric_data in section_data.items():
            row = f"  {metric_name:<20}"
            date_map = {item["end"]: item for item in metric_data}
            for d in dates:
                if d in date_map:
                    val = date_map[d].get("val")
                    currency = date_map[d].get("currency", "CNY")
                    row += f" {_fmt_money(val, currency):>12}"
                else:
                    row += f" {'N/A':>12}"
            lines.append(row)
    
    print_section("资产负债表", data.get("balance_sheet", {}))
    print_section("利润表", data.get("income_statement", {}))
    print_section("现金流量表", data.get("cash_flow", {}))
    print_section("每股指标", data.get("per_share", {}))
    
    lines.append(f"\n{'═' * width}")
    lines.append(f"  数据来源: SEC EDGAR XBRL  |  更新时间: {data.get('data_updated', 'N/A')}")
    
    return "\n".join(lines)


def generate_pdf_report(data: Dict, output_path: str) -> str:
    """生成 PDF 财务报表"""
    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import mm
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
    except ImportError:
        raise ImportError("需要安装 reportlab: pip3 install reportlab --break-system-packages")
    
    # 尝试注册中文字体
    chinese_font = 'Helvetica'
    font_paths = [
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
        "/System/Library/Fonts/PingFang.ttc",
    ]
    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                pdfmetrics.registerFont(TTFont('ChineseFont', font_path, subfontIndex=0))
                chinese_font = 'ChineseFont'
                break
            except Exception:
                continue
    
    doc = SimpleDocTemplate(output_path, pagesize=A4, topMargin=20*mm, bottomMargin=20*mm)
    elements = []
    styles = getSampleStyleSheet()
    
    # 自定义样式
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontName=chinese_font,
        fontSize=18,
        spaceAfter=10,
        alignment=1,
    )
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontName=chinese_font,
        fontSize=10,
        textColor=colors.grey,
        alignment=1,
    )
    section_style = ParagraphStyle(
        'SectionTitle',
        parent=styles['Heading2'],
        fontName=chinese_font,
        fontSize=14,
        spaceBefore=15,
        spaceAfter=8,
    )
    
    # 标题
    company_name = data.get('company_name', 'Unknown')
    elements.append(Paragraph(f"{company_name}", title_style))
    elements.append(Paragraph(
        f"Financial Report | CIK: {data.get('cik')} | Period: {data.get('period_type', 'annual').upper()}",
        subtitle_style
    ))
    elements.append(Spacer(1, 10*mm))
    
    def create_table(title: str, section_data: Dict):
        if not section_data:
            return
        
        elements.append(Paragraph(title, section_style))
        
        # 获取日期
        all_dates = set()
        for metric_data in section_data.values():
            for item in metric_data:
                all_dates.add(item.get("end", ""))
        dates = sorted(all_dates, reverse=True)[:4]
        
        if not dates:
            return
        
        # 构建表格数据
        table_data = [["Metric"] + [d[-7:] for d in dates]]
        
        for metric_name, metric_data in section_data.items():
            row = [metric_name]
            date_map = {item["end"]: item for item in metric_data}
            for d in dates:
                if d in date_map:
                    val = date_map[d].get("val")
                    currency = date_map[d].get("currency", "CNY")
                    row.append(_fmt_money(val, currency))
                else:
                    row.append("N/A")
            table_data.append(row)
        
        table = Table(table_data, repeatRows=1)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2C3E50')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (0, 1), (0, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), chinese_font),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('TOPPADDING', (0, 0), (-1, 0), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#ECF0F1')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#ECF0F1')]),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        elements.append(table)
        elements.append(Spacer(1, 5*mm))
    
    create_table("Balance Sheet", data.get("balance_sheet", {}))
    create_table("Income Statement", data.get("income_statement", {}))
    create_table("Cash Flow Statement", data.get("cash_flow", {}))
    create_table("Per Share Data", data.get("per_share", {}))
    
    # 页脚
    elements.append(Spacer(1, 10*mm))
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontName=chinese_font,
        fontSize=8,
        textColor=colors.grey,
        alignment=1,
    )
    elements.append(Paragraph(
        f"Data Source: SEC EDGAR XBRL | Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')} | Data Updated: {data.get('data_updated', 'N/A')}",
        footer_style
    ))
    
    doc.build(elements)
    return output_path


def main():
    parser = argparse.ArgumentParser(
        description="Fetch comprehensive financial data from SEC XBRL and generate PDF reports.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""
            Examples:
              python3 sec_finance.py --search JD.com
              python3 sec_finance.py --search Alibaba --period annual
              python3 sec_finance.py --search JD.com --pdf report.pdf
              python3 sec_finance.py --cik 0001549802 --output json
        """),
    )
    parser.add_argument("--search", type=str, help="Company name, ticker, or alias")
    parser.add_argument("--cik", type=str, help="10-digit CIK")
    parser.add_argument("--period", choices=["quarterly", "annual", "all"], default="annual")
    parser.add_argument("--output", choices=["json", "table"], default="table")
    parser.add_argument("--pdf", type=str, help="Generate PDF report to specified path")
    parser.add_argument("--limit", type=int, default=8)
    args = parser.parse_args()

    try:
        cik = None
        company_info = None
        
        if args.search:
            company_info = cik_from_name(args.search)
            print(f"\n✅ Found: {company_info['name']}")
            print(f"   CIK:      {company_info['cik']}")
            print(f"   Ticker:   {company_info.get('ticker', 'N/A')}")
            print(f"   Exchange: {company_info.get('exchange', 'N/A')}")
            print("\n   Fetching comprehensive financials...\n")
            cik = company_info["cik"]
        elif args.cik:
            cik = args.cik.strip().zfill(10)
        else:
            parser.print_help()
            print("\n\nBuilt-in issuers with validated CIKs:")
            for issuer in ISSUERS:
                if issuer.get("cik"):
                    print(f"  {issuer['name']:<22} {issuer['cik']}  {issuer.get('ticker','')}")
            return
        
        data = fetch_comprehensive_financials(cik, period=args.period)
        
        if args.pdf:
            pdf_path = generate_pdf_report(data, args.pdf)
            print(f"✅ PDF report generated: {pdf_path}")
        elif args.output == "json":
            print(json.dumps(data, indent=2, ensure_ascii=False))
        else:
            print(format_comprehensive_table(data))
            
    except ValueError as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)
    except ConnectionError as e:
        print(f"🌐 {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
