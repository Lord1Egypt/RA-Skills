## Description: <br>
ZKE Exchange Trading Skill provides agent tools for spot and futures trading, wallet operations, asset transfers, withdrawals, and real-time market data on ZKE Exchange. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ZKE-Exchange](https://clawhub.ai/user/ZKE-Exchange) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers with a ZKE account use this skill to query market and account data, manage spot and futures orders, transfer funds between account types, and request withdrawals through an agent interface. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control a live ZKE account, including trading, transfers, withdrawals, leverage changes, order cancellation, and cancel-all actions. <br>
Mitigation: Install only for intentional live account control; use API keys with withdrawals disabled, IP allowlisting, and the narrowest trade permissions possible, and require manual confirmation outside the agent before high-impact actions. <br>
Risk: Local logs may contain sensitive account activity, order details, amounts, and withdrawal addresses. <br>
Mitigation: Treat ~/.zke-trading/openclaw-plugin.log as sensitive, restrict local access, avoid sharing it, and remove or rotate it according to the user's security policy. <br>
Risk: Large balances can be exposed to agent-controlled keys if broad account permissions are used. <br>
Mitigation: Avoid storing large balances under API keys available to the plugin and separate operational funds from longer-term holdings. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ZKE-Exchange/zke-trading) <br>
- [ZKE-Exchange publisher profile](https://clawhub.ai/user/ZKE-Exchange) <br>
- [ZKE skill guide](https://support.zke.com/skills/) <br>
- [ZKE Exchange](https://zke.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Tool responses as JSON or text, with setup guidance and shell commands in Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ZKE_API_KEY and ZKE_SECRET_KEY environment variables for authenticated account actions.] <br>

## Skill Version(s): <br>
1.0.13 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
