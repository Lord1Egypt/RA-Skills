#!/bin/bash
#===============================================================================
# 豆包文生图 API 调用脚本 - Doubao SeeDream Image Generation
# 
# 功能：调用火山引擎 ARK API 生成 AI 图片
# 版本：2.0.0
# 作者：YangYang
# 许可：MIT License
#
# 用法:
#   ./doubao-image-generate.sh "<prompt>" [size] [watermark] [output_dir]
#
# 参数:
#   prompt      - 图片描述（必需）
#   size        - 分辨率：2K|1080P|720P（默认：2K）
#   watermark   - 是否水印：true|false（默认：true）
#   output_dir  - 输出目录（默认：generated-images）
#
# 示例:
#   ./doubao-image-generate.sh "一只在月光下的白色小猫"
#   ./doubao-image-generate.sh "赛博朋克城市夜景" "1080P" "false"
#   ./doubao-image-generate.sh "山水画" "2K" "true" "./my-images"
#
# 环境变量:
#   ARK_API_KEY           - 火山引擎 ARK API Key（必需）
#   DOUBAO_API_TIMEOUT    - API 超时时间（秒，默认：60）
#   DOUBAO_RETRY_COUNT    - 失败重试次数（默认：3）
#   DOUBAO_OUTPUT_DIR     - 默认输出目录（默认：generated-images）
#   DOUBAO_VERBOSE        - 详细日志模式（默认：false）
#===============================================================================

set -euo pipefail

#-------------------------------------------------------------------------------
# 配置常量
#-------------------------------------------------------------------------------
readonly VERSION="2.0.0"
readonly SCRIPT_NAME=$(basename "$0")
readonly SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
readonly API_URL="https://ark.cn-beijing.volces.com/api/v3/images/generations"
readonly MODEL="doubao-seedream-5-0-260128"

# 默认参数
DEFAULT_SIZE="2K"
DEFAULT_WATERMARK="true"
DEFAULT_TIMEOUT="${DOUBAO_API_TIMEOUT:-60}"
DEFAULT_RETRY_COUNT="${DOUBAO_RETRY_COUNT:-3}"
DEFAULT_OUTPUT_DIR="${DOUBAO_OUTPUT_DIR:-generated-images}"
VERBOSE="${DOUBAO_VERBOSE:-false}"

# 颜色输出
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly NC='\033[0m' # No Color

#-------------------------------------------------------------------------------
# 日志函数
#-------------------------------------------------------------------------------
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

log_debug() {
    if [ "$VERBOSE" = "true" ]; then
        echo -e "${BLUE}[DEBUG]${NC} $1"
    fi
}

log_timestamp() {
    date "+%Y-%m-%d %H:%M:%S"
}

#-------------------------------------------------------------------------------
# 使用帮助
#-------------------------------------------------------------------------------
show_help() {
    cat << EOF
${SCRIPT_NAME} v${VERSION} - 豆包文生图 API 调用脚本

用法:
  $SCRIPT_NAME "<prompt>" [size] [watermark] [output_dir]

参数:
  prompt       图片描述文本（必需，使用引号包裹）
  size         分辨率：2K, 1080P, 720P（默认：$DEFAULT_SIZE）
  watermark    是否添加水印：true, false（默认：$DEFAULT_WATERMARK）
  output_dir   图片保存目录（默认：$DEFAULT_OUTPUT_DIR）

示例:
  $SCRIPT_NAME "一只在月光下的白色小猫"
  $SCRIPT_NAME "赛博朋克风格的城市夜景" "1080P"
  $SCRIPT_NAME "中国风山水画" "2K" "false" "./artworks"

环境变量:
  ARK_API_KEY           火山引擎 ARK API Key（必需）
  DOUBAO_API_TIMEOUT    API 超时时间（秒，默认：60）
  DOUBAO_RETRY_COUNT    失败重试次数（默认：3）
  DOUBAO_OUTPUT_DIR     默认输出目录（默认：generated-images）
  DOUBAO_VERBOSE        启用详细日志（true/false）

退出码:
  0   成功
  1   参数错误或缺少必需环境变量
  2   API 调用失败
  3   图片下载失败
  4   文件系统错误

EOF
}

#-------------------------------------------------------------------------------
# 版本信息
#-------------------------------------------------------------------------------
show_version() {
    echo "$SCRIPT_NAME version $VERSION"
}

#-------------------------------------------------------------------------------
# 环境检查
#-------------------------------------------------------------------------------
check_environment() {
    local errors=0
    
    log_debug "开始环境检查..."
    
    # 检查 ARK_API_KEY
    if [ -z "${ARK_API_KEY:-}" ]; then
        log_error "缺少 ARK_API_KEY 环境变量"
        log_error "请设置：export ARK_API_KEY=your_api_key"
        log_error "获取地址：https://console.volcengine.com/ark"
        errors=$((errors + 1))
    else
        log_debug "✓ ARK_API_KEY 已配置"
    fi
    
    # 检查 curl
    if ! command -v curl &> /dev/null; then
        log_error "缺少 curl 命令，请安装：brew install curl (macOS) 或 apt-get install curl (Linux)"
        errors=$((errors + 1))
    else
        log_debug "✓ curl 已安装"
    fi
    
    # 检查 python3（用于 JSON 处理）
    if ! command -v python3 &> /dev/null; then
        log_error "缺少 Python 3，请安装：brew install python3 (macOS) 或 apt-get install python3 (Linux)"
        errors=$((errors + 1))
    else
        log_debug "✓ Python 3 已安装"
    fi
    
    if [ $errors -gt 0 ]; then
        log_error "环境检查失败，发现 $errors 个错误"
        return 1
    fi
    
    log_debug "✓ 环境检查通过"
    return 0
}

