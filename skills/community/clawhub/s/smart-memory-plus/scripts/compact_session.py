#!/usr/bin/env python3
"""
compact_session.py — Context compression for OpenClaw sessions.

Extracts structured digests from conversation text, saves to disk,
and retrieves recent compacts for injection into new sessions.

Usage:
  compact_session.py --extract < conversation.txt
  compact_session.py --from-file conversation.md
  compact_session.py --list
  compact_session.py --latest
  compact_session.py --stats
"""

import argparse
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

WORKSPACE = Path(os.environ.get("OPENCLAW_WORKSPACE", os.path.expanduser("~/.openclaw/workspace")))
COMPACTS_DIR = WORKSPACE / "memory" / "compacts"

# Hard security: verify all paths stay within workspace
def assert_safe_path(path: Path) -> None:
    """Reject any path outside workspace/memory/compacts/."""
    try:
        resolved = path.resolve()
        workspace_resolved = WORKSPACE.resolve()
        if not str(resolved).startswith(str(workspace_resolved)):
            raise ValueError(f"Path outside workspace: {resolved}")
        if not str(resolved).startswith(str(COMPACTS_DIR.resolve())):
            if resolved != WORKSPACE / "SESSION-STATE.md":
                raise ValueError(f"Write outside compacts dir: {resolved}")
    except (OSError, ValueError) as e:
        print(f"SECURITY: {e}")
        sys.exit(1)

# Sensitive patterns — strip from compacts
SENSITIVE = re.compile(
    r"(?:password|passwd|pwd)\s*[:=]\s*\S+|"
    r"(?:api[_-]?key|token|secret|bearer)\s*[:=]\s*\S+|"
    r"clh_[A-Za-z0-9]{30,}|sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{30,}|"
    r"-----BEGIN (?:RSA |EC )?PRIVATE KEY-----",
    re.IGNORECASE,
)

# Patterns to redact — paths and URLs replaced with placeholders
REDACT_PATH = re.compile(r"(?:^|[\s(])((?:/[\w.\-]+){2,}|(?:~|\.)/[\w./\-]+)")
REDACT_URL = re.compile(r"https?://[^\s\])>\"]+")
REDACT_INTERNAL = re.compile(r"(?:localhost|127\.0\.0\.1|10\.\d+\.\d+\.\d+|172\.(?:1[6-9]|2\d|3[01])\.\d+\.\d+|192\.168\.\d+\.\d+)[^\s\])>\"]*")

# Patterns for extraction
DECISION_PATTERNS = [
    re.compile(r"(?:chose|decided|going with|picked|selected|settled on)\s+(.{10,100})", re.IGNORECASE),
    re.compile(r"(?:决定|选择|用|采用)\s*(.{5,80})", re.IGNORECASE),
]

FACT_PATTERNS = {
    "PROJ": re.compile(r"(?:project|repo|website|site|app|项目|网站|仓库)[\s:：]+(.{5,100})", re.IGNORECASE),
    "TECH": re.compile(r"(?:config|database|api|port|server|配置|数据库|端口|服务器)[\s:：]+(.{5,80})", re.IGNORECASE),
}

PENDING_PATTERNS = [
    re.compile(r"(?:TODO|todo|待办|下一步|next step|later|need to)[\s:：]*(.{5,100})", re.IGNORECASE),
    re.compile(r"\[ \]\s*(.{5,100})"),
]

BLOCKER_PATTERNS = [
    re.compile(r"(?:blocked by|need .+ first|waiting for|需要先|等.+才能)\s*(.{5,80})", re.IGNORECASE),
]

NOISE_PATTERNS = [
    re.compile(r"^(ok|好的|嗯|emmm|哈哈|haha|lol|nice|cool|谢谢|thanks)\s*[.。!！]*$", re.IGNORECASE),
    re.compile(r"^.{0,5}$"),  # Too short
]


def is_noise(line: str) -> bool:
    """Check if a line is noise (greetings, filler, etc.)."""
    stripped = line.strip()
    if not stripped:
        return True
    return any(p.match(stripped) for p in NOISE_PATTERNS)


def sanitize(text: str) -> str:
    """Remove sensitive data, redact paths and URLs, strip control characters."""
    # Redact secrets first
    text = SENSITIVE.sub("[REDACTED]", text)
    # Redact internal IPs
    text = REDACT_INTERNAL.sub("<INTERNAL_URL>", text)
    # Redact URLs
    text = REDACT_URL.sub("<REDACTED_URL>", text)
    # Redact file paths (2+ segments)
    text = REDACT_PATH.sub(lambda m: m.group(0).replace(m.group(1), "<REDACTED_PATH>"), text)
    # Strip control chars
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", text)
    return text.strip()


