## Description: <br>
The Messari BTC & ETH Tracker helps agents retrieve Bitcoin and Ethereum market analytics through the Teneo Protocol network. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teneoprotocoldev](https://clawhub.ai/user/teneoprotocoldev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents, developers, traders, analysts, and researchers use this skill to connect to a Teneo-hosted Messari tracker and request BTC and ETH market data for portfolio review, financial modeling, or automated analytics workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to connect a funded wallet for automatic USDC payments without enough payment-scope detail. <br>
Mitigation: Use only a low-balance wallet, verify the Teneo SDK and backend independently, and manually review every transaction amount and recipient before signing. <br>
Risk: The security verdict is suspicious for this release. <br>
Mitigation: Review the skill carefully before installation and treat the payment flow as requiring additional human approval. <br>


## Reference(s): <br>
- [Messari BTC & ETH Tracker on ClawHub](https://clawhub.ai/teneoprotocoldev/teneo-agent-messari-btc-eth-tracker) <br>
- [Teneo Protocol](https://teneo-protocol.ai) <br>
- [Teneo Agent SDK on ClawHub](https://clawhub.ai/teneoprotocoldev/teneo-agent-sdk) <br>
- [@teneo-protocol/sdk on npm](https://www.npmjs.com/package/@teneo-protocol/sdk) <br>
- [Teneo Agent SDK GitHub Repository](https://github.com/TeneoProtocolAI/teneo-agent-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with bash and TypeScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes WebSocket connection details, payment network configuration, and supported USDC contract addresses.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
