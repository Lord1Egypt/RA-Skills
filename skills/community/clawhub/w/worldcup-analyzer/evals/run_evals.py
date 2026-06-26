"""Local eval runner for the worldcup-analyzer skill.

Run this on your dev machine where the prediction API is reachable
(typically https://www.jiajielitong.com in production, or
http://localhost:8000 during dev).

Prereqs for live API cases:
    export SOCCER_API_KEY="your_key_here"
    export WORLDCUP_API_BASE="https://www.jiajielitong.com"   # optional default

If SOCCER_API_KEY is missing, live cases are skipped by default so local evals
do not consume Agent temporary-key credits accidentally. To test live calls
with the automatic temp-key flow, set RUN_AGENT_TEMP_LIVE_EVALS=1.

Usage:
    cd /home/mira/files/skills/worldcup-analyzer
    python3 evals/run_evals.py

What it does:
    Executes the three eval cases declared in evals/evals.json. For the two
    prediction cases it actually calls the API and renders via
    format_prediction(). For the compliance case it does NOT call the API
    (the whole point is that the skill must refuse) — it just checks that
    the refusal template from references/compliance.md is reachable and
    free of forbidden phrases.

    For each case it prints:
      - the prompt
      - the rendered output (or refusal text)
      - PASS / FAIL for each must_include / must_not_include assertion
      - a final summary line

Exit code 0 if all cases pass, 1 otherwise.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL_ROOT = HERE.parent
sys.path.insert(0, str(SKILL_ROOT / "scripts"))

from wc_client import (  # noqa: E402
    WorldCupAPIError,
    cache_clear,
    canonicalize_team_name,
    first_use_message,
    format_prediction,
    format_response,
    predict_match,
)

EVALS_PATH = HERE / "evals.json"

# The refusal template lifted from references/compliance.md. The runner
# uses this directly for the compliance case so we don't need an LLM in
# the loop to evaluate refusal behavior — we just verify the canonical
# refusal text passes the forbidden-phrase check.
REFUSAL_TEMPLATE_EN = (
    "This skill is for statistical analysis only, not betting advice. "
    "I can show you the model's projected outcome and expected goal "
    "difference for any specific matchup — just tell me which two teams "
    "you'd like compared, and you can interpret the numbers however you "
    "like."
)

LIVE_CASES = {
    "predict_basic_worldcup",
    "predict_alias_reverse_fixture",
    "validate_team_typo_suggestion",
}


def run_case(case: dict) -> tuple[bool, str]:
    """Execute a single eval case. Returns (passed, rendered_output)."""
    case_id = case["id"]

    if case_id == "compliance_refuse_betting":
        # No API call: this case asserts the refusal template is correct.
        rendered = format_response(REFUSAL_TEMPLATE_EN)
        return _assert(case, rendered), rendered

    if case_id == "predict_basic_worldcup":
        data = predict_match("Germany", "France", "worldcup")
        rendered = format_prediction(data)
        return _assert(case, rendered), rendered

    if case_id == "predict_alias_reverse_fixture":
        # Verifies the alias map handles both Chinese user phrasing and
        # common English aliases before the quota-burning prediction call.
        assert canonicalize_team_name("USA") == "United States"
        assert canonicalize_team_name("美国") == "United States"
        assert canonicalize_team_name("Korea") == "South Korea"
        assert canonicalize_team_name("韩国") == "South Korea"
        data = predict_match("United States", "South Korea", "worldcup")
        rendered = format_prediction(data)
        return _assert(case, rendered), rendered

    if case_id == "format_chinese_quota_limit":
        data = {
            "results": {
                "home_team": "Brazil",
                "visitor_team": "Morocco",
                "win_goals": 0.57,
                "win_or_not": "Win",
                "updatedAt": "2026-06-07 05:01:07.298412",
            },
            "usage": {"used": 4, "limit": 4, "vip_level": "plus"},
        }
        rendered = format_prediction(data, language="zh")
        return _assert(case, rendered), rendered

    if case_id == "first_use_missing_key_zh":
        rendered = first_use_message("zh")
        return _assert(case, rendered), rendered

    raise ValueError(f"Unknown case id: {case_id}")


def _assert(case: dict, rendered: str) -> bool:
    """Check must_include / must_not_include assertions."""
    ok = True
    for needle in case.get("must_include", []):
        if needle.lower() not in rendered.lower():
            print(f"  [FAIL] missing required substring: {needle!r}")
            ok = False
        else:
            print(f"  [pass] contains: {needle!r}")
    for needle in case.get("must_not_include", []):
        if needle.lower() in rendered.lower():
            print(f"  [FAIL] contains forbidden substring: {needle!r}")
            ok = False
        else:
            print(f"  [pass] absent:   {needle!r}")
    return ok


def main() -> int:
    cases = json.loads(EVALS_PATH.read_text(encoding="utf-8"))["cases"]
    has_key = bool(os.environ.get("SOCCER_API_KEY"))
    allow_temp_live = os.environ.get("RUN_AGENT_TEMP_LIVE_EVALS") == "1"
    if not has_key and not allow_temp_live:
        print("SOCCER_API_KEY is not set; live API cases will be skipped.")
        print("Set SOCCER_API_KEY, or set RUN_AGENT_TEMP_LIVE_EVALS=1 to use temp-key credits.")
    cache_clear()

    results: list[tuple[str, bool]] = []
    for case in cases:
        if case["id"] in LIVE_CASES and not has_key and not allow_temp_live:
            print("\n" + "=" * 70)
            print(f"CASE: {case['id']}")
            print("RESULT: SKIP (SOCCER_API_KEY not set)")
            continue
        print("\n" + "=" * 70)
        print(f"CASE: {case['id']}")
        print(f"PROMPT: {case['prompt']}")
        print("-" * 70)
        try:
            passed, rendered = run_case(case)
        except WorldCupAPIError as e:
            print(f"  [ERROR] API call failed: {e}")
            results.append((case["id"], False))
            continue
        except Exception as e:  # noqa: BLE001
            print(f"  [ERROR] unexpected: {type(e).__name__}: {e}")
            results.append((case["id"], False))
            continue
        print("-" * 70)
        print("RENDERED OUTPUT:")
        print(rendered)
        print("-" * 70)
        print(f"RESULT: {'PASS' if passed else 'FAIL'}")
        results.append((case["id"], passed))

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    for cid, ok in results:
        print(f"  {'PASS' if ok else 'FAIL'}  {cid}")
    all_ok = all(ok for _, ok in results)
    print("-" * 70)
    print("OVERALL:", "PASS" if all_ok else "FAIL")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
