#!/bin/bash
# xhs-kit Cookie规范化保存脚本
# 将cookie字符串保存为规范化的JSON文件

set -euo pipefail

COOKIE_DIR="xhs_cookies"
ACTIVE_FILE="$COOKIE_DIR/active.json"

# 颜色
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log() { echo -e "${BLUE}[INFO]${NC} $1"; }
success() { echo -e "${GREEN}✅${NC} $1"; }
warning() { echo -e "${YELLOW}⚠️${NC} $1"; }
error() { echo -e "${RED}❌${NC} $1"; }

show_help() {
    cat << EOF
xhs-kit Cookie规范化保存脚本

用法: $0 [选项]

选项:
  --name NAME          cookie名称（必需，如：new_main, old_backup）
  --cookie STRING      cookie字符串（与--file二选一）
  --file FILE          包含cookie的文件（与--cookie二选一）
  --desc DESCRIPTION   描述信息（可选）
  --set-active         设置为当前激活cookie
  --help              显示此帮助

命名规范:
  格式: 账号标识_描述_日期.json
  示例: new_main_20260314.json, old_backup_today.json

账号标识建议:
  new    - 新账号
  old    - 旧账号
  test   - 测试账号
  backup - 备份账号

示例:
  $0 --name new_main --cookie "a1=xxx;webId=yyy" --desc "主账号"
  $0 --name old_backup --file raw_cookie.txt --set-active
  $0 --name test_temp --cookie "\$(cat cookie.txt)" --desc "临时测试"

EOF
}

# 创建cookie目录
init_cookie_dir() {
    if [[ ! -d "$COOKIE_DIR" ]]; then
        mkdir -p "$COOKIE_DIR"
        log "创建cookie目录: $COOKIE_DIR"
    fi
    
    if [[ ! -d "$COOKIE_DIR/archive" ]]; then
        mkdir -p "$COOKIE_DIR/archive"
        log "创建归档目录: $COOKIE_DIR/archive"
    fi
}

# 生成文件名
generate_filename() {
    local name="$1"
    local desc="$2"
    local date_str=$(date +%Y%m%d)
    
    if [[ -n "$desc" ]]; then
        echo "${name}_${desc}_${date_str}.json"
    else
        echo "${name}_${date_str}.json"
    fi
}

# 解析cookie字符串
parse_cookie_string() {
    local cookie_str="$1"
    
    python3 -c "
import json, sys

cookie_str = '''$cookie_str'''

# 解析cookie字符串
cookies = []
for item in cookie_str.split('; '):
    item = item.strip()
    if not item:
        continue
    if '=' in item:
        key, value = item.split('=', 1)
        cookies.append({
            'name': key.strip(),
            'value': value.strip(),
            'domain': '.xiaohongshu.com',
            'path': '/'
        })

if not cookies:
    print('error:未解析到有效的cookie')
    sys.exit(1)

# 获取用户ID
user_id = next((c['value'] for c in cookies if c['name'] == 'x-user-id-creator.xiaohongshu.com'), '未知')

print(f'success:{user_id}:{len(cookies)}')
print(json.dumps(cookies, ensure_ascii=False, indent=2))
"
}

# 从文件读取cookie
read_cookie_from_file() {
    local file="$1"
    
    if [[ ! -f "$file" ]]; then
        error "文件不存在: $file"
        return 1
    fi
    
    # 尝试读取文件内容
    local content
    content=$(cat "$file")
    
    if [[ -z "$content" ]]; then
        error "文件为空: $file"
        return 1
    fi
    
    echo "$content"
}

