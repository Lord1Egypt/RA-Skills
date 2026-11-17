# workbuddy-skill-session-callback

**会话回调（Session Callback）** — WorkBuddy 技能：让一个会话（或外部 cron job / 监控进程）**唤醒另一个会话**并注入消息，目标 agent 带着**完整上下文**继续处理。

等价于 openclaw 的 `sessions_send`（`agent:main:session-xxx` + `visibility=agent`），基于 WorkBuddy 官方实现的 **ACP 协议（Agent Client Protocol）**，原生支持，无需 hook 桥接。

> 注意：这是 **WorkBuddy 特化**技能，与 openclaw 生态的 `cron-callback-session`（openclaw 原生 cron/session 注入）是**互补关系**，技术链路不同。如果你用 WorkBuddy 桌面版，用本技能；用 openclaw，用你已发布的 cron-callback-session。

---

## 安全性说明（重要）

本技能具备**跨会话消息注入**能力（向任意指定会话注入消息并触发其 agent 处理），属于**高影响操作**。使用前必须理解并遵守以下安全边界：

### 风险认知

- **注入 = 触发目标会话的 agent 执行**：被注入的消息会被当作该会话的 user 消息处理，可能触发工具调用（读文件、执行命令等）
- **注入内容不可信风险**：如果注入源（cron job、外部进程、其他会话）被攻陷或配置错误，可能导致目标会话执行非预期操作
- **会话隔离可能被绕过**：本技能提供了跨会话通信通道，绕过了"会话间不共享上下文"的默认隔离

### 安全使用准则

1. **只注入可信内容**：注入消息必须来自可信来源（自己控制的 cron job / 脚本 / 会话），绝不能把外部不可信输入直接注入会话
2. **最小化注入范围**：明确指定目标会话 UUID，不要用通配或动态推断；只注入需要回调的会话
3. **注入消息要自包含、低权限**：注入内容应尽量是"提醒/状态通知"而非"命令/指令"；需要执行操作时，让目标 agent 按自身权限判断，而非由注入消息直接驱动危险动作
4. **使用 WorkBuddy 内置 automation 作为调度**（宿主管理，可审计）；避免用不受控的外部脚本
5. **本地回环限制**：本技能仅连接 `127.0.0.1` 本地端点，不要把它暴露到网络（不要在远程/容器环境对宿主机 endpoint 调用）

### 默认安全边界

- 仅访问本地回环端点（`127.0.0.1`），不涉及云端接口
- 不读取会话内容之外的数据，不做越权操作
- ACP 端点由 WorkBuddy 桌面版管理，认证（loopback 豁免）仅限本机

### 对审核意见的回应

> "enables high-impact cross-session prompt injection into live WorkBuddy sessions without enough user confirmation, scoping, or authorization controls"

**已采取的缓解**：
- **scoping（范围限定）**：必须显式指定目标会话 UUID，脚本不做通配/自动选择；默认只注入明确指定的会话
- **authorization（授权）**：脚本设计为仅由用户明确发起的自动化任务调用；建议配合 WorkBuddy 的权限模式（bypassPermissions 之外的模式）使用，让目标会话的工具调用受权限控制
- **confirmation（确认）**：定时回调场景中，automation 的 prompt 应写明注入目标和内容，便于用户在任务定义中确认；重大操作建议先在目标会话内确认再执行

**建议的额外加固**（用户自行决定）：
- 回调脚本仅允许 `--session-id` 白名单内的会话
- 注入消息使用固定前缀（如 `【回调】`）便于目标会话识别来源
- 敏感操作（删除、写文件、发消息）在注入内容中明确要求目标 agent 先征求用户确认

### 使用完毕的收敛（用完恢复默认）

本技能是高影响操作，**使用完毕后建议收敛回默认状态**：

1. **临时回调用完**：删除不再需要的 automation；脚本不留后台进程
2. **权限收敛**：若为实验临时放宽过任何配置，用毕恢复默认；WorkBuddy 默认的会话隔离（不共享上下文）是安全基线，非必要不长期保持跨会话通道
3. **日志清理**：callback 运行日志用完可删，避免残留敏感信息（会话 ID、消息内容）
4. **目标会话保持**：被唤醒的会话如无后续任务，可正常关闭

**原则**：跨会话注入是"按需开启、用完即收"的能力，不应作为长期常开的通道。

## 解决的问题

