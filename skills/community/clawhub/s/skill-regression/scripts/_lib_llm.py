#!/usr/bin/env python3
"""
_lib_llm.py — Unified OpenAI-compatible LLM client.

Used by both:
  - Agent layer (api backend): trigger -> LLM acting as skill -> response
  - Scoring layer (always):    score 0-10 of response vs expected
  - Inference layer:           AI-generate test cases from SKILL.md

Uses stdlib urllib only (zero external deps).
"""
from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from typing import Optional


def chat_completion(
    messages: list,
    api_key: str,
    base_url: str,
    model: str,
    timeout: int = 60,
    max_retries: int = 2,
    temperature: float = 0.3,
) -> str:
    """
    Call OpenAI-compatible chat completion API.
    Returns assistant message content (string).
    Raises RuntimeError on failure.
    """
    url = base_url.rstrip("/") + "/chat/completions"
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
    }
    data = json.dumps(payload).encode("utf-8")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    last_err = None
    for attempt in range(max_retries + 1):
        try:
            req = urllib.request.Request(url, data=data, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                body = resp.read().decode("utf-8")
            obj = json.loads(body)
            choices = obj.get("choices") or []
            if not choices:
                raise RuntimeError(f"LLM returned no choices: {body[:200]}")
            return choices[0].get("message", {}).get("content", "")
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="replace")[:300]
            last_err = f"HTTP {e.code}: {err_body}"
            # 4xx (except 429) shouldn't retry
            if 400 <= e.code < 500 and e.code != 429:
                raise RuntimeError(f"LLM call failed (no retry): {last_err}")
        except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
            last_err = f"network: {e}"
        except Exception as e:
            last_err = f"unexpected: {e}"

        if attempt < max_retries:
            time.sleep(1.5 ** attempt)

    raise RuntimeError(f"LLM call failed after {max_retries+1} attempts: {last_err}")


def simulate_skill_response(
    skill_md_content: str,
    trigger: str,
    cfg: dict,
    timeout: int = 60,
) -> str:
    """
    Agent layer (api backend): feed SKILL.md as system prompt, trigger as user message.
    Returns the LLM's response (simulating what an agent following this skill would do).
    """
    system_prompt = (
        "You are an AI assistant following the skill specification below. "
        "When the user message matches this skill's trigger conditions, respond "
        "as if you were executing this skill. Follow its instructions precisely.\n\n"
        "--- SKILL.md ---\n"
        f"{skill_md_content}\n"
        "--- END SKILL.md ---"
    )
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": trigger},
    ]
    return chat_completion(
        messages=messages,
        api_key=cfg["SR_LLM_API_KEY"],
        base_url=cfg["SR_LLM_BASE_URL"],
        model=cfg["SR_LLM_MODEL"],
        timeout=timeout,
    )


def score_response(
    response: str,
    expected: str,
    case_input: str,
    cfg: dict,
    timeout: int = 30,
) -> tuple[float, str]:
    """
    Scoring layer: ask LLM to judge response quality (0-10).
    Returns (score, reasoning).
    """
    judge_prompt = f"""You are a quality judge. Evaluate the response below against the expected behavior.

USER INPUT: {case_input}

EXPECTED BEHAVIOR: {expected}

ACTUAL RESPONSE:
{response}

Score 0-10 (10=perfect match, 7-8=acceptable with minor issues, 5-6=partial match, 0-4=poor/wrong).

Respond ONLY in this exact JSON format:
{{"score": <number 0-10>, "reason": "<one sentence>"}}"""

    messages = [
        {"role": "system", "content": "You are a strict but fair test result evaluator. Output only JSON."},
        {"role": "user", "content": judge_prompt},
    ]
    raw = chat_completion(
        messages=messages,
        api_key=cfg["SR_LLM_API_KEY"],
        base_url=cfg["SR_LLM_BASE_URL"],
        model=cfg["SR_LLM_MODEL"],
        timeout=timeout,
        temperature=0.0,
    )

    # Parse JSON robustly
    raw = raw.strip()
    # Extract first {...} block
    start = raw.find("{")
    end = raw.rfind("}")
    if start != -1 and end > start:
        try:
            obj = json.loads(raw[start:end+1])
            score = float(obj.get("score", 0))
            reason = str(obj.get("reason", ""))
            return max(0.0, min(10.0, score)), reason
        except Exception:
            pass
    # Fallback: scrape first number
    import re
    m = re.search(r"\b([0-9]|10)(\.\d+)?\b", raw)
    if m:
        try:
            return float(m.group(0)), raw[:200]
        except Exception:
            pass
    return 0.0, f"unparseable: {raw[:200]}"


def infer_test_cases(
    skill_md: str,
    readme_md: str,
    normal_count: int,
    error_count: int,
    cfg: dict,
    timeout: int = 60,
) -> list:
    """
    Inference layer: generate test case array from SKILL.md/README.md.
    Returns list of dicts (may be empty on failure).
    """
    prompt = f"""Generate {normal_count} normal test cases + {error_count} error cases for this skill.

--- SKILL.md ---
{skill_md[:4000]}

--- README.md ---
{readme_md[:2000] if readme_md else "(none)"}

Output a JSON array. Each item must have:
{{
  "id": "tc-XXX",
  "name": "short test name",
  "description": "what this case tests",
  "is_error_case": false,
  "trigger": "user message that should activate the skill",
  "script_cmd": "shell command to run, or empty string",
  "expected_output": "keyword/regex for script output, or empty",
  "expected_output_mode": "contains",
  "expected_agent_response": "natural language description of expected response"
}}

Use placeholders {{SKILL_DIR}}, {{TESTRES_DIR}}, {{WORK_DIR}} in script_cmd if needed.
Output ONLY the JSON array, no markdown fences, no explanation."""

    messages = [
        {"role": "system", "content": "You are a test case generator. Output only valid JSON arrays."},
        {"role": "user", "content": prompt},
    ]
    try:
        raw = chat_completion(
            messages=messages,
            api_key=cfg["SR_LLM_API_KEY"],
            base_url=cfg["SR_LLM_BASE_URL"],
            model=cfg["SR_LLM_MODEL"],
            timeout=timeout,
            temperature=0.5,
        )
    except Exception as e:
        print(f"  ⚠️  LLM inference failed: {e}", file=__import__("sys").stderr)
        return []

    raw = raw.strip()
    # Strip markdown fences if present
    if raw.startswith("```"):
        raw = raw.split("```", 2)[1]
        if raw.lstrip().startswith("json"):
            raw = raw.lstrip()[4:]
    raw = raw.strip().rstrip("`").strip()

    # Extract [...] block
    import re
    m = re.search(r"\[.*\]", raw, re.DOTALL)
    if m:
        try:
            arr = json.loads(m.group())
            if isinstance(arr, list):
                return arr
        except Exception as e:
            print(f"  ⚠️  Could not parse test cases JSON: {e}", file=__import__("sys").stderr)
    return []
