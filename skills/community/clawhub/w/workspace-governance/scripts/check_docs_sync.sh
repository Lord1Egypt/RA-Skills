#!/usr/bin/env bash
# 功能：检查 SKILL.md 的关键章节是否在中英文 reference 手册中有对应说明
# 参数：无
# 用法：bash scripts/check_docs_sync.sh

set -euo pipefail

SKILL_FILE="./SKILL.md"
ZH_FILE="./references/治理手册.zh-CN.md"
EN_FILE="./references/Governance-Manual.md"

for f in "$SKILL_FILE" "$ZH_FILE" "$EN_FILE"; do
  if [[ ! -f "$f" ]]; then
    echo "[ERROR] Missing required file: $f"
    exit 2
  fi
done

skill_markers=(
  "## Required Capabilities and Preconditions"
  "### Adapt Loading Rules (Mandatory)"
  "## Non-Interactive Safety Policy (Mandatory)"
  "### Rollback and Checkpoint Schema (Minimum)"
  "## Skill Interoperability (Optional)"
)

zh_markers=(
  "## 定位"
  "## 真源规则"
  "## 常见运维动作"
)

en_markers=(
  "## Positioning"
  "## Source-of-Truth Policy"
  "## Common Ops Playbook"
)

missing=0

echo "[INFO] Checking SKILL.md mandatory markers..."
for marker in "${skill_markers[@]}"; do
  if grep -Fq "$marker" "$SKILL_FILE"; then
    echo "[PASS] SKILL marker found: $marker"
  else
    echo "[FAIL] SKILL marker missing: $marker"
    missing=$((missing + 1))
  fi
done

echo "[INFO] Checking Chinese reference markers..."
for marker in "${zh_markers[@]}"; do
  if grep -Fq "$marker" "$ZH_FILE"; then
    echo "[PASS] ZH marker found: $marker"
  else
    echo "[FAIL] ZH marker missing: $marker"
    missing=$((missing + 1))
  fi
done

echo "[INFO] Checking English reference markers..."
for marker in "${en_markers[@]}"; do
  if grep -Fq "$marker" "$EN_FILE"; then
    echo "[PASS] EN marker found: $marker"
  else
    echo "[FAIL] EN marker missing: $marker"
    missing=$((missing + 1))
  fi
done

if [[ "$missing" -gt 0 ]]; then
  echo "[ERROR] Docs sync check failed with $missing issue(s)."
  exit 1
fi

echo "[OK] Docs sync check passed."
