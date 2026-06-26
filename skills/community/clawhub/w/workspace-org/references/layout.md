# Directory Layout Reference

## Core principle

All agent-generated content goes under a single `files/` directory. The workspace root
contains only core configuration, system directories, and the `files/` container.

## Per-agent workspace

```
<agent-name>/
├── AGENTS.md          Core config: routing, dispatch rules
├── SOUL.md            Tone, persona, work style
├── IDENTITY.md        Name, role, one-line identity
├── USER.md            Human owner profile
├── MEMORY.md          Long-term memory notes
├── HEARTBEAT.md       Event/recurring check instructions
├── BOOTSTRAP.md       First-run setup
├── TOOLS.md           Tool usage rules
├── skills/            ClawHub-installed skills
├── memory/            Long-term memory files
├── files/
│   ├── tmp/           Disposable: scripts, patches, one-off output
│   ├── notes/         Keep-worthy: design docs, analysis, snapshots
│   ├── inbox/         Incoming deliverables from other agents
│   ├── outbox/        Outgoing deliverables for owner/other agents
│   └── archive/       Inactive projects, old data
```

## Multi-agent workspace (root)

```
workspace/                          ← ~/.openclaw/workspace/
├── AGENTS.md / SOUL.md ...        ← Root-level configs
├── liyj/                          ← Main agent
├── hr/                            ← HR agent
├── memory/                        ← Shared memory
├── skills/                        ← Shared skills
├── runtime/                       ← OpenClaw runtime
├── files/
│   ├── tmp/
│   ├── notes/
│   ├── inbox/
│   ├── outbox/
│   ├── archive/
│   └── experts/                   ← All expert-* engagements
│       ├── accounting-20260501/
│       ├── legal-20260503/
│       └── ...
```

## Expert lifecycle

1. HR creates `files/experts/<domain>-<date>/` with core configs
2. Expert works in its own directory using the same files/ layout
3. Deliverables go to expert's `files/outbox/` → main's `files/inbox/`
4. After engagement: expert dir stays in `files/experts/` for reference

## Cleanup rules

| Path | When to clean | Method |
|------|--------------|--------|
| `files/tmp/` | Any time | Delete all contents |
| `files/notes/` | Never | Keep forever |
| `files/inbox/` | After processing each item | Delete processed item |
| `files/outbox/` | After owner acknowledges | Delete or archive |
| `files/archive/` | Periodic review | Manual review |
| `files/experts/` | After engagement ends | Archive or delete |
