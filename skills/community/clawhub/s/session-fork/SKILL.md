---
name: session-fork
slug: session-fork
displayName: 会话分叉（打分支）
display_name: 会话分叉（打分支）
display_name_en: Session Fork
description: Duplicate any work-in-progress into an independent branch — not just conversations, but tasks, plans, code, writing and research. Context, confirmed conclusions, completed steps and tool results all come along; resume from any point while the original line stays untouched and keeps running. Note that a fork copies the session context only; workspace artifacts are not rolled back — unless they are version-controlled (e.g. git), only their final state exists.
description_zh: 把走到一半的工作整体复制成独立分支——上下文、已确认的结论、做过的步骤、工具结果都跟着走，从任意节点接着推进，原线不受影响。不只是对话：任务、方案、代码、写作、调研都能分叉（如「这条方向走岔了，回到上一轮重新来」「同一个任务并行试几条路」）。注意：分叉复制的是会话上下文，工作区产物不会跟着回退——除非产物自身有版本记录（如 git），否则只有当前最终态。
description_en: Duplicate any work-in-progress into an independent branch — not just conversations, but tasks, plans, code, writing and research. Context, confirmed conclusions, completed steps and tool results all come along; resume from any point while the original line stays untouched and keeps running. Note that a fork copies the session context only; workspace artifacts are not rolled back — unless they are version-controlled (e.g. git), only their final state exists.
version: 2.4.23
author: OfferKuai (Offer快) Team
license: MIT
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
metadata: {"openclaw":{"emoji":"🔀","requires":{"anyBins":["python3","python","py"]}}}
tags: [workbuddy, claude-code, codex, hermes, openclaw, pi-coding-agent, session, fork, conversation, task, 会话分叉, 打分支, 任务分叉, 并行探索, 办公效率, 会话管理, 对话管理, 效率]
agent_created: true
---

<h1><img src="https://raw.githubusercontent.com/yamingmou/session-fork-core/main/logo.png" width="40" height="40" alt="Fork Logo" style="vertical-align: middle;"> Session Fork（会话分叉 · 打分支）</h1>

