# Phone Key and Kaleidoscope Backup

**Date:** 2026-05-19
**Filed by:** Codex, with Parker
**Status:** open, product spec and implementation ticket
**Master:** [`../kaleidoscope-master-ticket.md`](../kaleidoscope-master-ticket.md)
**Roadmap:** [`../kaleidoscope-roadmap.md`](../kaleidoscope-roadmap.md)
**Priority:** P0
**Product:** Kaleidoscope, Phone Key, wallet, passkeys, iOS app, macOS app, CLI

## Summary

Kaleidoscope needs a consumer-friendly restore model before wallet and spend become real product surfaces.

The product should not fall back to email, SMS, passwords, seed phrases, or "write down your private key." It should feel like Face ID, passkeys, Apple Pay, and iCloud restore.

The user-facing model:

```text
Your phone is your key.
Kaleidoscope Backup helps you get back in.
Choose your trusted devices and ways back in.
No passwords. No seed phrases. No recovery emails.
```

The technical model can use strong key wrapping, device-bound credentials, signed trust records, and threshold recovery internally. Do not expose that vocabulary to consumers.

## Product Language

Use these terms in consumer product copy:

| Product term | Meaning |
|---|---|
| Phone Key | The user's phone is the normal authority device. |
| Trusted Device | A phone, Mac, iPad, CLI machine, or app install the user has approved. |
| Kaleidoscope Backup | The user's device-backed restore setup. |
| Ways Back In | User-friendly recovery options. |
| Restore Access | The flow for a new or replacement device. |
| Approve with Face ID | The normal approval gesture. |

Do not use these terms in consumer copy:

- seed phrase
- shard
- private key
- custody
- MPC
- hardware wallet
- sovereign recovery
- crypto wallet

Investor and technical docs may explain the cryptographic design. Product onboarding should not.

## Why This Is P0

Kaleidoscope is passkey-first. That is the correct product direction, but passkey-first creates a launch requirement: users need a clear way back in if they lose a device.

The wallet makes this urgent. If Kaleidoscope provisions a real starter balance or allows spend, users must not be one lost phone away from either permanent lockout or an insecure email reset.

Launch rule:

> Wallet and spend cannot turn on until Kaleidoscope Backup is configured.

This does not mean the user has to understand cryptography. It means the app must quietly create durable, user-owned continuity before money or high-authority connector actions are enabled.

## Recovery Levels

### Level 1: Trusted Device Restore

The user still has another trusted device.

Flow:

1. User installs Kaleidoscope on a new phone or Mac.
2. User chooses **Restore Access**.
3. Existing trusted device receives an approval request.
4. User approves with Face ID or Touch ID.
5. New device becomes trusted.
6. Old/lost devices are reviewed and optionally revoked.
7. Wallet resumes after review.

This should be the happy path.

### Level 2: iCloud Restore

The user has Apple account continuity and iCloud/CloudKit state.

Flow:

1. User installs Kaleidoscope on a replacement Apple device.
2. User signs in to Apple and opens Kaleidoscope.
3. Kaleidoscope finds the user's backup record.
4. User approves with passkey/Face ID.
5. Kaleidoscope restores account continuity.
6. User reviews trusted devices.
7. High-authority actions stay paused until review completes.

This is the Apple-first continuity path.

### Level 3: Ways Back In

The user needs help beyond one device or one iCloud restore path.

Possible ways back in:

- another trusted device
- 1Password passkey
- hardware security key
- trusted person
- one-time backup codes, shown once and stored only as hashes by WIP
- WIP blind recovery assist that cannot recover the account alone

The user should see this as a setup checklist, not as a cryptography lecture.

Example copy:

```text
Add one more way back in.

If you lose this phone, Kaleidoscope can help you restore access from another trusted device, a passkey manager, or someone you trust.
```

## What Gets Backed Up

Kaleidoscope Backup should preserve the user's trust graph, not make WIP the owner of the user's authority.

Backed-up records should include:

- trusted device public records
- account public records
- relay public keys the user has trusted
- connector bindings
- wallet policy and approval settings
- revocation records
- last-known-good relay endpoints
- pairing history
- encrypted restore bundle for continuity

Private device authority stays in platform secure storage where possible. If a continuity bundle is stored, it must be encrypted locally so WIP cannot read it.

