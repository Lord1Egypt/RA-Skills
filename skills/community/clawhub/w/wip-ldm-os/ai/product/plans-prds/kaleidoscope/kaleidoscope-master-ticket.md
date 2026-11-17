# Kaleidoscope Master Ticket

**Date:** 2026-05-19
**Filed by:** Codex, with Parker
**Status:** open, master ticket
**Scope:** `ai/product/plans-prds/kaleidoscope/`
**Roadmap:** [`kaleidoscope-roadmap.md`](kaleidoscope-roadmap.md)
**Tickets:** [`tickets/`](tickets/)
**Bug master:** [`../../bugs/kaleidoscope/kaleidoscope-bugs-master-ticket.md`](../../bugs/kaleidoscope/kaleidoscope-bugs-master-ticket.md)

This is the rolling master ticket for Kaleidoscope product planning. It is the source of truth for ordering, dependencies, and current product context. The ticket files in `tickets/` remain the source of truth for their own scope.

## Product Frame

Kaleidoscope is the app.
Lēsa is the AI inside it.
LDM OS is the operating layer underneath.
Sapien ID is the human authorization layer.
Agent Pay is the wallet and spend layer.
Memory Crystal is the remembering layer.

## Repo And Website Boundary

Kaleidoscope app logic belongs in:

```text
repos/ldm-os/apps/kaleidoscope-private/
```

That repo should own the eventual web app, iOS app, macOS app, shared MVVM-style product logic, API contracts, onboarding state, passkey identity flows, wallet/Agent Pay state, generated-output state, and native app coordination.

The WIP website lives under:

```text
repos/wip-web/wip-computer-website/
```

That website lane owns public company pages, site shell, header/footer, marketing pages, install prompts, visualization page shell, and the static-to-Next.js migration for `wip.computer`.

The current website lanes are:

| Lane | Role |
|---|---|
| `static/wip-websites-private/` | Current live static `wip.computer` source. |
| `dev/` | Staging/prototype lane for moving static site shell work toward the full Next.js app. |
| `next-js/wip-web-private/` | Future full Next.js website app. Not the current production source. |

The website can link to or display Kaleidoscope surfaces. It must not own Kaleidoscope application state.

The product direction is now four surfaces over one account and authority model:

| Surface | Product job |
|---|---|
| Web | Instant entry, onboarding, passkey login, starter wallet, agent approval |
| CLI | Builder harness, LDM OS install, local agent connectors, machine setup |
| iOS | The Kaleidoscope app: opens as a chat, shows all your chats across every agent, plus Phone Key, Face ID approval, wallet authority, Kaleidoscope Backup |
| macOS | local trust anchor, Keychain helper, CloudKit bridge, service controller |

The iOS surface was re-scoped on 2026-07-01 (decision D1 in [`claude-ios/2026-07-01--cc-mini--spec-0-7-1a-repo-reconciliation.md`](claude-ios/2026-07-01--cc-mini--spec-0-7-1a-repo-reconciliation.md)): one app that has everything from the Phone Key plan AND looks like a chat. Seeing all your chats across every agent is the key consumer feature. Feature layering after visibility: open/continue a chat in its harness, remote control, on-device search across everything. Kaleidoscope is the central brain.

The consumer promise should feel like Face ID and passkeys, not crypto recovery. Users should not hear seed phrase, shard, private key, custody, MPC, or hardware wallet. Technical implementation can use strong cryptography, but the product language is:

- Phone Key
- Trusted Devices
- Kaleidoscope Backup
- Ways Back In
- Restore Access
- Approve with Face ID

## Why This Exists

The existing Kaleidoscope folder had several correct but scattered plans: demo preservation, QR login, identity storage, Sapien ID, guided onboarding, native voice, and the first CLI/four-surface synthesis that was drafted from Vision Quest.

Those no longer belong as equal-priority notes. They need one master order and one roadmap.

The critical new requirement is access recovery before wallet launch. Kaleidoscope can be passkey-first only if users have a consumer-friendly way back in that does not fall back to email, SMS, passwords, or written keys.

The wallet cannot become real until Phone Key plus Kaleidoscope Backup exists as a product rule.

## Operating Principles

1. **Phone first, not password first.** The user's phone is the normal approval surface.
2. **Passkeys are first-class.** Kaleidoscope should assume the user wants to log in from any device using the passkey on their phone or trusted passkey manager.
3. **No crypto vocabulary in consumer copy.** Internals can be cryptographic; the product should feel like Apple Pay, Face ID, and iCloud restore.
4. **Wallet requires backup.** Do not turn on real spend until Kaleidoscope Backup is configured.
5. **The CLI is a full surface.** It is not a helper script for the web app.
6. **Connectors are capabilities.** Codex, Claude Code, OpenClaw, Memory Crystal, Agent Pay, Bridge, Directory, and Remote Control are connected through one device and approval model.
7. **WIP routes but should not become the user.** WIP can coordinate relay, billing, discovery, and recovery, but WIP cannot alone recover the user's authority.
8. **Do not rewrite the demo proof casually.** Preserve proven behavior while turning the product path into onboarding.
9. **Local and External login modes must be semantic.** Local means the browser and OS ecosystem owns the passkey ceremony on this device. External means WIP owns a QR-based cross-device login path from another trusted device.

