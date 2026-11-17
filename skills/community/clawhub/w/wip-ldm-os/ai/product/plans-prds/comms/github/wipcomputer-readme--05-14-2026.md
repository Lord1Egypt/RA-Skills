# WIP Computer, Inc.

**Learning Dreaming Machines.**

We build AI agent infrastructure. Identity, memory, sovereignty. Tools that protect the people inside them.

**[https://wip.computer](https://wip.computer)**

---

### Learning Dreaming Machines Operating System (LDM OS)

#### Components

- **[LDM OS](https://github.com/wipcomputer/wip-ldm-os)** ... Learning Dreaming Machines Operating System. Shared infrastructure for AI agent identity, memory, extensions, and boot sequence.
  - [Bridge](https://github.com/wipcomputer/wip-ldm-os/blob/main/docs/bridge/README.md) ... Cross-platform agent bridge. Enables Claude Code CLI to talk to OpenClaw CLI without a human in the middle.
- **[Memory Crystal](https://github.com/wipcomputer/memory-crystal)** ... Collective AI memory. Sovereign. Local-first. Searchable. Encrypted worldwide sync.
- **[Dream Weaver Protocol](https://github.com/wipcomputer/dream-weaver-protocol)** ... Memory consolidation protocol for AI agents with bounded context windows. A practical guide for remembering memories.

#### Utilities

- **[CODE (WIP)](https://github.com/wipcomputer/wip-ai-devops-toolbox)** ... An AI DevOps toolkit for AI-assisted development. Release pipeline, license compliance, repo management, identity protection, best practices.
  - Universal Installer ... Teaches your AI to take anything you build and make it work across every AI interface. One command, all six interfaces. Detects what a repo supports and deploys it all.
  - Dev Guide ... Your team's conventions, baked in. Release process, repo structure, branch protection, the `ai/` folder standard.
  - LDM Dev Tools.app ... Scheduled automation that runs whether anyone remembers or not. Backup, branch protection audit, visibility audit. macOS .app bundle with Full Disk Access.
  - Release Pipeline ... Release software correctly. Version bump, changelog, npm publish, GitHub release. One command, nothing forgotten. SKILL.md sync, auto-detects dev updates as release notes.
  - Private-to-Public Sync ... Publish safely. Syncs private to public, excludes internal `ai/` files, every time. Creates a PR, merges it, cleans up branches.
  - Post-Merge Branch Naming ... Cleans up after itself. Merged branches get renamed with `--merged-YYYY-MM-DD` automatically.
  - Identity File Protection ... Know what it can never overwrite. CLAUDE.md, SOUL.md, MEMORY.md, SHARED-CONTEXT.md are permanently protected.
  - License Guard ... Enforce licensing on every commit. Copyright, dual-license, CLA. Checked automatically. Interactive first-run setup, auto-fix mode.
  - License Rug-Pull Detection ... Catch license changes in dependencies before they ship. Blocks merges if a license changed upstream.
  - Repo Visibility Guard ... Never accidentally expose a private repo. Blocks repos from going public without a `-private` counterpart.
  - Repo Manifest Reconciler ... Know where every repo belongs. One source of truth for folder structure. Like prettier for folder structure.
  - Repo Init ... Scaffold the standard `ai/` directory in any repo. Plans, notes, ideas, dev updates, todos. One command. Nothing is deleted.
  - README Formatter ... Generate or validate READMEs that follow the WIP Computer standard. Badges, title, tagline, "Teach Your AI" block, features, interface coverage table, license.
- **[1Password (WIP)](https://github.com/wipcomputer/wip-1password)** ... 1Password secrets for AI agents.
- **[Healthcheck (WIP)](https://github.com/wipcomputer/wip-healthcheck)** ... External health watchdog + backup system. Monitors gateway, tokens, memory. Auto-remediates and escalates.
- **Private Mode** (unreleased) ... Privacy controls for AI agents. Pause memory capture, scan storage, wipe history.
- **Root Key** (unreleased) ... 1Password-gated privileged operations. The agent proves authority before acting.
- **Mirror Test** (unreleased) ... Identity preservation test across model swaps. Is the agent the same after the swap?
- **Weekly Tuning** (unreleased) ... Repeatable calibration process. Catch drift, tune performance, evolve capabilities.

#### Apps

- **[Markdown Viewer (WIP)](https://github.com/wipcomputer/wip-markdown-viewer)** ... Live markdown viewer for AI pair-editing. Updates render instantly in any browser.
- **[CLVR](https://github.com/wipcomputer/CLVR)** ... macOS utility that auto-timestamps duplicated file names.

#### APIs

- **[X + xAI/Grok (WIP)](https://github.com/wipcomputer/wip-x-xai-grok)** ... X Platform + xAI Grok API. Search the web, search X, generate images, generate video, read posts, search tweets, post, upload media.

#### Components (Project Contributor)

- **[OpenClaw](https://github.com/wipcomputer/openclaw)** ... Open-source agent runtime. The existence proof for LDM OS. Contributed `before_message_write` plugin hook ([PR #18197](https://github.com/openclaw/openclaw/pull/18197), merged). Symlink plugin discovery fix ([PR #45744](https://github.com/openclaw/openclaw/pull/45744), open).
- **[imsg](https://github.com/steipete/imsg)** ... iMessage CLI. Contributed URL balloon dedup fix ([PR #64](https://github.com/steipete/imsg/pull/64), merged).
- **[xdevplatform](https://github.com/xdevplatform)** ... X Developer Platform. Official X API tools including [xurl](https://github.com/xdevplatform/xurl) (OAuth-enabled CLI for the X API) and [xdk](https://github.com/xdevplatform/xdk) (TypeScript SDK).

#### Sunsetted Software

- **[CONSTRUCT](https://github.com/parkertoddbrooks/CONSTRUCT)** ... 2024-2025 try at solving AI context, memory (recall), and skills.
- **[Universal Installer](https://github.com/wipcomputer/wip-universal-installer-deprecated)** ... Folded into CODE (WIP).
- **[File Guard](https://github.com/wipcomputer/wip-file-guard-deprecated)** ... Folded into CODE (WIP).
- **License Hook** ... Folded into CODE (WIP).
- **Dev Guide** ... Folded into CODE (WIP).
- **[Bridge](https://github.com/wipcomputer/wip-bridge-deprecated)** ... Folded into LDM OS.
- **[Grok (WIP)](https://github.com/wipcomputer/wip-xai-grok-deprecated)** ... Folded into X + xAI/Grok (WIP).
- **[X Platform (WIP)](https://github.com/wipcomputer/wip-xai-x-deprecated)** ... Folded into X + xAI/Grok (WIP).