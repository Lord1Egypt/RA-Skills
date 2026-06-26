## Description: <br>
DeFi intelligence powered by Silverback - 19 x402 endpoints on Base chain for market data, swap quotes, technical analysis, yield opportunities, token audits, whale tracking, and AI chat with pay-per-call USDC payments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RidingLiquid](https://clawhub.ai/user/RidingLiquid) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and DeFi agents use this skill to call Silverback x402 endpoints for Base-chain market intelligence, swap data, yield discovery, token audits, whale tracking, and AI-assisted DeFi questions. It is intended for agents that can make HTTP requests and handle x402 wallet payments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Using paid x402 endpoints can trigger USDC charges from the agent wallet. <br>
Mitigation: Use a limited-balance wallet and confirm each HTTP 402 payment amount before authorizing payment. <br>
Risk: Swap flows may return unsigned Permit2 data or other signing requests for client-side approval. <br>
Mitigation: Independently verify token addresses, amounts, spender permissions, and transaction details before signing. <br>
Risk: The optional MCP npm package is separate executable software installed globally. <br>
Mitigation: Review the package before global installation and only install it in environments where that executable trust boundary is acceptable. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/RidingLiquid/silverback-defi) <br>
- [Silverback DeFi Website](https://silverbackdefi.app) <br>
- [Silverback x402 Docs](https://silverbackdefi.app/x402) <br>
- [Silverback x402 API](https://x402.silverbackdefi.app) <br>
- [Silverback x402 MCP Package](https://www.npmjs.com/package/silverback-x402-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, API calls, configuration] <br>
**Output Format:** [Markdown with curl examples and endpoint descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and jq; paid endpoints use x402 USDC payments and may return unsigned Permit2 swap data for client-side signing.] <br>

## Skill Version(s): <br>
2.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
