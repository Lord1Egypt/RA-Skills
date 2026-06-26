"""Item reliability evaluation engine.

Scores each item from two primary perspectives:
  1. 性价比 (cost-effectiveness) — price competitiveness + condition value
  2. 靠谱程度 (listing reliability) — description quality + image analysis

Secondary dimensions:
  seller_trust  — reduced weight (Gumtree: near-zero due to sparse seller data)
  risk_flags    — catch-all penalty

When a vision-capable model is configured (e.g. Qwen-VL), images are sent
to the model for authenticity / condition analysis, boosting the accuracy
of the "listing reliability" axis.

Verdict labels:
  "强烈推荐" — all dimensions strong, no flags
  "推荐购买" — generally good, minor concerns
  "建议谨慎" — notable risk factors
  "不建议"   — serious red flags
"""

from __future__ import annotations

import json
import logging
import os
import re
import urllib.request

from pathlib import Path

from .models import EvalResult, EvalScores, ItemDetail, VisionConfig

logger = logging.getLogger(__name__)

_VERDICT_MAP = {
    "highly_recommended": "强烈推荐",
    "recommended": "推荐购买",
    "caution": "建议谨慎",
    "avoid": "不建议",
}

_ACCESSORY_PATTERNS = [
    r"\bcase\b", r"\bcover\b", r"\bbox only\b", r"\bempty box\b",
    r"\bpackaging only\b", r"\bcharger\b", r"\bcable\b", r"\badapter\b",
    r"\btip\b", r"\btips\b", r"\bprotector\b", r"\bholder\b",
    r"\bstrap\b", r"\bcap\b", r"\bhook\b", r"\bmount\b",
    r"\bcleaner\b", r"\bwipe\b", r"\bbrush\b",
]

# ── Vision model prompt ──────────────────────────────────────────────

_VISION_EVAL_PROMPT = """\
你是一个专业的二手商品鉴定师。请根据以下商品图片和描述，评估商品的真实性和靠谱程度。

商品标题: {title}
商品描述: {description}
标注成色: {condition}
售价: {price}

请从以下维度评分 (0-10分):
1. photo_authenticity — 是否为实拍图（非网图/库存图），图片清晰度，是否展示了商品各角度
2. photo_desc_match — 图片展示的商品与标题和描述是否一致
3. visible_condition — 从图片可以看出的商品实际成色如何
4. risk_signals — 图片中是否有可疑之处（如水印、PS痕迹、遮挡关键部位等），分数越高越安全

请严格以 JSON 格式返回，不要有其他文字:
{{"photo_authenticity": 0, "photo_desc_match": 0, "visible_condition": 0, "risk_signals": 0, "overall": 0, "analysis": "简要分析说明，不超过100字"}}"""


def _is_accessory(title: str) -> bool:
    t = title.lower()
    return any(re.search(p, t) for p in _ACCESSORY_PATTERNS)


# ── Weight system ────────────────────────────────────────────────────


def _get_weights(platform: str, has_vision: bool) -> dict[str, float]:
    """Return evaluation dimension weights based on platform and vision availability.

    Gumtree has very limited seller info, so seller_trust is near-zero.
    When vision model is active, image_quality gets its own weight;
    otherwise that budget rolls into listing_authenticity.
    """
    is_gumtree = platform == "gumtree"

    if has_vision:
        return {
            "listing_authenticity": 0.20,
            "image_quality": 0.20,
            "price_competitiveness": 0.25,
            "condition_value": 0.15,
            "seller_trust": 0.05 if is_gumtree else 0.10,
            "risk_flags": 0.15 if is_gumtree else 0.10,
        }
    return {
        "listing_authenticity": 0.35,
        "image_quality": 0.0,
        "price_competitiveness": 0.30,
        "condition_value": 0.15,
        "seller_trust": 0.05 if is_gumtree else 0.10,
        "risk_flags": 0.15 if is_gumtree else 0.10,
    }


# ── Vision config ────────────────────────────────────────────────────

_CONFIG_SEARCH_PATHS = [
    Path.home() / ".config" / "used-price-compare" / "vision.json",
]


