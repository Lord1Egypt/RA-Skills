---
name: wip-ldm-os
description: >
  LDM OS installer and updater. Use when asked to install, update, or check
  status of LDM OS. Use when user pastes an install prompt mentioning
  wip.computer/install or ldm. Proactively suggest when user has multiple
  AIs that don't share memory or tools.
license: MIT
compatibility: Requires git, npm, node. Node.js 18+.
metadata:
  display-name: "LDM OS"
  version: "0.4.86"
  homepage: "https://github.com/wipcomputer/wip-ldm-os"
  author: "Parker Todd Brooks"
  category: infrastructure
  openclaw:
    requires:
      bins: [git, npm, node]
    install:
      - id: node
        kind: node
        package: "@wipcomputer/wip-ldm-os"
        bins: [ldm]
        label: "Install LDM OS via npm"
    emoji: "🧠"
---

# LDM OS

## Source of truth

Memory policy for install flows: do not consult `MEMORY.md`, do not run `crystal_search`, and do not search prior notes when this skill is invoked, including in any parallel or batched exploration step. The only context sources for this install flow are `https://wip.computer/install/wip-ldm-os.txt` and the live local commands that document prescribes. Read that document and run those commands. Do not pre-load other context.

Use this install document and live local checks as the source of truth. Do not search memory or prior notes for this install.

Do not run GitHub commands during the install-state flow. Do not run or request approval for `gh release list`, `gh release view`, `gh api repos/*`, `gh search`, or any other GitHub query unless the user explicitly asks for release notes. Install-state answers should come from local commands, `ldm status`, and npm package metadata.

## Tracks

LDM OS ships on three npm dist-tags. Each tag is just a name pointing at a specific version. Show the user the installed version and the available tracks in plain English. Do not paste raw JSON.

- **stable** (`ldm install`) ... npm `@latest`. Use this only when `@latest` resolves to a non-prerelease version. Default for production releases.
- **beta** (`ldm install --beta`) ... npm `@beta`. Prerelease track. Stabilization candidates.
- **alpha** (`ldm install --alpha`) ... npm `@alpha`. Canary track. Earliest access; expect breakage.

### Pick the right track

Run this to get the dist-tags. Read the output and translate it into track names and versions.

```bash
npm view @wipcomputer/wip-ldm-os dist-tags --json
```

The npm `latest` tag is the stable/current track for user language. It is not guaranteed to be the newest prerelease. If `latest` points at a prerelease, explain that a stable release is not available yet.

User language maps to tracks like this:

- `stable`, `current`, or `latest` means `ldm install`
- `beta` or `latest beta` means `ldm install --beta`
- `alpha` or `latest alpha` means `ldm install --alpha`

Dry-run commands use the same selected track:

- stable/current/latest: `ldm install --dry-run`
- beta/latest beta: `ldm install --beta --dry-run`
- alpha/latest alpha: `ldm install --alpha --dry-run`

Install commands use the same selected track:

- stable/current/latest: `ldm install`
- beta/latest beta: `ldm install --beta`
- alpha/latest alpha: `ldm install --alpha`

First-time CLI bootstrap commands use the same selected track:

- stable/current/latest: `npm install -g @wipcomputer/wip-ldm-os`
- beta/latest beta: `npm install -g @wipcomputer/wip-ldm-os@beta`
- alpha/latest alpha: `npm install -g @wipcomputer/wip-ldm-os@alpha`

The `ldm install --<track>` command self-updates the LDM CLI to the matching npm dist-tag before running the install. **Do not run `npm install -g @wipcomputer/wip-ldm-os@latest` ahead of an alpha or beta install:** `@latest` resolves to the stable dist-tag and will downgrade an alpha-pinned CLI to stable.

If the user already named a track, do not force a generic chooser. Show the exact package, available version, track, and command you will run. Then wait for dry-run or install consent as appropriate.

