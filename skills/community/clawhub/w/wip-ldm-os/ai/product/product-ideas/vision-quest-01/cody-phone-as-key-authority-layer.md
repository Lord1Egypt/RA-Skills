# Cody: Phone as Key, Apple as Authority Layer

**Date:** 2026-04-28
**Author:** Cody
**Status:** working thesis
**Context:** Follow-on thinking from Codex Remote Control, Kaleidoscope login and demo flows, passkeys, agent authentication, multi-agent pay, and the Vision Quest sovereignty line.

## The thesis

The computer runs the agent. The phone holds the user's authority.

That is the core product idea. Agents should not ask users for passwords, vault entries, long-lived API keys, or shared secrets. When an agent needs authority, it should route that moment to the user's phone. The phone proves the user, signs the challenge, and returns only a scoped capability for the requested action.

The phone is not just a second screen. It is the user's root of authority.

## Why this matters now

Codex Remote Control exposed the pattern clearly.

The Mac is where Codex runs. It has the local files, local tools, local repo state, local Codex auth, and local guardrails. The phone is where the user can approve pairing, remote control, interrupts, payments, installs, and high-risk actions. The WIP relay can connect those surfaces, but the user's authority should live in the phone.

This is the same product direction as Kaleidoscope:

- Kaleidoscope is the app and user-facing harness.
- LDM OS is the kernel and hosted/local substrate.
- The phone is the user authority device.
- The Mac or local computer is the agent execution device.
- WIP builds the experience that lets those pieces cooperate.

Codex Remote Control is not the only proof. It is one more surface where the same model becomes useful.

## Existing proof surfaces

The phone-as-key pattern is already present in multiple WIP prototypes and flows. This note is not proposing a brand-new proof of concept. It is naming the common product architecture across the work that already exists.

### `/demo/login`

The Kaleidoscope demo login already demonstrates the onboarding pattern:

- the default flow pushes users toward phone/passkey authentication
- Chrome desktop falls back to a QR code that sends the user to the phone
- the phone creates or uses a passkey
- the desktop polls until the phone approves the session
- no password is created or shared

The interesting detail is not only "passkeys exist." It is that the desktop experience can intentionally route authority to the phone when the phone is the better key device.

### Agent QR auth

`/demo/agent.txt` and the agent-auth routes already demonstrate agent-initiated authorization:

- agent requests an authorization URL
- human opens it
- page shows the requesting agent and a passphrase/context string
- human signs in or creates an account with passkey
- agent receives a token after approval

That is the right primitive for the agent era: the agent asks, the human approves on the authority device, and the agent receives a delegated token.

### Wallet and multi-agent pay

The demo wallet and spend flow are already a seed of multi-agent pay:

- agent gets an approved token
- agent can check wallet balance
- agent can spend against a metered action
- balance updates after the action

The larger product is not just "Agent Pay" in isolation. It is multi-agent pay and multi-agent authority: different agents, tools, and devices can request scoped spending authority from the same user-controlled phone key.

### Device pairing

The `ldm pair` style flow already shows local-device onboarding:

- CLI creates a pairing code
- user signs in through Kaleidoscope
- user enters/approves the code
- server issues a device token
- local device stores that token

Codex Remote Control is a specialized version of this pattern for a Codex daemon. It should reuse the pattern rather than inventing one.

## The problem with passwords and vaults

The normal model is wrong for agents:

- make an account
- choose a password
- save it in a password manager
- share or paste a secret into a local environment
- give the agent a token, vault item, or API key
- hope it only uses that secret for the intended thing

That model was already awkward for humans. It is worse for agents.

Agents operate across tools, terminals, browsers, repositories, payment surfaces, and APIs. They constantly need narrow bursts of authority. A password or vault item is too broad, too durable, and too easy to copy into the wrong context.

The better model:

- agent asks for authority
- agent shows QR or triggers push
- phone presents a clear approval moment
- user approves with Face ID
- server verifies a signed challenge
- agent receives a scoped, revocable, short-lived capability

