---
title: "Remote Control Safari handoff must not expose long-lived bearer token to same-origin JavaScript"
status: open
priority: P1
owner: hosted auth token security K-partner / Cody
repo: wip-ldm-os-private / kaleidoscope-private
created: 2026-05-06
---

# Remote Control Safari Handoff Bearer Token

## Problem

The Safari handoff cookie carries the long-lived `ck` bearer token at `Path=/` for 60 seconds and is readable by same-origin JavaScript.

That is workable for Parker-only smoke, but it is too broad for non-Parker users. The handoff should use an opaque one-time code or server-side exchange, not the bearer itself.

CC security review notes this is acceptable for v1 as a known property if Parker is the only user, but it should remain tracked before broader users.

## Security Review Evidence

Finding:

```text
Medium: the Safari handoff cookie carries the long-lived ck bearer at Path=/ for 60 seconds and is readable by same-origin JavaScript.
```

Source pointers from review:

- writer: `repos/ldm-os/wip-ldm-os-private/src/hosted-mcp/app/kaleidoscope-login.html:334`
- reader: `repos/ldm-os/apps/kaleidoscope-private/web/src/app/codex-remote-control/[threadId]/page.tsx:158`
- same-origin proxy: `repos/ldm-os/wip-ldm-os-private/src/hosted-mcp/nginx/wip.computer.conf:42`

## Expected Behavior

Safari login handoff should not expose a reusable bearer token to same-origin JavaScript.

Preferred shape:

- login writes a short-lived opaque one-time handoff code,
- Remote Control exchanges that code server-side for the needed session state,
- the code is single-use,
- the code is scoped to the intended next route,
- the long-lived bearer is never placed in a JavaScript-readable cookie.

## Acceptance

- No `ck` bearer token is written to a JavaScript-readable handoff cookie.
- Handoff code is single-use.
- Handoff code expires quickly.
- Handoff code is scoped to the intended route or thread where appropriate.
- Safari login to Remote Control still works.
- Desktop login and pair-mode flows still work.
- Regression proves stale handoff code reuse fails.

## Non-Goals

- Do not weaken passkey auth.
- Do not change Remote Control E2EE.
- Do not solve pair/relink fresh-presence in this ticket unless the same exchange primitive cleanly covers both.