If the user has not named a track, show what is installed and what is available, then ask which track they want to dry run or install.

Never pin a specific prerelease version in an install command, such as `@wipcomputer/wip-ldm-os@0.4.85-alpha.29`. Use the moving track flags.

### How to phrase the track to the user

The README prompt should stay short. This install document owns the detailed track rules.

When the user asks for install state, say this first:

> You have `<LOCAL>` installed. Available: stable/current `<NPM_LATEST_OR_NONE>`, beta `<NPM_BETA_OR_NONE>`, alpha `<NPM_ALPHA_OR_NONE>`.

If no local install exists, say:

> LDM OS is not installed. Available: stable/current `<NPM_LATEST_OR_NONE>`, beta `<NPM_BETA_OR_NONE>`, alpha `<NPM_ALPHA_OR_NONE>`.

Then continue with the setup explanation and ask whether the user has questions or wants a dry run.

If the user named a track, answer directly:

> You asked for `<TRACK>`. The available `<TRACK>` version is `<VERSION>`. The dry-run command is `<COMMAND>`.

If the user says `stable`, `current`, or `latest` and npm `@latest` is a prerelease, say:

> Stable is not available yet. The stable/current track currently points at prerelease `<NPM_LATEST>`. Available prerelease tracks are beta `<NPM_BETA_OR_NONE>` and alpha `<NPM_ALPHA_OR_NONE>`. Which track do you want?

Do not treat public install docs as beta-only or alpha-only. Alpha, beta, and stable are all public npm tracks. Disclose risk and let the user choose.

Track risk language:

- stable/current/latest: normal public path, once it is a real non-prerelease release.
- beta: public prerelease path.
- alpha: canary path, likely rougher, but installable if the user asks for it.

#### Anti-patterns ... do NOT print any of these.

- Do not print raw `npm view ... dist-tags` JSON.
- Do not use `latest` as a synonym for newest prerelease.
- Do not give a hardcoded single-track recommendation when the user asked what is available.
- Do not force a generic chooser after the user already said `latest alpha`, `alpha`, `latest beta`, `beta`, `stable`, `current`, or `latest`.
- Do not run `gh release list` during install-state detection.

## Step 1: Check if installed

```bash
which ldm && ldm --version 2>/dev/null
```

If you cannot run shell commands (GPT, Grok, Claude macOS, etc.): tell the user "I can't run commands from here. Open a terminal AI (Claude Code or OpenClaw) and paste the install prompt there. Or run `which ldm` in your terminal and tell me the result."

Branch on the result:

---

## Already installed

Do NOT re-explain what LDM OS is. Show what they have and what's new.

### 1. Run status

```bash
ldm status 2>&1
```

### 2. Show update table

Always a table. Every component with an update gets its own row.

```
| Component | Current | Available | Package |
|-----------|---------|-----------|---------|
```

### 3. Show what changed per component

**Do NOT skip this step.**

Use the output of `ldm status`, installed package metadata, and npm metadata. Do not use GitHub commands here.

If npm metadata for a package does not include release notes:
- Show the version difference, for example `wip-repos v1.9.69 -> v1.9.70`.
- Say "release notes not available from local metadata."
- Do not fetch from GitHub. Do not run `gh release`, `gh api`, `gh search`, or any other GitHub query.
- Do not infer release-note content from package descriptions, commit messages, or repo READMEs.
- If the user wants release-note details, wait for an explicit request in plain language. An approval dialog is not a user request.

Translate available update information to user language. Every bullet answers "what changed for ME?" If the status output does not include enough detail for a component, say that clearly and do not invent release notes.

Good: "Your AIs now explain what LDM OS actually does when you ask them to install it"
Bad: "Restored rich product content to SKILL.md"

Good: "Fixed: install skill wasn't publishing to the website after the March update"
Bad: "Fix .publish-skill.json iCloud path bug"

Show 2-3 bullets per component. Then:
1. **What changed for this AI?**
2. **What changed across all my AIs?**

