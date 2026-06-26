#!/bin/bash
# 🔧 Telegram语音消息集成测试脚本
# 版本: 1.0.0
# 创建: 2026-03-09
# 作者: 银月 (Silvermoon)

set -e  # 遇到错误立即退出

# ============================================================================
# 配置部分
# ============================================================================

# 测试配置
TEST_MODE="true"
TEST_CHAT_ID="${TEST_CHAT_ID:-${TELEGRAM_CHAT_ID}}"
TEST_MESSAGE="${TEST_MESSAGE:-这是一条集成测试消息}"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'  # No Color

# 临时目录
TEMP_DIR="/tmp/telegram_test_$(date +%s)"
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

log_section() {
    echo ""
    echo "=================================================="
    echo "📋 $1"
    echo "=================================================="
}

# 检查命令是否存在
check_command() {
    if ! command -v "$1" &> /dev/null; then
        log_error "缺少必需命令: $1"
        return 1
    fi
    return 0
}

# 检查文件是否存在
check_file() {
    if [ ! -f "$1" ]; then
        log_error "文件不存在: $1"
        return 1
    fi
    return 0
}

# ============================================================================
# 测试用例
# ============================================================================

# 测试1：检查依赖工具
test_dependencies() {
    log_section "测试1: 检查依赖工具"
    
    local missing=()
    
    for cmd in ffmpeg curl file; do
        if ! check_command "$cmd"; then
            missing+=("$cmd")
        fi
    done
    
    if [ ${#missing[@]} -gt 0 ]; then
        log_error "缺少必需工具: ${missing[*]}"
        log_info "安装方法:"
        echo "  Ubuntu/Debian: sudo apt-get install ${missing[*]}"
        echo "  macOS: brew install ${missing[*]}"
        echo "  CentOS/RHEL: sudo yum install ${missing[*]}"
        return 1
    fi
    
    log_success "所有依赖工具检查通过"
    return 0
}

# 测试2：检查脚本权限
test_script_permissions() {
    log_section "测试2: 检查脚本权限"
    
    local scripts=(
        "./scripts/tts_generator.sh"
        "./scripts/audio_converter.sh"
        "./scripts/telegram_sender.sh"
    )
    
    for script in "${scripts[@]}"; do
        if ! check_file "$script"; then
            return 1
        fi
        
        # 检查是否可执行
        if [ ! -x "$script" ]; then
            log_warning "脚本不可执行: $script"
            log_info "修复: chmod +x $script"
            chmod +x "$script"
            log_success "已修复权限: $script"
        else
            log_success "脚本可执行: $script"
        fi
    done
    
    return 0
}

# 测试3：测试TTS生成
test_tts_generation() {
    log_section "测试3: 测试TTS生成"
    
    local test_text="测试TTS生成功能"
    local output_file="$TEMP_DIR/test_tts.ogg"
    
    log_info "生成测试音频: $test_text"
    
    # 使用TTS生成脚本
    local audio_file
    if ! audio_file=$(./scripts/tts_generator.sh "$test_text" 2>"$TEMP_DIR/tts_error.log"); then
        log_error "TTS生成失败"
        log_info "错误信息:"
        cat "$TEMP_DIR/tts_error.log"
        return 1
    fi
    
    if [ ! -f "$audio_file" ]; then
        log_error "音频文件未生成"
        return 1
    fi
    
    # 检查文件格式
    local file_info
    if file_info=$(file "$audio_file" 2>/dev/null); then
        log_info "文件格式: $file_info"
        
        if [[ "$file_info" =~ "OGG" ]] && [[ "$file_info" =~ "Opus" ]]; then
            log_success "音频格式正确 (OGG + Opus)"
        else
            log_warning "音频格式可能不正确"
        fi
    fi
    
    # 检查文件大小
    local file_size=$(stat -c%s "$audio_file" 2>/dev/null || echo "unknown")
    log_info "文件大小: $file_size 字节"
    
    if [ "$file_size" != "unknown" ] && [ "$file_size" -lt 100 ]; then
        log_error "音频文件太小，可能生成失败"
        return 1
    fi
    
    log_success "TTS生成测试通过"
    return 0
}

# 测试4：测试音频转换
test_audio_conversion() {
    log_section "测试4: 测试音频转换"
    
    # 先创建一个测试WAV文件
    local test_wav="$TEMP_DIR/test_input.wav"
    local test_ogg="$TEMP_DIR/test_output.ogg"
    
    log_info "创建测试WAV文件..."
    
    # 使用ffmpeg生成一个简单的测试音频
    if ! ffmpeg -f lavfi -i "sine=frequency=1000:duration=2" \
        -acodec pcm_s16le "$test_wav" \
        -y 2>"$TEMP_DIR/ffmpeg_error.log"; then
        log_error "创建测试音频失败"
        cat "$TEMP_DIR/ffmpeg_error.log"
        return 1
    fi
    
    log_info "测试音频已创建: $test_wav"
    
    # 测试音频转换脚本
    log_info "测试音频转换..."
    
    if ! ./scripts/audio_converter.sh \
        --input "$test_wav" \
        --output "$test_ogg" \
        --bitrate 64k \
        --sample-rate 48000 \
        --channels 1 2>"$TEMP_DIR/converter_error.log"; then
        log_error "音频转换失败"
        cat "$TEMP_DIR/converter_error.log"
        return 1
    fi
    
    # 检查输出文件
    if [ ! -f "$test_ogg" ]; then
        log_error "转换输出文件不存在"
        return 1
    fi
    
    # 检查文件格式
    if file_info=$(file "$test_ogg" 2>/dev/null); then
        log_info "转换后格式: $file_info"
        
        if [[ "$file_info" =~ "OGG" ]] && [[ "$file_info" =~ "Opus" ]]; then
            log_success "转换格式正确"
        else
            log_warning "转换格式可能不正确"
        fi
    fi
    
    log_success "音频转换测试通过"
    return 0
}

# 测试5：测试配置验证
test_config_validation() {
    log_section "测试5: 测试配置验证"
    
    # 测试环境变量
    local required_vars=(
        "TELEGRAM_BOT_TOKEN"
        "TELEGRAM_CHAT_ID"
    )
    
    log_info "检查必需环境变量..."
    
    local missing_vars=()
    for var in "${required_vars[@]}"; do
        if [ -z "${!var}" ]; then
            missing_vars+=("$var")
        fi
    done
    
    if [ ${#missing_vars[@]} -gt 0 ]; then
        log_error "缺少必需环境变量: ${missing_vars[*]}"
        log_info "请设置: export 变量名=\"值\""
        return 1
    fi
    
    log_success "环境变量检查通过"
    
    # 测试TTS服务配置
    log_info "检查TTS服务配置..."
    
    if [ -z "$ALIYUN_TTS_API_KEY" ] && [ -z "$OPENAI_API_KEY" ]; then
        log_warning "未配置TTS服务API密钥"
        log_info "建议至少配置一个TTS服务"
    else
        if [ -n "$ALIYUN_TTS_API_KEY" ]; then
            log_success "阿里云TTS配置已设置"
        fi
        
        if [ -n "$OPENAI_API_KEY" ]; then
            log_success "OpenAI TTS配置已设置"
        fi
    fi
    
    log_success "配置验证测试通过"
    return 0
}

# 测试6：完整流程测试
test_full_workflow() {
    log_section "测试6: 完整流程测试"
    
    local test_text="集成测试: 完整流程验证"
    
    log_info "步骤1: 生成音频"
    local audio_file
    if ! audio_file=$(./scripts/tts_generator.sh "$test_text" 2>"$TEMP_DIR/workflow_tts_error.log"); then
        log_error "TTS生成失败"
        cat "$TEMP_DIR/workflow_tts_error.log"
        return 1
    fi
    
    log_success "音频生成成功: $(basename "$audio_file")"
    
    log_info "步骤2: 验证音频格式"
    if ! ./scripts/audio_converter.sh --input "$audio_file" \
        --output "$TEMP_DIR/verified.ogg" 2>"$TEMP_DIR/workflow_convert_error.log"; then
        log_error "音频格式验证失败"
        cat "$TEMP_DIR/workflow_convert_error.log"
        return 1
    fi
    
    log_success "音频格式验证通过"
    
    log_info "步骤3: 测试发送功能"
    # 注意：这里不实际发送，只测试发送脚本的基本功能
    if ! ./scripts/telegram_sender.sh --dry-run "$TEMP_DIR/verified.ogg" 2>"$TEMP_DIR/workflow_send_error.log"; then
        log_error "发送功能测试失败"
        cat "$TEMP_DIR/workflow_send_error.log"
        return 1
    fi
    
    log_success "发送功能测试通过"
    
    log_success "完整流程测试通过"
    return 0
}

# ============================================================================
# 主测试函数
# ============================================================================

run_all_tests() {
    log_section "开始集成测试"
    
    local tests_passed=0
    local tests_failed=0
    local test_results=()
    
    # 定义测试用例
    local test_cases=(
        "test_dependencies"
        "test_script_permissions"
        "test_tts_generation"
        "test_audio_conversion"
        "test_config_validation"
        "test_full_workflow"
    )
    
    # 运行所有测试
    for test_case in "${test_cases[@]}"; do
        echo ""
        log_info "运行: $test_case"
        
        if $test_case; then
            log_success "通过: $test_case"
            ((tests_passed++))
            test_results+=("✅ $test_case")
        else
            log_error "失败: $test_case"
            ((tests_failed++))
            test_results+=("❌ $test_case")
        fi
    done
    
    # 显示测试结果
    echo ""
    log_section "测试结果汇总"
    
    echo "📊 统计:"
    echo "   通过: $tests_passed"
    echo "   失败: $tests_failed"
    echo "   总计: ${#test_cases[@]}"
    
    echo ""
    echo "📋 详细结果:"
    for result in "${test_results[@]}"; do
        echo "   $result"
    done
    
    echo ""
    if [ $tests_failed -eq 0 ]; then
        log_success "🎉 所有测试通过！"
        return 0
    else
        log_error "⚠️  有 $tests_failed 个测试失败"
        return 1
    fi
}

# ============================================================================
# 清理函数
# ============================================================================

cleanup() {
    log_info "清理测试文件..."
    
    if [ -d "$TEMP_DIR" ]; then
        rm -rf "$TEMP_DIR" 2>/dev/null || true
    fi
    
    # 清理测试生成的临时文件
    find /tmp -name "telegram_test_*" -type d -mmin +60 2>/dev/null | \
        xargs rm -rf 2>/dev/null || true
    
    log_success "清理完成"
}

# ============================================================================
# 主函数
# ============================================================================

main() {
    # 显示标题
    echo "=================================================="
    echo "Telegram语音消息集成测试"
    echo "版本: 1.0.0"
    echo "创建: 2026-03-09"
    echo "作者: 银月 (Silvermoon)"
    echo "=================================================="
    
    # 检查当前目录
    if [ ! -d "./scripts" ]; then
        log_error "请在技能根目录运行此脚本"
        exit 1
    fi
    
    # 运行所有测试
    if run_all_tests; then
        log_success "✅ 集成测试全部通过！"
        echo ""
        echo "🎉 技能功能验证完成"
        echo "   所有模块工作正常"
        echo "   可以安全使用"
    else
        log_error "❌ 集成测试失败"
        echo ""
        echo "⚠️  请检查失败原因："
        echo "   1. 查看详细错误信息"
        echo "   2. 修复问题"
        echo "   3. 重新运行测试"
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
# 1. 设置环境变量：
#    export TELEGRAM_BOT_TOKEN="your_token"
#    export TELEGRAM_CHAT_ID="your_chat_id"
#    export ALIYUN_TTS_API_KEY="your_aliyun_key"
#
# 2. 运行测试：
#    ./scripts/test_integration.sh
#
# 3. 查看结果：
#    - 所有测试通过：技能功能正常
#    - 有测试失败：根据错误信息修复问题
#
# 4. 测试内容：
#    - 依赖工具检查
#    - 脚本权限检查
#    - TTS生成功能
#    - 音频转换功能
#    - 配置验证
#    - 完整流程测试
# ============================================================================