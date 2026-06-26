#!/bin/bash
# plan-manager.sh - 计划文件管理工具
# 用于创建、更新、查询复杂任务的计划文件

set -euo pipefail

# 配置
WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
PLAN_DIR="$WORKSPACE/temp"
TEMPLATE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../templates" && pwd)"
ARCHIVE_DIR="$WORKSPACE/Assets/Projects"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 显示帮助
show_help() {
    cat << EOF
计划文件管理工具 - Session Guardian v2.0

用法:
  $0 create <任务名>              创建新的计划文件
  $0 update <任务名> <子任务ID>   更新子任务状态
  $0 list                         列出所有计划文件
  $0 show <任务名>                显示计划文件内容
  $0 archive <任务名>             归档已完成的计划文件
  $0 clean                        清理旧的计划文件（>30天）

示例:
  $0 create "智能巡检产品演示材料"
  $0 update "智能巡检产品演示材料" 1.1
  $0 show "智能巡检产品演示材料"
  $0 archive "智能巡检产品演示材料"

EOF
}

# 创建计划文件
create_plan() {
    local task_name="$1"
    local plan_file="$PLAN_DIR/${task_name}-plan.md"
    local template_file="$TEMPLATE_DIR/task-plan-template.md"
    
    # 检查是否已存在
    if [[ -f "$plan_file" ]]; then
        log_warning "计划文件已存在: $plan_file"
        read -p "是否覆盖? (y/N) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            log_info "取消创建"
            return 1
        fi
    fi
    
    # 确保目录存在
    mkdir -p "$PLAN_DIR"
    
    # 从模板创建
    if [[ -f "$template_file" ]]; then
        cp "$template_file" "$plan_file"
        # 替换任务名和时间
        sed -i.bak "s/{{TASK_NAME}}/$task_name/g" "$plan_file"
        sed -i.bak "s/{{CREATE_TIME}}/$(date '+%Y-%m-%d %H:%M')/g" "$plan_file"
        rm -f "$plan_file.bak"
    else
        # 如果模板不存在，创建基础结构
        cat > "$plan_file" << EOF
# $task_name - 任务计划

**创建时间**: $(date '+%Y-%m-%d %H:%M')
**状态**: 进行中
**负责人**: 

---

## 任务目标


---

## 子任务清单

### 阶段1: 
- [ ] 1.1 

---

## 当前进度

**状态**: 待办
**当前阶段**: 阶段1
**完成度**: 0/1

---

## 下一步行动

1. 

---

## 风险与阻塞


---

## 技术决策


---

**最后更新**: $(date '+%Y-%m-%d %H:%M')
EOF
    fi
    
    log_success "计划文件已创建: $plan_file"
    log_info "请编辑文件填写详细内容"
}

# 更新子任务状态
update_task() {
    local task_name="$1"
    local subtask_id="$2"
    local plan_file="$PLAN_DIR/${task_name}-plan.md"
    
    if [[ ! -f "$plan_file" ]]; then
        log_error "计划文件不存在: $plan_file"
        return 1
    fi
    
    # 将 [ ] 改为 [x]
    if grep -q "^\- \[ \] $subtask_id" "$plan_file"; then
        sed -i.bak "s/^- \[ \] $subtask_id/- [x] $subtask_id/" "$plan_file"
        rm -f "$plan_file.bak"
        
        # 更新最后更新时间
        sed -i.bak "s/\*\*最后更新\*\*:.*/\*\*最后更新\*\*: $(date '+%Y-%m-%d %H:%M')/" "$plan_file"
        rm -f "$plan_file.bak"
        
        log_success "子任务 $subtask_id 已标记为完成"
        
        # 计算完成度
        local total=$(grep -c "^\- \[" "$plan_file" || echo 0)
        local done=$(grep -c "^\- \[x\]" "$plan_file" || echo 0)
        log_info "当前完成度: $done/$total"
    else
        log_warning "子任务 $subtask_id 未找到或已完成"
    fi
}