No passwords. No seed phrases. No vault handoff. No long-lived root secret in the agent's prompt or filesystem.

## Apple as the authority layer

WIP should not compete with Apple on hardware security.

The iPhone already gives consumers the hardware-backed key store, biometric approval gesture, recovery story, and trusted daily-use device that separate security hardware vendors try to create. For most users, adding a Ledger, Square-style hardware device, or custom security gadget only adds friction.

The better product move is to defer key custody and biometric proof to Apple, then build the agent experience on top.

This does not mean Safari-only. It does not mean the user cannot use Chrome. It means the authority primitive is rooted in Apple devices:

- iPhone holds the user's passkeys and approval keys.
- Face ID is the approval gesture.
- iCloud Keychain and Apple's platform security handle key storage and recovery.
- Mac, Chrome, web apps, local agents, and native apps can all participate as surfaces.
- The trusted key stays with the Apple device.

The market line:

> Others sell a new security device. WIP uses the security device already in your pocket.

## WIP becomes an experience company

If WIP defers the root key custody layer to Apple, WIP becomes less of a security-hardware company and more of an experience company.

That is the right shape.

WIP should not spend its product energy convincing users to trust a new key device. Apple has already earned that daily trust. Users already understand:

- scan a QR code
- Face ID
- approve
- continue

WIP's job is to make that gesture work for agents:

- pair this Mac daemon
- allow this Codex remote-control session
- approve this shell action
- pay this invoice
- install this tool
- publish this repo
- rotate this device key
- let this agent talk to that agent

Every one of those should feel like "approve on your phone," not "find a secret."

## Apple-first, not necessarily Apple-only

The first-class product should be Apple-first because the security and user experience story is cleanest there.

That does not require pretending other platforms cannot ever work. Android and other hardware-backed devices can be supported later if they meet the same authority bar. But the product center should be:

- iPhone as the primary key device
- Mac as the natural local agent computer
- Apple passkeys and platform security as the default trust primitive
- Kaleidoscope app as the native experience

Other devices can earn support by proving equivalent non-exportable key custody, attestation, recovery, and biometric approval. They should not water down the Apple-first product promise.

## Account recovery and fallback authority

The phone-as-key model still needs a recovery story. The important constraint is that recovery should not pull WIP back into the password business.

WIP should not offer a normal email-and-password fallback as the default emergency path. That recreates the exact problem this model is trying to escape: WIP would own password security, phishing resistance, credential stuffing defenses, reset flows, and all of the user confusion around shared secrets.

The better recovery model is keys first, with a small set of user-visible fallback authority methods:

1. Apple account recovery
2. Google account recovery
3. one-time backup codes
4. hardware security key

These should live on the user's profile page as explicit recovery options:

- Connect Apple for account recovery.
- Connect Google for account recovery.
- Generate backup codes.
- Add a security key.
- Add another passkey or trusted device.

Apple should be first-class because it matches the product's Apple-first authority thesis. Google can be offered as a practical secondary identity provider because many users understand it, already trust it, and may need a cross-platform recovery anchor. The key distinction is that Apple and Google are recovery identity proofs, not the root authority for every agent action.

When a user recovers through Apple or Google, WIP should put them into a limited recovery mode:

1. Verify the linked Apple or Google account.
2. Notify existing trusted devices and recovery contacts if present.
3. Require the user to add a new passkey or trusted phone.
4. Let the user revoke lost devices and daemons.
5. Rotate local device and relay keys where needed.
6. Delay or require extra approval for high-risk actions.

Recovery should not instantly restore full spending authority, remote-control authority, repo-publish authority, or access to encrypted data. It should let the user rebuild authority safely.

This creates two separate recovery concepts:

- **Account recovery:** prove that the human should regain access to the WIP account.
- **Key/data recovery:** regain access to encrypted data, daemon sessions, local devices, and private relay content.

