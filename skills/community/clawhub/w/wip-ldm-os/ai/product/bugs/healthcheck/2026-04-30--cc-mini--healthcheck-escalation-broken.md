---
title: P1 wip-healthcheck escalation path silently broken (operator never warned)
date: 2026-04-30
severity: P1
status: open
component: wip-healthcheck
also-affects: wip-healthcheck-private
reported-by: cc-mini (observed during multi-day HB monitoring)
---

# P1: wip-healthcheck escalation path silently broken

## What happened

Throughout an extended HB monitoring window (~2026-04-27 to 2026-04-30), every wip-healthcheck cycle that reached the `escalate()` branch logged the same three-line failure pattern:

```
[WARN ] Token warning failed: 400  (or: read ECONNRESET)
[INFO ] Escalating via agent: Agent at NN% context
[WARN ] Agent escalation failed (400), trying direct iMessage
[ERROR] No escalation path. Agent unreachable, no escalationContact configured
```

The watchdog detects an alert condition (token saturation, restart loop, probe timeout, mem warnings), tries to notify the operator via the gateway agent, the gateway returns 400, falls through to direct iMessage, and the iMessage path is unconfigured. Result: the alert is logged to disk and never reaches a human.

This is the second-order failure mode of the system the watchdog was built to monitor. The watchdog's value is exactly proportional to its ability to surface alerts, and that ability is currently zero on this deployment.

## Mechanism

Source: `wip-healthcheck/healthcheck.mjs:286-321` (`escalate()`).

```
async function escalate(config, state, subject, details) {
  ...
  if (config.escalation.viaAgent) {
    log('info', `Escalating via agent: ${subject}`);
    const result = await sendToAgent(config, ...);
    if (result.ok) { ...; return; }
    log('warn', `Agent escalation failed (...)`);
  }

  if (config.escalation.escalationContact) {
    if (sendDirectIMessage(config.escalation.escalationContact, alert)) { ... }
    else { log('error', 'Direct iMessage failed'); }
  } else {
    log('error', 'No escalation path. Agent unreachable, no escalationContact configured');
  }
}
```

Two-stage fallback: agent chatCompletions -> direct iMessage. Both stages are currently failing on this deployment.

### Stage 1: agent chatCompletions returns 400

`sendToAgent()` at `healthcheck.mjs:240-269` POSTs to `http://127.0.0.1:18789/v1/chat/completions`. The gateway returns 400 because the active session (Lēsa's main session) has been at or above the `tokenCriticalPct` (92%) threshold. The very condition the watchdog is trying to alert about (a saturated agent context) is the same condition that prevents the agent from being able to receive the alert. Circular dependency.

### Stage 2: direct iMessage swallowed by empty config

`sendDirectIMessage()` at `healthcheck.mjs:271-284` sends via AppleScript. It is gated by `config.escalation.escalationContact`. The deployed config at `~/.openclaw/wip-healthcheck/config.json` (and the repo source at `wip-healthcheck-private/config.json`) has:

```
"escalation": {
  "escalationContact": "",
  ...
}
```

Empty string is falsy in JS, so the iMessage branch is skipped, and `log('error', 'No escalation path...')` fires.

Additionally, `sendDirectIMessage()` has a bare `catch {}` (`healthcheck.mjs:281-283`). Even when `escalationContact` is set, an AppleScript failure (Messages.app not running, contact not on iMessage, sandbox denial) is swallowed without logging the error.

## Evidence

Sample healthcheck log lines from `~/.openclaw/wip-healthcheck/logs/healthcheck-2026-04-29.log`:

```
2026-04-29T17:23:21.657Z [WARN ] Token warning failed: 400
2026-04-29T17:23:21.665Z [INFO ] Escalating via agent: Agent at 97% context
2026-04-29T17:23:21.667Z [WARN ] Agent escalation failed (400), trying direct iMessage
2026-04-29T17:23:21.667Z [ERROR] No escalation path. Agent unreachable, no escalationContact configured
2026-04-29T17:23:21.667Z [INFO ] OK -- pid=65345 probe=4ms fds=0/1048575 sessions=1 max-tokens=97% mem=ok
```

This pattern repeated dozens of times across 2026-04-28 and 2026-04-29 with `max-tokens` reported up to 136% (multi-session-sum metric, separate bug, but indicative of sustained pressure that should have escalated).

## Why this is P1, not P2

The watchdog also auto-restarts the gateway (`maybeRestartGateway()` at `healthcheck.mjs:213-236`) up to 3 times per 15-minute window. If the gateway enters a state requiring more than 3 restarts, the watchdog stops trying and the operator is never told. With escalation broken, that silent-give-up failure has no observability path. Two compounding failures with no operator surface is a real availability hole.

## Proposed fix (multi-part)

### Part A: configure `escalationContact` in the private deploy config (immediate)

Set `escalation.escalationContact` in `wip-healthcheck-private/config.json` to the operator's iMessage handle (`parkertoddbrooks@me.com`, the same handle Lēsa's HB skill already messages). After re-running `bash install.sh`, the deployed config at `~/.openclaw/wip-healthcheck/config.json` will have a populated fallback path. The next escalation that fails through to Stage 2 will reach Parker via direct iMessage instead of dying silently.

