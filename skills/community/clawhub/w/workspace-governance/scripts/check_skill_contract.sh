#!/usr/bin/env bash
# 功能：检查 SKILL.md 是否包含关键治理契约段落
# 参数：可选，目标文件路径（默认 ./SKILL.md）
# 用法：bash scripts/check_skill_contract.sh

set -euo pipefail

TARGET_FILE="${1:-./SKILL.md}"

if [[ ! -f "$TARGET_FILE" ]]; then
  echo "[ERROR] File not found: $TARGET_FILE"
  exit 2
fi

required_headers=(
  "## Required Capabilities and Preconditions"
  "### Adapt Loading Rules (Mandatory)"
  "## Execution Pattern (Generic)"
  "## Non-Interactive Safety Policy (Mandatory)"
  "### Rollback and Checkpoint Schema (Minimum)"
)

missing_count=0

echo "[INFO] Checking skill contract in: $TARGET_FILE"
for header in "${required_headers[@]}"; do
  if ! grep -Fq "$header" "$TARGET_FILE"; then
    echo "[FAIL] Missing required section: $header"
    missing_count=$((missing_count + 1))
  else
    echo "[PASS] Found section: $header"
  fi
done

if [[ "$missing_count" -gt 0 ]]; then
  echo "[ERROR] Contract check failed: $missing_count required section(s) missing."
  exit 1
fi

echo "[OK] Contract check passed."
