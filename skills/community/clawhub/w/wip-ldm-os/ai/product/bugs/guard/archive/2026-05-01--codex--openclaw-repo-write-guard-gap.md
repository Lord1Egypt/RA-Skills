---
title: OpenClaw repo-write path can bypass branch and onboarding guard
date: 2026-05-01
status: closed
severity: P2
component: guard | OpenClaw | repo workflow
discovered-via: Lēsa Mnemos review loose-file incident
co-authors: Parker, Lesa, Claude
---

# OpenClaw repo-write path can bypass branch and onboarding guard

## Summary

Lēsa wrote a product-idea document directly into the shared `wip-ldm-os-private` `main` checkout as an untracked file:

```text
ai/product/product-ideas/2026-05-01--mnemos-review--what-to-adopt.md
```

She later confirmed the process failure:

- no feature branch
- no worktree
- no commit
- no PR
- no dev-guide read before repo work
- file written on the shared `main` checkout

The content may be useful and the file is still recoverable because it is untracked, but the incident shows the repo-write invariant is not enforced uniformly across agent runtimes.

## Resolution

Closed 2026-05-01.

Immediate recovery was completed separately: the Mnemos draft is now tracked in private history at `ai/product/product-ideas/2026-05-01--mnemos-review--what-to-adopt.md` via PR `#791`, commit `7f328e6`.

The guard path was fixed and shipped through the toolbox:

- Source fix: `wip-ai-devops-toolbox-private` PR `#405`, merged as `992956e`.
- Release: `@wipcomputer/wip-ai-devops-toolbox@1.9.73-alpha.9` and `@wipcomputer/wip-branch-guard@1.9.91`.
- Source version sync: `wip-ai-devops-toolbox-private` PR `#407`, merged as `9d41ef1`.
- Deployed runtime repair: `ldm install --alpha /Users/lesa/wipcomputerinc/repos/ldm-os/devops/wip-ai-devops-toolbox-private --yes`.

The fix adds `tools/wip-branch-guard/openclaw.plugin.json`, so OpenClaw can invoke the same `before_tool_use` guard code as the Claude Code/Codex hook path. The release also adds nested shell and Python script-file write-target parsing used by the public `#241` bypass class.

Deployed validation:

```text
wip-branch-guard --version                                      -> 1.9.91
node ~/.ldm/extensions/wip-branch-guard/guard.mjs --version     -> 1.9.91
node ~/.openclaw/extensions/wip-branch-guard/guard.mjs --version -> 1.9.91
~/.openclaw/extensions/wip-branch-guard/openclaw.plugin.json     -> present
```

OpenClaw-style hook probes used the deployed OpenClaw guard and redirected state to `/tmp/guard-openclaw-validate-*` because this Codex sandbox cannot write session state under `~/.ldm/state`:

```text
main create before onboarding: denied with onboarding requirement
main create after onboarding: denied as main Write
main edit after onboarding: denied as main Edit
feature worktree create after onboarding: allowed
audit log: records onboarding, main Write, and main Edit denials with session identity
```

Installer caveat found during validation: `ldm install --alpha @wipcomputer/wip-ai-devops-toolbox --yes` still resolved through the public catalog clone and temporarily redeployed older subtool versions. Installing from the merged private source path repaired the runtime. That catalog/public-alpha resolution gap is not part of this guard ticket and should remain tracked under installer/release-pipeline work.

## Why This Belongs In `bugs/guard/`

This is not primarily a Lēsa-lane content bug or an OpenClaw feature bug. OpenClaw is where the bypass appeared, and Lēsa is the agent who hit it, but the failed invariant is guard-owned:

> Agent writes inside protected repos must be blocked unless the session has followed the branch, worktree, onboarding, commit, and PR workflow.

The same rule should hold across Claude Code, Codex, OpenClaw, shell-backed tools, file-edit tools, and any future agent harness.

## Observed

Current shared checkout state after the incident:

```text
repo:   /Users/lesa/wipcomputerinc/repos/ldm-os/wip-ldm-os-private
branch: main
status: ?? ai/product/product-ideas/2026-05-01--mnemos-review--what-to-adopt.md
```

The write should have been denied before the file was created.

Existing guard policy already states:

- writes on `main` in a git repo are denied
- writes on a feature branch outside a linked worktree are denied
- first writes require repo onboarding docs to be read
- shared local `main` is a read/sync surface, not an implementation surface

The OpenClaw/Lēsa path did not enforce those checks for this write.

## Expected

