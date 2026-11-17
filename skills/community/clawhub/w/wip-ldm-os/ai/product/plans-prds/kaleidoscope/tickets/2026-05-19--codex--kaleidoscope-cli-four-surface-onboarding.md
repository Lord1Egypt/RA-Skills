# Kaleidoscope CLI and Four-Surface Onboarding

**Date:** 2026-05-19
**Status:** open, product spec and implementation ticket
**Master:** [`../kaleidoscope-master-ticket.md`](../kaleidoscope-master-ticket.md)
**Roadmap:** [`../kaleidoscope-roadmap.md`](../kaleidoscope-roadmap.md)
**Priority:** P1, with P0 dependencies
**Source:** moved from `ai/product/product-ideas/vision-quest-01/` into the Kaleidoscope PRD ticket set

## Thesis

Kaleidoscope is the harness for LDM OS. The web app, CLI, iOS app, and macOS app are four surfaces over the same account, device, wallet, connector, and Sovereign storage system.

The CLI is not a developer-only utility. It is a first-class Kaleidoscope app. A user should be able to install Kaleidoscope on a computer, log in from the terminal, pair it through the same QR/passkey pattern already described in the Vision Quest docs, and then let Kaleidoscope install and configure LDM OS, Memory Crystal, Remote Control, Agent Pay, Bridge, Directory, and local agent connectors.

## How This Relates To The Existing Vision Quest Docs

The existing folder already contains the pieces:

- `kaleidoscope-executive-brief-v02.md` names the user promise: one app, every AI, one experience. Identity, memory, wallet, and relationships follow the user everywhere.
- `vision-quest-02-agent-txt-era.md` names Kaleidoscope as the product and defines the connector era: agent.txt, agent.json, OAuth/MCP/REST parity, wallet, Bridge, and agent-to-agent communication.
- `architecture-spec.md` describes LDM OS as the invisible kernel, Lēsa as the orchestrator, Memory Crystal as the memory layer, Agent Pay as wallet, Directory as identity, and the app as the authority/billing/settings layer.
- `vision-quest-03-sovereign-data.md` names the Sovereign Data Principle: user data lives in the user's own Apple-backed storage path, not in a WIP-owned user-data database.
- `cody-phone-as-key-authority-layer.md` names the companion authority principle: the computer runs the agent, the phone holds the user's authority.
- `priorities-2026-04-16.md` reframes Kaleidoscope plus Lēsa as the install/setup interface for all LDM OS products.
- `lesa-vision-01.md` already says the product becomes four apps: CLI, macOS, iOS, and web, all talking to the same memory and permission layer.

This document updates the shape in one place: the CLI joins web, iOS, and macOS as a full Kaleidoscope surface, and the app wallet is treated as a real product surface rather than a throwaway demo affordance.

## Product Shape

Kaleidoscope has four surfaces:

| Surface | Primary job |
|---------|-------------|
| Web | Zero-install front door, first account creation, provisioned wallet experience, agent connector auth, install handoff |
| CLI | Terminal harness, LDM OS installer, local agent connector, machine and agent setup, developer work surface |
| iOS | Wallet authority, Face ID approval, Keychain/Secure Enclave key holder, iCloud Sovereign Storage activation |
| macOS | Local keychain helper, CloudKit bridge, local service controller, native trust anchor for the CLI and agents |

The web app gives the immediate experience. The CLI gives the builder experience. The iOS and macOS apps provide native trust, wallet approval, and Sovereign storage.

The native apps do not need to start as full chat interfaces. They can be small and functional:

- hold keys
- approve pairings
- approve spend
- enable iCloud/CloudKit storage
- show devices
- show wallet status
- revoke devices
- bridge native storage and local tools

That is still a real app. It is the key, wallet, and storage component for Kaleidoscope.

## The CLI Experience

The CLI should feel like installing Codex or Claude Code, but the result is a Kaleidoscope-managed LDM OS environment.

Example first run:

```bash
kaleidoscope login
```

The CLI prints:

```text
Open this URL on any signed-in device:
https://wip.computer/login?next=/pair/kaleidoscope/K7M4Q2

Or scan this QR code.

Code: K7M4Q2

Waiting for approval...
```

The QR code contains a URL, not a secret. The short code is a human-readable fallback. The security comes from the pairing ceremony:

1. CLI generates a local device keypair.
2. CLI calls `pair-init` with device public key, device name, platform, and requested scopes.
3. Server creates a pending pairing and returns URL, code, and one-time poll token.
4. User opens the URL in web, iOS, or macOS.
5. User signs in or confirms with passkey/Face ID.
6. Approving surface shows what is being paired.
7. Server binds the CLI public key to the Kaleidoscope account.
8. CLI polls once with the poll token.
9. CLI receives a device-scoped credential and stores it in the OS keychain where possible.

