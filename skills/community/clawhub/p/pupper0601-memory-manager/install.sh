#!/usr/bin/env bash
#
# OpenClaw Memory Manager 专用安装脚本
# 专为 OpenClaw 设计的三层AI记忆系统
#
# 用法:
#   curl -fsSL https://raw.githubusercontent.com/Pupper0601/memory-manager/main/install.sh | bash -s -- -p "$HOME/.openclaw/memory"
#   # 或下载后运行:
#   chmod +x install.sh && ./install.sh -p "$HOME/.openclaw/memory"
#
# OpenClaw 推荐:
#   - 路径: $HOME/.openclaw/memory
#   - 后端: siliconflow (国内可用)
#   - 用户: 系统用户名或 OpenClaw UID
set -eu

# ══════════════════════════════════════════════════════════════
#  跨平台工具函数
# ══════════════════════════════════════════════════════════════

# 获取当前时间（跨平台兼容：Linux / macOS BSD）
# macOS 的 date 不支持 %Y-%m-%d %H:%M 格式，需用 Python 兜底
_now() {
    if [[ "$(uname -s)" == "Darwin" ]]; then
        # macOS: 用 Python 生成 ISO 格式时间
        "$PYTHON_CMD" -c "from datetime import datetime; print(datetime.now().strftime('%Y-%m-%d %H:%M'))"
    else
        # Linux: 直接用 date
        date "+%Y-%m-%d %H:%M"
    fi
}

# ══════════════════════════════════════════════════════════════
#  配置
# ══════════════════════════════════════════════════════════════

VERSION="3.5.0"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND="openai"
SKIP_DEPS=false
SKIP_CONFIG=false
SILENT=false
NO_SHELL_RC=false

# ══════════════════════════════════════════════════════════════
#  颜色输出
# ══════════════════════════════════════════════════════════════

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color
BOLD='\033[1m'

success() { echo -e "${GREEN}✅ $1${NC}"; }
info()    { echo -e "${CYAN}ℹ️  $1${NC}"; }
warn()    { echo -e "${YELLOW}⚠️  $1${NC}"; }
error()   { echo -e "${RED}❌ $1${NC}"; }
title()   { echo -e "\n${MAGENTA}╔════════════════════════════════════════════════════════════╗${NC}"
           echo -e "${MAGENTA}║${NC} $1"
           echo -e "${MAGENTA}╚════════════════════════════════════════════════════════════╝${NC}\n"; }

# ══════════════════════════════════════════════════════════════
#  帮助信息
# ══════════════════════════════════════════════════════════════

show_help() {
    cat << EOF
${BOLD}Memory Manager 安装脚本 v${VERSION}${NC}

${BOLD}用法:${NC}
    $0 [选项]

${BOLD}选项:${NC}
    -u, --user <用户名>     用户名 (默认: 当前用户)
    -b, --backend <后端>   Embedding 后端: openai|siliconflow|zhipu (默认: openai)
    -p, --path <路径>       记忆仓库路径 (默认: ./memory)
    --skip-deps            跳过依赖安装
    --skip-config         跳过交互式配置
    --no-shell-rc         不修改shell配置文件(推荐，更安全)
    --silent              静默模式
    -h, --help            显示帮助

${BOLD}示例:${NC}
    $0 -u john -b siliconflow
    curl -fsSL https://.../install.sh | bash
EOF
}

# ══════════════════════════════════════════════════════════════
#  参数解析
# ══════════════════════════════════════════════════════════════

parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            -u|--user)
                USER_NAME="$2"
                shift 2
                ;;
            -b|--backend)
                BACKEND="$2"
                shift 2
                ;;
            -p|--path)
                MEMORY_PATH="$2"
                shift 2
                ;;
            --skip-deps)
                SKIP_DEPS=true
                shift
                ;;
            --skip-config)
                SKIP_CONFIG=true
                shift
                ;;
            --silent)
                SILENT=true
                shift
                ;;
            --no-shell-rc)
                NO_SHELL_RC=true
                shift
                ;;
            -h|--help)
                show_help
                exit 0
                ;;
            *)
                error "未知参数: $1"
                show_help
                exit 1
                ;;
        esac
    done
}

# ══════════════════════════════════════════════════════════════
#  前置检查
# ══════════════════════════════════════════════════════════════

