#!/usr/bin/env bash
# ensure_python_env.sh
#
# 【OpenClaw 内部工具脚本】
# 检查并确保指定 Python 版本的虚拟环境存在于 ~/.python_env/<python_version>
# 该环境可被多个 skill 共享复用。
# 如果 uv 未安装，则先自动安装 uv，再创建环境。
#
# 用法:
#   ensure_python_env.sh <python_version> [packages...]
#
# 参数:
#   python_version  Python 版本，如 3.11、3.12（必填）
#   packages        需要额外安装的包，如 requests pillow（可选）
#
# 示例:
#   ensure_python_env.sh 3.11
#   ensure_python_env.sh 3.11 requests httpx
#   ensure_python_env.sh 3.12 requests pillow numpy
#
# 成功时：stdout 末尾输出机器可读行并以 exit 0 退出
#   PYTHON_ENV_ACTIVATE:/path/to/activate
#   PYTHON_ENV_DIR:/path/to/env
# 失败时：输出错误信息并以 exit 1 退出

set -euo pipefail

# ── 参数解析 ─────────────────────────────────────────────
PYTHON_VERSION="${1:-}"
shift 1 2>/dev/null || true
PACKAGES=("$@")

if [[ -z "$PYTHON_VERSION" ]]; then
    echo "[skill-python-env] 错误：必须指定 Python 版本" >&2
    echo "用法: ensure_python_env.sh <python_version> [packages...]" >&2
    echo "示例: ensure_python_env.sh 3.11 requests" >&2
    exit 1
fi

ENV_BASE="$HOME/.python_env"
ENV_DIR="$ENV_BASE/$PYTHON_VERSION"

# ── 检测 OS，选择 activate 路径 ────────────────────────────
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" ]]; then
    IS_WINDOWS=true
    ACTIVATE_PATH="$ENV_DIR/Scripts/activate"
else
    IS_WINDOWS=false
    ACTIVATE_PATH="$ENV_DIR/bin/activate"
fi

# ── 辅助函数 ──────────────────────────────────────────────
log_info()  { echo "[skill-python-env] $*"; }
log_ok()    { echo "[skill-python-env] ✓ $*"; }
log_warn()  { echo "[skill-python-env] ⚠ $*" >&2; }
log_error() { echo "[skill-python-env] ✗ $*" >&2; }

# ── 1. 检查/安装 uv ───────────────────────────────────────
check_or_install_uv() {
    if command -v uv &>/dev/null; then
        UV_VERSION=$(uv --version 2>&1 | head -1)
        log_ok "uv 已安装：$UV_VERSION"
        return 0
    fi

    # 尝试常见非 PATH 位置
    for candidate in "$HOME/.local/bin/uv" "$HOME/.cargo/bin/uv"; do
        if [[ -x "$candidate" ]]; then
            export PATH="$(dirname "$candidate"):$PATH"
            UV_VERSION=$("$candidate" --version 2>&1 | head -1)
            log_ok "uv 已找到（非 PATH）：$UV_VERSION"
            return 0
        fi
    done

    log_warn "未检测到 uv，正在安装..."

    if [[ "$IS_WINDOWS" == true ]]; then
        if command -v powershell.exe &>/dev/null; then
            log_info "使用 PowerShell 安装 uv..."
            powershell.exe -ExecutionPolicy ByPass -Command \
                "irm https://astral.sh/uv/install.ps1 | iex"
        else
            log_error "未找到 powershell.exe，请手动安装 uv："
            log_error "  https://docs.astral.sh/uv/getting-started/installation/"
            exit 1
        fi
        export PATH="$USERPROFILE/.local/bin:$HOME/.local/bin:$PATH"
    else
        if command -v curl &>/dev/null; then
            log_info "使用 curl 安装 uv..."
            curl -LsSf https://astral.sh/uv/install.sh | sh
        elif command -v wget &>/dev/null; then
            log_info "使用 wget 安装 uv..."
            wget -qO- https://astral.sh/uv/install.sh | sh
        else
            log_error "未找到 curl 或 wget，请手动安装 uv："
            log_error "  https://docs.astral.sh/uv/getting-started/installation/"
            exit 1
        fi
        export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"
    fi

    if command -v uv &>/dev/null; then
        UV_VERSION=$(uv --version 2>&1 | head -1)
        log_ok "uv 安装成功：$UV_VERSION"
        if [[ "$IS_WINDOWS" == true ]]; then
            log_warn "请将 %USERPROFILE%\\.local\\bin 加入系统 PATH 以永久生效"
        else
            log_warn "请将以下行加入 shell 配置文件（~/.bashrc 或 ~/.zshrc）以永久生效："
            log_warn "  export PATH=\"\$HOME/.local/bin:\$PATH\""
        fi
    else
        log_error "uv 安装失败，请手动安装："
        log_error "  https://docs.astral.sh/uv/getting-started/installation/"
        exit 1
    fi
}

# ── 2. 检查/创建虚拟环境 ──────────────────────────────────
ensure_env() {
    mkdir -p "$ENV_BASE"

    if [[ -d "$ENV_DIR" && -f "$ACTIVATE_PATH" ]]; then
        log_ok "Python $PYTHON_VERSION 环境已存在：$ENV_DIR"
        return 0
    fi

    if [[ -d "$ENV_DIR" && ! -f "$ACTIVATE_PATH" ]]; then
        log_warn "目录 $ENV_DIR 存在但环境不完整，重新创建..."
        rm -rf "$ENV_DIR"
    fi

    log_info "创建 Python $PYTHON_VERSION 虚拟环境：$ENV_DIR"

    if uv venv "$ENV_DIR" --python "$PYTHON_VERSION"; then
        log_ok "虚拟环境创建成功"
    else
        log_error "虚拟环境创建失败（Python $PYTHON_VERSION）"
        exit 1
    fi
}

# ── 3. 安装依赖包（幂等，已安装的包会被跳过） ────────────
install_packages() {
    if [[ ${#PACKAGES[@]} -eq 0 ]]; then
        return 0
    fi

    log_info "安装依赖包：${PACKAGES[*]}"

    if uv pip install --python "$ENV_DIR" "${PACKAGES[@]}"; then
        log_ok "依赖包安装成功"
    else
        log_error "依赖包安装失败：${PACKAGES[*]}"
        exit 1
    fi
}

# ── 4. 输出机器可读结果 ───────────────────────────────────
print_result() {
    echo ""
    echo "[skill-python-env] ── 环境就绪 ──────────────────────────────"
    echo "[skill-python-env] Python 版本：$PYTHON_VERSION"
    echo "[skill-python-env] 环境路径：$ENV_DIR"
    if [[ "$IS_WINDOWS" == true ]]; then
        echo "[skill-python-env] 激活（bash）：source \"$ACTIVATE_PATH\""
        echo "[skill-python-env] 激活（PS）  ：& \"$ENV_DIR\\Scripts\\Activate.ps1\""
    else
        echo "[skill-python-env] 激活命令：source \"$ACTIVATE_PATH\""
    fi
    echo "[skill-python-env] ─────────────────────────────────────────"
    # 机器可读行，供调用方脚本 grep 解析
    echo "PYTHON_ENV_ACTIVATE:$ACTIVATE_PATH"
    echo "PYTHON_ENV_DIR:$ENV_DIR"
    echo "PYTHON_ENV_VERSION:$PYTHON_VERSION"
}

# ── 主流程 ────────────────────────────────────────────────
main() {
    log_info "检查 Python $PYTHON_VERSION 共享环境"
    check_or_install_uv
    ensure_env
    install_packages
    print_result
}

main
