#!/bin/bash
# Server Maintenance - Cleanup Script
# 清理服务器缓存和临时文件

set -e

SERVER_HOST="${1:-localhost}"
SERVER_NAME="${2:-本地}"
DRY_RUN="${3:-false}"

echo "=== $SERVER_NAME 服务器清理 ==="

if [ "$SERVER_HOST" = "localhost" ]; then
    CMD_PREFIX=""
else
    CMD_PREFIX="ssh root@$SERVER_HOST"
fi

# 显示清理前状态
echo "清理前："
$CMD_PREFIX df -h / | tail -1

if [ "$DRY_RUN" = "true" ]; then
    echo -e "\n[DRY RUN] 将执行以下清理："
    echo "1. npm cache clean --force"
    echo "2. 清理 Playwright 旧版本"
    exit 0
fi

# 清理 npm 缓存
echo -e "\n清理 npm 缓存..."
$CMD_PREFIX "npm cache clean --force 2>&1 | grep -v 'npm warn'"

# 清理 Playwright 旧版本（保留最新版本）
echo -e "\n检查 Playwright 缓存..."
$CMD_PREFIX "
if [ -d ~/.cache/ms-playwright ]; then
    cd ~/.cache/ms-playwright
    # 找出最新版本号
    LATEST=\$(ls -d chromium-* 2>/dev/null | sort -V | tail -1 | sed 's/chromium-//')
    if [ -n \"\$LATEST\" ]; then
        echo \"保留最新版本: \$LATEST\"
        # 删除旧版本
        for dir in chromium-* chromium_headless_shell-*; do
            if [[ \$dir != *\$LATEST* ]] && [ -d \"\$dir\" ]; then
                echo \"删除旧版本: \$dir\"
                rm -rf \"\$dir\"
            fi
        done
    fi
fi
"

# 显示清理后状态
echo -e "\n清理后："
$CMD_PREFIX df -h / | tail -1

echo -e "\n✓ 清理完成"
