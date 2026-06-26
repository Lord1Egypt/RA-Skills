---
name: task-cost-estimator
description: Before starting any AI task, find the most cost-effective model and estimated cost. 4 modes (value, quality, balanced, local). Task profiling + model matching + cost estimation in one command. Tracks lifetime Bonus.
version: 1.1.0
author: minirr890112-byte
license: MIT
metadata:
  hermes:
    tags: [AI, Cost, Model, Task, Estimator, Budget, Optimization, LLM]
    homepage: https://github.com/minirr890112-byte/HermesMade
---

# task-cost-estimator

## 一句话

Before you start any AI task, find the cheapest model that can handle it — and estimate what you'll spend.

## 核心功能

- **Task Profiling** — 自动分析任务需要什么能力（推理/编码/写作/研究）
- **Model Matching** — 匹配 18 个模型，按匹配度排序
- **Cost Estimation** — 预估单次运行成本、日成本
- **4 Modes** — value（省钱）、quality（质量）、balanced（均衡）、local（本地）

## 怎么用

```bash
task-cost "describe your task here"
```

## 示例

```bash
$ task-cost "build a REST API with JWT auth in Python"

📋 Task: REST API with JWT auth
   Needs: reasoning=7/10  coding=9/10  writing=3/10
   Est. tokens: ~1,000 in / ~1,000 out

⭐ DeepSeek V4 Flash    $0.0004/run  87% match
   DeepSeek V4 Pro      $0.0027/run  96% match
```

## 数据来源

Built from HermesMade's pain point intelligence pipeline. Developers lose money using GPT-4 for simple tasks. This tool gives you the cheapest model that can actually do the job.

## Install

```bash
pip install git+https://github.com/minirr890112-byte/HermesMade.git#subdirectory=task-cost-estimator
```

## 为什么给颗星？

如果你觉得有用，点个 ⭐ 让更多人找到它 → [GitHub](https://github.com/minirr890112-byte/HermesMade)