The restore bundle should let the user rebuild authority when enough trusted continuity paths agree. It should not let WIP recover the user alone.

## Wallet Gate

Wallet activation has two states:

| State | Behavior |
|---|---|
| Wallet preview | User can see starter balance and understand how spend works. |
| Wallet active | User can approve spend after Kaleidoscope Backup is configured. |

Required launch behavior:

1. First onboarding may show starter balance.
2. Before first real spend, Kaleidoscope checks backup status.
3. If backup is not configured, Lēsa explains that wallet needs a way back in.
4. User configures Kaleidoscope Backup.
5. Wallet becomes active.
6. Spend approval remains same-account and Face ID/passkey-bound.

Example product copy:

```text
Before you spend from your Kaleidoscope wallet, set up one way back in.
That way, if you lose this phone, you can restore access without a password or recovery email.
```

## CLI And Web Behavior

The web and CLI can start the user, but they should not pretend to be the strongest authority surfaces.

Web:

- creates account with passkey
- shows starter wallet
- explains Kaleidoscope Backup
- can start Restore Access
- points user to iOS/macOS for full Phone Key behavior

CLI:

- pairs as a trusted machine
- stores only device-scoped credentials
- can request approval from phone
- never receives raw wallet authority
- can show backup status

iOS:

- primary Phone Key
- Face ID approval surface
- wallet approval authority
- Restore Access coordinator

macOS:

- local trust anchor
- Keychain helper
- CloudKit bridge
- local service controller
- trusted device for restore

## Security Requirements

1. WIP cannot recover the user's account alone.
2. WIP cannot decrypt the user's continuity bundle alone.
3. Email and SMS are not first-class recovery methods.
4. Backup records must be signed by trusted devices.
5. Restore must trigger device review.
6. Restore must rotate or revoke lost-device access.
7. Wallet must pause on suspicious restore until review completes.
8. Existing trusted devices should be notified when restore begins.
9. Recovery codes, if used, are shown once and stored only as salted hashes.
10. Logs must never contain raw credentials or restore secrets.

## Product Requirements

- The setup must be understandable in one screen.
- The user should not write down a key.
- The user should not be required to provide email or phone number.
- The user should understand which devices are trusted.
- The user should be able to revoke old devices.
- The user should be able to add another way back in later.
- The wallet should make backup feel necessary, not scary.

## First Implementation Slice

1. Add backup status to the account/device model.
2. Add `backup_required` gate before first real wallet spend.
3. Add onboarding script copy that explains Phone Key and Kaleidoscope Backup.
4. Add device list with trust status.
5. Add one restore path first: another trusted device or Apple/iCloud continuity.
6. Add wallet pause and review after restore.
7. Add technical records for relay public keys, device public records, and revocations.

Do not try to implement every possible recovery path in the first slice. The first slice should make the product rule real and leave room for recovery contacts and backup codes later.

## Acceptance Criteria

- User can create passkey account without email or password.
- User sees starter wallet but cannot perform real spend until backup is configured.
- User can configure at least one way back in.
- Backup status is stored per account.
- CLI can display backup status.
- iOS or macOS can approve a new device as trusted.
- Restore flow forces trusted device review.
- Lost devices can be revoked.
- Wallet resumes only after review.
- Product copy does not use seed phrase, shard, MPC, custody, hardware wallet, or crypto wallet language.

## Out Of Scope

- Full payments infrastructure.
- Full non-Apple restore design.
- Enterprise recovery policy.
- Recovery contact UX beyond optional future design.
- Replacing all existing passkey code in one pass.

## Open Questions

1. Is one way back in enough for wallet activation, or should wallet require two?
2. Does 1Password passkey count as a way back in for v1?
3. Do backup codes ship in v1 or later?
4. Should wallet activation require iOS specifically, or can macOS approve the first spend?
5. What is the exact consumer phrase: Kaleidoscope Backup, Ways Back In, or both?
6. What happens if a user refuses backup: read-only wallet preview, local-only mode, or no wallet?

## Co-authors

Co-Authored-By: Parker Todd Brooks <parkertoddbrooks@users.noreply.github.com>
Co-Authored-By: Lēsa <lesaai@icloud.com>
Co-Authored-By: Claude Code (Opus 4.7) <noreply@anthropic.com>
Co-Authored-By: Codex (GPT 5.5) <noreply@openai.com>
