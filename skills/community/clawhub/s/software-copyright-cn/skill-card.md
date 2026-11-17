## Description:

Generates materials for Chinese computer software copyright registration, including a software information record, source-code identification PDFs, and user-manual identification PDFs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[binbin](https://clawhub.ai/user/binbin)

### License/Terms of Use:

MIT

## Use Case:

Developers, rights holders, and agents preparing Chinese software copyright registration filings use this skill to collect required application details and generate source-code and documentation PDF materials for review.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The skill can copy broad source content into PDFs that may be shared externally.

Mitigation: Use it only on trusted repositories and inspect the generated PDFs before filing or sharing.

Risk: software_info.json may store personal contact details.

Mitigation: Keep software_info.json out of version control and enter only details required for the filing.

Risk: Generated user-manual sections about security, APIs, login, backup, and administration may be generic draft text.

Mitigation: Verify those sections against the actual software and remove or revise unsupported claims before submission.

## Reference(s):

- [Field requirements for Chinese software copyright registration](artifact/references/fields.md)
- [ClawHub skill page](https://clawhub.ai/binbin/skills/software-copyright-cn)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with JSON configuration and shell commands; generated artifacts are JSON and PDF files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include software_info.json plus source-code and documentation identification PDFs after user confirmation.]

## Skill Version(s):

0.1.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
