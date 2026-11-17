## Description:

Fetches earnings call transcripts from Stock Analysis or the QVeris API, mines theme signals, and produces an evidence ledger, theme time series, and summary report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cgxxxxxxxxxxxx](https://clawhub.ai/user/cgxxxxxxxxxxxx)

### License/Terms of Use:

MIT-0

## Use Case:

External users, analysts, and developers use this skill to compare earnings call transcripts across quarters and surface topic-level business signals with source-backed outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence reports that the skill ships and uses a built-in third-party API credential.

Mitigation: Review before installing, prefer web mode, and avoid API mode until the embedded credential is removed and users provide their own secret securely.

Risk: The release evidence reports that provider-returned content URLs are followed without validation.

Mitigation: Validate returned content URLs against an allowlist and apply size limits before using API mode.

## Reference(s):

- [Transcript Analysis ClawHub Page](https://clawhub.ai/cgxxxxxxxxxxxx/skills/transcript-analysis)
- [Stock Analysis](https://stockanalysis.com)
- [QVeris API](https://qveris.ai/api/v1)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated CSV and Markdown files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces evidence ledger CSV, theme time series CSV, and summary report Markdown files.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
