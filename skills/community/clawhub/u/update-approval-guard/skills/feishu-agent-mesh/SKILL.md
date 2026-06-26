---
name: feishu-agent-mesh
description: >-
  Blueprint for wiring multiple OpenClaw agents (running on different servers) into the same
  Feishu group chats so they can hold autonomous multi-turn discussions, hand off tasks,
  log every cross-agent message, and pause for human approval at key checkpoints.
  Use when you need Xiao呱、小咕等机器人在飞书里互相@、协作执行任务，而不新增新的
  前台机器人账号。
---

# Feishu Agent Mesh

把多个 OpenClaw 机器人（不同实例/服务器）接入同一个飞书群：用户依旧 @ 本来的机器人，后台通过共享 Relay/队列同步上下文、日志和审批。

## 0. At-a-glance
1. **选择模式** —— 先读 [references/architecture.md](references/architecture.md)，确定是 MVP（共享表/JSON）、推荐架构（双 Bot + Relay 服务）还是高级模式（含审批/异步）。
2. **部署 Relay** —— 根据模式完成 [references/deployment-checklist.md](references/deployment-checklist.md)：配置飞书订阅、共享存储、HTTP/CLI 调用方式。
3. **注册机器人能力** —— 复制 [scripts/relay-config.example.json](scripts/relay-config.example.json) 并填入每个机器人的能力、回调 URL、所在服务器。
4. **落地 Workflow** —— 参照 [references/workflow-templates.md](references/workflow-templates.md) 运行「指派协作」或「无领导讨论」两类模板。
5. **日志 & 审批** —— 按 [references/logging-schema.md](references/logging-schema.md) 设计日志字段、审批节点，确保所有跨机器人消息都有据可查。

## 1. 关键原则
- **前台不变**：群里仍是现有机器人（小呱、小咕…），任何扩展只发生在后台。
- **共享上下文**：所有机器人通过同一个 Relay/队列同步讨论内容与任务状态。
- **多群隔离**：以 `chat_id` 维度存储上下文、日志、审批规则，避免串线。
- **渐进式演进**：先跑 MVP，再升级到推荐架构，最后再加高级特性。

## 2. 快速启动（MVP ≤ 1h）
1. **共享存储**：建一个飞书多维表格或 SQLite/JSON 文件，字段至少包括 `chat_id`、`thread_id`、`message`, `actor`, `task_state`。
2. **机器人轮询**：在每个机器人实例里添加一个定时任务（60s 内），读取共享存储中“自己未处理”的记录。
3. **写回策略**：机器人在群里发言后，同时写入共享存储，供其他机器人读取。
4. **审批钩子**：人工定义关键字段（如 `phase="ready_for_approval"`），当检测到该字段时，机器人自动 @ 人类确认。
> 适合验证能否「在同一群里互相接力」，但对延迟要求高的场景不适合长期使用。

## 3. 推荐架构（双 Bot + Relay 服务）
1. **Feishu 事件**：为每个机器人配置事件订阅，把回调统一指向 Relay 服务；Relay 按 `bot_id + chat_id` 写入共享上下文。
2. **消息分发**：Relay 根据 [scripts/relay-config.example.json](scripts/relay-config.example.json) 中的 `routes` 决定是通知另一个机器人，还是写入队列等待异步处理。
3. **能力调用**：优先使用 HTTP `/tools/invoke`（或你们自定义 API）触发对方机器人；CLI 仅作兜底。
4. **日志**：Relay 所有操作都写入 `logs` 表，字段参考 [references/logging-schema.md](references/logging-schema.md)。
5. **审批**：在配置里声明 `approval_hooks`。当任务状态达到某个 hook，Relay 汇总信息，并由相应机器人账号 @ 人类确认。

## 4. 高级特性（可选）
- **无领导讨论**：按 [references/workflow-templates.md](references/workflow-templates.md#无领导讨论) 的流程，自动分配发言顺序、观点收敛、行动项指派。
- **异步任务队列**：为长耗时任务配置 Redis / 消息队列；队列项最少包含 `task_id`、`chat_id`、`origin_bot`、`assignee_bot`、`payload`。
- **意图识别**：Phase 1 使用关键词/显式 @；Phase 2 加入 LLM 分类或正则 DSL，并允许人工 fallback。
- **多群策略**：在 Relay 配置中加入 `chat_whitelist/blacklist`、每群的审批和限流规则。

## 5. 运维 & 故障
1. **消息未到达**：检查飞书订阅是否指向 Relay、签名是否一致；核对 `chat_id` 是否在白名单。
2. **机器人重复响应**：查看共享上下文中 `last_actor` 是否正确，避免双写；必要时启用分布式锁或乐观锁。
3. **日志膨胀**：以时间或条数阈值定期归档到对象存储；短期日志保留在主库即可。
4. **审批超时**：在 Relay 中为审批 hook 设置超时策略（例如 10 分钟未确认则自动降级为提醒）。

## 6. 交付物
- **技能文件**：本 SKILL.md + references + scripts，定义流程、配置、日志、审批、常见问题。
- **配置模板**：`scripts/relay-config.example.json`，作为机器人注册与路由的起点。
- **部署模板**：`references/deployment-checklist.md`，含 MVP → 推荐架构 → 高级特性 3 级清单。
- **动作模板**：`references/workflow-templates.md`，覆盖指派协作 / 无领导讨论。

Follow the references to implement the actual Relay/队列；有了这套 skill，任何新的 OpenClaw 机器人都能按统一流程被纳入 Feishu 群聊协作网络。