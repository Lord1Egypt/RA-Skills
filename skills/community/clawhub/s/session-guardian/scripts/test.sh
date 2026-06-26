#!/bin/bash
# Session Guardian 快速测试脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "=== Session Guardian 快速测试 ==="
echo ""

# 测试1：配置文件
echo "[1/5] 测试配置文件..."
if source "$SKILL_DIR/scripts/config.sh"; then
    echo "  ✅ 配置文件加载成功"
else
    echo "  ❌ 配置文件加载失败"
    exit 1
fi

# 测试2：备份目录
echo "[2/5] 测试备份目录..."
if [ -d "$BACKUP_ROOT" ]; then
    echo "  ✅ 备份目录存在: $BACKUP_ROOT"
else
    echo "  ⚠️  备份目录不存在，创建中..."
    mkdir -p "$BACKUP_ROOT"/{incremental,hourly,daily}
    echo "  ✅ 备份目录已创建"
fi

# 测试3：增量备份
echo "[3/5] 测试增量备份..."
if bash "$SKILL_DIR/scripts/incremental-backup.sh" > /dev/null 2>&1; then
    echo "  ✅ 增量备份测试通过"
else
    echo "  ❌ 增量备份测试失败"
    exit 1
fi

# 测试4：快照
echo "[4/5] 测试快照..."
if bash "$SKILL_DIR/scripts/hourly-snapshot.sh" > /dev/null 2>&1; then
    echo "  ✅ 快照测试通过"
else
    echo "  ❌ 快照测试失败"
    exit 1
fi

# 测试5：恢复脚本
echo "[5/5] 测试恢复脚本..."
if bash "$SKILL_DIR/scripts/restore.sh" --source incremental --dry-run > /dev/null 2>&1; then
    echo "  ✅ 恢复脚本测试通过"
else
    echo "  ❌ 恢复脚本测试失败"
    exit 1
fi

echo ""
echo "=== 所有测试通过！ ==="
echo ""
echo "下一步："
echo "  bash $SKILL_DIR/scripts/install.sh"
