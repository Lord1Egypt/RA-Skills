#!/usr/bin/env bash
#
# sync_skills.sh - 技能同步脚本
# 根据 meta.yaml 中的 scope 配置，自动维护各 Agent 目录下的符号链接
#
# 用法：
#   bash sync_skills.sh [options]
#
# 选项：
#   --dry-run          预览模式，不做实际更改
#   --project-dir DIR  同时同步项目级技能（指定项目根目录）
#   --verbose          详细输出
#   --clean-only       仅清理无效链接，不创建新链接
#

set -euo pipefail

SKILLS_HUB="$HOME/.skills"
AGENTS_YAML="$SKILLS_HUB/agents.yaml"
DRY_RUN=false
VERBOSE=false
CLEAN_ONLY=false
PROJECT_DIR=""

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

log_info()    { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn()    { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error()   { echo -e "${RED}[ERROR]${NC} $1"; }
log_action()  { echo -e "${BLUE}[SYNC]${NC} $1"; }
log_verbose() { $VERBOSE && echo -e "${CYAN}[VERBOSE]${NC} $1" || true; }

# 统计
CREATED=0
REMOVED=0
UNCHANGED=0
ERRORS=0

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --dry-run) DRY_RUN=true; shift ;;
        --verbose) VERBOSE=true; shift ;;
        --clean-only) CLEAN_ONLY=true; shift ;;
        --project-dir) PROJECT_DIR="$2"; shift 2 ;;
        *) log_error "未知参数: $1"; exit 1 ;;
    esac
done

if $DRY_RUN; then
    log_warn "=== DRY RUN MODE ==="
fi

# ============================================================
# 解析 agents.yaml（轻量级 YAML 解析）
# ============================================================
declare -A AGENT_GLOBAL_DIRS
declare -A AGENT_PROJECT_DIRS
AGENT_NAMES=()

