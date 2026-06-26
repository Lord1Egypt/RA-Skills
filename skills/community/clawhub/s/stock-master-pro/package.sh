#!/bin/bash

# Stock Master Pro 打包脚本
# 用于打包技能以上传到 ClawHub

set -e

SKILL_NAME="stock-master-pro"
VERSION="0.0.1"
WORKSPACE="$HOME/.openclaw/workspace/skills/$SKILL_NAME"
BUILD_DIR="$WORKSPACE/build"
PACKAGE_FILE="$WORKSPACE/${SKILL_NAME}-v${VERSION}.tar.gz"

echo "🔧 开始打包 $SKILL_NAME v$VERSION..."

# 清理旧的构建目录
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"

# 复制必要文件
echo "📦 复制文件..."
cp -r "$WORKSPACE"/* "$BUILD_DIR/"

# 删除不需要打包的文件
echo "🗑️ 清理临时文件..."
rm -rf "$BUILD_DIR/build"
rm -rf "$BUILD_DIR/stocks"  # 用户数据不打包
rm -f "$BUILD_DIR/web/stocks"  # 符号链接不打包
rm -rf "$BUILD_DIR/.git"
rm -f "$BUILD_DIR/*.log"
rm -f "$BUILD_DIR/web/test*.html"
rm -f "$BUILD_DIR/web/diag.html"

# 创建示例持仓文件
echo "📝 创建示例配置..."
cat > "$BUILD_DIR/stocks/holdings.example.json" << 'EOF'
{
  "stocks": [
    {
      "code": "000531.SZ",
      "name": "穗恒运 A",
      "cost": 7.15,
      "position": 500,
      "notes": "趋势票，电力概念"
    }
  ]
}
EOF

# 创建空的 stocks 目录
mkdir -p "$BUILD_DIR/stocks"
cp "$BUILD_DIR/stocks/holdings.example.json" "$BUILD_DIR/stocks/holdings.json.example"

# 创建 README（如果不存在）
if [ ! -f "$BUILD_DIR/README.md" ]; then
  cat > "$BUILD_DIR/README.md" << 'EOF'
# Stock Master Pro

基于 QVeris AI 的 A 股实时持仓监控与深度复盘系统。

## 快速开始

1. 安装 QVeris: `skillhub install qveris`
2. 配置 API Key
3. 编辑 `stocks/holdings.json` 添加持仓
4. 运行复盘脚本或启动 Web Dashboard

## 文档

- [安装指南](INSTALL.md)
- [使用指南](USAGE_GUIDE.md)
- [Web Dashboard](WEB_DASHBOARD_SUMMARY.md)

## 功能

- 📊 三时段复盘（午盘/尾盘/收盘）
- 🔥 板块深度分析（为什么涨、持续性评级）
- ⭐ 强势股评分推荐（100 分制 + 推荐理由）
- 💰 持仓监控（主力意图、目标价/止损价）
- 🐉 龙虎榜监控
- 🖥️ Web Dashboard（专业金融终端风格）

## 依赖

- QVeris AI（必需）
- Node.js 18+

## License

MIT
EOF
fi

# 打包
echo "📦 创建压缩包..."
cd "$BUILD_DIR"
tar -czf "$PACKAGE_FILE" ./*

# 显示打包结果
echo ""
echo "✅ 打包完成！"
echo ""
echo "📦 压缩包：$PACKAGE_FILE"
echo "📊 文件大小：$(du -h "$PACKAGE_FILE" | cut -f1)"
echo ""
echo "📋 上传到 ClawHub:"
echo "   1. 访问 https://clawhub.com/skills/create"
echo "   2. 上传 $PACKAGE_FILE"
echo "   3. 填写技能信息（参考 _meta.json）"
echo ""
echo "🔗 QVeris 分享链接:"
echo "   https://clawhub.com/skills/qveris?ref=stock-master-pro"
echo ""

# 清理构建目录
# rm -rf "$BUILD_DIR"

echo "✨ 完成！"
