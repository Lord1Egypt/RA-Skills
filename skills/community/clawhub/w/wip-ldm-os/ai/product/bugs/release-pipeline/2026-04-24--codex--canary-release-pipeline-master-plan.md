# Canary Release Pipeline Master Plan

Date: 2026-04-24
Author: Codex
Status: Planned
Severity: Critical
Area: release-pipeline
Primary repo for tracking: wip-ldm-os-private
Implementation repos: wip-ldm-os-private, wip-ai-devops-toolbox-private, wipcomputer/.github, and every repo enrolled in the WIP release system

## Purpose

This is the durable master plan for the LDM OS release pipeline. It consolidates the four open release-pipeline bugs, the archived release-pipeline bugs, and the 2026-04-24 CI review into one step-by-step plan.

All bug and planning records for this work live in the LDM OS bug tree:

```text
ai/product/bugs/release-pipeline/
```

Implementation may happen in other repos, especially the DevOps Toolbox and shared GitHub workflow repo, but the plan and the child bug trail stay here so the full history can be reviewed years later.

## Reviewed Inputs

Open release-pipeline bugs reviewed:

- `2026-04-05--cc-mini--release-pipeline-master-plan.md`
- `2026-04-06--cc-mini--shared-universal-config-layer.md`
- `2026-04-08--cc-mini--silent-skip-without-license-guard-config.md`
- `2026-04-17--cc-mini--release-pipeline-hardening-and-ci.md`
- `2026-04-24--codex--prerelease-installs-vs-stable-dogfood.md`

Archived release-pipeline bugs reviewed:

- `archive/2026-03-27--cc-mini--version-mismatch-deploy-gap.md`
- `archive/2026-03-30--cc-mini--installer-skips-bridge-deploy.md`
- `archive/2026-03-31--cc-mini--installer-dependency-resolution.md`
- `archive/2026-03-31--cc-mini--installer-deploy-order.md`

Current-state review performed on 2026-04-24:

- LDM OS private repo has a thin top-level GitHub Actions CI workflow.
- `wipcomputer/.github` does not yet contain reusable WIP CI workflows.
- The local repo manifest is stale: 73 manifest entries, 181 repos on disk, 45 matched, 136 on disk but not in manifest, and 28 in manifest but not on disk.
- `wip-release` already appears to contain some fixes from older plans, including mandatory license guard checks, sub-tool version validation, tag and dist-tag collision checks, and deploy-public hooks for some flows.
- `wip-release check` was not found in the current DevOps Toolbox CLI surface.
- The canary install loop, release artifact verification, shared workflow rollout, manifest-driven repo enrollment, and rollback/promotion record are still missing.

## Root Thesis

The missing link is not one command. It is release confidence across three boundaries:

1. Before merge: PR checks must fail broken changes before they enter private main.
2. After merge: alpha release output must be installed and validated as an artifact, not trusted because source tests passed.
3. Before public or stable promotion: the system must prove that the public install path works and that rollback is available.

The prerequisite is a trustworthy repo inventory. Shared CI cannot be rolled out safely when the manifest does not match the repos that actually exist.

## Operating Principles

- Fail before merge whenever possible.
- Validate built and published artifacts, not only source files.
- Keep source of truth in repos. Local runtime copies under home directories are install products, not truth.
- Centralize CI logic in shared workflow templates. Individual repos should have tiny shims and manifest metadata.
- Keep LDM OS and the DevOps Toolbox separate packages, but make the release experience feel like one system.
- Treat alpha, beta, stable, private mirror, public mirror, npm, and local install as distinct states with explicit handoffs.
- Install-track ownership is explicit: agents and CI validate alpha and beta tracks; Parker dogfoods stable/latest through the install prompt unless he explicitly asks an agent to install.
- Protected main is a hard release constraint. Any release flow that mutates version files, changelogs, or SKILL.md must land those mutations through a release branch and PR.
- Every phase needs acceptance criteria that can be rechecked later.
- Do not archive the old active bugs until their requirements are mapped, implemented, and linked back to this plan.

## MVP Path

The full plan is intentionally broad, but the first shipped milestone must be smaller:

