#!/bin/bash
# Skill Usage Analyzer 安装脚本

set -e

echo "🔍 安装 Skill Usage Analyzer..."

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 需要 Python 3"
    exit 1
fi

# 检查 OpenClaw 技能目录
SKILLS_DIR="${HOME}/.openclaw/workspace/skills"
if [ ! -d "$SKILLS_DIR" ]; then
    echo "⚠️  警告: OpenClaw 技能目录不存在: $SKILLS_DIR"
    echo "   将安装到当前目录"
    SKILLS_DIR="."
fi

# 确定安装路径
INSTALL_DIR="${SKILLS_DIR}/skill-usage-analyzer"

# 如果已存在，询问是否覆盖
if [ -d "$INSTALL_DIR" ]; then
    echo "⚠️  skill-usage-analyzer 已存在"
    read -p "是否覆盖? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ 安装取消"
        exit 0
    fi
    rm -rf "$INSTALL_DIR"
fi

# 创建目录
mkdir -p "$INSTALL_DIR"
mkdir -p "$INSTALL_DIR/scripts"

# 复制文件
echo "📦 复制文件..."
cp -r scripts/*.py "$INSTALL_DIR/scripts/"
cp SKILL.md "$INSTALL_DIR/"
cp README.md "$INSTALL_DIR/" 2>/dev/null || true
cp LICENSE "$INSTALL_DIR/" 2>/dev/null || true
cp CHANGELOG.md "$INSTALL_DIR/" 2>/dev/null || true
cp package.json "$INSTALL_DIR/" 2>/dev/null || true

# 设置权限
chmod +x "$INSTALL_DIR/scripts/"*.py

echo "✅ 安装完成!"
echo ""
echo "📍 安装位置: $INSTALL_DIR"
echo ""
echo "🚀 快速开始:"
echo "  cd $INSTALL_DIR"
echo "  python3 scripts/analyze_skill.py /path/to/skill/SKILL.md"
echo ""
echo "💡 常用命令:"
echo "  python3 scripts/creative_usage.py <技能名>     # 获取创意用法"
echo "  python3 scripts/find_combinations.py            # 发现技能组合"
echo "  python3 scripts/recommend_skill.py '<任务描述>' # 智能推荐"
echo "  python3 scripts/compare_matrix.py <技能1> <技能2> # 对比技能"
echo "  python3 scripts/analyze_all.py                  # 分析所有技能"
