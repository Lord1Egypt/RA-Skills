---
name: position
description: Bootstrap the session into a team position. Loads the position profile from `ai-workspace/team/<name>.md`, loads sibling state directory if present (PLAYBOOK + DECISIONS), runs the position's session-start sequence. Use when a teammate session needs to assume a persistent role identity.
---

# /position — load a team position into the session

`/position <name>` is the generic teammate-bootstrap skill. It loads a position profile from `ai-workspace/team/<name>.md` and runs the bootstrap sequence the profile defines. Replaces the bespoke `/tpm` (which, where present, is a thin wrapper around `/position tpm` that adds a unidirectional refusal contract — see "Wrapper skills" below).

## Position vs role

- **Position** = persistent identity, loaded once per teammate session. Lives in `ai-workspace/team/<name>.md`. Examples: `tpm`, `software-engineer`, `technical-editor`, `architect`.
- **Role** = one-shot activity dispatched at a `/task` step. Lives in `ai-workspace/agents/<name>.md`. Examples: `implementer`, `code-reviewer`, `test-writer`, `explorer`.

`/position` operates on positions only. For one-shot role dispatch, use your tool's subagent-dispatch mechanism — Claude Code: `Agent({subagent_type: <role-name>})`; Codex/Cursor: see your project's `AGENTS.md` §Agent Roles for the equivalent dispatch pattern.

## 1. Resolve position

```bash
NAME="<arg>"
PROFILE="ai-workspace/team/${NAME}.md"
STATE_DIR="ai-workspace/team/${NAME}"
```

Pre-flight: if `$PROFILE` does not exist, refuse with:

> Position `<name>` not found at `ai-workspace/team/<name>.md`. Available positions: list them by running `ls ai-workspace/team/*.md`. (For one-shot subagent role dispatch instead, use your tool's role-dispatch mechanism — Claude Code: `Agent({subagent_type: <role>})`.)

Do not auto-bootstrap. Absence is a signal to verify the environment.

## 2. Load profile + state

Read in order. **Load all files into context first, then reason** — do not summarize as you read.

1. `$PROFILE` (required) — the position's role identity, working agreement, decision rules, triggers, anti-patterns, lifecycle hooks.
2. `${STATE_DIR}/PLAYBOOK.md` (if exists) — the position's operating manual.
3. `${STATE_DIR}/DECISIONS.md` (if exists) — the position's append-only judgment log.

Most positions have NO sibling state directory — only stateful positions (currently just `tpm`) do. The skill silently skips state-load when the directory is absent.

## 3. Regenerate live state (if profile prescribes it)

The position's profile body specifies whether/how to regenerate live state on session start. Common patterns:

- TPM: `gh project item-list` + `git worktree list` + `gh pr list`
- Software-engineer: tail `#general` chat + read `.branch-context.md` if resuming
- Technical-editor: tail `#general` chat for review requests

Follow the profile's `## Session lifecycle / Session start` section verbatim. The skill doesn't prescribe regeneration steps — the profile owns them.

## 4. Acknowledge + take the position

After load + bootstrap:

1. **Acknowledge**: `Position '<name>' loaded. Following profile session-start instructions.`
2. **Hold the position** for the rest of the session — the agent operates as `@<name>` according to profile rules until session end.
3. **Chat handle** (if the position's chat substrate is online): post the registration message the profile prescribes.

## 5. `--resume` flag (optional)

`/position <name> --resume` signals resumption of an interrupted session:

- Read `.branch-context.md` if present (per the position's profile resume convention)
- Skip the registration chat post (the position is presumed already known to the team)
- Pick up where the prior session left off

If the profile has no resume semantics, `--resume` is a no-op silently.

## 6. Switching positions

A session can switch positions by re-invoking `/position <other>`. Latest wins. Profile rules from the prior position drop. **Exception:** the `tpm` position has a unidirectional refusal contract (enforced by the `/tpm` wrapper skill, where installed) — switching out of TPM mid-session is refused per its own rules.

## Anti-patterns

| Anti-pattern | Why wrong |
|---|---|
| Reading from `ai-workspace/agents/` for `/position` | That's the role directory (subagents). Positions live in `team/`. |
| Auto-bootstrapping a missing position | Refusal is the contract — positions must be defined first |
| Soft-loading just the profile without the state dir | Stateful positions need both; skipping state breaks continuity |
| Summarizing the profile as you load it | Load first, reason second — same as `/tpm` v0 contract |
| Treating `/position <subagent-role>` as valid (e.g. `/position implementer`) | Roles are not positions; refuse and direct to your tool's role-dispatch mechanism (Claude Code: `Agent({subagent_type: <role>})`) |

## Invocation forms

- `/position <name>` — load position, run bootstrap
- `/position <name> --resume` — same, but resume semantics if the profile defines them

## Wrapper skills

A position can ship with a sibling **wrapper skill** that adds position-specific lifecycle behavior on top of `/position`. Wrappers are optional — `/position <name>` always works directly. If a wrapper is installed alongside `/position` in the same skills repo, prefer the wrapper for the position it covers (it handles position-specific contracts the generic loader can't).

Example: `/tpm` (where shipped as a separate skill) is the wrapper for the `tpm` position — it invokes `/position tpm` and adds a unidirectional refusal contract. If `/tpm` is not installed in your environment, use `/position tpm` directly; the position loads cleanly without the wrapper, just without the refusal-contract enforcement.

## Quick reference

| Step | Action | On failure |
|---|---|---|
| 1 | Resolve `team/<name>.md` | Refuse with available positions list |
| 2 | Read profile + state dir | Silently skip state if dir absent |
| 3 | Regenerate live state per profile | — |
| 4 | Acknowledge + hold position | — |
| 5 | Honor `--resume` if present | No-op if profile has no resume semantics |
| 6 | Switch positions on re-invoke | Refuse for unidirectional positions (tpm) |
