---
name: second-brain-aphorism
description: Generate grounded Chinese reflections, aphorisms, maxims, quote-card lines, article endings, daily thoughts, or short "感悟" from the user's second brain, GBrain, llm-wiki, cognitive anchors, notes, and long-term questions. Use when the user asks for 感悟、箴言、金句、短句、每日一念、一段话、文章结尾、卡片文案, or asks to distill an idea from 第二大脑, GBrain, llm-wiki, wiki, notes, anchors, or personal knowledge context.
metadata:
  slug: second-brain-maxim
  version: 0.1.1
  tags:
    - second-brain
    - gbrain
    - llm-wiki
    - aphorism
    - reflection
    - writing
    - knowledge-management
  openclaw:
    requires:
      bins:
        - gbrain
      env: []
    os:
      - linux
      - darwin
      - win32
  hermes:
    category: knowledge-management
    tags:
      - second-brain
      - gbrain
      - llm-wiki
      - aphorism
      - reflection
      - writing
---

# Second Brain Aphorism

Use this skill to turn the user's second-brain material into a concise, personally grounded thought. The result should feel like a distilled insight from the user's own thinking, not a generic inspirational quote.

Default to Chinese unless the user asks for another language.

## Workflow

1. Clarify the requested shape only when necessary.
   - If the user says "感悟", produce one short paragraph.
   - If the user says "箴言", "金句", or "短句", produce concise aphoristic lines.
   - If unspecified, produce one `感悟` and one compressed `箴言`.
2. Run lightweight second-brain recall.
   - Prefer the user's local second brain over web knowledge.
   - Resolve local paths without hardcoded personal information:
     - Prefer `SECOND_BRAIN_WIKI_ROOT` when set.
     - Otherwise try `$SECOND_BRAIN_ROOT/llm-wiki` when `SECOND_BRAIN_ROOT` is set.
     - Otherwise try common user-local candidates such as `~/Hbrain/llm-wiki`.
     - If no likely wiki root exists, infer it from the current project or ask one concise question.
   - Once the wiki root is found, use:
     - Core questions: `<wiki-root>/my-core-questions.md`
     - Anchor index: `<wiki-root>/links/index.md`
   - Read `my-core-questions.md` and `links/index.md` if they exist.
   - Select 1-3 relevant anchor pages from `links/*.md` and read only those pages.
   - Run focused recall when available:

```bash
gbrain search "<user's exact topic>" --limit 5
gbrain search "<selected anchor or close synonym>" --limit 5
cm context "<user's exact topic>" --json --limit 5 --history 5
```

3. Extract a "seed of tension" before writing.
   - Name the lived tension: what is being pulled against what?
   - Name the user's recurring anchor or long-term question.
   - Name the practical turn: what changes in how one sees, chooses, or acts?
4. Generate the line or paragraph.
   - Write from the recalled context, not from generic advice.
   - Prefer concrete verbs, precise nouns, and a small paradox.
   - Remove motivational filler, slogans, and abstract padding.
   - If the recall is thin, be transparent and write a lower-confidence draft.
5. Present the result.
   - For normal requests, output:
     - `感悟：` one paragraph, 80-180 Chinese characters
     - `箴言：` one line, 8-32 Chinese characters
   - For batch requests, give 3-7 numbered candidates.
   - Include a concise `第二大脑回路` receipt unless the user explicitly asks for copy-only output.

## Style Guide

Read `references/style-guide.md` when the user asks for a specific tone, more variants, quote-card copy, article endings, or when the first draft risks sounding generic.

## Grounding Rules

- Do not claim the user believes something unless it is supported by recall.
- Do not invent book titles, source notes, anchors, or personal experiences.
- Do not search the web unless the user explicitly asks for outside references.
- Do not write back to the second brain unless the user explicitly asks to save, archive, 沉淀, 写入, or update.
- If recall tools fail, continue with available anchor files and briefly state what failed.

## Writeback

Default to no writeback. When the user explicitly asks to save the result:

1. Choose the smallest durable target:
   - `queries/` for reusable generated answers or quote collections.
   - `concepts/` for a stable idea that should become a concept page.
   - `links/` only when updating an existing cognitive anchor.
   - `practices/` only when the output implies a repeatable routine.
2. Preserve existing frontmatter and content.
3. Add the generated line plus the recall receipt or source context.
4. Bump `updated` dates on edited wiki pages.

## Quality Checklist

- It can be traced to at least one recalled anchor, note, or core question.
- It says one thing sharply instead of three things vaguely.
- It contains a tension, reversal, or implication.
- It sounds like a private notebook becoming public for a moment.
- It remains useful even if stripped of decorative language.
