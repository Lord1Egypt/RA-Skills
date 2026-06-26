#!/usr/bin/env python3

import argparse
import json
import math
import os
import re
import sys
import warnings
from datetime import date, datetime, timedelta
from difflib import SequenceMatcher
from pathlib import Path

import pandas as pd
import tushare as ts
from trading_analysis import list_indicator_specs, run_indicator_suite, technical_analysis_keywords


warnings.filterwarnings("ignore", category=FutureWarning, module=r"tushare(\.|$)")


DEFAULT_USER_POINTS = int(os.environ.get("TUSHARE_POINTS", "5120"))
CACHE_DIR = Path(os.environ.get("TUSHARE_STOCK_CACHE_DIR", "/tmp/tushare_stock_skill"))
CATALOG_PATH = Path(__file__).resolve().parents[1] / "references" / "stock_endpoints.json"

STOCK_ENDPOINT_ALIASES = {
    "stock_basic": ["股票列表", "股票清单", "上市股票", "a股列表", "证券列表"],
    "daily": ["历史日线", "日线", "日k", "日k线", "日级行情"],
    "rt_k": ["实时日线", "实时日k", "当日实时日线"],
    "stk_mins": ["历史分钟", "分钟行情", "分钟线", "分时历史", "1分钟", "5分钟", "15分钟", "30分钟", "60分钟"],
    "rt_min": ["实时分钟", "实时分时", "当日分钟", "分钟实时"],
    "weekly": ["周线", "周k", "周线行情"],
    "monthly": ["月线", "月k", "月线行情"],
    "adj_factor": ["复权因子"],
    "pro_bar": ["通用行情接口", "通用行情", "复权行情", "前复权", "后复权", "不复权", "未复权", "pro bar", "probar"],
    "daily_basic": ["每日指标", "估值指标", "市盈率", "市净率", "股息率", "换手率", "量比", "总市值", "流通市值"],
    "income": ["利润表", "营收", "营业收入", "净利润"],
    "balancesheet": ["资产负债表"],
    "cashflow": ["现金流量表", "现金流"],
    "forecast": ["业绩预告"],
    "express": ["业绩快报"],
    "dividend": ["分红送股", "分红", "送股", "派息"],
    "fina_indicator": ["财务指标", "roe", "roa", "毛利率", "净利率", "资产负债率"],
    "fina_audit": ["审计意见", "财务审计"],
    "fina_mainbz": ["主营业务构成", "主营构成"],
    "disclosure_date": ["财报披露日期", "披露日期表"],
    "top10_holders": ["前十大股东", "十大股东"],
    "top10_floatholders": ["前十大流通股东", "流通股东"],
    "pledge_stat": ["股权质押统计"],
    "pledge_detail": ["股权质押明细", "质押明细"],
    "repurchase": ["股票回购", "回购"],
    "share_float": ["限售股解禁", "解禁"],
    "block_trade": ["大宗交易"],
    "stk_holdernumber": ["股东人数", "股东户数"],
    "stk_holdertrade": ["股东增减持", "高管增减持", "增减持"],
    "report_rc": ["券商盈利预测", "盈利预测", "研报预测", "卖方预测"],
    "cyq_perf": ["筹码及胜率", "胜率"],
    "cyq_chips": ["筹码分布"],
    "stk_factor_pro": ["技术面因子", "技术因子", "技术面", "因子专业版"],
    "ccass_hold": ["中央结算系统持股统计", "ccass持股统计"],
    "ccass_hold_detail": ["中央结算系统持股明细", "ccass持股明细"],
    "hk_hold": ["沪深股通持股明细", "陆股通持股"],
    "stk_auction_o": ["开盘集合竞价", "开盘竞价数据"],
    "stk_auction_c": ["收盘集合竞价", "收盘竞价数据"],
    "stk_nineturn": ["神奇九转", "九转"],
    "stk_ah_comparison": ["ah股比价", "ah比价"],
    "margin": ["融资融券交易汇总", "两融汇总"],
    "margin_detail": ["融资融券交易明细", "两融明细"],
    "margin_secs": ["融资融券标的", "两融标的"],
    "slb_sec": ["转融券交易明细", "转融券明细"],
    "slb_len": ["转融资交易汇总", "转融资"],
    "moneyflow": ["个股资金流向", "资金流向"],
    "moneyflow_ths": ["个股资金流向ths", "同花顺资金流"],
    "moneyflow_dc": ["个股资金流向dc", "东财个股资金流"],
    "moneyflow_ind_ths": ["行业资金流向", "ths行业资金流"],
    "moneyflow_ind_dc": ["板块资金流向dc", "东财板块资金流"],
    "moneyflow_mkt_dc": ["大盘资金流向", "市场资金流向"],
    "moneyflow_hsgt": ["沪深港通资金流向", "北向资金流向", "南向资金流向"],
    "top_list": ["龙虎榜每日统计单", "龙虎榜", "龙榜"],
    "top_inst": ["龙虎榜机构交易单", "龙虎榜机构", "机构龙虎榜"],
    "limit_list_ths": ["同花顺涨跌停榜单", "同花顺涨停榜", "涨跌停榜单"],
    "limit_list_d": ["涨跌停和炸板数据", "炸板", "封板", "涨停数据"],
    "limit_step": ["涨停股票连板天梯", "连板天梯", "连板"],
    "limit_cpt_list": ["涨停最强板块统计", "最强板块"],
    "ths_index": ["同花顺行业概念板块", "ths行业概念板块"],
    "ths_daily": ["同花顺概念和行业指数行情", "ths概念行业行情"],
    "ths_member": ["同花顺行业概念成分", "ths成分股"],
    "dc_index": ["东方财富概念板块", "东财概念板块"],
    "dc_member": ["东方财富概念成分", "东财概念成分"],
    "dc_daily": ["东财概念和行业指数行情", "东财概念行业行情"],
    "stk_auction": ["开盘竞价成交", "竞价成交"],
    "hm_list": ["市场游资最全名录", "游资名录"],
    "hm_detail": ["游资交易每日明细", "游资交易"],
    "ths_hot": ["同花顺app热榜", "同花顺热榜"],
    "dc_hot": ["东方财富app热榜", "东财热榜"],
    "tdx_index": ["通达信板块信息", "tdx板块信息"],
    "tdx_member": ["通达信板块成分", "tdx板块成分"],
    "tdx_daily": ["通达信板块行情", "tdx板块行情"],
    "kpl_list": ["开盘啦榜单", "开盘啦涨停榜", "开盘啦榜单数据"],
    "kpl_concept_cons": ["开盘啦题材成分", "开盘啦题材成分股"],
}

DATE_PRIORITY_PARAMS = ["trade_date", "ann_date", "period", "report_date", "start_date", "end_date"]
ANALYSIS_STRONG_KEYWORDS = [
    "分析",
    "怎么看",
    "解读",
    "评价",
    "投资价值",
    "研究报告",
    "总结",
    "报告",
]
ANALYSIS_SOFT_KEYWORDS = [
    "估值",
    "基本面",
    "财务质量",
    "盈利能力",
    "成长性",
    "趋势",
    "财务",
    "风险",
    "质量",
]
FUNDAMENTAL_ANALYSIS_KEYWORDS = [
    "估值",
    "基本面",
    "财务质量",
    "盈利能力",
    "成长性",
    "财务",
    "股东",
    "分红",
    "审计",
]
TRADING_ANALYSIS_KEYWORDS = technical_analysis_keywords() + [
    "交易观察",
    "交易信号",
    "盘面",
    "量价",
    "量能",
    "技术分析",
    "技术走势",
    "走势结构",
    "主力",
    "资金面",
]
TRADING_DEEP_TOPICS = [
    "龙虎榜",
    "机构席位",
    "游资",
    "席位",
]
TRADING_DEEP_HINTS = [
    "深度交易观察",
    "深度技术分析",
    "深度观察",
    "深入观察",
    "深挖",
    "深档",
]
ANALYSIS_EXCLUDE_PHRASES = [
    "风险警示板",
    "列表",
    "明细",
    "接口目录",
    "字段说明",
    "技术因子",
    "技术面因子",
]


def zh_status(value: str) -> str:
    mapping = {
        "ok": "成功",
        "error": "错误",
        "ambiguous": "需澄清",
        "gated": "受限",
    }
    return mapping.get(value, value)


def localize_payload(payload):
    if isinstance(payload, list):
        return [localize_payload(item) for item in payload]
    if not isinstance(payload, dict):
        return payload

    mapping = {
        "status": "状态",
        "message": "说明",
        "endpoint": "接口",
        "title": "接口名称",
        "category": "分类",
        "params": "参数",
        "gating": "权限校验",
        "candidates": "候选接口",
        "match_reasons": "匹配原因",
        "stock_resolution": "股票解析",
        "fields": "字段",
        "row_count": "总行数",
        "truncated": "是否截断",
        "rows": "数据",
        "docs_url": "文档链接",
        "allowed": "允许访问",
        "reason": "限制原因",
        "access_note": "权限说明",
        "tier": "权限层级",
        "warning": "提示",
        "count": "数量",
        "catalog": "接口目录",
        "api_name": "接口代码",
        "inactive": "是否停用",
        "doc_id": "文档ID",
        "url": "链接",
        "score": "匹配分数",
        "ts_code": "ts_code",
        "name": "名称",
        "match_type": "匹配类型",
        "matched_text": "命中文本",
        "formal_min_points": "正式权限积分门槛",
        "trial_points": "试用积分门槛",
        "unlimited_points": "不限量积分门槛",
        "requires_extra_permission": "是否需要额外权限",
        "analysis": "分析",
        "supporting_data": "数据摘要",
        "used_endpoints": "使用接口",
        "indicators": "技术指标目录",
        "aliases": "别名",
        "description": "说明",
        "min_periods": "最少交易日",
        "default_enabled": "默认启用",
        "key": "标识",
    }
    reason_mapping = {
        "inactive": "接口已停用",
        "extra_permission": "需要额外权限",
        "points": "积分不足",
    }
    tier_mapping = {
        "formal": "正式权限",
        "trial": "试用权限",
        "unknown": "未明确",
    }
    match_type_mapping = {
        "explicit_code": "显式代码",
        "ambiguous_name": "名称歧义",
        "name_match": "名称匹配",
    }

    localized = {}
    for key, value in payload.items():
        target_key = mapping.get(key, key)
        if key == "status" and isinstance(value, str):
            localized[target_key] = zh_status(value)
        elif key == "reason" and isinstance(value, str):
            localized[target_key] = reason_mapping.get(value, value)
        elif key == "tier" and isinstance(value, str):
            localized[target_key] = tier_mapping.get(value, value)
        elif key == "match_type" and isinstance(value, str):
            localized[target_key] = match_type_mapping.get(value, value)
        else:
            localized[target_key] = localize_payload(value)
    return localized


