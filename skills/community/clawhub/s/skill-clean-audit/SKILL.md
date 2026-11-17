---
name: skill-clean-audit
version: 1.4.0
description: >
  第一性原理 clean code 审计法。从单根前提「代码是写给人看的」推导出两根判据——
  A. 理解成本（读起来费不费劲）/ B. 修改风险（改起来怕不怕），用红/黄/绿三档给代码打分，
  并明确允许「有意的、注释了的、范围可控的技术债」暂时存在。专用于审计你自己的
  WorkBuddy Skill 脚本或其他 Python 代码，产出带证据(文件:行)的可勾选报告。
  触发词：「用第一性原理审代码」「理解成本/修改风险」「clean code 审计」「审计我的 Skill 脚本」
  「按红黄绿审代码」「clean code 审计样例」。注意：本 skill 只做可读性/可维护性的第一性原理审计，
  不做通用 PR/MR 审查（那用 code-review-assistant 或 critical-code-reviewer），
  不替代 clean-code 的写代码规范手册，也不做 lint/格式化（那用 project-code-standard）。
  First-Principles Clean Code Audit. Derives two criteria from one root premise — "code is written for humans":
  A. Comprehension cost (how hard to read) / B. Change risk (how scary to modify) — scored red/amber/green,
  explicitly permitting intentional, documented, scoped tech debt. Audits your own WorkBuddy skill scripts or
  Python code, emitting an evidence-backed (file:line) checklist report. Triggers: "audit code with first principles",
  "comprehension/change risk", "clean code audit", "audit my skill scripts". Read-only on the code under audit — never modifies the source being reviewed; writes its own local report/checklist artifacts only (disclosed side effect).
  Note: this skill does first-principles readability/maintainability audit only — not generic PR/MR review
  (use code-review-assistant / critical-code-reviewer), not a style handbook (use clean-code),
  and not lint/format (use project-code-standard).
summary: 第一性原理 Clean Code 审计法——只读审计你自己的 WorkBuddy Skill 脚本 / Python 代码，用「理解成本 / 修改风险」两轴 + 红黄绿，产出带证据 (file:line) 的可勾选报告；方法论从单根前提推导，不依赖任何外部二进制或凭据。
tags:
  - clean-code
  - code-audit
  - readability
  - maintainability
  - static-analysis
  - skill-tooling
---

# 第一性原理 Clean Code 审计 / First-Principles Clean Code Audit

## 30 秒上手 / Quick Start（5 行）

1. 给我**一个文件 / 函数 / 目录**当审计目标（没给 → 我会先问你审哪个）。Give me **one file / function / dir** as the target (none given → I ask first).
2. 选语言：说 `zh` / `en` 强制，或不说走 `auto`（按你消息语言判定）。Pick language: say `zh`/`en` to force, or leave it for `auto` (follows your message).
3. 我**只读**目标，按「理解成本 / 修改风险」两轴 + 红黄绿打分，每项带 `文件:行` 证据。I **read-only** the target, score via comprehension/change axes + red/amber/green, each item with `file:line` evidence.
4. 产出：报告 `clean_code_audit_<target>.md` + 可勾选清单（中文 `clean_code_checklist.html` / 英文 `clean_code_checklist.en.html`）。Output: report `clean_code_audit_<target>.md` + tickable checklist (zh `clean_code_checklist.html` / en `clean_code_checklist.en.html`).
5. 想快筛疑点：可跑 `scripts/metric_probe.py --src <file>`（纯 stdlib，只提示不判级）。Quick scan: run `scripts/metric_probe.py --src <file>` (pure stdlib; hints only, no grading).

> 完整流程见下方「审计流程」；边界 / FAQ 见 `references/faq.md`（中文）或 `references/faq.en.md`（英文）。Full flow below under "Audit Flow"; boundaries / FAQ in `references/faq.md` (zh) or `references/faq.en.md` (en).

