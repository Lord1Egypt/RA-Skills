---
name: taichi
description: 太极架构多 Agent 协作框架，支持集中式、分布式，元混合三种执行模式。基于 Redis 消息总线，实现 Planner/Drafter/Validator/Dispatcher 四个阶段的工作流。
version: "2.1.0"
author: taichi-architecture
type: skill
tags: [multi-agent, orchestration, distributed, workflow, coordination]
homepage: https://github.com/Indivisible2025/Cloudfin
license: MIT
---

# 太极架构 (Taichi Framework)

多 Agent 协作框架，支持三种执行模式。

## 使用方式

当用户需要使用太极框架执行任务时，通过 `exec` 工具调用：

```bash
cd $HOME/.openclaw/workspace/taichi-framework && \
source venv/bin/activate && \
python orchestrator.py --mode <模式> --request "<任务描述>"
```

## 三种模式

| 模式 | 命令 | 适用场景 |
|------|------|---------|
| 集中式 | `--mode centralized` | 线性依赖任务（默认） |
| 分布式 | `--mode distributed --workers N` | 数据并行任务 |
| 元混合 | `--mode hybrid --workers P,D,V,DP` | 多阶段复杂任务 |

## 示例

**集中式**：
```bash
cd $HOME/.openclaw/workspace/taichi-framework && \
source venv/bin/activate && \
python orchestrator.py --mode centralized --request "分析日志文件 app.log"
```

**分布式（5个Worker并行）**：
```bash
cd $HOME/.openclaw/workspace/taichi-framework && \
source venv/bin/activate && \
python orchestrator.py --mode distributed --workers 5 --request "处理数据: 1,2,3,4,5"
```

**元混合**：
```bash
cd $HOME/.openclaw/workspace/taichi-framework && \
source venv/bin/activate && \
python orchestrator.py --mode hybrid --workers 3,5,3,2 --request "复杂任务"
```

## 前置要求

- Redis 运行中（`redis-server`）
- Python 虚拟环境已安装（`./install.sh`）
