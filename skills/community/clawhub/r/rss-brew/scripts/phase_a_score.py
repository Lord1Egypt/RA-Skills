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

SYSTEM = """You are Phase-A scorer for RSS-Brew.
Return STRICT JSON only: {\"score\": int, \"score_reason\": str}
Rules:
- score must be integer 0..5.
- Evaluate with 5 binary dimensions (0/1 each): Value&Insight, Relevance, Depth&Data, Authority, Objectivity.
- Keep score_reason to one short sentence.
"""


class PhaseAConfig(Dict[str, Any]):
    pass


def clamp_score(v: Any) -> int:
    try:
        s = int(v)
    except Exception:
        s = 0
    return max(0, min(5, s))


def _build_prompt(article: Dict[str, Any]) -> str:
    short_text = (article.get("summary") or "").strip()
    if not short_text:
        short_text = (article.get("text") or "")[:800]
    return (
        "Evaluate this article for VC/startup/MBA/frontier-tech reading list.\n"
        f"Title: {article.get('title','')}\n"
        f"Source: {article.get('source','')}\n"
        f"Published: {article.get('published','')}\n"
        f"URL: {article.get('url','')}\n"
        f"Summary/Text:\n{short_text}\n"
    )


def _extract_json_object(content: str) -> Dict[str, Any]:
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        start = content.find("{")
        end = content.rfind("}")
        if start >= 0 and end > start:
            return json.loads(content[start : end + 1])
        raise


def _parse_scoring(content: str) -> Dict[str, Any]:
    parsed = _extract_json_object(content)
    score = clamp_score(parsed.get("score"))
    reason = str(parsed.get("score_reason", "")).strip() or "Scored by Phase-A rubric."
    return {"score": score, "score_reason": reason}


def _load_phase_a_config() -> PhaseAConfig:
    api_key = os.getenv("DEEPSEEK_API_KEY", "").strip()
    base_url = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1").strip()
    model = os.getenv("DEEPSEEK_MODEL", "deepseek-reasoner").strip() or "deepseek-reasoner"
    timeout = float(os.getenv("DEEPSEEK_TIMEOUT_SECONDS", "60"))
    retries = int(os.getenv("DEEPSEEK_RETRY_COUNT", "2"))
    return PhaseAConfig(
        api_key=api_key,
        base_url=base_url,
        model=model,
        timeout=timeout,
        retries=max(0, retries),
    )


def _build_client(config: PhaseAConfig) -> Any:
    if not config.get("api_key"):
        raise RuntimeError("DEEPSEEK_API_KEY is required unless --mock is used")
    try:
        from openai import OpenAI
    except Exception as exc:  # pragma: no cover - import path/environment dependent
        raise RuntimeError("openai package is required for direct DeepSeek API mode") from exc

    return OpenAI(api_key=config["api_key"], base_url=config["base_url"], timeout=config["timeout"])


def _call_deepseek(prompt: str, config: PhaseAConfig, client: Any) -> str:
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
    config: Optional[PhaseAConfig] = None,
) -> Dict[str, Any]:
    prompt = _build_prompt(article)

    if mock:
        text = ((article.get("summary") or "").strip() or (article.get("text") or "")[:800]).lower()
        signal = sum(1 for kw in ["ai", "startup", "vc", "fund", "data", "market"] if kw in text)
        article["score"] = clamp_score(min(5, max(0, signal)))
        article["score_reason"] = "Mock scoring based on keyword signal."
        return article

    cfg = config or _load_phase_a_config()
    api_client = client or _build_client(cfg)
    content = _call_deepseek(prompt, cfg, api_client)
    parsed = _parse_scoring(content)

    article["score"] = parsed["score"]
    article["score_reason"] = parsed["score_reason"]
    return article


def main() -> None:
    ap = argparse.ArgumentParser(description="Phase A scoring (DeepSeek direct API)")
    ap.add_argument("--input", required=True, help="new-articles.json")
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

    print(f"[phase_a] model={args.model} articles={len(articles)}")
    scored: List[Dict[str, Any]] = []

    cfg = None if args.mock else _load_phase_a_config()
    client = None if args.mock else _build_client(cfg)

    for i, article in enumerate(articles, start=1):
        try:
            scored.append(score_one(dict(article), args.model, mock=args.mock, client=client, config=cfg))
            print(f"[phase_a] scored {i}/{len(articles)}")
        except Exception as e:
            print(f"[phase_a] ERROR scoring index={i-1}: {e}", file=sys.stderr)
            sys.exit(11)

    out_payload = {
        "generated_at": payload.get("generated_at"),
        "article_count": len(scored),
        "model": args.model,
        "articles": scored,
    }
    write_json(out_path, out_payload)
    print(f"[phase_a] wrote {out_path}")


if __name__ == "__main__":
    main()