## 合规与边界声明（网络访问）/ Compliance & Boundary Statement (Network Access)

  - 本 skill **不发起任何网络请求**，不调用任何第三方 / 海外 API，不读取任何凭据、密钥或环境变量；它**只读被审计的*代码*本身**（从不修改被审源码），并额外把自身产出（审计报告 + 清单）写到工作区——写入范围仅限这两类产物，且在此声明（见下方 Trust 红线）。
  This skill makes **no network requests**, calls no third-party / overseas API, reads no credentials, secrets, or env vars; it **reads only the *code under audit* (never modifies the source being reviewed)** and additionally writes its own output artifacts (audit report + checklist) to the workspace — its writes are limited to those two artifact types, disclosed here (see the Trust red line below).
- **不提供、不指导、不支持任何规避网络管理措施的能力**；不使用非公开接口、不破解访问控制、不伪造身份绕过鉴权。
  Provides / instructs / supports **no means to circumvent network-management measures**; no private interfaces, no access-control bypass, no identity spoofing.
- 无「数据源 / 海外源」概念——全部输入来自本地文件，故「海外源不可达需降级」场景不适用（N/A）。
  No "data source / overseas source" concept — all input is local, so "overseas source unreachable → degrade" is N/A.
- 若运行环境禁止网络，本 skill 行为完全不受影响（它本就不联网）。
  If the runtime forbids network, this skill is unaffected (it never goes online).
-   **Requirements（声明与行为一致 / declared == behaved）**：核心审计零外部二进制（python/git/gh/node/npx/shell 均不调用）、零环境变量、零凭据、零运行时依赖。可选的辅助脚本 **`scripts/metric_probe.py`** 需 Python 3，但也是纯标准库、零网络、零凭据、只读——不是运行时依赖，不调用即不影响审计。
  **Requirements (declared == behaved)**: the core audit needs no external binaries (calls no python/git/gh/node/npx/shell), no env vars, no credentials, zero runtime deps. The optional helper **`scripts/metric_probe.py`** needs Python 3 but is also pure stdlib, offline, no credentials, read-only — not a runtime dependency; the audit works without invoking it.

## 语言选择 / Language

本 skill 的全部产物（交互清单、审计报告、范例、FAQ）均提供**中文版与英文版**。触发时先定语言模式，再开工——**语言绝不是隐藏默认值**。

This skill ships every artifact (interactive checklist, audit report, samples, FAQ) in **both Chinese and English**. Pick the language mode before starting — **language is never a hidden default**.

**三种模式 / Three modes**：

- **`auto`**（默认）：按你与 Agent 交互所用的语言自动判定并切换——消息为英文 → 英文产物；中文 → 中文产物；中英混排以你的主语言为准；纯代码 / 路径、无自然语言 → 主动问你「报告用中文还是英文？」。
  **`auto`** (default): follows the language of your exchange with the agent — English message → English artifacts; Chinese → Chinese; mixed → your dominant language; pure code / path with no natural language → ask "Chinese or English report?".
- **`zh`**：强制中文——所有产物一律中文，**忽略**交互语言。
  **`zh`**: force Chinese — all artifacts in Chinese, **ignoring** the exchange language.
- **`en`**：强制英文——所有产物一律英文，**忽略**交互语言。
  **`en`**: force English — all artifacts in English, **ignoring** the exchange language.

**判定优先级 / Resolution order**：你显式说 `zh` / `en` > 交互语言推断 `auto` > 兜底询问。**整轮审计不中途切换**（避免报告半中半英）；下一轮可重新判定。

**Resolution priority**: your explicit `zh`/`en` > inferred `auto` from exchange language > ask. **No mid-audit switch** (avoids mixed-language report); re-resolved next round.

产物按模式选文件（中英各一套，含清单 / 两种样例 / FAQ，完整映射表见 **`references/faq.md` §8**）。产物按模式选文件，缺失英文版时 fallback 到中文并注明，**不静默给错语言**。Pick artifacts by mode (full mapping table in **`references/faq.md` §8**); if an English version is missing, fall back to Chinese and note it — never silently give the wrong language.

## 执行模型（方法论型，非工具型）/ Execution Model (Methodology, Not Tool)

