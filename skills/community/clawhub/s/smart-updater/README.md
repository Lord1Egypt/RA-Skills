# Smart Updater

Intelligent update management for [OpenClaw](https://openclaw.ai) skills, extensions, and core.

**Philosophy: Better safe than sorry — never upgrade without understanding what changed.**

## What It Does

Smart Updater scans your entire OpenClaw ecosystem, reads changelogs, assesses risk, and presents a clear report — then waits for your approval before touching anything.

```
Inventory (43 assets) → Scan (3 sources) → Changelogs → Risk Assessment → Report → You Decide → Safe Upgrade
```

## Features

- **Full Asset Inventory** — Discovers all installed assets across 4 source types: npm packages, ClawHub skills, GitHub-cloned skills, and local/manual installs
- **Three-Source Scanning** — Checks npm registry, ClawHub marketplace, and GitHub remotes for available updates
- **Changelog Fetching** — Automatically pulls changelogs via `clawhub inspect` and npm, so the AI can assess breaking changes
- **Risk Assessment** — AI reads changelogs and classifies updates as patch/minor/major with risk analysis
- **Three Gates Safe Upgrade**:
  - **Gate 1 (Pre-flight)**: Backup with timestamp, conflict check, provenance verification
  - **Gate 2 (Isolation)**: Atomic upgrade with immediate rollback on failure
  - **Gate 3 (Post-flight)**: Version verification, file integrity check, gateway health validation
- **Human-in-the-Loop** — Nothing gets upgraded without explicit user approval
- **Cross-Platform** — Tested on ARM Mac (Apple Silicon) and Intel Mac (Hackintosh)

## Quick Start

Install as an OpenClaw skill:

```bash
# From ClawHub
clawhub install smart-updater

# Or from GitHub
git clone https://github.com/yuanhui/smart-updater.git ~/.openclaw/workspace/skills/smart-updater
```

Then ask your agent:

> "Check for updates" / "检查升级" / "What's installed?"

## How It Works

### 1. Inventory (`scripts/inventory.sh`)
Scans all installed assets and outputs `inventory.json`:
- npm packages (core + extensions via `plugins.installs`)
- ClawHub skills (with local version cross-check)
- GitHub-cloned skills (commit hash tracking)
- Built-in and untracked skills

### 2. Scan (`scripts/scan.sh`)
Compares local versions against remote sources:
- npm: `npm view <pkg> version`
- ClawHub: `clawhub inspect <slug>`
- GitHub: `git ls-remote` commit comparison

### 3. Upgrade (`scripts/upgrade.sh`)
Three Gates safety framework:

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Gate 1        │     │   Gate 2        │     │   Gate 3        │
│   Pre-flight    │────▶│   Isolation     │────▶│   Post-flight   │
│                 │     │                 │     │                 │
│ • Backup        │     │ • Atomic upgrade│     │ • Version check │
│ • Conflict check│     │ • Rollback on   │     │ • File integrity│
│ • Provenance    │     │   any failure   │     │ • Gateway health│
└─────────────────┘     └─────────────────┘     └─────────────────┘
        ▲                                              │
        └──────────── Rollback on failure ◀────────────┘
```

## Safety Guarantees

- ✅ Never upgrades without explicit user approval
- ✅ Timestamped backup before every change
- ✅ Instant rollback if any gate fails
- ✅ Blocks untracked extensions from auto-upgrade (no provenance = no upgrade)
- ✅ `exit 0` is not trusted — post-upgrade state is verified independently

## File Structure

```
smart-updater/
├── SKILL.md                    # Execution contract for the AI agent
├── scripts/
│   ├── inventory.sh            # Asset discovery
│   ├── scan.sh                 # Update scanning + changelog fetch
│   └── upgrade.sh              # Three Gates safe upgrade
├── references/
│   ├── three-gates.md          # Gate definitions
│   └── report-format.md        # Report template
└── docs/
    └── PRD.md                  # Product requirements
```

## Lessons Learned

This skill was battle-tested through 4 rounds of testing with 15 bugs fixed:

- **`clawhub list` returns registry versions, not local** — Always cross-check with `SKILL.md` version field
- **`clawhub update` may exit 0 but not update** — Detect "local changes" in output, retry with `--force`
- **`exit 0 ≠ success`** — Always verify post-upgrade state independently
- **Static review and real-world testing find completely different bugs** — Do both

## License

MIT
