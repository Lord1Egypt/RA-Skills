## Description:

Query Microsoft 365 data (emails, meetings, documents, Teams messages, people) using WorkIQ CLI

This skill is ready for commercial/non-commercial use.

## Publisher:

[likudo95](https://clawhub.ai/user/likudo95)

### License/Terms of Use:


## Use Case:

Employees and agents use this skill to ask natural-language questions about Microsoft 365 emails, meetings, documents, Teams messages, and people or organization data available to the signed-in user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can query sensitive Microsoft 365 data available to the signed-in account.

Mitigation: Install and run it only in accounts and tenants where that access is acceptable, and review returned content before using or sharing it.

Risk: The skill includes shell-style command templates for natural-language questions.

Mitigation: Pass the question as a separate process argument and avoid constructing shell command strings from user text.

Risk: Fallback execution through npx may run an unpinned package at runtime.

Mitigation: Prefer a preinstalled, reviewed, version-pinned WorkIQ binary and avoid npx -y runtime execution.

## Reference(s):

- [Microsoft WorkIQ overview](https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/workiq-overview)
- [ClawHub WorkIQ release](https://clawhub.ai/likudo95/skills/workiq)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Queries are stateless per call and should be run standalone.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
