#!/bin/bash
# install.sh — Synapse Brain 安装脚本
#
# 用法:
#   ./install.sh
#   ./install.sh --dry-run
#   ./install.sh --uninstall

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_NAME="$(basename "$SCRIPT_DIR")"
SKILL_DEST="$HOME/.openclaw/skills/$SKILL_NAME"

BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[✓]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[⚠]${NC} $1"; }
log_error() { echo -e "${RED}[✗]${NC} $1"; }
log_step() { echo -e "${CYAN}[⟳]${NC} $1"; }

DRY_RUN=false
UNINSTALL=false
FORCE=false

for arg in "$@"; do
    case $arg in
        --dry-run) DRY_RUN=true ;;
        --uninstall) UNINSTALL=true ;;
        --force) FORCE=true ;;
        --help|-h)
            echo "Synapse Brain 安装脚本"
            echo "用法: $0 [--dry-run] [--uninstall] [--force]"
            exit 0 ;;
    esac
done

install_skill() {
    log_step "安装 $SKILL_NAME..."

    if [[ -d "$SKILL_DEST" ]]; then
        if [[ "$FORCE" == true ]]; then
            log_warning "强制覆盖已存在的安装..."
            rm -rf "$SKILL_DEST"
        else
            log_warning "已存在: $SKILL_DEST"
            rm -rf "$SKILL_DEST"
        fi
    fi

    if [[ "$DRY_RUN" == true ]]; then
        log_info "[DRY-RUN] Would copy: $SCRIPT_DIR → $SKILL_DEST"
        return 0
    fi

    # Create parent directory
    mkdir -p "$(dirname "$SKILL_DEST")"

    # Copy skill files
    rsync -av --exclude 'node_modules' --exclude '.git' --exclude '__pycache__' \
        "$SCRIPT_DIR/" "$SKILL_DEST/"
    log_success "文件复制完成"

    # Create brain state directory
    STATE_DIR="$HOME/.openclaw/brain-state"
    if [[ ! -d "$STATE_DIR" ]]; then
        mkdir -p "$STATE_DIR"
        log_success "创建状态目录: $STATE_DIR"
    fi

    # Create default config
    CONFIG_FILE="$SKILL_DEST/config.json"
    if [[ ! -f "$CONFIG_FILE" ]]; then
        cat > "$CONFIG_FILE" << 'EOF'
{
  "brain": {
    "state_dir": "~/.openclaw/brain-state",
    "auto_save": true,
    "auto_save_interval": 300,
    "skills": {
      "code": "synapse-code",
      "wiki": "synapse-wiki"
    }
  }
}
EOF
        log_success "创建默认配置: config.json"
    fi
}

uninstall_skill() {
    if [[ ! -d "$SKILL_DEST" ]]; then
        log_warning "未找到安装: $SKILL_DEST"
        return 0
    fi
    if [[ "$DRY_RUN" == true ]]; then
        log_info "[DRY-RUN] Would remove: $SKILL_DEST"
        return 0
    fi
    rm -rf "$SKILL_DEST"
    log_success "卸载完成"
}

post_install() {
    log_step "后安装检查..."

    if [[ -f "$SKILL_DEST/SKILL.md" ]]; then
        log_success "SKILL.md exists"
    else
        log_error "SKILL.md not found!"
        exit 1
    fi

    if [[ -f "$SKILL_DEST/SOUL.md" ]]; then
        log_success "SOUL.md exists"
    else
        log_error "SOUL.md not found!"
        exit 1
    fi

    # Verify Python scripts
    local syntax_ok=0
    local syntax_err=0
    for script in "$SKILL_DEST/scripts"/*.py; do
        if [[ -f "$script" ]]; then
            if python3 -m py_compile "$script" 2>/dev/null; then
                ((syntax_ok++))
            else
                log_warning "语法错误: $(basename "$script")"
                ((syntax_err++))
            fi
        fi
    done
    log_success "Python 脚本: $syntax_ok 正确, $syntax_err 错误"

    echo ""
    echo -e "${BOLD}Synapse Brain 安装完成!${NC}"
    echo ""
    echo "配置: $SKILL_DEST/config.json"
    echo "状态: $HOME/.openclaw/brain-state/"
    echo ""
    echo "下一步:"
    echo "  1. 确保 synapse-code 和 synapse-wiki 已安装"
    echo "  2. 编辑 config.json 配置关联 skills"
    echo "  3. 使用 /synapse-brain init my-project \"项目名\" 开始"
}

main() {
    if [[ "$UNINSTALL" == true ]]; then
        uninstall_skill
    else
        install_skill
        if [[ "$DRY_RUN" == false ]]; then
            post_install
        fi
    fi
}

main
