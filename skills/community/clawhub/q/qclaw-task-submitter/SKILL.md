---
name: QClaw任务提交
description: |
  通过 QClaw 向 WorkBuddy 提交需要复杂执行的任务。当用户想要：
  - 通过微信/对话将任务交给 WorkBuddy 执行
  - "帮我生成/制作/分析/整理..."
  - 需要创建文档、PPT、Excel、报告
  - 深度数据分析、多步骤操作
  - 批量文件处理
  - 定时自动化任务
  - 明确说"交给 WorkBuddy"、"远程执行"
  - QClaw 做不到的事，WorkBuddy 来做
  触发词：交给WorkBuddy、QClaw发任务、微信转WorkBuddy、远程执行、任务分发、WorkBuddy生成、WorkBuddy分析
version: 1.0.0
---

# QClaw → WorkBuddy 任务提交

将复杂任务提交到 WorkBuddy 执行队列，WorkBuddy 会自动处理并返回结果。

## 使用方法

当用户请求需要 WorkBuddy 执行的任务时，直接调用队列脚本添加任务：

```bash
python3 ~/.workbuddy/skills/qclaw-workbuddy-bridge/scripts/qclaw_queue.py add "任务描述" [--intent "用户原始意图"] [--ctx '{"key": "value"}']
```

**注意**：`add` 命令会自动发送触发信号（`.trigger` 文件），WorkBuddy 收到信号后会**立即**处理，无需等待轮询间隔。

## 示例场景

### 场景 1：生成文档/报告
```
用户: 帮我生成一份本周的工作周报
→ python3 .../qclaw_queue.py add "生成本周工作周报，包含ITS系统进展和下周计划" --ctx '{"user": "刘博", "source": "wechat"}'
→ 返回任务ID给用户
```

### 场景 2：数据分析
```
用户: 帮我分析这份销售数据
→ 询问文件路径
→ python3 .../qclaw_queue.py add "分析销售数据，生成可视化图表和关键洞察" --ctx '{"file": "/path/to/sales.xlsx"}'
```

### 场景 3：批量处理
```
用户: 帮我整理一下Downloads文件夹
→ python3 .../qclaw_queue.py add "整理Downloads文件夹，按类型分类文件" --ctx '{"user": "刘博", "source": "wechat"}'
```

## 提交任务后的回复模板

```
✅ 任务已提交给 WorkBuddy 执行
🆔 任务编号: <task_id>
⏱ 预计处理时间: 1-5 分钟（触发式响应，极速）
📋 任务内容: <任务描述>

WorkBuddy 执行完成后会通过以下渠道通知您结果。
```

## 查看任务状态

```bash
# 查看所有任务
python3 ~/.workbuddy/skills/qclaw-workbuddy-bridge/scripts/qclaw_queue.py list

# 只看待处理
python3 ~/.workbuddy/skills/qclaw-workbuddy-bridge/scripts/qclaw_queue.py list --status pending

# 获取已完成任务的结果
python3 ~/.workbuddy/skills/qclaw-workbuddy-bridge/scripts/qclaw_queue.py result <task_id>
```

## 自动分流规则

**直接执行**（QClaw 可以完成）：
- 简单问答、计算、翻译
- 信息查询（天气、时间）
- 文本总结（1000字以内）

**提交队列**（需要 WorkBuddy 执行）：
- 生成长文档（报告、方案、合同）
- Excel/PPT/Word 文档生成
- 深度数据分析（多文件、多数据源）
- 批量文件操作
- 涉及本地文件系统访问
- 需要多步骤/复杂工具链的操作
- 定时自动化任务

## 任务提交决策树

```
用户请求 → 判断复杂度
    │
    ├── 简单（5分钟内可完成） → 直接回答
    │
    ├── 文档生成/长报告 → 提交队列
    │
    ├── 文件处理（批量/多文件） → 提交队列
    │
    ├── 数据分析（需工具） → 提交队列
    │
    └── 用户明确要求WorkBuddy → 提交队列
```
