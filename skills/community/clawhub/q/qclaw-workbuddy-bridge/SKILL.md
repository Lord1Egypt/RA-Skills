---
name: qclaw-workbuddy-bridge
description: |
  QClaw 与 WorkBuddy 任务分发集成桥。当用户想要：
  - 通过微信让 QClaw 发送任务给 WorkBuddy 执行
  - QClaw 写任务 → WorkBuddy 执行 → 微信推送结果
  - 打通 QClaw（微信入口）和 WorkBuddy（执行引擎）
  - 远程任务分发、跨客户端任务执行
  触发词：QClaw发任务、微信转WorkBuddy、QClaw工作流、远程任务、任务分发
version: 1.0.0
---

# QClaw ↔ WorkBuddy 任务分发桥

通过共享 JSON 队列文件，实现 QClaw（微信入口）和 WorkBuddy（执行引擎）的双向打通。

## 架构概览

```
微信消息
    ↓
QClaw（解析意图） → 写入任务到队列文件
    ↓
WorkBuddy（自动化轮询） → 读取任务 → 执行 → 写回结果
    ↓
QClaw（读取结果） → 微信推送回复给用户
```

- **队列文件**: `~/.workbuddy/queue/qclaw_tasks.json`
- **队列管理器**: `~/.workbuddy/skills/qclaw-workbuddy-bridge/scripts/qclaw_queue.py`
- **轮询方式**: WorkBuddy 自动化（recurring）定期检查队列

---

## 第一步：安装与初始化

### 1.1 验证依赖

```bash
# 确认 Python 3 已安装
python3 --version

# 确认队列目录存在
ls ~/.workbuddy/queue/
# 首次运行会自动创建
```

### 1.2 初始化队列文件

```bash
python3 ~/.workbuddy/skills/qclaw-workbuddy-bridge/scripts/qclaw_queue.py list
```

---

## 第二步：在 QClaw 侧配置

QClaw 通过对话解析用户意图，将需要 WorkBuddy 执行的任务写入队列。

### QClaw 提示词配置（发送给 QClaw）

在 QClaw 的自定义提示词或系统提示中加入以下规则：

```
---
你有一个新的能力：当用户请求的任务需要：
- 生成长文档、报告、PPT、Excel
- 深度数据分析或研究
- 需要访问本地文件的复杂操作
- 定时自动化任务
- 批量文件处理

你应主动将任务写入队列文件，格式如下：

任务分发触发条件（满足任一即写入）：
1. 用户说"帮我生成/制作/分析/整理..."
2. 涉及文件创建、数据处理、多步骤操作
3. 用户说"远程执行"、"交给 WorkBuddy"、"你做不到的事"

写入命令：
```bash
python3 ~/.workbuddy/queue/qclaw_tasks.py add "任务描述"
```

如果任务复杂，先简要总结（100字内），再写入队列。

队列文件路径：~/.workbuddy/queue/qclaw_tasks.json
队列管理脚本：~/.workbuddy/skills/qclaw-workbuddy-bridge/scripts/qclaw_queue.py
```

### 快速手动测试（QClaw 侧）

```bash
# 添加一个测试任务
python3 ~/.workbuddy/skills/qclaw-workbuddy-bridge/scripts/qclaw_queue.py add "帮我查一下今天的天气并生成出行建议"

# 查看队列
python3 ~/.workbuddy/skills/qclaw-workbuddy-bridge/scripts/qclaw_queue.py list

# 只看待处理任务
python3 ~/.workbuddy/skills/qclaw-workbuddy-bridge/scripts/qclaw_queue.py list --status pending
```

---

## 第三步：在 WorkBuddy 侧配置自动化

### 3.1 创建轮询自动化

在 WorkBuddy 中创建定时自动化：

- **名称**: `qclaw-bridge-poll`
- **触发频率**: 每 5 分钟一次（FREQ=MINUTELY;INTERVAL=5）
- **执行内容**: 见下方自动化脚本

### 3.2 自动化执行脚本

创建自动化时，在 prompt 中填入：

```
检查任务队列 ~/.workbuddy/queue/qclaw_tasks.json 中是否有 status="pending" 的任务。

如果有，按以下步骤处理：

1. 先运行：
   python3 ~/.workbuddy/skills/qclaw-workbuddy-bridge/scripts/qclaw_queue.py poll --once

2. 读取返回的 JSON 任务内容，提取 input.description 作为任务描述

3. 自主执行任务（调用所有需要的工具、Skill 完成工作）

4. 任务完成后，将结果写入队列：
   python3 ~/.workbuddy/skills/qclaw-workbuddy-bridge/scripts/qclaw_queue.py done <task_id> - << 'EOF'
   {"summary": "一句话结果描述", "details": "详细说明", "files": ["文件路径列表"]}
   EOF

5. 如果执行失败：
   python3 ~/.workbuddy/skills/qclaw-workbuddy-bridge/scripts/qclaw_queue.py error <task_id> "失败原因"

如果队列为空，不做任何操作，直接退出。
```

