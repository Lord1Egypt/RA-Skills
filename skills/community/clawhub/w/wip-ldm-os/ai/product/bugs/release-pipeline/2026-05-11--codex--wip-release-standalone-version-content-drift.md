# Bug: standalone wip-release can share a version with newer toolbox source content

Date: 2026-05-11
Status: open
Owner: unassigned
Component: wip-release, DevOps Toolkit, sub-tool publishing
Severity: Medium

## Summary

The standalone npm package `@wipcomputer/wip-release@1.9.78` was published before the later toolbox source fix for prerelease sub-tool staging landed. After that, the toolbox source copy of `tools/wip-release` was updated and its package version was set to `1.9.78`.

That creates a version/content drift hazard:

```text
npm @wipcomputer/wip-release@1.9.78
toolbox source tools/wip-release package version 1.9.78
```

Both report the same version, but they may not contain the same code.

## Problem

The Remote Control beta retry needed the standalone npm package because local `wip-release` was installed from `@wipcomputer/wip-release`. The npm `1.9.78` package contains the dist-tag timeout fix needed for that release.

Separately, PR #410 added the prerelease sub-tool staging fix to toolbox source after the standalone `1.9.78` package had already been published.

For Remote Control, this does not block the beta retry because Remote Control has no toolbox sub-tools.

For future toolbox releases, it matters. A release process that only compares package version strings may decide there is no standalone `wip-release` sub-tool change to publish, leaving the prerelease staging fix in source but not in the standalone npm package.

## Required Behavior

The next DevOps Toolkit stable release should force-publish a new standalone `@wipcomputer/wip-release` version, likely `1.9.79`, that includes the prerelease sub-tool staging fix.

The release pipeline should also prevent this class of drift going forward.

Possible guardrails:

- compare packed tarball contents or git tree hashes, not just package versions;
- require sub-tool version bump whenever files under `tools/<name>/` changed after the npm version was published;
- fail release if source package version equals npm version but source content differs from the npm tarball;
- add a release checklist item for toolbox sub-tools that were patched after a standalone publish.

## Acceptance

- Standalone `@wipcomputer/wip-release` is bumped and published with the prerelease sub-tool staging fix.
- The next stable toolbox release does not leave `tools/wip-release` source ahead of the standalone npm package.
- A guard or documented release check prevents same-version different-content drift for future sub-tools.
- Remote Control beta retry remains scoped to installing the already-published dist-tag timeout fix and does not depend on this follow-up.
- No manual npm publish bypasses the normal release process.

## Non-Goals

- Do not block the Remote Control beta retry on this ticket.
- Do not manually edit npm package metadata.
- Do not collapse toolbox and standalone sub-tool release identities. The fix is to keep their published artifacts synchronized, not to pretend they are the same artifact.

