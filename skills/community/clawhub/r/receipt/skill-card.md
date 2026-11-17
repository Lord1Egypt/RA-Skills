## Description:

Receipt helps agents record, search, summarize, and export local receipt and expense notes for a manual expense journal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to create shell-command based workflows for manually logging receipt and expense notes, viewing recent entries, searching logs, and exporting local files for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security review flagged suspicious behavior because the skill overstates finance-analysis capabilities.

Mitigation: Use it only as a manual local expense journal; verify totals, forecasts, tax notes, and any financial conclusions independently.

Risk: Receipt notes and exports may contain sensitive purchase, tax, or account details stored in plaintext.

Mitigation: Avoid entering sensitive details unless local file permissions and sharing controls are acceptable; protect or remove export files before sharing.

Risk: The skill is not supported by evidence as a receipt scanner or OCR tool.

Mitigation: Enter receipt information manually and do not rely on the skill to extract or validate receipt contents.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ckchzh/skills/receipt)
- [Publisher profile](https://clawhub.ai/user/ckchzh)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance]

**Output Format:** [Markdown with inline shell commands and plain-text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands can write plaintext logs and export files under ~/.local/share/receipt.]

## Skill Version(s):

2.0.1 (source: server release metadata; artifact frontmatter and script report 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
