#!/bin/bash
# 小红书热点发布技能上传到ClawHub的脚本
# 使用方法：bash publish_to_clawhub.sh

echo "🎯 开始上传小红书热点发布技能到ClawHub"
echo "=========================================="

# 检查clawhub是否安装
if ! command -v clawhub &> /dev/null; then
    echo "❌ ClawHub CLI未安装"
    echo "请先安装：npm i -g clawhub 或 pnpm add -g clawhub"
    exit 1
fi

echo "✅ ClawHub CLI已安装"

# 检查是否登录
echo "🔐 检查登录状态..."
if ! clawhub whoami &> /dev/null; then
    echo "⚠️  未登录，请先登录"
    echo "正在打开浏览器登录..."
    clawhub login
else
    echo "✅ 已登录"
fi

# 显示技能信息
echo ""
echo "📦 技能信息："
echo "   名称: 小红书热点半自动化发布系统"
echo "   Slug: xiaohongshu-hot-publish"
echo "   版本: 1.1.0"
echo "   路径: $(pwd)"
echo ""

# 显示文件夹内容
echo "📁 技能文件夹内容："
ls -la

echo ""
echo "📋 准备发布..."
echo ""

# 发布技能
echo "🚀 正在发布技能到ClawHub..."
clawhub publish . \
  --slug xiaohongshu-hot-publish \
  --name "小红书热点半自动化发布系统" \
  --version 1.1.0 \
  --changelog "优化版本：完整的文档、测试套件、使用示例、错误处理" \
  --tags "xiaohongshu,content-creation,automation,chinese,social-media,ai-tools"

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 技能发布成功！"
    echo ""
    echo "🔗 技能将在以下地址可用："
    echo "   https://clawhub.ai/skills/xiaohongshu-hot-publish"
    echo ""
    echo "📊 下一步："
    echo "   1. 访问 https://clawhub.ai 查看你的技能"
    echo "   2. 分享给其他OpenClaw用户"
    echo "   3. 收集反馈并更新版本"
else
    echo ""
    echo "❌ 发布失败，请检查错误信息"
    exit 1
fi

echo ""
echo "✨ 上传完成！"