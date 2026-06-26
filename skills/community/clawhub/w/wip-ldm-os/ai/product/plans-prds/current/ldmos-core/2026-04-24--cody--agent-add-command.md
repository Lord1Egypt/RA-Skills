# Plan: Generic `ldm agent add`

**Date:** 2026-04-24
**Author:** Cody / Kody, with Parker
**Status:** plan
**Area:** LDM OS core
**Related systems:** Memory Crystal, Bridge, Dream Weaver, Kaleidoscope, shared workspace

## Problem

LDM OS already has the architecture for agents: identity files, per-agent memory, Bridge addressing, Memory Crystal attribution, Dream Weaver consolidation, and team workspace folders.

What is missing is the generic product surface for adding a new agent.

Today, adding an agent is still too manual. A human or agent can create folders and edit config, but that creates drift:

- Bridge can know about a target before Memory Crystal knows the agent.
- Memory Crystal can receive an agent namespace that is not registered in LDM OS.
- Team folders can exist without runtime identity.
- Harness-specific setup can be hardcoded for Claude Code or OpenClaw.
- Runtime config shapes can diverge between `~/.ldm/config.json`, agent `config.json`, and package-level helpers.

The first concrete case is adding the Codex/OpenAI agent as `kody`, with display name `Kody` and aliases `Kay` and `K`. But the product should not be Kody-specific. The product is generic agent onboarding.

## Principle

LDM OS owns agent identity.

Memory Crystal, Bridge, Dream Weaver, Kaleidoscope, and harness adapters resolve agents through LDM OS. They do not invent their own agent registries.

Adding an agent should be one idempotent command:

```bash
ldm agent add <agent-id> --harness <harness>
```

Running the command twice should validate the existing setup and repair missing generated pieces without duplicating state or overwriting user-authored identity files.

The command should borrow OpenClaw's first-run shape: seed enough files for a new agent to become operational, create a one-time bootstrap prompt for the first conversation, and track onboarding state so the bootstrap prompt never comes back after completion.

## Product Decisions

- Agent aliases are globally unique across LDM OS. `ldm agent add` should fail on an alias collision unless a later explicit migration command supports a forced alias move.
- `memory.namespace` equals `id` for v1. A configurable namespace creates drift before the basic agent identity path is stable.
- The agent record includes schema and provenance fields so config mutations can be audited.
- `ldm agent add` writes an audit event with the agent id, harness, created paths, adapter status, memory namespace, bridge target, timestamp, and writer identity.
- `ldm agent remove <id> --archive` means disable/archive only. Deletion is out of scope for this command family.
- The installer should not create a fake initialized `SOUL.md`. It can create `ROLE.md`, `IDENTITY.md`, `CONTEXT.md`, `REFERENCE.md`, and a first-run `BOOTSTRAP.md`; `SOUL.md` is created by the bootstrap conversation or Dream Weaver when there is evidence.
- Codex Memory Crystal capture is the hard blocker for Kody. Directory scaffolding without reliable transcript capture is not enough.

## Proposed CLI

```bash
ldm agent add kody \
  --harness codex \
  --provider openai \
  --display-name Kody \
  --alias Kay \
  --alias K
```

Generic form:

```bash
ldm agent add <id> \
  --harness <claude-code|openclaw|codex|chatgpt|claude-desktop|custom> \
  [--provider <provider>] \
  [--display-name <name>] \
  [--alias <alias>]... \
  [--machine <machine>] \
  [--team-path <path>] \
  [--dry-run]
```

Companion commands:

```bash
ldm agent list
ldm agent show <id>
ldm agent doctor <id>
ldm agent remove <id> --archive
```

Removal should archive, not delete. Agent identity and memory are user data.

## Agent Record

The canonical runtime record should live in `~/.ldm/config.json` and point to `~/.ldm/agents/<id>/config.json`.

Recommended shape:

```json
{
  "schemaVersion": 1,
  "id": "kody",
  "displayName": "Kody",
  "aliases": ["Kay", "K"],
  "kind": "agent",
  "harness": "codex",
  "provider": "openai",
  "source": "ldm-agent-add",
  "createdBy": "kody",
  "updatedBy": "kody",
  "machine": "mac-mini",
  "workspace": {
    "teamPath": "team/kody"
  },
  "memory": {
    "namespace": "kody",
    "transcripts": "~/.ldm/agents/kody/memory/transcripts",
    "daily": "~/.ldm/agents/kody/memory/daily",
    "journals": "~/.ldm/agents/kody/memory/journals",
    "sessions": "~/.ldm/agents/kody/memory/sessions"
  },
  "bridge": {
    "target": "kody",
    "enabled": true
  },
  "dreamWeaver": {
    "enabled": true,
    "lastConsolidation": null,
    "schedule": "weekly"
  },
  "createdAt": "2026-04-24T00:00:00-07:00",
  "updatedAt": "2026-04-24T00:00:00-07:00"
}
```