## Login Mode Model

Kaleidoscope login has two modes:

| Mode | Owner | Product meaning |
|---|---|---|
| Local | browser and OS ecosystem | Use this device's passkey ceremony. Apple, Google, Chrome, Safari, Android, iCloud Keychain, and passkey providers own the local UX. |
| External | WIP | Show WIP's QR cross-device login so another trusted device can authenticate this session. |

Defaults should follow the user's likely intent:

- Mobile defaults Local on.
- Desktop defaults Local off.
- Local off always means External QR login on every device.

This belongs to Kaleidoscope first because users experience it in the login and onboarding surface. The deeper system owner is Sapien ID, but the visible bug should stay in Kaleidoscope until fixed and verified.

## Execution Order

### P0: Launch Safety, Identity, Wallet, and Recovery

| Ticket | Status | Notes |
|---|---|---|
| [`2026-05-19--codex--phone-key-and-kaleidoscope-backup.md`](tickets/2026-05-19--codex--phone-key-and-kaleidoscope-backup.md) | open | New critical ticket. Defines Phone Key, Trusted Devices, Kaleidoscope Backup, Ways Back In, and the rule that wallet/spend cannot launch until backup is configured. |
| [`2026-05-18--codex--guided-onboarding-intent-engine.md`](tickets/2026-05-18--codex--guided-onboarding-intent-engine.md) | open | Turns the current demo path into product onboarding: scripted first, real authorization underneath, bounded model help only at safe steps. |
| [`2026-05-21--codex--kaleidoscope-public-stats-baseline.md`](tickets/2026-05-21--codex--kaleidoscope-public-stats-baseline.md) | open | Public live-wall metrics baseline. Keep current counts at 3 keys, 11 generic Kaleidoscopes, and 3 image-based Kaleidoscopes, then count new post-baseline activity while excluding `wiptest-*` keys. |
| [`2026-05-21--codex--qr-authenticator-confirmation-screen.md`](../../bugs/kaleidoscope/open-tickets/2026-05-21--codex--qr-authenticator-confirmation-screen.md) | open | Interim QR continuation fix. Requesting device enters chat automatically after QR approval; authenticator device stops on a Kaleidoscope confirmation screen unless the user explicitly continues. |
| [`2026-05-20--codex--kaleidoscope-passkey-terms-acceptance.md`](tickets/2026-05-20--codex--kaleidoscope-passkey-terms-acceptance.md) | open | Product UI follow-up from Ticket 18. Add visible Terms and Privacy acceptance at passkey creation. Not a legal rewrite. |
| [`2026-05-20--codex--kaleidoscope-generated-output-rights-notice.md`](tickets/2026-05-20--codex--kaleidoscope-generated-output-rights-notice.md) | open | Product UI follow-up from Ticket 18. Add visible generated-output rights notice before image generation. Not a legal rewrite. |
| [`2026-05-20--codex--local-passkey-same-account-guard-rejects-qr-accepted-account.md`](../../bugs/kaleidoscope/closed-tickets/2026-05-20--codex--local-passkey-same-account-guard-rejects-qr-accepted-account.md) | closed, fixed live by #1047 | Same-account reauthorization now compares canonical account ids first. Parker verified local passkey authorization and External QR both work for the same account. |
| [`2026-05-20--codex--mobile-local-passkeys-off-qr-cross-device-login.md`](../../bugs/kaleidoscope/closed-tickets/2026-05-20--codex--mobile-local-passkeys-off-qr-cross-device-login.md) | closed, fixed by #1045 and #1047 | Mobile defaults Local on, desktop defaults Local off, and Local off shows WIP's QR cross-device login on every device. Related to Sapien ID, but filed under Kaleidoscope because the bug was visible in login/onboarding. |
| [`2026-05-18--codex--sapien-id-agent-login-handoff.md`](tickets/2026-05-18--codex--sapien-id-agent-login-handoff.md) | open | Agent reaches a gated action, asks the human, human approves on phone, agent receives scoped token. |
| [`2026-04-06--cc-mini--postgres-prisma-infrastructure.md`](tickets/2026-04-06--cc-mini--postgres-prisma-infrastructure.md) | verify current state, likely P0 | Production identity, passkeys, wallets, paired devices, API keys, and server config must be durable and recoverable. Verify what has already shipped before coding. |
| [`2026-04-07--cc-mini--features-to-preserve-from-demo.md`](tickets/2026-04-07--cc-mini--features-to-preserve-from-demo.md) | reference, P0 behavior | Agent auth, approve page, QR login concept, wallet permission, and "You can't do Face ID. Your human can." must carry forward. |
| [`2026-04-07--cc-mini--chrome-qr-login-plan.md`](tickets/2026-04-07--cc-mini--chrome-qr-login-plan.md) | open, promote to P0 | Passkey-first only works if Chrome desktop can hand off cleanly to the phone. Custom QR login becomes a launch-path requirement. |

