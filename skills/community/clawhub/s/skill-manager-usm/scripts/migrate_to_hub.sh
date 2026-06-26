#!/usr/bin/env bash
#
# migrate_to_hub.sh - 一次性迁移脚本
# 将现有分散在各 Agent 目录中的技能统一到 ~/.skills/ (Global Hub)
#
# 执行流程：
#   1. 将 ~/.claude/skills/ 中的真实目录移入 ~/.skills/
#   2. 在 ~/.claude/skills/ 中创建指向 ~/.skills/ 的符号链接
#   3. 合并 ~/.cursor/skills/（去重，同名保留 Claude 版本）
#   4. 删除 ~/.skills/ 中指向 Agent 目录的旧反向链接
#   5. 为每个技能生成默认 meta.yaml
#
# 用法：
#   bash migrate_to_hub.sh [--dry-run]
#

set -euo pipefail

SKILLS_HUB="$HOME/.skills"
DRY_RUN=false
BACKUP_DIR="$SKILLS_HUB/.migration-backup-$(date +%Y%m%d%H%M%S)"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info()  { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }
log_action(){ echo -e "${BLUE}[ACTION]${NC} $1"; }
log_dry()   { echo -e "${YELLOW}[DRY-RUN]${NC} $1"; }

# 解析参数
for arg in "$@"; do
    case $arg in
        --dry-run) DRY_RUN=true ;;
        *) log_error "Unknown argument: $arg"; exit 1 ;;
    esac
done

if $DRY_RUN; then
    log_warn "=== DRY RUN MODE — 不会做任何更改 ==="
    echo
fi

# 需要处理的 Agent 源目录（排除 codex .system）
AGENT_SKILL_DIRS=(
    "$HOME/.claude/skills"
    "$HOME/.cursor/skills"
    "$HOME/.openclaw/skills"
)

# 排除列表（不迁移的目录）
EXCLUDE_LIST=(".system")

is_excluded() {
    local name="$1"
    for exc in "${EXCLUDE_LIST[@]}"; do
        [[ "$name" == "$exc" ]] && return 0
    done
    return 1
}

# ============================================================
# 阶段 0：备份
# ============================================================
log_info "=== 阶段 0：创建备份 ==="

if ! $DRY_RUN; then
    mkdir -p "$BACKUP_DIR"
    # 备份当前 ~/.skills/ 的链接状态
    ls -la "$SKILLS_HUB" > "$BACKUP_DIR/skills_hub_before.txt" 2>/dev/null || true
    for dir in "${AGENT_SKILL_DIRS[@]}"; do
        if [[ -d "$dir" ]]; then
            agent_name=$(basename "$(dirname "$dir")")
            ls -la "$dir" > "$BACKUP_DIR/${agent_name}_skills_before.txt" 2>/dev/null || true
        fi
    done
    log_info "备份已保存到: $BACKUP_DIR"
else
    log_dry "将创建备份目录: $BACKUP_DIR"
fi

# ============================================================
# 阶段 1：清理 ~/.skills/ 中的旧反向链接
# ============================================================
log_info "=== 阶段 1：清理 ~/.skills/ 中指向 Agent 目录的旧反向链接 ==="

for item in "$SKILLS_HUB"/*/; do
    [[ ! -e "$item" ]] && continue
    name=$(basename "$item")
    
    if [[ -L "${SKILLS_HUB}/${name}" ]]; then
        target=$(readlink "${SKILLS_HUB}/${name}")
        # 检查是否指向 Agent 目录
        if [[ "$target" == *"/.claude/"* ]] || [[ "$target" == *"/.cursor/"* ]] || [[ "$target" == *"/.codex/"* ]]; then
            log_action "删除旧反向链接: ~/.skills/$name -> $target"
            if ! $DRY_RUN; then
                rm "${SKILLS_HUB}/${name}"
            fi
        fi
    fi
done

echo

# ============================================================
# 阶段 2：将 Agent 目录中的真实技能移入 Hub
# ============================================================
log_info "=== 阶段 2：将 Agent 目录中的真实技能移入 ~/.skills/ ==="

# 优先处理 Claude（作为主版本）
for agent_dir in "${AGENT_SKILL_DIRS[@]}"; do
    [[ ! -d "$agent_dir" ]] && continue
    agent_name=$(basename "$(dirname "$agent_dir")")
    log_info "处理 Agent: $agent_name ($agent_dir)"
    
    for skill_path in "$agent_dir"/*/; do
        [[ ! -e "$skill_path" ]] && continue
        skill_name=$(basename "$skill_path")
        
        # 跳过排除项
        if is_excluded "$skill_name"; then
            log_warn "跳过排除项: $skill_name"
            continue
        fi
        
        # 如果已经是链接（指向 hub），跳过
        if [[ -L "$agent_dir/$skill_name" ]]; then
            link_target=$(readlink "$agent_dir/$skill_name")
            if [[ "$link_target" == "$SKILLS_HUB/"* ]]; then
                log_info "  已是正确链接: $skill_name -> $link_target"
                continue
            fi
        fi
        
        hub_path="$SKILLS_HUB/$skill_name"
        
        # 如果 hub 中已存在真实目录，跳过（保留先到的版本）
        if [[ -d "$hub_path" ]] && [[ ! -L "$hub_path" ]]; then
            log_warn "  Hub 已存在 $skill_name (真实目录)，跳过移动"
            # 仍然需要把 Agent 目录的替换为链接
            if [[ ! -L "$agent_dir/$skill_name" ]]; then
                log_action "  删除 $agent_dir/$skill_name 并创建链接"
                if ! $DRY_RUN; then
                    rm -rf "$agent_dir/$skill_name"
                    ln -s "$hub_path" "$agent_dir/$skill_name"
                fi
            fi
            continue
        fi
        
        # 移动技能到 hub
        log_action "  移动: $agent_dir/$skill_name -> $hub_path"
        if ! $DRY_RUN; then
            mv "$agent_dir/$skill_name" "$hub_path"
        fi
        
        # 在原位创建链接
        log_action "  创建链接: $agent_dir/$skill_name -> $hub_path"
        if ! $DRY_RUN; then
            ln -s "$hub_path" "$agent_dir/$skill_name"
        fi
    done
    echo
