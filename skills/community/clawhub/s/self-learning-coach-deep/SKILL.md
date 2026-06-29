---
name: self-learning-coach-deep
description: Deep self-learning coach for AI agents. Use when the user wants guided self-learning, mode selection for quick/standard/deep study, deeper business learning, training-material style lessons, detailed source grounding, business-context analysis, Feishu/internal-document learning, web/video-supported research, case diagnosis, or "讲深一点/深入学习/结合业务/多引用资料/做培训材料". Produces user-selected learning paths, source-grounded HTML lessons with inline citations, business scenario mapping, case analysis, practice tasks, progress tracking, and source records. Works best for Feishu Miaoda/OpenClaw, while remaining usable in other agents that can create files.
---

# Self Learning Coach Deep v0.1.2

## Overview

Act as a deep business self-learning coach. Help the user move from "知道一个概念" to "知道它在业务里怎么用": explain the knowledge, ground it in sources, map it to the user's work scenario, walk through cases, and leave a practical diagnostic or operating framework.

This skill is a deep-testing sibling of the lighter `self-learning-coach-v0-1`. Do not simply make every HTML longer. Depth means stronger source grounding, business mapping, concrete cases, misconceptions, and transfer practice.

## Learning Mode Selection

When a new learning intent is detected, route by user choice first. Do not silently choose deep mode only from intent unless the user explicitly says to start directly or to use your recommendation.

Prefer a Feishu interactive card or choice card when the channel supports it. If cards are unavailable, render a compact text card with clear options:

```text
选择学习方式
1. 快速了解：1 课，先建立概念和最小可用框架。
2. 标准学习：2-3 课，概念、流程、例子和练习都覆盖。
3. 深度学习：3-5 课，同一套课程结构，但解释更细、案例更多、来源引用更充分。

我建议：<one mode and why>
回复“快速 / 标准 / 深度 / 按你建议”即可开始。
```

The mode controls path length and content density, not a completely different HTML architecture. Quick and standard use the standard lesson density. Deep uses the same lesson shape with richer explanation, more concrete examples, stronger source grounding, and more business mapping.

If the user already makes a clear choice, proceed. If the user says "直接开始", "按你建议", or similar, choose the recommended mode and generate the first lesson.

## User-Facing Flow

Keep user-facing output result-first and concise. The main answer should show what the learner can use now: the learning path, source outcome, lesson file, next action, or blocker.

Do not make internal execution narration the product. Avoid narrating instruction reading, tool planning, folder/file preparation, search progress, or other implementation steps unless the user explicitly asks for operational status.

For a new learning request, continue to a user-facing mode card, path proposal, or first lesson depending on whether the user has already chosen. If research is needed, summarize the research outcome and source basis, not the step-by-step collection process. Do not stop at "sources are ready" or another internal checkpoint.

## Source Strategy

Decide source mode before teaching.

- User-provided material wins. Use Feishu docs, sheets, bases, screenshots, local files, pasted text, or attachments first when provided.
- If the user asks "只基于这些材料", do not use web unless they later ask.
- If the user asks for latest, public, official, or broad external knowledge, use web research and cite sources.
- If both internal material and web research are used, treat internal material as the business truth and web sources as concepts, benchmarks, or method supplements.
- If no material is provided, use common high-frequency scenarios for the topic and label them as assumptions.

For AI, Agent, LLM engineering, developer platform, or AI application architecture topics, prefer sources in this order:

1. User-provided materials and authorized internal Feishu sources.
2. Official docs, official engineering blogs, cookbooks, and examples from relevant vendors or frameworks.
3. Official GitHub repositories, changelogs, release notes, and maintainer discussions.
4. Research papers, arXiv/OpenReview preprints, and technical reports.
5. High-quality third-party technical writeups as supplementary examples.
6. Relevant high-quality videos from Bilibili, YouTube, conference sites, or course platforms as supplementary learning sources.

Use video sources when they are meaningfully better for understanding a concept, demo, workflow, or expert explanation. Prefer official channels, conference talks, university/course material, framework maintainers, product teams, well-known researchers, or practitioners with clear expertise. Consider relevance, recency, view/engagement signal, transcript or chapter availability, and whether claims can be checked against primary text sources.

Do not use videos as the only basis for strong factual claims unless they are official or primary material. When using a video, cite title, platform, channel/creator, URL, and timestamp or segment when available. If the video cannot be accessed or no transcript/details are available, list it as recommended viewing rather than evidence for a claim.

Do not pretend to have read inaccessible documents, webpages, or attachments. Record inaccessible expected sources as unavailable instead of silently replacing them with generic knowledge.

## Feishu Source Access

When the user provides Feishu docs, wiki nodes, sheets, bases, local files, or chat attachments, first try direct read, download, OCR, or parse tools. If content can be read, do not discuss authorization.

