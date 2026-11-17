# Kaleidoscope Guided Onboarding Intent Engine

**Date:** 2026-05-18
**Filed by:** Codex, with Parker
**Status:** open, product spec and implementation ticket
**Master:** [`../kaleidoscope-master-ticket.md`](../kaleidoscope-master-ticket.md)
**Roadmap:** [`../kaleidoscope-roadmap.md`](../kaleidoscope-roadmap.md)
**Priority:** P0
**Product:** Kaleidoscope, Lēsa, Sapien ID, Agent Pay, LDM OS onboarding
**Current surface:** `src/hosted-mcp/demo/`
**Product target:** Kaleidoscope onboarding, not a throwaway demo path

## Summary

The current `/demo` path proved the product loop: a person signs in with a phone-rooted passkey, meets Lēsa, approves a real AI action, and sees an image generated through a wallet-backed permission moment.

The next step is not to build a separate "real app" beside the demo. The next step is to turn the current demo into the real onboarding path.

Rename the product concept from demo to onboarding:

```text
Demo Kaleidoscope -> Start Kaleidoscope / Start onboarding
/demo -> /onboarding
```

The current scripted flow should remain scripted on purpose. It should become a guided onboarding engine: finite choices first, real actions underneath, model help only after the user reaches a safe help point.

## Product Principle

Kaleidoscope should not open as a blank ChatGPT-style prompt.

The first experience should be controlled:

1. The user logs in.
2. Lēsa greets them and knows whether this is a first run or a returning session.
3. Lēsa offers a small set of allowed onboarding paths.
4. Each path is a choose-your-own-adventure script with explicit steps.
5. Real actions are attached only to specific approved steps.
6. The chat input stays disabled until the script opens a safe question point.
7. At that point, the model can turn on with bounded context and a constrained task.

This is not fake chat. It is guided agent onboarding with real authorization behind it.

## Why This Exists

The launch path currently looks like a demo because it is named `/demo`, uses demo language, and presents a single scripted proof. That was correct for Speedrun. It is not the long-term product shape.

The product should be:

```text
Scripted onboarding.
Real authorization.
Constrained model help.
```

People should be able to inspect the source and see the script. That is a feature. The source reveals what the app will and will not do before it asks for identity, money, tools, or install access.

## Current Behavior To Preserve

Preserve these launch-proven behaviors:

- passkey signup and sign-in
- `/login?next=/demo` authenticated continuation
- direct gated entry instead of unauthenticated raw demo
- scripted Lēsa conversation
- disabled freeform chat during the scripted flow
- explicit choice buttons
- phone biometric authorization before spend
- wallet/cost language
- image generation as a real server-backed action
- xAI API call behind the server, not from the browser

## Product Rename

### Required naming direction

The product path should become onboarding:

- Human-facing language should stop saying "Demo Kaleidoscope" where the experience is becoming product onboarding.
- The canonical path should become `/onboarding`.
- `/demo` may remain as a compatibility redirect or legacy alias, but it should not be the primary path in new copy.
- Homepage CTAs should eventually point to `/login?next=/onboarding`.
- Login next allowlist should include exact `/onboarding`, not a wildcard or prefix.

### Migration rule

Do not break the current launch path while renaming.

Suggested staged approach:

1. Add `/onboarding` as an alias served by the same current code.
2. Add exact `/onboarding` to the safe next allowlist.
3. Update copy and CTAs to prefer `/login?next=/onboarding`.
4. Keep `/demo` as a redirect or compatibility alias until traffic and docs are migrated.
5. Only remove `/demo` after a separate compatibility decision.

## Guided Intent Engine

The current script should evolve into a declarative script or state-machine model.

Minimum model:

```text
script_id
step_id
speaker
message
choices
allowed_actions
requires_auth
requires_wallet
opens_model_help
next_step
```

Initial onboarding paths should be finite. Example first menu:

1. Set up Remote Control.
2. Connect one AI.
3. Understand my passkey and wallet.
4. Try a paid AI action.
5. Ask Lēsa a question after setup.

These names can change, but the shape matters: the user picks one of a few product paths. They do not start with an unrestricted prompt.

