---
name: soyoung-clinic-tools
description: "在 agent 启动时注入新氧青春诊所工具的触发规则，确保门店查询/预约/项目查询自动走正确的技能，不被 Tavily 等通用搜索工具截胡"
metadata: {"openclaw":{"emoji":"🏥","events":["agent:bootstrap"]}}
---

# Soyoung Clinic Tools — Bootstrap Hook

在每次 session 启动时，将触发规则注入为 virtual bootstrap file，让 Agent 在收到任何会话消息前就知道如何处理新氧相关请求，并遵守 API Key 私聊限制与群聊审批规则。

## What It Does

- 触发时机：`agent:bootstrap`（workspace 文件注入之前）
- 注入内容：触发关键词 + API Key 私聊限制 + MessageContext 透传要求 + 审批流规则 + skill 路径
- 跳过：sub-agent session（避免 bootstrap 干扰）

## Enable

```bash
openclaw hooks enable soyoung-clinic-tools
```
