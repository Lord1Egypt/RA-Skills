#!/bin/bash

# Obsidian知识库实用工具脚本
# 适配小编的编剧工作需求

API_BASE="http://192.168.18.15:5000"

# 获取当前日期
CURRENT_DATE=$(date +%Y-%m-%d)

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
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

# 健康检查
check_health() {
    log_info "检查API服务状态..."
    response=$(wget --timeout=5 -q -O - "$API_BASE/health")
    if echo "$response" | grep -q '"status":"ok"'; then
        log_success "API服务运行正常"
        echo "$response" | grep -o '"service":"[^"]*"' | cut -d'"' -f4
    else
        log_error "API服务异常: $response"
        return 1
    fi
}

# 获取统计信息
get_stats() {
    log_info "获取知识库统计信息..."
    response=$(wget --timeout=5 -q -O - "$API_BASE/api/stats")
    if echo "$response" | grep -q "total_notes"; then
        total_notes=$(echo "$response" | grep -o '"total_notes":[0-9]*' | cut -d: -f2)
        echo "总笔记数: $total_notes"
    else
        log_error "获取统计信息失败"
    fi
}

# 搜索笔记
search_notes() {
    local query="$1"
    if [ -z "$query" ]; then
        log_error "请提供搜索关键词"
        return 1
    fi
    
    log_info "搜索相关笔记: $query"
    
    # 使用GET方式的搜索（如果API支持）
    response=$(wget --timeout=10 -q -O - "$API_BASE/api/search?query=$query")
    
    if echo "$response" | grep -q "results"; then
        results=$(echo "$response" | grep -o '"results":\[.*\]' | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    results = data.get('results', [])
    print(f'找到 {len(results)} 条相关结果')
    for i, result in enumerate(results[:5]):
        title = result.get('title', '无标题')
        score = result.get('score', 0)
        print(f'  {i+1}. {title} (相似度: {score:.3f})')
except:
    print('解析结果失败')
")
        echo "$results"
    else
        log_warning "搜索结果格式异常"
    fi
}

# 列出项目笔记
list_project_notes() {
    local project_name="$1"
    if [ -z "$project_name" ]; then
        log_error "请提供项目名称"
        return 1
    fi
    
    local folder="project_${project_name}/scripts"
    log_info "列出项目 '$project_name' 的编剧笔记..."
    
    response=$(wget --timeout=5 -q -O - "$API_BASE/api/notes?folder=$folder")
    if echo "$response" | grep -q "notes"; then
        count=$(echo "$response" | grep -o '"notes":\[.*\]' | grep -o '"' | wc -l)
        if [ "$count" -gt 2 ]; then  # 减去前后括号
            note_count=$((count/2))
            echo "找到 $note_count 条编剧笔记:"
            echo "$response" | grep -o '"title":"[^"]*"' | sed 's/"title":"/- /' | sed 's/"$//'
        else
            echo "暂无编剧笔记"
        fi
    else
        log_warning "获取项目笔记失败"
    fi
}

# 创建编剧工作笔记（需要curl，这里是基础版本）
create_script_note_manual() {
    local project_name="$1"
    local note_title="$2"
    local content="$3"
    
    if [ -z "$project_name" ] || [ -z "$note_title" ] || [ -z "$content" ]; then
        log_error "项目名称、笔记标题和内容都不能为空"
        return 1
    fi
    
    log_info "创建编剧笔记: $note_title"
    
    # 构建完整内容（包括元数据）
    local full_content=$(cat <<EOF
---
host: 4090服务器 (192.168.18.15)
agent: 小编 (编剧)
created: $(date +%Y-%m-%d)
updated: $(date +%Y-%m-%d)
---

# $note_title

$content
EOF
)
    
    # 临时文件
    local temp_file="/tmp/script_note_$(date +%s).md"
    echo "$full_content" > "$temp_file"
    
    log_info "笔记内容已保存到临时文件: $temp_file"
    log_warning "由于系统没有curl，无法自动创建到Obsidian库"
    log_info "您可以手动将文件移动到: /mnt/share2win/openclaw_datas/obsidian_db/project_${project_name}/scripts/"
    echo "文件内容:"
    echo "$full_content"
    
    # 清理临时文件
    rm -f "$temp_file"
}

# 创建编剧工作日志
create_script_log() {
    local project_name="$1"
    local log_content="$2"
    
    if [ -z "$project_name" ]; then
        log_error "请提供项目名称"
        return 1
    fi
    
    local title="$CURRENT_DATE - 工作日志"
    
    if [ -z "$log_content" ]; then
        log_content=$(cat <<EOF
# $CURRENT_DATE 工作日志

## 今日完成
- 项目进展记录
- 创作心得
- 问题解决

## 明日计划
- 继续创作
- 完善细节
- 团队协作

## 需要协助
- 
EOF
)
    fi
    
    create_script_note_manual "$project_name" "$title" "$log_content"
}

# 显示帮助
show_help() {
    echo "Obsidian知识库工具 - 小编专用"
    echo ""
    echo "用法: $0 [命令] [参数]"
    echo ""
    echo "可用命令:"
    echo "  health              检查API服务状态"
    echo "  stats              获取知识库统计信息"
    echo "  search <关键词>     搜索相关笔记"
    echo "  list <项目名>       列出项目的编剧笔记"
    echo "  log <项目名> [内容] 创建工作日志"
    echo "  note <项目名> <标题> <内容> 创建编剧笔记"
    echo "  help               显示此帮助"
    echo ""
    echo "示例:"
    echo "  $0 health"
    echo "  $0 search 角色塑造"
    echo "  $0 list project_001"
    echo "  $0 log project_001"
    echo "  $0 note project_001 角色设计 '详细设计内容...'"
}

# 主函数
main() {
    case "$1" in
        "health")
            check_health
            ;;
        "stats")
            get_stats
            ;;
        "search")
            search_notes "$2"
            ;;
        "list")
            list_project_notes "$2"
            ;;
        "log")
            create_script_log "$2" "$3"
            ;;
        "note")
            create_script_note_manual "$2" "$3" "$4"
            ;;
        "help"|"-h"|"--help")
            show_help
            ;;
        "")
            log_error "请提供命令，使用 '$0 help' 查看帮助"
            ;;
        *)
            log_error "未知命令: $1"
            show_help
            ;;
    esac
}

# 执行主函数
main "$@"