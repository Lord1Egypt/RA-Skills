#!/bin/bash
# install.sh — Synapse Code 安装脚本（增强版）
#
# 用法:
#   ./install.sh
#   ./install.sh --dry-run
#   ./install.sh --uninstall
#   ./install.sh --force

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_NAME="$(basename "$SCRIPT_DIR")"
SKILL_DEST="$HOME/.claude/skills/$SKILL_NAME"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 颜色输出
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[⚠]${NC} $1"
}

log_error() {
    echo -e "${RED}[✗]${NC} $1"
}

log_step() {
    echo -e "${CYAN}[⟳]${NC} $1"
}

print_header() {
    echo ""
    echo -e "${CYAN}════════════════════════════════════════════════════${NC}"
    echo -e "${BOLD}  $1${NC}"
    echo -e "${CYAN}════════════════════════════════════════════════════${NC}"
}

print_section() {
    echo ""
    echo -e "${CYAN}────────────────────────────────────────────────────${NC}"
    echo -e "${BOLD}$1${NC}"
    echo -e "${CYAN}────────────────────────────────────────────────────${NC}"
}

# Parse arguments
DRY_RUN=false
UNINSTALL=false
FORCE=false
SKIP_NPM=false

for arg in "$@"; do
    case $arg in
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --uninstall)
            UNINSTALL=true
            shift
            ;;
        --force)
            FORCE=true
            shift
            ;;
        --skip-npm)
            SKIP_NPM=true
            shift
            ;;
        --help|-h)
            print_header "Synapse Code 安装脚本"
            echo ""
            echo -e "${BOLD}用法：${NC}$0 [OPTIONS]"
            echo ""
            echo -e "${BOLD}选项:${NC}"
            echo "    --dry-run       预览安装过程，不实际执行"
            echo "    --uninstall     卸载已安装的 skill"
            echo "    --force         强制覆盖已存在的安装"
            echo "    --skip-npm      跳过 npm 依赖安装"
            echo "    --help, -h      显示帮助信息"
            echo ""
            echo -e "${BOLD}示例:${NC}"
            echo "    $0                    # 安装"
            echo "    $0 --dry-run          # 预览"
            echo "    $0 --uninstall        # 卸载"
            echo "    $0 --force            # 强制覆盖"
            echo "    $0 --skip-npm         # 跳过 npm 安装"
            echo ""
            exit 0
            ;;
    esac
done

# Check prerequisites
check_prerequisites() {
    print_section "检查前置条件"

    local has_error=false

    # Check Python 3
    log_step "检查 Python 3..."
    if ! command -v python3 &> /dev/null; then
        log_error "Python 3 未安装"
        echo -e "  ${YELLOW}请先安装 Python 3:${NC}"
        echo "    macOS:  brew install python3"
        echo "    Ubuntu: sudo apt-get install python3"
        echo "    Windows: 从 python.org 下载安装"
        has_error=true
    else
        local py_version=$(python3 --version)
        log_success "Python 3: $py_version"
    fi

    # Check Node.js (for npm)
    if [[ "$SKIP_NPM" == false ]]; then
        log_step "检查 Node.js..."
        if ! command -v node &> /dev/null; then
            log_warning "Node.js 未安装 (npm 依赖安装需要)"
            echo -e "  ${YELLOW}如要安装 GitNexus，请先安装 Node.js:${NC}"
            echo "    macOS:  brew install node"
            echo "    Ubuntu: sudo apt-get install nodejs npm"
        else
            local node_version=$(node --version)
            local node_major=$(echo "$node_version" | sed 's/v//' | cut -d. -f1)

            # Check Node.js version compatibility
            if [[ "$node_major" -ge 25 ]]; then
                log_warning "Node.js 版本可能不兼容：$node_version"
                echo -e "  ${YELLOW}警告：GitNexus 依赖的 tree-sitter v0.21.1 在 Node.js v25+ 上可能编译失败${NC}"
                echo -e "  ${YELLOW}建议使用 Node.js v18-v24，或手动安装新版 tree-sitter:${NC}"
                echo "    cd ~/.claude/skills/synapse-code"
                echo "    npm install tree-sitter@latest"
                echo "    npm install"
            else
                log_success "Node.js: $node_version"
            fi
        fi
    fi

    # Check Claude skills directory
    log_step "检查 Claude skills 目录..."
    if [[ ! -d "$HOME/.claude/skills" ]]; then
        log_warning "Claude skills 目录不存在"
        if [[ "$DRY_RUN" == false ]]; then
            log_step "创建目录..."
            mkdir -p "$HOME/.claude/skills"
            log_success "Created: $HOME/.claude/skills"
        else
            log_info "[DRY-RUN] Would create: $HOME/.claude/skills"
        fi
    else
        log_success "Claude skills directory exists"
    fi

    # Check rsync
    log_step "检查 rsync..."
    if ! command -v rsync &> /dev/null; then
        log_error "rsync 未安装"
        echo -e "  ${YELLOW}请安装 rsync:${NC}"
        echo "    macOS:  brew install rsync"
        echo "    Ubuntu: sudo apt-get install rsync"
        has_error=true
    else
        log_success "rsync: $(rsync --version | head -1)"
    fi

    # Check disk space (at least 10MB free)
    log_step "检查磁盘空间..."
    local free_space=$(df -k "$HOME" | tail -1 | awk '{print $4}')
    if [[ "$free_space" -lt 10240 ]]; then
        log_error "磁盘空间不足 (需要至少 10MB)"
        echo -e "  ${YELLOW}当前可用空间：${free_space}KB${NC}"
        has_error=true
    else
        local free_mb=$((free_space / 1024))
        log_success "磁盘空间：${free_mb}MB 可用"
    fi

    if [[ "$has_error" == true ]]; then
        echo ""
        log_error "前置检查失败，请修复上述问题后重试"
        exit 1
    fi
}

