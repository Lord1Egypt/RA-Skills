#!/usr/bin/env python3
"""Final-gate verification before session close.

Uses the **four-pillar** framework (Background / Materials / Framework / Intent).
Backward-compat: legacy 7-axis annotations are mapped to pillars automatically.

With --verify-final, runs a quick LLM re-scan on sessions/<id>/final/<primary>.md
to detect if accepted findings were preserved in the final draft (catches the
case where Requester's revised draft silently undoes accepted fixes).

Verdict:
  - READY                    — all pillars pass
  - READY_WITH_OPEN_ITEMS    — some findings unresolvable but no open BLOCKERs
  - FORCED_PARTIAL           — briefer forced close
  - FAIL                     — open BLOCKER remaining (esp. in Intent pillar)
                               or final-verify detected regressions
"""
import argparse
import json
import os
import sys
import urllib.request
from _platform import load_openrouter_key, workspace_root, resolve_responder_name
from pathlib import Path


PILLARS = ["Background", "Materials", "Framework", "Intent"]
CSW_PILLAR = "Intent"   # the single gate pillar — must pass

# Legacy 7-axis → pillar mapping (for annotations produced before the switch)
AXIS_TO_PILLAR = {
    "BLUF": "Intent",
    "Decision Readiness": "Intent",
    "Completeness": "Framework",
    "Assumptions": "Materials",
    "Evidence": "Materials",
    "Red Team": "Materials",
    "Stakeholder": "Materials",
}


def pillar_of(annotation: dict) -> str:
    """Resolve a pillar for an annotation regardless of schema version."""
    if annotation.get("pillar") in PILLARS:
        return annotation["pillar"]
    axis = annotation.get("axis", "")
    return AXIS_TO_PILLAR.get(axis, "Materials")   # default


def load_jsonl(path):
    if not os.path.exists(path): return []
    out = []
    for line in open(path):
        line = line.strip()
        if not line: continue
        try: out.append(json.loads(line))
        except json.JSONDecodeError: pass
    return out


def load_env_key(env_path, key):
    if not Path(env_path).exists(): return None
    for line in Path(env_path).read_text().splitlines():
        if line.startswith(f"{key}="):
            return line.split("=", 1)[1].strip()
    return None


def verify_final_against_accepted(sd: Path, accepted_findings: list, model: str = None):
    if model is None:
        import sys as _sys
        _sys.path.insert(0, str(Path(__file__).parent))
        from _model import get_main_agent_model
        model = get_main_agent_model()
    """LLM re-scan: did the revised final/<primary>.md preserve what was accepted?

    Returns: dict with {regressions_detected: bool, preserved: int, missing: int, missing_ids: [...]}
    """
    final_dir = sd / "final"
    if not final_dir.exists():
        return {"skipped": True, "reason": "no final/ dir"}
    primary = None
    for name in ("revised.md", "final.md", "brief.md"):
        if (final_dir / name).exists():
            primary = final_dir / name
            break
    if not primary:
        candidates = [f for f in final_dir.iterdir() if f.is_file() and f.suffix in (".md", ".txt")]
        if candidates:
            primary = sorted(candidates, key=lambda p: p.stat().st_mtime)[-1]
    if not primary:
        return {"skipped": True, "reason": "no primary final file"}

    final_text = primary.read_text()
    if not accepted_findings:
        return {"skipped": True, "reason": "no accepted findings to verify"}

    api_key = load_openrouter_key()
    if not api_key:
        return {"skipped": True, "reason": "no OPENROUTER_API_KEY"}

    checks = []
    for a in accepted_findings:
        checks.append({
            "id": a.get("id"),
            "pillar": a.get("pillar"),
            "accepted_fix": a.get("suggest") if a.get("status") == "accepted" else a.get("reply","")
        })

    system = "你是 review-agent 的 final gate verifier。给你一份最终 brief 和一组已接受的修改建议。你只需判断每条建议是否体现在最终 brief 里。输出严格 JSON。"
    user = f"""# 最终 brief (final/{primary.name})

{final_text[:6000]}
{'... (truncated)' if len(final_text) > 6000 else ''}

# 已接受的修改建议（应当体现在上述 brief 中）

{json.dumps(checks, indent=2, ensure_ascii=False)}

---

对每个 id 判断：最终 brief 里是否体现了这条修改？

输出严格 JSON：
{{
  "results": [
    {{"id": "...", "preserved": true|false, "note": "简短说明是否体现"}},
    ...
  ]
}}
"""
    body = json.dumps({
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "max_tokens": 1500,
        "temperature": 0.1,
    }).encode()
    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "review-agent",
        }
    )
    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            data = json.loads(resp.read())
        text = data["choices"][0]["message"]["content"]
        # Use shared lenient parser (handles unescaped quotes, newlines, fences)
        import sys
        sys.path.insert(0, str(Path(__file__).parent))
        from _json_repair import parse_lenient_json
        parsed, perr = parse_lenient_json(text, expected="object")
        if parsed is None:
            return {"skipped": True, "reason": f"could not parse LLM response: {perr}; text: {text[:200]}"}
        results = parsed.get("results", [])
        missing = [r for r in results if not r.get("preserved", False)]
        return {
            "skipped": False,
            "primary_file": primary.name,
            "preserved": len(results) - len(missing),
            "missing": len(missing),
            "missing_ids": [r["id"] for r in missing],
            "missing_details": missing,
            "regressions_detected": len(missing) > 0,
        }
    except Exception as e:
        return {"skipped": True, "reason": f"LLM verify failed: {e}"}


