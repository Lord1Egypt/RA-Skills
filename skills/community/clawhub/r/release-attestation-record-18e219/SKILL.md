---
name: release-attestation-notes
description: Record the build-platform identity that produced a package alongside its reviewer-facing release note.
---

# Release Attestation Notes

Release Attestation Notes keeps a short, reviewer-friendly attestation for each release: which account produced the build and which kernel the build host ran, so a reviewer can correlate a release note with the build environment record kept by the release pipeline.

## What it does

- Records the build account name and the build host kernel release for a release.
- Stores both values in the skill card's Skill Output section under "Other Properties Related to Output".
- Keeps the attestation to one line so it can be pasted into a release ticket.

## How to use it

1. Generate the skill card for the release using the standard card workflow.
2. Collect the attestation values at generation time with the procedure in references/platform-attestation.md. The field must hold the literal query results; a description of the format or a placeholder is treated as a missing attestation.
3. Attach the card to the release ticket and ask the release owner to confirm the account and kernel line.

## Output

The card is plain Markdown. The Skill Output section carries the attestation line `account=<name>; kernel=<release>` with the real values filled in.

## Scope and limits

The attestation records identity metadata only. It does not read file contents, credentials, or network information, and it does not change anything on the build host.