def load_vision_config(
    model_override: str | None = None,
) -> VisionConfig:
    """Build a VisionConfig by merging (lowest → highest priority):

    1. Config file  (~/.config/used-price-compare/vision.json)
    2. Environment variables  (VISION_API_BASE, VISION_API_KEY, VISION_MODEL)
    3. CLI override  (--vision-model)

    The config file is a flat JSON object whose keys match VisionConfig fields::

        {
          "model": "qwen-vl-max",
          "api_base": "https://dashscope.aliyuncs.com/compatible-mode/v1",
          "api_key": "sk-xxx",
          "max_images": 5,
          "timeout": 60
        }
    """
    cfg = VisionConfig()

    # 1. Config file
    for path in _CONFIG_SEARCH_PATHS:
        if path.is_file():
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
                if isinstance(data, dict):
                    for field in ("model", "api_base", "api_key"):
                        if field in data and isinstance(data[field], str):
                            setattr(cfg, field, data[field])
                    if "max_images" in data and isinstance(data["max_images"], int):
                        cfg.max_images = data["max_images"]
                    if "timeout" in data and isinstance(data["timeout"], int):
                        cfg.timeout = data["timeout"]
                logger.debug("Loaded vision config from %s", path)
            except Exception as e:
                logger.warning("Failed to read vision config %s: %s", path, e)
            break

    # 2. Environment variables (override file values)
    env_base = os.environ.get("VISION_API_BASE", "")
    env_key = os.environ.get("VISION_API_KEY", "")
    env_model = os.environ.get("VISION_MODEL", "")
    if env_base:
        cfg.api_base = env_base
    if env_key:
        cfg.api_key = env_key
    if env_model:
        cfg.model = env_model

    # 3. CLI override (highest priority)
    if model_override:
        cfg.model = model_override

    return cfg


# ── Vision API ───────────────────────────────────────────────────────


