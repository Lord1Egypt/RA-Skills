#!/usr/bin/env python3
"""Evidence pack builder: parallel fetch, business analysis, and context generation."""

from __future__ import annotations

import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

import pandas as pd

from cninfo import validate_cninfo_date_range
from common import (
    _clean_nan,
    _num,
    _to_float,
    compact_records,
    dataframe_to_records,
)
from fetcher_core import StockDataFetcher
from retry import _is_retriable_error


def serialize_payload(payload: Any) -> Any:
    """Convert supported fetch results to JSON-serializable values."""
    if isinstance(payload, pd.DataFrame):
        return dataframe_to_records(payload)
    if isinstance(payload, dict) or payload is None:
        return payload
    return payload

def fetch_or_error(name: str, fetch_fn: Callable[[], Any]) -> Dict[str, Any]:
    """Fetch a dataset for evidence-pack and preserve per-dataset errors."""
    try:
        payload = serialize_payload(fetch_fn())
        return {"ok": True, "data": payload, "error": None, "error_type": None, "retriable": False}
    except Exception as exc:  # noqa: BLE001 - evidence packs should degrade per dataset.
        return {
            "ok": False,
            "data": [] if name != "company" else None,
            "error": str(exc),
            "error_type": type(exc).__name__,
            "retriable": _is_retriable_error(exc),
        }


def latest_records(dataset: Dict[str, Any], limit: int) -> List[Dict[str, Any]]:
    """Return bounded records from a packed dataset."""
    data = dataset.get("data") if isinstance(dataset, dict) else []
    if isinstance(data, list):
        return data[:limit]
    if isinstance(data, dict):
        return [data]
    return []


def _normalize_product_name(name: str) -> str:
    """Normalize product names to handle slight variations across periods."""
    if not name:
        return "其他"
    name = str(name).strip()
    # Merge common synonyms
    if name in ("服务费收入", "服务收入"):
        return "服务收入"
    return name


def _normalize_region_name(name: str) -> str:
    """Normalize region names and classify as domestic/overseas."""
    if not name:
        return "其他"
    name = str(name).strip()
    if name in ("国外", "海外", "港澳台地区及海外地区", "境外", "海外地区"):
        return "海外"
    if "大陆" in name or "境内" in name or "国内" in name:
        return "国内"
    return name


def _to_float(value: Any) -> Optional[float]:
    try:
        f = float(value)
        if pd.isna(f):
            return None
        return f
    except (TypeError, ValueError):
        return None


def _num(value: Any) -> Optional[float]:
    """Safely coerce a value to float, returning None on failure or NaN."""
    try:
        f = float(value)
    except (TypeError, ValueError):
        return None
    return round(f, 4) if f == f else None


