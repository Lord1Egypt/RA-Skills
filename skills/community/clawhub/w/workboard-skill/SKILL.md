---
name: workboard
description: 当用户想用 OpenClaw Workboard 看板管理智能体工作卡片时使用——列出/创建/查看卡片、把就绪卡片分派给子智能体 worker、查看卡片生命周期与诊断、或排查卡片无法保存、分派仅数据、worker 不启动等问题。涉及 openclaw workboard CLI、/workboard 斜杠命令、看板状态机与会话生命周期同步。
---

# Workboard

## 定位

OpenClaw Workboard 是内置看板插件，给 Control UI 加一个 Kanban 风格的看板：智能体粒度的工作卡片、分配给智能体，并返回卡片对应任务、运行和仪表盘会话的链接。它跟踪一个 OpenClaw Gateway 网关的本地操作工作，**不是** GitHub Issues / Linear / Jira 这类团队项目管理系统的替代品。

这个 skill 面向操作员视角，负责三件事：

- 帮 AI 把「列出 / 创建 / 查看 / 分派卡片」落成正确的 `openclaw workboard` 命令
- 约束 AI 在卡片生命周期、调度、会话同步、诊断、排障上的默认路径
- 在需要看智能体工具协议（`workboard_*` 工具、认领令牌、worker 上下文）时指向参考资料

CLI（`openclaw workboard`）、仪表盘分派操作、聊天斜杠命令（`/workboard`）三者操作的是同一份 Workboard 插件自有 SQLite 状态。Claude Code 在这里通常是操作员助手，用 CLI 操作看板；智能体工具是给子智能体 worker 调用的，本 skill 把它们收在参考资料里，不要求 Claude Code 直接调用。

## 前置

Workboard 内置但默认禁用。使用前确认插件已启用、Gateway 在运行：

```bash
openclaw plugins enable workboard
openclaw gateway restart
openclaw gateway status --deep
```

检查插件运行状态：

```bash
openclaw plugins inspect workboard --runtime --json
```

`openclaw` CLI 不在 PATH、或插件未为当前 profile / 状态根目录启用时，所有 `openclaw workboard` 命令都会失败——先排这两项再调命令。

## CLI 用法

```bash
openclaw workboard list   [--board <id>] [--status <status>] [--include-archived] [--json]
openclaw workboard create <title...> [--notes <text>] [--status <status>] [--priority <priority>] [--agent <id>] [--board <id>] [--labels <items>] [--json]
openclaw workboard show   <id> [--json]
openclaw workboard dispatch [--url <url>] [--token <token>] [--timeout <ms>] [--json]
```

要点：

- 卡片 id 是 UUID；`show` 等接受 id 的命令也接受无歧义前缀（紧凑输出只显示前 8 位）
- `list` / `create` / `show` 直接读写本地插件 SQLite 状态，不经过 Gateway；只有 `dispatch` 调用运行中的 Gateway
- 有效 status：`triage backlog todo scheduled ready running review blocked done`
- 有效 priority：`low normal high urgent`

### list

```bash
openclaw workboard list
openclaw workboard list --board default --status ready
openclaw workboard list --json
```

紧凑文本输出（列依次：id 前缀 / 状态 / 优先级 / 看板 id / 可选智能体 id / 标题）：

```
7f4a2c10 ready high default agent-a Fix stale worker heartbeat
```

- 默认隐藏已归档卡片；`--include-archived` 显示；`--json` 始终包含已归档卡片（兼容现有自动化）

### create

```bash
openclaw workboard create "Fix stale worker heartbeat" --priority high --labels bug,workboard
openclaw workboard create "Write Workboard docs" --status ready --agent docs-agent --board docs \
  --notes "Cover CLI, slash command, dispatch, and SQLite state."
```

默认 `status=todo`、`priority=normal`。`create` 直接写 SQLite，卡片立即出现在 Control UI 的 Workboard 标签页和智能体工具里。

### show

```bash
openclaw workboard show 7f4a2c10
openclaw workboard show 7f4a2c10 --json
```

文本输出打印紧凑卡片行 + 备注；`--json` 返回完整卡片记录（执行元数据、尝试次数、评论、链接、证明、工件、worker 日志、协议状态、诊断、自动化元数据）。排查卡片卡住时优先用 `--json` 看诊断字段。

### dispatch

```bash
openclaw workboard dispatch
openclaw workboard dispatch --json
openclaw workboard dispatch --url http://127.0.0.1:18789 --token "$OPENCLAW_GATEWAY_TOKEN"
```

