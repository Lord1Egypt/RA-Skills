# Product Idea: Enforce full GitHub issue metadata on every issue

**Filed by:** CC-Mini on 2026-03-13
**GitHub Issue:** #166 (https://github.com/wipcomputer/wip-ai-devops-toolbox-private/issues/166)

---

## The Problem

Agents file issues with bare minimum metadata. A typical issue gets `filed-by:cc-mini` and nothing else. No type label (bug vs enhancement vs product-idea). No project. No milestone. No assignee. No relationships.

GitHub gives us all these tools:
- **Labels:** bug, enhancement, product-idea, filed-by:*, priority, component
- **Type:** Bug, Feature, etc. (GitHub issue types)
- **Projects:** kanban/roadmap tracking
- **Milestones:** release or sprint grouping
- **Assignees:** who owns it
- **Relationships:** linked issues, parent/child

We're using almost none of them. Issues pile up as flat, unlabeled lists. No one can triage at a glance.

## What the DevOps Toolbox Should Do

### 1. Issue filing checklist (in the Dev Guide)

Every issue filed by any harness must include:
- `filed-by:{harness}` label (cc-mini, cc-air, oc-lesa-mini, etc.)
- At least one type label: `bug`, `enhancement`, `product-idea`, `documentation`
- Component label if applicable (e.g., `wip-release`, `wip-install`, `deploy-public`)
- Severity or priority if it's a bug

### 2. Suggested labels (create across all repos)

| Label | Color | Description |
|-------|-------|-------------|
| `bug` | #d73a4a | Something isn't working |
| `enhancement` | #a2eeef | Improvement to existing feature |
| `product-idea` | #0e8a16 | Product idea or feature request |
| `documentation` | #0075ca | Docs improvement |
| `filed-by:cc-mini` | #1d76db | Filed by Claude Code on mini |
| `filed-by:cc-air` | #1d76db | Filed by Claude Code on Air |
| `filed-by:oc-lesa-mini` | #d876e3 | Filed by Lesa on mini |
| `priority:high` | #b60205 | Needs attention soon |
| `priority:low` | #c5def5 | Nice to have |

### 3. GitHub Projects setup

Create a `wipcomputer` org-level project board so issues across repos can be tracked in one view. Columns: Backlog, Up Next, In Progress, Done.

### 4. Milestones per repo

At minimum, a "Next Release" milestone in each active repo. Move issues into it when they're targeted for the next version.

### 5. wip-release integration

When `wip-release` runs, it could:
- Check for open issues tagged with the current milestone
- Warn if releasing with unresolved bugs
- Auto-close milestone on release
- Include issue references in release notes

## Why This Matters

Without metadata, issues are just a growing list nobody can prioritize. With metadata, any agent or human can triage in seconds: "show me all high-priority bugs in wip-release" or "what's left for the next milestone." The toolbox should enforce this, not rely on agents remembering.
