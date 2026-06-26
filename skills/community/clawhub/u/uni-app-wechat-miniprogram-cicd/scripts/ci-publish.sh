#!/usr/bin/env bash
# ============================================================
# uni-app 微信小程序 CI/CD 一键发布脚本
# 支持 GitHub Actions / GitLab CI / Jenkins
#
# 环境变量（必需）：
#   WEAPP_APPID            - 小程序 AppID
#   WEAPP_PRIVATE_KEY      - 私钥文件内容
#   VERSION                - 发布版本号（semver）
#
# 可选变量：
#   CI_MODE                - experience | review | release
#   WEAPP_PRIVATE_KEY_PATH - 私钥保存路径
# ============================================================

set -e

VERSION="${VERSION:-1.0.0}"
APP_ID="${WEAPP_APPID}"
PRIVATE_KEY="${WEAPP_PRIVATE_KEY}"
CI_MODE="${CI_MODE:-experience}"
KEY_PATH="${WEAPP_PRIVATE_KEY_PATH:-keys/private.key}"
BUILD_OUTPUT="dist/build/mp-weixin"

echo "========================================="
echo "  uni-app 微信小程序 CI 发布"
echo "  版本: $VERSION"
echo "  模式: $CI_MODE"
echo "  AppID: $APP_ID"
echo "========================================="

# 前置检查
if [ -z "$APP_ID" ]; then
  echo "❌ 错误: 缺少 WEAPP_APPID 环境变量"
  exit 1
fi

if [ -z "$PRIVATE_KEY" ]; then
  echo "❌ 错误: 缺少 WEAPP_PRIVATE_KEY 环境变量"
  exit 1
fi

# Step 1: 安装依赖
echo ""
echo "📦 Step 1/4 - 安装依赖..."
npm ci --prefer-offline

# Step 2: 写入私钥
echo ""
echo "🔑 Step 2/4 - 写入私钥..."
mkdir -p "$(dirname "$KEY_PATH")"
echo "$PRIVATE_KEY" > "$KEY_PATH"
chmod 400 "$KEY_PATH"
echo "   私钥已写入: $KEY_PATH"

# Step 3: 构建 uni-app
echo ""
echo "🔨 Step 3/4 - 构建 uni-app..."
npm run build:mp-weixin

if [ ! -d "$BUILD_OUTPUT" ]; then
  echo "❌ 错误: 构建产物不存在: $BUILD_OUTPUT"
  exit 1
fi
echo "   构建完成: $BUILD_OUTPUT"

# Step 4: 发布
echo ""
echo "🚀 Step 4/4 - 发布微信小程序..."
export WEAPP_PRIVATE_KEY_PATH="$KEY_PATH"
export WEAPP_APPID="$APP_ID"

node scripts/build-uni.js

echo ""
echo "========================================="
echo "  ✅ CI 发布完成！"
echo "========================================="
