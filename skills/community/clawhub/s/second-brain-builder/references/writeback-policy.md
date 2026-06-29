# Writeback Policy

Use this policy before modifying any second-brain file.

## Non-Negotiables

- All AI-generated additions must visibly include `AI 注`.
- Do not rewrite, delete, or silently normalize user-authored content.
- Prefer appending a new `AI 注` block to editing existing prose.
- If a correction to existing text is necessary, add an `AI 注：更正建议` block explaining the issue and source instead of changing the original sentence.
- Preserve frontmatter, local link style, headings, and naming conventions.
- Keep each write small enough that the user can audit it quickly.

## Approved Annotation Forms

For a durable block:

```markdown
## AI 注：<主题>（<YYYY-MM-DD>）

<AI-generated content>

来源：<short source list or links>
可信度：高/中/低；<reason>
```

For a short inline addition:

```markdown
> AI 注（<YYYY-MM-DD>）：<one concise note> 来源：<source or local file>.
```

For a stub page:

```markdown
# <概念名>

## AI 注：概念存根（<YYYY-MM-DD>）

- 暂定定义：<definition>
- 为什么值得补：<connection to central topic>
- 待核实：<what remains unknown>
```

## Target Selection

- Existing matching page: append a dated `AI 注` section.
- Missing concept page: create a new concept page using the local naming convention.
- Index or map page: add links only when the relationship is strong and useful.
- Related concept stubs: create no more than 3 by default.

## Final Audit

Before reporting completion, verify:

- Every changed file contains `AI 注` in the AI-generated addition.
- No user text was removed.
- New links point to existing files or intentional stubs.
- Source claims are either cited or explicitly marked uncertain.
