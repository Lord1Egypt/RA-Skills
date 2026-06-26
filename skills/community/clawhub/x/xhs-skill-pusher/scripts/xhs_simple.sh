#!/bin/bash
# xhs-kit简单发布脚本 - 完全基于文件路径
# 设计原则：一致性、简单性、透明性

set -euo pipefail

# 配置
SCRIPT_NAME="xhs_simple.sh"
DEFAULT_COOKIE="cookies.json"

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 日志
log() { echo -e "${BLUE}[INFO]${NC} $1"; }
success() { echo -e "${GREEN}✅${NC} $1"; }
error() { echo -e "${RED}❌${NC} $1"; }
warning() { echo -e "${YELLOW}⚠️${NC} $1"; }

# 显示帮助
show_help() {
    cat << EOF
xhs-kit简单发布脚本 - 完全基于文件路径

设计原则：
  1. 一致性：只使用文件路径，不使用账号名映射
  2. 简单性：一个--cookie参数解决所有问题
  3. 透明性：所有操作基于实际文件

核心命令：
  ./xhs_simple.sh --cookie <cookie文件> --title "标题" --content "内容" --image 图片.jpg

必需参数：
  --cookie FILE      Cookie文件路径（支持两种格式）
  --title TEXT       笔记标题（≤20字）
  --content TEXT     笔记内容
  --image FILE       图片路径（可多次指定）

可选参数：
  --tag TEXT         标签（可多次指定）
  --schedule TIME    定时发布时间，格式：2026-03-14T14:00:00+08:00
  --show-browser     显示浏览器窗口
  --debug-only       仅验证，不实际发布
  --check-status     仅检查登录状态
  --list-cookies     列出所有cookie文件
  --help             显示此帮助

文件管理命令：
  # 列出所有cookie文件
  ./xhs_simple.sh --list-cookies
  
  # 使用指定cookie文件发布
  ./xhs_simple.sh --cookie cookies_new_account.json --title "..." --content "..." --image ...
  
  # 使用原始格式cookie文件发布
  ./xhs_simple.sh --cookie new_xhs_cookies.json --title "..." --content "..." --image ...
  
  # 检查cookie状态
  ./xhs_simple.sh --cookie cookies.json --check-status

Cookie文件支持：
  1. xhs-kit格式：[{"name":"key","value":"value","domain":".xiaohongshu.com","path":"/"}]
  2. 原始格式：{"key": "value", "key2": "value2"}

当前目录的重要文件：
  cookies.json              - xhs-kit默认读取的文件
  cookies_new_account.json  - 新账号cookie（xhs-kit格式）
  cookies_old_account.json  - 旧账号cookie（xhs-kit格式）
  new_xhs_cookies.json      - 原始格式cookie

使用流程：
  1. 获取cookie，保存为文件（如：my_cookie.json）
  2. 直接使用：./xhs_simple.sh --cookie my_cookie.json --title "..." --image ...
  3. 无需切换账号，无需账号名映射

EOF
}

# 激活虚拟环境
activate_env() {
    if [[ -f "xhs-env/bin/activate" ]]; then
        source xhs-env/bin/activate
        log "虚拟环境已激活"
    else
        error "虚拟环境不存在：xhs-env"
        exit 1
    fi
}

# 检查依赖
check_deps() {
    if ! command -v xhs-kit &> /dev/null; then
        error "xhs-kit未安装"
        exit 1
    fi
    success "xhs-kit已就绪"
}

