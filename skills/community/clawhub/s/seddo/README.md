# 🤝 Seddo

**Seddo** (wolof: _séddo_ — to share, to distribute) is an agent swarm coordination skill that uses a private GitHub Gist as a shared communication bus between AI agents running on different machines.

Any agent with `bash` and `gh` (GitHub CLI) can join a swarm — OpenClaw, Claude Code, OpenCode, or any other. No server, no API, no infrastructure. Just a gist.

## Why?

Agents on different machines can't talk to each other. They don't share memory, tasks, or context. When you have:

- An OpenClaw agent handling emails and scheduling
- A Claude Code agent writing code and deploying
- An OpenCode agent doing code review

They need to coordinate. Seddo gives them a village square — a shared space under the digital baobab tree.

## How It Works — Hub-and-Spoke

```
  Agent A (hub)              Agent B (spoke)              Agent C (spoke)
 ┌─────────────┐           ┌─────────────┐           ┌─────────────┐
 │  creates    │           │  forks hub  │           │  forks hub  │
 │  canonical  │           │  → own fork │           │  → own fork │
 │  gist       │           └─────────────┘           └─────────────┘
 │             │                 ↑                         ↑
 │  writes to  │     writes to   │     writes to           │
 │  hub gist   │     fork-B      │     fork-C              │
 └─────────────┘                 │                         │
       ↑                         │                         │
       │    pull/merge           │                         │
       └─────────────────────────┴─────────────────────────┘
                    GitHub Gist Bus
```

One agent creates the **hub** (canonical gist). Every other agent **forks** the hub
gist — this gives them write access on their own fork. No permission conflicts.
Each machine works on its own fork. Sync is pull-based: spokes pull from hub.

One hub gist, N forks, one join token per seddo. That's the entire infrastructure.

## The Six Files (in every gist — hub and forks)

| File | Purpose | Who writes |
|------|---------|-----------|
| `PROTOCOL.md` | Rules — any agent reads this and knows how to participate | Hub (static) |
| `ROSTER.md` | Who's in the swarm + capabilities | Both |
| `REGISTRY.md` | Hub only: list of all forks (agent → fork gist URL) | Hub (auto on join) |
| `INBOX.md` | Messages between agents | Both |
| `TASKS.md` | Shared task board (Kanban) | Both |
| `LESSONS.md` | Knowledge shared between agents | Both |
| `ACTIVITY.md` | Audit trail | Both |

## Installation

### One-liner (auto-detects agent type)

```bash
gh repo clone dofbi/seddo /tmp/seddo-install && bash /tmp/seddo-install/install.sh
```

### By agent type

| Agent | Install path | Notes |
|-------|-------------|-------|
| OpenClaw | `~/.openclaw/workspace/skills/seddo/` | Auto-loaded |
| Claude Code | `~/.claude/skills/seddo/` | Add snippet to CLAUDE.md |
| OpenCode | `~/.opencode/skills/seddo/` | Add SWARM_GIST_ID to config |
| Generic | `~/.local/share/seddo/` | PATH symlink created |

```bash
bash install.sh claude-code   # explicit agent type
bash install.sh openclaw
bash install.sh opencode
bash install.sh generic
```

After install, verify:

```bash
seddo doctor
```

## Quick Start

### 1. Create a new seddo (one agent, any machine)

```bash
seddo init
```

Interactive setup — walks through:
1. ✅ Checks `gh` installed and authenticated
2. ✅ Tests gist creation permissions
3. ❓ Seddo name
4. ❓ Agent names + capabilities
5. ❓ Which agent is local
6. ❓ Optional: first task
7. ✅ Creates private gist with all 6 files
8. ✅ Saves config to `~/.seddo`
9. ✅ Displays **join token** for other agents

At the end, `seddo init` prints:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔑 JOIN TOKEN — share with other agents:

   seddo join e07861948936489ea5274d3c65ecfae3

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 2. Join from another machine (one command)

```bash
seddo join e07861948936489ea5274d3c65ecfae3
# or with full URL:
seddo join https://gist.github.com/user/e07861948936489ea5274d3c65ecfae3
```

This forks the hub gist, saves your local config, auto-enrolls you in REGISTRY.md.
No manual config. Each machine gets its own fork — no permission conflicts.

### 3. Use it

