# Version history

## 0.1.6
- Require Lead number before intake handoff


## 0.1.5
- Require Lead number before estimator flow


## 0.1.4
- Added ClawHub publish metadata headers (`homepage`, `metadata.openclaw.emoji`) for registry publishing.


## 0.1.3 - 2026-04-05
- Added top-level `Required Missing Data Summary` guidance for multi-lead review.
- Clarified grouped triage output when required fields are missing across pasted leads.

## 0.1.2 - 2026-04-05
- Added hard required-data gate: do not move forward into estimating when address is missing.
- Added rule to return missing-required-data output for affected leads before continuing.

## 0.1.1 - 2026-04-05
- Added rule: Workiz Lead # is the required primary identifier for manual lead blobs when available.
- Clarified that missing phone/email/address in pasted blobs may simply mean the data was not included in the lead description field.
- Clarified future API mode should associate lead + client data together for pre-job estimate workflows.

## 0.1.0 - 2026-04-05
- Initial release of `rolling-suds-workiz-lead-runner`.
- Defined read-only scope for Workiz leads and associated client data.
- Added manual-mode workflow using pasted/exported data.
- Reserved future read-only API mode for leads + client data once permissions/token access exist.