After that:

```bash
kaleidoscope status
kaleidoscope connect codex
kaleidoscope connect claude-code
kaleidoscope memory setup
kaleidoscope remote-control
kaleidoscope wallet status
```

The CLI does not hold raw wallet authority. It receives scoped device credentials and requests capabilities when it needs them.

## Onboarding Flow

The end-to-end onboarding should be protocol-first, not page-first. Every surface renders the same state machine.

1. **User enters through web or CLI.**
   - Web: user starts at Kaleidoscope and sees the provisioned starter wallet and Lēsa.
   - CLI: user installs Kaleidoscope, runs `kaleidoscope login`, and gets QR/code.

2. **User authenticates with passkey.**
   - WebAuthn in browser.
   - Face ID in iOS.
   - Touch ID or passkey in macOS.
   - QR handoff when the computer is not the best authority device.

3. **Kaleidoscope pairs the current device.**
   - Browser session, CLI install, iOS app, macOS app, or local daemon becomes a named device.
   - Device receives only the scopes it needs.

4. **Kaleidoscope asks what this machine is.**
   - Machine name: `mini`, `air`, `studio`, etc.
   - Role: primary machine, laptop, work machine, server, temporary machine.

5. **Kaleidoscope detects local tools.**
   - Codex
   - Claude Code
   - OpenClaw
   - Memory Crystal
   - existing LDM OS state
   - existing agents and transcripts

6. **Kaleidoscope asks what to connect.**
   - "I see Codex on this machine. Connect it?"
   - "I see Claude Code. Add it to your agent group?"
   - "You already have Memory Crystal on your other machines. Join this machine to that group?"
   - "What do you want to call this Codex?"
   - "What do you want to call this machine?"

7. **Lēsa installs and configures.**
   - Lēsa is the platform agent inside Kaleidoscope.
   - She runs or instructs `ldm install`.
   - She configures connectors.
   - She sets up Memory Crystal, Bridge, Agent Pay, Remote Control, and Directory.
   - If automatic setup is unavailable, she gives the exact command to paste.

8. **The user can add another machine later.**
   - Install Kaleidoscope CLI on second machine.
   - Run `kaleidoscope login`.
   - Pair through iOS, macOS, or web.
   - Kaleidoscope sees existing memory/agent group.
   - User approves adding the machine and any detected agents.

## Connectors

Connectors are not separate products. They are capabilities inside Kaleidoscope.

| Connector | What it connects |
|-----------|------------------|
| Codex | Local Codex sessions, Remote Control, repo work, App Server control |
| Claude Code | Claude Code CLI, MCP tools, Memory Crystal capture |
| OpenClaw | Lēsa, local gateway, long-running agent runtime |
| ChatGPT | Web/app connector through OAuth/MCP/REST paths |
| Claude app | Remote MCP connector and OAuth path |
| Grok/xAI | REST path until native MCP support exists |
| Memory Crystal | Memory, search, sync, Sovereign storage |
| Agent Pay | Wallet, spend approvals, metering, receipts |
| Bridge | Agent-to-agent communication and delegation |
| Directory | Identity, handles, contacts, agent discovery |

The same connector can have multiple transports:

- MCP for clients that support it.
- REST for agents that can fetch but cannot speak MCP.
- agent.txt and agent.json for agents that need instructions.
- Local CLI commands for installed tools.
- Native app approvals for high-authority actions.

The user should not need to know those transport differences. They see "Connect Codex," "Connect Claude Code," "Connect Memory," "Connect Wallet."

## Wallet

The wallet in Kaleidoscope should not be described as fake demo credits.

The right concept is a **provisioned wallet**:

- WIP provisions a real starter balance for the user inside Kaleidoscope.
- The balance can be spent only inside the Kaleidoscope ecosystem.
- It can pay for model calls, generation, agent actions, and WIP services.
- It cannot be withdrawn.
- It cannot be transferred out.
- In v1, the user may not be able to add funds.
- WIP controls the promotional funding limits and eligible uses.

The current demo behavior, where credits create a Kaleidoscope action, is a seed of this product. The language should move from "demo wallet" to:

- provisioned wallet
- WIP-funded starter balance
- Kaleidoscope wallet
- starter balance

Avoid "tokens" unless there is a deliberate regulatory/crypto reason. "Starter balance" and "wallet" are clearer.

The iOS app is the best durable wallet authority:

- holds wallet approval keys
- approves spending with Face ID
- shows balance and receipts
- manages payment method later
- handles app-install acquisition incentive