# Install skill
install_skill() {
    print_section "安装 Skill"

    if [[ "$DRY_RUN" == true ]]; then
        log_info "[DRY-RUN] Would copy: $SCRIPT_DIR → $SKILL_DEST"
        return 0
    fi

    # Remove existing installation
    if [[ -d "$SKILL_DEST" ]]; then
        if [[ "$FORCE" == true ]]; then
            log_warning "已存在安装，强制覆盖中..."
            rm -rf "$SKILL_DEST"
        else
            log_warning "已存在安装：$SKILL_DEST"
            echo ""
            echo -e "${YELLOW}请选择操作:${NC}"
            echo "  1. 覆盖安装 (删除现有安装)"
            echo "  2. 取消安装"
            echo ""
            read -p "输入选项 (1/2): " -n 1 -r
            echo ""
            if [[ $REPLY =~ ^[1]$ ]]; then
                rm -rf "$SKILL_DEST"
                log_info "已删除现有安装"
            else
                log_info "安装已取消"
                exit 0
            fi
        fi
    fi

    # Copy skill (exclude node_modules)
    log_step "复制文件..."
    rsync -av --exclude 'node_modules' --exclude '.git' --exclude '__pycache__' \
        "$SCRIPT_DIR/" "$SKILL_DEST/"
    log_success "文件复制完成：$SKILL_DEST"

    # Create symlink for config
    if [[ ! -f "$SKILL_DEST/config.json" ]] && [[ -f "$SKILL_DEST/config.template.json" ]]; then
        log_step "创建默认配置文件..."
        cp "$SKILL_DEST/config.template.json" "$SKILL_DEST/config.json"
        log_success "Created: $SKILL_DEST/config.json"
    fi

    # Install npm dependencies (gitnexus)
    if [[ "$SKIP_NPM" == false ]]; then
        if [[ -f "$SKILL_DEST/package.json" ]]; then
            log_step "安装 GitNexus CLI (内建依赖)..."
            cd "$SKILL_DEST"

            if command -v npm &> /dev/null; then
                # Run npm install with error handling
                if npm install 2>&1 | tee /tmp/synapse-npm-install.log; then
                    if [[ -f "$SKILL_DEST/node_modules/.bin/gitnexus" ]]; then
                        log_success "GitNexus installed: $SKILL_DEST/node_modules/.bin/gitnexus"
                    else
                        log_warning "GitNexus 安装可能失败，请手动运行：cd $SKILL_DEST && npm install"
                    fi
                else
                    log_error "npm install 失败"
                    echo -e "\n${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
                    echo -e "${YELLOW}可能的原因：tree-sitter 与 Node.js 版本不兼容${NC}"
                    echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"

                    # Check Node.js version
                    local node_ver=$(node --version 2>/dev/null)
                    local node_major=$(echo "$node_ver" | sed 's/v//' | cut -d. -f1)

                    if [[ "$node_major" -ge 25 ]]; then
                        echo -e "${YELLOW}检测到 Node.js v25+，tree-sitter v0.21.1 不支持此版本${NC}\n"
                        echo -e "${YELLOW}解决方案：${NC}"
                        echo "  1. 降级 Node.js 到 v18-v24 (推荐)"
                        echo "     macOS: brew install node@22"
                        echo "     或使用 nvm: nvm install 22 && nvm use 22"
                        echo ""
                        echo "  2. 或手动安装新版 tree-sitter（可能不稳定）"
                        echo "     cd $SKILL_DEST"
                        echo "     npm install tree-sitter@latest"
                        echo "     npm install"
                        echo ""
                        echo "  3. 或跳过 GitNexus 安装（不使用代码图谱功能）"
                        echo "     重新运行：./install.sh --skip-npm"
                    else
                        echo -e "${YELLOW}错误详情已保存到：/tmp/synapse-npm-install.log${NC}"
                        echo -e "${YELLOW}请检查日志后重试：cd $SKILL_DEST && npm install${NC}"
                    fi
                    echo ""
                fi
            else
                log_warning "npm 未找到，跳过 GitNexus 安装"
                echo -e "  ${YELLOW}后续可手动安装：cd $SKILL_DEST && npm install${NC}"
            fi
        fi
    else
        log_info "跳过 npm 依赖安装 (--skip-npm)"
    fi
}

