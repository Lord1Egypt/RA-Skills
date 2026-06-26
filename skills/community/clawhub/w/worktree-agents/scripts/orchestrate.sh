#!/usr/bin/env bash
# worktree-agents/scripts/orchestrate.sh
# OpenClaw 多 Agent Worktree 编排脚本
#
# 用法:
#   orchestrate.sh <repo_dir> <claude_bin> <agent_name> <worktree_path> <branch> <task_prompt> <log_file>
#
# 本脚本由 OpenClaw 主控器为每个 Agent 单独调用（并行），执行以下操作:
#   1. 进入 worktree 目录
#   2. 以 --dangerously-skip-permissions --print 模式运行 Claude Code
#   3. 捕获输出到 log_file
#   4. 完成后 git add -A && git commit

set -euo pipefail

REPO_DIR="$1"
CLAUDE_BIN="$2"
AGENT_NAME="$3"
WORKTREE_PATH="$4"
BRANCH="$5"
TASK_PROMPT="$6"
LOG_FILE="$7"

echo "[$(date '+%H:%M:%S')] $AGENT_NAME starting in $WORKTREE_PATH" | tee "$LOG_FILE"

cd "$WORKTREE_PATH"

# 运行 Claude Code
"$CLAUDE_BIN" --dangerously-skip-permissions --print -p "$TASK_PROMPT" \
  >> "$LOG_FILE" 2>&1

EXIT_CODE=$?

echo "[$(date '+%H:%M:%S')] $AGENT_NAME claude exited with code $EXIT_CODE" | tee -a "$LOG_FILE"

# 检查是否有需要提交的文件
if git diff --quiet && git diff --staged --quiet; then
  echo "[$(date '+%H:%M:%S')] $AGENT_NAME: no changes to commit" | tee -a "$LOG_FILE"
else
  # 如果 Claude 没有自己 commit，帮它收尾
  if git status --porcelain | grep -q .; then
    git add -A
    git commit -m "feat: $AGENT_NAME task complete" --no-verify 2>&1 | tee -a "$LOG_FILE"
    echo "[$(date '+%H:%M:%S')] $AGENT_NAME: committed uncommitted changes" | tee -a "$LOG_FILE"
  fi
fi

echo "AGENT_DONE:$AGENT_NAME" | tee -a "$LOG_FILE"
