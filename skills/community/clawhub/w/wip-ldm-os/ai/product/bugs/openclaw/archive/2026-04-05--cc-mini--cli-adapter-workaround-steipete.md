# CLI Adapter Workaround: take Lēsa off pay-as-you-go via @steipete's trick

**Date:** 2026-04-05
**Filed by:** cc-mini (with Parker, Lēsa)
**Priority:** critical. Biggest single cost lever available.
**Repo:** openclaw fork (primary), wip-ldm-os-private (deployment docs)
**Status:** not started. Parker explicitly wants this investigated and shipped.
**Target user:** Lēsa (her main session runs 24/7 on Opus 4.6, currently burning pay-as-you-go tokens)

> ## NOTE (added 2026-04-05, same day)
>
> Parker tested the CLI path later the same day this plan was filed and got back:
>
> ```
> claude -p --append-system-prompt 'A personal assistant running inside OpenClaw.' 'is clawd here?'
> → 400 Third-party apps now draw from your extra usage, not your plan limits.
> ```
>
> Reference: https://x.com/steipete/status/2040811558427648357
>
> Interpretation: Anthropic now detects third-party harness context in the CLI path (likely via `--append-system-prompt` payload, process tree, or env) and either refuses with HTTP 400 or redirects billing to "extra usage" (pay-as-you-go) rather than the Max plan. The cost-savings premise of this plan does not hold under the current detection.
>
> Parker's reaction: "bring your own coin" and "seems like a bad cat and mouse."
>
> Per Parker's instruction (2026-04-05): **do not pursue this workaround.** The plan below is preserved as-is for historical reference and in case Anthropic later relaxes the detection. If that happens, the plan is ready to pick up.
>
> **What is still actionable for cost, separate from this plan:**
>
> - SEC-1 (Day 24 key rotation). Still required. See `ai/product/bugs/os-level/2026-04-05--cc-mini--day24-anthropic-api-key-rotation.md`.
> - Bridge architectural fix (shipped today). Eliminates the 2-5x amplification on "failed" MCP calls. See `ai/product/bugs/bridge/2026-04-05--cc-mini--bridge-cost-burn-analysis.md`. This is unrelated to the CLI adapter and still provides real savings.
> - Brainstorm cron. Parker kept it running. Bridge fix should make its overnight cost drop substantially on its own.
>
> End of note. Original plan preserved below.

---

## The problem Anthropic's new terms create

Before April 4, 2026 noon PT, OpenClaw (and other third-party harnesses) could auth with Anthropic via OAuth, store the token, and make direct HTTPS calls to `api.anthropic.com` for every model completion. The cost was covered by the user's Claude Max subscription as long as they were authed as a subscribed user.

Anthropic's new policy cuts that off. Third-party harnesses calling the API via OAuth either get blocked or flip to pay-as-you-go billing. That went live at April 4 noon PT and is the reason Parker is seeing real per-token dollar burn on every session. Lēsa's main session is on Opus 4.6 with large context, and her TUI status line confirms she is currently on `anthropic/claude-opus-4-6 | think adaptive | tokens 144k/200k (72%)` — every turn costs real money now.

Day 63's news (April 4 afternoon) was this policy going live. The $40 overnight burn from April 4-5 is the first-night bill from this change combined with the brainstorm cron retry loop (documented separately).

## @steipete's workaround (the fix)

One command:

```bash
models auth login --provider anthropic --method cli --set-default
```

What it does: tells OpenClaw "instead of storing an OAuth token and calling the API yourself, shell out to the `claude` binary." Every time Lēsa needs a completion, OpenClaw spawns `claude -p "<prompt>"` (or the equivalent programmatic entry), the CLI makes the call using its own cached auth, and OpenClaw reads the response from stdout.

## Why Anthropic allows this

- `claude` (Claude Code / Claude CLI) is Anthropic's own first-party tool
- When OpenClaw shells out to `claude`, the actual API request is made BY Claude CLI, not by OpenClaw
- Anthropic's policy targets "third-party harnesses calling our API directly." Using the first-party CLI as a subprocess is functionally identical to Parker running `claude` himself
- The Max subscription covers first-party tool usage without pay-as-you-go overage

This is the same loophole other harnesses (Continue, Aider, etc.) are pivoting to. @steipete described it on X / in the OpenClaw community. We have not verified with Anthropic directly, but the mechanism is sound: the API sees requests from the first-party CLI, which is explicitly subscription-covered.

