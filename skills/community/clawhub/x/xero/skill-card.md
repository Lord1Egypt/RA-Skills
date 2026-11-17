## Description:

Helps agents access Xero accounting data through Maton to manage contacts, invoices, payments, and accounts and retrieve financial reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

People managing a connected Xero account can ask an agent to look up accounting records and reports or, with explicit approval, create or update records and set up automations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Access to sensitive Xero accounting data may exceed the task's needs.

Mitigation: Authorize only the needed account and the narrowest available OAuth scopes; disclose only the requested data.

Risk: Changes to invoices, payments, or other records can affect financial data.

Mitigation: Prefer read-only requests and confirm each write with the user before execution.

Risk: Hosted functions and trigger destinations can maintain ongoing access or forward data.

Mitigation: Require separate approval for automation and destinations, and confirm what data will flow and where.

Risk: Raw API keys can be exposed when used outside the Maton CLI.

Mitigation: Prefer OAuth through the CLI; when a key is unavoidable, keep it out of commands, files, and logs.

## Reference(s):

- [Xero skill release](https://clawhub.ai/byungkyu/skills/xero)
- [Maton](https://maton.ai)
- [Maton documentation](https://docs.maton.ai)
- [Xero Accounting API overview](https://developer.xero.com/documentation/api/accounting/overview)
- [Scheduled trigger reference](artifact/references/time/triggers.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration guidance]

**Output Format:** [Markdown with command, code, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the connected Xero account and its authorized scopes.]

## Skill Version(s):

1.2.5 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