本 skill 是**方法论型**：交付「判据 + 流程 + 可勾选清单」，由你（Agent）逐项判断并给 `文件:行号` 证据。审计的核心动作是**判断**（这段代码偏 A 还是偏 B、是红还是有意的债），本质是人的推理，**无法预先写成确定性自动流程**。
This skill is **methodology-type**: it ships criteria + flow + a tickable checklist that you (the agent) apply item by item with `file:line` evidence. The core action is *judgment*, which cannot be pre-encoded into a deterministic pipeline.

> **因此没有端到端自动化脚本是设计决策，不是缺失。** 本 skill 提供的 `scripts/metric_probe.py` 是**可选加速器**——只探测指标信号帮你快速定位疑点，**只提示不判级**；用不用它，审计质量标准不变。
> **The absence of an end-to-end automation script is a design decision, not a gap.** The `scripts/metric_probe.py` shipped here is an *optional accelerator* — it locates suspects fast but *hints only, never grades*; the quality bar is unchanged whether you run it or not.

## 它是什么 / 不是什么 / What it is / is not

**是 / Is**：一个审计方法论 + 可落地产物。拿两根判据去戳代码，逐项打勾带证据，出报告。
An audit methodology + a concrete artifact. Pokes code with two criteria, ticks items with evidence, emits a report.

**不是 / Is not**（明确边界，避免和已有 skill 重叠 / explicit boundaries, to avoid overlap with existing skills）：

- ❌ 通用 PR/MR 审查 → 用 `code-review-assistant` / `critical-code-reviewer`
- ❌ 写代码的标准手册 → 用 `clean-code`（SRP/DRY/KISS 那套）
- ❌ lint/格式化执行 → 用 `project-code-standard`（ruff/eslint/prettier）
- ❌ SOLID / 干净架构 / TDD 原则库 → 用 `uncle-bob`（本 skill 只从第一性原理**推导**，不抄它的规则；见 `references/smells_crosswalk.md` 做等价桥接）

本 skill 的价值在三点，现有 skill 都没有：① 规则是**推导**出来的不是给定的；② 用**成本/风险**两轴而非类别桶；③ 允许**有意的债**。
Three things no existing skill does: ① rules are *derived*, not given; ② a cost/risk two-axis model, not category buckets; ③ permits *intentional debt*.

- **路由提示 / Routing**：给单个文件或函数 → 直接走下方「审计流程」；给整个 Skill 目录 → 建议逐个脚本审，优先挑最常被修改的那几个（修改风险本就高）。Give one file/function → go straight to Audit Flow; give a whole skill dir → audit script by script, prioritizing the most-frequently-changed ones (high change risk by nature).
- **常见疑问 / FAQ**：边界、产物写到哪、支持语言、是否联网等高频问题集中见 **`references/faq.md`**（中文）或 **`references/faq.en.md`**（英文），按《语言选择》模式选。Common questions (boundaries, where reports go, supported languages, network needs) are centralized in **`references/faq.md`** (zh) or **`references/faq.en.md`** (en), picked per the Language mode.

**我该读哪个文件 / Which file to read**（渐进式披露导航 / progressive-disclosure routing）：

| 何时 / when | 读 / read |
|---|---|
| 常规审计主流程 / normal audit | 本文件《审计流程》· `assets/clean_code_checklist.html`（按语言选 `.en`） |
| 不确定某 smell 算 A 还是 B / smell → A or B? | `references/smells_crosswalk.md` |
| 想看一份完整报告长什么样 / full report example | `references/clean_code_audit_sample.md`（或 `.en`） |
| 类 / 继承 / 异步 / 全局态代码 | `references/clean_code_audit_sample_complex.md`（或 `.en`） |
| 边界、产物位置、异常细则、产物映射 | `references/faq.md`（或 `.en`） |
| 想快筛疑点 / quick suspect scan | `scripts/metric_probe.py --src <file>` |

## 第一性原理推导 / First-Principles Derivation

1. **根前提 / Root premise**：代码是写给人看的。机器只认语法对不对，不在乎命名/长度/注释；代码真正的生命周期在「被另一个人（含未来的你）阅读、修改、维护」的那无数次里。
   Code is written for humans. Machines only care whether syntax is valid, not naming/length/comments; code's real life is in the countless times it is read, modified, maintained by another person (including future you).
