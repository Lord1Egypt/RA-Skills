#!/bin/bash
# Taro 项目初始化脚本
# 用法: bash init_project.sh <项目名>

set -e

PROJECT_NAME=${1:-my-miniprogram}
PROJECT_DIR="../${PROJECT_NAME}"

echo "📦 正在创建项目: $PROJECT_NAME"

# 复制模板
cp -r ../assets/project-template "$PROJECT_DIR"
cd "$PROJECT_DIR"

# 替换占位符
sed -i "s/{{projectName}}/$PROJECT_NAME/g" package.json taro.config.js config/index.js project.config.json app.config.js project.config.json 2>/dev/null || true
sed -i "s/{{projectDescription}}/$PROJECT_NAME 小程序/g" package.json project.config.json 2>/dev/null || true

echo "✅ 项目创建成功: $PROJECT_DIR"
echo ""
echo "下一步:"
echo "  cd $PROJECT_DIR"
echo "  npm install"
echo "  npm run dev:weapp"
