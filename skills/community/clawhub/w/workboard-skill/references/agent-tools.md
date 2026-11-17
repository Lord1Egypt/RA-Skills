# Workboard 智能体工具协议

本文是 `workboard` skill 的参考资料，记录子智能体 worker 用的 `workboard_*` 工具、认领令牌语义、worker 上下文、链接 / 分解 / 通知游标规则。SKILL.md 默认只引用本文。Claude Code 作为操作员助手通常**不**直接调用这些工具——它们是给 Gateway 子智能体 worker 运行时调用的；本文用于回答「worker 拿到哪些工具」「认领令牌怎么流转」之类的问题。

## 工具表

| 工具 | 用途 |
|---|---|
| `workboard_list` | 列出带声明 / 诊断状态的紧凑卡片；可选看板过滤器 |
| `workboard_read` | 返回一张卡片及有界 worker 上下文（备注、尝试、评论、链接、证明、工件、父级结果、最近的负责人工作、活动诊断） |
| `workboard_create` | 创建一张卡片，可附带可选父级、租户、Skills、看板、工作区元数据、幂等键、运行时限制、重试预算 |
| `workboard_link` | 将父卡片链接到子卡片；子卡片保持 `todo`，直到每个父卡片都达到 `done`，然后调度提升会将它们移动到 `ready` |
| `workboard_claim` | 为调用智能体声明一张卡片；将 `backlog` / `todo` / `ready` 移动到 `running` |
| `workboard_heartbeat` | 在较长运行期间刷新声明心跳 |
| `workboard_release` | 在完成、暂停或移交后释放声明；可以把卡片移动到下一个状态 |
| `workboard_complete` | 终态摘要工具——记录最终摘要、证明、工件和已创建卡片清单（必须引用链接回已完成卡片的卡片），把卡片推进到 `done` |
| `workboard_block` | 结构化生命周期工具——记录阻塞原因，把卡片移到 `blocked` |
| `workboard_attachment_add` | 将小型卡片附件存储在插件 SQLite 状态中，在卡片上建立索引 |
| `workboard_attachment_read` | 读取卡片附件 |
| `workboard_attachment_delete` | 删除卡片附件 |
| `workboard_worker_log` | 记录 worker 日志行 |
| `workboard_protocol_violation` | 在自动化 worker 未调用 `workboard_complete` / `workboard_block` 就停止时阻塞卡片 |
| `workboard_board_create` | 管理持久化看板元数据（显示名称、描述、默认工作区） |
| `workboard_board_archive` | 归档看板 |
| `workboard_board_delete` | 删除看板 |
| `workboard_runs` | 返回一张卡片的持久化运行尝试历史 |
| `workboard_specify` | 将粗略的分诊 / 待办卡片转为澄清后的 `todo` 卡片；在卡片上记录规格摘要 |
| `workboard_decompose` | 将父级编排卡片展开为已关联的子卡片，并继承看板 / 租户元数据；可以用已创建卡片清单完成父卡片 |
| `workboard_notify_subscribe` | 订阅通知 |
| `workboard_notify_list` | 列出通知订阅 |
| `workboard_notify_events` | 读取通知事件——可安全重放 |
| `workboard_notify_advance` | 移动持久游标，使调用方恢复时不会丢失或重复读取已完成 / 失败 / 陈旧卡片事件 |
| `workboard_notify_unsubscribe` | 取消订阅 |
| `workboard_boards` | 检查看板命名空间 |
| `workboard_stats` | 查看队列统计信息 |
| `workboard_promote` | 恢复或移交卡住的工作（不需要令牌） |
| `workboard_reassign` | 把卡片重新分配给另一智能体（不需要令牌） |
| `workboard_reclaim` | 重新认领卡住的卡片（不需要令牌） |
| `workboard_comment` | 添加移交备注 |
| `workboard_proof` | 附加证明 / 工件引用 |
| `workboard_unblock` | 将被阻塞的工作移回 `todo` |
| `workboard_dispatch` | 触发依赖提升或陈旧声明清理 |

## 认领令牌语义

- **认领令牌一次性返回**：`workboard_claim` 成功时，令牌作为顶层字段返回**一次**。
- **其余位置全部脱敏**：智能体工具或 Gateway RPC 调用返回的每张卡片都会把 `metadata.claim.token` 脱敏为 `[redacted]`。所以仪表盘操作员和其他智能体能检查认领状态，但永远不会看到可用令牌。
- **认领后拒绝其他智能体变更**：已认领的卡片会拒绝来自其他智能体的智能体工具变更，除非调用方持有 `workboard_claim` 返回的认领令牌。
- **恢复不需要令牌**：`workboard_promote` / `workboard_reassign` / `workboard_reclaim` 用于恢复或移交卡住的工作，这些操作不需要认领令牌。

这意味着 worker 拿到令牌后必须在自身运行内保管并用它做 `workboard_heartbeat` / `workboard_release` / `workboard_complete` / `workboard_block`；令牌不会在卡片记录里持久可见，丢了就只能走 promote / reassign / reclaim 恢复。

## worker 上下文

`workboard_read` 返回的有界 worker 上下文包括：备注、尝试、评论、链接、证明、工件、父级结果、最近的负责人工作、活动诊断。Worker 在分派时获得这份上下文 + 卡片认领令牌，并据此对卡片执行 heartbeat / complete / block。

## 链接与分解

- **`workboard_link`**：父卡链接到子卡。子卡保持 `todo`，直到**每个**父卡都达到 `done`，然后调度提升把它们移到 `ready`——这是依赖闸门，不是手动连线。
- **`workboard_decompose`**：把父级编排卡展开为已关联子卡，继承看板 / 租户元数据；可以用已创建卡片清单完成父卡。看板配置的 `autoDecompose` / `autoDecomposePerDispatch` 只记录意图并在 worker 上下文公开，实际分解仍走 `workboard_decompose` 工具。

## 通知游标

- **`workboard_notify_events` 可安全重放**：读取事件不会移动游标，调用方可以重放历史而不丢数据。
- **`workboard_notify_advance` 移动持久游标**：调用方恢复时不会丢失或重复读取已完成 / 失败 / 陈旧卡片事件。模式是「先 events 读、处理完再 advance 推进游标」。

## 权限映射（RPC `workboard.*`）

| 权限范围 | 方法 |
|---|---|
| `operator.read` | `cards.list`、`cards.export`、`cards.diagnostics`、attachment list / get、notification event reads、`boards.list`、`cards.stats`、`cards.runs` |
| `operator.write` | `cards.diagnostics.refresh`、create / update / move / delete / comment / link / linkDependency / proof / artifact、attachment add / delete、worker log、protocol violation、claim / heartbeat / release / promote / reassign / reclaim / complete / block / unblock、`cards.dispatch`、`cards.bulk`、archive、`boards.upsert` / archive / delete、`cards.specify` / decompose、notification subscribe / delete / advance |

没有 RPC 方法需要 `operator.admin`。以只读操作员访问权限连接的浏览器可以检查看板，但不能变更卡片。
