---
title: "WIP Inc design skills should install through LDM OS to all agent surfaces"
status: done
priority: P1
owner: Cody
repo: wip-inc
created: 2026-05-06
---

# WIP Inc Design Skills Install Through LDM OS To All Surfaces

## Problem

WIP now has reusable design guidance skills that ship from a private working repo as public npm packages, starting with:

```text
/Users/lesa/wipcomputerinc/repos/wip-inc-private-only/design/skills/wip-ai-chat-ui
```

The public npm package is:

```text
@wipcomputer/wip-ai-chat-ui
```

These skills live in WIP Inc source, but the ticket belongs in LDM OS bugs because LDM OS / Universal Installer is the install path for all WIP agent skills.

The affected source repo is:

```text
repos/wip-inc-private-only/design/skills/wip-ai-chat-ui
```

The implementation surface is:

```text
repos/ldm-os/wip-ldm-os-private
```

The expected product behavior is that WIP Inc design skills install through LDM OS like the rest of WIP's agent capabilities.

Original failing local dry run:

```bash
ldm install --dry-run /Users/lesa/wipcomputerinc/repos/wip-inc-private-only/design
```

returned:

```text
No installable interfaces detected.
```

That meant the source skill existed, but the Universal Installer did not yet detect or deploy it.

Manual symlinks or manual copies are not acceptable as the product path.

## Product Rule

Use Universal Installer.

Do not create a one-off install script for this skill.
Do not tell users or agents to manually copy or symlink the skill into `~/.codex/skills`.
Do not make this a React component package.
Do not add assistant-ui runtime dependencies.

The install model should be:

```text
private source repo -> public npm package -> ldm install / Universal Installer -> every supported agent skill surface
```

## Expected Behavior

Running:

```bash
ldm install --dry-run @wipcomputer/wip-ai-chat-ui
```

should detect the package-root `SKILL.md` interface and report exactly which skill targets would change.

Running the real install should deploy the skill to all supported local agent surfaces.

At minimum for this machine:

```text
~/.codex/skills/wip-ai-chat-ui
~/.agents/skills/wip-ai-chat-ui
```

If Claude Code/OpenClaw skill paths are still active for compatibility, include them too through the normal Universal Installer harness map.

The authoritative source remains:

```text
repos/wip-inc-private-only/design/skills/wip-ai-chat-ui/
```

## Install Prompt Shape

This should follow the same product pattern as Codex Remote Control.

User-facing prompt should be something like:

```text
Read https://wip.computer/install/wip-ai-chat-ui.txt

Use the install document and live local checks as the source of truth.
Check whether the WIP AI Chat UI skill is installed.
If yes, show me what version or source I have.
If not, explain what the skill does and what it installs.
Then ask whether I want a dry run.

Do not install anything until I say "install".
```

This install prompt should drive Universal Installer against the npm package. It should not be a separate bespoke installer.

## Likely Implementation

Extend Universal Installer / `ldm install` detection to support repos whose primary interface is a `skills/` folder with one or more Codex/OpenClaw/agent skills. For public npm distribution, the `wip-ai-chat-ui` package should expose the skill at package root:

Detection should recognize:

```text
skills/<skill-name>/SKILL.md
skills/<skill-name>/agents/openai.yaml
skills/<skill-name>/references/*
SKILL.md
agents/openai.yaml
references/*
```

Deployment should copy or sync the full skill folder, including `references/` and `agents/`, to the supported harness skill directories.

The dry run should clearly show:

```text
Skill: wip-ai-chat-ui
Source: @wipcomputer/wip-ai-chat-ui
Targets:
- ~/.codex/skills/wip-ai-chat-ui
- ~/.agents/skills/wip-ai-chat-ui
```

## Acceptance

- `ldm install --dry-run /Users/lesa/wipcomputerinc/repos/wip-inc-private-only/design` detects `wip-ai-chat-ui`. Done in PR.
- `ldm install --dry-run @wipcomputer/wip-ai-chat-ui` detects `wip-ai-chat-ui` after the package is published.
- Dry run reports all target harness skill paths without writing files. Done in PR.
- Real install deploys `wip-ai-chat-ui` to all supported local agent skill surfaces. Covered by temp-home regression test in PR.
- Installed skill includes `SKILL.md`, `agents/openai.yaml`, and all `references/`. Covered by temp-home regression test in PR.
- The npm tarball contains `SKILL.md`, `agents/openai.yaml`, and all four referenced docs: `stack.md`, `components.md`, `anti-patterns.md`, and `remote-control.md`.
- The npm tarball excludes `ai/`, `_trash/`, `_sort/`, `.env`, `.worktrees/`, and `node_modules/`.
- Codex can load `wip-ai-chat-ui` after restart.
- The installer does not require manual symlinks. Done in PR.
- The installer does not create a React component library. Done in PR.
- The installer preserves the private source repo as the source of truth. Done in PR.
- The install prompt can explain the skill, show installed state, run dry run, and wait for explicit `install`.

## Implementation

Implemented in PR.

- `lib/detect.mjs` detects `skills/<skill-name>/SKILL.md`.
- `lib/deploy.mjs` deploys full skill folders to detected harness skill paths, including Codex and WIP agent compatibility paths.
- `scripts/test-installer-skill-directory.mjs` covers detection plus temp-home deployment to `.claude`, `.openclaw`, `.codex`, and `.agents`.
- Verified dry run against `repos/wip-inc-private-only/design` reports `wip-ai-chat-ui` and all local skill targets without writing files.

## Non-Goals

- Do not implement Remote Control UI changes in this ticket.
- Do not move the skill source out of `repos/wip-inc-private-only/design/skills/wip-ai-chat-ui`.
- Do not create a separate bespoke installer for WIP design skills.
- Do not make this depend on a paid third-party service.
