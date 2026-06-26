## Description: <br>
Interact with The Sealer Protocol for onchain AI-agent attestations on Base, including difficulty previews, SMART commitments, commitment status checks, agent profiles, leaderboards, Sealer IDs, and EIP-712 signing payloads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iamdevving](https://clawhub.ai/user/iamdevving) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to interact with The Sealer Protocol for wallet-based onchain commitments, agent identity, attestation status, profile lookup, leaderboard lookup, and EVM signing-payload preparation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents through wallet-based onchain write operations that require x402 USDC payment. <br>
Mitigation: Before any write action, verify the thesealer.xyz domain, the Base network, the exact USDC amount, and the wallet prompt. <br>
Risk: Commitments, Sealer IDs, and attestations are treated as public and permanent protocol records. <br>
Mitigation: Preview difficulty and review commitment text, metrics, deadlines, and wallet identity before submitting an onchain transaction. <br>
Risk: EVM operations use EIP-712 signatures and wallet authentication. <br>
Mitigation: Never provide private keys or seed phrases, and only sign expected payloads for the intended action. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/iamdevving/sealer-attest) <br>
- [Publisher Profile](https://clawhub.ai/user/iamdevving) <br>
- [Skill Definition](artifact/SKILL.md) <br>
- [The Sealer Protocol](https://thesealer.xyz) <br>
- [API Reference](https://thesealer.xyz/api/infoproducts) <br>
- [Scoring Docs](https://thesealer.xyz/docs) <br>
- [Leaderboard](https://thesealer.xyz/leaderboard) <br>
- [MCP Server Reference](https://github.com/iamdevving/the-sealer/tree/main/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Text, Configuration] <br>
**Output Format:** [Markdown guidance with HTTP endpoint descriptions, request parameters, and JSON-style API response summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Write operations require wallet signing and x402 USDC payment on Base; read and preview operations are described as free.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
