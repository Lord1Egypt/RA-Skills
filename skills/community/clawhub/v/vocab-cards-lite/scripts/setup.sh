#!/usr/bin/env bash
# setup.sh — 安装 vocab-cards-lite 的 Python 依赖并校验字体可用性。
# 用法:
#   bash setup.sh                     # 优先使用 venv;系统 Python 受 PEP 668 保护时给出指引
#   bash setup.sh --allow-global      # 显式确认后,才允许安装到系统 Python(需自担风险)
#   bash setup.sh --venv [路径]       # 在指定路径(默认 ./.venv)创建虚拟环境并安装
set -euo pipefail

cd "$(dirname "$0")/.."

ALLOW_GLOBAL=0
VENV_DIR=""
while [ $# -gt 0 ]; do
    case "$1" in
        --allow-global) ALLOW_GLOBAL=1; shift ;;
        --venv) VENV_DIR="${2:-.venv}"; shift 2 ;;
        *) echo "!! 未知参数: $1 (支持: --allow-global / --venv [路径])"; exit 2 ;;
    esac
done

echo "==> 安装 Python 依赖 (pillow / fonttools / qrcode[pil])"

# 判断 pip 命令
if command -v pip3 >/dev/null 2>&1; then
    PIP_CMD="pip3"
elif command -v pip >/dev/null 2>&1; then
    PIP_CMD="pip"
else
    PIP_CMD="python3 -m pip"
fi

# 1) 用户显式要求 venv
if [ -n "$VENV_DIR" ]; then
    echo "   创建虚拟环境: $VENV_DIR"
    python3 -m venv "$VENV_DIR"
    # shellcheck disable=SC1091
    source "$VENV_DIR/bin/activate"
    echo "   虚拟环境中安装依赖..."
    python3 -m pip install -r requirements.txt
    echo "   完成(venv: $VENV_DIR)。后续使用: source $VENV_DIR/bin/activate"
    exit 0
fi

# 2) 已在虚拟环境中(有 VIRTUAL_ENV 或 .venv 存在且激活)
if [ -n "${VIRTUAL_ENV:-}" ] || [ -f ".venv/bin/activate" ]; then
    echo "   检测到虚拟环境,直接安装..."
    if [ -n "${VIRTUAL_ENV:-}" ]; then
        "$PIP_CMD" install -r requirements.txt
    else
        # shellcheck disable=SC1091
        source .venv/bin/activate
        python3 -m pip install -r requirements.txt
    fi
    echo "   完成。"
    exit 0
fi

# 3) 尝试普通安装(尊重系统 Python 的 PEP 668 保护)
if "$PIP_CMD" install -r requirements.txt 2>/tmp/vocab_pip_err.txt; then
    echo "   依赖安装完成。"
else
    if grep -qi "externally-managed-environment" /tmp/vocab_pip_err.txt; then
        if [ "$ALLOW_GLOBAL" -eq 1 ]; then
            echo "   用户显式确认(--allow-global),绕过 PEP 668 安装到系统 Python..."
            "$PIP_CMD" install --break-system-packages -r requirements.txt
        else
            echo ""
            echo "!! 系统 Python 受 PEP 668 保护(externally-managed-environment),禁止直接安装。"
            echo "   为保护你的系统环境,本脚本不会自动绕过该保护。请选择以下任一方式:"
            echo ""
            echo "   A. 推荐: 使用虚拟环境"
            echo "      bash setup.sh --venv .venv"
            echo "      或: python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt"
            echo ""
            echo "   B. 自担风险: 显式允许安装到系统 Python"
            echo "      bash setup.sh --allow-global"
            echo "      (等效于 pip install --break-system-packages -r requirements.txt)"
            echo ""
            exit 1
        fi
    else
        echo "!! 安装失败,错误信息:"
        cat /tmp/vocab_pip_err.txt
        exit 1
    fi
fi

echo "==> 校验包内 IPA 字体(裁剪版)"
missing=0
for f in \
    assets/fonts/DejaVuSans.ttf \
    assets/fonts/DejaVuSans-Bold.ttf; do
    if [ -f "$f" ]; then
        echo "   OK  $f"
    else
        echo "   MISS $f"
        missing=1
    fi
done

if [ "$missing" -ne 0 ]; then
    echo "!! 缺少包内 IPA 字体。请确认 assets/fonts/ 下有 DejaVuSans.ttf 与 DejaVuSans-Bold.ttf。"
    exit 1
fi

echo "==> 检测系统字体(lite 版中/英文依赖系统字体)"
sys_missing=0

# 逐个路径检测,任一存在即视为该字体可用(避免多行 ls 一错全错)
any_exists() {
    local f
    for f in "$@"; do
        [ -f "$f" ] && return 0
    done
    return 1
}

# 中文: NotoSansCJK(.ttc/.ttf 任一)
if any_exists \
    /usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc \
    /usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttf \
    /usr/share/fonts/noto/NotoSansCJK-Regular.ttc \
    /usr/local/share/fonts/NotoSansCJK-Regular.ttc \
    "$HOME/.local/share/fonts/NotoSansCJK-Regular.ttc"; then
    echo "   OK  NotoSansCJK(中文)"
else
    echo "   MISS NotoSansCJK(中文系统字体)"
    sys_missing=1
fi

# 英文: DejaVuSans
if any_exists \
    /usr/share/fonts/truetype/dejavu/DejaVuSans.ttf \
    /usr/share/fonts/dejavu/DejaVuSans.ttf \
    "$HOME/.local/share/fonts/DejaVuSans.ttf"; then
    echo "   OK  DejaVuSans(英文)"
else
    echo "   MISS DejaVuSans(英文系统字体)"
    sys_missing=1
fi

if [ "$sys_missing" -ne 0 ]; then
    echo ""
    echo "!! 缺少系统字体,请按你的发行版安装:"
    echo "   Ubuntu/Debian : sudo apt install fonts-noto-cjk fonts-dejavu"
    echo "   CentOS/RHEL   : sudo yum install google-noto-sans-cjk-fonts dejavu-sans-fonts"
    echo "   macOS         : 系统已自带;如需 Noto 可 brew install --cask font-noto-sans-cjk"
    echo "   (或改用内置完整字体的 vocab-cards-pro,开箱即用)"
    exit 1
fi

echo "==> 验证依赖可导入"
python3 -c "import PIL, fontTools, qrcode; print('   全部依赖就绪 ✓')"

echo ""
echo "完成。快速验证(自带示例):"
echo "  python3 scripts/vocab_cards.py examples/sample.json /tmp/vocab_demo"
