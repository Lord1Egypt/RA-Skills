#!/usr/bin/env bash
set -euo pipefail

status=0

for file in \
  "workspace/skills/self-improving-agent/scripts/activator.sh" \
  "workspace/skills/self-improving-agent/scripts/error-detector.sh" \
  "workspace/skills/self-improving-agent/scripts/extract-skill.sh"; do
  if [[ -x "$file" ]]; then
    echo "[ok] executable: $file"
  elif [[ -f "$file" ]]; then
    echo "[warn] not executable: $file" >&2
    status=1
  else
    echo "[missing] $file" >&2
    status=1
  fi
done

if [[ -d ".learnings" ]]; then
  echo "[ok] .learnings directory exists in current working directory"
else
  echo "[warn] .learnings directory not found in current working directory"
  echo "[hint] create with: mkdir -p .learnings"
fi

for log in LEARNINGS.md ERRORS.md FEATURE_REQUESTS.md; do
  if [[ -f ".learnings/$log" ]]; then
    echo "[ok] .learnings/$log"
  else
    echo "[warn] missing .learnings/$log"
  fi
done

if [[ $status -ne 0 ]]; then
  echo "Environment check found issues." >&2
  exit 1
fi

echo "Environment check complete."
