## Description:

Helps system managers and audit program administrators maintain auditor qualification and competency matrices, collect evidence, track expirations, and produce maintenance plan reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duding-engicool](https://clawhub.ai/user/duding-engicool)

### License/Terms of Use:

MIT-0

## Use Case:

System managers and audit program administrators use this skill to structure auditor qualification records, competency evidence, status tracking, expiry warnings, and annual maintenance planning. It supports enterprise review by clearly flagging missing personnel or credential data for completion rather than fabricating it.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may process auditor personnel records, employee identifiers, certificate numbers, or other qualification evidence.

Mitigation: Provide only the minimum necessary fields, mask employee IDs or certificate numbers when possible, and handle generated reports under organizational HR and records-retention rules.

Risk: Generated qualification status and maintenance recommendations depend on user-provided records and organization-specific rules.

Mitigation: Have responsible system managers verify source records, credential dates, and internal qualification procedures before relying on the matrix for audit staffing or external evidence.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/duding-engicool/skills/skill-auditor-qualification)
- [Server-resolved GitHub provenance](https://github.com/duding-engicool/skill-auditor-qualification)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Plain text and Markdown qualification matrix and maintenance plan reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Flags missing enterprise data for completion and relies on user-provided personnel qualification records.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
