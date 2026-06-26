#!/usr/bin/env bash
# /spidershield scan-all
# Scan ALL installed OpenClaw skills for malicious patterns.
# Wraps: spidershield agent-check --skills

set -euo pipefail

echo ""
echo "SpiderShield — Scan All Installed Skills"
echo "(also includes OpenClaw config audit)"
echo ""

# Resolve CLI: prefer spidershield (open-source, pip install spidershield)
if command -v spidershield &>/dev/null; then
  spidershield agent-check --skills
elif python3 -c "import spidershield" 2>/dev/null; then
  python3 -m spidershield agent-check --skills
else
  echo "" >&2
  echo "spidershield not installed. To use this command:" >&2
  echo "" >&2
  echo "  pip install spidershield" >&2
  echo "" >&2
  echo "Or use /spidershield check <skill-name> (works without installation)." >&2
  exit 1
fi