def extract_from_text(text: str) -> dict:
    """Extract structured data from conversation text."""
    lines = text.split("\n")
    decisions = []
    facts = {"PROJ": [], "URL": [], "PATH": [], "TECH": []}
    pending = []
    blockers = []
    total_lines = 0
    noise_lines = 0

    for line in lines:
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("```"):
            continue

        total_lines += 1
        if is_noise(line):
            noise_lines += 1
            continue

        # Sanitize
        safe = sanitize(line)
        if not safe or safe == "[REDACTED]":
            continue

        # Extract decisions
        for pat in DECISION_PATTERNS:
            m = pat.search(safe)
            if m:
                decisions.append(sanitize(m.group(0)))
                break

        # Extract facts
        for fact_type, pat in FACT_PATTERNS.items():
            matches = pat.findall(safe)
            for match in matches:
                if isinstance(match, tuple):
                    match = match[0] if match else ""
                if match and len(match) > 3:
                    facts[fact_type].append(match)

        # Extract pending
        for pat in PENDING_PATTERNS:
            m = pat.search(safe)
            if m:
                pending.append(sanitize(m.group(1) if m.lastindex else m.group(0)))
                break

        # Extract blockers
        for pat in BLOCKER_PATTERNS:
            m = pat.search(safe)
            if m:
                blockers.append(sanitize(m.group(1) if m.lastindex else m.group(0)))
                break

    # Deduplicate
    for key in facts:
        facts[key] = list(dict.fromkeys(facts[key]))[:5]  # Cap at 5 per type
    decisions = list(dict.fromkeys(decisions))[:10]
    pending = list(dict.fromkeys(pending))[:10]
    blockers = list(dict.fromkeys(blockers))[:5]

    # Estimate tokens saved
    est_tokens = total_lines * 25  # Rough: 25 tokens per line average
    compact_tokens = (len(decisions) + sum(len(v) for v in facts.values()) +
                      len(pending) + len(blockers)) * 15
    tokens_saved = max(0, est_tokens - compact_tokens)

    return {
        "decisions": decisions,
        "facts": facts,
        "pending": pending,
        "blockers": blockers,
        "total_lines": total_lines,
        "noise_lines": noise_lines,
        "tokens_saved": tokens_saved,
    }


def format_compact(data: dict, summary: str = "") -> str:
    """Format extracted data as a compact markdown document."""
    now = datetime.now(timezone.utc)
    ts = now.strftime("%Y-%m-%d %H:%M UTC")
    filename_ts = now.strftime("%Y-%m-%d-%H%M")

    lines = [
        f"# Session Compact — {ts}",
        f"**Lines processed**: {data['total_lines']} | **Noise filtered**: {data['noise_lines']} | **Est. tokens saved**: ~{data['tokens_saved']:,}",
        "",
    ]

    if data["decisions"]:
        lines.append("## Decisions Made")
        for d in data["decisions"]:
            lines.append(f"- {d}")
        lines.append("")

    all_facts = []
    for fact_type, items in data["facts"].items():
        for item in items:
            tag = f"[{fact_type}]" if fact_type in ("PROJ", "TECH") else ""
            all_facts.append(f"{tag} {item}".strip())

    if all_facts:
        lines.append("## Facts Established")
        for f in all_facts:
            lines.append(f"- {f}")
        lines.append("")

    if data["pending"]:
        lines.append("## Pending Actions")
        for p in data["pending"]:
            lines.append(f"- [ ] {p}")
        lines.append("")

    if data["blockers"]:
        lines.append("## Blockers")
        for b in data["blockers"]:
            lines.append(f"- ⚠️ {b}")
        lines.append("")

    if summary:
        lines.append("## Session Summary")
        lines.append(summary)
        lines.append("")

    return "\n".join(lines)


def save_compact(content: str) -> Path:
    """Save compact to disk. Only to memory/compacts/."""
    COMPACTS_DIR.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc)
    filename = f"{now.strftime('%Y-%m-%d-%H%M')}.md"
    filepath = COMPACTS_DIR / filename
    assert_safe_path(filepath)

    # Avoid overwriting existing
    counter = 1
    while filepath.exists():
        filepath = COMPACTS_DIR / f"{now.strftime('%Y-%m-%d-%H%M')}-{counter}.md"
        counter += 1

    filepath.write_text(content, encoding="utf-8")

    # Keep only last 30 compacts
    compacts = sorted(COMPACTS_DIR.glob("*.md"))
    while len(compacts) > 30:
        compacts.pop(0).unlink()

    return filepath


def cmd_extract(text: str):
    """Extract and format a compact from text, print to stdout (no save)."""
    data = extract_from_text(text)
    content = format_compact(data)
    print(content)


