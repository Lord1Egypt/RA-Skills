#!/usr/bin/env python3
"""Data capability guard for requirement preflight."""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Set


# Baseline capability list from SDK_USER_API.md (documented interfaces).
DOCUMENTED_APIS: Set[str] = {
    #基础数据
    "stock_basic", "stk_premarket", "trade_cal", "stock_st", "st", "stock_hsgt",
    "namechange", "stock_company", "stk_managers", "stk_rewards", "bse_mapping", "new_share", "bak_basic",
    #行情数据
    "stk_mins", "daily", "stk_weekly_monthly", "stk_week_month_adj", "weekly", "monthly",
    "adj_factor", "daily_basic", "stk_limit", "suspend_d", "stk_auction", "stk_auction_o", "stk_auction_c",
    #ETF专题
    "etf_basic", "etf_stk_mins", "fund_adj", "fund_daily", "etf_index", "etf_share_size",
    #公募基金
    "fund_basic", "fund_company", "fund_manager", "fund_share", "fund_nav", "fund_div", "fund_portfolio", "fund_factor_pro",
    #指数专题
    "index_basic", "index_daily", "index_weekly", "index_monthly", "idx_mins", "index_dailybasic",
    "index_weight", "index_classify", "index_member_all", "index_global", "idx_factor_pro",
    "sw_daily", "ci_daily", "daily_info", "sz_daily_info",
    #港股数据
    "hk_basic", "hk_tradecal", "hk_daily", "hk_daily_adj", "hk_adjfactor", "hk_mins",
    #沪深港通
    "hsgt_top10", "ggt_top10", "ggt_daily", "ggt_monthly",
    #财务数据
    "income", "balancesheet", "cashflow", "forecast", "express", "dividend", "fina_indicator", "fina_audit",
    "fina_mainbz", "disclosure_date",
    #股东与机构
    "top10_holders", "top10_floatholders", "pledge_stat", "pledge_detail", "repurchase", "share_float",
    "block_trade", "stk_holdernumber", "stk_holdertrade", "report_rc", "ccass_hold", "ccass_hold_detail", "hk_hold",
    #技术指标与筹码
    "cyq_perf", "cyq_chips", "stk_factor_pro", "stk_nineturn", "stk_ah_comparison",
    #融资融券与资金流向
    "margin_detail", "margin_secs", "margin", "slb_len",
    "moneyflow", "moneyflow_ths", "moneyflow_dc", "moneyflow_cnt_ths", "moneyflow_ind_ths",
    "moneyflow_ind_dc", "moneyflow_mkt_dc", "moneyflow_hsgt",
    #龙虎榜与涨跌停
    "top_list", "top_inst", "limit_list_ths", "limit_list_d", "limit_step", "limit_cpt_list",
    #板块与指数
    "ths_index", "ths_daily", "ths_member", "dc_index", "dc_member", "dc_daily", "tdx_index", "tdx_member", "tdx_daily",
    #利率数据
    "shibor", "shibor_quote", "shibor_lpr", "libor", "hibor", "wz_index", "gz_index",
    #美国利率
    "us_tycr", "us_trycr", "us_tbr", "us_tltr", "us_trltr",
    #宏观经济
    "cn_gdp", "cn_cpi", "cn_ppi", "cn_m", "sf_month", "cn_pmi",
    #资讯与语料
    "research_report", "news", "major_news", "cctv_news", "anns_d", "irm_qa_sh", "irm_qa_sz", "npr",
    #其他
    "stk_surv", "broker_recommend", "hm_list", "hm_detail", "ths_hot", "dc_hot", "kpl_list", "kpl_concept_cons",
}

