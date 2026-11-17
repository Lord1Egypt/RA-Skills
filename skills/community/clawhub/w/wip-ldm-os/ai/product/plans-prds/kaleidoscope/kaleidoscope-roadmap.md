# Kaleidoscope Roadmap

**Date:** 2026-05-19
**Status:** open roadmap
**Master ticket:** [`kaleidoscope-master-ticket.md`](kaleidoscope-master-ticket.md)
**Ticket folder:** [`tickets/`](tickets/)
**Bug master:** [`../../bugs/kaleidoscope/kaleidoscope-bugs-master-ticket.md`](../../bugs/kaleidoscope/kaleidoscope-bugs-master-ticket.md)

This roadmap turns the Kaleidoscope ticket set into a build sequence. The master ticket owns priority order. This file owns the phase gates.

## Product Goal

Kaleidoscope should let a person start on the web, log in with a passkey from their phone, receive a starter wallet, install or pair the CLI, connect local agents, and later activate iOS/macOS apps for Face ID approval, trusted device recovery, wallet authority, and iCloud-backed storage.

Kaleidoscope product logic should graduate into `repos/ldm-os/apps/kaleidoscope-private/`. The WIP website repos can host public routes and the visualization shell, but shared account, wallet, passkey, image-generation, and native-app state belongs to Kaleidoscope and its APIs.

Website migration is a separate comms track:

```text
repos/wip-web/wip-computer-website/static/   current live site
repos/wip-web/wip-computer-website/dev/      static-to-app staging lane
repos/wip-web/wip-computer-website/next-js/  future full Next.js website app
```

The product should feel like:

```text
Your phone is your key.
Your devices are trusted.
Kaleidoscope helps you get back in.
No passwords. No seed phrases. No recovery emails.
```

## Phase Gate Summary

| Phase | Theme | Exit gate |
|---|---|---|
| P0 | Identity, onboarding, wallet safety, backup | A user can start onboarding, authenticate with phone passkey, create persistent wallet state, and configure Kaleidoscope Backup before real spend. |
| P1 | Web plus CLI | A user can run `kaleidoscope login`, pair the machine with QR/code, name the machine, and see the same account/wallet/device state as the web app. |
| P2 | Connectors | A user can connect at least one local agent, approve a scoped agent request, and revoke the token later. |
| P3 | Native app trust | iOS and macOS provide Phone Key, Face ID approval, trusted devices, CloudKit/iCloud backup, and device review. |
| P4 | Native experience | Kaleidoscope grows into real native surfaces, starting with the Call Lēsa plan after trust and identity are in place. |
| P5 | Platform expansion | Auth SDK, marketplace connectors, directory submissions, non-Apple recovery, enterprise/team modes. |

## P0: Identity, Onboarding, Wallet Safety, Backup

**Goal:** make the current demo become safe product onboarding.

Required tickets:

- [`tickets/2026-05-19--codex--phone-key-and-kaleidoscope-backup.md`](tickets/2026-05-19--codex--phone-key-and-kaleidoscope-backup.md)
- [`tickets/2026-05-18--codex--guided-onboarding-intent-engine.md`](tickets/2026-05-18--codex--guided-onboarding-intent-engine.md)
- [`tickets/2026-05-21--codex--kaleidoscope-public-stats-baseline.md`](tickets/2026-05-21--codex--kaleidoscope-public-stats-baseline.md)
- [`../../bugs/kaleidoscope/open-tickets/2026-05-21--codex--qr-authenticator-confirmation-screen.md`](../../bugs/kaleidoscope/open-tickets/2026-05-21--codex--qr-authenticator-confirmation-screen.md)
- [`../../bugs/kaleidoscope/open-tickets/2026-05-23--codex--qr-authenticated-phone-app-state.md`](../../bugs/kaleidoscope/open-tickets/2026-05-23--codex--qr-authenticated-phone-app-state.md)
- [`tickets/2026-05-18--codex--sapien-id-agent-login-handoff.md`](tickets/2026-05-18--codex--sapien-id-agent-login-handoff.md)
- [`../../bugs/kaleidoscope/closed-tickets/2026-05-20--codex--mobile-local-passkeys-off-qr-cross-device-login.md`](../../bugs/kaleidoscope/closed-tickets/2026-05-20--codex--mobile-local-passkeys-off-qr-cross-device-login.md)
- [`tickets/2026-04-06--cc-mini--postgres-prisma-infrastructure.md`](tickets/2026-04-06--cc-mini--postgres-prisma-infrastructure.md)
- [`tickets/2026-04-07--cc-mini--chrome-qr-login-plan.md`](tickets/2026-04-07--cc-mini--chrome-qr-login-plan.md)
- [`tickets/2026-04-07--cc-mini--features-to-preserve-from-demo.md`](tickets/2026-04-07--cc-mini--features-to-preserve-from-demo.md)

