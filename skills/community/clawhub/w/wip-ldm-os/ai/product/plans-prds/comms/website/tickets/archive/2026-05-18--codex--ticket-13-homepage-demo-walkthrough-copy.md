# Ticket 13: Add the demo walkthrough to the homepage letter

**Date:** 2026-05-18
**Filed by:** Codex, with Parker
**Status:** archived 2026-05-18. Implemented by `wip-websites-private` PR #52 and polished by PR #53; walkthrough copy is live.
**Master:** `ai/product/plans-prds/comms/website/tickets/website-launch-masterticket.md`
**Depends on:** Ticket 04 homepage static hardening
**Surface:** `repos/wip-web/wip-websites-private/wip.computer/index.html`

## Summary

The homepage letter works, but it should more explicitly explain what the current demo proves. Add a short walkthrough immediately after the account-key paragraph.

Insert after this existing paragraph:

```text
Your account is a key on your device, not an email. We have no way to market to you. That is the point: it is yours, and there is something waiting when you come back.
```

The new copy should explain the current demo in the same direct, plain voice as the letter:

```text
In the demo:

1. You sign in with your phone's biometrics.
2. A portable identity token is created automatically.
3. You meet Lēsa.
4. You authorize an xAI microtransaction from your phone.

That is the walkthrough. From there, the same phone-rooted identity can log you into any other machine without starting over. Over time, it can also carry your AI context with you. This first demo stops at identity, authorization, and Lēsa.
```

## Desired behavior

- The homepage explains exactly what a user experiences in Demo 1.
- The copy makes clear that this demo stops at identity, authorization, and Lēsa.
- The copy does not overclaim full memory, wallet, or cross-machine AI-context portability as already complete in the demo.
- The new copy appears in raw HTML so agents and reviewers can read it without JavaScript execution.

## Scope

Allowed:

- Add the walkthrough copy to `wip.computer/index.html`.
- Minimal spacing/style adjustment if the inserted copy needs existing paragraph/list spacing.
- If the homepage has duplicated source copy in `app.js`, update only what is required to keep rendered copy aligned.

Not allowed:

- No homepage redesign.
- No CTA changes.
- No typewriter changes.
- No architecture section rewrite.
- No demo/login/hosted-mcp changes.
- No deploy changes.

## Acceptance criteria

- The new walkthrough appears after the account-key paragraph.
- Raw HTML contains the four numbered steps.
- The copy includes `This first demo stops at identity, authorization, and Lēsa.`
- Existing primary CTA remains `https://wip.computer/login?next=/demo`.
- No React, Babel, JSX, unpkg, or Google Fonts are reintroduced.
- Run `git diff --check`.
- Run `node --check wip.computer/app.js` if `app.js` changes.

## Out of scope

- Changing Demo 1 behavior.
- Changing the Speedrun application.
- Changing `agent.txt` or `llms.txt`.
- Changing GitHub org README copy.
