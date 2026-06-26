#!/usr/bin/env bash
# qg-skill-sync - 定时执行脚本（由 OpenClaw cron 触发）
# 用法: bash ~/.qg-skill-sync/sync.sh
# 依赖: ~/.qg-skill-sync/config（由 setup.sh 生成）

set -euo pipefail

CONFIG="$HOME/.qg-skill-sync/config"

if [ ! -f "$CONFIG" ]; then
    echo "[$(date '+%F %T')] 错误: 未找到配置文件，请先运行 setup.sh 完成初始化" >&2
    exit 1
fi

# 加载配置
# shellcheck source=/dev/null
source "$CONFIG"

mkdir -p "$LOG_DIR"

cd "$REPO_DIR" || exit 1

# 拉取最新代码
git fetch origin
git pull --rebase --autostash

# 增量同步有 SKILL.md 的目录到 OpenClaw
SYNCED=0
for skill_dir in "$REPO_DIR/$SKILLS_SUBDIR"/*/; do
    [ -d "$skill_dir" ] || continue
    [ -f "$skill_dir/SKILL.md" ] || continue
    skill_name="$(basename "$skill_dir")"
    rsync -a --delete "$skill_dir" "$OPENCLAW_SKILLS/$skill_name/"
    SYNCED=$((SYNCED + 1))
done

echo "[$(date '+%F %T')] 同步完成: $SYNCED 个技能已更新"
