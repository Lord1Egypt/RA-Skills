# 🧊💦 泉水复活 (Spring Fountain Revival)

> 让记忆如泉水般永不枯竭，无论遭遇什么意外都能复活。

AI 与用户互动记忆的终极生存系统。三重备份 + 时间点快照 + 一键还原。

## ✨ 特性

- 🧠 **全面备份** — 自动扫描所有记忆文件（MEMORY.md、日记、用户信息等）
- ⏱️ **时间点快照** — 每次备份生成带时间戳的 zip 快照，可还原到任意时间点
- ☁️ **云端同步** — 自动同步到云盘（默认百度网盘，可配置）
- 🔒 **本地隐藏备份** — 独立于工作区的隐藏目录，防误删
- ⚡ **一键还原** — 图形界面，双击选择快照即可还原
- 🔍 **完整性校验** — SHA256 哈希比对，发现不一致立即告警
- 📅 **自动备份** — 每日定时自动备份（支持 cron）
- 💻 **桌面快捷方式** — 一键备份 / 一键还原，零门槛操作

## 📁 记忆文件清单

| 文件 | 说明 |
|------|------|
| `MEMORY.md` | 长期记忆（重要事件、决策、偏好） |
| `USER.md` | 用户信息（姓名、偏好、时区） |
| `IDENTITY.md` | AI 身份（名字、性格、头像） |
| `AGENTS.md` | 工作区规则 |
| `SOUL.md` | 灵魂文件 |
| `diary/*.md` | 日记文件 |
| `memory/*.md` | 每日记忆 |

## 🛡️ 三重备份架构

```
工作区(主存储)              本地隐藏备份                云端
~/.qclaw/workspace/         ~/.qclaw/.memory_backup/    ~/Desktop/QC百度同步/QClaw记忆备份/
       │                           │                             │
       │──── 即时/定时备份 ────────→│                             │
       │                           │──── 云端同步 ──────────────→│
       │                           │                             │
       │←──── 一键还原 ←──────────│←──── 一键还原 ←────────────│
```

## 🚀 安装

### 方式一：作为 OpenClaw Skill 安装

```bash
# 克隆到 skill 目录
git clone https://github.com/你的用户名/泉水复活skill.git ~/.qclaw/skills/spring-fountain-revival
```

### 方式二：手动安装

1. 下载整个仓库
2. 将文件夹复制到 `~/.qclaw/skills/spring-fountain-revival/`
3. 运行一次备份初始化：

```bash
python ~/.qclaw/skills/spring-fountain-revival/scripts/memory_backup.py backup init
```

## ⚡ 使用方式

### 桌面快捷方式

在桌面创建两个文本文件：

**QClaw一键备份.bat** (内容):
```bat
@echo off
python "%USERPROFILE%\.qclaw\workspace\scripts\memory_backup.py" backup manual
pause
```

**QClaw一键还原.bat** (内容):
```bat
@echo off
python "%USERPROFILE%\.qclaw\workspace\scripts\restore_gui.py"
pause
```

### 命令行

```bash
# 完整备份（本地 + 快照 + 云端）
python scripts/memory_backup.py backup [标签]

# 仅创建快照
python scripts/memory_backup.py snapshot [标签]

# 同步到云端
python scripts/memory_backup.py sync

# 列出所有快照
python scripts/memory_backup.py list

# 还原（交互式选择快照）
python scripts/memory_backup.py restore

# 快速还原最新备份
python scripts/memory_backup.py restore latest

# 完整性检查
python scripts/memory_backup.py check
```

## ☁️ 云端配置

编辑 `scripts/memory_backup.py` 中的 `CLOUD_SYNC_DIR` 变量：

```python
# 默认配置（百度网盘）
CLOUD_SYNC_DIR = Path(r"C:\Users\Administrator\Desktop\QC百度同步\QClaw记忆备份")

# 修改为你的云盘路径，例如：
# CLOUD_SYNC_DIR = Path(r"D:\OneDrive\QClaw记忆备份")
# CLOUD_SYNC_DIR = Path.home() / "坚果云" / "QClaw记忆备份"
```

同时编辑 `scripts/restore_gui.py` 中相同的变量保持一致。

## 🆘 灾难恢复

### 场景：电脑报废，换新电脑

1. 新电脑安装 Python 3.8+
2. 安装云盘软件并登录，等待同步
3. 打开云盘目录中的 `QClaw一键还原.bat`
4. 选择最新快照 → 一键还原
5. **记忆重生！**

### 场景：误删工作区文件

双击桌面 `QClaw一键还原.bat` → 还原最新备份

### 场景：云盘也挂了

本地隐藏目录 `~/.qclaw/.memory_backup/` 是最后防线，只要硬盘还在就能恢复。

## 📂 文件结构

```
泉水复活skill/
├── SKILL.md                          # Skill 描述（OpenClaw 加载用）
├── README.md                         # 本文件
└── scripts/
    ├── memory_backup.py              # 核心备份引擎
    └── restore_gui.py                # 图形界面还原工具
```

> **注意**：桌面快捷方式请手动创建，见上方说明。

## 📜 License

MIT
