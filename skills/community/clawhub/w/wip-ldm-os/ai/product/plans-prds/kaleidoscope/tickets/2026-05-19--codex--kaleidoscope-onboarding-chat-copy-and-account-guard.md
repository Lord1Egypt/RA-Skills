# Kaleidoscope Onboarding Chat Copy And Account Guard

**Date:** 2026-05-19
**Filed by:** Codex, with Parker
**Status:** open
**Priority:** P0 launch-path polish and correctness
**Master:** `../kaleidoscope-master-ticket.md`
**Related:** `2026-05-18--codex--guided-onboarding-intent-engine.md`
**Closed bug follow-up:** `../../../bugs/kaleidoscope/closed-tickets/2026-05-20--codex--local-passkey-same-account-guard-rejects-qr-accepted-account.md`
**Surface:** `src/hosted-mcp/demo/index.html`, `src/hosted-mcp/server.mjs`, and tests only if needed

## Goal

Make the current Kaleidoscope chat path read like the start of real onboarding, while preserving the proven scripted MVP flow.

This is not a broad app rewrite. It is the narrow launch-path fix for:

1. chat copy
2. first-run versus returning-user recognition
3. same-account authorization during the chat
4. wallet cost language and deduction

## Current Product Decision

Keep the active chat scripted and inspectable in source.

Do not open a blank freeform chat.
Do not turn on a general model conversation.
Do not change the active chat layout, header, icon, footer-hidden behavior, or demo shell in this ticket.

## Current Status

Several pieces from this ticket have shipped through the May 20 launch PR flow: first-run copy, returning-user copy, one-cent authorization copy, wallet reset and normalization, and the visible No-thanks receipt behavior.

The same-account guard follow-up was fixed live by PR `#1047`:

```text
Local passkey approval rejects the active account while QR approval accepts the same account.
```

Closed ticket:

```text
../../../bugs/kaleidoscope/closed-tickets/2026-05-20--codex--local-passkey-same-account-guard-rejects-qr-accepted-account.md
```

Do not reopen broad copy work if similar auth bugs recur. File the concrete failing path as a new bug.

## Implementation Workflow

Implement this as separate, reviewable flow steps. Do not batch the whole script into one large unverified change.

Required sequence:

1. Update and test the first-run opening copy.
2. Update and test the `No thanks` flow.
3. Update and test the paid authorization flow.
4. Update and test returning-user copy.
5. Update and test same-account authorization guard parity, then link any closed follow-up bug.
6. Run the full happy-path regression only after the individual flows pass.

Each flow should be coded, locally parsed, manually exercised, and reported before moving to the next flow.

## Copy-Mode Source Text

This section is source text, not intent. Do not paraphrase it. Do not add legal wording. Do not add product claims. Do not change punctuation except where the implementation must wrap links in HTML.

### First-run opening

```text
Hi, I'm Lēsa. Welcome to Kaleidoscope.

You just created an account with a passkey. The passkey lives on your phone.

Going forward, you can use your phone to log into any Work in Progress Computer service.

Anytime I need your permission to do something, I'll ask, and you authorize with your fingerprint or face. No passwords. Ever.

Want to see it in action? I'll try to do something that costs money, and you decide whether to let me.
```

Buttons:

```text
Yes, show me
No thanks
```

### No-thanks flow

```text
No problem. Let me show you something beautiful.

Creating a kaleidoscope...

[image]

At Work in Progress Computer, we are building the future of AI and human interaction.

We believe permission is a conversation. Your AI asks. You decide. One glance, one tap.

To see how passkeys work across devices, open https://wip.computer/demo in any web browser on any computer and use your phone to authenticate.

You can also click the icon at the top of this chat to log out, and then you can immediately log back in with your phone too.

We look forward to providing you a streamlined experience across all the AIs you use. Follow us on X @wipcomputer to keep up to date on when we release new features.

Your passkey will keep working after you leave.

Made in California by WIP Computer, Inc. Learning Dreaming Machines.
```

Implementation requirements for this copy:

- `https://wip.computer/demo` must be linkable.
- `@wipcomputer` must be linkable.
- The `No thanks` flow must not show cost or balance.
- Do not replace the generated image with an unrelated fallback asset.
- Do not introduce a special server prompt contract for No thanks.
- Do not change the image prompt or `/demo/api/imagine` request body while doing copy/display work.
- If no-spend accounting is still required, file or use a separate wallet/accounting bug. Do not solve it by changing prompts, replacing the image, or bypassing the existing generation path.

