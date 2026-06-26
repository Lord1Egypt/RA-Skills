## Description: <br>
Trade security tokens on the X platform by checking balances, placing confirmed orders, viewing market data, and reviewing trade history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seineruo](https://clawhub.ai/user/seineruo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users with an X Trading API key use this skill to retrieve account, portfolio, market, order, and trade-history information and to place or cancel security-token orders after explicit confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose sensitive financial account, portfolio, trade-history, and transaction data. <br>
Mitigation: Use the least-privilege API key possible, prefer read-only permissions when trading is not needed, and avoid requesting account history in shared contexts. <br>
Risk: The skill can place or cancel security-token orders through the X trading account API. <br>
Mitigation: Manually verify every order detail and require explicit confirmation before order execution. <br>
Risk: An exposed or over-permissioned X_TRADING_API_KEY could allow unauthorized account access. <br>
Mitigation: Store the API key only in the environment, never repeat it in responses, and rotate or restrict the key if exposure is suspected. <br>


## Reference(s): <br>
- [Account & Portfolio API](artifact/api-account.md) <br>
- [Market Data API](artifact/api-market.md) <br>
- [Order Execution API](artifact/api-orders.md) <br>
- [Trade History & Reports API](artifact/api-history.md) <br>
- [X Trading API access](https://xtrading.com/api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Markdown or text responses with API request guidance and JSON-shaped API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires X_TRADING_API_KEY; order placement requires explicit user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
