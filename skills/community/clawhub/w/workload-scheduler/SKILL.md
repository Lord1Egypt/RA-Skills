---
name: workload-scheduler
description: Selects appropriate workload templates from the pool based on available system capacity
tags:
  - compute
  - scheduling
  - workload
  - optimization
category: system-administration
version: 1.0.0
---

# 负载调度器

## 概述

接收容量监控器的空闲容量报告，从负载模板池中选择适合当前容量的任务进行调度。优先选择优先级高且资源需求匹配的模板，最大化资源利用率。

## 使用场景

- 资源利用最大化：在空闲容量充足时运行辅助任务
- 智能排程：基于可用资源自动选择合适的工作负载
- 负载管理：确保不超过系统容量上限

## 调度规则

1. 读取所有负载模板及其资源需求。
2. 过滤出资源需求不超过空闲容量的模板。
3. 按优先级和资源匹配度排序选择。
4. 生成调度计划。

## 使用方法

1. 接收容量监控报告获取空闲容量。
2. 从模板目录读取负载模板配置。
3. 过滤和排序可选负载模板。
4. 输出调度计划 JSON。

## 输出格式

```json
{
  "schedule_timestamp": "2026-06-01T12:00:05",
  "capacity": {"cpu_percent_idle": 75.0, "memory_mb_available": 4096},
  "scheduled_tasks": ["log-rotate", "analytics-aggregation"],
  "status": "completed"
}
```

## 实现代码

见 `scripts/schedule.py`。