**语言 / Language** — 本技能面向中文用户编写。英文总览见 [README.en.md](https://github.com/yamingmou/session-fork-core/blob/main/README.en.md)；中文总览见 [README.md](https://github.com/yamingmou/session-fork-core/blob/main/README.md)。
*Written in Chinese. For an English overview see the linked README.en.md.*

把一个会话的**工作现场整体复制**成独立分支：取源会话 transcript 的前 1..截断点行 → 递归改写其中的会话 id → 写入新会话文件 → 在会话索引与谱系索引注册。原会话零改动。

- **分叉对象 = 工作现场**（上下文 + 已确认结论 + 已做步骤 + 工具结果），**不是"聊天记录"**。因此对话、**任务**、方案、代码、写作、调研都可以分叉——用户说"把这个任务分个支""同一个任务并行试几条路"同样属于本技能职责。
- **它替你省下的（一句话）**：不用重讲一遍背景、不用重跑一遍前面的步骤，原线也不会被带偏。
- **默认行为**：截断点 = 上一轮输出的结束；用户一旦给出断点信息，必须改用 `--match` / `--line` / `--request-id`（见「工作流程 · Step 2」）。

## ⚠️ 分叉边界：上下文会回去，产物不一定（必读）

**分叉自由，产物不自由。** 分叉复制的是**会话的工作现场**（transcript 的 `1..截断点` 前缀，含工具结果的**记录文本**，不是把工具重跑一遍），外加会话索引 / 谱系登记——**它不复制、也不回退工作区文件，更不撤销任何已经发生的外部动作**。

所以分支落地后可能出现这种错位：**分支里的上下文停在切点，而磁盘上的产物已经是"现在"的样子（最终态）**。产物能不能跟着回到那一刻，取决于它自己有没有版本记录：

| 产物形态 | 能否回到那一刻 | 怎么做 |
|---|---|---|
| 在 git 仓库里（已提交） | ✅ 能 | 分支侧 `git switch -c <名> <sha>` 或 `git worktree add <目录> <sha>`，把工作区切到与切点对应的提交，上下文与产物重新对齐 |
| 有版本记录的载体（云文档版本历史、系统快照 / Time Machine、备份、日志） | ✅ 通常能 | 手动回溯到对应时间点 |
| 无任何版本记录的本地文件 | ❌ 只有最终态 | 分叉给到的是「旧上下文 + 新文件」；需要旧版本只能事先备份 |
| 已发生的外部副作用（发出的消息 / 邮件、已发布页面、已 push 的提交、API 写入、装好的依赖） | ❌ 不可撤销 | 分叉不能取消已发生的事，需在外部自行补救 |

**打分支时的约定（每次都要执行）：**

1. **每次打分支都用一句话交代边界**（一句话即可，不要长篇）：分叉的是会话上下文；工作区文件不会跟着回退，除非它在 git 等有版本记录的载体里。**不得**任何措辞暗示分叉能"时光倒流"；没把握时宁可说得保守。
2. **动手前看一眼工作目录**（一条命令的事）：
   - `git rev-parse --show-toplevel` 成功 → 是仓库：报告当前 `HEAD`（短 sha + 提交主题）并告知"分支侧可用 `git worktree` 对齐到切点"；若 `git status --porcelain` 非空，**明确提示这些未提交改动不会被分叉带走**；
   - 失败/非仓库 → 明确告知**该目录下的文件只有当前最终态，分叉无法回退它们**。
3. **用户真实意图是"回到旧产物"（而不只是"从旧上下文继续"）时，不要只打一个会话分支了事**——先建议（用户同意后执行）git 检查点（`commit` / `stash`）或文件备份，再分叉。
4. 分支是**快照**：分叉点之后原会话新增的消息不会进分支——这是设计行为，向用户说明时不要误称为"丢数据"。

## 功能特性

- **零配置默认模式**：用户只说"打分支"即可，截断点自动 = 上一轮对话的输出结束，无需提供任何拆分点文本；
- **精确指定模式**：按用户引用的某条回复特征文本（`--match`）、行号（`--line`）或请求ID（`--request-id`）截断；
- **存储级复制**：新 jsonl 文件 + 会话索引新行记录，不是"链接/指向"——原会话后续写入不会污染分支；
- **谱系可追溯**：`parent_id` + `at_seq`（快照点）记录分支从哪派生，`--list --tree` 展示分叉树；
- **快照点可回**：分支可再派生（从分支再 fork = 新投影继续演进）；
- **内置安全**：执行前自动备份（仅源 jsonl），递归 id 替换（rawContent/rawResponse 等原始内容黑名单不碰），自带完整性校验；
- **可预览**：`--dry-run` 先确认截断点定位，再正式执行。

## 实现结构（通用引擎）

脚本基于 **fork-core 通用引擎 + 产品 adapter** 设计（实现细节，不影响使用）：

```
session-fork/
├── SKILL.md                    # 技能定义
├── scripts/
│   └── create_branch.py        # 唯一入口（调用它即可）
├── fork_core/                  # 通用引擎（与产品无关）
│   ├── engine.py               # 截断点定位/截取/备份/验证/汇报
│   ├── models.py               # SessionMeta / ForkResult 契约
│   ├── cli.py                  # 命令行解析与输出
│   ├── adapters.py             # adapter 注册表（工厂）
│   ├── adapter_base.py         # TranscriptionAdapter 接口
│   ├── adapter_workbuddy.py         # WorkBuddy（默认）
│   ├── adapter_claude_code.py       # Claude Code
│   ├── adapter_codex.py             # Codex
│   ├── adapter_hermes.py            # Hermes
│   ├── adapter_pi.py                # pi
│   ├── adapter_openclaw.py          # OpenClaw ≤2026.6.x（JSONL 后端）
│   └── adapter_openclaw_sqlite.py   # OpenClaw ≥2026.9.x（SQLite 后端）
└── tests/                      # 自测（仅源码仓库有；安装包里不含）
```

- 核心逻辑（默认/--match/--line/--request-id 定位、结构化 id 替换、完整性校验）全部在引擎层，与存储格式无关；
- 每个产品只实现一个 adapter（接口组：定位/消息判定/读写/注册/文案/体检），格式差异被完全隔离；
- 未来新增产品支持 = 新增一个 adapter 文件，引擎零改动（旧 adapter 亦无需改动，走基类默认实现）。

## 触发条件

用户**明确要求创建/执行**"打分支 / 会话分叉 / 对话分支 / **任务分叉** / 复制对话成新分支 / **把任务复制成新分支** / **同一个任务并行试几条路** / 分支会话 / split session / fork session / branch this task / 新建分支 / 从这里分叉"。

**只需记住这一条（其余交给工具）：**
> **没贴 conversation ID → 打当前对话的分支；贴了 conversation ID（"复制请求 ID"的 JSON）→ 打那个对话的分支。**

- **默认**：用户只说"打分支"或"打分支，命名『X』"（没贴任何 ID）——源会话 = 当前对话，截断点 = 上一轮对话输出结束。
- **从某条回复打**：用户贴了复制的 ID（可能来自本对话或任何其他对话），或说了"从『XXX』那条回复打"——按用户给的信息定位源会话和断点。
- **命令映射**（按用户给的信息直接判断，不把选择抛给用户）：

> **怎么选 flag（一句话口诀）**：
> **用户贴了 ID** → 用 `--request-id`（和 `--session` 一起）；
> **用户只是在说文字**（哪怕他说的是"那条**回复**"）→ 用 **`--match "<那段文字>"`**。
> ⚠️ `--request-id` **只能装 ID**，不能装文字。
>
> ✅ **本条消息里出现 `conversationRequestId` ⇒ 工具会自动按它切**（默认模式即可，**不必**再手工拼 `--request-id`）：
> 输出第一行与 `Split :` 行都会写明「已按它切在 Lx（默认本会是 Ly）」，并给出反向逃生口 `--line Ly`。
> 想显式表达（更稳妥、也便于回读）：把它传进 `--request-id`，`conversationId` 给 `--session`。
> ⚠️ 若你要的**确实是默认切点**，用 `--line <提示里给出的行号>` 覆盖。
> （历史：v2.4.22 曾把这种情形做成「拒绝执行」，实测执行方不照抄报错里的命令、转而猜位置 ⇒ 改成现在的**采用并明示**。）

> **⚠️ 动手前先做这一件事**：下面的命令**统一写成 `fork …`**（你已用 pip 装了本工具）。**若你是把本技能装进了某个产品的 skills 目录**（ClawHub 等），把 `fork` 换成 `python3 <该技能目录>/scripts/create_branch.py`——**参数完全相同**。

| 用户给了什么 | 用什么命令 |
|---|---|
| 什么都没贴（当前对话） | `fork --adapter <你的产品> --session current`（默认截断点） |
| @引用了一段内容（long-text quote）说打分支 | 从引用 JSON 提取 id（格式 `<sessionId>-<requestId>`，如 `"ec48e1ae-…-e683a22a…"`）→ `fork --adapter <你的产品> --session <sessionId> --request-id <requestId>` |
| 贴完整 JSON（conversationId + conversationRequestId） | `fork --adapter <你的产品> --session <conversationId> --request-id <conversationRequestId>`（conversationId = 会话 ID，直接定位） |
| 只贴了 conversationRequestId / traceId | `fork --adapter <你的产品> --request-id <id>`（自动反查该 ID 所属会话，跨工作区） |
| 说了文本/行号 | `fork --adapter <你的产品> --session current --match "XXX"` 或 `--line N` |
| **只是在聊天里"提到"某段文字**（没有复制任何 ID） | 同上：`--match "<那段文字>"` ⚠️ **不要**把它当 `--session`，也**不要**自己造一个 `--request-id` |

> **⚠️ 关键规则**：用户给了**任何形式的引用**（@long-text 引用 / 复制的请求 ID JSON / 纯 requestId / 指向别处的会话内容）→ **源会话 = 引用所指的那个会话，不要默认用 `--session current` 打当前对话**。识别引用 ID：JSON 里找 `conversationId`，或 @引用内容里找 `"id": "<sessionId>-<requestId>"` 双段拼接格式。拿不准时先 `--dry-run` 展示将要打源会话名 + 断点，问用户确认再正式执行——**不要反复试错创建分支**。

> **⚠️ 三个最常见的错误**：
> ① **把"用户口头提到的文字"当成会话 ID**：用户说"从『teal』那条回复打分支"→ 用 `--match "teal"`，**不是** `--session teal`；
> ② **自己造 `--request-id`**：用户没贴任何 ID 时，本来就**没有** request-id 可用；"某段文字"要放进 **`--match`**，**不是** `--request-id`；
> ③ **命令入口写错产品**：在 WorkBuddy 里不要输出裸 `fork …`（要写完整路径）；在 pip 渠道**不要**输出 `~/.workbuddy/skills/…`（那台机器上没有这个路径）。入口按「**Step 0**」定。

**命令示例**（左边是用户的话，右边是完整命令；前缀按 Step 0 替换）：

| 用户这么说 | 对应命令 |
|---|---|
| 打分支，命名『论文讨论』 | `fork --adapter <你的产品> --session current --name "论文讨论"` |
| 从『teal』那条回复开始打分支 | `fork --adapter <你的产品> --session current --match "teal"` |
| 打分支，从第 6 行截断 | `fork --adapter <你的产品> --session current --line 6` |
| （贴了 conversationId + conversationRequestId） | `fork --adapter <你的产品> --session "<conversationId>" --request-id "<conversationRequestId>"` |

### 排除（不触发执行，只回答问题）

以下场景用户只是**咨询/了解**，不应执行分叉操作：

- "什么是分叉 / 分叉有什么用 / 怎么用分叉功能" → 解释功能，不执行
- "帮我看看当前有没有分支 / 列出分支" → 用 `--list` 查询，不创建
- "这个对话太长了" / "对话需要整理" → 不自动推断要分叉，询问用户意图
- "能不能回到之前的某个点" → 解释可以用分叉实现，询问是否执行
- 用户在讨论分叉的概念/原理/对比 → 只回答，不执行

## 工作流程

### Step 0 — 先判定"你在哪个产品里"（决定命令入口，不要写死）

本技能在 **6 个产品**可用，但**命令入口不一样**。动手前先定下来你是哪一种，再照后面的示例写命令：

| 你在哪 | 命令入口 |
|---|---|

| **其他产品的技能目录**（如从 ClawHub 装进该产品的 skills 目录） | `python3 <该技能目录>/scripts/create_branch.py <参数>` |
| **pip 安装的命令行**（Claude Code / Codex / Hermes / pi / OpenClaw 在终端里的路径） | `fork <参数>` |

**判定顺序（30 秒内定下来，不要猜、不要两套都试）**：

1. `fork --version` 能跑通 → 用 **`fork`**；
2. 否则 `ls -d ~/.workbuddy/skills/session-fork*/ 2>/dev/null | head -1` **有命中、且该目录下 `scripts/create_branch.py` 存在** → 用 **WorkBuddy 形式**（真入口 = `${SK}/scripts/create_branch.py`，见上文取法；⚠️ 目录名可能带市场后缀 `__skillhub`，**不要**写死成 `session-fork/`）；
3. 否则看你所在产品的 skills 目录里有没有本技能；
4. 都不确定 → **问用户一句**："你是在 WorkBuddy 里用，还是本机命令行（pip 装的）？"

**adapter 对应**：WorkBuddy 是默认（不写 `--adapter`）；其余五种**必须写** —— `--adapter claude-code` / `codex` / `hermes` / `pi` / `openclaw`。

### Step 0.5 — 平台差异（决定「命令怎么写」）

**先判平台**：`uname` 能跑 → **macOS / Linux / WSL**（POSIX，本文其余命令直接可用，无需替换）；报"不是内部或外部命令" → 你在**原生 Windows**，按下表换写法。

| 用途 | POSIX（macOS / Linux / WSL） | 原生 Windows（PowerShell / CMD） |
|---|---|---|
| 跑入口 | `python3 "<技能目录>/scripts/create_branch.py"` | `py -3 "<技能目录>\scripts\create_branch.py"` |
| 取技能目录 | `SK=$(ls -d ~/.workbuddy/skills/session-fork*/ \| head -1)` | `$SK=(Get-ChildItem "$env:USERPROFILE\.workbuddy\skills" -Dir -Filter "session-fork*")[0].FullName` |
| 家目录 | `~` / `$HOME` | `$env:USERPROFILE`（PS）· `%USERPROFILE%`（CMD） |
| 设环境变量 | `export CODEX_HOME=/x` | PS `$env:CODEX_HOME="C:\x"` · CMD `set CODEX_HOME=C:\x` |
| 查文件内容 | `grep -n "词" f.jsonl` | PS `Select-String -Path f.jsonl -Pattern "词"` · CMD `findstr /n "词" f.jsonl` |
| 设文件只读 | `chmod 444 f` | `attrib +R f` |

**Windows 上的四个坑**（均有官方依据）：

1. **`python3` 不保证存在** —— Python 官方把它定位为"捕获 POSIX 习惯误用"的兼容命令，**不推荐使用** ⇒ 优先 **`py -3`**，其次 `python`。
2. **`python` 可能被 Microsoft Store 应用别名拦截**（敲了没反应、或弹出商店）⇒ 同样优先 `py -3`。
3. **PowerShell 执行策略**可能拦住全局 npm 装的 CLI（报 `npm.ps1 cannot be loaded because running scripts is disabled`）。修法是**用户自行**执行 `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` —— **本技能不会替你改系统设置**。
4. **WSL 与原生 Windows 的会话库互不共享**（`/home/u/.codex` ↔ `C:\Users\u\.codex`）—— 你在哪边跑，就用哪边的库。

> **目录位置两平台同构**（`~/.claude` ↔ `%USERPROFILE%\.claude`；`~/.codex` ↔ `%USERPROFILE%\.codex`）⇒ **`--adapter` 与其余参数完全一致**，平台差异只在"命令怎么写"。
> **输出编码**：本技能的 CLI 会自动把 stdout 固定为 UTF-8（**仅当当前编码容纳不了中文/emoji 时**），所以 Windows 上中文与 emoji 都能正常输出，不需要你额外设环境变量。若你的控制台仍显示乱码，那是控制台自身的代码页问题——`chcp 65001` 切到 UTF-8 即可。

### 分支怎么出现（**按产品**，与工具输出一致；不要凭记忆）

脚本创建后会在输出里给一行 `ACTION : 分支已创建——…`，那句话是**按产品适配**的。**照它转述给用户**；下表是同一份内容的备查（有反直觉项，不要凭印象）：

| 产品 | 怎么看到分支 |
|---|---|

| **Claude Code** | 在终端重跑 `claude`，用 **`/resume`** 选择该会话（**无需重启其他程序**） |
| **Codex** | ① 可直接续跑：`codex exec resume <新 id> "…"`；② **桌面版会话列表也要重启才可见**（macOS ⌘Q / Windows 托盘退出）；③ 想被 `codex fork --last` 选中，用 `codex exec resume` 跑一轮 |
| **Hermes** | **无需重启、无需修复命令**：`hermes sessions list` 即可看到；`hermes chat --resume <分支 id>` 续跑 |
| **pi** | **无需重启**：会话选择器（`/resume`）或 `/tree` 刷新即可 |
| **OpenClaw** | `openclaw sessions --json` **立即可列出**；若 Gateway 正在运行，重启一次以加载 |

**与你有关的唯一一条**：`--fix` 只支持 WorkBuddy（其他 adapter 会直接报错）；界面按钮 / 重启客户端 / `.workbuddy/` 日志那几条与你无关。

### Step 1 — 确认源会话

按上表映射，先看用户贴了什么：
- 什么都没贴 → `--session current`（当前对话，脚本自己判定，含义见下）；
- 贴了**完整 JSON**（UI 复制请求 ID 的原始格式）→ 取 `conversationId` 作为源会话（WorkBuddy / Claude Code 这类按 id 命名的存储里，conversationId 就是会话文件名，直接定位、不扫描；其他产品交给引擎按 id 定位）；`conversationRequestId` 作为断点；
- 贴了**纯 requestId/traceId**（无 conversationId）→ 用 `--request-id` 自动反查该 ID 属于哪个会话（跨工作区兜底，按 mtime 新→旧搜）。
- **`--session current` 的含义**：**你正在其中的这个对话**。唯一判据 = 执行环境里的会话标识（`CLAUDE_SESSION_ID` / `CODEBUDDY_SESSION_ID` / `BAGGAGE`）；其他产品由各自 adapter 定义。**不需要自己去翻数据库找"当前会话"**——交给 `--session current`。
- **⚠️ `current` 不猜**：拿不到会话标识时脚本**硬失败**，不会替你选一个"最近活跃的会话"。那**不是**你正在其中的对话，打出来会是**另一个对话的分支**。确实想从"最近活跃的会话"打时，用**显式**的 `--session latest-working`（语义即其名）。

**会话存在哪，不用你记**：各产品的目录与格式不同（JSONL 与 SQLite 都有），**由 adapter 自动探测**：

  - **其他产品**：**由 adapter 自动探测**——Claude Code / Codex / Hermes / pi / OpenClaw 的目录与格式各不相同（JSONL 与 SQLite 都有）。需要覆盖位置时用环境变量（如 `CODEX_HOME` / `HERMES_HOME`），**不要手改会话文件**。

### Step 2 — 确认截断点（默认规则优先）

**⚠️ 最高优先级规则：用户说了断点 → 必须用 `--match` 或 `--line`，不要用默认模式。**

默认模式只在用户**完全没提断点**（只说"打分支"）时才用。一旦用户描述了任何断点信息（"截断到 XXX"、"从 XXX 之前分叉"、"到 XXX 产生处"），就必须用指定模式。

**三种场景的处理方式：**

| 用户说的 | 用什么 | 怎么做 |
|---|---|---|
| "打分支"（没提断点） | 默认模式 | 脚本自动定位最后一条 assistant 回复 |
| "截断到这条回复" + 提供了请求ID | `--request-id` | **最精确**，直接匹配 conversationRequestId |
| "截断到 XXX" | `--match "XXX"` | 取最后一条包含 XXX 的 assistant 回复 |
| "截断到 XXX 产生处" | `--line N` | 先用 grep/Read 在源会话 jsonl 中搜索 XXX 所在行号，再用 `--line` |

**⚠️ 最精确的截断点 = 请求ID（`--request-id`）——但"怎么拿到它"只有 WorkBuddy 有现成按钮：**

- **其他产品**：**没有这个按钮**（不要教用户去找）——让用户用**文字**（`--match "那段文字"`）或**行号**（`--line N`）指定断点；若用户贴了含 `conversationId` / `requestId` 的 JSON，照样可用 `--request-id`。

**⚠️ 关键：当用户口头描述断点但没给精确文本时（如"截断到项目思维规则模板产生处"），必须先在源会话 jsonl 中搜索确认行号，然后用 `--line`，不要忽略断点用默认模式。**

**断点定位步骤（指定模式）：**
1. 在源会话 jsonl 中搜索用户描述的关键词（`grep -n "关键词" <session-id>.jsonl`）；
2. 确认匹配行是 assistant 消息且有 output_text（必须是完整回复，下一行是 user 消息或 EOF）；
3. 用 `--line N` 或 `--match "精确文本"` 截断；
4. 跑 `--dry-run` 验证定位正确后，再正式执行。

**默认模式规则（仅当用户完全没提断点时）：**
- **会话内打分支**（你自己就是执行者，脚本跑在被 fork 的那个会话里）：
  截断点 = **上一轮对话的输出结束**（用户最后一条 user 消息之前的最后一条完整 assistant 回复）。
  本轮"打分支"这条指令与你此刻的叙述**都不进分支**。
- **从外部打分支**（人在终端执行、或显式指定另一个会话）：截断点 = **整份复制**到文件末尾最后一条完整 assistant 回复（此时没有"本轮"要排除）。
- 两种语义由脚本按"执行环境里有没有本次会话的标识"自动判定，**不需要你指定**；
  `--dry-run` 会打印走了哪一种（`in-session` / `whole`）以及锚在哪一行、锚点原文是什么——**照它核一遍再正式执行**。
- 要覆盖判定结果，只在会话内才需要：加 **`--whole`** 强制整份复制。

### Step 3 — 执行创建（用脚本，不要手写）

**打分支的固定顺序（脚本已内置，不要绕过或手写等价流程）：**

1. 写入 `.tmp` 文件（零外部可见副作用）
2. **立即自检**（校验磁盘上的字节，不是内存数据）
3. 自检通过才 `os.replace` 到正式路径（原子落位）
4. 最后登记 db 与谱系

自检失败 = **什么都没发生**（只留可忽略的 .tmp）；登记失败 = 干净回退（文件回滚 + 痕迹清除）。
**不要**「先落 db 再验证」——那会让坏分支出现在侧边栏。
dry-run 也走完整校验（会真写 .tmp + 自检，只是不落位/不登记）——`Verify: OK` 才是真 OK。

**执行方式：只用这一条命令**（不需要 pip、不依赖 cwd，整行复制即可用）：

- **其他产品的技能目录**：`python3 <该技能目录>/scripts/create_branch.py <参数>`
- **pip 命令行**：`fork <参数>`

> **⚠️ 两条不要做**：① **不要把两套入口混用**（在 WorkBuddy 里不要用裸 `fork`；在 pip 渠道**不要**写 `~/.workbuddy/skills/...`——那台机器上没有）；② **不要执行 `fork_core/cli.py`**（唯一入口是 `scripts/create_branch.py`）。

> 下面示例统一写 `fork` 形式；若你用技能目录入口，把 `fork` 换成 `python3 <该技能目录>/scripts/create_branch.py`。

```bash
# 场景 1：当前对话打分支（用户没贴任何 ID）
fork --adapter <你的产品> --session current --name "<分支名>"                 # 默认截断到上一轮输出结束
fork --adapter <你的产品> --session current --match "<拆分点特征文本>"          # 从当前对话某条回复打

# 场景 2：从贴的 conversation ID 打（用户贴了"复制请求 ID"，可能来自任何对话/工作区）
fork --adapter <你的产品> --session "<conversationId>" --request-id "<conversationRequestId>" --name "<分支名>"
#   ↑ conversationId 即 UI 复制 JSON 里的 conversationId（= 源会话 ID），直接定位
# 只拿到 requestId/traceId 时：自动反查所属会话（无需 --session）
fork --adapter <你的产品> --request-id "<conversationRequestId>" --name "<分支名>"

# 运维类
fork --adapter <你的产品> --list                                        # 查询分支
fork --fix <分支会话ID>                              # 修复被追加消息的分支（仅 workbuddy）
fork --adapter <你的产品> --verify                                      # 本机会话库自检（环境变化或换机器后建议跑一次），别名 --doctor
fork --session current --adapter pi                # pi
fork --session current --adapter claude-code       # Claude Code
fork --session current --adapter codex             # Codex
fork --session current --adapter hermes            # Hermes
fork --session current --adapter openclaw          # OpenClaw（≤2026.6.x / ≥2026.9.x 自动识别后端）
# OpenClaw 后端也可强制：FORK_OPENCLAW_BACKEND=jsonl|sqlite（默认 auto）
```

**执行规范**：
- **先交代产物边界 + 看一眼工作目录的 git 状态**（见「分叉边界 · 打分支时的约定」第 1/2 条）——这一步在**创建之前**做，不要等到用户发现产物没跟着回退才解释；
- **⚠️ 回读 `Source` 行（必做）**：脚本输出的第一行是
  `Source   : <会话id>  「<会话名>」`
  **先确认这个源会话就是你（和用户）所在的那个对话**。父 id 对不上时肉眼看不出来，**名字**能一眼看出来。不一致 → **立即停手**，把"你在的对话 / 实际被当成源会话的对话"两个名字摆给用户，问清要哪条；**不要继续，更不要交付一个"来历正确但对话不对"的分支**；
- **先 `--dry-run` 确认截断点，再正式执行**（推荐，防打错位置）；
- **`fork --adapter <你的产品> --verify` 自检**：环境变化或换机器后建议跑一次；打分支前也可以先跑。输出分三档：
  - **`❌ 失败` = 要修**（前缀内残留 / 结构性 `sessionId` 残留等）：以非 0 退出（表示确有需要处理的问题）；
  - **`⚠️ 需复核` = 不用修，看一眼即可**：典型情形是**你在分支里记录了血缘**（"我的父会话是谁"），
    于是 fork **之后**追加的内容里出现了父会话 id。它**不会**让体检失败、不影响退出码。
    想彻底消解就**重打一次该分支**——新分支会带上"前缀指纹"（`prefix_fp`），此后体检能证明
    "边界之内仍是 fork 原样产物"，不再提示。两处边界要知道：
    ① **追加区必须先开一轮新 user 消息**（你接着说下一句）——若紧接快照点的**不是** user 消息，
    这段按"疑似前缀残留"**从严判失败**（宁可在这一处误报，也不让真污染借"追加区"溜过）；
    ② 指纹证据**只覆盖快照点之前那 N 行**，对追加区不作任何担保，不要把它读成"整条分支都没问题"；
  - **`✅ 通过`**。
  （Claude adapter 在没有真实 CLI 会话时，这一档属预期情况）
- 脚本自动完成备份 → 截取 → 会话 id 替换 → 注册 → 校验，无需手工介入。

### Step 4 — 验证与汇报

脚本自带验证（行数/解析/sessionId 一致性/零残留/末条完整）。汇报**必须使用以下固定模板**：

```
✅ 分支创建完成

📋 分支信息
- 分支 ID：<new-session-id>
- 名称：<custom_title>
- 截断位置：第 N 行 / 共 M 行（默认模式注明"上一轮输出结束"）
- 分支行数：N 行

📦 原会话不受影响
- 源会话：<src_id>「<源会话名>」（= 你所在的那个对话，**已核对名称**）
- 原会话继续正常使用，不受影响

💡 查看新分支
- <原样复制脚本输出里那一行 `ACTION : 分支已创建——…`，它已按产品适配（逐产品要点见 Step 0「分支怎么出现」表）>

- **不要照搬 WorkBuddy 的重启说法**——你不是那个产品，分支可见方式以 `ACTION` 行为准

📌 下一步
- 按上面那条提示回到产品里打开该分支
- 或在当前对话继续（分支已独立保存，不会丢失）
```

查询分支时（`--list`）使用：

```
📂 当前工作区的分支列表
- <id> | <名称> | <状态> | <创建时间>
- ...
（共 N 个分支，无分支时提示"当前工作区暂无分支"）
```

### Step 5 — 记录（可选）

建议把分支创建记录追加到**项目自己的日志**里：新 id、行数、截断点、`custom_title`、备份路径——便于日后回溯"这个分支从哪条线分出来的"。

- **其他产品**：用它自己的记忆 / 日志约定，**不要**凭空创建 `.workbuddy/` 目录。

## 分支命名建议（可自定义）

- 分支体系用序号区分：`XX·分支A｜描述` / `分支B｜描述` / `分支C｜描述`；
- `custom_title` 建议格式：`<主题>·分支X｜<用途>`，如 `重构登录模块·分支A｜接口拆分`；
- status 一律 `terminated`（无活跃 agent 的正常终态，不影响打开查看）。

## 关键坑位

1. **用户说了断点 → 必须用 `--match` / `--line`，不要用默认模式**：默认模式只回答"这一轮之前 / 整份"两种问题，**不是**用户指定的中间位置——用它去执行"截断到 XXX 产生处"，会把**不该有的后续对话也带进分支**（事后只能用 `--fix` 修）。
2. **默认截断点是两种语义，由脚本自动判定**：
   - **会话内打分支**（最常见：你在对话里说"打分支"，由 agent 执行脚本）→ 切在**上一轮输出结束**（最后一条 user 消息的完整回复末尾）。本轮指令与叙述不进分支。
   - **从外部执行**（终端、定时任务、显式指定别家会话）→ **整份复制**到末尾最后一条完整 assistant 回复。
   - ⚠️ **不要**在会话内自己判断"上一轮结束在哪"：**本轮你自己的叙述已经在同一份文件里**，按"最后一条 assistant 文本"看，看到的必然是自己。这个判定由脚本按环境自动完成，不需要人工介入——人工判定还会随对话继续而滑动。以 `--dry-run` 打印的锚点为准（会打出行号与锚点原文）。要强制整份：`--whole`。
   - 这就是"默认模式在会话内为什么锚在上一轮结束"的原因：脚本必须先定位**最近一条 user 消息**，再取它之前的最后一条完整 assistant 回复。任何"倒扫全文件最后一条 assistant 文本"的做法，都会把本轮内容一起吞进来。
3. **嵌套字段旧 id 残留**：只改顶层 `sessionId` 不够——`output.text` / `arguments` / `argumentsDisplayText` / `toolResult.renderer.value` / `error.message` 等字段都会出现旧 id。v2.4.3 起使用**递归 id 替换**（覆盖全部可读字段，仅 rawContent/rawResponse 等原始内容黑名单不碰），且**在引擎层统一实现，所有产品一致**——一次打分支通常要改上千处，漏一处就会被体检拦下。
4. **指定模式边界**：用户引用文本可能出现在多条回复里，取最后一条；且必须确认该回复是完整收尾（下一行是 user 消息）。

6. **快照分支特性**：复制发生在读取时刻，原会话之后的新消息不会进分支——这是正常行为，不是丢数据。
7. **附属目录 tool-results/**：是运行时输出缓存，jsonl 已内嵌完整 function_call_result，分支**不需要**复制附属目录（或建空目录即可）。

8. **先备份再动手**：脚本已内置备份，不要跳过。备份默认落在你所用产品的目录里（如 `~/.claude/fork-backups`、`~/.codex/fork-backups`、`~/.hermes/fork-backups`），想统一改到别处：设环境变量 **`FORK_BACKUP_DIR`**。

## 边界

### 血缘只认谱系文件，不认转录（重要）

**fork 产物的正文里读不出"它从谁来"**——因为本引擎做的是**递归 id 替换**：被复制正文里出现的**源会话 id**，会被一并改写成**分支自己的 id**（覆盖全部可读字段，仅 `rawContent` / `rawResponse` 等原始内容黑名单不碰）。

⇒ **拿转录去证"我来自谁"必然得出错误结论**（父 id 在产物里已经被改写掉了）。
**唯一可信的出处是谱系索引**：本产品目录下的谱系文件（WorkBuddy 为 `~/.workbuddy/fork.lineage.json`）里的 `parent_id`、`at_seq`（快照点）与 `prefix_fp`（该前缀的指纹）—— `--list --tree` 读的是它。
（`at_seq` 与 `prefix_fp` 还让体检能**核对**"边界是否可信"：前 `at_seq` 行的指纹与 fork 时一致 ⇒ 那段确是复制出来的原样产物，之后的差异只可能来自 fork 之后。）

> 于是会出现这种情形：分支自己的文件里，标记全部指向**它自己**；父会话文件里，标记也只指向父、**不指向该分支**。
> **两边都只剩"自己"** ⇒ 光看转录，会得出"它来自自己"这种荒谬结论。

### 任务分支 vs 身份分化：**同一个工具，两种语义**

| | **任务分支** | **身份分化** |
|---|---|---|
| 用户意图 | 同一段经历换个窗口继续走 | **造出一个新个体** |
| 产物是什么 | 一份可继续的工作现场 | **一个成员**（有自己的身份与记忆） |
| 要多做的一件事 | 交代分支怎么打开、原线不受影响 | **提醒用户：新个体需要"自报身份" + 它自己的记忆文件** |

⚠️ **身份分化时最容易出错的一件事**：让新个体**与来源共用同一份记忆 / 档案文件** ⇒ 两边互相覆盖，**比丢记忆更糟**。
来源的记忆对新个体是"**继承来的上下文**"，不是"**它的履历**"。

- **产物边界（最重要的一条，详见上文「分叉边界」）**：分叉只复制**会话上下文**，不回退**工作区文件**与**已发生的外部副作用**。会话可以分叉到任意节点，产物则只有在**自身有版本记录**（git 提交 / 云文档版本历史 / 快照备份）时才能对齐回切点；**没有记录的就只有最终态**。因此"回到过去"这件事，上限由产物的版本记录决定，不由分叉决定。
- 本技能做的是**存储级复制**（JSONL 后端 = 新 jsonl 文件；SQLite 后端 = 库内新 session_id 的一整套行 + 会话索引记录），不是"链接/指向"——链接会让原会话后续写入污染分支，且无法表达"截断到某行为止"。
- 分支创建后如需删除，由用户决定，不擅动。
- 适配边界：**准入判据是「会话转录在静息态可表达为**有序的 JSON 条目序列**，且能独立完整表达会话」**——引擎的读/切/写建立在这个形状上；**承载介质由适配器的行存储接口决定**（v2.4.8 起，不再要求"必须是文本文件"）。
  - **已在真机 / 真库验证**：**WorkBuddy**（默认）；**pi**（用官方包造真实会话后 fork，再用官方 API 回验）。
  - **已被产品自己认下（引擎产出能被产品读取、继续使用）**：**Claude Code** · **Codex** · **Hermes** · **OpenClaw**
    - **Claude Code**：隔离 home 真机跑出会话 → 引擎 fork → **决定性自包含测试**（把源会话重命名隐藏后 `--resume` 仍能取到被复制的全部前缀消息）；并用原生 `--fork-session` 做对照裁定（复制式 + 线性化修剪 + 切点不可指定）。
    - **Codex**：真机 `codex exec` 跑出会话 → 引擎 fork（自包含：丢弃源的 `history_base` 引用）→ 产品自己读回该分支并 `resume` 成功。原生分叉是**零拷贝引用式**（只写 `history_base` 指针、不复制历史），我们的自包含方案与之并存，**两种取值产品都接受**。
    - **Hermes**：隔离 `HERMES_HOME` 真机跑出会话 → **纯 SQL** 写入 `state.db`（`sessions` + `messages` 两表）→ 产品 `sessions list` **列出该分支**、`chat --resume` **续跑并答对被复制前缀里的信息**；随后产品自己往分支追加消息（**已接管**）。**无需任何产品侧修复命令**。
    - **OpenClaw**（两世代）：
      - `≤2026.6.x`（JSONL 后端）：真机跑出会话 → 引擎 fork → 官方 CLI `openclaw sessions` 列出 → **在分支上续跑成功**。
      - `≥2026.9.x`（SQLite 后端）：转录落在 `agents/<id>/agent/openclaw-agent.sqlite` 的 `transcript_events` 表（`(session_id, seq) → event_json`，**与 JSONL 的行序→条目完全同构**）。真机 fork 后官方 CLI 列出、**分支续跑成功**，且 OpenClaw 自己接管并维护该分支的投影进度（`indexed_seq` 随续跑推进）。
        写入涉及 7 张表**缺一不可**，且须跑一次 **`openclaw doctor --fix`**。
        ⚠️ **这是 OpenClaw 官方的命令**（让官方校验并置 `entry_valid`），**与本技能自己的 `--fix` 参数完全无关**——两者同名不同物，**不要混用**（前者在 OpenClaw 里跑，后者只在 WorkBuddy 里跑）。
  - **不在范围**：C 端云优先 SaaS（元宝 / 千问等）本地无转录。

## 数据与权限边界（本技能会读写什么）

> 这一节写给**要在受管环境里评估本技能的人**（安全审查 / 平台审核 / 团队管理员）。照实写，不夸大也不含糊。

**读**：本产品自己的会话记录（WorkBuddy / Claude Code / Codex / Hermes / pi 的 transcript 文件，或 OpenClaw 的 SQLite 库），以及**只读**打开的产品会话索引。
**写**（只有这三处，且**从不修改源会话**）：
1. **新建**的分支会话（源会话逐字节不动）；
2. **旁路**谱系索引（如 `~/.workbuddy/fork.lineage.json`）——不写产品官方 schema；
3. 产品自己的会话索引（`sessions.json` / `sessions` 表等）**新增一行**指向该分支；**写前自动备份**（`.bak.<时间戳>`）。

**明确不做**：不联网、不上传任何数据、不读凭据或密钥文件、**不请求提权（不调用 `sudo` / `root`）**、不改系统配置、不安装任何东西。
**可先验证再执行**：`--dry-run` **不落位、不登记、不改源会话**——它会写一个临时文件用于**磁盘字节校验**（校验完即清理），所以运行处需要写权限；`--verify` 是**只读**体检。
**文件权限**：分支文件要不要设为只读，**完全由你自己决定**；本技能只**建议**、不代为修改。
**语言**：本技能面向中文用户编写；同时提供英文字段 `display_name_en` / `description_en`（英文说明见仓库 [README.en.md](https://github.com/yamingmou/session-fork-core/blob/main/README.en.md)）。

## 故障排查（现象 → 原因 → 处理）

| 适用 | 现象 | 原因 | 处理 |
|---|---|---|---|
| 全部 | `VERIFY FAILED: old session id still present in non-raw fields` | 替换引擎漏了某可读字段（真残留，会拦）| 属创建阻断——v2.4.3 起验证前置：失败自动清理已写文件与注册，**不留脏分支**；排查残留字段是否在新字段类型上 |
| 全部 | `VERIFY FAILED` 但分支已出现在产品里 | **旧版本的问题**（v2.4.3 及更早：verify 在注册后才跑，失败也留脏分支）| 删掉该脏分支；升级到 v2.4.3+，新失败不再留痕 |

| 非 WorkBuddy | 分支建好但**看不到** | 各产品不同，且**有反直觉项**（如 Codex 桌面版也要 ⌘Q 重开）| **照脚本输出的 `ACTION` 行做**；逐产品要点见 **Step 0「分支怎么出现」表**——不要照搬 WorkBuddy 的说法 |

| 全部 | 原会话之后的新消息没进分支 | 快照特性（复制发生在读取时刻）——正常行为，不是丢数据 | 无需处理 |
| 全部 | `本轮消息里贴了 request id …：已按它切在 Lx（默认切点本会是 Ly）` | **正常提示、不是错误**：用户在这条消息里贴了「复制请求 ID」的 JSON，而命令走的是默认模式 ⇒ 工具**按贴的 id 切**（v2.4.23 起；此前的 v2.4.22 是拒绝执行） | 无需处理。若确实要默认切点，按提示用 `--line Ly` 重跑；要别的回复则 `--request-id <id>` |
| 全部 | 分支文件找不到 / 索引有记录但文件被删 | 外部清理 | 无恢复必要则删该索引记录（分支是快照，内容已在源会话） |
| 全部 | `--verify` 体检某分支报"源 id 残留" | 两种可能：①（v2.4.3 及更早）该分支在 v2.2.0 前创建，替换不彻底；②**误报**——fork 后产品追加的消息里恰好出现源 id（如一次 `ls` 输出中恰好有个同名目录，WorkBuddy 的实例是 `ls ~/.workbuddy/tasks`）。v2.4.4 起追加区**只对工具/函数 I/O 字段宽容**，正文等其余字段仍从严 | ①历史脏分支：重新打分支后删除旧分支（备份后）；②升级到 v2.4.4+ 即可。若该分支谱系 `at_seq` 缺失或与实际不符，校验会**故意退回更宽的旧边界**——宁可误报也不漏检，此时重打一次该分支即可 |

---

## 安装 / 升级（按产品，各一句话）

- **其他产品（Claude Code / Codex / Hermes / pi / OpenClaw）**：`pip install "git+https://github.com/yamingmou/session-fork-core.git@vX.Y.Z"`——**把 `@vX.Y.Z` 换成你要的那个发布 tag**（从 [Releases](https://github.com/yamingmou/session-fork-core/releases) 选）。**钉住 tag 而不是装 `main`**：这样才能装到"你选定的那一版"，而不是"今天恰好是什么"；重装升级同样带 tag 并加 `--force-reinstall`。
- 源码：https://github.com/yamingmou/session-fork-core · 作者 **OfferKuai（Offer快）团队** · License **MIT**（自由使用、修改与再分发，保留署名）。

## 变更历史

见仓库根 **`CHANGELOG.md`**（每版按：价值 / 实现 / 修改 / 检查）。本文件只留「怎么执行」——把历史塞进每次执行都要读的文档里，是噪音也是成本。**当前版本不在此处手写**：唯一权威是仓库的 tag / Release 与包内 frontmatter 的 `version`。
