#!/usr/bin/env bash
# token-pilot/scripts/uninstall.sh
# 从所有 Agent 的 AGENTS.md 移除 Token 优化核心规则块
# 幂等安全，可重复运行

set -euo pipefail

OPENCLAW_DIR="${OPENCLAW_DIR:-$HOME/.openclaw}"
AGENTS_DIR="$OPENCLAW_DIR/agents"
START_MARKER="<!-- TOKEN-PILOT:START -->"
END_MARKER="<!-- TOKEN-PILOT:END -->"

removed=0
skipped=0

echo "========================================"
echo "  token-pilot 卸载"
echo "========================================"
echo ""

for agent_dir in "$AGENTS_DIR"/*/; do
  [ -d "$agent_dir" ] || continue
  agent_name="$(basename "$agent_dir")"
  agents_md="$agent_dir/agent/AGENTS.md"

  if [ ! -f "$agents_md" ]; then
    continue
  fi

  if grep -qF "$START_MARKER" "$agents_md"; then
    tmp="$(mktemp)"
    awk -v start="$START_MARKER" -v end="$END_MARKER" '
      $0 == start { skip=1; next }
      skip && $0 == end { skip=0; next }
      !skip { print }
    ' "$agents_md" > "$tmp"
    # 去掉文件末尾多余空行
    sed -i -e :a -e '/^\n*$/{$d;N;ba}' "$tmp" 2>/dev/null || true
    mv "$tmp" "$agents_md"
    echo "[REMOVED]  $agent_name/AGENTS.md"
    ((removed++)) || true
  else
    echo "[SKIP]     $agent_name/AGENTS.md（未注入，跳过）"
    ((skipped++)) || true
  fi

done

# 移除初始化标记
flag_file="$(dirname "$0")/../.initialized"
if [ -f "$flag_file" ]; then
  rm "$flag_file"
  echo ""
  echo "[REMOVED]  .initialized 标记"
fi

echo ""
echo "========================================"
echo "  已清理: $removed  跳过: $skipped"
echo "========================================"
echo ""
echo "Token 优化规则注入已全部移除。如需重新注入，运行："
echo "  bash ~/.openclaw/skills/token-pilot/scripts/init.sh"
