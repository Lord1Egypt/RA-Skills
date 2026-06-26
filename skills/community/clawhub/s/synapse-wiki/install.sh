#!/bin/bash
# install.sh — Synapse Skills 安装脚本
#
# 用法:
#   ./install.sh
#   ./install.sh --dry-run
#   ./install.sh --uninstall

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_NAME="$(basename "$SCRIPT_DIR")"
SKILL_DEST="$HOME/.claude/skills/$SKILL_NAME"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[OK]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Parse arguments
DRY_RUN=false
UNINSTALL=false

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
        --help|-h)
            echo "Synapse Skills 安装脚本"
            echo ""
            echo "用法：$0 [OPTIONS]"
            echo ""
            echo "选项:"
            echo "  --dry-run     预览安装过程，不实际执行"
            echo "  --uninstall   卸载已安装的 skill"
            echo "  --help, -h    显示帮助信息"
            echo ""
            echo "示例:"
            echo "  $0                    # 安装"
            echo "  $0 --dry-run          # 预览"
            echo "  $0 --uninstall        # 卸载"
            exit 0
            ;;
    esac
done

# Check prerequisites
check_prerequisites() {
    log_info "检查前置条件..."

    # Check Python 3
    if ! command -v python3 &> /dev/null; then
        log_error "Python 3 未安装"
        echo "请先安装 Python 3: brew install python3"
        exit 1
    fi
    log_success "Python 3: $(python3 --version)"

    # Check GitNexus (for synapse-code only)
    if [[ "$SKILL_NAME" == *"synapse-code"* ]]; then
        if ! command -v gitnexus &> /dev/null; then
            log_warning "GitNexus CLI 未安装"
            echo "安装命令：npm install -g gitnexus"
            echo "或者跳过此检查：export SKIP_GITNEXUS_CHECK=1"
            if [[ -z "$SKIP_GITNEXUS_CHECK" ]]; then
                log_info "继续安装（GitNexus 为可选依赖）..."
            fi
        else
            log_success "GitNexus: $(gitnexus --version 2>/dev/null || echo '已安装')"
        fi
    fi

    # Check Claude skills directory
    if [[ ! -d "$HOME/.claude/skills" ]]; then
        log_info "Creating Claude skills directory..."
        if [[ "$DRY_RUN" == false ]]; then
            mkdir -p "$HOME/.claude/skills"
            log_success "Created: $HOME/.claude/skills"
        else
            log_info "[DRY-RUN] Would create: $HOME/.claude/skills"
        fi
    else
        log_success "Claude skills directory exists"
    fi
}

# Install skill
install_skill() {
    log_info "安装 $SKILL_NAME 到 $SKILL_DEST..."

    if [[ "$DRY_RUN" == true ]]; then
        log_info "[DRY-RUN] Would copy: $SCRIPT_DIR → $SKILL_DEST"
        return 0
    fi

    # Remove existing installation
    if [[ -d "$SKILL_DEST" ]]; then
        log_warning "已存在安装，覆盖中..."
        rm -rf "$SKILL_DEST"
    fi

    # Copy skill
    cp -r "$SCRIPT_DIR" "$SKILL_DEST"
    log_success "安装完成：$SKILL_DEST"

    # Create symlink for config
    if [[ ! -f "$SKILL_DEST/config.json" ]] && [[ -f "$SKILL_DEST/config.template.json" ]]; then
        log_info "创建默认配置文件..."
        cp "$SKILL_DEST/config.template.json" "$SKILL_DEST/config.json"
        log_success "Created: $SKILL_DEST/config.json"
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
    echo ""
    log_info "后安装检查..."

    # Check skill files
    if [[ -f "$SKILL_DEST/SKILL.md" ]]; then
        log_success "SKILL.md exists"
    else
        log_error "SKILL.md not found!"
        exit 1
    fi

    # Check scripts
    if [[ -d "$SKILL_DEST/scripts" ]]; then
        script_count=$(ls -1 "$SKILL_DEST/scripts"/*.py 2>/dev/null | wc -l)
        log_success "Scripts: $script_count Python files"
    fi

    # Show usage
    echo ""
    echo "=========================================="
    echo "  $SKILL_NAME 安装完成!"
    echo "=========================================="
    echo ""
    echo "使用方式:"
    echo "  /$SKILL_NAME <command> [args]"
    echo ""
    echo "可用命令:"
    if [[ -d "$SKILL_DEST/commands" ]]; then
        for cmd in "$SKILL_DEST/commands"/*.sh; do
            if [[ -f "$cmd" ]]; then
                echo "  - $(basename "$cmd" .sh)"
            fi
        done
    fi
    echo ""
    echo "配置:"
    echo "  $SKILL_DEST/config.json"
    echo ""
    if [[ "$SKILL_NAME" == *"synapse-code"* ]]; then
        echo "注意:"
        echo "  - 首次使用前请配置 config.json"
        echo "  - 需要安装 Pipeline workspace: ~/pipeline-workspace/"
        echo "  - GitNexus CLI 可选：npm install -g gitnexus"
    fi
    echo ""
}

# Main
main() {
    echo "=========================================="
    echo "  Synapse Skills 安装程序"
    echo "=========================================="
    echo ""

    check_prerequisites

    if [[ "$UNINSTALL" == true ]]; then
        uninstall_skill
    else
        install_skill
        post_install
    fi

    echo ""
    if [[ "$DRY_RUN" == true ]]; then
        log_info "Dry run completed. No changes were made."
    else
        log_success "安装成功!"
    fi
}

main
