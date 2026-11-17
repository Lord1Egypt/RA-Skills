# Ticket 09: Route the demo icon through login next demo

**Date:** 2026-05-17
**Filed by:** Codex, with Parker
**Status:** archived 2026-05-18. Implemented by `wip-ldm-os-private` PR #993 and included in later hosted-mcp deploys; demo icon now routes through `/login?next=/demo`.
**Master:** `ai/product/plans-prds/comms/website/tickets/website-launch-masterticket.md`
**Depends on:** Ticket 02 login/demo entry
**Surface:** `repos/ldm-os/wip-ldm-os-private/src/hosted-mcp/demo/index.html`

## Summary

In the active Kaleidoscope demo, clicking the icon should send the user to:

```text
https://wip.computer/login?next=/demo
```

It should not send the user back to raw `/demo`, restart the demo directly, or bypass the login continuation path.

## Observed behavior

Parker is testing:

```text
https://wip.computer/login?next=/demo
```

The scripted demo works far enough to enter the chat. In the active chat header, the Kaleidoscope icon is the visible navigation/restart affordance. Current copy near the end of the demo says:

```text
This is the end of the demo. Tap icon or refresh page to start over.
```

That icon behavior needs to be aligned with the launch path. The correct restart/entry path is the login continuation URL, not raw `/demo`.

Parker's direction:

```text
This should be the icon. When you click the icon, it shouldn't go back to demo. It should go to this. https://wip.computer/login?next=/demo
```

## Desired behavior

- In the active `/demo` chat surface, clicking the Kaleidoscope icon navigates to `https://wip.computer/login?next=/demo`.
- The user re-enters through the real login/passkey continuation path.
- The icon must not navigate directly to `/demo` or `/demo/`.
- The icon must not clear identity/session state directly in client code.
- The scripted demo remains otherwise unchanged.

## Implementation direction

Keep this as a tiny launch fix.

Likely implementation:

1. Locate the active chat header icon in `src/hosted-mcp/demo/index.html`.
2. Make it a real link or click target whose destination is exactly:

   ```text
   /login?next=/demo
   ```

   Absolute `https://wip.computer/login?next=/demo` is also acceptable if the existing file style prefers absolute URLs.

3. If there is existing icon click JavaScript that restarts the demo or sends users to `/demo`, replace only that behavior.
4. Update the end-of-demo copy only if needed so it does not imply a raw refresh/restart path.

## Constraints

1. No auth logic changes.
2. No `next` allowlist changes.
3. No passkey/WebAuthn changes.
4. No wallet, image generation, xAI, Remote Control, pair/relink, relay, daemon sync, or E2EE changes.
5. No homepage changes.
6. Do not deploy. Stop at PR.

## Acceptance criteria

- The active chat icon target is `/login?next=/demo` or `https://wip.computer/login?next=/demo`.
- There is no icon click path that sends users directly to `/demo` or `/demo/`.
- Existing login screen still renders.
- Existing scripted demo still starts.
- Existing footer-hidden behavior from Ticket 07 remains intact.
- Inline executable script parse for `src/hosted-mcp/demo/index.html` passes.
- `git diff --check` passes.
- Diff is limited to `src/hosted-mcp/demo/index.html` unless the coder finds a documented reason.

## Out of scope

- Fixing xAI image generation. That is Ticket 08.
- Changing login success copy.
- Changing passkey behavior.
- Redesigning the chat header.
- Moving `/demo` to the future Kaleidoscope app architecture.
