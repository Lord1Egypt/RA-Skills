"""
parse_changelog.py — Extract and flag risky changelog entries between versions.

Usage: python3 parse_changelog.py <changelog_path> <current_version> <latest_version>
Output: JSON with keys: delta, flagged, [latest_not_local], [same_version], [already_latest]
"""
import sys
import re
import json

if len(sys.argv) < 4:
    print(json.dumps({"error": "Usage: parse_changelog.py <changelog_path> <current> <latest>"}))
    sys.exit(1)

changelog_path = sys.argv[1]
current = sys.argv[2]
latest  = sys.argv[3]

# Validate version format to prevent unexpected string manipulation
VERSION_RE = re.compile(r'^\d{4}\.\d+\.\d+$')
if not VERSION_RE.match(current) or not VERSION_RE.match(latest):
    print(json.dumps({"delta": f"Unexpected version format: current={current!r} latest={latest!r}", "flagged": []}))
    sys.exit(0)

try:
    with open(changelog_path, 'r', encoding='utf-8') as f:
        content = f.read()
except FileNotFoundError:
    print(json.dumps({"delta": f"CHANGELOG.md not found: {changelog_path}", "flagged": []}))
    sys.exit(0)

if not content.strip():
    print(json.dumps({"delta": "CHANGELOG.md exists but is empty.", "flagged": [], "changelog_empty": True}))
    sys.exit(0)

# Split into version blocks (entries start with "## YYYY.N.N")
# CHANGELOG headings may be "## 2026.4.14" or "## 2026.4.14 — title"; capture only version portion.
blocks = re.split(r'\n(?=## \d{4}\.\d+\.\d)', content)
version_map = {}
for block in blocks:
    m = re.match(r'^## (\d{4}\.\d+\.\d+)', block)  # strict: digits only up to version number
    if m:
        version_map[m.group(1)] = block.strip()

# Versions are in reverse chronological order (newest first) as per OpenClaw CHANGELOG
all_versions = list(version_map.keys())

if current == latest:
    print(json.dumps({"delta": "", "flagged": [], "same_version": True}))
    sys.exit(0)

if latest not in version_map:
    # latest is newer than all local CHANGELOG entries (not yet installed)
    idx_current = all_versions.index(current) if current in all_versions else -1
    if idx_current == -1:
        print(json.dumps({
            "delta": f"Current version {current} not found in local CHANGELOG.",
            "flagged": [],
            "latest_not_local": True
        }))
        sys.exit(0)

    if current == all_versions[0]:
        # Current is already the local CHANGELOG's newest; new version changelog unavailable until installed
        note = (
            f"⚠️  Version {latest} changelog is not available locally (only present after installation).\n"
            f"Local CHANGELOG newest: {all_versions[0]} (currently installed: {current}).\n"
            f"New version details can be reviewed after updating."
        )
        print(json.dumps({
            "delta": note,
            "flagged": [],
            "latest_not_local": True
        }, ensure_ascii=False))
        sys.exit(0)

    # There are intermediate local versions between current and the local CHANGELOG head
    note = (
        f"⚠️  Version {latest} changelog is not available locally.\n"
        f"Showing locally known entries newer than {current}:\n\n"
    )
    delta_blocks = [version_map[v] for v in all_versions[:idx_current]]
    delta_text = note + "\n\n".join(delta_blocks)

else:
    try:
        idx_current = all_versions.index(current)
        idx_latest  = all_versions.index(latest)
    except ValueError as e:
        print(json.dumps({"delta": f"Version lookup failed: {e}", "flagged": []}))
        sys.exit(0)

    if idx_latest >= idx_current:
        # latest appears at same position or after current — user is at or ahead of registry
        print(json.dumps({"delta": "", "flagged": [], "already_latest": True}))
        sys.exit(0)

    delta_blocks = [version_map[v] for v in all_versions[idx_latest:idx_current]]
    delta_text = "\n\n".join(delta_blocks)

# ── Risk keyword pre-screening ────────────────────────────────────────────────
RISK_KEYWORDS = [
    'breaking', 'deprecated', 'removed', 'migration', 'rename',
    'no longer', 'incompatible', 'must now', 'behavior change',
    'security', 'tighten', 'harden', 'config', 'schema',
    'requires', 'mandatory',
]

flagged = []
for line in delta_text.splitlines():
    stripped = line.strip()
    # Match top-level and nested bullet points (-, *, •)
    if not re.match(r'^[-*•]', stripped):
        continue
    line_lower = stripped.lower()
    matched_kw = [kw for kw in RISK_KEYWORDS if kw in line_lower]
    if matched_kw:
        flagged.append({"line": stripped, "keywords": matched_kw})

# Cap flagged items to avoid overwhelming the agent on large version gaps
if len(flagged) > 30:
    total = len(flagged)
    flagged = flagged[:30]
    flagged.append({"line": f"[... {total - 30} additional flagged items truncated]", "keywords": ["truncated"]})

# Truncate very long deltas to avoid overwhelming the agent context
delta_lines = delta_text.splitlines()
if len(delta_lines) > 250:
    delta_text = "\n".join(delta_lines[:250]) + f"\n\n[... truncated — {len(delta_lines)} total lines]"

print(json.dumps({"delta": delta_text, "flagged": flagged}, ensure_ascii=False))
