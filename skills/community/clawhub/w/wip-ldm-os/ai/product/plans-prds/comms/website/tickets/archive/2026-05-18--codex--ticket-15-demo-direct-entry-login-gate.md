# Ticket 15: Route direct demo entry through login

**Date:** 2026-05-18
**Filed by:** Codex, with Parker
**Status:** archived 2026-05-18. Implemented by `wip-ldm-os-private` PR #1002 and deployed; Parker confirmed direct `/demo` gating works.
**Master:** `ai/product/plans-prds/comms/website/tickets/website-launch-masterticket.md`
**Depends on:** Ticket 02 login/demo entry, Ticket 09 demo icon login next
**Surface:** `repos/ldm-os/wip-ldm-os-private/src/hosted-mcp/demo/index.html`, and server routing in `repos/ldm-os/wip-ldm-os-private/src/hosted-mcp/server.mjs` only if required

## Summary

The public demo entry point should be login-first. User-facing links should point to:

```text
https://wip.computer/login?next=/demo
```

Raw `/demo` can remain the post-login destination, but direct entry to `/demo` should not start the demo as an unauthenticated public page. If someone types `/demo` into the browser, or an agent links to raw `/demo`, it should route into the login flow.

Parker's direction:

```text
it should link to the log in demo

the demo in the chat should, if you type that in, go into the login
```

## Desired behavior

- Public links to the demo use `/login?next=/demo`.
- Direct unauthenticated entry to `/demo` routes to `/login?next=/demo`.
- After successful login through `/login?next=/demo`, the user lands in `/demo` and the scripted demo starts.
- The already-authenticated handoff must not loop back to login.
- The active demo icon should still route to `/login?next=/demo`.
- Existing Remote Control, pair/relink, passkey, wallet, and image generation behavior remain unchanged.

## Implementation direction

Prefer the smallest safe fix.

Expected shape:

1. In `src/hosted-mcp/demo/index.html`, add an early client-side entry guard if no server-side gate already exists.
2. The guard should only redirect to `/login?next=/demo` when there is no demo login handoff or session state.
3. If the demo already has `lesa-token` or whatever token/name state the login handoff writes, do not redirect.
4. Keep the exact `/login?next=/demo` target. Do not use raw `/demo`, `/demo/`, wildcard next paths, or external redirects.
5. If server-side routing already has an authenticated route-bound ticket mechanism that can do this more safely, use that instead, but do not refactor auth.

The coder must first inspect the current demo identity state names before coding. Recent login work used the `lesa-*` sessionStorage namespace for demo identity. Do not guess.

## Constraints

1. No broad auth refactor.
2. No `next` wildcard changes.
3. No Remote Control changes.
4. No pair/relink changes.
5. No relay, daemon sync, passkey/WebAuthn, wallet, image API, or E2EE changes.
6. No homepage changes.
7. No deploy. Stop at PR.
8. Keep `/login?next=/demo` as the canonical public demo entry.
9. Avoid loops: a successful `/login?next=/demo` must reach the demo.

## Acceptance criteria

- A user-facing raw `/demo` link is not introduced anywhere.
- Direct unauthenticated `/demo` redirects or navigates to `/login?next=/demo`.
- Successful `/login?next=/demo` still lands in `/demo`.
- Once landed through login, `/demo` does not immediately bounce back to login.
- The active demo icon points to `/login?next=/demo`.
- Existing Remote Control login paths are unchanged.
- Existing pair/relink behavior is unchanged.
- Run an inline parse check for changed HTML files.
- Run `node --check src/hosted-mcp/server.mjs` if server code changes.
- Run `git diff --check`.

## Out of scope

- Redesigning the demo.
- Changing the demo script.
- Changing image generation.
- Changing homepage copy.
- Changing `agent.txt` or `llms.txt`.
- Building Demo 2.
