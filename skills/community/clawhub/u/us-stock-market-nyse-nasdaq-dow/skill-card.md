## Description: <br>
Get US stock market data (NYSE, NASDAQ, and major indices) via FinanceAgent on OneKey Gateway. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ai-hub-admin](https://clawhub.ai/user/ai-hub-admin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve US stock market data for NYSE, NASDAQ, DOW, and standard ticker symbols through the OneKey Gateway FinanceAgent API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on an external OneKey Gateway package and DeepNLP agent router. <br>
Mitigation: Install only from trusted package sources and verify the gateway and router are acceptable for the deployment environment. <br>
Risk: The skill requires an API key and examples include verbose command-line invocation. <br>
Mitigation: Use a dedicated or revocable API key and avoid exposing verbose curl output in shared terminals, logs, or CI systems. <br>
Risk: Ticker symbols are sent to an external service. <br>
Mitigation: Submit only symbol lists that are appropriate to disclose to the external service. <br>


## Reference(s): <br>
- [US Stock Market NYSE NASDAQ DOW ClawHub page](https://clawhub.ai/ai-hub-admin/us-stock-market-nyse-nasdaq-dow) <br>
- [DeepNLP OneKey Agent Router endpoint](https://agent.deepnlp.org/agent_router) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON stock-market quote responses with Markdown usage guidance and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DEEPNLP_ONEKEY_ROUTER_ACCESS and a symbol_list array of US ticker strings] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
