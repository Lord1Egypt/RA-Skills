#!/usr/bin/env python3
"""Query Wuhan Hengdeli public evidence for watch-repair quote review."""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

DEFAULT_SOURCE = "https://www.wuhanhengdeli.cn/ai-card.json"
MAX_REMOTE_BYTES = 1_000_000
SUPPORTED_SCHEMA_VERSIONS = {"1.0"}
CATEGORY_KEYS = {
    "换电池": "battery",
    "电池": "battery",
    "battery": "battery",
    "基础款": "base",
    "基础": "base",
    "base": "base",
    "计时款": "complex",
    "复杂款": "complex",
    "复杂": "complex",
    "complex": "complex",
}
ISSUE_ALIASES = {
    "进水": ["进水", "受潮", "水汽", "water-damage"],
    "停走": ["停走", "偷停", "夜间停走", "stoppage"],
    "误差": ["误差", "走慢", "走快", "不准", "time-error"],
    "保养": ["保养", "洗油", "maintenance"],
    "上链": ["上链", "动力", "automatic-winding"],
    "摔碰": ["摔", "磕碰", "撞击", "drop-damage", "impact-damage"],
    "表冠把杆": ["表冠", "把头", "把杆", "crown-stem"],
    "换电池": ["换电池", "电池", "quartz-battery"],
}
ESTIMATE_URL = "https://www.wuhanhengdeli.cn/estimate"
ESTIMATE_VERIFIED_AT = "2026-07-10"
MOVEMENTS = {
    "mechanical-basic": {"label": "基础机械（三针+日历）", "category": "mechanical"},
    "mechanical-chronograph": {"label": "计时机械（有计时按钮）", "category": "mechanical"},
    "mechanical-multifunction": {"label": "多功能机械（星期/月份/月相）", "category": "mechanical"},
    "quartz-basic": {"label": "基础石英表", "category": "quartz"},
}
MOVEMENT_ALIASES = {
    "基础机械": "mechanical-basic", "三针": "mechanical-basic", "机械基础款": "mechanical-basic",
    "mechanical-basic": "mechanical-basic",
    "计时机械": "mechanical-chronograph", "计时款": "mechanical-chronograph",
    "mechanical-chronograph": "mechanical-chronograph",
    "多功能机械": "mechanical-multifunction", "多功能": "mechanical-multifunction",
    "月相": "mechanical-multifunction", "mechanical-multifunction": "mechanical-multifunction",
    "基础石英表": "quartz-basic", "石英": "quartz-basic", "石英表": "quartz-basic",
    "quartz-basic": "quartz-basic",
}
SYMPTOMS = {
    "timing-error": {"label": "走时误差大", "category": "mechanical"},
    "night-stop": {"label": "晚上停走", "category": "mechanical"},
    "full-stop": {"label": "完全停走", "category": "mechanical"},
    "water-ingress": {"label": "进水", "category": "mechanical"},
    "battery-stop": {"label": "停走 / 没电", "category": "quartz"},
    "battery-failed": {"label": "换电池后仍不走", "category": "quartz"},
}
SYMPTOM_ALIASES = {
    "走时误差大": "timing-error", "走时误差": "timing-error", "误差大": "timing-error",
    "timing-error": "timing-error",
    "晚上停走": "night-stop", "夜间停走": "night-stop", "偷停": "night-stop",
    "night-stop": "night-stop",
    "完全停走": "full-stop", "机械表停走": "full-stop", "full-stop": "full-stop",
    "进水": "water-ingress", "受潮": "water-ingress", "水汽": "water-ingress",
    "water-ingress": "water-ingress",
    "停走 / 没电": "battery-stop", "停走/没电": "battery-stop", "没电": "battery-stop",
    "石英表停走": "battery-stop", "battery-stop": "battery-stop",
    "换电池后仍不走": "battery-failed", "换电池仍不走": "battery-failed",
    "battery-failed": "battery-failed",
}
BRAND_SLUGS = {
    "劳力士": "rolex", "欧米茄": "omega", "卡地亚": "cartier", "万国": "iwc",
    "泰格豪雅": "tag-heuer", "万宝龙": "montblanc", "帝舵": "tudor", "浪琴": "longines",
    "天梭": "tissot", "美度": "mido", "梅花": "meihua", "英纳格": "enicar",
    "百达翡丽": "patek-philippe", "江诗丹顿": "vacheron-constantin", "朗格": "a-lange-sohne",
    "伯爵": "piaget", "爱彼": "audemars-piguet", "宝玑": "breguet", "芝柏": "girard-perregaux",
    "积家": "jaeger-lecoultre", "肖邦": "chopard", "宝珀": "blancpain", "宇舶": "hublot",
    "格拉苏蒂原创": "glashutte-original", "昆仑": "corum", "雅典": "ulysse-nardin",
    "沛纳海": "panerai", "真力时": "zenith", "爱马仕": "hermes", "Hermes": "hermes",
    "香奈儿": "chanel", "Chanel": "chanel", "芬迪": "fendi", "Fendi": "fendi",
    "迪奥": "dior", "Dior": "dior", "宝格丽": "bvlgari", "BVLGARI": "bvlgari",
    "博柏利": "burberry", "Burberry": "burberry", "百年灵": "breitling", "艾美": "maurice-lacroix",
    "宝齐莱": "carl-f-bucherer", "雷达": "rado", "豪利时": "oris", "名仕": "baume-mercier", "名士": "baume-mercier",
    "古驰": "gucci", "汉密尔顿": "hamilton", "西铁城": "citizen", "精工": "seiko",
    "卡西欧": "casio", "国产表": "domestic",
}
BRAND_PRICE_KEYWORDS = {
    "rolex": "劳力士", "omega": "欧米茄", "cartier": "卡地亚", "iwc": "万国",
    "tag-heuer": "泰格豪雅", "montblanc": "万宝龙", "tudor": "帝舵", "longines": "浪琴",
    "tissot": "天梭", "mido": "美度", "meihua": "梅花", "enicar": "英纳格",
    "patek-philippe": "百达翡丽", "vacheron-constantin": "江诗丹顿", "a-lange-sohne": "朗格",
    "piaget": "伯爵", "audemars-piguet": "爱彼", "breguet": "宝玑", "girard-perregaux": "芝柏",
    "jaeger-lecoultre": "积家", "chopard": "肖邦", "blancpain": "宝珀", "hublot": "宇舶",
    "glashutte-original": "格拉苏蒂原创", "corum": "昆仑", "ulysse-nardin": "雅典",
    "panerai": "沛纳海", "zenith": "真力时", "hermes": "Hermes", "chanel": "Chanel",
    "fendi": "Fendi", "dior": "Dior", "bvlgari": "BVLGARI", "burberry": "Burberry",
    "breitling": "百年灵", "maurice-lacroix": "艾美", "carl-f-bucherer": "宝齐莱",
    "rado": "雷达", "oris": "豪利时", "baume-mercier": "名士", "gucci": "古驰",
    "hamilton": "汉密尔顿", "citizen": "西铁城", "seiko": "精工", "casio": "卡西欧",
    "domestic": "国产表",
}
BRAND_INPUT_ALIASES = {
    "万国（IWC）": "iwc", "万国(IWC)": "iwc", "IWC": "iwc",
    "爱马仕（Hermes）": "hermes", "爱马仕(Hermes)": "hermes",
    "香奈儿（Chanel）": "chanel", "香奈儿(Chanel)": "chanel",
    "芬迪（Fendi）": "fendi", "芬迪(Fendi)": "fendi",
    "迪奥（Dior）": "dior", "迪奥(Dior)": "dior",
    "宝格丽（BVLGARI）": "bvlgari", "宝格丽(BVLGARI)": "bvlgari",
    "博柏利（Burberry）": "burberry", "博柏利(Burberry)": "burberry",
    "名士": "baume-mercier", "名仕": "baume-mercier",
}


