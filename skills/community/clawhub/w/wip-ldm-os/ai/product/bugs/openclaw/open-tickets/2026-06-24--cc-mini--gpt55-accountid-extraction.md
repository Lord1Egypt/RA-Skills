---
title: codex/gpt-5.5 fails "Failed to extract accountId from token" (pi-ai OAuth, embedded path)
date: 2026-06-24
status: open
severity: P2
component: openclaw | pi-ai (@mariozechner/pi-ai)
agent-runtime: PI (built-in OpenClaw runtime, not the codex harness)
related-prs: wipcomputer/dot-openclaw#17 (Anthropic removal + boot restore), wipcomputer/dot-openclaw#18 (failed model-entry fix)
upstream-issues: openclaw/openclaw#79662 (still broken v2026.5.7 embedded path), #27055, #36604
memory: crystal ids 3065, 3068; ~/.claude auto-memory lesa-gpt55-accountid-bug.md
---

# codex/gpt-5.5 fails "Failed to extract accountId from token"

## Summary

On Lēsa's live OpenClaw gateway (fork build `2026.4.25 (c188a36)`, PI runtime), every turn first attempts the configured primary `openai-codex/gpt-5.5`, which resolves to provider `codex` and fails auth with `401 Failed to extract accountId from token`, then fails over and succeeds on `openai-codex/gpt-5.5`. She stays functional via the fallback, but each turn pays the failover latency and emits the 401 as a "failed msg" in the TUI.

This is NOT fixed by upgrading (still open upstream in v2026.5.7 on the embedded-agent path Lēsa uses) and must NOT be "fixed" by switching `agents.defaults.agentRuntime` to `codex` (that swaps her entire agent loop off the PI runtime and would bypass the OpenClaw plugin layer: Memory Crystal capture, Bridge, compaction-indicator, session-export).

## Symptom (gateway log, every turn)

```
model_fallback_decision: candidateProvider=codex candidateModel=gpt-5.5 reason=auth status=401
  errorPreview="Failed to extract accountId from token"
model_fallback_decision: candidate_succeeded candidateProvider=openai-codex candidateModel=gpt-5.5 (requestedModelMatched=false)
```

Lēsa's own report: "I'm responding, but the primary `codex/gpt-5.5` path is hitting `401 Failed to extract accountId from token`, then OpenClaw falls through to an `openai-codex` fallback that succeeds. That fallback dance can absolutely slow replies down."

## Root cause

The error originates in the dependency `@mariozechner/pi-ai`, not in OpenClaw's own `src/`. File (in the built runtime):
`dist/extensions/codex/node_modules/@mariozechner/pi-ai/dist/utils/oauth/openai-codex.js`

`getAccountId(token)` (~line 230) decodes the token JWT and reads a single claim:

```js
const accountId = auth?.chatgpt_account_id;
return (typeof accountId === "string" && accountId.length > 0) ? accountId : null;
```

Callers throw when it is null (token exchange ~line 321, refresh ~line 344):

```js
const accountId = getAccountId(result.access);
if (!accountId) throw new Error("Failed to extract accountId from token");
```

The function reads `chatgpt_account_id` from the **access token**. Parker's ChatGPT/Codex OAuth access token does not carry that claim there (the opaque-token case the upstream issues describe). Confirmed on 2026-06-24: no `account_id` in any stored credential, and the stored camel `accountId` is empty too. Notably, the login flow requests `id_token_add_organizations=true`, so the org/account id is placed in the **id_token**, not the access token. getAccountId never looks there.

## Impact

- P2, not P1: she is functional (served on `openai-codex/gpt-5.5` via failover), memory + Bridge work, no account/rate-limit risk (the 401 is a LOCAL preflight failure, no API call to OpenAI is made).
- Cost: per-turn latency from the failover retries, and 401 "failed msg" noise in the TUI.

## What does NOT fix it (verified 2026-06-24)