The exact field names can change during implementation, but the invariants should not:

- `id` is the stable machine key.
- `displayName` is human-facing.
- `aliases` are human-facing alternate names and must not collide with another agent id or alias.
- `harness` names the runtime family.
- `memory.namespace` matches the agent id for v1.
- `bridge.target` matches the agent id for v1.
- `schemaVersion`, `source`, `createdBy`, and `updatedBy` are present on every record.
- Every config mutation emits an audit event.

## Files Created

For every agent:

```text
~/.ldm/agents/<id>/
  config.json
  IDENTITY.md
  CONTEXT.md
  REFERENCE.md
  ROLE.md
  BOOTSTRAP.md
  rules/
  commands/
  memory/
    daily/
    journals/
    sessions/
    transcripts/
    workspace/
```

`SOUL.md` is intentionally not created as an initialized placeholder by `ldm agent add`. If a harness requires a physical file, the adapter may create an explicitly uninitialized `SOUL.md` that says it is waiting for first-run or Dream Weaver evidence.

For the shared workspace:

```text
<workspace>/team/<id>/
  automated/
  documents/
  journals/
  repos/
```

`ldm agent add` may create starter files on first run, but it must not overwrite non-empty user-authored files. If a file already exists, doctor should validate it and report status.

## Agent File Semantics

The first-run file model should be generic across agents and adapters:

- `IDENTITY.md` is the factual identity card. It should contain stable facts such as agent id, display name, familiar names, aliases, harness, provider, creation date, and canonical paths. It is installer-owned at creation time and then user/agent-editable after first run.
- `ROLE.md` is the assignment. It answers what this agent is for inside the team: responsibilities, capabilities, collaboration boundaries, default operating mode, Bridge behavior, and what it should not claim to be. This is the right installer-created substitute for a premature `SOUL.md`.
- `CONTEXT.md` is the active working context. It should stay short and current: active projects, recent decisions, open loops, blockers, and next actions. Dream Weaver or Memory Crystal can update it incrementally.
- `REFERENCE.md` is durable background. It can be longer and should hold stable reference material, links, team conventions, and project lore that should be searchable but not necessarily injected every turn.
- `BOOTSTRAP.md` is the one-time first-run ritual. It should guide the first conversation, gather the missing human/agent details, initialize or revise `IDENTITY.md`, `ROLE.md`, `CONTEXT.md`, and optionally `SOUL.md`, then be removed or marked complete.
- `SOUL.md` is the personal continuity/persona artifact. It should be initialized only by first-run conversation or Dream Weaver consolidation, not guessed by the installer.

## OpenClaw First-Run Pattern

OpenClaw already implements the pattern LDM OS should reuse:

- `openclaw agents add <name> --workspace <path>` creates an agent config entry, resolves an agent workspace, and calls the shared workspace/session setup path.
- `ensureAgentWorkspace({ ensureBootstrapFiles: true })` creates the workspace and writes starter files only when missing.
- OpenClaw uses `writeFileIfMissing`, so existing user-authored files are preserved.
- The standard workspace files are `AGENTS.md`, `SOUL.md`, `TOOLS.md`, `IDENTITY.md`, `USER.md`, `HEARTBEAT.md`, optional `MEMORY.md`, optional `memory/YYYY-MM-DD.md`, and one-time `BOOTSTRAP.md`.
- `BOOTSTRAP.md` is created only for brand-new or not-yet-onboarded workspaces.
- `.openclaw/workspace-state.json` tracks `bootstrapSeededAt` and `onboardingCompletedAt`.
- If `BOOTSTRAP.md` was seeded and later disappears, OpenClaw marks onboarding complete and does not recreate it.
- For legacy workspaces, if `IDENTITY.md` or `USER.md` diverged from the template, OpenClaw treats onboarding as complete and avoids reintroducing `BOOTSTRAP.md`.
- Runtime loading treats missing bootstrap files as missing markers, not fatal errors.
- Subagent and cron sessions load only the minimal instruction files, not the whole persona/memory bundle.

LDM OS should adapt this, not copy it literally. The LDM version should use:

```text
~/.ldm/agents/<id>/
  config.json
  IDENTITY.md
  ROLE.md
  CONTEXT.md
  REFERENCE.md
  BOOTSTRAP.md
  .ldm/onboarding-state.json
```

The LDM state file should track at least:

```json
{
  "schemaVersion": 1,
  "bootstrapSeededAt": "2026-04-24T00:00:00-07:00",
  "onboardingCompletedAt": null,
  "completedBy": null
}
```

