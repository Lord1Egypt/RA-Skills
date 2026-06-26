## Description: <br>
Interact with the BudgetBakers Wallet API for personal finance data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andresubri](https://clawhub.ai/user/andresubri) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External Wallet users and agents use this skill to query personal finance accounts, categories, transactions, budgets, and templates from the BudgetBakers Wallet REST API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill accesses personal financial data through a Wallet API token. <br>
Mitigation: Use it only with trusted publishers and accounts where the agent should read Wallet data. <br>
Risk: WALLET_API_TOKEN exposure could allow unauthorized access to Wallet API data. <br>
Mitigation: Keep the token out of chats, logs, screenshots, and committed files; set it only in the runtime environment and rotate or revoke it when no longer needed. <br>


## Reference(s): <br>
- [BudgetBakers Wallet API Reference](references/api-reference.md) <br>
- [BudgetBakers Wallet OpenAPI UI](https://rest.budgetbakers.com/wallet/openapi/ui) <br>
- [ClawHub Skill Page](https://clawhub.ai/andresubri/wallet-api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses from the helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires WALLET_API_TOKEN and a BudgetBakers Wallet Premium plan; list endpoints support limit, offset, and documented filters.] <br>

## Skill Version(s): <br>
0.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