WorkBuddy 原生会话隔离：
- 内置 automation = **另开会话执行**（上下文不共享）
- REST API 的 sessions 端点只有 list/delete/rename（**没有 send**）

而"监控回传 → 主会话续跑"、"异步任务完成 → 通知会话"、"多会话协作接力"都需要**在既有会话里注入消息**。本技能填补这个缺口。

## 核心能力

1. **唤醒**：确认/拉起目标会话进程
2. **注入**：向目标会话发送消息（转 user 消息，agent 自动处理）
3. **上下文延续**：目标会话转录全量加载，agent 记得该会话所有历史（实测 `prompt_tokens` = 完整上下文）

## 技术基础

| 层面 | 性质 |
|------|------|
| **ACP（Agent Client Protocol）** | 开放协议标准（agentclientprotocol.com，Anthropic 发起，与 MCP 同级）|
| `session/load` / `session/prompt` | ACP 协议公开定义 |
| WorkBuddy 暴露 `/api/v1/acp/*` | 官方实现（官方 HTTP API 文档收录）|

本技能 = 基于公开协议调用官方端点。仅调用本地回环端点（127.0.0.1），不涉及云端、不做越权操作。

## 安装

### 方式一：手动安装（推荐）

1. 下载本仓库 zip 或 clone
2. 将 `workbuddy-skill-session-callback` 整个目录复制到：
   - 用户级：`~/.workbuddy/skills/`
   - 项目级：`<workspace>/.workbuddy/skills/`

### 方式二：ClawHub

```bash
openclaw skills install @onesfuture/workbuddy-skill-session-callback
```

或使用 ClawHub CLI：

```bash
clawhub install @onesfuture/workbuddy-skill-session-callback
```

## 使用

### 一键回调

```bash
python scripts/callback.py <目标会话UUID> "要注入的消息" [--workdir <路径>] [--endpoint <URL>]
```

脚本自动完成：发现 endpoint（心跳排序 + 连通性探测）→ connect → initialize → session/load → session/prompt。

### 定时回调（cron job 场景）

用 WorkBuddy 内置 automation 作为调度器（宿主调度，独立于任何 agent 回合，可靠）：

1. 创建 automation，rrule 设执行频率
2. prompt 里指示运行 `callback.py` 注入到目标会话
3. automation 触发 → 注入 → 目标会话被唤醒

> ⚠️ 不要用 nohup / Start-Process 后台进程做定时注入——它们会随 agent 回合结束被回收，不可靠。

### 目标会话 ID 从哪来

- 会话索引：`~/.workbuddy/app/sessions.json`（conversationId ↔ workDir，resumedAt 标记活跃）
- 当前会话：环境变量 `CODEBUDDY_SESSION_ID`

## 队列与空闲机制

| 目标会话状态 | 行为 |
|-------------|------|
| 空闲 | 消息立即处理 + 立即落盘 |
| 忙（正在跑任务）| 消息进队列，不打断当前 run，空闲后执行 |

注入忙会话不丢、不打断——监控回传不会插队打断正在进行的 agent。

## 兼容性与已知坑

- 实测版本：WorkBuddy 桌面版 2.x（CLI 引擎 2.115.0）
- **目标会话必须活着**：进程退出（endpoint 拒连）时注入失败，需先在界面打开会话
- **会话 ID 对齐**：界面窗口 / 环境变量 / 会话索引 / 转录实时写入四信号应一致；重启后可能错位，先对齐再注入
- 自动发现 endpoint 已做**心跳排序 + 连通性探测**，规避注册表残留死进程误导
- 方法名必须精确：`session/load` + `session/prompt`（不是 newSession/loadSession）

## 目录结构

```
workbuddy-skill-session-callback/
├── clawhub.yaml                # ClawHub 元数据
├── SKILL.md                    # 技能说明（定位/工作流/队列机制/发布声明）
├── scripts/
│   └── callback.py             # 一键回调脚本（心跳排序 + 连通性探测）
└── references/
    └── api_reference.md        # ACP 协议详细参考
```

## 免责声明

本技能基于公开协议（ACP）与实测经验编写，不构成对 WorkBuddy 官方能力的承诺。协议与本地数据布局可能随版本变化，使用前请验证兼容性。

## 反馈

发现 bug 或有改进建议？请开 [GitHub Issue](https://github.com/onesfuture/workbuddy-skill-session-callback/issues)。
