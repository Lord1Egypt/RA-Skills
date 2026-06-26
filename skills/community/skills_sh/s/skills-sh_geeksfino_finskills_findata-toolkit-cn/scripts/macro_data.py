#!/usr/bin/env python3
"""
China Macro Economic Data Fetcher
====================================
Fetch A-share macro indicators using AKShare (no API key required).

Covers: LPR, CPI/PPI, GDP, PMI, social financing, money supply, northbound flow.

Usage:
    python macro_data.py --dashboard                  # All key indicators
    python macro_data.py --rates                      # Interest rates (LPR, MLF)
    python macro_data.py --inflation                  # CPI/PPI data
    python macro_data.py --pmi                        # PMI data
    python macro_data.py --social-financing            # Social financing
    python macro_data.py --cycle                      # Business cycle assessment
"""
import argparse
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common.utils import output_json, safe_float, error_exit


def _direction(values: list, lookback: int = 6) -> str:
    """Determine trend direction from a list of numeric values."""
    valid = [v for v in values if v is not None]
    if len(valid) < 2:
        return "insufficient_data"
    recent = valid[-lookback:]
    if len(recent) < 2:
        return "insufficient_data"
    change = (recent[-1] - recent[0]) / abs(recent[0]) if recent[0] != 0 else 0
    if change > 0.03:
        return "rising"
    elif change < -0.03:
        return "falling"
    return "stable"


# ---------------------------------------------------------------------------
# Interest Rates
# ---------------------------------------------------------------------------

def fetch_rates() -> dict:
    """Fetch Chinese interest rate data (LPR, MLF, etc.)."""
    import akshare as ak

    result = {}

    # LPR (Loan Prime Rate)
    try:
        df = ak.macro_china_lpr()
        if df is not None and not df.empty:
            recent = df.tail(12)
            lpr_1y = []
            lpr_5y = []
            for _, row in recent.iterrows():
                lpr_1y.append({
                    "date": str(row.get("TRADE_DATE", "")),
                    "value": safe_float(row.get("LPR1Y")),
                })
                lpr_5y.append({
                    "date": str(row.get("TRADE_DATE", "")),
                    "value": safe_float(row.get("LPR5Y")),
                })
            result["lpr_1y"] = {
                "latest": lpr_1y[-1]["value"] if lpr_1y else None,
                "direction": _direction([e["value"] for e in lpr_1y]),
                "series": lpr_1y,
            }
            result["lpr_5y"] = {
                "latest": lpr_5y[-1]["value"] if lpr_5y else None,
                "direction": _direction([e["value"] for e in lpr_5y]),
                "series": lpr_5y,
            }
    except Exception as e:
        result["lpr"] = {"error": str(e)}

    # Shibor
    try:
        df = ak.rate_interbank(market="上海银行间同业拆放利率(Shibor)", symbol="隔夜",
                               indicator="利率")
        if df is not None and not df.empty:
            recent = df.tail(30)
            records = []
            for _, row in recent.iterrows():
                records.append({
                    "date": str(row.iloc[0]) if len(row) > 0 else "",
                    "value": safe_float(row.iloc[1]) if len(row) > 1 else None,
                })
            result["shibor_overnight"] = {
                "latest": records[-1]["value"] if records else None,
                "direction": _direction([e["value"] for e in records]),
            }
    except Exception:
        result["shibor_overnight"] = {"note": "Data not available"}

    return result


# ---------------------------------------------------------------------------
# Inflation
# ---------------------------------------------------------------------------

