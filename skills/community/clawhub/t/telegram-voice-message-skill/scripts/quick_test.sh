#!/bin/bash
# ⚡ Telegram语音消息快速测试脚本
# 版本: 1.0.0
# 创建: 2026-03-09
# 作者: 银月 (Silvermoon)

set -e  # 遇到错误立即退出

# ============================================================================
# 配置部分
# ============================================================================

# 测试配置
QUICK_TEST_MESSAGE="快速测试: 功能验证"
MAX_TEST_DURATION=30  # 最大测试时间（秒）

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'  # No Color

# 临时目录
TEMP_DIR="/tmp/telegram_quick_$(date +%s)"
mkdir -p "$TEMP_DIR"

# ============================================================================
# 工具函数
# ============================================================================

# 带颜色的日志函数
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}" >&2
}

log_step() {
    echo -e "${CYAN}➡️  $1${NC}"
}

log_header() {
    echo ""
    echo "=================================================="
    echo "🚀 $1"
    echo "=================================================="
}

# 检查命令是否存在
check_command() {
    if ! command -v "$1" &> /dev/null; then
        log_error "缺少命令: $1"
        return 1
    fi
    return 0
}

# 超时函数
with_timeout() {
    local timeout=$1
    shift
    
    (
        "$@" &
        pid=$!
        
        # 等待超时
        sleep "$timeout"
        
        # 如果进程还在运行，杀掉它
        if kill -0 "$pid" 2>/dev/null; then
            kill "$pid" 2>/dev/null
            log_warning "操作超时（${timeout}秒）"
            return 124  # 超时退出码
        fi
    )
}

# ============================================================================
# 快速测试函数
# ============================================================================

# 快速检查依赖
quick_check_dependencies() {
    log_step "检查依赖工具..."
    
    local essential=("ffmpeg" "curl")
    local optional=("file" "ffprobe")
    
    # 检查必需工具
    for cmd in "${essential[@]}"; do
        if check_command "$cmd"; then
            echo "   ✅ $cmd"
        else
            echo "   ❌ $cmd (必需)"
            return 1
        fi
    done
    
    # 检查可选工具
    for cmd in "${optional[@]}"; do
        if check_command "$cmd"; then
            echo "   ✅ $cmd (可选)"
        else
            echo "   ⚠️  $cmd (可选，未安装)"
        fi
    done
    
    return 0
}

# 快速配置检查
quick_check_config() {
    log_step "检查配置..."
    
    local config_ok=true
    
    # 检查Telegram配置
    if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
        echo "   ❌ TELEGRAM_BOT_TOKEN 未设置"
        config_ok=false
    else
        echo "   ✅ TELEGRAM_BOT_TOKEN 已设置"
    fi
    
    if [ -z "$TELEGRAM_CHAT_ID" ]; then
        echo "   ❌ TELEGRAM_CHAT_ID 未设置"
        config_ok=false
    else
        echo "   ✅ TELEGRAM_CHAT_ID 已设置"
    fi
    
    # 检查TTS配置
    if [ -z "$ALIYUN_TTS_API_KEY" ] && [ -z "$OPENAI_API_KEY" ]; then
        echo "   ⚠️  未配置TTS服务API密钥"
    else
        if [ -n "$ALIYUN_TTS_API_KEY" ]; then
            echo "   ✅ 阿里云TTS 已配置"
        fi
        
        if [ -n "$OPENAI_API_KEY" ]; then
            echo "   ✅ OpenAI TTS 已配置"
        fi
    fi
    
    if [ "$config_ok" = false ]; then
        return 1
    fi
    
    return 0
}

# 快速音频生成测试
quick_tts_test() {
    log_step "测试TTS生成..."
    
    local test_text="测试"
    local output_file="$TEMP_DIR/quick_test.ogg"
    
    # 设置超时
    if with_timeout 15 ./scripts/tts_generator.sh "$test_text" > "$output_file" 2>"$TEMP_DIR/tts_error.log"; then
        if [ -s "$output_file" ]; then
            local file_size=$(stat -c%s "$output_file" 2>/dev/null || echo "unknown")
            echo "   ✅ 生成成功 (大小: $file_size 字节)"
            return 0
        else
            echo "   ❌ 生成的文件为空"
            return 1
        fi
    else
        echo "   ❌ 生成失败"
        if [ -f "$TEMP_DIR/tts_error.log" ]; then
            echo "   错误信息:"
            tail -5 "$TEMP_DIR/tts_error.log" | sed 's/^/      /'
        fi
        return 1
    fi
}

