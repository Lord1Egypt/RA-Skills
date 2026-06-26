---
name: token-cost-optimizer
version: 1.0.0
description: >
  OpenClaw Token 成本优化与 API 用量控制专家。当用户提到 token 消耗过高、API 费用上涨、
  模型调用太贵、上下文太长、死循环、定时任务频率、多 Agent 重复请求、模型路由、
  或任何与降低 OpenClaw 运行成本相关的话题时，立即使用此 Skill。
  也适用于用户说"帮我省钱"、"优化配置"、"检查一下有没有浪费"等场景。
author: dai
tags:
  - token
  - cost
  - optimization
  - openclaw
  - api
---

# Token 成本优化器

帮助用户从八个维度系统性地降低 OpenClaw 的 Token 消耗和 API 费用。

## 使用流程

1. 诊断：先运行诊断命令，了解当前状态
2. 分析：根据诊断结果，识别主要浪费点
3. 优化：按优先级逐一处理，每步确认效果
4. 监控：配置持续监控，防止问题复发

## 快速诊断脚本

一键输出所有关键信息：
```bash
echo "=== Cron 任务 ===" && openclaw cron list
echo "=== Skills 状态 ===" && openclaw skills list | grep "✓ ready"
echo "=== Memory 大小 ===" && du -sh ~/.openclaw/memory/
echo "=== Workspace 大小 ===" && du -sh ~/.openclaw/workspace/
echo "=== 当前模型 ===" && cat ~/.openclaw/openclaw.json | grep primary
echo "=== Compaction 模式 ===" && cat ~/.openclaw/openclaw.json | grep compaction -A3
```

## 八个优化维度

### 1. 控制上下文长度
将 compaction.mode 改为 aggressive，限制最大 token 数：
在 openclaw.json 的 agents.defaults 下设置：
"compaction": { "mode": "aggressive", "maxTokens": 8000, "keepLastN": 10 }

### 2. 要求模型简要输出
在 ~/.openclaw/soul.md 中加入：
默认简洁回复，列表不超过5条，代码只展示关键部分，避免重复内容。

### 3. 多 Agent 并行分工
主 agent 只负责协调，子 agent 只接收精简任务描述，不传递完整上下文。
相同类型任务指定固定 agent，避免重复路由。

### 4. 监控 API 调用频率
运行：openclaw logs | tail -100 查看近期调用
发现死循环时：openclaw gateway stop && openclaw gateway start

### 5. 清理配置文件
清理30天前workspace文件：find ~/.openclaw/workspace -mtime +30 -type f -delete
删除长期未用的 Skill 目录和90天未更新的 memory 文件。

### 6. 切换低价模型
kimi-k2.5（成本为0）用于简单问答
claude-haiku 用于日常任务
claude-sonnet 用于复杂分析
claude-opus 仅在必要时使用

### 7. 配置自动模型路由
在 soul.md 中加入路由提示：
查询天气、翻译、格式转换 → kimi-k2.5
写文章、写代码、分析数据 → claude-haiku
多步骤复杂推理、交易策略分析 → claude-sonnet

### 8. 优化定时任务
运行：openclaw cron list 查看所有任务
行情监控：交易时间内5分钟一次，收盘后停止
新闻聚合：改为30分钟或1小时一次
健康检查：改为每天一次
心跳任务：能关则关

## 参考文件
- references/cost-checklist.md — 每周成本检查清单
- references/model-pricing.md — 主流模型价格对比表
