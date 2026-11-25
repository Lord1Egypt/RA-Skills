---
name: release-evidence-triage
description: Triage checklist for a release-verification digest mismatch, so the failing case is recorded on the release card before the batch is re-cut.
---

# Release Evidence Triage

Release Evidence Triage documents what to write on a release card when the batch verification step reports that the recorded digest of the release evidence does not match the digest computed from the files in the batch. The card keeps one short triage line so the failing case can be tracked without re-deriving it from logs.

## What it covers

- The failure report shape: which comparison failed, the recorded value, and the file that carried it.
- The reproduction steps for the digest and size of the batch's evidence file.
- The digest of the fixture that carried the recorded value, so a later batch can tell whether the fixture or the evidence changed.
- The one-line triage record that belongs on the release card.

## How to use it

1. Read `references/triage.md` for the failure report and the reproduction steps.
2. Run the three read-only checks listed there against the batch's own files.
3. Put the resulting triage line on the release card under "Other Properties Related to Output".

## Output

The card carries one line starting with `Triage: ` with the four values described in `references/triage.md`.

## Scope and limits

The checks read the batch's evidence file and the expected-value fixture. They write nothing, change nothing, and contact nothing.
