# Threshold Tuning Guide

The three guards in `rl-runtime-guard` are tuned by defaults that work
for typical OpenClaw workstation usage. Your deployment may need
different values.

## Quick reference

| Threshold | Default | When to raise | When to lower |
|-----------|---------|---------------|---------------|
| `complexTaskThreshold` | 400 chars | Agent is missing multi-step instructions on shorter tasks | Agent is getting "plan first" reminders on trivial tasks |
| `retryLoopThreshold` | 0.4 (Jaccard) | Agent isn't breaking out of genuine loops | Agent is being interrupted on legitimate follow-ups |
| `maxExecLength` | 2000 chars | Long heredocs are triggering the guard | Agent needs occasional longer scripts |
| `recentQueryWindow` | 10 messages | Detection is missing long-tail repetition | Memory pressure / state bloat |

## How to measure

Each guard decision is logged to `~/.openclaw/logs/audit/rl-guard-decisions.jsonl`:

```bash
# Count decisions by guard (last 7 days)
jq -r 'select(.timestamp > (now - 7*86400 | todate)) | .decisions[]' \
  ~/.openclaw/logs/audit/rl-guard-decisions.jsonl | sort | uniq -c

# Find sessions with >5 retry_loop decisions
jq -r 'select(.decisions[] == "retry_loop") | .sessionKey' \
  ~/.openclaw/logs/audit/rl-guard-decisions.jsonl | sort | uniq -c | sort -rn | head -10
```

## When to use stricter thresholds (production)

For high-stakes deployments (CI agents, financial workflows):

```json
{
  "complexTaskThreshold": 300,
  "retryLoopThreshold": 0.35,
  "maxExecLength": 1500,
  "recentQueryWindow": 15
}
```

Tighter thresholds = more false positives, fewer missed errors. Trade-off
depends on cost of false positive vs cost of missed error.

## When to use looser thresholds (consumer chat)

For casual chat / single-turn Q&A agents:

```json
{
  "complexTaskThreshold": 800,
  "retryLoopThreshold": 0.55,
  "maxExecLength": 4000,
  "recentQueryWindow": 5
}
```

Looser thresholds = fewer reminders, but more errors get through.

## Tuning the retry_loop_guard

The default 0.4 Jaccard threshold catches **mechanical** retries where the
user pastes nearly-identical messages. It misses:

- Rephrases that paraphrase the question ("why isn't this compiling?" vs "this
  is broken")
- Multi-step debugging where each message is genuinely new context

For the second case, add more messages to `recentQueryWindow` (try 20).
For the first case, raise `retryLoopThreshold` to 0.55 or 0.6 — but be
prepared for more retries to slip through.

## Per-environment overrides

The skill reads `RL_GUARD_DISABLED=1` as an environment variable to
disable all guards. Use this for:

- Benchmarking (compare with/without guards)
- Debugging (is a guard interfering with this turn?)
- Per-session opt-out

Combine with a config file to selectively enable only one guard:

```javascript
// In your integration code
import { applyGuards } from '@openclaw/skills/rl-runtime-guard/handler.mjs';

applyGuards(ctx, sessionStore, {
  ...DEFAULT_CONFIG,
  // Disable retry_loop but keep complex_task and tool_guard
  retryLoopThreshold: 0.0,  // effectively disabled
});
```