# Uninstall skill
uninstall_skill() {
    log_info "卸载 $SKILL_NAME..."

    if [[ ! -d "$SKILL_DEST" ]]; then
        log_warning "未找到安装：$SKILL_DEST"
        return 0
    fi

    if [[ "$DRY_RUN" == true ]]; then
        log_info "[DRY-RUN] Would remove: $SKILL_DEST"
        return 0
    fi

    rm -rf "$SKILL_DEST"
    log_success "卸载完成"
}

# Post-install checks
post_install() {
    print_section "后安装检查"

    local has_error=false

    # Check skill files
    log_step "检查 SKILL.md..."
    if [[ -f "$SKILL_DEST/SKILL.md" ]]; then
        log_success "SKILL.md exists"
    else
        log_error "SKILL.md not found!"
        has_error=true
    fi

    # Check scripts directory
    log_step "检查 scripts 目录..."
    if [[ -d "$SKILL_DEST/scripts" ]]; then
        local script_count=$(ls -1 "$SKILL_DEST/scripts"/*.py 2>/dev/null | wc -l)
        log_success "Scripts: $script_count Python files"
    else
        log_warning "scripts 目录不存在"
    fi

    # Check commands directory
    log_step "检查 commands 目录..."
    if [[ -d "$SKILL_DEST/commands" ]]; then
        local cmd_count=$(ls -1 "$SKILL_DEST/commands"/*.sh 2>/dev/null | wc -l)
        log_success "Commands: $cmd_count shell scripts"
    else
        log_info "commands 目录不存在 (可选)"
    fi

    # Check agents directory
    log_step "检查 agents 目录..."
    if [[ -d "$SKILL_DEST/agents" ]]; then
        local agent_count=$(find "$SKILL_DEST/agents" -name "*.md" | wc -l)
        log_success "Agents: $agent_count agent templates"
    else
        log_info "agents 目录不存在 (可选)"
    fi

    # Verify Python scripts syntax
    log_step "验证 Python 脚本语法..."
    local syntax_error=0
    for script in "$SKILL_DEST/scripts"/*.py; do
        if [[ -f "$script" ]]; then
            if python3 -m py_compile "$script" 2>/dev/null; then
                : # OK
            else
                log_warning "语法错误：$(basename "$script")"
                ((syntax_error++))
            fi
        fi
    done
    if [[ $syntax_error -eq 0 ]]; then
        log_success "所有 Python 脚本语法正确"
    else
        log_warning "$syntax_error 个脚本有语法错误"
    fi

    if [[ "$has_error" == true ]]; then
        echo ""
        log_error "后安装检查失败"
        exit 1
    fi

    # Show usage
    print_header "$SKILL_NAME 安装完成!"

    echo ""
    echo -e "${BOLD}使用方式:${NC}"
    echo "  /$SKILL_NAME <command> [args]"
    echo ""
    echo -e "${BOLD}可用命令:${NC}"
    if [[ -d "$SKILL_DEST/commands" ]]; then
        for cmd in "$SKILL_DEST/commands"/*.sh; do
            if [[ -f "$cmd" ]]; then
                echo "  - $(basename "$cmd" .sh)"
            fi
        done
    fi
    echo ""
    echo -e "${BOLD}配置:${NC}"
    echo "  $SKILL_DEST/config.json"
    echo ""
    echo -e "${BOLD}内建组件:${NC}"
    echo "  - GitNexus CLI (代码图谱分析)"
    if [[ -f "$SKILL_DEST/node_modules/.bin/gitnexus" ]]; then
        echo "    ${GREEN}✓ 已安装${NC}"
    else
        echo "    ${YELLOW}⚠ 未安装 (需手动运行 npm install)${NC}"
    fi
    echo ""
    echo -e "${BOLD}快速开始:${NC}"
    echo "  1. 配置 config.json (设置 Pipeline workspace 路径)"
    echo "  2. 运行 /$SKILL_NAME init /path/to/project"
    echo "  3. 运行 /$SKILL_NAME run my-project \"需求描述\""
    echo ""
}

# Main
main() {
    print_header "Synapse Code 安装程序"

    check_prerequisites

    if [[ "$UNINSTALL" == true ]]; then
        uninstall_skill
        echo ""
        log_success "卸载完成!"
    else
        install_skill
        if [[ "$DRY_RUN" == false ]]; then
            post_install
        fi
    fi

    echo ""
    if [[ "$DRY_RUN" == true ]]; then
        log_info "Dry run completed. No changes were made."
        echo ""
        echo -e "${YELLOW}以上为预览输出，未进行任何修改${NC}"
    else
        if [[ "$UNINSTALL" != true ]]; then
            log_success "安装成功!"
            echo ""
            echo -e "${CYAN}下一步:${NC}"
            echo "  1. 编辑配置文件：$SKILL_DEST/config.json"
            echo "  2. 初始化项目：/$SKILL_NAME init /path/to/project"
            echo "  3. 查看帮助：/$SKILL_NAME --help"
        fi
    fi
}

main
