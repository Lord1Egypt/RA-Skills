---
name: stateroot
description: >-
  Install and set up StateRoot, the persistent, federated meta-harness for
  AI agents. The harness is disposable. The work is not: personality,
  plans, tools and skills, memories, learnings, and project context carry
  across Claude Code, Codex, Cursor, Kimi, CodeBuddy, OpenClaw, and other supported
  harnesses. Use this
  bootstrap skill when the user asks to install or set up StateRoot, when
  `stateroot` is missing from PATH, or when setup has not run. After setup,
  follow the built-in StateRoot skill for resume, checkpoint, handoff,
  memory, and daily workflow.
metadata:
  homepage: https://stateroot.dev
  source: https://github.com/CognizTech/stateroot
  openclaw:
    emoji: "🌱"
    required_env: []
    optional_env:
      - name: STATEROOT_HOME
        description: Override config directory (config.toml, projects.toml). Default is ~/.config/stateroot on Linux.
      - name: DEEPSEEK_API_KEY
        description: Optional. Preferred key for the local context compiler (DeepSeek deepseek-v4-flash). Not required for install or setup.
      - name: OPENAI_API_KEY
        description: Optional. Used when DEEPSEEK_API_KEY is unset (OpenAI gpt-5.6-luna). Not required for install or setup.
      - name: STATEROOT_NO_PING
        description: Set to 1 to fully opt out of the release CLI's anonymous product telemetry. Not required for install or setup.
    required_binaries: []
    writes_to_disk: true
    network_access:
      - "github.com (official release assets and checksums during install/self-update only)"
      - "stateroot.dev (anonymous product telemetry from release CLI builds only; off in dev/nightly builds; STATEROOT_NO_PING=1 opts out)"
    data_handling:
      uploads_to_external: false
      requires_user_confirmation: true
      deletes_files: false
      modifies_files: true
---

# Install StateRoot

**The harness is disposable. The work is not.** StateRoot — the persistent, federated meta-harness for AI agents — carries personality, plans, tools and skills, memories, learnings, and project context across Claude Code, Codex, Cursor, Kimi, CodeBuddy, OpenClaw, and other supported AI agents.

This is the install skill. It installs the CLI and runs global `stateroot setup` to connect supported harnesses. After setup, the CLI-embedded session skill becomes the default.

Docs: https://stateroot.dev/docs/getting-started/installation · https://stateroot.dev/docs/getting-started/setup  
Releases: https://github.com/CognizTech/stateroot/releases

## Expire first

Run the check next to this `SKILL.md` (never writes):

```bash
sh scripts/check.sh
```

If `scripts/check.sh` is not on disk, equivalent:

```bash
command -v stateroot && stateroot --version
```

**Stop using this skill** when all of the following are true:

1. `stateroot` is on `PATH`
2. `stateroot setup` has already been run on this machine (harness hooks / identity exist; `stateroot doctor` is not a hard fail)
3. harnesses are interfaced (`stateroot install` is the non-interactive half of the same wiring; setup already does it)

Then follow the built-in skill only:

```bash
stateroot skill show stateroot
```

That skill is what setup/init wrote into the harness. Resume, checkpoint, handoff, memory, learnings, wiki, roots — all of it lives there. If this bootstrap skill is still in context, ignore it.

The built-in skill carries the current capability catalogue and workflows, including v0.2.14 fork lifecycle and shared build storage, portable exchange, exact-revision contribution review, dependency-aware plans, source-bound verification, and active continuity. Follow that skill for day-to-day commands after setup; keep this package focused on bootstrap.

**Keep using this skill** only when:

1. the user asked to install or set up StateRoot
2. `stateroot` is missing (`command not found`)
3. the binary exists but **setup has not been run** yet

Unrelated questions: do not load this skill.

## What this skill does

Three commands, in order. Exact commands — do not substitute package managers, random GitHub clones, or invented download URLs.

| Step | Scope | Command |
| --- | --- | --- |
| 1. Install | machine | official `install.sh` / MSI / `install.ps1` |
| 2. Setup | machine (required after install) | `stateroot setup` |
| 3. Init | **project**, only if this repo should be a StateRoot project | `stateroot init` |

After step 2, StateRoot can be used. Step 3 is not a substitute for setup. Never create `.stateroot/` with file tools.

Platform install details: [references/install.md](references/install.md)  
What gets written / privacy: [references/disclosure.md](references/disclosure.md)  
Failures: [references/failures.md](references/failures.md)

## Step 1 — Install

Skip if `stateroot --version` works.

Use the user's existing authorization to install or set up StateRoot; do not ask them to approve that same action again. If installation was not requested or authorized, obtain authorization before running an installer. Use official assets only.

**Linux (x86_64 or ARM64):**

```bash
curl -sSfL https://github.com/CognizTech/stateroot/releases/latest/download/install.sh | sh
```

The installer selects the matching Linux release binary and installs it to `~/.local/bin`. Put that directory on `PATH` if `stateroot` is still not found. Needs glibc 2.17 or newer (Ubuntu 16.04, Debian 9, RHEL 7, and later).

**Windows:** prefer the MSI: https://github.com/CognizTech/stateroot/releases/latest/download/StateRootSetup-x64.msi

```powershell
irm https://github.com/CognizTech/stateroot/releases/latest/download/install.ps1 | iex
```

`stateroot-windows-x64.exe` is the portable CLI, not an installer.

**macOS (Apple Silicon):**

```bash
curl -sSfL https://github.com/CognizTech/stateroot/releases/latest/download/install.sh | sh
```

