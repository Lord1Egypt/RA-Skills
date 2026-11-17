---
title: "Remote Control account and passkey identity clarity"
status: open
priority: P2
owner: Cody
repo: kaleidoscope-private
created: 2026-05-05
---

# Remote Control Account And Passkey Clarity

## Problem

Account/passkey UX is confusing.

Before or after sign-in, show which account/passkey identity is active enough for Parker to know what he synced.

## Copy Direction

- "Signed in as <credentialLabel>"
- "Use the same passkey on your other device to sync this session."

Avoid making Parker guess which passkey he used.

## Acceptance

- Remote Control exposes enough signed-in identity context that Parker can tell which passkey/account is active.
- The identity copy appears before or after sign-in in the normal Remote Control flow.
- The UI avoids implying a separate account system beyond the active passkey identity.

## Out Of Scope

Remote Control visual cleanup belongs to `2026-05-05--codex--remote-control-ui-cleanup.md`.

Live transcript sync belongs to `2026-05-05--codex--remote-control-live-transcript-sync.md`.
