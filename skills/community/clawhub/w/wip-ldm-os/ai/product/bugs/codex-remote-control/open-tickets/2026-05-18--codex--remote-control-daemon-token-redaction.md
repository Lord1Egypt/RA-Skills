---
title: "Remote Control daemon CLI must not print local control tokens"
status: open
priority: P1
owner: Hardening Cody
repo: wip-codex-remote-control-private
created: 2026-05-18
source_review: 2026-05-18 security triage of private Remote Control architecture
master_plan_item: 36
---

# Remote Control Daemon CLI Must Not Print Local Control Tokens

## Problem

The 2026-05-18 security triage found that the private Remote Control daemon is much stronger than the old public relay snapshot, but still alpha-secure rather than production-secure.

One concrete footgun: `codex-daemon status` and foreground start can print the full local daemon control token.

Observed review references:

- `wip-codex-remote-control-private/src/cli.ts:127`
- `wip-codex-remote-control-private/src/cli.ts:202`

The local daemon token is generated with strong randomness and stored with restrictive file permissions, which is good. Printing it to terminal output or logs weakens that property. It can land in screenshots, pasted transcripts, shell scrollback, task logs, or agent summaries.

## Risk

P1 local/log exposure.

This is not a remote exploit by itself. An attacker still needs local access to the output channel. But the token controls the local daemon HTTP surface, and WIP uses agent transcripts and logs heavily. Secrets should not be printed by default.

## Fix shape

- Redact the token in all normal `codex-daemon status` output.
- Redact the token in normal foreground start output.
- Preserve a deliberate diagnostic path only if needed, for example `--show-token`, with explicit warning text and no use in install prompts.
- Prefer token fingerprints for diagnostics:

```text
token: ct-...f4a2 (redacted)
token fingerprint: sha256:abcd1234
```

- Audit daemon logs for the same token-print path.
- Update any tests, docs, install prompts, and troubleshooting snippets that currently expect the full token.

## Acceptance

- `codex-daemon status` never prints the full local control token by default.
- `codex-daemon start --foreground` never prints the full local control token by default.
- Existing status information remains useful: running state, pid, relay-paired state, log path, and a short non-secret token fingerprint are acceptable.
- A regression test fails if a `ct-` token-shaped value appears in default status or foreground output.
- If a diagnostic `--show-token` path is added, it is opt-in, clearly named, and not referenced by normal install or dogfood flows.

## Validation

- Run Remote Control daemon tests.
- Run a local smoke:
  - `codex-daemon status`
  - `codex-daemon start --foreground` in a controlled test environment, or the nearest non-disruptive equivalent
  - confirm no full token appears in stdout or stderr.

## Non-goals

- Do not rotate existing local tokens in this ticket unless a live leak is found.
- Do not change the bearer-token auth model.
- Do not weaken localhost binding or daemon auth.
- Do not change hosted relay behavior.