# 保存cookie文件
save_cookie_file() {
    local filename="$1"
    local cookie_json="$2"
    local set_active="${3:-false}"
    
    local filepath="$COOKIE_DIR/$filename"
    
    # 保存JSON文件
    echo "$cookie_json" > "$filepath"
    
    # 获取用户ID用于显示
    local user_id
    user_id=$(echo "$cookie_json" | python3 -c "
import json, sys
data = json.load(sys.stdin)
user_id = next((c['value'] for c in data if c['name'] == 'x-user-id-creator.xiaohongshu.com'), '未知')
print(user_id)
")
    
    success "Cookie已保存: $filename"
    log "  用户ID: $user_id"
    log "  位置: $filepath"
    
    # 设置为激活cookie
    if [[ "$set_active" == "true" ]]; then
        set_active_cookie "$filename"
    fi
    
    echo "$filepath"
}

# 设置为激活cookie
set_active_cookie() {
    local filename="$1"
    local source_file="$COOKIE_DIR/$filename"
    local active_file="$ACTIVE_FILE"
    
    if [[ ! -f "$source_file" ]]; then
        error "Cookie文件不存在: $source_file"
        return 1
    fi
    
    # 创建或更新软链接
    ln -sf "$filename" "$active_file"
    
    success "已设置为激活cookie: $filename"
    log "  active.json -> $filename"
}

# 主函数
main() {
    # 解析参数
    local NAME=""
    local COOKIE_STR=""
    local COOKIE_FILE=""
    local DESC=""
    local SET_ACTIVE=false
    
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --name)
                NAME="$2"
                shift 2
                ;;
            --cookie)
                COOKIE_STR="$2"
                shift 2
                ;;
            --file)
                COOKIE_FILE="$2"
                shift 2
                ;;
            --desc)
                DESC="$2"
                shift 2
                ;;
            --set-active)
                SET_ACTIVE=true
                shift
                ;;
            --help|-h)
                show_help
                exit 0
                ;;
            *)
                error "未知选项: $1"
                show_help
                exit 1
                ;;
        esac
    done
    
    # 检查必需参数
    if [[ -z "$NAME" ]]; then
        error "必须指定cookie名称 (--name)"
        show_help
        exit 1
    fi
    
    if [[ -z "$COOKIE_STR" && -z "$COOKIE_FILE" ]]; then
        error "必须提供cookie字符串 (--cookie) 或文件 (--file)"
        show_help
        exit 1
    fi
    
    if [[ -n "$COOKIE_STR" && -n "$COOKIE_FILE" ]]; then
        warning "同时提供了--cookie和--file，优先使用--cookie"
    fi
    
    # 初始化目录
    init_cookie_dir
    
    # 获取cookie内容
    local cookie_content
    if [[ -n "$COOKIE_STR" ]]; then
        cookie_content="$COOKIE_STR"
        log "使用提供的cookie字符串"
    else
        cookie_content=$(read_cookie_from_file "$COOKIE_FILE") || exit 1
        log "从文件读取cookie: $(basename "$COOKIE_FILE")"
    fi
    
    # 解析cookie
    log "解析cookie..."
    local parse_result
    parse_result=$(parse_cookie_string "$cookie_content")
    
    if [[ $parse_result != success:* ]]; then
        error "解析失败: ${parse_result#error:}"
        exit 1
    fi
    
    # 提取结果
    IFS=':' read -r _ user_id count <<< "$(echo "$parse_result" | head -1)"
    local cookie_json=$(echo "$parse_result" | tail -n +2)
    
    success "Cookie解析成功"
    log "  用户ID: $user_id"
    log "  Cookie数量: $count"
    
    # 生成文件名
    local filename
    filename=$(generate_filename "$NAME" "$DESC")
    
    # 保存文件
    local saved_file
    saved_file=$(save_cookie_file "$filename" "$cookie_json" "$SET_ACTIVE")
    
    # 显示总结
    echo ""
    success "🎉 Cookie保存完成！"
    echo ""
    echo "📋 保存信息:"
    echo "  文件名: $filename"
    echo "  用户ID: $user_id"
    echo "  位置: $saved_file"
    
    if [[ "$SET_ACTIVE" == "true" ]]; then
        echo "  状态: ✅ 已设置为激活cookie"
    else
        echo "  状态: 📁 已保存，未激活"
        echo ""
        echo "💡 使用建议:"
        echo "  设置为激活: $0 --name $NAME --set-active"
        echo "  直接使用: ./xhs_final.sh --cookie $saved_file --title \"...\" --image ..."
    fi
    
    echo ""
    echo "🚀 立即使用:"
    echo "  ./xhs_final.sh --cookie $saved_file --title \"测试\" --content \"内容\" --image 图片.jpg"
}

# 运行主函数
main "$@"