## Description:

SaleSmartly API automation skill with 29 core scripts for customer, session, marketing, WhatsApp management, reporting, and team workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[binzaga](https://clawhub.ai/user/binzaga)

### License/Terms of Use:

MIT

## Use Case:

Employees, operators, and developers use this skill to query SaleSmartly customer and conversation data, generate reports, manage WhatsApp devices, and prepare scripted business actions through the bundled command-line tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release ships exposed credentials.

Mitigation: Rotate and remove the packaged API key before installation or use.

Risk: The skill has broad authority over customer data, business actions, local commands, and external notifications.

Mitigation: Use least-privilege SaleSmartly credentials and restrict API and webhook destinations to approved SaleSmartly and DingTalk hosts.

Risk: The skill can support sends, imports, assignments, session endings, device changes, scheduled jobs, and third-party posting.

Mitigation: Require explicit human confirmation before executing those actions.

Risk: Local agent permission files may grant more access than intended.

Mitigation: Delete local permission files such as .claude/settings.local.json before installing or running the skill.

Risk: Generated scripts may be unsafe or incorrect until reviewed.

Mitigation: Treat generated scripts as untrusted and manually review them before execution.

## Reference(s):

- [SaleSmartly API authentication reference](references/authentication.md)
- [Reference materials index](references/README.md)
- [Script command reference](scripts/README.md)
- [Direct API usage guardrail](NO-DIRECT-API.md)
- [SaleSmartly API documentation](https://salesmartly-api.apifox.cn/llms.txt)
- [SaleSmartly API header signing documentation](https://help.salesmartly.com/docs/API-Header)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and optional structured JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Script outputs can use --json; mutating business actions should require explicit user confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata and pyproject.toml; artifact CHANGELOG latest released entry is 3.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
