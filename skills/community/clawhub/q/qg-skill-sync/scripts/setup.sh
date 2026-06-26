#!/usr/bin/env bash
# qg-skill-sync - 首次初始化
# 用法: bash setup.sh [Git仓库地址] [skills子目录]
# 默认仓库: https://github.com/wzj666666/ai-platform-skills.git
# 默认 skills 子目录: skills（仓库内路径），同步目标: ~/.openclaw/skills
# 数据目录: ~/.qg-skill-sync（与技能名一致）
# 示例: bash setup.sh
#        bash setup.sh "https://github.com/other/other-repo.git"
#        bash setup.sh "https://github.com/other/other-repo.git" openclaw/skills

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_URL="${1:-https://github.com/wzj666666/ai-platform-skills.git}"
SKILLS_SUBDIR="${2:-skills}"

SYNC_HOME="$HOME/.qg-skill-sync"
REPO_DIR="$SYNC_HOME/repo"
LOG_DIR="$SYNC_HOME/logs"
OPENCLAW_SKILLS="$HOME/.openclaw/skills"

mkdir -p "$LOG_DIR" "$OPENCLAW_SKILLS"

# 保存配置，供 sync.sh 读取
cat > "$SYNC_HOME/config" <<EOF
REPO_URL=$REPO_URL
REPO_DIR=$REPO_DIR
SKILLS_SUBDIR=$SKILLS_SUBDIR
OPENCLAW_SKILLS=$OPENCLAW_SKILLS
LOG_DIR=$LOG_DIR
EOF

# 复制 sync.sh 到固定位置，供 cron 调用（不依赖 skill 安装路径）
cp "$SCRIPT_DIR/sync.sh" "$SYNC_HOME/sync.sh"
chmod +x "$SYNC_HOME/sync.sh"

# Clone 或 Pull
if [ -d "$REPO_DIR/.git" ]; then
    echo "仓库已存在，执行 pull..."
    cd "$REPO_DIR" && git pull --rebase --autostash
else
    echo "首次 clone 仓库..."
    git clone "$REPO_URL" "$REPO_DIR"
fi

# 首次同步 skills 到 OpenClaw
echo "同步技能到 $OPENCLAW_SKILLS ..."
SYNCED=0
for skill_dir in "$REPO_DIR/$SKILLS_SUBDIR"/*/; do
    [ -d "$skill_dir" ] || continue
    [ -f "$skill_dir/SKILL.md" ] || continue
    skill_name="$(basename "$skill_dir")"
    rsync -a --delete "$skill_dir" "$OPENCLAW_SKILLS/$skill_name/"
    SYNCED=$((SYNCED + 1))
done

echo ""
echo "================================================"
echo "初始化完成！"
echo "  仓库地址:   $REPO_URL"
echo "  本地仓库:   $REPO_DIR"
echo "  同步目标:   $OPENCLAW_SKILLS"
echo "  已同步技能: $SYNCED 个"
echo "  同步日志:   $LOG_DIR/sync.log"
echo ""
echo "接下来请在 OpenClaw 中创建定时任务（每天 10:30 和 17:30 各执行一次）："
echo ""
echo "  openclaw cron add \\"
echo "    --name \"qg-skill-sync-1030\" \\"
echo "    --cron \"30 10 * * *\" \\"
echo "    --session isolated \\"
echo "    --no-deliver \\"
echo "    --message \"执行 qg-skill-sync：运行 bash $SYNC_HOME/sync.sh，输出同步结果。\""
echo ""
echo "  openclaw cron add \\"
echo "    --name \"qg-skill-sync-1730\" \\"
echo "    --cron \"30 17 * * *\" \\"
echo "    --session isolated \\"
echo "    --no-deliver \\"
echo "    --message \"执行 qg-skill-sync：运行 bash $SYNC_HOME/sync.sh，输出同步结果。\""
echo ""
echo "新开 OpenClaw 会话即可使用同步的技能。"
echo "================================================"
