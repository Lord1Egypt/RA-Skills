#!/bin/bash
# 自动更新脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_DIR="$SCRIPT_DIR/../.."
VERSION_FILE="$SCRIPT_DIR/VERSION"
BACKUP_DIR="/tmp/xianyu-grabber-backup-$$"

echo "🐾 闲鱼数据抓取技能 - 自动更新"
echo "========================================"
echo ""

# 加载当前版本
if [ -f "$VERSION_FILE" ]; then
    CURRENT_VERSION=$(cat "$VERSION_FILE" | jq -r '.version')
    echo "📦 当前版本：v$CURRENT_VERSION"
else
    echo "⚠️  版本文件不存在"
    CURRENT_VERSION="unknown"
fi

# 从配置加载 Gitee 信息
CONFIG_FILE="$WORKSPACE_DIR/.xianyu-grabber-config.json"
if [ -f "$CONFIG_FILE" ]; then
    GITEE_OWNER=$(cat "$CONFIG_FILE" | jq -r '.gitee.owner')
    GITEE_REPO="xianyu-data-grabber"
    GITEE_TOKEN=$(cat "$CONFIG_FILE" | jq -r '.gitee.token')
else
    echo "❌ 配置文件不存在：$CONFIG_FILE"
    exit 1
fi

if [ "$GITEE_OWNER" = "your_username" ] || [ -z "$GITEE_TOKEN" ]; then
    echo "❌ Gitee 配置无效，请先配置 ~/.openclaw/workspace/.xianyu-grabber-config.json"
    exit 1
fi

echo "🌐 检查 Gitee 仓库：$GITEE_OWNER/$GITEE_REPO"
echo ""

# 检查远程版本
echo "🔍 检查最新版本..."
REMOTE_VERSION=$(curl -sL "https://gitee.com/$GITEE_OWNER/$GITEE_REPO/raw/main/VERSION" 2>/dev/null | jq -r '.version' || echo "0.0.0")

if [ "$REMOTE_VERSION" = "0.0.0" ]; then
    echo "❌ 无法获取远程版本，请检查网络连接"
    exit 1
fi

echo "📦 最新版本：v$REMOTE_VERSION"

# 比较版本
if [ "$CURRENT_VERSION" = "$REMOTE_VERSION" ]; then
    echo "✅ 已是最新版本！"
    exit 0
fi

echo ""
echo "🆕 发现新版本：v$CURRENT_VERSION → v$REMOTE_VERSION"
echo ""

# 备份当前版本
echo "💾 备份当前版本..."
mkdir -p "$BACKUP_DIR"
cp -r "$SCRIPT_DIR"/* "$BACKUP_DIR/" 2>/dev/null || true
cp "$CONFIG_FILE" "$BACKUP_DIR/config.json" 2>/dev/null || true
echo "✅ 备份完成：$BACKUP_DIR"
echo ""

# 下载新版本
echo "📥 下载新版本..."
DOWNLOAD_URL="https://gitee.com/$GITEE_OWNER/$GITEE_REPO/archive/main.zip"
TEMP_DIR="/tmp/xianyu-grabber-update-$$"
mkdir -p "$TEMP_DIR"

if command -v curl &> /dev/null; then
    curl -sL "$DOWNLOAD_URL" -o "$TEMP_DIR/update.zip"
elif command -v wget &> /dev/null; then
    wget -q "$DOWNLOAD_URL" -O "$TEMP_DIR/update.zip"
else
    echo "❌ 需要 curl 或 wget"
    exit 1
fi

if [ ! -f "$TEMP_DIR/update.zip" ] || [ ! -s "$TEMP_DIR/update.zip" ]; then
    echo "❌ 下载失败"
    exit 1
fi

echo "✅ 下载完成"
echo ""

# 解压
echo "📦 解压新版本..."
unzip -q "$TEMP_DIR/update.zip" -d "$TEMP_DIR"
UPDATE_DIR="$TEMP_DIR/xianyu-data-grabber-main"

if [ ! -d "$UPDATE_DIR" ]; then
    echo "❌ 解压失败"
    exit 1
fi

echo "✅ 解压完成"
echo ""

# 备份配置文件
echo "💾 保留用户配置..."
if [ -f "$CONFIG_FILE" ]; then
    cp "$CONFIG_FILE" "$UPDATE_DIR/.xianyu-grabber-config.json"
fi
echo "✅ 配置已保留"
echo ""

# 覆盖安装
echo "🔄 安装新版本..."
rm -rf "$SCRIPT_DIR"/*
cp -r "$UPDATE_DIR"/* "$SCRIPT_DIR/"
echo "✅ 安装完成"
echo ""

# 清理
rm -rf "$TEMP_DIR"
echo "🧹 清理临时文件..."
echo ""

# 设置权限
echo "🔐 设置权限..."
chmod +x "$SCRIPT_DIR"/*.sh "$SCRIPT_DIR"/*.py 2>/dev/null || true
echo "✅ 权限设置完成"
echo ""

# 显示更新日志
echo "📝 更新日志:"
curl -sL "https://gitee.com/$GITEE_OWNER/$GITEE_REPO/raw/main/VERSION" 2>/dev/null | jq -r '.changelog | to_entries | .[] | "\(.key): \(.value | join(", "))"' || true
echo ""

echo "========================================"
echo "🎉 更新完成！"
echo ""
echo "当前版本：v$REMOTE_VERSION"
echo "更新时间：$(date)"
echo ""
echo "========================================"
