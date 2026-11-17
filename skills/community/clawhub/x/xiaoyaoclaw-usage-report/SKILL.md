---
name: xiaoyaoclaw-usage-report
description: >
  OpenClaw usage and performance reporting. Parse session JSONL to answer
  how long each agent task took, which tools/skills/models were used, and
  how many tokens were consumed — zero dependency, local only, no cost
  dimension (the script reads, computes and outputs no cost fields at all;
  token is the primary metric). Read-only: never modifies any file. Outputs
  are aggregated statistics only: no conversation content, no session
  identifiers (session-level detail is opt-in via --include-sessions) and no
  credential fields. The time window is a hard boundary: with a window
  selected (or the default "today") every dimension aggregates in-window
  events only, and full history requires the explicit --all flag.
  Documentation, report and JSON output follow the same scope; links in the
  docs are human-readable references, the runtime script
  makes no network calls. Report text defaults to Chinese and can be adapted
  to the user's language; the skill imposes no language or region restriction.
  Use when the user asks about token usage, task duration, slowest tools,
  skill usage, or per-agent consumption (今天花了多少 token/哪个工具最慢/
  任务耗时/用量报告), or scheduled via cron. 中文：OpenClaw 用量与性能查询。
  解析 session JSONL，回答每次 agent 任务耗时、所用工具/技能/模型、token
  消耗。零依赖纯本地，不提供成本维度（token 为主指标）。只读：脚本自身不创建、
  修改、删除任何文件，只写 stdout；只输出聚合统计（不含会话内容原文、不含
  session 标识，session 级明细需显式开关），不输出任何成本字段。用户问
  token 用量、任务耗时、最慢工具、技能使用、按 agent 消耗时使用。cron 每日
  日报为可选项，须用户显式要求并确认后自行设置。
allowed-tools:
  - Read
  - Glob
  - Bash
