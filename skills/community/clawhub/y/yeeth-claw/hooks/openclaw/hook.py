#!/usr/bin/env python3
"""
OpenClaw — Claude Code PreToolUse hook
Intercepts package install commands and checks for supply chain risk signals
before allowing Claude to execute them.

Tier 1 (WARN)  : package age < 30 days OR typosquat distance < 2
Tier 2 (BLOCK) : package age < 7 days AND typosquat hit
Tier 3 (ARGUS) : BLOCK + submit to Argus API for full analysis (if configured)

Exit codes (Claude Code hook spec):
  0  = allow
  1  = warn (non-blocking, message shown)
  2  = block (tool call is cancelled, message shown to Claude)
"""

from __future__ import annotations

import json
import re
import sys
from lib.registry import get_package_meta
from lib.typosquat import typosquat_score

ARGUS_API_URL = None   # Set via OPENCLAW_ARGUS_URL env var
ARGUS_API_KEY = None   # Set via OPENCLAW_ARGUS_KEY env var

# Package managers to watch and regexes to extract package names from commands
INSTALL_PATTERNS = [
    # npm install pkg, npm i pkg, npm install -g pkg
    (r"npm\s+(?:install|i)\b[^#\n]*", "npm"),
    # yarn add pkg
    (r"yarn\s+add\b[^#\n]*", "npm"),
    # pnpm add pkg
    (r"pnpm\s+add\b[^#\n]*", "npm"),
    # pip install pkg, pip3 install pkg
    (r"pip3?\s+install\b[^#\n]*", "pypi"),
    # cargo add pkg
    (r"cargo\s+add\b[^#\n]*", "crates"),
]

# Flags that indicate local/path installs — skip registry check
LOCAL_INSTALL_RE = re.compile(r'(?:\.{1,2}/|file:|https?://|git\+|github:|tarball)', re.IGNORECASE)


def extract_packages(command: str, ecosystem: str) -> list[str]:
    """Extract package names from an install command, ignoring flags and local paths."""
    # Strip the install verb and everything before it
    cmd = re.sub(r'^.*?(?:install|add|i)\s+', '', command.strip(), count=1, flags=re.IGNORECASE)
    tokens = cmd.split()
    packages = []
    for tok in tokens:
        if tok.startswith('-'):          # flag like -g, --save-dev
            continue
        if LOCAL_INSTALL_RE.search(tok): # local path or URL
            continue
        # Strip version specifiers: pkg@1.2.3, pkg==1.2.3, pkg>=1.0
        name = re.split(r'[@=><~^]', tok)[0].strip()
        if name:
            packages.append(name)
    return packages


def check_package(name: str, ecosystem: str) -> dict:
    """Return a risk dict for a single package."""
    meta = get_package_meta(name, ecosystem)
    if meta is None:
        return {"name": name, "tier": "WARN", "reasons": ["package not found in registry"], "meta": {}}

    score = typosquat_score(name, ecosystem, meta)
    age_days = meta.get("age_days")

    tier = "OK"
    reasons = []

    if age_days is not None:
        if age_days < 7:
            tier = "BLOCK"
            reasons.append(f"published {age_days}d ago (< 7 days)")
        elif age_days < 30:
            tier = max_tier(tier, "WARN")
            reasons.append(f"published {age_days}d ago (< 30 days)")

    if score is not None:
        if score >= 0.85:
            tier = "BLOCK"
            reasons.append(f"typosquat score {score:.2f} — possible impersonation of '{meta.get('similar_to', '?')}'")
        elif score >= 0.65:
            if tier == "OK":
                tier = "WARN"
            reasons.append(f"name similar to '{meta.get('similar_to', '?')}' (score {score:.2f})")

    if meta.get("has_install_script") and tier != "OK":
        reasons.append("has postinstall hook")

    return {"name": name, "tier": tier, "reasons": reasons, "meta": meta}


def tier_rank(t: str) -> int:
    return {"OK": 0, "WARN": 1, "BLOCK": 2}.get(t, 0)


def max_tier(a: str, b: str) -> str:
    return a if tier_rank(a) >= tier_rank(b) else b


def main():
    import os

    global ARGUS_API_URL, ARGUS_API_KEY
    ARGUS_API_URL = os.environ.get("OPENCLAW_ARGUS_URL")
    ARGUS_API_KEY = os.environ.get("OPENCLAW_ARGUS_KEY")

    hook_input = json.load(sys.stdin)
    tool_name = hook_input.get("tool_name", "")
    tool_input = hook_input.get("tool_input", {})

    if tool_name != "Bash":
        sys.exit(0)

    command = tool_input.get("command", "")
    if not command:
        sys.exit(0)

    # Collect all package installs found in the command
    hits: list[tuple[str, str]] = []  # (package_name, ecosystem)
    for pattern, ecosystem in INSTALL_PATTERNS:
        for match in re.finditer(pattern, command, re.IGNORECASE):
            for pkg in extract_packages(match.group(), ecosystem):
                hits.append((pkg, ecosystem))

    if not hits:
        sys.exit(0)

    results = [check_package(name, eco) for name, eco in hits]
    worst = "OK"
    for r in results:
        worst = max_tier(worst, r["tier"])

    if worst == "OK":
        sys.exit(0)

    # Build human-readable output
    lines = ["[OpenClaw] Package risk detected:\n"]
    for r in results:
        if r["tier"] == "OK":
            continue
        icon = "⚠" if r["tier"] == "WARN" else "✗"
        lines.append(f"  {icon} {r['name']} [{r['tier']}]")
        for reason in r["reasons"]:
            lines.append(f"      • {reason}")

    if worst == "BLOCK":
        lines.append("\nInstall blocked. Verify these packages before proceeding.")
        if ARGUS_API_URL and ARGUS_API_KEY:
            lines.append("Escalating to Argus for full analysis...")
            try:
                from lib.argus import submit_packages
                job_ids = submit_packages(
                    [(r["name"], r["meta"]) for r in results if r["tier"] == "BLOCK"],
                    ARGUS_API_URL,
                    ARGUS_API_KEY,
                )
                for job_id in job_ids:
                    lines.append(f"  Argus job: {ARGUS_API_URL}/scan/{job_id}")
            except Exception as e:
                lines.append(f"  (Argus submission failed: {e})")
        print("\n".join(lines))
        sys.exit(2)
    else:
        lines.append("\nProceed with caution — verify before installing.")
        print("\n".join(lines))
        sys.exit(1)


if __name__ == "__main__":
    main()
