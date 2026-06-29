#!/usr/bin/env python3
"""
generate_report.py — Merge test results into a Markdown report.

Open-source version:
  - Writes Markdown to local file (--output).
  - Optionally invokes a user-defined upload hook (env: SR_REPORT_UPLOAD_HOOK)
    after writing the report, passing the report path as $1 and skill name as $2.
    The hook script's stdout becomes the printed URL.
  - AI suggestion layer uses _lib_llm (OpenAI-compatible) instead of internal CLI.
"""
import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# Local imports
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib_config import resolve_config  # noqa: E402
from _lib_llm import chat_completion  # noqa: E402


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--skill-dir", required=True)
    p.add_argument("--cases", required=True)
    p.add_argument("--script-results", required=True)
    p.add_argument("--agent-results", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--threshold", type=float, default=7.0)
    p.add_argument("--skip-agent", type=str, default="false")
    p.add_argument("--detail", type=str, default="false", help="Detailed mode: full input/output for each case")
    p.add_argument("--no-ai-suggestions", type=str, default="false", help="Skip AI improvement suggestions (saves LLM calls)")
    p.add_argument("--space-dir", default="", help="skill-regression-space root")
    return p.parse_args()


def _rule_suggestions(skill_dir: str, total: int, script_fail: int, agent_fail: int, skip_agent: bool) -> list:
    """Rule-based fallback suggestions (no LLM call). Shared with ai_suggestions."""
    base = []
    has_test_file = os.path.exists(os.path.join(skill_dir, "TEST.md"))
    if not has_test_file:
        base.append("Recommend creating a TEST.md to define test cases explicitly for better accuracy")
    if script_fail > 0:
        base.append("Script-layer failures present — check script dependencies and path configuration")
    if not skip_agent and agent_fail > 0:
        base.append("AI-layer scores below threshold — refine SKILL.md trigger phrasing for clearer semantics")
    if total < 5:
        base.append(f"Only {total} test cases — consider adding more edge cases for better coverage")
    if not base:
        base.append("Skill is in good shape! Keep adding tests for new functionality.")
    return base


def ai_suggestions(
    skill_name, skill_dir, cases, script_results, agent_results,
    skip_agent, total, script_fail, agent_fail,
) -> list:
    """Generate rule-based suggestions, then try LLM for failure-specific advice."""
    base = _rule_suggestions(skill_dir, total, script_fail, agent_fail, skip_agent)

    failed_summary = []
    script_by_id = {r["id"]: r for r in script_results}
    agent_by_id  = {r["id"]: r for r in agent_results}
    for c in cases:
        sr = script_by_id.get(c["id"], {})
        ar = agent_by_id.get(c["id"], {})
        if sr.get("status") == "fail":
            failed_summary.append(
                f"- [{c['id']}] script fail: {c['name']} | cmd: {sr.get('script_cmd','')} | reason: {sr.get('match_reason') or sr.get('error','')}"
            )
        if ar.get("status") == "fail" and not skip_agent:
            failed_summary.append(
                f"- [{c['id']}] AI fail ({ar.get('score',0):.1f}): {c['name']} | expected: {ar.get('expected_response','')} | got: {str(ar.get('actual_response',''))[:100]}"
            )

    if not failed_summary:
        return base

    # Try LLM suggestions
    try:
        cfg = resolve_config(project_dir=Path(skill_dir).parent if skill_dir else None)
        if not cfg.get("SR_LLM_API_KEY"):
            return base  # No LLM key, stick with rule-based
        prompt = (
            f"You are a skill quality engineer reviewing regression test results for: {skill_name}\n\n"
            f"Failed cases:\n" + "\n".join(failed_summary) + "\n\n"
            "Provide 2-4 specific, actionable improvement suggestions (one per line, max 50 chars each).\n"
            "Output ONLY a bulleted list (lines starting with '-'). No numbering, no extra text."
        )
        out = chat_completion(
            messages=[
                {"role": "system", "content": "You output only concise bulleted improvement suggestions."},
                {"role": "user", "content": prompt},
            ],
            api_key=cfg["SR_LLM_API_KEY"],
            base_url=cfg.get("SR_LLM_BASE_URL", "https://api.openai.com/v1"),
            model=cfg.get("SR_LLM_MODEL", "gpt-4o-mini"),
            timeout=30,
        )
        ai_items = [
            line.lstrip("- •·").strip()
            for line in out.strip().splitlines()
            if line.strip().startswith(("-", "•", "·")) and len(line.strip()) > 3
        ]
        if ai_items:
            return base + ai_items
    except Exception:
        pass
    return base


def status_icon(status: str) -> str:
    return {"pass": "✅", "fail": "❌", "skip": "⏭️"}.get(status, "❓")


def overall_status(pass_rate: float, has_normal_failure: bool) -> tuple[str, str]:
    if pass_rate >= 0.9 and not has_normal_failure:
        return "🟢 Healthy", "Core functionality OK, pass rate excellent"
    elif pass_rate >= 0.7:
        return "🟡 Needs attention", "Some cases failed, check failure details"
    else:
        return "🔴 At risk", "Low pass rate or core failure, fix immediately"


def truncate(text: str, max_len: int = 300) -> str:
    """Truncate long text gracefully. For longer thresholds, keep head and tail."""
    text = text.strip()
    if len(text) <= max_len:
        return text
    if max_len >= 600:
        half = max_len // 2
        return text[:half] + f"\n… ({len(text)} chars total, middle omitted) …\n" + text[-half:]
    return text[:max_len] + f"\n… ({len(text)} chars total, truncated)"


def generate_markdown(
    skill_name: str,
    skill_dir: str,
    cases: list,
    script_results: list,
    agent_results: list,
    threshold: float,
    skip_agent: bool,
    detail_mode: bool,
    now: str,
    source: str = "TEST.md",
    no_ai_suggestions: bool = False,
) -> str:
    # Build case_id index
    script_by_id = {r["id"]: r for r in script_results}
    agent_by_id = {r["id"]: r for r in agent_results}

    # Stats
    total = len(cases)
    script_pass = sum(1 for r in script_results if r["status"] == "pass")
    script_fail = sum(1 for r in script_results if r["status"] == "fail")
    agent_pass = sum(1 for r in agent_results if r["status"] == "pass")
    agent_fail = sum(1 for r in agent_results if r["status"] == "fail")

    # Combined pass: script not failed AND AI not failed (skipped doesn't count as failed)
    combined_pass = sum(
        1 for c in cases
        if script_by_id.get(c["id"], {}).get("status") != "fail"
        and agent_by_id.get(c["id"], {}).get("status") != "fail"
    )
    combined_rate = combined_pass / total if total > 0 else 0

    # Has any normal-flow failure
    has_normal_failure = any(
        c["type"] == "normal" and (
            script_by_id.get(c["id"], {}).get("status") == "fail" or
            agent_by_id.get(c["id"], {}).get("status") == "fail"
        )
        for c in cases
    )

    overall_label, overall_summary = overall_status(combined_rate, has_normal_failure)
    core_ok = "✅ OK" if not has_normal_failure else "❌ Failed"

    script_rate_str = f"{script_pass}/{total} ({script_pass/total:.0%})" if total else "N/A"
    agent_rate_str = (
        f"{agent_pass}/{total} ({agent_pass/total:.0%})" if not skip_agent and total
        else "skipped"
    )
    combined_rate_str = f"{combined_pass}/{total} ({combined_rate:.0%})" if total else "N/A"

    mode_label = "Detailed" if detail_mode else "Simple"

    lines = [
        f"# [{skill_name}] Regression Test Report",
        "",
        f"| Field | Value |",
        f"|-------|-------|",
        f"| Test time | {now} |",
        f"| Test runner | skill-regression (open-source) |",
        f"| Total cases | {total} |",
        f"| Case source | {source} |",
        f"| Script-layer pass rate | {script_rate_str} |",
        f"| AI-layer pass rate | {agent_rate_str} |",
        f"| Combined pass rate | {combined_rate_str} |",
        f"| Semantic score threshold | {threshold} |",
        f"| Scoring caveat | LLM-as-judge with same family ⚠️ |",
        f"| Report mode | {mode_label} |",
        "",
        "---",
        "",
        "## 📋 Conclusion",
        "",
        f"**Overall status**: {overall_label}",
        "",
        f"**Core functionality**: {core_ok}",
        "",
        f"**Summary**: {overall_summary}",
        "",
        "---",
        "",
        "## 🧪 Case Execution Details",
        "",
    ]

    # Table
    if skip_agent:
        lines += ["| # | Name | Type | Script | Conclusion |",
                  "|---|------|------|--------|------------|"]
    else:
        lines += ["| # | Name | Type | Script | AI | Score | Conclusion |",
                  "|---|------|------|--------|----|----|-----------|"]

    for i, case in enumerate(cases, 1):
        sr = script_by_id.get(case["id"], {})
        ar = agent_by_id.get(case["id"], {})
        s_icon = status_icon(sr.get("status", "skip"))
        a_icon = status_icon(ar.get("status", "skip"))
        score_str = f"{ar.get('score', 0):.1f}" if ar.get("score") is not None else "—"
        combined = (
            "Passed" if sr.get("status") != "fail" and ar.get("status") != "fail"
            else "Failed"
        )
        type_label = {"normal": "normal", "error": "error", "edge": "edge"}.get(case["type"], case["type"])

        if skip_agent:
            lines.append(f"| {i} | {case['name']} | {type_label} | {s_icon} | {combined} |")
        else:
            lines.append(f"| {i} | {case['name']} | {type_label} | {s_icon} | {a_icon} | {score_str} | {combined} |")

    # Failure Details
    failed_cases = [
        c for c in cases
        if script_by_id.get(c["id"], {}).get("status") == "fail"
        or agent_by_id.get(c["id"], {}).get("status") == "fail"
    ]

    # ── Failure Details (both modes output failed cases) ──
    if failed_cases:
        lines += ["", "---", ""]
        for case in failed_cases:
            sr = script_by_id.get(case["id"], {})
            ar = agent_by_id.get(case["id"], {})
            type_label = {"normal": "normal", "error": "error", "edge": "edge"}.get(case["type"], case["type"])
            lines += [
                f"### ❌ {case['name']} Failure Detail",
                "",
                f"**Type**: {type_label}  ",
                f"**Trigger**: `{case.get('trigger', '')}`",
                "",
            ]
            # Script layer
            if sr.get("status") == "fail":
                actual_out = truncate(sr.get('actual_output', ''), 1500)
                lines += [
                    f"**Script layer**: ❌ Failed  ",
                    f"- Command:`{sr.get('script_cmd', '')}`",
                    f"- Expected match:`{sr.get('expected_output', '')}` ({sr.get('match_mode', '')})",
                    f"- Actual output:",
                    f"```",
                    actual_out or "(no output)",
                    f"```",
                    f"- FailedReason: {sr.get('match_reason', '') or sr.get('error', '')}",
                    "",
                ]
            else:
                lines.append(f"**Script layer**: {status_icon(sr.get('status', 'skip'))} {sr.get('match_reason', '')}  \n")

            # AI Layer
            if not skip_agent:
                if ar.get("status") == "fail":
                    actual_resp = truncate(ar.get('actual_response', ''), 3000)
                    lines += [
                        f"**AI Layer**: ❌ Failed (score {ar.get('score', 0):.1f}, threshold {threshold})  ",
                        f"- Expected: {ar.get('expected_response', '')}",
                        f"- Actual response: ",
                        f"```",
                        actual_resp or "(no response)",
                        f"```",
                        f"- Score reason: {ar.get('score_reason', '')}",
                        "",
                    ]
                else:
                    _score = ar.get('score')
                    _score_str = f"{_score:.1f}" if _score is not None else "—"
                    lines.append(f"**AI Layer**: {status_icon(ar.get('status', 'skip'))} Score {_score_str}  \n")

    # ── Detailed mode: expand every case (including passed) ──
    if detail_mode:
        lines += ["", "---", "", "## 📂 Full Case Records(Detailed mode)", ""]
        for i, case in enumerate(cases, 1):
            sr = script_by_id.get(case["id"], {})
            ar = agent_by_id.get(case["id"], {})
            s_status = sr.get("status", "skip")
            a_status = ar.get("status", "skip")
            combined_ok = s_status != "fail" and a_status != "fail"
            type_label = {"normal": "normal", "error": "error", "edge": "edge"}.get(case["type"], case["type"])
            icon = "✅" if combined_ok else "❌"

            lines += [
                f"### {icon} Case {i}: {case['name']}",
                "",
                f"| Field | Value |",
                f"|------|------|",
                f"| Type | {type_label} |",
                f"| Trigger | `{case.get('trigger', '')}` |",
                f"| Conclusion | {'Passed' if combined_ok else 'Failed'} |",
                "",
            ]

            # Script layerDetail
            if sr.get("script_cmd", "").strip():
                actual_out = truncate(sr.get("actual_output", ""), 2000)
                lines += [
                    f"**🔧 Script Layer**: {status_icon(s_status)} {sr.get('match_reason', sr.get('error', ''))}",
                    f"",
                    f"Command:",
                    f"```bash",
                    sr.get("script_cmd", ""),
                    f"```",
                    f"Expected output ({sr.get('match_mode', 'contains')}): `{sr.get('expected_output', '(no assertion)')}`",
                    f"",
                    f"Actual output: ",
                    f"```",
                    actual_out or "(no output)",
                    f"```",
                    f"Elapsed: {sr.get('duration_ms', 0)}ms",
                    "",
                ]
            else:
                lines += [
                    f"**🔧 Script Layer**: ⏭️ Skipped(no script cmd)",
                    "",
                ]

            # AI LayerDetail
            if not skip_agent:
                score = ar.get("score")
                score_str = f"{score:.1f}" if score is not None else "—"
                actual_resp = truncate(ar.get("actual_response", ""), 4000)
                lines += [
                    f"**🤖 AI Layer**: {status_icon(a_status)} Score {score_str} / {threshold}",
                    f"",
                    f"Trigger: `{case.get('trigger', '')}`",
                    f"",
                    f"Expected: {ar.get('expected_response', case.get('expected_agent_response', ''))}",
                    f"",
                    f"Actual response: ",
                    f"```",
                    actual_resp or "(no response / skipped)",
                    f"```",
                    f"Score reason: {ar.get('score_reason', '')}",
                    f"Elapsed: {ar.get('duration_ms', 0)}ms",
                    "",
                ]
            else:
                lines += [f"**🤖 AI Layer**: ⏭️ Skipped(--skip-agent)", ""]

            lines.append("---")

    # Known issues / TODO
    lines += ["", "---", "", "## 🐛 Known Issues / TODO", ""]
    issues = []
    for case in failed_cases:
        sr = script_by_id.get(case["id"], {})
        ar = agent_by_id.get(case["id"], {})
        if sr.get("status") == "fail":
            issues.append((
                "High" if case["type"] == "normal" else "Medium",
                f"Script layerFailed: {case['name']}",
                case["id"],
            ))
        if ar.get("status") == "fail" and not skip_agent:
            issues.append((
                "Medium" if case["type"] == "normal" else "Low",
                f"AI Layer score below threshold({ar.get('score', 0):.1f}): {case['name']}",
                case["id"],
            ))

    if issues:
        lines += ["| # | Severity | Description | Related cases |",
                  "|---|---------|------|---------|"]
        for i, (severity, desc, cid) in enumerate(issues, 1):
            lines.append(f"| {i} | {severity} | {desc} | {cid} |")
    else:
        lines.append("No known issues 🎉")

    # Improvement Suggestions (rule fallback + LLM-enhanced)
    # --no-ai-suggestions skips LLM call, output only rule-based suggestions
    lines += ["", "---", "", "## 💡 Improvement Suggestions", ""]
    if no_ai_suggestions:
        print("  ℹ️  --no-ai-suggestions: skipping LLM suggestions, rule-based only")
        suggestions = _rule_suggestions(skill_dir, total, script_fail, agent_fail, skip_agent)
    else:
        suggestions = ai_suggestions(
            skill_name=skill_name,
            skill_dir=skill_dir,
            cases=cases,
            script_results=script_results,
            agent_results=agent_results,
            skip_agent=skip_agent,
            total=total,
            script_fail=script_fail,
            agent_fail=agent_fail,
        )
    for i, s in enumerate(suggestions, 1):
        lines.append(f"{i}. {s}")

    # Appendix
    lines += [
        "",
        "---",
        "",
        "## 📎 Appendix",
        "",
        f"- **Skill path**: `{skill_dir}`",
        f"- **Case source**: {source}",
        f"- **Report generated at**: {now}",
    ]

    return "\n".join(lines)


def main():
    args = parse_args()
    skip_agent = args.skip_agent.lower() in ("true", "1", "yes")
    no_ai_suggestions = args.no_ai_suggestions.lower() in ("true", "1", "yes")
    space_dir = os.path.expanduser(args.space_dir) if args.space_dir else ""

    # Input file existence check (clearer error than a crash)
    for label, path in [
        ("cases", args.cases),
        ("script-results", args.script_results),
        ("agent-results", args.agent_results),
    ]:
        if not os.path.exists(path):
            print(f"  ❌ Error: could not find {label} file: {path}", file=sys.stderr)
            sys.exit(1)

    with open(args.cases, "r", encoding="utf-8") as f:
        cases_data = json.load(f)
    with open(args.script_results, "r", encoding="utf-8") as f:
        script_results = json.load(f)
    with open(args.agent_results, "r", encoding="utf-8") as f:
        agent_raw = json.load(f)
    # Schema compat: run_agent_tests writes {"backend":..., "results":[...]};
    # older test fixtures may write a bare list. Normalize to list.
    agent_results = agent_raw.get("results", agent_raw) if isinstance(agent_raw, dict) else agent_raw

    skill_name = cases_data["skill_name"]
    skill_dir = cases_data["skill_dir"]
    cases = cases_data["cases"]
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    now_date = datetime.now().strftime("%Y-%m-%d")

    detail_mode = args.detail.lower() in ("true", "1", "yes")

    report_md = generate_markdown(
        skill_name=skill_name,
        skill_dir=skill_dir,
        cases=cases,
        script_results=script_results,
        agent_results=agent_results,
        threshold=args.threshold,
        skip_agent=skip_agent,
        detail_mode=detail_mode,
        now=now,
        source=cases_data.get("source", "TEST.md"),
        no_ai_suggestions=no_ai_suggestions,
    )

    # Write local report
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(report_md)
    print(f"  → Report saved: {args.output}")

    # Optional upload hook (user-provided script via SR_REPORT_UPLOAD_HOOK env var)
    # The hook receives: $1 = report path, $2 = skill name, $3 = date.
    # It should print the resulting URL to stdout (one line). Exit 0 on success.
    upload_hook = os.environ.get("SR_REPORT_UPLOAD_HOOK", "").strip()
    upload_url = ""
    if upload_hook:
        print(f"  → Running upload hook: {upload_hook}")
        try:
            proc = subprocess.run(
                [upload_hook, args.output, skill_name, now_date],
                capture_output=True, text=True, timeout=120,
            )
            if proc.returncode == 0:
                upload_url = proc.stdout.strip().splitlines()[-1] if proc.stdout.strip() else ""
                if upload_url:
                    print(f"\n  📄 Uploaded: {upload_url}")
            else:
                print(f"  ⚠️  Upload hook failed (exit={proc.returncode}): {proc.stderr[:200]}")
        except Exception as e:
            print(f"  ⚠️  Upload hook error: {e}")

    # Output report path for shell script consumption
    print(f"REPORT_PATH={args.output}")
    if upload_url:
        print(f"REPORT_URL={upload_url}")


if __name__ == "__main__":
    main()
