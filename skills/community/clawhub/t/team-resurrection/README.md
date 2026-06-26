# Team Resurrection

一键打包 / 搬家 / 分身你的 Agent 团队配置。
保留 SOUL.md、MEMORY.md、团队成员、skills 等所有资料，换电脑或开新团队时一键搞定。

---

## 安装

```bash
clawhub install team-resurrection
```

---

## ⚠️ 权限说明

本 skill 执行时需要以下权限：

| 操作 | 文件 | 说明 |
|------|------|------|
| 读取/修改 | `~/.qclaw/openclaw.json` | 添加 agent 配置 |
| 读写文件系统 | `~/.qclaw/` | 复制 workspace、备份配置 |
| 创建 | cron 定时任务 | 定时任务迁移 |
| 执行 | `openclaw gateway restart` | 重启 Gateway 使配置生效 |

**安全措施：** 所有操作前自动备份到 `~/.qclaw/backup/`

---

## 特性

- **三合一**：打包 · 搬家 · 分身，一键切换
- **自动检测**：不硬编码路径，智能识别当前 workspace
- **安全优先**：操作前自动备份，配置 deep merge 不覆盖其他设置

## 快速开始

### 打包（备份 / 准备搬家）

```bash
cd ~/.qclaw/workspace/skills/team-resurrection
python3 pack.py
```

生成：`~/一键搬家包/{Agent名称}搬家包_YYYYMMDD.zip`

### 搬家（新环境恢复）

```bash
unzip 搬家包.zip && cd 搬家包 && python3 migrate.py
```

### 分身（同环境复制）

```bash
python3 clone.py --suffix "测试"
```

---

## 三大功能

| 功能 | 脚本 | 场景 |
|------|------|------|
| 打包 | `pack.py` | 备份 / 跨环境迁移 |
| 搬家 | `migrate.py` | 新环境恢复 |
| 分身 | `clone.py` | 同环境复制团队 |

---

## 版本

- **1.1.0**（2026-04-24）— 新增--dry-run/--no-cron/--no-restart细粒度控制，agents.list追加不替换，copy_team用配置路径，Zip Slip防御，审查展示cron payload