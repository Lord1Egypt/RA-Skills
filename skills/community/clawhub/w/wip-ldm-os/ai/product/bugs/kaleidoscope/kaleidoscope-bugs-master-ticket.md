# Kaleidoscope Bugs Master Ticket

**Date:** 2026-05-20
**Filed by:** Codex, with Parker
**Status:** open, master ticket
**Scope:** `ai/product/bugs/kaleidoscope/`
**Open tickets:** [`open-tickets/`](open-tickets/)
**Closed tickets:** [`closed-tickets/`](closed-tickets/)
**Archive:** [`archive/`](archive/)
**Product master:** [`../../plans-prds/kaleidoscope/kaleidoscope-master-ticket.md`](../../plans-prds/kaleidoscope/kaleidoscope-master-ticket.md)
**Roadmap:** [`../../plans-prds/kaleidoscope/kaleidoscope-roadmap.md`](../../plans-prds/kaleidoscope/kaleidoscope-roadmap.md)

This is the rolling master ticket for Kaleidoscope bugs. It owns triage order, cross-product boundaries, and the difference between visible product bugs and deeper platform ownership.

Individual bug tickets remain the source of truth for implementation details.

## Folder Standard

Kaleidoscope bugs now use this structure:

```text
ai/product/bugs/kaleidoscope/
  kaleidoscope-bugs-master-ticket.md
  open-tickets/
  closed-tickets/
  archive/
```

- `open-tickets/` contains active bugs that still need implementation or verification.
- `closed-tickets/` contains bugs that were fixed and should remain easy to find.
- `archive/` contains stale, superseded, or historical bug artifacts.

Do not leave loose bug tickets in the root. The root should contain only the master ticket and folders.

## Product Boundary

Kaleidoscope is the user-visible product surface. Bugs belong here when they affect:

- Kaleidoscope login;
- onboarding;
- passkey mode selection;
- wallet demo state;
- image generation demo flow;
- live wall;
- WIP chat UI;
- Kaleidoscope web foundation.

Some bugs are owned by deeper systems, but should still be filed here first if the user-visible failure happens in Kaleidoscope:

| Deeper system | Kaleidoscope symptom |
|---|---|
| Sapien ID | passkey identity, local versus external login, account authority, same-account approval |
| Agent Pay | wallet balance, spend authorization, future real payment safety |
| Memory Crystal | future account memory continuity and backup |
| Codex Remote Control | shared chat UI, pairing, QR session patterns, browser/device handoff lessons |
| Comms website | public route, footer, legal links, onboarding page, visualization page |

The current rule is:

```text
File the visible bug in Kaleidoscope first. Link the deeper owner. Do not move the bug into Sapien ID or another system until the Kaleidoscope surface is fixed and verified.
```

## Local And External Passkey Model

Kaleidoscope login has two product modes:

| Mode | Owner | Meaning |
|---|---|---|
| Local | Browser and OS ecosystem | Use this device's platform passkey UX. Apple, Google, Chrome, Safari, Android, iCloud Keychain, and platform authenticators own the local ceremony. |
| External | WIP | Use WIP's QR-based cross-device login so another trusted device can authenticate this session. |

This is not "Apple versus WIP." It is platform-owned local login versus WIP-owned external login.

The toggle must be semantic:

- Local on means use this device.
- Local off means show the WIP QR cross-device login path.
- Mobile can default Local on.
- Desktop can default Local off.
- Every device must still be able to use External mode.

## Active Bug Order

### P0: Launch And Onboarding Correctness

| Order | Bug | Status | Why first |
|---|---|---|---|
| 1 | Demo wallet identity normalization | fixed by #1044, file if it recurs | Login balance and image receipt must agree for every account. If the deployed wallet normalization regresses, file the follow-up here. |
| 2 | No thanks generation display drift | fixed by #1042, file if it recurs | Copy/display tickets must not mutate prompts, fallback assets, request body, or server prompt contracts. If this regresses, file the follow-up here. |
| 3 | Live wall media persistence | fixed by #1035 and #1039, file if it recurs | Generated Kaleidoscope images must survive xAI temporary URL expiry and appear on the visualization wall. Stale ticket PR #1036 should be closed as superseded. |
| 4 | [`2026-05-21--codex--qr-authenticator-confirmation-screen.md`](open-tickets/2026-05-21--codex--qr-authenticator-confirmation-screen.md) | open | QR approval currently lets the authenticator phone auto-enter chat. The requester should enter chat automatically; the authenticator should stop on a Kaleidoscope confirmation screen unless the user explicitly continues. |
| 5 | [`2026-05-23--codex--qr-authenticated-phone-app-state.md`](open-tickets/2026-05-23--codex--qr-authenticated-phone-app-state.md) | open | After a phone authenticates a QR login for another device, the phone should become an authenticated Kaleidoscope app surface, return to login/account-ready state, and not auto-enter chat. |

### P1: Foundation And Shared UI