check_prerequisites() {
    title "检查系统环境"

    # 检测 OS
    OS_TYPE="$(uname -s)"
    case "$OS_TYPE" in
        Darwin*)  OS_NAME="macOS" ;;
        Linux*)   OS_NAME="Linux" ;;
        MINGW*|MSYS*|CYGWIN*) OS_NAME="Windows" ;;
        *)        OS_NAME="Unknown" ;;
    esac
    info "操作系统: $OS_NAME ($OS_TYPE)"

    # Python 检查（兼容 macOS 的 grep，不使用 -P）
    PYTHON_CMD=""
    for cmd in python3 python; do
        if command -v "$cmd" &> /dev/null; then
            PY_VER_STR=$("$cmd" --version 2>&1)
            # 用 awk/sed 替代 grep -P（macOS grep 不支持 -P）
            PYTHON_MAJOR=$("$cmd" -c "import sys; print(sys.version_info.major)" 2>/dev/null)
            PYTHON_MINOR=$("$cmd" -c "import sys; print(sys.version_info.minor)" 2>/dev/null)
            if [[ -n "$PYTHON_MAJOR" ]] && [[ "$PYTHON_MAJOR" -ge 3 ]] && [[ "$PYTHON_MINOR" -ge 8 ]]; then
                PYTHON_CMD="$cmd"
                success "Python 版本: $PY_VER_STR"
                break
            else
                warn "Python 版本过低 ($PY_VER_STR)，跳过"
            fi
        fi
    done

    if [[ -z "$PYTHON_CMD" ]]; then
        error "未检测到 Python 3.8+，请先安装: https://python.org"
        exit 1
    fi

    # pip 检查（优先使用 python -m pip）
    # 注意：PIP_CMD 存储完整命令，用 eval 或数组展开执行
    PIP_PYTHON_CMD=""  # 仅 python 可执行文件
    PIP_IS_MODULE=false
    if "$PYTHON_CMD" -m pip --version &> /dev/null; then
        PIP_IS_MODULE=true
        PIP_PYTHON_CMD="$PYTHON_CMD"
        success "pip 可用 (python -m pip)"
    elif command -v pip3 &> /dev/null; then
        PIP_PYTHON_CMD="pip3"
        success "pip3 可用"
    elif command -v pip &> /dev/null; then
        PIP_PYTHON_CMD="pip"
        success "pip 可用"
    else
        warn "pip 不可用，尝试安装..."
        "$PYTHON_CMD" -m ensurepip --upgrade 2>/dev/null || true
        PIP_IS_MODULE=true
        PIP_PYTHON_CMD="$PYTHON_CMD"
    fi

    # Git 检查 (可选)
    if command -v git &> /dev/null; then
        success "Git: $(git --version 2>&1)"
        HAS_GIT=true
    else
        warn "未检测到 Git，GitHub 同步功能将不可用"
        warn "如需 GitHub 同步，请安装: https://git-scm.com"
        HAS_GIT=false
    fi
}

# ══════════════════════════════════════════════════════════════
#  pip 封装（避免变量含空格问题，兼容 python -m pip / pip3 / pip）
# ══════════════════════════════════════════════════════════════

pip_run() {
    if [[ "${PIP_IS_MODULE:-false}" == true ]]; then
        "$PIP_PYTHON_CMD" -m pip "$@"
    else
        "$PIP_PYTHON_CMD" "$@"
    fi
}

# ══════════════════════════════════════════════════════════════
#  依赖安装
# ══════════════════════════════════════════════════════════════

install_dependencies() {
    if [[ "$SKIP_DEPS" == true ]]; then
        info "跳过依赖安装 (--skip-deps)"
        return
    fi

    title "安装 Python 依赖"

    # 核心依赖（使用 pip_run 确保安装到正确环境）
    info "安装核心依赖: openai, numpy"
    pip_run install "openai>=1.0.0" "numpy>=1.20.0" --quiet --disable-pip-version-check

    if [[ $? -eq 0 ]]; then
        success "核心依赖安装完成"
    else
        error "核心依赖安装失败"
        exit 1
    fi

    # LanceDB (可选)
    install_lancedb=true
    if [[ "$SILENT" != true ]]; then
        read -p "$(echo -e "${YELLOW}是否安装 LanceDB (向量搜索加速 100x)? [Y/n]${NC}") " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Nn]$ ]]; then
            install_lancedb=false
        fi
    fi

    if [[ "$install_lancedb" == true ]]; then
        info "安装 LanceDB (向量搜索加速 100x)..."
        pip_run install "lancedb>=0.5.0" --quiet --disable-pip-version-check
        if [[ $? -eq 0 ]]; then
            success "LanceDB 安装完成"
        else
            warn "LanceDB 安装失败，但不影响基本功能"
        fi
    fi
}

