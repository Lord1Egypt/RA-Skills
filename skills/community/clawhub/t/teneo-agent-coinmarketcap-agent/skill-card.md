## Description: <br>
The CoinMarketCap Agent provides access to real-time and historical cryptocurrency market data through CoinMarketCap's official API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teneoprotocoldev](https://clawhub.ai/user/teneoprotocoldev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve cryptocurrency prices, quotes, rankings, trends, gainers and losers, and performance metrics through the Teneo Protocol integration. It is suited for trading research, portfolio monitoring, market analysis, and cryptocurrency performance comparison. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet authentication and automatic USDC payments may expose users to unintended spending or transaction approval risk. <br>
Mitigation: Review the Teneo SDK and payment terms, use a wallet with limited funds, avoid sharing private keys, and confirm spending limits and revocation steps before use. <br>
Risk: The artifact does not describe payment costs or controls in enough detail for low-risk installation decisions. <br>
Mitigation: Confirm payment network, asset, approval amount, recurring charges, and stop or revoke procedures before connecting a funded wallet. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/teneoprotocoldev/teneo-agent-coinmarketcap-agent) <br>
- [Teneo Protocol](https://teneo-protocol.ai) <br>
- [Teneo Agent SDK on ClawHub](https://clawhub.ai/teneoprotocoldev/teneo-agent-sdk) <br>
- [Teneo SDK NPM Package](https://www.npmjs.com/package/@teneo-protocol/sdk) <br>
- [Teneo SDK GitHub Repository](https://github.com/TeneoProtocolAI/teneo-agent-sdk) <br>
- [CoinMarketCap API v1 Documentation](https://coinmarketcap.com/api/documentation/v1/#section/Introduction) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with TypeScript and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs guide agents through SDK setup and access to cryptocurrency market data; usage may require wallet authentication and USDC payment configuration.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
