#!/usr/bin/env bash
# 功能：检查 Claude Code profile 是否包含关键字段
# 参数：可选，目标文件路径（默认 ./tools/adapt-profiles/claude-code.yaml）
# 用法：bash scripts/check_claude_profile.sh

set -euo pipefail

TARGET_FILE="${1:-./tools/adapt-profiles/claude-code.yaml}"

if [[ ! -f "$TARGET_FILE" ]]; then
  echo "[ERROR] File not found: $TARGET_FILE"
  exit 2
fi

required_keys=(
  "platform: claude-code"
  "detection_signals:"
  "immutable_dirs:"
  "protected_files:"
  "non_interactive_policy:"
  "enforce_blocked_on_ask_user: true"
  "enforce_fail_fast_on_unconfirmed_destructive: true"
  "merge_rules:"
  "constraint: strict_only"
)

missing=0
echo "[INFO] Checking Claude Code profile contract in: $TARGET_FILE"
for key in "${required_keys[@]}"; do
  if grep -Fq "$key" "$TARGET_FILE"; then
    echo "[PASS] Found key: $key"
  else
    echo "[FAIL] Missing key: $key"
    missing=$((missing + 1))
  fi
done

if [[ "$missing" -gt 0 ]]; then
  echo "[ERROR] Claude Code profile check failed: $missing missing key(s)."
  exit 1
fi

echo "[OK] Claude Code profile check passed."
