#!/usr/bin/env python3
"""One-shot finalization pipeline for a signal-scout analysis.json.

Chains what SKILL.md previously required as separate commands — schema
validation, source verification, HTML report generation, CSV export for CRM
import, and (when saved snapshots exist) the cross-run diff — into a single
invocation with one condensed summary, so an agent spends one tool call and a
few output lines instead of four calls and four transcripts.

Usage:
    python3 finalize.py analysis.json [--out report.html] [--validate-only]
        [--skip-verify] [--no-csv] [--no-people] [--timeout 10]
        [--allow-private-addresses] [--use-proxy]

No-people mode (--no-people, or `"people": false` in the input JSON) is the
hard filter for public output: Individuals are dropped before verification,
person names, handles, emails, and profile URLs are redacted from every other
section after it, and every output (filtered JSON, handoff.json, HTML, CSV)
goes to a `public/` folder next to the input. The input file is not modified.
The cross-run diff is skipped in this mode.

Steps (each skippable/failable independently):
  1. validate  — top-level required fields + per-prospect schema via
                 signal_scout_core.validate_prospect, plus a score-drift check
                 recomputing each score from its dimensions. Fails fast, before
                 any network traffic. --validate-only stops here (draft loop).
  2. verify    — runs verify_sources.py with --annotate-out (in place) and
                 --handoff-out <dir>/handoff.json. Prints only non-verified
                 prospects and the tier summary, not the full table.
  3. report    — runs generate_report.py (history/outcomes auto-detected).
  4. csv       — writes <dir>/prospects.csv with the same columns as the HTML
                 report's Export CSV button, ready for spreadsheet/CRM import.
  5. diff      — if sibling analysis-*.json snapshots exist, runs
                 diff_reports.py across all of them (+ sibling outcomes.jsonl).

Exit codes: 1 on validation failure, verify_sources failure (broken source /
not-on-page claim), or report-generation failure.
"""

from __future__ import annotations

import argparse
import atexit
import csv
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from people_filter import add_limits_note, drop_people, has_prospects, redact_people
from signal_scout_core import (
    TIER_BROKEN,
    TIER_LABELS,
    TIER_VERIFIED,
    compute_score,
    csv_safe,
    validate_prospect,
)
from verify_sources import PROXY_HINT, env_proxy_set

SCRIPTS_DIR = Path(__file__).resolve().parent

REQUIRED_TOP_LEVEL = (
    "title", "product", "product_url", "target_customer", "search_scope",
    "generated_at", "verdict", "outreach_plan", "limits",
)

PROSPECT_KINDS = {"individuals": "individual", "segments": "segment", "companies": "company"}

# Bare registrable domain, the key Clay and CRMs match company records on.
DOMAIN_RE = re.compile(r"^(?=.{4,253}$)[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(?:\.[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)+$")

def normalize_domain(value: object) -> str | None:
    """Reduce 'https://www.Acme.com/partners' to 'acme.com'; None when the value
    is not a domain. For model output that finalize.validate never sees (MCP path)."""
    text = str(value or "").strip().lower()
    text = re.sub(r"^[a-z][a-z0-9+.-]*://", "", text).split("/", 1)[0].split("?", 1)[0].split(":", 1)[0]
    text = text.removeprefix("www.")
    return text if DOMAIN_RE.match(text) else None


# Same columns as the HTML report's Export CSV button (report-artifact.md).
CSV_COLUMNS = (
    "type", "name", "domain", "stage", "score", "verification", "pain_signal", "why_fit",
    "why_now", "source_title", "source_url", "source_type", "signal_date",
    "next_action", "caution",
)


