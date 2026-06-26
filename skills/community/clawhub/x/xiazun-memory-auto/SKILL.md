---
name: memory-auto-manager
version: 1.0.0
description: |
  记忆自动主动管理：每15分钟自动扫描对话，发现重要信息自动写入每日memory。解决"主动感知靠自觉经常失效"的问题。
  
  使用场景：
  - 每次对话结束后自动检查是否有遗漏的重要信息
  - 自动记录完成的任务、决策、教训、配置变更
  - 增量扫描对话历史，不遗漏不重复
  - user + assistant 消息双读，确保不漏AI回复中的结论
  
  核心组件：
  - memory-scan.py：增量扫描脚本
  - 两个 cron：Memory自动检查（每15分钟）+ 每周六记忆合并
  
  适用版本：OpenClaw
allowed-tools: ["exec", "read", "write"]
---

# Memory Auto Manager Skill

自动记忆管理系统，解决"agent经常忘记记录重要信息"的问题。

## 核心机制

**Hybrid 方案：cron 自动扫描 + AI 对比判断**

```
每15分钟 cron 自动触发
        ↓
exec 运行 memory-scan.py
        ↓
读取主会话 transcript .jsonl（增量：只读新消息，user+assistant 都读）
        ↓
读取当前 memory 文件
        ↓
AI 分析：对话 vs 现有memory → 判断是否有遗漏
        ↓
有遗漏 → 写入 memory/YYYY-MM-DD.md + 更新 last-memory-write.json
无遗漏 → 静默结束
```

## 判断标准

满足任一 → **必须写入 memory**：
1. 完成了什么（任务、里程碑）
2. 确认了什么（方案、决策）
3. 发现了什么（关键数据）
4. 犯了什么错（教训、踩坑）
5. 配置改了什么
6. 有阻塞/待确认

**不写入**：过程讨论、简单确认、无结论的闲聊

## 文件结构

```
~/.openclaw/
├── agents/main/sessions/
│   └── {session-id}.jsonl              ← 主会话 transcript
├── scripts/
│   └── memory-scan.py                   ← 扫描脚本
└── workspace/
    ├── memory/
    │   ├── YYYY-MM-DD.md               ← 每日 memory
    │   ├── last-memory-write.json       ← 上次写入时间
    │   └── scan-state.json             ← 增量扫描状态
    └── HEARTBEAT.md                    ← 汇报规则
```

## 快速安装

### Step 1：创建 cron（自动检查，每15分钟）

```bash
openclaw cron add \
  --name "Memory自动检查V3" \
  --every "15m" \
  --session isolated \
  --message "你是记忆管理员。执行memory扫描：
1. exec 运行：python3 ~/.openclaw/scripts/memory-scan.py
2. 读取输出的新消息内容（user + assistant）
3. 分析是否有重要信息（完成的任务/决策/教训/配置变更）
4. 有重要信息？→ 写入 memory/YYYY-MM-DD.md + 更新 last-memory-write.json
5. 输出：检查完成，写入X条/无新增

判断标准：
- 完成了什么（任务、里程碑）
- 确认了什么（方案、决策）
- 发现了什么（关键数据）
- 犯了什么错（教训、踩坑）
- 配置改了什么
- 有阻塞/待确认" \
  --tools "exec,read,write" \
  --no-deliver
```

### Step 2：创建 cron（每周六记忆合并）

```bash
openclaw cron add \
  --name "每周六记忆合并" \
  --cron "0 0 * * 6" \
  --tz "Asia/Shanghai" \
  --session isolated \
  --message "你是记忆管理员。每周六自动执行记忆合并。
1. 读取本周所有 memory/YYYY-MM-DD.md 文件
2. 提炼重要信息：里程碑/教训/关键数据/配置变更/决策
3. 合并写入 MEMORY.md 对应区块
4. 更新 last-memory-write.json 的 lastMemoryMerge
5. 向用户发送合并完成通知" \
  --timeout-seconds 300 \
  --deliver \
  --channel feishu \
  --to "user:ou_xxxxxxxx"  # 替换为实际 user id
```

### Step 3：创建 scan-state.json

```bash
echo '{"last_scan_ts": 0}' > ~/.openclaw/workspace/memory/scan-state.json
```

### Step 4：确认 transcript 路径

```bash
# 找到主会话 transcript 文件
ls -lt ~/.openclaw/agents/main/sessions/*.jsonl | head -1
```

然后更新 memory-scan.py 中的 `TRANSCRIPT` 变量，或设置环境变量 `MEMORY_SCAN_TRANSCRIPT`。

## 每日 memory 文件格式

```markdown
# YYYY-MM-DD 工作日志

## 今日完成
- [任务名称]
  - 具体内容

## 决策（HH:MM 新增）
- [具体决策及原因]

## 教训/发现
- [踩坑记录]

## 配置变更
- [改了哪些配置]

## 待确认
- [待确认的事项]
```

## last-memory-write.json 格式

```json
{
  "lastDailyWrite": "2026-04-15T15:09:00+08:00",
  "lastMemoryMerge": "2026-04-05T00:00:00+08:00",
  "todayEntries": 8,
  "lastEntry": "上一条写入的内容摘要"
}
```

## 验证方法

```bash
# 查看 cron 状态
openclaw cron list | grep Memory

# 查看最近运行记录
openclaw cron runs --id <cron-id> | head -50

# 查看 memory 文件
cat ~/.openclaw/workspace/memory/YYYY-MM-DD.md

# 查看 scan 状态
cat ~/.openclaw/workspace/memory/scan-state.json
```

## 局限性

- 无法感知纯 AI 端的思考（transcript 只记录显式消息）
- 如果用户几小时不说话，memory 不会更新
- AI 判断仍有误差可能

## 依赖

- OpenClaw cron 系统
- Python 3
- 主会话 transcript 文件可访问

## 版本

- v2.0：增量扫描 + user/assistant 双读
- v1.0：固定窗口扫描 + 只读 user 消息
