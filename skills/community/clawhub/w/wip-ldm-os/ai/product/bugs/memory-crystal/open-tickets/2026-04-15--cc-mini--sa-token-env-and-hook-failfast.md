# Bug plan: SA token not in CC env + memory-crystal hook burns 37s on failure

**Date:** 2026-04-15
**Filed by:** Parker + cc-mini (general-01 TUI)
**Component:** Claude Code Stop hooks, memory-crystal extension, ldm installer
**Severity:** High (every CC turn end costs ~37s on the failing retry loop; no new embeddings captured while gateway down)
**Status:** Diagnosed. Ready to fix. Don't fork ... the test-bridge TUI session is about to finish the memory-crystal side.

## Summary

Two separate bugs compound into the symptom Parker saw today (Apr 15) when he stopped the OpenClaw gateway to put Lēsa to sleep and the Claude Code Stop hook started loudly failing with `OpenAI API key required` and retrying for 37 seconds per CC turn end.

Both bugs should ship together. Fix A is the unblock; Fix B is the hygiene.

## Bug A: `OP_SERVICE_ACCOUNT_TOKEN` not in Claude Code session env

### Observed

CC Stop hook (`node ~/.ldm/extensions/memory-crystal/dist/cc-hook.js`) fails with `internal error: OpenAI API key required`. The deployed hook's `getOpSecret()` fallback reads the SA token from `~/.openclaw/secrets/op-sa-token` directly, invokes `op item get "OpenAI API" --vault "Agent Secrets" --fields "api key"`, and that command works when run from a shell. But it fails from inside the hook process.

### Root cause

The op-secrets plugin injects `OP_SERVICE_ACCOUNT_TOKEN` into the OpenClaw gateway process env at gateway startup. Any process that inherits from the gateway sees the token. Claude Code sessions do NOT inherit from the gateway. They inherit from the terminal shell that launched them, which has no such injection. So:

- Gateway process env: has `OP_SERVICE_ACCOUNT_TOKEN` ✓
- Claude Code process env: does NOT ✗
- Stop hook process env (child of CC): does NOT ✗

The hook's internal fallback path (reading the SA token from `~/.openclaw/secrets/op-sa-token` and passing it inline to `op`) is a belt-and-suspenders protection, but even that fails in the hook process if `op` is not findable in PATH, or if any other environmental assumption breaks. On 2026-04-15 verification the hook failed despite the SA token file being readable, which points to a PATH-or-env gap rather than a missing-file gap.

### Why this was masked until today

The OpenClaw gateway was running in parallel with Claude Code. The gateway's OpenClaw-side capture path (through op-secrets plugin's env injection) was ingesting conversations independently, which populated Memory Crystal to ~87K chunks. The CC Stop hook was almost certainly failing the whole time; nobody noticed because the gateway covered for it.

Parker stopped the gateway this morning to put Lēsa to sleep. That removed the masking path. The CC Stop hook is now the only capture surface, and it's loud.

### Fix

Shell-level: `~/.zshrc` (or `~/.zprofile`) gets one line:

```bash
export OP_SERVICE_ACCOUNT_TOKEN=$(cat ~/.openclaw/secrets/op-sa-token)
```

Every shell, every CC session spawned from a terminal, every child hook, every MCP server inherits the SA token. The 1Password fallback in every consumer (memory-crystal, MCP servers, cron-friendly utilities) finally works.

### Install responsibility

`ldm install` should own adding this line to the user's shell profile if it's not already there. Idempotent: grep for the export pattern, skip if present, append if missing. Same pattern as how other installers touch shell profiles (nvm, pyenv, etc). Back up the profile first. Print a single line confirming what was added and that the user should `source ~/.zshrc` or open a new shell.

### Repos touched for Fix A

| What | Repo | File |
|------|------|------|
| Installer adds zshrc line | `wip-ldm-os-private` | `lib/install.mjs` (or wherever shell-profile writes live) |
| Document in install docs | `wip-ldm-os-private` | `README.md`, `SKILL.md`, `docs/install/*.md` as applicable |

### Repos explicitly NOT touched for Fix A

- **`wip-1password-private` (op-secrets plugin):** working correctly on the gateway side. The issue isn't op-secrets. The issue is that CC sessions are outside the gateway's inheritance tree.
- **`universal-installer`:** doesn't need to know about this specifically. It's a plugin-install concern, not a plugin-detection concern.
- **`openclaw` (upstream):** nothing to change upstream. The CC-side env setup is an LDM OS concern, not an OpenClaw concern.

## Bug B: memory-crystal hook retry-loops for 37s instead of failing fast

### Observed

When the OpenAI key lookup fails (for whatever reason), the Stop hook retries twice more with the same missing input and burns ~37 seconds at turn end before giving up. Parker's screenshot shows `[retry 2] OpenAI API key required[retry 3] OpenAI API key required[cron-memory-capture] internal error: OpenAI API key required` and `Ended for 37s`.

