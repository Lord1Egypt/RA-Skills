# skill-sediment plugin internals (troubleshooting reference)

## Contents

- [What it is](#what-it-is)
- [The 6 Gates of trigger](#the-6-gates-of-trigger)
- [Lifecycle](#lifecycle)
- [Promote second-hit guard](#promote-second-hit-guard)
- [Status tags](#status-tags)
- [Tunable parameters](#tunable-parameters)
- [OpenClaw APIs the plugin depends on](#openclaw-apis-the-plugin-depends-on)
- [Common troubleshooting](#common-troubleshooting)

## What it is

An OpenClaw plugin extension (entry: `index.ts`, TypeScript runs directly without
compile step). Listens to conversations and automatically writes successful
non-trivial workflows out as `SKILL.md`.

- Not an MCP server, not a standalone process
- Does NOT depend on vector retrieval / embeddings — hit detection uses a
  review sub-Agent that reads the conversation with an LLM
- The only third-party dependency is `@sinclair/typebox`, which OpenClaw core
  already bundles

## The 6 Gates of trigger

The background review sub-Agent only launches when **all 6** are satisfied:

1. The current session is not the review sub-Agent itself (anti-recursion)
2. The current model is whitelisted (`OPENCLAW_SKILL_SEDIMENT_MODEL_ALLOWLIST`;
   unrestricted when unset)
3. Session has been running > 5s and last review was > 30s ago
4. The agent id is in the `validAgentId` config
5. New tool-call turns since last review ≥ `nudgeInterval` (default 15)
6. Total user turns ≥ 2 AND new user turns ≥ 1

## Lifecycle

```
create (review sub-Agent calls skill_manage to create)
  → [sediment] stored under <workspace>/sediment_skills/<name>/
  → patch / edit iterations (revisionCount++)
  → second-hit → promote → moved to <workspace>/skills/ → [sediment-active]

Eviction (LRU / TTL):
  - Not touched for sedimentTtlDays days → evict (default 10)
  - Max sedimentMaxCount per agent (default 20; LRU-evict beyond limit)
  - Newly created items are protected for sedimentGracePeriodDays days (default 3)
  - Items already promoted to skills/ are never evicted
```

## Promote second-hit guard

For a sediment to be promoted, one of two paths must trigger:

- **Path A (cross-session)**: a review from a **different parent session** hits again
- **Path B (mature)**: the sediment is older than `promoteMaturationDays` (default 1),
  in which case the same parent session may also promote it

Design intent: prevent immediate auto-promote right after creation. Long-running
main agents with stable `sessionKey` mostly rely on Path B.

## Status tags

| Tag | Location | Writable |
|-----|----------|----------|
| `[sediment]` | sediment_skills/ | all actions |
| `[sediment-active]` | skills/ (after promote) | edit/patch |
| `[native]` | skills/ (user-built) | read-only |
| `[OFFICIAL]` | bundled skill | read-only |

## Tunable parameters

Under `openclaw.json` → `plugins.entries["skill-sediment"].config`:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `validAgentId` | (required) | Agents with sediment enabled, comma-separated or `*` |
| `enableAutoReview` | true | Whether auto-review is on |
| `nudgeInterval` | 15 | Trigger interval (new tool-call count) |
| `sedimentTtlDays` | 10 | TTL eviction days (0 disables) |
| `sedimentMaxCount` | 20 | Max retention per agent (0 disables) |
| `sedimentGracePeriodDays` | 3 | Grace window for newly-created sediments |
| `promoteMaturationDays` | 1 | Maturation days for Path B (0 disables time-path promote) |

## OpenClaw APIs the plugin depends on

These are the compatibility-sensitive points when porting to a newer OpenClaw version:

- **Hook events (6)**: `llm_input` / `llm_output` / `session_end` / `before_reset` /
  `agent_end` / `subagent_ended`
- **Sub-Agent**: `api.runtime.subagent.run` / `getSessionMessages`
- **Config**: `api.pluginConfig` / `api.runtime.config.loadConfig`
- **Tool registration**: `api.registerTool` (registers `skill_manage`, exposed only to the review sub-Agent)
- **SDK functions**: `parseSessionKey` / `postUbaEvent` / `reportSession` / `sendUserQueryWhitelistHiMessage`
- **Types**: `OpenClawConfig` / `OpenClawPluginApi`

If the target version renamed or changed the signature of any of these, sediment
will silently fail. `doctor` cannot see runtime mounts — check gateway logs for
`[skill-sediment]` to confirm the 6 hooks mount successfully.

## Common troubleshooting

| Symptom | What to check |
|---------|---------------|
| Installed but no sediment_skills/ shows up | (1) Did you restart the gateway? (2) Does the log show `[skill-sediment]`? (3) Does validAgentId include the current agent? (4) Has the conversation hit ≥15 tool calls? |
| Config got written, but it disappears after restart | Remote-config overwrite (Lobi/Apollo): about ~16s after gateway boot the remote source pushes back local. Run `config` and add the 3 fragments to the **remote control plane** (Lobi console / Apollo); writing local alone isn't enough. `doctor` warns when managed env is detected. |
| Plugin file is gone after restart | PVC volume swap — run `recover` to redeploy |
| Sediment never gets promoted | Second-hit guard: same session needs the sediment to mature (≥1 day), or trigger a hit from a different session |
| Sediments vanish unexpectedly | TTL/LRU eviction: untouched for 10 days, or count exceeded the per-agent cap of 20 |
