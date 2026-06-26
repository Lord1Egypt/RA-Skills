#!/bin/bash
# 心灵补手安装脚本
# 将INSERT_TO_SOUL.md内容注入到用户SOUL.md

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
INSERT_FILE="$SKILL_DIR/INSERT_TO_SOUL.md"
SOUL_FILE="$HOME/.openclaw/workspace/SOUL.md"
CONFIG_DIR="$HOME/.xinling-bushou"
CONFIG_FILE="$CONFIG_DIR/config.json"

echo "========================================"
echo "  心灵补手 安装程序"
echo "========================================"

# 检查INSERT_TO_SOUL.md是否存在
if [ ! -f "$INSERT_FILE" ]; then
    echo "❌ 错误：找不到 $INSERT_FILE"
    exit 1
fi

# 检查SOUL.md是否存在
if [ ! -f "$SOUL_FILE" ]; then
    echo "❌ 错误：找不到 $SOUL_FILE"
    exit 1
fi

# 检查是否已经安装（检查是否已有模块标记）
if grep -q "【心灵补手】" "$SOUL_FILE"; then
    echo "⚠️  检测到心灵补手模块已安装"
    read -p "是否重新安装？(y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装取消"
        exit 0
    fi
    # 移除旧模块
    sed -i '/# ═══════════════════════════════════════════════════════════════/,/# ═══════════════════════════════════════════════════════════════/d' "$SOUL_FILE"
fi

# 创建配置目录
mkdir -p "$CONFIG_DIR"

# 生成默认配置
cat > "$CONFIG_FILE" << 'EOF'
{
  "enabled": true,
  "persona": "taijian",
  "level": 5,
  "gender": "unknown",
  "gender_confidence": "low",
  "mode": "normal",
  "installed_at": "",
  "stats": {
    "triggered_count": 0,
    "last_triggered": null,
    "session_count": 0
  }
}
EOF

# 更新时间戳
date_str=$(date -Iseconds)
sed -i "s/\"installed_at\": \"\"/\"installed_at\": \"$date_str\"/" "$CONFIG_FILE"

# 注入模块到SOUL.md
echo "" >> "$SOUL_FILE"
echo "" >> "$SOUL_FILE"
cat "$INSERT_FILE" >> "$SOUL_FILE"

echo "✅ 心灵补手模块已成功安装到 SOUL.md"
echo "✅ 配置文件已创建: $CONFIG_FILE"
echo ""
echo "请重启Agent使配置生效"
echo ""
echo "首次使用时会自动分析您的性别并设置默认风格"
