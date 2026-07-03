## Description: <br>
Quantum-resistant payments and private AI inference for autonomous agents, including ML-DSA-65 payment signing, PQC payment verification, Ghost AI DeFi intent parsing, and ML-KEM-768 payload encryption. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[veil-protocol-1](https://clawhub.ai/user/veil-protocol-1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agents use this skill to sign and verify post-quantum payment headers, encrypt sensitive payloads, and parse private DeFi intents through an MCP server. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles high-impact wallet and DeFi data and the security review warns against pasting seed phrases, private keys, or unrecoverable secrets without independent runtime verification. <br>
Mitigation: Install only if the npm package and Veil service are trusted, and avoid entering seed phrases, private keys, or unrecoverable secrets unless runtime behavior, logging, and privacy handling have been independently verified. <br>
Risk: Ghost AI privacy claims may not apply when the documented local fallback mode is used, because the fallback parses intents without FHE. <br>
Mitigation: Treat fallback results as local parsing rather than FHE-protected private inference, and do not rely on fallback mode for confidential DeFi instructions. <br>
Risk: The artifact states that contracts are on Base Sepolia testnet only and mainnet deployment is pending a formal security audit. <br>
Mitigation: Use production networks only after confirming audited mainnet deployment status and reviewing the relevant contract and payment-flow security documentation. <br>


## Reference(s): <br>
- [Veil Protocol homepage](https://veilprotocol.net) <br>
- [ClawHub skill page](https://clawhub.ai/veil-protocol-1/veil-protocol) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [JSON tool-call results and Markdown guidance with inline shell and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Tool results may include payment signatures, payment headers, verification details, encrypted payloads, key encapsulation ciphertexts, and DeFi execution plans.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
