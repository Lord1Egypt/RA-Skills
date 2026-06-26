#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from shared_utils import load_json, write_json

SYSTEM = """You are Phase-C structured model scorer for RSS-Brew.
Return STRICT JSON only with keys:
{
  "MODEL_SCORE": number,        // REQUIRED: sum of 5 criteria, float 0.0..5.0
  "VALUE_INSIGHT": number,      // 0.0 to 1.0
  "RELEVANCE": number,          // 0.0 to 1.0
  "DEPTH_DATA": number,         // 0.0 to 1.0
  "AUTHORITY": number,          // 0.0 to 1.0
  "OBJECTIVITY": number,        // 0.0 to 1.0
  "score_reason": str,          // one short sentence explaining the score
  "confidence": number,         // float in [0.0, 1.0]
  "plus_tags": [str],           // 0..5 short tags, e.g. "market-data"
  "minus_tags": [str],          // 0..5 short tags, e.g. "thin-evidence"
  "evidence": [str]             // 1..4 short evidence snippets
}
Rules:
- MODEL_SCORE must equal VALUE_INSIGHT + RELEVANCE + DEPTH_DATA + AUTHORITY + OBJECTIVITY
- Each criterion is 0.0 to 1.0 (can use decimals like 0.5, 0.7)
- score_reason must be concise.
- Keep tags and evidence concise.
"""


class PhaseModelConfig(Dict[str, Any]):
    pass


def clamp_score(v: Any) -> int:
    try:
        s = int(v)
    except Exception:
        s = 0
    return max(0, min(5, s))


def clamp_confidence(v: Any) -> float:
    try:
        c = float(v)
    except Exception:
        c = 0.5
    return max(0.0, min(1.0, c))


def clamp_model_score(v: Any) -> float:
    try:
        s = float(v)
    except Exception:
        s = 0.0
    return max(0.0, min(5.0, s))  # V2: model_score is 0-5 sum of 5 criteria


def score_to_model_score(score: int) -> float:
    # V2: model_score is now 0-5 sum, same range as legacy score
    # Just return the score as float
    return float(clamp_score(score))


def model_score_to_score(model_score: float) -> int:
    # V2: model_score is 0-5, just round to int
    return clamp_score(round(clamp_model_score(model_score)))


def clean_tags(value: Any, max_items: int = 5) -> List[str]:
    if not isinstance(value, list):
        return []
    out: List[str] = []
    for item in value:
        t = str(item).strip().lower()
        if t:
            out.append(t)
        if len(out) >= max_items:
            break
    return out


def clean_evidence(value: Any, max_items: int = 4) -> List[str]:
    if not isinstance(value, list):
        return []
    out: List[str] = []
    for item in value:
        t = str(item).strip()
        if t:
            out.append(t)
        if len(out) >= max_items:
            break
    return out


def _build_prompt(article: Dict[str, Any]) -> str:
    short_text = (article.get("summary") or "").strip()
    if not short_text:
        short_text = (article.get("text") or "")[:1200]

    # Scoring V2 rule-filter output uses rule_plus_tags/rule_minus_tags.
    # Keep backward fallback to legacy plus_tags/minus_tags for mixed inputs.
    rule_plus = article.get("rule_plus_tags")
    if not isinstance(rule_plus, list):
        rule_plus = article.get("plus_tags", [])
    rule_minus = article.get("rule_minus_tags")
    if not isinstance(rule_minus, list):
        rule_minus = article.get("minus_tags", [])

    return (
        f"Evaluate this article based on the following FIVE criteria, scoring each from 0.0 (lowest) to 1.0 (highest). "
        f"The final MODEL_SCORE should be the sum of these five scores (total 0.0 to 5.0).\n"
        f"\n"
        f"READER PROFILE (use this to calibrate RELEVANCE scores):\n"
        f"Richard is a Chinese MBA student at London Business School and a part-time VC intern at a robotics-focused fund (Grishin Robotics). He has 4 years of cross-border e-commerce experience (Amazon/Shopify, China-to-global). Boost RELEVANCE when content involves: China tech / AI / cross-border e-commerce, VC deal flow and startup funding rounds, robotics and hardware AI, MBA/career development, China-US geopolitics (trade, tech policy), European startup ecosystem (London/Paris).\n"
        f"\n"
        f"CRITERIA:\n"
        f"1. VALUE_INSIGHT: Is there a clear, non-obvious, actionable insight? (0-1)\n"
        f"2. RELEVANCE: How relevant is this to VC/startup/frontier tech strategy? (0-1)\n"
        f"3. DEPTH_DATA: Is the article supported by strong data, multiple sources, or deep analysis? (0-1)\n"
        f"4. AUTHORITY: Is the source highly authoritative (FT/TC/Crunchbase) or is the author a known expert? (0-1)\n"
        f"5. OBJECTIVITY: Does the article present multiple sides or is it purely narrative/salesy? (0-1)\n"
        f"\n"
        f"Title: {article.get('title', '')}\n"
        f"Source: {article.get('source', '')}\n"
        f"Published: {article.get('published', '')}\n"
        f"URL: {article.get('url', '')}\n"
        f"Rule stage hints: plus={rule_plus}, minus={rule_minus}\n"
        f"Summary/Text:\n{short_text}\n"
        f"\n"
        f"Return STRICT JSON, ensuring MODEL_SCORE is the sum of the 5 criteria, and include the 5 criteria as a 'rationale' object."
    )


