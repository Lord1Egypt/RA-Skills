---
skill_bundle: a11y-audit
file_role: reference
version: 2
version_date: 2026-04-23
previous_version: null
change_summary: >
  Expanded the safe dry-run path to use project context, labels,
  additional standards, and simulated duplicate indexes.
---

# Issue Trackers

Read this file only when `output_mode` is `markdown+issues`.

## Preconditions

- Require explicit user confirmation before creating any tickets.
- Load tracker settings from `.a11y-audit/PROJECT_CONTEXT.md`.
- Create tickets only at or above the configured severity threshold.
- Prefer `scripts/plan-issues.js` first when you need a non-destructive
  dry run for user review or deduplication planning.

## Supported Trackers

| Tracker | CLI / API | Create Pattern |
|---|---|---|
| GitHub | `gh` | `gh issue create --title "..." --label "..." --body "..."` |
| GitLab | `glab` | `glab issue create --title "..." --label "..." --description "..."` |
| Linear | API or CLI | Create via API payload |
| Jira | `jira` or API | `jira issue create --project "..." --type Bug --summary "..."` |

## Ticket Structure

Each ticket should contain:

- WCAG criterion
- axe rule ID
- severity / priority
- affected pages
- plain-language description
- impact statement
- affected selectors or representative nodes
- suggested remediation
- references to axe help and WCAG understanding docs
- audit metadata

Title format:

`[A11y] [Severity] [Page]: [Brief description]`

## Deduplication

- Search for existing open tickets before creating new ones.
- Default deduplication key:
  `<!-- a11y-audit-key: [rule-id]::[page-path] -->`
- If the tracker strips HTML comments, use a custom field or label.
- If a match already exists, skip creation and record the existing ticket
  in the report.

## Priority Mapping

| axe Impact | Priority |
|---|---|
| critical | P0 |
| serious | P1 |
| moderate | P2 |
| minor | P3 |

## Reporting Rule

Even when tickets are created, the markdown report remains the primary
audit artifact. The issue section should summarize what was created,
what was skipped as duplicate, and what remained below threshold.

## Safe Dry-Run Path

Before live issue creation, you can generate a markdown issue plan from
helper scan JSON plus project context:

```bash
node a11y-audit/scripts/plan-issues.js \
  --input docs/accessibility/audits/audit-YYYY-MM-DD.json \
  --context .a11y-audit/PROJECT_CONTEXT.md \
  --existing /tmp/a11y-existing-keys.json \
  --output /tmp/a11y-issue-plan.md \
  --threshold P1
```

Use that plan to confirm scope, configured labels, standards mapping,
deduplication keys, duplicate skipping, and priority threshold before
invoking a tracker CLI.
