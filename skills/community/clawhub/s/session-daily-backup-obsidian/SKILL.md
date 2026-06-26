# Session Daily Backup - Obsidian

自动备份 OpenClaw 会话对话到 Obsidian Vault，支持增量备份、多 session 合并、Token 监控和 QQ 警告通知。

## 功能

- 📦 **每日自动备份**：凌晨 2 点自动执行（cron 定时任务）
- 📝 **增量备份**：只保存新增对话，避免重复
- 🗂️ **多 Session 合并**：备份当天所有 session 文件到一个每日文件
- 🎨 **Obsidian 格式**：使用 callout 格式，支持彩色对话区分
- ⚠️ **Token 监控**：80%/90% 阈值警告，通过 QQ 推送通知
- 📊 **统计信息**：Token 估算、行数统计、session 数量

## 配置

编辑 `config` 文件：

```bash
# Obsidian Vault 路径
VAULT_DIR="$HOME/Documents/Obsidian/Clawd Markdowns"

# Session 文件存储路径
SESSION_DIR="/root/.openclaw/agents/main/sessions"

# 跟踪文件路径
TRACKING_DIR="/root/clawd"

# QQ Bot 配置（可选，用于警告通知）
QQ_APPID=""
QQ_SECRET=""
QQ_USER_ID=""
```

## 使用

### 手动备份

```bash
# 完整快照（所有 session）
bash /root/.openclaw/workspace/skills/session-daily-backup-obsidian/scripts/save_full_snapshot.sh [主题名]

# 按小时整理
bash /root/.openclaw/workspace/skills/session-daily-backup-obsidian/scripts/create_hourly_snapshots.sh YYYY-MM-DD

# 监控并自动保存（每日增量备份）
bash /root/.openclaw/workspace/skills/session-daily-backup-obsidian/scripts/monitor_and_save.sh
```

### 设置定时任务

```bash
# 编辑 crontab
crontab -e

# 添加每日凌晨 2 点备份
0 2 * * * bash /root/.openclaw/workspace/skills/session-daily-backup-obsidian/scripts/monitor_and_save.sh >> /root/clawd/backup.log 2>&1
```

## 输出文件

- **每日备份**：`$VAULT_DIR/YYYY-MM-DD-daily.md`
- **完整快照**：`$VAULT_DIR/YYYY-MM-DD-HHMM-[主题].md`
- **小时快照**：`$VAULT_DIR/YYYY-MM-DD/HH-mm.md`
- **跟踪文件**：`$TRACKING_DIR/.last_snapshot_timestamp`（记录上次备份行数）

## 依赖

- `jq` - JSON 处理
- `bash` - Shell 环境
- OpenClaw session 文件（JSONL 格式）

## 注意事项

- 首次运行会创建完整的每日备份文件
- 后续运行仅追加新增对话（≥10 条新消息触发）
- Token 警告只会发送一次，直到 token 数回落后重新触发
- QQ 通知需要配置 QQ Bot 或使用 openclaw message 命令
