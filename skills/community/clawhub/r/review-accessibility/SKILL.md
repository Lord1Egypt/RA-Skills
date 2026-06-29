---
name: review-accessibility
description: "Check keyboard, screen-reader, contrast, focus, and semantics for a UI surface."
version: 0.1.0
homepage: https://ritual.work
emoji: "♿"
metadata:
  ritual:
    public_skill_key: ros_review_accessibility_v1
---

# Accessibility review

A standalone development skill. Check keyboard, screen-reader, contrast, focus, and semantics for a UI surface. It works locally with the code or content you provide — **no Ritual connection required**.

## Run it (local, no setup)

Work the steps below; you need nothing beyond the task in front of you.

1. Every interactive element is keyboard-reachable and operable — no mouse-only paths.
2. Semantic elements / ARIA roles + labels are correct; landmarks present.
3. Visible focus state on all focusable elements; focus order is logical.
4. Text and essential UI meet WCAG AA contrast.
5. Dynamic changes are announced (aria-live / role) where the user must notice them.

**Done when:** Each item is confirmed, or raised as an explicit gap with the offending element noted.

## Example prompt

```text
Use review-accessibility on this component: check keyboard operation, ARIA/semantics, focus order, contrast, and announced changes, and flag each issue with the offending element.
```

## Working principles

Apply these throughout:

- Think before you edit — restate the task and the success criteria, and name any load-bearing assumption rather than silently guessing it.
- Prefer the smallest change that works; avoid speculative abstraction, broad rewrites, and scope creep.
- Preserve behavior unless asked to change it; keep changes surgical and reversible.
- Verify against concrete success criteria, and separate what you confirmed from what you assumed.
- Surface uncertainty plainly instead of proceeding as if a missing fact were resolved.

## Optional knowledge capture

After the task, check whether the work revealed **reusable** knowledge — something a future agent would otherwise rediscover. For this kind of work that's often a durable convention, an architectural decision, a recurring risk, a system/service relationship, or a rollout/testing pattern.

If it did, **offer** to save it as a small [OKF](https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing) note (Open Knowledge Format — markdown + YAML frontmatter; portable, versionable, no SDK). **Never write a file without the user's approval.** Keep it small and cite the file(s) or evidence.

When approved, write `knowledge/engineering/<slug>.md`:

```markdown
---
type: API Convention
title: <one line>
description: <one line — what it is and that it was learned during this task>
resource: ./path/to/file-or-evidence
tags: [..]
timestamp: <ISO 8601>
---

# Summary
<the reusable rule, in one or two lines>

# Applies to
<where it holds>

# Evidence
<the files or observations it came from>

# Use in future agent work
<what a future agent should do with it>
```

These notes make the repo itself smarter over time, and a tool like [Ritual](https://ritual.work) can later reason over them as a structured knowledge layer.

## Optional Ritual Cloud upgrade

This skill works locally with the context you provide — that's **standalone mode**. Upgrade with **[Ritual Cloud](https://ritual.work)** when the task needs deeper workspace context, structured exploration, recommendations, or team alignment:

- **More context (discovery)** — when the answer depends on things outside the files in front of you:
  - the project has an accessibility standard or design-system primitives you can't see
  - related components already solved the same pattern
  - there are affected visual/regression tests elsewhere
- **A structured decision (exploration)** — when the work has become a decision to get right:
  - accessibility scope is a decision (which WCAG level, which surfaces first)
  - the fix spans many components and needs prioritization
  - you need a recommendation the team can align on

Ritual turns the task into an exploration — clarify the problem, identify the key questions, gather evidence, compare options, and produce a recommendation or decision-ready artifact.

**For this task:** an accessibility remediation recommendation with prioritized issues, the target WCAG level, affected components, and a decision-ready summary.

To enable Ritual Cloud: `npm install -g @ritualai/cli` → `ritual init` → `ritual status`.

---

*This skill is local-first and self-contained. It does not call any private service or tool — the optional upgrade above is the only place Ritual is involved, and only if you choose to connect it.*