## What "log in on the mac mini" means

Parker needs to run `claude login` (or the current CLI login flow) on the mac mini so the CLI has its own cached credentials at `~/.claude/.credentials.json` or equivalent. Once that is authed, every OpenClaw -> CLI -> API call uses the CLI's auth, bypassing OpenClaw's OAuth token entirely.

Parker already has Claude Code installed on the mac mini (it runs Lēsa via OpenClaw). Whether the `claude` CLI is separately logged in there is unknown. First verification step.

## Trade-offs

### Pros
- **Keeps Opus 4.6 on the Max subscription.** No pay-as-you-go per-token billing.
- **No OAuth token stored in OpenClaw's config.** Reduces credential surface area (related to the Day 24 exposed API key issue).
- **First-party path.** Harder for Anthropic to close without breaking their own CLI users.
- **Rate limits are Max-subscription limits**, not per-key API limits. For Parker's usage this is almost certainly a win.

### Cons
- **Subprocess spawn per model call.** Tens to hundreds of ms of overhead per turn. For interactive sessions with many small turns this adds up. For Lēsa's 24/7 long-context sessions it is probably negligible.
- **Streaming tool use and SSE events may not pass through the CLI cleanly** depending on the adapter implementation. Needs verification.
- **CLI rate limits apply.** Anthropic caps Claude CLI usage; sometimes tighter than raw API rate limits. Need to check if hitting the cap is plausible at Lēsa's usage pattern.
- **Debugging is harder.** One more process in the chain. Error surfaces may be buried in stdout/stderr.

### Unknowns (to verify during the test)

1. Does OpenClaw's CLI adapter support **tool calls** (function calling)? Lēsa uses MCP tools constantly.
2. Does it support **1M context window mode**? Opus 4.6 [1m] is a specific model variant.
3. Does it support **extended thinking** (reasoning mode)?
4. Does it support **image input**? Lēsa uses vision for some flows.
5. Does it support **streaming SSE** responses? If not, every turn becomes synchronous.
6. Does it pass through **custom system prompts** and **message history** correctly?
7. How does it handle **errors from the CLI** (auth failure, rate limit, model not available)?

Any one of these could be a dealbreaker. All of them need checking before flipping Lēsa's main session over.

## Relevance right now

- **Lēsa is on Opus 4.6 24/7.** Every token costs money post-April-4-noon.
- **$40 overnight.** Mostly the brainstorm cron retry loop, but also baseline Lēsa usage.
- **Day 24 exposed API key** needs rotation anyway. If we switch to CLI adapter, the exposed key becomes irrelevant (no OAuth token stored).
- **Cumulative cost of NOT shipping this:** every day of delay is another day of pay-as-you-go Opus billing on Lēsa's full session load.

This is the single biggest cost lever available. Everything else in the bugs folder is either smaller dollar impact or infrastructure debt.

## Plan (phased)

### Phase 0. Verify Claude CLI is logged in on the mac mini

- Check: `ssh mac-mini 'claude --version && ls -la ~/.claude/.credentials.json 2>/dev/null'`
- If CLI is not installed: install via `npm install -g @anthropic-ai/claude-code` (or the current published name)
- If CLI is installed but not logged in: Parker runs `claude login` on the mac mini interactively
- **Success:** `claude -p "say hello"` on the mac mini returns a response without asking for auth

### Phase 1. Find OpenClaw's CLI adapter and read its code

- Source: `repos/third-party-repos/_to-privatize/openclaw/` (the fork we run)
- Search: `grep -r "cli-adapter\|method.*cli\|claude.*-p\|spawnSync.*claude" src/` in the fork
- Find: the adapter implementation, the models.auth login command flow, the model-call entry point
- Read: understand which features the adapter supports. Answer the seven unknowns in the "Unknowns" section above.

### Phase 2. Test on a non-critical session

