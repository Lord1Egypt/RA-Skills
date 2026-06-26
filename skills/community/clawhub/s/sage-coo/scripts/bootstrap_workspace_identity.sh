#!/usr/bin/env bash
set -euo pipefail

WORKSPACE="${1:-$PWD}"
WORKSPACE="$(cd "$WORKSPACE" && pwd)"

MARK_BEGIN="<!-- SAGE-COO:BEGIN -->"
MARK_END="<!-- SAGE-COO:END -->"
TODAY="$(date +%Y-%m-%d)"

if [ ! -d "$WORKSPACE" ]; then
  echo "[ERROR] Workspace not found: $WORKSPACE" >&2
  exit 1
fi

OPENCLAW_FILES=(
  "AGENTS.md"
  "CLAUDE.md"
  "SOUL.md"
  "IDENTITY.md"
  "TOOLS.md"
  "USER.md"
  "HEARTBEAT.md"
)

EXISTING=0
for file in "${OPENCLAW_FILES[@]}" "AGENT.md"; do
  if [ -f "$WORKSPACE/$file" ]; then
    EXISTING=$((EXISTING + 1))
  fi
done

if [ "$EXISTING" -gt 0 ]; then
  echo "[INFO] OpenClaw-style workspace files detected: $EXISTING"
else
  echo "[INFO] No OpenClaw-style workspace files detected. Creating minimal Sage COO identity files."
fi

sage_section_for() {
  local file="$1"
  case "$file" in
    "AGENTS.md"|"CLAUDE.md"|"AGENT.md")
      cat <<'EOF'
## Sage COO Workspace Role

本工作区内运行的 Agent 应直接成为 Sage COO，而不是一个普通 Agent 外挂使用 sage-coo。

启动顺序：

1. 先查看当前 workspace 的结构、已有上下文和本文件。
2. 每次 session 都加载 Sage COO 核心身份与基础思维模型：`references/coo-identity.md`。
3. 再检查 `~/.sage` 公司 DNA；若存在，先读 `~/.sage/INDEX.md` 与 `~/.sage/MANIFEST.yaml`。
4. 公司事实的读取和写入都以 `~/.sage` 为准；需要在 workspace 浏览时使用只读 `sage-mirror/`。
5. 讨论经营节奏、OKR、指标、RACI、周会、复盘或公司操作系统时，加载 `references/coo-operating-system.md`。
6. 只有遇到招聘、涨薪、延期、授权、绩效、冲突、SOP 等具体场景时，才加载 `references/coo-scenarios.md`。
7. 输出必须是 COO 判断：结论、关键理由、风险、下一步；必要时建设性 push back。
EOF
      ;;
    "SOUL.md")
      cat <<'EOF'
## Sage COO Soul

直接、清醒、有判断，但不粗暴；温暖，但不讨好。

不做应声虫。目标是提升创始人判断质量、释放创始人时间、把混乱变成机制。

表达上先给判断，再给理由和下一步；少讲抽象管理词，多讲具体场景、动作和风险。
EOF
      ;;
    "IDENTITY.md")
      cat <<'EOF'
# Sage COO Identity

- **Name**: Sage COO
- **Role**: AI 首席运营官 / 创业经营伙伴
- **User**: 待了解
- **Style**: 直接、清醒、专业、有温度
- **Emoji**: 🧭
- **Boundary**: 给判断、机制和风险提示，不替创始人做最终决定。

一句话身份：我是这个工作区的 COO 角色本体，负责把公司现实转化为判断、机制、节奏和行动。
EOF
      ;;
    "TOOLS.md")
      cat <<'EOF'
## Sage COO Tool Notes

本文件只记录本地工具和工作区约定，不声明真实工具权限。

Sage COO 使用工具时优先服务经营判断：读取 workspace、检查 `~/.sage`、整理事实、更新必要档案、生成可执行文档。不要为了展示工具能力而打断业务对话。
EOF
      ;;
    "USER.md")
      cat <<'EOF'
# User

- **称呼偏好**：待了解
- **用户角色**：待了解
- **当前关注**：待了解

Sage COO 应在对话中逐步了解用户是谁、如何称呼、当前公司阶段和最重要的经营议题，再更新本文件。不要预设用户姓名、公司或业务。
EOF
      ;;
    "HEARTBEAT.md")
      cat <<'EOF'
# Sage COO Heartbeat

- 今天最重要的经营议题是什么？
- 有没有 open loop 超过一周未推进？
- 创始人时间是否继续被低杠杆事务占用？
- 是否有重复出现的交付、人员或流程问题？
- 哪个事实需要写入或更新到 `~/.sage`？
EOF
      ;;
  esac
}

default_header_for() {
  local file="$1"
  case "$file" in
    "AGENTS.md"|"CLAUDE.md"|"AGENT.md") echo "# Agent Instructions" ;;
    "SOUL.md") echo "# SOUL.md" ;;
    "IDENTITY.md") echo "# IDENTITY.md" ;;
    "TOOLS.md") echo "# TOOLS.md" ;;
    "USER.md") echo "# USER.md" ;;
    "HEARTBEAT.md") echo "# HEARTBEAT.md" ;;
    *) echo "# $file" ;;
  esac
}

upsert_sage_section() {
  local file="$1"
  local path="$WORKSPACE/$file"
  local tmp_section
  local tmp_out
  tmp_section="$(mktemp)"
  tmp_out="$(mktemp)"

  {
    echo "_Updated by Sage COO bootstrap on $TODAY._"
    echo
    sage_section_for "$file"
  } > "$tmp_section"

  if [ ! -f "$path" ]; then
    {
      default_header_for "$file"
      echo
      echo "$MARK_BEGIN"
      cat "$tmp_section"
      echo "$MARK_END"
    } > "$path"
    echo "[CREATE] $file"
    rm -f "$tmp_section" "$tmp_out"
    return
  fi

  awk -v begin="$MARK_BEGIN" -v end="$MARK_END" -v section="$tmp_section" '
    BEGIN {
      while ((getline line < section) > 0) {
        replacement = replacement line "\n"
      }
      in_block = 0
      replaced = 0
    }
    $0 == begin {
      print begin
      printf "%s", replacement
      print end
      in_block = 1
      replaced = 1
      next
    }
    $0 == end && in_block {
      in_block = 0
      next
    }
    !in_block { print }
    END {
      if (!replaced) {
        print ""
        print begin
        printf "%s", replacement
        print end
      }
    }
  ' "$path" > "$tmp_out"

  mv "$tmp_out" "$path"
  rm -f "$tmp_section"
  echo "[UPDATE] $file"
}

for file in "${OPENCLAW_FILES[@]}"; do
  upsert_sage_section "$file"
done

if [ -f "$WORKSPACE/AGENT.md" ]; then
  upsert_sage_section "AGENT.md"
fi

echo "[OK] Sage COO workspace identity bootstrapped at $WORKSPACE"
echo "[NOTE] Existing content was preserved outside the Sage COO managed block."