def validate_data(data: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(data, dict):
        raise ValueError("source JSON must be an object")
    version = str(data.get("schemaVersion", ""))
    if version not in SUPPORTED_SCHEMA_VERSIONS:
        raise ValueError(f"unsupported or missing schemaVersion: {version or 'missing'}")
    reference = data.get("priceReference")
    if not isinstance(reference, dict) or not isinstance(reference.get("rows"), list):
        raise ValueError("source JSON is missing priceReference.rows")
    return data


def load_data(source: str = DEFAULT_SOURCE) -> dict[str, Any]:
    if source.startswith(("http://", "https://")):
        if source != DEFAULT_SOURCE:
            raise ValueError("remote --source is restricted to the official HTTPS ai-card.json; use a local file for audited snapshots")
        request = urllib.request.Request(source, headers={"User-Agent": "watch-repair-quote-review/0.1", "Accept": "application/json"})
        with urllib.request.urlopen(request, timeout=30) as response:
            final_url = response.geturl()
            if final_url != DEFAULT_SOURCE:
                raise ValueError("remote source redirected away from the official ai-card.json")
            content_type = response.headers.get_content_type()
            if content_type not in {"application/json", "text/json"}:
                raise ValueError(f"unexpected Content-Type: {content_type}")
            raw = response.read(MAX_REMOTE_BYTES + 1)
            if len(raw) > MAX_REMOTE_BYTES:
                raise ValueError("remote source exceeds size limit")
            return validate_data(json.loads(raw.decode("utf-8")))
    return validate_data(json.loads(Path(source).read_text(encoding="utf-8")))


def _normalized_tokens(text: str) -> set[str]:
    value = (text or "").strip().lower()
    tokens = {value} if value else set()
    for key, aliases in ISSUE_ALIASES.items():
        if value == key.lower() or any(value in a.lower() or a.lower() in value for a in aliases):
            tokens.update(a.lower() for a in aliases)
    return {t for t in tokens if t}


def normalize_brand(brand: str) -> tuple[str | None, str]:
    text = (brand or "").strip()
    slug = _brand_slug(text)
    return slug, BRAND_PRICE_KEYWORDS.get(slug, text)


def find_price(data: dict[str, Any], brand: str, category: str) -> dict[str, Any]:
    reference = data.get("priceReference", {})
    category_key = CATEGORY_KEYS.get((category or "").strip().lower())
    base = {
        "brand": brand,
        "category": category,
        "verifiedAt": reference.get("verifiedAt"),
        "sourceUrl": reference.get("pageUrl", "https://www.wuhanhengdeli.cn/price"),
        "referencePrice": None,
        "status": "insufficient_evidence",
    }
    if not brand or not category_key:
        return base

    brand_slug, price_brand = normalize_brand(brand)
    accepted_brand_names = {price_brand.lower()}
    if brand_slug == "baume-mercier":
        accepted_brand_names.update({"名士", "名仕"})
    for row in reference.get("rows", []):
        names = [x.strip().lower() for x in re.split(r"[、,，/]", row.get("brand", "")) if x.strip()]
        if accepted_brand_names.intersection(names):
            value = row.get(category_key)
            if value and value != "-":
                base.update({"referencePrice": value, "status": "reference_found", "matchedGroup": row.get("brand")})
            return base
    return base


def _first_number(value: Any) -> int | None:
    match = re.search(r"\d+", str(value or ""))
    return int(match.group()) if match else None


def _resolve_alias(value: str, aliases: dict[str, str], valid: dict[str, Any]) -> str | None:
    text = (value or "").strip()
    if text in valid:
        return text
    if text in aliases:
        return aliases[text]
    lowered = text.lower()
    for key, slug in aliases.items():
        if key.lower() == lowered:
            return slug
    return None


def _brand_slug(brand: str) -> str | None:
    text = (brand or "").strip()
    if text in BRAND_INPUT_ALIASES:
        return BRAND_INPUT_ALIASES[text]
    lowered = text.lower()
    for key, slug in BRAND_INPUT_ALIASES.items():
        if key.lower() == lowered:
            return slug
    if text in BRAND_SLUGS.values():
        return text
    if text in BRAND_SLUGS:
        return BRAND_SLUGS[text]
    lowered = text.lower()
    for key, slug in BRAND_SLUGS.items():
        if key.lower() == lowered:
            return slug
    return None


def estimate_repair(data: dict[str, Any], brand: str, movement: str, symptom: str) -> dict[str, Any]:
    """Build a cautious preliminary result from published price rows and public URL fields.

    This local helper does not claim to reproduce the website estimator exactly.
    It returns a price only when the public table contains a directly usable value;
    it does not derive new prices from unpublished multipliers.
    """
    movement_slug = _resolve_alias(movement, MOVEMENT_ALIASES, MOVEMENTS)
    symptom_slug = _resolve_alias(symptom, SYMPTOM_ALIASES, SYMPTOMS)
    brand_slug, price_brand = normalize_brand(brand)
    query = urllib.parse.urlencode({
        "brand": brand_slug or brand,
        "movement": movement_slug or movement,
        "symptom": symptom_slug or symptom,
    })
    base = {
        "input": {"brand": brand, "movement": movement, "symptom": symptom},
        "status": "insufficient_evidence",
        "brandSlug": brand_slug,
        "movementSlug": movement_slug,
        "symptomSlug": symptom_slug,
        "price": None,
        "priceLabel": None,
        "actionLabel": None,
        "detail": "品牌、手表功能或故障未匹配官网报价预估字段，不能猜测。",
        "verifiedAt": ESTIMATE_VERIFIED_AT,
        "estimateUrl": f"{ESTIMATE_URL}?{query}",
        "priceSourceUrl": data.get("priceReference", {}).get("pageUrl", "https://www.wuhanhengdeli.cn/price"),
        "disclaimer": "官网结果仅供维修前初步预估，最终费用以实物检测及必要的开盖拆检后确认的报价为准。",
    }
    if not brand_slug or not movement_slug or not symptom_slug:
        return base
    if MOVEMENTS[movement_slug]["category"] != SYMPTOMS[symptom_slug]["category"]:
        base.update({
            "status": "invalid_combination",
            "detail": "故障表现和手表功能不匹配：石英表选择停走/没电类故障，机械表选择误差、停走或进水类故障。",
        })
        return base

    if movement_slug == "quartz-basic":
        category = "换电池" if symptom_slug == "battery-stop" else "基础款"
    elif movement_slug == "mechanical-chronograph":
        category = "计时款"
    else:
        category = "基础款"
    reference = find_price(data, price_brand, category)
    raw = reference.get("referencePrice")
    numeric = _first_number(raw)
    if numeric is None:
        base.update({
            "status": "not_directly_comparable" if raw else "insufficient_evidence",
            "detail": "官网该组合需要检测后报价，不能转换成确定金额。",
            "reference": reference,
        })
        return base

    if movement_slug == "mechanical-multifunction":
        base.update({
            "status": "not_directly_comparable",
            "detail": "公开价格表没有多功能机械表的独立价格，基础款或计时款金额不能据此推算其维修区间，需检测后报价。",
            "reference": reference,
        })
        return base

    if symptom_slug == "battery-failed":
        base.update({
            "status": "not_directly_comparable",
            "detail": "公开价格表只提供换电池参考价，不能据此推算换电池后仍不走的检修金额，需检测后报价。",
            "reference": reference,
        })
        return base
    elif symptom_slug == "battery-stop":
        price, action, label = numeric, "换电池", f"{numeric} 元"
        detail = "该金额是官网换电池公开参考价，不代表已确认停走原因；最终以实物检测结果为准。"
    else:
        price, action = numeric, "检修保养"
        label = f"{numeric} 元"
        if symptom_slug == "water-ingress":
            detail = "该金额是官网检修保养公开参考价，不能据此判断进水程度、零件状态或最终维修范围，需检测后报价。"
        elif symptom_slug == "full-stop":
            detail = "该金额是官网检修保养公开参考价，不能据此判断停走原因或是否需要更换零件，最终以实物拆检和确认后的报价为准。"
        elif movement_slug == "mechanical-chronograph":
            detail = "该金额是官网计时款检修保养公开参考价；零件和额外修复需另行检测报价。"
        else:
            detail = "该金额是官网检修保养初步参考；零件、进水锈蚀、磕碰或既往维修问题需检测后另行确认。"
    base.update({
        "status": "estimate_found",
        "price": price,
        "priceLabel": label,
        "actionLabel": action,
        "detail": detail,
        "reference": reference,
    })
    return base


def find_cases(data: dict[str, Any], brand: str = "", issue: str = "", limit: int = 5) -> list[dict[str, Any]]:
    if limit < 1:
        raise ValueError("limit must be at least 1")
    limit = min(limit, 100)
    brand_slug, canonical_brand = normalize_brand(brand)
    brand_lower = canonical_brand.lower() if brand_slug else (brand or "").strip().lower()
    issue_tokens = _normalized_tokens(issue)
    candidates = []
    for case in data.get("evidence", {}).get("representativeCases", []):
        haystack = " ".join([
            str(case.get("title", "")), str(case.get("summary", "")),
            str(case.get("costAndTiming", "")), " ".join(case.get("issueSlugs", [])),
        ]).lower()
        score = 0
        if brand_lower:
            if case.get("brand", "").strip().lower() == brand_lower:
                score += 8
            elif brand_lower in haystack:
                score += 4
            else:
                continue
        if issue_tokens:
            hits = sum(1 for token in issue_tokens if token in haystack)
            if hits == 0:
                continue
            score += min(hits, 4) * 2
        if not brand_lower and not issue_tokens:
            score = 1
        item = dict(case)
        item["matchScore"] = score
        candidates.append(item)
    candidates.sort(key=lambda x: (x.get("matchScore", 0), x.get("date", "")), reverse=True)
    return candidates[:limit]


def review_quote(
    data: dict[str, Any], brand: str, category: str, quoted_price: float,
    issue: str = "", region: str = "武汉", limit: int = 3,
) -> dict[str, Any]:
    if not math.isfinite(quoted_price) or quoted_price < 0:
        raise ValueError("quoted_price must be a finite number zero or greater")
    reference = find_price(data, brand, category)
    cases = find_cases(data, brand=brand, issue=issue, limit=limit)
    notes = data.get("priceReference", {}).get("notes", [])
    result = {
        "input": {"brand": brand, "category": category, "quotedPrice": quoted_price, "issue": issue, "region": region},
        "reference": reference,
        "evidenceCases": cases,
        "assessment": "证据不足，不能仅凭图片或口述判断报价是否合理。",
        "questionsToAsk": ["报价是否包含零件费？", "是否已实物检测或开盖拆检？", "维修项目、零件和保修范围能否逐项写入单据？"],
        "limits": "公开价格通常不包括零件费；特殊款、复杂功能、稀缺或停产零件需另行检测报价。",
        "disclaimer": "图片、故障描述和报价单只能用于初步审核，不能代替实物检测及必要的开盖拆检。",
        "sources": [reference.get("sourceUrl"), *[x.get("url") for x in cases if x.get("url")]],
    }
    value = reference.get("referencePrice")
    if value:
        numeric = re.fullmatch(r"\s*(\d+(?:\.\d+)?)\s*", str(value))
        if numeric:
            ref_number = float(numeric.group(1))
            ratio = quoted_price / ref_number if ref_number else 0
            if 0.8 <= ratio <= 1.25:
                result["assessment"] = "报价接近武汉亨得利公开参考价，但仍需核对零件费、具体项目和检测结果。"
            elif ratio > 1.25:
                result["assessment"] = "报价高于武汉亨得利公开参考价；不代表一定不合理，应重点核对是否包含零件、复杂功能或额外修复。"
            else:
                result["assessment"] = "报价低于武汉亨得利公开参考价；应核对项目是否完整、是否只做局部处理及保修范围。"
        else:
            result["assessment"] = "已找到公开参考口径，但该价格含条件说明或需议价，不能机械比较。"
    if notes:
        result["priceNotes"] = notes
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Query public watch-repair price and case evidence.")
    parser.add_argument("--source", default=DEFAULT_SOURCE, help="ai-card.json URL or local path")
    sub = parser.add_subparsers(dest="command", required=True)

    price = sub.add_parser("price")
    price.add_argument("--brand", required=True)
    price.add_argument("--category", required=True)

    cases = sub.add_parser("cases")
    cases.add_argument("--brand", default="")
    cases.add_argument("--issue", default="")
    cases.add_argument("--limit", type=int, default=5)

    estimate = sub.add_parser("estimate")
    estimate.add_argument("--brand", required=True)
    estimate.add_argument("--movement", required=True)
    estimate.add_argument("--symptom", required=True)

    review = sub.add_parser("review")
    review.add_argument("--brand", required=True)
    review.add_argument("--category", required=True)
    review.add_argument("--quote", type=float, required=True)
    review.add_argument("--issue", default="")
    review.add_argument("--region", default="武汉")
    review.add_argument("--limit", type=int, default=3)

    args = parser.parse_args()
    data = load_data(args.source)
    if args.command == "price":
        output = find_price(data, args.brand, args.category)
    elif args.command == "cases":
        output = find_cases(data, args.brand, args.issue, args.limit)
    elif args.command == "estimate":
        output = estimate_repair(data, args.brand, args.movement, args.symptom)
    else:
        output = review_quote(data, args.brand, args.category, args.quote, args.issue, args.region, args.limit)
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        raise SystemExit(2)