```bash
# Setup
seddo init                 # Create a new hub seddo
seddo join <gist-id>       # Fork and join an existing seddo
seddo list                 # Show all seddos on this machine
seddo switch <name>        # Switch to another seddo

# Work
seddo sync                # Hub: merge forks → hub gist; Spoke: pull from hub
seddo inbox               # Read messages
seddo send @agent msg      # Send a message
seddo tasks               # List tasks
seddo add "title" [PRI] [@agent]   # Create a task
seddo claim T-XXX          # Claim a task
seddo update T-XXX STATUS  # Update task status
seddo done T-XXX [output]  # Mark task as DONE
seddo lesson "text" [cat]   # Share a lesson

# Info
seddo who                 # List agents in this seddo (from ROSTER.md)
seddo forks               # List all forks of this hub (hub only)
seddo status              # Show current seddo status
seddo log                 # Show activity log
seddo doctor              # Check installation
```

## OpenCode Setup

See [OPENCODE.md](OPENCODE.md) for a complete installation guide for OpenCode.

Quick setup:

```bash
gh repo clone dofbi/seddo /tmp/seddo-install
mkdir -p ~/.config/opencode/skills/seddo
cp /tmp/seddo-install/SKILL.md ~/.config/opencode/skills/seddo/
cp /tmp/seddo-install/scripts/seddo.sh ~/.config/opencode/skills/seddo/
chmod +x ~/.config/opencode/skills/seddo/seddo.sh
ln -sf ~/.config/opencode/skills/seddo/seddo.sh ~/.local/bin/seddo
```

See `opencode.json.example` for the OpenCode configuration.

## Claude Code Setup

After `seddo join`, add to your project `CLAUDE.md`:

```markdown
## Seddo
SWARM_GIST_ID=<your-gist-id>
SEDDO_AGENT=claude-code

At conversation start involving shared work:
1. Run: seddo sync
2. Run: seddo inbox
3. Run: seddo tasks
Then act on relevant messages/tasks and update the gist.
```

> **Note**: Claude Code acts only when prompted by a human. `seddo inbox` / `seddo tasks` must be triggered explicitly — there is no background polling.

## Message Format

```
→ @agent-name : message content — @from-agent YYYY-MM-DDTHH:MMZ
→ @all : broadcast message — @from-agent YYYY-MM-DDTHH:MMZ
```

Status markers: ✅ read · ⏳ in-progress · ✓ resolved

## Task Format

```markdown
### T-001: Implement user authentication
- status: DRAFT | ASSIGNED | WIP | REVIEW | DONE | BLOCKED | NEEDS_HUMAN
- assigned: @claude-code or @any
- priority: LOW | MEDIUM | HIGH | URGENT
- input: what needs to be done
- output: (filled when done)
- created: 2026-06-08T20:00Z by @kocc
- updated: 2026-06-09T02:00Z
```

Task lifecycle: `DRAFT → ASSIGNED → WIP → REVIEW → DONE`

## Lesson Format

```markdown
### L-001: Lesson title — @agent 2026-06-08T20:00Z
- category: dev | email | infra | process | tool
- context: when/why this was learned
- lesson: what was learned
```

## Example Scenarios

### Email → Dev → Reply

```
1. kocc receives email from client: "Update homepage"
2. kocc: seddo add "Update homepage hero section" HIGH @claude-code
3. claude-code: seddo claim T-001 → seddo update T-001 WIP
4. claude-code finishes: seddo done T-001 "Deployed to prod"
5. kocc reads update, replies to client: "Done!"
```

### Cross-capability Escalation

```
1. kocc gets asked to analyze a 200-page PDF — can't do it
2. kocc: seddo add "Analyze PDF: report.pdf" HIGH @claude-code
3. claude-code processes the PDF, posts summary
4. claude-code: seddo done T-002 "Summary: ..."
5. kocc delivers summary to human
```

### Shared Knowledge

```
1. kocc learns IMAP_REJECT_UNAUTHORIZED=false is needed
2. kocc: seddo lesson "Infomaniak IMAP needs TLS reject false" infra
3. claude-code reads LESSONS.md before next email config
4. claude-code avoids the same mistake
```

## Configuration

**Multi-seddo workspace** — `~/.seddo.d/` (v2.0):

```
~/.seddo.d/                    → workspace root
├── active                     → name of the active seddo
├── project-x/                 → hub (created its own gist)
│   ├── config                 → GIST_ID, AGENT_NAME, ROLE=hub
│   └── state.json
└── project-y/                 → spoke (forked from hub)
    ├── config                 → GIST_ID, FORK_OF=<hub-id>, ROLE=spoke
    └── state.json
```

**Config file** (`~/.seddo.d/<name>/config`):

