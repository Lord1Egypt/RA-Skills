# Report Template and SPEC Handoff

Phase 3 writes `design-review-{YYYYMMDD}.md` at the repo root. Phase 4 turns each approved finding group into a `write-specs` handoff packet.

## Report Structure

```markdown
# Design Review — {YYYY-MM-DD}

**Mode**: code review | lighthouse | both
**Scope**: {file globs reviewed} / {URLs measured}
**Tooling**: interface-guidelines (vendored from vercel-labs/web-interface-guidelines); Lighthouse {version} mobile+desktop

## Findings

### Accessibility
- `critical|high|medium|low` — `file:line` — rule — evidence — fix direction

### Performance (static)
…same pattern…

### Lighthouse — {URL}
| Metric | Run 1 | Run 2 | Run 3 | Target |
| --- | --- | --- | --- | --- |
| Performance | 82 | 85 | 84 | ≥95 |
| Accessibility | 97 | 97 | 97 | ≥95 |
| Best Practices | 96 | 96 | 96 | ≥95 |
| SEO | 100 | 100 | 100 | ≥95 |

- `high` — `lcp-breakdown-insight` — LCP 3.4s — element: `h1.hero`, `elementRenderDelay` 2.1s — waiting on `font-variable.woff2` (129KB) — fix: self-host + instance/subset
- `medium` — `color-contrast` — selector `.nav a` — insufficient contrast 3.1:1 — fix: token change or specificity fix

## Coverage

**Reviewed**: {n} files — {list or glob}
**Skipped**: {file} — {reason}
**Rules not applicable**: {categories}
**Not measured**: {URLs not measured and why — e.g., "localhost only, no deploy"}
**Caveats**: {e.g., "preview URL measured — production alias unconfirmed"}

## Finding Groups (proposed SPECs)

| # | Group | Findings | Max severity | Suggested SPEC |
| --- | --- | --- | --- | --- |
| 1 | Form accessibility | 12 | high | `SPEC-{YYYYMMDD}-form-a11y` |
| 2 | Font loading & LCP | 3 | critical | `SPEC-{YYYYMMDD}-lcp-fonts` |
| 3 | Image hygiene | 8 | medium | `SPEC-{YYYYMMDD}-image-dimensions` |
```

## Severity Rubric

| Severity | Meaning |
| --- | --- |
| `critical` | User-blocking or metric-destroying: unusable without keyboard/screen reader, LCP >4s, content invisible when JS fails, broken zoom |
| `high` | Standards violation with real user impact: missing labels, contrast failures, CLS-inducing images, no reduced-motion |
| `medium` | Degraded UX: missing hover/focus states, no URL state sync, hardcoded formats |
| `low` | Polish: typographic details (`…`, curly quotes), copy style |

## Grouping Rules for SPECs

- Group by **fix strategy**, not by file count — "all a11y label fixes in forms" is one group even across 8 files; "font loading" and "image preload" are separate groups even on one page.
- Each group must be independently shippable (one PR can fix it).
- Merge groups that share a root cause (e.g., missing `width`/`height` AND missing `loading="lazy"` on the same images → one "image hygiene" group).
- Never exceed ~15 findings per SPEC — split further by page/area if needed.

## SPEC Handoff Packet (per group)

Pass to `write-specs`:

```text
Audit: design-review-{YYYYMMDD}.md (findings #{ids})
Group: {name} — {n} findings, max severity {x}
Goal: {one sentence — the user-visible outcome}
Findings: {verbatim file:line list / Lighthouse audit evidence}
Fix direction: {playbook entry or approach — NOT implementation}
Acceptance: {verifiable criteria — e.g., "Lighthouse a11y ≥95 on 3 consecutive mobile runs", "zero axe violations on /checkout", "all icon buttons expose aria-label"}
Out of scope: {related findings deliberately excluded — other groups}
```

## Epic and Issues

- Epic title: `Design Review {YYYYMMDD} — {n} pendências`
- Slice Issues: one per SPEC, title `Design fix: {group name}`
- Dependencies: order groups when a fix unlocks another (e.g., self-host fonts → then tune preloads)