Completion can be detected by explicit CLI command, adapter event, or the OpenClaw-style heuristic that a seeded `BOOTSTRAP.md` has been removed. The critical behavior is that first-run bootstrap is recoverable, idempotent, and not recreated after completion.

## Memory Crystal Integration

Memory Crystal already defines the five-layer memory stack:

1. Raw transcripts
2. Vector index
3. Structured memory
4. Dream Weaver narrative consolidation
5. Active boot context

`ldm agent add` should integrate a new agent into that existing stack. It should not redesign Memory Crystal.

Required behavior:

- Set or document the agent's `CRYSTAL_AGENT_ID` equivalent for its harness.
- Ensure raw transcript capture lands under `~/.ldm/agents/<id>/memory/transcripts/`.
- Ensure chunks written to `~/.ldm/memory/crystal.db` use `agent_id = <id>`.
- Ensure explicit memories use the same agent id or namespace.
- Ensure daily logs and session summaries land under the agent memory tree.
- Ensure `crystal doctor` can report per-agent capture status.

For Codex, this likely requires a new Codex capture adapter, parallel to the Claude Code poller/hook and OpenClaw plugin paths.

## Bridge Integration

Bridge already supports agent addressing and session discovery through `~/.ldm/sessions/` and file inbox messages at `~/.ldm/messages/`.

`ldm agent add` should:

- Register the Bridge target for the agent.
- Install or configure the harness-specific Bridge adapter.
- Ensure sessions register as `<agent-id>:<session-name>`.
- Ensure messages can target `<agent-id>`, `<agent-id>:<session>`, and `<agent-id>:*`.
- Preserve session-level attribution so multiple sessions of the same agent do not collapse into one ambiguous speaker.
- For Codex, update Bridge to resolve human-facing Codex thread titles to stable Codex thread ids. A request like "talk to K on the `test` thread" should let Bridge look up candidate Codex threads by title, return enough metadata to disambiguate (`id`, `title`, `cwd`, `updated_at`), and then use the stable thread id for all subsequent machine-to-machine messaging. Thread titles are aliases, not durable protocol keys.

Bridge remains transport. It should use LDM identity. It should not own identity.

## Dream Weaver Integration

Dream Weaver is Layer 4. It reads raw transcripts and writes narrative identity/context artifacts.

`ldm agent add` should prepare the agent for Dream Weaver by creating the transcript and output paths. It should not force a full Dream Weaver run unless requested.

Recommended commands:

```bash
ldm agent dream-weave <id> --full
ldm agent dream-weave <id> --incremental
```

Or the existing Memory Crystal command can remain canonical, as long as `ldm agent doctor <id>` verifies the Dream Weaver state.

First-run behavior:

- For a brand-new agent with no transcripts, create `IDENTITY.md`, `ROLE.md`, `CONTEXT.md`, `REFERENCE.md`, and `BOOTSTRAP.md`.
- The first-run conversation can initialize `SOUL.md` if the user and agent actually discuss persona, boundaries, and continuity.
- Once transcripts exist, a full Dream Weaver run can generate or propose revisions to `IDENTITY.md`, `ROLE.md`, `SOUL.md`, `CONTEXT.md`, and `REFERENCE.md`.
- Incremental runs update `CONTEXT.md` and write journals without regenerating identity, role, or soul unless explicitly requested.

## Kaleidoscope Integration

Kaleidoscope should read agents from LDM OS, not from a separate product registry.

Minimum requirements:

- Agent list shows registered agents.
- Agent detail page shows harness, provider, Bridge status, Memory Crystal status, and recent Dream Weaver state.
- Aliases are displayed as human-facing names, not separate agents.
- Agent creation in Kaleidoscope should call the same underlying `ldm agent add` logic.

## Harness Adapter Contract

Each harness adapter should answer:

- How does this harness identify the current agent?
- Where are raw transcripts stored?
- How does Memory Crystal capture turns?
- How does Bridge deliver incoming messages?
- How does Bridge send outgoing messages?
- Where do agent rules and skills get installed?
- How does the harness boot from `IDENTITY.md`, `ROLE.md`, `CONTEXT.md`, `REFERENCE.md`, and, when initialized, `SOUL.md`?
- Does the harness need projected files with different names, such as OpenClaw's `AGENTS.md`, `USER.md`, or `TOOLS.md`?
- What can `doctor` verify automatically?

Initial adapters:

| Harness | Existing status | Needed for generic agent add |
|---|---|---|
| `claude-code` | Mostly supported through hooks, poller, sessions | Normalize through `ldm agent add` |
| `openclaw` | Supported through plugin and gateway | Normalize identity record and doctor |
| `codex` | Detected in LDM config, not first-class as an agent | Add capture, Bridge, boot, and doctor adapter |
| `custom` | Manual | Scaffolding plus documented adapter contract |

