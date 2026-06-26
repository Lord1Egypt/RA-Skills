## Description: <br>
股票交易下单和查询功能，需要提供股票代码、价格、数量等信息，支持买入、卖出、持仓查询、账户查询、撤单等操作。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yangheng3](https://clawhub.ai/user/yangheng3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can use this skill to have an agent prepare local HTTP API calls for stock buy, sell, cancellation, position, account, and order-status operations. It is intended for use only with a configured local stock trading assistant. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can cause high-impact trading and account actions through a local API. <br>
Mitigation: Require manual confirmation for every buy, sell, or cancellation request and prefer paper trading before live use. <br>
Risk: The artifact documents a default API key for the trading assistant. <br>
Mitigation: Change the default API key before use and use only with a verified trading assistant. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yangheng3/stock-auto-trade) <br>
- [Publisher profile](https://clawhub.ai/user/yangheng3) <br>
- [Stock trading assistant website](https://www.gp998.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Guidance] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and a local trading assistant API on localhost.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
