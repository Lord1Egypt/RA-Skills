###### WIP Computer

[![npm](https://img.shields.io/npm/v/@wipcomputer/wip-license-hook)](https://www.npmjs.com/package/@wipcomputer/wip-license-hook) [![CLI / TUI](https://img.shields.io/badge/interface-CLI_/_TUI-black)](https://github.com/wipcomputer/wip-ai-devops-toolbox/blob/main/tools/wip-license-hook/cli.js) [![MCP Server](https://img.shields.io/badge/interface-MCP_Server-black)](https://github.com/wipcomputer/wip-ai-devops-toolbox/blob/main/tools/wip-license-hook/mcp-server.mjs) [![Claude Code Skill](https://img.shields.io/badge/interface-Claude_Code_Skill-black)](https://github.com/wipcomputer/wip-ai-devops-toolbox/blob/main/tools/wip-license-hook/SKILL.md) [![Universal Interface Spec](https://img.shields.io/badge/Universal_Interface_Spec-black?style=flat&color=black)](https://github.com/wipcomputer/wip-ai-devops-toolbox/blob/main/tools/wip-universal-installer/SPEC.md)

# wip-license-hook

License rug-pull detection and dependency license compliance for open source projects.

## The Problem

You fork an MIT project. You build on it. Six months later, the upstream quietly changes to BSL or proprietary. You pull the update without checking. Now your project is poisoned.

This has happened. It will happen again.

## The Solution

A pre-merge hook + daily scanner + public dashboard that:

1. **Maintains a license ledger** of every dependency and fork at time of adoption
2. **Gates all upstream merges** — if the license changed, the merge is blocked
3. **Scans daily** — catches license drift before it reaches your codebase
4. **Publishes a dashboard** — public proof of license health for anyone using your forks

## How It Works

### Git Hooks (Always On)

**Two mandatory hooks. No bypass.**

**Pre-pull** — before pulling anything from upstream:
```
git pull upstream main
  → hook fires FIRST
  → fetch without merge
  → check LICENSE, package.json, SPDX headers
  → compare against ledger
  → SAME? → pull proceeds
  → CHANGED? → BLOCK. Flag. Document. Notify. Do NOT pull.
```

**Pre-push** — before pushing any commit to our branch:
```
git push origin main
  → hook fires FIRST
  → check upstream license status
  → compare against ledger
  → SAME? → push proceeds
  → CHANGED? → ALERT. Warn that upstream has drifted. Push still allowed (it's our code) but we know.
```

Pre-pull = hard gate (blocks).
Pre-push = alert (warns, doesn't block our own work).

### License Ledger

`LICENSE-LEDGER.json` tracks every dependency:

```json
{
  "dependencies": [
    {
      "name": "openclaw",
      "source": "github:openclaw/openclaw",
      "type": "fork",
      "license_at_adoption": "MIT",
      "license_current": "MIT",
      "adopted_date": "2026-02-05",
      "last_checked": "2026-02-15",
      "commit_at_adoption": "abc123",
      "status": "clean"
    }
  ],
  "last_full_scan": "2026-02-15T08:00:00Z",
  "alerts": []
}
```

Status values: `clean` | `changed` | `removed` | `unknown`

### LICENSE Snapshots

Physical copies of LICENSE files at adoption. Not just metadata. Proof that survives git history rewrites.

```
ledger/
  snapshots/
    openclaw/
      LICENSE-2026-02-05.txt    ← what it was when we forked
      LICENSE-2026-02-15.txt    ← latest check
```

If they rug-pull and rewrite history, we have the receipt on disk.

### Daily Cron Scan

Runs every morning:

1. For each fork: `git fetch upstream` (no merge), check LICENSE file
2. For each npm/pip dependency: check registry for current license metadata
3. Compare everything against the ledger
4. Generate report
5. If anything changed: alert immediately (message, email, or both)

### Public Dashboard

Static site (GitHub Pages or similar) generated from the ledger:

- List of all dependencies and forks
- License at adoption vs current license
- Last checked date
- Health status (green/yellow/red)
- Proof links (commit hashes, archived LICENSE files)

Anyone using our forks can verify: "WIP Computer adopted this when it was MIT, and it's still MIT."

## Detection Methods

### For Forks (git repos)
- Check `LICENSE` / `LICENSE.md` / `COPYING` file content
- Parse `package.json` license field
- Check for SPDX headers in source files
- Compare against known license text fingerprints

### For npm Dependencies
- `npm view <package> license`
- Compare against ledger

### For Python Dependencies
- `pip show <package>` license field
- PyPI API metadata

## Installation

### As an OpenClaw Skill
```bash
clawhub install wip-license-hook
```

### As a Git Hook
```bash
wip-license-hook install --repo .
```

### As a Cron Job
```bash
wip-license-hook scan --all --report
```

## Architecture

```
core/
  scanner.ts       — license detection logic
  ledger.ts        — ledger read/write/compare
  detector.ts      — license text fingerprinting
  reporter.ts      — generate reports and alerts
cli/
  index.ts         — CLI wrapper
skill/
  SKILL.md         — OpenClaw/agent skill definition
dashboard/
  index.html       — static dashboard generator
hooks/
  pre-merge.sh     — git hook script
```

## Commands

```bash
wip-license-hook init              # Initialize ledger for current project
wip-license-hook scan              # Scan all deps, update ledger
wip-license-hook check <dep>       # Check specific dependency
wip-license-hook gate              # Pre-merge license gate (for hooks)
wip-license-hook report            # Generate report
wip-license-hook dashboard         # Generate static dashboard
wip-license-hook alert             # Send alerts for any changes
```

## Why This Matters

> "Been dubious of MIT open source. Seen too many pull it or hide non-MIT bins for it all to work."

This tool is the guardrail. The receipt. The proof.

If your dependency gets rug-pulled, you have:
- The exact commit where the license was what you agreed to
- Documentation of when and what changed
- A clean fork point to fall back to
- Public proof for anyone downstream of you

## License

```
CLI, MCP server, skills                        MIT    (use anywhere, no restrictions)
Hosted or cloud service use                    AGPL   (network service distribution)
```

AGPL for personal use is free.

Built by Parker Todd Brooks, Lēsa (OpenClaw, Claude Opus 4.6), Claude Code (Claude Opus 4.6).
