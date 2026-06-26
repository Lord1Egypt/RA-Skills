# 🦞 三只虾协同体系 (Three Shrimp Collaboration)

**版本：** v1.0  
**创建：** 2026-03-09  
**适用：** OpenClaw 多 agent 协同场景

---

## 📋 概述

三只虾协同体系是一个**多 agent 任务分配、执行、通知的完整框架**，支持：

- ✅ 实时任务监控（fswatch，<1 秒触发）
- ✅ 自动心跳检查（工作时间 8:00-18:00）
- ✅ 任务完成自动通知
- ✅ 角色分工（CPMO/COO/CGO）

---

## 🎯 三只虾角色

| 角色 | 名字 | 职责 | Emoji |
|------|------|------|-------|
| **CPMO** | 终端虾（CPMO） | PMO 全权核心 | 🖥️ |
| **COO** | 飞书虾（COO） | 统筹 + 协管 | 📱 |
| **CGO** | Telegram 虾（CGO） | 副业全域执行 | 🌐 |

---

## 🚀 快速开始

### 1. 安装依赖

```bash
# 安装 fswatch（文件监控）
brew install fswatch
```

### 2. 配置心跳监控

```bash
# 加载 launchd 配置
cp scripts/com.openclaw.heartbeat.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.openclaw.heartbeat.plist

# 加载 fswatch 监控
cp scripts/com.openclaw.fswatch.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.openclaw.fswatch.plist
```

### 3. 验证状态

```bash
# 检查心跳服务
launchctl list | grep openclaw.heartbeat

# 检查监控服务
launchctl list | grep openclaw.fswatch

# 查看日志
tail -f ~/Library/Logs/openclaw/heartbeat.log
```

---

## 📁 文件结构

```
skills/three-shrimp-collab/
├── SKILL.md                          # 本文件
├── README.md                         # 详细文档
├── scripts/
│   ├── heartbeat-check.sh            # 心跳检查脚本
│   ├── fswatch-monitor.sh            # 文件监控脚本
│   ├── notify-task-complete.sh       # 任务完成通知脚本
│   ├── setup-heartbeat.sh            # 一键配置脚本
│   ├── com.openclaw.heartbeat.plist  # 心跳 launchd 配置
│   └── com.openclaw.fswatch.plist    # 监控 launchd 配置
├── tasks/
│   └── queue.md                      # 任务队列
├── logs/
│   ├── heartbeat-*.log               # 心跳日志
│   └── fswatch-monitor.log           # 监控日志
└── docs/
    ├── 三只虾分工体系.md              # 角色分工
    ├── 三只虾协同协议.md              # 协同规范
    ├── 三只虾汇报模板.md              # 汇报格式
    └── 三只虾自动化流程.md            # 流程图
```

---

## 📝 核心功能

### 1. 任务分配

**格式：**
```markdown
- [ ] [角色] 任务描述 - 分配人 @时间
```

**示例：**
```markdown
- [ ] [CPMO] 整理项目周报 - 飞书虾统筹 @2026-03-09 14:00
- [ ] [CGO] 写一篇小红书教程 - 老板 @2026-03-09 15:00
```

### 2. 任务执行

**终端虾（CPMO）流程：**
1. 检测到新任务（fswatch 监控）
2. 领取任务（更新为 `[~]` 处理中）
3. 执行任务
4. 标记完成（更新为 `[x]` 已完成）

### 3. 任务通知

**自动通知流程：**
1. 心跳检测完成任务
2. 生成通知消息
3. 飞书虾发送飞书消息给老板

**通知格式：**
```
✅ 任务完成

📋 任务：[CPMO] 整理项目周报
🦞 执行者：终端虾（CPMO）
⏰ 完成时间：2026-03-09 14:30

【任务结果】
具体内容...

---
_任务已完成，请老板查阅_
```

---

## 🕐 心跳机制

### 工作时间
- **时间：** 每天 8:00-18:00
- **频率：** 每小时一次
- **触发：** fswatch 实时监控（<1 秒）

### 检查层级

