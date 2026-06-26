---
name: syft-guidance-rulebook
description: Use when the user wants to capture long-lived preferences, editorial rules, branch preferences, or filtering instructions into a persistent rulebook in Codex or Claude Code without local helper scripts. Also use when the user wants a confirmation-first workflow before saving durable preferences.
---

# Syft Guidance Rulebook

Use this skill when the user expresses something that may deserve long-term storage.

## Goal

Maintain a persistent user guidance document that future profile, briefing, and storyline work can read as parallel guidance.

Recommended file:

- `profiles/user_guidance_rulebook.md`

If a workspace already uses a JSON rulebook, reuse it instead of forcing Markdown.
The critical behavior is the workflow, not the file format.

## Golden rule

Never store a long-lived rule directly from one raw user sentence.

Always do this first:

1. summarize your understanding
2. ask whether the summary is correct
3. ask whether the user wants it persisted
4. only then write it into the rulebook

## Good candidates for storage

- long-term content preferences
- structural editorial preferences
- storyline / branch handling preferences
- search extension preferences
- recurring dislikes or red lines

## Bad candidates for storage

- one-off requests for today only
- temporary formatting asks
- speculative guesses that the user has not confirmed

## Rulebook entry shape

Each stored rule should preserve:

- id
- name
- scope
- kind
- priority
- status
- canonical guidance text
- short rationale
- source note
- confirmed date

Read `references/rulebook-template.md` before editing the file.

## Scope guidance

Use:

- `all` for rules that should influence almost everything
- `editorial` for daily briefing behavior
- `storyline` for event-tree organization
- `syft_search` for search completion behavior
- `recommendation` for future recommendation logic

## Priority guidance

Use broad bands:

- `85-100`: strong, identity-defining, should almost always affect output
- `65-80`: meaningful preference, usually keep active
- `40-60`: soft preference
- `<40`: weak or situational preference