### P0 Parallel Lane: Kaleidoscope iOS App and Capture (started 2026-07-01)

Runs alongside P0. Decision D4 (Parker, 2026-07-01): we don't have a Kaleidoscope app today; start building it now. TestFlight first: the basic iOS 27 app frame plus the Safari capture plugin that just works for claude.ai, then the GPT surface.

| Item | Status | Notes |
|---|---|---|
| [`claude-ios/spec-0-7-1a/kaleidoscope-capture-extension-SPEC-v0.7.1-FROZEN.md`](claude-ios/spec-0-7-1a/kaleidoscope-capture-extension-SPEC-v0.7.1-FROZEN.md) | frozen, authoritative | Safari Web Extension capture architecture. v0.7.1a errata applied. Architecture locked; remaining work is code and tickets. |
| [`claude-ios/spec-0-7-1a/kaleidoscope-phase0-build.md`](claude-ios/spec-0-7-1a/kaleidoscope-phase0-build.md) | ready to build | Phase 0 ticket breakdown (T1-T11) and binary test matrix. MVP: chat in Safari, open Kaleidoscope, it's there. |
| [`claude-ios/2026-07-01--cc-mini--spec-0-7-1a-repo-reconciliation.md`](claude-ios/2026-07-01--cc-mini--spec-0-7-1a-repo-reconciliation.md) | decisions recorded | Repo reconciliation plus decisions D1-D5: one app, agent_id stays identity, all raw memory in the app, start now, capture everything visible. |
| [`claude-ios/harness-profile-catalog.md`](claude-ios/harness-profile-catalog.md) | v0.1 | Harness profiles and stream_key to agent_id mapping. Answers spec §5.4 and §19.4-5. |
| GPT capture surface (chatgpt.com adapter) | next after Claude works | Second surface per D4. Same pipeline, new content-script adapter. |
| App code location | decided | `repos/ldm-os/apps/kaleidoscope-private/ios/` per the 2026-04-06 architecture ticket. SwiftUI, no React Native, per vision-quest-02 MVVM rule. |

### P1: Web Plus CLI Onboarding

| Ticket | Status | Notes |
|---|---|---|
| [`2026-05-19--codex--kaleidoscope-cli-four-surface-onboarding.md`](tickets/2026-05-19--codex--kaleidoscope-cli-four-surface-onboarding.md) | open | Moved out of Vision Quest into Kaleidoscope PRDs. Defines web, CLI, iOS, and macOS as coordinated product surfaces. |
| [`2026-04-06--cc-mini--kaleidoscope-architecture.md`](tickets/2026-04-06--cc-mini--kaleidoscope-architecture.md) | reference, verify before implementation | Repo and product boundary. Use for `kaleidoscope-private`, hosted-mcp, and website split, but verify current live routing first. |
| [`2026-05-21--codex--qr-session-co-presence.md`](../../bugs/kaleidoscope/open-tickets/2026-05-21--codex--qr-session-co-presence.md) | open | Later QR continuation model. Same actual Kaleidoscope session can be joined by another surface with live updates, following the Remote Control co-presence pattern without reinventing the session engine. |

### P2: Connectors, Agent Authorization, and Device Management

| Ticket | Status | Notes |
|---|---|---|
| [`2026-05-18--codex--sapien-id-agent-login-handoff.md`](tickets/2026-05-18--codex--sapien-id-agent-login-handoff.md) | also P2 implementation lane | P0 for product requirement, P2 for broader connector rollout after first protected action works. |
| [`2026-05-19--codex--kaleidoscope-cli-four-surface-onboarding.md`](tickets/2026-05-19--codex--kaleidoscope-cli-four-surface-onboarding.md) | also P2 implementation lane | Codex, Claude Code, OpenClaw, Memory Crystal, Remote Control, Agent Pay, Bridge, and Directory connectors. |

### P3: Native App Trust and Sovereign Storage

