---
title: "Codex Remote Control iOS App Plan"
date: 2026-05-06
author: Codex
status: active-plan
surface: codex-remote-control
priority: P0
---

# Codex Remote Control iOS App Plan

## Decision

Codex Remote Control should become an iOS app in parallel with the web dogfood path.

The website remains the fastest place to prove the protocol, fix relay behavior, and keep a universal fallback. The iOS app becomes the product surface for real use: secure account administration, pairing, token wallet, Face ID approvals, passkeys, secret access, and the best mobile Remote Control experience.

Do not wait for the website to become perfect before starting the app. Do not fork the backend behavior into two products. Build one Remote Control protocol and two clients:

- Web: proving ground, fallback client, shareable URL, debug surface.
- iOS: secure primary client, wallet, approvals, token custody, polished mobile experience.

## Product Thesis

The web page proves that Remote Control works from any browser.

The iOS app is why a user should actually trust it.

Remote Control lets a phone drive a live local Codex session. That is useful on the web, but the higher-value product is native:

- Face ID before sensitive actions.
- Keychain and Secure Enclave-backed storage.
- Passkeys for account presence.
- Token wallet and secrets broker.
- Native push notifications for approvals.
- App-level control over background reconnect and session state.
- A cleaner mobile UI than a browser page can provide.

The product line should be:

```text
Works on the web.
Best and safest in the app.
```

## What Must Be Native

These features belong in the iOS app first. The website can expose limited admin later, but should not become the authority for secrets or wallet custody.

| Capability | Native iOS role |
|---|---|
| Token wallet | Store and unlock user tokens, payment credentials, and agent wallet state through Keychain-backed storage. |
| Face ID approval | Gate sensitive operations with `LocalAuthentication`: unlock wallet, reveal secret, approve agent payment, rotate daemon key. |
| Passkeys | Use native passkey flows for fresh presence and account authentication. |
| Secret broker | Let agents request password-like secrets. The app prompts the user, unlocks with Face ID, then releases only the approved secret or scoped credential. |
| Pairing and relink | Pair Mac, daemon, browser, and future devices. Re-key daemon identity with explicit biometric confirmation. |
| Security alerts | Show "daemon key changed", "new device paired", "agent requested secret", and "remote session active" as native alerts. |
| Token hygiene | Keep long-lived tokens out of browser storage and handoff cookies. Use opaque one-time codes or native app-to-server exchange. |
| App Store trust | Give users a clear installed app that owns the sensitive parts instead of asking them to trust a browser tab. |

## What Can Stay Web

The web Remote Control page is still valuable. It should not be thrown away.

Keep the web surface for:

- one-click Remote Control links from Codex;
- desktop browser dogfood;
- cross-platform fallback where no app is installed;
- protocol debugging;
- authenticated transcript viewing;
- lightweight send and Stop;
- app install prompts and handoff.

The web should not own:

- long-lived credential custody;
- wallet unlock;
- password-like secret storage;
- daemon key replacement without native presence;
- high-value account administration once the app exists.

## Shared Protocol Contract

The web and iOS app must consume the same protocol. Do not let the app become a second implementation with its own session rules.

Shared events:

```text
connection.status
e2ee.handshake.started
e2ee.handshake.ready
session.attach.started
session.attach.completed
session.history
session.user_message
session.assistant_delta
session.assistant_message
session.turn_started
session.turn_completed
session.turn_interrupted
session.error
session.title_updated
```

Shared commands:

```text
session.attach
session.send
session.interrupt
session.close
session.history.read
daemon.identity
pair.start
pair.complete
pair.relink
secret.request.approve
secret.request.deny
wallet.unlock
wallet.lock
```

The app can wrap these in native APIs, but the backend contract should stay common.

## MVVM App Shape

Build the iOS app as MVVM from the start.

Suggested modules:

```text
RemoteControlSessionView
RemoteControlSessionViewModel
RemoteControlSessionStore
RemoteControlClient
WebSocketRemoteControlClient
E2EESession
PairingView
PairingViewModel
TokenWalletView
TokenWalletViewModel
SecretRequestView
SecretRequestViewModel
BiometricGate
KeychainStore
PasskeyCoordinator
DeviceRegistryStore
SecurityEventStore
```

Core protocols:

```swift
protocol RemoteControlClient {
    func connect(threadId: String) async throws
    func attach(threadId: String) async throws
    func send(_ text: String, threadId: String) async throws
    func interrupt(threadId: String) async throws
    var events: AsyncStream<RemoteControlEvent> { get }
}

protocol BiometricGate {
    func requirePresence(reason: String) async throws
}

protocol SecretStore {
    func store(_ secret: SecretRecord) async throws
    func resolve(id: SecretID, reason: String) async throws -> SecretValue
}
```

View models should own UI state. Network and crypto should live behind protocols so the first app can run against mocked event streams before real E2EE is wired.

## App Submission Track

The app should be scoped for App Store submission as soon as the Remote Control loop is reliable.

First submission candidate:

- Sign in with passkey.
- Pair local daemon.
- Show active Remote Control session.
- Attach to one Codex thread.
- Hydrate transcript.
- Send messages.
- Receive streamed Codex replies.
- Stop active turn.
- Show device and connection status.
- Use Face ID for relink or sensitive key operations.

Do not include the full wallet in the first submission unless it is already production-safe. It is better to ship the app with the secure shell, pairing, Face ID gate, and Remote Control than to delay everything for full payments/secrets.

Second submission candidate:

- Token wallet.
- Secret broker.
- Agent payment approvals.
- Push notifications for requests.
- Account/device admin.
- Daemon key rotation warnings.

## Build Phases

### Phase 0: Web Dogfood Stabilization

Keep using the web page to prove backend correctness.

Required before app real-network work:

- mobile composer safe area fixed;
- refresh hydration stable;
- Stop shared state verified;
- security blockers tracked and ordered;
- event normalization stable enough for a second client.

### Phase 1: Native Skeleton With Mock Client

Build the iOS app without depending on the live relay yet.

Deliver:

- MVVM session screen;
- transcript rendering;
- composer and Stop button;
- connection status line;
- mock event stream;
- mocked hydration;
- mocked interruption;
- iPhone Safari/Chrome visual lessons applied natively.

This lets UI, state shape, and App Store shell move while backend security work continues.

### Phase 2: Real Attach And Transcript

Wire the app to the same Remote Control relay path used by web.

Deliver:

- WebSocket connect;
- E2EE handshake;
- session attach;
- history hydration;
- live event stream;
- send;
- Stop;
- reconnect.

Acceptance:

- TUI to app works.
- App to TUI works.
- Browser and app can both attach to the same thread.
- Refresh/reopen app hydrates the transcript.
- Stop interrupts only the bound thread.

### Phase 3: Native Pairing And Relink

Move pairing and relink into app-first flows.

Deliver:

- QR/deep-link pairing;
- passkey sign-in;
- Face ID before daemon key replacement;
- device list;
- "key changed" warning;
- relink recovery flow;
- server-side pair status token support.

This phase should close the security review findings around relink and daemon key replacement.

### Phase 4: Token Wallet And Secret Broker

Add native-only sensitive surfaces.

Deliver:

- Keychain-backed token wallet;
- Face ID unlock;
- scoped secret approval;
- secret request inbox;
- audit history;
- deny and expire paths;
- no long-lived bearer tokens in browser storage.

The web can request an approval, but the app owns the secret and token release.

### Phase 5: Native Polish And App Store Hardening

Deliver:

- accessibility pass;
- small-screen layout pass;
- degraded connection states;
- privacy copy;
- security explainer;
- App Store screenshots;
- TestFlight build;
- App Review notes that explain local daemon, encrypted relay, and user-controlled AI session access.

## Security Boundary

The app should make the trust model clearer, not more complicated.

Core rules:

- Codex still runs locally on the user's Mac.
- WIP relay remains transport only.
- The app owns user presence, wallet unlock, and sensitive approvals.
- The website does not store long-lived secrets.
- The daemon is bound to an immutable account id, not a user-chosen display handle.
- Browser and app sessions are bound to one authorized thread after attach.
- Relink is re-keying. Re-keying requires fresh presence.

The iOS app should become the place where a user can answer:

```text
Which devices are paired?
Which Codex session is remote-controlled right now?
Which app or browser is attached?
Which secrets has my agent requested?
Which token or wallet action did I approve?
```

## Relationship To Existing Plans

This plan depends on the existing iOS app as core direction:

`ai/product/plans-prds/bridge/2026-03-30--cc-mini--ios-app-as-core.md`

That plan says the phone is the center for pairing, secrets, payments, notifications, and approvals. This document applies that strategy specifically to Codex Remote Control.

It also depends on the current one-URL live-session contract:

`ai/product/plans-prds/codex-remote-control/2026-05-04--codex--remote-control-v1-one-url-live-session.md`

The app must not weaken that contract. It should use the same live thread model and make the secure surfaces native.

## Near-Term Agent Handoff

Ask the iOS coder to start here:

1. Create the MVVM app skeleton for one Remote Control session.
2. Implement the transcript screen against mocked Remote Control events.
3. Implement composer, Stop button, and connection status state.
4. Define Swift models for the shared event and command contract.
5. Stub `RemoteControlClient`, `E2EESession`, `BiometricGate`, and `KeychainStore`.
6. Do not implement token wallet yet. Put the interfaces in place.
7. Do not fork protocol behavior from web. Consume the same event shapes.

Ask the web/backend coder to continue here:

1. Finish mobile composer safe area.
2. Keep refresh hydration and Stop green.
3. Close security blockers in the ordered P0/P1 security track.
4. Normalize event shapes so iOS and web render the same session model.

## Non-Goals

- Do not make iOS wait for all web polish.
- Do not build a separate native-only Remote Control backend.
- Do not put long-lived token wallet custody in the web page.
- Do not ship full wallet/secrets in the first app submission if that delays the Remote Control shell.
- Do not turn the app into a dashboard before the one-thread Remote Control flow is excellent.
- Do not make the relay the session authority. The local Codex runtime remains authoritative.