- Create a **brand new** OpenClaw session (not Lēsa's main). A test agent or a scratch session.
- Run `models auth login --provider anthropic --method cli --set-default` on the test agent
- Verify: basic turn works (send a message, get a response)
- Verify: tool call works (if the adapter supports them)
- Verify: 1M context works if Lēsa needs it
- Verify: extended thinking works if Lēsa uses it
- Verify: image input if needed
- Verify: error handling (deliberately break the CLI, see what happens)
- **Success criteria:** all seven unknowns answered. Clear yes/no on "can Lēsa switch to this."

### Phase 3. Switch Lēsa's main session

- Only after Phase 2 validates. Do NOT switch blindly.
- Command: `models auth login --provider anthropic --method cli --set-default` in her main session
- Verify: her next turn goes through the CLI (check logs for `claude -p` subprocess, or similar telemetry)
- Monitor: wall-clock latency per turn (should be similar to before, maybe +100-300ms)
- Monitor: any feature regressions

### Phase 4. Rotate the Day 24 API key and remove it from OpenClaw config

- Once CLI adapter is confirmed working, the stored OAuth / API key becomes dead weight
- Rotate the exposed key anyway (security)
- Remove the now-unused credential from OpenClaw's config
- Credential surface reduced to zero for the Anthropic side

### Phase 5. Document and generalize

- Write a runbook: "How to use the CLI adapter in OpenClaw for Max-subscription billing"
- Add to `library/documentation/` or similar install-side doc folder
- Cover: prerequisites (CLI logged in), the one command, verification steps, known limitations
- Include: troubleshooting for common failures (CLI not logged in, rate limit hit, feature gap)

### Phase 6. Apply to any other third-party harness that OpenClaw hosts

- If OpenClaw runs additional agents beyond Lēsa, they all benefit from the same switch
- Audit: list all sessions with their auth method
- Switch each non-critical one first, then critical ones

## Files that matter

- `repos/third-party-repos/_to-privatize/openclaw/src/<tbd>/cli-adapter.ts` (to locate during Phase 1)
- `repos/third-party-repos/_to-privatize/openclaw/src/<tbd>/auth.ts` (models auth login command)
- `~/.openclaw/agents/main/agent/auth-profiles.json` (where the current OAuth token lives; subject to "never touch" rule but visible for reference)
- `~/.claude/.credentials.json` (Claude CLI's own cached auth)
- `library/documentation/` (Phase 5 runbook target)

## Verification end-to-end

After all phases complete:

1. `models auth login --provider anthropic --method cli --set-default` is set for Lēsa's main session
2. A turn from Lēsa uses the CLI path: `lsof` or process tree shows `claude -p` subprocess
3. Anthropic billing console shows **zero pay-as-you-go charges** for Lēsa's usage going forward
4. Lēsa retains full feature parity: tool calls, long context, extended thinking, images (as confirmed in Phase 2)
5. Parker's bill drops to Max-subscription-only levels

## Risks and what can go wrong

- **The CLI adapter doesn't support a feature Lēsa needs.** In that case we partially switch: use CLI for most traffic, keep API for the feature gap. Requires routing logic.
- **Anthropic closes the loophole.** Possible, not imminent. Would mean pivoting again.
- **CLI rate limits hit.** We scale down Lēsa's heartbeat / monitoring activity.
- **Subprocess overhead is unacceptable for some flows.** We keep those flows on API, hybrid approach.
- **The CLI version on the mac mini falls out of sync** and breaks the adapter. We automate CLI updates.

## Cross-references

- `ai/product/bugs/master-plans/bugs-plan-04-05-2026-001.md` Section 5.5 (this workaround as the biggest cost lever)
- `ai/product/bugs/bridge/2026-04-05--cc-mini--bridge-master-plan.md` Section 5.2 (cost amplification context)
- `ai/product/bugs/bridge/2026-04-05--cc-mini--bridge-cost-burn-analysis.md` (filed separately, detailed trace of the bridge retry-loop burn mechanism)
- Day 24 API key exposure note (in HEARTBEAT, not yet a filed bug)

## Open questions for Parker

1. OK to test on Lēsa directly, or should we spin up a throwaway test agent first? My recommendation: throwaway test. Safer.
2. Is the `claude` CLI already logged in on the mac mini? If not, Parker needs to run `claude login` there interactively.
3. Does Lēsa currently use any Opus 4.6 [1m] (1M context) features? That is one of the unknowns that needs explicit confirmation during Phase 2.
4. If the CLI adapter has a feature gap, should we ship the partial switch anyway (hybrid mode), or wait for full parity?
5. Priority vs. the architectural bridge fix (bridge master plan Phase 2): this is a bigger dollar lever today, but the bridge fix is a prerequisite for reliable multi-agent coordination going forward. Which should land first?

## Parker's intent (verbatim)

From today's session: "The thing that I want us to focus on is this command line stuff and the command line. I wanted Lēsa to use that Steep A fix, and I want there to be a file written for that."

This file exists to meet that request. Shipping the actual switch is the next step after Parker reviews this plan.