# 转换cookie格式
convert_cookie() {
    local src="$1"
    local dst="$2"
    
    python3 -c "
import json, sys
try:
    with open('$src', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if isinstance(data, list) and data and 'name' in data[0]:
        # 已经是xhs-kit格式
        converted = data
        format_type = 'xhs-kit格式'
    else:
        # 转换原始格式
        converted = []
        for key, value in data.items():
            converted.append({
                'name': key,
                'value': str(value),
                'domain': '.xiaohongshu.com',
                'path': '/'
            })
        format_type = '原始格式（已转换）'
    
    with open('$dst', 'w', encoding='utf-8') as f:
        json.dump(converted, f, ensure_ascii=False, indent=2)
    
    # 获取用户ID
    user_id = next((c['value'] for c in converted if c['name'] == 'x-user-id-creator.xiaohongshu.com'), '未知')
    
    print(f'success:{format_type}:{user_id}:{len(converted)}')
    
except Exception as e:
    print(f'error:{e}')
    sys.exit(1)
"
}

# 准备cookie
prepare_cookie() {
    local cookie_file="$1"
    
    if [[ ! -f "$cookie_file" ]]; then
        error "Cookie文件不存在：$cookie_file"
        return 1
    fi
    
    log "使用Cookie文件：$(basename "$cookie_file")"
    
    local result
    result=$(convert_cookie "$cookie_file" "$DEFAULT_COOKIE")
    
    if [[ $result == success:* ]]; then
        IFS=':' read -r _ format_type user_id count <<< "$result"
        success "Cookie已准备"
        log "  格式：$format_type"
        log "  用户ID：$user_id"
        log "  Cookie数量：$count"
        return 0
    else
        error "Cookie转换失败：${result#error:}"
        return 1
    fi
}

# 列出所有cookie文件
list_cookies() {
    log "查找Cookie文件..."
    
    local files=()
    while IFS= read -r file; do
        files+=("$file")
    done < <(find . -maxdepth 1 -name "*.json" -type f | sort)
    
    if [[ ${#files[@]} -eq 0 ]]; then
        warning "未找到JSON文件"
        return
    fi
    
    echo ""
    echo "📁 Cookie文件列表："
    echo "----------------------------------------"
    
    for file in "${files[@]}"; do
        local basename=$(basename "$file")
        local size=$(stat -f%z "$file" 2>/dev/null || echo "?")
        
        # 尝试获取用户ID
        local user_info=""
        if python3 -c "
import json, sys
try:
    with open('$file', 'r') as f:
        data = json.load(f)
    if isinstance(data, list):
        user_id = next((c['value'] for c in data if c['name'] == 'x-user-id-creator.xiaohongshu.com'), None)
    else:
        user_id = data.get('x-user-id-creator.xiaohongshu.com')
    if user_id:
        print(user_id[:8] + '...')
except:
    pass
" 2>/dev/null; then
            user_info=$(python3 -c "
import json
try:
    with open('$file', 'r') as f:
        data = json.load(f)
    if isinstance(data, list):
        user_id = next((c['value'] for c in data if c['name'] == 'x-user-id-creator.xiaohongshu.com'), '未知')
    else:
        user_id = data.get('x-user-id-creator.xiaohongshu.com', '未知')
    print(user_id)
except:
    print('格式错误')
" 2>/dev/null)
        fi
        
        if [[ "$basename" == "$DEFAULT_COOKIE" ]]; then
            echo "  📌 $basename (${size}字节) - $user_info ← 当前激活"
        else
            echo "  📄 $basename (${size}字节) - $user_info"
        fi
    done
    
    echo ""
    echo "💡 使用方式："
    echo "  ./xhs_simple.sh --cookie 文件名.json --title \"标题\" --image 图片.jpg"
}

# 检查状态
check_status() {
    log "检查登录状态..."
    if xhs-kit status; then
        success "登录状态正常"
        return 0
    else
        error "登录状态异常"
        return 1
    fi
}

# debug验证
debug_validate() {
    local title="$1"
    local content="$2"
    shift 2
    local images=("$@")
    
    log "debug验证..."
    
    local cmd=("xhs-kit" "debug-publish" "--title" "$title" "--content" "$content" "--verbose")
    
    for img in "${images[@]}"; do
        if [[ ! -f "$img" ]]; then
            error "图片不存在：$img"
            return 1
        fi
        cmd+=("--image" "$img")
    done
    
    for tag in "${TAGS[@]:-}"; do
        cmd+=("--tag" "$tag")
    done
    
    if "${cmd[@]}"; then
        success "debug验证通过"
        return 0
    else
        error "debug验证失败"
        return 1
    fi
}

# 实际发布
do_publish() {
    local title="$1"
    local content="$2"
    shift 2
    local images=("$@")
    
    log "开始发布..."
    
    local cmd=("xhs-kit" "publish" "--title" "$title" "--content" "$content")
    
    for img in "${images[@]}"; do
        cmd+=("--image" "$img")
    done
    
    for tag in "${TAGS[@]:-}"; do
        cmd+=("--tag" "$tag")
    done
    
    if [[ -n "${SCHEDULE:-}" ]]; then
        cmd+=("--schedule-at" "$SCHEDULE")
    fi
    
    if [[ "${SHOW_BROWSER:-false}" == "true" ]]; then
        cmd+=("--no-headless")
        export XHS_ALLOW_NON_HEADLESS=1
    fi
    
    if "${cmd[@]}"; then
        success "发布完成！"
        return 0
    else
        error "发布失败"
        return 1
    fi
}

# 主函数
main() {
    # 解析参数
    local COOKIE_FILE=""
    local TITLE=""
    local CONTENT=""
    local IMAGES=()
    local TAGS=()
    local SCHEDULE=""
    local SHOW_BROWSER=false
    local DEBUG_ONLY=false
    local CHECK_STATUS=false
    local LIST_COOKIES=false
    
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --cookie)
                COOKIE_FILE="$2"
                shift 2
                ;;
            --title)
                TITLE="$2"
                shift 2
                ;;
            --content)
                CONTENT="$2"
                shift 2
                ;;
            --image)
                IMAGES+=("$2")
                shift 2
                ;;
            --tag)
                TAGS+=("$2")
                shift 2
                ;;
            --schedule)
                SCHEDULE="$2"
                shift 2
                ;;
            --show-browser)
                SHOW_BROWSER=true
                shift
                ;;
            --debug-only)
                DEBUG_ONLY=true
                shift
                ;;
            --check-status)
                CHECK_STATUS=true
                shift
                ;;
            --list-cookies)
                LIST_COOKIES=true
                shift
                ;;
            --help|-h)
                show_help
                exit 0
                ;;
            *)
                error "未知选项：$1"
                show_help
                exit 1
                ;;
        esac
    done
    
    # 激活环境
    activate_env
    check_deps
    
    # 处理特殊命令
    if [[ "$LIST_COOKIES" == true ]]; then
        list_cookies
        exit 0
    fi
    
    # 检查必需参数
    if [[ -z "$COOKIE_FILE" ]] && [[ "$CHECK_STATUS" != true ]]; then
        error "必须指定cookie文件（使用--cookie参数）"
        show_help
        exit 1
    fi
    
    if [[ "$CHECK_STATUS" == true ]]; then
        if [[ -n "$COOKIE_FILE" ]]; then
            prepare_cookie "$COOKIE_FILE" || exit 1
        fi
        check_status
        exit $?
    fi
    
    if [[ -z "$TITLE" || -z "$CONTENT" || ${#IMAGES[@]} -eq 0 ]]; then
        error "标题、内容和图片为必需参数"
        show_help
        exit 1
    fi
    
    # 准备cookie
    prepare_cookie "$COOKIE_FILE" || exit 1
    
    # 检查状态
    check_status || exit 1
    
    # 显示发布信息
    echo ""
    echo "📝 发布信息："
    echo "----------------------------------------"
    log "标题：$TITLE"
    log "内容长度：${#CONTENT}字符"
    log "图片：${#IMAGES[@]}张"
    [[ ${#TAGS[@]} -gt 0 ]] && log "标签：${TAGS[*]}"
    [[ -n "$SCHEDULE" ]] && log "定时发布：$SCHEDULE"
    [[ "$SHOW_BROWSER" == true ]] && log "浏览器：显示窗口" || log "浏览器：无头模式"
    echo ""
    
    # debug验证
    debug_validate "$TITLE" "$CONTENT" "${IMAGES[@]}" || exit 1
    
    # 如果只需要debug验证
    if [[ "$DEBUG_ONLY" == true ]]; then
        success "debug验证完成"
        exit 0
    fi
    
    # 实际发布
    if do_publish "$TITLE" "$CONTENT" "${IMAGES[@]}"; then
        echo ""
        success "🎉 发布成功！请在小红书App中确认。"
    else
        error "发布失败"
        exit 1
    fi
}

# 运行
main "$@"