---
name: schedule-manager
version: 1.0.0
description: 日程任务管理 - 查看/添加/修改/删除定时任务和临时提醒
metadata: {"openclaw":{"emoji":"📅"},"requires":{"bins":["bash","python3","edge-tts"]}}
tags: [schedule, task, cron, reminder, calendar, tts]
---

# schedule-manager

> 📅 管理工作区的定时任务和临时提醒

---

## 🚀 快速使用

```bash
# 查看所有任务
python scripts/schedule.py list

# 添加定时任务
python scripts/schedule.py add --time "07:00" --name "起床提醒" --type tts --content "早上好" --weekday "1-5"

# 添加临时任务（一次性）
python scripts/schedule.py temp --time "2026-03-02 10:00" --message "明天上午 10 点开会"

# 修改任务
python scripts/schedule.py edit "起床提醒" --time "07:30"

# 暂停任务
python scripts/schedule.py toggle "起床提醒"

# 删除任务
python scripts/schedule.py delete "起床提醒"
```

---

## 📋 命令说明

### 1. 查看任务

```bash
# 查看所有定时任务
python scripts/schedule.py list

# 查看临时任务
python scripts/schedule.py list --temp

# 查看今日待执行临时任务
python scripts/schedule.py list --today
```

### 2. 添加定时任务

```bash
python scripts/schedule.py add \
  --time "07:00" \
  --name "起床提醒" \
  --type "tts" \
  --content "早上好，该起床啦" \
  --weekday "1-5" \
  --notify "本地播放 + 飞书"
```

**参数说明：**

| 参数 | 说明 | 必填 | 默认值 |
|------|------|------|--------|
| `--time` | 执行时间 (HH:MM) | ✅ | - |
| `--name` | 任务名称 | ✅ | - |
| `--type` | 任务类型 (`tts`/`news`) | ✅ | - |
| `--content` | TTS 文本或新闻目录 | ✅ | - |
| `--weekday` | 星期规格 | ❌ | `1-7` |
| `--notify` | 通知方式 | ❌ | `本地播放` |

### 3. 添加临时任务

```bash
# 指定日期时间
python scripts/schedule.py temp \
  --time "2026-03-02 10:00" \
  --message "明天上午 10 点开会"

# 相对时间（1 小时后）
python scripts/schedule.py temp \
  --in "1h" \
  --message "1 小时后提醒我"

# 明天早上 8 点
python scripts/schedule.py temp \
  --tomorrow "08:00" \
  --message "明天早上 8 点提醒"
```

**临时任务参数：**

| 参数 | 说明 | 示例 |
|------|------|------|
| `--time` | 绝对时间 | `2026-03-02 10:00` |
| `--in` | 相对时间 | `30m` / `1h` / `2d` |
| `--tomorrow` | 明天指定时间 | `08:00` |
| `--message` | 提醒内容 | `"开会"` |
| `--notify` | 通知方式 | `本地播放` / `飞书` |

### 4. 修改任务

```bash
# 修改时间
python scripts/schedule.py edit "起床提醒" --time "07:30"

# 修改内容
python scripts/schedule.py edit "起床提醒" --content "早上好呀"

# 修改星期
python scripts/schedule.py edit "起床提醒" --weekday "1-7"

# 修改多个字段
python scripts/schedule.py edit "起床提醒" --time "07:30" --content "新内容"
```

### 5. 启用/暂停任务

```bash
# 切换状态（启用↔暂停）
python scripts/schedule.py toggle "起床提醒"

# 直接启用
python scripts/schedule.py enable "起床提醒"

# 直接暂停
python scripts/schedule.py disable "起床提醒"
```

### 6. 删除任务

```bash
# 删除定时任务
python scripts/schedule.py delete "起床提醒"

# 删除临时任务
python scripts/schedule.py delete --temp "临时任务 ID"

# 清理已过期的临时任务
python scripts/schedule.py cleanup
```

---

## 📁 文件结构

```
~/.openclaw/workspace/
├── daily-tasks.md              # 定时任务配置
├── calendar/
│   ├── temp-tasks.md           # 临时任务列表
│   └── daily-news/             # 新闻文件目录
├── task-logs/                  # 执行日志
└── skills/schedule-manager/
    ├── SKILL.md                # 本文件
    └── scripts/
        └── schedule.py         # 主脚本
```

---

## 🔧 技术细节

### 定时任务存储

**`daily-tasks.md`** - Markdown 表格格式：

```markdown
| 时间 | 任务名 | 类型 | 内容/参数 | 星期 | 通知方式 | 状态 |
|------|--------|------|----------|------|----------|------|
| 07:00 | 起床提醒 | tts | "早上好" | 1-5 | 本地播放 + 飞书 | ✅ |
```

### 临时任务存储

**`calendar/temp-tasks.md`** - YAML 格式：

```yaml
tasks:
  - id: "temp_001"
    time: "2026-03-02 10:00"
    message: "明天上午 10 点开会"
    notify: "本地播放 + 飞书"
    status: "pending"  # pending / done / expired
    created_at: "2026-03-01 18:00"
```

### crontab 集成

- 定时任务：通过 crontab 精确执行
- 临时任务：心跳轮询检查（每 5 分钟）

---

## 💡 使用场景

### 每日固定任务

```bash
# 工作日早上起床提醒
python scripts/schedule.py add \
  --time "07:00" \
  --name "起床提醒" \
  --type "tts" \
  --content "早上好，该起床啦" \
  --weekday "1-5"

# 每晚孩子睡觉提醒
python scripts/schedule.py add \
  --time "21:30" \
  --name "孩子洗漱" \
  --type "tts" \
  --content "宝贝，该洗漱准备睡觉啦" \
  --weekday "1-7"
```

### 临时提醒

```bash
# 1 小时后提醒
python scripts/schedule.py temp --in "1h" --message "该休息了"

# 明天早上 9 点会议
python scripts/schedule.py temp --tomorrow "09:00" --message "周会"

# 指定日期时间
python scripts/schedule.py temp --time "2026-03-05 14:00" --message "看牙医"
```

### 任务管理

```bash
# 查看所有任务
python scripts/schedule.py list

# 暂停周末任务
python scripts/schedule.py disable "周末跑步"

# 修改任务时间
python scripts/schedule.py edit "起床提醒" --time "07:30"
```

---

## ⚠️ 注意事项

1. **临时任务检查** - 需要心跳轮询（建议 5 分钟间隔）
2. **crontab 权限** - 确保用户有 crontab 权限
3. **时间格式** - 使用 24 小时制 (HH:MM)
4. **星期规格** - `1-5` (工作日), `1-7` (每天), `1,3,5` (隔天)
5. **任务名称** - 必须唯一，不能重复

---

## 🛠️ 故障排查

### 任务不执行

```bash
# 检查 crontab
crontab -l

# 检查任务状态
python scripts/schedule.py list

# 手动执行测试
~/.openclaw/workspace/scripts/run-task.sh "任务名" --force
```

### 临时任务不触发

```bash
# 查看临时任务列表
python scripts/schedule.py list --temp

# 检查心跳配置
cat ~/.openclaw/workspace/HEARTBEAT.md

# 手动触发检查
python scripts/schedule.py check-temp
```

---

## 📞 相关文档

- [定时任务配置](../../daily-tasks.md)
- [执行脚本](../../scripts/run-task.sh)
- [日历系统](../../calendar/README.md)