调 Gateway RPC `workboard.cards.dispatch`，用与仪表盘分派相同的子智能体运行时把就绪卡片变成带任务跟踪的 worker 运行。文本输出：

```
dispatch complete: started=2 failures=0
```

回退时明确标注：

```
gateway unavailable; data dispatch only: promoted=1 blocked=0
```

`--json` 在 Gateway 支持时含 `started` 和 `startFailures`；仅数据回退含 `gatewayUnavailable: true`。卡片 JSON 输出里认领令牌会被隐去。完整调度语义见下方「调度语义」。

## 斜杠命令

支持命令的渠道可用斜杠命令，与 CLI 对应：

```
/workboard list
/workboard show 7f4a2c10
/workboard create Fix stale worker heartbeat
/workboard dispatch
```

- `list` / `show` 对任何已授权命令发送者都是读取操作
- `create` / `dispatch` 修改看板状态，聊天界面需要 owner 身份，或需要具备 `operator.write` / `operator.admin` 的 Gateway 客户端

## 卡片字段

| 字段 | 取值 |
|---|---|
| status | triage, backlog, todo, scheduled, ready, running, review, blocked, done |
| priority | low, normal, high, urgent |
| labels | 自由格式字符串 |
| agentId | 可选的已分配智能体 |
| 关联引用 | 可选的任务、运行、会话或源 URL |
| execution | 从卡片启动的 Codex/Claude 运行的可选元数据（引擎、模式、模型、会话、运行 id、状态） |

卡片还携带紧凑元数据：尝试、评论、链接、证明、工件、自动化设置、附件、worker 日志、worker 协议状态、声明、诊断、通知、模板 id、归档状态、陈旧会话检测，以及最近事件列表。完整模型、状态机、会话同步规则见 [card-lifecycle.md](./references/card-lifecycle.md)。

新卡片可从模板开始：`bugfix`、`docs`、`release`、`pr_review`、`plugin`——预填标题 / notes / 标签 / 优先级，模板 id 存为卡片元数据。

## 创建卡片：必填字段清单

创建一张工作卡片时，至少填齐以下字段。CLI 用 `openclaw workboard create`，仪表盘在 Workboard 标签页新建——两者写入同一份 SQLite 状态。

| 字段 | 必填 | 写法 | CLI flag |
|---|---|---|---|
| 标题 | 是 | 一句话点明这张卡要做什么 | 位置参数 `<title>` |
| 备注 | 是 | 写清三块：① 背景 / 概述 ② **验收标准**（完成判定，逐条列） ③ **相关链接**（任务 / 运行 / 会话 / 源 URL）。务必清晰可执行 | `--notes <text>` |
| 状态 | 是 | 新建一般 `todo`；已就绪可分派用 `ready` | `--status <status>`（默认 `todo`） |
| 优先级 | 是 | `low` / `normal` / `high` / `urgent` | `--priority <priority>`（默认 `normal`） |
| 代理 | 是 | 选定负责的 agent id（Workboard 本身允许留空，本规范要求必填） | `--agent <id>` |
| 会话 | 是 | **必须绑定一个唯一会话**；建议**新建一个会话**绑定，不要复用（见下） | CLI 无；仪表盘绑定 |
| 标签 | 是 | 逗号分隔，用于分类 / 筛选 | `--labels <items>` |

### 会话绑定（重点）

- **一张卡绑定一个唯一会话**：不要多卡共用一个会话。会话生命周期同步会按会话状态推进卡片（active→`running`、completed→`review`、failed/killed/timeout→`blocked`），多卡共用一个会话会把它们的状态搅在一起。
- **建议新建会话绑定**，而不是复用现有会话——新建能保证唯一性和干净的生命周期。
- **CLI 的 `create` 不带会话参数**：`openclaw workboard create` 没有 session 选项。建卡后到仪表盘 **Sessions 标签页 → Add to Workboard** 绑定一个（新）会话；或从卡片「开始工作」创建 / 复用会话并自动链接。
- 若链接的会话缺失，卡片仍保持链接以保留上下文，并提供启动控件重启到新会话。

### 备注写法

备注里的**验收标准**和**链接**必须清晰可执行：

- **验收标准**：写「做到什么算完成」，逐条列，可被完成者对照判定。
- **链接**：贴具体的任务 id / 运行 id / 会话键 / 源 URL，不要只写笼统描述。

### CLI 建卡示例