## Kody Acceptance Case

The first dogfood case is:

```json
{
  "id": "kody",
  "displayName": "Kody",
  "aliases": ["Kay", "K"],
  "harness": "codex",
  "provider": "openai",
  "bridgeTarget": "kody",
  "memoryNamespace": "kody",
  "teamPath": "team/kody"
}
```

After implementation:

- `ldm agent list` shows `kody`.
- `ldm agent show kody` shows Codex/OpenAI, aliases, paths, Bridge status, Memory status, and Dream Weaver status.
- `/Users/lesa/wipcomputerinc/team/kody/` exists.
- `~/.ldm/agents/kody/` exists with config, `IDENTITY.md`, `ROLE.md`, `CONTEXT.md`, `REFERENCE.md`, first-run state, and memory directories.
- `SOUL.md` is absent or explicitly uninitialized until first-run conversation or Dream Weaver has evidence.
- Codex turns can be captured as `agent_id = kody`.
- Bridge can address `kody`.
- Dream Weaver can run for `agentId = kody` after transcripts exist.
- `ldm agent add kody ...` is idempotent.

## Doctor Checks

`ldm agent doctor <id>` should verify:

- Agent exists in `~/.ldm/config.json`.
- Agent config exists and parses.
- Required directories exist.
- `IDENTITY.md`, `ROLE.md`, `CONTEXT.md`, and `REFERENCE.md` exist.
- `BOOTSTRAP.md` state is consistent: present before onboarding completion, absent or archived after completion, and never recreated after completion.
- `SOUL.md` is either initialized with provenance or explicitly reported as not initialized yet.
- Team path exists.
- Memory Crystal can see the agent namespace.
- Transcript capture is configured for the harness.
- Bridge target is valid.
- Session registration works if the harness is currently running.
- Dream Weaver state exists or is correctly reported as not yet run.
- No duplicate aliases conflict with another agent id.
- The last `ldm agent add` audit event exists and matches the agent record.

## Implementation Phases

### Phase 1: Spec and config normalization

- Define canonical agent schema.
- Normalize the current `~/.ldm/config.json` agent object shape against package helpers that still expect a string array.
- Add schema/provenance fields and audit event shape.
- Enforce global alias uniqueness.
- Add schema validation and migration tests.

### Phase 2: First-run scaffolding

- Implement `ldm agent add`, `list`, `show`, and `doctor`.
- Create directories and starter files idempotently.
- Add OpenClaw-style onboarding state with `bootstrapSeededAt` and `onboardingCompletedAt`.
- Create `ROLE.md` instead of an initialized `SOUL.md`.
- Add dry-run output.

### Phase 3: Harness adapter registry

- Add adapter contract.
- Move Claude Code and OpenClaw setup behind adapters.
- Let adapters project LDM-owned files into harness-specific bootstrap files when needed.
- Add `custom` adapter scaffolding.

### Phase 4: Codex adapter

- Add Codex as a first-class harness.
- Configure Memory Crystal capture for Codex turns.
- Configure Bridge session registration and inbox delivery for Codex.
- Add Bridge support for Codex thread-title lookup as a human alias resolver, then route by Codex thread id.
- Add boot/context reads for Kody where the Codex harness permits.

### Phase 5: Dream Weaver and Kaleidoscope wiring

- Ensure Dream Weaver commands resolve paths through the agent record.
- Surface agent status in Kaleidoscope from LDM OS.

## Non-goals

- Do not change how Memory Crystal decides what to capture.
- Do not merge Bridge and Memory Crystal.
- Do not make Kody a hardcoded special case.
- Do not overwrite existing identity files.
- Do not create fake initialized soul/persona content.
- Do not delete or wipe agent memory as part of onboarding.

## Open Questions

1. Should `ldm agent add` run `crystal init` if Memory Crystal is not installed, or only report the missing dependency?
2. What Codex-local transcript source is stable enough for automatic capture?
3. How much boot context can the Codex harness reliably read from LDM identity files?
4. Should first-run completion be an explicit command, inferred from `BOOTSTRAP.md` removal, or both?
5. Which OpenClaw files should be direct projections from LDM files versus OpenClaw-owned adapter files?

## Success Criteria

- Adding a new agent is one idempotent command.
- Bridge, Memory Crystal, Dream Weaver, Kaleidoscope, and the team workspace all resolve the same LDM identity.
- Kody is added through the generic path, not by hand edits.
- Existing `cc-mini` and `oc-lesa-mini` can be represented by the same schema without losing current behavior.
- `ldm agent doctor kody` gives a clear, actionable report.
- First-run onboarding is recoverable and idempotent, and `BOOTSTRAP.md` does not return after completion.
- `SOUL.md` is initialized only from first-run conversation or Dream Weaver evidence.
