---
name: qg-skill-sync
description: 从团队 Git 仓库同步最新技能到本机 OpenClaw。支持首次设置、定时自动更新、手动同步和卸载。当用户需要同步技能、设置技能同步、安装或更新团队技能，或提到「技能同步」「同步技能」时使用。
metadata: { "openclaw": { "emoji": "🔄", "requires": { "bins": ["git", "bash"] } } }
---

# 技能同步（qg-skill-sync）

从团队 Git 仓库自动同步最新 skills 到本机 OpenClaw（`~/.openclaw/skills/`）。

## 首次设置

当用户说"设置技能同步"/"安装团队技能"时，执行以下两步：

### 第 1 步：运行初始化

直接执行：

```bash
bash {baseDir}/scripts/setup.sh
```

默认使用仓库 `https://github.com/wzj666666/ai-platform-skills.git`，将仓库内 `skills` 子目录同步到 `~/.openclaw/skills/`。

如需自定义，可传入参数：

```bash
bash {baseDir}/scripts/setup.sh [仓库地址] [skills子目录]
```

脚本会：
1. 将仓库 clone 到 `~/.qg-skill-sync/repo/`
2. 保存配置到 `~/.qg-skill-sync/config`
3. 将 `sync.sh` 复制到 `~/.qg-skill-sync/sync.sh`（供 cron 调用）
4. 首次将仓库中的 skills 同步到 `~/.openclaw/skills/`

### 第 2 步：创建 OpenClaw 定时任务

初始化成功后，立即创建两个定时同步任务（每天 10:30 和 17:30 各执行一次）,直接执行下面的脚本：

```bash
openclaw cron add \
  --name "qg-skill-sync-1030" \
  --cron "30 10 * * *" \
  --session isolated \
  --no-deliver \
  --message "执行 qg-skill-sync：运行 bash ~/.qg-skill-sync/sync.sh，输出同步结果。"

openclaw cron add \
  --name "qg-skill-sync-1730" \
  --cron "30 17 * * *" \
  --session isolated \
  --no-deliver \
  --message "执行 qg-skill-sync：运行 bash ~/.qg-skill-sync/sync.sh，输出同步结果。"
```

向用户确认：**"技能同步已设置完成，每天 10:30 和 17:30 自动从 Git 仓库拉取最新技能。请新开一个 OpenClaw 会话以加载新技能。"**

## 手动同步

用户说"手动同步技能"/"立即同步"时：

```bash
bash ~/.qg-skill-sync/sync.sh
```

## 查看同步日志

用户说"查看同步日志"/"上次同步结果"时：

```bash
tail -20 ~/.qg-skill-sync/logs/sync.log
```

## 卸载

用户说"卸载技能同步"/"关闭技能同步"时：

1. 移除定时任务（先用 `openclaw cron list` 找到 job id，再用 `cron.remove` 移除 name 为 "qg-skill-sync-1030" 和 "qg-skill-sync-1730" 的两个任务）
2. 清理本地仓库缓存：

```bash
bash {baseDir}/scripts/uninstall.sh
```

## 注意事项

- 同步后需**新开 OpenClaw 会话**才能加载新技能（OpenClaw 在会话启动时快照技能列表），因此需要告知用户"请新开一个 OpenClaw 会话以加载新技能"。
