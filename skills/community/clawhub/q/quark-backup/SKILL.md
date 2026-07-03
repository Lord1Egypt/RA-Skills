---
name: quark-backup
description: OpenClaw 定时备份技能，将 .openclaw 目录打包上传至夸克网盘。触发条件：（1）用户提到"备份"、"自动备份"、"定时备份"、"上传夸克"；（2）配置每天 04:00 自动备份任务；（3）手动触发一次性备份。执行时会打包 workspace、memory、sessions、配置等，排除 node_modules 和浏览器缓存。
---

# quark-backup

## 功能概述

将 OpenClaw 的 `.openclaw` 目录打包为 tar.gz 并上传到夸克网盘指定目录，支持每日定时自动执行。

## 快速开始

### 手动执行备份

```bash
cd /home/openclaw/.openclaw/workspace
bash tools/kuake/backup-openclaw-full.sh
```

脚本会自动：
1. 打包 `.openclaw`（排除 node_modules、浏览器缓存）
2. 在夸克网盘 `/openclaw/` 创建目标目录
3. 上传压缩包
4. 校验上传是否成功

### 配置每日自动备份（04:00）

使用 cron 调度：
```bash
# 每天 04:00 执行备份
0 4 * * * cd /home/openclaw/.openclaw/workspace && bash tools/kuake/backup-openclaw-full.sh >> /home/openclaw/log/backup.log 2>&1
```

## 工作流程

### 首次配置（需要 Cookie）

1. 登录 https://pan.quark.cn
2. 浏览器开发者工具复制 Cookie
3. 写入 `/home/openclaw/.config/openclaw-quark-backup.env`：
   ```bash
   KUAKE_COOKIE='你的完整Cookie'
   ```

### 备份脚本结构

```
tools/kuake/
├── bin/kuake          # kuake CLI 二进制
├── use-kuake.sh       # 包装脚本（设置 Cookie 环境变量）
├── backup-openclaw-full.sh  # 主备份脚本
└── .env               # 不存在则跳过（Cookie 由上一步提供）
```

### 打包排除项

- `node_modules`（可重建，节省空间）
- Chrome 浏览器配置文件
- CDP profile 和 browser-runtime
- `tools/kuake/.env`（敏感信息）

## 本地保留备份（可选）

如需在本地也留一份备份，修改脚本将 ARCHIVE 路径改为本地目录：

```bash
LOCAL_BACKUP_DIR="${OPENCLAW_HOME}/local-backups"
ARCHIVE="${LOCAL_BACKUP_DIR}/openclaw-full-backup-${STAMP}.tar.gz"
mkdir -p "$LOCAL_BACKUP_DIR"
```

## 恢复流程

1. 从夸克网盘 `/openclaw/` 下载最新备份
2. 解压到新机器的 `/home/openclaw/` 下
3. 重新安装 OpenClaw：`npm install -g openclaw`
4. 重新配置 cron 任务
5. 重新配置夸克 Cookie

## 注意事项

- Cookie 有时效性，约 30 天检查一次是否失效
- 备份文件命名格式：`openclaw-full-backup-YYYYMMDD-HHMMSS.tar.gz`
- 备份目标目录：`/openclaw/`（可修改 `KUAKE_REMOTE_DIR` 环境变量）
- 备份本身不包含 OpenClaw 全局包，需在新环境重新安装