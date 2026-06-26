#!/bin/bash
# qwen-portal OAuth 链接获取工具
# 基于 2026-03-09 实战经验总结
# 解决: openclaw models auth login 需要交互式 TTY 的问题

set -e

echo "🔗 qwen-portal OAuth 链接获取工具"
echo "========================================"
echo "版本: 1.0.0 | 基于实战经验 | 2026-03-09"
echo

# 配置
SESSION_NAME="qwen-oauth-$(date +%s)"
OUTPUT_FILE="/tmp/qwen-oauth-$(date +%s).txt"
LOG_FILE="/tmp/qwen-oauth-log-$(date +%Y%m%d).log"
MAX_WAIT_SECONDS=15

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 函数：记录日志
log() {
    local level="$1"
    local message="$2"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    case "$level" in
        "INFO") color=$BLUE ;;
        "SUCCESS") color=$GREEN ;;
        "WARNING") color=$YELLOW ;;
        "ERROR") color=$RED ;;
        *) color=$NC ;;
    esac
    
    echo -e "${color}[$timestamp] [$level] $message${NC}"
    echo "[$timestamp] [$level] $message" >> "$LOG_FILE"
}

# 函数：清理资源
cleanup() {
    log "INFO" "清理资源..."
    
    # 结束 tmux 会话
    if tmux has-session -t "$SESSION_NAME" 2>/dev/null; then
        log "INFO" "结束 tmux 会话: $SESSION_NAME"
        tmux kill-session -t "$SESSION_NAME" 2>/dev/null
    fi
    
    # 清理临时文件
    if [ -f "$OUTPUT_FILE" ]; then
        rm -f "$OUTPUT_FILE"
    fi
}

# 函数：提取 OAuth 链接
extract_oauth_info() {
    local output_file="$1"
    
    log "INFO" "从输出中提取 OAuth 信息..."
    
    # 提取链接
    local link=$(grep -o "https://chat.qwen.ai/authorize[^ ]*" "$output_file" | head -1)
    
    # 提取验证码 (7位大写字母数字)
    local code=$(grep -o "code [A-Z0-9]\{7\}" "$output_file" | cut -d' ' -f2 | head -1)
    
    # 备用提取方法
    if [ -z "$link" ]; then
        link=$(grep -E "(http|https)://" "$output_file" | grep -i "authorize" | head -1 | sed 's/.*\(https[^ ]*\).*/\1/')
    fi
    
    if [ -z "$code" ]; then
        code=$(grep -i "enter the code" "$output_file" | grep -o "[A-Z0-9]\{7\}" | head -1)
    fi
    
    echo "$link|$code"
}

# 函数：验证输出
validate_output() {
    local output_file="$1"
    
    log "INFO" "验证输出内容..."
    
    # 检查是否有错误
    if grep -q "requires an interactive TTY" "$output_file"; then
        log "ERROR" "命令需要交互式 TTY (tmux 应该能解决此问题)"
        return 1
    fi
    
    if grep -q "Error:" "$output_file" | grep -v "Doctor warnings"; then
        log "WARNING" "命令返回错误"
        grep "Error:" "$output_file" | head -2
        return 1
    fi
    
    # 检查是否有预期的输出
    if ! grep -q "chat.qwen.ai" "$output_file"; then
        log "WARNING" "输出中未找到预期的 qwen 链接"
        return 1
    fi
    
    return 0
}