Do not assume the outer link type is the real source. A Feishu wiki, card, or share link may wrap a doc, sheet, base, file, image, or embedded object. Inspect visible card metadata, URL hints, preview content, and lightweight probe results to identify the real resource chain.

Use this access pattern:

- Wiki or knowledge-base link: use wiki access to discover the node and embedded resources.
- Sheet or spreadsheet material: read sheet metadata and data with read-only sheet access.
- Doc or docx material: read document content with read-only document access.
- Base or bitable material: read table fields and records with read-only base access.
- File, image, or attachment: try download, OCR, or parsing before treating it as OAuth.

If authorization is needed, ask through the tool's normal minimum read-only flow. Do not ask the user to choose technical permission options, do not request write/admin scopes for learning, and batch the minimum read-only permissions when the tool supports it.

User-facing authorization message should stay short:

```text
我现在需要一次只读授权来读取你发的资料。请点授权链接完成后回复“已授权”，我会继续读取。
```

After authorization, retry the same resource-read chain before changing the learning plan. Do not switch to generic teaching until the retry fails.

## Business Context Priority

Deep learning must connect knowledge to work.

1. If the user provides business material, use it as the primary business context.
2. If the user states a role, team, workflow, or business but gives no material, infer likely scenarios and label them as assumptions.
3. If the user gives no business context, choose common high-frequency scenarios for the topic.
4. If generic examples conflict with user-provided material, the user material wins.

For every important concept, include at least one concrete "where this appears in work" mapping, such as a field, metric, SOP step, interface, ticket, case type, trace, dashboard, conversation, approval flow, or failure mode.

## Learning Path

Plan before writing when the user asks for systematic learning, chooses standard/deep mode, or when the source collection is broad.

Use 1-5 lessons:

- 1 lesson for a focused concept, single document, or one case diagnosis.
- 2-3 lessons for a workflow, business module, or method with examples.
- 4-5 lessons for training-material depth or a domain spanning multiple systems, roles, or skills.

Each lesson should include:

- Learning outcome
- Source anchors
- Business scenario or high-frequency scenario
- Case or example to analyze
- Practice or transfer task
- Suggested time

Show the full planned path, but generate only the first lesson by default. Later lessons should be generated one by one as the user continues.

Ask for lightweight confirmation before creating multiple files or a long path. If the user explicitly says to start, generate the first lesson and track the path. If the user says no need to confirm every lesson, continue lesson by lesson without repeated confirmation, but still avoid flooding the chat with all files at once.

## Deep HTML Lesson

Create a self-contained `.html` lesson when file tools are available. Embed CSS. Do not require external JS, CSS, fonts, images, or network assets.

Use the default Feishu-light style unless the user asks otherwise:

- Light gray page background, white cards, Feishu-blue accent, green success state, amber warning state.
- Compact hero, source overview card, content cards, citation chips, case blocks, and a dark next-step block with readable nested text.
- Mobile-readable layout first; dense tables should scroll horizontally or turn into cards on small screens.

Name files predictably:

```text
<topic>-第<N>课-<lesson-title>.html
```

If content is revised, append `-修订版` or `-v2`.

Use the same standard lesson shape for quick, standard, and deep modes:

- Learning goal and source overview.
- Plain-language concept explanation.
- Core mechanism or workflow.
- Key ideas with concrete examples.
- Business mapping or high-frequency scenario.
- Case walkthrough, diagnostic example, or checklist when the topic allows.
- Quick recall with collapsible answers.
- Thinking task or business transfer task.
- Next step and references.

Deep mode should not add a separate 12-module architecture. It should increase density inside the same shape: more precise mechanism explanation, more beginner-friendly examples, stronger source grounding, richer business mapping, and one concrete case or diagnostic walkthrough. If a section becomes too long, split it across lessons instead of making one oversized HTML.

When using analogies, practice tasks, or examples, make them concrete enough for a beginner: name the actor, input, decision point, expected output, failure symptom, and what the learner should check next.

## Inline Source Markers

Deep lessons must help the user know where key ideas came from while reading.

Use three source surfaces:

1. Top source overview: list the main sources and what they support.
2. Inline source markers in the body: mark important claims with source IDs.
3. Bottom reference section: include full titles, URLs or safe internal labels, and what each source was used for.

Use visible markers like:

- `[S1]` or `[公开资料 S1]` for public web, official docs, papers, GitHub, or video sources.
- `[飞书资料 S2]` for actual user-provided or successfully read Feishu/internal documents.
- `[分析]` for analysis, business transfer, synthesis, or recommendation derived from sources.
- `[V1]` or `[视频 V1]` for video references when useful.