def print_json(payload: dict) -> None:
    print(json.dumps(localize_payload(payload), ensure_ascii=False, indent=2, default=str))


def fail(message: str, *, code: int = 1, **extra) -> None:
    payload = {"status": "error", "message": message}
    payload.update(extra)
    print_json(payload)
    raise SystemExit(code)


def normalize_text(text: str) -> str:
    lowered = text.lower()
    return re.sub(r"[\s\u3000,，。:：;；!！?？'\"“”‘’（）()\[\]【】/\\-]+", "", lowered)


def parse_dotenv_value(path: Path, key: str) -> str | None:
    if not path.exists():
        return None
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        env_key, value = line.split("=", 1)
        if env_key.strip() != key:
            continue
        value = value.strip().strip("\"'")
        return value or None
    return None


def load_token() -> str | None:
    token = os.environ.get("TUSHARE_TOKEN")
    if token:
        return token
    env_file = os.environ.get("TUSHARE_STOCK_ENV_FILE")
    if env_file:
        return parse_dotenv_value(Path(env_file).expanduser(), "TUSHARE_TOKEN")
    return None


def load_catalog() -> list[dict]:
    if not CATALOG_PATH.exists():
        fail(
            f"接口目录不存在：{CATALOG_PATH}。请先运行 scripts/build_catalog.py。",
            code=2,
        )
    payload = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    return payload["catalog"]


def init_pro():
    token = load_token()
    if not token:
        fail("未找到 TUSHARE_TOKEN。请设置环境变量 TUSHARE_TOKEN，或显式设置 TUSHARE_STOCK_ENV_FILE 指向包含该变量的 env 文件。")
    return ts.pro_api(token)


def parse_date_token(raw: str) -> date | None:
    token = raw.strip()
    for fmt in ("%Y%m%d", "%Y-%m-%d", "%Y/%m/%d", "%Y.%m.%d", "%Y年%m月%d日"):
        try:
            return datetime.strptime(token, fmt).date()
        except ValueError:
            continue
    return None


def date_to_str(day: date, *, time_like: bool = False) -> str:
    if time_like:
        return f"{day:%Y-%m-%d} 00:00:00"
    return f"{day:%Y%m%d}"


def extract_quarter_period(query: str) -> str | None:
    match = re.search(r"(20\d{2})\s*[qQ]\s*([1-4])", query)
    if match:
        year = int(match.group(1))
        quarter = int(match.group(2))
        return {1: f"{year}0331", 2: f"{year}0630", 3: f"{year}0930", 4: f"{year}1231"}[quarter]

    cn_match = re.search(r"(20\d{2})年?\s*(一季报|中报|半年报|三季报|年报)", query)
    if not cn_match:
        return None
    year = int(cn_match.group(1))
    label = cn_match.group(2)
    mapping = {
        "一季报": f"{year}0331",
        "中报": f"{year}0630",
        "半年报": f"{year}0630",
        "三季报": f"{year}0930",
        "年报": f"{year}1231",
    }
    return mapping[label]


def parse_relative_window(query: str) -> tuple[date, date] | None:
    today = date.today()
    direct = {
        "近一周": 7,
        "最近一周": 7,
        "近1周": 7,
        "近一月": 30,
        "最近一月": 30,
        "近1月": 30,
        "近三月": 90,
        "最近三月": 90,
        "近3月": 90,
        "近半年": 180,
        "近一年": 365,
        "最近一年": 365,
        "近1年": 365,
    }
    normalized = query.replace("个", "")
    for key, days in direct.items():
        if key in normalized:
            return today - timedelta(days=days), today

    match = re.search(r"近(\d+)(天|周|月|年)", normalized)
    if not match:
        return None
    amount = int(match.group(1))
    unit = match.group(2)
    multiplier = {"天": 1, "周": 7, "月": 30, "年": 365}[unit]
    return today - timedelta(days=amount * multiplier), today


def extract_explicit_dates(query: str) -> list[date]:
    tokens = re.findall(r"(20\d{2}(?:[-/.年]?\d{1,2}(?:[-/.月]?\d{1,2}日?)?)?)", query)
    result = []
    for token in tokens:
        parsed = parse_date_token(token)
        if parsed:
            result.append(parsed)
    return result


def infer_market_code(code: str) -> str:
    if "." in code:
        return code.upper()
    if code.startswith(("6", "9")):
        return f"{code}.SH"
    if code.startswith(("0", "2", "3")):
        return f"{code}.SZ"
    if code.startswith(("4", "8")):
        return f"{code}.BJ"
    return code.upper()


def has_data_query_intent(query: str) -> bool:
    return any(word in query for word in ["数据", "接口", "字段", "抓取", "提取", "查询", "列表", "明细", "原始"])


def has_trading_analysis_focus(query: str) -> bool:
    if any(phrase in query for phrase in ["技术因子", "技术面因子", "个股资金流向", "龙虎榜机构交易单"]):
        return False
    lowered = query.lower()
    if any(keyword.lower() in lowered for keyword in TRADING_ANALYSIS_KEYWORDS):
        return True
    return False


def has_trading_deep_topic(query: str) -> bool:
    return any(keyword in query for keyword in TRADING_DEEP_TOPICS)


def infer_trading_depth(query: str) -> str:
    if has_trading_deep_topic(query):
        return "deep"
    if any(keyword in query for keyword in TRADING_DEEP_HINTS) and has_trading_analysis_focus(query):
        return "deep"
    return "quick"


def infer_analysis_scope(query: str) -> dict:
    trading = has_trading_analysis_focus(query)
    fundamental = any(keyword in query for keyword in FUNDAMENTAL_ANALYSIS_KEYWORDS)
    generic = any(keyword in query for keyword in ANALYSIS_STRONG_KEYWORDS)
    trading_depth = infer_trading_depth(query)

    if generic and has_trading_deep_topic(query) and not fundamental:
        return {"fundamental": False, "trading": True, "trading_depth": "deep"}
    if generic and not trading and not fundamental:
        return {"fundamental": True, "trading": True, "trading_depth": trading_depth}
    if trading and not fundamental:
        return {"fundamental": False, "trading": True, "trading_depth": trading_depth}
    if fundamental and not trading:
        return {"fundamental": True, "trading": "趋势" in query, "trading_depth": trading_depth}
    return {
        "fundamental": fundamental or generic,
        "trading": trading or generic,
        "trading_depth": trading_depth,
    }


def is_analysis_request(query: str) -> bool:
    if any(phrase in query for phrase in ANALYSIS_EXCLUDE_PHRASES):
        return False
    if has_trading_analysis_focus(query) and not has_data_query_intent(query):
        return True
    if any(keyword in query for keyword in ANALYSIS_STRONG_KEYWORDS):
        return True
    if any(keyword in query for keyword in ANALYSIS_SOFT_KEYWORDS) and not has_data_query_intent(query):
        return True
    return False


def cache_path(name: str) -> Path:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    return CACHE_DIR / name


def load_stock_cache() -> list[dict] | None:
    path = cache_path("stock_basic_cache.json")
    if not path.exists():
        return None
    age = time_since(path)
    if age > timedelta(hours=24):
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def time_since(path: Path) -> timedelta:
    return datetime.now() - datetime.fromtimestamp(path.stat().st_mtime)


def to_float(value):
    if value is None:
        return None
    if isinstance(value, (int, float)):
        if isinstance(value, float) and math.isnan(value):
            return None
        return float(value)
    try:
        value = float(value)
    except (TypeError, ValueError):
        return None
    if math.isnan(value):
        return None
    return value


def round_if(value, digits: int = 2):
    number = to_float(value)
    if number is None:
        return None
    return round(number, digits)


def format_num(value, digits: int = 2, suffix: str = "") -> str:
    number = to_float(value)
    if number is None:
        return "暂无"
    return f"{round(number, digits)}{suffix}"


def format_pct(value, digits: int = 2) -> str:
    return format_num(value, digits, "%")


def format_yi_from_wanyuan(value) -> str:
    number = to_float(value)
    if number is None:
        return "暂无"
    return f"{round(number / 10000, 2)}亿元"


def format_yi_from_yuan(value) -> str:
    number = to_float(value)
    if number is None:
        return "暂无"
    return f"{round(number / 1e8, 2)}亿元"


def format_wangu(value) -> str:
    number = to_float(value)
    if number is None:
        return "暂无"
    return f"{round(number / 10000, 2)}万股"


def clamp_score(score: float) -> int:
    return max(1, min(5, int(round(score))))


def strength_label(score: int) -> str:
    mapping = {
        1: "很弱",
        2: "偏弱",
        3: "中性",
        4: "较强",
        5: "很强",
    }
    return mapping[score]


def attractiveness_label(score: int) -> str:
    mapping = {
        1: "很低",
        2: "偏低",
        3: "中性",
        4: "较高",
        5: "很高",
    }
    return mapping[score]


def clean_record(record: dict | None) -> dict:
    if not record:
        return {}
    return {key: clean_value(value) for key, value in record.items() if clean_value(value) is not None}


def latest_record(df: pd.DataFrame, sort_cols: list[str] | None = None) -> dict:
    if df is None or df.empty:
        return {}
    sort_cols = sort_cols or ["trade_date", "ann_date", "end_date", "float_date"]
    frame = df.copy()
    for col in sort_cols:
        if col in frame.columns:
            frame = frame.sort_values(col, ascending=False)
            break
    return clean_record(frame.iloc[0].to_dict())


def top_records(df: pd.DataFrame, limit: int = 5, sort_cols: list[str] | None = None) -> list[dict]:
    if df is None or df.empty:
        return []
    sort_cols = sort_cols or ["trade_date", "ann_date", "end_date", "float_date"]
    frame = df.copy()
    for col in sort_cols:
        if col in frame.columns:
            frame = frame.sort_values(col, ascending=False)
            break
    subset = frame.head(limit)
    return [clean_record(record) for record in subset.to_dict(orient="records")]


