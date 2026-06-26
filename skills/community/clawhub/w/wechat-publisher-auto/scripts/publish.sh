#!/bin/bash
#===============================================================================
# wechat-publisher - 微信公众号发布脚本
# 
# 完全独立实现，不依赖任何外部 CLI 工具
# 
# 使用方式: ./publish.sh <markdown_or_html_file>
# 示例: 
#   ./publish.sh article.html
#   ./publish.sh article.md
#===============================================================================

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 默认值
HUMANIZE="${WECHAT_HUMANIZE:-true}"
INTENSITY="${WECHAT_HUMANIZE_INTENSITY:-medium}"

# 帮助信息
show_help() {
    cat << EOF
${BLUE}wechat-publisher - 微信公众号发布工具${NC}

${YELLOW}使用方法:${NC}
    $0 <file> [options]

${YELLOW}参数:${NC}
    file             HTML 或 Markdown 文件路径（必填）

${YELLOW}选项:${NC}
    --title <title>     指定文章标题
    --cover <path>      指定封面图片
    --humanize          启用 AI 去痕（默认）
    --no-humanize       禁用 AI 去痕
    --intensity <level> 去痕强度 (light/medium/heavy)

${YELLOW}环境变量:${NC}
    WECHAT_APP_ID              微信 AppID
    WECHAT_APP_SECRET          微信 AppSecret
    WECHAT_HUMANIZE            是否启用 AI 去痕 (true/false)
    WECHAT_HUMANIZE_INTENSITY  去痕强度 (light/medium/heavy)
    AI_API_KEY                 AI API Key
    AI_PROVIDER                AI Provider

${YELLOW}示例:${NC}
    $0 article.html
    $0 article.html --title "我的文章"
    $0 article.html --no-humanize
    $0 article.html --intensity heavy

EOF
}

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
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

# 检查依赖
check_dependencies() {
    log_info "检查依赖..."
    
    if ! command -v python3 &> /dev/null; then
        log_error "python3 未安装"
        exit 1
    fi
    
    if ! python3 -c "import wechat_publisher" 2>/dev/null; then
        log_error "wechat-publisher 未安装，请运行: pip install wechat-publisher"
        exit 1
    fi
    
    log_success "依赖检查通过"
}

# 加载环境变量
load_env() {
    local env_file="$HOME/.openclaw/.env"
    if [[ -f "$env_file" ]]; then
        log_info "从 $env_file 加载环境变量"
        set -a
        source "$env_file"
        set +a
    fi
}

# 主流程
main() {
    local file=""
    local title=""
    local cover=""
    
    # 解析参数
    while [[ $# -gt 0 ]]; do
        case "$1" in
            -h|--help)
                show_help
                exit 0
                ;;
            --title)
                title="$2"
                shift 2
                ;;
            --cover)
                cover="$2"
                shift 2
                ;;
            --humanize)
                HUMANIZE="true"
                shift
                ;;
            --no-humanize)
                HUMANIZE="false"
                shift
                ;;
            --intensity)
                INTENSITY="$2"
                shift 2
                ;;
            -*)
                log_error "未知选项: $1"
                show_help
                exit 1
                ;;
            *)
                if [[ -z "$file" ]]; then
                    file="$1"
                fi
                shift
                ;;
        esac
    done
    
    # 检查必填参数
    if [[ -z "$file" ]]; then
        log_error "缺少必填参数：file"
        show_help
        exit 1
    fi
    
    # 检查文件是否存在
    if [[ ! -f "$file" ]]; then
        log_error "文件不存在: $file"
        exit 1
    fi
    
    # 转换为绝对路径
    file="$(cd "$(dirname "$file")" && pwd)/$(basename "$file")"
    log_info "文件: $file"
    
    # 检查依赖
    check_dependencies
    
    # 加载环境变量
    load_env
    
    # 构建发布命令
    local publish_cmd="wechat-publisher publish \"$file\""
    
    [[ -n "$title" ]] && publish_cmd="$publish_cmd --title \"$title\""
    [[ -n "$cover" ]] && publish_cmd="$publish_cmd --cover \"$cover\""
    
    if [[ "$HUMANIZE" != "true" ]]; then
        publish_cmd="$publish_cmd --no-humanize"
        log_info "AI 去痕: 禁用"
    else
        publish_cmd="$publish_cmd --intensity $INTENSITY"
        log_info "AI 去痕: 启用 (强度: $INTENSITY)"
    fi
    
    log_info "执行: $publish_cmd"
    
    # 执行发布命令
    eval $publish_cmd
    
    log_success "发布完成！"
    log_info "请前往微信公众号后台草稿箱查看: https://mp.weixin.qq.com/"
}

main "$@"
