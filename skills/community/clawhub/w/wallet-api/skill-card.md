## Description:

Interact with the BudgetBakers Wallet API to query accounts, categories, transactions, budgets, templates, and user details from a Wallet account using a WALLET_API_TOKEN.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andresubri](https://clawhub.ai/user/andresubri)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to query personal finance data from BudgetBakers Wallet through authenticated REST API calls. It supports account, category, transaction, budget, template, and current-user lookups with filtering and pagination guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Wallet API token can grant access to personal finance data if exposed.

Mitigation: Store WALLET_API_TOKEN only in a protected environment variable and do not paste it into prompts, chat history, logs, or shared files.

Risk: Broad transaction queries can return sensitive financial history.

Mitigation: Use narrow date ranges, filters, and pagination limits when retrieving records.

Risk: Repeated or unbounded requests can hit the documented 500 requests per hour rate limit.

Mitigation: Use limit and offset parameters, request only the needed endpoints, and monitor rate-limit responses before retrying.

## Reference(s):

- [BudgetBakers Wallet API Reference](references/api-reference.md)
- [BudgetBakers Wallet OpenAPI UI](https://rest.budgetbakers.com/wallet/openapi/ui)
- [BudgetBakers API Token Settings](https://web.budgetbakers.com/settings/apiTokens)
- [ClawHub Skill Page](https://clawhub.ai/andresubri/skills/wallet-api)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Configuration, Guidance, Text]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires WALLET_API_TOKEN; list endpoints support limit and offset pagination.]

## Skill Version(s):

0.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