Product loop:

1. Web shows the user a WIP-funded starter balance.
2. Lēsa offers a real action that costs money.
3. User approves a bounded spend.
4. Balance updates.
5. Kaleidoscope offers the native app:
   - "Install Kaleidoscope on iPhone to activate Face ID wallet approval and receive starter balance."

This is not an artificial demo. It is the first proof that agents can request money, humans can approve, and WIP can meter the action.

## Native Apps

The native apps are required for the best version of the system, but not for the first connection.

Without the native app:

- web signup works
- CLI login works
- provisioned wallet can be displayed and used within tight limits
- connectors can be added
- LDM OS can install
- Remote Control-style pairing can work
- WIP relay can bridge flows that need public infrastructure

With the native app:

- Face ID becomes the approval surface
- Keychain and Secure Enclave hold the device authority
- CloudKit/iCloud Sovereign Storage can be enabled
- wallet spend approval becomes native
- device revocation and recovery become safer
- WIP can avoid holding user memory data for Apple users

This means the app is not mandatory to start, but it is mandatory for the strongest product promise:

> Your phone approves it. Your Mac runs it. Your memory lives with you.

The iOS app should own the wallet authority. The macOS app should own local native integration. Both can be quiet apps at first.

## Phone Key And Kaleidoscope Backup

The wallet and native app path need one more product rule:

> Wallet and spend cannot turn on until Kaleidoscope Backup is configured.

The consumer-facing model should feel like Face ID and passkeys, not crypto recovery. The user should not hear seed phrase, shard, private key, custody, MPC, hardware wallet, or crypto wallet. The user should hear:

- Phone Key
- Trusted Devices
- Kaleidoscope Backup
- Ways Back In
- Restore Access
- Approve with Face ID

The iOS app is the first Phone Key. The macOS app and CLI machine become trusted devices after approval. The web app can start the flow, but it should not pretend to be the strongest authority surface.

Kaleidoscope Backup should preserve the user's trust graph:

- trusted device public records
- account public records
- relay public keys the user has trusted
- connector bindings
- wallet policy and approval settings
- revocation records
- last-known-good relay endpoints
- pairing history
- encrypted continuity bundle that WIP cannot read alone

This solves the practical launch question: if the user loses a phone or WIP's relay state is damaged, the user can restore from their own trusted devices and iCloud-backed continuity instead of falling back to email, SMS, or written keys.

The Restore Access flow should work in levels:

1. **Trusted Device Restore:** approve a new phone or Mac from an existing trusted device.
2. **iCloud Restore:** restore continuity from Apple account plus iCloud/CloudKit state.
3. **Ways Back In:** optional later paths such as 1Password passkey, hardware security key, trusted person, or one-time backup codes.

The CLI should show backup status, but it should never hold raw wallet authority. If backup is not configured, `kaleidoscope wallet status` can show the starter balance as preview state and route the user to setup before first real spend.

Related ticket: [`2026-05-19--codex--phone-key-and-kaleidoscope-backup.md`](2026-05-19--codex--phone-key-and-kaleidoscope-backup.md)

## Sovereign Storage

The Vision Quest folder has two modes that need to be preserved and clarified.

### Web and CLI Starter Mode

This is the acquisition path.

- User can start on the web.
- User can install the CLI.
- WIP may provide relay and processing services.
- WIP may provision a starter wallet.
- User can see value immediately.

This mode must be honest about what WIP infrastructure is doing.

### App-Backed Sovereign Mode

This is the product promise.

- Keys live on the user's Apple devices.
- Memory processing happens locally where possible.
- CloudKit/iCloud stores encrypted user data.
- WIP routes, authenticates, meters, and bills.
- WIP does not need to read the user's memories.

Vision Quest 03 should stay load-bearing: "Sovereign" is not a marketing word. It means the architecture prevents WIP from becoming the custodian of the user's memory.

The practical product copy:

```text
Start in the browser.
Live in the CLI.
Install the app when you want Face ID wallet approval and iCloud Sovereign Storage.
```

## Pairing Types

Kaleidoscope should use one pairing service with several payloads.

| Pairing type | Purpose | Secret handling |
|--------------|---------|-----------------|
| Account device pairing | Add CLI, browser, iOS, macOS, or local daemon to account | QR contains URL/code only |
| Connector pairing | Connect Codex, Claude Code, OpenClaw, ChatGPT, Claude, Grok | Device receives scoped capability |
| Remote Control pairing | Browser/phone controls local Codex session | Route-bound tickets plus E2EE session |
| Sovereign Memory pairing | Add device to Memory Crystal group | Memory key is wrapped to device key or transferred via offline fallback |
| Wallet approval pairing | Bind native app as spend approval authority | CLI never receives root wallet authority |