Apple or Google can help with account recovery. They should not be treated as magic decryption keys for everything WIP routes or stores. Encrypted data recovery still needs a separate mechanism: Apple passkey/iCloud Keychain continuity, another trusted device, a hardware security key, recovery codes, or an encrypted recovery bundle that WIP cannot open alone.

### One-time backup codes

Backup codes are the simplest non-device emergency path. They should be generated only after a strong approval moment, shown once, and stored by WIP only as salted hashes.

Requirements:

- each code is single-use
- codes are displayed once and never recoverable from WIP
- using a code triggers notification to trusted devices and email
- using a code enters limited recovery mode, not full authority mode
- codes can be regenerated only after a fresh passkey or trusted-device approval

The copy should avoid "seed phrase" language unless the product truly requires seed-phrase semantics. Users understand backup codes better than wallet recovery phrases, and backup codes keep the product closer to account recovery than crypto custody.

### Hardware security keys

The advanced recovery option should be phrased as "security key," not "Ledger," unless Ledger support is actually implemented through the same WebAuthn/FIDO2 path.

Requirements:

- support standard hardware authenticators first
- make this optional and advanced
- do not force normal users into hardware-wallet concepts
- let power users add a physical key as a backup authority device
- treat the hardware key as another trusted authenticator, not a separate product center

This keeps the positioning clean. WIP is not saying hardware keys are bad. WIP is saying most users already carry a strong authority device, and hardware keys are there for people who need extra recovery or institutional policy.

### What needs to be spec'd and built

This should become a real product spec later. The build plan needs to cover:

- profile UI for connected recovery methods
- Apple and Google account-linking flows
- recovery-mode session type and permissions
- backup-code generation, storage, redemption, and rotation
- hardware security key enrollment through WebAuthn/FIDO2
- trusted-device notification on recovery attempts
- lost-device revocation and daemon key rotation
- rules for when recovery can restore identity versus when it can restore encrypted data
- copy that makes the model simple: "Use your iPhone as your key. Add Apple, Google, backup codes, or a security key for recovery."

## Relationship to Vision Quest 03

Vision Quest 03 says user data should live in the user's own Apple-backed storage path, not in WIP's database.

This note adds the authority companion:

> User data lives with the user. User authority lives on the user's phone.

The two principles reinforce each other.

Sovereign data without sovereign authority is incomplete. If the memory is in the user's iCloud but the agent still authenticates by pasted password or shared vault item, the control layer is still fragile. If the phone holds authority, every delegation can be narrow, visible, revocable, and tied to the user's approval gesture.

## Relationship to Codex Remote Control

Codex Remote Control is another usable application of the phone-as-key model. It is not the only proof of concept, and it should not be described as the thing that proves the whole thesis by itself.

The product shape:

1. Codex runs locally on the Mac.
2. `codex-daemon link` prints a QR/code.
3. User opens Kaleidoscope on phone.
4. Phone proves user identity with passkey/Face ID.
5. Phone approves daemon pairing.
6. WIP binds that daemon to the user's handle.
7. Phone opens remote-control UI.
8. Phone authorizes the session and controls the local agent.

Separate but related:

- Phone/passkey proves who may connect.
- End-to-end encryption protects what moves through WIP relay.

Those must stay distinct. Passkeys solve identity and authority. E2EE solves content privacy. Both are required for the final product.

The promotion line:

> Claude Code has Remote Control. Codex should too. WIP brings it to Codex, local-first and phone-authorized.

The stronger WIP promise once the security work lands:

> WIP routes it, but WIP cannot read it. Your phone approves it. Your Mac runs it.

## Relationship to multi-agent pay

Multi-agent pay becomes much more natural under this model.

An agent does not hold a card number, wallet seed, bank password, or full payment credential. The agent requests authority:

- "This agent wants to spend $3.20 on X."
- Phone receives a push or QR handoff.
- User sees the merchant, amount, agent, and reason.
- User approves with Face ID.
- Agent receives a payment-specific capability or confirmation.

