#!/usr/bin/env bash
# 配置模块

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MEMORY_ROOT="${MEMORY_ROOT:-$HOME/.openclaw/workspace/memory}"
SKILL_ROOT="${SKILL_ROOT:-$HOME/.openclaw/workspace/skills/unified-self-improving}"

# 层级配置
HOT_DIR="$MEMORY_ROOT/hot"
WARM_DIR="$MEMORY_ROOT/warm/learnings"
COLD_DIR="$MEMORY_ROOT/cold/archive"
NAMESPACE_DIR="$MEMORY_ROOT/namespace"
INDEX_FILE="$MEMORY_ROOT/index.jsonl"

# 配置默认值
DEFAULT_NAMESPACE="default"
HOT_RETENTION=3
WARM_RETENTION=10
AUTO_UPGRADE_THRESHOLD=3

# 创建必要目录
init_storage() {
    mkdir -p "$HOT_DIR" "$WARM_DIR" "$COLD_DIR" "$NAMESPACE_DIR"
}

# 获取当前时间 ISO 格式
now() {
    date -u +"%Y-%m-%dT%H:%M:%SZ"
}

# 生成唯一 ID
generate_id() {
    echo "learn-$(date -u +%Y%m%d)-$(date -u +%H%M%S)-$RANDOM"
}