# 主函数
main() {
    log "INFO" "开始获取 qwen-portal OAuth 链接"
    
    # 检查依赖
    if ! command -v tmux &> /dev/null; then
        log "ERROR" "需要 tmux 但未安装。请安装: brew install tmux"
        exit 1
    fi
    
    if ! command -v openclaw &> /dev/null; then
        log "ERROR" "openclaw 命令未找到"
        exit 1
    fi
    
    # 注册清理函数
    trap cleanup EXIT
    
    log "INFO" "创建 tmux 会话: $SESSION_NAME"
    
    # 创建 tmux 会话运行命令
    tmux new-session -d -s "$SESSION_NAME" "openclaw models auth login --provider qwen-portal 2>&1 | tee '$OUTPUT_FILE'"
    
    if [ $? -ne 0 ]; then
        log "ERROR" "创建 tmux 会话失败"
        exit 1
    fi
    
    log "SUCCESS" "tmux 会话创建成功，等待输出..."
    
    # 等待输出
    local waited=0
    while [ $waited -lt $MAX_WAIT_SECONDS ]; do
        if [ -s "$OUTPUT_FILE" ]; then
            log "INFO" "检测到输出内容"
            break
        fi
        sleep 1
        waited=$((waited + 1))
        log "INFO" "等待输出... ($waited/$MAX_WAIT_SECONDS 秒)"
    done
    
    # 捕获输出
    log "INFO" "捕获输出..."
    tmux capture-pane -t "$SESSION_NAME" -p >> "$OUTPUT_FILE" 2>/dev/null
    
    # 验证输出
    if ! validate_output "$OUTPUT_FILE"; then
        log "WARNING" "输出验证失败，显示内容供调试:"
        cat "$OUTPUT_FILE"
        exit 1
    fi
    
    # 提取 OAuth 信息
    local oauth_info=$(extract_oauth_info "$OUTPUT_FILE")
    local link=$(echo "$oauth_info" | cut -d'|' -f1)
    local code=$(echo "$oauth_info" | cut -d'|' -f2)
    
    if [ -z "$link" ] || [ -z "$code" ]; then
        log "ERROR" "无法提取 OAuth 链接或验证码"
        log "INFO" "原始输出:"
        cat "$OUTPUT_FILE"
        exit 1
    fi
    
    # 显示结果
    echo
    echo "🎉 ${GREEN}成功获取 OAuth 信息！${NC}"
    echo "========================================"
    echo
    echo "${BLUE}🔗 OAuth 链接:${NC}"
    echo "   $link"
    echo
    echo "${YELLOW}📱 Device Code:${NC}"
    echo "   $code"
    echo
    echo "${GREEN}📋 操作步骤:${NC}"
    echo "   1. 点击上面的链接"
    echo "   2. 登录你的 qwen 账户"
    echo "   3. 授权应用访问"
    echo "   4. 授权后会自动完成认证"
    echo
    echo "${YELLOW}⚠️  注意:${NC}"
    echo "   • 链接有效时间通常为 15-30 分钟"
    echo "   • 需要在同一浏览器会话中完成"
    echo "   • 授权后，tmux 会话会自动结束"
    echo
    echo "========================================"
    
    log "SUCCESS" "OAuth 链接获取成功"
    log "INFO" "链接: $link"
    log "INFO" "验证码: $code"
    
    # 提供验证命令
    echo
    echo "${BLUE}🔧 验证认证是否成功:${NC}"
    echo "   等待用户完成授权后，运行:"
    echo "   openclaw cron run <新闻任务ID>"
    echo "   检查: openclaw cron runs --id <任务ID>"
    echo
    echo "${GREEN}✅ 完成！${NC}"
}

# 错误处理
handle_error() {
    local line="$1"
    local command="$2"
    
    log "ERROR" "脚本执行出错!"
    log "ERROR" "行号: $line"
    log "ERROR" "命令: $command"
    
    cleanup
    
    exit 1
}

# 设置错误处理
trap 'handle_error $LINENO "$BASH_COMMAND"' ERR

# 显示帮助
show_help() {
    echo "使用: $0 [选项]"
    echo
    echo "选项:"
    echo "  -h, --help     显示此帮助信息"
    echo "  -v, --verbose  详细模式"
    echo "  --test-only    仅测试，不实际运行"
    echo
    echo "示例:"
    echo "  $0             获取 qwen-portal OAuth 链接"
    echo "  $0 --verbose   详细模式获取链接"
    echo
    echo "基于 2026-03-09 qwen-portal OAuth 修复实战经验"
    echo "解决: openclaw models auth login 需要交互式 TTY 的问题"
}

# 解析参数
VERBOSE=false
TEST_ONLY=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        --test-only)
            TEST_ONLY=true
            shift
            ;;
        *)
            echo "未知参数: $1"
            show_help
            exit 1
            ;;
    esac
done

if [ "$TEST_ONLY" = true ]; then
    echo "🔧 测试模式 - 验证环境"
    echo "检查 tmux: $(command -v tmux || echo '未安装')"
    echo "检查 openclaw: $(command -v openclaw || echo '未安装')"
    echo "测试完成"
    exit 0
fi

# 运行主函数
main "$@"

# 记录执行完成
log "INFO" "脚本执行完成"
echo "日志文件: $LOG_FILE"