def safe_fetch_dataframe(loader, *, label: str, limitations: list[str]) -> pd.DataFrame:
    try:
        df = loader()
        if df is None:
            return pd.DataFrame()
        return df
    except Exception as exc:
        limitations.append(f"{label} 获取失败：{exc}")
        return pd.DataFrame()


def pick_stock_info(ts_code: str, pro) -> dict:
    stocks = fetch_stock_lookup(pro)
    for row in stocks:
        if row.get("ts_code") == ts_code:
            return clean_record(row)
    return {"ts_code": ts_code}


def select_holder_snapshot(df: pd.DataFrame) -> list[dict]:
    if df is None or df.empty or "end_date" not in df.columns:
        return []
    latest_end = df["end_date"].astype(str).max()
    snapshot = df[df["end_date"].astype(str) == latest_end].sort_values("hold_ratio", ascending=False)
    return [clean_record(record) for record in snapshot.head(10).to_dict(orient="records")]


def moving_return(closes: pd.Series, days: int):
    if len(closes) <= days:
        return None
    base = to_float(closes.iloc[-days - 1])
    latest = to_float(closes.iloc[-1])
    if base in (None, 0) or latest is None:
        return None
    return (latest / base - 1) * 100


def summarize_valuation(daily_basic: dict) -> tuple[dict, int]:
    pe_ttm = to_float(daily_basic.get("pe_ttm"))
    pb = to_float(daily_basic.get("pb"))
    ps_ttm = to_float(daily_basic.get("ps_ttm"))
    dv_ttm = to_float(daily_basic.get("dv_ttm"))
    total_mv = to_float(daily_basic.get("total_mv"))

    score = 3.0
    comments = []

    if pe_ttm is not None:
        if pe_ttm <= 15:
            score += 1
            comments.append("PE(TTM)不高")
        elif pe_ttm >= 30:
            score -= 1
            comments.append("PE(TTM)偏高")
        elif pe_ttm >= 22:
            score -= 0.5
            comments.append("PE(TTM)不低")

    if pb is not None:
        if pb <= 2:
            score += 0.8
            comments.append("PB较低")
        elif pb >= 5:
            score -= 0.8
            comments.append("PB偏高")

    if dv_ttm is not None:
        if dv_ttm >= 4:
            score += 0.6
            comments.append("股息率较好")
        elif dv_ttm < 1:
            score -= 0.4
            comments.append("股息率偏低")

    final_score = clamp_score(score)
    if final_score >= 4:
        conclusion = "从绝对估值看，当前估值吸引力较高。"
    elif final_score <= 2:
        conclusion = "从绝对估值看，当前并不便宜，需要更强基本面来支撑。"
    else:
        conclusion = "从绝对估值看，当前大致处于中性区间。"
    if comments:
        conclusion = f"{conclusion} 主要依据：{'、'.join(comments)}。"

    return (
        {
            "估值吸引力": attractiveness_label(final_score),
            "结论": conclusion,
            "指标": {
                "收盘价": round_if(daily_basic.get("close")),
                "PE_TTM": round_if(pe_ttm),
                "PB": round_if(pb),
                "PS_TTM": round_if(ps_ttm),
                "股息率_TTM": round_if(dv_ttm),
                "总市值": format_yi_from_wanyuan(total_mv),
            },
        },
        final_score,
    )


def summarize_quality(fina: dict, cashflow: dict, audit: dict) -> tuple[dict, int]:
    roe = to_float(fina.get("roe"))
    gross_margin = to_float(fina.get("grossprofit_margin"))
    debt_to_assets = to_float(fina.get("debt_to_assets"))
    current_ratio = to_float(fina.get("current_ratio"))
    quick_ratio = to_float(fina.get("quick_ratio"))
    ocfps = to_float(fina.get("ocfps"))
    eps = to_float(fina.get("eps"))
    cash_profit_ratio = None
    if ocfps is not None and eps not in (None, 0):
        cash_profit_ratio = ocfps / eps
    free_cashflow = to_float(cashflow.get("free_cashflow"))
    audit_result = audit.get("audit_result")

    score = 3.0
    notes = []

    if roe is not None:
        if roe >= 20:
            score += 1
            notes.append("ROE较高")
        elif roe < 10:
            score -= 1
            notes.append("ROE偏低")
    if gross_margin is not None:
        if gross_margin >= 40:
            score += 0.8
            notes.append("毛利率高")
        elif gross_margin < 15:
            score -= 0.8
            notes.append("毛利率偏低")
    if debt_to_assets is not None:
        if debt_to_assets <= 30:
            score += 0.6
            notes.append("资产负债率低")
        elif debt_to_assets >= 60:
            score -= 1
            notes.append("资产负债率高")
    if current_ratio is not None and current_ratio >= 1.5:
        score += 0.3
    elif current_ratio is not None and current_ratio < 1:
        score -= 0.5
        notes.append("流动比率偏弱")
    if quick_ratio is not None and quick_ratio < 1:
        score -= 0.3
        notes.append("速动比率偏弱")
    if cash_profit_ratio is not None:
        if cash_profit_ratio >= 1:
            score += 0.5
            notes.append("每股经营现金流覆盖每股收益")
        elif cash_profit_ratio < 0.8:
            score -= 0.5
            notes.append("现金流与利润匹配度一般")
    if free_cashflow is not None and free_cashflow > 0:
        score += 0.4
    elif free_cashflow is not None and free_cashflow < 0:
        score -= 0.4
        notes.append("自由现金流为负")
    if audit_result and audit_result != "标准无保留意见":
        score -= 1.5
        notes.append(f"审计意见为{audit_result}")

    final_score = clamp_score(score)
    conclusion = f"财务质量{strength_label(final_score)}。"
    if notes:
        conclusion = f"{conclusion} 主要依据：{'、'.join(notes)}。"

    return (
        {
            "财务质量": strength_label(final_score),
            "结论": conclusion,
            "指标": {
                "ROE": round_if(roe),
                "毛利率": round_if(gross_margin),
                "资产负债率": round_if(debt_to_assets),
                "流动比率": round_if(current_ratio),
                "速动比率": round_if(quick_ratio),
                "每股经营现金流/每股收益": round_if(cash_profit_ratio),
                "自由现金流": format_yi_from_yuan(free_cashflow),
                "审计意见": audit_result or "暂无",
            },
        },
        final_score,
    )


def summarize_growth(fina: dict) -> tuple[dict, int]:
    revenue_yoy = to_float(fina.get("or_yoy") if fina.get("or_yoy") is not None else fina.get("tr_yoy"))
    profit_yoy = to_float(fina.get("dt_netprofit_yoy") if fina.get("dt_netprofit_yoy") is not None else fina.get("netprofit_yoy"))
    ocf_yoy = to_float(fina.get("ocf_yoy"))
    q_sales_yoy = to_float(fina.get("q_sales_yoy"))

    score = 3.0
    notes = []

    if revenue_yoy is not None:
        if revenue_yoy >= 15:
            score += 1
            notes.append("营收增速较快")
        elif revenue_yoy >= 5:
            score += 0.4
        elif revenue_yoy < 0:
            score -= 1
            notes.append("营收同比转负")
    if profit_yoy is not None:
        if profit_yoy >= 15:
            score += 1
            notes.append("净利润增速较快")
        elif profit_yoy >= 5:
            score += 0.4
        elif profit_yoy < 0:
            score -= 1
            notes.append("净利润同比转负")
    if ocf_yoy is not None:
        if ocf_yoy >= 10:
            score += 0.5
        elif ocf_yoy <= -20:
            score -= 0.5
            notes.append("经营现金流同比下滑较快")
    if q_sales_yoy is not None and q_sales_yoy < 0:
        score -= 0.4
        notes.append("单季营收同比转负")

    final_score = clamp_score(score)
    conclusion = f"成长性{strength_label(final_score)}。"
    if notes:
        conclusion = f"{conclusion} 主要依据：{'、'.join(notes)}。"

    return (
        {
            "成长性": strength_label(final_score),
            "结论": conclusion,
            "指标": {
                "营业收入同比": round_if(revenue_yoy),
                "净利润同比": round_if(profit_yoy),
                "经营现金流同比": round_if(ocf_yoy),
                "单季营收同比": round_if(q_sales_yoy),
            },
        },
        final_score,
    )


def summarize_trend(price_df: pd.DataFrame) -> tuple[dict, int]:
    if price_df is None or price_df.empty:
        return (
            {
                "趋势强弱": "暂无",
                "结论": "暂无足够价格序列，无法生成趋势分析。",
                "指标": {},
            },
            3,
        )

    frame = price_df.copy().sort_values("trade_date")
    closes = pd.to_numeric(frame["close"], errors="coerce").dropna()
    if closes.empty:
        return (
            {
                "趋势强弱": "暂无",
                "结论": "价格序列为空，无法生成趋势分析。",
                "指标": {},
            },
            3,
        )

    latest_close = to_float(closes.iloc[-1])
    ma20 = closes.tail(20).mean() if len(closes) >= 20 else None
    ma60 = closes.tail(60).mean() if len(closes) >= 60 else None
    ma250 = closes.tail(250).mean() if len(closes) >= 250 else None
    ret20 = moving_return(closes, 20)
    ret60 = moving_return(closes, 60)
    ret250 = moving_return(closes, 250)
    high_250 = to_float(closes.tail(250).max()) if len(closes) >= 20 else to_float(closes.max())
    low_250 = to_float(closes.tail(250).min()) if len(closes) >= 20 else to_float(closes.min())
    range_pos = None
    if latest_close is not None and high_250 is not None and low_250 is not None and high_250 != low_250:
        range_pos = (latest_close - low_250) / (high_250 - low_250) * 100

    score = 3.0
    notes = []
    if latest_close is not None and ma20 is not None:
        if latest_close > ma20:
            score += 0.5
        else:
            score -= 0.5
            notes.append("股价低于20日均线")
    if latest_close is not None and ma60 is not None:
        if latest_close > ma60:
            score += 0.5
        else:
            score -= 0.5
            notes.append("股价低于60日均线")
    if ret60 is not None:
        if ret60 >= 10:
            score += 0.6
            notes.append("近60日表现偏强")
        elif ret60 <= -10:
            score -= 0.6
            notes.append("近60日表现偏弱")
    if ret250 is not None:
        if ret250 >= 15:
            score += 0.4
        elif ret250 <= -15:
            score -= 0.4

    final_score = clamp_score(score)
    conclusion = f"价格趋势{strength_label(final_score)}。"
    if notes:
        conclusion = f"{conclusion} 主要依据：{'、'.join(notes)}。"

    return (
        {
            "趋势强弱": strength_label(final_score),
            "结论": conclusion,
            "指标": {
                "最新收盘价": round_if(latest_close),
                "20日涨跌幅": round_if(ret20),
                "60日涨跌幅": round_if(ret60),
                "250日涨跌幅": round_if(ret250),
                "20日均线": round_if(ma20),
                "60日均线": round_if(ma60),
                "250日均线": round_if(ma250),
                "近一年价格区间位置": round_if(range_pos),
            },
        },
        final_score,
    )


