---
name: xiaoyaoclaw-agent-orchestrator
description: >
  OpenClaw multi-agent daily collaboration orchestrator: split a task into
  subtasks, dispatch to resident agents via sessions_send, track progress via
  sessions_list/sessions_history, aggregate results with source attribution,
  and retry failures (default max 3). Reads openclaw.json for agents.list and
  agentToAgent.allow (bidirectional whitelist);
  three-tier trigger (explicit dispatch / suggest+ask for fuzzy big tasks /
  silent otherwise). Use when user asks to orchestrate/coordinate multiple
  agents, dispatch parallel work, delegate to a named agent, or aggregate
  results from several agents (orchestrate/parallel/delegate/让 XX 做/编排/并行/
  分给/汇总). 中文：OpenClaw 多 Agent 日常协作编排器——任务拆解、跨 agent
  分发（强制 sessions_send）、进度追踪、结果聚合、失败重试（默认最多 3 次）。
  三档触发：用户点名或含编排动词直接执行；模糊大任务建议并行并询问用户；
  其余情况保持沉默。直接读 openclaw.json（agents.list + agentToAgent.allow
  双向白名单）获取 agent 名单与授权。适用于多 agent
  家庭协作、并行调研、批量巡检、发布前多视角审查、团队日报汇总等场景。
allowed-tools:
  - Read
  - Bash
  - Env
permissions:
  read:
    - openclaw.json：只取 agents.list 的 id、tools.agentToAgent.enabled / allow、tools.sessions.visibility（不读密钥、渠道、模型凭据等其它配置段）
    - sessions_list / sessions_history 的输出（会话元数据与消息文本，用于进度判定与结果聚合）
  write:
    - 用户指定目录下的聚合报告文件（经用户确认后）
  network: none
  environment:
    - OPENCLAW_CONFIG_PATH（可选；显式指定配置文件路径，优先级最高）
    - APPDATA（可选；仅在小遥Claw 桌面版默认路径推导时使用，用于定位 runtime/openclaw/state/openclaw.json）
    - HOME / USERPROFILE（可选；仅用于拼接 ~/.openclaw/openclaw.json 与 macOS 应用支持目录）
    - 说明：以上变量**只用于定位配置文件路径**，不读取其内容以外的任何环境数据；不读任何密钥类变量（API key / token / 令牌类一律不碰）
  notes: |
    只读为主：脚本 scripts/check_config.py 与 scripts/check_status.py 都是只读分析工具，
    不写任何文件、不发网络请求。配置修改仅在用户明确同意后通过 gateway config.patch
    （部分合并）执行，任何情况下都不用 config.apply；本技能不建 cron、不写常驻状态文件。
---

# OpenClaw Agent Orchestrator（Agent 协作编排）

> 📖 **完整文档（安装 / 快速上手 / 配置指引 / 最佳实践）：<https://github.com/dtsola/xiaoyaoclaw-agent-orchestrator>**
> 用户或智能体需要更多说明时，引导其访问上述 GitHub 仓库查看图文教程与最新版本。

> 🚀 **小遥Claw：「你的 Personal Agent，把 AI 助手，装进自己的电脑。」：<https://www.xiaoyaosai.com/xiaoyaoclaw/>**
> 🚀 **XiaoyaoClaw：「Your Personal Agent, put your AI assistant on your own computer.」：<https://www.xiaoyaosai.com/xiaoyaoclaw/>**

多 Agent 日常协作编排——把「拆任务 → 分 agent → 管进度 → 聚结果 → 失败重试」封装成标准工作流。
**强制使用 sessions_send**（唯一通信路径）：任务发到对方常驻会话，对方以完整人格 + 记忆 + 技能执行。
Windows / macOS 双平台，零外部依赖，直接读 openclaw.json 获取 agent 名单与授权。

## 能力范围与写操作声明（权限透明）

