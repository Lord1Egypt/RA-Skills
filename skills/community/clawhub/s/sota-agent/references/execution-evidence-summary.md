# Execution Evidence Summary

Use this reference when execution was handled outside `sota-agent` and the
planning skill needs a public-safe summary for claim review.

## Required Summary Fields

- benchmark name, metric, split, and target threshold
- baseline score and candidate score
- commit or configuration identifier
- dataset identifier and version
- hardware or runtime class, stated broadly
- artifact manifest path or checksum
- review status: promote, hold, cut, or rerun

## Review Rules

- Do not promote from live runtime state.
- Do not include private URLs, local endpoints, credentials, personal account
  labels, or host-specific machine names.
- Prefer synced artifacts, public references, and redacted manifests over raw
  logs.
- Keep long-run management, account-bound execution, and artifact transfer in
  the paired execution skill.

## Handoff Rule

If execution is still in progress, this planning skill should record the
remaining evidence gap and stop at a hold decision.
