#!/bin/bash

# YiDun Defense - Setup Script
# 易盾加固工具初始化和下载脚本

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 配置
YIDUN_DIR="$HOME/.yidun-defense"
TOOL_URL="https://clienttool.dun.163.com/api/v1/client/jarTool/download"
TOOL_ZIP="$YIDUN_DIR/yidun-tool.zip"
TOOL_JAR="$YIDUN_DIR/NHPProtect.jar"
CONFIG_FILE="$YIDUN_DIR/config.ini"

# 参数
FORCE_REINSTALL=false

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

# 检查 Java 环境
check_java() {
    log_info "检查 Java 环境..."

    if ! command -v java &> /dev/null; then
        log_error "未检测到 Java 环境！"
        log_info "请安装 Java Runtime Environment (JRE) 8 或更高版本"
        log_info "macOS: brew install openjdk@11"
        log_info "Ubuntu: sudo apt install openjdk-11-jre"
        exit 1
    fi

    # 检测 Java 版本（兼容 Java 8 的 "1.8.x" 和 Java 9+ 的 "9.x" 格式）
    java_version_str=$(java -version 2>&1 | head -n 1 | cut -d'"' -f2)
    major=$(echo "$java_version_str" | cut -d'.' -f1)
    minor=$(echo "$java_version_str" | cut -d'.' -f2)

    # Java 8 及以前版本使用 "1.x.y" 格式，major=1，minor 是实际大版本号
    # Java 9+ 使用 "x.y.z" 格式，major 是实际大版本号
    if [ "$major" -eq 1 ]; then
        java_version="$minor"
    else
        java_version="$major"
    fi

    if [ "$java_version" -lt 8 ]; then
        log_error "Java 版本过低！需要 JRE 8 或更高版本"
        exit 1
    fi

    log_success "Java 环境检查通过 (version: $(java -version 2>&1 | head -n 1))"
}

# 创建工作目录
setup_directory() {
    log_info "创建工作目录..."

    if [ ! -d "$YIDUN_DIR" ]; then
        mkdir -p "$YIDUN_DIR"
        log_success "工作目录创建成功: $YIDUN_DIR"
    else
        log_info "工作目录已存在: $YIDUN_DIR"
    fi
}

# 下载加固工具
download_tool() {
    # 检查工具是否已存在
    if [ -f "$TOOL_JAR" ] && [ "$FORCE_REINSTALL" = false ]; then
        log_warning "工具已存在，跳过下载"
        log_info "已安装: $TOOL_JAR"
        log_info "如需重新下载，请使用: $0 --force"
        return 0
    fi

    log_info "开始下载易盾加固工具..."

    # 如果是强制重装，先删除旧文件
    if [ "$FORCE_REINSTALL" = true ]; then
        log_info "强制重新安装，删除旧文件..."
        rm -f "$TOOL_JAR"
        rm -rf "$YIDUN_DIR/YiDunPackTool2-"*
        rm -rf "$YIDUN_DIR/tool"
        rm -rf "$YIDUN_DIR/ProtectBin"
    fi

    # 尝试使用 curl 下载
    if command -v curl &> /dev/null; then
        log_info "使用 curl 下载..."
        if curl -L -o "$TOOL_ZIP" "$TOOL_URL"; then
            log_success "工具下载成功！"

            # TODO: 校验文件完整性
            # 待官方提供 SHA256 哈希后启用：
            # EXPECTED_SHA256="官方公布的哈希值"
            # actual_sha=$(shasum -a 256 "$TOOL_ZIP" | cut -d' ' -f1)
            # if [ "$actual_sha" != "$EXPECTED_SHA256" ]; then
            #     log_error "工具包完整性校验失败！文件可能已被篡改"
            #     log_error "预期: $EXPECTED_SHA256"
            #     log_error "实际: $actual_sha"
            #     rm -f "$TOOL_ZIP"
            #     exit 1
            # fi
            # log_success "完整性校验通过"

            return 0
        else
            log_error "使用 curl 下载失败"
            rm -f "$TOOL_ZIP"
        fi
    fi

    # 尝试使用 wget 下载
    if command -v wget &> /dev/null; then
        log_info "使用 wget 下载..."
        if wget -O "$TOOL_ZIP" "$TOOL_URL"; then
            log_success "工具下载成功！"
            return 0
        else
            log_error "使用 wget 下载失败"
            rm -f "$TOOL_ZIP"
        fi
    fi

    log_error "下载失败！请检查网络连接或手动下载"
    log_info "下载地址: $TOOL_URL"
    log_info "保存路径: $TOOL_ZIP"
    exit 1
}