| Priority | Phase | Owner | MVP reason |
| --- | --- | --- | --- |
| MVP | Phase 0: Repo Inventory and Enrollment | Codex, reviewed by Lēsa | Shared CI needs a trustworthy repo list. |
| MVP | Phase 2: `wip-release check` | Codex with DevOps Toolbox implementation | PRs need a single pre-merge release gate. |
| MVP | Phase 3: Installer and Runtime Smoke Harness | Codex | Historical installer failures need regression coverage before canary can be trusted. |
| MVP | Phase 5: Alpha Release Automation | Codex, reviewed by Lēsa | Alpha artifacts need durable release records. |
| MVP | Phase 6: Canary Artifact Validation | Codex and CI; Lēsa reviews results | The published artifact must install cleanly before promotion. |
| Post-MVP | Phase 1: Audit Existing Release Fixes | Codex | Audit runs in parallel where possible, but does not block first canary loop unless it finds a release blocker. |
| Post-MVP | Phase 4: Shared GitHub Workflow Library | Codex | Centralization follows after the first two repos prove the shape. |
| Post-MVP | Phase 7: Promotion, Rollback, and Known-Bad Releases | Codex with Lēsa approval | Needed before stable automation, but not before the first alpha canary. |
| Post-MVP | Phase 8: Private/Public Mirror Policy | Codex | Needed before stable/public promotion. |
| Post-MVP | Phase 9: Shared Rules, Docs, and Universal Config | Codex | Continues in parallel with rule/doc child bugs. |
| Post-MVP | Phase 10: Branch Hygiene and Worktree Cleanup | Codex | Operational cleanup after critical gates exist. |
| Post-MVP | Phase 11: Rollout Order | Codex | Broad rollout waits for the MVP loop. |
| Post-MVP | Phase 12: Tracking Model | Codex | Ongoing governance for the child bug tree. |

## Current State

Several important fixes from the earlier plans are partially or mostly present in the current DevOps Toolbox code. They should be audited and tested rather than blindly reimplemented:

- `wip-release` has worktree and branch safety helpers.
- `wip-release` has sub-tool version validation.
- `wip-release` has checks for existing npm versions, tags, and prerelease dist-tags.
- `wip-release` requires `.license-guard.json` in stable, prerelease, and hotfix flows.
- `wip-release` checks for `CLA.md` and `.npmignore` in release flows.
- `wip-release` integrates deploy-public for stable and some prerelease flows.
- Current alpha behavior appears to intentionally skip deploy-public because alpha is treated as private dev-only.

The remaining gap is the system around those fixes:

- No manifest-clean rollout target.
- No shared CI workflow library.
- No `wip-release check` command for PRs.
- No clean-home canary install job after alpha publish.
- No durable release record with source commit, package version, npm integrity, public mirror SHA, canary result, and rollback pointer.
- No enforced promotion gate from alpha to beta or stable.
- No release-state dashboard or machine-readable status file.

## Existing Tooling Inventory

Do not reinvent these. Phase 1 should audit and wire them into the pipeline where appropriate:

| Tooling | Exists today | Use in this plan |
| --- | --- | --- |
| `wip-repos check` | CLI and MCP-style repo inventory check already exist. | Phase 0 should improve signal and manifest classification, not invent a new checker. |
| `wip-repos compliance` | Compliance checks and fix mode exist for repo scaffold files. | Phase 0 and Phase 2 should reuse this for missing license, CLA, and npmignore checks. |
| `wip-release` | Release CLI exists and already mutates version, changelog, and release docs. | Phase 5 must wrap it in a protected-main-compatible release branch or release PR flow. |
| `mcp__wip-release__release` | MCP release surface exists. | Phase 5 should decide whether GitHub Actions calls the CLI, MCP surface, or a shared library behind both. |
| `mcp__wip-release__release_status` | MCP release-status surface exists. | Phase 5 and Phase 7 should use or extend this for release records and visible state. |
| `wip-license-guard` | License compliance guard exists. | Phase 1 and Phase 2 should reuse it for file-level and package metadata checks. |
| `wip-license-hook` | License rug-pull and ledger tooling exists. | Phase 1 and Phase 2 should reuse it for dependency/license drift gates. |
| `wip-repo-init` | Repo scaffold tool exists. | Phase 2 should fail with a clear instruction to run or repair scaffold output. |