#-------------------------------------------------------------------------------
# 参数验证
#-------------------------------------------------------------------------------
validate_params() {
    local prompt="$1"
    local size="$2"
    local watermark="$3"
    
    # 检查 prompt
    if [ -z "$prompt" ]; then
        log_error "请提供图片描述 prompt"
        log_error "用法：$SCRIPT_NAME \"<prompt>\" [size] [watermark] [output_dir]"
        return 1
    fi
    
    # 验证 size 参数
    case "$size" in
        2K|1080P|720P)
            log_debug "✓ 尺寸参数有效：$size"
            ;;
        *)
            log_error "无效的尺寸参数：$size"
            log_error "有效值：2K, 1080P, 720P"
            return 1
            ;;
    esac
    
    # 验证 watermark 参数
    case "$watermark" in
        true|false)
            log_debug "✓ 水印参数有效：$watermark"
            ;;
        *)
            log_error "无效的水印参数：$watermark"
            log_error "有效值：true, false"
            return 1
            ;;
    esac
    
    return 0
}

#-------------------------------------------------------------------------------
# 创建输出目录
#-------------------------------------------------------------------------------
ensure_output_dir() {
    local output_dir="$1"
    
    if [ ! -d "$output_dir" ]; then
        log_debug "创建输出目录：$output_dir"
        if ! mkdir -p "$output_dir"; then
            log_error "无法创建输出目录：$output_dir"
            log_error "请检查目录权限"
            return 1
        fi
    fi
    
    # 检查写权限
    if [ ! -w "$output_dir" ]; then
        log_error "输出目录不可写：$output_dir"
        log_error "请检查目录权限"
        return 1
    fi
    
    log_debug "✓ 输出目录就绪：$output_dir"
    return 0
}

#-------------------------------------------------------------------------------
# 构建 API 请求体
#-------------------------------------------------------------------------------
build_request_body() {
    local prompt="$1"
    local size="$2"
    local watermark="$3"
    
    # 使用 Python 构建 JSON（避免 shell 转义问题）
    python3 -c "
import json
import sys

body = {
    'model': '$MODEL',
    'prompt': sys.argv[1],
    'sequential_image_generation': 'disabled',
    'response_format': 'url',
    'size': sys.argv[2],
    'stream': False,
    'watermark': sys.argv[3].lower() == 'true'
}

print(json.dumps(body, ensure_ascii=False))
" "$prompt" "$size" "$watermark"
}

#-------------------------------------------------------------------------------
# 调用 API（带重试）
#-------------------------------------------------------------------------------
call_api_with_retry() {
    local body="$1"
    local retry_count="${DEFAULT_RETRY_COUNT}"
    local retry_delay=1
    local attempt=1
    
    while [ $attempt -le $retry_count ]; do
        log_debug "API 调用尝试 $attempt/$retry_count"
        
        # 调用 API
        local response
        local http_code
        
        # 使用临时文件存储响应
        local temp_file
        temp_file=$(mktemp)
        
        http_code=$(curl -s -w "%{http_code}" -o "$temp_file" \
            -X POST "$API_URL" \
            -H "Content-Type: application/json" \
            -H "Authorization: Bearer $ARK_API_KEY" \
            -H "User-Agent: doubao-image-skill/$VERSION" \
            --connect-timeout 10 \
            --max-time "$DEFAULT_TIMEOUT" \
            -d "$body" 2>/dev/null || echo "000")
        
        local response_body
        response_body=$(cat "$temp_file")
        rm -f "$temp_file"
        
        log_debug "HTTP 状态码：$http_code"
        
        # 处理不同状态码
        case "$http_code" in
            200)
                log_debug "✓ API 调用成功"
                echo "$response_body"
                return 0
                ;;
            401)
                log_error "认证失败：API Key 无效或已过期"
                log_error "请重新获取：https://console.volcengine.com/ark"
                return 2
                ;;
            402)
                log_error "账户余额不足，请充值后重试"
                return 2
                ;;
            400)
                log_error "请求被拒绝：${response_body}"
                log_error "可能包含敏感词汇，请修改描述后重试"
                return 2
                ;;
            429)
                # 频率限制，尝试重试
                local retry_after
                retry_after=$(echo "$response_body" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('retry_after', 5))" 2>/dev/null || echo "5")
                log_warn "请求频率超限，等待 ${retry_after}秒后重试..."
                sleep "$retry_after"
                ;;
            500|503|504)
                # 服务器错误，指数退避重试
                log_warn "服务器繁忙（HTTP $http_code），等待 ${retry_delay}秒后重试..."
                sleep "$retry_delay"
                retry_delay=$((retry_delay * 2))
                ;;
            *)
                log_error "未知 HTTP 错误：$http_code"
                log_error "响应：${response_body}"
                return 2
                ;;
        esac
        
        attempt=$((attempt + 1))
    done
    
    log_error "API 调用失败：已达到最大重试次数 ($retry_count)"
    return 2
}