def summarize_capital_actions(holders: list[dict], holdertrade: list[dict], repurchase: list[dict], share_float: list[dict]) -> dict:
    top_holder = holders[0] if holders else {}
    top3_ratio = sum(to_float(item.get("hold_ratio")) or 0 for item in holders[:3]) if holders else None
    hkcc = next((item for item in holders if "香港中央结算" in str(item.get("holder_name", ""))), None)

    in_total = sum(to_float(item.get("change_vol")) or 0 for item in holdertrade if item.get("in_de") == "IN")
    de_total = sum(to_float(item.get("change_vol")) or 0 for item in holdertrade if item.get("in_de") == "DE")
    net_holder_change = in_total - de_total
    repurchase_amount = sum(to_float(item.get("amount")) or 0 for item in repurchase)

    signals = []
    if net_holder_change > 0:
        signals.append(f"近一年重要股东净增持约 {format_wangu(net_holder_change)}")
    elif net_holder_change < 0:
        signals.append(f"近一年重要股东净减持约 {format_wangu(abs(net_holder_change))}")

    if repurchase_amount > 0:
        signals.append(f"近期实施回购约 {format_yi_from_yuan(repurchase_amount)}")

    if hkcc and hkcc.get("hold_change") is not None:
        hold_change = to_float(hkcc.get("hold_change"))
        if hold_change is not None:
            direction = "增加" if hold_change > 0 else "减少"
            signals.append(f"香港中央结算最新一期持股变动为{direction} {format_wangu(abs(hold_change))}")

    if share_float:
        upcoming = share_float[0]
        signals.append(
            f"最近可见解禁日期为 {upcoming.get('float_date')}，解禁比例约 {format_pct(upcoming.get('float_ratio'))}"
        )
    else:
        signals.append("近期未查到明显解禁安排")

    if not signals:
        signals.append("近期未见明显资本动作。")

    return {
        "结论": "；".join(signals) + "。",
        "指标": {
            "第一大股东": top_holder.get("holder_name", "暂无"),
            "第一大股东持股比例": round_if(top_holder.get("hold_ratio")),
            "前三大股东合计持股比例": round_if(top3_ratio),
            "近一年重要股东净变动": format_wangu(net_holder_change) if net_holder_change else "0.0万股",
            "近期回购金额": format_yi_from_yuan(repurchase_amount),
        },
        "近期事件": {
            "股东增减持": holdertrade[:5],
            "回购": repurchase[:5],
            "解禁": share_float[:5],
        },
    }


def format_signed_yi_from_wanyuan(value) -> str:
    number = to_float(value)
    if number is None:
        return "暂无"
    direction = "净流入" if number > 0 else "净流出" if number < 0 else "净流平"
    return f"{direction}{round(abs(number) / 10000, 2)}亿元"


def ratio_vs_average(value, baseline) -> float | None:
    current = to_float(value)
    base = to_float(baseline)
    if current is None or base in (None, 0):
        return None
    return current / base


def build_endpoint_map() -> dict[str, dict]:
    return {item["api_name"]: item for item in load_catalog() if item.get("api_name")}


def fetch_analysis_df(pro, endpoint_map: dict[str, dict], api_name: str, loader, *, limitations: list[str], label: str | None = None) -> pd.DataFrame:
    endpoint = endpoint_map.get(api_name)
    if endpoint:
        gate = gating_decision(endpoint)
        if not gate["allowed"]:
            limitations.append(f"{api_name} 未调取：{gate.get('message') or gate.get('access_note') or '受权限限制'}")
            return pd.DataFrame()
    return safe_fetch_dataframe(loader, label=label or api_name, limitations=limitations)


def scan_recent_rank_records(
    pro,
    endpoint_map: dict[str, dict],
    api_name: str,
    ts_code: str,
    trade_dates: list[str],
    *,
    limitations: list[str],
    scan_days: int = 12,
    row_limit: int = 5,
) -> tuple[list[dict], int]:
    endpoint = endpoint_map.get(api_name)
    if endpoint:
        gate = gating_decision(endpoint)
        if not gate["allowed"]:
            limitations.append(f"{api_name} 未调取：{gate.get('message') or gate.get('access_note') or '受权限限制'}")
            return [], 0

    records = []
    scanned_days = 0
    for trade_date in trade_dates[:scan_days]:
        scanned_days += 1
        df = safe_fetch_dataframe(
            lambda trade_date=trade_date: getattr(pro, api_name)(trade_date=trade_date),
            label=f"{api_name}:{trade_date}",
            limitations=limitations,
        )
        if df.empty or "ts_code" not in df.columns:
            continue
        matched = df[df["ts_code"].astype(str) == ts_code]
        if matched.empty:
            continue
        records.extend([clean_record(item) for item in matched.head(row_limit).to_dict(orient="records")])
        if len(records) >= row_limit:
            break
    return records[:row_limit], scanned_days


def summarize_volume_profile(price_df: pd.DataFrame, daily_basic_df: pd.DataFrame) -> tuple[dict, int]:
    if price_df is None or price_df.empty or daily_basic_df is None or daily_basic_df.empty:
        return (
            {
                "量价强弱": "暂无",
                "结论": "量价所需数据不足，暂不生成量能观察。",
                "指标": {},
            },
            3,
        )

    price_frame = price_df.copy().sort_values("trade_date")
    basic_frame = daily_basic_df.copy().sort_values("trade_date")
    latest_price = clean_record(price_frame.iloc[-1].to_dict())
    latest_basic = clean_record(basic_frame.iloc[-1].to_dict())
    latest_amount = to_float(latest_price.get("amount"))
    avg5_amount = to_float(pd.to_numeric(price_frame["amount"], errors="coerce").tail(5).mean()) if "amount" in price_frame.columns else None
    avg20_amount = to_float(pd.to_numeric(price_frame["amount"], errors="coerce").tail(20).mean()) if "amount" in price_frame.columns else None
    amount_ratio_5 = ratio_vs_average(latest_amount, avg5_amount)
    amount_ratio_20 = ratio_vs_average(latest_amount, avg20_amount)
    pct_chg = to_float(latest_price.get("pct_chg"))
    turnover = to_float(latest_basic.get("turnover_rate"))
    volume_ratio = to_float(latest_basic.get("volume_ratio"))

    score = 3.0
    notes = []
    if pct_chg is not None and amount_ratio_5 is not None:
        if pct_chg > 0 and amount_ratio_5 >= 1.15:
            score += 0.9
            notes.append("放量上涨")
        elif pct_chg < 0 and amount_ratio_5 >= 1.15:
            score -= 0.9
            notes.append("放量下跌")
        elif pct_chg > 0 and amount_ratio_5 <= 0.9:
            score += 0.2
            notes.append("缩量上涨")
        elif pct_chg < 0 and amount_ratio_5 <= 0.9:
            score -= 0.2
            notes.append("缩量下跌")
    if volume_ratio is not None:
        if volume_ratio >= 1.5:
            score += 0.4
            notes.append("量比偏高")
        elif volume_ratio <= 0.8:
            score -= 0.2
            notes.append("量比偏低")
    if turnover is not None and turnover >= 5:
        score += 0.2

    final_score = clamp_score(score)
    conclusion = f"量价配合{strength_label(final_score)}。"
    if notes:
        conclusion = f"{conclusion} 主要依据：{'、'.join(notes)}。"
    return (
        {
            "量价强弱": strength_label(final_score),
            "结论": conclusion,
            "指标": {
                "最新涨跌幅": round_if(pct_chg),
                "最新换手率": round_if(turnover),
                "最新量比": round_if(volume_ratio),
                "最新成交额/5日均额": round_if(amount_ratio_5),
                "最新成交额/20日均额": round_if(amount_ratio_20),
            },
        },
        final_score,
    )


def summarize_moneyflow(moneyflow_df: pd.DataFrame) -> tuple[dict, int]:
    if moneyflow_df is None or moneyflow_df.empty:
        return (
            {
                "资金强弱": "暂无",
                "结论": "未取到个股资金流数据，暂不生成资金面观察。",
                "指标": {},
            },
            3,
        )

    frame = moneyflow_df.copy().sort_values("trade_date")
    latest = clean_record(frame.iloc[-1].to_dict())
    net_5 = to_float(pd.to_numeric(frame["net_mf_amount"], errors="coerce").tail(5).sum())
    net_20 = to_float(pd.to_numeric(frame["net_mf_amount"], errors="coerce").tail(20).sum())
    large_5 = to_float(
        (
            pd.to_numeric(frame["buy_lg_amount"], errors="coerce")
            + pd.to_numeric(frame["buy_elg_amount"], errors="coerce")
            - pd.to_numeric(frame["sell_lg_amount"], errors="coerce")
            - pd.to_numeric(frame["sell_elg_amount"], errors="coerce")
        ).tail(5).sum()
    )
    positive_days = int((pd.to_numeric(frame["net_mf_amount"], errors="coerce").tail(10) > 0).sum())
    latest_net = to_float(latest.get("net_mf_amount"))

    score = 3.0
    notes = []
    if net_20 is not None:
        if net_20 > 0:
            score += 0.8
            notes.append("近20日主资金净流入")
        elif net_20 < 0:
            score -= 0.8
            notes.append("近20日主资金净流出")
    if large_5 is not None:
        if large_5 > 0:
            score += 0.6
            notes.append("近5日大单与超大单偏净流入")
        elif large_5 < 0:
            score -= 0.6
            notes.append("近5日大单与超大单偏净流出")
    if latest_net is not None and latest_net > 0:
        score += 0.2
    elif latest_net is not None and latest_net < 0:
        score -= 0.2

    final_score = clamp_score(score)
    conclusion = f"资金面{strength_label(final_score)}。"
    if notes:
        conclusion = f"{conclusion} 主要依据：{'、'.join(notes)}。"
    return (
        {
            "资金强弱": strength_label(final_score),
            "结论": conclusion,
            "指标": {
                "最新主力净额": format_signed_yi_from_wanyuan(latest_net),
                "近5日主力净额": format_signed_yi_from_wanyuan(net_5),
                "近20日主力净额": format_signed_yi_from_wanyuan(net_20),
                "近5日大单与超大单净额": format_signed_yi_from_wanyuan(large_5),
                "近10日净流入天数": positive_days,
            },
        },
        final_score,
    )


