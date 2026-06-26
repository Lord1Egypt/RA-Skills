## Description: <br>
Get UK (London Stock Exchange, LSE) market data via FinanceAgent on OneKey Gateway. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ai-hub-admin](https://clawhub.ai/user/ai-hub-admin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to query UK London Stock Exchange symbols through the OneKey Gateway and receive stock market data from the FinanceAgent endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries and selected stock symbols are sent to the external OneKey/DeepNLP gateway and its npm package dependency. <br>
Mitigation: Install only if the gateway and npm package are trusted, and send only symbols suitable for that external provider. <br>
Risk: The required OneKey Gateway API key could be exposed in logs, shell history, or shared chats. <br>
Mitigation: Use a revocable API key and avoid printing or pasting it into shared contexts. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ai-hub-admin/uk-stock-market-lse) <br>
- [DeepNLP OneKey Agent Router endpoint](https://agent.deepnlp.org/agent_router) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Configuration] <br>
**Output Format:** [JSON responses with CLI and HTTP usage examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a OneKey Gateway API key and a symbol_list array of LSE ticker strings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