| 层级 | 频率 | 内容 |
|------|------|------|
| **Layer 1** | 每小时 | 快速检查任务队列 |
| **Layer 2** | 每天 12:00 | 完整同步（读取所有文件） |
| **Layer 3** | 每天 17:00 | 每日总结 |
| **Layer 4** | 实时 | 任务完成通知 |

---

## 🔧 配置选项

### 环境变量

```bash
# 飞书通知配置
export FEISHU_WEBHOOK="https://open.feishu.cn/open-apis/bot/v2/hook/xxx"
export FEISHU_USER_ID="ou_xxx"

# 工作时间配置
export WORK_START_HOUR=8
export WORK_END_HOUR=18
```

### 自定义心跳频率

编辑 `scripts/com.openclaw.heartbeat.plist`，修改 `StartCalendarInterval` 数组。

---

## 📊 监控和调试

### 查看服务状态

```bash
# 心跳服务
launchctl list | grep openclaw.heartbeat

# 监控服务
launchctl list | grep openclaw.fswatch
```

### 查看日志

```bash
# 心跳日志
tail -f ~/Library/Logs/openclaw/heartbeat.log

# 监控日志
tail -f ~/Library/Logs/openclaw/fswatch-monitor.log

# 任务通知日志
tail -f ~/Library/Logs/openclaw/pending-notifications.log
```

### 手动测试

```bash
# 手动执行心跳检查
./scripts/heartbeat-check.sh

# 手动触发通知
./scripts/notify-task-complete.sh "任务名称" "执行者" "完成时间" "详情"
```

---

## 🎯 使用场景

### 场景 1：老板分配任务

```
老板：飞书虾，给终端虾安排个活，整理下项目周报

飞书虾：好的老板！
✅ 已添加到任务队列
✅ 监控已触发
⏳ 等待终端虾执行
```

### 场景 2：任务自动通知

```
（终端虾完成任务后）
飞书虾：📱 自动发送飞书消息

✅ 任务完成
📋 任务：项目周报整理
🦞 执行者：终端虾
⏰ 完成时间：2026-03-09 14:30
📎 链接：https://feishu.cn/docx/xxx
```

### 场景 3：每小时进展简报

```
📊 三只虾进展简报（14:00）

【任务状态】
- [CPMO] 终端虾：编写项目周报（进行中 50%）
- [COO] 飞书虾：统筹今日汇报（已完成）
- [CGO] Telegram 虾：小红书文案（待处理）

【统计】
待处理：2 | 进行中：1 | 已完成：5
```

---

## 🚨 常见问题

### Q1: 任务监控不工作？
**A:** 检查 fswatch 服务是否运行：
```bash
launchctl list | grep openclaw.fswatch
```

### Q2: 通知没收到？
**A:** 检查 pending-notifications 文件：
```bash
cat logs/pending-notifications-*.md
```

### Q3: 心跳不执行？
**A:** 检查是否在工作时间（8:00-18:00），脚本会自动跳过非工作时间

### Q4: 如何临时关闭监控？
**A:** 
```bash
launchctl unload ~/Library/LaunchAgents/com.openclaw.fswatch.plist
```

---

## 📚 相关文档

- `三只虾分工体系.md` - 详细角色分工
- `三只虾协同协议.md` - 协同规范
- `三只虾汇报模板.md` - 汇报格式
- `三只虾自动化流程.md` - 流程图
- `HEARTBEAT.md` - 心跳配置

---

## 🎉 最佳实践

1. **任务命名清晰** - 包含角色、内容、截止时间
2. **及时更新状态** - 领取→处理中→完成
3. **主动汇报进展** - 重要任务实时同步
4. **定期清理任务** - 每日 17:00 清理旧任务

---

## 📝 更新日志

### v1.0 (2026-03-09)
- ✅ 初始版本
- ✅ fswatch 实时监控
- ✅ 心跳检查机制
- ✅ 任务完成自动通知
- ✅ 三只虾角色分工

---

_创建人：飞书虾（COO）_  
_批准人：老板_  
_最后更新：2026-03-09 16:23_