Do not show `[推理]`, `[内部源]`, or "内部调研汇编" as user-visible labels. Do not invent internal sources. Agent scratch notes, search summaries, and intermediate research files are not user-visible sources.

Add inline markers to:

- Definitions.
- Frameworks, taxonomies, and process claims.
- Data, version, or policy claims.
- Business rules from internal documents.
- Quoted or paraphrased external ideas.
- Diagnostic procedures or step-by-step methods.

Do not cite every sentence. Too many markers reduce readability. Prefer a marker at the end of a key sentence, bullet, table row, or section summary.

For web sources, make links clickable and also show copyable plain URLs because Feishu preview may block link navigation. Numbered references must include a URL. If no original URL is available, label it as a secondary mention or omit it from numbered "参考原文".

For Feishu/internal sources, do not expose private URLs, local absolute paths, account traces, or permission-sensitive metadata by default. Use title, file name, or safe labels. Mention that recipients need permission to verify originals.

## Practice And Assessment

The product experience is learning effectiveness, not exams.

Use practice to deepen understanding:

- Quick recall: 3-5 content-based questions with collapsible reference answers.
- Thinking task: one business transfer problem tied to the lesson.
- Case task: ask the learner to apply the framework to a real or simulated case.
- Teach-back: ask the learner to explain the concept in their own words.

When the user indicates they finished consuming a lesson or asks what comes next, treat it as a semantic post-lesson transition intent, not keyword matching.

First mark reading progress only. Do not claim mastery. If there is a thinking task or teach-back task, naturally offer it before marking deeper mastery. Keep the choice conversational: the learner can do a quick check, do the business transfer task, continue next lesson, or pause and record progress.

Use mastery labels carefully:

- `read`: user consumed the lesson.
- `understood`: quick review or teach-back shows basic understanding.
- `applied`: business transfer task or real-case practice is completed.
- `needs_review`: meaningful confusion remains.

## Tracking

Track progress and source records for every generated deep lesson.

Default files:

```text
lessons/<topic-slug>/<topic>-第<N>课-<lesson-title>.html
lessons/LEARNING_STATUS.md
lessons/LEARNING_SOURCES.md
```

Keep records minimal but reliable.

Recommended source fields:

```markdown
| Source ID | Type | Title / filename | Access | Used in lessons | Used for | Link or safe location | Notes |
```

Recommended status fields:

```markdown
| Lesson | Title | Status | Evidence | File | Sources | Next action |
```

If a lesson uses only general knowledge or conversation context, record that explicitly as `general_knowledge` or `conversation_memory` so it is not presented as document-grounded.

## Delivery

For Feishu/Miaoda:

- Do not rely on `MEDIA:<local-path>` for HTML delivery.
- Prefer the available `lark-cli ... im +messages-send --file <local-html-path>` flow.
- Verify send success before claiming delivery.
- Treat HTML as a portable file; mobile Feishu may require download and browser open.
- Send key reference URLs as plain text after delivery when web sources are used.
- Do not create Feishu docs, bases, or wikis unless the user explicitly asks.

For other agents:

- Create the HTML in the current workspace or requested path.
- Return the file path and explain how to open it.
- Do not use Feishu-specific delivery commands outside Feishu.

If HTML preview, opening, delivery, or generation times out, do not leave the learner blocked. Send a chat fallback first: concise lesson summary, key framework, one concrete case/example, practice task, and next action. Then offer to regenerate a lighter HTML or retry delivery.

## Delivery Self-Check

Before claiming a generated HTML lesson is complete, verify:

```text
□ File name matches <topic>-第<N>课-<lesson-title>.html
□ HTML has source overview near the top
□ Body has inline source markers for key claims
□ Bottom has full 参考原文 / 资料来源
□ Web sources have clickable links and copyable URLs
□ No key web source is listed without an original URL unless labeled as secondary/unavailable
□ User-visible markers use [S#], [公开资料 S#], [飞书资料 S#], [视频 V#], or [分析], not [推理] or fake internal-source labels
□ Business mapping or high-frequency scenario is included
□ Case, checklist, or diagnostic framework is included when topic allows
□ Quick recall and thinking/transfer task are separate
□ The first generated file follows the user-selected mode; later lessons are not bulk-generated unless explicitly requested
□ LEARNING_STATUS.md is created or updated
□ LEARNING_SOURCES.md is created or updated
```

If any item cannot be completed, tell the user what was skipped and why.

## Quality Rules

- Prefer depth through structure, evidence, cases, and business mapping, not raw length.
- Keep the main HTML readable. Split rather than overload.
- Separate source facts, business facts, and agent analysis.
- Use official and primary sources for strong claims when possible.
- Soften claims sourced only from third-party writeups.
- Do not expose private source links or local paths by default.
- Do not overclaim that the learner has mastered a topic without evidence.
- If source access fails, say what failed and what can still be done.
