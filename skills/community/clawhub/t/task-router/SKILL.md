---
name: task-router
description: 智能任务路由 - 自动分析任务类型并路由到最合适的Agent
---

# Task Router - 智能任务路由

## 功能
当用户发送任务时，自动分析任务类型并路由到合适的Agent或Skill。

## 路由规则

### Agent路由
| 任务关键词 | 路由目标 | 说明 |
|------------|---------|------|
| 股票、交易、跟单、持仓、IBKR | jiaoyi | 量化交易 |
| 规划、城市设计、项目、土地 | planning | 城市规划 |
| 报告、文章、内容、创作、小红书 | bigan | 内容创作 |
| 代码、脚本、开发、调试、Python | jinhua | 技术开发 |
| 研究、分析、调研、竞品、市场 | canmou | 情报研究 |
| 架构、系统设计、技术决策、审查 | architect | 架构审查 |

### Skill路由
| 任务关键词 | 路由目标 |
|------------|---------|
| 飞书、日历、通知 | feishu-calendar |
| 文件、文档、PDF | minimax-pdf |
| Excel、数据表格 | minimax-xlsx |
| PPT、演示 | pptx-generator |

## 执行逻辑

1. 解析用户任务文本
2. 提取关键词（TF-IDF）
3. 匹配路由规则
4. 路由到对应Agent/Skill

## 使用方式

自动触发，无需手动调用。
当用户发送任务时自动分析并路由。
