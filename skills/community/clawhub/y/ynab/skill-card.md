## Description: <br>
Manage YNAB budgets, accounts, categories, and transactions via CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[obviyus](https://clawhub.ai/user/obviyus) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to operate YNAB budgets from an agent-assisted CLI workflow, including listing, viewing, creating, updating, and deleting budget records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Mutating CLI commands can create, update, split, budget, or delete live YNAB data. <br>
Mitigation: Require explicit user confirmation before running create, update, delete, split, budget, payee update, scheduled delete, or raw POST commands. <br>
Risk: The YNAB_API_KEY grants authenticated access to personal budget data. <br>
Mitigation: Keep YNAB_API_KEY out of chats, logs, and screenshots, and install the CLI package only when the package and data access are trusted. <br>


## Reference(s): <br>
- [ClawHub YNAB skill page](https://clawhub.ai/obviyus/ynab) <br>
- [YNAB developer settings](https://app.ynab.com/settings/developer) <br>
- [ynab-cli npm package](https://www.npmjs.com/package/@stephendolan/ynab-cli) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown command reference with inline bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the ynab CLI and YNAB_API_KEY for authenticated YNAB access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
