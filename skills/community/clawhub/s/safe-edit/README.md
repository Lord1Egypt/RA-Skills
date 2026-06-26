# 🛡️ safe-edit

> 安全配置修改辅助技能 for OpenClaw

在修改重要配置文件前自动设置回滚机制，支持多平台。

## ✨ 特性

- 🔄 自动备份 - 修改前自动备份原文件
- ⏱️ 延迟回滚 - 15 分钟后自动恢复备份
- ✅ 手动确认 - 确认成功后立即取消回滚
- 🌐 跨平台 - 支持 Linux / macOS / FreeBSD
- 🔒 安全优先 - 避免手误导致服务崩溃

## 📦 安装

```bash
# 方式1: 复制脚本到 OpenClaw 脚本目录
cp safe-edit.sh ~/.openclaw/scripts/
chmod +x ~/.openclaw/scripts/safe-edit.sh

# 方式2: 使用 ClawHub (如果有)
clawhub install safe-edit
```

## 🚀 使用方法

### 命令行

```bash
# 开始修改并设置回滚
safe-edit start /root/.openclaw/openclaw.json

# 确认成功，取消回滚
safe-edit confirm

# 取消回滚
safe-edit cancel

# 查看状态
safe-edit status
```

### 在 OpenClaw 中使用

```markdown
请使用 safe-edit 开始修改配置文件: /path/to/config.json
```

## 🔧 支持的系统

| 系统 | 回滚方式 | 依赖 |
|------|----------|------|
| Linux (Debian/Ubuntu) | at 命令 | at |
| Linux (RHEL/CentOS) | at 命令 | at |
| Linux (WSL) | at 命令 | at |
| macOS | at / sleep | at |
| FreeBSD | at 命令 | at |
| Windows (Git Bash) | schtasks / sleep | schtasks |
| Windows (MSYS/Cygwin) | sleep 后台进程 | - |

## 📁 文件结构

```
safe-edit/
├── SKILL.md           # OpenClaw Skill 定义
├── safe-edit.sh       # 主脚本
├── README.md          # 本文件
└── package.json       # npm 元数据
```

## 📜 许可证

MIT