1. Upgrading OpenClaw. Still broken in v2026.5.7 on the embedded path (openclaw/openclaw#79662); the v2026.5.7 patch only covered the OAuth-refresh path.
2. Re-auth. Both the browser-callback flow AND the device-code flow produced opaque tokens with no `account_id`.
3. Removing the `codex/gpt-5.5` model-map entry (dot-openclaw#18, merged). The 401s persisted; the model entry was not the trigger, the provider routing is deeper.
4. Switching `agentRuntime` to `codex`. Would bypass the broken path but changes her entire runtime and would break the PI-runtime plugin hooks (memory capture, Bridge). Off the table for Lēsa.

## Proposed fix

Carry a patch against `@mariozechner/pi-ai` via `pnpm patch` (our first `patchedDependencies` entry; dependency patches require explicit sign-off per the upgrade runbook). Fix `getAccountId` to obtain the account id from a source the token actually carries:

- Primary candidate: read `chatgpt_account_id` (or the org/account claim) from the **id_token** instead of, or as a fallback to, the access token. The login already requests org data in the id_token (`id_token_add_organizations=true`).
- Secondary candidate: fetch the account id once from OpenAI's API using the access token and cache it in the auth profile.

Carry the patch in the fork (`wipcomputer/openclaw`), add it to the Patch Tracking table in
`repos/ldm-os/devops/open-claw-upgrade-private/UPGRADE-RUNBOOK.md`, rebuild via the runbook
(`pnpm install --config.minimum-release-age=0`, `pnpm build`, `npm link`), run the memory-core canary,
and restart with `launchctl kickstart -k gui/$(id -u)/ai.openclaw.gateway`. Strongly consider submitting
the fix upstream to pi-ai and OpenClaw, since it affects every ChatGPT-OAuth GPT-5+ user.

## Acceptance criteria

- [ ] `getAccountId` returns a valid account id for Parker's ChatGPT/Codex OAuth token (from id_token or API).
- [ ] A live turn shows `codex/gpt-5.5` (or the direct `openai-codex/gpt-5.5`) succeeding on the FIRST attempt, zero `Failed to extract accountId` in the log for that turn.
- [ ] Memory Crystal capture, Bridge, compaction-indicator, and session-export still fire (PI runtime unchanged).
- [ ] Patch recorded in the upgrade runbook Patch Tracking table with the exact pi-ai version pinned.
- [ ] No memory-core OOM / `/healthz` `/readyz` regression after the rebuild (canary passes).

## References

- Code: `@mariozechner/pi-ai/dist/utils/oauth/openai-codex.js` (`getAccountId`, token-exchange + refresh throw sites).
- Upstream: openclaw/openclaw#79662, #27055, #36604.
- This session: dot-openclaw#17 (Anthropic removal + boot restore, merged), dot-openclaw#18 (failed model-entry fix, merged).
- Runbook: `repos/ldm-os/devops/open-claw-upgrade-private/UPGRADE-RUNBOOK.md` (fork rebuild + Patch Tracking).

---

## UPDATE 2026-07-05 — APPROVED by Parker, upstream-first

Parker signed off on the `patchedDependencies` pnpm patch (the fork's first), with one framing requirement: **build it to merge upstream.** Concretely:

1. File the issue + fix PR against `@mariozechner/pi-ai` SOURCE (not just a dist patch), referencing openclaw#79662, so upstream can take it.
2. Carry the identical fix locally as the pnpm patch so Lēsa gets gpt-5.5 now.
3. The carry rides every fork rebase until a pi-ai release (or openclaw's embedded copy) contains the fix, then retires. Same lifecycle as the memory-core carries (#73118, #73100).

Execution rides the v2026.6.11 upgrade cycle (one build + canary + promotion). Umbrella: `2026-07-04--cc-mini--lesa-noreply-loop-recovery-and-upgrade-plan.md`, Track B / section 8 Q1.