```bash
openclaw workboard create "修复 worker 心跳超时" \
  --status todo \
  --priority high \
  --agent agent-a \
  --labels bug,workboard \
  --notes "背景：running 卡 >20min 无心跳被标 running_without_heartbeat。
验收标准：
- 复现并定位心跳丢失原因
- 修复后 running 卡持续心跳 ≥30min 不再触发该诊断
- 回归 1 次 dispatch 无 startFailures
链接：任务 #123 / 运行 run-abc / 会话（新建后于仪表盘绑定）"
```

建卡后到仪表盘给这张卡绑定一个新会话。

## 默认流程

- 用户想看现在有什么卡：`openclaw workboard list`，需要某状态就加 `--status ready`
- 用户想建卡：按「创建卡片：必填字段清单」填齐标题 / 备注（含验收标准与链接）/ 状态 / 优先级 / 代理 / 标签，再 `openclaw workboard create` 建卡；CLI 不带会话参数，建卡后到仪表盘绑定一个**新**会话
- 用户想看某张卡细节：`openclaw workboard show <id>`，要机器消费加 `--json`
- 用户想让 worker 跑起来：先 `openclaw workboard list --status ready` 确认有未认领的就绪卡，再 `openclaw workboard dispatch`
- 用户反馈「分派没启动」或「只报了数据调度」：走「故障排查」里的分派分支
- 用户问卡片为什么停在某状态 / 为什么被标 stale：查 [card-lifecycle.md](./references/card-lifecycle.md) 的状态机、会话同步和诊断规则
- 用户问 worker 拿到哪些工具、认领令牌怎么用：查 [agent-tools.md](./references/agent-tools.md)

## 调度语义

调度是 Gateway 本地的，不生成任意 OS 进程；正常 OpenClaw 子智能体会话仍拥有执行权。一次 `dispatch` 会：

1. 把依赖已就绪的子卡片提升为 `ready`
2. 阻塞过期认领或超时 worker 运行
3. 在就绪卡片上记录分派元数据
4. 选一小批未认领的 `ready` 卡片
5. 为分派器或已分配智能体认领每张选中卡片
6. 用有界卡片上下文 + 卡片认领令牌启动子智能体 worker 运行
7. 在卡片上存 worker 运行 id、会话键、任务链接、执行状态、worker 日志

**Worker 选择**（较保守）：

- 一次分派默认最多启动 3 个 worker
- 就绪卡片按优先级 → 位置 → 创建时间排序
- 一次分派只为每个 owner / 智能体启动一张卡片，跳过看板上已有 `running` 或 `review` 工作的 owner
- 已归档卡片、有活跃认领的卡片、状态不是 `ready` 的卡片，永远不会被选中启动 worker（但仍受数据侧影响：陈旧认领清理、依赖提升、超时清理）
- 会话键按看板 / 卡片确定性生成，重复分派会路由回同一 worker 通道，不会创建无关会话：
  - 已分配：`agent:<agentId>:subagent:workboard-<boardId>-<cardId>`
  - 未分配：`subagent:workboard-<boardId>-<cardId>`（Gateway 解析已配置的默认智能体）

**启动失败处理**：卡片被认领后无法启动 worker 时，Workboard 阻塞该卡片、清除认领、记录运行启动失败、追加 worker 日志行——失败保持可见，而不是静默把卡片放回队列。

**Gateway 不可用回退（仅数据调度）**：当 Gateway RPC 因连接 / 不可用失败（或旧版返回 `unknown method`），且没有显式 `--url` / `--token`、也没有已配置远程 Gateway（`OPENCLAW_GATEWAY_URL` 或 `gateway.mode: remote`）时，CLI 对本地 SQLite 跑仅数据分派：能提升依赖、清理陈旧认领、阻塞超时运行，**但**不能启动 worker。来自可访问 Gateway 的身份验证 / 权限 / 校验失败不算不可用，作为命令错误直接报；给了显式 `--url` / `--token` 时，任何 Gateway 失败也直接报、不回退。

三个分派入口在 Gateway 可用时都用其子智能体运行时：仪表盘分派操作、`openclaw workboard dispatch`、`/workboard dispatch`。

## 诊断

诊断根据本地卡片元数据计算，内置检查：

