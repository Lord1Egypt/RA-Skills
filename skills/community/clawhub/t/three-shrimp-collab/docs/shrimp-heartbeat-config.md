# 🦞 三只虾心跳配置说明

_2026-03-09 创建_

---

## 一、心跳机制概述

### 工作时间
- **时间：** 每天 8:00-18:00（共 11 次检查）
- **频率：** 每小时一次
- **下班后：** 不执行（节省 token）

### 检查层级

| 层级 | 时间 | 内容 | Token 消耗 |
|------|------|------|-----------|
| **Layer 1** | 每小时 | 快速检查任务队列 | ~500 |
| **Layer 2** | 每天 12:00 | 完整同步（读取所有文件） | ~8000 |
| **Layer 3** | 每天 17:00 | 每日总结（清理旧任务） | ~15000 |

**预估成本：** ~$5-8/月（三只虾合计）

---

## 二、自动执行配置

### 方案 A：macOS launchd（推荐）

**适用：** 本地 Mac 运行 OpenClaw

#### 1. 创建 plist 文件

```bash
# 创建目录
mkdir -p ~/Library/LaunchAgents

# 创建 plist 文件
cat > ~/Library/LaunchAgents/com.openclaw.heartbeat.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
 "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.openclaw.heartbeat</string>
    
    <key>ProgramArguments</key>
    <array>
        <string>/Users/zhangyang/.openclaw/workspace/scripts/heartbeat-check.sh</string>
    </array>
    
    <key>StartCalendarInterval</key>
    <array>
        <!-- 8:00 -->
        <dict><key>Hour</key><integer>8</integer><key>Minute</key><integer>0</integer></dict>
        <!-- 9:00 -->
        <dict><key>Hour</key><integer>9</integer><key>Minute</key><integer>0</integer></dict>
        <!-- 10:00 -->
        <dict><key>Hour</key><integer>10</integer><key>Minute</key><integer>0</integer></dict>
        <!-- 11:00 -->
        <dict><key>Hour</key><integer>11</integer><key>Minute</key><integer>0</integer></dict>
        <!-- 12:00 -->
        <dict><key>Hour</key><integer>12</integer><key>Minute</key><integer>0</integer></dict>
        <!-- 13:00 -->
        <dict><key>Hour</key><integer>13</integer><key>Minute</key><integer>0</integer></dict>
        <!-- 14:00 -->
        <dict><key>Hour</key><integer>14</integer><key>Minute</key><integer>0</integer></dict>
        <!-- 15:00 -->
        <dict><key>Hour</key><integer>15</integer><key>Minute</key><integer>0</integer></dict>
        <!-- 16:00 -->
        <dict><key>Hour</key><integer>16</integer><key>Minute</key><integer>0</integer></dict>
        <!-- 17:00 -->
        <dict><key>Hour</key><integer>17</integer><key>Minute</key><integer>0</integer></dict>
    </array>
    
    <key>WorkingDirectory</key>
    <string>/Users/zhangyang/.openclaw/workspace</string>
    
    <key>StandardOutPath</key>
    <string>/Users/zhangyang/.openclaw/logs/heartbeat-stdout.log</string>
    
    <key>StandardErrorPath</key>
    <string>/Users/zhangyang/.openclaw/logs/heartbeat-stderr.log</string>
</dict>
</plist>
EOF
```

#### 2. 加载服务

```bash
# 加载
launchctl load ~/Library/LaunchAgents/com.openclaw.heartbeat.plist

# 检查状态
launchctl list | grep openclaw.heartbeat

# 卸载（如需要）
launchctl unload ~/Library/LaunchAgents/com.openclaw.heartbeat.plist
```

---

### 方案 B：cron

**适用：** Linux 服务器或 macOS

```bash
# 编辑 crontab
crontab -e

# 添加以下内容（每小时 8:00-17:00）
0 8-17 * * * /Users/zhangyang/.openclaw/workspace/scripts/heartbeat-check.sh >> /Users/zhangyang/.openclaw/logs/heartbeat.log 2>&1
```

---

### 方案 C：OpenClaw HEARTBEAT.md 集成

**适用：** OpenClaw 内置心跳机制

**说明：** OpenClaw 会自动读取 `HEARTBEAT.md` 并按配置执行

**配置：** 已在 `HEARTBEAT.md` 中定义，无需额外配置

---

## 三、手动触发

### 测试心跳脚本

```bash
# 手动执行
/Users/zhangyang/.openclaw/workspace/scripts/heartbeat-check.sh

# 查看日志
tail -f /Users/zhangyang/.openclaw/logs/heartbeat.log
```

### 强制完整同步

```bash
# 创建强制同步标记
touch /Users/zhangyang/.openclaw/workspace/.force-heartbeat

# 下次心跳时会执行完整同步
```

---

## 四、监控和调试

### 查看执行日志

```bash
# 最近 10 条日志
tail -n 10 /Users/zhangyang/.openclaw/logs/heartbeat.log

# 搜索错误
grep -i error /Users/zhangyang/.openclaw/logs/heartbeat.log

# 查看今天的所有执行
grep "$(date +%Y-%m-%d)" /Users/zhangyang/.openclaw/logs/heartbeat.log
```

### 检查服务状态

```bash
# launchd
launchctl list | grep openclaw.heartbeat

# cron
crontab -l

# 进程
ps aux | grep heartbeat
```

---

## 五、文件结构

```
/Users/zhangyang/.openclaw/workspace/
├── HEARTBEAT.md                    # 心跳配置（主文件）
├── 三只虾协同协议.md                # 协同规范
├── 三只虾分工体系.md                # 职责说明
├── MEMORY.md                       # 长期记忆
├── tasks/
│   └── queue.md                    # 任务队列
├── scripts/
│   └── heartbeat-check.sh          # 心跳检查脚本
└── logs/
    ├── heartbeat.log               # 心跳日志
    ├── heartbeat-stdout.log        # 标准输出
    └── heartbeat-stderr.log        # 错误输出
```

---

## 六、常见问题

### Q1: 为什么心跳不执行？
**A:** 检查是否在工作时间（8:00-18:00），脚本会自动跳过非工作时间

### Q2: token 消耗太高怎么办？
**A:** 调整心跳频率，或关闭 Layer 2/3（修改 HEARTBEAT.md）

### Q3: 如何临时关闭心跳？
**A:** 在 `HEARTBEAT.md` 顶部添加 `# DISABLED` 标记

### Q4: 周末也执行吗？
**A:** 默认执行，如需关闭可在脚本中添加周末判断

---

## 七、下一步

1. ✅ 选择执行方案（推荐 launchd）
2. ✅ 配置自动执行
3. ✅ 测试第一次心跳
4. ✅ 观察 1-2 天，优化配置

---

_创建人：飞书虾（飞书 COO）_
_批准人：老板（CEO）_
