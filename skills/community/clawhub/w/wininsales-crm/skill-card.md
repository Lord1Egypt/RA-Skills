## Description:

Use when users need WininSales CRM sales operations, including customer search, duplicate checks, ownership lookup, customer creation, follow-up records, assignment, sharing, lead and opportunity management, contracts, payments, expiry reminders, inactive-customer lists, product lookup, employee lookup, performance analysis, or daily reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hijasongithub](https://clawhub.ai/user/hijasongithub)

### License/Terms of Use:

MIT-0

## Use Case:

Sales representatives, sales managers, and CRM operations staff use this skill to query and update WininSales CRM records, manage leads and opportunities, review contracts and payments, identify renewal or inactivity risks, and draft daily sales reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read and change sensitive CRM records under the user's account.

Mitigation: Install only for trusted WininSales CRM endpoints, keep CRM permissions scoped to the user, and require explicit confirmation before each write action.

Risk: Examples use token-in-URL and shared temporary-file patterns.

Mitigation: Pass tokens through protected secrets or authorization headers and use unique protected temporary files when shell examples are adapted.

Risk: CRM outputs may contain customer contact details, contract information, or other sensitive sales data.

Mitigation: Limit operations to clearly identified CRM records and mask sensitive contact fields in displayed results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hijasongithub/skills/wininsales-crm)
- [WininSales CRM login](https://www.wininsales.com/login)
- [WininSales MCP API endpoint](https://www.wininsales.com/mcp_api/mcp?token=)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with CRM summaries, confirmation prompts, daily-report prose, and inline shell/API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Displayed CRM results should mask sensitive contact fields; write actions require explicit user confirmation before submission.]

## Skill Version(s):

1.0.9 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
