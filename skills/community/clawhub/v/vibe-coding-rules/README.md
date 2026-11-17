# Vibe Coding Rules V2.5

> **AI 写代码最大的敌人，是它自己——它会忘记昨天修好的 Bug，会在同一个坑里反复跌倒。**
>
> 6 个会自我进化的 Skill，给 AI 装上"编程纪律"。改前自查 → 安全执行 → 改后自检 → 自动测试 → 变更记录。一条流水线，闭环交付。
>
> **AI's biggest enemy is itself — it forgets the bugs it fixed yesterday.**
> 6 self-evolving Skills that install "code discipline" into AI agents. Pre-check → Safe exec → Post-check → Auto-test → Changelog. Closed loop, every time.

---

## 🤔 为什么需要这个？/ Why do you need this?

用 AI 写代码的人都会遇到 / If you code with AI, you know these pains:

| 痛点 / Pain | 表现 / Symptom |
|:--|:--|
| 🧠 **AI 失忆 / Amnesia** | 昨天修好的 Bug 今天原样重现。改 B 模块时破坏 A 模块。<br>Bug you fixed yesterday? Back today. Fix module A, break module B. |
| 🔁 **重复踩坑 / Repeat Mistakes** | 同样的错误（`\|\|` 吞 0、select 假选中）犯了又犯。<br>Same traps (`\|\|` eats `0`, select pseudo-select) over and over. |
| 📝 **改完不知道改了什么 / No Trace** | 没有变更记录，不知道动了哪些文件、影响了什么。<br>No changelog. What did I touch? What did I break? |
| 🧪 **改完不知道坏了没有 / No Regression** | 改一行 CSS 导致整个页面挂了，手动回归太累。<br>One CSS line → entire page broken. Manual testing is exhausting. |
| 🗺️ **项目越大越迷路 / Lost in Code** | 打开一个文件，不知道它关联了谁、上次怎么改的。<br>Open a file. What's coupled to it? How was it last modified? |

**Vibe Coding Rules solves all of these.**

---

## 🛠️ 6 个 Skill 怎么工作 / How the 6 Skills work

```
                    ┌──────────────────────────────────────────┐
                    │         🥇 coding-principles             │
                    │    改前自查 / Pre-code: 5 principles      │
                    │    + 🍞 breadcrumb pre-scan               │
                    └──────────────┬───────────────────────────┘
                                   │
                    ┌──────────────▼───────────────────────────┐
                    │      🛡️ safe-terminal-executor           │
                    │    安全终端 / Safe terminal execution      │
                    │    timeout + guaranteed exit              │
                    └──────────────┬───────────────────────────┘
                                   │
                    ┌──────────────▼───────────────────────────┐
                    │         🔍 self-check                    │
                    │    改后自检 / Post-change: 28 rules       │
                    │    + 🍞 breadcrumb auto-seeding            │
                    └──────────────┬───────────────────────────┘
                                   │
                    ┌──────────────▼───────────────────────────┐
                    │        🧪 web-testing                    │
                    │    回归测试 / Regression: DOM+screen+OCR  │
                    │    auto browser testing                   │
                    └──────────────┬───────────────────────────┘
                                   │
                    ┌──────────────▼───────────────────────────┐
                    │        📝 changelog                      │
                    │    变更日志 / Changelog + growth detect   │
                    │    what changed + what was learned        │
                    └──────────────┬───────────────────────────┘
                                   │
                              git commit
                              ✅ Closed Loop
```

---

### 🥇 coding-principles — 改前五大原则 / Pre-Code 5 Principles

> **在 AI 输出代码之前，强制它先过一遍脑子。**
> **Forces AI to think before spitting out code.**

| 原则 / Principle | 问什么 / What it checks |
|:--|:--|
| 🍞 **Breadcrumb Pre-scan** | 打开文件先看 🍞 头部——这个文件关联了谁？（V2.5）<br>Read 🍞 header first — what's coupled to this file? |
| 1️⃣ **Think First** | 我真的理解问题了吗？确定在改正确的文件？<br>Do I understand the problem? Am I touching the right file? |
| 2️⃣ **Subtract First** | 能不能删代码解决？是不是在过度工程化？<br>Can deletion fix this? Am I over-engineering? |
| 3️⃣ **Surgical Change** | 只改必须改的，有没有碰了无关代码？<br>Minimal change. Did I touch anything unrelated? |
| 4️⃣ **It Must Run** | 改完能跑吗？JS + CSS + Template 三端都检查了吗？<br>Does it run? JS + CSS + Template — all checked? |

+3 个常见陷阱自动拦截 / +3 auto-trap detection：`\|\|` eats `0` / select pseudo-select / POST hardcoded fields

---

### 🛡️ safe-terminal-executor — 安全终端 / Safe Terminal

> **禁止裸跑网络命令。所有 curl/wget 包裹成 Node 脚本——超时保护、强制退出、日志留存。**
> **No bare network commands. All curl/wget wrapped as Node scripts — timeout protection, guaranteed exit, log output.**

You will never see an AI curl request hanging for 5 minutes again.

---

### 🔍 self-check — 改后 28 条自检 + 🍞 面包屑 / Post-Change 28-Rule Check

> **代码改完不是结束。28 条规则逐项检查，三条信任轨道自动化。**
> **Code change isn't done. 28 rules checked. 3 trust tiers. Fully automated.**

| 轨道 / Tier | 行为 / Behavior | 累积后 / Promotes at |
|:--|:--|:--|
| Tier 0 Observation | 仅记录不阻断 / Record only | — |
| Tier 1 Soft Rule | 警告，可放过 / Warn, skippable | Confidence ≥ 3 |
| Tier 2 Hard Rule | 阻断，必须修 / Block, must fix | Confidence ≥ 5 |

