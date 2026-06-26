#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from billing import BillingError, build_billing_client  # noqa: E402
from web3_client import BinanceWeb3Client, BinanceWeb3Error, CHAIN_ALIASES  # noqa: E402


TEXT = {
    "zh": {
        "title": "Token Risk Explainer",
        "low": "低风险",
        "medium": "中风险",
        "high": "高风险",
        "critical": "极高风险",
        "continue_yes": "可以继续研究，但仍需人工复核。",
        "continue_no": "不建议直接推进，先排除明显风险项。",
        "community_prefix": "社群预警",
        "square_prefix": "广场提示",
        "disclaimer": "仅供风险解释与研究参考，不构成投资建议。",
    },
    "en": {
        "title": "Token Risk Explainer",
        "low": "Low risk",
        "medium": "Medium risk",
        "high": "High risk",
        "critical": "Critical risk",
        "continue_yes": "Continue research if needed, but keep manual review in the loop.",
        "continue_no": "Do not move forward blindly. Resolve major risk flags first.",
        "community_prefix": "Community alert",
        "square_prefix": "Square post",
        "disclaimer": "For risk explanation and research only. Not investment advice.",
    },
}

FACTOR_COPY = {
    "top10": {
        "zh": "前十持仓集中度偏高，筹码分布不够分散。",
        "en": "Top-10 holder concentration is elevated, so supply looks less distributed.",
    },
    "dev": {
        "zh": "开发者持仓占比较高，存在集中控制风险。",
        "en": "Developer holding share is elevated, which raises centralization risk.",
    },
    "sniper": {
        "zh": "狙击地址占比较高，短线抛压风险更大。",
        "en": "Sniper participation is elevated, which can increase short-term dump risk.",
    },
    "insider": {
        "zh": "内部地址占比较高，需警惕信息不对称。",
        "en": "Insider share is elevated, so information asymmetry risk is higher.",
    },
    "bundler": {
        "zh": "打包地址占比较高，持仓结构不够自然。",
        "en": "Bundler share is elevated, suggesting a less organic holder structure.",
    },
    "liquidity": {
        "zh": "流动性偏低，大额进出更容易滑点。",
        "en": "Liquidity is thin, so larger trades may face heavier slippage.",
    },
    "tax": {
        "zh": "买卖税偏高，交易成本明显增加。",
        "en": "Buy or sell tax is elevated, increasing trading friction materially.",
    },
    "unverified": {
        "zh": "合约未验证，透明度不足。",
        "en": "Contract is not verified, which reduces transparency.",
    },
    "audit_hits": {
        "zh": "审计命中风险项，建议逐条复核。",
        "en": "Audit reported active risk findings. Review each hit before moving on.",
    },
    "missing_social": {
        "zh": "公开链接不足，项目外部可验证信息偏少。",
        "en": "Public links are missing, leaving less external context to verify.",
    },
}


