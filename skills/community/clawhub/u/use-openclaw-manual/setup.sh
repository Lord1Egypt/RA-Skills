#!/bin/bash
# setup.sh - use-openclaw-manual 技能配置脚本
# 基于相对路径设计，可在任何安装位置执行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "═══════════════════════════════════════════"
echo "  use-openclaw-manual 技能配置"
echo "═══════════════════════════════════════════"
echo ""

# ───────────────────────────────────────────────
# 1. 检查必需依赖
# ───────────────────────────────────────────────
echo "📋 检查依赖..."

missing_deps=()

if ! command -v git &> /dev/null; then
  missing_deps+=("git")
fi

if ! command -v curl &> /dev/null; then
  missing_deps+=("curl")
fi

if ! command -v python3 &> /dev/null; then
  missing_deps+=("python3")
fi

if [ ${#missing_deps[@]} -gt 0 ]; then
  echo "❌ 缺少必需依赖：${missing_deps[*]}"
  echo ""
  echo "请先安装："
  echo "   macOS:  brew install ${missing_deps[*]}"
  echo "   Ubuntu: sudo apt install ${missing_deps[*]}"
  exit 1
fi

echo "✅ 依赖检查通过 (git, curl, python3)"
echo ""

# ───────────────────────────────────────────────
# 2. 添加执行权限
# ───────────────────────────────────────────────
echo "🔐 配置执行权限..."

chmod +x "$SCRIPT_DIR/run.sh"
chmod +x "$SCRIPT_DIR/scripts/"*.sh

echo "✅ 已添加权限："
echo "   - run.sh"
echo "   - scripts/sync-docs.sh"
echo "   - scripts/search-docs.sh"
echo ""

# ───────────────────────────────────────────────
# 3. 初始化文档
# ───────────────────────────────────────────────
echo "📚 文档初始化"
echo ""

# 检查是否已初始化
if [ -f "$SCRIPT_DIR/.initialized" ]; then
  echo "ℹ️  检测到文档已初始化"
  echo ""
  read -p "是否重新初始化（覆盖现有文档）？(y/n) " -n 1 -r
  echo ""
  if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "⏭️  跳过文档初始化"
    echo ""
  else
    echo "🔄 重新初始化文档..."
    "$SCRIPT_DIR/run.sh" --init
  fi
else
  echo "首次使用需要下载 OpenClaw 官方文档（约 700+ 文件，~10MB）"
  echo ""
  read -p "是否现在初始化？(y/n) " -n 1 -r
  echo ""
  if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "📥 开始初始化文档..."
    echo ""
    "$SCRIPT_DIR/run.sh" --init
  else
    echo "⏭️  跳过文档初始化"
    echo "   稍后手动执行：./run.sh --init"
    echo ""
  fi
fi

# ───────────────────────────────────────────────
# 4. 完成
# ───────────────────────────────────────────────
echo ""
echo "═══════════════════════════════════════════"
echo "  配置完成！"
echo "═══════════════════════════════════════════"
echo ""
echo "📚 使用帮助："
echo "   ./run.sh --help"
echo "   ./run.sh --search \"cron\""
echo "   ./run.sh --sync"
echo ""
