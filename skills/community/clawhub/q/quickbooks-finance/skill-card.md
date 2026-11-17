## Description:

Manage QuickBooks accounts, customers, invoices, payments, bills, expenses, and financial workflows via the QuickBooks Online API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

External users, finance teams, and developers use this skill to read QuickBooks company data, manage customers, invoices, vendors, bills, payments, accounts, and run financial reports through a connected QuickBooks Online account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on a persistent third-party ClawLink plugin with broad access to connected QuickBooks financial data.

Mitigation: Install only when the publisher and plugin are trusted, verify the plugin source and version where possible, and use the least-privileged QuickBooks account available.

Risk: Write operations can create, update, delete, void, reverse, or process financial records and payments.

Mitigation: Require previews and explicit user confirmation before writes, and verify amounts, accounts, dates, target records, and OAuth permissions before execution.

Risk: A connected QuickBooks OAuth session can continue to authorize access after setup.

Mitigation: Review granted OAuth scopes and know how to revoke the QuickBooks connection and disable the plugin when it is no longer needed.

## Reference(s):

- [QuickBooks Online API](https://developer.intuit.com/)
- [QuickBooks API Reference](https://developer.intuit.com/docs/api/accounting)
- [ClawLink OpenClaw Docs](https://docs.claw-link.dev/openclaw)
- [ClawLink Verification](https://claw-link.dev/verify)
- [ClawHub Skill Page](https://clawhub.ai/hith3sh/skills/quickbooks-finance)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON-like tool call parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include financial record summaries, report outputs, previews of write operations, and error-handling guidance.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
