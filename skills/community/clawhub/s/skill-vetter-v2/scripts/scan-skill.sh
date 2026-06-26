#!/bin/bash
# Local scan helper for Skill Vetter v2
# Usage: ./scan-skill.sh /path/to/skill
set -euo pipefail

TARGET="${1:-}"
if [[ -z "$TARGET" ]]; then
  echo "Usage: $(basename "$0") /path/to/skill" >&2
  exit 1
fi
if [[ ! -d "$TARGET" ]]; then
  echo "Target is not a directory: $TARGET" >&2
  exit 1
fi

if ! command -v grep >/dev/null 2>&1; then
  echo "grep is required" >&2
  exit 1
fi

echo "SKILL VETTER LOCAL SCAN"
echo "Target: $TARGET"
echo "========================================"

echo
echo "Files:"
find "$TARGET" -maxdepth 4 -type f | sort

echo
echo "Potential indicators:"

declare -A CHECKS=(
  [network]='curl |wget |http://|https://|fetch\(|axios|requests\.'
  [credentials]='API_KEY|api_key|token|Authorization:|secret|~/.ssh|~/.aws|credentials'
  [dangerous_exec]='eval\(|exec\(|child_process|subprocess|os\.system|bash -c'
  [package_installs]='npm install|pnpm add|pip install|brew install|apt-get install|yum install'
  [privilege]='sudo|chmod 777|chown '
  [obfuscation]='base64|atob\(|fromCharCode|compressed|minified'
)

for name in "${!CHECKS[@]}"; do
  echo "--- $name ---"
  grep -RInE --exclude-dir=.git --exclude='*.png' --exclude='*.jpg' --exclude='*.jpeg' --exclude='*.gif' "${CHECKS[$name]}" "$TARGET" || true
  echo
 done

echo "Notes:"
echo "- Matches are signals, not automatic proof of malicious behavior."
echo "- Review context, scope, and stated purpose before assigning a verdict."
echo "- Keep the final decision local."