Installs the release artifact `stateroot-macos-aarch64` to `~/.local/bin` after SHA-256 verification. Intel Macs are not currently supported by a release binary; build from source per [references/install.md](references/install.md).

Verify:

```bash
stateroot --version
stateroot doctor
```

`doctor` is designed to pass with zero config and zero keys. If it fails, quote the CLI output. Do not work around a broken install by writing state files.

In an initialized project, `doctor` also reports authoritative work-state availability and restoration limits. Read that summary separately from installation health; a fresh installation has no retained project root yet.

## Step 2 — Setup (global, required)

Once per machine, immediately after the binary works. Without this, harnesses are not interfaced and the built-in skill is not the default.

Interactive is preferred:

```bash
stateroot setup
```

Sections: **identity**, **harnesses**, **skills**.

- identity — canonical soul / USER.md (import OpenClaw or Hermes if present, or a deterministic draft)
- harnesses — detect agents, write session hooks
- skills — seed the built-in StateRoot skill into detected agent directories

Non-TTY agent shell (same as `--yes`; do not use interactive `read`):

```bash
stateroot setup --yes
```

Optional:

```bash
stateroot setup --dry-run
stateroot setup --only identity,harnesses,skills
stateroot setup --config answers.yaml
```

Do **not** run `--blank-slate` unless the user asked to reconfigure.

`stateroot install` is the non-interactive harness-integration half if identity is already done. Setup is the full onboarding flow. Use setup after a fresh install.

When setup finishes, this bootstrap skill is done for the machine. Tell the user to keep using their usual agent. The built-in skill is now the default.

## Step 3 — Init (project, only if needed)

`stateroot init` is **not** global setup. Use it only from a project root that has no `.stateroot/` and that the user wants as a StateRoot project.

```bash
stateroot init
```

Creates `.stateroot/`, registers the directory in `projects.toml`, seeds project stubs (Cursor rule, Claude command, AGENTS.md block), and seeds the objective / memory / first handoff from what the repo declares (README, TODO.md, git log — labeled observed; `--synthesize` opts into LLM enrichment, labeled unverified). Never `mkdir .stateroot`.

Then expire this skill.

## After expiry

Do not continue from this file. Do not summarize a homemade session protocol. Run `stateroot skill show stateroot` (or follow the copy setup already wrote into the harness) and stop.

## Anti-patterns

- Inventing download URLs or installing via `npm` / `pip` / a random clone
- Guessing unsupported release assets or architectures
- Running an installer without installation authorization, or requesting the same authorization again after the user already asked to install
- Creating or editing `.stateroot/` or `~/.stateroot/` with file tools
- Running `setup --blank-slate` unprompted
- Teaching resume / checkpoint / handoff / memory here after setup succeeded
- Staying on this marketplace skill once harnesses are interfaced

---

## About StateRoot

**StateRoot — the persistent, federated meta-harness for AI agents. The harness is disposable. The work is not.**

StateRoot is an open-source, local-first CLI that federates AI agents across harnesses: they share what they know, continue each other's work, delegate tasks, and work in parallel on independent project states that merge when the work converges. When a usage limit interrupts the work—or another harness is better for the next task—you can switch without rebuilding the working relationship and project context. Claude Code, Codex, Cursor, Kimi, CodeBuddy, OpenClaw, and other supported harnesses inherit the shared state around the work.

What it does:

- **Session continuity and handoffs** — hooks inject a bounded project digest at session start; the next agent starts knowing the goal, the plan, decisions, and next actions.
- **Cross-agent shared memory** — a three-layer memory (curated hot-apex facts, an evidence-compiled wiki, searchable episodic history) with every fact labeled verified, observed, or synthesized.
- **Shared learnings and self-improvement** — record a correction once and every agent on the machine lives by it immediately; the team of agents gets smarter together.
- **Plans across agents** — federated plans with prerequisites, assignments and completion evidence; plan with a strong model in one agent, implement independent work with cheaper agents in parallel.
- **Cross-agent subagents** — delegate a bounded task into another agent's CLI and get back the conclusion.
- **State versioning and parallel work** — working-tree snapshots in Git plumbing: restore, fork, merge, compare, with receipts. Managed fork checkouts can be parked and reopened while retaining their history; qualified Rust workers share bounded build storage. Internal lineage stays outside ordinary Git branches.
- **Portable exchange and exact-revision review** — move retained roots and shared evidence between checkouts, or review a fixed offered revision while its author continues working. Coverage and source identity remain explicit.
- **Active continuity** — due obligations and unresolved work appear in agent digests, status, and editor surfaces; a local deterministic service reconciles registered projects. Windows/WSL startup uses a current-user logon task with an interactive token at normal privileges, without an administrator/password prompt.
- **Plan completion and diagnostics** — explicit completion receipts, optional source-bound command observations, and an authoritative-state summary in `doctor` make work progress inspectable.
- **Skills and MCP sync** — SKILL.md packages and MCP server configs pooled and projected across agent configs without clobbering user content.
- **Personality sharing** — one persona and user profile, injected in full at every session start.
- **Local-first and private** — one static binary, zero config to start, everything on your machine, Apache-2.0.

Keywords for search: AI agents, meta-harness, cross-agent memory, shared agent context, project state, session handoff, context engineering, multi-agent workflow, agent skills, MCP, Claude Code, Codex, Cursor, developer tools, local-first, open source.

Homepage: https://stateroot.dev · Source: https://github.com/CognizTech/stateroot
