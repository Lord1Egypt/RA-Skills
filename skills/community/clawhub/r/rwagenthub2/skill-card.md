## Description: <br>
Call 32 real-world APIs for travel, weather, finance, web search, geocoding, IP reputation, blockchain data, code execution, and email, paying per call in USDC on Base via x402. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marcelo-rowship](https://clawhub.ai/user/marcelo-rowship) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to make paid AgentHub API calls from an agent workflow after configuring Node.js, the SDK, and a dedicated Base wallet. It is suited for retrieving real-world data, sending email, and running code through the listed gateway APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to a Base wallet private key for USDC micropayments. <br>
Mitigation: Use a dedicated wallet with only a small USDC balance and do not reuse a primary wallet key. <br>
Risk: Paid API calls may execute without clear spending or confirmation controls. <br>
Mitigation: Require explicit approval before each paid call and monitor wallet balance and transaction history. <br>
Risk: The skill can call email sending and code execution APIs. <br>
Mitigation: Review request parameters before execution, especially email recipients, message content, code, language, and timeout. <br>
Risk: The installed SDK dependency controls how calls and wallet signing are performed. <br>
Mitigation: Review or pin the rwagenthub-sdk dependency before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/marcelo-rowship/rwagenthub2) <br>
- [AgentHub gateway](https://agents-production-73c1.up.railway.app) <br>
- [rwagenthub-sdk package](https://www.npmjs.com/package/rwagenthub-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [API calls, JSON, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown guidance with bash and JavaScript snippets; API results are returned as JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js, npm, rwagenthub-sdk, MCP_WALLET_PRIVATE_KEY, and a funded Base wallet for paid calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