def validate(data: dict) -> list[str]:
    errors: list[str] = []
    for field in REQUIRED_TOP_LEVEL:
        if not data.get(field):
            errors.append(f"missing top-level field: {field}")
    if not any(data.get(kind) for kind in PROSPECT_KINDS):
        errors.append("at least one of individuals/segments/companies must be non-empty")
    for kind, prospect_type in PROSPECT_KINDS.items():
        for i, item in enumerate(data.get(kind) or []):
            if not isinstance(item, dict):
                errors.append(f"{kind}[{i}]: must be an object")
                continue
            name = item.get("name") or f"#{i}"
            for problem in validate_prospect(prospect_type, item):
                errors.append(f"{kind}[{i}] ({name}): {problem}")
            dimensions = item.get("dimensions")
            if isinstance(dimensions, dict):
                try:
                    expected = compute_score(prospect_type, dimensions)
                    stated = float(item.get("score", 0))
                    if abs(stated - expected) > 3:
                        errors.append(
                            f"{kind}[{i}] ({name}): score {stated:g} does not match "
                            f"dimensions (computed {expected}) — recompute or fix dimensions"
                        )
                except (TypeError, ValueError):
                    pass
            if kind == "companies" and item.get("domain") not in (None, ""):
                if not DOMAIN_RE.match(str(item.get("domain"))):
                    errors.append(f"{kind}[{i}] ({name}): domain must be a bare lowercase domain like "
                                  f"'acme.com' (no scheme or path), got {item.get('domain')!r}")
            if kind == "companies" and item.get("tier") is not None:
                if item.get("tier") not in (1, 2, 3):
                    errors.append(f"{kind}[{i}] ({name}): tier must be 1, 2, or 3, got {item.get('tier')!r}")
                if not str(item.get("tier_rationale", "")).strip():
                    errors.append(f"{kind}[{i}] ({name}): tier requires tier_rationale")

    summary = data.get("executive_summary")
    if summary is not None and not isinstance(summary, dict):
        errors.append("executive_summary must be an object")

    ctx = data.get("competitive_context")
    if isinstance(ctx, dict):
        for i, entry in enumerate(ctx.get("battlecard") or []):
            if not isinstance(entry, dict):
                errors.append(f"battlecard[{i}]: must be an object")
                continue
            label = entry.get("competitor") or f"#{i}"
            for field in ("competitor", "claim", "evidence", "counter_angle"):
                if not str(entry.get(field, "")).strip():
                    errors.append(f"battlecard[{i}] ({label}): missing {field}")
            if not str(entry.get("source_url", "")).strip().startswith(("http://", "https://")):
                errors.append(f"battlecard[{i}] ({label}): source_url must be a valid http(s) URL — battlecard claims are verified like prospects")
    return errors


def run_step(label: str, cmd: list[str]) -> tuple[int, str]:
    result = subprocess.run(cmd, capture_output=True, text=True)
    output = (result.stdout + result.stderr).strip()
    return result.returncode, output


def next_action_for(kind: str, item: dict) -> str:
    if kind == "individuals":
        return str(item.get("opener") or item.get("suggested_channel") or "")
    if kind == "segments":
        return str(item.get("content_angle") or "")
    return str(item.get("bd_angle") or "")


def write_csv(data: dict, out_path: Path) -> int:
    rows = 0
    with out_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(CSV_COLUMNS)
        for kind, prospect_type in PROSPECT_KINDS.items():
            for item in data.get(kind) or []:
                if not isinstance(item, dict):
                    continue
                writer.writerow(csv_safe(cell) for cell in [
                    prospect_type,
                    item.get("name", ""),
                    item.get("domain") or "",
                    item.get("stage", ""),
                    item.get("score", ""),
                    TIER_LABELS.get(item.get("verification_tier", ""), item.get("verification_tier", "")),
                    item.get("pain_signal", ""),
                    item.get("why_fit", ""),
                    item.get("why_now", ""),
                    item.get("source_title", ""),
                    item.get("source_url", ""),
                    item.get("source_type", ""),
                    item.get("signal_date", ""),
                    next_action_for(kind, item),
                    item.get("caution", ""),
                ])
                rows += 1
    return rows