class AppError(RuntimeError):
    pass


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _json_print(payload: Dict[str, Any]) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def to_float(value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def risk_bucket(score: int) -> str:
    if score >= 75:
        return "critical"
    if score >= 50:
        return "high"
    if score >= 25:
        return "medium"
    return "low"


def flatten_audit_hits(audit: Dict[str, Any]) -> List[str]:
    hits: List[str] = []
    for item in audit.get("riskItems", []) or []:
        if not isinstance(item, dict):
            continue
        for detail in item.get("details", []) or []:
            if isinstance(detail, dict) and detail.get("isHit"):
                title = detail.get("title")
                if isinstance(title, str) and title:
                    hits.append(title)
    return hits


def build_risk_factors(token: Dict[str, Any], audit: Dict[str, Any], meta: Dict[str, Any]) -> List[Dict[str, Any]]:
    factors: List[Dict[str, Any]] = []

    def add_factor(code: str, severity: str, value: Any) -> None:
        factors.append(
            {
                "code": code,
                "severity": severity,
                "value": value,
                "explanation_zh": FACTOR_COPY[code]["zh"],
                "explanation_en": FACTOR_COPY[code]["en"],
            }
        )

    top10 = to_float(token.get("holdersTop10Percent"))
    dev = to_float(token.get("holdersDevPercent"))
    sniper = to_float(token.get("holdersSniperPercent"))
    insider = to_float(token.get("holdersInsiderPercent"))
    bundler = to_float(token.get("bundlerHoldingPercent"))
    liquidity = to_float(token.get("liquidity"))
    extra = audit.get("extraInfo", {}) or {}
    buy_tax = to_float(extra.get("buyTax"))
    sell_tax = to_float(extra.get("sellTax"))
    hits = flatten_audit_hits(audit)

    if top10 >= 65:
        add_factor("top10", "high" if top10 >= 80 else "medium", round(top10, 2))
    if dev >= 5:
        add_factor("dev", "high" if dev >= 10 else "medium", round(dev, 2))
    if sniper >= 8:
        add_factor("sniper", "high" if sniper >= 15 else "medium", round(sniper, 2))
    if insider >= 8:
        add_factor("insider", "high" if insider >= 15 else "medium", round(insider, 2))
    if bundler >= 20:
        add_factor("bundler", "medium", round(bundler, 2))
    if 0 < liquidity < 20_000:
        add_factor("liquidity", "high" if liquidity < 5_000 else "medium", round(liquidity, 2))
    if max(buy_tax, sell_tax) > 5:
        add_factor("tax", "high" if max(buy_tax, sell_tax) > 10 else "medium", max(buy_tax, sell_tax))
    if extra.get("isVerified") is False:
        add_factor("unverified", "medium", False)
    if hits:
        add_factor("audit_hits", "high", hits[:3])
    if not (meta.get("links", []) or []):
        add_factor("missing_social", "low", 0)
    return factors


def calculate_risk_score(factors: List[Dict[str, Any]]) -> int:
    weights = {"low": 6, "medium": 12, "high": 20}
    return min(sum(weights.get(item["severity"], 0) for item in factors), 100)


def build_drafts(display: str, risk_level_en: str, continue_research: bool) -> Dict[str, str]:
    next_step_zh = "建议继续观察和人工复核。" if continue_research else "建议先暂停推进并继续核查。"
    next_step_en = "Continue manual review." if continue_research else "Pause and investigate further first."
    community_zh = f"{TEXT['zh']['community_prefix']}：{display} 当前风险级别为 {risk_level_en}。{next_step_zh}"
    community_en = f"{TEXT['en']['community_prefix']}: {display} is currently rated {risk_level_en}. {next_step_en}"
    square_zh = f"{TEXT['zh']['square_prefix']}：{display} 的风险解释已更新，当前更适合先做风控复核，再决定是否继续研究。"
    square_en = f"{TEXT['en']['square_prefix']}: Risk explanation for {display} is updated. Review risk before taking the next research step."
    return {"community_alert_draft": f"{community_zh}\n{community_en}", "square_post_draft": f"{square_zh}\n{square_en}"}


def maybe_bill(call_name: str, user_ref: str, skip_billing: bool) -> Dict[str, Any]:
    if skip_billing:
        return {"ok": True, "code": "skipped", "message": "billing skipped"}
    client = build_billing_client()
    amount = os.getenv("SKILLPAY_PRICE_USDT", "0.01").strip() or "0.01"
    result = client.charge(call_name, amount, user_ref, str(uuid4()))
    if not result.ok:
        raise BillingError(f"billing_failed:{result.code}:{result.message}")
    return result.to_dict()


def explain_token(client: BinanceWeb3Client, chain: str, query: str, lang: str) -> Dict[str, Any]:
    chain_id = CHAIN_ALIASES[chain]
    resolved = client.resolve_token(chain_id, query)
    contract = str(resolved.get("contractAddress") or query).strip()
    if not contract:
        raise AppError("missing_contract")

    token = resolved if resolved.get("symbol") else {"symbol": "", "name": "", "contractAddress": contract}
    try:
        meta = client.token_meta(chain_id, contract)
    except BinanceWeb3Error:
        meta = {}
    try:
        audit = client.token_audit(chain_id, contract)
    except BinanceWeb3Error:
        audit = {"hasResult": False, "isSupported": False, "riskItems": [], "extraInfo": {}}

    symbol = str(token.get("symbol") or meta.get("symbol") or meta.get("name") or query)
    display = f"{symbol} | {contract}"
    factors = build_risk_factors(token, audit, meta)
    score = calculate_risk_score(factors)
    bucket = risk_bucket(score)
    continue_research = score < 60
    drafts = build_drafts(display, TEXT["en"][bucket], continue_research)
    hits = flatten_audit_hits(audit)
    risk_summary_zh = f"{display} 当前风险级别为 {TEXT['zh'][bucket]}。主要风险数量：{len(factors)}。"
    risk_summary_en = f"{display} is currently rated {TEXT['en'][bucket]}. Visible risk factors: {len(factors)}."

    return {
        "token": symbol,
        "display_token": display,
        "contract_address": contract,
        "chain": chain,
        "risk_score": score,
        "risk_level": {"zh": TEXT["zh"][bucket], "en": TEXT["en"][bucket]},
        "risk_summary_zh": risk_summary_zh,
        "risk_summary_en": risk_summary_en,
        "risk_factors": factors,
        "audit_hits": hits,
        "links": meta.get("links", []),
        "continue_research": continue_research,
        "continue_research_zh": TEXT["zh"]["continue_yes"] if continue_research else TEXT["zh"]["continue_no"],
        "continue_research_en": TEXT["en"]["continue_yes"] if continue_research else TEXT["en"]["continue_no"],
        **drafts,
        "lang": lang,
    }


def cmd_explain(args: argparse.Namespace) -> None:
    user_ref = args.user_id or os.getenv("SKILLPAY_USER_REF", "anonymous").strip() or "anonymous"
    client = BinanceWeb3Client()
    token = explain_token(client, chain=args.chain, query=args.contract or args.symbol, lang=args.lang)
    billing = maybe_bill("explain", user_ref=user_ref, skip_billing=args.skip_billing)
    _json_print(
        {
            "title": TEXT[args.lang]["title"],
            "generated_at_utc": utc_now(),
            "billing": billing,
            "token_report": token,
            "disclaimer": TEXT[args.lang]["disclaimer"],
        }
    )


def cmd_compare(args: argparse.Namespace) -> None:
    queries = [item.strip() for item in args.contracts.split(",") if item.strip()]
    if len(queries) < 2:
        raise AppError("compare_requires_at_least_two_contracts")
    user_ref = args.user_id or os.getenv("SKILLPAY_USER_REF", "anonymous").strip() or "anonymous"
    client = BinanceWeb3Client()
    reports = [explain_token(client, chain=args.chain, query=item, lang=args.lang) for item in queries]
    reports.sort(key=lambda item: item["risk_score"], reverse=True)
    billing = maybe_bill("compare", user_ref=user_ref, skip_billing=args.skip_billing)
    _json_print(
        {
            "title": TEXT[args.lang]["title"],
            "generated_at_utc": utc_now(),
            "chain": args.chain,
            "billing": billing,
            "comparison": reports,
            "highest_risk_token": reports[0]["display_token"],
            "disclaimer": TEXT[args.lang]["disclaimer"],
        }
    )


def cmd_watchlist(args: argparse.Namespace) -> None:
    queries: List[str] = []
    if args.contracts:
        queries.extend(item.strip() for item in args.contracts.split(",") if item.strip())
    if args.input:
        queries.extend(line.strip() for line in Path(args.input).read_text(encoding="utf-8").splitlines() if line.strip())
    if not queries:
        raise AppError("watchlist_requires_contracts_or_input")
    user_ref = args.user_id or os.getenv("SKILLPAY_USER_REF", "anonymous").strip() or "anonymous"
    client = BinanceWeb3Client()
    reports = [explain_token(client, chain=args.chain, query=item, lang=args.lang) for item in queries]
    reports.sort(key=lambda item: item["risk_score"], reverse=True)
    billing = maybe_bill("watchlist", user_ref=user_ref, skip_billing=args.skip_billing)
    _json_print(
        {
            "title": TEXT[args.lang]["title"],
            "generated_at_utc": utc_now(),
            "chain": args.chain,
            "billing": billing,
            "watchlist": reports,
            "disclaimer": TEXT[args.lang]["disclaimer"],
        }
    )


def cmd_health(_: argparse.Namespace) -> None:
    _json_print({"ok": True, "service": "token-risk-explainer-skill", "generated_at_utc": utc_now(), "billing_mode": os.getenv("SKILLPAY_BILLING_MODE", "skillpay")})


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Token Risk Explainer")
    subparsers = parser.add_subparsers(dest="command", required=True)

    explain = subparsers.add_parser("explain", help="Explain a token's risk profile")
    explain.add_argument("--chain", choices=sorted(CHAIN_ALIASES), default="bsc")
    explain.add_argument("--contract", default="")
    explain.add_argument("--symbol", default="")
    explain.add_argument("--lang", choices=("zh", "en"), default="zh")
    explain.add_argument("--user-id", default="")
    explain.add_argument("--skip-billing", action="store_true")
    explain.set_defaults(func=cmd_explain)

    compare = subparsers.add_parser("compare", help="Compare multiple token contracts")
    compare.add_argument("--chain", choices=sorted(CHAIN_ALIASES), default="bsc")
    compare.add_argument("--contracts", required=True)
    compare.add_argument("--lang", choices=("zh", "en"), default="zh")
    compare.add_argument("--user-id", default="")
    compare.add_argument("--skip-billing", action="store_true")
    compare.set_defaults(func=cmd_compare)

    watchlist = subparsers.add_parser("watchlist", help="Rank a watchlist by visible risk")
    watchlist.add_argument("--chain", choices=sorted(CHAIN_ALIASES), default="bsc")
    watchlist.add_argument("--contracts", default="")
    watchlist.add_argument("--input", default="")
    watchlist.add_argument("--lang", choices=("zh", "en"), default="zh")
    watchlist.add_argument("--user-id", default="")
    watchlist.add_argument("--skip-billing", action="store_true")
    watchlist.set_defaults(func=cmd_watchlist)

    health = subparsers.add_parser("health", help="Health check")
    health.set_defaults(func=cmd_health)
    return parser


def main(argv: Iterable[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)
    try:
        args.func(args)
        return 0
    except (AppError, BillingError, BinanceWeb3Error) as exc:
        _json_print({"ok": False, "error": str(exc)})
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
