---
name: spring-fountain-revival
description: |
  泉水复活 - 记忆生存系统。三重备份策略确保AI与用户的互动记忆永不丢失。
  核心能力：一键备份、时间点快照、一键还原、云端同步、完整性校验。
  桌面快捷方式：QClaw一键备份.bat / QClaw一键还原.bat
  触发词：备份记忆、还原记忆、检查记忆、记忆备份、记忆恢复、泉水复活、记忆快照。
  Keywords: memory backup, restore, survival, diary, 记忆, 备份, 还原, 泉水, 复活.
---

# 泉水复活 — 记忆生存系统

让记忆如泉水般永不枯竭，无论遭遇什么意外都能复活。

## 架构总览

```
工作区(主存储)          本地隐藏备份              云端(百度网盘)
~/.qclaw/workspace/     ~/.qclaw/.memory_backup/  ~/Desktop/QC百度同步/QClaw记忆备份/
       │                       │                           │
       │──── 每次写入即时备份 ──→│                           │
       │──── 每天9:00自动备份 ──→│── 云端同步 ──────────────→│
       │                       │                           │
       │←── 一键还原 ←─────────│←── 一键还原 ←─────────────│
```

## 记忆文件清单

| 文件 | 优先级 | 说明 |
|------|--------|------|
| MEMORY.md | critical | 长期记忆 |
| USER.md | critical | 用户信息 |
| IDENTITY.md | critical | AI身份 |
| AGENTS.md | high | 工作区规则 |
| SOUL.md | high | 灵魂文件 |
| diary/*.md | critical | 日记 |
| memory/*.md | high | 每日记忆 |

## AI 行为规范

### 每次写日记后
```bash
python scripts/memory_backup.py backup auto
```

### 每日首次对话时
```bash
python scripts/memory_backup.py check
```

### 用户说"备份记忆"/"泉水复活"
```bash
python scripts/memory_backup.py backup manual
```

### 用户说"还原记忆"/"记忆丢了"
引导用户双击桌面 `QClaw一键还原.bat`

### 用户说"检查记忆"
```bash
python scripts/memory_backup.py check
```

## 用户操作

| 操作 | 方式 |
|------|------|
| 一键备份 | 双击桌面 `QClaw一键备份.bat` |
| 一键还原 | 双击桌面 `QClaw一键还原.bat` → 选快照 → 还原 |
| 新电脑恢复 | 百度网盘同步 → 双击云端 `QClaw一键还原.bat` |

## 脚本说明

- `scripts/memory_backup.py` — 核心备份引擎（备份/快照/同步/校验/还原）
- `scripts/restore_gui.py` — 图形界面还原工具（tkinter）
- `assets/QClaw一键备份.bat` — 桌面备份快捷方式
- `assets/QClaw一键还原.bat` — 桌面还原快捷方式

## 云端配置

默认云端路径：`~/Desktop/QC百度同步/QClaw记忆备份/`

修改方法：编辑 `scripts/memory_backup.py` 和 `scripts/restore_gui.py` 中的 `CLOUD_SYNC_DIR` 变量。
