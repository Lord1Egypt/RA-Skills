# How to Disable rl-runtime-guard

This skill is **soft** — it never blocks requests, only augments prompts.
But you may want to disable it for any of these reasons:

- Benchmarking (with vs without guards)
- Debugging (suspect a guard is interfering)
- Per-session opt-out (e.g., benchmarking specific agents)

## Three ways to disable

### 1. Environment variable (per-invocation)

```bash
RL_GUARD_DISABLED=1 openclaw ...
```

This is the cleanest way to test "what if no guard ran?".

### 2. Master switch in config

If you use a config object:

```javascript
applyGuards(ctx, sessionStore, {
  ...DEFAULT_CONFIG,
  enabled: false,
});
```

Or if loading from a config file, set `"enabled": false`.

### 3. Globally (config file)

If you have a hook-level config at
`~/.openclaw/hooks/rl-runtime-guard/config.json`:

```json
{
  "enabled": false
}
```

To re-enable, set `"enabled": true` or remove the field.

## Disabling individual guards

You cannot disable individual guards via env var. Use the config object:

```javascript
// Disable retry_loop but keep complex_task and tool_guard
applyGuards(ctx, sessionStore, {
  ...DEFAULT_CONFIG,
  retryLoopThreshold: 1.0,  // effectively unreachable
});
```

Or set the threshold so high it never fires (1.0 = require 100% match).

## Verifying it's off

The audit log records every decision. After disabling, you should see:

```bash
tail -f ~/.openclaw/logs/audit/rl-guard-decisions.jsonl
```

No output = guard is off. If entries still appear, check that the env var
or config is actually being read (sometimes hooks load config at startup).

## Permanent disable

If you've decided you don't want this skill:

```bash
# OpenClaw CLI
openclaw skills disable rl-runtime-guard

# Or uninstall
openclaw skills uninstall rl-runtime-guard
```

The audit log will remain on disk; delete manually if no longer wanted:

```bash
rm ~/.openclaw/logs/audit/rl-guard-decisions.jsonl
```