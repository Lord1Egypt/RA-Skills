#!/bin/bash

# Video Frame Extractor 诊断脚本
# 用于检查安装状态和常见问题

echo "🔍 Video Frame Extractor 诊断工具"
echo "================================"
echo ""

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查函数
check_pass() {
    echo -e "${GREEN}✅ $1${NC}"
}

check_fail() {
    echo -e "${RED}❌ $1${NC}"
}

check_warn() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

check_info() {
    echo -e "ℹ️  $1"
}

# 1. 检查 Python
echo "📦 检查 Python 环境"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    check_pass "Python 3 已安装: $PYTHON_VERSION"

    # 检查 Python 版本是否 >= 3.8
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

    if [ "$PYTHON_MAJOR" -ge 3 ] && [ "$PYTHON_MINOR" -ge 8 ]; then
        check_pass "Python 版本符合要求 (>= 3.8)"
    else
        check_fail "Python 版本过低，需要 >= 3.8"
    fi
else
    check_fail "Python 3 未安装"
fi
echo ""

# 2. 检查 PATH 配置
echo "🔧 检查 PATH 配置"
if echo "$PATH" | grep -q "$HOME/.local/bin"; then
    check_pass "~/.local/bin 已在 PATH 中"
else
    check_warn "~/.local/bin 不在 PATH 中"
    check_info "请运行: echo 'export PATH=\"\$HOME/.local/bin:\$PATH\"' >> ~/.zshrc && source ~/.zshrc"
fi
echo ""

# 3. 检查 frame-extractor 命令
echo "🎬 检查 frame-extractor 命令"
if command -v frame-extractor &> /dev/null; then
    FRAME_EXTRACTOR_PATH=$(which frame-extractor)
    check_pass "frame-extractor 命令存在: $FRAME_EXTRACTOR_PATH"

    # 检查可执行权限
    if [ -x "$FRAME_EXTRACTOR_PATH" ]; then
        check_pass "frame-extractor 有执行权限"
    else
        check_fail "frame-extractor 缺少执行权限"
        check_info "请运行: chmod +x $FRAME_EXTRACTOR_PATH"
    fi

    # 尝试运行版本命令
    echo ""
    check_info "尝试运行 frame-extractor -v..."
    if frame-extractor -v &> /dev/null; then
        VERSION=$(frame-extractor -v 2>&1 | head -n 1)
        check_pass "frame-extractor 运行正常"
        check_info "版本信息: $VERSION"
    else
        check_fail "frame-extractor 运行失败"
        check_info "可能缺少依赖或 Python 环境"
    fi
else
    check_fail "frame-extractor 命令不存在"
    check_info "请运行安装脚本: curl -sSL https://raw.githubusercontent.com/indulgeback/video-frame-extractor/main/install.sh | bash"
fi
echo ""

# 4. 检查安装目录
echo "📁 检查安装目录"
INSTALL_DIR="$HOME/.video-frame-extractor"
if [ -d "$INSTALL_DIR" ]; then
    check_pass "安装目录存在: $INSTALL_DIR"

    # 检查关键文件
    if [ -f "$INSTALL_DIR/frame-extractor.py" ]; then
        check_pass "frame-extractor.py 存在"
    else
        check_fail "frame-extractor.py 不存在"
    fi

    # 检查虚拟环境
    if [ -d "$INSTALL_DIR/venv" ]; then
        check_pass "Python 虚拟环境存在"

        # 检查 Python 可执行文件
        if [ -f "$INSTALL_DIR/venv/bin/python" ]; then
            check_pass "虚拟环境 Python 可执行文件存在"
        else
            check_fail "虚拟环境 Python 可执行文件不存在"
        fi
    else
        check_warn "Python 虚拟环境不存在"
        check_info "请运行: cd $INSTALL_DIR && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    fi
else
    check_fail "安装目录不存在: $INSTALL_DIR"
    check_info "请运行安装脚本"
fi
echo ""

# 5. 检查依赖
echo "📚 检查 Python 依赖"
if [ -d "$INSTALL_DIR/venv" ]; then
    check_info "检查已安装的包..."

    # 尝试激活虚拟环境并检查依赖
    if source "$INSTALL_DIR/venv/bin/activate" 2>/dev/null; then
        # 检查 PyAV
        if python3 -c "import av" 2>/dev/null; then
            AV_VERSION=$(python3 -c "import av; print(av.__version__)" 2>/dev/null)
            check_pass "PyAV 已安装 (版本: $AV_VERSION)"
        else
            check_fail "PyAV 未安装"
            check_info "请运行: pip install av"
        fi

        # 检查 tqdm
        if python3 -c "import tqdm" 2>/dev/null; then
            TQDM_VERSION=$(python3 -c "import tqdm; print(tqdm.__version__)" 2>/dev/null)
            check_pass "tqdm 已安装 (版本: $TQDM_VERSION)"
        else
            check_fail "tqdm 未安装"
            check_info "请运行: pip install tqdm"
        fi

        # 检查 Pillow
        if python3 -c "import PIL" 2>/dev/null; then
            PILLOW_VERSION=$(python3 -c "from PIL import Image; print(Image.__version__)" 2>/dev/null)
            check_pass "Pillow 已安装 (版本: $PILLOW_VERSION)"
        else
            check_fail "Pillow 未安装"
            check_info "请运行: pip install Pillow"
        fi

        deactivate 2>/dev/null
    else
        check_fail "无法激活虚拟环境"
    fi
else
    check_warn "虚拟环境不存在，跳过依赖检查"
fi
echo ""

# 6. 检查 FFmpeg（PyAV 内置，但检查系统 FFmpeg 也有用）
echo "🎥 检查 FFmpeg"
if command -v ffmpeg &> /dev/null; then
    FFMPEG_VERSION=$(ffmpeg -version 2>&1 | head -n 1)
    check_pass "FFmpeg 已安装"
    check_info "$FFMPEG_VERSION"
else
    check_warn "系统 FFmpeg 未安装（PyAV 内置 FFmpeg，通常不需要）"
    check_info "如果遇到 FFmpeg 相关错误，可以安装:"
    check_info "  macOS: brew install ffmpeg"
    check_info "  Ubuntu: sudo apt-get install ffmpeg"
fi
echo ""

# 7. 测试基本功能
echo "🧪 测试基本功能"
if command -v frame-extractor &> /dev/null; then
    check_info "测试 frame-extractor -v..."
    if frame-extractor -v &> /dev/null; then
        check_pass "版本命令测试通过"
    else
        check_fail "版本命令测试失败"
    fi
else
    check_warn "frame-extractor 不可用，跳过功能测试"
fi
echo ""

# 8. 总结
echo "================================"
echo "📊 诊断总结"
echo ""
echo "如果所有检查都通过，frame-extractor 应该可以正常使用。"
echo ""
echo "如果遇到问题，请参考以下解决方案："
echo ""
echo "1. 重新安装工具："
echo "   curl -sSL https://raw.githubusercontent.com/indulgeback/video-frame-extractor/main/install.sh | bash"
echo ""
echo "2. 手动修复依赖："
echo "   cd ~/.video-frame-extractor"
echo "   source venv/bin/activate"
echo "   pip install -r requirements.txt"
echo ""
echo "3. 检查 PATH："
echo "   echo 'export PATH=\"\$HOME/.local/bin:\$PATH\"' >> ~/.zshrc"
echo "   source ~/.zshrc"
echo ""
echo "4. 如果仍有问题，请访问："
echo "   https://github.com/indulgeback/video-frame-extractor/issues"
echo ""
