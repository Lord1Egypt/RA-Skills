---
name: workspace-git-sync
description: >
  将 OpenClaw workspace 目录（~/.openclaw/workspace/）同步到指定的本地 Git 仓库，
  自动执行 git add、commit 和 push 操作。
  
  使用场景：
  - 备份 workspace 文件到 Git 仓库
  - 将工作目录同步到远程备份
  - 定期归档 OpenClaw 工作数据
  
  触发方式：
  - "将 workspace 同步到 /path/to/repo"
  - "备份 workspace 到 ~/projects/backup-repo"
  - "推送 workspace 到指定本地仓库"
---

# Workspace Git Sync

将 OpenClaw 工作目录同步到 Git 仓库，实现自动备份和版本控制。

## 功能特性

- **自动排除**：默认排除 `skills/`、`__pycache__/`、`.clawhub/` 等
- **Git 操作**：自动执行 pull → copy → commit → push
- **冲突处理**：同步前自动拉取远程变更
- **安全推送**：使用 `--force-with-lease` 而非 `--force`

## 使用方法

### 基础用法

```bash
# 同步到指定 Git 仓库
python3 ~/.openclaw/workspace/skills/workspace-git-sync/scripts/sync_workspace.py ~/projects/backup-repo

# 带自定义提交信息
python3 ~/.openclaw/workspace/skills/workspace-git-sync/scripts/sync_workspace.py ~/projects/backup-repo "每日备份"
```

### Python API

```python
from scripts.sync_workspace import sync_workspace_to_git, quick_sync, force_sync

# 标准同步
result = sync_workspace_to_git("~/projects/backup-repo")

# 快速同步
result = quick_sync("~/projects/backup-repo", "快速备份")

# 强制同步（危险）
result = force_sync("~/projects/backup-repo", "强制覆盖")
```

## 参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `target_repo_path` | str | 必需 | 目标 Git 仓库本地路径 |
| `branch` | str | 自动检测 | 目标分支 |
| `commit_msg` | str | 自动生成 | 提交信息 |
| `exclude_patterns` | list | `["skills", ".git", ...]` | 额外排除项 |
| `pull_before_push` | bool | True | 推送前是否先 pull |
| `strategy` | str | "rebase" | 合并策略 (rebase/merge/force) |

## 执行流程

1. **检查源目录** — 验证 `~/.openclaw/workspace/` 存在
2. **检查目标仓库** — 验证是有效的 Git 仓库
3. **拉取远程变更** — `git pull --rebase` 避免冲突
4. **清理目标目录** — 删除旧文件（保留 `.git/`）
5. **复制文件** — 从 workspace 复制到目标目录
6. **提交并推送** — `git add -A` → `git commit` → `git push`

## 默认排除项

以下文件/目录会自动排除，不会同步：

- `skills/` — 技能目录（通常很大）
- `.git/` — Git 元数据
- `__pycache__/` — Python 缓存
- `.DS_Store` — macOS 系统文件
- `node_modules/` — Node.js 依赖
- `.clawhub/` — OpenClaw 缓存

## 使用示例

### 示例 1：基础同步

```
用户：将 workspace 同步到 ~/backup/openclaw
AI：执行 sync_workspace.py ~/backup/openclaw
```

### 示例 2：指定分支和提交信息

```python
sync_workspace_to_git(
    target_repo_path="~/github-pages",
    branch="gh-pages",
    commit_msg="Deploy workspace backup"
)
```

### 示例 3：强制同步（危险）

```python
# 跳过 pull，直接强制推送
force_sync("~/projects/backup-repo", "Emergency update")
```

## 错误处理

| 错误场景 | 处理方式 |
|----------|----------|
| 源目录不存在 | 报错，检查 `~/.openclaw/workspace/` |
| 目标不是 Git 仓库 | 报错，提示初始化仓库：`git init` |
| 合并冲突 | 中止操作，提示手动解决 |
| 无推送权限 | 显示 Git 错误，检查权限或 Token |

## 脚本位置

```
~/.openclaw/workspace/skills/workspace-git-sync/
├── SKILL.md
└── scripts/
    └── sync_workspace.py
```

## 注意事项

1. **目标必须是 Git 仓库**：文件夹必须包含 `.git/` 目录
2. **路径格式**：支持 `~` 展开（如 `~/projects/repo`）
3. **数据安全**：清理目标目录时会**保留 `.git/`**，不会丢失版本历史
4. **权限要求**：对目标目录有读写权限，对 Git 仓库有写权限
