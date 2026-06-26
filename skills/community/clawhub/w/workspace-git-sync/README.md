# Workspace Git Sync

将 OpenClaw/Kimi-Claw workspace 自动同步到 Git 仓库。

## 功能

- 📦 **自动备份** - 一键将 workspace 同步到 Git 仓库
- 🔄 **智能同步** - 自动执行 pull → copy → commit → push
- 🛡️ **安全推送** - 使用 `--force-with-lease` 而非 `--force`
- 🚫 **自动排除** - 跳过 `skills/`、`__pycache__/` 等不需要备份的目录

## 安装

### 方式1：使用 OpenClaw 安装

```bash
openclaw plugins install workspace-git-sync
```

### 方式2：手动安装

```bash
# 克隆到 skills 目录
git clone https://github.com/yourname/workspace-git-sync.git ~/.openclaw/workspace/skills/workspace-git-sync
```

## 使用方法

### 命令行

```bash
# 基础同步
python3 ~/.openclaw/workspace/skills/workspace-git-sync/scripts/sync_workspace.py ~/projects/backup-repo

# 带自定义提交信息
python3 ~/.openclaw/workspace/skills/workspace-git-sync/scripts/sync_workspace.py ~/projects/backup-repo "每日备份"
```

### Python API

```python
from scripts.sync_workspace import sync_workspace_to_git, quick_sync

# 标准同步
result = sync_workspace_to_git("~/projects/backup-repo")

# 快速同步
result = quick_sync("~/projects/backup-repo", "快速备份")
```

## 参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `target_repo_path` | str | 必需 | 目标 Git 仓库本地路径 |
| `branch` | str | 自动检测 | 目标分支 |
| `commit_msg` | str | 自动生成 | 提交信息 |
| `exclude_patterns` | list | `["skills", ".git", ...]` | 额外排除项 |
| `strategy` | str | "rebase" | 合并策略 |

## 默认排除项

以下目录会自动排除：

- `skills/` - 技能目录（通常很大）
- `.git/` - Git 元数据
- `__pycache__/` - Python 缓存
- `.DS_Store` - macOS 系统文件
- `node_modules/` - Node.js 依赖
- `.clawhub/` - OpenClaw 缓存

## 工作流程

```
检查源目录 → 检查目标仓库 → 拉取远程变更 → 清理旧文件 → 复制新文件 → 提交推送
```

## 要求

- Python 3.8+
- Git
- 目标目录必须是 Git 仓库（已初始化）

## 许可证

MIT

## 作者

你的名字
