## Description:

Automate Raiffeisen ELBA online banking to access account balances, transactions, and securities positions after user-approved login.

This skill is ready for commercial/non-commercial use.

## Publisher:

[odrobnik](https://clawhub.ai/user/odrobnik)

### License/Terms of Use:

MIT-0

## Use Case:

Raiffeisen ELBA account holders and their agents can retrieve balances, transactions, and portfolio positions after approving login with pushTAN.

### Deployment Geography for Use:

Austria

## Known Risks and Mitigations:

Risk: The skill stores an ELBA ID and PIN locally, despite inconsistent disclosure of PIN storage.

Mitigation: Review the setup and security documentation before use; keep credentials in a private workspace and delete them when no longer needed.

Risk: Bulk mailbox collection and download can save sensitive banking documents locally without prominent disclosure.

Mitigation: Do not run document collection or download scripts unless you intend to save mailbox documents; delete downloaded documents and exports when finished.

Risk: Cached banking sessions and tokens may remain available after use.

Mitigation: Run logout after each session and remove cached sessions and exports when finished; avoid debug mode unless necessary.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/odrobnik/skills/raiffeisen-elba)
- [Setup and configuration](artifact/SETUP.md)
- [Security and data handling](artifact/SECURITY.md)
- [Accounts output schema](artifact/references/accounts.schema.json)
- [Transactions output schema](artifact/references/transactions.schema.json)

## Skill Output:

**Output Type(s):** [JSON, Text, Shell commands, Guidance]

**Output Format:** [JSON banking data and text guidance with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user pushTAN approval for login; can save financial exports and mailbox documents locally.]

## Skill Version(s):

1.5.3 (source: skill frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