def _extract_json_object(content: str) -> Dict[str, Any]:
    """Extract JSON object from model response, handling various formats."""
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        # Try to find JSON object in the response
        start = content.find("{")
        end = content.rfind("}")
        if start >= 0 and end > start:
            return json.loads(content[start : end + 1])
        raise


def _parse_scoring(content: str) -> Dict[str, Any]:
    parsed = _extract_json_object(content)

    # V2: Extract model_score (0-5 sum of 5 criteria)
    # First try explicit MODEL_SCORE/model_score field
    model_score_sum = parsed.get("MODEL_SCORE", parsed.get("model_score", None))
    
    # If not provided, sum the 5 criteria
    if model_score_sum is None:
        value_insight = float(parsed.get("VALUE_INSIGHT", parsed.get("value_insight", 0.0)))
        relevance = float(parsed.get("RELEVANCE", parsed.get("relevance", 0.0)))
        depth_data = float(parsed.get("DEPTH_DATA", parsed.get("depth_data", 0.0)))
        authority = float(parsed.get("AUTHORITY", parsed.get("authority", 0.0)))
        objectivity = float(parsed.get("OBJECTIVITY", parsed.get("objectivity", 0.0)))
        model_score_sum = value_insight + relevance + depth_data + authority + objectivity
    else:
        model_score_sum = float(model_score_sum)
    
    model_score_sum = clamp_model_score(model_score_sum)
    
    # Legacy score is derived from model_score (both 0-5 now)
    score = clamp_score(round(model_score_sum)) 
    
    reason = str(parsed.get("score_reason", "")).strip() or "Scored by structured 5-criteria model rubric."
    confidence = clamp_confidence(parsed.get("confidence", 0.5))
    plus_tags = clean_tags(parsed.get("plus_tags"))
    minus_tags = clean_tags(parsed.get("minus_tags"))
    evidence = clean_evidence(parsed.get("evidence"))

    # Build rationale from 5 criteria
    rationale = {
        "value_insight": float(parsed.get("VALUE_INSIGHT", parsed.get("value_insight", 0.0))),
        "relevance": float(parsed.get("RELEVANCE", parsed.get("relevance", 0.0))),
        "depth_data": float(parsed.get("DEPTH_DATA", parsed.get("depth_data", 0.0))),
        "authority": float(parsed.get("AUTHORITY", parsed.get("authority", 0.0))),
        "objectivity": float(parsed.get("OBJECTIVITY", parsed.get("objectivity", 0.0))),
    }

    return {
        "score": score,
        "score_reason": reason,
        "model_score": model_score_sum,  # 0-5 sum
        "confidence": confidence,
        "plus_tags": plus_tags,
        "minus_tags": minus_tags,
        "evidence": evidence,
        "rationale": rationale,
    }


def _load_model_config() -> PhaseModelConfig:
    api_key = os.getenv("DEEPSEEK_API_KEY", "").strip()
    base_url = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1").strip()
    # V2 scoring needs predictable latency; default to chat model unless explicitly overridden.
    model = os.getenv("DEEPSEEK_MODEL", "deepseek-chat").strip() or "deepseek-chat"
    timeout = float(os.getenv("DEEPSEEK_TIMEOUT_SECONDS", "60"))
    retries = int(os.getenv("DEEPSEEK_RETRY_COUNT", "2"))
    return PhaseModelConfig(
        api_key=api_key,
        base_url=base_url,
        model=model,
        timeout=timeout,
        retries=max(0, retries),
    )


def _build_client(config: PhaseModelConfig) -> Any:
    if not config.get("api_key"):
        raise RuntimeError("DEEPSEEK_API_KEY is required unless --mock is used")
    try:
        from openai import OpenAI
    except Exception as exc:  # pragma: no cover
        raise RuntimeError("openai package is required for direct DeepSeek API mode") from exc

    return OpenAI(api_key=config["api_key"], base_url=config["base_url"], timeout=config["timeout"])


