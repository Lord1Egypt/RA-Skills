# Article Templates

These templates define the structural skeleton for each article type. Use them as starting outlines for the writing step. Each template includes:

- Frontmatter schema
- Section structure with purpose and word count target
- Writing notes per section
- A filled example outline

---

## How Templates Are Used

During `forge write` or `forge draft`, after topic selection the agent selects the appropriate template based on article type. The template becomes the outline scaffold — each section is then filled in with researched content and shaped to the author's voice profile.

The agent may deviate from the template when content demands it, but section count and purpose should remain close.

---

## Template 1: 资讯 (News / Updates)

**Purpose:** Report on a recent development, product release, or industry event. Fast to write. Auto-publishes.

**Target length:** 800–1500 characters (Chinese)

**Frontmatter:**
```yaml
title: ""          # ≤ 26 chars; include the news subject
type: 资讯
date: YYYY-MM-DD
tags: []
```

### Section Structure

| # | Section | Purpose | Target chars |
|---|---------|---------|-------------|
| 0 | **开篇** (no heading) | Hook + core news in 2–3 sentences. What happened? Why does it matter right now? | 150–200 |
| 1 | **背景** | Brief context: what was the situation before this news? Reader needs ≤ 3 sentences to understand the significance. | 200–300 |
| 2 | **核心内容** | The actual news, broken into 3–5 bullet points. Facts, figures, quotes. Cite sources inline. | 300–500 |
| 3 | **影响与解读** | What does this mean for the reader's work / industry? 2–3 paragraphs of analysis. | 200–350 |
| 4 | **结语** | 1–2 sentences. Either a forward-looking statement ("接下来值得关注…") or a question for the reader. | 80–120 |

### Writing Notes

- Use **past tense** for events, **present tense** for implications
- Lead with the most newsworthy fact — don't bury the lede
- Citations: use format `据[来源]报道` or `根据[来源]数据`
- No H3 subheadings needed — this is a short-form piece

### Example Outline (Filled)

```
标题：OpenAI发布GPT-4 Turbo：上下文扩至128K

开篇：
OpenAI在开发者大会上宣布GPT-4 Turbo，上下文窗口从8K扩展到128K，
相当于一本完整技术书籍。对开发者意味着什么？

背景：
GPT-4自2023年3月发布以来，上下文限制（8192 tokens）是最常见的开发者投诉之一。
长文档分析、代码库问答都受此制约。

核心内容：
• 上下文窗口：128K tokens（约100,000字）
• 定价下调：输入降低3倍，输出降低2倍
• 知识截止日期更新至2023年4月
• 新增JSON模式，保证结构化输出
• 函数调用支持多函数并行

影响与解读：
对RAG架构的冲击：更大上下文窗口意味着部分场景无需向量数据库…
对成本的影响：按照新定价计算，处理一本书只需约…

结语：
128K上下文是迈向"无限上下文"的重要一步，但这真的解决了企业用户的痛点吗？
```

---

## Template 2: 周报 (Weekly Roundup)

**Purpose:** Curate and summarize the week's most important items in a domain. Consistent, repeatable format. Auto-publishes.

**Target length:** 1000–2000 characters

**Frontmatter:**
```yaml
title: ""          # Pattern: "[Domain]周报 | 第X期"  e.g. "AI周报 | 第42期"
type: 周报
date: YYYY-MM-DD
issue_number: 42
tags: []
```

### Section Structure

| # | Section | Purpose | Target chars |
|---|---------|---------|-------------|
| 0 | **卷首语** (no heading) | 1 short paragraph. The week's mood, a key theme, or an editorial take. Personal voice. | 100–150 |
| 1 | **本周要闻** | 3–5 top news items. Each item: bold headline, 2–3 sentences of context + significance. | 400–600 |
| 2 | **工具 & 资源** | 3–5 tools, repos, articles, or resources worth bookmarking. Format: name → one-line description → why it matters. | 300–400 |
| 3 | **深度推荐** (optional) | 1 article, paper, or podcast worth reading in full. 2–3 sentences on why. | 100–150 |
| 4 | **一句话观点** | 3–5 short, punchy takes on the week. Format: `💬 "观点内容"` | 150–200 |
| 5 | **下周关注** | 2–3 things to watch next week (events, launches, deadlines). | 80–120 |

### Writing Notes