def summarize_dragon_tiger(top_list_records: list[dict], top_inst_records: list[dict], scanned_days: int, scan_mode: str) -> tuple[dict, int]:
    if scan_mode != "deep":
        return (
            {
                "活跃度": "未扫描",
                "结论": "当前为快档交易观察，默认未扫描龙虎榜；如需补充，请明确说明“深度交易观察”或“龙虎榜/机构席位”。",
                "指标": {
                    "扫描模式": "快档",
                    "扫描交易日数": 0,
                    "上榜次数": 0,
                    "机构席位记录数": 0,
                },
                "明细": {
                    "龙虎榜": [],
                    "机构席位": [],
                },
            },
            3,
        )
    if not top_list_records and not top_inst_records:
        return (
            {
                "活跃度": "一般",
                "结论": f"最近扫描的 {scanned_days} 个交易日内未见明显龙虎榜上榜记录。",
                "指标": {
                    "扫描模式": "深档",
                    "扫描交易日数": scanned_days,
                    "上榜次数": 0,
                    "机构席位记录数": 0,
                },
                "明细": {
                    "龙虎榜": [],
                    "机构席位": [],
                },
            },
            3,
        )

    top_dates = {record.get("trade_date") for record in top_list_records if record.get("trade_date")}
    total_net_amount = sum(to_float(record.get("net_amount")) or 0 for record in top_list_records)
    inst_net_buy = sum(to_float(record.get("net_buy")) or 0 for record in top_inst_records)
    score = 3.0
    notes = [f"最近 {scanned_days} 个交易日上榜 {len(top_dates)} 次"]

    if total_net_amount > 0:
        score += 0.4
        notes.append("榜单净额偏正")
    elif total_net_amount < 0:
        score -= 0.4
        notes.append("榜单净额偏负")
    if inst_net_buy > 0:
        score += 0.6
        notes.append("机构席位偏净买入")
    elif inst_net_buy < 0:
        score -= 0.6
        notes.append("机构席位偏净卖出")

    final_score = clamp_score(score)
    activity = "较高" if len(top_dates) >= 2 else "一般"
    conclusion = f"龙虎榜活跃度{activity}。"
    if notes:
        conclusion = f"{conclusion} 主要依据：{'、'.join(notes)}。"
    return (
        {
            "活跃度": activity,
            "结论": conclusion,
            "指标": {
                "扫描模式": "深档",
                "扫描交易日数": scanned_days,
                "上榜次数": len(top_dates),
                "榜单净额合计": format_yi_from_yuan(total_net_amount),
                "机构席位净买入合计": format_yi_from_yuan(inst_net_buy),
            },
            "明细": {
                "龙虎榜": top_list_records[:5],
                "机构席位": top_inst_records[:5],
            },
        },
        final_score,
    )


def build_trading_risk_flags(
    trend_score: int,
    volume_score: int,
    moneyflow_score: int,
    technical_score: float,
    dragon_summary: dict,
) -> tuple[list[str], str]:
    flags = []
    if trend_score <= 2:
        flags.append("趋势偏弱，短中期价格结构仍需修复。")
    if volume_score <= 2:
        flags.append("量价配合一般，暂未形成明显右侧放量信号。")
    if moneyflow_score <= 2:
        flags.append("资金面偏弱，主力净流向尚未明显转强。")
    if clamp_score(technical_score) <= 2:
        flags.append("技术指标整体偏弱，需观察是否出现进一步钝化。")
    if "机构席位偏净卖出" in dragon_summary.get("结论", ""):
        flags.append("龙虎榜机构席位偏净卖出，短线博弈压力偏大。")

    if not flags:
        flags = ["交易层面暂未看到特别突出的负向信号，但仍需防范短期波动和情绪切换。"]

    risk_level = "中等"
    if len(flags) >= 4:
        risk_level = "偏高"
    elif len(flags) == 1 and "暂未看到" in flags[0]:
        risk_level = "可控"
    return flags, risk_level


def build_risk_flags(valuation_score: int, quality_score: int, growth_score: int, trend_score: int, fina: dict, audit: dict, capital_summary: dict) -> tuple[list[str], str]:
    flags = []
    if valuation_score <= 2:
        flags.append("绝对估值不低，后续回报更依赖业绩兑现。")
    if quality_score <= 2:
        flags.append("财务质量偏弱，需要重点复核盈利质量与负债结构。")
    if growth_score <= 2:
        flags.append("增长动能偏弱，需关注营收和利润增速是否继续下行。")
    if trend_score <= 2:
        flags.append("股价趋势偏弱，短中期交易体验可能一般。")

    ocf_yoy = to_float(fina.get("ocf_yoy"))
    netprofit_yoy = to_float(fina.get("dt_netprofit_yoy") if fina.get("dt_netprofit_yoy") is not None else fina.get("netprofit_yoy"))
    if ocf_yoy is not None and ocf_yoy < -20 and netprofit_yoy is not None and netprofit_yoy > 0:
        flags.append("利润仍在增长，但经营现金流同比下滑较快。")

    audit_result = audit.get("audit_result")
    if audit_result and audit_result != "标准无保留意见":
        flags.append(f"审计意见并非标准无保留：{audit_result}。")

    holder_signal = capital_summary.get("指标", {}).get("近一年重要股东净变动")
    if holder_signal and holder_signal not in {"0.0万股", "暂无"} and "净减持" in capital_summary.get("结论", ""):
        flags.append("近期重要股东存在净减持信号。")

    if not flags:
        flags = ["当前未发现特别突出的硬风险信号，但仍需结合行业景气、政策与估值容忍度判断。"]

    risk_level = "中等"
    if len(flags) >= 4:
        risk_level = "偏高"
    elif len(flags) == 1 and "未发现" in flags[0]:
        risk_level = "可控"

    return flags, risk_level


def merge_risk_levels(levels: list[str]) -> str:
    severity = {"可控": 1, "中等": 2, "偏高": 3}
    if not levels:
        return "中等"
    return max(levels, key=lambda item: severity.get(item, 2))


