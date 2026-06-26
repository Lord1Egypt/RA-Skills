#!/usr/bin/env python3
"""Generate new benchmark cases for skill-hr P02 matching evaluation.

Uses an LLM to generate realistic benchmark cases for randomly selected profession
domains. Each generated case includes: user_task, gold_jd (P01-style), skill_catalog
(3 skills: 1 correct + 2 distractors), and gold labels for P02 evaluation.

Environment:
  OPENAI_API_KEY   Required.
  OPENAI_BASE_URL  Optional; defaults to https://api.openai.com/v1.

Example (PowerShell):
  $env:OPENAI_API_KEY = "sk-..."
  $env:OPENAI_BASE_URL = "https://api.duckcoding.ai/v1"
  python generate_cases.py --model gpt-5-codex --out generated_cases.jsonl
"""

from __future__ import annotations

import argparse
import json
import os
import random
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

# Profession domains available for random selection
PROFESSION_DOMAINS = [
    "数据工程师",
    "前端开发工程师",
    "产品经理",
    "数据科学家",
    "DevOps工程师",
    "后端开发工程师",
    "UI/UX设计师",
    "机器学习工程师",
    "安全工程师",
    "技术文档工程师",
    "移动端开发工程师",
    "测试工程师",
    "算法工程师",
    "架构师",
    "全栈工程师",
]

SYSTEM_PROMPT = """You are a JSON generator. Output ONLY valid JSON. Never output prose, markdown, or explanation.
Start your response with { and end with }."""

CASE_GENERATION_TEMPLATE = """Generate {n_cases} benchmark cases for skill-hr P02 matching evaluation.
Profession domain: "{profession}"

The skill-hr system routes user tasks to AI agent capability SKILL modules (like "pdf", "xlsx", "mcp-builder", "security-auditor", etc.).

Output format — respond with ONLY this JSON, nothing else:

{{"cases": [
  {{
    "case_id": "gen_{slug}_1",
    "user_task": "...",
    "gold_jd": {{
      "role_title": "...",
      "mission_statement": "...",
      "must_have_competencies": ["...", "..."],
      "deliverables": ["..."],
      "success_criteria": ["..."],
      "complexity_tier": "S",
      "tools_and_access": ["..."]
    }},
    "skill_catalog": [
      {{"id": "s_correct", "name": "skill-name", "description": "...", "registry_status": "active", "skill_body_excerpt": "..."}},
      {{"id": "s_distract1", "name": "skill-name2", "description": "...", "registry_status": "active", "skill_body_excerpt": "..."}},
      {{"id": "s_distract2", "name": "skill-name3", "description": "...", "registry_status": "active", "skill_body_excerpt": "..."}}
    ],
    "gold_primary_skill_id": "s_correct",
    "gold_decision": "delegate",
    "notes": "why distractors are wrong",
    "matching": {{"delegate_min_score": 75, "confirm_band_min": 60}}
  }}
]}}

Rules:
- Generate exactly {n_cases} cases in the array
- skill_catalog: EXACTLY 3 skills per case (1 correct + 2 distractors)
- At least 1 case must have gold_decision="recruit" and gold_primary_skill_id=null
- complexity_tier must vary: use "S", "M", "L" across cases
- Skills are AI capability modules (pdf, docx, xlsx, pptx, mcp-builder, webapp-testing, frontend-design, security-auditor, seo, jupyter-notebook, git-essentials, evaluation, canvas-design)
- case_id format: gen_{slug}_1, gen_{slug}_2, ..., gen_{slug}_{n_cases}
- Output ONLY the JSON object. No explanations."""


def chat_completion(
    *,
    base_url: str,
    api_key: str,
    model: str,
    messages: list[dict[str, str]],
    temperature: float = 0.7,
    timeout_s: int = 120,
) -> str:
    url = base_url.rstrip("/") + "/chat/completions"
    body = json.dumps(
        {
            "model": model,
            "messages": messages,
            "temperature": temperature,
        },
        ensure_ascii=False,
    ).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout_s) as resp:
            raw = resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {e.code}: {detail}") from e
    data = json.loads(raw)
    choices = data.get("choices")
    if not choices:
        raise RuntimeError(f"No choices in API response: {raw[:2000]}")
    msg = choices[0].get("message") or {}
    content = msg.get("content")
    if not isinstance(content, str):
        raise RuntimeError(f"Missing message.content: {raw[:2000]}")
    return content


