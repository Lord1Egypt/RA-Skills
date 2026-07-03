#!/bin/bash

# ============================================================
# Language Detection
# ============================================================
if [[ "${LANG:-}" == zh_* ]] || [[ "${LC_ALL:-}" == zh_* ]] || [[ "${LANGUAGE:-}" == zh_* ]]; then
    SCRIPT_LANG="zh"
else
    SCRIPT_LANG="en"
fi

LANG_ZH() { [[ "$SCRIPT_LANG" == "zh" ]] && echo "$1" || echo "$2"; }

# StatTransfer 检测与配置脚本
# 支持平台: Windows, macOS, Linux

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检测平台
detect_platform() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        LANG_ZH "linux" "linux"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        LANG_ZH "macos" "macos"
    elif [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
        LANG_ZH "windows" "windows"
    else
        LANG_ZH "unknown" "unknown"
    fi
}

# 检测 StatTransfer
detect_stattransfer() {
    local platform=$1
    local st_path=""
    
    log_info "检测 StatTransfer..."
    
    # 首先检查 PATH
    if command -v st &> /dev/null; then
        st_path=$(command -v st)
        log_info "在 PATH 中找到 StatTransfer: $st_path"
        LANG_ZH "$st_path" "$st_path"
        return 0
    fi
    
    # 平台特定路径
    if [[ "$platform" == "windows" ]]; then
        local win_paths=(
            "C:/Program Files/StatTransfer/st.exe"
            "C:/Program Files (x86)/StatTransfer/st.exe"
        )
        
        for path in "${win_paths[@]}"; do
            if [[ -f "$path" ]]; then
                st_path="$path"
                log_info "找到 StatTransfer: $st_path"
                LANG_ZH "$st_path" "$st_path"
                return 0
            fi
        done
    elif [[ "$platform" == "macos" ]]; then
        local mac_paths=(
            "/Applications/StatTransfer/st"
            "/usr/local/bin/st"
        )
        
        for path in "${mac_paths[@]}"; do
            if [[ -f "$path" ]]; then
                st_path="$path"
                log_info "找到 StatTransfer: $st_path"
                LANG_ZH "$st_path" "$st_path"
                return 0
            fi
        done
    elif [[ "$platform" == "linux" ]]; then
        local linux_paths=(
            "/usr/local/bin/st"
            "/opt/stattransfer/st"
        )
        
        for path in "${linux_paths[@]}"; do
            if [[ -f "$path" ]]; then
                st_path="$path"
                log_info "找到 StatTransfer: $st_path"
                LANG_ZH "$st_path" "$st_path"
                return 0
            fi
        done
    fi
    
    log_warn "未找到 StatTransfer"
    LANG_ZH "" ""
    return 1
}

# 验证 StatTransfer
verify_stattransfer() {
    local st_path=$1
    
    log_info "验证 StatTransfer..."
    
    if [[ -z "$st_path" ]]; then
        log_error "StatTransfer 路径为空"
        return 1
    fi
    
    # 检查可执行文件
    if [[ ! -f "$st_path" ]] && [[ ! -f "$st_path.exe" ]]; then
        log_error "StatTransfer 可执行文件不存在: $st_path"
        return 1
    fi
    
    # 运行版本命令
    local version_output
    if [[ "$st_path" == *.exe ]]; then
        version_output=$("$st_path" --version 2>&1 || true)
    else
        version_output=$("$st_path" --version 2>&1 || true)
    fi
    
    if [[ -n "$version_output" ]]; then
        log_info "StatTransfer 版本信息: $version_output"
    else
        log_warn "无法获取 StatTransfer 版本信息"
    fi
    
    log_info "StatTransfer 验证成功"
    return 0
}

# 配置 StatTransfer
configure_stattransfer() {
    local st_path=$1
    local platform=$2
    local config_file="$HOME/.workbuddy/skills/statsoft-cli/config.json"
    
    log_info "配置 StatTransfer..."
    
    # 创建配置目录
    mkdir -p "$(dirname "$config_file")"
    
    # 读取现有配置
    local config="{}"
    if [[ -f "$config_file" ]]; then
        config=$(cat "$config_file")
    fi
    
    # 更新配置（使用 Python 进行 JSON 操作）
    CONFIG_FILE="$config_file"
    ST_PATH="$st_path"
    PLATFORM="$platform"
    local new_config=$(python3 -c "
import json
import sys

config_file = sys.argv[1]
st_path = sys.argv[2]
platform = sys.argv[3]

try:
    with open(config_file, 'r') as f:
        config = json.load(f)
except:
    config = {}

if 'StatTransfer' not in config:
    config['StatTransfer'] = {}

config['StatTransfer']['installed'] = True
config['StatTransfer']['path'] = st_path
config['StatTransfer']['platform'] = platform
config['StatTransfer']['version'] = 'Unknown'

with open(config_file, 'w') as f:
    json.dump(config, f, indent=2)

print('config.json updated.')
" "$CONFIG_FILE" "$ST_PATH" "$PLATFORM" 2>/dev/null || echo "$config")
    
    # 保存配置
    LANG_ZH "$new_config" "$new_config"
    
    log_info "StatTransfer 配置已保存到: $config_file"
    return 0
}

# 主函数
main() {
    log_info "开始 StatTransfer 检测与配置..."
    
    # 检测平台
    local platform=$(detect_platform)
    log_info "检测到平台: $platform"
    
    if [[ "$platform" == "unknown" ]]; then
        log_error "不支持的平台"
        exit 1
    fi
    
    # 检测 StatTransfer
    local st_path=$(detect_stattransfer "$platform")
    
    if [[ -z "$st_path" ]]; then
        log_warn "未找到 StatTransfer，请手动指定路径"
        
        # 提示用户输入路径
        LANG_ZH "请输入 StatTransfer 安装路径（按 Enter 跳过）: " "请输入 StatTransfer 安装路径（按 Enter 跳过）: "
        read -r user_path
        
        if [[ -n "$user_path" ]]; then
            st_path="$user_path"
        else
            log_error "未配置 StatTransfer"
            exit 1
        fi
    fi
    
    # 验证 StatTransfer
    if ! verify_stattransfer "$st_path"; then
        log_error "StatTransfer 验证失败"
        exit 1
    fi
    
    # 配置 StatTransfer
    if ! configure_stattransfer "$st_path" "$platform"; then
        log_error "StatTransfer 配置失败"
        exit 1
    fi
    
    log_info "✅ StatTransfer 配置完成！"
    log_info ""
    log_info "⚠️ 配置完成提示:"
    log_info "  - ✅ Stat/Transfer 是纯 CLI 工具，完全无 GUI，适合自动化"
    log_info "  - ⚠️ 转换前请确认目标格式支持所需的数据类型"
    log_info "  - 💡 在 AI 工作流中的角色：数据格式转换桥梁"
    log_info ""
    log_info "📋 推荐使用方式:"
    log_info "  # 单文件转换"
    log_info "  \"$st_path\" in.sas7bdat out.dta"
    log_info ""
    log_info "  # 批量转换"
    log_info "  \"$st_path\" in\\*.sav out\\*.dta"
    
    return 0
}

# 运行主函数
main "$@"