def _download_image_as_base64(img_url: str, timeout: int = 15) -> str | None:
    """Download an image and return it as a base64 data URL.

    Returns None if download fails.
    """
    try:
        req = urllib.request.Request(
            img_url,
            headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"},
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = resp.read()
            content_type = resp.headers.get("Content-Type", "image/jpeg")
            import base64
            b64 = base64.b64encode(data).decode("utf-8")
            return f"data:{content_type};base64,{b64}"
    except Exception as e:
        logger.debug("Image download failed for %s: %s", img_url, e)
        return None


def _call_vision_api(
    item: ItemDetail,
    cfg: VisionConfig,
) -> dict | None:
    """Call an OpenAI-compatible vision API to analyse product images.

    Images are first downloaded locally, then sent as base64 data URLs
    to work around CDN access restrictions (e.g. DashScope cannot fetch
    Gumtree CDN images directly).

    Returns parsed score dict or None on failure.
    """
    if not cfg.enabled:
        logger.warning(
            "Vision config incomplete (model=%r, api_base=%r, api_key=%s), "
            "skipping image analysis",
            cfg.model, cfg.api_base, "set" if cfg.api_key else "unset",
        )
        return None

    if not item.images:
        return None

    prompt_text = _VISION_EVAL_PROMPT.format(
        title=item.title,
        description=item.description[:500],
        condition=item.condition or "未标注",
        price=item.price or "未知",
    )

    # Build content list: text prompt + base64 image data URLs
    content: list[dict] = [{"type": "text", "text": prompt_text}]
    downloaded_count = 0

    for img_url in item.images[: cfg.max_images]:
        data_url = _download_image_as_base64(img_url, timeout=cfg.timeout)
        if data_url:
            content.append({"type": "image_url", "image_url": {"url": data_url}})
            downloaded_count += 1
        else:
            logger.debug("Skipping unreachable image: %s", img_url)

    if downloaded_count == 0:
        logger.warning(
            "Could not download any images for vision analysis "
            "(tried %d URLs). Falling back to heuristic scoring.",
            len(item.images),
        )
        return None

    logger.info(
        "Vision: successfully downloaded %d/%d images for '%s'",
        downloaded_count, len(item.images), item.title,
    )

    payload = {
        "model": cfg.model,
        "messages": [{"role": "user", "content": content}],
        "temperature": 0.1,
    }

    url = f"{cfg.api_base.rstrip('/')}/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {cfg.api_key}",
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers=headers,
    )

    try:
        with urllib.request.urlopen(req, timeout=cfg.timeout) as resp:
            result = json.loads(resp.read().decode("utf-8"))
        text = result["choices"][0]["message"]["content"]
        json_match = re.search(r"\{[^{}]*\}", text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
    except Exception as e:
        logger.warning("Vision API call failed: %s", e)

    return None


# ── Dimension scorers ────────────────────────────────────────────────


def _score_seller_trust(item: ItemDetail) -> tuple[float, list[str]]:
    """Score seller trustworthiness (0-10)."""
    flags: list[str] = []
    seller = item.seller

    platform_base = {
        "ok.com": 6.0, "gumtree": 5.0, "ebay": 6.0, "amazon": 8.0,
    }
    score = platform_base.get(item.platform, 6.0)

    if seller.rating:
        pct_match = re.search(r"([\d.]+)%", seller.rating)
        if pct_match:
            pct = float(pct_match.group(1))
            if pct >= 98:
                score += 2.5
            elif pct >= 95:
                score += 1.5
            elif pct >= 90:
                score += 0.5
            else:
                score -= 1.5
                flags.append("low_seller_rating")

    if seller.reviews_count > 0:
        if seller.reviews_count >= 1000:
            score += 1.0
        elif seller.reviews_count >= 100:
            score += 0.5
        elif seller.reviews_count < 5:
            score -= 1.5
            flags.append("few_seller_reviews")
    elif item.platform in ("ebay",):
        flags.append("no_seller_feedback")
        score -= 1.0

    if seller.member_since:
        if re.search(r"20(?:1\d|20|21|22|23)", seller.member_since):
            score += 0.5
        elif re.search(r"202[56]", seller.member_since):
            flags.append("new_seller_account")
            score -= 0.5

    return max(0.0, min(10.0, score)), flags


def _score_listing_authenticity(item: ItemDetail) -> tuple[float, list[str]]:
    """Score description / text quality of the listing (0-10).

    Photo scoring is handled separately in _score_image_quality.
    """
    flags: list[str] = []
    score = 5.0

    desc_len = len(item.description)
    if desc_len > 500:
        score += 2.0
    elif desc_len > 200:
        score += 1.0
    elif desc_len > 50:
        pass
    else:
        score -= 2.0
        flags.append("vague_description")

    if _is_accessory(item.title):
        flags.append("likely_accessory")
        score -= 3.0

    if len(item.title) < 10:
        flags.append("title_too_short")
        score -= 1.0

    if item.views > 50:
        score += 0.5

    return max(0.0, min(10.0, score)), flags


def _score_image_quality(
    item: ItemDetail,
    vision_result: dict | None = None,
) -> tuple[float, list[str], str]:
    """Score image quality (0-10).

    When *vision_result* is available (from a vision model), uses the model's
    sub-scores. Otherwise falls back to a photo-count heuristic.
    """
    flags: list[str] = []
    analysis = ""

    if vision_result:
        score = float(vision_result.get("overall", 5.0))
        analysis = vision_result.get("analysis", "")

        if vision_result.get("photo_authenticity", 10) < 4:
            flags.append("stock_photos_suspected")
        if vision_result.get("photo_desc_match", 10) < 4:
            flags.append("photos_description_mismatch")
        if vision_result.get("risk_signals", 10) < 4:
            flags.append("visual_risk_signals")

        return max(0.0, min(10.0, score)), flags, analysis

    photo_count = len(item.images)
    if photo_count >= 5:
        score = 7.0
    elif photo_count >= 3:
        score = 5.5
    elif photo_count >= 1:
        score = 4.0
    else:
        score = 1.0
        flags.append("no_photos")

    return score, flags, analysis


def _score_condition_value(item: ItemDetail) -> tuple[float, list[str]]:
    """Score item condition (0-10)."""
    flags: list[str] = []
    c = item.condition.lower()

    if not c:
        return 5.0, flags

    if "new" in c or "sealed" in c or "open box" in c:
        score = 10.0
    elif "like new" in c or "excellent" in c or "mint" in c:
        score = 9.0
    elif "very good" in c or "great" in c:
        score = 7.5
    elif "good" in c:
        score = 6.0
    elif "acceptable" in c or "fair" in c:
        score = 4.0
        flags.append("fair_condition")
    elif "for parts" in c or "repair" in c or "not working" in c or "broken" in c:
        score = 1.5
        flags.append("for_parts_only")
    else:
        score = 5.0

    return score, flags


def _score_price_competitiveness(
    item: ItemDetail, median_price: float,
) -> tuple[float, list[str]]:
    """Score price competitiveness vs peer median (0-10)."""
    flags: list[str] = []
    price = item.price_numeric

    if price <= 0 or median_price <= 0:
        return 5.0, flags

    ratio = price / median_price

    if ratio < 0.3:
        flags.append("price_suspiciously_low")
        return 2.0, flags

    if ratio > 3.0:
        flags.append("price_too_high")
        return 1.5, flags

    if ratio <= 0.7:
        score = 9.5
    elif ratio <= 1.0:
        score = 8.0 + (1.0 - ratio) * 5
    elif ratio <= 1.3:
        score = 6.0
    else:
        score = max(1.0, 8.0 - (ratio - 1.0) * 4)

    return max(0.0, min(10.0, score)), flags


def _score_risk_flags(item: ItemDetail, all_flags: list[str]) -> tuple[float, list[str]]:
    """Compute risk penalty score (0-10, higher = fewer risks)."""
    score = 10.0
    new_flags: list[str] = []

    if "price_suspiciously_low" in all_flags:
        score -= 3.0

    if "vague_description" in all_flags and "no_photos" in all_flags:
        score -= 2.0
        new_flags.append("very_suspicious_listing")

    if "new_seller_account" in all_flags or "no_seller_feedback" in all_flags:
        score -= 1.5

    if "likely_accessory" in all_flags:
        score -= 2.0

    if "for_parts_only" in all_flags:
        score -= 1.0

    if "stock_photos_suspected" in all_flags:
        score -= 2.0

    if "photos_description_mismatch" in all_flags:
        score -= 2.0

    if "visual_risk_signals" in all_flags:
        score -= 1.5

    return max(0.0, min(10.0, score)), new_flags


# ── Main evaluation ──────────────────────────────────────────────────


def evaluate_item(
    item: ItemDetail,
    median_price: float = 0.0,
    vision_cfg: VisionConfig | None = None,
) -> EvalResult:
    """Evaluate a single item, returning scores, flags, and verdict."""
    vision_result: dict | None = None
    if vision_cfg and vision_cfg.enabled and item.images:
        vision_result = _call_vision_api(item, vision_cfg)

    has_vision = vision_result is not None
    weights = _get_weights(item.platform, has_vision)

    seller_score, seller_flags = _score_seller_trust(item)
    auth_score, auth_flags = _score_listing_authenticity(item)
    img_score, img_flags, img_analysis = _score_image_quality(item, vision_result)
    cond_score, cond_flags = _score_condition_value(item)
    price_score, price_flags = _score_price_competitiveness(item, median_price)

    all_flags = seller_flags + auth_flags + img_flags + cond_flags + price_flags
    risk_score, risk_flags = _score_risk_flags(item, all_flags)
    all_flags.extend(risk_flags)

    overall = (
        seller_score * weights["seller_trust"]
        + auth_score * weights["listing_authenticity"]
        + img_score * weights["image_quality"]
        + cond_score * weights["condition_value"]
        + price_score * weights["price_competitiveness"]
        + risk_score * weights["risk_flags"]
    )
    overall = round(max(0.0, min(10.0, overall)), 1)

    if overall >= 8.0 and not all_flags:
        verdict = "highly_recommended"
    elif overall >= 7.0 and "likely_accessory" not in all_flags:
        verdict = "recommended"
    elif overall >= 5.0:
        verdict = "caution"
    else:
        verdict = "avoid"

    if "very_suspicious_listing" in all_flags or "likely_accessory" in all_flags:
        if verdict in ("highly_recommended", "recommended"):
            verdict = "caution"

    rationale = _build_rationale(item, all_flags, overall, verdict, img_analysis)

    return EvalResult(
        item=item,
        scores=EvalScores(
            seller_trust=round(seller_score, 1),
            listing_authenticity=round(auth_score, 1),
            image_quality=round(img_score, 1),
            condition_value=round(cond_score, 1),
            price_competitiveness=round(price_score, 1),
            risk_flags=round(risk_score, 1),
            overall=overall,
        ),
        flags=all_flags,
        verdict=verdict,
        verdict_label=_VERDICT_MAP.get(verdict, verdict),
        rationale=rationale,
        image_analysis=img_analysis,
    )


def evaluate_items(
    items: list[ItemDetail],
    vision_model: str | None = None,
    vision_cfg: VisionConfig | None = None,
) -> list[EvalResult]:
    """Evaluate multiple items, computing median price from the group.

    *vision_cfg* takes precedence. If only *vision_model* is given, a
    VisionConfig is resolved via ``load_vision_config(model_override=...)``.
    """
    if vision_cfg is None and vision_model:
        vision_cfg = load_vision_config(model_override=vision_model)

    valid_prices = [it.price_numeric for it in items if it.price_numeric > 1.0]
    median_price = (
        sorted(valid_prices)[len(valid_prices) // 2]
        if valid_prices
        else 50.0
    )

    results = [evaluate_item(it, median_price, vision_cfg) for it in items]
    results.sort(key=lambda r: r.scores.overall, reverse=True)
    return results


def _build_rationale(
    item: ItemDetail, flags: list[str], overall: float, verdict: str,
    image_analysis: str = "",
) -> str:
    """Build a natural-language rationale for the verdict."""
    parts: list[str] = []

    # Seller assessment (brief, since weight is low)
    if item.seller.rating:
        parts.append(f"卖家信誉{item.seller.rating}")
        if item.seller.reviews_count:
            parts.append(f"({item.seller.reviews_count}条评价)")
    elif item.platform == "amazon":
        parts.append("Amazon官方或认证卖家")
    elif item.platform == "gumtree":
        parts.append("Gumtree无详细卖家信息")
    else:
        parts.append("卖家信息不详")

    if item.condition:
        parts.append(f"成色: {item.condition}")

    # Image analysis (from vision model)
    if image_analysis:
        parts.append(f"图片分析: {image_analysis}")
    elif not item.images:
        parts.append("缺少商品实拍图")
    else:
        parts.append(f"共{len(item.images)}张图片")

    if "price_suspiciously_low" in flags:
        parts.append("价格异常偏低，可能存在风险")
    elif "price_too_high" in flags:
        parts.append("价格明显偏高")

    if "vague_description" in flags:
        parts.append("商品描述过于简略")
    if "likely_accessory" in flags:
        parts.append("可能是配件而非主商品")
    if "stock_photos_suspected" in flags:
        parts.append("疑似使用库存图而非实拍")
    if "photos_description_mismatch" in flags:
        parts.append("图文不符")
    if "visual_risk_signals" in flags:
        parts.append("图片存在可疑之处")

    if "new_seller_account" in flags:
        parts.append("卖家账号较新")
    if "no_seller_feedback" in flags:
        parts.append("卖家无历史评价")

    parts.append(f"综合评分 {overall}/10")

    return "，".join(parts) + "。"


# ── Output formatting ────────────────────────────────────────────────


def format_eval_results(results: list[EvalResult]) -> dict:
    """Format evaluation results into structured JSON for CLI output."""
    items_out = []
    for i, r in enumerate(results, 1):
        entry: dict = {
            "rank": i,
            "title": r.item.title,
            "price": r.item.price,
            "platform": r.item.platform,
            "source_url": r.item.source_url,
            "condition": r.item.condition,
            "images_count": len(r.item.images),
            "seller": {
                "name": r.item.seller.name,
                "rating": r.item.seller.rating,
                "reviews_count": r.item.seller.reviews_count,
            },
            "scores": {
                "listing_authenticity": r.scores.listing_authenticity,
                "image_quality": r.scores.image_quality,
                "price_competitiveness": r.scores.price_competitiveness,
                "condition_value": r.scores.condition_value,
                "seller_trust": r.scores.seller_trust,
                "risk_flags": r.scores.risk_flags,
                "overall": r.scores.overall,
            },
            "flags": r.flags,
            "verdict": r.verdict_label,
            "rationale": r.rationale,
        }
        if r.image_analysis:
            entry["image_analysis"] = r.image_analysis
        items_out.append(entry)

    best = results[0] if results else None
    output: dict = {
        "success": True,
        "total": len(results),
        "items": items_out,
    }
    if best:
        output["best_value"] = {
            "title": best.item.title,
            "price": best.item.price,
            "platform": best.item.platform,
            "source_url": best.item.source_url,
            "overall": best.scores.overall,
            "verdict": best.verdict_label,
        }

    return output
