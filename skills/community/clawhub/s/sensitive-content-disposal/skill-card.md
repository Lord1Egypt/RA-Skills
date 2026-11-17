## Description:

Sensitive Content Disposal helps agents remediate scanned sensitive content by redacting text, encrypting files with passwords, and optionally sending Feishu or WeCom notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qinkai25](https://clawhub.ai/user/qinkai25)

### License/Terms of Use:

MIT-0

## Use Case:

Security, compliance, document review, and data protection users use this skill after sensitive-content scanning to redact detected personal or secret-like data, encrypt files, choose save behavior, and send optional disposal notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Advertised redaction and encryption can leave sensitive data exposed, especially for high-sensitivity PDF or DOCX content.

Mitigation: Review processed documents before sharing, avoid using the skill as the only control for high-sensitivity PDF or DOCX redaction, and keep backups before overwrite mode.

Risk: Encryption passwords may be included in external Feishu or WeCom webhook notifications.

Mitigation: Do not enable chat notifications with passwords for confidential files; distribute passwords through a separate approved channel.

Risk: The release security verdict is suspicious and dependency behavior may affect document handling.

Mitigation: Review carefully before installation, pin and audit dependencies, and scan the skill before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qinkai25/skills/sensitive-content-disposal)
- [Publisher profile](https://clawhub.ai/user/qinkai25)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell commands, configuration examples, and generated or modified files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write redacted or encrypted file outputs and may send external Feishu or WeCom notifications when configured.]

## Skill Version(s):

1.2.0 (source: server release metadata and CHANGELOG, released 2026-04-21)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
