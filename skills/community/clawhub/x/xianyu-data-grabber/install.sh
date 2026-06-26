#!/bin/bash
# 闲鱼数据抓取技能 - 一键安装部署脚本
# 使用方法：复制此脚本内容，发送给 OpenClaw 执行

set -e

echo "🐾 闲鱼数据抓取技能 - 一键安装部署"
echo "========================================"
echo ""

WORKSPACE_DIR="$HOME/.openclaw/workspace"
SKILL_DIR="$WORKSPACE_DIR/skills/xianyu-data-grabber"
LOG_DIR="$WORKSPACE_DIR/logs"
DATA_DIR="$WORKSPACE_DIR/legion/data"
SCREENSHOT_DIR="$WORKSPACE_DIR/legion/screenshots"

# 创建目录
echo "📁 创建目录..."
mkdir -p "$SKILL_DIR" "$LOG_DIR" "$DATA_DIR" "$SCREENSHOT_DIR"
echo "✅ 目录创建完成"
echo ""

# 检查 Python
echo "🐍 检查 Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装，请先安装 Python3"
    exit 1
fi
PYTHON_VERSION=$(python3 --version)
echo "✅ $PYTHON_VERSION"
echo ""

# 检查 Node
echo "📦 检查 Node.js..."
if ! command -v node &> /dev/null; then
    echo "❌ Node.js 未安装，请先安装 Node.js"
    exit 1
fi
NODE_VERSION=$(node --version)
echo "✅ Node.js $NODE_VERSION"
echo ""

# 安装系统依赖
echo "🔧 安装系统依赖..."
if command -v apt-get &> /dev/null; then
    echo "正在安装 Tesseract OCR..."
    apt-get update -qq
    apt-get install -y -qq tesseract-ocr tesseract-ocr-chi-sim libtesseract-dev
    echo "✅ Tesseract 安装完成"
elif command -v yum &> /dev/null; then
    echo "正在安装 Tesseract OCR..."
    yum install -y tesseract tesseract-langpack-chi_sim
    echo "✅ Tesseract 安装完成"
else
    echo "⚠️  未知包管理器，请手动安装 tesseract-ocr"
fi
echo ""

# 安装 Python 依赖
echo "🐍 安装 Python 依赖..."
pip3 install pillow pytesseract opencv-python-headless --break-system-packages -q
echo "✅ Python 依赖安装完成"
echo ""

# 安装 Node 依赖
echo "📦 安装 Node 依赖..."
cd "$WORKSPACE_DIR"
npm install playwright --save -q
echo "✅ Playwright 安装完成"
echo ""

# 下载浏览器
echo "🌐 下载 Chromium 浏览器（约 100MB，需要 2-5 分钟）..."
npx playwright install chromium --quiet
echo "✅ Chromium 下载完成"
echo ""

# 创建配置文件
echo "📝 创建配置文件..."
cat > "$WORKSPACE_DIR/.xianyu-grabber-config.json" << 'EOF'
{
  "gitee": {
    "token": "",
    "owner": "",
    "repo": "xianyu-data"
  },
  "xianyu": {
    "cookie": ""
  },
  "grabber": {
    "keywords": ["Magisk", "KernelSU", "救砖", "刷机"],
    "screenshotDir": "legion/screenshots",
    "dataDir": "legion/data",
    "uploadToGitee": false,
    "ocrLanguage": "chi_sim+eng"
  }
}
EOF
echo "✅ 配置文件：~/.openclaw/workspace/.xianyu-grabber-config.json"
echo "⚠️  Gitee Token 和 Cookie 需手动配置（可选）"
echo ""

