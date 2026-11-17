## Description:

YNAB budget management skill that helps agents add transactions, track goals, monitor spending, create transfers, and generate budget reports through the YNAB API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[f-liva](https://clawhub.ai/user/f-liva)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers who manage YNAB budgets use this skill to inspect budget status, add transactions or transfers, review goals, compare months, and produce budget reports. It is intended for workflows where an agent is explicitly allowed to access a live YNAB account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read from and write to a live YNAB budget, including creating transactions and transfers.

Mitigation: Install only when YNAB access is intended and require explicit confirmation before any write action.

Risk: The skill requires a YNAB API key and budget identifier.

Mitigation: Store credentials in environment variables or a protected config file, avoid logging full API keys, and rotate tokens periodically.

Risk: Broad finance-related activation phrases may invoke the skill even when the user did not explicitly mention YNAB.

Mitigation: Confirm that the user intends to use YNAB and verify the target budget or account before running scripts or API calls.

Risk: Transient API errors and rate limits can produce misleading failure messages.

Mitigation: Retry 401, 429, and 5xx responses with short delays before reporting failure, and do not treat the first 401 as proof of token expiration.

## Reference(s):

- [YNAB API Guide](references/api-guide.md)
- [Category Examples](references/category-examples.md)
- [YNAB API documentation](https://api.ynab.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal-oriented text with shell command examples and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, YNAB_API_KEY, and YNAB_BUDGET_ID or an equivalent protected YNAB config file.]

## Skill Version(s):

2.4.0 (source: server release metadata and skill.toml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
