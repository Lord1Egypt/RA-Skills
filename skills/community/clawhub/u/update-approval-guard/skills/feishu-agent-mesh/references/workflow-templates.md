# Workflow Templates

## 1. 指派协作（Commanded Collaboration）
1. **起始**（用户 @ 若干机器人）
   - Relay 记录 `task_id`（chat_id + timestamp）。
   - 解析文本中的角色指派，例如“@小呱 拆解，@小咕 实现”。
2. **拆解阶段（机器人 A）**
   - A 获取上下文，更新 `contexts.summary`。
   - 在群里回复：拆解结果 + 行动项列表。
   - 写日志：`action=breakdown_completed`。
3. **执行阶段（机器人 B/C）**
   - Relay 将行动项指派给相应机器人；必要时写入 `task_queue`。
   - B/C 执行后在群里同步结果，并写入日志。
4. **审批节点**
   - 当 `state=ready_for_approval`，Relay 自动在群里 @ 人类，附带：任务概述、执行人、关键输出链接。
   - 等待 `approved / rejected` 指令后继续。
5. **收尾**
   - 汇总结论、更新 `contexts.summary_final`。
   - 写日志 `action=task_closed` 并归档记录。

## 2. 无领导讨论（Leaderless Discussion）
1. **议题发布**：用户抛出问题，Relay 生成“讨论会话”记录。
2. **轮流发言**：
   - Relay 给所有机器人发送“Round Robin” cue。
   - 每个机器人按顺序：陈述观点 → 写回 `discussion_log`。
   - 可以设定最多 N 轮或指定停止条件。
3. **观点收敛**：
   - 任何机器人可调用 `sessions_send` 请求其他机器人执行子任务；结果仍需回写上下文。
   - 当检测到 `consensus` 或时间到，进入总结阶段。
4. **总结 & 行动项**：
   - 指定“记录员”机器人整理行动项，在群里发布。
   - 若需要审批则走审批流程，否则标记 `state=discussion_closed`。

## 3. 异常/重试模板
- **机器人无响应**：Relay 记录 `status=timeout`，改派任务或通知人类。
- **审批逾期**：自动提醒一次，如仍无人响应，降级为“人工处理”。
- **冲突解法**：若两个机器人同时处理同一任务，使用 `task_locks`（chat_id + task_id）保证串行。

> 将以上模板与 `relay-config.json` 的 rules 结合：可以快速为新机器人添加职责，也方便复制到新的群聊。
