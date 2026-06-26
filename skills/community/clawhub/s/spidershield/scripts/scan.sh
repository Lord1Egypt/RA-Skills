#!/usr/bin/env bash
# /spidershield scan <path>
# Scan a single skill for malicious patterns (24 detection rules).
# Wraps: spidershield agent-check <path> (open-source CLI)

set -euo pipefail

TARGET="${1:-}"
if [[ -z "$TARGET" ]]; then
  echo "Usage: /spidershield scan <path-to-skill-or-SKILL.md>" >&2
  echo "" >&2
  echo "Examples:" >&2
  echo "  /spidershield scan ./my-skill/" >&2
  echo "  /spidershield scan ./my-skill/SKILL.md" >&2
  exit 1
fi

echo ""
echo "SpiderShield — Skill Malware Scan"
echo "Target: $TARGET"
echo ""

# Resolve CLI: prefer spidershield (open-source, pip install spidershield)
if command -v spidershield &>/dev/null; then
  spidershield agent-check "$TARGET"
elif python3 -c "import spidershield" 2>/dev/null; then
  python3 -m spidershield agent-check "$TARGET"
else
  echo "" >&2
  echo "spidershield not installed. To use this command:" >&2
  echo "" >&2
  echo "  pip install spidershield" >&2
  echo "" >&2
  echo "Or use /spidershield check <skill-name> (works without installation)." >&2
  exit 1
fi