def finish_people_filter(
    path: Path, data: dict, stats: dict, handoff: Path | None = None, handoff_out: Path | None = None
) -> dict:
    """Phase 2 of no-people mode, after verification: redact person references
    from every string, disclose it in `limits`, and write the public JSON to
    `path` and the redacted handoff to `handoff_out` (default: over `handoff`)."""
    redacted, count = redact_people(data, stats["names"])
    stats["redactions"] = count
    add_limits_note(redacted, stats)
    path.write_text(json.dumps(redacted, indent=2), encoding="utf-8")
    if handoff is not None and handoff.exists():
        handoff_data, _ = redact_people(json.loads(handoff.read_text(encoding="utf-8")), stats["names"])
        add_limits_note(handoff_data, stats)
        (handoff_out or handoff).write_text(json.dumps(handoff_data, indent=2), encoding="utf-8")
    return redacted


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("input", type=Path, help="Path to analysis.json")
    parser.add_argument("--out", type=Path, default=None,
                        help="HTML report path (default: <input dir>/signal-scout-report.html)")
    parser.add_argument("--validate-only", action="store_true",
                        help="Schema-check the JSON and stop — for the drafting loop, no network")
    parser.add_argument("--skip-verify", action="store_true",
                        help="Skip source verification (offline/dry runs only — never for a shipped report)")
    parser.add_argument("--no-csv", action="store_true", help="Skip prospects.csv export")
    parser.add_argument("--no-people", action="store_true",
                        help="Hard filter for public output: no Individuals, no person names, handles, "
                        "or profile URLs anywhere; outputs go to <input dir>/public/. Also on when the "
                        "input JSON has \"people\": false")
    parser.add_argument("--timeout", type=int, default=10, help="Per-fetch timeout for verification")
    parser.add_argument("--allow-private-addresses", action="store_true",
                        help="Let source_url reach loopback and private addresses during verification. "
                        "For checking a local copy of a page; never on input you did not write")
    parser.add_argument("--use-proxy", action="store_true",
                        help="Verify through HTTP(S)_PROXY, for a machine with no direct route out. "
                        "The proxy connects, so DNS rebinding is not prevented")
    args = parser.parse_args()

    input_path = args.input.resolve()
    workdir = input_path.parent

    data = json.loads(input_path.read_text(encoding="utf-8"))
    no_people = args.no_people or data.get("people") is False
    errors = validate(data)
    if errors:
        print(f"VALIDATION FAILED — {len(errors)} problem(s):")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)
    total = sum(len(data.get(kind) or []) for kind in PROSPECT_KINDS)
    print(f"validate: OK — {total} prospect(s), schema and scores consistent")

    people_stats: dict = {}
    if no_people:
        data, people_stats = drop_people(data)
        print(f"no-people: {people_stats['individuals_removed']} Individual(s) and "
              f"{people_stats['dropped_for_personal_source']} prospect(s) with a personal-profile source removed")
        if not has_prospects(data):
            print("no-people: FAILED, no Segments or Companies left to report. A public report needs at "
                  "least one prospect that is not a person.")
            sys.exit(1)
    if args.validate_only:
        return

    if no_people:
        # Never edit the private draft in place. Verification runs on a copy in
        # a private temp dir; only redacted files are ever written to public/,
        # the folder to publish, so an interrupted run cannot leave text there.
        if workdir.name != "public":
            workdir = workdir / "public"
        workdir.mkdir(parents=True, exist_ok=True)
        staging = Path(tempfile.mkdtemp(prefix="signal-scout-private-"))
        atexit.register(shutil.rmtree, staging, True)
        public_path = workdir / input_path.name
        verify_path = staging / input_path.name
        verify_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        input_path = public_path
    else:
        verify_path = input_path
    out_html = args.out or workdir / "signal-scout-report.html"

    if not args.skip_verify:
        handoff = workdir / "handoff.json"
        verify_handoff = verify_path.parent / "handoff.json" if no_people else handoff
        code, _output = run_step("verify", [
            sys.executable, str(SCRIPTS_DIR / "verify_sources.py"), str(verify_path),
            "--timeout", str(args.timeout),
            "--annotate-out", str(verify_path),
            "--handoff-out", str(verify_handoff),
            *(["--allow-private-addresses"] if args.allow_private_addresses else []),
            *(["--use-proxy"] if args.use_proxy else []),
        ])
        # Re-read the annotated JSON rather than parsing the verifier's table —
        # print only what needs action, not every verified row.
        data = json.loads(verify_path.read_text(encoding="utf-8"))
        if no_people:
            data = finish_people_filter(input_path, data, people_stats, verify_handoff, handoff)
        counts: dict[str, int] = {}
        for kind in PROSPECT_KINDS:
            for item in data.get(kind) or []:
                tier = item.get("verification_tier", "unverified")
                counts[tier] = counts.get(tier, 0) + 1
                if tier != TIER_VERIFIED:
                    label = TIER_LABELS.get(tier, tier)
                    print(f"  [{label}] {item.get('name', '(unnamed)')}: "
                          f"{item.get('verification_note') or item.get('source_url', '')}")
                note = item.get("opener_grounding_note")
                if note:
                    print(f"  [Opener] {item.get('name', '(unnamed)')}: {note}")
        ctx = data.get("competitive_context")
        for i, entry in enumerate((ctx.get("battlecard") or []) if isinstance(ctx, dict) else []):
            if not isinstance(entry, dict):
                continue
            tier = entry.get("verification_tier", "unverified")
            label = entry.get("competitor", f"#{i}")
            if tier != TIER_VERIFIED:
                print(f"  [Battlecard/{TIER_LABELS.get(tier, tier)}] {label}: "
                      f"{entry.get('verification_note') or entry.get('source_url', '')}")
            if entry.get("corroboration_note"):
                print(f"  [Battlecard/Single-source] {label}: {entry['corroboration_note']}")
        summary = ", ".join(f"{n} {TIER_LABELS.get(t, t).lower()}" for t, n in sorted(counts.items()))
        print(f"verify: {summary} — handoff written to {handoff}")
        if code != 0:
            if counts.get(TIER_BROKEN) and not args.use_proxy and env_proxy_set():
                print(f"verify: {PROXY_HINT}")
            print("verify: FAILED — fix or drop the prospects above (Not on page / Broken source), then re-run")
            sys.exit(1)
    else:
        print("verify: SKIPPED (--skip-verify) — do not ship this report")
        if no_people:
            data = finish_people_filter(input_path, data, people_stats)
    if no_people:
        print(f"no-people: {people_stats['redactions']} person reference(s) redacted; publish only {workdir}")

    code, output = run_step("report", [
        sys.executable, str(SCRIPTS_DIR / "generate_report.py"), str(input_path), str(out_html),
    ])
    print(f"report: {output}" if code == 0 else f"report: FAILED\n{output}")
    if code != 0:
        sys.exit(1)

    if not args.no_csv:
        csv_path = workdir / "prospects.csv"
        rows = write_csv(data, csv_path)
        print(f"csv: {rows} prospect(s) written to {csv_path} (CRM-import ready)")

    siblings = sorted(p for p in workdir.glob("analysis-*.json") if p.resolve() != input_path)
    if siblings and no_people:
        print("diff: SKIPPED in no-people mode (prior snapshots may name people)")
    elif siblings:
        cmd = [sys.executable, str(SCRIPTS_DIR / "diff_reports.py"), *map(str, siblings), str(input_path)]
        outcomes = workdir / "outcomes.jsonl"
        if outcomes.exists():
            cmd += ["--outcomes", str(outcomes)]
        code, output = run_step("diff", cmd)
        print(f"diff vs {len(siblings)} prior snapshot(s):\n{output}" if code == 0
              else f"diff: FAILED (non-fatal)\n{output}")

    print(f"\nDone: {out_html.resolve()}")


if __name__ == "__main__":
    main()