# Requirement keyword -> expected APIs.
KEYWORD_API_RULES: Dict[str, List[str]] = {
    "分钟": ["stk_mins"],
    "分时": ["stk_mins"],
    "tick": ["stk_mins"],
    "日线": ["daily"],
    "周线": ["weekly"],
    "月线": ["monthly"],
    "复权": ["adj_factor"],
    "财务": ["income", "balancesheet", "cashflow", "fina_indicator"],
    "利润表": ["income"],
    "资产负债": ["balancesheet"],
    "现金流": ["cashflow"],
    "审计": ["fina_audit"],
    "分红": ["dividend"],
    "资金流": ["moneyflow", "moneyflow_ths", "moneyflow_dc"],
    "融资融券": ["margin", "margin_detail"],
    "龙虎榜": ["top_list", "top_inst"],
    "涨停": ["limit_list_d", "stk_limit"],
    "连板": ["limit_step"],
    "板块": ["ths_index", "ths_member", "dc_index", "dc_member", "tdx_index", "tdx_member"],
    "概念": ["ths_index", "ths_member", "dc_index", "dc_member"],
    "行业": ["ths_index", "ths_daily"],
    "指数": ["index_basic", "index_daily", "index_weekly", "index_monthly", "idx_mins", "index_dailybasic"],
    "港股通": ["ggt_daily", "ggt_monthly", "ggt_top10", "hsgt_top10"],
    "港股": ["hk_basic", "hk_daily", "hk_mins"],
    "持股": ["hk_hold", "ccass_hold", "ccass_hold_detail"],
    "机构调研": ["stk_surv"],
    "热榜": ["ths_hot", "dc_hot"],
    "ETF": ["etf_basic", "fund_daily", "etf_stk_mins"],
    "基金": ["fund_basic", "fund_nav", "fund_daily", "fund_portfolio"],
    "净值": ["fund_nav"],
    "GDP": ["cn_gdp"],
    "CPI": ["cn_cpi"],
    "PPI": ["cn_ppi"],
    "宏观": ["cn_gdp", "cn_cpi", "cn_ppi", "cn_m", "cn_pmi"],
    "PMI": ["cn_pmi"],
    "利率": ["shibor", "shibor_lpr", "libor", "hibor"],
    "新闻": ["news", "major_news", "cctv_news"],
    "研报": ["research_report"],
    "公告": ["anns_d"],
    "互动易": ["irm_qa_sh", "irm_qa_sz"],
    "申万": ["sw_daily"],
    "权重": ["index_weight"],
    "美债": ["us_tycr", "us_trycr"],
}

# Keywords that usually imply out-of-scope or ambiguous requirement.
from qg_constants import QGDATA_RECHARGE_URL, QGDATA_SHARED_TOKEN, classify_qgdata_error

UNSUPPORTED_HINTS: Dict[str, str] = {
    "期权": "当前编排器默认股票策略，期权需要单独执行链路。",
    "期货": "当前编排器默认股票策略，期货需要单独执行链路。",
    "舆情": "无社交媒体情绪分析API，建议用热榜/资金流代理指标或接入外部源。",
}


def list_runtime_apis() -> tuple[Set[str], str]:
    """返回 (可用API集合, 警告信息)。警告非空表示Token问题。"""
    token = os.getenv("QGDATA_TOKEN", "")
    if not token:
        return set(), f"未配置QGDATA_TOKEN，使用文档声明的API列表。获取Token: {QGDATA_RECHARGE_URL}"
    try:
        import qgdata as qg  # type: ignore
        qg.set_token(token)
        pro = qg.pro_api(timeout=10.0)
        apis = pro.list_apis(enabled_only=True)
        if isinstance(apis, list):
            return {str(x) for x in apis}, ""
        if isinstance(apis, dict):
            return {str(k) for k in apis.keys()}, ""
    except Exception as exc:
        _, user_msg = classify_qgdata_error(exc)
        return set(), f"qgdata API能力探测失败: {user_msg}"
    return set(), ""


@dataclass
class CapabilityResult:
    ok: bool
    status: str
    required_apis: List[str]
    missing_apis: List[str]
    matched_rules: List[str]
    unsupported_reasons: List[str]
    suggestion: str
    token_hint: str = ""

    def to_dict(self) -> Dict[str, Any]:
        d = {
            "ok": self.ok,
            "status": self.status,
            "required_apis": self.required_apis,
            "missing_apis": self.missing_apis,
            "matched_rules": self.matched_rules,
            "unsupported_reasons": self.unsupported_reasons,
            "suggestion": self.suggestion,
        }
        if self.token_hint: d["token_hint"] = self.token_hint
        return d