---

## 第四步：QClaw 读取结果并推送

### 自动化推送脚本（WorkBuddy 端）

任务完成后，WorkBuddy 可以主动将结果写入一个结果文件：

```bash
# 在 WorkBuddy 自动化中，完成任务后调用：
python3 ~/.workbuddy/skills/qclaw-workbuddy-bridge/scripts/qclaw_queue.py result <task_id>
```

### QClaw 读取结果（轮询模式）

QClaw 可以设置一个定期检查结果的逻辑：

```
定期检查结果：
每 5 分钟检查一次 ~/.workbuddy/queue/qclaw_tasks.json
找出所有 status="done" 且尚未推送的任务
将 result.summary 通过微信消息发送给用户
然后将任务 status 改为 "pushed"
```

---

## 队列任务数据结构

```json
{
  "version": "1.0",
  "tasks": [
    {
      "id": "a1b2c3d4",
      "created_at": "2026-04-15T08:30:00+08:00",
      "status": "pending",
      "input": {
        "description": "帮我生成一份本周的工作周报",
        "intent": "用户原始意图描述",
        "context": {
          "user": "刘博",
          "project": "ITS系统"
        }
      },
      "result": {
        "summary": "周报已生成，共5个工作项",
        "details": "...",
        "files": ["/path/to/weekly_report.md"]
      },
      "done_at": null,
      "error": null
    }
  ]
}
```

## 队列操作命令速查

| 操作 | 命令 |
|------|------|
| 添加任务 | `python3 .../qclaw_queue.py add "任务描述" [--intent "意图"]` |
| 查看队列 | `python3 .../qclaw_queue.py list [--status pending]` |
| 等待任务 | `python3 .../qclaw_queue.py poll --once` |
| 获取结果 | `python3 .../qclaw_queue.py result <task_id>` |
| 标记完成 | `python3 .../qclaw_queue.py done <task_id> <result.json>` |
| 标记失败 | `python3 .../qclaw_queue.py error <task_id> "原因"` |
| 更新状态 | `python3 .../qclaw_queue.py status <task_id> <new_status>` |

---

## 场景示例

### 场景 1：微信说"帮我生成周报"

**QClaw 侧**:
```
用户: 帮我生成本周的工作周报
→ QClaw 识别为复杂任务，写入队列
→ python3 .../qclaw_queue.py add "生成本周工作周报，包含ITS系统进展和下周计划"
```

**WorkBuddy 侧**（自动化触发）:
```
→ 读取任务，识别为"生成周报"
→ 询问/查找本周的工作内容
→ 调用 Word/DOCX Skill 生成周报文档
→ 完成后写入结果
```

**结果推送**:
```
✅ 周报已生成！
📄 文件: ~/weekly_report_2026-04-15.docx
📝 摘要: 包含ITS系统、配置管理、问题管理等5个工作项
```

### 场景 2：微信说"帮我分析这份Excel"

**QClaw 侧**:
```
用户: 帮我分析一下这份销售数据
→ QClaw 询问用户文件路径
→ 用户提供路径后，写入队列
→ python3 .../qclaw_queue.py add "分析销售数据，生成可视化图表和关键洞察" --ctx '{"file": "/path/to/sales.xlsx"}'
```

---

## 进阶：多用户支持

如果需要支持多用户场景，可以在队列中加入 `user_id` 字段：

```json
{
  "input": {
    "description": "...",
    "user_id": "liubo",
    "reply_to": "wechat"
  }
}
```

WorkBuddy 在处理时根据 `user_id` 区分用户，结果通过对应渠道推送。

---

## 故障排查

| 问题 | 原因 | 解决方法 |
|------|------|----------|
| 队列文件不存在 | 首次未初始化 | 运行 `qclaw_queue.py list` 自动创建 |
| 自动化没触发 | 频率太低/自动化暂停 | 改为每 1 分钟或手动触发一次 |
| 结果未推送 | QClaw 未轮询结果 | 检查 QClaw 侧结果读取逻辑 |
| 权限错误 | 队列文件无读写权限 | `chmod 600 ~/.workbuddy/queue/qclaw_tasks.json` |
