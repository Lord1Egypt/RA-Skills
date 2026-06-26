#!/usr/bin/env bash
# Solvea Chat Skill - 一键安装脚本

set -e

# ── 参数解析 ──────────────────────────────────────────────────────────────────
DRY_RUN=false
for arg in "$@"; do
    case "$arg" in
        --dry-run) DRY_RUN=true ;;
    esac
done
[ "$DRY_RUN" = true ] && echo "[dry-run 模式：只模拟流程，不写入任何文件]"

SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
OPENCLAW_DIR="$HOME/.openclaw"
OPENCLAW_JSON="$OPENCLAW_DIR/openclaw.json"
TEMPLATES_DIR="$SKILL_DIR/templates"

# ── 辅助：渲染模板 ────────────────────────────────────────────────────────────
render_template() {
    local src="$1" dst="$2"
    if [ "$DRY_RUN" = true ]; then
        echo "  [dry-run] 写入 $dst"
    else
        sed \
            -e "s|{{AGENT_NAME}}|$AGENT_NAME|g" \
            -e "s|{{CHANNEL}}|$SELECTED_CHANNEL|g" \
            -e "s|{{BUSINESS_DESC}}|$BUSINESS_DESC|g" \
            -e "s|{{SKILL_DIR}}|$TARGET_SKILL_DIR|g" \
            "$src" > "$dst"
        echo "  ✓ 写入 $dst"
    fi
}

# ── 前置校验 ──────────────────────────────────────────────────────────────────
if [ ! -f "$OPENCLAW_JSON" ]; then
    echo ""
    echo "✖ 错误：未找到 OpenClaw 配置文件"
    echo ""
    echo "  请确认 OpenClaw 已正确安装，配置文件应位于：$OPENCLAW_JSON"
    echo ""
    exit 1
fi

# ── 1. 读取 OpenClaw 配置 ─────────────────────────────────────────────────────
echo ""
echo "→ 读取 OpenClaw 配置..."

CHANNEL_LIST=()
while IFS= read -r line; do
    CHANNEL_LIST+=("$line")
done < <(python3 - "$OPENCLAW_JSON" <<'PYEOF'
import json, sys
with open(sys.argv[1]) as f:
    cfg = json.load(f)
for k, v in cfg.get("channels", {}).items():
    if v.get("enabled", False):
        print(k)
PYEOF
)

AGENT_LIST=()
while IFS= read -r line; do
    AGENT_LIST+=("$line")
done < <(python3 - "$OPENCLAW_JSON" <<'PYEOF'
import json, sys
with open(sys.argv[1]) as f:
    cfg = json.load(f)
for a in cfg.get("agents", {}).get("list", []):
    print(a["id"])
PYEOF
)

