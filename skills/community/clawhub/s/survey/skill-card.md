## Description:

Build surveys, collect responses, and analyze results. Use when creating forms, checking responses, converting data, analyzing trends, generating reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain3](https://clawhub.ai/user/bytesagain3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other users use Survey to run a local command-line utility for recording survey-related entries, checking status, exporting local data, and producing simple reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review describes this as a local plaintext command logger presented as a survey builder.

Mitigation: Review the skill before installing and avoid entering sensitive personal, customer, health, financial, or confidential survey data.

Risk: Survey entries and exports may be stored as local plaintext files under ~/.local/share/survey.

Mitigation: Use non-sensitive data unless the local storage location and file handling meet your requirements.

## Reference(s):

- [Survey on ClawHub](https://clawhub.ai/bytesagain3/skills/survey)
- [BytesAgain](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [Text, Files, Shell commands]

**Output Format:** [Plain text command output with optional local JSON, CSV, or TXT exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local logs and exports under ~/.local/share/survey unless SURVEY_DIR changes the data directory.]

## Skill Version(s):

2.0.0 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
