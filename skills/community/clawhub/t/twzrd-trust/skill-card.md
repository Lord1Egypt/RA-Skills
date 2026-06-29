## Description: <br>
Checks Solana wallets and x402 sellers before payment, returning a ReadinessCard with an allow, warn, or block decision, trust score, and caveats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twzrd-sol](https://clawhub.ai/user/twzrd-sol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run pre-spend counterparty checks before signing or sending Solana x402 payments. It helps decide whether to proceed, warn the user, or abort based on TWZRD's wallet-risk and seller-readiness signals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet-risk scores and ReadinessCard decisions are advisory and may be incomplete or stale. <br>
Mitigation: Use TWZRD as a preflight signal, but confirm payment details and final transaction approval in the user's own signer. <br>
Risk: The optional MCP setup connects the agent to TWZRD's remote service. <br>
Mitigation: Enable the MCP server only when remote TWZRD access is intended, and prefer direct HTTP checks when a narrower integration is sufficient. <br>
Risk: The skill supports workflows that may lead to signed Solana/x402 payments. <br>
Mitigation: Run preflight before payment, abort on block decisions, and require explicit user confirmation before any wallet transaction is signed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/twzrd-sol/twzrd-trust) <br>
- [TWZRD Homepage](https://intel.twzrd.xyz) <br>
- [Machine-Readable Service Descriptor](https://intel.twzrd.xyz/.well-known/x402) <br>
- [OpenAPI 3.1 Specification](https://intel.twzrd.xyz/openapi.json) <br>
- [Agent Orientation](https://intel.twzrd.xyz/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash commands and HTTP endpoint guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe remote API responses such as ReadinessCard decisions, trust scores, caveats, and signed receipt verification guidance.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