parse_agents_yaml() {
    if [[ ! -f "$AGENTS_YAML" ]]; then
        log_error "agents.yaml 不存在: $AGENTS_YAML"
        exit 1
    fi
    
    local current_agent=""
    while IFS= read -r line; do
        # 跳过注释和空行
        [[ "$line" =~ ^[[:space:]]*# ]] && continue
        [[ -z "${line// /}" ]] && continue
        
        # 检测 agent 名称（顶层缩进 2 空格的键）
        if [[ "$line" =~ ^[[:space:]]{2}([a-zA-Z_][a-zA-Z0-9_]*): ]]; then
            potential_agent="${BASH_REMATCH[1]}"
            # 排除 global_skills_dir 和 project_skills_dir
            if [[ "$potential_agent" != "global_skills_dir" ]] && [[ "$potential_agent" != "project_skills_dir" ]]; then
                current_agent="$potential_agent"
                AGENT_NAMES+=("$current_agent")
            fi
        fi
        
        # 读取 global_skills_dir
        if [[ -n "$current_agent" ]] && [[ "$line" =~ global_skills_dir:[[:space:]]*\"?([^\"]+)\"? ]]; then
            local dir="${BASH_REMATCH[1]}"
            dir="${dir/#\~/$HOME}"  # 展开 ~
            AGENT_GLOBAL_DIRS[$current_agent]="$dir"
        fi
        
        # 读取 project_skills_dir
        if [[ -n "$current_agent" ]] && [[ "$line" =~ project_skills_dir:[[:space:]]*\"?([^\"]+)\"? ]]; then
            AGENT_PROJECT_DIRS[$current_agent]="${BASH_REMATCH[1]}"
        fi
    done < "$AGENTS_YAML"
    
    log_info "已加载 ${#AGENT_NAMES[@]} 个 Agent: ${AGENT_NAMES[*]}"
}

# ============================================================
# 解析 meta.yaml 的 scope 字段
# ============================================================
parse_scope() {
    local meta_file="$1"
    
    if [[ ! -f "$meta_file" ]]; then
        # 无 meta.yaml 默认 universal
        echo "universal"
        return
    fi
    
    local scope_line=""
    local in_scope_list=false
    local scopes=()
    
    while IFS= read -r line; do
        [[ "$line" =~ ^[[:space:]]*# ]] && continue
        
        # scope: "universal" 或 scope: universal
        if [[ "$line" =~ ^scope:[[:space:]]*\"?([a-zA-Z_]+)\"?[[:space:]]*$ ]]; then
            echo "${BASH_REMATCH[1]}"
            return
        fi
        
        # scope: (列表形式开始)
        if [[ "$line" =~ ^scope:[[:space:]]*$ ]]; then
            in_scope_list=true
            continue
        fi
        
        # 列表项: - agent_name
        if $in_scope_list; then
            if [[ "$line" =~ ^[[:space:]]*-[[:space:]]*([a-zA-Z_][a-zA-Z0-9_]*) ]]; then
                scopes+=("${BASH_REMATCH[1]}")
            else
                # 列表结束
                break
            fi
        fi
    done < "$meta_file"
    
    if [[ ${#scopes[@]} -gt 0 ]]; then
        echo "${scopes[*]}"
    else
        echo "universal"
    fi
}

# ============================================================
# 检查 Agent 是否在 scope 内
# ============================================================
agent_in_scope() {
    local agent="$1"
    local scope="$2"
    
    if [[ "$scope" == "universal" ]]; then
        return 0
    fi
    
    for s in $scope; do
        [[ "$s" == "$agent" ]] && return 0
    done
    
    return 1
}

# ============================================================
# 同步单个技能 Hub
# ============================================================
sync_hub() {
    local hub_dir="$1"
    local level="$2"  # "global" 或 "project"
    
    log_info "同步 $level 层: $hub_dir"
    
    if [[ ! -d "$hub_dir" ]]; then
        log_warn "Hub 目录不存在: $hub_dir"
        return
    fi
    
    # 遍历 hub 中的每个技能
    for skill_path in "$hub_dir"/*/; do
        [[ ! -d "$skill_path" ]] && continue
        
        local skill_name
        skill_name=$(basename "$skill_path")
        
        # 跳过以 . 开头的隐藏目录
        [[ "$skill_name" == .* ]] && continue
        
        # 跳过自身是链接的（不应该出现，但安全起见）
        [[ -L "${skill_path%/}" ]] && continue
        
        local meta_file="$skill_path/meta.yaml"
        local scope
        scope=$(parse_scope "$meta_file")
        
        log_verbose "技能 $skill_name: scope=[$scope]"
        
        # 对每个已注册 Agent 处理
        for agent in "${AGENT_NAMES[@]}"; do
            local agent_skills_dir
            if [[ "$level" == "global" ]]; then
                agent_skills_dir="${AGENT_GLOBAL_DIRS[$agent]}"
            else
                agent_skills_dir="${PROJECT_DIR}/${AGENT_PROJECT_DIRS[$agent]}"
            fi
            
            local link_path="$agent_skills_dir/$skill_name"
            local link_target="$hub_dir/$skill_name"
            
            if agent_in_scope "$agent" "$scope"; then
                # 应该存在链接
                if $CLEAN_ONLY; then
                    continue
                fi
                
                if [[ -L "$link_path" ]]; then
                    local existing_target
                    existing_target=$(readlink "$link_path")
                    if [[ "$existing_target" == "$link_target" ]]; then
                        log_verbose "  $agent/$skill_name: 已存在且正确"
                        ((UNCHANGED++)) || true
                        continue
                    else
                        log_action "  更新链接: $agent/$skill_name -> $link_target (旧: $existing_target)"
                        if ! $DRY_RUN; then
                            rm "$link_path"
                            ln -s "$link_target" "$link_path"
                        fi
                        ((CREATED++)) || true
                    fi
                elif [[ -d "$link_path" ]]; then
                    # 是真实目录而非链接 — 说明未迁移，先警告
                    log_warn "  $agent/$skill_name: 是真实目录而非链接（可能需要先运行 migrate_to_hub.sh）"
                    ((ERRORS++)) || true
                elif [[ ! -e "$link_path" ]]; then
                    # 创建链接
                    log_action "  创建链接: $agent/$skill_name -> $link_target"
                    if ! $DRY_RUN; then
                        mkdir -p "$agent_skills_dir"
                        ln -s "$link_target" "$link_path"
                    fi
                    ((CREATED++)) || true
                fi
            else
                # 不应该存在链接
                if [[ -L "$link_path" ]]; then
                    local existing_target
                    existing_target=$(readlink "$link_path")
                    if [[ "$existing_target" == "$link_target" ]]; then
                        log_action "  移除链接: $agent/$skill_name (不在 scope 内)"
                        if ! $DRY_RUN; then
                            rm "$link_path"
                        fi
                        ((REMOVED++)) || true
                    fi
                fi
            fi
        done
    done
    
    # 清理：检查 Agent 目录中是否有指向 hub 的链接，但 hub 中技能已不存在
    for agent in "${AGENT_NAMES[@]}"; do
        local agent_skills_dir
        if [[ "$level" == "global" ]]; then
            agent_skills_dir="${AGENT_GLOBAL_DIRS[$agent]}"
        else
            agent_skills_dir="${PROJECT_DIR}/${AGENT_PROJECT_DIRS[$agent]}"
        fi
        
        [[ ! -d "$agent_skills_dir" ]] && continue
        
        for link in "$agent_skills_dir"/*/; do
            [[ ! -e "$link" ]] && continue
            local item="${link%/}"
            local item_name
            item_name=$(basename "$item")
            
            if [[ -L "$item" ]]; then
                local target
                target=$(readlink "$item")
                # 检查目标是否在 hub 中且仍存在
                if [[ "$target" == "$hub_dir/"* ]] && [[ ! -d "$target" ]]; then
                    log_action "  清理死链接: $agent/$item_name (目标已不存在)"
                    if ! $DRY_RUN; then
                        rm "$item"
                    fi
                    ((REMOVED++)) || true
                fi
            fi
        done
    done
}

# ============================================================
# 主流程
# ============================================================
main() {
    echo
    log_info "============================================"
    log_info "  Skill Manager — 同步技能链接"
    log_info "============================================"
    echo
    
    # 解析 Agent 注册表
    parse_agents_yaml
    echo
    
    # 同步 Global 层
    sync_hub "$SKILLS_HUB" "global"
    echo
    
    # 同步 Project 层（如果指定）
    if [[ -n "$PROJECT_DIR" ]]; then
        local project_skills="$PROJECT_DIR/.skills"
        if [[ -d "$project_skills" ]]; then
            sync_hub "$project_skills" "project"
        else
            log_warn "项目级 .skills 目录不存在: $project_skills"
        fi
        echo
    fi
    
    # 汇总报告
    echo
    log_info "============================================"
    log_info "  同步完成"
    log_info "============================================"
    log_info "  创建/更新链接: $CREATED"
    log_info "  移除链接:       $REMOVED"
    log_info "  未变更:         $UNCHANGED"
    if [[ $ERRORS -gt 0 ]]; then
        log_warn "  需注意:         $ERRORS"
    fi
    echo
    
    if $DRY_RUN; then
        log_warn "以上为 DRY RUN 预览，未做任何实际更改"
    fi
}

main
