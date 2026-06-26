#!/usr/bin/env bash
# 功能：检查 OpenClaw profile 是否包含关键安全与合并策略字段
# 参数：可选，目标文件路径（默认 ./tools/adapt-profiles/openclaw.yaml）
# 用法：bash scripts/check_openclaw_profile.sh

set -euo pipefail

TARGET_FILE="${1:-./tools/adapt-profiles/openclaw.yaml}"

if [[ ! -f "$TARGET_FILE" ]]; then
  echo "[ERROR] File not found: $TARGET_FILE"
  exit 2
fi

required_keys=(
  "platform: openclaw"
  "detection_signals:"
  "immutable_dirs:"
  "protected_files:"
  "non_interactive_policy:"
  "enforce_blocked_on_ask_user: true"
  "enforce_fail_fast_on_unconfirmed_destructive: true"
  "logs_policy:"
  "extensions_policy:"
  "merge_rules:"
  "strategy: union"
  "constraint: strict_only"
)

missing=0
echo "[INFO] Checking OpenClaw profile contract in: $TARGET_FILE"
for key in "${required_keys[@]}"; do
  if grep -Fq "$key" "$TARGET_FILE"; then
    echo "[PASS] Found key: $key"
  else
    echo "[FAIL] Missing key: $key"
    missing=$((missing + 1))
  fi
done

if [[ "$missing" -gt 0 ]]; then
  echo "[ERROR] OpenClaw profile check failed: $missing missing key(s)."
  exit 1
fi

echo "[OK] OpenClaw profile check passed."