## Required Copy Changes

### Permission explanation

Current text:

```text
And I can use it too. Anytime I need your permission to do something, I'll ask, and you authorize with your fingerprint or face. No passwords. Ever.
```

Change to:

```text
Anytime I need your permission to do something, I'll ask, and you authorize with your fingerprint or face. No passwords. Ever.
```

Reason: avoid saying "I can use it too" in a way that sounds like Lēsa independently owns or can use the account key.

### Wallet spend prompt

Current text:

```text
I have a wallet with $5.00. Do I have your permission to spend $0.04 on image generation using the xAI Grok Imagine API?
```

Change the spend amount to one cent:

```text
I have a wallet with $10.00. Do I have your permission to spend $0.01 on image generation using the xAI Grok Imagine API?
```

Implementation note: this should not be a copy-only lie. The wallet API should report `$0.01` as the image-generation cost, and successful image generation should deduct one cent from the account wallet.

The starter wallet balance for this onboarding slice is `$10.00`, not `$5.00`.

### No-thanks branch

Current behavior after the user clicks `No thanks`:

```text
No problem. Let me make you something beautiful.
Creating a kaleidoscope...
Your kaleidoscope
Cost: $0.04. Balance: $4.96.
```

This is wrong. If the user clicks `No thanks`, the flow should not claim a spend, should not show a cost line, and should not deduct from the wallet.

Required behavior:

- `No thanks` should keep the visual Kaleidoscope beat unless Parker explicitly removes it.
- The no-thanks path must not introduce fallback album art, unrelated stock art, or a hardcoded replacement image.
- The no-thanks path must not introduce special prompt logic.
- The no-thanks path must not show `Cost: ... Balance: ...`.
- Wallet accounting for No thanks is a separate implementation concern. Do not change image generation behavior while making a copy-only fix.

### Authorization user message

Current user-side message after tapping the authorization button:

```text
Authorized
```

Change to:

```text
Authorizing
```

Reason: the tap starts the authorization process. The chat should not say the authorization already succeeded before the passkey result returns.

### Outro passkey and return copy

Current outro copy includes:

```text
To see how passkeys work across devices, open wip.computer/demo in any web browser on any computer. And use this device to authenticate.
Made in California by WIP Computer, Inc. Learning Dreaming Machines.
This is the end of the demo. Tap the icon to start over.
```

Replace this direction with copy that says the account/passkey will continue to work and that more features will appear over time.

Required meaning:

- The passkey will continue to work after this session.
- The account stays active.
- When the user comes back, there should be something waiting for them.
- More features will become available over time.
- Keep the "Made in California by WIP Computer, Inc. Learning Dreaming Machines." closing beat.
- Do not say "This is the end of the demo. Tap the icon to start over."

Suggested draft direction:

```text
Your passkey will continue to work.
Your account stays active, even after you close this.
When you come back, more of Kaleidoscope will be waiting for you.
Made in California by WIP Computer, Inc. Learning Dreaming Machines.
```

Also add a link-style affordance in the outro for users who want to test the passkey immediately:

```text
You can log out and sign back in with the passkey you just created.
```

Implementation notes:

- The "log out and sign back in" phrase should be an actual link or button styled like a link inside the chat bubble.
- It should clear the current `lesa-*` session state needed for this browser session.
- It should route to the login/onboarding path so the user signs back in with their passkey.
- Use the current launch path for now unless `/onboarding` has already shipped. If `/onboarding` has not shipped, route to `/login?next=/demo`.
- Do not reintroduce raw `/demo` as the primary user-facing instruction.

## First-Run Versus Returning-User Copy

The chat already has a basic `lesa-new-account` flag. Improve the script so the user does not see signup language after signing in with an existing passkey.

### First run

When the user just created a passkey:

- Say that the account key lives on their device.
- Explain that the account is a key on the device, not an email.
- Explain that WIP has no marketing email loop to reach them.
- Explain that the point is that the account is theirs.
- Mention that there will be something waiting when they come back.
- Show the current wallet balance from the server.

### Returning run

