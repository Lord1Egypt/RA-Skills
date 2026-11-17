# Ticket 02: Fix the login page so the demo is reachable again

**Date:** 2026-05-17
**Filed by:** cc-mini (reviewer session, with Parker)
**Status:** archived 2026-05-18. Implemented by `wip-ldm-os-private` PR #986, merged 2026-05-18, and deployed to the hosted-mcp lane. Parker confirmed the login/demo path works.
**Master:** `ai/product/plans-prds/comms/website/tickets/website-launch-masterticket.md`
**Surface:** `repos/ldm-os/wip-ldm-os-private/src/hosted-mcp/app/kaleidoscope-login.html` for the primary `/login` route, plus `repos/ldm-os/wip-ldm-os-private/src/hosted-mcp/demo/login.html` as the legacy fallback. Server support, if needed: `repos/ldm-os/wip-ldm-os-private/src/hosted-mcp/server.mjs` (around line 1725). There is no `src/hosted-mcp/demo/server.mjs`.
**Sequence:** ticket two. After Ticket 01 (homepage), before Ticket 03 (launch).

## Summary

The `wip.computer/login` page used to send a person who logs in or creates an account straight at the demo: a clear "Try the Demo" call to action. That action got demoted and the demo entry effectively feels lost on the plain login path. This ticket restores it, makes `/login?next=/demo` land in the demo, does the bounded login-page redesign so it reads as one product with the new homepage, and tests all of it. It does not touch Remote Control.

## Observed launch blocker

Observed by Parker on 2026-05-17 while entering from Kaleidoscope: after tapping Enter and creating a phone passkey, the flow stops on the generic success screen:

```text
Kaleidoscope
Every AI. One experience.

Welcome, user-aIsQXs2S.

Your passkey has been saved to your phone.

You can use it to sign in to any WIP Computer service.
```

That is wrong for the homepage CTA path. A person who enters from Kaleidoscope and successfully creates the passkey should continue directly into the start of Demo 1 at `/demo`, not stop on the passkey explainer screen. The passkey explainer screen is only acceptable for the plain `/login` path with no `next`, and even there "Try the Demo" must be the primary action.

## Verified evidence (from this session, do not re-derive)

1. Route truth pinned during #986: current `src/hosted-mcp/server.mjs` serves `src/hosted-mcp/app/kaleidoscope-login.html` first for `GET /login` and `GET /login/`; if that file is unavailable, it falls back to `src/hosted-mcp/demo/login.html`; if both are unavailable, it falls back to `handleLoginPage`. The live route is still hosted-mcp HTML, not the Next.js `kaleidoscope-private/web` app. The implementation must keep the `/demo` allowlist and `/demo` token handoff equivalent in both login HTML files.
2. The "Try the Demo" button still exists in the code (the success-view block, around `demo/login.html:150-158`, anchor around line 156). The no-`next` path still routes to the success-view (the `else` branch around `demo/login.html:497-509`). So this is a copy and framing regression, not a deleted button, unless the live VPS is serving a stale deploy. The coder verifies live-versus-repo before assuming code is the only cause.
3. Two commits reframed it from action-forward to passkey-explanation-forward:
   - `01ef579` "Success page: explain passkey, set account flag, Try the Demo" replaced the terse `Your passkey is saved.` with two passkey-explanation lines and demoted "Try the Demo" to the third element.
   - `6c2523a` "fix(welcome): align welcome label with saved passkey label" changed the `Welcome, <name>` line from the handle the user typed to the passkey credential label.
4. The `next` allowlist is `PAIR_NEXT_REGEX` / `REMOTE_CONTROL_NEXT_REGEX` plus `isWhitelistedNext` around `demo/login.html:284-289`, with server-side validation in `server.mjs`. `/demo` is not currently a whitelisted `next` target, so `/login?next=/demo` is not a recognized continuation today. Making it work requires adding `/demo` as an allowed next target.
5. The login page is shared infrastructure. The same file also handles the Codex Remote Control pairing handoff (`redirectToRemoteControlIfDirectLogin`, `REMOTE_CONTROL_NEXT_REGEX`, the pair-mode views). This is why the change must be surgical.

## Desired behavior

1. Log in with a referral `?next=/demo`: authenticate normally, then land in the demo. Other `next` targets (Remote Control) behave exactly as today.
2. Plain login or create account with no referral: the success screen presents "Try the Demo" as the clear primary action ("click here to see the demo"), not buried under passkey-saved explanation. The greeting uses the user's chosen handle with a sane fallback, not the raw credential label.

Key sentence (canonical, do not paraphrase): plain `/login` shows the "Try the Demo" action; `/login?next=/demo` skips the success screen and redirects directly into `/demo` after a successful login.

## Scope

