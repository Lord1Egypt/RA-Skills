**中文版本：**

# soul-undead

一个可发布的 OpenClaw 技能项目，用于通过 GitHub 仓库备份和恢复核心工作区 Markdown 文件。

## 目的

`soul-undead` 管理以下固定核心文件：
- `AGENTS.md`
- `HEARTBEAT.md`
- `IDENTITY.md`
- `SOUL.md`
- `TOOLS.md`
- `USER.md`
- `MEMORY.md`

支持两种主要流程：
1. **将本地核心文件同步到 GitHub**
2. **从 GitHub 恢复到本地工作区**

远程恢复覆盖本地文件前，会自动创建带时间戳的本地快照以确保回滚安全。

## 项目包含文件

- `SKILL.md`
- `scripts/init_or_sync.sh`
- `assets/logic-diagram-zh.png`
- `assets/logic-diagram-en.png`

## 项目不包含文件

以下为运行时产物，不应提交或发布：
- `local-backups/`
- `.workspace-backup-state.json`

安装技能运行时会自动创建。

## 逻辑图

### 中文版
![soul-undead 逻辑图 (ZH)](assets/logic-diagram-zh.png)

## 注意事项

- 默认仓库名为 `soul-undead`。
- 技能依赖 `gh`、`git` 和 `python3`。
- 恢复或同步前必须完成 `gh auth login`。
- 首次初始化时，若远程仓库已存在，则先创建本地快照，再将远程文件恢复到本地。
- 若恢复的远程版本错误，可从 `local-backups/<timestamp>/` 回滚，并将修正后的本地版本同步回 GitHub。
