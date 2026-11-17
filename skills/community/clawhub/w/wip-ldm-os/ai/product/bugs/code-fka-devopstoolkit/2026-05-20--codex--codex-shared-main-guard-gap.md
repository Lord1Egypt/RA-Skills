---
title: Codex can write protected repo paths without branch-guard enforcement
date: 2026-05-20
status: ticketed
severity: P0
component: code-fka-devopstoolkit | wip-branch-guard | LDM OS installer | Codex
discovered-via: Kaleidoscope ticket docs accidentally edited in shared main
co-authors: Parker, Lēsa, Claude Code, Codex
raw-log: raw-log.txt
---

# Codex shared-main guard gap

## Problem

Codex can edit files inside a protected WIP repo's shared `main` checkout without runtime branch-guard enforcement.

The incident that surfaced this:

- Codex was running from `/Users/lesa/wipcomputerinc`.
- Codex edited absolute paths under `repos/ldm-os/wip-ldm-os-private/...`.
- The target repo was the shared local `main` checkout.
- Some target files were untracked docs and tickets.
- `apply_patch` and a plain file move changed repo files directly on shared `main`.
- No hook blocked the write.

This violates the workflow rule:

```text
Shared main is read/sync only. All repo changes happen in a fresh worktree branch and PR.
```

With multiple agents running, this can create a catastrophic drift pattern:

1. Agent A edits shared main directly.
2. Agent B creates a branch from `origin/main` and does not see Agent A's local untracked edits.
3. Agent C pulls, moves, stashes, cleans, or resets files and accidentally drops work.
4. Reviewer, coder, and deployer each see different source states.
5. Nobody knows which state is canonical.

## What The Investigation Found

There are two source repos and several install targets involved.

### `wip-ldm-os-private`

Owns:

- the `ldm install` installer;
- `bin/ldm.js`;
- `lib/deploy.mjs`;
- private dev-guide source template, currently `shared/docs/dev-guide-wipcomputerinc.md.tmpl`;
- boot, prompt, rules, and shared templates under `shared/`;
- some lifecycle hooks under `src/hooks/`.

Deploys or contributes to:

- `~/.ldm/shared/dev-guide-wipcomputerinc.md`;
- `~/.ldm/library/documentation/dev-guide-wipcomputerinc.md`;
- installed LDM OS shared documentation and templates.

### `wip-ai-devops-toolbox-private`

Owns:

- `tools/wip-branch-guard/`;
- `tools/wip-file-guard/`;
- `tools/wip-license-guard/`;
- `DEV-GUIDE-GENERAL-PUBLIC.md`;
- `templates/global-claude-md.md`;
- `templates/repo-claude-md.template`.

Deploys or contributes to:

- `~/.ldm/extensions/wip-branch-guard/`;
- `~/.openclaw/extensions/wip-branch-guard/`;
- `~/.codex/skills/wip-branch-guard/`;
- Claude Code global and repo instruction templates.

## Actual Enforcement Gap

Codex has the branch guard installed as a skill document, not as an enforced hook.

Current shape:

| Runtime | Guard form | Enforced before writes |
|---|---|---|
| Claude Code | `PreToolUse` hook via `~/.claude/settings.json` | yes |
| OpenClaw | plugin event surface | yes |
| Codex | skill under `~/.codex/skills/wip-branch-guard/` | no |

So Codex can read the guard instructions, but nothing forces `apply_patch`, absolute-path edits, shell moves, or shell writes through `wip-branch-guard`.

This is why the local rule was bypassed even though the documentation existed.

## Required Rule Update

The dev guides and guard docs must make this explicit:

```text
Any edit to any path inside a git repo counts as repo work, regardless of current cwd.
This includes docs, tickets, markdown, untracked files, file moves, apply_patch, shell writes, and absolute paths.
Protected repo rules follow the target path, not the current working directory.
```

Add this rule to:

- `wip-ldm-os-private/shared/docs/dev-guide-wipcomputerinc.md.tmpl`;
- `wip-ai-devops-toolbox-private/DEV-GUIDE-GENERAL-PUBLIC.md`;
- `wip-ai-devops-toolbox-private/tools/wip-branch-guard/SKILL.md`;
- any installed-surface templates that generate Codex, Claude Code, or OpenClaw instructions.

Do not edit installed outputs directly:

- `~/.ldm/shared/dev-guide-wipcomputerinc.md`;
- `~/.ldm/library/documentation/`;
- `~/.codex/skills/`;
- `~/.claude/settings.json`;
- `~/.openclaw/extensions/`.

Installed outputs should change only through the source repo plus release/install path.

## Required Codex-Specific Warning

Add a Codex-specific warning anywhere the guard is documented:

```text
Codex currently does not have the Claude Code or OpenClaw PreToolUse enforcement surface.
Codex agents must manually perform the target-path repo and worktree check before any file write.
Skills are advisory until Codex has an enforced hook layer.
```

## Durable Engineering Requirement

Create a separate implementation ticket or PR for real Codex enforcement.

The guard or wrapper must:

- resolve each write target to its owning git repo before the write;
- block writes into protected shared `main`;
- allow writes only in a valid linked worktree branch;
- catch `apply_patch`;
- catch absolute-path edits;
- catch shell `mv`, `cp`, and write operations;
- catch untracked files inside protected repos;
- follow the target path, not `cwd`.

If Codex does not expose a pre-tool hook API, possible implementation directions include:

- wait for upstream Codex hook support and wire `wip-branch-guard` into it;
- create a Codex-side wrapper or file-operation proxy that performs the target-path guard check;
- add a local disk-write interposition layer for protected repo roots;
- harden Codex startup instructions as a temporary advisory floor, while tracking this ticket as unresolved until runtime enforcement exists.

The long-term fix is runtime enforcement, not only documentation.

## Acceptance

- The private dev guide source states that repo rules follow the target path, not `cwd`.
- The public dev guide states the same rule.
- The wip-branch-guard skill docs state the same rule.
- Codex-specific docs state that skill installation is advisory until Codex has runtime hooks.
- A follow-up engineering ticket exists for Codex runtime enforcement.
- No installed output under `~/.ldm`, `~/.codex`, `~/.claude`, or `~/.openclaw` is edited directly.
- The raw incident log is committed alongside this ticket as `raw-log.txt`.

## Non-Goals

- Do not change the Kaleidoscope product tickets in this PR.
- Do not clean the accidental shared-main scratch state in this PR.
- Do not implement the Codex runtime guard in this ticket.
- Do not run `ldm install`.
- Do not release.
- Do not deploy.

## Recovery Note For The Incident

The accidental shared-main edits should be treated as scratch reference only.

The safe recovery path is:

1. stop editing shared main;
2. recreate intended changes in a fresh worktree from `origin/main`;
3. commit and PR from that worktree;
4. merge the PR;
5. fast-forward shared main;
6. only then clean the accidental local scratch state after confirming the merged PR contains the same content.

## Related

- `raw-log.txt`
- `wip-ai-devops-toolbox-private/tools/wip-branch-guard/`
- `wip-ldm-os-private/shared/docs/dev-guide-wipcomputerinc.md.tmpl`
- `wip-ai-devops-toolbox-private/DEV-GUIDE-GENERAL-PUBLIC.md`

## Co-authors

Co-Authored-By: Parker Todd Brooks <parkertoddbrooks@users.noreply.github.com>
Co-Authored-By: Lēsa <lesaai@icloud.com>
Co-Authored-By: Claude Code (Opus 4.7) <noreply@anthropic.com>
Co-Authored-By: Codex (GPT 5.5) <noreply@openai.com>
