#!/bin/bash

# Workday Calculator Skill 安装脚本
# 适用于 OpenClaw 技能安装

set -e

echo "=========================================="
echo " Workday Calculator Skill 安装脚本"
echo "=========================================="

# 检查Python版本
echo "🔍 检查Python版本..."
python3 --version || {
    echo "❌ 未找到Python3，请先安装Python3"
    exit 1
}

# 检查是否在OpenClaw环境
echo "🔍 检查OpenClaw环境..."
if [ -d "/usr/lib/node_modules/openclaw" ] || [ -d "$HOME/.openclaw" ]; then
    echo "✅ 检测到OpenClaw环境"
else
    echo "⚠️  未检测到OpenClaw环境，继续安装..."
fi

# 确定安装目录
if [ -d "$HOME/.openclaw/workspace/skills" ]; then
    INSTALL_DIR="$HOME/.openclaw/workspace/skills/workday-calculator"
elif [ -d "/usr/lib/node_modules/openclaw/skills" ]; then
    INSTALL_DIR="/usr/lib/node_modules/openclaw/skills/workday-calculator"
else
    INSTALL_DIR="./workday-calculator-install"
    echo "⚠️  使用当前目录安装: $INSTALL_DIR"
fi

echo "📁 安装目录: $INSTALL_DIR"

# 创建目录
echo "📁 创建目录..."
mkdir -p "$INSTALL_DIR"

# 复制文件
echo "📄 复制文件..."
cp -r scripts/ "$INSTALL_DIR/" 2>/dev/null || {
    echo "❌ 复制scripts目录失败"
    exit 1
}

cp SKILL.md "$INSTALL_DIR/" 2>/dev/null || echo "⚠️  复制SKILL.md失败"
cp README.md "$INSTALL_DIR/" 2>/dev/null || echo "⚠️  复制README.md失败"
cp _meta.json "$INSTALL_DIR/" 2>/dev/null || echo "⚠️  复制_meta.json失败"
cp LICENSE "$INSTALL_DIR/" 2>/dev/null || echo "⚠️  复制LICENSE失败"
cp package.json "$INSTALL_DIR/" 2>/dev/null || echo "⚠️  复制package.json失败"

# 创建.clawhub目录
echo "📁 创建.clawhub配置..."
mkdir -p "$INSTALL_DIR/.clawhub"
cp .clawhub/origin.json "$INSTALL_DIR/.clawhub/" 2>/dev/null || {
    # 如果不存在，创建一个
    cat > "$INSTALL_DIR/.clawhub/origin.json" << EOF
{
  "version": 1,
  "registry": "https://clawhub.ai",
  "slug": "workday-calculator",
  "installedVersion": "1.0.0",
  "installedAt": $(date +%s)000,
  "source": "manual"
}
EOF
}

# 设置权限
echo "🔒 设置文件权限..."
chmod +x "$INSTALL_DIR/scripts/workday_calculator.py" 2>/dev/null || true
chmod +x "$INSTALL_DIR/scripts/update_holidays.py" 2>/dev/null || true
chmod +x "$INSTALL_DIR/scripts/example_usage.py" 2>/dev/null || true

# 测试安装
echo "🧪 测试安装..."
cd "$INSTALL_DIR"
if python3 scripts/workday_calculator.py --version >/dev/null 2>&1; then
    echo "✅ 测试成功"
else
    echo "⚠️  测试失败，但安装继续"
fi

echo ""
echo "=========================================="
echo "🎉 安装完成！"
echo "=========================================="
echo ""
echo "📋 使用说明:"
echo "1. 基本使用:"
echo "   cd $INSTALL_DIR"
echo "   python3 scripts/workday_calculator.py 2025-01-01 2025-01-31"
echo ""
echo "2. 查看详细信息:"
echo "   python3 scripts/workday_calculator.py 2026-02-01 2026-02-28 --details"
echo ""
echo "3. 更新节假日:"
echo "   python3 scripts/update_holidays.py"
echo ""
echo "4. 查看示例:"
echo "   python3 scripts/example_usage.py"
echo ""
echo "5. 在OpenClaw中使用:"
echo "   当用户询问'工作日计算'、'节假日'等问题时，技能会自动触发"
echo ""
echo "📌 重要提示:"
echo "- 节假日数据需要每年更新"
echo "- 使用 update_holidays.py 工具更新数据"
echo "- 最权威的信息来源是中国政府网 (www.gov.cn)"
echo ""
echo "🔗 文档: $INSTALL_DIR/README.md"
echo "📧 联系: hunterxysy@126.com"
echo ""
echo "=========================================="
echo "感谢使用 Workday Calculator Skill！"
echo "=========================================="