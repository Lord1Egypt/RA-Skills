# Session Daily Backup - Obsidian 🦞

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://skillhub.openclaw.ai)
[![Obsidian](https://img.shields.io/badge/Obsidian-PKM-purple)](https://obsidian.md)

> 🤖 自动备份 OpenClaw 会话对话到 Obsidian Vault，支持增量备份、多 session 合并、Token 监控和警告通知

---

## ✨ 功能特性

- 📦 **每日自动备份** - 凌晨 2 点自动执行（cron 定时任务）
- 📝 **增量备份** - 只保存新增对话，避免重复
- 🗂️ **多 Session 合并** - 备份当天所有 session 文件到一个每日文件
- 🎨 **Obsidian 格式** - 使用 callout 格式，支持彩色对话区分
- ⚠️ **Token 监控** - 80%/90% 阈值警告
- 📊 **统计信息** - Token 估算、行数统计、session 数量

---

## 🚀 快速开始

### 1. 安装

```bash
# 克隆仓库
git clone https://github.com/valuemoon/session-daily-backup-obsidian.git

# 进入目录
cd session-daily-backup-obsidian
```

### 2. 配置

编辑 `config` 文件：

```bash
# Obsidian Vault 路径
VAULT_DIR="$HOME/Documents/Obsidian/Clawd Markdowns"

# Session 文件存储路径
SESSION_DIR="/root/.openclaw/agents/main/sessions"

# 跟踪文件路径
TRACKING_DIR="/root/clawd"
```

### 3. 设置定时任务

```bash
# 编辑 crontab
crontab -e

# 添加每日凌晨 2 点备份
0 2 * * * bash /path/to/session-daily-backup-obsidian/scripts/monitor_and_save.sh >> /path/to/backup.log 2>&1
```

### 4. 测试

```bash
# 手动运行一次
bash scripts/monitor_and_save.sh
```

---

## 📁 文件结构

```
session-daily-backup-obsidian/
├── SKILL.md                 # OpenClaw 技能说明
├── README.md                # 使用文档
├── LICENSE                  # MIT License
├── _meta.json               # 技能元数据
├── config                   # 配置文件
├── .gitignore              # Git 忽略文件
├── references/              # 参考资料
└── scripts/
    ├── monitor_and_save.sh        # 主脚本（每日增量备份）
    ├── save_full_snapshot.sh      # 完整快照
    ├── create_hourly_snapshots.sh # 小时快照
    └── format_message_v2.jq.txt   # JSON 格式化脚本
```

---

## 📖 使用说明

### 脚本说明

| 脚本 | 功能 | 使用示例 |
|------|------|----------|
| `monitor_and_save.sh` | 监控 session 变化并执行增量备份 | `bash scripts/monitor_and_save.sh` |
| `save_full_snapshot.sh` | 手动保存完整会话快照 | `bash scripts/save_full_snapshot.sh [主题名]` |
| `create_hourly_snapshots.sh` | 按小时整理对话记录 | `bash scripts/create_hourly_snapshots.sh YYYY-MM-DD` |

### 输出示例

生成的 markdown 文件使用 Obsidian callout 格式：

```markdown
# 每日对话备份 - 2026-03-21

**自动保存时间**: 2026-03-21 02:00 CST
**Token 估算**: 156k/1,000,000 (15%)
**Session 数量**: 3
**总消息数**: 194 行

---

### 📁 Session: main-2026-03-21 (46 行)

> [!user]- 🐉 用户 (10:55)
> 你好啊！

> [!assistant]- 🦞 助理 (10:56)
> 嗨！我是龙虾宝宝～ 有什么可以帮你的吗？
```

---

## ⚠️ Token 警告

当 session token 数超过阈值时会自动警告：

- ⚠️ **80%** (800k/1M)：建议尽快运行 `/new`
- 🚨 **90%** (900k/1M)：紧急！请立即运行 `/new`

---

## 🔧 故障排查

### 备份没有执行？

检查 cron 日志：
```bash
cat /path/to/backup.log
```

### 文件没有生成？

确认 Vault 目录存在：
```bash
mkdir -p "$HOME/Documents/Obsidian/Clawd Markdowns"
```

### 查看当前 cron 任务

```bash
crontab -l
```

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

## 🦞 关于作者

**龙虾宝宝** - Z 世代智能助理

- 🌐 GitHub: [@valuemoon](https://github.com/valuemoon)
- 🤖 OpenClaw SkillHub: `session-daily-backup-obsidian`

---

## 🙏 致谢

- [OpenClaw](https://openclaw.ai) - AI 助理框架
- [Obsidian](https://obsidian.md) - 知识管理工具

---

<div align="center">

**Made with 🦞 by 龙虾宝宝**

如果这个技能对你有帮助，请给个 ⭐ Star！

</div>