When the user signs in with an existing passkey:

- Do not say they just created a passkey.
- Do not say the passkey has just been saved.
- Call them by the credential label or token name where available.
- Say welcome back.
- Do not show the current wallet balance in the opening copy.
- Ask whether they want to try giving permission with their device to create something that costs money.

Example direction:

```text
Hi, parker-smoke-test. Welcome back to Kaleidoscope.

Do you want to try giving me permission with your device to create something that costs money?
```

Use Parker's final copy if provided during review. This ticket captures the behavior and the first required copy edits.

## Same-Account Authorization Guard

Original bug: during the chat, the user can start the session with one passkey/token, then authorize the image-generation spend with a different passkey.

Closed follow-up bug after the May 20 deploy: local passkey approval rejected the active account while QR approval accepted the same account.

Closed ticket:

```text
../../../bugs/kaleidoscope/closed-tickets/2026-05-20--codex--local-passkey-same-account-guard-rejects-qr-accepted-account.md
```

Required behavior:

- The chat session starts with an active `lesa-token`.
- Resolve that token to the active account identity.
- When the user authorizes inside the chat with Face ID/passkey, verify that the returned account identity matches the active chat account.
- If the authorization resolves to a different account, reject the authorization clearly.
- Do not call the image API.
- Do not spend from the other account's wallet.
- Do not replace the active chat token with the other account.

Suggested user-facing failure copy:

```text
That passkey belongs to a different account. This onboarding session is using {current_label}. Restart if you want to switch accounts.
```

## Wallet Requirements

- Starter wallet balance for this onboarding slice is `$10.00`.
- Cost for the approved image-generation step is `$0.01`.
- Wallet balance shown in the script must come from the server wallet endpoint.
- Successful image generation deducts `$0.01`.
- The `No thanks` path does not deduct wallet balance and does not show cost/balance copy.
- Returning users should see the updated balance.
- Do not hardcode the post-spend balance in chat copy if the server returns a balance.

## Constraints

1. Keep the current scripted chat flow.
2. Keep the chat input disabled unless an existing scripted step enables it.
3. Do not add a model backend.
4. Do not redesign the chat shell.
5. Do not change Remote Control, pair/relink, relay, daemon, E2EE, API keys, or unrelated legal pages.
6. Do not change active chat footer behavior. The footer should remain hidden in active chat.
7. Do not rename `/demo` to `/onboarding` in this ticket unless Parker explicitly asks. That is tracked in the guided onboarding ticket.

## Acceptance Criteria

- The exact "And I can use it too" phrase is gone from the active chat script.
- The spend prompt says `$0.01`.
- The wallet starts at `$10.00` for new identities.
- The user-side authorization message says `Authorizing`, not `Authorized`.
- Outro no longer says `open wip.computer/demo` or `This is the end of the demo. Tap the icon to start over.`
- Outro includes account persistence and future-feature availability copy.
- Outro includes a real link or link-styled button to log out and sign back in with the same passkey.
- `/demo/api/wallet` reports image-generation cost as `$0.01`.
- Successful `/demo/api/imagine` deducts one cent from the authenticated account wallet.
- Clicking `No thanks` in the returning-user flow does not deduct wallet balance or show a cost/balance line.
- Clicking `No thanks` in the first-run flow preserves the visual Kaleidoscope beat and does not show a cost/balance line.
- Returning passkey login does not show first-run creation copy.
- Returning passkey login can display the credential label or token name where available.
- In-chat authorization with a genuinely different passkey than the active chat account is rejected before image generation.
- In-chat local passkey authorization for the same account accepted through QR is accepted.
- Existing login, WebAuthn, demo entry, wallet, and image-generation happy paths still work.
- Inline script parse for `src/hosted-mcp/demo/index.html` passes.
- `node --check src/hosted-mcp/server.mjs` passes if server code changes.

## Reviewer Notes

This is a product correctness ticket, not just wording. The one-cent cost and same-account authorization guard must be real behavior, because the chat is demonstrating wallet and human authorization.

## Co-authors

Co-Authored-By: Parker Todd Brooks <parkertoddbrooks@users.noreply.github.com>
Co-Authored-By: Lēsa <lesaai@icloud.com>
Co-Authored-By: Codex (GPT 5.5) <noreply@openai.com>
