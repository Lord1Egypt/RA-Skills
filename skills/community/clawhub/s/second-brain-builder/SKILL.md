---
name: second-brain-builder
description: Expand, compile, and write back the user's second brain around a knowledge point. Use when the user gives a topic/concept and asks to 拓展, 编译, 沉淀, 扩充, 构建, enrich, research, or update their second brain with precise definitions, intellectual lineage, originators, related concepts, recommended papers/books, and AI-annotated note edits.
---

# Second Brain Builder

## Overview

Use this skill to turn a knowledge point into durable second-brain material: a precise concept page, a lineage map, related knowledge links, and a source-backed reading path. Default to Chinese unless the user asks otherwise.

The skill is allowed to write back when the user explicitly invokes it with a topic or asks to expand/build/update the second brain. All AI-generated edits to second-brain files must be marked with `AI 注`.

## Operating Principles

- Prefer the user's local second brain before public web material.
- Preserve the user's original notes. Make additive edits by default.
- Keep expansion bounded: one central concept, 5-12 related concepts, and a curated reading list before deeper recursion.
- Separate fact, interpretation, and recommendation.
- Use primary or high-quality sources for origin claims, papers, books, and "who proposed this" claims.
- Do not invent papers, books, people, dates, or source links.
- If source quality is weak, write the uncertainty into the `AI 注`.

## Workflow

1. Resolve the target.
   - Extract the exact knowledge point from the user's request.
   - Identify aliases, Chinese/English terms, adjacent meanings, and likely false friends.
   - If the topic is ambiguous enough to cause wrong writeback, ask one concise clarification question. Otherwise proceed with a stated assumption.

2. Locate the second-brain root.
   - Prefer `SECOND_BRAIN_WIKI_ROOT` when set.
   - Otherwise try `$SECOND_BRAIN_ROOT/llm-wiki` when `SECOND_BRAIN_ROOT` is set.
   - Otherwise try common local candidates such as `~/Hbrain/llm-wiki`, `~/Hbrain`, `~/gbrain`, the current workspace, and obvious `llm-wiki` folders.
   - If no root is found, produce a research packet only and ask where to write it.

3. Recall existing local context.
   - Search filenames and note content for the exact topic, aliases, and related terms.
   - Prefer `rg` for file search.
   - When available, run focused recall:

```bash
gbrain search "<exact topic>" --limit 8
gbrain search "<close alias or English term>" --limit 8
cm context "<exact topic>" --json --limit 8 --history 5
```

4. Research the concept.
   - For stable concepts, still verify origin, canonical definitions, and recommended readings with reliable sources.
   - For recent, contested, or recommendation-heavy requests, browse public sources and cite them.
   - Prefer primary sources, original papers/books, author pages, publisher pages, university pages, encyclopedias, and peer-reviewed surveys.
   - Use `references/research-packet.md` when producing a full concept packet.

5. Build the concept packet.
   - Precise concept: one tight definition plus boundary conditions.
   - Background: the problem situation that made the concept necessary.
   - Lineage: predecessors, proposer(s), first use or canonical formulation, later development.
   - Structure: components, mechanism, assumptions, and failure modes.
   - Related knowledge: parent concepts, sibling concepts, contrasting concepts, applied domains.
   - Reading path: 3-7 essential papers/books, ordered from entry point to primary/canonical sources.
   - Second-brain fit: how this concept connects to the user's existing notes, anchors, questions, or projects.

6. Decide write targets.
   - Follow existing directory conventions when the wiki already has them.
   - Prefer `concepts/<topic-slug>.md` for durable concept pages.
   - Prefer updating an existing concept page over creating a duplicate.
   - Add related links to existing anchor/index pages only when the connection is strong.
   - Create related concept stubs only when they are clearly useful; keep stubs short and marked with `AI 注`.

7. Write back with AI annotation.
   - Before editing any second-brain file, read `references/writeback-policy.md`.
   - Every inserted AI-generated block must be under a heading or prefix containing `AI 注`.
   - Preserve frontmatter and user-authored content.
   - Update `updated` dates only if that is already local convention; do not force new metadata patterns.

8. Report the result.
   - List files created or changed.
   - Summarize the core concept in 3-5 bullets.
   - Include the strongest sources used.
   - Name uncertainty, missing local context, or suggested next expansion topics.

## Recursion Policy

Do not explode the graph. After the first concept is expanded, propose the next 3-5 best expansion targets instead of automatically expanding every related concept. Automatically expand one more hop only when the user explicitly asks for recursive expansion.

Use this priority order for next topics:

1. Concepts required to understand the central concept.
2. Concepts that appear repeatedly in the user's existing second brain.
3. Contrasting concepts that sharpen the boundary.
4. Originator or canonical-work pages when the person/book/paper is central.
5. Application concepts tied to the user's current projects.

## Quality Checklist

- The definition is specific enough to exclude nearby but different ideas.
- The origin/proposer claim has a source or is marked uncertain.
- The reading list contains real works with author/title/year where available.
- The note connects to at least one local file, anchor, or explicit user interest when local context exists.
- The writeback is additive and visibly marked with `AI 注`.
- The final response tells the user exactly what changed.
