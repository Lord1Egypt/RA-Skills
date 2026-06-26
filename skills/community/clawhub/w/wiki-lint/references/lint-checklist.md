# Wiki Lint Checklist

Use this checklist when reviewing a markdown knowledge wiki.

## Structural checks

- Does the wiki have a clear schema or at least stable conventions?
- Is `index.md` still useful as a navigation map?
- Is `log.md` append-only and parseable?
- Are page names stable and human-readable?

## Content checks

- Do important pages start with a short summary?
- Are claims supported by source pages or clearly marked as synthesis?
- Are contradictions surfaced instead of smoothed over?
- Are outdated claims still presented as current?

## Linking checks

- Do major pages link to related concepts and entities?
- Are there orphan pages?
- Are there duplicate pages that should be merged?
- Are durable analysis pages linked from the pages they affect?

## Reporting pattern

```markdown
# Wiki Lint Report

## Critical consistency issues
- issue

## Important quality improvements
- issue

## Optional structure improvements
- issue
```
```

## Fix prioritization

Prioritize:
1. contradictions and stale claims
2. duplicate or ambiguous canonical pages
3. broken navigation and missing cross-links
4. cosmetic consistency improvements
