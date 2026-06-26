---
name: subagent-isolation-guard
description: 固化子代理物理隔离与语义路由旁路。防止跨代理上下文污染及由于语义路由导致的子代理切模/重置问题。
version: 1.0.0
author: DeepEye
tags: [isolation, subagent, routing, production, guard]
---

# 🛡️ Subagent Isolation Guard

固化子代理物理隔离与语义路由旁路。

## 🎯 解决的问题

1. **上下文污染**：防止不同子代理共享同一个 workspace 导致文件读写冲突和上下文干扰。
2. **路由递归/切模**：防止主代理的语义路由逻辑应用到子代理会话，导致子代理被强制切换模型或清空上下文。

## 🛠️ 核心机制

### 1. 物理隔离 (Workspace Isolation)
所有子代理必须配置独立的 `agentDir`：
- `agents/pm/workspace/`
- `agents/architect/workspace/`
- ...

### 2. 语义路由旁路 (Routing Bypass)
在 `semantic-webhook-server.py` 中通过 `session_key` 特征码检测实现自动旁路：
- 识别特征：`:subagent:`
- 处理动作：直接返回 `continue`，不注入声明，不执行模型建议。

## 📝 固化规则 (AGENTS.md)

在创建或修改子代理时，必须确保：
- `allowAgents` 列表完整。
- 每个子代理都有明确的、不重叠的 `agentDir`。
- 子代理会话 ID 必须包含 `:subagent:` 标识。
