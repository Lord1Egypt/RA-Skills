## Description: <br>
The Amazon Agent turns e-commerce data from Amazon into structured intelligence for pricing, catalog, and review analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teneoprotocoldev](https://clawhub.ai/user/teneoprotocoldev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, businesses, and e-commerce researchers use this agent through the Teneo SDK to retrieve Amazon product details, marketplace search results, and customer reviews for pricing intelligence, catalog audits, and sentiment analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet-based USDC payments may occur automatically without clearly documented spending limits or per-use confirmation controls. <br>
Mitigation: Use a limited-purpose wallet with minimal USDC, verify the Teneo SDK source, avoid main wallets or unrestricted private keys, and require clear cost and spending controls before allowing agents to run @amazon commands automatically. <br>


## Reference(s): <br>
- [Teneo Agent SDK on ClawHub](https://clawhub.ai/teneoprotocoldev/teneo-agent-sdk) <br>
- [Teneo Agent SDK NPM Package](https://www.npmjs.com/package/@teneo-protocol/sdk) <br>
- [Teneo Agent SDK GitHub Repository](https://github.com/TeneoProtocolAI/teneo-agent-sdk) <br>
- [Teneo Protocol](https://teneo-protocol.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, API Calls, Guidance] <br>
**Output Format:** [Markdown responses and structured response content returned through Teneo SDK messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports product, search, reviews, and help commands; paid queries require wallet-based USDC payments on supported networks.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