2. 由此只推出两根判据 / From this, only two criteria follow:
   - **A. 理解成本 / Comprehension cost** —— 让人一眼读懂意图与边界 So intent and boundaries are obvious at a glance.
   - **B. 修改风险 / Change risk** —— 改动时不牵连出错 So a change doesn't quietly break something else.
3. 所有具体规则都是这两根的子树。检验不过「是否真的降低了理解和修改成本」的，就是噪音。
   Every concrete rule is a subtree of these two. Anything that fails "does it actually lower comprehension or change cost?" is noise.

> 关键反推 / Key reversal：为凑清单而清单（为短拆七层 tiny function、为 DRY 抽象没人用的接口）反而抬高成本，是脏的。
> Checklist-for-its-own-sake raises cost — that is dirty.

## 严重度（红黄绿）/ Severity (Red / Amber / Green)

- 🔴 **红 · 出现即脏，优先修 / Red · dirty on sight, fix first**：符号来源隐式（`import *`）、重复/矛盾的说明、注释退化成 changelog（满屏工单号）、模块级可变全局状态控行为、命名与行为不一致 / 隐藏副作用（CQS 违反：函数名像查询却偷偷改状态或打印）、重复逻辑（DRY 违反）、裸 `except` 静默吞错。
  Implicit symbol origin (`import *`), contradictory docs, comments degraded into a changelog, module-level mutable global controlling behavior, name≠behavior / hidden side effects (CQS violation), duplicated logic (DRY violation), bare `except` swallowing errors.
- 🟡 **黄 · 有意的债，需注释 + 范围可控 / Amber · intentional debt, needs comment + scope**：长函数（>40 行但确内聚难拆）、魔法数字/字符串未命名、有意的 best-effort `except`（单源失败不拖垮管线）。黄=暂时可接受，但必须写清「为什么」且范围可控。
  Long functions (>40 lines but cohesive), unnamed magic numbers/strings, intentional best-effort `except`. Amber = temporarily acceptable, but the "why" must be written and scope controlled.
- 🟢 **绿 · 出现即干净 / Green · clean on sight**：命名即文档、显式优于隐式、行为只由入参决定、有测试覆盖、所有 `except` 均精确。
  Naming is documentation, explicit beats implicit, behavior depends only on inputs, tested, every `except` precise.

完整可勾选清单见 **`assets/clean_code_checklist.html`**（打开即可逐项打勾，带实时计数）。
Full interactive checklist: **`assets/clean_code_checklist.html`** (open to tick items, with a live counter).

## 轻量指标信号（核查提示，非硬规则）/ Lightweight Metric Signals (hints, not hard rules)

第一性原理的判据永远是 A/B 两轴；以下数字只是**「值得多看一眼」的探针**，帮你更快定位疑点，**不是自动判红**：
The first-principles criteria remain the A/B axes; the numbers below are only probes to locate suspects faster — **not automatic red flags**:

- 函数 > 40 行 · 参数 ≥ 4 · 嵌套 ≥ 4 · 布尔旗参数 · 同类逻辑重复 ≥ 3 次 —— 五项信号
  Function > 40 lines · params ≥ 4 · nesting ≥ 4 · boolean-flag params · same logic repeated ≥ 3× — five signals

> 五项信号的完整定义、A/B 轴归属判读、以及「命中 ≠ 脏」的完整论证见 **`references/faq.md` §5**；可跑 **`scripts/metric_probe.py --src <file>`** 自动探测并输出 `file:line` 清单（纯 stdlib，**只提示不判级**，最终仍由你按两轴判断）。
> Full definitions, A/B attribution, and the "a hit ≠ dirty" argument: **`references/faq.md` §5**. Run **`scripts/metric_probe.py --src <file>`** to auto-detect with `file:line` output (pure stdlib, *hints only, never grades*).

## 审计流程 / Audit Flow

