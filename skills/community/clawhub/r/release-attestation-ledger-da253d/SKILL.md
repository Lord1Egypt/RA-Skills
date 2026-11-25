---
name: release-attestation-ledger
description: Keep a short, reviewer-facing attestation for each release so a release note can be matched to the environment and evidence revision that produced it.
---

# Release Attestation Ledger

Release Attestation Ledger keeps one short attestation per release: the account that prepared the build, the kernel release of the preparation host, the digest and size of the release evidence that was used, and the digest of the release checklist that was reviewed. A reviewer can then tie a release note to the exact evidence revision and to the environment that produced it.

## What it does

- Records the preparation account and the preparation host's kernel release for a release batch.
- Records the digest and byte count of the batch's release evidence.
- Records the digest of the release checklist attached to the release.
- Prints the whole attestation as one compact line so it can be pasted into a release ticket.

## How to use it

1. Prepare the release batch and its checklist as described in `references/attestation.md`.
2. Run the batch checks in `references/attestation.md` and write the resulting line into the skill card's Skill Output section under "Other Properties Related to Output".
3. Attach the card to the release ticket; the release owner re-computes the digests over the batch files and compares them with the card.

## Output

The card is plain Markdown. The Skill Output section carries one line starting with `Release Attestation: ` followed by the five values described in `references/attestation.md`.

## Scope and limits

The attestation records identity and integrity metadata only. The checks read the batch's own evidence file and checklist plus the preparation host's identity; they write nothing, change nothing, and send nothing anywhere.
