# Local Passkeys Tooltip Needs Mobile And Desktop Copy

**Date:** 2026-05-20
**Filed by:** Codex, with Parker
**Status:** closed, fixed by hosted-mcp PR #1048 and website PR #59
**Priority:** P1
**Product surface:** Kaleidoscope footer and login help copy
**Related system owner:** Sapien ID
**Primary surfaces:** homepage-style footer, Kaleidoscope login, Kaleidoscope visualization footer
**Bug master:** [`../kaleidoscope-bugs-master-ticket.md`](../kaleidoscope-bugs-master-ticket.md)

## Problem

Resolution 2026-05-21: tooltip copy was updated across hosted-mcp login and the public website/live-wall footer lanes. This did not change toggle behavior.

The Local passkeys tooltip currently uses one desktop-leaning explanation everywhere:

```text
Local passkeys are off by default.
Your phone's passkeys are used for login and device sync. Turn this on to use or save passkeys on this machine.
```

That is wrong or confusing on mobile, where Local passkeys should default on.

The copy also says "phone," but the product model is broader than phone-only. It should cover iPhone, Android, iPad, and other mobile passkey devices.

## Expected Behavior

The tooltip copy should change based on device class.

### Mobile Copy

Use this copy when Local passkeys default on:

```text
Local passkeys are on by default on mobile devices.
This device's passkeys are used for login and device sync.
Turn this off to use or save passkeys on a different device.
```

### Desktop Copy

Use this copy when Local passkeys default off:

```text
Local passkeys are off by default on desktop.
Your mobile device's passkeys are used for login and device sync.
Turn this on to use or save passkeys on this computer.
```

## Product Language Decision

Use `mobile device`, not `phone`.

Reason:

- It covers iPhone, Android, iPad, and future mobile passkey devices.
- It avoids implying phone-only behavior.
- It maps to the Local versus External passkey model.

Avoid:

```text
your mobile devices' passkeys
```

That phrase is awkward and harder to parse.

## Scope

This is a copy and presentation bug. It should not change login mechanics.

Allowed:

- tooltip text;
- tooltip device-conditional copy selection;
- tests or fixtures for mobile versus desktop copy if practical.

Not allowed:

- passkey creation changes;
- WebAuthn challenge changes;
- QR login behavior changes;
- Local on or Local off state logic changes beyond reading the current default;
- wallet logic;
- demo chat copy;
- image generation;
- live wall;
- legal pages;
- nginx;
- Remote Control, relay, daemon, E2EE, or API keys.

## Acceptance

- On mobile, the tooltip says Local passkeys are on by default on mobile devices.
- On mobile, the tooltip says this device's passkeys are used.
- On mobile, the tooltip says turning Local off uses or saves passkeys on a different device.
- On desktop, the tooltip says Local passkeys are off by default on desktop.
- On desktop, the tooltip says the user's mobile device passkeys are used.
- On desktop, the tooltip says turning Local on uses or saves passkeys on this computer.
- No tooltip copy says `phone's passkeys`.
- No tooltip copy uses the awkward possessive plural `mobile devices' passkeys`.

## Related

- [`2026-05-20--codex--mobile-local-passkeys-off-qr-cross-device-login.md`](2026-05-20--codex--mobile-local-passkeys-off-qr-cross-device-login.md)
- [`../closed-tickets/2026-05-20--codex--local-passkey-same-account-guard-rejects-qr-accepted-account.md`](../closed-tickets/2026-05-20--codex--local-passkey-same-account-guard-rejects-qr-accepted-account.md)

## Co-authors

Co-Authored-By: Parker Todd Brooks <parkertoddbrooks@users.noreply.github.com>
Co-Authored-By: Lēsa <lesaai@icloud.com>
Co-Authored-By: Claude Code (Opus 4.7) <noreply@anthropic.com>
Co-Authored-By: Codex (GPT 5.5) <noreply@openai.com>