## Phase 0: Repo Inventory and Enrollment

Goal: establish the complete set of repos that the release pipeline owns.

This phase starts from the existing `wip-repos check` tooling. The work is to make its output actionable for release enrollment and CI rollout, not to create a separate inventory system.

Steps:

- [ ] Reconcile `repos-manifest.json` against the actual repos on disk.
- [ ] Classify each repo as canonical, archived, deprecated, generated, worktree, third-party, runtime clone, or unowned.
- [ ] Decide which repos are enrolled in WIP CI and which are deliberately excluded.
- [ ] Add or extend manifest metadata for release behavior:
  - package manager
  - build command
  - test command
  - lint command
  - release type
  - npm package name, if any
  - private repo name
  - public mirror repo name, if any
  - install smoke profile
  - docs sync profile
  - required secrets
- [ ] Add a manifest check that fails if a repo appears on disk but is not classified.
- [ ] Add an allowlist for intentionally unmanaged directories.
- [ ] Create a child bug in this folder for manifest reconciliation.

Acceptance criteria:

- [ ] `wip-repos check` has zero unexplained mismatches.
- [ ] Every release-owned repo has an explicit CI profile.
- [ ] Every excluded repo has an explicit reason.
- [ ] Future CI rollout uses manifest metadata instead of guesses.

## Phase 1: Audit Existing Release Fixes

Goal: preserve and prove the fixes that already exist.

Use existing tools first: `wip-release`, `wip-repos compliance`, `wip-license-guard`, and `wip-license-hook`. Add new release-pipeline code only where existing tools do not cover the requirement or cannot fail closed in CI.

Steps:

- [ ] Audit `wip-release` worktree and main-branch checks against the 2026-04-05 plan.
- [ ] Audit stale tag, npm version, dist-tag, and release conflict handling.
- [ ] Audit sub-tool version drift behavior and confirm drift is an error unless explicitly overridden.
- [ ] Audit sub-tool publish behavior and confirm failures are surfaced.
- [ ] Audit `.license-guard.json`, `CLA.md`, `.npmignore`, and README template gates against the 2026-04-08 bug.
- [ ] Audit deploy-public behavior for stable, beta, hotfix, and alpha.
- [ ] Add regression tests for each audited behavior.
- [ ] Mark each old requirement as implemented, still open, or superseded.

Acceptance criteria:

- [ ] Every 2026-04-05 requirement has a code test or a documented open child bug.
- [ ] Every 2026-04-08 requirement has a code test or a documented open child bug.
- [ ] Current alpha public-mirror behavior is documented and intentional.

## Phase 2: `wip-release check`

Goal: create the command that PR CI runs before merge.

Recommended command:

```sh
wip-release check
```

The command should be safe to run in pull requests and should avoid publishing, tagging, pushing, or mutating release state.

Checks:

- [ ] Verify repo is classified in the manifest.
- [ ] Verify release profile exists for the repo.
- [ ] Verify required files exist:
  - `.license-guard.json`
  - `CLA.md`
  - `.npmignore` when package publishing is possible
  - README or repo-specific README template output
  - changelog or release notes, when required by repo profile
- [ ] Verify package version has not already been published to npm.
- [ ] Verify release bump and changelog state are coherent.
- [ ] Verify license headers and license metadata.
- [ ] Verify sub-tool versions are aligned.
- [ ] Verify package scripts referenced by the profile exist.
- [ ] Run build, test, lint, and typecheck according to repo profile.
- [ ] Run `npm pack --dry-run` or equivalent package dry-run where applicable.
- [ ] Run installer dry-run or repo-specific smoke checks where applicable.
- [ ] Verify docs and shared rule sync status.
- [ ] Verify no protected private paths or `ai/` content would be published to public packages or mirrors.
- [ ] Emit machine-readable JSON for GitHub Actions annotations.

Acceptance criteria:

- [ ] PR CI can call one command per repo.
- [ ] The command fails closed when required config is missing.
- [ ] The command can run locally and in GitHub Actions.
- [ ] Network-dependent checks are explicit and do not silently skip.

## Phase 3: Installer and Runtime Smoke Harness