def _clean_nan(obj: Any) -> Any:
    """Recursively replace NaN/inf/numpy types with native Python types for valid JSON."""
    # Handle numpy types first
    if hasattr(obj, "item"):  # numpy scalar
        obj = obj.item()
    if isinstance(obj, float):
        if pd.isna(obj) or obj != obj:  # NaN check
            return None
        if obj == float("inf") or obj == float("-inf"):
            return None
        return obj
    if isinstance(obj, dict):
        return {k: _clean_nan(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_clean_nan(v) for v in obj]
    return obj


def analyze_business_product(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze product structure changes: growth, share shift, margin trends.

    Returns a deterministic summary with no model judgement — just computed
    metrics that the model interprets according to SKILL.md.
    """
    if not rows:
        return {"ok": False, "error": "no_data", "periods": [], "products": []}

    # Build DataFrame
    df = pd.DataFrame(rows)
    required = {"end_date", "bz_item", "bz_sales", "bz_profit"}
    if not required.issubset(df.columns):
        return {"ok": False, "error": "missing_columns", "periods": [], "products": []}

    df["product"] = df["bz_item"].apply(_normalize_product_name)
    df["sales"] = df["bz_sales"].apply(_to_float)
    df["profit"] = df["bz_profit"].apply(_to_float)
    df["cost"] = df["bz_cost"].apply(_to_float) if "bz_cost" in df.columns else None

    # Deduplicate: aggregate sales/profit/cost by (period, normalized_product)
    agg_cols = {"sales": "sum", "profit": "sum"}
    if "cost" in df.columns and df["cost"].notna().any():
        agg_cols["cost"] = "sum"
    df = df.groupby(["end_date", "product"], as_index=False).agg(agg_cols)

    df["margin"] = df.apply(
        lambda r: round(r["profit"] / r["sales"] * 100, 2)
        if r["profit"] is not None and r["sales"] and r["sales"] > 0
        else None,
        axis=1,
    )

    # Group by period
    periods = sorted(df["end_date"].dropna().unique(), reverse=True)
    # Prefer annual (1231) for YoY, but keep all periods
    annual_periods = [p for p in periods if str(p).endswith("1231")]
    analysis_periods = annual_periods if len(annual_periods) >= 2 else periods

    # Per-period aggregates
    period_summary: List[Dict[str, Any]] = []
    product_periods: Dict[str, List[Dict[str, Any]]] = {}

    for period in analysis_periods:
        sub = df[df["end_date"] == period]
        total_sales = sub["sales"].sum()
        total_profit = sub["profit"].sum()
        total_margin = round(total_profit / total_sales * 100, 2) if total_sales and total_sales > 0 else None

        p_data = {
            "period": period,
            "total_sales": round(total_sales, 2) if total_sales else None,
            "total_profit": round(total_profit, 2) if total_profit else None,
            "total_margin_pct": total_margin,
            "product_count": sub["product"].nunique(),
            "products": [],
        }

        for _, row in sub.iterrows():
            prod = row["product"]
            sales = row["sales"]
            margin = row["margin"]
            share = round(sales / total_sales * 100, 2) if sales and total_sales and total_sales > 0 else None
            prod_entry = {
                "product": prod,
                "sales": round(sales, 2) if sales else None,
                "share_pct": share,
                "margin_pct": margin,
            }
            p_data["products"].append(prod_entry)
            product_periods.setdefault(prod, []).append({"period": period, "sales": sales, "share_pct": share, "margin_pct": margin})

        period_summary.append(p_data)

    # Cross-period analysis ( YoY growth, share shift, margin change )
    product_trends: List[Dict[str, Any]] = []
    for prod, history in product_periods.items():
        history = sorted(history, key=lambda x: x["period"], reverse=True)
        if len(history) < 2:
            continue
        latest = history[0]
        previous = history[1]
        sales_growth = None
        if latest["sales"] and previous["sales"] and previous["sales"] > 0:
            sales_growth = round((latest["sales"] - previous["sales"]) / previous["sales"] * 100, 2)
        share_change = None
        if latest["share_pct"] is not None and previous["share_pct"] is not None:
            share_change = round(latest["share_pct"] - previous["share_pct"], 2)
        margin_change = None
        if latest["margin_pct"] is not None and previous["margin_pct"] is not None:
            margin_change = round(latest["margin_pct"] - previous["margin_pct"], 2)

        product_trends.append({
            "product": prod,
            "latest_period": latest["period"],
            "previous_period": previous["period"],
            "sales_growth_yoy_pct": sales_growth,
            "share_change_pct_points": share_change,
            "margin_change_pct_points": margin_change,
            "latest_share_pct": latest["share_pct"],
            "latest_margin_pct": latest["margin_pct"],
        })

    # Rankings (deterministic only)
    def safe_sort(items, key, reverse=True):
        return sorted([i for i in items if i.get(key) is not None], key=lambda x: x[key], reverse=reverse)

    result = {
        "ok": True,
        "periods": period_summary,
        "product_trends": product_trends,
        "rankings": {
            "fastest_growth": safe_sort(product_trends, "sales_growth_yoy_pct")[:3],
            "slowest_growth": safe_sort(product_trends, "sales_growth_yoy_pct", reverse=False)[:3],
            "share_expanding": safe_sort(product_trends, "share_change_pct_points")[:3],
            "share_shrinking": safe_sort(product_trends, "share_change_pct_points", reverse=False)[:3],
            "margin_improving": safe_sort(product_trends, "margin_change_pct_points")[:3],
            "margin_deteriorating": safe_sort(product_trends, "margin_change_pct_points", reverse=False)[:3],
        },
        "model_responsibility": (
            "以上均为确定性计算：收入增速、占比变化、毛利率变化。"
            "判断'主力产品线是否切换'、'毛利率改善是否来自结构升级'等结论由模型完成。"
        ),
    }
    return _clean_nan(result)


def analyze_business_region(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze regional structure: domestic/overseas split, globalization trend.

    Returns deterministic metrics for model interpretation.
    """
    if not rows:
        return {"ok": False, "error": "no_data", "periods": [], "regions": []}

    df = pd.DataFrame(rows)
    required = {"end_date", "bz_item", "bz_sales", "bz_profit"}
    if not required.issubset(df.columns):
        return {"ok": False, "error": "missing_columns", "periods": [], "regions": []}

    df["region"] = df["bz_item"].apply(_normalize_region_name)
    df["sales"] = df["bz_sales"].apply(_to_float)
    df["profit"] = df["bz_profit"].apply(_to_float)

    # Deduplicate: aggregate by (period, normalized_region)
    df = df.groupby(["end_date", "region"], as_index=False).agg({"sales": "sum", "profit": "sum"})

    df["margin"] = df.apply(
        lambda r: round(r["profit"] / r["sales"] * 100, 2)
        if r["profit"] is not None and r["sales"] and r["sales"] > 0
        else None,
        axis=1,
    )

    periods = sorted(df["end_date"].dropna().unique(), reverse=True)
    annual_periods = [p for p in periods if str(p).endswith("1231")]
    analysis_periods = annual_periods if len(annual_periods) >= 2 else periods

    period_summary: List[Dict[str, Any]] = []
    region_periods: Dict[str, List[Dict[str, Any]]] = {}

    for period in analysis_periods:
        sub = df[df["end_date"] == period]
        total_sales = sub["sales"].sum()
        total_profit = sub["profit"].sum()
        total_margin = round(total_profit / total_sales * 100, 2) if total_sales and total_sales > 0 else None

        # Domestic vs overseas split
        domestic_sales = sub[sub["region"] == "国内"]["sales"].sum()
        overseas_sales = sub[sub["region"] == "海外"]["sales"].sum()
        other_sales = total_sales - domestic_sales - overseas_sales if total_sales else 0

        domestic_margin = None
        overseas_margin = None
        domestic_sub = sub[sub["region"] == "国内"]
        overseas_sub = sub[sub["region"] == "海外"]
        if not domestic_sub.empty:
            ds = domestic_sub["sales"].sum()
            dp = domestic_sub["profit"].sum()
            domestic_margin = round(dp / ds * 100, 2) if ds and ds > 0 else None
        if not overseas_sub.empty:
            os_ = overseas_sub["sales"].sum()
            op = overseas_sub["profit"].sum()
            overseas_margin = round(op / os_ * 100, 2) if os_ and os_ > 0 else None

        p_data = {
            "period": period,
            "total_sales": round(total_sales, 2) if total_sales else None,
            "total_margin_pct": total_margin,
            "domestic": {
                "sales": round(domestic_sales, 2) if domestic_sales else None,
                "share_pct": round(domestic_sales / total_sales * 100, 2) if domestic_sales and total_sales and total_sales > 0 else None,
                "margin_pct": domestic_margin,
            },
            "overseas": {
                "sales": round(overseas_sales, 2) if overseas_sales else None,
                "share_pct": round(overseas_sales / total_sales * 100, 2) if overseas_sales and total_sales and total_sales > 0 else None,
                "margin_pct": overseas_margin,
            },
            "other_sales": round(other_sales, 2) if other_sales else None,
            "regions": [],
        }

        for _, row in sub.iterrows():
            region = row["region"]
            sales = row["sales"]
            share = round(sales / total_sales * 100, 2) if sales and total_sales and total_sales > 0 else None
            p_data["regions"].append({
                "region": region,
                "sales": round(sales, 2) if sales else None,
                "share_pct": share,
                "margin_pct": row["margin"],
            })
            region_periods.setdefault(region, []).append({
                "period": period, "sales": sales, "share_pct": share, "margin_pct": row["margin"],
            })

        period_summary.append(p_data)

    # Cross-period trends
    region_trends: List[Dict[str, Any]] = []
    for region, history in region_periods.items():
        history = sorted(history, key=lambda x: x["period"], reverse=True)
        if len(history) < 2:
            continue
        latest = history[0]
        previous = history[1]
        sales_growth = None
        if latest["sales"] and previous["sales"] and previous["sales"] > 0:
            sales_growth = round((latest["sales"] - previous["sales"]) / previous["sales"] * 100, 2)
        share_change = None
        if latest["share_pct"] is not None and previous["share_pct"] is not None:
            share_change = round(latest["share_pct"] - previous["share_pct"], 2)
        margin_change = None
        if latest["margin_pct"] is not None and previous["margin_pct"] is not None:
            margin_change = round(latest["margin_pct"] - previous["margin_pct"], 2)

        region_trends.append({
            "region": region,
            "latest_period": latest["period"],
            "previous_period": previous["period"],
            "sales_growth_yoy_pct": sales_growth,
            "share_change_pct_points": share_change,
            "margin_change_pct_points": margin_change,
            "latest_share_pct": latest["share_pct"],
            "latest_margin_pct": latest["margin_pct"],
        })

    # Overseas trend summary
    overseas_trend = None
    domestic_trend = None
    for t in region_trends:
        if t["region"] == "海外":
            overseas_trend = t
        if t["region"] == "国内":
            domestic_trend = t

    result = {
        "ok": True,
        "periods": period_summary,
        "region_trends": region_trends,
        "globalization_summary": {
            "overseas_share_trend": overseas_trend["share_change_pct_points"] if overseas_trend else None,
            "overseas_growth_vs_domestic": (
                round(overseas_trend["sales_growth_yoy_pct"] - domestic_trend["sales_growth_yoy_pct"], 2)
                if overseas_trend and domestic_trend
                and overseas_trend.get("sales_growth_yoy_pct") is not None
                and domestic_trend.get("sales_growth_yoy_pct") is not None
                else None
            ),
            "overseas_margin_vs_domestic": (
                round(overseas_trend["latest_margin_pct"] - domestic_trend["latest_margin_pct"], 2)
                if overseas_trend and domestic_trend
                and overseas_trend.get("latest_margin_pct") is not None
                and domestic_trend.get("latest_margin_pct") is not None
                else None
            ),
        },
        "model_responsibility": (
            "以上均为确定性计算：地区收入占比、海外vs国内增速差、毛利率差。"
            "判断'出海逻辑是否成立'、'汇率风险敞口'等结论由模型完成。"
        ),
    }
    return _clean_nan(result)


def build_analysis_context(evidence: Dict[str, Any]) -> Dict[str, Any]:
    """Build compact model context from the full evidence pack."""
    datasets = evidence.get("datasets", {})
    company_data = (datasets.get("company") or {}).get("data") or {}
    announcements = ((datasets.get("announcements") or {}).get("data") or {}).get("announcements", [])
    original_text_candidates = [
        {
            "announcement_time": item.get("announcement_time"),
            "title": item.get("title"),
            "subcategory": item.get("subcategory"),
            "tags": item.get("tags"),
            "adjunct_url": item.get("adjunct_url"),
            "reason": "标题命中高信息密度事件，默认应进一步读取 PDF 原文。",
        }
        for item in announcements
        if item.get("needs_original_text")
    ][:5]

    research_fields = [
        "ts_code",
        "name",
        "trade_date",
        "surv_date",
        "fund_visitors",
        "rece_place",
        "rece_mode",
        "invest_org",
        "org_type",
        "comp_rece",
        "content",
    ]

    return {
        "metadata": {
            **(evidence.get("metadata") or {}),
            "context_generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "source": "data_fetcher.build_analysis_context",
        },
        "company": company_data,
        "financial_snapshot": {
            "financial": latest_records(datasets.get("financial", {}), 8),
            "income": latest_records(datasets.get("income", {}), 8),
            "balance": latest_records(datasets.get("balance", {}), 8),
            "cashflow": latest_records(datasets.get("cashflow", {}), 8),
        },
        "valuation_market": {
            "daily_basic_latest": latest_records(datasets.get("daily-basic", {}), 5),
            "daily_latest": latest_records(datasets.get("daily", {}), 5),
            "valuation_band": (datasets.get("valuation-band") or {}).get("data"),
        },
        "business_structure": {
            "product_raw": latest_records(datasets.get("main-business-product", {}), 20),
            "product_analysis": analyze_business_product(latest_records(datasets.get("main-business-product", {}), 40)),
            "region_raw": latest_records(datasets.get("main-business-region", {}), 20),
            "region_analysis": analyze_business_region(latest_records(datasets.get("main-business-region", {}), 40)),
        },
        "governance": {
            "top10_holders": latest_records(datasets.get("top10-holders", {}), 40),
            "managers": latest_records(datasets.get("managers", {}), 20),
            "rewards": latest_records(datasets.get("rewards", {}), 20),
            "holder_number": latest_records(datasets.get("holder-number", {}), 20),
            "holder_trade": latest_records(datasets.get("holder-trade", {}), 30),
            "share_float": latest_records(datasets.get("share-float", {}), 20),
            "block_trade": latest_records(datasets.get("block-trade", {}), 30),
        },
        "announcements": {
            "summary": {
                "count": len(announcements),
                "original_text_candidate_count": len(original_text_candidates),
            },
            "recent": compact_records(
                announcements,
                [
                    "announcement_time",
                    "sec_name",
                    "sec_code",
                    "title",
                    "subcategory",
                    "tags",
                    "needs_original_text",
                    "adjunct_url",
                ],
                20,
            ),
            "original_text_candidates": original_text_candidates,
        },
        "reports": {
            "recent": compact_records(
                latest_records(datasets.get("report-list", {}), 8),
                [
                    "announcement_time",
                    "sec_name",
                    "sec_code",
                    "title",
                    "report_type",
                    "report_type_label",
                    "report_year",
                    "is_full_report",
                    "adjunct_url",
                ],
                8,
            )
        },
        "institutional_research": {
            "recent": compact_records(
                latest_records(datasets.get("institutional-research", {}), 30),
                research_fields,
                30,
            ),
            "model_responsibility": "机构调研频率、机构类型和问题关键词只验证市场关注度与主线连接，不等同于业绩改善。",
        },
        "dataset_errors": {
            name: payload.get("error")
            for name, payload in datasets.items()
            if isinstance(payload, dict) and not payload.get("ok")
        },
    }


def build_module_contexts_from_context(context: Dict[str, Any]) -> Dict[str, Any]:
    """Split compact context into subagent-friendly modules."""
    metadata = context.get("metadata", {})
    return {
        "meta": {
            "metadata": metadata,
            "subagent_contract": {
                "module1_growth_financial": ["module1_growth_financial.json", "SKILL.md 第四节纲要 + references/qualitative_framework.md", "成长与财务质量"],
                "module2_valuation_market": ["module2_valuation_market.json", "SKILL.md 第五节纲要 + references/quantitative_framework.md（先 5.1 分型，再 5.2 估值快照/分位带）", "估值与市场定价"],
                "module3_governance": ["module3_governance.json", "SKILL.md 第六节", "股东与治理"],
                "module4_announcements": ["module4_announcements.json", "SKILL.md 公告与原文升级规则", "公告事件验证"],
                "module5_research_mainline": ["module5_research_mainline.json", "SKILL.md 主线归属 + 机构调研方法", "机构调研与主线验证"],
            },
        },
        "module1_growth_financial": {
            "metadata": metadata,
            "company": context.get("company"),
            "financial_snapshot": context.get("financial_snapshot"),
            "business_structure": context.get("business_structure"),
        },
        "module2_valuation_market": {
            "metadata": metadata,
            "valuation_market": context.get("valuation_market"),
            "financial_snapshot": context.get("financial_snapshot"),
        },
        "module3_governance": {
            "metadata": metadata,
            "governance": context.get("governance"),
        },
        "module4_announcements": {
            "metadata": metadata,
            "announcements": context.get("announcements"),
            "reports": context.get("reports"),
        },
        "module5_research_mainline": {
            "metadata": metadata,
            "institutional_research": context.get("institutional_research"),
            "valuation_market": context.get("valuation_market"),
            "announcements": {
                "original_text_candidates": (context.get("announcements") or {}).get("original_text_candidates"),
            },
        },
    }


def build_evidence_pack(fetcher: StockDataFetcher, args: argparse.Namespace) -> Dict[str, Any]:
    """Build full single-stock evidence plus compact/module contexts."""
    ts_code = fetcher.resolve_ts_code(args.query)
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    announcement_date = validate_cninfo_date_range(args.date)

    jobs: Dict[str, Callable[[], Any]] = {
        "company": lambda: fetcher.get_company(ts_code),
        "financial": lambda: fetcher.get_financial_indicators(ts_code, args.financial_limit),
        "income": lambda: fetcher.get_income(ts_code, args.financial_limit),
        "balance": lambda: fetcher.get_balance(ts_code, args.financial_limit),
        "cashflow": lambda: fetcher.get_cashflow(ts_code, args.financial_limit),
        "daily": lambda: fetcher.get_daily(ts_code, args.market_limit),
        "daily-basic": lambda: fetcher.get_daily_basic(ts_code, args.market_limit),
        "valuation-band": lambda: fetcher.get_valuation_band(ts_code, years=args.band_years),
        "main-business-product": lambda: fetcher.get_main_business(ts_code, "P", args.business_limit),
        "main-business-region": lambda: fetcher.get_main_business(ts_code, "D", args.business_limit),
        "top10-holders": lambda: fetcher.get_top10_holders(ts_code, args.holder_periods),
        "managers": lambda: fetcher.get_managers(ts_code),
        "rewards": lambda: fetcher.get_rewards(ts_code),
        "holder-number": lambda: fetcher.get_holder_number(ts_code, args.holder_limit),
        "holder-trade": lambda: fetcher.get_holder_trade(ts_code, limit=args.holder_limit),
        "share-float": lambda: fetcher.get_share_float(ts_code, limit=args.holder_limit),
        "block-trade": lambda: fetcher.get_block_trade(ts_code, limit=args.holder_limit),
        "report-list": lambda: fetcher.get_report_announcements(
            ts_code,
            report_type=args.report_type,
            report_year=args.report_year,
            limit=args.report_limit,
            include_variants=args.include_report_variants,
            timeout=args.timeout,
        ),
        "announcements": lambda: fetcher.get_announcements(
            ts_code,
            tab_type=args.tabtype,
            date_range=announcement_date,
            searchkey=args.searchkey,
            category=args.category,
            trade=args.trade,
            page_num=args.page_num,
            page_size=args.page_size,
            limit=args.announcement_limit,
            include_excluded=args.include_excluded,
            timeout=args.timeout,
        ),
        "institutional-research": lambda: fetcher.get_institutional_research(
            ts_code,
            start_date=args.start_date,
            end_date=args.end_date,
            trade_date=args.trade_date,
            limit=args.research_limit,
        ),
    }

    max_workers = getattr(args, "max_workers", 4)
    datasets: Dict[str, Dict[str, Any]] = {}
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        future_map = {
            pool.submit(fetch_or_error, name, fn): name
            for name, fn in jobs.items()
        }
        for future in as_completed(future_map):
            name = future_map[future]
            datasets[name] = future.result()

    evidence = {
        "metadata": {
            "type": "stock_ai_analyzer_evidence_pack",
            "ts_code": ts_code,
            "query": args.query,
            "generated_at": generated_at,
            "announcement_date": announcement_date,
            "source": "data_fetcher.build_evidence_pack",
        },
        "datasets": datasets,
    }
    # Compute analysis_context once, then derive module_contexts from it
    analysis_context = build_analysis_context(evidence)
    return {
        "evidence": evidence,
        "analysis_context": analysis_context,
        "module_contexts": build_module_contexts_from_context(analysis_context),
    }


def write_json_file(path: str, payload: Any) -> str:
    """Write JSON to a path and return the resolved path."""
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    return str(output_path.resolve())


def write_pack_outputs(package: Dict[str, Any], args: argparse.Namespace) -> Optional[Dict[str, Any]]:
    """Write requested pack artifacts and return a manifest, if any files are written."""
    manifest: Dict[str, Any] = {}
    if args.evidence_out:
        manifest["evidence"] = write_json_file(args.evidence_out, package["evidence"])
    if args.context_out:
        manifest["analysis_context"] = write_json_file(args.context_out, package["analysis_context"])
    if args.module_context_dir:
        module_dir = Path(args.module_context_dir)
        module_dir.mkdir(parents=True, exist_ok=True)
        module_paths: Dict[str, str] = {}
        for name, payload in package["module_contexts"].items():
            path = module_dir / f"{name}.json"
            path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
            module_paths[name] = str(path.resolve())
        manifest["module_context_dir"] = str(module_dir.resolve())
        manifest["module_contexts"] = module_paths
    if not manifest:
        return None
    manifest["ts_code"] = package["evidence"].get("metadata", {}).get("ts_code")
    return manifest