def build_analysis_bundle(pro, ts_code: str, stock_meta: dict | None, scope: dict) -> dict:
    today = date.today()
    start_90 = (today - timedelta(days=120)).strftime("%Y%m%d")
    start_1y = (today - timedelta(days=420)).strftime("%Y%m%d")
    end_today = today.strftime("%Y%m%d")
    share_end = (today + timedelta(days=365)).strftime("%Y%m%d")
    limitations = []
    endpoint_map = build_endpoint_map()
    used_endpoints = ["stock_basic"]
    trading_depth = scope.get("trading_depth", "quick")

    bundle = {"股票信息": pick_stock_info(ts_code, pro)}

    daily_basic_df = fetch_analysis_df(
        pro,
        endpoint_map,
        "daily_basic",
        lambda: pro.daily_basic(ts_code=ts_code, start_date=start_90, end_date=end_today),
        limitations=limitations,
    )
    if not daily_basic_df.empty:
        used_endpoints.append("daily_basic")
    price_df = fetch_analysis_df(
        pro,
        endpoint_map,
        "pro_bar",
        lambda: ts.pro_bar(api=pro, ts_code=ts_code, asset="E", freq="D", adj="qfq", start_date=start_1y, end_date=end_today),
        limitations=limitations,
    )
    if not price_df.empty:
        used_endpoints.append("pro_bar")

    bundle["daily_basic序列"] = daily_basic_df
    bundle["最新估值"] = latest_record(daily_basic_df, ["trade_date"])
    bundle["价格序列"] = price_df

    if scope.get("fundamental"):
        fina_df = fetch_analysis_df(pro, endpoint_map, "fina_indicator", lambda: pro.fina_indicator(ts_code=ts_code), limitations=limitations)
        income_df = fetch_analysis_df(pro, endpoint_map, "income", lambda: pro.income(ts_code=ts_code), limitations=limitations)
        cashflow_df = fetch_analysis_df(pro, endpoint_map, "cashflow", lambda: pro.cashflow(ts_code=ts_code), limitations=limitations)
        balance_df = fetch_analysis_df(pro, endpoint_map, "balancesheet", lambda: pro.balancesheet(ts_code=ts_code), limitations=limitations)
        audit_df = fetch_analysis_df(pro, endpoint_map, "fina_audit", lambda: pro.fina_audit(ts_code=ts_code), limitations=limitations)
        holders_df = fetch_analysis_df(pro, endpoint_map, "top10_holders", lambda: pro.top10_holders(ts_code=ts_code), limitations=limitations)
        holdertrade_df = fetch_analysis_df(
            pro,
            endpoint_map,
            "stk_holdertrade",
            lambda: pro.stk_holdertrade(ts_code=ts_code, start_date=(today - timedelta(days=365)).strftime("%Y%m%d"), end_date=end_today),
            limitations=limitations,
        )
        repurchase_df = fetch_analysis_df(pro, endpoint_map, "repurchase", lambda: pro.repurchase(ts_code=ts_code), limitations=limitations)
        share_float_df = fetch_analysis_df(
            pro,
            endpoint_map,
            "share_float",
            lambda: pro.share_float(ts_code=ts_code, start_date=(today - timedelta(days=180)).strftime("%Y%m%d"), end_date=share_end),
            limitations=limitations,
        )
        used_endpoints.extend(
            [
                api_name
                for api_name, df in [
                    ("fina_indicator", fina_df),
                    ("income", income_df),
                    ("cashflow", cashflow_df),
                    ("balancesheet", balance_df),
                    ("fina_audit", audit_df),
                    ("top10_holders", holders_df),
                    ("stk_holdertrade", holdertrade_df),
                    ("repurchase", repurchase_df),
                    ("share_float", share_float_df),
                ]
                if not df.empty
            ]
        )
        bundle["最新财务指标"] = latest_record(fina_df, ["ann_date", "end_date"])
        bundle["上期财务指标"] = clean_record(fina_df.sort_values(["ann_date", "end_date"], ascending=False).iloc[1].to_dict()) if len(fina_df.index) > 1 else {}
        bundle["最新利润表"] = latest_record(income_df, ["ann_date", "end_date"])
        bundle["最新现金流"] = latest_record(cashflow_df, ["ann_date", "end_date"])
        bundle["最新资产负债表"] = latest_record(balance_df, ["ann_date", "end_date"])
        bundle["最新审计"] = latest_record(audit_df, ["ann_date", "end_date"])
        bundle["十大股东快照"] = select_holder_snapshot(holders_df)
        bundle["近期股东增减持"] = top_records(holdertrade_df, limit=5, sort_cols=["ann_date"])
        bundle["近期回购"] = top_records(repurchase_df, limit=5, sort_cols=["ann_date", "end_date"])
        bundle["近期解禁"] = top_records(share_float_df, limit=5, sort_cols=["float_date", "ann_date"])
    else:
        bundle["最新财务指标"] = {}
        bundle["上期财务指标"] = {}
        bundle["最新利润表"] = {}
        bundle["最新现金流"] = {}
        bundle["最新资产负债表"] = {}
        bundle["最新审计"] = {}
        bundle["十大股东快照"] = []
        bundle["近期股东增减持"] = []
        bundle["近期回购"] = []
        bundle["近期解禁"] = []

    if scope.get("trading"):
        moneyflow_df = fetch_analysis_df(
            pro,
            endpoint_map,
            "moneyflow",
            lambda: pro.moneyflow(ts_code=ts_code, start_date=(today - timedelta(days=90)).strftime("%Y%m%d"), end_date=end_today),
            limitations=limitations,
        )
        if not moneyflow_df.empty:
            used_endpoints.append("moneyflow")
        top_list_records = []
        top_inst_records = []
        top_list_days = 0
        top_inst_days = 0
        if trading_depth == "deep":
            trade_dates = []
            if not price_df.empty and "trade_date" in price_df.columns:
                trade_dates = [str(item) for item in price_df.sort_values("trade_date", ascending=False)["trade_date"].dropna().head(12).tolist()]
            top_list_records, top_list_days = scan_recent_rank_records(
                pro,
                endpoint_map,
                "top_list",
                ts_code,
                trade_dates,
                limitations=limitations,
                scan_days=12,
                row_limit=5,
            )
            top_inst_records, top_inst_days = scan_recent_rank_records(
                pro,
                endpoint_map,
                "top_inst",
                ts_code,
                trade_dates,
                limitations=limitations,
                scan_days=12,
                row_limit=5,
            )
            if trade_dates:
                used_endpoints.extend(["top_list", "top_inst"])
        bundle["资金流序列"] = moneyflow_df
        bundle["龙虎榜记录"] = top_list_records
        bundle["龙虎榜机构记录"] = top_inst_records
        bundle["龙虎榜扫描天数"] = max(top_list_days, top_inst_days)
        bundle["交易观察深度"] = trading_depth
    else:
        bundle["资金流序列"] = pd.DataFrame()
        bundle["龙虎榜记录"] = []
        bundle["龙虎榜机构记录"] = []
        bundle["龙虎榜扫描天数"] = 0
        bundle["交易观察深度"] = trading_depth

    bundle["数据限制"] = limitations
    bundle["使用接口"] = list(dict.fromkeys(used_endpoints))
    if stock_meta:
        bundle["股票信息"].update({k: v for k, v in stock_meta.items() if v})
    return bundle


def run_analysis_query(text: str, *, limit: int) -> dict:
    pro = init_pro()
    ts_code, stock_meta = resolve_stock_code(text, pro)
    if stock_meta and stock_meta.get("match_type") == "ambiguous_name":
        return {
            "status": "ambiguous",
            "message": "分析请求命中了多个股票名称，请提供更明确的股票代码或名称。",
            "candidates": stock_meta["candidates"],
        }
    if not ts_code:
        return {
            "status": "ambiguous",
            "message": "进行个股分析时，请至少提供一个股票代码或股票名称。",
        }

    scope = infer_analysis_scope(text)
    bundle = build_analysis_bundle(pro, ts_code, stock_meta, scope)
    stock_info = bundle["股票信息"]
    stock_name = stock_info.get("name") or (stock_meta.get("name") if stock_meta else None)
    stock_name = stock_name or ts_code

    trend, trend_score = summarize_trend(bundle["价格序列"])
    valuation = quality = growth = capital = None
    valuation_score = quality_score = growth_score = None
    risk_flags = []
    risk_levels = []
    summary = []

    if scope.get("fundamental"):
        valuation, valuation_score = summarize_valuation(bundle["最新估值"])
        quality, quality_score = summarize_quality(bundle["最新财务指标"], bundle["最新现金流"], bundle["最新审计"])
        growth, growth_score = summarize_growth(bundle["最新财务指标"])
        capital = summarize_capital_actions(bundle["十大股东快照"], bundle["近期股东增减持"], bundle["近期回购"], bundle["近期解禁"])
        fundamental_flags, fundamental_risk = build_risk_flags(
            valuation_score,
            quality_score,
            growth_score,
            trend_score,
            bundle["最新财务指标"],
            bundle["最新审计"],
            capital,
        )
        risk_flags.extend(fundamental_flags)
        risk_levels.append(fundamental_risk)

    technical = volume = moneyflow = dragon_tiger = None
    trading_score = None
    if scope.get("trading"):
        technical = run_indicator_suite(bundle["价格序列"], text)
        volume, volume_score = summarize_volume_profile(bundle["价格序列"], bundle["daily_basic序列"])
        moneyflow, moneyflow_score = summarize_moneyflow(bundle["资金流序列"])
        dragon_tiger, dragon_score = summarize_dragon_tiger(
            bundle["龙虎榜记录"],
            bundle["龙虎榜机构记录"],
            bundle["龙虎榜扫描天数"],
            bundle["交易观察深度"],
        )
        trading_score = round(
            trend_score * 0.25
            + volume_score * 0.2
            + moneyflow_score * 0.25
            + technical["技术评分"] * 0.2
            + dragon_score * 0.1,
            2,
        )
        trading_flags, trading_risk = build_trading_risk_flags(
            trend_score,
            volume_score,
            moneyflow_score,
            technical["技术评分"],
            dragon_tiger,
        )
        risk_flags.extend(trading_flags)
        risk_levels.append(trading_risk)

    if scope.get("fundamental"):
        fundamental_score = round(quality_score * 0.35 + growth_score * 0.25 + trend_score * 0.2 + valuation_score * 0.2, 2)
    else:
        fundamental_score = None

    if fundamental_score is not None and trading_score is not None:
        overall_score = round(fundamental_score * 0.65 + trading_score * 0.35, 2)
        mode_name = "综合分析"
        title = "个股综合分析"
    elif fundamental_score is not None:
        overall_score = fundamental_score
        mode_name = "基本面分析"
        title = "个股基本面分析"
    else:
        overall_score = trading_score if trading_score is not None else trend_score
        mode_name = "交易观察"
        title = "个股交易观察"

    overall_label = strength_label(clamp_score(overall_score))
    summary.append(f"{stock_name}（{ts_code}）{mode_name}判断为{overall_label}，综合评分 {overall_score}/5。")
    if scope.get("fundamental"):
        summary.extend(
            [
                f"估值侧：{valuation['结论']}",
                f"基本面侧：{quality['结论']}",
                f"成长侧：{growth['结论']}",
                f"资本动作：{capital['结论']}",
            ]
        )
    if scope.get("trading"):
        summary.extend(
            [
                f"趋势侧：{trend['结论']}",
                f"量价侧：{volume['结论']}",
                f"资金侧：{moneyflow['结论']}",
                f"龙虎榜侧：{dragon_tiger['结论']}",
            ]
        )
        if technical["指标摘要"]:
            summary.append(f"技术指标：{'；'.join(technical['指标摘要'][:3])}")
        if bundle["交易观察深度"] == "quick":
            summary.append("当前为快档交易观察，默认未做龙虎榜逐日扫描。")

    risk_flags = list(dict.fromkeys(risk_flags))
    risk_level = merge_risk_levels(risk_levels)

    support = {
        "股票信息": {
            "名称": stock_name,
            "ts_code": ts_code,
            "行业": stock_info.get("industry"),
            "地域": stock_info.get("area"),
            "市场": stock_info.get("market"),
            "上市状态": stock_info.get("list_status"),
        },
        "趋势快照": trend["指标"],
    }
    if scope.get("fundamental"):
        support.update(
            {
                "估值快照": valuation["指标"],
                "财务快照": quality["指标"],
                "成长快照": growth["指标"],
                "审计快照": bundle["最新审计"],
                "近期股东增减持": bundle["近期股东增减持"][:limit],
                "近期回购": bundle["近期回购"][:limit],
                "近期解禁": bundle["近期解禁"][:limit],
            }
        )
    if scope.get("trading"):
        support.update(
            {
                "观察深度": "快档" if bundle["交易观察深度"] == "quick" else "深档",
                "量价快照": volume["指标"],
                "资金流快照": moneyflow["指标"],
                "龙虎榜快照": dragon_tiger["指标"],
                "技术指标快照": {name: detail.get("指标", {}) for name, detail in technical["指标明细"].items()},
                "近期龙虎榜": dragon_tiger["明细"]["龙虎榜"][:limit],
                "近期机构席位": dragon_tiger["明细"]["机构席位"][:limit],
            }
        )

    analysis_payload = {
        "分析模式": mode_name,
        "综合评分": overall_score,
        "综合判断": overall_label,
        "风险等级": risk_level,
        "摘要": summary,
        "趋势分析": trend,
    }
    if scope.get("fundamental"):
        analysis_payload.update(
            {
                "基本面评分": fundamental_score,
                "估值分析": valuation,
                "财务质量": quality,
                "成长性": growth,
                "股东与资本动作": capital,
            }
        )
    if scope.get("trading"):
        analysis_payload.update(
            {
                "交易评分": trading_score,
                "交易观察": {
                    "观察深度": "快档" if bundle["交易观察深度"] == "quick" else "深档",
                    "交易判断": strength_label(clamp_score(trading_score)),
                    "量价观察": volume,
                    "资金流观察": moneyflow,
                    "龙虎榜观察": dragon_tiger,
                    "技术指标": technical,
                },
            }
        )
    analysis_payload["风险提示"] = risk_flags
    analysis_payload["数据限制"] = bundle["数据限制"]

    return {
        "status": "ok",
        "endpoint": mode_name,
        "title": title,
        "stock_resolution": {
            "match_type": (stock_meta or {}).get("match_type", "name_match"),
            "name": stock_name,
            "matched_text": (stock_meta or {}).get("matched_text"),
            "ts_code": ts_code,
        },
        "used_endpoints": bundle["使用接口"],
        "analysis": analysis_payload,
        "supporting_data": support,
    }