def _call_deepseek(prompt: str, config: PhaseModelConfig, client: Any) -> str:
    attempts = config["retries"] + 1
    last_err: Optional[Exception] = None
    for attempt in range(1, attempts + 1):
        try:
            resp = client.chat.completions.create(
                model=config["model"],
                messages=[
                    {"role": "system", "content": SYSTEM},
                    {"role": "user", "content": prompt},
                ],
                temperature=0,
                timeout=config["timeout"],
            )
            msg = resp.choices[0].message.content if resp.choices else ""
            if not msg:
                raise RuntimeError("Empty response from DeepSeek")
            return msg
        except Exception as exc:
            last_err = exc
            if attempt >= attempts:
                break
            time.sleep(min(2 ** (attempt - 1), 4))
    raise RuntimeError(f"DeepSeek request failed after {attempts} attempts: {last_err}")


def score_one(
    article: Dict[str, Any],
    model_alias: str,
    mock: bool = False,
    client: Any = None,
    config: Optional[PhaseModelConfig] = None,
) -> Dict[str, Any]:
    prompt = _build_prompt(article)

    if mock:
        text = ((article.get("summary") or "").strip() or (article.get("text") or "")[:1200]).lower()
        # Mocking the 5 criteria sums to a value in [0, 5]
        signal = sum(1 for kw in ["ai", "startup", "vc", "fund", "data", "market"] if kw in text)
        model_score_sum = min(5.0, float(signal) * 1.2) # Mock signal = model_score_sum
        
        score = clamp_score(round(model_score_sum))
        
        article["score"] = score
        article["score_reason"] = "Mock structured scoring based on keyword signal."
        article["model_score"] = model_score_sum # Store the 0-5 sum here
        article["confidence"] = 0.6
        article["plus_tags"] = ["keyword-signal"] if signal > 0 else []
        article["minus_tags"] = [] if signal > 0 else ["low-signal"]
        article["evidence"] = ["Keyword overlap with VC/startup themes in summary/text."]
        article["rationale"] = {
            "value_insight": 1 if signal >= 1 else 0,
            "relevance": 1 if signal >= 2 else 0,
            "depth_data": 1 if signal >= 3 else 0,
            "authority": 1 if signal >= 4 else 0,
            "objectivity": 1 if signal >= 5 else 0,
        }
        return article

    cfg = config or _load_model_config()
    api_client = client or _build_client(cfg)
    content = _call_deepseek(prompt, cfg, api_client)
    parsed = _parse_scoring(content)

    # Backward compatibility: always keep legacy score + score_reason (if they existed).
    article["score"] = parsed["score"]
    article["score_reason"] = parsed["score_reason"]

    # NEW: Store the actual 0-5 sum in model_score field
    article["model_score"] = float(parsed["model_score"]) # This is the 0-5 sum
    
    article["confidence"] = parsed["confidence"]
    article["plus_tags"] = parsed["plus_tags"]
    article["minus_tags"] = parsed["minus_tags"]
    article["evidence"] = parsed["evidence"]
    article["rationale"] = parsed["rationale"]
    return article


def main() -> None:
    ap = argparse.ArgumentParser(description="Phase C structured model scoring (DeepSeek direct API)")
    ap.add_argument("--input", required=True, help="new-articles.json or rule-filtered-articles.json")
    ap.add_argument("--output", required=True, help="scored-articles.json")
    ap.add_argument("--model", default="CHEAP", help="Model alias label for output metadata")
    ap.add_argument("--limit", type=int, default=0, help="Optional limit for scoring (debug)")
    ap.add_argument("--mock", action="store_true", help="Mock mode without model API")
    args = ap.parse_args()

    in_path = Path(args.input)
    out_path = Path(args.output)

    payload = load_json(in_path, {})
    articles: List[Dict[str, Any]] = payload.get("articles", []) or []
    if args.limit and args.limit > 0:
        articles = articles[: args.limit]

    print(f"[phase_model_score] model={args.model} articles={len(articles)}")
    scored: List[Dict[str, Any]] = []

    cfg = None if args.mock else _load_model_config()
    client = None if args.mock else _build_client(cfg)

    for i, article in enumerate(articles, start=1):
        try:
            scored.append(score_one(dict(article), args.model, mock=args.mock, client=client, config=cfg))
            print(f"[phase_model_score] scored {i}/{len(articles)}")
        except Exception as e:
            print(f"[phase_model_score] ERROR scoring index={i-1}: {e}", file=sys.stderr)
            sys.exit(11)

    out_payload = {
        "generated_at": payload.get("generated_at"),
        "article_count": len(scored),
        "model": args.model,
        "articles": scored,
    }
    write_json(out_path, out_payload)
    print(f"[phase_model_score] wrote {out_path}")


if __name__ == "__main__":
    main()