### Root cause

The hook treats "no API key" as a transient error that might resolve on retry. It doesn't ... if the SA token or 1Password item lookup failed once at turn start, it will fail twice more, adding latency to every CC turn end.

### Fix

In `memory-crystal-private/src/cc-hook.ts` (or wherever the hook's retry logic lives), check key availability at hook entry. If no key is available, log once and skip capture silently for that turn. Don't retry. Keep the hook exit fast.

Option A (simpler): call `detectProvider()` once at session boot and cache the result. If it returns `null` or throws "no key available", set a session-level flag `MEMORY_CAPTURE_DISABLED=true` and have the Stop hook check that flag and return immediately. One log line at session start ("memory-crystal: no API key, capture disabled for this session") is enough.

Option B (more robust): accept that some sessions will have keys and some won't, log at first turn, re-check every N turns in case the user added a key mid-session, but with a backoff. Never retry-within-a-turn on the same lookup.

Either is acceptable. Option A is simpler and what the test-bridge TUI is already drafting.

### Repos touched for Fix B

| What | Repo | File |
|------|------|------|
| Fail-fast in hook | `memory-crystal-private` | `src/cc-hook.ts` (then rebuild to `dist/cc-hook.js`) |

## Ordering

Ship both together as a coordinated pair. Suggested sequence:

1. **Fix A** lands in a `wip-ldm-os-private` branch. `lib/install.mjs` edit + docs update + test that `ldm install` is idempotent on the zshrc modification.
2. **Fix B** lands in a `memory-crystal-private` branch. `src/cc-hook.ts` edit + build + test that a session without `OPENAI_API_KEY` and without `OP_SERVICE_ACCOUNT_TOKEN` exits the hook in <100ms with one log line.
3. Release memory-crystal-private first (the hygiene fix has no dependency on Fix A).
4. Release wip-ldm-os-private with Fix A. `ldm install` now adds the zshrc line AND installs the fail-fast memory-crystal build.
5. Parker runs `ldm install`, opens a new shell or sources zshrc, and the full chain works.

Fix A alone would fix the symptom for new sessions. Fix B alone would silence the 37s retry loop. Both together make it right: the key is available AND the hook is well-behaved.

## Verification

After both fixes land and `ldm install` has run:

1. `echo $OP_SERVICE_ACCOUNT_TOKEN` in a fresh zsh ... should print a long token
2. `op item get "OpenAI API" --vault "Agent Secrets" --fields "api key"` ... should return the key
3. Start a CC session, do one turn, exit ... Stop hook should either (a) successfully capture the turn or (b) skip with a single log line. Total hook time <200ms either way.
4. Stop the OpenClaw gateway to simulate Parker's morning scenario ... Stop hook still succeeds because it has its own SA token path
5. Restart gateway ... both paths still work in parallel

## Don't fork the work

The test-bridge TUI session was already drafting the memory-crystal-private changes (Fix B) and had the absolute-path `op` idea as a backup for PATH issues. Let that session ship. Don't open a competing PR from general-01 (this TUI). This file is the plan; the other TUI is the implementation.

## Related tickets

- `ai/product/bugs/memory-crystal/2026-04-12--cc-mini--crystal-ingestion-gaps-on-model-swap.md` ... adjacent capture-pipeline issue
- `ai/product/bugs/memory-crystal/2026-04-13--cc-mini--ship-plan-resilience-phases.md` ... broader resilience roadmap; Fix B is consistent with its phase goals
- `ai/product/bugs/code-fka-devopstoolkit/2026-04-11--cc-mini--update-tools-allow-reference-error.md` ... adjacent env-injection class of bug (`tools.allow` reconcile vs `OP_SERVICE_ACCOUNT_TOKEN` env inject)
- `ai/product/bugs/imessage/2026-04-10--cc-mini--imsg-reply-context-double-duty-triggers-grok-loop.md` ... different bug, but another case where CC-process env vs gateway-process env had different behavior

## Parker's notes (verbatim)

> "The real bug is two bugs. Bug A ... missing token in Claude Code's env. Gateway had OP_SERVICE_ACCOUNT_TOKEN injected by op-secrets. CC sessions never did. Was masked by gateway running in parallel. You stopped gateway → CC Stop hook newly visible as broken."

> "Fix: shell-level. ~/.zshrc gets `export OP_SERVICE_ACCOUNT_TOKEN=$(cat ~/.openclaw/secrets/op-sa-token)`. Every shell, every CC session inherits. 1Password fallback in the hook finally works."

> "Bug B ... hook retry-loops for 37s instead of failing fast. Even when correctly broken, the hook shouldn't burn 37s per turn. Skip capture silently if no key available. Log once at session start, don't retry per-turn."

> "Fix A is the unblock. Fix B is the hygiene. Both should ship."