def cmd_write(text: str):
    """Write a compact through the full security pipeline (sanitize + path check + save)."""
    data = extract_from_text(text)
    # Also sanitize the raw text for any missed patterns
    sanitized_text = sanitize(text)
    content = format_compact(data)
    filepath = save_compact(content)
    print(f"Compact saved: {filepath}")
    print(f"  Decisions: {len(data['decisions'])}")
    print(f"  Facts: {sum(len(v) for v in data['facts'].values())}")
    print(f"  Pending: {len(data['pending'])}")


def cmd_write_raw(content: str):
    """Write pre-formatted compact content through security checks only."""
    # Verify no sensitive data in the content
    if SENSITIVE.search(content):
        print("SECURITY: Content contains sensitive patterns. Redact and retry.")
        sys.exit(1)
    if REDACT_URL.search(content):
        print("SECURITY: Content contains URLs. Replace with <REDACTED_URL> and retry.")
        sys.exit(1)
    if REDACT_INTERNAL.search(content):
        print("SECURITY: Content contains internal IPs. Replace with <INTERNAL_URL> and retry.")
        sys.exit(1)
    if REDACT_PATH.search(content):
        print("SECURITY: Content contains file paths. Replace with <REDACTED_PATH> and retry.")
        sys.exit(1)

    filepath = save_compact(content)
    print(f"Compact saved: {filepath}")


def cmd_from_file(filepath: str):
    """Extract compact from a file. Restricted to workspace only."""
    path = Path(filepath)
    if not path.exists():
        print(f"File not found: {filepath}")
        sys.exit(1)
    # Security: only read files inside workspace
    assert_safe_path(path)
    text = path.read_text(encoding="utf-8")
    cmd_extract(text)


def cmd_list():
    """List all compacts."""
    if not COMPACTS_DIR.exists():
        print("No compacts found.")
        return

    compacts = sorted(COMPACTS_DIR.glob("*.md"))
    if not compacts:
        print("No compacts found.")
        return

    for c in compacts:
        size = c.stat().st_size
        mtime = datetime.fromtimestamp(c.stat().st_mtime, tz=timezone.utc).strftime("%Y-%m-%d %H:%M")
        print(f"  {c.name}  ({size:,}B, {mtime} UTC)")
    print(f"Total: {len(compacts)} compacts")


def cmd_latest():
    """Print the latest compact."""
    if not COMPACTS_DIR.exists():
        print("No compacts found.")
        return

    compacts = sorted(COMPACTS_DIR.glob("*.md"))
    if not compacts:
        print("No compacts found.")
        return

    latest = compacts[-1]
    print(latest.read_text(encoding="utf-8"))


def cmd_stats():
    """Show compaction statistics."""
    if not COMPACTS_DIR.exists():
        print("No compacts found.")
        return

    compacts = sorted(COMPACTS_DIR.glob("*.md"))
    if not compacts:
        print("No compacts found.")
        return

    total_size = sum(c.stat().st_size for c in compacts)
    total_tokens_saved = 0

    for c in compacts:
        content = c.read_text(encoding="utf-8")
        m = re.search(r"tokens saved\*\*: ~([\d,]+)", content)
        if m:
            total_tokens_saved += int(m.group(1).replace(",", ""))

    oldest = compacts[0].name
    newest = compacts[-1].name

    print(f"=== Compaction Stats ===")
    print(f"Compacts: {len(compacts)}")
    print(f"Total size: {total_size:,}B")
    print(f"Total est. tokens saved: ~{total_tokens_saved:,}")
    print(f"Date range: {oldest} → {newest}")
    print(f"Avg tokens saved/compact: ~{total_tokens_saved // max(len(compacts), 1):,}")


def main():
    parser = argparse.ArgumentParser(description="Context compactor for OpenClaw sessions")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--extract", action="store_true", help="Extract compact from stdin")
    group.add_argument("--write", action="store_true", help="Write pre-formatted compact from stdin (with security checks)")
    group.add_argument("--from-file", type=str, help="Extract compact from file")
    group.add_argument("--list", action="store_true", help="List all compacts")
    group.add_argument("--latest", action="store_true", help="Print latest compact")
    group.add_argument("--stats", action="store_true", help="Show compaction statistics")

    args = parser.parse_args()

    if args.extract:
        text = sys.stdin.read()
        if not text.strip():
            print("No input provided.")
            sys.exit(1)
        cmd_extract(text)
    elif args.write:
        content = sys.stdin.read()
        if not content.strip():
            print("No input provided.")
            sys.exit(1)
        cmd_write_raw(content)
    elif args.from_file:
        cmd_from_file(args.from_file)
    elif args.list:
        cmd_list()
    elif args.latest:
        cmd_latest()
    elif args.stats:
        cmd_stats()


if __name__ == "__main__":
    main()
