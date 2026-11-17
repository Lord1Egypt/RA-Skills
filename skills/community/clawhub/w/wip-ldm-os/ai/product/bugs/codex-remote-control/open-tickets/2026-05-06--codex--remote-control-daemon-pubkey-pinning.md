---
title: "Remote Control browser should pin daemon public key after first trusted E2EE session"
status: open
priority: P2
owner: hosted auth token security K-partner / Cody
repo: kaleidoscope-private / wip-ldm-os-private
created: 2026-05-06
---

# Remote Control Daemon Public Key Pinning

## Problem

The browser trusts the daemon public key returned by relay bootstrap. A compromised relay or database write path could substitute a relay-controlled daemon public key and perform a man-in-the-middle attack on future browser sessions.

This is defense in depth. It does not block Parker-only dogfood, but it should be tracked before broader users.

## Security Review Evidence

Finding:

```text
H3. No daemon-pubkey pinning on the browser side.
```

Source pointer from review:

- `repos/ldm-os/wip-ldm-os-private/src/hosted-mcp/server.mjs:2764`

## Expected Behavior

Browser remembers the daemon public key after the first trusted E2EE session and warns on unexpected changes.

Possible v1 shape:

- TOFU pin `(agentId, daemon_public_key_spki)` in browser persistent storage,
- on future bootstrap, compare returned daemon key to the stored pin,
- if it changes, show a clear key-changed warning before connecting,
- expected relink or daemon re-key flow can rotate the pin after fresh user presence.

Longer-term option:

- sign daemon public keys with a root not held by the relay.

## Acceptance

- First successful E2EE session stores daemon public key fingerprint.
- Subsequent session with same daemon key proceeds.
- Subsequent session with different daemon key warns or blocks until user confirms through fresh presence.
- Legitimate relink/re-key updates the pin through the approved flow.
- Regression can inject a changed bootstrap key and assert the warning or block.

## Non-Goals

- Do not block current Parker-only dogfood on this ticket.
- Do not replace E2EE key persistence.
- Do not store daemon private keys in the browser or relay.
