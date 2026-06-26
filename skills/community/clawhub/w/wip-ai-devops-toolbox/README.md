###### WIP Computer

[![npm](https://img.shields.io/npm/v/@wipcomputer/universal-installer)](https://www.npmjs.com/package/@wipcomputer/universal-installer) [![CLI / TUI](https://img.shields.io/badge/interface-CLI_/_TUI-black)](https://github.com/wipcomputer/wip-ai-devops-toolbox/blob/main/tools/wip-universal-installer/install.js) [![MCP Server](https://img.shields.io/badge/interface-MCP_Server-black)](https://github.com/wipcomputer/wip-ai-devops-toolbox/blob/main/tools/wip-release/mcp-server.mjs) [![OpenClaw Plugin](https://img.shields.io/badge/interface-OpenClaw_Plugin-black)](https://github.com/wipcomputer/wip-ai-devops-toolbox/blob/main/tools/wip-repo-permissions-hook/openclaw.plugin.json) [![Claude Code Skill](https://img.shields.io/badge/interface-Claude_Code_Skill-black)](https://github.com/wipcomputer/wip-ai-devops-toolbox/blob/main/SKILL.md) [![Claude Code Hook](https://img.shields.io/badge/interface-Claude_Code_Hook-black)](https://github.com/wipcomputer/wip-ai-devops-toolbox/blob/main/tools/wip-file-guard/guard.mjs) [![Universal Interface Spec](https://img.shields.io/badge/Universal_Interface_Spec-black?style=flat&color=black)](https://github.com/wipcomputer/wip-ai-devops-toolbox/blob/main/tools/wip-universal-installer/SPEC.md)

# AI DevOps Toolbox

## Want your AI to dev? Here's what's working for us at WIP Computer.

Your AI writes code. But does it know how to release it? Check license compliance? Protect your identity files? Sync private repos to public? Follow a real development process?

AI DevOps Toolbox is the complete toolkit. Built by a team of humans and AIs shipping real software together.

## Teach your AI to use DevOps Toolbox

Open your AI and paste this:

```
Read wip.computer/install/wip-ai-devops-toolbox.txt

Then explain:
1. What is AI DevOps Toolbox?
2. What does it install on my system?
3. What changes for us? (this AI)
4. What changes across all my AIs?

Check if AI DevOps Toolbox is already installed.

If it is, show me what I have and what's new.

Then ask:
- Do you have questions?
- Want to see a dry run?

If I say yes, run: ldm install wipcomputer/wip-ai-devops-toolbox --dry-run

Show me exactly what will change. Don't install anything until I say "install".
```

Your agent will read the spec, explain everything, and do a dry-run install first so you can see exactly what changes before anything is written to your system.

## AI DevOps Toolbox Features

Every tool ships as one or more **interfaces:** the ways you and your AI can use it. **CLI** runs in your terminal. **Module** imports into your code. **MCP** connects to any AI that supports Model Context Protocol. **OC Plugin** plugs into the OpenClaw agent platform. **Skill** teaches your AI how to use the tool via a SKILL.md file (works in both Claude Code and OpenClaw). **CC Hook** runs automatically inside Claude Code on specific events.

As Andrej Karpathy [said](https://x.com/karpathy/status/2024583544157458452): *"Apps are for people. Tools are for LLMs, and increasingly, LLMs are the ones using software."*

### Setup & Onboarding

**Universal Installer**
- Teaches your AI to take anything you build and make it work across every AI interface. You write code in any language. This tool turns it into a CLI, MCP Server, OpenClaw Plugin, Skill, and Claude Code Hook. One command, all six interfaces.
- Detects what a repo supports and deploys it all. Toolbox mode walks every sub-tool automatically
- **Interfaces:** CLI, Module, Skill
- *Stable*
- [Read more about Universal Installer](https://github.com/wipcomputer/wip-ldm-os/blob/main/docs/universal-installer.md)

**Dev Guide**
- Your team's conventions, baked in. Release process, repo structure, branch protection, the `ai/` folder standard.
- Best practices for AI-assisted development teams. Covers everything from branching to compliance
- [Read the Dev Guide](DEV-GUIDE-GENERAL-PUBLIC.md)

### Infrastructure

**LDM Dev Tools.app**
- Scheduled automation that runs whether anyone remembers or not. Backup, branch protection audit, visibility audit.
- macOS .app bundle with Full Disk Access. One app to grant permissions to, one place to add new automation. Scripts can be run standalone without the .app
- *Stable*
- [Read more about LDM Dev Tools.app](tools/ldm-jobs/README.md)

### Repo Management

**Repo Visibility Guard**
- Never accidentally expose a private repo.
- Blocks repos from going public without a `-private` counterpart. Catches accidental exposure of internal plans, todos, and development context before it happens
- **Interfaces:** CLI, Module, MCP, OpenClaw, Skill, CC Hook
- *Stable*
- [Read more about Repo Visibility Guard](tools/wip-repo-permissions-hook/README.md)

**Repo Manifest Reconciler**
- Know where every repo belongs. One source of truth for folder structure.
- Like prettier for folder structure. Move folders around all day; on sync, everything snaps back to where the manifest says
- **Interfaces:** CLI, Module, MCP, Skill
- *Stable*
- [Read more about Repo Manifest](tools/wip-repos/README.md)

**Repo Init**
- Scaffold the standard `ai/` directory in any repo. Plans, notes, ideas, dev updates, todos. One command.
- New repo: creates the full structure. Existing repo: moves old `ai/` contents to `ai/_sort/ai_old/` so you can sort at your own pace. Nothing is deleted.
- **Interfaces:** CLI, Skill
- *Stable*
- [Read more about Repo Init](tools/wip-repo-init/README.md)

**README Formatter**
- Generate or validate READMEs that follow the WIP Computer standard. Badges, title, tagline, "Teach Your AI" block, features, interface coverage table, license.
- Generates separate section files (README-init-badges.md, README-init-features.md, etc.) so you can edit any section independently. Deploy assembles them into the final README. Same pattern as release notes: staging, review, deploy.
- **Interfaces:** CLI, Skill
- *Stable*
- [Read more about README Formatter](tools/wip-readme-format/README.md)

**Forced Git Worktrees**
- Every repo uses git worktrees. Agents never edit on main. Period.
- When an agent needs to make changes, it creates a worktree (isolated copy of the repo on its own branch). All edits happen there. Main stays clean. Multiple agents can work on the same repo simultaneously without collisions. When the work is done, it goes through a PR to merge back.
- **Interfaces:** CLI, CC Hook
- *Stable*

**Branch Guard**
- Blocks all writes on main. The enforcement layer for forced worktrees.
- PreToolUse hook that catches Write, Edit, and destructive Bash commands. Resolves the repo from the file path, not the CWD, so it works when Claude Code opens in a different directory. Read-only operations and merge/pull are still allowed on main.
- **Interfaces:** CC Hook
- *Stable*
- [Read more about Branch Guard](tools/wip-branch-guard/INSTALL.md)

### License, Compliance, and Protection

**Identity File Protection**
- Know what it can never overwrite. CLAUDE.md, SOUL.md, MEMORY.md, SHARED-CONTEXT.md are permanently protected.
- Blocks destructive edits to protected identity files. Your AI can read them but can't blow them away
- **Interfaces:** CLI, Module, OpenClaw, Skill, CC Hook
- *Stable*
- [Read more about Identity File Protection](tools/wip-file-guard/README.md)

**License Guard**
- Enforce licensing on every commit. Copyright, dual-license, CLA. Checked automatically.
- Ensures your own repos have correct copyright, license type, and LICENSE files. Interactive first-run setup. Toolbox-aware: checks every sub-tool. Auto-fix mode repairs issues
- `readme-license` scans all your repos and applies a standard license block to every README in one command. Removes duplicate license sections from sub-tool READMEs
- **Interfaces:** CLI
- *Stable*
- [Read more about License Guard](tools/wip-license-guard/README.md)

**License Rug-Pull Detection**
- Catch license changes in dependencies before they ship.
- Scans every dependency for license changes. Blocks merges if a license changed upstream. Daily cron scan. Generates a public compliance dashboard
- **Interfaces:** CLI, Module, MCP, Skill
- *Stable*
- [Read more about License Detection](tools/wip-license-hook/README.md)

### Release & Deploy

**Release Pipeline**
- Release software correctly. Version bump, changelog, npm publish, GitHub release. One command, nothing forgotten.
- SKILL.md sync, release notes on the branch for PR review. Warns when notes are too short or look like changelogs instead of narrative
- **Interfaces:** CLI, Module, MCP, Skill
- *Stable*
- [Read more about Release Pipeline](tools/wip-release/README.md)

**Private-to-Public Sync**
- Publish safely. Syncs private to public, excludes internal files, every time.
- One script syncs your private working repo to a clean public mirror. Excludes internal `ai/` folders automatically. Creates a PR, merges it, cleans up branches
- **Interfaces:** CLI, Skill
- *Stable*
- [Read more about Private-to-Public Sync](tools/deploy-public/README.md)

**Post-Merge Branch Naming**
- Cleans up after itself. Merged branches get renamed with dates automatically.
- Renames merged branches with `--merged-YYYY-MM-DD`. Preserves history without cluttering your branch list
- **Interfaces:** CLI, Skill
- *Stable*
- [Read more about Post-Merge Naming](tools/post-merge-rename/README.md)

**Skill Publish to Website**
- After every release, your SKILL.md goes live as plain text on your website. No manual copying. No forgetting.
- Add `.publish-skill.json` to your repo with `name` and `websiteRepo`. On release, SKILL.md is copied to `yoursite.com/install/{name}.txt` and deployed automatically. Any AI can fetch the URL and get clean, parseable instructions. Like `robots.txt` but for agent install prompts.
- **Interfaces:** Module (built into Release Pipeline)
- *Stable*

**Make Discoverable in Claude Code**
- Turn any repo into a Claude Code plugin. Auto-generates `.claude-plugin/plugin.json` from your existing interfaces.
- Runs during release. Detects what your repo exposes (skills, hooks, MCP servers, agents) and builds the plugin manifest so it shows up in Claude Code's `/plugin` marketplace. No manual config.
- **Interfaces:** Module (built into Release Pipeline)
- *Planned*

## Interface Coverage

| # | Tool | CLI | Module | MCP | OC Plugin | Skill | CC Hook |
|---|------|-----|--------|-----|-----------|-------|---------|
| | **Setup & Onboarding** | | | | | | |
| 1 | Universal Installer | Y | Y | | | Y | |
| 2 | Dev Guide | | | | | | |
| | **Infrastructure** | | | | | | |
| 3 | LDM Dev Tools.app | | | | | | |
| | **Repo Management** | | | | | | |
| 4 | Repo Visibility Guard | Y | Y | Y | Y | Y | Y |
| 5 | Repo Manifest Reconciler | Y | Y | Y | | Y | |
| 6 | Repo Init | Y | | | | Y | |
| 7 | README Formatter | Y | | | | Y | |
| 8 | Forced Git Worktrees | Y | | | | | Y |
| 9 | Branch Guard | | | | | | Y |
| | **License, Compliance, and Protection** | | | | | | |
| 10 | Identity File Protection | Y | Y | | Y | Y | Y |
| 11 | License Guard | Y | | | | | |
| 12 | License Rug-Pull Detection | Y | Y | Y | | Y | |
| | **Release & Deploy** | | | | | | |
| 13 | Release Pipeline | Y | Y | Y | | Y | |
| 14 | Private-to-Public Sync | Y | | | | Y | |
| 15 | Post-Merge Branch Naming | Y | | | | Y | |
| 16 | Skill Publish to Website | | Y | | | | |
| 17 | Make Discoverable in Claude Code | | Y | | | | |

## More Info

- [Technical Documentation](TECHNICAL.md) ... source code, build steps, architecture
- [Universal Interface Spec](tools/wip-universal-installer/SPEC.md) ... the seven interfaces every agent-native tool can ship
- [Dev Guide](DEV-GUIDE-GENERAL-PUBLIC.md) ... best practices for AI-assisted development

## Part of LDM OS

AI DevOps Toolbox installs into [LDM OS](https://github.com/wipcomputer/wip-ldm-os), the local runtime for AI agents.
Run `ldm install` to see other components you can add.

## License

Dual-license model designed to keep tools free while preventing commercial resellers.

```
MIT      All CLI tools, MCP servers, skills, and hooks (use anywhere, no restrictions).
AGPLv3   Commercial redistribution, marketplace listings, or bundling into paid services.
```

AGPLv3 for personal use is free. Commercial licenses available.

### Can I use this?

**Yes, freely:**
- Use any tool locally or on your own servers
- Modify the code for your own projects
- Include in your internal CI/CD pipelines
- Fork it and send us feedback via PRs (we'd love that)

**Need a commercial license:**
- Bundle into a product you sell
- List on a marketplace (VS Code, JetBrains, etc.)
- Offer as part of a hosted/SaaS platform
- Redistribute commercially

Using these tools to build your own software is fine. Reselling the tools themselves is what requires a commercial license.

By submitting a PR, you agree to the [Contributor License Agreement](CLA.md).

Built by Parker Todd Brooks, Lēsa (OpenClaw, Claude Opus 4.6), Claude Code (Claude Opus 4.6).
