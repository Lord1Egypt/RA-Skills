#!/usr/bin/env bash
# token-pilot/scripts/init.sh
# 将 Token 优化核心规则注入所有 Agent 的 AGENTS.md（33行，极简无干扰）
# 默认先预览再征得用户同意，--yes 跳过确认（供自动化/CI 使用）

set -euo pipefail

OPENCLAW_DIR="${OPENCLAW_DIR:-$HOME/.openclaw}"
AGENTS_DIR="$OPENCLAW_DIR/agents"
CORE_FILE="$(dirname "$(dirname "$0")")/references/TOKEN-PILOT-CORE.md"
START_MARKER="<!-- TOKEN-PILOT:START -->"
END_MARKER="<!-- TOKEN-PILOT:END -->"

# Bootstrap size limits (from openclaw.json agents.defaults)
# Default: bootstrapMaxChars=6000, safe threshold = 80% = 4800 chars
BOOTSTRAP_MAX_CHARS=6000
SAFE_THRESHOLD=4800

YES=0
for arg in "$@"; do
  case "$arg" in --yes|-y) YES=1 ;; esac
done

if [ ! -f "$CORE_FILE" ]; then
  echo "ERROR: 找不到核心规则文件 $CORE_FILE"
  exit 1
fi

CORE_CONTENT="$(cat "$CORE_FILE")"
INJECT_LINES="$(wc -l < "$CORE_FILE" | tr -d ' ')"

# ── Phase 1: 扫描预览 ─────────────────────────────────────────────────────────
echo ""
echo "========================================"
echo "  token-pilot · 注入预览"
echo "========================================"
echo "  注入内容：TOKEN-PILOT-CORE.md（${INJECT_LINES} 行，7条规则）→ AGENTS.md 末尾"
echo ""

total=0; new_count=0; update_count=0; overlap_count=0

for agent_dir in "$AGENTS_DIR"/*/; do
  [ -d "$agent_dir" ] || continue
  agent_name="$(basename "$agent_dir")"
  agents_md="$agent_dir/agent/AGENTS.md"

  if [ ! -f "$agents_md" ]; then
    echo "  [新建]   $agent_name — AGENTS.md 不存在，将创建并注入"
    ((new_count++)) || true
  elif grep -qF "$START_MARKER" "$agents_md"; then
    lines="$(wc -l < "$agents_md" | tr -d ' ')"
    chars="$(wc -c < "$agents_md" | tr -d ' ')"
    size_flag=""
    if [ "$chars" -gt "$BOOTSTRAP_MAX_CHARS" ]; then
      size_flag=" 🔴 超${BOOTSTRAP_MAX_CHARS}字符，会被截断！"
    elif [ "$chars" -gt "$SAFE_THRESHOLD" ]; then
      size_flag=" ⚠️  接近上限(${chars}/${BOOTSTRAP_MAX_CHARS}字符)"
    fi
    echo "  [更新]   $agent_name — ${lines}行/${chars}字符${size_flag}，规则块已存在，将替换为最新版"
    ((update_count++)) || true
  else
    lines="$(wc -l < "$agents_md" | tr -d ' ')"
    chars="$(wc -c < "$agents_md" | tr -d ' ')"
    size_flag=""
    after_chars=$((chars + $(wc -c < "$CORE_FILE" | tr -d ' ') + 20))
    if [ "$after_chars" -gt "$BOOTSTRAP_MAX_CHARS" ]; then
      size_flag=" 🔴 注入后${after_chars}字符，超上限会被截断！"
    elif [ "$after_chars" -gt "$SAFE_THRESHOLD" ]; then
      size_flag=" ⚠️  注入后${after_chars}字符，接近上限"
    fi
    # 检测是否已有类似 token 优化规则
    if grep -qE "先读.{0,10}行|limit=30|不重复读|合并.{0,6}工具|edit.*write|prompt.?cache|动态内容|长上下文|compact" "$agents_md" 2>/dev/null; then
      echo "  [注入⚠]  $agent_name — ${lines}行/${chars}字符${size_flag}，检测到已有类似优化规则，注入后请核查重叠"
      ((overlap_count++)) || true
    else
      echo "  [注入]   $agent_name — ${lines}行/${chars}字符${size_flag}，将在末尾增加 ${INJECT_LINES} 行"
    fi
    ((new_count++)) || true
  fi
  ((total++)) || true
done

echo ""
echo "  合计 $total 只 Agent（新注入 $new_count，更新规则块 $update_count，含潜在重叠 $overlap_count）"
echo ""

if [ "$overlap_count" -gt 0 ]; then
  echo "  ⚠️  标注 [注入⚠] 的 Agent 已有类似规则，建议注入后手动检查 AGENTS.md 去重。"
  echo ""
fi

# ── Phase 2: 用户确认 ─────────────────────────────────────────────────────────
if [ "$YES" -eq 0 ]; then
  read -r -p "确认注入？[y/N] " reply
  case "$reply" in
    [Yy]*) ;;
    *) echo "已取消。如需跳过确认，使用 --yes 参数。"; exit 0 ;;
  esac
  echo ""
fi

# ── Phase 3: 执行注入 ─────────────────────────────────────────────────────────
injected=0; updated=0; skipped=0

inject_or_update() {
  local target="$1"
  local tmp
  tmp="$(mktemp)"

  if grep -qF "$START_MARKER" "$target"; then
    awk -v start="$START_MARKER" -v end="$END_MARKER" -v rules_file="$CORE_FILE" '
      BEGIN { while ((getline line < rules_file) > 0) rules = rules line "\n" }
      index($0, start) { printing=1; printf "%s", rules; next }
      index($0, end)   { printing=0; next }
      !printing        { print }
    ' "$target" > "$tmp"
    mv "$tmp" "$target"
    return 1
  else
    { cat "$target"; echo ""; echo "---"; echo ""; echo "$CORE_CONTENT"; } > "$tmp"
    mv "$tmp" "$target"
    return 0
  fi
}

for agent_dir in "$AGENTS_DIR"/*/; do
  agent_name="$(basename "$agent_dir")"
  agents_md="$agent_dir/agent/AGENTS.md"

  mkdir -p "$agent_dir/agent"

  if [ ! -f "$agents_md" ]; then
    echo "$CORE_CONTENT" > "$agents_md"
    echo "[NEW]     $agent_name/AGENTS.md"
    ((injected++)) || true
  else
    if inject_or_update "$agents_md"; then
      echo "[INJECT]  $agent_name/AGENTS.md"
      ((injected++)) || true
    else
      echo "[UPDATE]  $agent_name/AGENTS.md"
      ((updated++)) || true
    fi
  fi
done

echo ""
echo "========================================"
echo "  首次注入: $injected  规则更新: $updated  已跳过: $skipped"
echo "========================================"
echo ""
echo "核心规则已注入 $(( injected + updated )) 只 Agent（${INJECT_LINES} 行，每次会话自动生效）"
echo "完整规则按需加载：~/.openclaw/skills/token-pilot/SKILL.md"

touch "$(dirname "$(dirname "$0")")/.initialized"
