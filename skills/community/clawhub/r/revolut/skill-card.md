## Description:

Revolut web automation via Playwright: login/logout, list accounts, fetch transactions, and download Invest statements (year-end holdings, realised P&L, costs and charges).

This skill is ready for commercial/non-commercial use.

## Publisher:

[odrobnik](https://clawhub.ai/user/odrobnik)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals and developers use this skill to retrieve Revolut account balances, transaction history, and investment data, and to download brokerage statements for financial recordkeeping.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment reports portfolio and data-import capabilities beyond the stated tasks.

Mitigation: Review whether those capabilities are needed and inspect the tool access before installing.

Risk: The setup supports an optional app PIN in the configuration file, and the security guidance warns against storing it in plaintext.

Mitigation: Avoid putting the Revolut PIN in plaintext configuration.

Risk: The security assessment raises concern about deleting financial records and reports partial scan coverage.

Mitigation: Review the migration instructions and available security guidance before importing or deleting financial records.

## Reference(s):

- [Revolut skill release on ClawHub](https://clawhub.ai/odrobnik/skills/revolut)

## Skill Output:

**Output Type(s):** [JSON, Files]

**Output Format:** [JSON account and transaction data; PDF or CSV investment statements]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs can include sensitive account balances, transaction history, investment holdings, and tax-related details.]

## Skill Version(s):

1.4.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
