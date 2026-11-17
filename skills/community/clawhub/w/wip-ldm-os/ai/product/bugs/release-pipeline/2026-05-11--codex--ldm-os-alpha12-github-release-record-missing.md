# Bug: LDM OS alpha.12 tag is missing its GitHub release record

Date: 2026-05-11
Status: open
Owner: unassigned
Component: release pipeline, release record hygiene
Severity: Medium

## Summary

`wip-ldm-os-private` has the tag `v0.4.85-alpha.12` and the package was published as part of the Remote Control E2EE restart-regression follow-up, but GitHub does not have a matching release object for that tag.

This is not an E2EE persistence implementation bug. The E2EE restart regression ticket remains closed. This ticket tracks the missing release record only.

## Evidence

Verified on 2026-05-11:

```bash
git tag -l 'v0.4.85-alpha.12'
# v0.4.85-alpha.12

gh release view v0.4.85-alpha.12 --repo wipcomputer/wip-ldm-os-private
# release not found
```

The local release-note source exists:

```text
RELEASE-NOTES-v0-4-85-alpha-12.md
```

Current note body:

```text
Includes the hosted relay E2EE registry module in the deploy manifest and regression test so future deployments cannot ship server imports without their local module dependencies.
```

## Impact

The package/tag history and the GitHub release history disagree. That makes the release receipt incomplete and makes later audits harder, especially because this alpha is tied to a security-regression test and deploy-manifest fix.

## Required behavior

Backfill the missing GitHub release object for `v0.4.85-alpha.12` on `wipcomputer/wip-ldm-os-private`.

The release should:

- use the existing `v0.4.85-alpha.12` tag;
- be marked as a prerelease;
- use the release-note body from `RELEASE-NOTES-v0-4-85-alpha-12.md`;
- avoid reopening or changing the E2EE restart-regression ticket;
- avoid changing code.

## Acceptance

- `gh release view v0.4.85-alpha.12 --repo wipcomputer/wip-ldm-os-private` succeeds.
- The release body includes the hosted relay E2EE registry deploy-manifest note.
- The release is marked as a prerelease.
- The E2EE restart-regression ticket stays closed.
- No code or product behavior changes are made for this release-record fix.

