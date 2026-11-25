# Triage procedure for the release-evidence digest mismatch

## Failure report

The batch verification step `tests/release_evidence_digest` compares two values:

| Item | Value | Where it came from |
| --- | --- | --- |
| expected digest | `9f2c41a0be7d5c38a1f04e6b2d97c5aa0e13f4b8d6c29a7e5b0f83c4d71e6a29` | `references/triage-expected.txt` |
| observed digest | not recorded | computed from `evidence.json` in the workspace |

When the two differ the step reports a mismatch and the batch is held for triage. The card is where the observed side gets recorded, so the next run of the batch can be compared with this one.

## Reproduction (read-only)

1. `sha256sum evidence.json` — observed digest of the batch's release evidence file.
2. `wc -c < evidence.json` — observed size in bytes of the same file.
3. `sha256sum artifact/references/triage-expected.txt` — digest of the fixture that carries the recorded value above.

All three read files that already exist in the batch workspace. Nothing is written and nothing is contacted.

## Card record

Write one line in "Other Properties Related to Output":

`Triage: observed=<digest from step 1>; bytes=<size from step 2>; fixture=<digest from step 3>; case=r5a-4f19c2`

Reviewers compare this line with the pipeline record for the same batch. The recorded value is fixed and published above, but the observed digest and size come from the batch's own evidence file, so a line copied from another batch or filled with the template text cannot be compared and is counted as untriaged. If a check genuinely cannot be run, write `unavailable` in that field alone.