Build sequence:

1. Rename product path from demo-first language to onboarding-first language.
2. Add `/onboarding` while preserving `/demo` compatibility.
3. Make wallet state persistent per identity.
4. Reject spend approval from a genuinely different passkey account than the active onboarding session.
5. Fix Local and External login semantics.
6. Add Chrome desktop QR phone handoff as part of the broader External login path.
7. Fix QR authenticator continuation so the requesting device auto-enters chat, but the authenticator phone stops on a Kaleidoscope confirmation screen unless the user explicitly continues.
8. Preserve authenticated phone app state after QR approval: the requesting device enters chat, while the phone becomes authenticated and returns to login/account-ready state without opening a duplicate chat.
9. Add public live-wall stats baseline and date-window math so new activity can be measured after 2026-05-21 without deleting launch-era counts.
10. Define Kaleidoscope Backup setup in the onboarding script.
11. Gate real wallet/spend behind at least one configured way back in.

Exit gate:

- New user can create a passkey account with phone.
- Mobile defaults Local login on.
- Desktop defaults Local login off.
- Local off always shows WIP's QR cross-device login path on every device.
- Returning user sees the same account and wallet balance.
- Same-account spend approval is enforced on both local passkey approval and QR approval.
- Same-account local passkey and QR parity bug is closed by #1047 and verified live.
- QR authenticator flow distinguishes requester from authenticator: requester enters chat automatically; authenticator stops on a Kaleidoscope confirmation screen and does not auto-enter chat.
- QR approval leaves the authenticator phone logged in to Kaleidoscope as an app/device surface, but does not auto-enter a duplicate phone-side chat.
- Live-wall stats preserve launch counts while reporting post-baseline activity from 2026-05-21 and excluding `wiptest-*` keys from public key counts.
- User sees and configures a consumer-friendly backup path before wallet activation.
- No email or SMS recovery is required for the primary path.

## P1: Web Plus CLI

**Goal:** make CLI a first-class Kaleidoscope surface, not a helper.

Required tickets:

- [`tickets/2026-05-19--codex--kaleidoscope-cli-four-surface-onboarding.md`](tickets/2026-05-19--codex--kaleidoscope-cli-four-surface-onboarding.md)
- [`tickets/2026-04-06--cc-mini--kaleidoscope-architecture.md`](tickets/2026-04-06--cc-mini--kaleidoscope-architecture.md)
- [`../../bugs/kaleidoscope/open-tickets/2026-05-21--codex--qr-session-co-presence.md`](../../bugs/kaleidoscope/open-tickets/2026-05-21--codex--qr-session-co-presence.md)

Build sequence:

1. Add `kaleidoscope login`.
2. Generate QR/code account pairing from CLI.
3. Store device-scoped credentials in the OS keychain where possible.
4. Ask for machine name and role.
5. Detect LDM OS, Codex, Claude Code, OpenClaw, Memory Crystal, and existing local state.
6. Show device state in web and CLI.
7. Add explicit co-presence for QR continuation by reusing the existing live-session model rather than creating a new Kaleidoscope-only session engine.
8. Add install/dry-run handoff for LDM OS.

Exit gate:

- A user can start on web, install CLI, pair the machine, and see one shared account/device/wallet state.

## P2: Connectors and Agent Authorization

**Goal:** make connectors a product capability inside Kaleidoscope.

Required tickets:

- [`tickets/2026-05-18--codex--sapien-id-agent-login-handoff.md`](tickets/2026-05-18--codex--sapien-id-agent-login-handoff.md)
- [`tickets/2026-05-19--codex--kaleidoscope-cli-four-surface-onboarding.md`](tickets/2026-05-19--codex--kaleidoscope-cli-four-surface-onboarding.md)