# 快速格式转换测试
quick_conversion_test() {
    log_step "测试格式转换..."
    
    # 创建测试WAV文件
    local test_wav="$TEMP_DIR/test_audio.wav"
    
    echo "   创建测试音频..."
    ffmpeg -f lavfi -i "sine=frequency=440:duration=1" \
        -acodec pcm_s16le "$test_wav" \
        -y 2>/dev/null || {
        echo "   ❌ 创建测试音频失败"
        return 1
    }
    
    # 测试转换
    local test_ogg="$TEMP_DIR/converted.ogg"
    
    if with_timeout 10 ./scripts/audio_converter.sh \
        --input "$test_wav" \
        --output "$test_ogg" 2>"$TEMP_DIR/convert_error.log"; then
        
        if [ -f "$test_ogg" ] && [ -s "$test_ogg" ]; then
            echo "   ✅ 转换成功"
            return 0
        else
            echo "   ❌ 转换输出文件无效"
            return 1
        fi
    else
        echo "   ❌ 转换失败"
        return 1
    fi
}

# 快速发送测试（模拟）
quick_send_test() {
    log_step "测试发送功能..."
    
    # 创建一个测试音频文件
    local test_file="$TEMP_DIR/send_test.ogg"
    
    echo "   创建测试文件..."
    ffmpeg -f lavfi -i "sine=frequency=880:duration=1" \
        -acodec libopus "$test_file" \
        -y 2>/dev/null || {
        echo "   ❌ 创建测试文件失败"
        return 1
    }
    
    # 测试发送脚本（不实际发送）
    echo "   测试发送脚本..."
    
    if ./scripts/telegram_sender.sh --dry-run "$test_file" 2>"$TEMP_DIR/send_error.log"; then
        echo "   ✅ 发送功能正常"
        return 0
    else
        echo "   ❌ 发送功能测试失败"
        if [ -f "$TEMP_DIR/send_error.log" ]; then
            echo "   错误信息:"
            tail -5 "$TEMP_DIR/send_error.log" | sed 's/^/      /'
        fi
        return 1
    fi
}

# 快速完整流程测试
quick_full_test() {
    log_step "测试完整流程..."
    
    local test_text="完整流程测试"
    local start_time=$(date +%s)
    
    echo "   1. 生成音频..."
    local audio_file
    if ! audio_file=$(./scripts/tts_generator.sh "$test_text" 2>"$TEMP_DIR/full_tts_error.log"); then
        echo "   ❌ TTS生成失败"
        return 1
    fi
    
    echo "   2. 验证格式..."
    if ! ./scripts/audio_converter.sh --input "$audio_file" \
        --output "$TEMP_DIR/full_verified.ogg" 2>"$TEMP_DIR/full_convert_error.log"; then
        echo "   ❌ 格式验证失败"
        return 1
    fi
    
    echo "   3. 测试发送..."
    if ! ./scripts/telegram_sender.sh --dry-run "$TEMP_DIR/full_verified.ogg" 2>"$TEMP_DIR/full_send_error.log"; then
        echo "   ❌ 发送测试失败"
        return 1
    fi
    
    local end_time=$(date +%s)
    local duration=$((end_time - start_time))
    
    echo "   ✅ 完整流程测试通过 (耗时: ${duration}秒)"
    return 0
}

# ============================================================================
# 主测试函数
# ============================================================================

