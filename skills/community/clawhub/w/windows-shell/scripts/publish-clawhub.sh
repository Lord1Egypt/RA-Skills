#!/usr/bin/env bash
# Publish this skill to ClawHub.
#   1) clawhub login         (browser GitHub auth, account must be >= 1 week old)
#   2) bash scripts/publish-clawhub.sh
#
# Note: clawhub's publish resolves "." unreliably and reports "SKILL.md required",
# so we pass an absolute Windows-style path (cygpath/pwd -W).
set -euo pipefail

cd "$(dirname "$0")/.."

# Absolute Windows path that node (clawhub) resolves correctly under Git Bash.
SKILL_DIR="$(cygpath -w "$PWD" 2>/dev/null || pwd -W 2>/dev/null || pwd)"

VERSION="$(grep -m1 '^version:' SKILL.md | sed 's/version:[[:space:]]*//')"

echo "Publishing windows-shell@${VERSION} from ${SKILL_DIR}"

clawhub skill publish "${SKILL_DIR}" \
  --slug windows-shell \
  --name "windows-shell" \
  --version "${VERSION}" \
  --changelog "v${VERSION} —— 专治 Windows(GBK/936) 下 LLM 执行命令的编码错误：中文乱码、命令报错、反复重试。修复：setup-env 改用 Windows 用户级环境变量、Python 用 -X utf8、补充 pwsh 说明与环境自检、新增 11 项 CLI 测试。" \
  --clawscan-note "仅含 SKILL.md 文档，无可执行逻辑。" \
  --tags latest --no-input
