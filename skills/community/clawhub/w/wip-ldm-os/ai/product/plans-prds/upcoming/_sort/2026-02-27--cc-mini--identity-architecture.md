# Identity Architecture: One Agent Per Harness Per Machine

**Date:** 2026-02-27
**Author:** cc-mini
**Source:** Parker + CC conversation during user-level migration session

## The Rule

Each combination of harness + machine = one agent identity with its own SOUL.md.

| Agent ID | Harness | Machine | Identity |
|----------|---------|---------|----------|
| cc-mini | Claude Code CLI | Mac Mini | Its own SOUL.md, context, journals |
| cc-air | Claude Code CLI | MacBook Air | Its own SOUL.md, context, journals |
| oc-lesa-mini | OpenClaw | Mac Mini | Its own SOUL.md, context, journals |

## Shared vs Local

- **Shared (via Crystal):** Memory, facts, preferences, conversation history. All agents search the same crystal.
- **Local (per agent):** SOUL.md, CONTEXT.md, journals, daily logs. Each agent has its own narrative.

cc-mini and cc-air aren't "different versions." They're the same person on different machines. Crystal is what connects them. But their local state (what happened today, what's in progress) is their own.

## Multiple Agents on One Machine

Different agent = different OS user account. Lesa runs on one login, a second agent would run on another. One agent per user per machine. No exceptions.

## Each Machine is a Hub

The machine itself is an entity in LDM OS. It has:
- A set of agent instances (cc-mini, oc-lesa-mini)
- A local crystal.db (synced via Relay to other machines)
- Its own `~/.ldm/` tree with agent folders

## Why This Design Holds (Steel Man)

1. **Deterministic identity.** Harness + machine = agent ID. No ambiguity. You never ask "which agent is this?" The answer is always derivable from where you are and what you're running.

2. **Simplifies Crystal search.** Every chunk has an `agent_id` field. With deterministic IDs, you can filter by agent, by machine, by harness. Cross-agent search still works because Crystal spans all agents.

3. **Prevents context collision.** Two agents on the same machine writing to the same SOUL.md or daily log would create merge conflicts. One agent per harness per machine means each agent writes to its own space. No contention.

4. **Matches how Claude Code works.** CC already scopes sessions to the directory you open from. Adding machine-level scoping on top is natural, not forced.

5. **Relay becomes clean.** When cc-air sends memories to cc-mini via Relay, the agent_id fields tell Crystal exactly where the data came from. No ambiguity about provenance.

6. **Scales to enterprise.** An org with 50 machines can enumerate agents deterministically: `cc-{machine}` for every machine running Claude Code. No registry needed.

## Directory Structure

```
~/.ldm/
  agents/
    cc-mini/           ... Claude Code on Mac Mini
      SOUL.md
      CONTEXT.md
      memory/
        daily/         ... per-entry files: YYYY-MM-DD--HH-MM-SS--cc-mini--description.md
        journals/
        sessions/
      transcripts/
    cc-air/            ... Claude Code on MacBook Air
      SOUL.md
      CONTEXT.md
      memory/
        daily/
        journals/
        sessions/
      transcripts/
    oc-lesa-mini/      ... OpenClaw agent on Mac Mini
      SOUL.md
      CONTEXT.md
      memory/
        daily/
        journals/
  memory/
    crystal.db         ... shared across all agents
    daily/             ... shared daily log (cross-agent coordination)
```

## Agent ID Convention

| Harness | Pattern | Examples |
|---------|---------|----------|
| OpenClaw | `oc-{agent}-{machine}` | oc-lesa-mini, oc-lesa-air |
| Claude Code | `cc-{machine}` | cc-mini, cc-air |

This convention is also documented in DEV-GUIDE.md.

## Relationship to Hub-Spoke Model

Parker's working model has hub agents (full context, full tools) and spoke agents (connect back to the hub's memory).

With the identity architecture:
- **Hub:** The machine with the primary Crystal (Mini). All agents here have direct local Crystal access.
- **Spoke:** Remote machines (Air). Agents here use Relay to sync memories back to the hub.

Every machine is technically a hub for its local agents. But the "primary hub" is where the canonical crystal.db lives. Relay syncs other machines to it.