# ══════════════════════════════════════════════════════════════
#  获取 API Key
# ══════════════════════════════════════════════════════════════

get_api_key() {
    local backend=$1

    # 1. 检查环境变量
    local env_var=""
    case $backend in
        openai)      env_var="OPENAI_API_KEY" ;;
        siliconflow) env_var="SILICONFLOW_API_KEY" ;;
        zhipu)       env_var="ZHIPU_API_KEY" ;;
    esac

    local existing_key="${!env_var:-}"
    if [[ -n "$existing_key" ]] && [[ "$existing_key" == sk-* ]]; then
        success "检测到已保存的 $backend API Key"
        echo "$existing_key"
        return
    fi

    # 2. 交互输入
    if [[ "$SILENT" != true ]]; then
        echo ""
        echo -e "${YELLOW}🔑 请配置 $backend API Key:${NC}"

        local prompt=""
        case $backend in
            openai)      prompt="OpenAI API Key (sk-...)" ;;
            siliconflow) prompt="SiliconFlow API Key" ;;
            zhipu)       prompt="Zhipu API Key" ;;
        esac

        read -p "$prompt: " -s api_key
        echo

        if [[ -z "$api_key" ]]; then
            warn "未输入 API Key，将使用环境变量方式"
            echo ""
            return
        fi

        # 保存到 shell 配置
        if [[ "$NO_SHELL_RC" == true ]]; then
            info "跳过将API Key写入shell配置文件(使用--no-shell-rc选项)"
            info "请手动设置环境变量: export ${env_var}=<your-api-key>"
            return
        fi

        local shell_rc=""
        if [[ -f "$HOME/.zshrc" ]]; then
            shell_rc="$HOME/.zshrc"
        elif [[ -f "$HOME/.bashrc" ]]; then
            shell_rc="$HOME/.bashrc"
        fi

        if [[ -n "$shell_rc" ]]; then
            if ! grep -q "export ${env_var}=" "$shell_rc" 2>/dev/null; then
                echo "" >> "$shell_rc"
                echo "# Memory Manager API Key - $(date)" >> "$shell_rc"
                echo "export ${env_var}='${api_key}'" >> "$shell_rc"
                success "API Key 已保存到 $shell_rc"
            fi
        fi

        echo "$api_key"
    fi
}

# ══════════════════════════════════════════════════════════════
#  初始化记忆仓库
# ══════════════════════════════════════════════════════════════

