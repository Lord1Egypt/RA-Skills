#!/usr/bin/env python3
"""Run P02 matching benchmark cases through an OpenAI-compatible Chat Completions API.

Reads ``benchmarks/matching/cases.jsonl``, calls the model once per case with the
in-repo P02 prompt + rubric context, writes ``outputs.jsonl`` (``case_id`` + ``p02``),
then optionally runs ``compare_matching_benchmark.py``.

Environment:
  OPENAI_API_KEY   Required (unless --dry-run).
  OPENAI_BASE_URL  Optional; default ``https://api.openai.com/v1``.

Example:
  set OPENAI_API_KEY=sk-...
  python run_matching_benchmark_llm.py --out run-outputs.jsonl --compare
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as e:
            raise SystemExit(f"{path}:{line_no}: invalid JSON: {e}") from e
    return rows


def package_root(script: Path) -> Path:
    return script.resolve().parent.parent


def load_text(rel: str, root: Path) -> str:
    p = root / rel
    if not p.is_file():
        raise SystemExit(f"Missing required file: {p}")
    return p.read_text(encoding="utf-8")


def extract_json_object(text: str) -> dict[str, Any]:
    text = text.strip()
    m = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
    if m:
        text = m.group(1).strip()
    dec = json.JSONDecoder()
    start = text.find("{")
    if start < 0:
        raise ValueError("no JSON object in model output")
    try:
        obj, _end = dec.raw_decode(text, start)
    except json.JSONDecodeError:
        end = text.rfind("}")
        if start >= 0 and end > start:
            obj = json.loads(text[start : end + 1])
        else:
            raise
    if not isinstance(obj, dict):
        raise ValueError("model output is not a JSON object")
    return obj


def catalog_to_candidates(catalog: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for item in catalog:
        if not isinstance(item, dict):
            continue
        sid = item.get("id")
        if not isinstance(sid, str):
            continue
        excerpt = item.get("skill_body_excerpt")
        excerpts: list[str] = []
        if isinstance(excerpt, str) and excerpt.strip():
            excerpts.append(excerpt.strip())
        out.append(
            {
                "id": sid,
                "name": item.get("name", ""),
                "description": item.get("description", ""),
                "registry_status": item.get("registry_status", "active"),
                "excerpts": excerpts,
            }
        )
    return out


def build_user_payload(case: dict[str, Any]) -> dict[str, Any]:
    jd = case.get("gold_jd")
    if not isinstance(jd, dict):
        raise ValueError("case missing gold_jd object")
    catalog = case.get("skill_catalog")
    if not isinstance(catalog, list):
        raise ValueError("case missing skill_catalog array")
    matching = case.get("matching")
    if not isinstance(matching, dict):
        matching = {}
    delegate_min = matching.get("delegate_min_score", 75)
    confirm_min = matching.get("confirm_band_min", 60)
    return {
        "case_id": case.get("case_id"),
        "user_task": case.get("user_task", ""),
        "jd": jd,
        "candidates": catalog_to_candidates(catalog),
        "matching_config": {
            "delegate_min_score": delegate_min,
            "confirm_band_min": confirm_min,
        },
    }


def chat_completion(
    *,
    base_url: str,
    api_key: str,
    model: str,
    messages: list[dict[str, str]],
    temperature: float,
    timeout_s: int,
) -> str:
    url = base_url.rstrip("/") + "/chat/completions"
    body = json.dumps(
        {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "response_format": {"type": "json_object"},
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


def main() -> int:
    script = Path(__file__)
    root = package_root(script)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--cases",
        type=Path,
        default=root / "benchmarks" / "matching" / "cases.jsonl",
    )
    parser.add_argument("--out", type=Path, required=True, help="outputs.jsonl path")
    parser.add_argument("--model", default="gpt-4o-mini")
    parser.add_argument(
        "--base-url",
        default=os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1"),
    )
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument("--sleep", type=float, default=0.35, help="seconds between calls")
    parser.add_argument("--limit", type=int, default=0, help="only first N cases (0=all)")
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="print first user message only; no network",
    )
    parser.add_argument(
        "--compare",
        action="store_true",
        help="run compare_matching_benchmark.py after writing outputs",
    )
    args = parser.parse_args()

    if not args.cases.is_file():
        print(f"Cases not found: {args.cases}", file=sys.stderr)
        return 2

    p02_doc = load_text("references/prompts/P02-match-installed.md", root)
    rubric_doc = load_text("references/03-matching-rubric.md", root)
    lexicon_doc = load_text("references/matching-lexicon.md", root)

    system_parts = [
        "You execute Skill-HR phase P02 (match installed skills to a JD).",
        "Follow the procedures and JSON shape below exactly.",
        "Return a single JSON object with one top-level key: \"p02\".",
        "The value of \"p02\" must satisfy schemas/p02-output.schema.json (same repo):",
        "required keys: recall_shortlist, candidates, best, decision, decision_rationale.",
        "Each candidate must include skill_id, skill_name, score, subscores (five ints summing to score),",
        "competency_coverage_matrix (one row per jd.must_have_competency string), evidence, gaps, confidence.",
        "recall_shortlist must list every skill_id that appears in candidates, in recall order.",
        "candidates must be exactly one row per id in recall_shortlist, same set.",
        "Omit terminated and frozen skills from the pool. Apply skill-hr exclusion per lexicon for non-meta JDs.",
        "\n--- P02 specification ---\n",
        p02_doc,
        "\n--- Matching rubric ---\n",
        rubric_doc,
        "\n--- Matching lexicon ---\n",
        lexicon_doc,
    ]
    system_content = "".join(system_parts)

    cases = load_jsonl(args.cases)
    if args.limit and args.limit > 0:
        cases = cases[: args.limit]

    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not args.dry_run and not api_key:
        print("OPENAI_API_KEY is not set.", file=sys.stderr)
        return 2

    rows_out: list[dict[str, Any]] = []
    args.out.parent.mkdir(parents=True, exist_ok=True)
    # Truncate then append per row so a long run keeps partial results if a later case fails.
    args.out.write_text("", encoding="utf-8")

    for i, case in enumerate(cases):
        cid = case.get("case_id")
        if not isinstance(cid, str):
            print(f"skip row {i}: missing case_id", file=sys.stderr)
            continue
        try:
            payload = build_user_payload(case)
        except ValueError as e:
            print(f"{cid}: {e}", file=sys.stderr)
            continue
        user_content = (
            "Produce only JSON: {\"p02\": { ... }}.\n\nINPUT:\n"
            + json.dumps(payload, ensure_ascii=False, indent=2)
        )
        messages = [
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content},
        ]
        if args.dry_run:
            print("--- dry-run first user message (truncated) ---")
            print(user_content[:4000])
            return 0

        assert api_key
        print(f"{cid} ...", flush=True)
        content = chat_completion(
            base_url=args.base_url,
            api_key=api_key,
            model=args.model,
            messages=messages,
            temperature=args.temperature,
            timeout_s=args.timeout,
        )
        try:
            obj = extract_json_object(content)
        except (json.JSONDecodeError, ValueError) as e:
            print(f"{cid}: bad JSON: {e}\n--- raw ---\n{content[:2000]}", file=sys.stderr)
            return 1
        p02 = obj.get("p02")
        if not isinstance(p02, dict):
            print(f"{cid}: missing p02 object", file=sys.stderr)
            return 1
        row = {"case_id": cid, "p02": p02}
        rows_out.append(row)
        with args.out.open("a", encoding="utf-8") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
        if args.sleep > 0 and i < len(cases) - 1:
            time.sleep(args.sleep)

    print(f"Wrote {len(rows_out)} lines to {args.out}")

    if args.compare:
        cmp_script = script.parent / "compare_matching_benchmark.py"
        cmd = [
            sys.executable,
            str(cmp_script),
            "--cases",
            str(args.cases.resolve()),
            "--outputs",
            str(args.out.resolve()),
        ]
        print("Running:", " ".join(cmd))
        return subprocess.call(cmd)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
