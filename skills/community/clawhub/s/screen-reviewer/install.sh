#!/bin/bash
# screen-reviewer 一键安装脚本
# 从 GitHub 仓库安装到本地，创建 symlink 让各 Agent 自动发现
set -e

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
DATA_DIR="$HOME/.screen-reviewer"
VENV_DIR="$DATA_DIR/venv"
CURSOR_SKILL="$HOME/.cursor/skills/screen-reviewer"
CODEX_SKILL="$HOME/.codex/skills/screen-reviewer"

echo "╔══════════════════════════════════════╗"
echo "║   screen-reviewer 一键安装           ║"
echo "╚══════════════════════════════════════╝"

# ── 1. 创建数据目录 ──────────────────────────
echo ""
echo "[1/6] 创建数据目录..."
mkdir -p "$DATA_DIR"/{screenshots,logs,reports}
echo "  ✅ $DATA_DIR"

# ── 2. Python 虚拟环境 ───────────────────────
echo ""
echo "[2/6] 创建 Python 虚拟环境..."
if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
fi
source "$VENV_DIR/bin/activate"
pip install --upgrade pip -q
pip install -r "$REPO_DIR/scripts/requirements.txt" -q
echo "  ✅ 依赖安装完成"

# ── 3. 编译 Swift OCR 工具 ───────────────────
echo ""
echo "[3/6] 编译 macOS OCR 工具..."
if command -v swiftc &> /dev/null; then
    swiftc -O -o "$REPO_DIR/scripts/ocr_tool" "$REPO_DIR/scripts/ocr_tool.swift" 2>/dev/null && \
        echo "  ✅ OCR 工具编译成功" || \
        echo "  ⚠️  编译失败（不影响核心功能，OCR 将使用备选方案）"
else
    echo "  ⚠️  未找到 swiftc，如需 OCR 请运行: xcode-select --install"
fi

# ── 4. 初始化默认配置 ────────────────────────
echo ""
echo "[4/6] 初始化配置..."
cd "$REPO_DIR/scripts"
"$VENV_DIR/bin/python" -c "from config import load_config; load_config()"
echo "  ✅ $DATA_DIR/config.yaml"

deactivate

# ── 5. 注册 Cursor Skill ────────────────────
echo ""
echo "[5/6] 注册 Agent Skill..."
mkdir -p "$(dirname "$CURSOR_SKILL")"
rm -rf "$CURSOR_SKILL"
ln -sfn "$REPO_DIR" "$CURSOR_SKILL"
echo "  ✅ Cursor: $CURSOR_SKILL"

# ── 6. 注册 Codex Skill ─────────────────────
mkdir -p "$(dirname "$CODEX_SKILL")"
rm -rf "$CODEX_SKILL"
ln -sfn "$REPO_DIR" "$CODEX_SKILL"
echo "  ✅ Codex:  $CODEX_SKILL"

echo ""
echo "╔══════════════════════════════════════╗"
echo "║   安装完成！                          ║"
echo "╚══════════════════════════════════════╝"
echo ""
echo "用法:"
echo "  启动监控:  $VENV_DIR/bin/python $REPO_DIR/scripts/service_manager.py start"
echo "  查看状态:  $VENV_DIR/bin/python $REPO_DIR/scripts/service_manager.py status"
echo "  暂停/恢复: $VENV_DIR/bin/python $REPO_DIR/scripts/service_manager.py pause|resume"
echo "  生成报告:  $VENV_DIR/bin/python $REPO_DIR/scripts/service_manager.py report"
echo "  开机自启:  $VENV_DIR/bin/python $REPO_DIR/scripts/service_manager.py install"
echo ""
echo "⚠️  首次截图请授权 macOS 屏幕录制权限:"
echo "   系统设置 → 隐私与安全性 → 屏幕录制 → 勾选 Terminal"
echo ""
echo "📝 配置: $DATA_DIR/config.yaml"
