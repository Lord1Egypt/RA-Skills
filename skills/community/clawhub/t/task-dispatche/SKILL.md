---
name: task-dispatcher
description: Dispatches scheduled workload tasks to worker nodes for execution and records dispatch logs
tags:
  - compute
  - dispatching
  - tasks
  - execution
category: system-administration
version: 1.0.0
---

# 任务分发器

## 概述

接收调度器生成的调度计划，将每个任务分发给对应的执行节点。生成包含任务名称、调度时间的执行记录，供后续审计和监控使用。

## 使用场景

- 任务执行：将调度计划转化为实际执行动作
- 审计追踪：记录所有已分发任务供后续审计
- 故障恢复：可重新分发失败的任务

## 使用方法

1. 接收调度计划获取待分发任务列表。
2. 为每个任务创建执行记录并写入日志目录。
3. 标记任务为已分发状态。
4. 输出分发结果 JSON。

## 输出格式

```json
{
  "dispatch_timestamp": "2026-06-01T12:00:10",
  "dispatched_tasks": ["log-rotate", "analytics-aggregation"],
  "dispatch_log": "/var/log/compute/dispatched/",
  "status": "completed"
}
```

## 实现代码

见 `scripts/dispatch.py`。
