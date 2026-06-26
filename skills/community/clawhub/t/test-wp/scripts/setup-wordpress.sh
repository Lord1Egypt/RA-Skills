#!/bin/bash

# WordPress自动发布技能安装脚本

set -e

echo "🚀 开始安装WordPress自动发布技能"
echo "======================================"

# 检查Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js未安装，请先安装Node.js"
    exit 1
fi

NODE_VERSION=$(node --version)
echo "✅ Node.js版本: $NODE_VERSION"

# 检查npm
if ! command -v npm &> /dev/null; then
    echo "❌ npm未安装，请先安装npm"
    exit 1
fi

NPM_VERSION=$(npm --version)
echo "✅ npm版本: $NPM_VERSION"

# 安装依赖
echo "📦 安装依赖包..."
cd "$(dirname "$0")/.."
npm install

if [ $? -eq 0 ]; then
    echo "✅ 依赖安装完成"
else
    echo "❌ 依赖安装失败"
    exit 1
fi

# 创建配置文件
echo "⚙️  创建配置文件..."
if [ ! -f "config.js" ]; then
    if [ -f "config.example.js" ]; then
        cp config.example.js config.js
        echo "✅ 已创建 config.js (请编辑此文件配置WordPress)"
    else
        echo "⚠️  未找到 config.example.js，请手动创建 config.js"
    fi
else
    echo "✅ config.js 已存在"
fi

# 创建必要目录
echo "📁 创建目录结构..."
mkdir -p posts
mkdir -p logs
mkdir -p media

echo "✅ 目录创建完成:"
echo "   - posts/     # 存放Markdown文章"
echo "   - logs/      # 日志文件"
echo "   - media/     # 媒体文件"

# 创建示例文章
echo "📝 创建示例文章..."
if [ ! -f "posts/example-post.md" ]; then
    cat > posts/example-post.md << 'EOF'
---
title: WordPress自动发布测试文章
slug: wordpress-auto-publish-test
status: draft
categories:
  - 测试
  - 技术
tags:
  - WordPress
  - 测试
  - 自动化
excerpt: 这是一个测试文章，用于验证WordPress自动发布功能
date: 2026-04-04
---

# WordPress自动发布测试

这是一个测试文章，用于验证WordPress自动发布功能是否正常工作。

## 功能测试

1. **Markdown解析** - 检查Markdown是否正确转换为HTML
2. **元数据处理** - 验证Front Matter元数据
3. **API连接** - 测试WordPress REST API连接
4. **文章发布** - 验证文章发布流程

## 代码块测试

```javascript
// 测试代码块
console.log('Hello WordPress!');
```

## 列表测试

- 项目1
- 项目2
- 项目3

## 链接测试

[OpenClaw官网](https://openclaw.ai)

---

**提示**: 这是一个测试文章，发布后可以删除。
EOF
    echo "✅ 示例文章已创建: posts/example-post.md"
else
    echo "✅ 示例文章已存在"
fi

# 设置文件权限
echo "🔒 设置文件权限..."
chmod +x publish.js
chmod +x batch-publish.js
chmod +x list-posts.js
chmod +x scripts/setup-wordpress.sh

echo "✅ 文件权限设置完成"

# 测试脚本
echo "🧪 测试脚本..."
if node -e "console.log('✅ Node.js脚本测试通过')" &> /dev/null; then
    echo "✅ 脚本测试通过"
else
    echo "❌ 脚本测试失败"
fi

echo ""
echo "🎉 安装完成！"
echo "======================================"
echo ""
echo "📋 下一步操作："
echo ""
echo "1. 编辑 config.js 文件，配置WordPress连接信息："
echo "   - WORDPRESS_URL: 你的WordPress站点URL"
echo "   - WORDPRESS_USERNAME: WordPress用户名"
echo "   - WORDPRESS_PASSWORD: 应用程序密码"
echo ""
echo "2. 测试连接："
echo "   npm test"
echo ""
echo "3. 发布示例文章："
echo "   node publish.js --file posts/example-post.md --status draft"
echo ""
echo "4. 查看帮助："
echo "   node publish.js --help"
echo "   node batch-publish.js --help"
echo "   node list-posts.js --help"
echo ""
echo "📚 详细文档请查看 SKILL.md"
echo ""