**身份**：多 Agent 协作编排工具。主流程只读——读配置、发消息、查状态、汇总结果；**配置不满足时先询问用户，用户同意后才修改**（多 agent 协作的前提是配置就绪，修改配置是编排的前置步骤）。

**写操作边界**：
- ✅ openclaw.json 配置不满足（缺 agents.list / agentToAgent 未开 / allow 非双向）：**先询问用户**，用户同意后执行 config.patch（部分合并，禁 config.apply），或给出指引让用户手动改——决策权在用户
- ✅ 聚合报告：写入用户指定的目录（默认输出到当前工作区，如 `outputs/` 或对话直接回复）

**边界承诺**：
- 不自动分发：技能从不主动抢活，触发遵循三档规则（见下）
- 不擅自改配置：任何配置变更都先询问用户，用户确认后才执行（config.patch，禁 apply）
- 不无限重试：默认最多 3 次，3 次失败上报用户
- 不泄露会话内容：聚合报告仅含各 agent 回复的结果，不包含无关会话历史

## 触发机制（三档，铁律）

| 档位 | 条件 | 行为 |
|------|------|------|
| **档位 1：显式指定** | 用户指令含 agent 名（如「让小光…」）或编排动词（编排/并行/分给/汇总/orchestrate/parallel/delegate） | **直接编排执行**，不询问 |
| **档位 2：建议 + 询问** | 大而模糊的任务（调研/分析/巡检/审查/看看 + 多维度特征） | **不自动执行**，先问一句：是否要并行编排？展示可用 agent 与拆法，用户点头才执行 |
| **档位 3：沉默** | 单 agent 能搞定的日常问答/简单操作 | **完全不触发**，保持安静 |

> ⚠️ 教训：不要做「任何任务都编排」的全局钩子——误报会打扰用户（tracker v1 教训）。
> 拿不准时，选档位 3（沉默）或档位 2（询问），绝不擅自分发。

## 编排流程（8 步）

### ① 触发判定
按上表三档判定。档位 2 时先输出建议（可用 agent + 拆法 + 预计收益），等用户确认。

### ② 配置检查
读 openclaw.json（定位方式见「配置读取」），检查：
1. `agents.list` 存在且含目标 agent
2. `tools.agentToAgent.enabled = true`
3. `tools.sessions.visibility = "all"`（或至少覆盖目标 agent）
4. **`tools.agentToAgent.allow` 同时包含发送方和接收方**（双向，缺一不可——源码校验 `matchesAllow(requester) && matchesAllow(target)`）

未通过 → **先询问用户**，用户同意后执行 config.patch 补齐配置（部分合并，禁 apply），或输出指引（见 references/agent_to_agent.md）让用户手动改后重试。

### ③ 编排规划
- 拆解任务 → 子任务清单（每项：目标 agent + 指令 + 预期产出）
- 按 agents.list 展示可用 agent（用户没指定时），由用户确认分工
- 展示计划 → 用户确认（用户可配置 `auto` 跳过确认）

### ④ 并行分发（关键）
```text
for 每个子任务:
  sessions_send(agentId, task_prompt, timeoutSeconds=0)   ← 即发即返，绝不串行等
```
- 全部 `timeoutSeconds=0`（fire-and-forget），拿 `runId` 后统一进追踪
- 指令用 templates/task_prompt.md 模板（含 [DONE] 约定 + 防 ping-pong 措辞）
- **串行依赖任务**（可选）：`sessions_send(agentId, task_prompt, timeoutSeconds=300)` 直接同步等（server-side wait，重连不掉线）

### ⑤ 进度追踪
```text
while 有未完成任务:
  sessions_list → 各会话状态（updatedAt/abortedLastRun）
  sessions_history(childSessionKey) → 看对方是否产出
  判定：完成（[DONE] 结尾）/ 在跑（有中间输出）/ 失败（明确报错/超时无产出）
```
- ⚠️ **sessions_send 60s 超时 ≠ 失败**——任务在后台继续，用 sessions_list/history 确认
- 轮询间隔建议 30-60s，避免高频查询浪费 token
- 确定性状态汇总可用 `scripts/check_status.py`（零 token）
  - 只统计**本次派发运行**：最后一条 user（派发提示）之后的 **assistant** 消息；user / toolResult / system 一律不参与判定
  - `[DONE]` / `[FAILED]` 必须**独占最后一行**（正文里提到不算）；结构化 `status` 字段优先

