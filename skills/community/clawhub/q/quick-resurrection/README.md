# Quick Resurrection

打包并恢复你的 OpenClaw Agent 工作区配置。
换电脑或重装系统后，一个命令把整个团队迁移到新环境。
执行前展示配置内容供用户确认，确认后全自动执行。

---

## ⚠️ 重要提示

**打包内容含敏感信息。** 搬家包会包含 MEMORY.md、TOOLS.md 等文件，可能含有 API keys、账号密码、内部流程等敏感内容。请妥善保管搬家包，不要随意分享。

---

## 特性

- **零门槛**：一条命令完成打包/迁移
- **安全优先**：自动备份，config 合并不覆盖
- **通用适配**：支持 Main Agent + 任意数量子代理
- **跨平台**：Mac / Windows / Linux 均可用

## 快速开始

### 打包（旧环境）

```bash
cd ~/.qclaw/workspace/skills/quick-resurrection
python3 pack.py
```

### 迁移（新环境）

```bash
python3 migrate.py
```

按提示完成，全程引导式。

## 核心功能

| 功能 | 说明 |
|------|------|
| 自动检测 workspace | 读 openclaw.json，自动推断 active workspace |
| 自动备份 | 搬家前备份到 `~/.qclaw/backup/` |
| 配置合并 | deep merge，保护新环境原有配置 |
| 通用打包 | 有团队打包团队，无团队跳过 |
| 跨平台 | Mac / Windows / Linux |

---

## 权限说明

本 skill 需要以下权限：

| 操作 | 文件 | 说明 |
|------|------|------|
| 读取/修改 | `~/.qclaw/openclaw.json` | 添加/合并 agent 配置 |
| 读写文件系统 | `~/.qclaw/` | 复制 workspace、备份配置 |
| 创建 | cron 定时任务 | 定时任务迁移 |
| 执行 | `openclaw gateway restart` | 重启 Gateway 使配置生效 |

**安全措施：**
- 所有操作前自动备份到 `~/.qclaw/backup/`
- 执行前**展示所有变更内容**（含 cron payload），用户确认后全自动执行
- allowAgents 使用**最小白名单**（仅实际成员ID），不使用通配符 `["*"]`

---

## 版本

- **v3.0**（2026-04-24）— 新增--dry-run/--no-cron/--no-restart，merge_config写入前展示diff，agents.list追加不替换，Zip Slip防御，审查展示cron payload