init_memory_repo() {
    local user_name=$1
    local memory_path=$2

    title "初始化记忆仓库"

    # 创建目录结构
    info "创建目录: $memory_path"
    mkdir -p "$memory_path"

    # 公共目录
    mkdir -p "$memory_path/shared/daily"
    mkdir -p "$memory_path/shared/weekly"
    mkdir -p "$memory_path/shared/permanent"

    # 用户目录
    mkdir -p "$memory_path/users/$user_name/daily"
    mkdir -p "$memory_path/users/$user_name/weekly"
    mkdir -p "$memory_path/users/$user_name/permanent"

    success "目录结构创建完成"

    # 创建 .gitkeep
    touch "$memory_path/.gitkeep"

    # 生成 INDEX.md
    cat > "$memory_path/users/$user_name/INDEX.md" << EOF
# 用户索引 - $user_name

## 基本信息
- 用户名: $user_name
- 创建时间: $(_now)
- 版本: v${VERSION}

## 记忆统计
| 层级 | 位置 | 说明 |
|------|------|------|
| L1 临时 | \`daily/\` | 当天记录，自动清理 |
| L2 长期 | \`weekly/\` | 本周总结 |
| L3 永久 | \`permanent/\` | 重要记忆，长期保存 |

## 快速命令
\`\`\`bash
mm log "记录内容"    # 快速记录
mm search "关键词"   # 搜索
mm insight           # AI 总结
\`\`\`
EOF

    success "用户索引创建完成: users/$user_name/INDEX.md"
    echo "$memory_path"
}

# ══════════════════════════════════════════════════════════════
#  生成配置文件
# ══════════════════════════════════════════════════════════════

create_config() {
    local user_name=$1
    local memory_path=$2
    local backend=$3

    title "生成配置文件"

    # 全局配置
    local config_dir="$HOME/.memory-manager"
    mkdir -p "$config_dir"

    cat > "$config_dir/config.json" << EOF
{
    "version": "${VERSION}",
    "uid": "${user_name}",
    "base_dir": "${memory_path}",
    "backend": "${backend}",
    "created": "$(_now)"
}
EOF
    success "兼容配置文件: $config_dir/config.json"
    
    # OpenClaw 专用配置文件
    cat > "$memory_path/.memory_config.json" << EOF
{
    "version": "${VERSION}",
    "uid": "${user_name}",
    "base_dir": "${memory_path}",
    "backend": "${backend}",
    "openclaw_integration": true,
    "auto_sync": true,
    "created": "$(_now)",
    "max_file_size_kb": 10,
    "auto_compress_lines": {
        "L1": 150,
        "L2": 200,
        "L3": 300
    },
    "similarity_threshold": 0.85,
    "semantic_weight": 0.6
}
EOF
    success "OpenClaw 配置文件: $memory_path/.memory_config.json"
}

# ══════════════════════════════════════════════════════════════
#  GitHub 同步设置
# ══════════════════════════════════════════════════════════════

init_git_sync() {
    local memory_path=$1

    if [[ "$HAS_GIT" != true ]]; then
        return
    fi

    title "GitHub 同步设置"

    if [[ "$SILENT" != true ]]; then
        read -p "$(echo -e "${YELLOW}是否配置 GitHub 同步? [y/N]${NC}") " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            info "跳过 GitHub 配置"
            return
        fi

        read -p "$(echo -e "${CYAN}请输入 GitHub 仓库 URL:${NC} ")" repo_url
        if [[ -z "$repo_url" ]]; then
            info "跳过 GitHub 配置"
            return
        fi

        cd "$memory_path"

        if [[ -d ".git" ]]; then
            info "仓库已存在，添加远程..."
            git remote add origin "$repo_url" 2>/dev/null || true
        else
            info "初始化 Git 仓库..."
            git init
            git remote add origin "$repo_url"

            info "创建初始提交..."
            git add .
            git commit -m "feat: initial memory repository"
        fi

        success "GitHub 同步配置完成"
    fi
}

# ══════════════════════════════════════════════════════════════
#  向量索引
# ══════════════════════════════════════════════════════════════

init_vector_index() {
    local memory_path=$1
    local user_name=$2

    title "向量索引设置"

    if [[ "$SILENT" != true ]]; then
        read -p "$(echo -e "${YELLOW}是否立即生成向量索引? [Y/n]${NC}") " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Nn]$ ]]; then
            info "向量索引将在首次搜索时自动生成"
            return
        fi
    fi

    local embed_script="$SCRIPT_DIR/scripts/memory_embed.py"
    if [[ -f "$embed_script" ]]; then
        info "正在生成向量索引 (这可能需要几分钟)..."
        "$PYTHON_CMD" "$embed_script" --uid "$user_name" --base-dir "$memory_path"
        if [[ $? -eq 0 ]]; then
            success "向量索引生成完成"
        else
            warn "向量索引生成遇到问题，但不影响基本功能"
        fi
    else
        info "向量生成脚本未找到，跳过"
    fi
}

# ══════════════════════════════════════════════════════════════
#  创建快捷命令
# ══════════════════════════════════════════════════════════════

create_alias() {
    title "创建快捷命令"

    local mm_path="$SCRIPT_DIR/mm.py"

    # 检测 shell
    local shell_rc=""
    if [[ -n "${ZSH_VERSION:-}" ]] || [[ "$SHELL" == *"zsh"* ]]; then
        shell_rc="$HOME/.zshrc"
    elif [[ -n "${BASH_VERSION:-}" ]] || [[ "$SHELL" == *"bash"* ]]; then
        shell_rc="$HOME/.bashrc"
        # macOS 默认 .bash_profile
        [[ "$OS_NAME" == "macOS" ]] && [[ -f "$HOME/.bash_profile" ]] && shell_rc="$HOME/.bash_profile"
    fi

    if [[ -z "$shell_rc" ]]; then
        warn "无法检测 shell 配置文件，请手动添加:"
        echo "  alias mm='$PYTHON_CMD $mm_path'"
        return
    fi

    local alias_line="alias mm='$PYTHON_CMD $mm_path'"

    if [[ -f "$shell_rc" ]] && grep -q "Memory Manager" "$shell_rc" 2>/dev/null; then
        info "快捷命令已存在"
    else
        cat >> "$shell_rc" << EOF

# ══════════════════════════════════════════════════════════════
#  Memory Manager 快捷命令
#  安装时间: $(_now)
# ══════════════════════════════════════════════════════════════
$alias_line
EOF
        success "快捷命令 'mm' 已添加到 $shell_rc"
        info "运行 'source $shell_rc' 或重启终端生效"
    fi
}

# ══════════════════════════════════════════════════════════════
#  主流程
# ══════════════════════════════════════════════════════════════

main() {
    # 默认值
    USER_NAME="${USER:-$(id -un 2>/dev/null || echo "user")}"
    MEMORY_PATH="$SCRIPT_DIR/memory"
    PYTHON_CMD=""  # 由 check_prerequisites 赋值
    PIP_CMD=""     # 由 check_prerequisites 赋值
    OS_NAME=""     # 由 check_prerequisites 赋值

    # 解析参数
    parse_args "$@"

    echo ""
    echo -e "${MAGENTA}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${MAGENTA}║                                                            ║${NC}"
    echo -e "${MAGENTA}║          📦 Memory Manager 安装向导 v${VERSION}               ║${NC}"
    echo -e "${MAGENTA}║                                                            ║${NC}"
    echo -e "${MAGENTA}╚════════════════════════════════════════════════════════════╝${NC}"
    echo ""

    # 1. 检查环境
    check_prerequisites

    # 2. 安装依赖
    install_dependencies

    # 3. 交互式配置
    if [[ "$SKIP_CONFIG" != true ]]; then
        title "配置信息"

        if [[ "$SILENT" != true ]]; then
            read -p "$(echo -e "${CYAN}👤 请输入用户名 (用于区分多用户) [${USER_NAME}]:${NC} ")" input_user
            [[ -n "$input_user" ]] && USER_NAME="$input_user"

            echo ""
            echo -e "${YELLOW}🌐 选择 Embedding 后端:${NC}"
            echo "   [1] OpenAI (推荐)"
            echo "   [2] SiliconFlow (国内可用)"
            echo "   [3] Zhipu (国内可用)"

            read -p "$(echo -e "${CYAN}请选择 [1]:${NC} ")" choice
            case $choice in
                2) BACKEND="siliconflow" ;;
                3) BACKEND="zhipu" ;;
                *) BACKEND="openai" ;;
            esac

            echo ""
            echo -e "${YELLOW}📁 记忆仓库路径:${NC}"
            read -p "$(echo -e "${CYAN}   [${MEMORY_PATH}]:${NC} ")" input_path
            [[ -n "$input_path" ]] && MEMORY_PATH="$input_path"
        fi
    fi

    # 4. 获取 API Key
    api_key=$(get_api_key "$BACKEND")

    # 5. 初始化记忆仓库
    repo_path=$(init_memory_repo "$USER_NAME" "$MEMORY_PATH")

    # 6. 生成配置文件
    create_config "$USER_NAME" "$repo_path" "$BACKEND"

    # 7. GitHub 同步 (可选)
    init_git_sync "$repo_path"

    # 8. 向量索引 (可选)
    init_vector_index "$repo_path" "$USER_NAME"

    # 9. 快捷命令
    create_alias

    # 完成
    echo ""
    echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║                                                            ║${NC}"
    echo -e "${GREEN}║  ✅ Memory Manager 安装完成！                             ║${NC}"
    echo -e "${GREEN}║                                                            ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${CYAN}📖 快速开始:${NC}"
    echo -e "   ${BOLD}mm log \"这是我的第一条记忆\"${NC}   # 📝 记录"
    echo -e "   ${BOLD}mm search \"查找相关内容\"${NC}       # 🔍 搜索"
    echo -e "   ${BOLD}mm insight${NC}                      # 🧠 AI 总结"
    echo -e "   ${BOLD}mm stats${NC}                        # 📊 统计"
    echo ""
    echo -e "${CYAN}📚 完整文档: see README.md 或 SKILL.md${NC}"
    echo ""
}

main "$@"
