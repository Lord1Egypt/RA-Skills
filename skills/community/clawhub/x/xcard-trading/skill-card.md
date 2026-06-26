## Description: <br>
Trade security tokens on the XCard platform by checking balances, placing orders, viewing market data, and reviewing trade history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seineruo](https://clawhub.ai/user/seineruo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate an XCard trading assistant that retrieves account, portfolio, market, order, and history information and can prepare or execute security-token orders through the XCard API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access private account, portfolio, order, trade, and transaction data. <br>
Mitigation: Use a dedicated least-privilege XCARD_API_KEY and avoid exposing private account or history details in shared screens, logs, or transcripts. <br>
Risk: The skill can place or cancel security-token orders through XCard. <br>
Mitigation: Require explicit user confirmation before placing or cancelling orders, repeat the order details, and add a warning for large orders. <br>
Risk: The security verdict is suspicious because trading actions and private financial data are under-scoped. <br>
Mitigation: Install only when the XCard service and publisher are trusted, and limit API key permissions to required account, market, order, and history operations. <br>


## Reference(s): <br>
- [XCard API application page](https://xcard.com/api) <br>
- [XCard API base URL](https://api.xcard.com/v1) <br>
- [Account & Portfolio module](artifact/api-account.md) <br>
- [Market Data module](artifact/api-market.md) <br>
- [Order Execution module](artifact/api-orders.md) <br>
- [Trade History & Reports module](artifact/api-history.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API calls, Guidance] <br>
**Output Format:** [Markdown responses with API request guidance and JSON-shaped examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires XCARD_API_KEY; order placement requires explicit user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
