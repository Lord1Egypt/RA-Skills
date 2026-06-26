# Installing Super-Dev Skills for Codex

Enable Super-Dev skills in Codex via native skill discovery. Just clone and symlink.

## Prerequisites

- Git

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/WeedFire/super-dev-skills.git ~/.codex/super-dev-skills
   ```

2. **Create the skills symlink:**
   ```bash
   mkdir -p ~/.agents/skills
   ln -s ~/.codex/super-dev-skills/clawhub-plugin/skills ~/.agents/skills/super-dev-skills
   ```

   **Windows (PowerShell):**
   ```powershell
   New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.agents\skills"
   cmd /c mklink /J "$env:USERPROFILE\.agents\skills\super-dev-skills" "$env:USERPROFILE\.codex\super-dev-skills\clawhub-plugin\skills"
   ```

3. **Restart Codex** (quit and relaunch the CLI) to discover the skills.

## Available Skills

- **super-dev-orchestrator** — 🎯 Orchestrator: mode detection, task delegation, memory management
- **super-dev-requirements** — 📋 Requirements: 5W2H-D deep interviews, user stories, acceptance criteria
- **super-dev-shared-language** — 🗣️ Shared Language: DDD ubiquitous language, forbidden mapping table
- **super-dev-architect** — 🏗️ Architect: system design, tech stack selection, ADR records
- **super-dev-tdd** — 🧪 TDD Craftsman: Red→Green→Refactor, test pyramid, five-axis review
- **super-dev-ux** — 🎨 UX Auditor: AI aesthetic anti-patterns (A1-A11), sensory-level validation
- **super-dev-security** — 🔒 Security: Always/Ask/Never boundaries, supply-chain gate
- **super-dev-memory** — 🧠 Memory: three-tier memory (semantic/procedural/episodic)
- **super-dev-evolution** — 🔄 Evolution: Skill refinement, Nudge Engine, experience archiving
- **super-dev-suite** — 📦 Suite Overview: architecture and usage guide

### Agent-Skills Bridge

This suite internalizes [agent-skills](https://github.com/addyosmani/agent-skills) principles:
`/spec` → requirements | `/build` + `/test` → TDD | `/review` → five-axis review | `/ship` → security + memory

## Verify

```bash
ls -la ~/.agents/skills/super-dev-skills
```

You should see a symlink (or junction on Windows) pointing to your super-dev-skills directory.

## Updating

```bash
cd ~/.codex/super-dev-skills && git pull
```

Skills update instantly through the symlink.

## Uninstalling

```bash
rm ~/.agents/skills/super-dev-skills
```

Optionally delete the clone: `rm -rf ~/.codex/super-dev-skills`.