# 列出所有计划文件
list_plans() {
    log_info "当前计划文件:"
    echo
    
    if [[ ! -d "$PLAN_DIR" ]]; then
        log_warning "计划目录不存在: $PLAN_DIR"
        return 0
    fi
    
    local count=0
    for plan_file in "$PLAN_DIR"/*-plan.md; do
        if [[ -f "$plan_file" ]]; then
            local task_name=$(basename "$plan_file" | sed 's/-plan\.md$//')
            local status=$(grep "^\*\*状态\*\*:" "$plan_file" | sed 's/.*: //' || echo "未知")
            local updated=$(grep "^\*\*最后更新\*\*:" "$plan_file" | sed 's/.*: //' || echo "未知")
            local total=$(grep -c "^- \[" "$plan_file" || echo 0)
            local done=$(grep -c "^- \[x\]" "$plan_file" || echo 0)
            
            echo "📋 $task_name"
            echo "   状态: $status | 完成度: $done/$total | 更新: $updated"
            echo
            ((count++))
        fi
    done
    
    if [[ $count -eq 0 ]]; then
        log_info "没有找到计划文件"
    else
        log_info "共 $count 个计划文件"
    fi
}

# 显示计划文件内容
show_plan() {
    local task_name="$1"
    local plan_file="$PLAN_DIR/${task_name}-plan.md"
    
    if [[ ! -f "$plan_file" ]]; then
        log_error "计划文件不存在: $plan_file"
        return 1
    fi
    
    cat "$plan_file"
}

# 归档计划文件
archive_plan() {
    local task_name="$1"
    local plan_file="$PLAN_DIR/${task_name}-plan.md"
    
    if [[ ! -f "$plan_file" ]]; then
        log_error "计划文件不存在: $plan_file"
        return 1
    fi
    
    # 确保归档目录存在
    mkdir -p "$ARCHIVE_DIR"
    
    # 移动到归档目录
    local archive_file="$ARCHIVE_DIR/${task_name}-plan-$(date +%Y%m%d).md"
    mv "$plan_file" "$archive_file"
    
    log_success "计划文件已归档: $archive_file"
}

# 清理旧的计划文件
clean_plans() {
    log_info "清理超过30天的计划文件..."
    
    if [[ ! -d "$PLAN_DIR" ]]; then
        log_warning "计划目录不存在: $PLAN_DIR"
        return 0
    fi
    
    local count=0
    find "$PLAN_DIR" -name "*-plan.md" -type f -mtime +30 | while read -r plan_file; do
        local task_name=$(basename "$plan_file" | sed 's/-plan\.md$//')
        log_info "删除旧计划: $task_name"
        rm -f "$plan_file"
        ((count++))
    done
    
    if [[ $count -eq 0 ]]; then
        log_info "没有需要清理的文件"
    else
        log_success "已清理 $count 个旧计划文件"
    fi
}

# 主函数
main() {
    local command="${1:-}"
    
    case "$command" in
        create)
            if [[ -z "${2:-}" ]]; then
                log_error "请指定任务名"
                show_help
                exit 1
            fi
            create_plan "$2"
            ;;
        update)
            if [[ -z "${2:-}" ]] || [[ -z "${3:-}" ]]; then
                log_error "请指定任务名和子任务ID"
                show_help
                exit 1
            fi
            update_task "$2" "$3"
            ;;
        list)
            list_plans
            ;;
        show)
            if [[ -z "${2:-}" ]]; then
                log_error "请指定任务名"
                show_help
                exit 1
            fi
            show_plan "$2"
            ;;
        archive)
            if [[ -z "${2:-}" ]]; then
                log_error "请指定任务名"
                show_help
                exit 1
            fi
            archive_plan "$2"
            ;;
        clean)
            clean_plans
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            log_error "未知命令: $command"
            show_help
            exit 1
            ;;
    esac
}

main "$@"