## Model Handoff Rule

The model should not be active at the beginning.

The model can turn on only at a defined step, such as:

```text
Do you have questions before we continue?
```

When the model turns on, it must receive bounded context:

- the selected onboarding path
- current step
- what has been completed
- what actions are allowed next
- relevant docs for that path
- current account/wallet state
- safety boundaries

The model should answer questions, explain steps, and help the user proceed. It should not invent new installation or authorization actions outside the selected path.

## First-Run vs Returning Script

The script must branch based on account state.

### First run

If the user just created a passkey:

- Say that the account key lives on their device.
- Explain that their account is a key on the device, not an email.
- Explain that WIP has no marketing email loop to reach them.
- Explain that the point is that the account is theirs.
- Tell them there will be something waiting when they come back.
- Create or initialize the onboarding wallet.

### Returning run

If the user signs in with an existing passkey:

- Do not say they just created a passkey.
- Do not show signup language.
- Call them by the credential label or token name where available.
- Say welcome back.
- Show the current wallet balance.
- Continue from the appropriate onboarding state if available.

Example:

```text
Welcome back, parker-smoke-test.
Your passkey is still the key to this account.
Your wallet balance is $9.88.
```

## Token-Bound Reauthorization

The current chat authorization step has a correctness bug: a user can start the chat with one passkey/token and then approve the spend with a different passkey.

That must not be allowed.

Follow-up after the May 20 launch PRs: the opposite mismatch also appeared. Local passkey approval could reject the same account that QR approval accepted. That concrete bug was fixed live by PR `#1047` and closed here:

```text
../../../bugs/kaleidoscope/closed-tickets/2026-05-20--codex--local-passkey-same-account-guard-rejects-qr-accepted-account.md
```

Requirement:

- If the session entered onboarding with token/account A, any later Face ID/passkey authorization inside that onboarding session must resolve to the same account A.
- If the user authenticates as account B during an in-chat approval, the approval must fail clearly.
- If the user authenticates as account A through either local passkey approval or QR approval, both paths must succeed.
- The error should explain that this onboarding session belongs to account A and that the user should restart if they want to switch accounts.
- Do not silently switch the session identity from A to B.
- Do not spend from B's wallet while the chat session is displaying A.

Acceptance:

- Sign in as account A.
- Reach the spend approval step.
- Authenticate with account B.
- The approval is rejected.
- No wallet spend occurs.
- The UI remains in a recoverable state.

## Wallet Behavior

The wallet should become persistent per identity.

Near-term implementation can be a simple registry or database-backed ledger. It does not need full payments infrastructure in the first pass, but it must behave consistently.

### Product target

When the user first onboards, Kaleidoscope creates a wallet for that identity.

Initial product language:

```text
We created a wallet for you. It starts with $10.
When Lēsa does something that costs money, it comes out of this wallet.
```

The target is a real wallet balance. If launch implementation uses simulated credit while payments are still being wired, label the implementation honestly in code and docs, but keep the product behavior correct: the balance belongs to the account and persists across sessions.

### Required behavior

- Wallet is keyed by the authenticated identity, not by browser session.
- First onboarding creates or initializes a balance.
- Returning login reads the same balance.
- Each image generation spend subtracts the cost.
- If the user runs the action four times at $0.04, the displayed balance decreases by $0.16.
- Balance shown in the script must come from the server wallet state, not a hardcoded constant.
- The spend authorization must be token-bound to the same account as the current onboarding session.

### Example

1. User creates account.
2. Wallet starts at `$10.00`.
3. User authorizes one image at `$0.04`.
4. Wallet shows `$9.96`.
5. User leaves and returns.
6. Lēsa says welcome back and shows `$9.96`.
7. User authorizes three more images.
8. Wallet shows `$9.84`.

## Restart and Cross-Device Script

The script should invite the user to test the identity loop.

Desired script beat:

```text
You can test this right now.
Tap the icon on the left to sign out and come back.
Or open the onboarding URL on any other machine.
Use the passkey you just created, and I will know it is you.
```

Behavior:

