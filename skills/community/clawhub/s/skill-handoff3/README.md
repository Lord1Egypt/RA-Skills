# handoff3 — Incremental Session Memory & Handoff

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-compatible-blue.svg)](https://agentskills.io)
[![Version](https://img.shields.io/badge/version-1.0.8-green.svg)](SKILL.md)
[![Ko-fi](https://img.shields.io/badge/Sponsor-Ko--fi-FF5E5B.svg)](https://ko-fi.com/skpll)
[![Sponsor](https://img.shields.io/badge/Sponsor-IFDIAN-946ce6.svg)](https://ifdian.net/a/handoff3)

[English](#english) · [中文说明](#中文说明)

---

<a id="english"></a>

## English

**Any questions, suggestions, or feedback while using it? Welcome to [join the official QQ group 801546098](https://qm.qq.com/q/sLZU77gjni)**.

Cross-agent incremental session memory and handoff. Bookmark as you go; render a ready-to-use report with one command when you hand off. It helps you capture key decisions, content, events and so on, so you can hand off cleanly to another agent, a fresh context window, a teammate, or your future self six months down the road.

This skill isn't mutually exclusive — feel free to mix it with your agent's own memory system, cross-check the two, or extend it into custom features like daily reports and summaries.

This skill uses progressive disclosure and loads files on demand — day-to-day use never pulls every file into context at once.

- **Lightweight**: the memory flow uses only the host's built-in file read/write and grep — no config layer, no external tools.
- **Cross-agent**: every agent has a corresponding adapter (**adaptation not yet complete, but it does not affect usage**); the main flow hardcodes no vendor's private format.
- **Your data stays yours**: defaults to project-local `.handoff3/`, can point to an external library; plain Markdown — readable, diffable, committable.

### Why the skill files stay in Chinese

`SKILL.md` and `references/` — the files that actually drive behavior — are maintained in Chinese; the README is bilingual for readers, but the instructions themselves are not.

- **Native language**: the author writes in Chinese, so the rules are most accurate and lose the least in Chinese.
- **Stability**: a single source of truth — no two language versions drifting apart, no one rule behaving two ways.
- **Performance**: skill files enter the context every turn; making them bilingual burns extra tokens each turn without making the skill any more capable.
- **Multilingual by nature**: agents read Chinese instructions as reliably as English ones, so the instruction language does not affect results. Need another language? Just ask the AI to translate it.
- **Forced translation**: if you strongly want the skill files written to disk in a language of your choice, ask the AI to translate `SKILL.md` and the files under `references/`.

### Quick start

1. **Call `/handoff3` bare first** — no trigger word. One shot does it all (six self-check steps → fill gaps → rebuild view → render report).
2. Then add your request after invoking the skill. Starting with "from memory" is recommended (but not required) for better results. Examples:

`/handoff3 from memory, generate this week's report`

`/handoff3 from memory, give me a 50-word summary`

`/handoff3 from memory, what problem are we solving now`

`/handoff3 from memory, together with the agent's memory, plan my daily tasks for next week`

See [Usage](#usage) for details.

### Why "handoff3"

The skill has gone through three generations.

- **First generation · parse at handoff**: read the whole record into memory at handoff, split it into topic groups, score and trim to budget, then hand back only structured conclusions. But the scripts were heavy and the model light — **complexity piled up on the engineering side**.
- **Second generation · distill at handoff**: turned distillation into an eight-layer one-way pipeline, pure data between layers, hard token budgets of 1500/4000. Yet on a 77 MB real-world record, **all 36 self-checks passed while the artifact's usable output kept declining**.
- **Third generation · bookmark as you go**: each turn the model writes one memory entry with a verbatim quote; handoff merely reads a few `mem_` files and renders. With local semantic parsing offloaded, readability and usability improve substantially.

The first two still hold value for semantic parsing, architecture design, and engineering reference, and will keep being updated. But their overall practicality is now poor, so they are not open-sourced for the time being.

### Install

Copy the skill folder into your host's skills directory (WorkBuddy: `~/.workbuddy/skills/`). First use creates `.handoff3/` at the project root; no manual initialization.

To use an external library: write a single absolute path to the library root in `.handoff3/root.txt` at your project root (the skill reads only this line, no migrate command is provided). A wrong path stops with an error — it will not fall back to creating a new local library. Migration and backup are up to you.

### Usage

#### The basics

The skill creates a `.handoff3/` folder at your project root; all memory data lives there:

```
project/.handoff3/
├── root.txt            optional; one absolute path to an external library (a bad path stops with an error, never falls back)
├── memory/             source of truth — one file per session
│   └── mem_<agent>_<session>.md
├── handoff_memory.md   full view, rebuilt from memory/, refreshable any time
├── handoff_patches.md  criteria sentences — rule source, loaded every turn (skip if absent); appended only after you answer "yes"
└── handoff_report.md   artifact — the handoff report
```

What each file is for:

- `memory/mem_<agent>_<session>.md`: **source of truth**, one file per session, append-only and never rewritten; turns into read-only frozen memory once the session is deleted or archived.
- `handoff_memory.md`: **full view**, rebuilt from `memory/` at handoff and refreshable any time; this is what "from memory" reads.
- `handoff_report.md`: **handoff artifact**, written only by the handoff action, for whoever picks up next.
- `handoff_patches.md`: **criteria sentences rule source** (loaded every turn, not an archive; skipped when absent) — the only part of the skill that evolves; a checkable rule is appended only when you point out a problem and answer "yes".
- `root.txt`: optional single absolute path to an external library; a wrong path stops with an error, it never falls back to creating a new local one.

#### Fine-grained calls

For finer control — e.g. an audit without a report, or asking straight from memory — use the actions below:

| Action | How to trigger | What it does |
|---|---|---|
| Handoff | Bare `/handoff3`, or say handoff / handover / wrap up / report / archive / lost context / rebuild … | **Includes all six self-check steps** → fill gaps → rebuild view → render report. **The only action that writes a report** — this is all you need day to day |
| Update memory | update memory / refresh memory / sync memory … | **Only reads/writes the current session's own `mem_` file**: create if missing, fill gaps, repair structure in place; touches no other file, runs no self-check, rebuilds no view, writes no report. Use when the footer fails or you suspect that one file is broken or missing |
| Self-check | self-check / check memory / memory check / memory repair … | Six-step audit and repair, no report; handoff already includes it, use alone only for audit-without-report |
| From memory | **Requires** `/handoff3` prefix: from memory / based on memory … | Refreshes the view if stale, then answers from it; writes no report |
| Help | help | Prints the built-in usage guide, reads/writes no files |

These actions are **conventions, not hard rules**. You may invoke the skill any way you like — plain natural language included. Just keep the phrasing **colloquial and consistent**: stick to stable trigger words and vocabulary (e.g. "handoff", "update memory", "self-check", "from memory") rather than constantly inventing new ones, so the skill recognizes your intent reliably.

### End-of-reply signal

The **last** reply to the user each turn ends with one of two signals; missing either means the rule did not run:

- A `mem_` file was written or repaired → footer (`This turn's key points have been added to handoff3 memory:` + absolute file path + token readout); "update memory" repairing a file counts too
- No `mem_` file was touched → `No memory was written this turn; handoff3 did not change any memory file.` (**this is the default**, use it when unsure)

Only the last reply counts: process chatter and transitional one-liners between tool calls are out of scope.

### Six self-check steps

All six always run: S1 structure / S2 naming / S3 ownership / S4 reachability (a quiet period does not count as frozen) / S5 coverage / S6 orphans. Criteria and fixes are in [SKILL.md](SKILL.md) §6 and `references/selfcheck.md`. Self-check's write scope is limited: format and status words may cross files, but entry content is changed only in your own session's file.

### Files

```
SKILL.md                              main file: rules, actions, handoff flow
references/
├── commands.md                       the five actions: forms, triggers, prefix rules, boundaries
├── schema.md                         naming & parsing, file sources, entry format, gap criteria, legacy compat
├── types.md                          eight semantic categories, counterexamples, conflict priority
├── template.md                       handoff report skeleton & fixed gap-section format
├── selfcheck.md                      six self-check steps: criteria, fixes, false-positive guards
└── adapters/
    ├── index.md                      five interfaces, contract, steps to add an agent
    ├── workbuddy.md                  WorkBuddy / WorkBuddy AI
    ├── deepseek-harness.md           DSH (compressed records, limited capabilities)
    └── generic.md                    fallback + new-agent template
```

### Explicitly out of scope

Topic groups and grouping algorithms, multi-tier budgets and token shrinking, post-hoc validation scripts, web editors, MCP/hooks, weight-scoring scorecards, DSPy/GEPA/DPO, reading large files whole, and **automatically merging multi-session files** (fragments are unified by the view; merging only introduces new attribution ambiguity).

### Support

If handoff3 saves you time, you're welcome to buy me a coffee:

<p align="center">
  <a href="https://ko-fi.com/skpll">
    <img src="https://img.shields.io/badge/Buy_me_a_coffee-Ko--fi-FF5E5B?style=for-the-badge" alt="Buy me a coffee on Ko-fi">
  </a>
  &nbsp;
  <a href="https://ifdian.net/a/handoff3">
    <img src="https://img.shields.io/badge/Buy_me_a_coffee-IFDIAN-946ce6?style=for-the-badge" alt="Buy me a coffee on IFDIAN">
  </a>
</p>

### License

MIT — see [LICENSE](LICENSE).

---

<a id="中文说明"></a>

## 中文说明

**使用中有任何问题、建议或反馈，欢迎[加入官方QQ群 801546098](https://qm.qq.com/q/sLZU77gjni)**。

跨 agent 的会话记忆与交接技能。日常顺手记账，交接时一键成稿。可以辅助你记下关键决策、内容、事件等信息，以顺利交接给其他 agent、新的会话窗口、项目组的其他成员，或者半年后的自己。

本技能不与其他技能竞争，也不排他：你可以自由和 agent 自身的记忆系统混合使用、交叉验证，或自由拓展日报、总结等自定义功能。

本技能使用渐进披露、按需加载的方式，日常使用时不会一次性加载进全部文件。

- **轻负担**：记忆流程只用宿主自带的文件读写与 grep，无配置层、无外部工具。
- **跨 agent**：各 agent 都有对应的 adapter（**目前未适配完成，但不影响使用**），主流程不硬编码任何一家的私有格式。
- **本地数据**：默认写项目内 `.handoff3/`，可指向外部记忆库；明文 Markdown，可读可 diff 可入库。

### 为什么技能文件用中文

`SKILL.md` 与 `references/` 这些真正驱动行为的文件用中文维护；README 为了读者使用做成双语，指令本身不做双语。

- **母语**：作者用中文写作，规则用中文写最准确、损耗最小。
- **稳定**：单一真源。不会出现中英两个版本各自漂移、同一条规则两种行为。
- **性能**：技能文件每轮都进上下文，做成双语等于每轮多烧 token，却不会让技能更强。
- **兼容多语言**：模型天然多语言，读中文指令和英文指令的执行效果一样，指令语言不影响结果。需要别的语言，让 AI 翻译即可。
- **强制翻译**：如果你强烈希望技能文件以你所指定的语言落盘，可以让 AI 翻译 SKILL.md 和 references 中的文件。

### 快速使用

1. 首先**裸调用 `/handoff3`**——不加任何触发词。一步到位（含自检六步 → 补缺口 → 重建视图 → 出报告）。
2. 然后调用技能后，加入你的想法。推荐以“基于记忆”开头（但不强制），以增强效果。示例：

`/handoff3 基于记忆，生成本周周报`

`/handoff3 基于记忆，给我50字总结`

`/handoff3 基于记忆，当前解决的问题`

`/handoff3 基于记忆，和 agent 的记忆，给我规划下周每日任务`

详情参见 [用法](#用法)。

### 为什么叫 handoff3

其实这个技能已经迭代到第三版。

- **第一版 · 交接时解析**：在交接时把记录整份读进内存、切主题组、加权打分、按预算裁剪，只把结构化结论回传模型。但脚本重、模型轻，**复杂度全压在工程侧**。
- **第二版 · 交接时提炼**：把提炼改成八层单向流水线，层间只传纯数据，token 硬预算精确到 1500 / 4000。但在 77 MB 真实记录上，**自检 36 项全绿，产物可用性却持续下降**。
- **第三版 · 平时记账**：每轮产生实质结论时由模型自己写一条带原文引用的记忆，交接时只读几个 `mem_` 文件成稿。在减少本地语义解析的同时，可读性与可用性大幅提升。

第一版和第二版在语义解析、架构设计和工程参考方面仍具价值，会继续更新。但目前综合实用性非常差，暂不开源。

### 安装

技能目录放进宿主的技能目录即可（WorkBuddy 为 `~/.workbuddy/skills/`）。首次使用会在项目根建 `.handoff3/`，无需手动初始化。

想放到外部记忆库：在项目根 `.handoff3/root.txt` 写一行库根的绝对路径即可（技能只读这一行，不提供迁移命令）。路径指错会报错停止，不会回退到项目内新建库；迁移与备份由用户自行处理。

### 用法

#### 基础流程

本技能在你项目根目录建一个 `.handoff3/` 文件夹，记忆数据都在这里：

```
项目根/.handoff3/
├── root.txt            可选；一行绝对路径，指向外部记忆库（指错即停）
├── memory/             真源：一会话一文件
│   └── mem_<agent>_<会话>.md
├── handoff_memory.md   全量视图：由 memory/ 重建，可随时刷新
├── handoff_patches.md  判据句规则源（每轮加载、非档案；无则跳过），需用户答「是」才追加
└── handoff_report.md   产物：交接稿
```

各文件用途：

- `memory/mem_<agent>_<会话>.md`：**真源**，一会话一文件，每轮只追加、不重写；会话被删或归档后自动转只读沉淀。
- `handoff_memory.md`：**全量视图**，交接时由 `memory/` 重建，可随时刷新；「基于记忆」读的就是它。
- `handoff_report.md`：**交接产物**，只有「交接」这个动作会写，给接手人看。
- `handoff_patches.md`：**判据句规则源**（每轮加载、非档案；文件不存在则跳过），本技能唯一会「进化」的地方——你指出产物问题并答「是」才追加一条可判断的规则。
- `root.txt`：可选，一行绝对路径指向外部记忆库；指错即停，不会回退到项目内新建。

#### 精细调用解读

想精细操作（例如只体检不出稿、或直接问记忆里的内容），可以用下面这些动作：

| 动作 | 怎么触发 | 作用 |
|---|---|---|
| 交接 | 裸调用 `/handoff3`，或说 交接 / 生成 / 报告 / 归档 / 上下文接不上 … | **含自检六步** → 补缺口 → 重建视图 → 出报告。**唯一写报告的动作**，日常只需这一条 |
| 更新记忆 | 更新记忆 / 刷新本会话记忆 / 补全记忆 / 同步记忆 / 修复落款 | **只读写当前会话那一个 mem 文件**：缺失就建、漏记就补、结构问题就地修；不动别的文件、不跑自检、不重建视图、不出报告。落款失效或怀疑该文件有问题/缺失时用 |
| 自检 | 自检 / 检查记忆 / 修复记忆文件 … | 六步体检并修复记忆文件，不出报告；交接已含，只体检不出稿时才单独用 |
| 基于记忆 | **须** `/handoff3` 前缀：基于记忆 / 按记忆 … | 刷新视图后读它作答，不写报告 |
| 帮助 | 帮助 / help | 列出用法，不读写文件 |

这些动作只是**用法规范，不是硬性规定**——你可以用任何方式调用本技能，自然语言直说也行。但请保持**口语化、词汇用法的稳定**：触发词和说法尽量固定（交接 / 更新记忆 / 自检 / 基于记忆），别频繁换词，这样技能每次都能稳定识别你的意图。

### 结尾信号

每轮**最后一条**面向用户的回复末尾二选一，缺一即视为规则未执行：

- 写入或修复过 mem 文件 → 落款（`本轮对话要点已自动加入 handoff3 记忆：` + 文件绝对路径 + token 读数）；「更新记忆」修复了文件也算
- 完全没碰 mem 文件 → `本轮未写入记忆，handoff3 未改动记忆文件。`（**这是默认**，拿不准就用它）

范围只管最后一条回复：工具调用之间的过程话、过渡性短句不在范围内，不必附。

### 自检六个子步骤

六步固定全执行（S1 结构 / S2 命名 / S3 归属 / S4 可达性〔静默期不算沉淀〕 / S5 覆盖 / S6 缺档），判据与修法见 [SKILL.md](SKILL.md) §6 与 `references/selfcheck.md`。自检的写操作本就受限：格式与状态词可跨文件，条目内容只改自己会话的文件。

### 文件

```
SKILL.md                              主文件：规则、动作、交接流程
references/
├── commands.md                       五个动作的调用形式、触发词、前缀规则与触发边界
├── schema.md                         命名与解析、文件源、条目格式、缺口判据、旧格式兼容
├── types.md                          八类语义判据、反例、冲突优先级
├── template.md                       交接稿骨架与缺口段固定格式
├── selfcheck.md                      自检六步的判据、修法、误判防范
└── adapters/
    ├── index.md                      五个接口、契约、新增 agent 步骤
    ├── workbuddy.md                  WorkBuddy / WorkBuddy AI
    ├── deepseek-harness.md           DSH（压缩记录件，能力受限）
    └── generic.md                    兜底 + 新增 agent 模板
```

### 明确不做

主题组与分组算法、多档预算与 token 收缩、事后校验脚本、网页编辑器、MCP/钩子、权重评分打分卡、DSPy/GEPA/DPO、整读大文件、**自动合并多会话文件**（碎片由视图统一，合并只会引入新的归属歧义）。

### 支持

如果 handoff3 帮到了你，欢迎请我喝杯咖啡：

<p align="center">
  <a href="https://ifdian.net/a/handoff3">
    <img src="https://img.shields.io/badge/%E8%AF%B7%E6%88%91%E5%96%9D%E6%9D%AF%E5%92%96%E5%95%A1-%E7%88%B1%E5%8F%91%E7%94%B5-946ce6?style=for-the-badge" alt="在爱发电支持">
  </a>
  &nbsp;
  <a href="https://ko-fi.com/skpll">
    <img src="https://img.shields.io/badge/%E8%AF%B7%E6%88%91%E5%96%9D%E6%9D%AF%E5%92%96%E5%95%A1-Ko--fi-FF5E5B?style=for-the-badge" alt="在 Ko-fi 支持">
  </a>
</p>

### 许可

MIT —— 见 [LICENSE](LICENSE)。
