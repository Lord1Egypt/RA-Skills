#!/bin/bash
# GitHub Release Script for UniSkill V4

echo "🚀 UniSkill V4 GitHub Release"
echo "=============================="

# 初始化git
git init
git config user.email "miscaodd@gmail.com"
git config user.name "Timo"

# 添加所有文件
git add .
git commit -m "UniSkill V4.0.0 - The 3% Solution

- 260 lines of core code (97% reduction from V2)
- Socratic Engine for requirement anchoring
- High-speed async multi-model debate
- Memory-safe, 8C8G optimized

Author: Timo (miscaodd@gmail.com) + Beaver"

# 创建标签
git tag -a v4.0.0 -m "UniSkill V4.0.0 Release"

echo ""
echo "✅ Git仓库已初始化"
echo ""
echo "下一步操作："
echo "1. 创建GitHub仓库: https://github.com/new"
echo "   仓库名: uniskill-v4"
echo "   描述: Minimalist AI Agent Framework - The 3% Solution"
echo ""
echo "2. 推送代码:"
echo "   git remote add origin https://github.com/timo/uniskill-v4.git"
echo "   git push -u origin main"
echo "   git push origin v4.0.0"
echo ""
echo "3. 创建Release:"
echo "   访问 https://github.com/timo/uniskill-v4/releases/new"
echo "   上传 UniSkill_V4_v4.0.0.zip"