- The left icon should route through login/onboarding intentionally.
- The returning script should recognize the existing account.
- The returning script should not reset wallet or first-run copy.
- The user should be able to test the passkey on another machine once QR/desktop handoff allows it.

## First Implementation Slice

Today's practical fix should not attempt the whole product engine. It should make the current flow stop lying about being a throwaway demo and fix the account correctness issues.

Implement in this order:

1. Add `/onboarding` as a served alias for the current `/demo` experience.
2. Add exact `/onboarding` to login `next` allowlists.
3. Update user-facing copy from demo-first language to onboarding language where it is now product-facing.
4. Keep `/demo` as a compatibility alias.
5. Add first-run vs returning script branches.
6. Bind in-chat reauthorization to the current account.
7. Make wallet balance persistent per identity with a simple ledger.
8. Update script language to explain the wallet starts at `$10.00` and spends come from that wallet.
9. Keep chat input disabled until a scripted step opens it.

## Launch Hotfix vs Dev Lane

Parker may choose to ship a few narrow fixes directly to live for the a16z Speedrun path so the experience works better immediately. That is an emergency launch posture, not the long-term development model.

Allowed launch hotfixes:

- copy changes from demo language to onboarding language
- `/onboarding` alias and exact login `next` allowlist
- first-run vs returning script branch
- token-bound reauthorization check
- simple wallet persistence and balance display
- direct bugs that block the current onboarding path

Not allowed as live hotfixes:

- broad app rewrite
- production Kaleidoscope migration
- new model-backed freeform chat
- Remote Control installation automation
- payment infrastructure changes beyond the existing wallet demo ledger
- auth model replacement

After the Speedrun rescue fixes, this work must move to a dev or staging situation immediately.

Required follow-up:

1. Define where hosted-mcp onboarding dev runs.
2. Define how `/onboarding` is previewed before production.
3. Define how Parker tests dev without touching production wallet/token state.
4. Define the deployer rule: production receives scoped, reviewed fixes only; ongoing onboarding iteration happens in dev.
5. Cross-link this with the website deploy topology cleanup ticket and the Kaleidoscope production app boundary plan.

The point is not to slow down the current rescue. The point is to stop living permanently in production for product iteration.

## Security And Product Boundaries

- No wildcard `next` allowlist.
- No account switching inside an active onboarding session.
- No spend without same-account passkey approval.
- No long-lived broad token shown to the user.
- No model freeform mode before a scripted help step.
- No real install mutation without explicit human approval.
- No agent-run install on Parker's production machine during validation unless Parker explicitly delegates that exact run.

## Out Of Scope

- Full native iOS app.
- Full `kaleidoscope-private` migration.
- Full model-backed Lēsa chat.
- Full Agent Pay production payments.
- Removing `/demo` compatibility.
- Remote Control installation automation beyond scripted guidance and dry-run unless separately ticketed.

## Acceptance Criteria

- `/onboarding` exists and can be reached through `/login?next=/onboarding`.
- `/demo` still works or redirects compatibly.
- Homepage and agent-facing copy can point at onboarding without implying a throwaway demo.
- Returning users get returning copy, not first-run passkey-created copy.
- Lēsa can call the returning user by credential label or token/account name when available.
- Wallet state persists per account.
- Wallet starts at `$10.00` for a new onboarding account.
- Repeated spends decrement the same account wallet.
- Reauth with a different passkey during the spend approval step is rejected.
- No wallet spend happens on mismatched reauth.
- The scripted flow remains inspectable in source.
- Chat input remains disabled until explicitly opened by a script step.
- Existing launch image generation still works after the rename.

## Review Notes For Coder

Before coding, inspect current live source:

- `src/hosted-mcp/demo/index.html`
- `src/hosted-mcp/demo/login.html`
- `src/hosted-mcp/app/kaleidoscope-login.html`
- `src/hosted-mcp/server.mjs`
- website CTA source in `repos/wip-web/wip-computer-website/static/wip-websites-private/wip.computer/`

Preserve existing Remote Control, pair/relink, relay, daemon, E2EE, and MCP behavior unless a separate ticket explicitly scopes those changes.

Stop at PR. Parker tests live onboarding manually after deploy.