_PORTFOLIO_STRONG = {"轮动", "组合", "多标的", "全市场", "等权", "仓位分配"}
_PORTFOLIO_WEAK = {"排序", "筛选", "选股", "调仓", "排列", "持仓周期"}
_PORTFOLIO_CTX = {"板块", "成分股", "指数", "行业", "概念", "股票池"}
_PROJECT_ROOT = Path(__file__).resolve().parents[1]

def _looks_portfolio(text: str) -> bool:
    if any(kw in text for kw in _PORTFOLIO_STRONG): return True
    if re.search(r'前\s*\d+\s*名', text): return True
    return any(kw in text for kw in _PORTFOLIO_WEAK) and any(kw in text for kw in _PORTFOLIO_CTX)

def _read_env_value_from_files(key: str, candidates: list[Path]) -> str:
    for path in candidates:
        if not path.exists(): continue
        try:
            for line in path.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line: continue
                k, v = line.split("=", 1)
                if k.strip() == key: return v.strip().strip('"').strip("'")
        except Exception:
            continue
    return ""

def _token_context() -> str:
    env_tok = (os.getenv("QGDATA_TOKEN", "") or _read_env_value_from_files("QGDATA_TOKEN", [_PROJECT_ROOT / ".env", Path.home() / ".openclaw" / ".env", Path("/opt/.env")])).strip()
    if not env_tok: return "missing" #未传token，将回退共享token
    if env_tok == QGDATA_SHARED_TOKEN: return "shared"
    return "personal"

def evaluate_requirement(requirement: str) -> CapabilityResult:
    text = requirement.lower()
    required: Set[str] = set()
    matched_rules: List[str] = []
    for keyword, apis in KEYWORD_API_RULES.items():
        if keyword.lower() in text:
            required.update(apis)
            matched_rules.append(keyword)

    unsupported: List[str] = []
    for keyword, reason in UNSUPPORTED_HINTS.items():
        if keyword.lower() in text:
            unsupported.append(f"{keyword}: {reason}")

    runtime_apis, token_warn = list_runtime_apis()
    available = runtime_apis if runtime_apis else DOCUMENTED_APIS
    missing = sorted(api for api in required if api not in available)

    token_hint = ""
    _tok_ctx = _token_context()
    if _looks_portfolio(requirement) and _tok_ctx != "personal":
        token_hint = f"Portfolio策略需下载多只标的数据，API调用量较大。当前未传Token（将使用共享试用Token）或正在使用共享试用Token，每日调用频次有限，多标的回测可能因频率限制中断。建议前往 {QGDATA_RECHARGE_URL} 获取个人Token（免费注册即可提升频率上限）。"

    if unsupported:
        return CapabilityResult(
            ok=False, status="unsupported", required_apis=sorted(required), missing_apis=missing,
            matched_rules=matched_rules, unsupported_reasons=unsupported,
            suggestion="请先改写需求为股票+文档内可用数据接口，或扩展数据源后再执行。", token_hint=token_hint,
        )

    if missing:
        sug = f"当前需求依赖的部分数据接口不可用({', '.join(missing)})。请调整需求，或到 {QGDATA_RECHARGE_URL} 升级套餐启用缺失接口。"
        return CapabilityResult(
            ok=False, status="clarification_needed", required_apis=sorted(required), missing_apis=missing,
            matched_rules=matched_rules, unsupported_reasons=[token_warn] if token_warn else [],
            suggestion=sug, token_hint=token_hint,
        )

    return CapabilityResult(
        ok=True, status="ok", required_apis=sorted(required), missing_apis=[],
        matched_rules=matched_rules, unsupported_reasons=[token_warn] if token_warn else [],
        suggestion="数据能力检查通过，可启动编排。" + (f" 注意: {token_warn}" if token_warn else ""), token_hint=token_hint,
    )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="QGData capability preflight")
    parser.add_argument("--requirement", required=True)
    args = parser.parse_args()
    print(json.dumps(evaluate_requirement(args.requirement).to_dict(), ensure_ascii=False, indent=2))