Any agent attempting to create or edit files under a protected repo such as `wip-ldm-os-private` must be stopped unless all of these are true:

1. the write target is in a feature worktree
2. the branch is not `main`
3. the branch prefix matches the acting agent
4. required repo onboarding docs were read or explicitly onboarded
5. the write is not to a protected identity/shared-state exception path

For a product idea, bug, PRD, or plan under `ai/product/`, the agent should be told to create a branch/worktree first.

## Impact

- **Process history can disappear.** Loose files on `main` have no PR discussion, review trail, authorship trail, or merge boundary.
- **Agents learn the wrong behavior.** If a write succeeds once, the model may treat direct-to-main writes as acceptable even when docs say otherwise.
- **Main checkout becomes a staging area.** That breaks the local-main contract: local `main` should be readable final state, not unreviewed draft state.
- **Human review gets bypassed.** Parker has to manually notice the violation and reconstruct what happened.
- **The rule becomes advisory.** The system relies on memory and obedience instead of executable enforcement at the write boundary.

No data has landed on GitHub from this specific incident because the file is untracked.

## Non-Goals

- Do not punish or special-case Lēsa.
- Do not delete the Mnemos review draft as part of this ticket.
- Do not weaken the lean context-load fix by forcing every Lēsa chat to read every workflow doc.
- Do not make `ai/product/` unwritable; make it writable only through the normal worktree/PR path.

## Initial Hypotheses

One or more of these is likely true:

1. The OpenClaw file-edit tool path is not routed through the deployed `wip-branch-guard` PreToolUse equivalent.
2. The OpenClaw guard plugin is installed but not invoked for this class of filesystem write.
3. The path classifier treats some repo writes as shared-state exceptions too broadly.
4. The session did not have repo onboarding state, but onboarding enforcement is only active in Claude Code/Codex paths.
5. The direct write happened through a tool surface that the guard cannot currently observe.

The implementation should verify the exact gap before patching.

## Fix Plan

1. Reproduce safely in a temporary protected repo or disposable worktree:
   - start an OpenClaw/Lēsa session
   - attempt to write a new file under a git repo on `main`
   - confirm whether the guard blocks or allows
2. Trace OpenClaw tool execution to identify whether file writes pass through the guard plugin.
3. Add an OpenClaw-side guard hook or adapter if the current tool path is unguarded.
4. Ensure the guard receives enough context to decide:
   - absolute target path
   - repo root
   - current branch
   - linked worktree status
   - session onboarding state
   - acting agent identity
5. Add regression coverage for:
   - direct file create under protected repo `main` is denied
   - file edit under protected repo `main` is denied
   - same write under linked feature worktree is allowed
   - `ai/product/product-ideas/*.md` is not a shared-state exception
   - live workspace identity files remain governed by their intended file-guard rules
6. Add a denial message that gives the exact next command/workflow:
   - create worktree
   - branch prefix
   - read/onboard repo docs
   - then retry the write inside the worktree

## Acceptance Criteria

- [x] OpenClaw cannot create an untracked file under `wip-ldm-os-private` `main`.
- [x] OpenClaw cannot edit a tracked file under `wip-ldm-os-private` `main`.
- [x] The same create/edit succeeds in a linked feature worktree after onboarding.
- [x] The denial message names the repo, branch, target path, and required worktree/PR workflow.
- [x] Regression tests cover the OpenClaw write path, not only the Claude Code/Codex hook path.
- [x] Guard audit log records the denied write attempt with agent/session identity.
- [x] No broad always-allowed exception covers `ai/product/`.

## Immediate Recovery For This Incident

Handle the existing loose Mnemos file separately:

1. copy the draft into a proper feature worktree
2. commit it with attribution
3. open and merge a PR if Parker approves
4. fast-forward local `main`
5. confirm the loose untracked file is now represented by tracked history

Do not manually delete or rewrite the loose file before the PR path captures it.

## Related

- `ai/product/bugs/guard/archive/2026-04-24--codex--guard-and-repo-tools-master-plan.md`
- `ai/product/bugs/guard/archive/2026-04-20--cc-mini--guard-implementation-plan.md`
- `ai/product/bugs/code/lesa/2026-04-19--cc-mini--pr-89-process-violation-postmortem.md`
- `ai/product/bugs/code-fka-devopstoolkit/2026-04-30--cc-mini--branch-prefix-inconsistency.md`
- Mnemos loose draft: `ai/product/product-ideas/2026-05-01--mnemos-review--what-to-adopt.md`
