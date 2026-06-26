---
name: telegram-markdown-adapter
description: Adapt markdown-style replies into Telegram-friendly rich text without broken rendering. Use when the user prefers Markdown structure but the destination is Telegram, or when drafts contain headings, tables, nested lists, code fences, checklists, or other Markdown that Telegram will render poorly. Trigger for Telegram reply formatting, Telegram-friendly rewriting, converting Markdown to Telegram-safe output, or preserving Markdown clarity while avoiding raw Markdown artifacts. 将 Markdown 风格回复转换为 Telegram 友好的富文本格式，避免标题、表格、嵌套列表、代码块、任务列表等在 Telegram 中渲染异常。适用于用户偏好 Markdown 结构、但目标渠道是 Telegram，或需要把 Markdown 味道保留下来同时避免原始语法外露的场景。
---

# Telegram Markdown Adapter

Keep the structure and readability of Markdown, but output in a format Telegram actually renders well.

## 中文摘要 / 中文使用说明

这个技能的目标不是保留原始 Markdown 语法，而是保留 Markdown 的**结构感、层次感、可读性**，再把最终输出适配成 Telegram 真正适合阅读和渲染的形式。

适合这些场景：
- 用户喜欢 Markdown 风格回复，但当前渠道是 Telegram
- 回复里包含标题、表格、任务列表、嵌套列表、代码块等 Markdown 元素
- 希望消息看起来清楚、整齐、有结构，但不要出现大量未渲染的原始 Markdown 符号

默认策略：
- 先按 Markdown 结构组织内容
- 再根据 Telegram 场景自动选择更合适的最终表现形式
- 表格类内容优先在 `伪表格 / 卡片式 / Emoji 分栏式` 之间自动判断
- 如果不确定，默认使用可读性最稳的卡片式

## Core Rule

When the destination is Telegram, do **not** dump raw Markdown just because it looks nice in plain text. Rewrite it into Telegram-safe formatting while preserving the original structure and emphasis.

Prefer these goals in order:
1. Readability in Telegram
2. Structural clarity
3. Visual polish
4. Fidelity to original Markdown syntax

## Workflow

### 0. Default output posture

Unless the user explicitly asks for plain text, draft the reply in Markdown-like structure first, then adapt it for Telegram-safe rendering.

Default writing style:
- use bold section headers instead of raw Markdown headings when sending final Telegram text
- keep lists, spacing, and sectioning from Markdown
- preserve inline code for commands, paths, env vars, and identifiers
- prefer readable visual structure over literal Markdown syntax fidelity

### 1. Identify Markdown features that will break or degrade in Telegram

Watch for these problem patterns:
- ATX headings like `# Heading`
- Markdown tables
- task lists like `- [ ]`
- nested bullets deeper than Telegram renders comfortably
- fenced code blocks that are too long or too frequent
- inline HTML
- footnotes
- blockquotes stacked too heavily

If the original content uses these, adapt rather than preserve literally.

### 2. Convert to Telegram-safe structure

Use these conversions by default:

- `# Heading` → `**Heading**` on its own line, optionally with an emoji if it improves scanability
- `## Section` → `**Section**`
- horizontal rules → `───`
- Markdown tables → bullet lists or compact field/value lines
- task lists → `- [ ]` becomes `- 待办：...` or `- ☐ ...`
- checked items → `- ✅ ...`
- blockquotes → short lead-in lines, not layered `>` stacks
- long code fences → summarize first; keep raw code only when truly needed
- multi-column comparisons → split into repeated blocks instead of tables
- links → keep raw URLs visible when copy/paste matters; avoid Markdown link syntax if Telegram rendering is uncertain

If Telegram HTML mode or rich formatting is available through the runtime, prefer the subset that is widely supported and low-risk. Do not rely on fragile formatting tricks.
### 3. Keep Telegram output compact

Telegram reads better with short blocks.

Default style:
- short paragraphs
- bullets instead of dense prose
- one idea per bullet
- whitespace between sections
- avoid giant monolithic messages

If a reply is long, split it into 2–3 chunks naturally.

### 4. Preserve meaning, not syntax

Do not say things like:
- “Telegram doesn’t support this Markdown”
- “Here is a Telegram-compatible rewrite”

Just output the adapted version directly unless the user asks about the transformation itself.

### 5. Message splitting and fallbacks

When the reply is long, split naturally into multiple Telegram messages instead of forcing one giant block.

Preferred split order:
1. headline or answer first
2. detail second
3. optional code / appendix third

If a section would render awkwardly in Telegram:
- replace tables with repeated item blocks
- replace dense hierarchy with 2–3 bold section labels
- collapse low-value detail into a short summary
- move exact raw content into a compact code block only if fidelity matters

### 6. Telegram-specific reply conventions

For Telegram-facing final output:
- favor bold section labels over raw Markdown heading markers
- keep paragraphs short
- separate sections with blank lines
- prefer bullets over prose when scanning matters
- avoid markdown tables entirely
- avoid unnecessary escaping clutter
- when multiple links are present, keep each link on its own line or its own bullet for easy tapping

### 7. HTML mode guidance

OpenClaw's Telegram **message-tool sending path** supports HTML parse mode and falls back to plain text if HTML parsing fails. However, ordinary assistant reply rendering may not always preserve HTML parse mode. Therefore, HTML should be used selectively.