Goal: test the installer like a user would experience it.

This phase absorbs the archived installer bugs.

Steps:

- [ ] Build a clean-home test harness for LDM OS.
- [ ] Use an isolated temporary `HOME`.
- [ ] Install into an isolated `.ldm` directory.
- [ ] Verify bridge deployment from npm package output, not just source tree output.
- [ ] Verify installer self-update deploys bridge files.
- [ ] Verify local `file:` dependencies are resolved after package installation, not before package manager install clobbers symlinks.
- [ ] Verify install order is `npm install`, then local dependency resolution, then build.
- [ ] Verify tool config and permission surfaces are installed.
- [ ] Verify skill frontmatter is valid before deployment.
- [ ] Verify shared rules and docs sync are installed.
- [ ] Add fixture tests for malformed `SKILL.md` frontmatter.
- [ ] Add fixture tests for local sibling dependency resolution.
- [ ] Add fixture tests for bridge deploy paths.
- [ ] Add fixture tests for actual build output, not only dry-run output.

Acceptance criteria:

- [ ] The historical bridge deploy bug is covered by a regression test.
- [ ] The historical dependency resolution bug is covered by a regression test.
- [ ] The historical deploy order bug is covered by a regression test.
- [ ] A dry-run pass is no longer enough to claim installer health.

## Phase 4: Shared GitHub Workflow Library

Goal: centralize release CI so repo shims stay small.

Implementation location:

```text
wipcomputer/.github/.github/workflows/
```

Reusable workflows:

- [ ] `wip-ci.yml`: PR and push validation for enrolled repos.
- [ ] `wip-release-alpha.yml`: private main to alpha release flow.
- [ ] `wip-canary.yml`: install and runtime validation after alpha publish.
- [ ] `wip-promote.yml`: beta and stable promotion gate.
- [ ] `wip-public-sync.yml`: private-to-public mirror validation.
- [ ] `wip-branch-hygiene.yml`: merged branch rename and stale branch reporting.
- [ ] `wip-manifest-watchdog.yml`: manifest drift detection.

Repo shim requirements:

- [ ] Each repo has a small workflow file that calls the shared workflow.
- [ ] Repo-specific behavior comes from manifest metadata or a tiny config file.
- [ ] Shared workflows emit GitHub summaries and machine-readable artifacts.
- [ ] Shared workflows do not require copy-pasting release logic into every repo.

Acceptance criteria:

- [ ] LDM OS and DevOps Toolbox both use the shared workflow.
- [ ] A new repo can enroll by adding manifest metadata plus a small workflow shim.
- [ ] Workflow changes can be reviewed in one place.

## Phase 5: Alpha Release Automation

Goal: private main produces an alpha artifact that can be tested automatically.

Hard constraint: protected main cannot be mutated directly by release automation. Because `wip-release` mutates version files, changelogs, and SKILL.md, automated release must run from a canonical release branch or release-PR worktree and land through PR before main is considered released.

Steps:

- [ ] Define the canonical release branch or release-PR worktree pattern.
- [ ] Ensure alpha release cannot run from an arbitrary feature worktree unless explicitly configured for a dry run.
- [ ] Ensure release mutations land through PR before release state is marked complete.
- [ ] Publish the alpha npm artifact.
- [ ] Create a durable release record with:
  - repo
  - package name
  - version
  - dist-tag
  - source commit
  - release commit
  - npm tarball integrity
  - GitHub run ID
  - public mirror SHA, if applicable
  - canary result
  - rollback pointer
- [ ] Store the release record as a workflow artifact and in a repo-visible release ledger.
- [ ] Prevent a second release from starting while the first one is unresolved.
- [ ] Mark release as `published-unvalidated` until canary passes.

Acceptance criteria:

- [ ] Every alpha has a durable release record.
- [ ] Alpha release state is visible without reading raw CI logs.
- [ ] Failed alpha publish cannot masquerade as a successful release.

## Phase 6: Canary Artifact Validation

Goal: prove the thing users install actually works.

The canary must install from the published artifact path, not from the local source checkout.

Validation has two modes:

- Local/manual validation: agents may run alpha and beta installs while actively debugging or validating a prerelease.
- Automated CI validation: the normal gate should be a clean-home GitHub Actions canary that installs the published alpha or beta artifact without relying on an agent's machine.

The long-term goal is that most alpha and beta validation happens in CI. Manual agent installs remain useful for debugging and targeted verification, but they are not the release confidence boundary.

Runner policy:

- MVP canary may be on-demand or nightly to control macOS runner cost.
- Promotion canary must run before beta or stable promotion.
- After cost and runtime are understood, decide whether every alpha triggers canary automatically.
- Stable/latest dogfooding remains Parker-owned through the install prompt even when alpha and beta canaries are automated.

Steps:

- [ ] Start from a clean macOS GitHub-hosted runner.
- [ ] Use a temporary `HOME`.
- [ ] Install the just-published alpha package.
- [ ] Run `ldm install --alpha --yes` or the current alpha install equivalent.
- [ ] Add the equivalent beta canary path with `ldm install --beta --yes` or the current beta install equivalent.
- [ ] Verify the installer does not depend on stale public repos for alpha-only artifacts.
- [ ] Run `ldm doctor --json` or add it if missing.
- [ ] Verify required skills are installed and parse cleanly.
- [ ] Verify shared rules are installed.
- [ ] Verify prerelease install ownership rules are installed from `2026-04-24--codex--prerelease-installs-vs-stable-dogfood.md`.
- [ ] Verify bridge files exist and load.
- [ ] Verify DevOps Toolbox commands are available.
- [ ] Run a minimal command smoke test for each core installed tool.
- [ ] Save logs, installed file inventory, doctor output, package versions, and release record.
- [ ] Mark the release record `canary-passed` or `canary-failed`.

Acceptance criteria:

- [ ] A release cannot be promoted unless canary passed.
- [ ] Canary failure produces actionable logs.
- [ ] Canary verifies npm package output and installer behavior together.
- [ ] Manual agent alpha and beta installs are documented as debugging and validation work.
- [ ] Automated clean-home alpha and beta canaries are the normal promotion gate.

## Phase 7: Promotion, Rollback, and Known-Bad Releases

Goal: make release recovery explicit.

Stable promotion requires two different kinds of confidence: automated artifact confidence from alpha/beta canary, and Parker's stable/latest dogfood through the install prompt unless he explicitly delegates the install.

Steps:

- [ ] Define promotion states:
  - `candidate`
  - `alpha-published`
  - `alpha-canary-passed`
  - `beta-published`
  - `public-sync-passed`
  - `stable-published`
  - `stable-canary-passed`
  - `known-bad`
  - `rolled-back`
- [ ] Implement or finish `wip-release --rollback`.
- [ ] Maintain a last-known-good record per package.
- [ ] On rollback, move npm dist-tags back to last-known-good.
- [ ] Deprecate or mark known-bad npm versions where appropriate.
- [ ] Mark GitHub releases as bad or superseded where applicable.
- [ ] Revert or repair public mirror state through PRs, not untracked local edits.
- [ ] Add installer awareness of known-bad versions if users could otherwise install them.
- [ ] Add a command to show current release health.
- [ ] Require Parker dogfood signoff before stable/latest is treated as owner-accepted.

Acceptance criteria:

- [ ] There is a documented path from failed canary to rollback.
- [ ] Last-known-good can be found without searching Slack, memory, or shell history.
- [ ] Installer can avoid known-bad release paths.

## Phase 8: Private/Public Mirror Policy

Goal: resolve the historical version mismatch and deploy-public gap.

Policy recommendation:

- Alpha is private dev-only and should not require public mirror sync.
- Beta and stable must validate public mirror sync.
- If alpha install currently depends on public repos, fix the installer or package layout so alpha installs from the alpha artifact path.
- Public mirrors must never contain `ai/`, private planning files, secrets, or private-only implementation notes.

Steps:

- [ ] Document alpha, beta, stable, hotfix, and public mirror behavior.
- [ ] Verify `deploy-public` fails loudly on sub-tool publish errors.
- [ ] Verify public mirror package versions match the release being promoted.
- [ ] Add a public install smoke test before stable.
- [ ] Add a check that public mirror content excludes private paths.
- [ ] Add a check that the npm package excludes private paths.
- [ ] Add a release ledger field for public mirror SHA.

