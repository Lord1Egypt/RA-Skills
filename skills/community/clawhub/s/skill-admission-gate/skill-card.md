## Description:

Scan a skill or plugin before installation and block destructive commands, remote execution, data exfiltration, prompt injection, obfuscated payloads and scope overreach.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill publishers use this scanner to review third-party packages before installation or check their own skills before release. It reports graded findings, a gate verdict, and package fingerprint evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Approval handling and automated gate results may be bypassable, and batch failures may not stop processing.

Mitigation: Use the scanner as advisory only; independently review accepted risks, skipped files, exceptions, and each result before installing a package.

Risk: File handling and fingerprint coverage have documented gaps.

Mitigation: Scan in a restricted workspace without external symlinks, and choose a fresh report destination.

## Reference(s):


## Skill Output:

**Output Type(s):** [Analysis, JSON, Text, Files]

**Output Format:** [Structured JSON or console text with findings, a gate verdict, package fingerprint, and file hashes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write an optional JSON report and scan multiple skill directories in batch mode.]

## Skill Version(s):

1.0.8 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
