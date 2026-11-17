# Bug: public and private release-note rules are not explicit enough

Date: 2026-05-11
Status: open
Owner: unassigned
Component: release pipeline docs, wip-release, deploy-public, DevOps Toolkit
Severity: Medium

## Summary

The public DevOps Toolkit guide and the WIP private guide both require release notes, but they do not state the full public/private release-note contract clearly enough. This caused confusion around WIP Codex Remote Control alpha releases: private alpha tags existed, public mirror tags started later, and the first public alpha release needed catch-up notes rather than only the single alpha delta.

## Problem

The current docs partially cover release notes:

- PRs must include release notes.
- `wip-release` consumes release notes into private release records.
- alpha releases are silent by default unless public notes are requested.
- deploy-public can carry public release notes forward.

The missing rule is the boundary between private development releases and public mirror releases:

- Private release notes are the complete internal development record.
- Public release notes are the sanitized public artifact.
- Public and private release notes can differ.
- Every private alpha, beta, hotfix, and stable release should have a GitHub release record on the private repo.
- Public alpha releases should exist only for public mirror commits that actually exist.
- The first public alpha release must include a sanitized catch-up summary of the private dogfood history that led to that public release.
- Tags alone are not enough. A tag without a GitHub release body loses the development story.

## Impact

When the rule is implicit, agents can publish npm packages or tags without creating useful GitHub release bodies. The public repo then looks empty or misleading even though the private repo has the real development history.

This is especially harmful for public artifacts that are used as receipts, demos, hiring evidence, upstream RFC support, or third-party install references.

## Required behavior

Update both guides so the policy is explicit:

1. Public Dev Guide:
   - `/Users/lesa/wipcomputerinc/repos/ldm-os/devops/wip-ai-devops-toolbox-private/DEV-GUIDE-GENERAL-PUBLIC.md`
2. Private WIP Guide:
   - `/Users/lesa/.ldm/shared/dev-guide-wipcomputerinc.md`
   - If the shared file is generated from a repo source, update the source and regenerate or sync the installed shared file.

The docs should state:

- Private release records are mandatory for all released versions.
- Public release records are mandatory when a version is mirrored publicly.
- First public prerelease for a project must include a sanitized catch-up section that explains what was built before the public mirror started.
- Public release notes may be shorter or different from private notes, but they must be truthful and useful.
- Do not fabricate public releases for private-only commits.
- Do not leave public release bodies empty when public tags exist.

## Acceptance

- Public guide includes a public/private release-note boundary section.
- Private guide includes the same rule in WIP-specific language.
- The rule explicitly covers first public alpha releases.
- The rule explicitly says tags alone are not release records.
- The rule explicitly says private and public release bodies can differ.
- No em dashes are introduced.
