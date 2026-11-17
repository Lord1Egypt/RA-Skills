---
title: "Remote Control E2EE should track long-term forward secrecy upgrade"
status: open
priority: P3
owner: Cody
repo: wip-codex-remote-control-private
created: 2026-05-06
---

# Remote Control E2EE Forward Secrecy Follow-Up

## Problem

The daemon currently uses a long-lived ECDH key for browser sessions. If `~/.codex-daemon/e2ee-key.json` is exfiltrated, captured ciphertext from past sessions could be decrypted.

This is an accepted v1 simplicity tradeoff, but it should be tracked as a long-term security improvement.

## Security Review Evidence

Finding:

```text
L1. No forward secrecy within the E2EE session.
```

Source pointer from review:

- `repos/ldm-os/apps/wip-codex-remote-control-private/src/e2ee.ts:71-110`

## Possible Upgrade Paths

- Rotate daemon E2EE keys on a schedule with overlap.
- Use per-session daemon ephemeral keys signed by a durable device identity.
- Add a ratcheting scheme for long sessions.

## Acceptance

- A future design chooses a forward-secrecy strategy.
- Existing paired daemon recovery remains understandable.
- Browser key-change warnings and relink semantics stay clear.
- Tests cover old and new key behavior during rotation.

## Non-Goals

- Do not block current Parker-only dogfood.
- Do not block first public alpha if the critical and high findings are fixed.
- Do not weaken current E2EE while adding rotation.