Acceptance criteria:

- [ ] The archived version mismatch bug cannot recur silently.
- [ ] Public release promotion proves that public install paths work.
- [ ] Alpha remains fast without depending on stale public mirrors.

## Phase 9: Shared Rules, Docs, and Universal Config

Goal: make every agent and harness learn the same workflow from the same source.

This phase absorbs the shared universal config layer bug.

It also tracks `2026-04-24--codex--prerelease-installs-vs-stable-dogfood.md`, which distinguishes alpha/beta agent validation from stable/latest owner dogfooding.

Steps:

- [ ] Create or finalize repo-owned shared config under `shared/`.
- [ ] Install shared config to `~/.ldm/shared/`.
- [ ] Generate harness-specific adapters for Claude, OpenClaw, Codex, and future harnesses.
- [ ] Add `how-we-work.md` covering:
  - worktrees
  - PRs
  - private main
  - alpha dogfood
  - beta
  - stable
  - public mirror
  - installer verification
  - rollback
- [ ] Add `ldm docs sync`.
- [ ] Add `ldm docs status`.
- [ ] Make doctor report docs and shared-rule drift.
- [ ] Add CI checks that workflow changes update shared rules and docs.

Acceptance criteria:

- [ ] The release workflow is taught by installed shared rules, not only hidden in a bug file.
- [ ] Agents can recover the process after context loss by reading installed rules.
- [ ] Docs drift is visible in CI and doctor output.

## Phase 10: Branch Hygiene and Worktree Cleanup

Goal: keep release history understandable.

Steps:

- [ ] Add merged branch rename automation.
- [ ] Use the established `--merged-YYYY-MM-DD` suffix convention.
- [ ] Add stale branch reporting.
- [ ] Add stale worktree reporting.
- [ ] Ensure release branches and release PRs are easy to distinguish from feature branches.
- [ ] Add branch hygiene output to release health summaries.

Acceptance criteria:

- [ ] Merged release branches are preserved but clearly marked.
- [ ] Stale release worktrees do not hide old state.
- [ ] Release history remains auditable.

## Phase 11: Rollout Order

Goal: enroll repos without breaking everything at once.

Order:

1. LDM OS private repo.
2. DevOps Toolbox private repo.
3. Shared `.github` workflow repo.
4. Memory Crystal.
5. Bridge and installer-adjacent repos.
6. 1Password and other local runtime integrations.
7. API client repos.
8. App repos with deployment workflows.
9. Remaining canonical repos from the manifest.

Per-repo enrollment steps:

- [ ] Confirm manifest entry and CI profile.
- [ ] Add workflow shim.
- [ ] Run `wip-release check` locally.
- [ ] Open PR.
- [ ] Verify PR CI.
- [ ] Merge.
- [ ] Verify alpha release.
- [ ] Verify canary.
- [ ] Update release ledger.

Acceptance criteria:

- [ ] LDM OS and DevOps Toolbox are fully enrolled before broad fan-out.
- [ ] Every later repo uses the same enrollment checklist.
- [ ] Failures in later repos improve the shared workflow rather than creating one-off local hacks.

## Phase 12: Tracking Model

Goal: keep all planning and bug state visible from this folder.

Rules:

- [ ] Child bugs for this release-pipeline work live in `ai/product/bugs/release-pipeline/`.
- [ ] Each child bug includes `Implementation repo:` when code changes live elsewhere.
- [ ] Each child bug links back to this master plan.
- [ ] Each implementation PR links to the child bug and this master plan.
- [ ] Old open bugs are not archived until their acceptance criteria are either complete or copied into an open child bug.
- [ ] Archived historical bugs remain archived but are referenced from this plan.

Recommended child bugs:

- [ ] Repo manifest reconciliation.
- [ ] Existing `wip-release` gate audit.
- [ ] `wip-release check`.
- [ ] LDM installer clean-home smoke harness.
- [ ] Shared GitHub workflow library.
- [ ] Alpha release record and canary status.
- [ ] Rollback and known-bad release ledger.
- [ ] Public mirror promotion gate.
- [ ] Shared rules and docs sync.
- [ ] Branch hygiene automation.

