---
name: ugreen-nas-openclaw-backup
description: 绿联NAS OpenClaw Docker部署的备份与恢复工具 / Ugreen NAS OpenClaw Docker deployment backup and restore tool
metadata: {"openclaw": {"emoji": "💾", "requires": {"bins": ["tar"]}}}
---

# 绿联NAS OpenClaw备份 / Ugreen NAS OpenClaw Backup

## 简介 / Introduction

绿联NAS提供了通过应用中心直接部署OpenClaw的服务。用此方式部署的OpenClaw托管在Docker上，但托管方式有一些限制，无法使用Docker的克隆和导出功能对OpenClaw容器进行备份。针对此情况，本Skill提供OpenClaw容器设置和Skills镜像备份和恢复的功能。

Ugreen NAS provides a service to deploy OpenClaw directly through the App Center. OpenClaw deployed this way runs on Docker, but the hosting method has limitations - Docker's clone and export features cannot be used to backup the OpenClaw container. This Skill provides backup and restore functionality for OpenClaw container configuration and skills.

## 什么时候使用 / When to Use

用户要求 / User requests:
- "备份 OpenClaw" / "Backup OpenClaw"
- "创建快照" / "Create snapshot"
- "备份部署" / "Backup deployment"
- "导出配置" / "Export configuration"
- "恢复备份" / "Restore backup"
- "还原配置" / "Restore configuration"

---

## 备份功能 / Backup Feature

### 自动检测备份位置 / Auto-detect Backup Location

此 Skill 会自动查找可访问的宿主目录进行备份 / This Skill automatically finds accessible host directory for backup:

1. 读取 OpenClaw 配置获取工作空间路径 (`~/.openclaw/workspace`) / Read OpenClaw config to get workspace path
2. 从工作空间路径推断宿主挂载目录（如 `/root/.openclaw/workspace` → `/home/dylan/OpenClaw`）/ Infer host mount directory from workspace path
3. 验证该目录可写 / Verify the directory is writable

如果无法自动检测到有效目录，会提示用户指定备份目录 / If unable to detect, prompt user to specify backup directory.

### 备份命令 / Backup Command

```bash
# 自动检测备份路径 / Auto-detect backup path
OPENCLAW_DIR="/root/.openclaw"
WORKSPACE_DIR="$OPENCLAW_DIR/workspace"

# 尝试从工作空间路径推断宿主的共享目录 / Try to infer host shared directory from workspace path
if [ -d "$WORKSPACE_DIR" ]; then
  MOUNT_BASE=$(dirname "$WORKSPACE_DIR")
  if [ -w "$MOUNT_BASE" ]; then
    BACKUP_DIR="$MOUNT_BASE"
  fi
fi

# 如果未找到可写目录，提示用户手动指定 / If no writable directory found, prompt user to specify manually
if [ -z "$BACKUP_DIR" ]; then
  echo "无法自动检测备份目录，请手动指定备份目录路径"
  # 向用户请求指定目录 / Request user to specify directory
fi

# 执行备份 / Execute backup
cd "$OPENCLAW_DIR"
tar -czf "$BACKUP_DIR/openclaw-backup-$(date +%Y%m%d-%H%M%S).tar.gz" .openclaw/
```

### 手动指定备份目录 / Specify Backup Directory Manually

```bash
# 示例：指定 /custom/backup/path 作为备份目录 / Example: specify /custom/backup/path as backup directory
tar -czf /custom/backup/path/openclaw-backup-$(date +%Y%m%d).tar.gz /root/.openclaw/
```

---

## 恢复功能 / Restore Feature

### 自动查找备份文件 / Auto-find Backup Files

1. 自动检测备份目录（同备份功能）/ Auto-detect backup directory (same as backup)
2. 列出目录中所有 `openclaw-backup-*.tar.gz` 文件 / List all backup files
3. 按文件修改时间排序，显示日期和时间 / Sort by modification time, show date and time
4. 让用户选择要恢复的时间点 / Let user select restore point
5. 用户确认后执行恢复 / Execute restore after user confirmation

### 恢复命令 / Restore Command

```bash
# 1. 查找备份目录 / Find backup directory
BACKUP_DIR=$(自动检测 / auto-detect)

# 2. 列出可用备份 / List available backups
ls -lt "$BACKUP_DIR"/openclaw-backup-*.tar.gz

# 3. 让用户选择 / Let user select
# 用户选择: openclaw-backup-20260317-143022.tar.gz / User selects: openclaw-backup-20260317-143022.tar.gz

# 4. 确认恢复 / Confirm restore
# 警告：恢复会覆盖现有配置，是否继续？(y/n) / Warning: Restore will overwrite existing config, continue? (y/n)

# 5. 执行恢复（建议先停止 OpenClaw）/ Execute restore (recommend stopping OpenClaw first)
cd /root
tar -xzf "$BACKUP_DIR/openclaw-backup-20260317-143022.tar.gz"

# 6. 重启 OpenClaw 容器 / Restart OpenClaw container
```

### 恢复注意事项 / Restore Notes

- ⚠️ **恢复会覆盖现有配置**，请提前确认 / **Restore will overwrite existing config**, please confirm in advance
- 建议恢复前**停止 OpenClaw 容器** / Recommend **stopping OpenClaw container** before restore
- 如果只是想查看备份内容，可以不解压直接查看 / If only need to view backup content, can view without extracting:
  ```bash
  tar -tzf /path/to/backup.tar.gz | head -20
  ```

---

## 备份内容 / Backup Contents

- `~/.openclaw/` — 所有配置和数据 / All config and data
- `~/.openclaw/workspace/` — 工作空间和 Skills / Workspace and skills
- `~/.openclaw/openclaw.json` — 主配置文件 / Main config file

---

## 注意事项 / Notes

- 备份文件较大（约 45MB），请定期清理旧备份 / Backup file is large (~45MB), please clean up old backups regularly
- 恢复前建议先停止 OpenClaw 容器 / Recommend stopping OpenClaw container before restore
- 如果无法自动检测目录，咪乐会询问你指定的备份/恢复目录 / If unable to auto-detect directory, MiLe will ask you to specify backup/restore directory