This is Apple Pay for agents in the broader sense, even when the underlying payment rail is not literally Apple Pay. The broader target is multi-agent pay: many agents can request spending authority, but the phone remains the user's approval surface and the policy root.

## Relationship to Bridge and agent collaboration

Bridge lets agents talk to each other. Phone-as-key decides when they are allowed to.

Examples:

- Claude Code wants to ask OpenClaw to run a long background task.
- Codex wants to hand a repo operation to a different local agent.
- A web agent wants to pair with a local Mac daemon.
- An agent wants to access Memory Crystal or a sensitive bucket.

The default should not be a shared static token. The default should be phone-mediated delegation:

1. agent requests bridge authority
2. phone shows who is asking and what capability is being requested
3. user approves
4. Bridge issues scoped permission

This keeps agent collaboration from becoming a pile of shared secrets.

## Product implications

### Onboarding

Onboarding should be:

1. Install/run local tool.
2. Tool shows QR.
3. User scans with iPhone.
4. Face ID approves.
5. Device is paired.
6. Agent receives scoped local capability.

The user should not need to understand API keys, `.env` files, OAuth client secrets, or password manager sharing.

### Auth copy

The copy should not say "make an account with a password." It should say:

- Use your iPhone as your key.
- Approve with Face ID.
- No passwords to share with agents.
- Your agent receives only the permission you approve.

### Security copy

The copy should be honest and layered:

- Apple protects the keys on your device.
- WIP verifies signed challenges and issues scoped capabilities.
- WIP does not need your root secrets.
- For private work relayed through WIP, payloads should be end-to-end encrypted.

### Product surfaces

Phone-as-key should appear everywhere:

- Codex Remote Control pairing
- LDM OS install/pair
- multi-agent pay approvals
- Bridge agent-to-agent delegation
- repo publish approvals
- tool install approvals
- memory bucket access
- device revocation and key rotation

## Technical shape

The core pattern:

```text
agent/computer requests authority
        |
        v
QR or push to iPhone
        |
        v
Face ID / passkey signed challenge
        |
        v
WIP verifies identity and intent
        |
        v
scoped, revocable, short-lived capability
        |
        v
agent proceeds
```

Capabilities should be:

- narrow in scope
- bound to the requesting device or agent
- short-lived
- auditable
- revocable
- renewable only through fresh phone approval when risk is high

The phone-held key should not be converted into a broad bearer secret that agents can copy forever.

## Open questions

1. What is the exact boundary between Apple-held passkeys and WIP-issued capability tokens?
2. Which actions require fresh phone approval versus background refresh?
3. How does a user recover if they lose their iPhone, and which recovery paths restore identity versus encrypted data?
4. How does a user revoke one Mac daemon without breaking every agent?
5. What is the non-Apple support policy?
6. Can the Kaleidoscope native app become the durable key-management surface while web remains the first implementation path?
7. How do we express "Apple-first" without implying the product is browser-locked or impossible to use with Chrome?
8. What metadata can WIP retain while still keeping the user authority story honest?
9. Which actions remain blocked during limited recovery mode until the user has a fresh trusted device?

## Working language

Useful lines from this thread:

> The computer runs the agent. The phone holds the user's authority.

> The phone is not just a second screen. It is the user's root of authority.

> WIP does not need to become a hardware wallet company. The iPhone already is the consumer hardware wallet.

> Others sell a new security device. WIP uses the security device already in your pocket.

> We become less of a security company and more of a user experience company.

> Your phone approves it. Your Mac runs it.

## Closing thought

The old model asks users to share secrets with software.

The agent era needs a different model: agents request authority, and the user's phone grants it.

That makes onboarding simpler, security more legible, and delegation safer. It also makes WIP's role clearer. WIP is not trying to be Apple, Ledger, or 1Password. WIP is building the agent experience that sits on top of the security hardware users already carry.

The iPhone is the key. Kaleidoscope is the experience. LDM OS is the substrate. Agents become safe to use because authority stays with the user.