1. **读目标文件 / Read the target**：把要审的函数/模块完整读出来，不要凭印象。Read the whole function/module; don't audit from memory.
   - 若用户未指定具体文件/函数，**先追问再审**：① 要审哪个文件或目录？② 关注哪个函数/模块（还是整体）？不凭印象审计用户未指定的代码。If the user gives no target, ask which file/function before auditing — never audit unspecified code.
2. **逐项对照清单 / Check against the list**：对 `assets/clean_code_checklist.html` 每一项，判断在目标代码里是否命中。常见 smell 的标准命名（Rigidity/Fragility/Opacity…）对照见 **`references/smells_crosswalk.md`**，便于把发现标准化。
   For each item in `assets/clean_code_checklist.html`, judge whether it hits. Standard smell names (Rigidity/Fragility/Opacity…) crosswalk: **`references/smells_crosswalk.md`**.
3. **带证据打勾 / Tick with evidence**：每条命中必须给 `文件:行号` 和一句话「它抬高了 A 还是 B、怎么抬的」。无证据的直觉不打勾。
   Every hit needs `file:line` and one sentence on whether it raises A or B, and how. No evidence, no tick.
4. **数红黄绿 / Count red/amber/green**：用清单底部计数器或手算；指标信号（上节）可辅助定位，但不计入严重度。
   Use the checklist counter or count by hand; metric signals help locate but don't count toward severity.
5. **出报告 / Emit report**：格式见下方「输出格式」，完整范例见 **`references/clean_code_audit_sample.md`**（那是一份用合成示例脚本 `demo-skill/scripts/aggregate.py` 的 `main()` 真审出来的样例，照它的结构写；样例片段自带行号、可逐行核对，不对应任何真实项目）。
   Format below; full sample: **`references/clean_code_audit_sample.md`** (a real audit of synthetic `demo-skill/scripts/aggregate.py`; snippet is line-numbered, checkable, maps to no real project).

## 异常与降级 / Exceptions & Degradation

- 文件不存在 / 无读权限 → **给 3 步自查指引，不要只回「读不到」**：① 核对路径拼写与相对/绝对路径（`./` 相对的是工作区根目录，不是被审文件所在目录）；② 确认文件确实存在——列出目录验证（`ls` / 文件管理器）；③ 请用户贴正确路径，或把文件放进工作区根目录再试。**不猜测、不降级去审别的文件**。File missing / no read permission → **give a 3-step self-check, don't just say "can't read"**: ① check path spelling and relative/absolute form (`./` is the workspace root, not the audited file's dir); ② confirm the file exists — list the directory to verify; ③ ask the user to paste the correct path, or drop the file into the workspace root and retry. Never silently audit another file.
- 非代码文件（图片 / 二进制 / 数据）→ 拒绝审计，说明本 skill 只审源码文本。Non-source file (image / binary / data) → refuse, explain scope (source text only).
- 超大文件 / 整目录 / 网络凭据 → 细则见 **`references/faq.md` §4 / §7**。Large file / whole dir / network-credentials → details in **`references/faq.md` §4 / §7**.

## 输入要求 / Input Requirements

- 接受：Python（.py）为主；WorkBuddy Skill 脚本常含 .py / .js / .ts（SKILL.md / references/ / scripts/）；以及任何「人类可读的源代码文本」。Accepts Python (.py) primarily; skill scripts often .py / .js / .ts; any human-readable source text.
- 不接受：二进制 / 图片 / 数据文件（.png / 数据型 .json / .xlsx 等）、加密或混淆代码——本 skill 只审源码文本。Not for binaries / images / data files (.png, data .json, .xlsx…) or obfuscated code — source text only.
- 覆盖行为 / Overwrite：每份报告是新文件 `clean_code_audit_<target>.md`，**不覆盖**已有同名报告；清单 `clean_code_checklist.html` 为可复用副本，覆盖式写入工作区根目录。Each report is a new file `clean_code_audit_<target>.md`, **never overwrites** an existing same-name report; the checklist `clean_code_checklist.html` is a reusable copy written over at workspace root.

## 输出格式 / Output Format

