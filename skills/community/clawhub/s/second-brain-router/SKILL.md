---
name: second-brain-router
description: Standalone lightweight router for a personal second-brain loop. Use when the user asks knowledge, judgment, writing, reflection, decision, AI-agent, product, learning, or long-term thinking questions. It maps the question to cognitive anchors, recalls local knowledge and experience context, answers, and optionally writes back to the right wiki layer.
version: 1.1.0
author: Haidong + AI Agents
license: MIT
metadata:
  hermes:
    tags: [second-brain, router, anchors, gbrain, cass, wiki]
    category: knowledge-management
---

# Second Brain Router

## Purpose

This is a standalone lightweight trigger skill for a personal second brain.

It routes a user question through cognitive anchors, local search, and experience memory without loading a large wiki-maintenance skill by default. It can be shared as one skill because it includes the minimum writeback protocol itself.

## Expected Vault Shape

Assume a Markdown wiki or vault with these optional paths:

- `my-core-questions.md` — long-term questions
- `links/index.md` — cognitive anchor index
- `links/*.md` — `type: anchor` cognitive anchor pages
- `concepts/` — stable concepts
- `queries/` — reusable answers and saved question explorations
- `practices/` — action routines and workflows
- `_meta/automation-runs/` — automation reports

For Dongge's machine, default paths are:

- Hbrain repo: `/Users/jianghaidong/Hbrain`
- Wiki root: `/Users/jianghaidong/Hbrain/llm-wiki`
- Anchor index: `/Users/jianghaidong/Hbrain/llm-wiki/links/index.md`

If these paths do not exist, infer the local wiki root from the current project or ask one concise question.

## Trigger Classifier

Classify each user request:

1. `ordinary`: answer normally; do not run the second-brain loop.
2. `anchor-worthy`: run the lightweight second-brain loop.
3. `writeback-needed`: run the lightweight loop, then write back only if the user explicitly requested saving/updating.

Use `anchor-worthy` when the user asks about:

- understanding, judgment, strategy, reflection, decision, writing, output, or review
- AI agents, coding agents, second brain, personal knowledge systems, memory, CASS, Gbrain, wiki
- cognition, metacognition, long-termism, compounding, feedback loops, self, no-self, meaning
- any long-term core question in the user's vault

Stay `ordinary` for simple commands, transient facts, basic calculations, or code tasks unrelated to the knowledge system.

Use `writeback-needed` only when the user says or clearly implies: save, write to wiki, update anchor, create page, preserve this, 沉淀, 保存, 写入 wiki, 更新锚点, 创建页面, 整理到第二大脑.

## Lightweight Loop

For `anchor-worthy` and `writeback-needed` requests:

1. Read only lightweight routing files when they exist:
   - `my-core-questions.md`
   - `links/index.md`
2. Select 1-3 likely anchors from `links/*.md`.
3. Read only those selected anchor pages.
4. Run focused recall when available:
   - `gbrain search "<user question>" --limit 5`
   - `gbrain search "<anchor name>" --limit 5`
   - `cm context "<user question>" --json --limit 5 --history 5`
5. If a recall tool fails or is unavailable, continue and state the failure briefly.
6. Answer using:
   - the user's first-brain framing
   - the anchor minimal model
   - retrieved local context
   - CASS/experience lessons when available
7. Decide whether to write back or propose a writeback.

Do not read the whole wiki index, full log, full schema, large references, or raw sources during the lightweight loop.

## Minimal Anchor Template

When explicitly creating or normalizing an anchor, use:

```markdown
---
title: Anchor Name
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: anchor
tags: [anchor, contact-point]
sources: []
weight: 0
last_active: null
core_questions: [Q1]
status: active
---

# Anchor Name

## 一句话理解

## 我的大脑里必须记住的最小模型

## 什么时候调用它

## 连接到第二大脑

## 常用提问

## 最近调用记录

## 下一步要补的连接
```

## Writeback Rules

Default to no file edits.

If the user explicitly asks for writeback, first choose the target layer:

- `links/` for cognitive anchors
- `concepts/` for stable ideas
- `queries/` for reusable answers
- `practices/` for action routines
- `_meta/automation-runs/` for automation reports
- CASS/playbook only for repeated agent workflow lessons

Keep writeback small and auditable:

1. Read the target file if it exists.
2. Preserve existing content and frontmatter.
3. Add only the smallest durable update.
4. Bump `updated` dates when editing wiki pages.
5. Add or propose an index/log update when the local wiki convention requires it.

Never delete, rename, migrate, publish, send external messages, edit raw source files, or handle sensitive raw data without explicit user confirmation.

## Routing Receipt

For every `anchor-worthy` or `writeback-needed` answer, include a concise receipt:

```text
第二大脑回路：
- 模式：anchor-worthy / writeback-needed
- 长期问题：Q?
- 锚点：[[links/...]], [[links/...]]
- 召回：Gbrain / CASS / anchor-only / unavailable
- 写回：不需要 / 建议 / 已按要求写入
```

If the request is `ordinary`, do not include the receipt unless the user asks whether the loop was used.

## Anti-Patterns

- Do not load a heavy wiki-maintenance skill by default.
- Do not do full-vault scans for ordinary questions.
- Do not create wiki pages just because a question is interesting.
- Do not hide recall failures; short transparency is better than pretending the loop ran.
- Do not answer as generic internet knowledge when a relevant anchor exists.

