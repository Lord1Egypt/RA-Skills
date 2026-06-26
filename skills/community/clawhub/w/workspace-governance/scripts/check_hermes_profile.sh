#!/usr/bin/env bash
# 功能：检查 Hermes profile 是否包含关键安全字段与策略
# 参数：可选，目标文件路径（默认 ./tools/adapt-profiles/hermes.yaml）
# 用法：bash scripts/check_hermes_profile.sh

set -euo pipefail

TARGET_FILE="${1:-./tools/adapt-profiles/hermes.yaml}"

if [[ ! -f "$TARGET_FILE" ]]; then
  echo "[ERROR] File not found: $TARGET_FILE"
  exit 2
fi

required_keys=(
  "platform: hermes"
  "hermes_version:"
  "detection_signals:"
  "immutable_dirs:"
  "protected_files:"
  "non_interactive_policy:"
  "enforce_blocked_on_ask_user: true"
  "enforce_fail_fast_on_unconfirmed_destructive: true"
  "logs_policy:"
  "extensions_policy:"
  "merge_rules:"
  "skill_management:"
  "session_policy:"
  "cron_policy:"
)

missing=0
echo "[INFO] Checking Hermes profile contract in: $TARGET_FILE"
for key in "${required_keys[@]}"; do
  if grep -Fq "$key" "$TARGET_FILE"; then
    echo "[PASS] Found key: $key"
  else
    echo "[FAIL] Missing key: $key"
    missing=$((missing + 1))
  fi
done

if [[ "$missing" -gt 0 ]]; then
  echo "[ERROR] Hermes profile check failed: $missing missing key(s)."
  exit 1
fi

echo "[OK] Hermes profile check passed."
