#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fetch.py
基于 AKShare 抓取 A 股公开数据

数据源策略：
  优先使用东方财富接口（数据最全）
  若连接被拒（常见于境外 VPS），自动切换新浪财经接口并给出明确提示
  如两者均失败，对应模块返回空数据，不影响其他模块运行
"""

import logging
import os
from datetime import datetime, timedelta
from pathlib import Path

import yaml

try:
    from pypinyin import lazy_pinyin, Style
    _PINYIN_AVAILABLE = True
except ImportError:
    _PINYIN_AVAILABLE = False

try:
    import akshare as ak
    import pandas as pd
except ImportError:
    raise ImportError("请先安装依赖：pip install akshare pandas")


# ============================================================
# 代理配置（从 config.yaml 读取）
# ============================================================
def _setup_proxy():
    config_path = Path(__file__).parent / "config.yaml"
    if not config_path.exists():
        return
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f) or {}
        proxy = cfg.get("proxy", "")
        if proxy:
            os.environ["HTTP_PROXY"] = proxy
            os.environ["HTTPS_PROXY"] = proxy
            logging.info(f"🌐 已启用代理：{proxy}")
    except Exception:
        pass

_setup_proxy()


# ============================================================
# 工具函数
# ============================================================
def _is_connection_error(e: Exception) -> bool:
    msg = str(e).lower()
    return any(k in msg for k in [
        "connection aborted", "remote end closed", "connection refused",
        "connectionerror", "timeout", "remotedisconnected"
    ])


def _warn_em_blocked(module_name: str):
    logging.warning(
        f"⚠️  [{module_name}] 东方财富接口连接失败。\n"
        f"   可能原因：您的 IP 被东方财富限制访问（境外服务器常见）。\n"
        f"   解决方案：在 config.yaml 中配置 proxy 代理，或在境内机器运行。\n"
        f"   当前已自动切换至新浪财经备用接口，部分字段可能缺失。"
    )


# ============================================================
# 股票代码标准化
# ============================================================
def normalize_code(raw: str) -> dict:
    raw = raw.strip()
    code = raw.upper().replace(".SH", "").replace(".SZ", "").replace(".BJ", "")
    code = code.replace("SH", "").replace("SZ", "").replace("BJ", "")
    code = "".join(filter(str.isdigit, code))

    if len(code) != 6:
        return search_by_name(raw)

    market = _detect_market(code)
    full = f"{code}.{market.upper()}"
    name = _get_stock_name(code)
    return {"code": code, "market": market, "full": full, "name": name}


def _detect_market(code: str) -> str:
    if code.startswith(("6", "500", "510", "511", "512", "513", "515", "518")):
        return "sh"
    elif code.startswith(("4", "8", "9")):
        return "bj"
    else:
        return "sz"


def _get_stock_name(code: str) -> str:
    try:
        info = ak.stock_individual_info_em(symbol=code)
        row = info[info["item"] == "股票简称"]
        if not row.empty:
            return row["value"].values[0]
    except Exception as e:
        if _is_connection_error(e):
            _warn_em_blocked("股票名称查询")
        try:
            df = ak.stock_info_a_code_name()
            row = df[df["code"] == code]
            if not row.empty:
                return row["name"].values[0]
        except Exception:
            pass
    return code


def _name_to_pinyin_abbr(name: str) -> str:
    """贵州茅台 → gzmt"""
    if not _PINYIN_AVAILABLE:
        return ""
    return "".join(lazy_pinyin(name, style=Style.FIRST_LETTER))


def _name_to_full_pinyin(name: str) -> str:
    """贵州茅台 → guizhoumaotai"""
    if not _PINYIN_AVAILABLE:
        return ""
    return "".join(lazy_pinyin(name))


def search_by_name(name: str) -> dict:
    """
    支持三种输入：
      - 中文全名或部分名：茅台、贵州茅台
      - 拼音缩写：gzmt
      - 全拼：guizhoumaotai
    """
    try:
        df = ak.stock_info_a_code_name()
        query = name.strip().lower()

        # 1. 优先中文匹配
        matched = df[df["name"].str.contains(query, na=False)]

        # 2. 中文未命中，尝试拼音匹配
        if matched.empty and _PINYIN_AVAILABLE:
            abbr_col = df["name"].apply(_name_to_pinyin_abbr)
            full_col = df["name"].apply(_name_to_full_pinyin)
            matched = df[abbr_col.str.lower() == query]          # 缩写精确匹配
            if matched.empty:
                matched = df[full_col.str.lower() == query]      # 全拼精确匹配
            if matched.empty:
                matched = df[abbr_col.str.lower().str.startswith(query)]  # 缩写前缀
            if matched.empty:
                matched = df[full_col.str.lower().str.contains(query)]    # 全拼模糊

        if matched.empty:
            raise ValueError(
                f"找不到股票：{name}\n"
                f"支持：中文名（茅台）、拼音缩写（gzmt）、全拼（guizhoumaotai）、6位代码（600519）"
            )

        row = matched.iloc[0]
        code = row["code"]
        market = _detect_market(code)
        logging.info(f"  → 搜索「{name}」匹配到：{row['name']}（{code}）")
        return {"code": code, "market": market,
                "full": f"{code}.{market.upper()}", "name": row["name"]}
    except ValueError:
        raise
    except Exception as e:
        raise ValueError(f"搜索股票失败：{e}")


# ============================================================
# 行情：东财 → 新浪K线取最新一日（避免全量快照超时）
# ============================================================
def fetch_quote(code: str) -> dict:
    # 优先东方财富
    try:
        df = ak.stock_zh_a_spot_em()
        row = df[df["代码"] == code]
        if not row.empty:
            return _parse_quote_em(row.iloc[0])
    except Exception as e:
        if _is_connection_error(e):
            _warn_em_blocked("实时行情")
        else:
            logging.warning(f"东财行情异常：{e}")

    # 备用：从新浪K线取最近2日数据推算当日行情
    # 比全量快照(stock_zh_a_spot)快得多，且境外可访问
    try:
        logging.info("  → [行情] 尝试新浪K线备用接口...")
        market = _detect_market(code)
        end = datetime.now().strftime("%Y%m%d")
        start = (datetime.now() - timedelta(days=5)).strftime("%Y%m%d")
        df = ak.stock_zh_a_daily(
            symbol=f"{market}{code}", adjust="",   # 不复权，取真实价格
            start_date=start, end_date=end
        )
        if df is not None and not df.empty:
            latest = df.iloc[-1]
            prev = df.iloc[-2] if len(df) >= 2 else latest
            price = float(latest.get("close", 0) or 0)
            pre_close = float(prev.get("close", 0) or 0)
            change_amt = round(price - pre_close, 2)
            change_pct = round(change_amt / pre_close * 100, 2) if pre_close else 0
            return {
                "price": price,
                "change_pct": change_pct,
                "change_amt": change_amt,
                "volume": float(latest.get("volume", 0) or 0),
                "amount": float(latest.get("amount", 0) or 0),
                "turnover": 0,        # 新浪K线无换手率
                "high": float(latest.get("high", 0) or 0),
                "low": float(latest.get("low", 0) or 0),
                "open": float(latest.get("open", 0) or 0),
                "pre_close": pre_close,
                "market_cap": 0,      # 新浪K线无总市值
                "pe_dynamic": 0,      # 新浪K线无PE
                "pb": 0,
            }
    except Exception as e:
        logging.warning(f"新浪K线备用行情也失败：{e}")

    return {}


def _parse_quote_em(r) -> dict:
    def f(k): return float(r.get(k, 0) or 0)
    return {
        "price": f("最新价"), "change_pct": f("涨跌幅"),
        "change_amt": f("涨跌额"), "volume": f("成交量"),
        "amount": f("成交额"), "turnover": f("换手率"),
        "high": f("最高"), "low": f("最低"),
        "open": f("今开"), "pre_close": f("昨收"),
        "market_cap": f("总市值"),
        "pe_dynamic": f("市盈率-动态"), "pb": f("市净率"),
    }


# ============================================================
# 历史K线：东财 → 新浪
# ============================================================
def fetch_history(code: str, days: int = 60) -> dict:
    end = datetime.now().strftime("%Y%m%d")
    start = (datetime.now() - timedelta(days=days + 20)).strftime("%Y%m%d")
    df = pd.DataFrame()

    try:
        df = ak.stock_zh_a_hist(
            symbol=code, period="daily",
            start_date=start, end_date=end, adjust="qfq"
        )
    except Exception as e:
        if _is_connection_error(e):
            _warn_em_blocked("历史K线")
        else:
            logging.warning(f"东财K线异常：{e}")

    if df is None or df.empty:
        try:
            logging.info("  → [K线] 尝试新浪财经备用接口...")
            market = _detect_market(code)
            df = ak.stock_zh_a_daily(symbol=f"{market}{code}", adjust="qfq")
            if df is not None and not df.empty:
                df = df.rename(columns={"close": "收盘", "date": "日期"})
                start_date = f"{start[:4]}-{start[4:6]}-{start[6:]}"
                df = df[df["日期"].astype(str) >= start_date]
        except Exception as e:
            logging.warning(f"新浪K线也失败：{e}")

    if df is None or df.empty:
        return {}

    df = df.tail(days)
    close_col = "收盘" if "收盘" in df.columns else "close"
    close = df[close_col].tolist()
    if not close:
        return {}

    week_chg = round((close[-1] / close[-5] - 1) * 100, 2) if len(close) >= 5 else None
    month_chg = round((close[-1] / close[-20] - 1) * 100, 2) if len(close) >= 20 else None
    ma5 = round(sum(close[-5:]) / 5, 2) if len(close) >= 5 else None
    ma20 = round(sum(close[-20:]) / 20, 2) if len(close) >= 20 else None
    ma60 = round(sum(close[-60:]) / 60, 2) if len(close) >= 60 else None

    return {
        "week_change": week_chg, "month_change": month_chg,
        "ma5": ma5, "ma20": ma20, "ma60": ma60,
        "current_price": close[-1],
        "recent_high": max(close[-20:]) if len(close) >= 20 else None,
        "recent_low": min(close[-20:]) if len(close) >= 20 else None,
    }


# ============================================================
# 财务指标（修正列名，带单位后缀）
# ============================================================
def fetch_financials(code: str) -> dict:
    try:
        df = ak.stock_financial_analysis_indicator(symbol=code, start_year="2023")
        if df is None or df.empty:
            return {}
        latest = df.iloc[0]

        def s(k):
            v = latest.get(k)
            try:
                return float(v) if v not in [None, "--", ""] and str(v) != "nan" else None
            except Exception:
                return None

        return {
            "report_date": str(latest.get("日期", "")),
            "roe": s("净资产收益率(%)"),           # 修正
            "gross_margin": s("销售毛利率(%)"),    # 修正
            "net_margin": s("销售净利率(%)"),      # 修正（原字段名是"净利率"，实为"销售净利率(%)"）
            "debt_ratio": s("资产负债率(%)"),      # 修正
            "revenue_growth": s("主营业务收入增长率(%)"),  # 修正
            "profit_growth": s("净利润增长率(%)"),         # 修正
            "eps": s("摊薄每股收益(元)"),          # 修正（原"每股收益"实为"摊薄每股收益(元)"）
        }
    except Exception as e:
        if _is_connection_error(e):
            _warn_em_blocked("财务指标")
            logging.warning("   财务指标模块暂无备用数据源，此项将在报告中显示为空。")
        else:
            logging.warning(f"获取财务指标失败：{e}")
        return {}


# ============================================================
# 主力资金流向（修正参数名：stock=，非 symbol=）
# ============================================================
def fetch_fund_flow(code: str, market: str) -> dict:
    try:
        df = ak.stock_individual_fund_flow(stock=code, market=market)  # 修正
        if df is None or df.empty:
            return {}
        latest = df.iloc[-1]

        def s(k):
            v = latest.get(k)
            try:
                return float(v) if v not in [None, "--", ""] and str(v) != "nan" else None
            except Exception:
                return None

        return {
            "date": str(latest.get("日期", "")),
            "main_net": s("主力净流入-净额"),
            "main_net_pct": s("主力净流入-净占比"),
            "super_net": s("超大单净流入-净额"),
            "big_net": s("大单净流入-净额"),
            "small_net": s("小单净流入-净额"),
        }
    except Exception as e:
        if _is_connection_error(e):
            _warn_em_blocked("主力资金流向")
            logging.warning("   资金流向模块暂无备用数据源，此项将在报告中显示为空。")
        else:
            logging.warning(f"获取资金流向失败：{e}")
        return {}


# ============================================================
# 近期新闻（东财唯一，无备用接口）
# ============================================================
def fetch_news(code: str, count: int = 5) -> list:
    try:
        df = ak.stock_news_em(symbol=code)
        if df is None or df.empty:
            return []
        news = []
        for _, row in df.head(count).iterrows():
            news.append({
                "title": str(row.get("新闻标题", "")),
                "date": str(row.get("发布时间", "")),
                "source": str(row.get("文章来源", "")),
            })
        return news
    except Exception as e:
        if _is_connection_error(e):
            _warn_em_blocked("个股新闻")
            logging.warning("   新闻模块暂无备用数据源，此项将在报告中显示为空。")
        else:
            logging.warning(f"获取新闻失败：{e}")
        return []


# ============================================================
# 股票基本信息
# ============================================================
def fetch_basic_info(code: str) -> dict:
    try:
        df = ak.stock_individual_info_em(symbol=code)
        info = dict(zip(df["item"], df["value"]))
        return {
            "name": info.get("股票简称", ""),
            "industry": info.get("行业", ""),
            "list_date": info.get("上市时间", ""),
            "total_shares": info.get("总股本", ""),
            "float_shares": info.get("流通股本", ""),
            "total_assets": info.get("总资产", ""),
        }
    except Exception as e:
        if _is_connection_error(e):
            _warn_em_blocked("基本信息")
        else:
            logging.warning(f"获取基本信息失败：{e}")
        return {}


# ============================================================
# 主入口
# ============================================================
def fetch_all(raw_input: str, news_count: int = 5) -> dict:
    stock = normalize_code(raw_input)
    code = stock["code"]
    market = stock["market"]
    logging.info(f"📡 抓取数据：{stock['name']}（{stock['full']}）")

    data = {"stock": stock}

    logging.info("  → 基本信息...")
    data["basic"] = fetch_basic_info(code)
    if not data["basic"].get("name"):
        data["basic"]["name"] = stock["name"]

    logging.info("  → 今日行情...")
    data["quote"] = fetch_quote(code)

    logging.info("  → 历史K线...")
    data["history"] = fetch_history(code)

    logging.info("  → 财务指标...")
    data["financials"] = fetch_financials(code)

    logging.info("  → 主力资金...")
    data["fund_flow"] = fetch_fund_flow(code, market)

    logging.info("  → 近期新闻...")
    data["news"] = fetch_news(code, news_count)

    logging.info("✅ 数据抓取完成")
    return data