run_quick_test() {
    log_header "Telegram语音消息快速测试"
    
    echo "⏱️  最大测试时间: ${MAX_TEST_DURATION}秒"
    echo ""
    
    local tests=(
        "quick_check_dependencies"
        "quick_check_config"
        "quick_tts_test"
        "quick_conversion_test"
        "quick_send_test"
        "quick_full_test"
    )
    
    local passed=0
    local failed=0
    local skipped=0
    
    for test_func in "${tests[@]}"; do
        echo ""
        
        # 检查是否超时
        local current_time=$(date +%s)
        local test_start_time=$(date +%s)
        
        log_step "运行: $test_func"
        
        # 运行测试
        if $test_func; then
            echo "   ✅ 通过"
            ((passed++))
        else
            echo "   ❌ 失败"
            ((failed++))
            
            # 如果依赖检查失败，跳过后续测试
            if [ "$test_func" = "quick_check_dependencies" ] && [ $failed -gt 0 ]; then
                log_warning "依赖检查失败，跳过后续测试"
                skipped=$(( ${#tests[@]} - 1 ))
                break
            fi
        fi
        
        # 检查总时间
        local test_end_time=$(date +%s)
        local total_duration=$((test_end_time - current_time))
        
        if [ $total_duration -ge $MAX_TEST_DURATION ]; then
            log_warning "达到最大测试时间，停止测试"
            skipped=$(( ${#tests[@]} - passed - failed ))
            break
        fi
    done
    
    # 显示结果
    echo ""
    echo "=================================================="
    echo "📊 测试结果汇总"
    echo "=================================================="
    
    echo ""
    echo "📈 统计:"
    echo "   通过: $passed"
    echo "   失败: $failed"
    echo "   跳过: $skipped"
    echo "   总计: ${#tests[@]}"
    
    echo ""
    
    if [ $failed -eq 0 ]; then
        if [ $skipped -eq 0 ]; then
            log_success "🎉 所有测试通过！"
            echo ""
            echo "✅ 技能功能完整"
            echo "✅ 配置正确"
            echo "✅ 可以正常使用"
        else
            log_warning "⚠️  部分测试跳过"
            echo ""
            echo "✅ 基础功能正常"
            echo "⚠️  部分测试未完成"
            echo "💡 建议运行完整测试"
        fi
    else
        log_error "❌ 有 $failed 个测试失败"
        echo ""
        echo "⚠️  请检查失败原因："
        echo "   1. 查看详细错误信息"
        echo "   2. 修复问题"
        echo "   3. 重新运行测试"
        
        # 显示失败建议
        if [ $failed -gt 0 ]; then
            echo ""
            echo "🔧 修复建议："
            
            if grep -q "ffmpeg" "$TEMP_DIR/tts_error.log" 2>/dev/null; then
                echo "   • 安装ffmpeg: sudo apt-get install ffmpeg"
            fi
            
            if grep -q "curl" "$TEMP_DIR/tts_error.log" 2>/dev/null; then
                echo "   • 安装curl: sudo apt-get install curl"
            fi
            
            if grep -q "TELEGRAM_BOT_TOKEN" "$TEMP_DIR/send_error.log" 2>/dev/null; then
                echo "   • 设置Telegram Bot Token: export TELEGRAM_BOT_TOKEN=\"your_token\""
            fi
        fi
    fi
    
    echo ""
    echo "⏱️  总耗时: $(( $(date +%s) - current_time ))秒"
    
    return $failed
}

# ============================================================================
# 清理函数
# ============================================================================

cleanup() {
    log_info "清理临时文件..."
    
    if [ -d "$TEMP_DIR" ]; then
        rm -rf "$TEMP_DIR" 2>/dev/null || true
    fi
    
    # 清理旧的测试文件
    find /tmp -name "telegram_quick_*" -type d -mmin +30 2>/dev/null | \
        xargs rm -rf 2>/dev/null || true
    
    log_success "清理完成"
}

# ============================================================================
# 主函数
# ============================================================================

main() {
    # 检查当前目录
    if [ ! -d "./scripts" ]; then
        log_error "请在技能根目录运行此脚本"
        echo ""
        echo "💡 使用方法:"
        echo "   cd /path/to/telegram-voice-message-skill"
        echo "   ./scripts/quick_test.sh"
        exit 1
    fi
    
    # 运行快速测试
    if run_quick_test; then
        echo ""
        log_success "🚀 快速测试完成！"
        echo ""
        echo "📋 下一步："
        echo "   ✅ 基础功能验证通过"
        echo "   💡 可以开始使用技能"
        echo ""
        echo "💡 使用示例："
        echo "   ./scripts/tts_generator.sh \"你的消息\""
        echo "   ./scripts/telegram_sender.sh audio.ogg"
    else
        echo ""
        log_error "⚠️  快速测试失败"
        echo ""
        echo "🔧 需要修复的问题："
        echo "   1. 检查配置是否正确"
        echo "   2. 确保依赖工具已安装"
        echo "   3. 查看详细错误信息"
        echo ""
        echo "📋 详细错误日志："
        if [ -f "$TEMP_DIR/tts_error.log" ] && [ -s "$TEMP_DIR/tts_error.log" ]; then
            echo "   TTS错误: $TEMP_DIR/tts_error.log"
        fi
        
        if [ -f "$TEMP_DIR/convert_error.log" ] && [ -s "$TEMP_DIR/convert_error.log" ]; then
            echo "   转换错误: $TEMP_DIR/convert_error.log"
        fi
        
        if [ -f "$TEMP_DIR/send_error.log" ] && [ -s "$TEMP_DIR/send_error.log" ]; then
            echo "   发送错误: $TEMP_DIR/send_error.log"
        fi
        
        exit 1
    fi
}

# ============================================================================
# 脚本执行
# ============================================================================

# 设置退出时清理
trap cleanup EXIT

# 运行主函数
main "$@"

# ============================================================================
# 使用说明：
# ============================================================================
# 1. 基本使用：
#    ./scripts/quick_test.sh
#
# 2. 设置环境变量（可选）：
#    export TELEGRAM_BOT_TOKEN="your_token"
#    export TELEGRAM_CHAT_ID="your_chat_id"
#
# 3. 测试内容：
#    - 依赖工具检查
#    - 配置验证
#    - TTS生成测试
#    - 格式转换测试
#    - 发送功能测试
#    - 完整流程测试
#
# 4. 预期结果：
#    - 所有测试通过：技能功能正常
#    - 有测试失败：根据提示修复问题
# 5. 快速修复建议：
#    # 安装必需工具
#    sudo apt-get install ffmpeg curl
#
#    # 设置配置
#    export TELEGRAM_BOT_TOKEN="your_token"
#    export TELEGRAM_CHAT_ID="your_chat_id"
# ============================================================================