def fetch_stock_lookup(pro) -> list[dict]:
    cached = load_stock_cache()
    if cached is not None:
        return cached

    frames = []
    for status in ["L", "D", "P"]:
        df = pro.stock_basic(
            exchange="",
            list_status=status,
            fields="ts_code,symbol,name,area,industry,market,list_status,list_date,delist_date,cnspell,fullname",
        )
        if not df.empty:
            frames.append(df)

    if not frames:
        return []
    merged = pd.concat(frames, ignore_index=True).drop_duplicates(subset=["ts_code"])
    merged = merged.fillna("")
    rows = merged.to_dict(orient="records")
    cache_path("stock_basic_cache.json").write_text(json.dumps(rows, ensure_ascii=False), encoding="utf-8")
    return rows


def resolve_stock_code(query: str, pro) -> tuple[str | None, dict | None]:
    explicit = re.search(r"\b(\d{6}(?:\.(?:SH|SZ|BJ))?)\b", query, flags=re.I)
    if explicit:
        code = infer_market_code(explicit.group(1))
        return code, {"match_type": "explicit_code", "name": None}

    stocks = fetch_stock_lookup(pro)
    if not stocks:
        return None, None

    normalized_query = normalize_text(query)
    matches = []
    for row in stocks:
        candidates = [row.get("name", ""), row.get("fullname", ""), row.get("cnspell", "")]
        score = 0
        reason = None
        for candidate in candidates:
            if not candidate:
                continue
            normalized_candidate = normalize_text(candidate)
            if not normalized_candidate:
                continue
            if normalized_candidate in normalized_query:
                score = max(score, 100 + len(normalized_candidate))
                reason = candidate
            elif candidate.lower() in query.lower():
                score = max(score, 95 + len(candidate))
                reason = candidate
            else:
                ratio = SequenceMatcher(None, normalized_query, normalized_candidate).ratio()
                if ratio >= 0.55:
                    fuzzy_score = int(ratio * 50)
                    if fuzzy_score > score:
                        score = fuzzy_score
                        reason = candidate
        if score:
            matches.append((score, row, reason))

    if not matches:
        return None, None
    matches.sort(key=lambda item: item[0], reverse=True)
    top_score, top_row, reason = matches[0]
    if len(matches) > 1 and top_score - matches[1][0] < 8 and top_score < 105:
        return None, {
            "match_type": "ambiguous_name",
            "candidates": [{"ts_code": row["ts_code"], "name": row["name"]} for _, row, _ in matches[:5]],
        }
    return top_row["ts_code"], {"match_type": "name_match", "name": top_row["name"], "matched_text": reason}


def endpoint_aliases(endpoint: dict) -> list[str]:
    aliases = list(endpoint.get("aliases", []))
    aliases.extend(STOCK_ENDPOINT_ALIASES.get(endpoint["api_name"], []))
    return sorted({alias for alias in aliases if alias})


def score_endpoint(query: str, endpoint: dict) -> tuple[int, list[str]]:
    query_norm = normalize_text(query)
    title_norm = normalize_text(endpoint["title"])
    api_name = endpoint["api_name"] or ""
    score = 0
    reasons = []

    if api_name and api_name.lower() in query.lower():
        score += 120
        reasons.append(f"接口代码命中:{api_name}")

    for alias in endpoint_aliases(endpoint):
        alias_norm = normalize_text(alias)
        if not alias_norm:
            continue
        if alias_norm == query_norm:
            score += 100
            reasons.append(f"别名精确匹配:{alias}")
        elif alias_norm in query_norm:
            increment = min(40, 10 + len(alias_norm))
            score += increment
            reasons.append(f"别名命中:{alias}")

    if title_norm and title_norm in query_norm:
        score += 35
        reasons.append("标题命中")

    similarity = SequenceMatcher(None, query_norm, title_norm).ratio() if title_norm else 0
    if similarity > 0.5:
        score += int(similarity * 10)

    if "实时" in query and api_name.startswith("rt_"):
        score += 10
    if "分钟" in query and "min" in api_name:
        score += 8
    if ("周线" in query or "周k" in query.lower()) and api_name == "weekly":
        score += 20
    if ("月线" in query or "月k" in query.lower()) and api_name == "monthly":
        score += 20
    if "复权" in query and ("adj" in api_name or "factor" in api_name):
        score += 10
    if api_name == "pro_bar" and any(term in query for term in ["前复权", "后复权", "不复权", "未复权", "复权行情"]):
        score += 45
    if api_name == "adj_factor" and "复权因子" in query:
        score += 35
    if "股东" in query and "holder" in api_name:
        score += 10
    if "资金流" in query and "moneyflow" in api_name:
        score += 10
    if "龙虎榜" in query and api_name.startswith("top_"):
        score += 15

    return score, reasons


def select_endpoint(query: str, catalog: list[dict]) -> dict:
    best_by_api = {}
    for endpoint in catalog:
        if not endpoint.get("api_name"):
            continue
        score, reasons = score_endpoint(query, endpoint)
        if score > 0:
            similarity = SequenceMatcher(None, normalize_text(query), normalize_text(endpoint["title"])).ratio()
            current = best_by_api.get(endpoint["api_name"])
            if current is None or score > current[0] or (score == current[0] and similarity > current[3]):
                best_by_api[endpoint["api_name"]] = (score, endpoint, reasons, similarity)

    scored = list(best_by_api.values())
    if not scored:
        return {"status": "ambiguous", "message": "没有匹配到明确的 Tushare 股票接口。"}

    scored.sort(key=lambda item: (item[0], item[3]), reverse=True)
    top_score, top_endpoint, reasons, _ = scored[0]
    top_candidates = [
        {
            "api_name": endpoint["api_name"],
            "title": endpoint["title"],
            "score": score,
        }
        for score, endpoint, _, _ in scored[:5]
    ]
    if top_score < 16:
        return {
            "status": "ambiguous",
            "message": "请求过于宽泛，无法安全选择单一股票接口。",
            "candidates": top_candidates,
        }
    if len(scored) > 1 and top_score - scored[1][0] < 6 and top_score < 80:
        return {
            "status": "ambiguous",
            "message": "有多个股票接口都比较匹配，需要进一步澄清。",
            "candidates": top_candidates,
        }
    return {
        "status": "ok",
        "endpoint": top_endpoint,
        "match_reasons": reasons,
        "candidates": top_candidates,
    }


def choose_primary_date_param(input_names: set[str]) -> str | None:
    for name in ["trade_date", "ann_date", "report_date", "period"]:
        if name in input_names:
            return name
    return None


def supports_datetime_range(api_name: str, input_names: set[str]) -> bool:
    return api_name in {"stk_mins", "rt_min", "stk_nineturn"} and {"start_date", "end_date"} <= input_names


def apply_endpoint_specific_params(api_name: str, query: str, params: dict) -> None:
    if api_name in {"stk_mins", "rt_min"}:
        freq_match = re.search(r"(1|5|15|30|60)\s*min", query.lower()) or re.search(r"(1|5|15|30|60)\s*分钟", query)
        freq = freq_match.group(1) if freq_match else "1"
        params["freq"] = f"{freq}MIN" if api_name == "rt_min" else f"{freq}min"

    if api_name == "pro_bar":
        params.setdefault("asset", "E")
        if "周线" in query or "周k" in query.lower():
            params["freq"] = "W"
        elif "月线" in query or "月k" in query.lower():
            params["freq"] = "M"
        elif re.search(r"(1|5|15|30|60)\s*(min|分钟)", query.lower()):
            freq_match = re.search(r"(1|5|15|30|60)\s*(?:min|分钟)", query.lower())
            params["freq"] = f"{freq_match.group(1)}min"
        else:
            params.setdefault("freq", "D")

        if "前复权" in query or "qfq" in query.lower():
            params["adj"] = "qfq"
        elif "后复权" in query or "hfq" in query.lower():
            params["adj"] = "hfq"
        elif "不复权" in query or "未复权" in query:
            params["adj"] = None

    if api_name == "kpl_list":
        if "炸板" in query:
            params["tag"] = "炸板"
        elif "跌停" in query:
            params["tag"] = "跌停"
        elif "自然涨停" in query:
            params["tag"] = "自然涨停"
        elif "竞价" in query:
            params["tag"] = "竞价"
        else:
            params.setdefault("tag", "涨停")


