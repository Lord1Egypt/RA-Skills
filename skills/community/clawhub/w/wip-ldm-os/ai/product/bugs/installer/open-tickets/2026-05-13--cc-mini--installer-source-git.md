---
title: "Installer: source.git for git-tracked extensions (Step 3)"
status: open
priority: P2
owner: Installer Cody
reviewer: Installer CC Partner
repo: wip-ldm-os-private
created: 2026-05-13
---

# Installer: `source.git` for git-tracked extensions

## Problem

Many WIP Computer extensions live in private GitHub repos with no npm publication. Today:

- `compaction-indicator` ... github.com/wipcomputer/compaction-indicator-private
- `root-key` ... github.com/wipcomputer/wip-root-key (private)
- `wip-agent-pay` ... github.com/wipcomputer/wip-agent-pay-private
- `dream-weaver-protocol` ... github.com/wipcomputer/dream-weaver-protocol (public)
- (and any other extension installed from a git repo rather than npm)

These have GitHub releases or tags representing real version progression, but the installer has no way to check them. Today the registry either says `source.npm: "<name>"` (404) or `source: { ... npm: "no-npm" }` (skip probe). Neither tracks updates.

End-user impact: extensions stay at the version installed at first deploy, and there's no way to notice when the source repo has a newer tag. `ldm status` silently can't tell you.

## Proposal

Add the `git` updateSource type to the registry schema (per the [parent design](2026-05-13--cc-mini--installer-registry-source-types-architecture.md)):

```jsonc
{
  "root-key": {
    "updateSource": { "type": "git", "ref": "wipcomputer/wip-root-key" },
    "installed": { "version": "0.2.0" }
  }
}
```

For a fork, add provenance:

```jsonc
{
  "openclaw-tavily": {
    "updateSource": { "type": "git", "ref": "wipcomputer/openclaw-tavily" },
    "provenance": {
      "fork-of": "openclaw-tavily",
      "upstream-version-at-fork": "0.2.1"
    },
    "installed": { "version": "1.0.1" }
  }
}
```

`updateSource.ref` is `<owner>/<repo>`, matching the format the `gh` CLI uses for repo refs. The repo can be public or private. The installer uses the user's `gh` auth (already configured for the dev environment).

### Forks (ahead-of-upstream)

Forks are just `git`-type updateSource entries where the local installed version is ahead of the upstream's latest tag. The probe runs the same way; the comparison is `semverNewer(local, upstream)`:

- If `semverNewer(upstream, local)`: update available. Report as `local v0.2.0 -> v0.3.0 (wipcomputer/wip-root-key, git)`.
- If `semverNewer(local, upstream)`: ahead of upstream. Report as `local v1.0.1 (ahead of wipcomputer/openclaw-tavily v0.2.1, git)`. Not flagged as update available.
- If versions equal: current. Report normally.

No separate `fork` type is needed.

### Install-prompt policy guard (important)

The `gh api` dispatch in this design lives **inside the installer** (in `cmdStatus`), called by `ldm` when probing `git`-type entries. It is NOT a sanctioned way for **agents** to call `gh release` or `gh api` directly during the install flow.

The alpha.25 install-prompt policy explicitly forbids agents from running raw `gh release list`, `gh release view`, `gh api repos/*`, or `gh search` during install-state detection. That policy remains in force. Agents continue to call `ldm status` or `ldm install --dry-run`, and the installer makes whatever `gh api` calls are needed internally.

If a future install-doc revision adds an explicit "user asked for release notes" path, that path may permit `gh release view` agent-side; this Step 3 ticket does NOT change that policy.

## How `ldm status` dispatches the git type (inside the installer)

When the probe runs (this is `cmdStatus` source code, not an agent action):

1. Call `gh api repos/<ref>/releases/latest --jq '.tag_name'`.
2. If 200 OK: strip a leading `v` from the tag, compare to installed version via `semverNewer`. If newer, mark as update available.
3. If 404 OR releases-not-found: fall back to `gh api repos/<ref>/tags --jq '.[0].name'` (latest tag).
4. If both fail (no releases, no tags): mark as `[no version info]`, not "update available" and not "current".
5. If `gh` itself errors (auth issue, rate limit, network): mark as `[git-probe failed: <reason>]`.

Concurrency and timeout: same controls as the npm probe path (`LDM_STATUS_NPM_CONCURRENCY`, `LDM_STATUS_NPM_TIMEOUT_MS`, `LDM_STATUS_TOTAL_BUDGET_MS`). Rename to `LDM_STATUS_PROBE_*` if the unification ticket lands first, otherwise keep separate but matched defaults.

