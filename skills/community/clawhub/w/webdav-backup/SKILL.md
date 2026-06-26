---
name: webdav-backup
version: 1.2.2
description: WebDAV 备份工具 - 将 OpenClaw 工作目录备份到 WebDAV 服务器或本地目录（默认 `~/openclaw/output`）。当用户需要备份数据、同步文件到云端、做本地归档、或配置自动备份计划时使用此技能。
metadata:
  openclaw:
    requires:
      env: [WEBDAV_URL, WEBDAV_USERNAME, WEBDAV_PASSWORD]
---

# WebDAV / 本地 备份工具

将 OpenClaw 工作目录与基础配置一起备份到 WebDAV 服务器，或直接备份到本地目录。

## 支持的 WebDAV 服务

- 坚果云 (jianguoyun.com)
- Nextcloud / ownCloud
- 阿里云盘（需 WebDAV 插件）
- 其他标准 WebDAV 服务

## 配置

如果只做本地备份，其实不需要配置 WebDAV。

- 本地默认输出目录：`~/openclaw/output`
- 如需云端同步，再配置 WebDAV 连接信息

### 方式一：openclaw.json（推荐）

编辑 `~/.openclaw/openclaw.json`，在 `skills.entries` 中添加：

```json
{
  "skills": {
    "entries": {
      "webdav-backup": {
        "enabled": true,
        "env": {
          "WEBDAV_URL": "https://dav.jianguoyun.com/dav/",
          "WEBDAV_USERNAME": "your-email@example.com",
          "WEBDAV_PASSWORD": "your-password"
        }
      }
    }
  }
}
```

### 方式二：环境变量

```bash
# 仅在当前 shell 会话中临时设置
export WEBDAV_URL="https://dav.jianguoyun.com/dav/"
export WEBDAV_USERNAME="your-email@example.com"
export WEBDAV_PASSWORD="your-password"
```

> **更安全的建议**：优先把配置写进 `~/.openclaw/openclaw.json`，并确保该文件权限受控；不建议把密码长期明文写入 `~/.bashrc` / `~/.zshrc`。

> **优先级**: 环境变量 > openclaw.json 配置

## 使用方法

### 手动备份

```bash
# 只做本地备份（默认保存到 ~/openclaw/output）
# 默认会备份：workspace + openclaw.json + cron + workspace/config
python3 ~/.openclaw/workspace/skills/webdav-backup/scripts/backup.py --local-only

# 备份默认清单到本地 + WebDAV
python3 ~/.openclaw/workspace/skills/webdav-backup/scripts/backup.py

# 只备份你指定的单个目录/文件
python3 ~/.openclaw/workspace/skills/webdav-backup/scripts/backup.py --source /path/to/data --local-only

# 指定备份文件名前缀
python3 ~/.openclaw/workspace/skills/webdav-backup/scripts/backup.py --name my-backup-2025 --local-only

# 指定本地备份目录
python3 ~/.openclaw/workspace/skills/webdav-backup/scripts/backup.py --local-only --local-dir ~/openclaw/my-backups

# 只上传 WebDAV，不保留本地副本
python3 ~/.openclaw/workspace/skills/webdav-backup/scripts/backup.py --remote-only
```

### 自动备份

使用 cron 设置定时备份：

```bash
# 每天凌晨2点做本地备份
cron add --schedule "0 2 * * *" --command "python3 ~/.openclaw/workspace/skills/webdav-backup/scripts/backup.py --local-only"

# 每天凌晨3点做本地 + WebDAV 双备份
cron add --schedule "0 3 * * *" --command "python3 ~/.openclaw/workspace/skills/webdav-backup/scripts/backup.py"
```

### 查看备份列表

```bash
# 查看本地备份
python3 ~/.openclaw/workspace/skills/webdav-backup/scripts/backup.py --list

# 查看远端备份
python3 ~/.openclaw/workspace/skills/webdav-backup/scripts/backup.py --list-remote
```

### 恢复备份

```bash
# 恢复本地最新备份到当前目录
python3 ~/.openclaw/workspace/skills/webdav-backup/scripts/backup.py --restore latest

# 恢复到指定目录
python3 ~/.openclaw/workspace/skills/webdav-backup/scripts/backup.py --restore latest --restore-dir ~/restore-test

# 恢复指定备份文件
python3 ~/.openclaw/workspace/skills/webdav-backup/scripts/backup.py --restore ~/openclaw/output/openclaw-backup-20260310-010203.tar.gz --restore-dir ~/restore-test

# 如需覆盖已存在文件
python3 ~/.openclaw/workspace/skills/webdav-backup/scripts/backup.py --restore latest --restore-dir ~/restore-test --force
```

#### 恢复判断建议（给 agent）

恢复阶段不要求死板固定流程，按场景自主判断即可：

- **只想查看内容 / 做核对**：优先恢复到临时目录或单独目录，先看 `openclaw/backup-manifest.json`，确认备份里实际包含了哪些内容。
- **想恢复部分文件**：先恢复到一个中间目录，再从中挑选 `openclaw/workspace/`、`openclaw/openclaw.json`、`openclaw/cron/` 等需要的部分拷回目标位置。
- **想整体迁移到新环境**：恢复到指定目录后，再按目标机器的实际目录结构落位，不要默认直接覆盖生产路径。
- **目标目录已存在内容**：默认不要覆盖；只有在用户明确要覆盖、或 agent 已完成核对后，才加 `--force`。
- **不确定备份包是否完整时**：先读取 manifest，再决定恢复范围；不要先覆盖再检查。

原则很简单：**先解出来、先核对，再决定怎么落位。**

## 默认备份内容

默认不再只看 workspace 根目录，而是打包一份更完整的 OpenClaw 备份清单：

- `~/.openclaw/workspace/` - 主工作区（包含 memory、skills、文档、媒体等）
- `~/.openclaw/openclaw.json` - 主配置
- `~/.openclaw/cron/` - 定时任务配置（如存在）
- `~/.openclaw/workspace/config/` - workspace 内补充配置（如存在）
- `openclaw/backup-manifest.json` - 本次备份实际包含内容清单

如果你传了 `--source`，则按你指定的目录或文件单独备份。

## 默认排除内容

为避免备份包过大、夹带无意义缓存，默认会排除这些内容：

- `.git/`
- `.ace-tool/`
- `.clawhub/`
- `__pycache__/`、`*.pyc`
- `node_modules/`
- `.cache/`
- `tmp/`、`temp/`
- `output/`、`outputs/` 及迁移前快照目录
- `.DS_Store`

这些排除规则也会写进 `backup-manifest.json`，方便你事后核对。

## 备份文件格式

备份文件以 tar.gz 压缩包形式存储，命名格式：
```
openclaw-backup-YYYYMMDD-HHMMSS.tar.gz
```

## 故障排除

详见 [references/config.md](references/config.md)