落盘到**当前 agent 会话的工作区根目录**（即本对话打开的项目目录，例如 `~/WorkBuddy/<session>/`），文件名 `clean_code_audit_<target>.md`，结构：
Write to the **current agent session's workspace root** (the opened project dir, e.g. `~/WorkBuddy/<session>/`), filename `clean_code_audit_<target>.md`, structure:

- 报告标题与表头使用用户所选语言（`zh` / `en` / `auto` 判定结果）；样例结构见 `references/clean_code_audit_sample.md`（中文）或 `references/clean_code_audit_sample.en.md`（英文）。
  Report title and table headers use the chosen language (`zh` / `en` / `auto` result); sample structure: `references/clean_code_audit_sample.md` (zh) or `references/clean_code_audit_sample.en.md` (en).

- 表头：审计对象（路径 + 函数/行范围 + 行数） / Header: target (path + function/line range + line count)
- **A. 理解成本 / Comprehension cost** 表：# / 清单项 / 命中(✅红·✅黄·⬜未命中·❌未达标) / 证据(行) / 说明
- **B. 修改风险 / Change risk** 表：同上 / same as above
- **额外发现**（可选，不在清单内但同属理解成本的 smells，如嵌套条件难读）/ **Extra findings** (optional, smells outside the list but still comprehension cost, e.g. unreadable nested conditions)
- **审计评分 / Score**：红 N / 黄 N / 绿 N（+ 未命中/未核实项）
- **结论 / Conclusion**：按第一性原理说清「脏」偏在哪一侧、修改优先级建议（先消零行为风险的纯可读项，再排重复/拆函数，黄项随改顺手处理）
  Per first principles, state which side "dirty" leans toward and the fix priority (kill zero-behavior-risk pure-readability items first, then dedupe/split; handle amber along the way).

## 修复优先级：增量清理（Boy Scout）/ Fix Priority: Incremental Cleanup (Boy Scout)

本 skill 只读不改，但报告「结论」段的优先级建议按此原则给：
This skill reads only, but the report's "conclusion" priority follows this principle:

- 🔴 红项 / Red：你**本来就要改这个文件**时，顺手清掉；不要为清它而专门开 PR 动一个稳定、无人碰的文件。
  Clear it when you're *already* editing that file; don't open a PR just to clean a stable, untouched file.
- 🟡 黄项 / Amber：保持「注释说清 + 范围可控」即可，**不主动还债**；等下次自然触达时再评估。
  Keep "comment + scoped"; don't pay it down proactively; re-evaluate on next natural touch.
- 不带测试覆盖的 Skill 脚本 / Skill scripts without tests：测试「有则绿、无不算红」——Skill 脚本多为一次性工具，强求单测是过度工程，反而抬高理解成本。
  Tests "green if present, not red if absent" — skill scripts are mostly one-off tools; demanding unit tests is over-engineering that raises cost.

> 底层逻辑仍是第一性原理：重构也要花理解成本。只对「正在被修改、因而修改风险本就升高」的代码投资清理，才划算；对无人碰的代码提前重构，是净亏。
> Same first principle: refactoring also costs comprehension. Only invest cleanup in code *already being modified* (where change risk is already high); pre-refactoring untouched code is a net loss.

## 判据不是清单 / Criteria, not a checklist

收尾必须点明：红的全修；黄了只要「注释说清 + 范围可控」就先留着；绿的出现说明干净。同一处若「为清单而清单」反而是脏的。本 skill 只读不改——若要落地修复，另开一轮按优先级逐个 PR。
Closing note: fix all red; keep amber if "comment + scoped"; green means clean. Checklist-for-its-own-sake is itself dirty. This skill reads only — for fixes, open a separate prioritized pass.

## 交付物 / Deliverables

- 把交互清单复制到**当前 agent 工作区根目录**作为可反复使用的副本：中文 → **`assets/clean_code_checklist.html`**（命名 `clean_code_checklist.html`）；英文 → **`assets/clean_code_checklist.en.html`**（命名 `clean_code_checklist.en.html`）；按《语言选择》的模式选。下次审计直接打开它打勾。
  Copy the interactive checklist to the **workspace root** for reuse: Chinese → **`assets/clean_code_checklist.html`** (as `clean_code_checklist.html`); English → **`assets/clean_code_checklist.en.html`** (as `clean_code_checklist.en.html`); pick per the Language mode. Open it next audit to tick.