The above lives in `bin/ldm.js`. Agents in the install flow never invoke these `gh api` calls directly; they invoke `ldm status`, and the installer makes the calls.

## Authentication

Use `gh api` directly. The user's `gh` CLI is already authenticated for the wipcomputer org and has access to private repos. The installer doesn't need a separate auth mechanism.

If `gh` is not installed or not authenticated, `gh api` fails fast and the row marks `[git-probe failed: gh-unavailable]`. Same as npm-not-installed today.

## How `ldm install` populates the git type

When `ldm install <git-url>` or `ldm install <owner>/<repo>` runs (catalog or direct), set `updateSource: { type: "git", ref: "<owner>/<repo>" }` in the new registry entry. The existing install code already accepts git URLs as install targets per `bin/ldm.js` `cmdInstall`; this just adds source tracking.

For existing registry entries whose extensions are git-installed but currently in the legacy bad-`source.npm` state, [Phase 1](2026-05-13--cc-mini--installer-source-npm-honest-cleanup.md) first migrates them to `updateSource.type: "untracked"`. The [migration ticket](2026-05-13--cc-mini--installer-source-types-migration.md) then runs `ldm doctor --reclassify-sources` to reclassify the untracked entries that are actually git-sourced.

## Acceptance

- Schema: `git` updateSource type documented in `bin/ldm.js` and the parent design ticket.
- `ldm install` writes `updateSource: { type: "git", ref: ... }` when the install target is a git source.
- `ldm status` probes via `gh api`, respects the same concurrency/timeout/budget controls as npm probes.
- `gh` auth failures surface clearly in the probe-failures section (no silent unavailable).
- Fork case: regression test stages a git-source extension where local installed version is newer than the latest upstream tag; assert status reports "ahead of upstream" and does NOT flag update available.
- Regression test: stage a fixture extension with the git type; mock `gh api` responses; assert status reports correctly for: newer-tag-available, same-version, ahead-of-upstream, no-releases-no-tags, gh-failed.
- Real-machine dogfood: at least one private-repo extension (e.g., `root-key` if migrated) reports a real version diff or "current" status from its GitHub tags.
- **Policy guard:** the install-prompt regression eval ([eval ticket](2026-05-12--cc-mini--install-prompt-regression-eval.md)) still passes after this lands. Agents must not call `gh release` or `gh api` directly during the install flow; the eval's pass criteria do not change. This ticket's `gh api` dispatch is an installer-internal mechanism, not an agent-facing one.

## Trade-offs

- `gh api` is slower than direct `fetch` to npm. The npm registry has CDNs everywhere; GitHub API has rate limits and per-request overhead. Per-probe budget may need to be higher (suggest 10s default vs npm's 5s).
- Private repos require user-side `gh` auth. The installer doesn't make this seamless for new users; it inherits whatever `gh` is configured for.
- GitHub rate limits (5000 req/hour for authenticated users) shouldn't bite for `ldm status` on a personal machine (32 extensions = 32 calls = nowhere near the limit), but a CI runner running status frequently could hit it.

## Why P2 not P1

Step 1 quiets the noise. Step 2 represents bundled extensions correctly. This step **adds new capability** ... it lets `ldm status` track updates for extensions that currently have no update visibility. Without it, those extensions are at the version they were when first installed and the user has no way to know. With it, the installer's promise ("install anything, know if there's an update") becomes real.

P2 because: it's a feature, not a fix. The user-facing flow doesn't break without it; it just stays opaque for git-tracked extensions.

## Out of scope

- Automatic git clone or update of the source repo. The installer only checks for new tags; pulling the update is a separate `ldm install <target>` command.
- Semver coercion for tags that don't follow strict semver (e.g., `2026-04-15` calendar tags). Decide a policy in the implementation slice (suggest: warn and treat as unavailable for non-semver).

## Recommendation

Alpha after fix. Dogfood with at least one private-repo extension. If happy, file follow-up for the unification with `cmdInstallCatalog` ([drift ticket](2026-05-12--codex--ldm-status-install-dry-run-update-detection-drift.md)).

## Related

- Parent: [Installer registry source types architecture](2026-05-13--cc-mini--installer-registry-source-types-architecture.md)
- Companion: [source.bundled support](2026-05-13--cc-mini--installer-source-bundled.md)
- Follow-up that depends on this: [ldm status output reformat](2026-05-13--cc-mini--installer-status-show-all-extensions.md)
- Master ticket: [ldmos-bugs-masterticket--installer.md](ldmos-bugs-masterticket--installer.md)