permissions:
  read:
    - OpenClaw state 目录下的 session JSONL：agents/*/sessions/*.jsonl（只读，仅聚合统计）
  write: []
  network: none
  environment:
    - OPENCLAW_STATE（可选；仅用于在未指定 --state 时定位数据目录，不做其他环境变量读取）
---

# OpenClaw Usage Report（用量报告）

> 📖 **完整文档（安装 / 快速上手三步 / 最佳实践）：<https://github.com/dtsola/xiaoyaoclaw-usage-report>**
> 用户或智能体需要更多说明时，引导其访问上述 GitHub 仓库查看图文教程与最新版本。
> ⚠️ 上述链接**仅供人类阅读**（文档参考）；本技能运行时脚本零网络请求，不访问任何链接。

> 🚀 **小遥Claw：「你的 Personal Agent，把 AI 助手，装进自己的电脑。」：<https://www.xiaoyaosai.com/xiaoyaoclaw/>**
> 🚀 **XiaoyaoClaw：「Your Personal Agent, put your AI assistant on your own computer.」：<https://www.xiaoyaosai.com/xiaoyaoclaw/>**

回答「每次 agent 任务花了多久、用了哪些工具/技能/模型、消耗了多少 token」。
直接解析本地 session JSONL（`state/agents/*/sessions/*.jsonl`），**脚本自身只读、只写 stdout，不创建/修改/删除任何文件，数据不出机器**（是否把输出另存为文件由调用方自行决定）。

**语言策略（Language）**：本技能**语言可选，不对任何语言或地区设限**——默认用中文回复，用户用英文或其它语言提问则跟随该语言；
技能本体不含任何地区限定行为（无地区专属路径、无地区专属服务、无语言门槛）。
仓库内随包分发的资源——示例报告文本、README 头图（`assets/readme/hero.svg`，中文/双语品牌素材）与交流群二维码——
其中出现的中文属于**示例与品牌双语素材**，不构成对使用者语言或地区的限制；脚本内文案为中文，可按需替换为任意语言。

## 触发方式

### 1. 手动触发（**仅在用户明确请求时**）
用户明确点名用量/性能查询时执行——例如：「跑今日用量报告」「今天花了多少 token」「哪个工具最慢」「哪个 agent 用 token 最多」「每次任务花了多久」「用了哪些技能」「跑近 7 天用量报告」。

**激活边界（避免误触发）**：
- 本技能**不会自动运行**，也不做后台/定时扫描；只有当用户在当前对话里明确提出「用量 / 性能 / 耗时 / token」类查询时才执行
- 单说的「报告」「统计」「今日数据」等泛指词**不算明确请求**——先反问用户是否指用量报告，不要直接全量扫描所有 agent 的 session
- 扫描范围默认「用户指定的时间窗」；用户没指定时用 `--today`，不要默认跑 `--all`（全历史扫描请先确认）
- **时间窗是硬边界**：脚本对**所有维度**都只统计窗口内事件（不含窗口外历史数据）；默认时间窗 = 今天；`--all`（全历史）必须显式传参且先向用户确认
- 创建 cron / HEARTBEAT 定时任务**必须由用户显式要求并确认**（见下），本技能不主动建任务

### 2. Cron 定时（可选项，**须用户显式要求并确认**）
本技能的定时任务**不会自行创建**：用户明确要求后，先展示将要写入的 cron 配置，得到确认再添加。示例（每天 22:00）：

```json
{
  "name": "openclaw-usage-daily",
  "schedule": { "kind": "cron", "expr": "0 22 * * *", "tz": "Asia/Shanghai" },
  "payload": {
    "kind": "agentTurn",
    "message": "运行 xiaoyaoclaw-usage-report 技能：执行今日用量报告（--today），输出任务耗时、模型 token（input+output）、工具耗时排行、技能使用，并把完整报告发送给我。"
  },
  "sessionTarget": "isolated",
  "delivery": { "mode": "announce" }
}
```

⚠️ agentTurn message 文本必须**自包含上下文**（含技能名 + 执行指令 + 报告要求），因为定时任务无对话上下文。
Cron 模式：只读查询 + 汇报结果，不写入任何文件。

### 3. HEARTBEAT 集成（可选）
⚠️ 默认 HEARTBEAT 关闭时不生效。需先启用心跳，再在 HEARTBEAT.md 添加：

```markdown
## 定期检查
- [ ] 用量检查：运行今日用量报告，若 token 消耗异常（如单日 > 阈值）则提醒用户
```

| 场景 | 推荐方式 |
|---|---|
| 固定时间日报 | Cron |
| token 异常监控 | HEARTBEAT |
| 临时查询 | 手动一句话 |

## 工作流

### Step 1: 定位技能与数据目录

1. **定位脚本**：`scripts/usage-report.py`（技能目录内；若缺失，提示用户从 GitHub 仓库获取或重新安装技能）
2. **检测 state 目录**（按顺序）：
   - `--state <路径>` 参数（用户显式指定）
   - `OPENCLAW_STATE` 环境变量
   - 自动检测（Windows 小遥Claw：`C:\Users\<user>\AppData\Roaming\xiaoyaoclaw-desktop\runtime\openclaw\state`）
   - 找不到 → 报告用户，请其确认 OpenClaw state 路径，**不猜测不硬编码**

### Step 2: 解析 session JSONL，输出报告

运行脚本（默认今日，全维度）：

```bash
python <skills>/xiaoyaoclaw-usage-report/scripts/usage-report.py --today
```

> ⏱️ **时间窗 = 硬边界**：不给 `--today` / `--week` / `--all` 时默认按**今天**统计（不会扫全历史）；
> 选定窗口后所有维度只统计窗口内事件，窗口外历史数据不参与任何聚合。

输出维度：
1. 总览：任务数、总 token(input+output)、总耗时
2. 按 agent/模型：调用次数、输入/输出 token、模型总耗时/平均（近似）
3. 按工具：次数、失败数、总耗时、平均、最慢
4. Skills 使用：技能名、读取次数、使用 agent
5. 任务排行：按活跃耗时（排除用户思考间隔）
6. 每日趋势：每日输入/输出 token、调用数

### Step 3: 按需过滤（对话追问）

用户继续追问时，用对应参数缩小范围：

| 用户问 | 命令 |
|---|---|
| 「近 7 天」 | `--week` |
| 「全部历史」 | `--all`（**显式传参**；窗口外数据默认不进任何聚合） |
| 「某某 agent 花了多少」 | `--agent <name>` |
| 「哪个工具最慢」 | `--by-tool` |
| 「用了哪些技能」 | `--skills` |
| 「导出 JSON」 | `--today --json`（默认仅聚合统计） |
| 「要 session 级明细」 | `--today --json --include-sessions`（含 session 标识/时间戳，属敏感运维元数据，提醒勿公开分享） |
| 「要看完整数据目录路径」 | 加 `--include-paths`（默认脱敏为末两级目录） |

### Step 4: 汇报结果

把脚本输出整理为清晰报告发给用户；按工具耗时排行指出瓶颈、按 agent 对账 token 消耗、按技能使用盘点闲置项——**只报告统计结论，不引用任何会话内容原文**。
报告首部会打印实际使用的数据目录与输出范围；JSON 默认只出聚合统计，session 级明细需显式 `--include-sessions`，输出前提醒用户勿公开分享。

## 统计口径（务必遵守，直接决定报告准确性）

- **token 真实消耗 = input + output**（totalTokens 含 cacheRead 每轮重复计数，禁用；实测虚高 1.3x~14x+，单条最高 568x）
- **工具耗时 = toolResult.ts − assistant(toolCall).ts**（含模型生成 toolCall 的决策时间，非纯执行时间）
- **模型耗时 = 近似估算**（事件顶层 ts 间隔，cap 10min；⚠️ 不能用 message.timestamp，那是批量写入时间戳；精确值在 OpenClaw diagnostics-otel 事件层）
- **不做成本估算**：脚本**不读取、不计算、不输出任何 cost 字段**（文档 / 报告 / JSON 口径完全一致）；各供应商定价不同且随时变动，token 才是通用主指标；用户需要成本时，引导其按 token × 单价自行换算
- **skills 仅统计被 read 加载过的**（metadata 注入未加载的不计）
- **时间窗 = 硬边界**：所有聚合都只基于**窗口内**事件（agent/模型、工具、技能、每日趋势、任务一律如此）；不指定时默认「今天」，不会扫全历史；`--all` 只统计全历史且必须显式传参；跨窗口的长会话按窗口内部分截断

## 安全红线

1. **只读**：本技能只解析 session JSONL 做统计聚合，**不修改、不删除、不写入任何文件**（无 `--write` 类选项）
2. **数据不出机器**：纯本地解析，无外部服务、无网络请求、无数据上传
3. **不泄露会话内容**：只输出聚合统计（耗时/token 数/次数），**绝不引用或复述会话原文**；session JSONL 含个人数据，统计口径之外的内容一律不外泄
4. **不读写配置文件**：不读取、不修改 `openclaw.json` 等任何配置文件；数据目录解析顺序固定为 `--state` 参数 → `OPENCLAW_STATE` 环境变量（**本技能唯一读取的环境变量**）→ 桌面版（小遥Claw）默认路径（`%APPDATA%\xiaoyaoclaw-desktop\runtime\openclaw\state`）；**报告首部会打印实际使用的目录，但默认脱敏为末两级**（如 `…/openclaw/state`），完整本机路径需显式 `--include-paths`；找不到就询问用户，不猜测
5. **零依赖**：仅 Python 3.8+ 标准库；不安装任何第三方包
6. **不做成本估算**：脚本完全不读取、不计算、不输出 cost 字段（与文档口径一致），只报 token
7. **cron 日报由用户决定**：不主动创建定时任务，用户明确要求并确认后才提供/添加配置
8. **输出最小化**：默认只输出聚合统计（次数/耗时/token/工具/模型/技能名）——**不含会话内容原文、不含 session id、不含本机绝对路径**（路径默认脱敏为末两级，完整路径需 `--include-paths`）；JSON 的 session 级明细须显式 `--include-sessions`，属敏感运维元数据，须提醒用户勿公开分享
9. **零网络**：运行时脚本只用 Python 标准库读本地文件，无网络请求、无外部服务调用；文档中的 GitHub / 官网链接仅供人类阅读，不参与技能运行
10. **时间窗不越界**：选定时间窗后，脚本**不读取窗口外的数据去参与统计**——遍历到窗口外事件即丢弃，不进入任何聚合、也不出现在输出（默认时间窗 = 今天；`--all` 须显式传参）

## 完整示例

### 场景 A：今日用量报告（手动）

用户说「跑今日用量报告」→ 定位技能 + 检测 state 目录 → `--today` 解析 → 输出总览（任务数/token/耗时）+ agent×模型表 + 工具耗时排行 + 技能使用 + 每日趋势 → 汇报瓶颈与对账结论。

### 场景 B：对话追问

用户说「哪个工具最慢」→ `--by-tool` → 汇报最慢工具及耗时，建议优先优化 → 用户说「xiaoxia 今天花了多少 token」→ `--agent xiaoxia` → 汇报该 agent 调用次数与 input/output token。

### 场景 C：cron 每日日报

用户说「配置每天 22:00 自动推送用量报告」→ 提供 cron 配置示例（agentTurn + announce）→ 用户自行在 OpenClaw 添加 → 之后每天定时收到日报。

## 权限与输出字段（透明声明）

| 能力 | 具体内容 |
|---|---|
| 读 | OpenClaw state 目录下 `agents/*/sessions/*.jsonl`（会话事件日志）——只读解析，产出聚合统计 |
| 写 | **无**——不创建、不修改、不删除任何文件 |
| 网络 | **无**——不使用任何网络能力 |
| 环境变量 | 仅 `OPENCLAW_STATE`（可选；未指定 `--state` 时用于定位数据目录），不读取其他环境变量 |
| 配置文件 | **不读不写** `openclaw.json` 等任何配置文件 |
| 时间窗 | **硬边界**——按所选窗口（`--today` / `--week`，默认「今天」）过滤事件；窗口外数据不参与任何聚合，全历史须显式 `--all` |

**默认输出字段**（脱敏口径）：时间范围、数据目录（脱敏末两级）、agent 过滤、任务数；按 agent/模型：调用次数 + 输入/输出 token + 模型耗时；按工具：次数/失败/总耗时/平均/最慢；skills：技能名/读取次数/agent；任务排行：agent/活跃耗时/窗口耗时/模型耗时/token/消息数/模型名（**任务级明细需显式 `--include-sessions`**）；每日趋势：日期/输入输出 token/调用数。**不含**会话内容原文、session id、本机绝对路径。

**`--agent <name>` 的口径**：按 agent 过滤时，工具与技能维度的次数/耗时/失败数**按该 agent 重新计算**，不把「别的 agent 也在用」的工具、技能的合并计数和他人名字带出来——单 agent 报告只反映该 agent 自己的活动。

**所有字段都只统计所选时间窗内的事件**（窗口即边界）；JSON 的 `meta.window` / `meta.window_scoped` / `meta.window_start` / `meta.window_end` 声明本次输出的窗口（`--all` 时 start/end 为 `null`）。

**`--include-sessions` 追加字段**（显式开启，输出前会打印敏感告警）：`agent` / `id`（session id）/ `start` / `end` / `duration_ms` / `active_ms` / `model_ms` / `models` / `tokens` / `tools` / `msgs`。

**`--include-paths` 追加字段**：`meta.state_dir` 与报告首部的数据目录显示为完整本机路径（默认脱敏为末两级）。

## 姊妹项目

> 以下链接**仅供人类阅读**（文档/社区参考）；本技能运行时零网络请求，不访问任何链接。

- 🏠 **xiaoyaoclaw-workspace-initializer**（工作区初始化器）：管 agent 的「家」——目录结构 + WORKSPACE.md 规范 + 多 agent 配置安全。<https://github.com/dtsola/xiaoyaoclaw-workspace-initializer>
- 🧠 **xiaoyaoclaw-memory-distill**（记忆整理）：把对话蒸馏成结构化记忆，解决上下文溢出。<https://github.com/dtsola/xiaoyaoclaw-memory-distill>
- 🗂️ **xiaoyaoclaw-task-progress-tracker**（任务进度跟踪器）：tasks/ 与 projects/ 生命周期管理。<https://github.com/dtsola/xiaoyaoclaw-task-progress-tracker>
- 📚 **xiaoyaoclaw-kb-retriever**（知识库检索器）：本地知识库检索，分层索引 + 渐进检索。<https://github.com/dtsola/xiaoyaoclaw-kb-retriever>
- 🩹 **xiaoyaoclaw-workspace-auditor**（工作区体检）：只读审计工作区健康度，永不改文件。<https://github.com/dtsola/xiaoyaoclaw-workspace-auditor>
- 📎 **xiaoyaoclaw-web-clipper**（网页剪藏）：任意网页 → 本地 Markdown，直通知识库。<https://github.com/dtsola/xiaoyaoclaw-web-clipper>
- 🤝 **xiaoyaoclaw-agent-orchestrator**（Agent 协作编排）：拆任务、分 agent、管进度、聚结果。<https://github.com/dtsola/xiaoyaoclaw-agent-orchestrator>
