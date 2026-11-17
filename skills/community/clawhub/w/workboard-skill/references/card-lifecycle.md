# Workboard 卡片生命周期

本文是 `workboard` skill 的参考资料，记录卡片状态机、会话生命周期同步、诊断、生命周期事件清单和从卡片启动工作的引擎选择。SKILL.md 默认只引用本文，需要解释「卡片为什么停在某状态」时再读。

## 状态取值

`triage`、`backlog`、`todo`、`scheduled`、`ready`、`running`、`review`、`blocked`、`done`。

## 状态转移

转移由智能体工具或会话生命周期同步触发（工具详见 [agent-tools.md](./agent-tools.md)）：

| 起点 | 到达 | 触发 |
|---|---|---|
| `triage` / `backlog` | `todo` | `workboard_specify`（把粗略卡转成澄清后的 todo 卡，记录规格摘要） |
| `backlog` / `todo` / `ready` | `running` | `workboard_claim`（为调用智能体认领）；或从卡片启动 Codex / Claude 运行（标记 running） |
| `ready` | `running` | dispatch 选中并认领该卡 |
| `todo`（作为依赖子卡） | `ready` | 父卡全部 `done` 后依赖提升 / dispatch 提升；`workboard_link` 建立的子卡会保持 `todo` 直到每个父卡 `done`，再由调度提升到 `ready` |
| `running` | `review` | 关联会话 `completed` / 任务完成 |
| `running` | `blocked` | 关联会话 `failed` / `killed` / `timed out` / `aborted`；`workboard_block`；worker 启动失败；或自动化 worker 未调 `workboard_complete` / `workboard_block` 就停止（`workboard_protocol_violation`） |
| `blocked` | `todo` | `workboard_unblock` |
| `review` | `done` | 手动接受后移到 `done`；`workboard_complete`（带摘要 / 证明 / 工件 / 已建卡清单） |
| `review` / `blocked` / `done` | （停止自动同步） | 手动移到这几个状态会停止会话自动同步，移回 `todo` / `running` 才恢复 |

手动 `review` 状态优先于会话同步——操作员显式置 `review` 时不会被会话状态覆盖。

## 会话生命周期同步

卡片可链接到现有仪表盘会话，也可链接到从卡片开始工作时创建的会话。已链接卡片内联显示会话生命周期：`running` / `stale` / `linked idle` / `done` / `failed` / `missing`。

当卡片处于活跃工作状态时，Workboard 跟随已链接会话：

| 关联会话状态 | 卡片状态 |
|---|---|
| active | `running` |
| completed | `review` |
| failed / killed / timed out / aborted | `blocked` |

边界规则：

- **手动 review 优先**：操作员手动置 `review` 不被会话状态覆盖。
- **停止自动同步**：把卡片移到 `review` / `blocked` / `done` 会停止该卡片的自动同步，直到移回 `todo` / `running`。
- **会话缺失**：链接的会话缺失时，卡片保持链接以保留上下文，仍提供启动控件以重启到新会话。
- **陈旧**：活跃已链接会话停止报告近期活动时，Workboard 把卡片标记 `stale` 并作为元数据存储，直到生命周期清除它。
- **Add to Workboard**：Sessions 标签页可对现有会话选 Add to Workboard——卡片链接到该会话，用会话标签或最近用户提示作标题，可用时用最近用户提示 + 最新助手响应填充 notes。
- **Stop**：对活跃已链接卡片用 Stop 会中止活跃运行，Workboard 把卡片标记 `blocked` 以保持可见便于后续处理。
- **存储归属**：启动卡片用正常的 Gateway 会话；Workboard 只存卡片元数据和链接。对话 transcript、模型选择、运行生命周期仍由常规会话系统拥有。

## 从卡片启动工作

| 入口 | 行为 |
|---|---|
| 运行 Codex | 显式引擎启动跟踪任务智能体运行，发送卡片提示，标记卡片 `running`；使用 `openai/gpt-5.5` |
| 运行 Claude | 同上，使用 `anthropic/claude-sonnet-4-6` |
| 打开 Codex / 打开 Claude | 创建已关联仪表盘会话，**不**发送卡片提示、**不**移动卡片——用于挂接到看板的手动工作 |
| 自主启动 | 用 Gateway 跟踪任务智能体运行路径（默认智能体和模型，除非显式选 Codex / Claude）；随后 Workboard 把生成的任务、运行 id 和会话键关联回卡片；每个已关联执行记录一次尝试摘要（引擎、模式、模型、运行 id、时间戳、状态、滚动失败次数），重复失败保持可见 |

仪表盘从 Gateway 任务账本刷新任务状态，按任务 id、运行 id 或已关联会话键把任务匹配到卡片。排队中 / 运行中的任务让卡片生命周期保持活跃；已完成、失败、超时或已取消的任务用与已关联会话相同的同步规则把卡片推进到 `review` 或 `blocked`。

## 诊断

根据本地卡片元数据计算：

| 类型 | 条件 |
|---|---|
| `stranded_ready` | 已分配的 `todo` / `backlog` / `ready` 卡片超过 1 小时未更新 |
| `running_without_heartbeat` | `running` 卡片超过 20 分钟没有认领 heartbeat 或执行更新 |
| `blocked_too_long` | `blocked` 卡片超过 24 小时未更新 |
| `repeated_failures` | 卡片跟踪的失败计数达到 2 次或更多 |
| `missing_proof` | `done` 卡片没有 proof / artifacts / attachments |
| `orphaned_session` | `running` 卡片有 `sessionKey` 但没有 `execution` 元数据 |

## 卡片元数据

卡片除核心字段外，还携带紧凑元数据，让操作员无需打开关联会话就能看到卡片如何在看板中流转——它是本地操作上下文，不是会话转录或 GitHub issue 历史的替代品。包括：

尝试、评论、链接、证明、工件、自动化设置、附件、worker 日志、worker 协议状态、声明、诊断、通知、模板 id、归档状态、陈旧会话检测，以及最近事件列表。

## 最近事件清单

卡片最近事件类型：`created`、`edited`、`moved`、`linked`、`specified`、`decomposed`、`claimed`、`heartbeat`、`execution_updated`、`attempt_started`、`attempt_updated`、`comment_added`、`link_added`、`proof_added`、`artifact_added`、`attachment_added`、`diagnostic`、`notification`、`dispatch`、`orchestration`、`protocol_violation`、`archived`、`unarchived`、`stale`。

## 看板配置与分派意图

看板元数据可设置 `autoDecompose`、`autoDecomposePerDispatch`、`defaultAssignee`、`orchestratorProfile`。OpenClaw 记录此意图并在 worker 上下文中公开；实际的规格说明 / 分解仍通过正常的 Workboard 工具运行（不绕过工具协议）。

## 仪表盘工作流（参考）

1. 在 Control UI 打开 Workboard 标签页
2. 创建带标题 / notes / 优先级 / 标签 / 可选智能体 / 可选已链接会话的卡片——或打开 Sessions 为现有会话选 Add to Workboard
3. 在列之间拖动卡片，或聚焦其紧凑状态控件用菜单或 `ArrowLeft` / `ArrowRight` 移动
4. 从卡片开始工作以创建或复用仪表盘会话
5. 智能体工作时，从卡片打开已链接会话
6. 让生命周期同步把运行中的工作移到 `review` / `blocked`，然后接受后手动移到 `done`
