## Description:

Manage YNAB budgets, accounts, categories, and transactions via CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[obviyus](https://clawhub.ai/user/obviyus)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to manage YNAB budgets, accounts, categories, payees, months, scheduled transactions, and live transactions through the ynab CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a YNAB API key and can access live financial data.

Mitigation: Install and use it only after reviewing the skill and keep YNAB_API_KEY protected from logs, transcripts, and shared environments.

Risk: The skill can create, update, split, budget, post raw API requests, or delete live YNAB records.

Mitigation: Require explicit confirmation before create, update, delete, split, budget, payee, or raw API POST commands.

Risk: The skill depends on the third-party npm package @stephendolan/ynab-cli.

Mitigation: Pin and review the npm package version before installing, and avoid elevated installs where a local install is practical.

## Reference(s):

- [YNAB Developer Settings](https://app.ynab.com/settings/developer)
- [ynab-cli npm package](https://www.npmjs.com/package/@stephendolan/ynab-cli)
- [ClawHub skill page](https://clawhub.ai/obviyus/skills/ynab)
- [ClawHub publisher profile](https://clawhub.ai/user/obviyus)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include YNAB CLI commands that read, create, update, or delete live budget data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
