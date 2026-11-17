#!/usr/bin/env bash
# 园林算量 · 发布前预检：自测 -> 发布合规扫描 -> 真图回归（复用 cad-file-reader 识图底座 regression）。
# 用法：scripts/run_preflight.sh [--manifest <真图清单.json>]
set -euo pipefail
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_BIN=""
for candidate in \
  "${CODEX_PYTHON:-}" \
  "$HOME"/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  "$HOME"/.cache/codex-runtimes/*/dependencies/python/bin/python3 \
  "$(command -v python3 || true)"
do
  if [[ -n "${candidate}" && -x "${candidate}" ]]; then
    PYTHON_BIN="${candidate}"
    break
  fi
done
[[ -z "${PYTHON_BIN}" ]] && { echo "❌ 找不到 python3（可设 CODEX_PYTHON）" >&2; exit 1; }

MANIFEST=""
if [[ "${1:-}" == "--manifest" ]]; then
  MANIFEST="${2:?--manifest 需要参数}"
  shift 2
fi

CAD_SKILL_DIR="${CAD_SKILL_DIR:-}"
if [[ -z "${CAD_SKILL_DIR}" ]]; then
  for d in "$SKILL_DIR/../cad-file-reader" "$HOME"/.workbuddy/skills/*/cad-file-reader "$HOME/.claude/skills/cad-file-reader" "$HOME/.codex/skills/cad-file-reader"; do
    [[ -d "$d" ]] && { CAD_SKILL_DIR="$d"; break; }
  done
fi
if [[ -n "${CAD_SKILL_DIR}" ]]; then
  export CAD_SKILL_DIR
  export PYTHONPATH="${SKILL_DIR}/scripts:${CAD_SKILL_DIR}/scripts:${CAD_SKILL_DIR}/vendor${PYTHONPATH:+:${PYTHONPATH}}"
fi

echo "=== 1/3 全量自测 ==="

echo "=== 2/3 发布合规扫描 ==="
CHECK_RELEASE="${HOME}/.codex/skills/skill-publisher/scripts/check_release.py"
if [[ -f "${CHECK_RELEASE}" ]]; then
  # 数据/算法词豁免表：rules/release-sensitive.allow；outputs/ 为本地内部报告，不随包上传。
  ALLOW_FILE="${SKILL_DIR}/rules/release-sensitive.allow"
  ALLOW_SENSITIVE=""
  if [[ -f "${ALLOW_FILE}" ]]; then
    ALLOW_SENSITIVE="$(tr '\n' ',' < "${ALLOW_FILE}" | sed 's/,$//')"
  fi
  "${PYTHON_BIN}" "${CHECK_RELEASE}" --path "${SKILL_DIR}" --exclude-dirs outputs --allow-sensitive "${ALLOW_SENSITIVE}"
else
  echo "⚠️ 未找到 skill-publisher/check_release.py，跳过发布合规扫描（发布前需补跑）"
fi

echo "=== 3/3 真图回归（识图底座层） ==="
if [[ -z "${MANIFEST}" ]]; then
  echo "⚠️ 未提供 --manifest，跳过真实图纸回归；发布前必须带真图清单跑一次。"
elif [[ -z "${CAD_SKILL_DIR}" || ! -x "${CAD_SKILL_DIR}/scripts/run_real_dwg_regression.sh" ]]; then
  echo "❌ 缺少识图底座 cad-file-reader，无法执行真图回归（设 CAD_SKILL_DIR）" >&2
  exit 2
else
  "${CAD_SKILL_DIR}/scripts/run_real_dwg_regression.sh" --manifest "${MANIFEST}"
  echo "✅ 真图回归通过"
fi
echo "✅ 园林算量发布预检完成"
