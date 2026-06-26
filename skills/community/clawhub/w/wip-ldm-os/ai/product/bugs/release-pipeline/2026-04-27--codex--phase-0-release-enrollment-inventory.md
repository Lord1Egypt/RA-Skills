# Phase 0: release enrollment inventory

**Date:** 2026-04-27
**Filed by:** Codex
**Component:** Release pipeline repo inventory
**Severity:** High
**Master plan:** `ai/product/bugs/release-pipeline/2026-04-24--codex--canary-release-pipeline-master-plan.md`
**Implementation repo:** `wip-ai-devops-toolbox-private`
**Implementation PR:** https://github.com/wipcomputer/wip-ai-devops-toolbox-private/pull/389
**Manifest PR:** https://github.com/wipcomputer/wipcomputer-ldmos-wipcomputerinc-home-private/pull/30
**Status:** MVP tooling and MVP repo enrollment shipped. Remaining manifest decisions still open.

## Summary

Phase 0 of the canary release pipeline needs a repo inventory that is actionable for release enrollment. Existing `wip-repos check` already compared manifest paths to repos on disk, but it did not answer the release-pipeline question:

- Which active repos are enrolled in release automation?
- Which repos are explicitly excluded?
- Which repos still need a release-profile decision?
- Which manifest entries point to repos missing on disk?
- Which active repos are on disk but absent from the manifest?

PR #389 adds that report to `wip-repos`.

## Shipped behavior

`wip-repos` now supports:

```bash
wip-repos release-enrollment
wip-repos release-enrollment --strict
wip-repos release-enrollment --json
```

It also exposes the same report through MCP:

```text
repos_release_enrollment
```

The command reuses the existing manifest loader and repo path classifier. It does not invent a second inventory system.

## Manifest metadata shape

Release enrollment metadata lives in each repo manifest entry:

```json
{
  "ldm-os/devops/my-tool-private": {
    "remote": "wipcomputer/my-tool-private",
    "release": {
      "enabled": true,
      "profile": "node-package",
      "smokeProfile": "ldm-tool",
      "publicMirror": "wipcomputer/my-tool",
      "requiredSecrets": ["NPM_TOKEN"]
    }
  },
  "ldm-os/docs/archive": {
    "remote": "wipcomputer/docs-archive",
    "release": {
      "enabled": false,
      "reason": "archived repo"
    }
  }
}
```

## Current local signal

Running the new command against the local manifest and repo root before MVP repo enrollment produced:

```text
Active manifest repos: 53
Enrolled:              0
Excluded:              0
Needs decision:        42
Missing on disk:       11
Unmanifested active:   23
Blockers:              34
```

This confirms the master plan's Phase 0 premise: shared CI cannot safely fan out until the repo manifest is reconciled and release enrollment decisions are explicit.

After PR #30 enrolled the two MVP repos and corrected their manifest paths, the report moved to:

```text
Active manifest repos: 53
Enrolled:              2
Excluded:              0
Needs decision:        42
Missing on disk:       9
Unmanifested active:   21
Blockers:              30
```

The two enrolled repos are:

- `ldm-os/wip-ldm-os-private`
- `ldm-os/devops/wip-ai-devops-toolbox-private`

## Acceptance criteria

- [x] Reuse existing `wip-repos` manifest and classifier logic.
- [x] Add a CLI report for release enrollment.
- [x] Add a JSON output suitable for CI and future release checks.
- [x] Add an MCP tool for agent-readable release inventory.
- [x] Document the manifest metadata shape.
- [x] Add regression coverage for enrolled, excluded, needs-decision, missing-on-disk, and unmanifested-active cases.
- [ ] Reconcile `repos-manifest.json` so active repos are either manifest-owned or deliberately excluded.
- [x] Add release metadata for the MVP repos:
  - `ldm-os/wip-ldm-os-private`
  - `ldm-os/devops/wip-ai-devops-toolbox-private`
- [ ] Decide release profiles for remaining active manifest repos.
- [ ] Run `wip-repos release-enrollment --strict --json` cleanly before using repo inventory as a CI gate.

## Validation

PR #389 validation:

```bash
node tools/wip-repos/test.mjs
node --check tools/wip-repos/cli.mjs
node --check tools/wip-repos/core.mjs
node --check tools/wip-repos/mcp-server.mjs
```

Real inventory validation:

```bash
node tools/wip-repos/cli.mjs release-enrollment \
  --manifest /Users/lesa/wipcomputerinc/repos/repos-manifest.json \
  --root /Users/lesa/wipcomputerinc/repos
```

That real inventory command exits nonzero right now because the manifest has blockers. That is expected.

## Next implementation slice

Phase 0 should now move from tooling to data:

1. Add or repair manifest entries for active repos on disk.
2. Mark deprecated, archived, trash, third-party, and generated repos so they do not pollute release enrollment.
3. Add release metadata for the two MVP repos first.
4. Use the clean JSON report as an input to Phase 2: `wip-release check`.