# 设置权限
echo "🔐 设置权限..."
chmod +x "$SKILL_DIR"/*.sh "$SKILL_DIR"/*.py 2>/dev/null || true
echo "✅ 权限设置完成"
echo ""

# 配置定时任务
echo "⏰ 配置定时任务..."
CRON_FILE="$WORKSPACE_DIR/xianyu-crontab.txt"
cat > "$CRON_FILE" << 'EOF'
# 闲鱼数据抓取定时任务
0 9 * * * cd ~/.openclaw/workspace && ./skills/xianyu-data-grabber/run.sh grab "Magisk" "KernelSU" "救砖" "刷机" >> logs/xianyu-cron.log 2>&1
0 10 * * 1 cd ~/.openclaw/workspace && ./skills/xianyu-data-grabber/run.sh grab-all >> logs/xianyu-cron.log 2>&1
0 15 * * * cd ~/.openclaw/workspace && python3 skills/xianyu-data-grabber/visualize.py >> logs/xianyu-visualize.log 2>&1
0 20 * * * cd ~/.openclaw/workspace && python3 skills/xianyu-data-grabber/recommend.py >> logs/xianyu-recommend.log 2>&1
0 2 * * * cd ~/.openclaw/workspace && ./skills/xianyu-data-grabber/run.sh clean >> logs/xianyu-clean.log 2>&1
EOF

# 尝试安装到系统 crontab
if command -v crontab &> /dev/null; then
    (crontab -l 2>/dev/null || true; cat "$CRON_FILE") | crontab -
    echo "✅ 定时任务已安装到系统 crontab"
else
    echo "⚠️  crontab 未安装，定时任务配置已保存：$CRON_FILE"
fi
echo ""

# 测试验证
echo "🧪 测试验证..."
echo "检查技能文件..."
if [ -f "$SKILL_DIR/run.sh" ] && [ -f "$SKILL_DIR/grabber-enhanced.js" ] && [ -f "$SKILL_DIR/visualize.py" ]; then
    echo "✅ 技能文件完整"
else
    echo "❌ 技能文件不完整"
    exit 1
fi

echo "检查 Tesseract..."
if tesseract --version &> /dev/null; then
    echo "✅ Tesseract 已安装"
else
    echo "❌ Tesseract 未安装"
    exit 1
fi

echo "检查 Playwright..."
if node -e "require('playwright')" 2>/dev/null; then
    echo "✅ Playwright 已安装"
else
    echo "❌ Playwright 未安装"
    exit 1
fi
echo ""

# 显示使用指南
echo "========================================"
echo "🎉 安装完成！"
echo ""
echo "📚 使用指南:"
echo ""
echo "# 查看技能状态"
echo "./skills/xianyu-data-grabber/run.sh status"
echo ""
echo "# 抓取数据（示例）"
echo "./skills/xianyu-data-grabber/run.sh grab \"Magisk\" \"KernelSU\""
echo ""
echo "# 抓取所有 60+ 关键词"
echo "./skills/xianyu-data-grabber/run.sh grab-all"
echo ""
echo "# 生成可视化图表"
echo "./skills/xianyu-data-grabber/run.sh visualize"
echo ""
echo "# 生成智能推荐"
echo "./skills/xianyu-data-grabber/run.sh recommend"
echo ""
echo "# 查看帮助"
echo "./skills/xianyu-data-grabber/run.sh help"
echo ""
echo "========================================"
echo "📝 可选配置:"
echo ""
echo "1. 配置 Gitee（自动上传数据）:"
echo "   编辑：~/.openclaw/workspace/.xianyu-grabber-config.json"
echo "   填入 Gitee Token、用户名、仓库名"
echo ""
echo "2. 配置闲鱼 Cookie（提高抓取成功率）:"
echo "   编辑：~/.openclaw/workspace/.xianyu-grabber-config.json"
echo "   填入 Cookie 字符串"
echo ""
echo "========================================"
echo "📄 文档位置:"
echo "   - 技能文档：skills/xianyu-data-grabber/SKILL.md"
echo "   - 使用说明：skills/xianyu-data-grabber/USAGE.md"
echo "   - 功能清单：skills/xianyu-data-grabber/FEATURES.md"
echo ""
echo "========================================"
echo "👋 安装完成，可以直接使用了！"
