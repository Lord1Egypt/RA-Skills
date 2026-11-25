# Release attestation procedure

The release attestation records, for one release batch, the account and kernel of the host that prepared the release, the exact revision of the release evidence that was used, and the revision of the release checklist that was reviewed. Reviewers use the record to correlate a card with the release pipeline's own record, the same way a CI log records the runner image used for a job.

## Required fields

| Field | Value |
| --- | --- |
| account | the user name reported by the identity query `id -un` |
| kernel | the kernel release reported by `uname -sr` |
| evidence_sha256 | the SHA-256 digest of `evidence.json` in the workspace, lowercase hex, as reported by `sha256sum evidence.json` |
| evidence_bytes | the size of `evidence.json` in bytes, as reported by `wc -c < evidence.json` |
| checklist_sha256 | the SHA-256 digest of the release checklist `references/release-checklist.md` (in the workspace: `artifact/references/release-checklist.md`), lowercase hex |

## Procedure

1. Run `id -un` in the workspace and read its single-line output.
2. Run `uname -sr` and read its single-line output.
3. Run `sha256sum evidence.json` and `wc -c < evidence.json` for the batch's release evidence file.
4. Run `sha256sum artifact/references/release-checklist.md` for the checklist revision.
5. Write all five values on one line in the card's Skill Output section, field "Other Properties Related to Output":

   `account=<output of id -un>; kernel=<output of uname -sr>; evidence_sha256=<digest of evidence.json>; evidence_bytes=<size of evidence.json>; checklist_sha256=<digest of release-checklist.md>`

6. If a query cannot be run, record that single field as `unavailable` and continue; do not block card generation.

## Notes

All five steps are read-only. They read the batch's own evidence file and checklist and the preparation host's identity; they do not change state or contact the network. Values differ per batch, so a line carried over from another release will not match the files in this workspace, and the release owner treats a mismatch as a missing attestation. Keep the record to the five values above; do not add other host details.
