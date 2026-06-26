---
name: qmd-learning-loop
description: Capture corrections, errors, feature requests, and recurring best practices in a QMD-native way for markdown-first agent workspaces. Use when a user corrects the agent, a command or tool fails, a missing capability is requested, a better recurring approach is discovered, or a lesson should be promoted into durable memory, runbooks, decisions, or workspace guidance without creating a separate .learnings silo.
---

# QMD Learning Loop

Capture useful learnings without creating a parallel memory system. Route raw chronology to lightweight logs, durable operational lessons to indexed docs, and stable cross-cutting rules to existing workspace guidance.

## Core workflow

1. Classify the event:
   - correction
   - error/failure
   - feature request
   - better practice / recurring pattern
2. Choose the lowest-appropriate destination.
3. Prefer updating an existing durable doc over creating a new one.
4. Use QMD-aware discipline: avoid duplicate policy documents.
5. Promote only when the lesson is recurring, cross-cutting, or policy-changing.

## First-pass routing rules

### Correction or misunderstanding
- Add chronological context to a daily log or other lightweight memory file when the correction matters.
- Promote only if the correction changes a stable rule, behavior, or operating convention.
- If promotion is warranted, update the most relevant durable target:
  - workflow guidance file
  - tooling notes file
  - behavior/principles file
  - decision or policy docs

### Error, tool failure, or command failure
- Log immediate chronology in a daily log if the failure matters to continuity.
- If the failure is operationally meaningful or recurring, add it to an indexed incident or error log.
- If the fix becomes reusable, update or create a runbook.

### Feature request
- Add a durable request to an indexed backlog or strategy file.
- If the request becomes accepted scope or changes policy, create or update a decision or project doc.

### Better practice or recurring pattern
- For workflow/tooling guidance, update a runbook or workspace guidance file.
- For durable system rules, create or update a decision memo.
- For stable behavior or communication principles, update the relevant behavior/principles file cautiously.

## Second-pass promotion rules

Use a second pass when the learning seems durable enough to influence future behavior, policy, or structure.

### Second-pass sequence

1. Check whether the event still matters after the immediate task.
2. Inspect existing durable docs and prefer updating them over creating a new file.
3. Choose the promotion target using `references/promotion-targets.md`.
4. Write the promoted rule concisely and prevention-first.
5. Leave detailed chronology in lightweight logs instead of copying it wholesale into durable docs.

### QMD-aware duplication check

Before creating a new durable rule, search the relevant QMD collections or inspect the existing indexed docs for the same topic. Do not create near-duplicate policy or workflow documents.

### Trigger conditions for second-pass promotion

Promote when one or more are true:
- the issue recurs
- it affects multiple tasks or agents
- it changes operating policy
- it prevents meaningful repeated waste
- it defines a stable convention worth retrieving later

Do not turn every one-off event into a permanent rule.

## Review loop

At natural breakpoints, review captured items and decide whether they should stay chronological, become operational logs, or be promoted into durable guidance. Read `references/review-loop.md` when doing this review.

## Existing-doc first rule

Read `references/routing-and-promotion.md` when routing is ambiguous. Read `references/templates.md` when you need starter formats for incident entries, feature requests, lightweight memory capture, or a new decision memo.
