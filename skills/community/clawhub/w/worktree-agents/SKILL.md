---
name: worktree-agents
description: >
  使用 git worktree 隔离多个 Claude Code 实例，由 OpenClaw 主控器并行调度完成同一项目的不同模块。
  适用场景：将一个编码项目拆分为独立子任务，让多个 Claude Code 实例并行实现，最后合并 PR。
  触发条件：用户要求"多个 Agent 协作"、"并行完成项目"、"worktree 实验"、"多 Agent 编排"时激活。
---

# Worktree Agents — 多 Agent 编排技能

## 前提条件

- Claude Code 二进制：`/mnt/c/Users/Inuyasha/.local/bin/claude.exe`（Windows 侧，可从 WSL 调用）
- GitHub Token：从 `~/.openclaw/openclaw.json` 读取（`skills.entries["gh-issues"].apiKey`）
- 目标 Git 仓库已存在（本地 + GitHub 远端）

## 核心工作流（5 步）

### 步骤 1：明确任务拆分

在开始前，必须确定：
- **每个 Agent 的任务**（1-3 个具体函数/文件）
- **文件所有权**（每个文件只允许一个 Agent 写）
- **并行 or 串行**（有依赖关系的任务需串行）

详见 `references/task-decomposition.md`

### 步骤 2：创建 Worktree

```bash
bash scripts/setup_worktrees.sh <repo_dir> <worktrees_base_dir> <agent-a> <agent-b> ...
```

输出格式：`agent_name:worktree_path:branch_name`（每行一个 Agent）

### 步骤 3：并行启动 Claude Code

用 exec(background=true) 并行启动多个 Agent，每个调用：

```bash
bash scripts/orchestrate.sh \
  <repo_dir> \
  /mnt/c/Users/Inuyasha/.local/bin/claude.exe \
  <agent_name> \
  <worktree_path> \
  <branch> \
  "<task_prompt>" \
  /tmp/<agent_name>.log
```

Task prompt 模板：
```
你是 <AgentName>，只能修改 <file1>, <file2>，不得碰其他文件。
任务：<具体实现要求，含函数签名、异常处理、docstring>
完成后执行：git add -A && git commit -m "<commit message>"
只输出 done。
```

### 步骤 4：监控 + 收尾

使用 `process(poll)` 等待所有 Agent 完成，然后检查：

```bash
cat /tmp/<agent_name>.log | grep "AGENT_DONE"
```

如果 Agent 没有自行 commit（常见于第一次），脚本会自动收尾。

### 步骤 5：推送 PR + 合并

```bash
bash scripts/push_and_pr.sh \
  <repo_dir> <gh_token> <owner/repo> <agent_name> <worktree_path> <branch> main
```

验证通过后通过 GitHub API 合并：

```bash
curl -s -X PUT \
  -H "Authorization: Bearer $GH_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  "https://api.github.com/repos/<owner/repo>/pulls/<pr_number>/merge" \
  -d '{"merge_method": "squash"}'
```

## 已知限制与解决方案

**WSL 写文件被沙盒阻止**
→ Claude Code 必须加 `--dangerously-skip-permissions`

**Codex `.cmd` 在 WSL 下无法运行**
→ 使用 `--dangerously-skip-permissions` 的 Claude Code 替代，或在 WSL 安装原生 codex：`npm install -g @openai/codex`

**主仓库 git pull 权限错误（NTFS）**
→ worktree 放在 WSL 本地文件系统（`~/projects/worktrees/`），不放 `/mnt/c/`

**Agent 没有自行 commit**
→ `orchestrate.sh` 脚本会检测未提交变更并自动 commit

## 环境变量获取

```bash
CLAUDE_BIN="/mnt/c/Users/Inuyasha/.local/bin/claude.exe"
GH_TOKEN=$(cat ~/.openclaw/openclaw.json | jq -r '.skills.entries["gh-issues"].apiKey')
```

## 使用 Codex 替代 Claude Code（更便宜）

Codex 已安装在 WSL，使用自建代理：

```bash
export OPENAI_API_KEY="sk-5Ds6eFbTEE1zu5fQ14F4FfB5892b419dB1BfC7292147B9Ef"
export OPENAI_BASE_URL="http://152.53.52.170:3003/v1"
CODEX_BIN="$HOME/.npm-global/bin/codex"
```

调用方式（替换 orchestrate.sh 里的 CLAUDE_BIN 部分）：

```bash
"$CODEX_BIN" exec --full-auto "$TASK_PROMPT"
# 或无沙盒更快：
"$CODEX_BIN" --yolo "$TASK_PROMPT"
```

注意：`OPENAI_BASE_URL` 必须在调用前 export，否则 Codex 会尝试连官方 OpenAI。
