---
title: "Remote Control browser must reject plaintext protocol after E2EE is ready"
status: done
priority: P1
owner: hosted auth token security K-partner / Cody
repo: kaleidoscope-private
created: 2026-05-06
---

# Remote Control Browser Plaintext After E2EE

## Problem

The browser decrypts `e2ee.frame`, but after E2EE is established it can still fall through to plaintext response handling for non-frame messages.

Once the encrypted channel is ready, Remote Control should not accept normal control protocol messages outside `e2ee.frame`, except a very narrow set of handshake or terminal error states.

## Security Review Evidence

Finding:

```text
Medium-high: the browser still accepts plaintext protocol messages after E2EE is ready.
```

Source pointers from review:

- `repos/ldm-os/apps/kaleidoscope-private/web/src/app/codex-remote-control/[threadId]/page.tsx:194`
- `repos/ldm-os/apps/kaleidoscope-private/web/src/app/codex-remote-control/[threadId]/page.tsx:237`

## Expected Behavior

Browser-side Remote Control has explicit protocol phases:

- before E2EE: allow only bootstrap, handshake, and explicit safe errors,
- after E2EE ready: accept only `e2ee.frame` for the current session plus narrowly allowed terminal handshake errors,
- reject or ignore plaintext `session.*` control messages after E2EE is ready,
- log metadata only when plaintext is dropped.

## Acceptance

- After E2EE ready, plaintext `session.event` is ignored or rejected.
- After E2EE ready, plaintext `session.ack` is ignored or rejected unless explicitly whitelisted for handshake.
- After E2EE ready, plaintext command responses cannot update the transcript or session state.
- `e2ee.frame` for the current session still works.
- Handshake failure errors still render clearly.
- Regression covers plaintext ignored after E2EE ready.

## Resolution

Shipped in `kaleidoscope-private` PR #47 and deployed by the Kaleidoscope main-branch workflow on 2026-05-12.

The Remote Control browser now tracks an explicit E2EE-ready phase. After `e2ee.ready` for the current session:

- encrypted `e2ee.frame` messages are still decrypted and handled;
- scoped `e2ee.error` messages can still surface terminal handshake or channel errors;
- plaintext `session.*`, `ack`, and `error` messages no longer reach the normal session response handler;
- dropped plaintext logs metadata only, currently the outer protocol type.

The deployed VPS source was verified at:

```text
/var/www/kaleidoscope.wip.computer/app/web/src/app/codex-remote-control/[threadId]/page.tsx
```

Validation:

```bash
cd web
npm run test:remote-control-plaintext-after-e2ee
npx eslint 'src/app/codex-remote-control/[threadId]/page.tsx'
npm run build
```

Full `npm run lint` remains blocked by pre-existing `no-explicit-any` errors in `src/app/login/page.tsx` and `src/app/pair/page.tsx`; the touched Remote Control page passes scoped eslint.

## Non-Goals

- Do not weaken E2EE.
- Do not add plaintext fallback for production.
- Do not change relay fanout behavior.