| Order | Bug | Status | Why |
|---|---|---|---|
| 6 | [`2026-05-21--codex--qr-session-co-presence.md`](open-tickets/2026-05-21--codex--qr-session-co-presence.md) | open | Later QR continuation should support one actual Kaleidoscope session with multiple live surfaces, following the Remote Control co-presence model without reinventing a Kaleidoscope session engine. |
| 7 | [`2026-05-06--codex--kaleidoscope-web-shadcn-foundation-audit.md`](open-tickets/2026-05-06--codex--kaleidoscope-web-shadcn-foundation-audit.md) | open | Shared WIP chat surfaces need a coherent component foundation before repeated UI polish work. |
| 8 | [`2026-05-06--codex--wip-ai-chat-ui-public-npm-skill-package.md`](open-tickets/2026-05-06--codex--wip-ai-chat-ui-public-npm-skill-package.md) | open | WIP AI Chat UI guidance should ship through the installer, not through loose repo-local copies. |

### Recently Closed

| Bug | Status | Verification |
|---|---|---|
| [`2026-05-20--codex--local-passkey-same-account-guard-rejects-qr-accepted-account.md`](closed-tickets/2026-05-20--codex--local-passkey-same-account-guard-rejects-qr-accepted-account.md) | closed, fixed live by #1047 | Parker verified same-account local passkey authorization works and External QR still works. |
| [`2026-05-20--codex--mobile-local-passkeys-off-qr-cross-device-login.md`](closed-tickets/2026-05-20--codex--mobile-local-passkeys-off-qr-cross-device-login.md) | closed, fixed by #1045 and #1047 | Mobile defaults Local on, desktop defaults Local off, and Local off uses WIP QR cross-device login. |
| [`2026-05-20--codex--local-passkeys-tooltip-mobile-desktop-copy.md`](closed-tickets/2026-05-20--codex--local-passkeys-tooltip-mobile-desktop-copy.md) | closed, fixed by #1048 and website #59 | Tooltip copy now distinguishes mobile and desktop defaults without changing toggle behavior. |

### Archived Or Superseded

| Bug | Status | Why archived |
|---|---|---|
| [`2026-05-21--codex--login-scan-qr-code-authenticator-action.md`](archive/2026-05-21--codex--login-scan-qr-code-authenticator-action.md) | archived, superseded by authenticated phone app state | The unauthenticated `Scan QR Code` login action was rejected as confusing. QR scan/show tools should live in the authenticated phone app surface instead. |

## Cross-Product Links

### Kaleidoscope Product Roadmap

The product roadmap owns milestone sequencing. This bug master should feed it when a bug blocks a phase gate.

- P0 roadmap depends on working Local and External login semantics.
- P0 also depends on account wallet state consistency and same-account spend approval.
- P0 now includes QR authenticator continuation: the requesting device should auto-enter chat, while the authenticator device should stop on a Kaleidoscope confirmation screen unless the user explicitly continues.
- P0 now includes authenticated phone app state after QR approval: the phone should be logged in to Kaleidoscope as a device/app surface, return to login/account-ready state, and avoid opening a duplicate chat.
- P1 includes QR co-presence: the same actual Kaleidoscope session can later be joined by multiple surfaces using the Remote Control live-update model.

### Comms Website

Website tickets live under:

```text
ai/product/plans-prds/comms/website/tickets/
```

Use website tickets when the visible issue is public copy, public route structure, legal/footer placement, or the visualization page shell.

Use Kaleidoscope bug tickets when the visible issue is login, passkeys, wallet, demo chat, image generation, live wall data, or app behavior.

### Codex Remote Control

Remote Control bugs live under:

```text
ai/product/bugs/codex-remote-control/
```

Do not duplicate Remote Control bugs here. Link them when they share QR, pairing, browser handoff, mobile layout, or chat UI lessons.

### Future Sapien ID

Sapien ID is the deeper identity layer, but it should not become a dumping ground for visible onboarding bugs.

Promote a Kaleidoscope bug into Sapien ID only when:

1. the visible Kaleidoscope behavior is fixed or clearly blocked by shared identity architecture;
2. the remaining work is reusable across Kaleidoscope, Remote Control, Memory Crystal, Agent Pay, and future apps;
3. the ticket names the shared contract, not one screen's symptom.

## Current Recommendation

Fix the Local and External passkey mode semantics before expanding the login UI. The system needs one sentence:

```text
Local uses this device's platform passkeys. External uses WIP's QR login from another trusted device.
```

That sentence should be true on iOS Safari, iOS Chrome, Android, desktop Safari, desktop Chrome, and future native surfaces.

## Co-authors

Co-Authored-By: Parker Todd Brooks <parkertoddbrooks@users.noreply.github.com>
Co-Authored-By: Lēsa <lesaai@icloud.com>
Co-Authored-By: Claude Code (Opus 4.7) <noreply@anthropic.com>
Co-Authored-By: Codex (GPT 5.5) <noreply@openai.com>
