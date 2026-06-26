# Plan: Route Lēsa Through Claude Code CLI Backend

**Date:** 2026-04-11
**Author:** Parker + CC Mini
**Branch:** cc-mini/lesa-claude-cli-plan
**Related:** Today's outage (Grok → Anthropic fallback broke tool_use IDs)

## Context

Two things converged today. They point in the same direction.

### 1. The Jeffrey/Steipete revelation

On X, Jeffrey (@JJeffrey100) asked: "why not set up a local adapter that uses CLI in the background? they wouldn't be able to tell at all. you'll have to change up the payload a bit, but paperclip has been chugging along fine doing this."

Peter Steinberger (@steipete) replied: "We do that."

Jeffrey: "well shit, why am i using tokens in openclaw 🤣"

lush_amorelli added the compliance clarification: using the actual Claude Code CLI with a connector is explicitly allowed. The "banned" use case Anthropic worried about was third-party apps bypassing Anthropic's caching and optimization layer by using the Claude Code token directly. When you spawn the actual CLI, Anthropic gets all its optimizations. Blocking that would mean banning MCPs, which Anthropic invented.

Jeffrey then built a local adapter in a day: "basically a command injection and it monitors each response from CLI, all within anthropic's ToS."

### 2. Today's Lēsa outage

Lēsa went down because her session had a broken tool_use at message 101 from the Anthropic API's perspective:

```
messages.101: `tool_use` ids were found without `tool_result` blocks
immediately after: call8e270cde5c414f01a8cf5ef4a0c0fd0431fc.
```