def extract_cases(content: str) -> list[dict[str, Any]]:
    """Extract a list of case dicts from the model's JSON response.

    Handles: JSON in code fences, bare JSON array, JSON object with cases key.
    """
    raw = content.strip()

    # 1. Try to extract from ```json ... ``` or ``` ... ``` code fences
    for m in re.finditer(r"```(?:json)?\s*([\s\S]*?)\s*```", raw):
        candidate = m.group(1).strip()
        result = _try_parse_cases(candidate)
        if result is not None:
            return result

    # 2. Try the full content as-is
    result = _try_parse_cases(raw)
    if result is not None:
        return result

    # 3. Try to find a JSON array directly
    arr_start = raw.find("[")
    if arr_start >= 0:
        for arr_end in range(len(raw) - 1, arr_start, -1):
            if raw[arr_end] == "]":
                try:
                    arr = json.loads(raw[arr_start : arr_end + 1])
                    if isinstance(arr, list) and arr:
                        return arr
                except json.JSONDecodeError:
                    pass

    # 4. Try each { ... } block found in the output
    for m in re.finditer(r"\{", raw):
        candidate = raw[m.start():]
        try:
            dec = json.JSONDecoder()
            obj, _ = dec.raw_decode(candidate)
            if isinstance(obj, dict):
                result = _cases_from_dict(obj)
                if result is not None:
                    return result
        except json.JSONDecodeError:
            pass

    raise ValueError(
        f"no JSON cases found in model output "
        f"(first 500 chars): {raw[:500]!r}"
    )


def _try_parse_cases(text: str) -> list[dict[str, Any]] | None:
    """Attempt to parse text as JSON and extract a cases list. Returns None on failure."""
    text = text.strip()
    if not text:
        return None
    try:
        obj = json.loads(text)
    except json.JSONDecodeError:
        # Try partial recovery: find first { and last }
        start = text.find("{")
        end = text.rfind("}")
        if start >= 0 and end > start:
            try:
                obj = json.loads(text[start : end + 1])
            except json.JSONDecodeError:
                return None
        else:
            return None

    if isinstance(obj, list):
        return obj
    if isinstance(obj, dict):
        return _cases_from_dict(obj)
    return None


def _cases_from_dict(obj: dict[str, Any]) -> list[dict[str, Any]] | None:
    """Extract a cases list from a dict response."""
    for key in ("cases", "data", "results", "benchmark_cases", "items", "output"):
        if key in obj and isinstance(obj[key], list) and obj[key]:
            return obj[key]
    # Single list value
    lists = [(k, v) for k, v in obj.items() if isinstance(v, list) and v]
    if len(lists) == 1:
        return lists[0][1]
    return None


def profession_to_slug(profession: str) -> str:
    """Convert profession name to a URL-safe slug."""
    slug = profession.lower()
    # Replace Chinese characters and spaces with underscores
    slug = re.sub(r"[^\w]", "_", slug, flags=re.UNICODE)
    slug = re.sub(r"_+", "_", slug).strip("_")
    return slug[:20]


def generate_cases_for_profession(
    profession: str,
    n_cases: int,
    base_url: str,
    api_key: str,
    model: str,
    timeout_s: int = 120,
) -> list[dict[str, Any]]:
    slug = profession_to_slug(profession)
    user_message = CASE_GENERATION_TEMPLATE.format(
        profession=profession,
        n_cases=n_cases,
        slug=slug,
    )

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message},
    ]

    content = chat_completion(
        base_url=base_url,
        api_key=api_key,
        model=model,
        messages=messages,
        temperature=0.7,
        timeout_s=timeout_s,
    )

    try:
        cases = extract_cases(content)
    except ValueError as e:
        # Re-raise with raw content preview for diagnosis
        preview = content[:800].replace("\n", "\\n")
        raise ValueError(f"{e} | raw_preview: {preview}") from e
    # Tag each case with the profession
    for c in cases:
        c["_profession"] = profession
    return cases