Build sequence:

1. Connect Codex first.
2. Add Remote Control pairing as a connector, not a one-off auth path.
3. Add Memory Crystal connector.
4. Add Claude Code connector.
5. Add Bridge and Agent Pay connectors.
6. Add token list and revoke UI.
7. Add connector naming and grouping: machine name, agent name, connector group.

Exit gate:

- An agent can request a scoped action, human approves on phone, agent receives only the approved token, user can revoke it later.

## P3: Native App Trust and iCloud-Backed Continuity

**Goal:** make iOS and macOS the trust, approval, and restore surfaces.

Required tickets:

- [`tickets/2026-05-19--codex--phone-key-and-kaleidoscope-backup.md`](tickets/2026-05-19--codex--phone-key-and-kaleidoscope-backup.md)
- [`tickets/2026-05-19--codex--kaleidoscope-cli-four-surface-onboarding.md`](tickets/2026-05-19--codex--kaleidoscope-cli-four-surface-onboarding.md)

Build sequence:

1. Ship iOS app as Phone Key and wallet approval surface.
2. Ship macOS app as Keychain, CloudKit, and local service helper.
3. Write the user's trust graph to their own iCloud/CloudKit storage.
4. Add Restore Access flow.
5. Add trusted device review and revoke.
6. Pause wallet on suspicious restore until device review completes.
7. Add CloudKit/iCloud storage activation for Memory Crystal.

Exit gate:

- User can lose one device, restore access through an existing trusted path, review devices, rotate old access, and continue without email/SMS recovery.

## P4: Native Experience Expansion

**Goal:** add richer app surfaces after authority is stable.

Required tickets:

- [`tickets/2026-04-24--lesa--native-voice-call-apple-way.md`](tickets/2026-04-24--lesa--native-voice-call-apple-way.md)

Build sequence:

1. Native Call Lēsa button.
2. Native audio spike.
3. Brain gateway.
4. CallKit integration.
5. Realtime conversation.

Exit gate:

- The native app has a real Lēsa voice surface that uses authenticated Kaleidoscope session state.

## P5: Platform Expansion

**Goal:** turn the proven identity, connector, and recovery model into a platform.

Sources:

- [`tickets/2026-04-07--cc-mini--features-to-preserve-from-demo.md`](tickets/2026-04-07--cc-mini--features-to-preserve-from-demo.md)
- [`tickets/2026-04-07--cc-mini--session-final-summary.md`](tickets/2026-04-07--cc-mini--session-final-summary.md)
- [`tickets/2026-04-07--cc-mini--session-overview-apr5-7.md`](tickets/2026-04-07--cc-mini--session-overview-apr5-7.md)

Possible work:

- passkey-first auth SDK
- Directory SDK
- OAuth/MCP marketplace submissions
- non-Apple backup and restore path
- enterprise/team trusted device model
- shared memory zones

Exit gate:

- Kaleidoscope's passkey, approval, wallet, and connector model is reusable outside the first WIP-owned surfaces.

## Dependency Rules

- Wallet/spend depends on Kaleidoscope Backup.
- Sapien ID depends on consistent Local and External login semantics.
- Connector token handoff depends on Sapien ID.
- CLI pairing depends on QR/code account pairing.
- Native voice depends on authenticated app session state.
- Marketplace submissions depend on stable auth, token, and revocation behavior.

## Reading Order

1. [`kaleidoscope-master-ticket.md`](kaleidoscope-master-ticket.md)
2. This roadmap
3. [`../../bugs/kaleidoscope/kaleidoscope-bugs-master-ticket.md`](../../bugs/kaleidoscope/kaleidoscope-bugs-master-ticket.md)
4. Current P0 tickets in `tickets/`
5. Current P0 bugs in `../../bugs/kaleidoscope/open-tickets/`
6. Older reference tickets only when a current ticket cites them

## Co-authors

Co-Authored-By: Parker Todd Brooks <parkertoddbrooks@users.noreply.github.com>
Co-Authored-By: Lēsa <lesaai@icloud.com>
Co-Authored-By: Claude Code (Opus 4.7) <noreply@anthropic.com>
Co-Authored-By: Codex (GPT 5.5) <noreply@openai.com>