- **Consistency is key**: the format should be identical every week — readers learn to navigate it
- Emoji work well as section bullets in roundups (provides visual rhythm without headers)
- Each news item follows: `**[标题]**：事件描述。为什么重要：一句分析。`
- Use `🔗 原文链接：[URL]` format for citations (links aren't clickable but readers can find them)
- First-person plural acceptable ("我们关注到…", "本周值得关注的是…")

### Example Outline (Filled)

```
标题：AI工具周报 | 第18期

卷首语：
这一周，模型越来越便宜，工具越来越多，但真正落地的产品还是那几个。
精心挑了五条值得你花时间的内容。

本周要闻：
**Mistral发布Mixtral 8x7B**：首个开源MoE架构大模型正式发布，
性能对标GPT-3.5，可本地运行。意味着：高质量本地LLM时代真的来了。

**Google Gemini Ultra泄露跑分**：内部跑分显示Gemini Ultra在多个
基准上超过GPT-4。但：跑分和实际体验差距有多大，还待观察。
…

工具 & 资源：
• **Continue** (VS Code插件) → 接入本地LLM的AI编程助手，完全免费
• **LlamaIndex v0.9** → RAG框架重大更新，支持多模态检索
…

下周关注：
• OpenAI DevDay第二季？据传下周有新发布
• Anthropic Claude 3发布计划时间窗口临近
```

---

## Template 3: 教程 (Tutorial / How-To)

**Purpose:** Teach the reader to do something specific, step by step. High value, strong SEO. Requires user review before publish.

**Target length:** 1500–3000 characters

**Frontmatter:**
```yaml
title: ""          # Pattern: "X分钟学会[技能]" or "手把手教你[做Y]"
type: 教程
date: YYYY-MM-DD
difficulty: 入门 | 进阶 | 高级
tags: []
```

### Section Structure

| # | Section | Purpose | Target chars |
|---|---------|---------|-------------|
| 0 | **开篇** (no heading) | Hook: the pain point this tutorial solves. "如果你曾经遇到过X问题…" | 150–200 |
| 1 | **你将学到什么** | Bullet list: 3–5 concrete skills/outcomes. Sets expectations. | 100–150 |
| 2 | **前提条件** | What the reader needs before starting. Keep it minimal. | 80–120 |
| 3 | **[Step 1 名称]** | First major step. Include: explanation, code/commands (if applicable), expected result. | 300–500 |
| 4 | **[Step 2 名称]** | Second step. Same format. | 300–500 |
| 5 | **[Step 3 名称]** | Third step. | 300–500 |
| 6 | **常见问题 & 坑** | 3–5 things that commonly go wrong, with fixes. "踩坑记录" format resonates well. | 200–300 |
| 7 | **总结 & 下一步** | Recap what was learned. Point to related resources or advanced topics. | 100–150 |

### Writing Notes

- Use numbered steps within each H2 section (`1. 安装依赖`, `2. 配置环境变量…`)
- Code blocks: use triple backtick with language identifier — `wenyan-cli` converts to highlighted HTML
- "踩坑" sections are very popular — readers share relatable failure experiences
- Screenshots or diagrams go between steps: `[图：X的示意图]` as placeholder, then generate/insert
- Avoid assuming the reader knows anything beyond the stated prerequisites

### Example Outline (Filled)

```
标题：5分钟在本地运行Llama 3——M1 Mac和Linux通用

开篇：
想用大模型做实验，每次API费用都让你心疼？
Llama 3 8B在本地运行，RTX 3060就够，M1 MacBook也行。这篇教程从零开始。

你将学到什么：
• 用Ollama在本地部署Llama 3 8B/70B
• 通过命令行和Open WebUI界面使用
• 对话速度基准测试方法
• 4-bit量化配置，降低显存需求

前提条件：
• macOS (Apple Silicon) 或 Linux，8GB+ 内存
• 基础命令行操作
• 无需GPU（CPU推理较慢但可用）

Step 1：安装Ollama
安装Ollama是最简单的一步...
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```
…

Step 2：拉取Llama 3模型
…

常见问题 & 坑：
Q：运行时提示"out of memory"怎么办？
A：改用4-bit量化版本：`ollama pull llama3:8b-instruct-q4_0`…
```

---

## Template 4: 观点 (Opinion / Analysis)

**Purpose:** Share a clear stance on a topic, back it with reasoning, and provoke reader thinking. Highest sharing rate when done well. Always requires user review.

**Target length:** 1200–2500 characters

**Frontmatter:**
```yaml
title: ""          # Provocative or unexpected. Pattern: "[反直觉观点]" or "为什么[X]是个错误"
type: 观点
date: YYYY-MM-DD
tags: []
```

### Section Structure

| # | Section | Purpose | Target chars |
|---|---------|---------|-------------|
| 0 | **开篇** (no heading) | The bold claim or uncomfortable truth. State the thesis immediately. Don't hedge. | 150–250 |
| 1 | **为什么这是个重要问题** | Establish stakes. Why should the reader care about this question? | 200–300 |
| 2 | **主流观点是什么** | Steel-man the opposing view fairly. Shows intellectual honesty. | 200–300 |
| 3 | **但是——** | The pivot. Why the mainstream view is incomplete, wrong, or misses something. This is the core of the article. | 400–600 |
| 4 | **证据 & 案例** | Concrete evidence: data, case studies, anecdotes, expert opinions. Min 2 evidence points. | 300–400 |
| 5 | **我的结论** | Restated thesis with more nuance. What the reader should take away. | 150–200 |
| 6 | **留给你的问题** | 1–2 questions for the reader to reflect on. Drives comments. | 80–100 |

### Writing Notes

- **Never hedge in the title** — "也许"、"可能" in a title kills shareability
- The "但是——" section is where the author's true voice must shine — resist the urge to soften
- Use first person liberally in opinion pieces ("我认为", "我的判断是")
- Evidence section: cite with `据[来源]的数据` — don't just assert facts
- Closing question should feel genuinely open, not rhetorical

### Example Outline (Filled)

```
标题：停止用RAG，开始用Fine-tuning——你可能选错了方案

开篇：
过去一年，"RAG"成了AI工程师的口头禅。
几乎每一个企业AI项目，第一反应都是"先搭个RAG"。
这个直觉是错的。

为什么这是个重要问题：
RAG和Fine-tuning的选择决定了项目成本、效果上限和维护负担。
错误的选择意味着三个月后推倒重来……

主流观点是什么：
RAG支持者的逻辑清晰：无需训练、数据随时更新、成本低……
这个逻辑在很多场景下是正确的。

但是——：
RAG本质上是一个检索问题，不是一个理解问题。
如果你的核心需求是"模型用我的方式回答问题"……

证据 & 案例：
• 某金融公司的实验：RAG准确率62%，Fine-tuning后达到91%
• Anthropic 2024年报告中关于Fine-tuning适用场景的分析
…

我的结论：
RAG适合知识检索，Fine-tuning适合风格和能力塑造。
大多数企业需要的是后者，却都在做前者。

留给你的问题：
你的AI项目，核心瓶颈是"找到正确信息"还是"用正确方式表达"？
```

---

## Template 5: 科普 (Explainer / Education)

**Purpose:** Make a complex technical or conceptual topic accessible to a non-expert audience. Evergreen content. Requires user review.

**Target length:** 1500–3000 characters

**Frontmatter:**
```yaml
title: ""          # Pattern: "[复杂概念]，其实没那么难" or "一文搞懂[X]"
type: 科普
date: YYYY-MM-DD
tags: []
```

### Section Structure

| # | Section | Purpose | Target chars |
|---|---------|---------|-------------|
| 0 | **开篇** (no heading) | Validate the reader's confusion: "如果你也觉得X很难懂，那这篇文章是为你写的。" | 120–180 |
| 1 | **先说最简单的版本** | Explain the concept in 2–3 sentences, as if to a friend with no background. No jargon. | 150–200 |
| 2 | **为什么它重要** | Real-world context: where does this concept appear? Why does ignoring it cost something? | 200–300 |
| 3 | **拆解核心机制** | The actual explanation, built up step by step. Use analogy as the primary teaching device. | 400–700 |
| 4 | **一个真实例子** | Walk through one complete real-world example that illustrates the concept end-to-end. | 300–400 |
| 5 | **常见误解** | 2–4 things people wrongly believe about this topic, with corrections. | 200–300 |
| 6 | **延伸阅读** | 2–3 resources for readers who want to go deeper. | 80–120 |

### Writing Notes

- **The Feynman Test**: Can you explain it in simple terms? If not, the understanding isn't there yet
- Every H2 section should be self-contained — a reader who skips section 3 can still understand section 4
- Analogies are the primary tool; use 2–3 per article. Make them concrete and from daily life
- Avoid phrases like "众所周知" — they alienate readers who don't know
- A Mermaid diagram or hand-drawn-style illustration goes very well in section 3

### Example Outline (Filled)

```
标题：向量数据库，一文搞懂

开篇：
"我们用向量数据库"——这句话在AI创业公司里被说烂了。
但如果你问"向量数据库和普通数据库有什么区别"，很多人答不上来。
这篇文章用一个外卖员的例子说清楚它。

先说最简单的版本：
向量数据库是一种专门存储和搜索"相似性"的数据库。
普通数据库问："这条记录是否存在？"
向量数据库问："哪些记录和这条最像？"

为什么它重要：
每次你在某音搜视频、在电商搜"类似这个风格的连衣裙"……

拆解核心机制：
把每个概念想象成地图上的一个点……
[Mermaid图：二维空间中的向量相似度示意]

一个真实例子：
假设你有一个文档问答系统……

常见误解：
❌ 误解1："向量数据库就是替换MySQL的"
✅ 实际上：它们解决不同问题，通常配合使用……
```

---

## Selecting the Right Template

When the article type is not specified by the user, infer from context:

| Signal | Suggested Type |
|--------|---------------|
| "最新发布"、"刚刚"、"今天"、"宣布" | 资讯 |
| "本周"、"周报"、"roundup"、"盘点本周" | 周报 |
| "怎么做"、"教程"、"步骤"、"手把手" | 教程 |
| "我认为"、"观点"、"为什么X是错的"、"应该" | 观点 |
| "一文搞懂"、"什么是"、"入门"、"解释" | 科普 |

When ambiguous, default to **科普** (evergreen, broadly useful) and note the assumption.