def fetch_inflation() -> dict:
    """Fetch Chinese CPI and PPI data."""
    import akshare as ak

    result = {}

    # CPI
    try:
        df = ak.macro_china_cpi_monthly()
        if df is not None and not df.empty:
            # Columns: ['商品', '日期', '今值', '预测值', '前值']
            # Chronological order (oldest first), so .tail(12) is correct
            recent = df.tail(12)
            records = []
            for _, row in recent.iterrows():
                records.append({
                    "date": str(row.iloc[1]),
                    "cpi_yoy": safe_float(row.iloc[2]) if len(row) > 2 else None,
                })
            result["cpi"] = {
                "latest": records[-1]["cpi_yoy"] if records else None,
                "direction": _direction([e["cpi_yoy"] for e in records]),
                "series": records,
            }
    except Exception as e:
        result["cpi"] = {"error": str(e)}

    # PPI
    try:
        df = ak.macro_china_ppi()
        if df is not None and not df.empty:
            # Columns: ['月份', '当月', '当月同比增长', '累计']
            # Reverse chronological order (newest first)
            recent = df.head(12).iloc[::-1]  # take newest 12, reverse to ascending
            records = []
            for _, row in recent.iterrows():
                records.append({
                    "date": str(row.iloc[0]),
                    "ppi_yoy": safe_float(row.iloc[2]) if len(row) > 2 else None,
                })
            result["ppi"] = {
                "latest": records[-1]["ppi_yoy"] if records else None,
                "direction": _direction([e["ppi_yoy"] for e in records]),
                "series": records,
            }
    except Exception as e:
        result["ppi"] = {"error": str(e)}

    return result


# ---------------------------------------------------------------------------
# PMI
# ---------------------------------------------------------------------------

def fetch_pmi() -> dict:
    """Fetch China PMI data."""
    import akshare as ak

    result = {}

    try:
        df = ak.macro_china_pmi()
        if df is not None and not df.empty:
            # macro_china_pmi() returns reverse chronological order (newest first)
            recent = df.head(12).iloc[::-1]  # take newest 12, reverse to ascending
            records = []
            for _, row in recent.iterrows():
                records.append({
                    "date": str(row.iloc[0]),
                    "manufacturing_pmi": safe_float(row.iloc[1]) if len(row) > 1 else None,
                    "non_manufacturing_pmi": safe_float(row.iloc[3]) if len(row) > 3 else None,
                })
            mfg_values = [e["manufacturing_pmi"] for e in records]
            result["manufacturing_pmi"] = {
                "latest": records[-1]["manufacturing_pmi"] if records else None,
                "direction": _direction(mfg_values),
                "above_50": (records[-1]["manufacturing_pmi"] or 0) > 50 if records else None,
                "interpretation": (
                    "Above 50 — manufacturing expanding"
                    if records and (records[-1]["manufacturing_pmi"] or 0) > 50
                    else "Below 50 — manufacturing contracting"
                ),
                "series": records,
            }
    except Exception as e:
        result["manufacturing_pmi"] = {"error": str(e)}

    return result


# ---------------------------------------------------------------------------
# Social Financing
# ---------------------------------------------------------------------------

def fetch_social_financing() -> dict:
    """Fetch China social financing data (社会融资规模)."""
    import akshare as ak

    result = {}

    try:
        df = ak.macro_china_shrzgm()
        if df is not None and not df.empty:
            recent = df.tail(12)
            records = []
            for _, row in recent.iterrows():
                records.append({
                    "date": str(row.iloc[0]),
                    "value": safe_float(row.iloc[1]) if len(row) > 1 else None,
                })
            result["social_financing"] = {
                "latest": records[-1]["value"] if records else None,
                "direction": _direction([e["value"] for e in records]),
                "series": records,
                "interpretation": "Social financing growth indicates credit expansion/contraction",
            }
    except Exception as e:
        result["social_financing"] = {"error": str(e)}

    # Money supply M2
    try:
        df = ak.macro_china_money_supply()
        if df is not None and not df.empty:
            # Columns: ['月份', '货币和准货币(M2)-数量(亿元)', '货币和准货币(M2)-同比增长', ...]
            # Reverse chronological order (newest first)
            recent = df.head(12).iloc[::-1]  # take newest 12, reverse to ascending
            records = []
            for _, row in recent.iterrows():
                records.append({
                    "date": str(row.iloc[0]),
                    "m2_yoy": safe_float(row.iloc[2]) if len(row) > 2 else None,
                })
            result["m2_growth"] = {
                "latest": records[-1]["m2_yoy"] if records else None,
                "direction": _direction([e["m2_yoy"] for e in records]),
                "series": records,
            }
    except Exception as e:
        result["m2_growth"] = {"error": str(e)}

    return result


# ---------------------------------------------------------------------------
# Business Cycle Assessment (China)
# ---------------------------------------------------------------------------