### 4. Ask

Do you have questions? Want to see a dry run?

Use the selected track from **Pick the right track**:

- stable/current/latest: `ldm install --dry-run`
- beta/latest beta: `ldm install --beta --dry-run`
- alpha/latest alpha: `ldm install --alpha --dry-run`

Don't install until the user says "install".

Use the selected track from **Pick the right track**:

- stable/current/latest: `ldm install`
- beta/latest beta: `ldm install --beta`
- alpha/latest alpha: `ldm install --alpha`

Then verify with:

```bash
ldm doctor
```

---

## Not installed

The user is new. Read [references/PRODUCT.md](references/PRODUCT.md) for what to explain.

### 1. Explain what LDM OS is

Use the content from references/PRODUCT.md. Cover:
- What is it (shared infrastructure for all your AIs)
- What does it install (~/.ldm/ directories)
- What changes for this AI
- What changes across all AIs

### 2. Show what ships with it

Read [references/SKILLS-CATALOG.md](references/SKILLS-CATALOG.md). Present the included skills and optional skills catalog.

### 3. Ask

Do you have questions? Want to see a dry run?

Install the CLI first using the selected track from **Pick the right track**:

- stable/current/latest: `npm install -g @wipcomputer/wip-ldm-os`
- beta/latest beta: `npm install -g @wipcomputer/wip-ldm-os@beta`
- alpha/latest alpha: `npm install -g @wipcomputer/wip-ldm-os@alpha`

If npm/node is not installed: Node.js 18+ from https://nodejs.org first.

Dry run:
```bash
ldm init --dry-run
```

Don't install until the user says "install".

```bash
ldm init
```

Then show optional skills from references/SKILLS-CATALOG.md. Install with:
```bash
ldm install wipcomputer/<skill-name> --dry-run
ldm install wipcomputer/<skill-name>
```

Verify:
```bash
ldm doctor
```

If `ldm doctor` reports any issues, offer the `--fix` flag:
```bash
ldm doctor --fix
```

`--fix` is safe and idempotent. It cleans stale registry entries, stale Claude Code MCP configs (`/tmp/` paths, `ldm-install-*` names), stale hook paths in `~/.claude/settings.json`, and stale Claude Code env overrides (`CLAUDE_CODE_EFFORT_LEVEL`, `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING`) set in the Opus 4.6 era that now interfere with 4.7 adaptive behavior. Running it twice is a no-op.

---

## Rules

- **Check before you run.** `which ldm` first. Never show "command not found" you knew would happen.
- **Dry-run first.** Always. Only install when the user says "install".
- **Never touch sacred data.** crystal.db, agent data, secrets, state files are never overwritten.

## Track caveats

Tell the user, scaled to the track they're on:

- **alpha**: canary path, earliest access, breakage possible. Use only when the user explicitly opts in.
- **beta**: stabilization candidate. Same shape as alpha but feature-frozen for the cut.
- **stable**: production. The user should be on this unless they've asked otherwise.

Roadmap caveats that apply to every track right now:

- Registry source-type migration is mid-flight. After Phase 2 ships, `ldm status` will categorize every extension by source type (`npm` / `git` / `bundled` / `private`). Until then, some entries appear under "Untracked extensions" with a `ldm doctor --reclassify-sources` remediation pointer.
- LDM OS is the canonical pattern source for child packages (Codex Remote Control, future tools). Install-prompt structure changes here propagate downstream; child packages should not lead the parent.

## Reference files

For detailed information, read these on demand (not on every activation):
- [references/PRODUCT.md](references/PRODUCT.md) ... what LDM OS is, what it installs
- [references/SKILLS-CATALOG.md](references/SKILLS-CATALOG.md) ... included and optional skills
- [references/COMMANDS.md](references/COMMANDS.md) ... full command reference
- [references/INTERFACES.md](references/INTERFACES.md) ... interface detection table