The actual stored tool_use ID was `call-8e270cde-5c41-4f01-a8cf-5ef4a0c0fd04-31|fc_ee314c75-1c4f-9852-86a1-5e884e5de4a8_0`. That composite format is Grok-native (xai's openai-responses API uses pipes and underscores to glue the call ID to the reasoning signature ID). The tool_use was paired with a proper toolResult in OpenClaw's own session store. The pairing broke only when OpenClaw's message serializer flattened the ID to alphanumerics for the Anthropic API.

The failure chain:

1. Assistant message with grok composite-ID tool_use
2. OpenClaw's model fallback hit anthropic/claude-sonnet-4-6
3. ID normalization stripped dashes/pipes: `call-8e270cde-...-31|fc_...` → `call8e270cde5c414f01a8cf5ef4a0c0fd0431fc`
4. The original tool_result's toolCallId didn't get the same normalization, so they no longer matched
5. Anthropic API rejected with format error
6. OpenClaw interpreted format error as auth profile problem and cooled down `anthropic:remote-03`
7. Grok fallback failed with 429 (team credits exhausted last night)
8. Haiku fallback failed because the anthropic cooldown was shared across all anthropic profiles
9. All 3 models failed, Lēsa died

**If Lēsa had been running on the claude-cli backend from the start, none of this would have happened.** Claude CLI manages its own session store via `--session-id`, never sends OpenClaw's internal message history to Anthropic as structured messages, and doesn't cross-provider fallback at the payload layer.

**Conclusion: routing Lēsa through `claude -p` is not just a token-economics play. It is a structural hedge against cross-provider fallback bugs.**

## What OpenClaw already has built

Looking at `repos/third-party-repos/ai-harness/openclaw/src/agents/`:

| File | What it does |
|------|-------------|
| `cli-runner.ts` | `runCliAgent(params)`: spawns `claude -p` per turn, injects system prompt via `--append-system-prompt`, uses `--session-id` for per-session persistence |
| `cli-backends.ts` | `DEFAULT_CLAUDE_BACKEND` config: `command: claude`, `args: [-p, --output-format, json, --dangerously-skip-permissions]`, `clearEnv: [ANTHROPIC_API_KEY, ANTHROPIC_API_KEY_OLD]` |
| `cli-session.ts` | Per-session CLI state tracking |
| `cli-credentials.ts` | OAuth handling for claude-cli |
| `claude-cli-runner.e2e.test.ts` | E2E test coverage |
| `cli-watchdog-defaults.ts` | Subprocess reliability config (watchdog timeouts) |

Key design points in the built-in Claude backend (`cli-backends.ts:34-63`):

1. **Clears `ANTHROPIC_API_KEY` before invoking** (line 55). That forces OAuth, so Claude CLI uses Parker's Max subscription instead of any ambient API key. Exactly what the economic argument predicts.

2. **`--append-system-prompt`** (line 53). Lēsa's system prompt is appended to Claude Code's own. Her identity, personality, tool rules, and workspace references come through.

3. **`--session-id {sessionId}`** (line 49). Per-session persistence so Claude CLI's own session store caches context across turns. OpenClaw does NOT re-serialize its full message history into a fresh prompt on every turn.

4. **Injected "Tools are disabled in this session. Do not call tools."** (`cli-runner.ts:84`). OpenClaw runs the nested Claude Code in text-only mode. OpenClaw's own tool ecosystem (memory-crystal, lesa-bridge, tavily, wip-x-xai-grok, etc.) continues to work at the OpenClaw layer. The nested CLI is pure inference.

5. **`serialize: true`** (line 62). Claude CLI requests for a given session are serialized so there are no concurrent writes to the same session store.

6. **Watchdog defaults** (lines 56-61): fresh and resume runs each have their own watchdog timeout, so a hung CLI subprocess gets killed rather than hanging the gateway.

**Proof of life:** `gateway.log` shows successful `[agent] cli exec: provider=claude-cli model=sonnet` entries from Apr 8. The backend has run in production on this machine before. Something changed since then that put Lēsa back on grok primary.

## What is already configured in Parker's openclaw.json

```json
"auth": {
  "profiles": {
    "anthropic:claude-cli": {
      "provider": "claude-cli",
      "mode": "oauth"
    }
  }
},
"agents": {
  "defaults": {
    "models": {
      "claude-cli/claude-opus-4-6": {
        "alias": "opus46",
        "params": { "cacheRetention": "long" }
      },
      "claude-cli/claude-sonnet-4-6": {
        "alias": "sonnet",
        "params": { "cacheRetention": "long" }
      }
    }
  }
}
```

OAuth profile plus opus 4-6 and sonnet 4-6 entries already exist. Nothing new to configure there.

**Claude CLI auth** (verified today with `claude auth status`):

- loggedIn: true
- authMethod: claude.ai
- subscriptionType: **max**
- email: remote.bunkers_5i@icloud.com (the iCloud burner tied to Parker's Max)

The infrastructure is ready. What is missing is the flip plus one upstream bug fix.

## The blocker: CLAUDE_MODEL_ALIASES is stale

From `cli-backends.ts:14-32`:

```typescript
const CLAUDE_MODEL_ALIASES: Record<string, string> = {
  opus: "opus",
  "opus-4.6": "opus",
  "opus-4.5": "opus",
  "opus-4": "opus",
  "claude-opus-4-6": "opus",     // present
  "claude-opus-4-5": "opus",
  "claude-opus-4": "opus",
  sonnet: "sonnet",
  "sonnet-4.5": "sonnet",
  "sonnet-4.1": "sonnet",
  "sonnet-4.0": "sonnet",
  "claude-sonnet-4-5": "sonnet", // last sonnet entry
  "claude-sonnet-4-1": "sonnet",
  "claude-sonnet-4-0": "sonnet",
  haiku: "haiku",
  "haiku-3.5": "haiku",
  "claude-haiku-3-5": "haiku",   // last haiku entry
};
```

**Missing:**

- `claude-sonnet-4-6: "sonnet"` (the latest Sonnet, shipped Feb 2026)
- `claude-haiku-4-5: "haiku"` (the latest Haiku, shipped Oct 2025)

When I tried `openclaw config set agents.defaults.model.primary claude-cli/claude-sonnet-4-6` today, the gateway warmup threw `Unknown model: claude-cli/claude-sonnet-4-6` via `pi-embedded-runner/model.ts`. The CLI backend's model alias lookup failed upstream before `runCliAgent` could even be dispatched. The fix is a 4-line patch to the alias map.

**Workaround until patched:** use `claude-cli/claude-opus-4-6` (`opus46` alias). Opus 4-6 IS in the alias map and works today. On metered billing it would be ~5x more expensive per token than sonnet. On Parker's Max subscription there is no per-token cost, just rate-limit pressure.

## Plan

### Phase A: Patch OpenClaw CLAUDE_MODEL_ALIASES (first move)

**Goal:** Add `claude-sonnet-4-6` and `claude-haiku-4-5` to the alias map so Lēsa can select them as claude-cli models.

**Where:** `repos/third-party-repos/ai-harness/openclaw/src/agents/cli-backends.ts`, lines 14-32.

**Diff:**

```diff
   sonnet: "sonnet",
+  "sonnet-4.6": "sonnet",
   "sonnet-4.5": "sonnet",
   "sonnet-4.1": "sonnet",
   "sonnet-4.0": "sonnet",
+  "claude-sonnet-4-6": "sonnet",
   "claude-sonnet-4-5": "sonnet",
   "claude-sonnet-4-1": "sonnet",
   "claude-sonnet-4-0": "sonnet",
   haiku: "haiku",
+  "haiku-4.5": "haiku",
   "haiku-3.5": "haiku",
+  "claude-haiku-4-5": "haiku",
   "claude-haiku-3-5": "haiku",
```

**How to ship:**

1. Create a feature branch in the openclaw repo clone at `repos/third-party-repos/ai-harness/openclaw/`
2. Apply the patch, rebuild, run the existing `claude-cli-runner.e2e.test.ts` to make sure nothing regressed
3. Open an upstream PR. This is a bug-fix not a feature. Should merge fast.
4. Until upstream merges: local hotfix by running `npm run build` in the openclaw worktree, then `cp dist/agents/cli-backends.js /opt/homebrew/lib/node_modules/openclaw/dist/agents/` (this is an extensions-path write, guard-allowed)
5. `openclaw gateway restart`

### Phase B: Flip Lēsa's primary model to claude-cli/claude-sonnet-4-6

Once Phase A is applied (locally or upstream):

```bash
openclaw config set agents.defaults.model.primary claude-cli/claude-sonnet-4-6
openclaw config set agents.defaults.model.fallbacks \
  '["claude-cli/claude-opus-4-6","anthropic/claude-sonnet-4-6","anthropic/claude-haiku-4-5"]'
openclaw gateway restart
```

**Fallback chain rationale:**

1. Primary: sonnet 4.6 via CLI (subscription, effectively free per token)
2. Fallback 1: opus 4.6 via CLI (same subscription, different model bucket for rate limits)
3. Fallback 2: sonnet 4.6 via direct API (if Max session quota is hard-capped)
4. Fallback 3: haiku 4.5 via direct API (emergency cheap path)

**What this avoids:** xAI grok (tool_use ID incompatibility plus team credits exhausted).

### Phase C: Route subagents through CLI, keep heartbeat on direct API

```bash
openclaw config set agents.defaults.subagents.model claude-cli/claude-sonnet-4-6
# leave heartbeat.model as anthropic/claude-haiku-4-5
```

Subagents are spawned with fresh session state each invocation so they benefit fully from Claude CLI's per-invocation caching. Heartbeat fires every ~30 minutes with <500 tokens of prompt and no structured state; the subprocess spawn overhead dominates the actual inference cost there.

### Phase D: Verify with a canary turn

After the flip:

1. Send Lēsa a simple test via `lesa_send_message` MCP (something like "ack test, reply with a single word")
2. Tail `~/.openclaw/logs/gateway.log` for `[agent] cli exec: provider=claude-cli model=sonnet`
3. Confirm the reply landed and no API-direct fallback fired
4. Check `claude auth status` usage counters to confirm the call consumed Max session quota
5. Verify `openclaw usage` and `~/.openclaw/agents/main/agent/auth-state.json` show the anthropic direct-API profile with zero new usage

## What to measure after the flip

| Metric | Before (direct API) | After (claude-cli) | How to check |
|--------|--------------------|--------------------|--------------|
| Per-turn cost | $0.003 - $0.015 | $0 (subscription) | `openclaw usage` or auth-state.json |
| Anthropic API usage in Parker's console | Non-zero | Zero for Lēsa's runs | console.anthropic.com/usage |
| Claude Max session quota | N/A | Consumed | `claude auth status` across the 5h window |
| Time to first token | ~1.5s (direct HTTP) | ~2.5s (subprocess spawn) | `gateway.log` `agent end` duration |
| Cross-provider fallback bugs | Possible | Eliminated | Absence of format errors in err log |
| Boot loops due to message.N format errors | Possible | Eliminated | Absence of the messages.X error signature |

**Cost floor:** Parker already pays for Claude Max. Adding Lēsa's traffic on top does not raise the bill. It raises the risk of Max rate limits kicking in across his 7 concurrent CC sessions plus Lēsa. Worth watching.

## Known tradeoffs

### Rate limits are shared across Max subscription

Claude Max has a rolling 5-hour session quota. Parker already runs up to 7 concurrent `cc-mini` Claude Code sessions on this machine. Adding Lēsa's gateway traffic means she competes with those sessions for the same quota. If Lēsa gets rate-limited at peak usage, the fallback chain kicks in (claude-cli → opus, then direct API). The direct API fallback does cost money.

**Mitigation:** move some cc-mini background session cadence to off-peak if Max limits start to pinch. Bump to Team plan if sustained.

### Subprocess spawn overhead

Each `claude -p` invocation spawns a Node subprocess, loads Claude Code's context, resolves MCP servers, etc. Roughly 1 second on top of the actual model inference. For Lēsa's iMessage conversation cadence (seconds between replies), imperceptible. For high-frequency operations like heartbeat, wasteful. That is why heartbeat stays on direct API.

### `--dangerously-skip-permissions`

The backend default uses this flag (`cli-backends.ts:36`). Within OpenClaw's nested CLI invocation, tools are already disabled (`cli-runner.ts:84` injects "Tools are disabled in this session"). So `--dangerously-skip-permissions` is moot ... there are no tools to run. The flag name is still alarming. Consider proposing `--allowedTools=""` to upstream as a clearer-intent alternative.

### No OpenAI/Grok inference via CLI backend

If Lēsa needs to reach Grok (for web search or multimodal via grok-imagine), that has to happen via OpenClaw's own MCP/tool layer, not via the CLI inference path. The CLI only does Claude inference. Verify memory-crystal, tavily, and wip-x-xai-grok MCPs are all wired in and functional after the flip.

### Session store divergence

OpenClaw maintains its own jsonl session store under `~/.openclaw/agents/main/sessions/*.jsonl`. Claude CLI maintains its own session store under `~/.claude/sessions/`. With `--session-id` the two are associated but not synchronized. If Lēsa's OpenClaw-side session gets corrupted (as happened today), the Claude CLI session may still be intact ... or vice versa. This is a feature, not a bug: it gives us two independent recovery paths. But we should document which store is authoritative for which kinds of state.

## Open questions

1. **Does `--session-id` persistence work across OpenClaw gateway restarts?** The session UUIDs OpenClaw generates are stable, so yes in theory. Verify: restart gateway mid-conversation, confirm Lēsa still has context.

2. **What happens when Claude CLI itself is updated?** Claude CLI auto-updates. Version skew between Claude CLI and OpenClaw's `cli-backends.ts` could cause incompatibilities (new flags, removed flags, changed output format). The watchdog catches total failures; silent format changes are scarier. **Recommendation:** pin a Claude CLI version in the launchagent env or freeze auto-update, upgrade deliberately.

3. **How does compaction interact between the two layers?** OpenClaw has its own compaction-indicator plugin that fires at 75% / 90% of its context budget. Claude CLI has its own `/compact` and auto-compaction logic. They are not coordinated. Which wins? Test: fill a session to 75% and observe.

4. **What about Parker's Claude CLI `.claude/` state?** The gateway runs as launchd user `lesa`. `claude auth status` showed logged-in for `remote.bunkers_5i@icloud.com`. Verify the gateway's node subprocess inherits `HOME=/Users/lesa` so it reads the same `.claude/` config the CLI auth uses.

5. **Do CLI sessions persist across Lēsa boot loops?** If Lēsa crashes mid-turn, does the Claude CLI session for that turn survive? Or orphan? Investigate via `ls ~/.claude/sessions/ -lt` before and after an induced crash.

6. **What to do about the cross-provider tool_use normalization bug?** The root cause of today's outage is OpenClaw's ID normalization bug. Even after migrating Lēsa to claude-cli, if fallback to direct Anthropic ever fires, the same bug could bite. Options:
   - File the bug upstream (correct long-term)
   - Disable fallback to anthropic when primary is claude-cli/* (short-term insurance)
   - Add a session-level ID sanitizer that normalizes incoming Grok/openai tool IDs to Anthropic-compatible format at write time (prevents the issue at the source)

## Rollback

If the flip misbehaves:

```bash
openclaw config set agents.defaults.model.primary anthropic/claude-sonnet-4-6
openclaw config set agents.defaults.model.fallbacks '["anthropic/claude-haiku-4-5"]'
openclaw gateway restart
```

Session data is untouched by model selection, so rollback is instant and lossless. If something in the current trimmed session turns out to be load-bearing and missing, `/tmp/lesa-session-backup-2026-04-11-1746.jsonl` still has the full pre-truncation jsonl from today's emergency repair.

## Related work

### xAI team credits

Lēsa still has `xai/grok-4.20-0309-reasoning` and friends in the model catalog. Current state: team credits exhausted (429s all day). Options:

- Prune grok models from the primary/fallback chain entirely (done today)
- Keep grok as a dedicated search provider (via `wip-x-xai-grok` MCP + xAI web search), NOT an inference backend
- Refill credits and re-enable as a fallback once stable

### Codex CLI backend

OpenClaw's `cli-backends.ts` also has `DEFAULT_CODEX_BACKEND` (OpenAI ChatGPT Plus path via `codex`). Parker has an `openai-codex:default` OAuth profile active. Same argument applies: if we need a non-Claude fallback, codex-cli beats openai direct API for cost on a Plus plan. Could be Phase E. Check `codex` CLI version compatibility first.

### Bugs to file upstream against openclaw

1. **CLAUDE_MODEL_ALIASES missing latest models** (Phase A patch above). Include claude-sonnet-4-6 and claude-haiku-4-5.
2. **Cross-provider tool_use ID normalization breaks Anthropic validation.** Grok composite IDs with pipes/underscores get flattened to alphanumerics inconsistently between tool_use and tool_result. Reproducer: force fallback from grok/openai-responses provider to anthropic provider mid-session with tool calls outstanding.
3. **Format errors from the provider API should not put the auth profile into cooldown.** They are payload errors, not profile problems. Today's outage compounded because a single format error (rightfully affecting that one request) cooled down `anthropic:remote-03` for ~30 seconds, which then cascaded with the grok 429 and haiku's shared-cooldown into a hard boot failure. The cooldown reason should be error-type-aware.

## What gets committed with this plan

This plan file itself, committed to the `cc-mini/lesa-claude-cli-plan` branch in wip-ldm-os-private. The actual code changes in Phase A go in a separate PR against the openclaw third-party repo at `repos/third-party-repos/ai-harness/openclaw/`.

## Signal for after-the-fact analysis

If this plan works, the forensic signature will be:

- `~/.openclaw/logs/gateway.log` shows `[agent] cli exec: provider=claude-cli model=sonnet` as the dominant pattern
- `~/.openclaw/agents/main/agent/auth-state.json` `usageStats["anthropic:remote-03"].lastUsed` stops advancing
- Anthropic console shows ~0 API usage during Lēsa's active hours
- `claude auth status` (as user lesa) shows Max session quota consumption that was previously spread across 7 cc-mini sessions now spread across 8 (including Lēsa)

If it does not work, the forensic signature will be:

- Repeated `Unknown model: claude-cli/claude-sonnet-4-6` at gateway warmup (Phase A was not applied correctly)
- Or `Error: Unknown CLI backend: claude-cli` from `cli-runner.ts:74` (auth profile resolution failed)
- Or subprocess crashes with `claude: command not found` (PATH issue in launchagent env)
- Or Claude CLI auth failures (OAuth token expired, needs `claude auth login` as user lesa)

Each has a clear fix path.
