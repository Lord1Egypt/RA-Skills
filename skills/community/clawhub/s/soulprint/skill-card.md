## Description: <br>
Soulprint helps agents use decentralized identity verification, local ZK proof checks, validator nodes, and API or MCP middleware for human and bot reputation workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ManuelFelipeArias](https://clawhub.ai/user/ManuelFelipeArias) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use Soulprint to verify that a human is behind an AI bot, issue or verify identity proofs, run validator nodes, add identity checks to APIs or MCP servers, and check bot reputation scores. Full identity-document verification is described for Colombian cedula workflows. <br>

### Deployment Geography for Use: <br>
Colombia for full identity-document verification; global for blockchain, validator, and middleware integration where legally appropriate. <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles government ID values, birth dates, document images, face data, biometric-derived proofs, SPT tokens, validator credentials, and private keys. <br>
Mitigation: Treat those values as sensitive, avoid logging or sharing them, use low-value testnet keys for testing, and confirm what is stored on-chain or sent to validators before use. <br>
Risk: The release depends on external npm identity-verification tools and validator services. <br>
Mitigation: Review package provenance, pin versions where possible, scan dependencies, and run in an isolated environment before using it with real identity data. <br>
Risk: The security verdict flags unclear privacy and control boundaries for identity, biometric, blockchain, and validator workflows. <br>
Mitigation: Perform a privacy and security review, document consent and retention expectations, and verify local processing claims against the exact installed package version. <br>


## Reference(s): <br>
- [ClawHub Soulprint page](https://clawhub.ai/ManuelFelipeArias/soulprint) <br>
- [Soulprint documentation](https://soulprint.digital) <br>
- [soulprint-network npm package](https://www.npmjs.com/package/soulprint-network) <br>
- [Soulprint live validator](https://soulprint-node-production.up.railway.app) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown with command and code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference npm packages, validator endpoints, smart-contract addresses, and local identity-verification commands.] <br>

## Skill Version(s): <br>
1.0.25 (source: server release metadata; artifact describes Soulprint v0.6.4) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