| 类型 | 条件 |
|---|---|
| stranded_ready | 已分配的 todo / backlog / ready 卡片超过 1 小时未更新 |
| running_without_heartbeat | running 卡片超过 20 分钟没有认领 heartbeat 或执行更新 |
| blocked_too_long | blocked 卡片超过 24 小时未更新 |
| repeated_failures | 卡片失败计数达到 2 次或更多 |
| missing_proof | done 卡片没有 proof / artifacts / attachments |
| orphaned_session | running 卡片有 sessionKey 但没有 execution 元数据 |

排查卡片卡住时，先用 `show --json` 看诊断字段，对照上表定位原因。

## 权限与存储

Gateway RPC 方法在 `workboard.*` 下：`operator.read` 覆盖只读方法（`cards.list` / `cards.export` / `cards.diagnostics` / attachment 读取 / notification 事件读取 / `boards.list` / `cards.stats` / `cards.runs`），`operator.write` 覆盖所有变更方法（创建 / 移动 / 删除 / 认领 / 分派 / 指定 / 分解等）。**没有**方法需要 `operator.admin`。只读操作员浏览器能看板但不能改卡。CLI 分派路径用 `operator.read` + `operator.write` 调 RPC；只读 Gateway 令牌能看数据但不能建卡或分派。

数据存在 OpenClaw 状态目录下、插件自有的关系型 SQLite 库里（boards / cards / labels / lifecycle events / run attempts / comments / dependency links / proof / artifact references / attachment metadata and blobs / diagnostics / notifications / worker logs / protocol state / subscriptions），随该 Gateway 的其他 OpenClaw 状态一起移动。`.28` 版本用过的安装可跑 `openclaw doctor --fix` 把旧版插件状态命名空间（`workboard.cards`、`workboard.boards`、`workboard.notify`，及若存在的 `workboard.attachments`）迁移到关系型库。

## 故障排查

| 现象 | 处理 |
|---|---|
| 标签页显示 Workboard 不可用 | `openclaw plugins inspect workboard --runtime --json`；若配了 `plugins.allow` 就把 `workboard` 加进去；若 `plugins.deny` 含 `workboard` 先移除再启用 |
| 卡片无法保存 | 确认浏览器 / 令牌有 `operator.write`；只读会话能列卡但不能建 / 改 / 移 / 删 |
| CLI 看不到卡但仪表盘有 | 确认 CLI 和仪表盘用同一 `--dev` / `--profile` / 状态根目录；`openclaw plugins inspect workboard --runtime --json` |
| 启动卡片没打开预期会话 | 查卡片的 agentId 和已链接会话，打开 Sessions / Chat 看实际运行状态 |
| 分派提示仅数据 | `openclaw gateway restart` → `openclaw gateway status --deep` → 重试 `openclaw workboard dispatch`；仅数据回退对本地清理有用，但 worker 运行要可用 Gateway |
| 分派没启动任何 worker | `openclaw workboard list --status ready` 确认有未认领就绪卡；同一 owner 已有 running / review 工作时会被跳过——先 complete / block / release 那些活跃工作再分派 |
| 卡片停在 running 不动 | 查 `show --json` 诊断：`running_without_heartbeat`（>20min 无心跳 / 执行更新）或 `orphaned_session`（有 sessionKey 无 execution） |

## 何时读取参考资料

- 需要状态机、会话生命周期同步表、诊断详情、生命周期事件清单：读 [card-lifecycle.md](./references/card-lifecycle.md)
- 需要智能体工具协议（`workboard_*` 工具表、认领令牌脱敏、worker 上下文、链接 / 分解 / 通知游标语义）：读 [agent-tools.md](./references/agent-tools.md)

## 使用原则

- 先确认 `openclaw` 在 PATH、插件已为当前 profile 启用，再调命令
- `list` / `create` / `show` 直接操作本地 SQLite，不依赖 Gateway；只有 `dispatch` 需要 Gateway
- 用 `show --json` 拿完整卡片记录（执行 / 尝试 / 评论 / 链接 / 证明 / 工件 / worker 日志 / 诊断），用纯 `show` 看紧凑行 + 备注
- 分派前先用 `list --status ready` 确认有未认领就绪卡，避免「分派没启动」的来回
- 一次分派每个 owner / 智能体只起一张卡、默认上限 3 个 worker；同一 owner 已有 running / review 时新卡会被跳过
- 只读令牌 / 浏览器能看不能改；改卡或分派需要 `operator.write`
- 不要把 Workboard 当团队项目管理系统用——它只跟踪单 Gateway 的本地操作工作
- 卡片结论、优先级判断由人 / LLM 决定，CLI 只返回状态和诊断数据
