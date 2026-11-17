## Description:

Manage your money with WIMM - add and search transactions, check balances, set budgets, and get spending reports from chat.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ipostny](https://clawhub.ai/user/ipostny)

### License/Terms of Use:

MIT-0

## Use Case:

External WIMM users use this skill to manage personal-finance data from chat, including accounts, transactions, budgets, categories, tags, balances, and spending reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent access to WIMM personal-finance data.

Mitigation: Install it only when the user intends to connect a WIMM account, and require WIMM_API_KEY for authenticated access.

Risk: Create, edit, or delete actions can change financial records.

Mitigation: Review the one-line confirmation carefully before approving any POST, PATCH, or DELETE action.

## Reference(s):

- [WIMM MCP documentation](https://wimm.my/docs/mcp)
- [WIMM ClawHub skill page](https://clawhub.ai/ipostny/skills/wimm)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires WIMM_API_KEY plus curl and jq for API-backed workflows.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