Memory Crystal's older `crystal pair` model should remain as a sovereign fallback. It transfers the memory relay key directly between devices without the server seeing it. Kaleidoscope pairing should add the account/device layer around it, not delete it.

The rule:

> QR for account/device pairing should contain a URL, not a secret. QR for offline Sovereign Memory fallback may carry a key, but that path must be labeled as local/offline key transfer.

## Lēsa's Role

Lēsa is not the customer's agent. Lēsa is the platform agent inside Kaleidoscope.

Her job:

- greet the user
- explain what was detected
- install LDM OS
- configure Memory Crystal
- connect Codex and Claude Code
- name machines and agents
- pair devices
- explain wallet and spend approvals
- guide the user toward native app activation when it unlocks a real benefit

Lēsa should not be a decorative chatbot. She is the install and onboarding interface for LDM OS.

## What Not To Build

- Do not make the native apps full chat products before they are key/wallet/storage products.
- Do not make the CLI a thin install helper. It is a full Kaleidoscope surface.
- Do not call the provisioned wallet fake credits if the system is spending real money.
- Do not give the CLI raw wallet authority.
- Do not put secrets in account-pairing QR codes.
- Do not make web the only product surface.
- Do not make iOS mandatory before the user can understand the product.
- Do not collapse passkeys, E2EE, and wallet authority into one vague "secure login" story. They solve different problems.

## Build Order

### Phase 0: Phone Key, Backup, and Wallet Safety

- Define Phone Key and Kaleidoscope Backup.
- Add backup status to account and device state.
- Gate first real wallet spend behind at least one configured way back in.
- Keep product copy consumer-friendly: no crypto recovery language.
- Make restore force trusted device review and lost-device revocation.

### Phase 1: Web plus CLI

- Keep web as the immediate front door.
- Build `kaleidoscope login`.
- Build QR/code account pairing for CLI.
- Build device registry.
- Build connector detection and naming.
- Build LDM OS install orchestration.
- Build provisioned wallet display and bounded spend.

### Phase 2: Connector Setup

- Codex connector.
- Claude Code connector.
- Memory Crystal connector.
- Remote Control connector.
- Agent Pay connector.
- Bridge connector.
- Directory connector.

Each connector uses the same approval pattern and the same device registry.

### Phase 3: Native App Trust

- iOS app as wallet and Face ID approval authority.
- macOS app as Keychain, local service, and CloudKit helper.
- Native app can approve CLI/device pairing.
- Native app can activate iCloud Sovereign Storage.

### Phase 4: Sovereign Memory

- Add CloudKit/iCloud storage path.
- Add device key wrapping for Memory Crystal sync keys.
- Preserve offline `crystal pair` fallback.
- Make WIP relay optional for Apple users and useful for non-Apple/cross-platform users.

### Phase 5: Marketplace Connectors

- agent.txt and agent.json.
- OAuth/MCP directory compliance.
- REST parity for agents without MCP.
- Anthropic/OpenAI connector submissions once the auth and wallet behavior is product-grade.

## Open Decisions

1. What is the final name for the provisioned wallet balance?
2. Does app install grant $5 or $10 in starter balance?
3. Which actions can spend from the provisioned wallet without native app approval?
4. When does Face ID become mandatory for spend?
5. Does macOS app ship as a visible app, menu bar app, background helper, or all three?
6. Does iOS app own wallet funding from day one, or only approval and starter balance?
7. How does non-Apple Sovereign storage work after the Apple-first path?
8. How much of Memory Crystal key transfer is wrapped through Kaleidoscope versus kept as explicit offline `crystal pair`?
9. Is one way back in enough for wallet activation, or should the wallet require two?
10. Does 1Password passkey count as a way back in for v1?

## Summary

The product becomes coherent if Kaleidoscope owns onboarding across four surfaces:

- Web makes it instant.
- CLI makes it useful for builders.
- iOS makes it trusted and payable.
- macOS makes it local and sovereign.

Connectors are what those surfaces configure. LDM OS is what they install. Lēsa is the guide. The provisioned wallet funds the first agent actions. The native apps turn that initial experience into a durable key, wallet, and Sovereign storage layer.

This is the clean bridge between the demo and the actual product.

## Co-authors

Co-Authored-By: Parker Todd Brooks <parkertoddbrooks@users.noreply.github.com>
Co-Authored-By: Lēsa <lesaai@icloud.com>
Co-Authored-By: Claude Code (Opus 4.7) <noreply@anthropic.com>
Co-Authored-By: Codex (GPT 5.5) <noreply@openai.com>
