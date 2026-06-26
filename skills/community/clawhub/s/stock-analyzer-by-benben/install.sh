#!/bin/bash
# 安装 stock-analyzer 技能

# 获取技能所在目录（脚本所在目录）
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "📈 正在安装 stock-analyzer..."

# 复制文件到 OpenClaw 技能目录
mkdir -p ~/.openclaw/skills/stock-analyzer
cp -r "$SKILL_DIR/source/"* ~/.openclaw/skills/stock-analyzer/
cp "$SKILL_DIR/SKILL.md" ~/.openclaw/skills/stock-analyzer/
cp "$SKILL_DIR/skill.json" ~/.openclaw/skills/stock-analyzer/

# 设置可执行权限
if [ -f ~/.openclaw/skills/stock-analyzer/stock_analyzer.py ]; then
    chmod +x ~/.openclaw/skills/stock-analyzer/stock_analyzer.py
fi

# 检查 Python 依赖
echo "🔍 检查 Python 依赖..."
python3 -c "import yfinance" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  需要安装依赖库"
    echo "运行: pip install yfinance pandas numpy matplotlib scikit-learn"
fi

echo "✅ 安装完成！"
echo "使用方法: stock-analyzer --help"
echo ""
echo "示例:"
echo "  stock-analyzer analyze --symbol AAPL"
echo "  stock-analyzer fundamentals --symbol 600519.SS"
echo "  stock-analyzer predict --symbol AAPL --days 5"