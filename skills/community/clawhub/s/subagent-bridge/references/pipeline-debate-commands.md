# Pipeline + Debate 实战命令参考

> 验证环境：同一 `agentId`（main）下，`sessionTool.visibility: tree`（默认）
> 测试结果：✅ 全部通过

## 前置条件

- 子会话必须处于激活状态（刚 spawn 还没结束）

---

## 步骤 1：Spawn 两个 subagent

```text
# 子会话 A：搜索专家
sessions_spawn(
  task="你是搜索专家 SearchBot。任务是：1) 等待被 sessions_send 叫到才开始工作
         2) 收到消息后用 web_search 查询
         3) 返回查询结果总结",
  taskName="search_bot",
  mode="run",
  cleanup="keep"
)
```

任务执行中

```
sessions_yield(message="等待 SearchBot 初始化")
```

进度通知

```text
# 子会话 B：分析专家
sessions_spawn(
  task="你是分析专家 AnalysisBot。任务是：1) 等待被 sessions_send 叫到才开始工作
         2) 收到消息后进行分析、总结、提炼观点",
  taskName="analysis_bot",
  mode="run",
  cleanup="keep"
)
```

子任务执行中

```
sessions_yield(message="等待 AnalysisBot 初始化")
```

两个 spawn 都会返回 childSessionKey，格式：

```
agent:main:subagent:<uuid-v4>
```

---

## 步骤 2：Pipeline — A 搜完传给 B

### 2a. 发消息给 SearchBot

```text
sessions_send(
  sessionKey="agent:main:subagent:<SearchBot-uuid>",
  message="搜索一下 2025-2026 年大模型领域的关键技术趋势...",
  timeoutSeconds=90
)
```

- `timeoutSeconds` ≥30 会等待 subagent 回复
- 返回 `reply` 字段包含 subagent 的回答

### 2b. 把结果传给 AnalysisBot

```text
sessions_send(
  sessionKey="agent:main:subagent:<AnalysisBot-uuid>",
  message="以下是 SearchBot 搜索到的结果：\n\n{SearchBot 的回答全文}\n\n请分析：\n1. 这些趋势的底层逻辑是什么？\n2. 对中小团队意味着什么？",
  timeoutSeconds=60
)
```

---

## 步骤 3：Debate — 双向讨论

### 3a. A 质疑 B 的观点

```text
sessions_send(
  sessionKey="agent:main:subagent:<SearchBot-uuid>",
  message="AnalysisBot 刚才认为「中小团队不要碰预训练...」。请查证这个观点是否过时？",
  timeoutSeconds=60
)
```

### 3b. B 回应 A 的质疑

```text
sessions_send(
  sessionKey="agent:main:subagent:<AnalysisBot-uuid>",
  message="SearchBot 查证后提出补充：\n1. 增量预训练 8 卡 A100 可行\n2. Uni-MoE 降低了 MoE 微调门槛\n...\n请逐条回应并说明坚持之处。",
  timeoutSeconds=60
)
```

---

## 周期事项

| 阶段 | 耗时 | 说明 |
|------|------|------|
| Spawn 等待初始化 | ~10-20s | spawn 后 sessions_yield 等待 completion 事件 |
| Pipeline 第一步（搜索） | ~30-45s | web_search 耗时 |
| Pipeline 第二步（分析） | ~20-30s | 模型生成分析 |
| Debate 每轮 | ~20-30s | 模型生成回复 |
| 一次完整 Pipeline+Debate | ~3-5min | 含初始化、搜索、分析、两轮辩论 |

## 注意事项

1. **用完记得关闭**：subagent 执行完生命周期就结束了，bridge 只能在存活期间使用
2. **不要依赖 completion 事件**：`sessions_send` 返回的 `reply` 字段是实时数据，completion 事件是延迟的冗余通知，内容相同
3. **timeoutSeconds 取值**：搜索类设 60-90s，分析/讨论类设 30-60s
4. **visibility 限制**：只能在同一个 agentId 下。跨 agent 需要配置 `tools.agentToAgent.enabled: true`
