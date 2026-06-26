#!/usr/bin/env bash
# worktree-agents/scripts/setup_worktrees.sh
# 为每个 Agent 创建 git worktree 并返回路径
#
# 用法: setup_worktrees.sh <repo_dir> <worktrees_base_dir> <agent_names_space_separated>
# 输出: 每行一个 "agent_name:worktree_path:branch_name"

set -euo pipefail

REPO_DIR="$1"
WORKTREES_BASE="$2"
shift 2
AGENTS=("$@")

cd "$REPO_DIR"
mkdir -p "$WORKTREES_BASE"

for AGENT in "${AGENTS[@]}"; do
  BRANCH="feature/$AGENT-$(date +%Y%m%d-%H%M%S)"
  WORKTREE_PATH="$WORKTREES_BASE/$AGENT"

  # 清理已存在的 worktree
  if git worktree list | grep -q "$WORKTREE_PATH"; then
    git worktree remove --force "$WORKTREE_PATH" 2>/dev/null || true
  fi
  rm -rf "$WORKTREE_PATH"

  # 创建分支 + worktree
  git checkout -b "$BRANCH" 2>/dev/null
  git checkout - 2>/dev/null  # 回到原分支
  git worktree add "$WORKTREE_PATH" "$BRANCH"

  echo "$AGENT:$WORKTREE_PATH:$BRANCH"
done