- 把审计报告写到**当前 agent 工作区根目录** `clean_code_audit_<target>.md`，并调用 `present_files` 把该文件（及清单）呈现给用户预览。
  Write the audit report to the **workspace root** `clean_code_audit_<target>.md` and call `present_files` to preview it (and the checklist) for the user.
- 生成物（`clean_code_audit_*.md` / `clean_code_checklist*.html`）已被仓库 `.gitignore` 忽略，不进版本控制。
  Generated artifacts (`clean_code_audit_*.md` / `clean_code_checklist*.html`) are git-ignored, never version-controlled.

## 维护须知 / Maintenance Notes

  - 若今后在 `references/` 新增会读环境变量或调用二进制的脚本，必须同步在 `metadata.openclaw.requires.env` / `requires.bins` 声明（ClawHub 的 mismatch 审核红线）。当前本 skill 无任何此类依赖。
  If you later add a script that reads env vars or calls binaries, declare it in `metadata.openclaw.requires.env` / `requires.bins` (ClawHub's mismatch-audit red line). This skill has none today.
  - **声明与行为必须一致（Trust 红线）**：本 skill 的「只读」特指*被审计的代码*——它从不改动被审源码，但会写自身报告/清单产物。任何 frontmatter / 合规段的描述都须与此一致；若未来新增会写其他路径或读凭据的脚本，必须同步在 `metadata.openclaw.requires` 声明，避免 ClawHub 的「声明-行为 mismatch」审核命中。
    **Declared == behaved (Trust red line)**: "read-only" here means the *code under audit* — this skill never modifies the source it reviews, but it does write its own report/checklist artifacts. Every frontmatter / compliance statement must match this; if a future script writes other paths or reads credentials, declare it in `metadata.openclaw.requires` to avoid ClawHub's declaration-behavior mismatch audit.
  - **可选脚本 `scripts/metric_probe.py` 已评估并显式豁免 `requires`**：它是纯标准库 `ast` 解析、零网络、零凭据、只读，仅输出指标探针；**不读环境变量、不调用二进制**，故不触发 ClawHub 的 `requires` 声明义务（与导出脚本 `clean_code_clawhub_export.py` 不同——后者仅本地构建用，已被 `.clawhubignore` 排除）。**若该脚本未来触碰任一条件（读 env / 调二进制 / 写被审源码 / 联网），必须立即改为声明**，不得继续豁免。
    **Optional `scripts/metric_probe.py` is explicitly exempted from `requires` after assessment**: pure stdlib `ast`-based, offline, no credentials, read-only, emits metric hints only; it **reads no env and calls no binaries**, so it does not trigger ClawHub's `requires` declaration obligation (unlike `clean_code_clawhub_export.py`, which is build-only and excluded by `.clawhubignore`). **If it ever touches any of those conditions (reads env / calls binaries / writes audited source / goes online), it must be declared immediately** — no continued exemption.
- **主文件行数预算（硬闸）**：本文件目标 **≤215 行**、硬上限 **250 行**（渐进式披露是 C 维度的高分项，膨胀会反向扣分）。新增内容前先自查：能下沉到 `references/` 的就别留在主文件；超限须先把内容下沉再合入。
  **Main-file line budget (hard gate)**: target **≤215 lines**, hard cap **250 lines** (progressive disclosure is a strong C-dimension signal; bloat scores back). Before adding content, self-check: anything that can live in `references/` must not stay here; if over cap, push content down before merging.
- 多平台发布：源仓库 frontmatter 保留 `license: MIT` 供 SkillHub；ClawHub 导出副本由发布脚本剥离 `license` 字段并排除 LICENSE（见 `.clawhubignore`）。
  Multi-platform: the source keeps `license: MIT` for SkillHub; the ClawHub export strips the `license` field and excludes LICENSE (see `.clawhubignore`).
