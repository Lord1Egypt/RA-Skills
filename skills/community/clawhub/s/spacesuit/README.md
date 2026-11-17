# 🧑‍🚀 OpenClaw Spacesuit

> *Your AI agent's workspace, suited up for the real world.*

A batteries-included framework scaffold for [OpenClaw](https://github.com/openclaw/openclaw) workspaces. When you install OpenClaw, you get an AI agent — but an agent without a workspace is like an astronaut without a spacesuit. This package gives your agent structure, memory, safety, and operational conventions.

## Core monitoring and agent flavors

[Command Center](https://github.com/jontsai/openclaw-command-center) works on its
own out of the box. **Spacesuit is its highly recommended companion** for workspace
conventions and optional per-agent flavors, without forking the dashboard.

**Spacesuit alone has no human-agent interaction UX.** It can scaffold a workspace
and collect data without Command Center, but Command Center supplies the dashboard
UI that makes the companion experience usable. Installing Spacesuit does not add a
chat composer or another interaction interface.

The first implemented flavor, [business operations](flavors/business-operations/README.md),
composes Intel, Pipeline and Monetization through a versioned read-only snapshot
contract. It requires a Command Center build with extension-host v1 support; older
builds do not consume these snapshots. Selection and collection are explicit:

```bash
node scripts/flavors.js preview --workspace /path/to/workspace
node scripts/flavors.js apply --workspace /path/to/workspace
node scripts/flavors.js collect --workspace /path/to/workspace
```

Requires Node.js 18+. See the flavor runbook for identity matching, bounds, core-only
disable, backups and restore. Base upgrades now preserve unmarked files unless explicitly adopted;
these commands do not schedule jobs or restart anything. See the
[architecture](docs/architecture/agent-flavors.md) and
[implementation plan](docs/plans/flavor-packages-v1.md).

## Unified project portfolio (read-only)

Spacesuit now includes [project tracker adapters](docs/adapters/project-trackers.md)
for Linear projects and explicitly configured Jira epics. The offline preview/apply
CLI converts provider exports into Command Center's shared project-board contract;
**live tracker synchronization is not configured**. An injected, bounded read-only
transport API is available for future authorized host connectors. Native status and
identity are preserved; memory/topic strategies remain independently composable.
Asana and GitHub Issues are planned adapter targets, not implemented providers.

## What's Included

- **Session startup protocol** — security-first file loading order
- **Memory system** — daily logs + curated long-term memory with commit discipline
- **Git workflow** — mandatory pre-commit checks, worktree conventions, parallel multi-agent coordination with merge locks
- **Safety rules** — pre-action checklist, destructive-action guards, stand-down protocol
- **Priority system** — P0–P5 triage for tasks and incidents
- **Cross-platform handoffs** — structured context transfer between Slack/Discord/Telegram
- **Heartbeat framework** — proactive periodic checks with state tracking
- **Decision logging** — mandatory audit trail for architectural decisions
- **Meta-learning framework** — expert-first research methodology (Dunning-Kruger aware)
- **Security baseline** — secret transmission policy, prompt injection defense, data classification

## Installation

### Via ClawHub (recommended)

```bash
clawhub install spacesuit
```

This places the package at `<workspace>/skills/spacesuit/`.

### Manual

```bash
cd <your-openclaw-workspace>
git clone https://github.com/jontsai/openclaw-spacesuit.git skills/spacesuit
```

### First-Time Setup

After installation, run the installer to create workspace files from templates:

```bash
cd skills/spacesuit
bash scripts/install.sh --workspace /absolute/workspace
```

This creates `AGENTS.md`, `SOUL.md`, `TOOLS.md`, `HEARTBEAT.md`, `SECURITY.md`, `MEMORY.md`, `IDENTITY.md`, `USER.md`, and `Makefile` at your workspace root — each with framework content wrapped in `SPACESUIT` markers and space for your customizations.

### Personalize

```bash
# Edit these files at your workspace root:
vi IDENTITY.md    # Name your AI
vi USER.md        # Tell it about yourself
vi SOUL.md        # Set the personality/vibe
vi TOOLS.md       # Add your tool configs
```

## How It Works

OpenClaw reads hardcoded filenames from the workspace root (`AGENTS.md`, `SOUL.md`, etc.). Since we can't change that loading behavior, Spacesuit uses **section-based merging**:

1. Framework content is wrapped in `<!-- SPACESUIT:BEGIN -->` / `<!-- SPACESUIT:END -->` markers
2. On upgrade, only the content between markers is replaced
3. Everything outside the markers (your customizations) is preserved

## Upgrading

```bash
cd skills/spacesuit

# See what would change
make diff

# Preview upgrade (no changes)
make upgrade-dry

# Apply upgrade
make upgrade

# Check version
make version
```

## Package Structure

```
openclaw-spacesuit/
├── SKILL.md               # ClawHub metadata
├── VERSION                # Package version
├── CHANGELOG.md           # Release history
├── Makefile               # init/upgrade/diff commands
├── base/                  # Framework source content
│   ├── AGENTS.md          # Session protocol, memory, git, safety, priorities
│   ├── HEARTBEAT.md       # Heartbeat check skeleton
│   ├── MEMORY.md          # Long-term memory starter
│   ├── SECURITY.md        # Immutable security rules
│   ├── SOUL.md            # Personality scaffold
│   └── TOOLS.md           # Tool organization guide
├── templates/             # Workspace file templates
│   ├── AGENTS.md          # Framework + customization sections
│   ├── HEARTBEAT.md
│   ├── IDENTITY.md        # Agent identity (name, emoji)
│   ├── Makefile            # Gateway management
│   ├── MEMORY.md
│   ├── SECURITY.md
│   ├── SOUL.md
│   ├── TOOLS.md
│   └── USER.md            # About your human
└── scripts/               # Automation
    ├── install.sh          # First-time setup
    ├── upgrade.sh          # Section-based merge upgrade
    ├── diff.sh             # Show pending changes
    └── sync-operators.sh   # Generate operators.json from sessions
```

## Data Layer Scripts

Spacesuit includes utility scripts that gather data for dashboards and tooling:

### sync-operators.sh

Auto-generates `state/operators.json` from session transcripts:

```bash
# Run from workspace
./scripts/sync-operators.sh

# Preview without writing
./scripts/sync-operators.sh --dry-run

# Explicit workspace
./scripts/sync-operators.sh --workspace /path/to/workspace

# Multi-profile support (uses ~/.openclaw-<name>)
./scripts/sync-operators.sh --profile myprofile
./scripts/sync-operators.sh --dev  # shortcut for --profile dev

# Or via environment variable
OPENCLAW_PROFILE=myprofile ./scripts/sync-operators.sh
```

**What it does:**
- Scans OpenClaw session transcripts for user messages
- Extracts Slack user IDs and usernames
- Counts messages per operator
- Preserves manually-set roles across syncs

**Output:** `state/operators.json` — used by [OpenClaw Command Center](https://github.com/jontsai/openclaw-command-center)

**Supported channels:**
- ✅ Slack (`] username (USERID):` pattern)
- 🔜 Telegram, Discord, Signal (PRs welcome!)

## Files Managed

| Workspace File | Base Content | User Content |
|----------------|-------------|--------------|
| `AGENTS.md` | Session protocol, memory, git, safety, priorities | Channel mappings, tool configs, personal rules |
| `SOUL.md` | Core personality scaffold | Personal vibe, human-specific tone |
| `TOOLS.md` | Tool organization guidance | Actual tool configs, credentials refs, API details |
| `HEARTBEAT.md` | Check framework & state tracking | Specific checks to run |
| `SECURITY.md` | Full security baseline | Contact-specific alert channels |
| `MEMORY.md` | Long-term memory structure | Project notes, personal context |
| `IDENTITY.md` | — (template only) | Name, avatar, personality |
| `USER.md` | — (template only) | All about your human |
| `Makefile` | — (template only) | Gateway management targets |

## Releasing

Version bumps go through review. Publication is separate from validation:

```bash
bash scripts/release.sh --current
bash scripts/release.sh 0.4.0
bash scripts/release.sh 0.4.0 --stage /absolute/new/staging-directory
```

These commands do not commit, tag, push or publish. Follow the
[release and migration guide](docs/releases/README.md), including Bash 4+
requirements, package validation and backup restoration. `version.txt` supports
registry downloads that omit extensionless `VERSION`/`Makefile` files. Starter
installation preserves existing files; upgrade preserves unmarked files unless
`--adopt-unmarked` is selected explicitly after reviewing a dry run.

## Author

Created by [jontsai](https://github.com/jontsai).

## License

MIT

## Work graph compiler

Normalize reviewed Linear/Jira exports and runtime assignments into an evidence-labeled operations graph. [Contract, usage, and inference limits](docs/work-graph.md). This is an offline compiler, not live tracker synchronization.