| Ticket | Status | Notes |
|---|---|---|
| [`2026-05-19--codex--phone-key-and-kaleidoscope-backup.md`](tickets/2026-05-19--codex--phone-key-and-kaleidoscope-backup.md) | also P3 implementation lane | iOS and macOS apps become the durable key, recovery, and trust surfaces. |
| [`2026-05-19--codex--kaleidoscope-cli-four-surface-onboarding.md`](tickets/2026-05-19--codex--kaleidoscope-cli-four-surface-onboarding.md) | also P3 implementation lane | Native apps activate CloudKit/iCloud-backed storage and local trust. |

### P4: Native Experience Expansion

| Ticket | Status | Notes |
|---|---|---|
| [`2026-04-24--lesa--native-voice-call-apple-way.md`](tickets/2026-04-24--lesa--native-voice-call-apple-way.md) | open, P4 | The Call Lēsa surface matters, but it should follow identity, Phone Key, wallet, and native app trust. |

### P5: Historical References and Later Platformization

| Ticket | Status | Notes |
|---|---|---|
| [`2026-04-07--cc-mini--session-final-summary.md`](tickets/2026-04-07--cc-mini--session-final-summary.md) | reference | Historical session summary. Useful for context, not direct execution. |
| [`2026-04-07--cc-mini--session-overview-apr5-7.md`](tickets/2026-04-07--cc-mini--session-overview-apr5-7.md) | reference | Historical session overview. Useful for context, not direct execution. |
| Auth SDK / framework idea inside [`2026-04-07--cc-mini--features-to-preserve-from-demo.md`](tickets/2026-04-07--cc-mini--features-to-preserve-from-demo.md) | future | Possible future Directory or auth SDK after Kaleidoscope proves the passkey and agent-auth loops. |

## Roadmap Linkage

Use the roadmap for phase gates and milestone sequencing:

- [`kaleidoscope-roadmap.md`](kaleidoscope-roadmap.md)

Use this master ticket for the active index and priority order.

Use `tickets/` for individual ticket scope.

Use the Kaleidoscope bug master for visible product bugs:

- [`../../bugs/kaleidoscope/kaleidoscope-bugs-master-ticket.md`](../../bugs/kaleidoscope/kaleidoscope-bugs-master-ticket.md)

## Current Recommendation

Do not launch wallet/spend as a real product surface until Phone Key plus Kaleidoscope Backup is defined and minimally implemented.

In parallel with the slice below, the Kaleidoscope iOS app lane runs now (2026-07-01): TestFlight frame plus the claude.ai Safari capture plugin, per the P0 Parallel Lane above.

Build the next slice in this order:

1. Add the recovery and backup product rule.
2. Add visible Terms and Privacy acceptance at passkey creation.
3. Add visible generated-output rights notice before image generation.
4. Add public live-wall stats baseline so launch-era counts stay stable and new activity can be measured from 2026-05-21.
5. Promote `/demo` into `/onboarding` without breaking the existing proof path.
6. Make wallet state persistent per passkey identity.
7. Fix Local and External login semantics: mobile defaults Local on, desktop defaults Local off, Local off always shows WIP QR cross-device login.
8. Implement custom QR phone handoff for Chrome desktop as part of the broader External login path.
9. Build the first `kaleidoscope login` CLI pairing loop.
10. Connect Codex as the first local agent connector.
11. Land Phone Key and wallet approval inside the Kaleidoscope iOS app (same app as the capture/chat view, per D1).
12. Add macOS as the local trust and CloudKit helper.

## Open Decisions

1. Consumer name: is the backup feature simply **Kaleidoscope Backup**, or should the UI say **Ways Back In** during setup?
2. Wallet launch gate: is one backup path enough, or do we require two ways back in before spend?
3. Starter balance: $5 or $10 for app install and first wallet activation?
4. First connector: Codex, Claude Code, or Memory Crystal?
5. ~~First native app: iOS wallet/Phone Key first, or macOS helper first?~~ DECIDED 2026-07-01: iOS, starting now, as one app that is both the chat-shaped capture/memory view and the Phone Key surface. See the P0 Parallel Lane and [`claude-ios/2026-07-01--cc-mini--spec-0-7-1a-repo-reconciliation.md`](claude-ios/2026-07-01--cc-mini--spec-0-7-1a-repo-reconciliation.md).
6. Recovery contacts: launch later, or include as an optional advanced path in v1?
7. Non-Apple path: local-only plus recovery codes, 1Password passkey, hardware key, or self-hosted backup?
8. UI naming: should the login toggle remain "Local passkeys," or should it become "This device" and "Another device" once the behavior is correct?

## Co-authors

Co-Authored-By: Parker Todd Brooks <parkertoddbrooks@users.noreply.github.com>
Co-Authored-By: Lēsa <lesaai@icloud.com>
Co-Authored-By: Claude Code (Opus 4.7) <noreply@anthropic.com>
Co-Authored-By: Codex (GPT 5.5) <noreply@openai.com>