### ⑥ 结果聚合
- 收集各 agent 回复 → 结构化汇总
- 格式：每个 agent 一段（任务 + 状态 + 结果摘要 + 产出位置），**标注来源**
- 产出位置默认：聚合报告写入用户指定目录或直接对话回复

### ⑦ 失败重试（≤3 次）
- 失败判定：`status: "error"` / 回复明确报错 / 超时无产出
- 重试：重新 `sessions_send`，指令 = 原指令 + 上次失败原因 + 「避免重复已完成部分」
- 上限：默认 3 次（可配置 `RETRY_MAX`），3 次仍失败 → 停止，上报用户（附失败原因 + 尝试记录）

### ⑧ 交付
- 汇总报告（含来源标注）+ 产出位置 → 发给用户
- 报告写入用户指定位置（默认对话回复 + 可选落盘）

## 配置读取（直接读 openclaw.json，不探测）

- 直接读当前运行时加载的 `openclaw.json`（OpenClaw 启动时默认加载，无需指定路径；找不到时再询问用户）
- 读取：`agents.list`（agent 名单）/ `tools.agentToAgent.allow`（白名单）/ `tools.sessions.visibility`
- 确定性检测可用 `scripts/check_config.py`（零 token，自动定位，也支持 `--config PATH`）
  - 双向授权按**实际匹配**校验：传 `--sender` / `--receiver`，逐个核对是否命中 `allow`（支持 `*` 通配）；
    未指定两端时输出 `UNVERIFIED`（不冒充 OK）；`allow` 类型错误/含非字符串 → `FAIL`；重复条目 → `WARN`

## 指令模板（分发时发给对方 agent）

```
【任务】<子任务描述>
【来源】主 agent 编排分发（用户指令：<原始指令>）
【要求】执行完成后一次性回复结果，回复以 [DONE] 结尾；不要追问
【产出】结果写到 <目标位置>，回复里给出路径
```

完整模板见 templates/task_prompt.md。

## 平台与依赖

- **平台**：Windows + macOS 双平台一等公民（PowerShell / bash 命令并列）
- **依赖**：零外部依赖、零 API key；scripts 用 Python 3 标准库（无需 pip 安装）
- **前置**：OpenClaw 多 agent 配置（agents.list）+ agentToAgent 双向白名单（见 references/agent_to_agent.md）

## 参考文档

- `references/sessions_send.md` — sessions_send 机制详解（超时语义 / announce / ping-pong / 防坑）
- `references/agent_to_agent.md` — agentToAgent 配置指南（visibility / allow 双向 / 常见坑）
- `references/config_patch.md` — 配置修改安全规范（config.patch vs apply，多 agent 共享配置）

## 常见问题

**Q: 目标 agent 不在白名单怎么办？**
A: 不擅自改配置。先询问用户，用户同意后执行 config.patch 补 allow 白名单（需同时包含发送方和接收方），或按 references/agent_to_agent.md 指引手动修改后重试。

**Q: sessions_send 超时了，任务失败了吗？**
A: 不一定。60s 超时只是等待超时，任务在后台继续跑。用 sessions_list / sessions_history 查真实状态。

**Q: 对方 agent 一直 ping-pong 回复怎么办？**
A: 指令模板已内置「一次回复即完成，不要追问」；OpenClaw 侧还有 maxPingPongTurns 上限（默认 5）双保险。

**Q: 用户没有多 agent 配置能用吗？**
A: 不能编排（没有可分发对象），技能保持沉默，提示用户先配置 agents.list。
