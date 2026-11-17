## Description:

QuickBooks Online CLI tool for managing customers, invoices, payments, bills, vendors, accounts, items, expenses, journal entries, deposits, transfers, estimates, purchase orders, and financial reports through the Intuit API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paulbudveit](https://clawhub.ai/user/paulbudveit)

### License/Terms of Use:


## Use Case:

Developers, operators, and finance teams use this skill to guide an agent through QuickBooks Online setup, authentication, accounting workflows, transaction management, imports, reconciliation helpers, and financial reporting through a Docker-based CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make live accounting changes in QuickBooks Online, including imports, batch operations, sends, voids, deletes, and journal entries.

Mitigation: Use a QuickBooks sandbox or tightly scoped company/app first, and require explicit human approval before any production-impacting command.

Risk: The install flow builds unpinned external code that will handle sensitive QuickBooks credentials and OAuth tokens.

Mitigation: Verify the upstream repository revision before building, protect the .env file and OAuth tokens, and review the skill before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/paulbudveit/skills/quickbooks-online)
- [QuickBooks Online CLI homepage](https://github.com/claw4business/quickbooks-online-cli)
- [Intuit Developer Portal](https://developer.intuit.com)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, JSON]

**Output Format:** [Markdown guidance with shell commands; CLI responses are JSON by default.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Docker, docker compose, and QuickBooks OAuth credentials; table and CSV output are also supported by the CLI.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
