#!/usr/bin/env bash
# 功能：检查 SKILL_ADAPT.yaml 是否包含关键策略字段
# 参数：可选，目标文件路径（默认 ./SKILL_ADAPT.yaml）
# 用法：bash scripts/check_adapt_contract.sh

set -euo pipefail

TARGET_FILE="${1:-./SKILL_ADAPT.yaml}"

if [[ ! -f "$TARGET_FILE" ]]; then
  echo "[ERROR] File not found: $TARGET_FILE"
  exit 2
fi

required_keys=(
  "required_capabilities:"
  "workspace_root:"
  "immutable_dirs:"
  "protected_files:"
  "destructive_guard:"
  "execution:"
  "logging:"
)

missing=0
echo "[INFO] Checking adapt contract in: $TARGET_FILE"
for key in "${required_keys[@]}"; do
  if grep -Fq "$key" "$TARGET_FILE"; then
    echo "[PASS] Found key: $key"
  else
    echo "[FAIL] Missing key: $key"
    missing=$((missing + 1))
  fi
done

if [[ "$missing" -gt 0 ]]; then
  echo "[ERROR] Adapt contract check failed: $missing missing key(s)."
  exit 1
fi

echo "[OK] Adapt contract check passed."
