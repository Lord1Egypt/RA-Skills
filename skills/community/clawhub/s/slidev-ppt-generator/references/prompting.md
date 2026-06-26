# Prompting Strategy

This reference file explains how `slidev-ppt-generator` should handle the boundary between "workflow rules" and "per-request style requirements."

## Layering Principle

- `SKILL.md` owns the fixed rules
- The user request owns the per-task variables

Do not hard-code aesthetic preferences that may change with every request into the skill.

## What Belongs in the Skill

- Must use the Slidev project workflow
- Install dependencies in the project directory, never globally
- Generate `slides.md` first, then preview, then export
- Run overflow, density, and hierarchy checks before exporting
- Avoid hollow table-of-contents slides, placeholder bullets, and consecutive slogan slides
- One main conclusion per slide

These define the quality floor and the execution path; they should remain stable.

## What the User Request Should Decide

- Chinese or English
- Topic and audience
- Slide count range
- Whether to export PDF / PPTX / HTML
- Leaning toward `formal` / `executive` / `technical` / `launch`
- Whether it resembles a launch event, client introduction, internal sharing, or architecture briefing

These are per-task variables and should not be hard-coded in the skill.

## Language Strategy

- Default to `auto`, following the primary language of the user's current message
- When the user explicitly requests English, the entire deck should be in English
- When the user explicitly requests Chinese, the entire deck should be in Chinese
- Do not default to English, and do not mix languages on the same slide
- If English proper nouns must be retained, ensure all other terminology remains consistent throughout the deck

## Official Theme Strategy

Let the skill choose from official themes first, rather than inventing new ones on the fly:

- `technical` -> `default`
- `formal` -> `apple-basic`
- `executive` -> `seriph`
- `launch` -> `apple-basic`

Only consider `bricks` or `shibainu` when the user explicitly wants a stronger personality.

Do not treat "search the web for a better theme" as a default step. For formal introduction decks, just pick the official theme per the mapping above.

## Structural Generation Constraints

- Prefer native Slidev Markdown syntax whenever possible
- For comparisons, prefer Markdown tables or card grids
- Avoid raw HTML tables; if you must use one, always include complete `thead` / `tbody`
- Avoid large, dense tables on a single slide -- this usually makes the deck look worse, not more professional

## Recommended Request Templates

### English

```text
Create a Slidev deck about OpenClaw.
Requirements:
- Language: English
- Tone: formal
- Length: 10-12 slides
- Deliverables: generate slides.md and export both PDF and PPTX
- Focus: architecture, workflow, use cases, and why local-first matters
```

### Chinese

```text
帮我用 Slidev 做一个关于 OpenClaw 介绍的 PPT。
要求：
- 语言：中文
- 风格：technical
- 页数：10-12 页
- 交付：生成 slides.md，并导出 PDF 和 PPTX
- 重点：讲清楚架构、工作流、适用场景和本地优先价值
```

## Generation Goals

- Let the skill guarantee "it won't be bad"
- Let the prompt decide "what it should look like this time"
- Prioritize a stable, professional, speakable deck first, then gradually add visual personality
