#!/bin/bash
# 闲鱼数据上传到 Gitee 脚本

set -e

DATA_DIR="${1:-legion/data}"
REPORT_FILE="${2:-legion/data/xianyu-summary.md}"
CONFIG_FILE="$HOME/.openclaw/workspace/.xianyu-grabber-config.json"

# 加载配置
GITEE_TOKEN=$(jq -r '.gitee.token' "$CONFIG_FILE" 2>/dev/null)
GITEE_OWNER=$(jq -r '.gitee.owner' "$CONFIG_FILE" 2>/dev/null)
GITEE_REPO=$(jq -r '.gitee.repo' "$CONFIG_FILE" 2>/dev/null)

if [ -z "$GITEE_TOKEN" ] || [ -z "$GITEE_OWNER" ] || [ -z "$GITEE_REPO" ]; then
    echo "❌ Gitee 配置不完整，请检查 $CONFIG_FILE"
    exit 1
fi

echo "📤 上传到 Gitee: $GITEE_OWNER/$GITEE_REPO"

# 创建临时目录
TEMP_DIR=$(mktemp -d)
cd "$TEMP_DIR"

# 克隆仓库（如果不存在则初始化）
if [ ! -d ".git" ]; then
    git init
    git remote add origin "https://gitee.com/$GITEE_OWNER/$GITEE_REPO.git"
fi

# 创建目录结构
mkdir -p data screenshots reports

# 复制文件
cp "$DATA_DIR"/*.json data/ 2>/dev/null || true
cp "$DATA_DIR"/../screenshots/*.png screenshots/ 2>/dev/null || true
cp "$REPORT_FILE" reports/ 2>/dev/null || true

# 生成 README
cat > README.md << EOF
# 闲鱼数据仓库

自动抓取的闲鱼商品数据。

## 目录结构

- \`data/\` - JSON 格式原始数据
- \`screenshots/\` - 搜索页面截图
- \`reports/\` - 分析报告

## 数据格式

每个关键词对应一个 JSON 文件，包含：
- keyword: 搜索关键词
- products: 商品列表（标题、价格、想要人数等）
- timestamp: 抓取时间

## 更新记录

EOF

echo "- $(date '+%Y-%m-%d %H:%M:%S'): 更新数据" >> README.md

# Git 操作
git add -A
git commit -m "auto: 更新闲鱼数据 $(date '+%Y-%m-%d %H:%M')" || echo "无变更"

# 推送到 Gitee
git push -f "https://$GITEE_TOKEN@gitee.com/$GITEE_OWNER/$GITEE_REPO.git" main || \
git push -f "https://$GITEE_TOKEN@gitee.com/$GITEE_OWNER/$GITEE_REPO.git" master || \
echo "⚠️ 推送失败，请检查仓库是否存在"

# 清理
cd -
rm -rf "$TEMP_DIR"

echo "✅ 上传完成"
