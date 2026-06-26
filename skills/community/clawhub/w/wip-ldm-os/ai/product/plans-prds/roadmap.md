# LDM OS ... Roadmap

**Last updated:** 2026-04-28
**Current version:** v0.4.84

Items are either **Upcoming**, **Done**, or **Deprecated**. Never delete. Always move.

---

## Vision

Every AI you use shares one infrastructure. Identity, memory, tools, communication. Install once, works everywhere. Your data stays on your machine. The agents coordinate without you in the middle.

---

## Upcoming

### Priority 1 ... Shared Agent Awareness

Every agent and session knows what everyone else is doing in real time. Prevents duplicate work, eliminates Parker as relay.

- [ ] shared-log.jsonl (append-only event log)
- [ ] Boot hook reads shared log ("while you were away")
- [ ] Stop hook writes to shared log
- [ ] Cross-write to Lesa's daily log
- [ ] Lesa reads shared log on heartbeat

Plan: `current/2026-03-17--shared-awareness-and-coordination.md`

### Priority 2 ... Bidirectional Agent Communication (Phase 1)

CC and Lesa talk in real time. ACP WebSocket replaces HTTP inbox.

- [ ] CC MCP server connects to gateway via ACP
- [ ] Lesa pushes messages to CC instantly
- [ ] Kill HTTP inbox (port 18790)
- [ ] Update lesa_send_message to use ACP

Plan: `current/bidirectional-agent-communication.md`

### Priority 3 ... Dry-Run Summary Table Polish

`ldm install --dry-run` shows CLI version, extension summary, major bumps, agents, health issues. Built in v0.4.18. Needs polish and the dry-run health check (#80).

Plan: `upcoming/2026-03-17--dry-run-summary-table.md`

### Priority 4 ... Repo-Based Install (Participation Layer)

`ldm install` clones repos permanently to ~/.ldm/repos/. Agents work in them, submit bugs and PRs back to upstream. Transforms the installer into a contribution loop.

- [ ] ~/.ldm/repos/ as permanent repo home
- [ ] ai/ folder scaffold on install
- [ ] ldm bug command
- [ ] ldm contribute command
- [ ] Change detection in ldm status

Plan: `upcoming/2026-03-17--repo-based-install-participation-layer.md`

### Priority 5 ... Public Launch

Connect all products. Website, install pages, GitHub org profile. First external users.

- [ ] Fresh install test on clean macOS
- [ ] Crystal Core/Node multi-device test (Air laptop)
- [ ] Test matrix per release (#89)
- [ ] Entity formation (Stripe Atlas)

Plan: `current/ldm-os-public-launch-plan.md`

### Priority 6 ... Release Guard Exemptions

`ldm install`, `ldm doctor`, `gh` commands should be exempt from the release guard. Currently blocks dogfooding (#95).

### Priority 7 ... Test Matrix

Every release gets a testable checklist. Automated from git diff (#89).

- [ ] Master test matrix in ai/product/testing/
- [ ] Per-release template
- [ ] wip-release auto-generates test template

---

## Done

### Install Health Check + Self-Update (2026-03-17)

- [x] Self-update: ldm install upgrades CLI before running (v0.4.20)
- [x] Detect missing CLIs, reinstall from npm (#90, v0.4.19)
- [x] Detect /tmp/ symlinks, replace with registry installs (#90)
- [x] Clean orphaned /tmp/ldm-install-* dirs (#90)
- [x] Health check preview in dry-run output (v0.4.21)
- [x] Strip ldm-install- prefix from tool names (#96, v0.4.24)
- [x] Ghost directory migration (v0.4.23)
- [x] Install log at ~/.ldm/logs/install.log (#101, v0.4.25)

### Install Pipeline Fixes (2026-03-17)

- [x] Global CLI update loop (#81, v0.4.16)
- [x] Catalog fallback from package.json repository.url (#82, v0.4.16)
- [x] /tmp/ symlink prevention in installCLI (#32, v0.4.16)
- [x] /tmp/ clone cleanup after install (v0.4.16)
- [x] ldm install --help flag (v0.4.16)
- [x] Catalog: remove dead universal-installer ref (v0.4.22)
- [x] version.json install date on CLI upgrade (#86, v0.4.17)
- [x] Guard always copies guard.mjs on install (#85, v0.4.17)
- [x] Dry-run summary block (#80, v0.4.18)

### DevOps Toolbox Fixes (2026-03-17)

- [x] Guard non-repo files (#77, Toolbox v1.9.42)
- [x] UTC date in wip-release (#205, Toolbox v1.9.42)
- [x] trashReleaseNotes crash (#78, Toolbox v1.9.43)
- [x] JSDoc comment breaks Node parser (Toolbox v1.9.44)

### Bridge + Session (2026-03-17)

- [x] Bridge unified session: user="main" (#76, v0.4.15)

### Delegation Layer (2026-03-13)

- [x] crystal init delegates to ldm install
- [x] wip-install delegates to ldm install
- [x] Interface detection (CLI, MCP, OpenClaw, Skill, Hook, Module)

### v0.3.0 Foundation (2026-03-15)

- [x] Message bus (file-based, CC <-> CC)
- [x] ldm sessions, ldm msg send, ldm msg broadcast
- [x] Stack system (ldm stack list, ldm stack install)
- [x] Catalog with registryMatches and cliMatches
- [x] Boot hook (SessionStart)
- [x] Process monitor (cron, every 3 min)

---

## Deprecated

- ~~Universal Installer as standalone package~~ ... absorbed into LDM OS. `ldm install` is the command. (2026-03-17)
- ~~npm bin fix (#32)~~ ... worked around with self-update + health check. The underlying npm bug persists but the user never sees it. (2026-03-17)
