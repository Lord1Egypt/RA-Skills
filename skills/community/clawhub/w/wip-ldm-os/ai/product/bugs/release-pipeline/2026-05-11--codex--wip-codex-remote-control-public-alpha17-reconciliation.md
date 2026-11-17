# Bug: WIP Codex Remote Control first public alpha release needs catch-up notes

Date: 2026-05-11
Status: done
Owner: Codex
Component: wip-codex-remote-control release history, public mirror releases
Severity: Medium

## Summary

`wip-codex-remote-control-private` had private alpha release history before the public mirror started publishing release records. The public repo begins its release history at `v0.0.2-alpha.17`, so that release must read like the first public alpha prerelease, not just a narrow alpha.17 delta.

## Problem

The public release record for `v0.0.2-alpha.17` initially only described the alpha.17 change:

- OpenAI-facing Coherence demo artifacts.
- Public issue packet.
- Backfilled private tag metadata.

That is accurate but incomplete for a first public release. A first public prerelease should also summarize the public-safe development history that happened before the public mirror began:

- local daemon
- pairing flow
- hosted relay
- browser and phone control surface
- E2EE channel work
- live co-presence proof
- installer and release-track behavior
- the boundary between private dogfood releases and public mirror releases

## Correct model

Private alpha releases are the complete dogfood record. Public alpha releases are public-safe mirror records.

The public repo should not invent releases for private-only alpha tags that do not have public mirror commits. Instead, the first public release should contain a catch-up section that explains the prior public-safe history.

## Recovery work

Manual recovery on 2026-05-11:

- Private release records were backfilled for `v0.0.2-alpha.1` through `v0.0.2-alpha.21`.
- Public release records were created only for public mirror tags that have public commits:
  - `v0.0.2-alpha.17`
  - `v0.0.2-alpha.18`
  - `v0.0.2-alpha.19`
- Public `v0.0.2-alpha.17` was updated as the first public alpha prerelease with catch-up notes.

## Verification

Verified on 2026-05-11:

- Public `v0.0.2-alpha.17` release now states that it is the first public alpha prerelease.
- The body includes public-safe catch-up history through alpha.17.
- The body keeps the specific alpha.17 Coherence packet delta.
- Public release history remains limited to public mirror commits instead of fabricating releases for earlier private-only tags.

## Required future follow-up

This recovery is complete. The remaining release-pipeline work belongs in the companion policy bug:

- `2026-05-11--codex--public-private-release-note-policy.md`

That policy update should make future manual recovery unnecessary. Future validations should still confirm:

- `https://github.com/wipcomputer/wip-codex-remote-control/releases/tag/v0.0.2-alpha.17` states that it is the first public alpha prerelease.
- The release body contains a sanitized catch-up history through alpha.17.
- The release body still includes the specific alpha.17 Coherence packet delta.
- Public releases are not created for private-only tags that lack public mirror commits.
- Future public prereleases get useful release bodies at publish time instead of requiring manual backfill.

## Acceptance

- Public `v0.0.2-alpha.17` release body is updated.
- Private release records exist for alpha.1 through alpha.21.
- Public release records exist for alpha.17 through alpha.19.
- No private ticket names, local paths, or internal notes are leaked into the public release body.
- A policy bug exists for updating the public and private release guides.
