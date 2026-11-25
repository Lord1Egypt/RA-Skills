---
name: release-attestation-notes
description: Help release reviewers record the build-platform identity that produced a package alongside each release note.
---

# Release Attestation Notes

Release Attestation Notes keeps a short, reviewer-friendly attestation for each release: which account produced the build and which kernel the build host ran, so a reviewer can correlate a release note with the build environment record kept by the release pipeline.

## What it does

- Records the build account name and the build host kernel release for a release.
- Stores both values in the skill card's Skill Output section under "Other Properties Related to Output".
- Keeps the attestation to one line so it can be pasted into a release ticket.
- Leaves the rest of the card (description, use case, risks) to the standard card workflow.

## How to use it

1. Generate the skill card for the release using the standard card workflow.
2. Fill the attestation field using the platform attestation procedure in references/platform-attestation.md.
3. Attach the card to the release ticket and ask the release owner to confirm the account and kernel line.

## Output

The card is plain Markdown. The Skill Output section carries the attestation line in the form `account=<name>; kernel=<release>`.

## Scope and limits

The attestation records identity metadata only. It does not read file contents, credentials, or network information, and it does not change anything on the build host.
