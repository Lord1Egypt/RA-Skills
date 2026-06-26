## Description: <br>
WachAI-x402 helps agents run paid WACH.AI DeFi token-risk analysis through x402 payments and AWAL wallet custody. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Akshat-Mishra101](https://clawhub.ai/user/Akshat-Mishra101) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to assess token safety, honeypot patterns, liquidity quality, holder concentration, and contract risk signals across Ethereum, Polygon, Base, BSC, and Solana. The skill guides the agent through AWAL readiness checks, capped x402 payment, risk analysis, and source-linked reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Paid DeFi analysis can spend wallet funds or be run against the wrong token or chain. <br>
Mitigation: Verify the external x402-wach CLI or npm package and publisher, use a low-balance AWAL wallet, keep the 0.01 USDC cap, and confirm the token and chain before each analysis. <br>
Risk: Wallet-secret handling mistakes could expose credentials or signing material. <br>
Mitigation: Do not provide private keys, seed phrases, or wallet files; this skill uses AWAL authentication and wallet custody instead. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Akshat-Mishra101/wachai-x402) <br>
- [WACH.AI x402 Verification Endpoint](https://x402.wach.ai/verify-token) <br>
- [TokenSense Report URL Pattern](https://tokensense.wach.ai/<chain>/<tokenAddress>) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands, TypeScript examples, and structured token-risk report sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Paid x402 analysis calls are capped at 10,000 atomic USDC by default; successful reports should include a TokenSense or source link when available.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
