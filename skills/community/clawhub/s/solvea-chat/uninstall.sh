#!/usr/bin/env bash
# Solvea Chat Skill - 卸载脚本

set -e

SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
OPENCLAW_DIR="$HOME/.openclaw"
OPENCLAW_JSON="$OPENCLAW_DIR/openclaw.json"

if [ ! -f "$OPENCLAW_JSON" ]; then
    echo "✖ 未找到 OpenClaw 配置文件：$OPENCLAW_JSON"
    exit 1
fi

# ── 1. 列出当前所有 bindings ──────────────────────────────────────────────────
echo ""
echo "→ 读取当前 bindings..."

BINDING_LIST=()
while IFS= read -r line; do
    BINDING_LIST+=("$line")
done < <(python3 - "$OPENCLAW_JSON" <<'PYEOF'
import json, sys
with open(sys.argv[1]) as f:
    cfg = json.load(f)
for b in cfg.get("bindings", []):
    print(f"{b.get('agentId','')}  ←→  {b.get('match',{}).get('channel','')}")
PYEOF
)

if [ ${#BINDING_LIST[@]} -eq 0 ]; then
    echo "没有找到任何 binding，无需卸载"
    exit 0
fi

echo ""
echo "当前 bindings："
for i in "${!BINDING_LIST[@]}"; do
    echo "  $((i+1))) ${BINDING_LIST[$i]}"
done
echo ""
echo -n "选择要移除的 binding 编号（直接回车取消）: "
read pick

if [ -z "$pick" ]; then
    echo "已取消"
    exit 0
fi

pick_idx=$((pick - 1))
if [ $pick_idx -lt 0 ] || [ $pick_idx -ge ${#BINDING_LIST[@]} ]; then
    echo "⚠ 无效编号"
    exit 1
fi

SELECTED="${BINDING_LIST[$pick_idx]}"
AGENT_ID=$(echo "$SELECTED" | awk '{print $1}')
CHANNEL=$(echo "$SELECTED" | awk '{print $3}')

# ── 2. 移除 binding ───────────────────────────────────────────────────────────
echo ""
python3 - "$OPENCLAW_JSON" "$AGENT_ID" "$CHANNEL" <<'PYEOF'
import json, sys
path, agent_id, channel = sys.argv[1], sys.argv[2], sys.argv[3]
with open(path) as f:
    cfg = json.load(f)
before = len(cfg.get("bindings", []))
cfg["bindings"] = [
    b for b in cfg.get("bindings", [])
    if not (b.get("agentId") == agent_id and b.get("match", {}).get("channel") == channel)
]
after = len(cfg["bindings"])
with open(path, "w") as f:
    json.dump(cfg, f, indent=2, ensure_ascii=False)
    f.write("\n")
print(f"✓ openclaw.json: 移除 binding {channel} → {agent_id}  ({before} → {after} 条)")
PYEOF

# ── 3. 是否移除 agent 条目 ────────────────────────────────────────────────────
echo ""
echo -n "同时从 openclaw.json 移除 agent \"$AGENT_ID\"？[y/N]: "
read remove_agent
case "$remove_agent" in
    [yY]|[yY][eE][sS])
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
        echo ""
        python3 - "$OPENCLAW_JSON" "$AGENT_ID" <<'PYEOF'
import json, sys
path, agent_id = sys.argv[1], sys.argv[2]
with open(path) as f:
    cfg = json.load(f)
lst = cfg.get("agents", {}).get("list", [])
before = len(lst)
cfg["agents"]["list"] = [a for a in lst if a["id"] != agent_id]
after = len(cfg["agents"]["list"])
with open(path, "w") as f:
    json.dump(cfg, f, indent=2, ensure_ascii=False)
    f.write("\n")
print(f"✓ openclaw.json: 移除 agent \"{agent_id}\"  ({before} → {after} 个)")
PYEOF
        ;;
    *)
        AGENT_WORKSPACE=""
        ;;
esac

# ── 4. 是否删除 workspace 目录 ────────────────────────────────────────────────
if [ -n "$AGENT_WORKSPACE" ] && [ -d "$AGENT_WORKSPACE" ]; then
    echo ""
    echo "⚠ workspace 目录：$AGENT_WORKSPACE"
    echo -n "  删除该目录？此操作不可恢复 [y/N]: "
    read remove_ws
    case "$remove_ws" in
        [yY]|[yY][eE][sS])
            rm -rf "$AGENT_WORKSPACE"
            echo "✓ 已删除目录：$AGENT_WORKSPACE"
            ;;
        *)
            echo "保留目录：$AGENT_WORKSPACE"
            ;;
    esac
fi

echo ""
echo "✓ 卸载完成，重启 OpenClaw 使变更生效。"