def infer_date_params(endpoint: dict, query: str) -> dict:
    input_names = {item["name"] for item in endpoint.get("input_params", [])}
    api_name = endpoint["api_name"]
    params = {}
    explicit_dates = extract_explicit_dates(query)
    relative_window = parse_relative_window(query)
    quarter_period = extract_quarter_period(query)

    if "period" in input_names and quarter_period:
        params["period"] = quarter_period
        return params

    if relative_window and {"start_date", "end_date"} <= input_names:
        start_day, end_day = relative_window
        params["start_date"] = date_to_str(start_day, time_like=supports_datetime_range(api_name, input_names))
        params["end_date"] = date_to_str(end_day, time_like=supports_datetime_range(api_name, input_names))
        return params

    if len(explicit_dates) >= 2 and {"start_date", "end_date"} <= input_names:
        start_day, end_day = sorted(explicit_dates[:2])
        params["start_date"] = date_to_str(start_day, time_like=supports_datetime_range(api_name, input_names))
        params["end_date"] = date_to_str(end_day, time_like=supports_datetime_range(api_name, input_names))
        return params

    if explicit_dates:
        primary = choose_primary_date_param(input_names)
        if primary:
            if primary == "period":
                params["period"] = explicit_dates[0].strftime("%Y%m%d")
            else:
                params[primary] = date_to_str(explicit_dates[0], time_like=supports_datetime_range(api_name, input_names))
            return params

    if api_name == "stk_mins" and {"start_date", "end_date"} <= input_names:
        end_day = date.today()
        start_day = end_day - timedelta(days=5)
        params["start_date"] = date_to_str(start_day, time_like=True)
        params["end_date"] = date_to_str(end_day, time_like=True)
    return params


def should_require_selector(endpoint: dict) -> bool:
    safe_without_selector = {
        "stock_basic",
        "trade_cal",
        "namechange",
        "stock_company",
        "stk_managers",
        "stk_rewards",
        "new_share",
        "hsgt_top10",
        "ggt_top10",
        "ggt_daily",
        "ggt_monthly",
        "moneyflow_hsgt",
        "ths_index",
        "dc_index",
        "tdx_index",
        "hm_list",
    }
    return endpoint["api_name"] not in safe_without_selector


def build_params(endpoint: dict, query: str, pro) -> tuple[dict, dict]:
    params = infer_date_params(endpoint, query)
    apply_endpoint_specific_params(endpoint["api_name"], query, params)

    input_names = {item["name"] for item in endpoint.get("input_params", [])}
    stock_code = None
    stock_meta = None
    if "ts_code" in input_names:
        stock_code, stock_meta = resolve_stock_code(query, pro)
        if stock_meta and stock_meta.get("match_type") == "ambiguous_name":
            return {}, {"status": "ambiguous_stock", **stock_meta}
        if stock_code:
            params["ts_code"] = stock_code

    if should_require_selector(endpoint):
        has_selector = any(name in params for name in ["ts_code", "trade_date", "ann_date", "period", "report_date", "start_date", "end_date"])
        if not has_selector and endpoint["api_name"] not in {"rt_k", "top_list", "top_inst", "kpl_list", "ths_hot", "dc_hot"}:
            return {}, {
                "status": "need_selector",
                "message": "该接口通常需要股票代码或日期条件，避免返回范围过大。",
            }

    return params, {"status": "ok", "stock_meta": stock_meta}


def gating_decision(endpoint: dict, user_points: int = DEFAULT_USER_POINTS) -> dict:
    access = endpoint.get("access") or {}
    note = endpoint.get("access_note")
    if endpoint.get("inactive"):
        return {
            "allowed": False,
            "reason": "inactive",
            "message": "该接口在 Tushare 文档中标记为停用或暂停。",
            "access_note": note,
        }

    if access.get("requires_extra_permission"):
        return {
            "allowed": False,
            "reason": "extra_permission",
            "message": "该接口需要额外权限或单独开通。",
            "access_note": note,
        }

    formal = access.get("formal_min_points")
    trial = access.get("trial_points")
    if formal is not None and formal <= user_points:
        return {"allowed": True, "tier": "formal", "access_note": note}
    if trial is not None and trial <= user_points:
        return {
            "allowed": True,
            "tier": "trial",
            "warning": "按当前积分层级，该接口大概率只能以试用权限访问。",
            "access_note": note,
        }
    if formal is not None and formal > user_points:
        return {
            "allowed": False,
            "reason": "points",
            "message": f"该接口至少需要 {formal} 积分；当前按 {user_points} 积分处理。",
            "access_note": note,
        }
    return {"allowed": True, "tier": "unknown", "access_note": note}


def clean_value(value):
    if isinstance(value, float) and math.isnan(value):
        return None
    if pd.isna(value):
        return None
    return value


def dataframe_to_rows(df: pd.DataFrame, limit: int) -> dict:
    if df.empty:
        return {"row_count": 0, "rows": [], "truncated": False, "fields": list(df.columns)}
    subset = df.head(limit).copy()
    subset = subset.where(pd.notna(subset), None)
    rows = []
    for record in subset.to_dict(orient="records"):
        rows.append({key: clean_value(value) for key, value in record.items()})
    return {
        "row_count": len(df.index),
        "rows": rows,
        "truncated": len(df.index) > limit,
        "fields": list(df.columns),
    }


def call_endpoint(pro, endpoint: dict, params: dict) -> pd.DataFrame:
    api_name = endpoint["api_name"]
    clean_params = {key: value for key, value in params.items() if value is not None}
    if api_name == "pro_bar":
        return ts.pro_bar(api=pro, **clean_params)
    method = getattr(pro, api_name, None)
    if callable(method):
        return method(**clean_params)
    return pro.query(api_name, **clean_params)


def run_query(text: str, *, limit: int) -> dict:
    if is_analysis_request(text):
        return run_analysis_query(text, limit=limit)

    catalog = load_catalog()
    chosen = select_endpoint(text, catalog)
    if chosen["status"] != "ok":
        return chosen

    endpoint = chosen["endpoint"]
    gate = gating_decision(endpoint)
    if not gate["allowed"]:
        return {
            "status": "gated",
            "endpoint": endpoint["api_name"],
            "title": endpoint["title"],
            "gating": gate,
            "candidates": chosen.get("candidates", []),
        }

    pro = init_pro()
    params, param_meta = build_params(endpoint, text, pro)
    if param_meta["status"] == "ambiguous_stock":
        return {
            "status": "ambiguous",
            "message": "请求中命中了多个股票名称，需要进一步确认。",
            "endpoint": endpoint["api_name"],
            "candidates": param_meta["candidates"],
        }
    if param_meta["status"] == "need_selector":
        return {
            "status": "ambiguous",
            "message": param_meta["message"],
            "endpoint": endpoint["api_name"],
            "title": endpoint["title"],
        }

    try:
        df = call_endpoint(pro, endpoint, params)
    except Exception as exc:
        return {
            "status": "error",
            "message": str(exc),
            "endpoint": endpoint["api_name"],
            "title": endpoint["title"],
            "params": params,
            "gating": gate,
        }

    rows = dataframe_to_rows(df, limit=limit)
    return {
        "status": "ok",
        "endpoint": endpoint["api_name"],
        "title": endpoint["title"],
        "category": endpoint["category"],
        "params": params,
        "gating": gate,
        "match_reasons": chosen.get("match_reasons", []),
        "stock_resolution": param_meta.get("stock_meta"),
        "fields": rows["fields"],
        "row_count": rows["row_count"],
        "truncated": rows["truncated"],
        "rows": rows["rows"],
        "docs_url": endpoint["url"],
    }


def command_catalog(args) -> None:
    catalog = load_catalog()
    output = []
    for item in catalog:
        output.append(
            {
                "category": item["category"],
                "api_name": item["api_name"],
                "title": item["title"],
                "inactive": item["inactive"],
                "access_note": item["access_note"],
                "doc_id": item["doc_id"],
                "url": item["url"],
            }
        )
    print_json({"status": "ok", "count": len(output), "catalog": output})


def command_indicators(args) -> None:
    print_json({"status": "ok", "count": len(list_indicator_specs()), "indicators": list_indicator_specs()})


def parse_key_value(items: list[str]) -> dict:
    params = {}
    for item in items:
        if "=" not in item:
            fail(f"无效的 --param 参数：{item}。格式应为 key=value。")
        key, value = item.split("=", 1)
        params[key] = value
    return params


def command_fetch(args) -> None:
    catalog = load_catalog()
    by_name = {item["api_name"]: item for item in catalog if item.get("api_name")}
    endpoint = by_name.get(args.endpoint)
    if not endpoint:
        fail(f"未知接口：{args.endpoint}")
    gate = gating_decision(endpoint)
    if not gate["allowed"]:
        print_json({"status": "gated", "endpoint": args.endpoint, "gating": gate})
        return
    pro = init_pro()
    params = parse_key_value(args.param or [])
    try:
        df = call_endpoint(pro, endpoint, params)
    except Exception as exc:
        print_json({"status": "error", "endpoint": args.endpoint, "params": params, "message": str(exc)})
        return
    rows = dataframe_to_rows(df, limit=args.limit)
    print_json(
        {
            "status": "ok",
            "endpoint": args.endpoint,
            "title": endpoint["title"],
            "params": params,
            "gating": gate,
            "fields": rows["fields"],
            "row_count": rows["row_count"],
            "truncated": rows["truncated"],
            "rows": rows["rows"],
        }
    )


def command_run(args) -> None:
    result = run_query(args.text, limit=args.limit)
    print_json(result)


def command_analyze(args) -> None:
    result = run_analysis_query(args.text, limit=args.limit)
    print_json(result)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Natural-language Tushare stock access.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    catalog_parser = subparsers.add_parser("catalog", help="List the stock endpoint catalog.")
    catalog_parser.set_defaults(func=command_catalog)

    indicators_parser = subparsers.add_parser("indicators", help="List built-in technical indicators.")
    indicators_parser.set_defaults(func=command_indicators)

    fetch_parser = subparsers.add_parser("fetch", help="Call an endpoint directly.")
    fetch_parser.add_argument("--endpoint", required=True)
    fetch_parser.add_argument("--param", action="append", default=[])
    fetch_parser.add_argument("--limit", type=int, default=20)
    fetch_parser.set_defaults(func=command_fetch)

    run_parser = subparsers.add_parser("run", help="Parse natural language and run the best endpoint.")
    run_parser.add_argument("--text", required=True)
    run_parser.add_argument("--limit", type=int, default=20)
    run_parser.set_defaults(func=command_run)

    analyze_parser = subparsers.add_parser("analyze", help="Run deterministic stock analysis from natural language.")
    analyze_parser.add_argument("--text", required=True)
    analyze_parser.add_argument("--limit", type=int, default=5)
    analyze_parser.set_defaults(func=command_analyze)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
