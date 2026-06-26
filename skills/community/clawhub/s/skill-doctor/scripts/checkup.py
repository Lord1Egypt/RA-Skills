#!/usr/bin/env python3
"""
Skill Doctor — checkup.py
A diagnostic engine for ClawHub skills and plugins.

Pulls live data via the `clawhub` CLI, compares it against the last stored
snapshot, runs it through a rule-based diagnostic engine, and prints a
prioritized prescription per skill/plugin.

Usage:
    python3 checkup.py --slug proof-of-contribution
    python3 checkup.py --all
    python3 checkup.py --all --deep
    python3 checkup.py --all --chart
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

CONFIG_DIR = Path.home() / ".skill-doctor"
CONFIG_FILE = CONFIG_DIR / "config.json"
STATE_DIR = CONFIG_DIR / "state"
CHARTS_DIR = CONFIG_DIR / "charts"

# --- Thresholds (see references/diagnostic-rules.md for rationale) ---
CONVERSION_RATIO_WARN = 0.05   # installs / downloads below this → conversion flag
STALENESS_DAYS_WARN = 90       # days since last version bump
ACTIVE_DROP_PCT_WARN = 0.25    # active installs dropping by this fraction → risk


def ensure_dirs():
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    if not CONFIG_FILE.exists():
        CONFIG_FILE.write_text(json.dumps(
            {"slugs": [], "plugins": [], "anthropic_api_key": None}, indent=2
        ))


def load_config():
    ensure_dirs()
    try:
        return json.loads(CONFIG_FILE.read_text())
    except json.JSONDecodeError:
        print("⚠️  config.json is corrupted, recreating defaults", file=sys.stderr)
        default = {"slugs": [], "plugins": [], "anthropic_api_key": None}
        CONFIG_FILE.write_text(json.dumps(default, indent=2))
        return default


def fetch_skill(slug: str) -> dict | None:
    """Fetch live data for a skill via clawhub inspect."""
    try:
        result = subprocess.run(
            ["clawhub", "inspect", slug, "--json"],
            capture_output=True, text=True, timeout=30
        )
    except FileNotFoundError:
        print("❌ clawhub CLI not found. Install it before running Skill Doctor.", file=sys.stderr)
        sys.exit(1)
    except subprocess.TimeoutExpired:
        print(f"⚠️  Timed out fetching '{slug}', skipping", file=sys.stderr)
        return None

    if result.returncode != 0 or not result.stdout.strip():
        print(f"⚠️  Could not fetch '{slug}', skipping", file=sys.stderr)
        return None

    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        print(f"⚠️  Bad JSON for '{slug}', skipping", file=sys.stderr)
        return None


def fetch_plugin(name: str) -> dict | None:
    """Fetch live data for a plugin via clawhub package inspect."""
    try:
        result = subprocess.run(
            ["clawhub", "package", "inspect", name, "--json"],
            capture_output=True, text=True, timeout=30
        )
    except FileNotFoundError:
        print("❌ clawhub CLI not found. Install it before running Skill Doctor.", file=sys.stderr)
        sys.exit(1)
    except subprocess.TimeoutExpired:
        print(f"⚠️  Timed out fetching plugin '{name}', skipping", file=sys.stderr)
        return None

    if result.returncode != 0 or not result.stdout.strip():
        print(f"⚠️  Could not fetch plugin '{name}', skipping", file=sys.stderr)
        return None

    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        print(f"⚠️  Bad JSON for plugin '{name}', skipping", file=sys.stderr)
        return None


def state_path(key: str) -> Path:
    safe_key = key.replace("/", "_").replace("@", "")
    return STATE_DIR / f"{safe_key}.json"


def load_previous_state(key: str) -> dict | None:
    p = state_path(key)
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text())
    except json.JSONDecodeError:
        return None


def save_state(key: str, snapshot: dict):
    state_path(key).write_text(json.dumps(snapshot, indent=2))


def extract_metrics(raw: dict, is_plugin: bool) -> dict:
    """Normalize the clawhub JSON payload into a flat metrics dict."""
    inner = raw.get("skill") or raw.get("package") or raw
    stats = inner.get("stats") or {}

    if is_plugin:
        downloads = stats.get("downloads", inner.get("downloads", 0)) or 0
        installs = stats.get("installs", inner.get("installs", 0)) or 0
        active_installs = installs
        stars = stats.get("stars", inner.get("stars", 0)) or 0
        version = inner.get("latestVersion") or inner.get("version", "unknown")
    else:
        downloads = stats.get("downloads", inner.get("downloads", 0)) or 0
        installs = stats.get("installsAllTime", inner.get("installsAllTime", 0)) or 0
        active_installs = stats.get("installsCurrent", inner.get("installsCurrent", 0)) or 0
        stars = stats.get("stars", inner.get("stars", 0)) or 0
        version = inner.get("version", "unknown")

    display_name = inner.get("displayName", inner.get("slug", "unknown"))

    verdict_block = raw.get("moderation") or inner.get("moderation") or {}
    verdict = (
        verdict_block.get("verdict")
        or raw.get("scanStatus")
        or inner.get("scanStatus")
        or "unknown"
    )
    reason_codes = verdict_block.get("reasonCodes") or []

    return {
        "display_name": display_name,
        "downloads": downloads,
        "installs_all_time": installs,
        "active_installs": active_installs,
        "stars": stars,
        "verdict": verdict,
        "reason_codes": reason_codes,
        "version": version,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
    }


def diagnose(key: str, current: dict, previous: dict | None) -> dict:
    """Run all rule-based checks and return a structured diagnosis."""
    findings = []

    downloads = current["downloads"]
    installs = current["installs_all_time"]
    active = current["active_installs"]
    verdict = current["verdict"]
    reason_codes = current.get("reason_codes", [])

    # --- Trust check ---
    if verdict in ("suspicious", "malware"):
        findings.append({
            "category": "moderation",
            "severity": "critical",
            "text": f"Verdict is '{verdict}' — this affects trust and visibility immediately."
        })
    elif verdict == "pending":
        findings.append({
            "category": "moderation",
            "severity": "info",
            "text": "Scan is pending — verdict not yet available."
        })

    if reason_codes:
        codes_str = ", ".join(reason_codes)
        findings.append({
            "category": "moderation",
            "severity": "warning",
            "text": (
                f"Verdict is 'clean' but flagged for manual review ({codes_str}). "
                "The dashboard will show this as 'Review' rather than 'Pass'."
            )
        })

    # --- Conversion check ---
    if downloads >= 20:  # only meaningful with enough volume
        ratio = installs / downloads if downloads else 0
        if ratio < CONVERSION_RATIO_WARN:
            findings.append({
                "category": "conversion",
                "severity": "warning",
                "text": (
                    f"Only {ratio:.1%} of downloads convert to installs "
                    f"({installs}/{downloads}). Consider tightening the description "
                    "or clarifying setup instructions — people are downloading but not adopting."
                )
            })

    # --- Momentum / delta check (needs previous state) ---
    if previous:
        d_downloads = downloads - previous.get("downloads", downloads)
        d_active = active - previous.get("active_installs", active)

        if d_downloads > 0:
            findings.append({
                "category": "momentum",
                "severity": "info",
                "text": f"Downloads grew by {d_downloads} since last check."
            })
        elif d_downloads == 0:
            findings.append({
                "category": "momentum",
                "severity": "info",
                "text": "No new downloads since last check — flat."
            })

        # Active-install drop check
        prev_active = previous.get("active_installs", 0)
        if prev_active >= 5 and d_active < 0:
            drop_pct = abs(d_active) / prev_active
            if drop_pct >= ACTIVE_DROP_PCT_WARN:
                findings.append({
                    "category": "risk",
                    "severity": "critical",
                    "text": (
                        f"Active installs dropped {drop_pct:.0%} "
                        f"({prev_active} → {active}) — users may be uninstalling. "
                        "Check recent versions for breaking changes."
                    )
                })
    else:
        findings.append({
            "category": "vitals",
            "severity": "info",
            "text": "First check-up for this item — establishing baseline, no trend data yet."
        })

    # --- Determine overall status ---
    if any(f["severity"] == "critical" for f in findings):
        status = "critical"
    elif any(f["severity"] == "warning" for f in findings):
        status = "needs-attention"
    else:
        status = "healthy"

    return {
        "status": status,
        "findings": findings,
    }


def prescribe(findings: list[dict]) -> list[str]:
    """Turn findings into concrete next actions, highest priority first."""
    actions = []
    severity_rank = {"critical": 0, "warning": 1, "info": 2}
    ordered = sorted(findings, key=lambda f: severity_rank.get(f["severity"], 3))

    for f in ordered:
        if f["category"] == "moderation" and f["severity"] == "critical":
            actions.append("Review moderation flags now and address any policy violations before doing anything else.")
        elif f["category"] == "conversion":
            actions.append("Rewrite the description's first two lines to state the concrete problem solved — this is usually the highest-leverage fix for conversion.")
        elif f["category"] == "risk":
            actions.append("Diff the last two versions for breaking changes and consider a patch release.")
        elif f["category"] == "staleness":
            actions.append("Ship a small update — even a docs/example refresh signals active maintenance.")

    # de-duplicate while preserving order
    seen = set()
    unique = []
    for a in actions:
        if a not in seen:
            unique.append(a)
            seen.add(a)
    return unique[:3]  # cap at top 3, per "don't chase every metric"


def format_report(key: str, current: dict, diagnosis: dict, previous: dict | None) -> str:
    lines = []
    lines.append(f"## 🩺 {current['display_name']} ({key})")
    lines.append("")
    lines.append(f"**Status**: {diagnosis['status']}")
    verdict_display = current['verdict']
    if current.get('reason_codes'):
        verdict_display = f"{current['verdict']} (flagged for review)"
    lines.append(f"**Verdict**: {verdict_display}")
    lines.append("")
    lines.append("### Vitals")

    d_downloads = ""
    if previous:
        delta = current["downloads"] - previous.get("downloads", current["downloads"])
        d_downloads = f" (Δ since last check: {delta:+d})"
    lines.append(f"- Downloads: {current['downloads']}{d_downloads}")
    lines.append(f"- Installs (all-time): {current['installs_all_time']}")
    lines.append(f"- Active installs: {current['active_installs']}")
    lines.append(f"- Stars: {current['stars']}")
    lines.append("")

    lines.append("### Findings")
    if diagnosis["findings"]:
        for f in diagnosis["findings"]:
            lines.append(f"- [{f['severity']}] {f['text']}")
    else:
        lines.append("- No notable findings.")
    lines.append("")

    actions = prescribe(diagnosis["findings"])
    lines.append("### Prescription")
    if actions:
        for i, a in enumerate(actions, 1):
            lines.append(f"{i}. {a}")
    else:
        lines.append("1. No action needed — keep doing what you're doing.")
    lines.append("")
    lines.append("---")
    return "\n".join(lines)


def run_checkup(key: str, is_plugin: bool) -> tuple[dict, dict] | None:
    raw = fetch_plugin(key) if is_plugin else fetch_skill(key)
    if raw is None:
        return None

    current = extract_metrics(raw, is_plugin)
    previous = load_previous_state(key)
    diagnosis = diagnose(key, current, previous)
    save_state(key, current)
    return current, diagnosis, previous


def main():
    parser = argparse.ArgumentParser(description="Skill Doctor — ClawHub portfolio check-up")
    parser.add_argument("--slug", help="Check a single skill by slug")
    parser.add_argument("--plugin", help="Check a single plugin by name")
    parser.add_argument("--all", action="store_true", help="Check every skill and plugin in config")
    parser.add_argument("--deep", action="store_true", help="Add AI-narrated analysis (requires API key)")
    parser.add_argument("--chart", action="store_true", help="Generate a trend chart PNG")
    args = parser.parse_args()

    config = load_config()

    targets = []  # list of (key, is_plugin)
    if args.slug:
        targets.append((args.slug, False))
    if args.plugin:
        targets.append((args.plugin, True))
    if args.all:
        targets.extend((s, False) for s in config.get("slugs", []))
        targets.extend((p, True) for p in config.get("plugins", []))

    if not targets:
        print("No targets specified. Use --slug, --plugin, or --all (with config.json populated).")
        print(f"Edit {CONFIG_FILE} to add slugs/plugins for --all to work.")
        sys.exit(1)

    reports = []
    structured_results = []

    for key, is_plugin in targets:
        result = run_checkup(key, is_plugin)
        if result is None:
            continue
        current, diagnosis, previous = result
        reports.append(format_report(key, current, diagnosis, previous))
        structured_results.append({"key": key, "current": current, "diagnosis": diagnosis})

    if not reports:
        print("No data could be fetched for any target.")
        sys.exit(1)

    print(f"\n# Skill Doctor Check-Up — {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}\n")
    print(f"Checked {len(reports)} item(s)\n")
    for r in reports:
        print(r)
        print()

    if args.deep:
        try:
            from deep_analysis import run_deep_analysis
            run_deep_analysis(structured_results, config.get("anthropic_api_key"))
        except ImportError:
            print("⚠️  deep_analysis.py not found alongside checkup.py — skipping --deep", file=sys.stderr)

    if args.chart:
        try:
            from chart import generate_chart
            generate_chart(structured_results, CHARTS_DIR)
        except ImportError:
            print("⚠️  chart.py not found alongside checkup.py — skipping --chart", file=sys.stderr)


if __name__ == "__main__":
    main()