# 解压工具包
extract_tool() {
    log_info "解压工具包..."

    if [ ! -f "$TOOL_ZIP" ]; then
        log_error "工具包不存在: $TOOL_ZIP"
        exit 1
    fi

    # 检查 unzip 命令
    if ! command -v unzip &> /dev/null; then
        log_error "未找到 unzip 命令，请先安装"
        log_info "macOS: brew install unzip"
        log_info "Ubuntu: sudo apt install unzip"
        exit 1
    fi

    # 检查 zip 文件路径安全性（防止 Zip Slip 攻击）
    log_info "验证压缩包安全性..."
    if unzip -l "$TOOL_ZIP" | grep -q '\.\./'; then
        log_error "检测到恶意压缩包：包含目录遍历路径"
        rm -f "$TOOL_ZIP"
        exit 1
    fi

    # 解压到工作目录
    if unzip -q -o "$TOOL_ZIP" -d "$YIDUN_DIR"; then
        log_success "工具包解压成功！"

        # 删除 zip 文件
        rm -f "$TOOL_ZIP"

        # 查找并移动 NHPProtect.jar
        if [ ! -f "$TOOL_JAR" ]; then
            # 可能在子目录中，尝试移动
            jar_file=$(find "$YIDUN_DIR" -name "NHPProtect.jar" -type f | head -n 1)
            if [ -n "$jar_file" ]; then
                cp "$jar_file" "$TOOL_JAR"
                log_success "找到核心工具: NHPProtect.jar"
            else
                log_error "未找到 NHPProtect.jar"
                exit 1
            fi
        fi

        # 复制 tool 目录（包含 aapt 等工具）
        tool_dir=$(find "$YIDUN_DIR" -type d -name "tool" | head -n 1)
        if [ -n "$tool_dir" ] && [ -d "$tool_dir" ]; then
            if [ ! -d "$YIDUN_DIR/tool" ]; then
                cp -r "$tool_dir" "$YIDUN_DIR/"
                log_success "工具目录复制成功"
            fi
        else
            log_warning "未找到 tool 目录，可能影响加固功能"
        fi

        return 0
    else
        log_error "解压失败"
        exit 1
    fi
}

# 验证工具完整性

# 验证工具完整性
verify_tool() {
    log_info "验证工具完整性..."

    if [ ! -f "$TOOL_JAR" ]; then
        log_error "工具文件不存在: $TOOL_JAR"
        exit 1
    fi

    # 检查文件大小（jar 文件应该大于 100KB）
    file_size=$(stat -f%z "$TOOL_JAR" 2>/dev/null || stat -c%s "$TOOL_JAR" 2>/dev/null)
    if [ "$file_size" -lt 102400 ]; then
        log_error "工具文件大小异常，可能不完整"
        log_info "文件大小: $file_size bytes"
        exit 1
    fi

    # 验证是否为有效的 jar 文件
    if ! file "$TOOL_JAR" | grep -q "Java archive\|Zip archive"; then
        log_error "工具文件格式错误，不是有效的 JAR 文件"
        exit 1
    fi

    log_success "工具验证通过（大小: $((file_size / 1024)) KB）"
}