**规则会自动生长**——今天踩的坑，明天变成 AI 不能再犯的硬规则。误报过多自动退役，全程不需要人审核。
**Self-growing rules** — today's pitfall becomes tomorrow's hard rule. False positives auto-retire. Zero manual review.

---

#### 🍞 面包屑系统 — The Soul of V2.5

这是整套工具的**灵魂机制**。改代码时 AI 会在文件头部自动播种"面包屑"：
This is **the soul** of the entire toolkit. AI auto-plants breadcrumbs in file headers:

```markdown
<!-- 🍞 BREADCRUMBS
@COUPLED: chat-core.js, wf-builder.js
📖 Docs: dev-docs/architecture/chat.md
@GOTCHA: State machine resets in openTab(), sync tab order changes
@BUGFIX: 2026-07-01 Fixed mobile overflow layout collapse
-->
```

- **改前扫描 / Pre-scan**：AI 打开文件先读 🍞，知道耦合关系和历史坑位<br>AI reads 🍞 header first — knows couplings & past pitfalls
- **改后播种 / Post-seed**：改完自动更新 🍞，下次 AI 不再失忆<br>Auto-updates 🍞 after changes — AI never forgets again
- **四环闭环 / 4-Loop Closure**：改代码 → 自检 → 更新文档 → 播种面包屑 → 下次改代码时有完整地图<br>Code → Check → Doc update → Seed breadcrumb → Next time has full map

---

### 🧪 web-testing — 自动化回归测试 / Auto Regression Test

> **改完代码自动打开浏览器，跑 DOM 断言 + 截图 + OCR 文字验证。**
> **Auto-opens browser after changes. DOM assertion + Screenshot + OCR text verification.**

| 检测方式 / Method | 做什么 / What it does |
|:--|:--|
| DOM 断言 / DOM Assertion | 关键元素在不在？按钮能不能点？<br>Key element present? Button clickable? |
| 截图对比 / Screenshot Diff | 跟上次截图比，布局有没有崩？<br>Layout broken vs. last screenshot? |
| OCR 验证 / OCR Check | 页面上的文字对不对？<br>Text on page correct? |

改一行 CSS 不会悄无声息地炸掉整个页面。
One CSS line won't silently destroy your entire page.

---

### 📝 changelog — 变更日志 + 生长检测 / Changelog + Growth Detection

> **每次交付自动记录：改了什么、学了什么、规则有没有进化。**
> **Auto-records every delivery: what changed, what was learned, did rules evolve.**

| 内容 / What | 说明 / Details |
|:--|:--|
| 改动概述 / Changes | 改了哪些文件、新增/删除行数<br>Which files, lines added/removed |
| 新增依赖 / New Deps | 是不是加了新包<br>New packages installed? |
| 自检结果 / Self-Check | 28 条规则通过了多少<br>28 rules — how many passed? |
| 生长事件 / Growth | 今天有规则从观察池晋升到硬规则了吗？<br>Any rule promoted from observation to hard today?

---

### 🚀 pipeline-init — 一键初始化 / One-Click Bootstrap

> **新项目：对话式问答 → 自动创建流水线 → 开箱即用。**
> **New project: conversational Q&A → auto-create pipeline → ready to go.**

你说"我要做一个 XX 项目"，AI 问 4 个问题（项目名/技术栈/类型/要不要自动测试），一分钟搭好全部质量基础设施。
Say "I want to build X." AI asks 4 questions (name/stack/type/auto-test?). One minute. Complete quality infra deployed.

---

## 📦 安装 / Install

```bash
# Windows
install.bat

# macOS / Linux
chmod +x install.sh && ./install.sh

# PowerShell
.\install.ps1
```

支持 **CodeBuddy / Cursor / Windsurf** 三种 AI Agent。

---

## 🎯 谁需要这个？/ Who is this for?

| 如果你 / If you | 你需要这个因为 / You need this because |
|:--|:--|
| 🐣 **用 AI 写代码但不懂编程 / AI-coder, non-programmer** | 这是你的"编程纪律外骨骼"，AI 不再瞎改<br>Your code-discipline exoskeleton. AI stops reckless edits. |
| 💻 **独立开发者 / 一人公司 / Solo dev** | 你是你自己的 QA，这 6 个 Skill 就是你的 QA 团队<br>You ARE your own QA. These 6 Skills ARE your QA team. |
| 🏢 **小型团队用 AI 辅助 / Small team + AI** | 统一代码质量标准，减少 Code Review 成本<br>Unified quality standard. Less code review overhead. |
| 🤖 **重度 AI Agent 用户 / Heavy AI agent user** | 你的 Agent 越用越聪明——规则自生长，不遗忘<br>Your agent gets smarter over time. Rules grow. Nothing forgotten. |

---

## 📖 作者的故事 / Author's Story

**I don't know how to code. Not a single line.**

45 days. Pure AI coding tools. Built a **140,000-line**, 3-platform (Web + Desktop + MiniApp) product from scratch — [躺不平联盟 (TangBuPing)](https://tangbuping.com), an AI knowledge democracy platform.

The biggest pain wasn't AI failing to write code. It was **AI forgetting what it wrote**. Bug fixed yesterday? Back today. Module A fixed, Module B destroyed.

3 months of battle scars, distilled into these 6 Skills. Open-sourced so you don't have to bleed the same way.

**躺不平不是卷，是让其他人也躺不平。**
*We don't hustle harder. We make it so others can't stay lying down either.*

---

## 🔗 链接 / Links

- 🏠 [躺不平联盟](https://tangbuping.com)
- 🐙 [GitHub Profile](https://github.com/Ron-dali)

## 📄 许可 / License

Apache 2.0 — Free to use, modify, distribute. 自由使用、修改、分发。
