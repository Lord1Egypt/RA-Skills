---
name: wiki-lint
description: Lint and health-check a persistent markdown knowledge wiki. Use when a user wants the agent to inspect a wiki for contradictions, stale claims, missing cross-links, orphan pages, duplicate pages, inconsistent naming, inconsistent frontmatter, schema drift, weak source attribution, or other maintenance issues. Best for Obsidian-friendly, plain markdown, or git-backed wikis that are maintained over time and need periodic cleanup or structural review.
---

# Wiki Lint

Inspect a markdown knowledge wiki for structural and content quality problems. Produce actionable findings that improve consistency, navigability, and trustworthiness without forcing unnecessary rewrites.

## Lint workflow

1. Inspect the wiki schema and top-level structure
2. Review `index.md` and `log.md` when available
3. Sample representative topic, entity, concept, source, and analysis pages
4. Identify the highest-value consistency and maintenance issues
5. Group findings by severity
6. Recommend concrete fixes
7. When asked, implement the highest-value fixes first

## What to look for

Check for:
- contradictions between pages
- stale claims superseded by newer material
- orphan pages with weak or missing inbound links
- duplicate pages with overlapping scope
- missing cross-links between obviously related pages
- important repeated concepts that still lack canonical pages
- broken naming conventions
- inconsistent frontmatter or page structure
- weak citation or source attribution
- analysis pages that should be linked from topic or entity pages but are not

## Output shape

Prefer a concise report grouped into:
- critical consistency issues
- important quality improvements
- optional structure improvements

For each issue, include:
- what is wrong
- why it matters
- the smallest useful fix

## Linting philosophy

Prefer gradual repair over massive rewrites. Follow existing conventions unless they are clearly harmful. If a larger schema change is justified, propose it before applying it.

## References

Read `references/lint-checklist.md` for a compact checklist and reporting pattern.