# 创建配置文件模板
create_config_template() {
    # 检查配置文件是否已存在
    if [ -f "$CONFIG_FILE" ] && [ "$FORCE_REINSTALL" = false ]; then
        log_warning "配置文件已存在，跳过创建"
        log_info "已有配置: $CONFIG_FILE"
        log_info "如需重新创建，请使用: $0 --force"
        return 0
    fi

    log_info "创建配置文件模板..."

    # 如果是强制重装，备份旧配置
    if [ -f "$CONFIG_FILE" ] && [ "$FORCE_REINSTALL" = true ]; then
        backup_file="${CONFIG_FILE}.backup.$(date +%Y%m%d_%H%M%S)"
        cp "$CONFIG_FILE" "$backup_file"
        log_info "旧配置已备份到: $backup_file"
    fi

    cat > "$CONFIG_FILE" << 'EOF'
[appkey]
key=
#appkey 请在 dun.163.com登录后安全加固-服务管理获取

[so]
so1=
so2=
#配置需要保护的 so 文件的名称，建议配置自研 so，第三方 so 不建议处理，例如 so1=libxxxx.so

[apksign]
keystore=
alias=
pswd=
aliaspswd=
signver=v1+v2
#apksign 用于 Android 加固时候的签名文件信息配置，结合命令-apksign 一起使用生效

[hapsign]
keystoreFile=
keystorePwd=
keyAlias=
keyPwd=
appCertFile=
profileFile=
mode=
signAlg=
#hapsign 用于鸿蒙加固时候的签名文件信息配置，结合命令-hapsign 一起使用生效

[update]
u=1
t=30
#配置工具是否定时自动检测更新，u=0 不检测更新， u=1 检测更新，t=x 为检测时间，单位天。

##更多功能 config 配置请参考对应官网文档，例如：https://support.dun.163.com/documents/15588074449563648?docId=989347548106215424
EOF

    # 设置文件权限为 600（仅所有者可读写）
    chmod 600 "$CONFIG_FILE"
    log_success "配置文件模板创建成功: $CONFIG_FILE"
    log_success "配置文件权限已设置为 600（仅所有者可读写）"
}

# 显示后续步骤
show_next_steps() {
    echo ""
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}  易盾加固工具安装成功！${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo ""
    echo -e "${YELLOW}后续步骤：${NC}"
    echo ""
    echo "1. 获取 AppKey"
    echo "   访问: https://dun.163.com/dashboard#/login/"
    echo "   注册账号并获取加固服务的 appkey"
    echo ""
    echo "2. 配置 AppKey"
    echo "   运行: ./scripts/configure.sh"
    echo "   或直接编辑: $CONFIG_FILE"
    echo ""
    echo "3. 开始使用"
    echo "   运行: ./scripts/defense-smart.sh /path/to/your-file"
    echo "   或通过 AI agent 对话: \"帮我加固 /path/to/your-file\""
    echo ""
}

# 显示使用帮助
show_help() {
    echo "易盾加固工具 - 安装脚本"
    echo ""
    echo "用法:"
    echo "  $0              # 正常安装（保留已有配置）"
    echo "  $0 --force      # 强制重新安装（会备份旧配置）"
    echo "  $0 --help       # 显示帮助"
    echo ""
    echo "说明:"
    echo "  默认情况下，如果工具和配置文件已存在，将跳过安装"
    echo "  使用 --force 参数可以强制重新下载和安装"
    echo ""
}

# 主函数
main() {
    # 处理参数
    case "$1" in
        --help|-h)
            show_help
            exit 0
            ;;
        --force|-f)
            FORCE_REINSTALL=true
            log_info "强制重新安装模式"
            ;;
        "")
            # 无参数，正常模式
            ;;
        *)
            echo "错误: 未知参数 '$1'"
            echo ""
            show_help
            exit 1
            ;;
    esac

    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}  易盾应用加固工具 - 安装向导${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""

    check_java
    setup_directory

    # 下载工具（如果已存在会跳过）
    download_tool
    download_result=$?

    # 只有下载了新工具才需要解压
    if [ $download_result -eq 0 ] && [ -f "$TOOL_ZIP" ]; then
        extract_tool
    fi

    # 验证工具
    verify_tool

    # 创建配置（如果已存在会跳过）
    create_config_template

    show_next_steps
}

# 执行主函数
main "$@"