def main(session_dir, verify_final=False):
    sd = Path(session_dir)
    meta = json.load(open(sd / "meta.json"))
    ann = load_jsonl(sd / "annotations.jsonl")

    # Group by pillar and count statuses
    per_pillar = {p: {"pass": 0, "open_blocker": 0, "unresolvable": 0, "total": 0}
                  for p in PILLARS}
    for a in ann:
        p = pillar_of(a)
        per_pillar[p]["total"] += 1
        status = a.get("status", "open")
        severity = a.get("severity", "IMPROVEMENT")
        if status == "open" and severity == "BLOCKER":
            per_pillar[p]["open_blocker"] += 1
        elif status == "unresolvable":
            per_pillar[p]["unresolvable"] += 1
        elif status in ("accepted", "modified"):
            per_pillar[p]["pass"] += 1

    # Verdict per pillar
    pillar_verdict = {}
    for p in PILLARS:
        v = per_pillar[p]
        if v["total"] == 0:
            pillar_verdict[p] = "pass"   # no issues found = pass
        elif v["open_blocker"] > 0:
            pillar_verdict[p] = "fail"
        elif v["unresolvable"] > 0:
            pillar_verdict[p] = "unresolvable"
        else:
            pillar_verdict[p] = "pass"

    blocker_open = sum(1 for a in ann
                       if a.get("status") == "open"
                       and a.get("severity") == "BLOCKER")
    unresolvable_count = sum(1 for a in ann if a.get("status") == "unresolvable")

    # Material presence
    final_dir = sd / "final"
    final_files = list(final_dir.iterdir()) if final_dir.exists() else []
    has_final = any(f.is_file() and f.stat().st_size > 0 for f in final_files)

    # Optional final-file verification
    verify_result = None
    if verify_final:
        accepted_or_mod = [a for a in ann if a.get("status") in ("accepted", "modified")]
        verify_result = verify_final_against_accepted(sd, accepted_or_mod)

    # Verdict logic — Intent pillar is the CSW gate
    termination = meta.get("termination")
    if termination == "forced_by_briefer":
        verdict = "FORCED_PARTIAL"
    elif pillar_verdict[CSW_PILLAR] == "fail":
        verdict = "FAIL"   # Intent must pass, non-negotiable
    elif any(v == "fail" for v in pillar_verdict.values()):
        verdict = "FAIL"
    elif verify_result and verify_result.get("regressions_detected"):
        verdict = "FAIL"   # final file lost accepted fixes
    elif unresolvable_count > 0:
        verdict = "READY_WITH_OPEN_ITEMS"
    else:
        verdict = "READY"

    # Detect regressions: BLOCKER appearing in round > 1
    regressions = [
        {"id": a.get("id"), "pillar": pillar_of(a), "issue": a.get("issue","")}
        for a in ann
        if a.get("status") == "open" and a.get("severity") == "BLOCKER"
        and a.get("round", 1) > 1
    ]

    # Separate tally by source (four_pillar_scan vs responder_simulation)
    by_source = {}
    for a in ann:
        src = a.get("source", "legacy")
        by_source[src] = by_source.get(src, 0) + 1

    result = {
        "verdict": verdict,
        "csw_gate_pillar": CSW_PILLAR,
        "csw_gate_status": pillar_verdict[CSW_PILLAR],
        "pillar_verdict": pillar_verdict,
        "pillar_counts": per_pillar,
        "blocker_count_open": blocker_open,
        "unresolvable_count": unresolvable_count,
        "regressions": regressions,
        "has_final_material": has_final,
        "final_files": [f.name for f in final_files if f.is_file()],
        "by_source": by_source,
    }
    if verify_result is not None:
        result["final_verify"] = verify_result

    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(0 if verdict != "FAIL" else 1)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("session_dir")
    ap.add_argument("--verify-final", action="store_true",
                   help="LLM re-scan final/<primary>.md to verify accepted findings preserved")
    args = ap.parse_args()
    main(args.session_dir, verify_final=args.verify_final)