#-------------------------------------------------------------------------------
# 解析 API 响应
#-------------------------------------------------------------------------------
parse_api_response() {
    local response="$1"
    
    # 提取图片 URL
    local image_url
    image_url=$(echo "$response" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    if 'data' in data and len(data['data']) > 0:
        print(data['data'][0].get('url', ''))
    else:
        print('')
except:
    print('')
" 2>/dev/null)
    
    if [ -z "$image_url" ]; then
        log_error "无法从响应中提取图片 URL"
        log_error "原始响应：$response"
        return 1
    fi
    
    echo "$image_url"
    return 0
}

#-------------------------------------------------------------------------------
# 下载图片
#-------------------------------------------------------------------------------
download_image() {
    local image_url="$1"
    local output_dir="$2"
    
    # 生成唯一文件名
    local timestamp
    timestamp=$(date "+%Y%m%d-%H%M%S")
    local random_str
    random_str=$(openssl rand -hex 3 2>/dev/null || echo "$RANDOM$RANDOM")
    local filename="doubao-${timestamp}-${random_str}.png"
    local output_path="${output_dir}/${filename}"
    
    log_info "正在下载图片..."
    log_debug "URL: $image_url"
    log_debug "保存路径：$output_path"
    
    # 下载图片
    if ! curl -sL --connect-timeout 10 --max-time 120 \
        -o "$output_path" \
        -A "doubao-image-skill/$VERSION" \
        "$image_url"; then
        log_error "图片下载失败"
        log_error "URL: $image_url"
        return 3
    fi
    
    # 验证下载结果
    if [ ! -f "$output_path" ]; then
        log_error "下载的文件不存在"
        return 3
    fi
    
    local file_size
    file_size=$(stat -f%z "$output_path" 2>/dev/null || stat -c%s "$output_path" 2>/dev/null || echo "0")
    
    if [ "$file_size" -lt 1024 ]; then
        log_error "下载的文件过小（${file_size} 字节），可能已损坏"
        rm -f "$output_path"
        return 3
    fi
    
    log_info "✓ 图片下载成功"
    log_info "保存位置：$output_path"
    log_info "文件大小：$file_size 字节"
    
    echo "$output_path"
    return 0
}

#-------------------------------------------------------------------------------
# 主函数
#-------------------------------------------------------------------------------
main() {
    # 处理特殊参数
    if [ "${1:-}" = "-h" ] || [ "${1:-}" = "--help" ]; then
        show_help
        exit 0
    fi
    
    if [ "${1:-}" = "-v" ] || [ "${1:-}" = "--version" ]; then
        show_version
        exit 0
    fi
    
    # 解析参数
    local prompt="${1:-}"
    local size="${2:-$DEFAULT_SIZE}"
    local watermark="${3:-$DEFAULT_WATERMARK}"
    local output_dir="${4:-$DEFAULT_OUTPUT_DIR}"
    
    log_info "$(log_timestamp) 开始生成图片..."
    log_info "Prompt: $prompt"
    log_debug "尺寸：$size"
    log_debug "水印：$watermark"
    log_debug "输出目录：$output_dir"
    
    # 环境检查
    if ! check_environment; then
        exit 1
    fi
    
    # 参数验证
    if ! validate_params "$prompt" "$size" "$watermark"; then
        exit 1
    fi
    
    # 确保输出目录存在
    if ! ensure_output_dir "$output_dir"; then
        exit 4
    fi
    
    # 构建请求体
    log_debug "构建 API 请求..."
    local body
    body=$(build_request_body "$prompt" "$size" "$watermark")
    log_debug "请求体：$body"
    
    # 调用 API
    log_info "正在调用 API..."
    local response
    if ! response=$(call_api_with_retry "$body"); then
        exit $?
    fi
    
    # 解析响应
    log_debug "解析 API 响应..."
    local image_url
    if ! image_url=$(parse_api_response "$response"); then
        exit 2
    fi
    
    log_info "✓ API 调用成功"
    log_debug "图片 URL: $image_url"
    
    # 下载图片
    local output_path
    if ! output_path=$(download_image "$image_url" "$output_dir"); then
        exit $?
    fi
    
    # 输出结果
    echo ""
    log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    log_info "图片生成完成！"
    log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    log_info "文件路径：$output_path"
    log_info "Prompt: $prompt"
    log_info "尺寸：$size"
    log_info "水印：$watermark"
    log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    # 输出用于 WorkBuddy 的结果标记
    echo ""
    echo "RESULT_FILE=$output_path"
    
    exit 0
}

# 执行主函数
main "$@"