if [ ${#CHANNEL_LIST[@]} -eq 0 ]; then
    echo "⚠ 没有已启用的渠道，请先在 OpenClaw 中接入渠道"
    exit 1
fi

# ── 2. 选择渠道 ───────────────────────────────────────────────────────────────
while true; do
    echo ""
    echo "已启用的渠道："
    for i in "${!CHANNEL_LIST[@]}"; do
        echo "  $((i+1))) ${CHANNEL_LIST[$i]}"
    done
    echo ""
    echo -n "选择要接入 Solvea 客服的渠道编号（直接回车跳过）: "
    read ch_pick

    if [ -z "$ch_pick" ]; then
        echo "跳过渠道绑定"
        echo ""
        echo "✓ 安装完成"
        exit 0
    fi

    ch_idx=$((ch_pick - 1))
    if [ $ch_idx -lt 0 ] || [ $ch_idx -ge ${#CHANNEL_LIST[@]} ]; then
        echo "⚠ 无效编号，请重新选择"
        continue
    fi
    SELECTED_CHANNEL="${CHANNEL_LIST[$ch_idx]}"

    # 检查渠道冲突
    EXISTING_BINDING=$(python3 - "$OPENCLAW_JSON" "$SELECTED_CHANNEL" <<'PYEOF'
import json, sys
with open(sys.argv[1]) as f:
    cfg = json.load(f)
channel = sys.argv[2]
for b in cfg.get("bindings", []):
    if b.get("match", {}).get("channel") == channel:
        print(b.get("agentId", ""))
        break
PYEOF
)

    if [ -n "$EXISTING_BINDING" ]; then
        echo ""
        echo "⚠ 渠道 $SELECTED_CHANNEL 已绑定到 agent: $EXISTING_BINDING"
        echo -n "  是否覆盖？原有绑定将被移除 [y/N]: "
        read confirm
        case "$confirm" in
            [yY]|[yY][eE][sS]) break ;;
            *) echo "请重新选择渠道" ;;
        esac
    else
        break
    fi
done

# ── 3. 选择或新建 agent ───────────────────────────────────────────────────────
echo ""
echo "选择 Agent："
for i in "${!AGENT_LIST[@]}"; do
    echo "  $((i+1))) ${AGENT_LIST[$i]}"
done
NEW_IDX=$((${#AGENT_LIST[@]} + 1))
echo "  $NEW_IDX) 新建 Agent（推荐）"
echo ""
echo -n "请选择编号 [默认 $NEW_IDX]: "
read agent_pick
agent_pick="${agent_pick:-$NEW_IDX}"

CREATE_NEW=false
if [ "$agent_pick" = "$NEW_IDX" ]; then
    CREATE_NEW=true
    echo ""
    echo -n "  Agent ID（英文，如 solvea）: "
    read AGENT_ID
    AGENT_ID="${AGENT_ID:-solvea}"
    AGENT_NAME="$AGENT_ID"
    DEFAULT_WORKSPACE="$OPENCLAW_DIR/workspaces/$AGENT_ID"
    echo -n "  Workspace 路径 [默认 $DEFAULT_WORKSPACE]: "
    read custom_workspace
    AGENT_WORKSPACE="${custom_workspace:-$DEFAULT_WORKSPACE}"
else
    agent_idx=$((agent_pick - 1))
    if [ $agent_idx -lt 0 ] || [ $agent_idx -ge ${#AGENT_LIST[@]} ]; then
        echo "⚠ 无效编号"
        exit 1
    fi
    AGENT_ID="${AGENT_LIST[$agent_idx]}"
    AGENT_NAME="$AGENT_ID"
    BUSINESS_DESC=""
    AGENT_WORKSPACE=$(python3 - "$OPENCLAW_JSON" "$AGENT_ID" <<'PYEOF'
import json, sys
with open(sys.argv[1]) as f:
    cfg = json.load(f)
for a in cfg.get("agents", {}).get("list", []):
    if a["id"] == sys.argv[2]:
        print(a.get("workspace", ""))
        break
PYEOF
)
fi

# ── 4. 写入 workspace 配置文件 ───────────────────────────────────────────────
echo ""
echo "→ 写入 workspace 配置: $AGENT_WORKSPACE"
if [ "$DRY_RUN" = false ]; then
    mkdir -p "$AGENT_WORKSPACE/memory"
fi
render_template "$TEMPLATES_DIR/IDENTITY.md"  "$AGENT_WORKSPACE/IDENTITY.md"
render_template "$TEMPLATES_DIR/AGENTS.md"   "$AGENT_WORKSPACE/AGENTS.md"
render_template "$TEMPLATES_DIR/SOUL.md"     "$AGENT_WORKSPACE/SOUL.md"
render_template "$TEMPLATES_DIR/USER.md"     "$AGENT_WORKSPACE/USER.md"
render_template "$TEMPLATES_DIR/TOOLS.md"    "$AGENT_WORKSPACE/TOOLS.md"
render_template "$TEMPLATES_DIR/HEARTBEAT.md" "$AGENT_WORKSPACE/HEARTBEAT.md"
render_template "$TEMPLATES_DIR/BOOTSTRAP.md" "$AGENT_WORKSPACE/BOOTSTRAP.md"
echo "✓ workspace 配置完成"

# ── 5. 将 skill 复制到 agent workspace ───────────────────────────────────────
TARGET_SKILL_DIR="$AGENT_WORKSPACE/skills/solvea-chat"

if [ "$DRY_RUN" = true ]; then
    echo ""
    echo "  [dry-run] cp -r $SKILL_DIR $TARGET_SKILL_DIR"
elif [ -d "$TARGET_SKILL_DIR" ]; then
    echo ""
    echo "⚠ skill 已存在: $TARGET_SKILL_DIR"
    echo -n "  是否覆盖？[y/N]: "
    read overwrite_skill
    case "$overwrite_skill" in
        [yY]|[yY][eE][sS])
            rm -rf "$TARGET_SKILL_DIR"
            ;;
        *)
            echo "跳过 skill 安装"
            ;;
    esac
fi
if [ "$DRY_RUN" = false ] && [ ! -d "$TARGET_SKILL_DIR" ]; then
    echo ""
    echo "→ 安装 skill 到 workspace..."
    mkdir -p "$AGENT_WORKSPACE/skills"
    cp -r "$SKILL_DIR" "$TARGET_SKILL_DIR"
    rm -rf "$TARGET_SKILL_DIR/.venv" "$TARGET_SKILL_DIR/.env"
    echo "✓ skill 已复制到 $TARGET_SKILL_DIR"
fi

# ── 6. 初始化 Python 环境 ─────────────────────────────────────────────────────
echo ""
if [ "$DRY_RUN" = true ]; then
    echo "  [dry-run] python3 -m venv $TARGET_SKILL_DIR/.venv"
    echo "  [dry-run] pip install -r $TARGET_SKILL_DIR/scripts/requirements.txt"
elif [ -d "$TARGET_SKILL_DIR/.venv" ]; then
    echo "✓ Python 虚拟环境已存在，跳过"
else
    echo "→ 创建 Python 虚拟环境..."
    python3 -m venv "$TARGET_SKILL_DIR/.venv"
    echo "→ 安装依赖..."
    "$TARGET_SKILL_DIR/.venv/bin/pip" install -q -r "$TARGET_SKILL_DIR/scripts/requirements.txt"
fi

# ── 7. Solvea API 配置 ────────────────────────────────────────────────────────
echo ""
if [ "$DRY_RUN" = true ]; then
    echo "请填写 Solvea API 配置（dry-run，不会写入）："
    echo ""
    echo -n "  SOLVEA_API_KEY  (X-Token): "
    read api_key
    echo -n "  SOLVEA_AGENT_ID (Agent ID): "
    read solvea_agent_id
    echo "  [dry-run] 写入 $TARGET_SKILL_DIR/.env"
else
    if [ -f "$TARGET_SKILL_DIR/.env" ]; then
        echo "已有 .env 配置，当前内容："
        echo ""
        cat "$TARGET_SKILL_DIR/.env" | sed 's/^/  /'
        echo ""
        echo -n "  是否重新填写？[y/N]: "
        read overwrite_env
        case "$overwrite_env" in
            [yY]|[yY][eE][sS]) ;;
            *)
                echo "保留现有 .env"
                # 读取现有值供 PENDING 检测使用
                api_key=$(grep "^SOLVEA_API_KEY=" "$TARGET_SKILL_DIR/.env" | cut -d= -f2)
                solvea_agent_id=$(grep "^SOLVEA_AGENT_ID=" "$TARGET_SKILL_DIR/.env" | cut -d= -f2)
                ;;
        esac
    fi
    case "${overwrite_env:-n}" in [yY]*) _do_write=true ;; *) _do_write=false ;; esac
    if [ ! -f "$TARGET_SKILL_DIR/.env" ] || [ "$_do_write" = true ]; then
        echo "请填写 Solvea API 配置（直接回车可跳过，稍后手动补全）："
        echo ""
        echo -n "  SOLVEA_API_KEY  (X-Token): "
        read api_key
        echo -n "  SOLVEA_AGENT_ID (Agent ID): "
        read solvea_agent_id

        cat > "$TARGET_SKILL_DIR/.env" <<EOF
SOLVEA_API_KEY=${api_key}
SOLVEA_AGENT_ID=${solvea_agent_id}
# 可选：自定义 API 地址，留空使用默认值 https://apps.voc.ai
SOLVEA_BASE_URL=https://apps.voc.ai
EOF
        echo "✓ 写入 $TARGET_SKILL_DIR/.env"
    fi
fi

# 收集未完成项
PENDING=()
[ -z "$api_key" ]         && PENDING+=("SOLVEA_API_KEY   → 在 Solvea 控制台获取 X-Token")
[ -z "$solvea_agent_id" ] && PENDING+=("SOLVEA_AGENT_ID  → 在 Solvea 控制台获取 Agent ID")

# ── 辅助：输出待办框 ──────────────────────────────────────────────────────────
print_pending() {
    if [ ${#PENDING[@]} -gt 0 ]; then
        echo ""
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "  待完成（请手动补全后重启 OpenClaw）："
        echo ""
        for item in "${PENDING[@]}"; do
            echo "  • $item"
        done
        echo ""
        echo "  配置文件：$TARGET_SKILL_DIR/.env"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    fi
}

# ── 8. 写入 openclaw.json ─────────────────────────────────────────────────────
if [ "$DRY_RUN" = true ]; then
    echo ""
    echo "  [dry-run] 写入 openclaw.json："
    echo "    agent:   $AGENT_ID  →  $AGENT_WORKSPACE"
    echo "    binding: $SELECTED_CHANNEL → $AGENT_ID"
    print_pending
    echo ""
    echo "✓ dry-run 完成，未写入任何文件"
    exit 0
fi

python3 - <<PYEOF
import json

with open("$OPENCLAW_JSON") as f:
    cfg = json.load(f)

agent_id        = "$AGENT_ID"
agent_workspace = "$AGENT_WORKSPACE"
channel         = "$SELECTED_CHANNEL"

# agent
existing_ids = [a["id"] for a in cfg.get("agents", {}).get("list", [])]
if agent_id not in existing_ids:
    cfg.setdefault("agents", {}).setdefault("list", []).append({
        "id": agent_id,
        "name": agent_id,
        "workspace": agent_workspace,
        "agentDir": "$OPENCLAW_DIR/agents/" + agent_id + "/agent",
        "model": cfg.get("agents", {}).get("defaults", {}).get("model", {}).get("primary", "openai/gpt-5.2")
    })
    print(f"✓ 已添加 agent: {agent_id}")
else:
    print(f"✓ agent {agent_id} 已存在，跳过")

# binding
new_bindings = [b for b in cfg.get("bindings", []) if b.get("match", {}).get("channel") != channel]
already_correct = any(
    b.get("agentId") == agent_id and b.get("match", {}).get("channel") == channel
    for b in cfg.get("bindings", [])
)
if already_correct:
    print(f"✓ 渠道 {channel} 已绑定到 {agent_id}，无需变更")
else:
    new_bindings.append({"agentId": agent_id, "match": {"channel": channel}})
    cfg["bindings"] = new_bindings
    print(f"✓ 已绑定渠道: {channel} → {agent_id}")

with open("$OPENCLAW_JSON", "w") as f:
    json.dump(cfg, f, indent=2, ensure_ascii=False)
    f.write("\n")
print(f"✓ 写入 $OPENCLAW_JSON")
PYEOF

echo ""
echo "✓ 安装完成"
print_pending
echo ""
echo "重启 OpenClaw 使渠道绑定生效: openclaw gateway restart"
