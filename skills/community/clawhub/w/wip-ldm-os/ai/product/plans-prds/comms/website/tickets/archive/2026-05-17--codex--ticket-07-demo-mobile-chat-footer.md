# Ticket 07: Remove the footer from the active demo chat

**Date:** 2026-05-17
**Filed by:** Codex, with Parker
**Status:** archived 2026-05-18. Implemented by `wip-ldm-os-private` PR #989 and deployed; active demo chat footer removal is no longer an open launch blocker.
**Master:** `ai/product/plans-prds/comms/website/tickets/website-launch-masterticket.md`
**Depends on:** Ticket 02 login/demo entry
**Surface:** `repos/ldm-os/wip-ldm-os-private/src/hosted-mcp/demo/index.html` and, only if needed, `repos/ldm-os/wip-ldm-os-private/src/hosted-mcp/demo/footer.js`

## Summary

The Kaleidoscope demo chat should feel like a focused app surface. The shared footer currently appears behind or above the active chat input area on mobile and desktop, which makes the demo feel like a web page leaking into the chat instead of a contained product experience.

Remove or hide the footer while the active chat/demo surface is shown. Do not change the login, passkey, wallet, image generation, Remote Control, pair/relink, relay, daemon sync, or E2EE behavior.

## Observed behavior

The demo page mounts the shared footer immediately after the login page:

```html
<div id="kscope-footer"></div>
<script src="/demo/footer.js"></script>
```

Then it mounts the chat page:

```html
<div class="chat-page" id="chatPage">
```

`footer.js` intentionally keeps the footer in normal page flow on mobile and fixes it at the bottom on desktop:

```js
container.style.cssText = 'background:#FFFDF5;padding:16px 0;';
container.style.cssText = 'position:fixed;bottom:0;left:0;right:0;background:#FFFDF5;padding:16px 0;';
```

That means the footer can remain visible once the demo/chat surface is active. Parker verified the bug on mobile and desktop. The footer text appears behind or above the chat input, including "Learning Dreaming Machines", copyright, Privacy Policy, Terms of Use, "Are you an AI Agent?", and "Made in California."

Parker's direction: "When we're in the chat, the footer should just be removed."

## Desired behavior

- Active chat/demo state: no footer visible behind, above, below, or near the chat input.
- Applies on mobile and desktop.
- Login state before chat starts: footer may remain if it does not interfere with the login screen.
- The chat input remains fixed, reachable, and visually clean.

## Scope

- Prefer the smallest CSS or class-based change.
- If `showChat()` is the cleanest hook, it may hide `#kscope-footer` when the chat starts.
- If CSS is enough, scope it to the active chat/demo state.
- Keep the scripted Demo 1 flow intact.
- Do not refactor `footer.js` globally unless required.

Likely smallest implementation:

```js
function showChat() {
  document.getElementById('loginPage').style.display = 'none';
  var footer = document.getElementById('kscope-footer');
  if (footer) footer.style.display = 'none';
  var chatPage = document.getElementById('chatPage');
  chatPage.style.display = 'flex';
  startDemo();
}
```

## Constraints

1. No auth changes.
2. No `next` allowlist changes.
3. No Remote Control, pair/relink, relay, daemon sync, passkey/WebAuthn, wallet, image generation, or E2EE changes.
4. No homepage changes.
5. No broad redesign. This is a footer removal for the active demo chat only.

## Acceptance criteria

- On a mobile viewport, after the chat/demo surface is active, the shared footer is not visible.
- On a desktop viewport, after the chat/demo surface is active, the shared footer is not visible.
- The chat input area remains visible and usable.
- The login/create-account screen still renders.
- Existing scripted demo flow still starts after login.
- `node --check src/hosted-mcp/server.mjs` is not required unless server code changes. If only HTML/CSS/JS changes, run an inline script parse check for `src/hosted-mcp/demo/index.html`.

## Out of scope

- Changing the demo script.
- Changing login redirect behavior.
- Fixing API image generation.
- Static homepage hardening.
- Footer redesign across all Kaleidoscope pages.