Acceptance criteria:

- [ ] Someone can start from this file and find every related implementation thread.
- [ ] No release-pipeline decision exists only in an agent context window.
- [ ] Completion can be audited years later.

## Mapping From Existing Bugs

| Existing bug | Covered by |
| --- | --- |
| `2026-04-05--cc-mini--release-pipeline-master-plan.md` | Phases 1, 5, 7, 8, 10 |
| `2026-04-06--cc-mini--shared-universal-config-layer.md` | Phase 9 |
| `2026-04-08--cc-mini--silent-skip-without-license-guard-config.md` | Phases 1, 2 |
| `2026-04-17--cc-mini--release-pipeline-hardening-and-ci.md` | Phases 0 through 12, especially 2, 4, 6, 7 |
| `2026-04-24--codex--prerelease-installs-vs-stable-dogfood.md` | Phases 6, 7, 9 |
| `archive/2026-03-27--cc-mini--version-mismatch-deploy-gap.md` | Phase 8 |
| `archive/2026-03-30--cc-mini--installer-skips-bridge-deploy.md` | Phase 3 |
| `archive/2026-03-31--cc-mini--installer-dependency-resolution.md` | Phase 3 |
| `archive/2026-03-31--cc-mini--installer-deploy-order.md` | Phase 3 |

## Open Decisions

1. Alpha public mirror policy.

   Recommendation: alpha does not sync public mirrors. If alpha install depends on public repos, fix the installer path so alpha uses the alpha artifact.

2. Release trigger model.

   Recommendation: use protected-main-compatible release PRs when release commands mutate files. Use direct workflow publish only for flows that do not mutate protected branches.

3. Runner model.

   Recommendation: use GitHub-hosted macOS runners for canary install. Self-hosted runners can come later for speed, but should not be the only source of release confidence.

4. Manifest schema.

   Recommendation: extend the existing repo manifest instead of creating an unrelated registry, but keep release metadata structured enough that workflows can consume it directly.

5. Release ledger location.

   Recommendation: store machine-readable release records in the implementation repo and keep human planning records in this LDM OS bug folder.

## Master Acceptance Criteria

The master plan is complete when:

- [ ] The repo manifest is reconciled and release-owned repos are classified.
- [ ] LDM OS and DevOps Toolbox use shared PR CI.
- [ ] `wip-release check` exists and is required before merge.
- [ ] Missing license, CLA, npmignore, README, release notes, and repo-init requirements fail closed.
- [ ] Sub-tool version drift fails closed.
- [ ] Release conflicts with existing npm versions, tags, or dist-tags fail closed.
- [ ] Installer clean-home smoke tests cover bridge deploy, dependency resolution, deploy order, skill frontmatter, shared rules, and docs sync.
- [ ] Alpha releases produce durable release records.
- [ ] Alpha canary installs from the published artifact and verifies runtime behavior.
- [ ] Beta and stable promotion require canary success.
- [ ] Public mirror sync is validated before stable release.
- [ ] Rollback can restore last-known-good dist-tags and release state.
- [ ] Known-bad releases are visible to tooling.
- [ ] Shared rules teach agents the release workflow.
- [ ] Branch hygiene keeps merged release work visible but clearly closed.
- [ ] Every open historical release-pipeline bug is completed, archived, or explicitly superseded by a child bug under this plan.

## Immediate Next Actions

1. Land this master plan in `ai/product/bugs/release-pipeline/`.
2. Add a short pointer from each of the four open release-pipeline bugs to this master plan.
3. Create the Phase 0 child bug for manifest reconciliation.
4. Create the Phase 1 child bug for auditing existing `wip-release` behavior.
5. Ship the MVP path first: Phase 0, Phase 2, Phase 3, Phase 5, and Phase 6.
6. Use existing `wip-repos`, `wip-release`, `wip-license-guard`, and `wip-license-hook` surfaces before adding new tools.
7. Implement Phase 4 after the first two repos prove the workflow shape.
8. Implement Phases 7 and 8 before stable/public promotion.
9. Implement Phases 9 and 10 as part of making the process durable for agents and humans.
10. Roll out to the remaining repos only after LDM OS and DevOps Toolbox pass the full MVP loop.
