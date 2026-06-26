---
name: session-archive-manager
description: 智能管理OpenClaw会话文件 - 裁剪大session、生成智能总结、归档旧会话、清理空间。使用场景：session文件过大、需要释放磁盘空间、整理旧会话记录、自动定期归档。当用户提到"归档session"、"裁剪会话"、"清理session空间"、"整理旧会话"、"session太大"、"运行session归档"、"使用session归档skill"时，立即使用此skill。
---

# Session Archive Manager - 会话归档管理器

智能裁剪、总结、提取和归档OpenClaw会话文件的工具集。

## 功能特性

- ✅ **智能裁剪** - 保留最近N条消息，裁剪旧消息
- ✅ **AI总结** - 自动生成被裁剪消息的智能摘要
- ✅ **完整备份** - 压缩备份原始文件到归档目录
- ✅ **空间释放** - 大幅减小session文件大小
- ✅ **定期归档** - 支持cron定时任务自动处理

## 快速开始

### 主要脚本

所有脚本位于 `scripts/` 目录：

| 脚本 | 功能 |
|------|------|
| `trim_and_archive.sh` | **主要入口** - 裁剪大文件 + 归档旧文件 |
| `archive_with_summary.sh` | 带总结的会话归档 |
| `archive_sessions.sh` | 基础会话归档 |
| `cleanup_old_sessions.sh` | 清理旧会话 |
| `setup_cron.sh` | 设置定时任务 |

### 使用方法

#### 1. 一键裁剪和归档（推荐）

```bash
# 进入skill目录
cd ~/.agents/skills/session-archive-manager

# 运行主要脚本
./scripts/trim_and_archive.sh
```

**默认配置：**
- 裁剪阈值：2MB
- 保留消息：150条
- 归档目录：`~/.openclaw/agents/main/sessions/archive/`
- 总结目录：`~/.openclaw/agents/main/sessions/summaries/`

#### 2. 自定义配置

编辑脚本中的变量：

```bash
# 在 trim_and_archive.sh 中修改：
MAX_SIZE_MB=2          # 裁剪阈值（MB）
KEEP_MESSAGES=150       # 保留消息数
```

#### 3. 设置定时自动归档

```bash
cd ~/.agents/skills/session-archive-manager
./scripts/setup_cron.sh
```

这会设置每天凌晨2点自动运行归档任务。

## 脚本详解

### trim_and_archive.sh - 智能裁剪归档主脚本

**功能流程：**
1. 扫描超过阈值的大session文件
2. 对每个大文件：
   - 使用AI生成旧消息总结
   - 压缩备份完整文件
   - 裁剪原文件，只保留最近N条
3. 运行常规归档处理旧文件

**输出示例：**
```
=== 裁剪完成 ===
原文件大小: 2.1M → 0.33M
保留消息: 150条
归档消息: 686条
总结已保存: summaries/xxx_trim_summary.json
备份已保存: archive/xxx_full.jsonl.gz
```

### session_trimmer.py - Python裁剪工具

**功能：**
- 读取.jsonl会话文件
- 分离新旧消息
- 调用AI生成旧消息总结
- 裁剪并重写原文件

**使用：**
```bash
python session_trimmer.py <session-file> [keep-count]
```

### archive_with_summary.sh - 带总结的归档

归档旧session的同时生成智能总结，适合清理不常用的会话。

### setup_cron.sh - 设置定时任务

自动添加cron任务，定期运行归档脚本。

## 目录结构

处理后的session目录结构：

```
~/.openclaw/agents/main/sessions/
├── *.jsonl              # 当前活动会话（裁剪后）
├── archive/             # 归档目录
│   ├── *.jsonl.gz       # 压缩备份的完整会话
│   └── *.jsonl          # 未压缩归档（如有）
├── summaries/           # 总结目录
│   └── *_summary.json   # AI生成的会话总结
└── sessions.json        # 会话索引
```

## 最佳实践

### 1. 定期检查

每周运行一次裁剪归档，保持session目录整洁：
```bash
cd ~/.agents/skills/session-archive-manager
./scripts/trim_and_archive.sh
```

### 2. 监控空间

检查session目录大小：
```bash
du -sh ~/.openclaw/agents/main/sessions/
```

### 3. 查看总结

随时查看已归档会话的总结：
```bash
cat ~/.openclaw/agents/main/sessions/summaries/*.json
```

### 4. 恢复备份

如需恢复完整会话：
```bash
cd ~/.openclaw/agents/main/sessions/archive/
gunzip xxx_full_20260328_081132.jsonl.gz
cp xxx_full_20260328_081132.jsonl ../xxx.jsonl
```

## 故障排除

### Lock文件问题

如果看到 `.lock` 文件，先删除：
```bash
rm -f ~/.openclaw/agents/main/sessions/*.lock
```

### 权限问题

确保脚本有执行权限：
```bash
chmod +x ~/.agents/skills/session-archive-manager/scripts/*.sh
chmod +x ~/.agents/skills/session-archive-manager/scripts/*.py
```

### Python依赖

确保有Python 3和所需库：
```bash
python3 --version
pip3 install json argparse datetime collections
```

## 配置参考

### 环境变量

可在运行前设置：
```bash
export SESSION_DIR="/path/to/sessions"
export ARCHIVE_DIR="/path/to/archive"
export SUMMARY_DIR="/path/to/summaries"
```

### 脚本变量

各脚本中的可调参数：

**trim_and_archive.sh:**
- `MAX_SIZE_MB=2` - 触发裁剪的文件大小
- `KEEP_MESSAGES=150` - 保留的消息数量
- `ARCHIVE_DAYS=2` - 归档旧文件的天数阈值

**archive_with_summary.sh:**
- `MAX_FILE_SIZE_MB=1` - 归档文件大小阈值
- `MAX_FILE_AGE_DAYS=2` - 归档文件天数阈值

## 总结预览

生成的总结JSON格式：

```json
{
  "trim_time": "2026-03-28T08:11:32.050922",
  "trimmed_count": 686,
  "kept_count": 150,
  "time_range": {
    "start": "2026-03-27T06:07:44.872000+00:00",
    "end": "2026-03-27T14:50:34.023000+00:00"
  },
  "statistics": {
    "user_messages": 48,
    "assistant_messages": 343,
    "tool_calls": 0
  },
  "topics": ["创建", "配置", "session", "文件"],
  "files_mentioned": ["SOUL.md", "USER.md", "sessions.json"]
}
```

---

**记住：** 先备份，后裁剪！这个工具会自动帮你完成备份，但小心驶得万年船。🚀