def validate_case(case: dict[str, Any]) -> list[str]:
    """Return a list of validation errors (empty = valid)."""
    errors: list[str] = []
    required = ["case_id", "user_task", "gold_jd", "skill_catalog", "gold_decision", "matching"]
    for field in required:
        if field not in case:
            errors.append(f"missing field: {field}")

    catalog = case.get("skill_catalog", [])
    if not isinstance(catalog, list) or len(catalog) != 3:
        errors.append(f"skill_catalog must have exactly 3 items, got {len(catalog) if isinstance(catalog, list) else 'non-list'}")

    gold_id = case.get("gold_primary_skill_id")
    decision = case.get("gold_decision", "")
    if decision == "recruit":
        if gold_id is not None:
            errors.append("recruit cases must have gold_primary_skill_id = null")
    else:
        if not gold_id:
            errors.append(f"non-recruit case missing gold_primary_skill_id")
        else:
            catalog_ids = {s.get("id") for s in catalog if isinstance(s, dict)}
            if gold_id not in catalog_ids:
                errors.append(f"gold_primary_skill_id '{gold_id}' not found in skill_catalog ids: {catalog_ids}")

    jd = case.get("gold_jd", {})
    if not isinstance(jd, dict):
        errors.append("gold_jd must be a dict")
    else:
        for jd_field in ["role_title", "mission_statement", "must_have_competencies"]:
            if not jd.get(jd_field):
                errors.append(f"gold_jd missing {jd_field}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True, help="Output .jsonl path")
    parser.add_argument("--model", default="gpt-4o-mini", help="Model name")
    parser.add_argument(
        "--base-url",
        default=os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1"),
        help="API base URL (e.g. https://api.duckcoding.ai/v1)",
    )
    parser.add_argument(
        "--n-professions",
        type=int,
        default=2,
        help="Number of random professions to select",
    )
    parser.add_argument(
        "--n-cases",
        type=int,
        default=5,
        help="Number of cases to generate per profession",
    )
    parser.add_argument(
        "--professions",
        nargs="+",
        help="Override random selection with specific profession names",
    )
    parser.add_argument("--seed", type=int, default=42, help="Random seed for profession selection")
    parser.add_argument("--timeout", type=int, default=180, help="API timeout in seconds")
    parser.add_argument("--sleep", type=float, default=1.0, help="Seconds between API calls")
    parser.add_argument("--debug", action="store_true", help="Print raw model output on error")
    args = parser.parse_args()

    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable is not set.", file=sys.stderr)
        return 2

    base_url = args.base_url
    # Ensure /v1 suffix for standard OpenAI-compatible endpoints
    if not base_url.rstrip("/").endswith("/v1") and "openai.com" not in base_url:
        candidate = base_url.rstrip("/") + "/v1"
        # Keep as-is if user explicitly specified a path; add /v1 for bare domains
        if base_url.count("/") <= 2:
            base_url = candidate
            print(f"[info] Appended /v1 to base URL: {base_url}")

    # Select professions
    if args.professions:
        selected_professions = args.professions
    else:
        random.seed(args.seed)
        selected_professions = random.sample(PROFESSION_DOMAINS, args.n_professions)

    print(f"Model  : {args.model}")
    print(f"API    : {base_url}")
    print(f"Professions ({len(selected_professions)}): {', '.join(selected_professions)}")
    print(f"Cases/profession: {args.n_cases}")
    print()

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text("", encoding="utf-8")

    total_written = 0
    total_errors = 0

    for idx, profession in enumerate(selected_professions):
        print(f"[{idx+1}/{len(selected_professions)}] Generating {args.n_cases} cases for: {profession} ...", flush=True)
        try:
            cases = generate_cases_for_profession(
                profession=profession,
                n_cases=args.n_cases,
                base_url=base_url,
                api_key=api_key,
                model=args.model,
                timeout_s=args.timeout,
            )
        except (RuntimeError, ValueError) as e:
            print(f"  ERROR generating cases: {e}", file=sys.stderr)
            if args.debug:
                import traceback
                traceback.print_exc()
            total_errors += 1
            continue

        received = len(cases)
        if received < args.n_cases:
            print(f"  WARNING: requested {args.n_cases} cases but got {received}")

        written = 0
        for case in cases[: args.n_cases]:
            errs = validate_case(case)
            if errs:
                print(f"  SKIP {case.get('case_id', '?')}: {'; '.join(errs)}", file=sys.stderr)
                total_errors += 1
                continue
            with args.out.open("a", encoding="utf-8") as f:
                f.write(json.dumps(case, ensure_ascii=False) + "\n")
            written += 1
            total_written += 1

        print(f"  -> wrote {written} valid cases")

        if idx < len(selected_professions) - 1 and args.sleep > 0:
            time.sleep(args.sleep)

    print()
    print(f"Done. Total cases written : {total_written}")
    print(f"      Validation errors    : {total_errors}")
    print(f"      Output file          : {args.out}")
    return 0 if total_errors == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