done

# ============================================================
# 阶段 3：为每个技能生成 meta.yaml
# ============================================================
log_info "=== 阶段 3：生成 meta.yaml ==="

# 预定义 scope 映射
declare -A SCOPE_MAP
SCOPE_MAP[skill-creator]="universal"
SCOPE_MAP[message-bridge]="universal"
SCOPE_MAP[xinyuan]="claude_code"
SCOPE_MAP[xinyuan-auto-recall]="claude_code"
SCOPE_MAP[xinyuan-auto-update]="claude_code"
SCOPE_MAP[xinyuan-knowledge-organize]="claude_code"
SCOPE_MAP[agent-reach]="universal"
SCOPE_MAP[agent-browser]="openclaw"
SCOPE_MAP[agent-deep-research]="openclaw"
SCOPE_MAP[agent-team-orchestration]="openclaw"
SCOPE_MAP[alist-upload]="openclaw"
SCOPE_MAP[doubao-image-gen]="openclaw"
SCOPE_MAP[file-share]="openclaw"
SCOPE_MAP[memory-tiering]="openclaw"
SCOPE_MAP[skill-installer]="openclaw"
SCOPE_MAP[webfetch-md]="openclaw"

for skill_path in "$SKILLS_HUB"/*/; do
    [[ ! -d "$skill_path" ]] && continue
    [[ -L "${skill_path%/}" ]] && continue  # 跳过仍是链接的
    
    skill_name=$(basename "$skill_path")
    meta_file="$skill_path/meta.yaml"
    
    # 跳过已有 meta.yaml 的
    if [[ -f "$meta_file" ]]; then
        log_info "  已存在: $skill_name/meta.yaml"
        continue
    fi
    
    # 确定 scope
    scope="${SCOPE_MAP[$skill_name]:-universal}"
    
    # 生成 meta.yaml
    log_action "  生成: $skill_name/meta.yaml (scope: $scope)"
    if ! $DRY_RUN; then
        if [[ "$scope" == "universal" ]]; then
            cat > "$meta_file" << EOF
name: "$skill_name"
version: "1.0"
scope: "universal"
EOF
        else
            cat > "$meta_file" << EOF
name: "$skill_name"
version: "1.0"
scope:
  - $scope
EOF
        fi
    fi
done

echo

# ============================================================
# 阶段 4：汇总
# ============================================================
log_info "=== 迁移完成 ==="
echo
log_info "Hub 目录最终状态:"
ls -la "$SKILLS_HUB"/ 2>/dev/null | grep -v "^total"
echo
log_info "各 Agent 目录链接状态:"
for agent_dir in "${AGENT_SKILL_DIRS[@]}"; do
    [[ ! -d "$agent_dir" ]] && continue
    agent_name=$(basename "$(dirname "$agent_dir")")
    echo "  $agent_name:"
    ls -la "$agent_dir"/ 2>/dev/null | grep "^l" | sed 's/^/    /'
done

echo
if $DRY_RUN; then
    log_warn "以上为 DRY RUN 预览，未做任何实际更改"
    log_info "移除 --dry-run 参数以执行实际迁移"
else
    log_info "迁移已完成！运行 sync_skills.sh 以确保所有 Agent 链接正确"
fi