Prefer Telegram HTML when:
- the reply will be sent through the `message` tool
- section headings should be clearly bolded
- inline code, paths, env vars, or commands matter
- links should render cleanly without MarkdownV2 escaping pain
- the message is a structured notification, report, alert, or summary

Do **not** assume raw HTML will render correctly in ordinary direct assistant replies. For standard conversational replies, prefer Telegram-safe structured text unless the runtime path is known to support HTML parse mode.

Safe tag subset to prefer:
- `<b>`
- `<i>`
- `<u>`
- `<s>`
- `<code>`
- `<pre>`
- `<a href="...">...<\/a>`

Rules:
- keep to simple, shallow HTML
- escape raw `<`, `>`, and `&` when they are plain text
- do not rely on exotic tags or deep nesting
- avoid mixing Markdown syntax and HTML in the same rendered output
- if content is highly dynamic or tag safety is uncertain, fall back to Telegram-safe structured text
- for normal assistant chat replies, structured plain Telegram text remains the safe default

Use HTML as the preferred rich-text mode for Telegram **only when the send path is compatible**, especially via the `message` tool.
## Format Selection Heuristics

Choose the presentation style based on content shape, not personal habit.

### Style 1: monospace pseudo-table

Use when all of these are mostly true:
- the content is strongly comparative
- rows are few
- each cell is short
- alignment matters more than conversational tone
- the audience is reading status/config/parameter data

Good fits:
- configuration snapshots
- model parameter comparisons
- short status matrices
- version / state / value grids

Avoid when:
- one column contains sentence-length explanations
- many rows would make the block tall and heavy
- Chinese text width makes alignment unreliable

### Style 2: card blocks

Use when any of these are true:
- one or more fields are medium or long
- readability matters more than visual alignment
- the output is for explanation, reporting, or decision support
- mobile readability is the priority

This is the default fallback.

Good fits:
- daily reports
- problem lists
- option comparisons with explanations
- anything the user needs to actually read, not just scan

### Style 4: emoji column style

Use when all or most of these are true:
- the content is short and easy to scan
- Telegram-native vibe is desirable
- status/priority/health cues matter
- the output is more like a dashboard, quick summary, or progress panel

Good fits:
- quick status updates
- lightweight summaries
- group-chat friendly reports
- operational snapshots

### Default selection order

1. If strict comparison matters and fields are short → Style 1
2. If explanations are present or text is medium/long → Style 2
3. If the content is short, status-heavy, and scan-first → Style 4
4. If uncertain → Style 2

### Rich-text mode choice

When the reply is Telegram-bound and rich formatting helps, prefer this order:
1. **HTML mode** for `message`-tool sends, headings, inline code, links, and structured reports
2. **Structured plain Telegram text** for ordinary assistant replies when parse-mode compatibility is uncertain
3. Avoid raw MarkdownV2 unless there is a specific reason to use it

In practice:
- reports / alerts / dashboards sent via `message` → often HTML or Style 4
- explanatory blocks in ordinary chat replies → Style 2
- technical short comparisons → Style 1, usually inside `<pre>` if HTML mode is used through a compatible send path

## Preferred Formatting Patterns

### Pattern A: Sectioned explanation

Instead of raw Markdown:

```md
# Today
## What changed
- Item A
- Item B
```

Output like:

```text
**Today**

**What changed**
- Item A
- Item B
```

### Pattern B: Replace tables with blocks

Instead of:

```md
| Item | Status | Note |
|---|---|---|
| A | Done | OK |
| B | Blocked | Waiting |
```

Output like:

```text
**Item A**
- Status: Done
- Note: OK

**Item B**
- Status: Blocked
- Note: Waiting
```

### Pattern C: Report-style Telegram output

Use when sending updates, summaries, or operational reports.

```text
📊 标题

───

**一、分类**
- 事项 1
- 事项 2

───

**二、分类**
- 事项 3
- 事项 4

───

📌 下一步
- 动作 1
- 动作 2
```

## When to keep code formatting

Keep inline code for:
- commands
- paths
- IDs
- short config keys

Keep fenced code blocks only when:
- the code itself is the deliverable
- line breaks matter
- the user explicitly wants raw code

Otherwise, summarize and only include the critical snippet.

## Anti-Patterns

Avoid these in Telegram replies unless the user explicitly asks for raw Markdown:
- Markdown tables
- giant heading hierarchies
- deeply nested lists
- repeated fenced blocks
- decorative syntax that Telegram won’t render meaningfully
- literal raw Markdown when a cleaner Telegram rendering is obvious

## Quick Decision Rule

If the content is mainly:
- **status / summary / plan / comparison** → choose among Style 1 / 2 / 4 using the heuristics above
- **code / config / command output** → keep minimal code formatting
- **mixed** → explain in Telegram-friendly sections, then include only the necessary code snippet

When table-like data appears, do not default blindly. Decide like this:
- short, rigid, technical rows → Style 1
- explanation-heavy rows → Style 2
- short status rows for scanability → Style 4
- uncertain → Style 2

## Reference

Read `references/telegram-format-rules.md` when you need concrete conversion rules and examples for headings, tables, checklists, code, and long replies.