def assess_business_cycle() -> dict:
    """
    Determine current China business cycle phase.
    Uses PMI, CPI, PPI, credit data, and policy signals.
    """
    inflation = fetch_inflation()
    pmi_data = fetch_pmi()
    financing = fetch_social_financing()

    signals = {}

    # PMI signal
    mfg_pmi = pmi_data.get("manufacturing_pmi", {})
    pmi_latest = mfg_pmi.get("latest")
    pmi_dir = mfg_pmi.get("direction", "stable")
    signals["pmi"] = {
        "value": pmi_latest,
        "direction": pmi_dir,
        "expanding": pmi_latest > 50 if pmi_latest else None,
    }

    # Inflation signals
    cpi_latest = inflation.get("cpi", {}).get("latest")
    ppi_latest = inflation.get("ppi", {}).get("latest")
    signals["cpi"] = {"value": cpi_latest, "direction": inflation.get("cpi", {}).get("direction")}
    signals["ppi"] = {"value": ppi_latest, "direction": inflation.get("ppi", {}).get("direction")}

    # Credit signal
    sf = financing.get("social_financing", {})
    sf_dir = sf.get("direction", "stable")
    m2 = financing.get("m2_growth", {})
    m2_dir = m2.get("direction", "stable")
    signals["credit"] = {"social_financing_direction": sf_dir, "m2_direction": m2_dir}

    # Phase determination
    pmi_expanding = pmi_latest and pmi_latest > 50
    pmi_rising = pmi_dir == "rising"
    credit_expanding = sf_dir == "rising" or m2_dir == "rising"

    if pmi_expanding and pmi_rising and credit_expanding:
        phase = "recovery"
        description = "经济复苏期：PMI回升，信用扩张，政策宽松"
        favored = ["消费", "科技", "金融"]
        disfavored = ["公用事业"]
    elif pmi_expanding and not pmi_rising:
        phase = "expansion"
        description = "经济扩张期：PMI维持高位，增长稳定"
        favored = ["制造业", "周期股", "金融"]
        disfavored = ["防御板块"]
    elif not pmi_expanding and ppi_latest and ppi_latest < 0:
        phase = "contraction"
        description = "经济收缩期：PMI低于50，PPI通缩"
        favored = ["消费防御", "公用事业", "高股息"]
        disfavored = ["周期股", "地产"]
    else:
        phase = "transition"
        description = "过渡期：经济信号混合"
        favored = ["均衡配置"]
        disfavored = []

    return {
        "phase": phase,
        "description": description,
        "signals": signals,
        "sector_implications": {
            "favored": favored,
            "disfavored": disfavored,
        },
        "factor_implications": {
            "recovery": "小盘、动量因子占优",
            "expansion": "质量、成长因子占优",
            "contraction": "低波动、红利因子占优",
            "transition": "均衡配置各因子",
        }.get(phase, ""),
    }


# ---------------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------------

def macro_dashboard() -> dict:
    """Comprehensive China macro dashboard."""
    return {
        "timestamp": datetime.now().isoformat(),
        "rates": fetch_rates(),
        "inflation": fetch_inflation(),
        "pmi": fetch_pmi(),
        "social_financing": fetch_social_financing(),
        "business_cycle": assess_business_cycle(),
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="China Macro Data Fetcher (AKShare, no API key)"
    )
    parser.add_argument("--dashboard", action="store_true", help="Full dashboard")
    parser.add_argument("--rates", action="store_true", help="Interest rates")
    parser.add_argument("--inflation", action="store_true", help="CPI/PPI")
    parser.add_argument("--pmi", action="store_true", help="PMI data")
    parser.add_argument("--social-financing", action="store_true",
                        help="Social financing + M2")
    parser.add_argument("--cycle", action="store_true",
                        help="Business cycle assessment")
    args = parser.parse_args()

    try:
        if args.rates:
            data = fetch_rates()
        elif args.inflation:
            data = fetch_inflation()
        elif args.pmi:
            data = fetch_pmi()
        elif args.social_financing:
            data = fetch_social_financing()
        elif args.cycle:
            data = assess_business_cycle()
        else:
            data = macro_dashboard()

        output_json(data)

    except ImportError:
        error_exit("akshare is required. Install: pip install akshare")
    except Exception as e:
        error_exit(f"Error: {e}")


if __name__ == "__main__":
    main()
