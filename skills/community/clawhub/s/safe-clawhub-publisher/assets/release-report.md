# ClawHub release report

- Target: `<owner>/<slug>`
- Local source: `<resolved path>`
- Detected type: `<skill | plugin-package>`
- CLI path: `<resolved executable>`
- CLI version: `<version>`
- CLI installation source/scope: `<existing | package@version, global/project>`
- Authenticated account: `<handle or not logged in>`
- Current remote version: `<version or new package>`
- Proposed version: `<version>`
- Version rationale: `<evidence>`
- Changelog: `<text>`
- Remote baseline checked at: `<timestamp>`
- Canonical package page: `https://clawhub.ai/<owner>/skills/<slug>`

## Package contents

- Included files and hashes: `<exact list or report reference>`
- Excluded: `<ignore rules and rationale>`
- Validator fingerprint: `<digest>`
- ClawHub dry-run fingerprint: `<digest>`
- Build/artifact digest: `<if applicable>`
- Executables, archives, and symlinks reviewed: `<result>`

## Validation

- Local validator: `<pass/warn/fail>`
- Ecosystem validator: `<result>`
- ClawHub dry-run: `<result>`
- Command result/error: `<exit status, sanitized stderr, phase, and classification>`
- Failure classification: `<rejected | unavailable | unknown | none>`
- Security review: `<blockers and warning details>`
- Validator/CLI file-set match: `<yes/no>`

## Final command

```text
<exact command, with no secret values>
```

## Confirmation

- Confirmed account/target/version/command/contents/fingerprint: `<yes/no>`
- Confirmation time: `<timestamp>`
- Confirmation invalidated by later changes: `<yes/no>`
- Pre-publication integrity gate: `<pass/fail and repeated fingerprint>`

## Post-release verification

- Remote version: `<result>`
- Owner/metadata/changelog: `<result>`
- Files/hashes/tags: `<result>`
- Publication state: `<published/pending/unknown>`
- Publication attempts: `<count; list each attempt's confirmation and result>`
- Non-mutating verification checks: `<0/1/2; never more than 2 for an unclear response>`
- Verification sources: `<CLI/API/canonical ClawHub page>`
- CLI/API visibility: `<confirmed/delayed/unavailable>`
- User-visible confirmation: `<not requested | user-confirmed in ClawHub UI at timestamp>`
- Retry decision: `<not needed/stopped/fresh confirmation required/manual resolution required>`
- Security scan: `<passed/pending/failed>`
- Verification stopped at: `<timestamp or completion>`
- Follow-up: `<none or action>`
