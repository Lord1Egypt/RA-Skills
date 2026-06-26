---
name: skill-sprint-pack-builder
description: Convert pasted lesson notes, workflow notes, upstream agent-skill ideas, or rough implementation notes into a public-safe ClawHub/Codex skill sprint pack with a 20-minute action, proof checklist, redaction checklist, Skool post, reusable skill card, next reps, and verification criteria.
---

# Skill Sprint Pack Builder

Use this skill when a user pastes lesson notes, workflow notes, teardown notes,
an upstream agent-skill idea, or an informal build process and wants to turn it
into a practical ClawHub, Codex, or Claude Code skill artifact for a Skool
audience.

## Inputs

Collect or infer:

- source notes or lesson transcript,
- target audience,
- one useful job the member can finish today,
- required tools or accounts,
- visible proof artifact,
- privacy risks,
- target runtime: ClawHub, Codex, Claude Code, or portable,
- whether the source is original notes or an upstream skill idea,
- what should become reusable next time.

If the notes include private names, links, credentials, exports, screenshots, or
unverified claims, pause and convert them into placeholders before drafting the
public artifact.

If the input is an upstream skill or skill repository, do not copy it verbatim.
Extract the useful behavior pattern, rewrite the trigger narrowly, remove
runtime-specific assumptions, and convert the result into a public-safe sprint
pack.

## Workflow

1. Extract the smallest repeatable outcome from the notes.
2. Define a 20-minute action:
   - one objective,
   - starting state,
   - exact steps,
   - stopping point,
   - proof to capture.
3. Build a proof checklist that verifies the action happened without exposing
   private data.
4. Build a redaction checklist before any public sharing.
5. Draft a public-safe Skool post that teaches the action without implying
   guaranteed results.
6. Create a reusable skill card for ClawHub or Codex:
   - skill name,
   - trigger phrase,
   - inputs,
   - step sequence,
   - expected artifact,
   - proof required,
   - safety notes.
   Keep the skill card installable: use a short kebab-case name, a clear
   trigger description, explicit inputs, and no hidden dependency on private
   files or accounts.
7. If adapting an upstream skill idea, add a runtime adaptation block:
   - what to keep,
   - what to rewrite,
   - what to reject,
   - Codex notes,
   - Claude Code notes,
   - ClawHub/OpenClaw notes,
   - install impact risk.
8. Define 3 next reps that make the skill stronger through real use.
9. Define verification criteria that decide whether the sprint pack is ready to
   post, reuse, or revise. If the proof artifact is client-facing, verify that
   it contains no private data, local paths, token-like strings, or implementation
   process wording before sharing.

## Output

Return:

- sprint title,
- 20-minute action,
- proof checklist,
- redaction checklist,
- public-safe Skool post,
- reusable ClawHub/Codex skill card,
- runtime adaptation block when relevant,
- next reps,
- verification criteria.

Keep the output concrete enough that a non-technical member can act without
understanding the full toolchain. Use advanced tool names only when they help
the user choose the right execution path.

## Examples

Good public-safe inputs:

- "Here are my notes from rebuilding a public browser workflow into a checklist."
- "Turn this creator-owned SOP into a 20-minute lesson-to-proof sprint."
- "Adapt this upstream agent-skill idea into a public-safe local sprint pack."

Avoid inputs that require copying private lesson text, paid community posts,
member DMs, customer records, credentials, or screenshots with account details.
Replace them with placeholders, synthetic rows, or the creator's own notes.

## Guardrails

- Do not scrape private communities, member lists, DMs, paid lessons, or hidden
  pages.
- Do not request, store, transform, or paste credentials, API keys, session
  cookies, recovery codes, payment data, or private exports.
- Do not provide medical, financial, or legal advice. Convert those topics into
  general workflow organization, source collection, or "ask a qualified
  professional" handoff steps.
- Do not promise or make earnings, growth, rank, conversion, or time-saved
  claims unless the user provides public evidence and the post frames it as a
  specific past example, not a promise.
- Remove or generalize names, handles, addresses, emails, phone numbers,
  private URLs, order IDs, account IDs, and screenshots with sensitive UI.
- Prefer consent-first public artifacts: member-submitted examples, synthetic
  examples, anonymized notes, or the creator's own workflow.