This is a one-line config change. Tracked separately for repo-discipline reasons (private repo, not this one). Filed as a follow-up PR against `wip-healthcheck-private`.

### Part B: surface AppleScript errors in `sendDirectIMessage()` (public repo)

Replace the bare `catch {}` at `healthcheck.mjs:281-283` with a logged error. Currently:

```
} catch {
  return false;
}
```

Should be:

```
} catch (err) {
  log('error', `Direct iMessage send failed: ${err.message}`);
  return false;
}
```

This means a failed iMessage send is at least visible in the log instead of indistinguishable from "we never tried."

### Part C: add a sentinel-file last-resort fallback (public repo)

When both Stage 1 and Stage 2 fail, write a sentinel file at `~/.openclaw/wip-healthcheck/escalation-failed.log` (append-only, with timestamp + alert payload). The operator who eventually checks status can see "we tried to escalate at 17:23:21 about token saturation but had no path." This is a third-tier fallback that does not require any external service to function.

### Part D: detect token-saturation specifically and short-circuit Stage 1 (public repo, optional)

If the watchdog already knows the active agent session is over `tokenCriticalPct`, calling that same agent's chatCompletions endpoint is guaranteed to fail. Skip Stage 1 in that case and go straight to Stage 2. Reduces noise in the log (one failed call instead of two) and slightly faster fallback.

This is a polish item, not required for the core fix.

## Action items

- [ ] **A:** Populate `escalationContact` in `wip-healthcheck-private/config.json`. Filed separately as a config-only PR against `wip-healthcheck-private`. Pending operator authorization to set the value.
- [ ] **B:** Log AppleScript errors in `sendDirectIMessage()` in public `wip-healthcheck/healthcheck.mjs:271-284`. Single-line catch-clause change.
- [ ] **C:** Sentinel-file fallback when both stages fail. New helper, ~10 lines.
- [ ] **D (optional):** Skip Stage 1 when token-saturation is the alert condition.

Parts B, C, D land via the public `wip-healthcheck` repo and flow through `wip-release` per repo policy.

## Out of scope (filed elsewhere or pre-existing)

- The `max-tokens=NNN%` multi-session-sum metric returning values > 100% is a separate bug. The metric sums token usage across all sessions and historical exports, not just the active one. Not addressed here.
- The gateway returning 400 on chatCompletions when the active session is at or above its limit is correct behavior in OpenClaw. Not a bug in the gateway.

## How this was found

Observed during a multi-day HB monitoring loop (2026-04-27 to 2026-04-30) where the watchdog log was tailed every ~10 minutes. The "No escalation path..." line appeared on essentially every cycle that crossed the warning threshold. Tracking the conditional flow in `healthcheck.mjs` confirmed the cause.