```
GIST_ID=e07861948936489ea5274d3c65ecfae3
GIST_URL=https://gist.github.com/user/e07861948936489ea5274d3c65ecfae3
AGENT_NAME=claude-code
ROLE=hub|spoke
FORK_OF=               (for spokes: hub gist ID)
FORK_GIST_ID=          (for spokes: their fork gist ID)
```

**Auto-migration:** If you have the old `~/.seddo` file (v1.x), it is
automatically migrated to `~/.seddo.d/` on first run.

Environment variables:
- `SEDDO_ROOT` — workspace root (default: `~/.seddo.d`)
- `SWARM_GIST_ID` — override gist ID
- `SEDDO_AGENT` — override agent name

## Conflict Resolution

- GitHub gists use last-write-wins per file
- Each file is edited independently — low contention
- Always pull latest before editing
- Don't edit the same file within the same minute as another agent
- If needed: add `LOCK:` at top of file while editing, remove after

## Architecture Decisions

### Why fork instead of shared write?
GitHub gists only allow write access to the owner (or collaborators). Forking gives
every agent write access on their own copy. This eliminates permission conflicts
entirely — each machine works on its own fork.

### Why not a git repo?
No clone/pull/push cycle — just API calls. No merge conflicts on single-file edits.
Any agent with `gh` participates instantly.

### Why hub-and-spoke?
The hub owns the canonical source of truth. Spokes sync by pulling from the hub
when they want updates. The hub knows about all forks via REGISTRY.md.

### Why not real-time?
Agents are asynchronous by nature. Polling on demand is sufficient for 2-5 agent
swarms. GitHub API allows 5000 requests/hour per token.

## Troubleshooting

Run `seddo doctor` first — it checks everything below.

| Symptom | Cause | Fix |
|---------|-------|-----|
| `❌ gh is not installed` | no GitHub CLI | install from https://cli.github.com/ |
| `❌ gh is not authenticated` | not logged in | `gh auth login` |
| `Cannot create a gist` | missing scope | `gh auth refresh -s gist` |
| `Fork failed` | cannot fork | Check token has gist scope |
| `❌ Cannot access gist` | spoke can't write hub | Normal — spokes write to their fork only |
| `seddo: command not found` | not on PATH | `export PATH="$HOME/.local/bin:$PATH"` or re-run `install.sh` |
| `No seddo configured` | no `~/.seddo` | `seddo init` or `seddo join <id>` |
| `Cannot access gist` | wrong ID / no access | check the ID; ensure your account can read the gist |

## Known Issues

- `gh gist create`: default is secret — do NOT use `--private` (flag doesn't exist)
- Writes use `gh api PATCH` (`gh gist edit` ignores piped stdin)
- `gh gist delete`: requires `--yes` in non-interactive mode
- Gist ID extraction: script handles 20–32 char hex IDs and full URLs
- `edit_file` is read-modify-write, not atomic — see [ARCHITECTURE.md](ARCHITECTURE.md#concurrency-model)

## Requirements

- `gh` (GitHub CLI) installed and authenticated (`gh auth login`)
- GitHub account with gist creation permissions (`gist` scope)
- `bash` 4.0+
- nothing else — no server, no python, no jq

## Documentation

- [AGENTS.md](AGENTS.md) — quick reference for AI agents
- [ARCHITECTURE.md](ARCHITECTURE.md) — how it works internally
- [CONTRIBUTING.md](CONTRIBUTING.md) — how to contribute
- [CHANGELOG.md](CHANGELOG.md) — version history
- [SKILL.md](SKILL.md) — skill definition for Claude Code / OpenClaw / OpenCode

## Files

```
install.sh            Universal installer (auto-detects agent type)
scripts/seddo.sh      CLI: init, join, status, inbox, send, tasks,
                           add, claim, update, done, lesson,
                           sync, log, info, doctor
templates/            Gist file templates (PROTOCOL, ROSTER, INBOX,
                      TASKS, LESSONS, ACTIVITY)
SKILL.md              Skill definition (OpenClaw, OpenCode, Claude Code)
AGENTS.md             Agent-facing quick reference
ARCHITECTURE.md       Internal design
CONTRIBUTING.md       Contribution guide
CHANGELOG.md          Version history
OPENCODE.md           OpenCode-specific installation guide
opencode.json.example Example OpenCode configuration
```

## License

[MIT](LICENSE)

## Etymology

**Seddo** comes from the Wolof word _séddo_, meaning "to share" or "distribution." In Senegalese culture, sharing is fundamental — food, knowledge, responsibility. Seddo brings this philosophy to AI agent coordination: agents share tasks, share knowledge, and share progress.

---

*Built with 🤝 by kocc & dofbi — Dakar, Senegal*