- Restore action-forward framing on the no-`next` success-view (rebalance the `01ef579` and `6c2523a` changes; do not delete the passkey-saved information, demote it to one secondary line).
- Add `/demo` as an allowed `next` target so `/login?next=/demo` works.
- For `/demo` continuations, store the demo runtime handoff keys that `demo/index.html` consumes: `lesa-token` from the server-issued API key and `lesa-agent` from the server-issued agent id. Set `lesa-new-account` only in create-account flows. Keep the existing `wip_api_key` / `wip_handle` handoff for Remote Control unchanged.
- Visual alignment, CSS-only. Make login and `/demo` read as one product with the new homepage: white background, International Klein Blue on the primary action only, clean type, no decorative chrome. CSS changes only, and only outside the auth and router code blocks. No edits to the WebAuthn, `next`-handling, or redirect JS for visual reasons. Anything broader than CSS is a separate follow-up ticket, not this one (Codex review 2026-05-17).
- Inside `/demo` for Demo 1: keep it scripted. Fix only the CSS and entry-state bugs needed for the launch path. Do not connect a live Lēsa backend. Do not build Demo 2.
- Demo 1 identity bar: after a successful WebAuthn login, the demo may consume the existing server-issued API key / identity handoff that login already returns; existing valid token/session behavior must continue to work. The demo must not invent identity from URL params, arbitrary localStorage, typed handles, or other client-only claims. Any displayed name comes from the server-issued login result or a server-verified token path, with a safe fallback. Do not build a new identity architecture for this.
- Full testing per the acceptance criteria.

## Constraints (decided, do not relitigate)

1. Edit `repos/ldm-os/wip-ldm-os-private/src/hosted-mcp/app/kaleidoscope-login.html` and keep `repos/ldm-os/wip-ldm-os-private/src/hosted-mcp/demo/login.html` equivalent for this `/demo` continuation behavior. If server support is needed, the file is `repos/ldm-os/wip-ldm-os-private/src/hosted-mcp/server.mjs` (around line 1725). There is no `src/hosted-mcp/demo/server.mjs`; do not look for one. Not `kaleidoscope-private/web`. Verified hosted-mcp surface. All work happens in a fresh worktree per the master's Worktree Rule.
2. Demo 1, not Demo 2. Real login, real passkey, server-known identity, limited or alpha capabilities. Do not harden the disposable client authority as final architecture; the positive bar is server-known identity after passkey.
3. Do not touch Remote Control, Codex relay, pair/relink, daemon sync, passkey/WebAuthn, or E2EE. The diff is read line by line and proven to touch zero Remote Control branch logic (hard gate), with Remote Control and pair smoke tests as additional verification. Adding `/demo` to shared continuation logic may change bytes in `login.html`; the gate is unchanged Remote Control behavior, not byte-equality.
4. Adding `/demo` to the allowlist is a security-relevant edit: exact-match only, no wildcard, no prefix trick, applied on both the client check and the server-side validation, with a negative test that a non-allowlisted or external `next` is still rejected.
5. Verify current state before coding: whether `/login?next=/demo` routes today, the `/demo` allowlist status, how the demo currently establishes identity, and whether the live VPS matches the repo. Report findings before proposing the change.

## Acceptance criteria

- Plain `wip.computer/login` create-account and sign-in, no `next`, present "Try the Demo" as the clear primary action; greeting is the chosen handle, not the raw credential label.
- `https://wip.computer/login?next=/demo` authenticates and then lands in Demo 1.
- On the `/demo` continuation, Demo 1 receives `lesa-token` and `lesa-agent` in `sessionStorage`; `lesa-new-account` is present only for create-account flows.
- On the plain `/login` success screen, "Try the Demo" is optional and must preserve the server-issued demo handoff. It must not clear `sessionStorage`. Plain `/login` does not auto-redirect; `/login?next=/demo` is the direct authenticated continuation path.
- Existing `/login?next=/codex-remote-control/<UUID>` is behavior-unchanged. Adding `/demo` to the shared allowlist will change bytes in the same file, so the gate is not byte-equality: it is no behavioral regression on the Remote Control path AND zero edits to the Remote Control, pair, passkey, relay, or E2EE branch logic, verified by reading the diff.
- A non-allowlisted or external `next` value is still rejected, including `/demo/`, `/demo/../admin`, `//evil.com`, `https://evil`, and `/demoX`.
- Live deploy confirmed current, so the fix actually reaches users.
- Previewed before any production deploy.

## Out of scope

- Demo 2 (full server-backed wallet, memory, permissions).
- Any Remote Control, pair/relink, or E2EE change.
- Migration of login/demo to the Next.js `kaleidoscope-private` app (post-launch).
- Any login-page redesign beyond CSS-only alignment. A broader login/visual redesign is a separate follow-up ticket, deliberately not bundled into this auth-adjacent change (Codex review 2026-05-17).

## Process

1. cc-mini wrote this ticket. (this PR)
2. Codex reviews this ticket.
3. Codex codes the fix on a branch, opens a PR, hands to both reviewers.
4. CC and Codex review the PR. The CC reviewer's explicit approval is the deploy gate.
5. A separate Claude Code deployer deploys.

Next step: Codex reviews this ticket.
