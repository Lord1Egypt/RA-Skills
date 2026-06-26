#!/bin/bash
# 安全写入文件（带文件锁）

if [ $# -lt 2 ]; then
    echo "用法: $0 <文件路径> <内容>"
    exit 1
fi

FILE_PATH="$1"
CONTENT="$2"
LOCK_FILE="$FILE_PATH.lock"
MAX_RETRY=5
RETRY_COUNT=0
LOCK_TIMEOUT=300  # 5分钟超时

# 清理超时的锁
if [ -d "$LOCK_FILE" ]; then
    lock_age=$(($(date +%s) - $(stat -f %m "$LOCK_FILE" 2>/dev/null || stat -c %Y "$LOCK_FILE")))
    if [ $lock_age -gt $LOCK_TIMEOUT ]; then
        echo "⚠️  检测到超时锁，自动清理"
        rmdir "$LOCK_FILE" 2>/dev/null
    fi
fi

# 尝试获取锁
while [ $RETRY_COUNT -lt $MAX_RETRY ]; do
    if mkdir "$LOCK_FILE" 2>/dev/null; then
        # 获得锁，执行写入
        echo "$CONTENT" > "$FILE_PATH"
        rmdir "$LOCK_FILE"
        echo "✅ 写入成功: $FILE_PATH"
        exit 0
    else
        # 锁被占用，等待
        echo "⏳ 文件被占用，等待中... ($((RETRY_COUNT + 1))/$MAX_RETRY)"
        sleep 1
        RETRY_COUNT=$((RETRY_COUNT + 1))
    fi
done

echo "❌ 无法获取文件锁: $FILE_PATH"
exit 1
