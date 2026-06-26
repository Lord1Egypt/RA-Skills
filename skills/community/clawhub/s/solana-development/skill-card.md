## Description: <br>
Build, test, deploy, and audit Solana programs with Anchor or native Rust, and build with ZK Compression (Light Protocol). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tenequm](https://clawhub.ai/user/tenequm) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers and engineers use this skill to build Solana smart contracts, client integrations, token operations, tests, deployments, security reviews, and ZK Compression workflows. It provides reference guidance for Anchor, native Rust, Light Protocol, wallets, clusters, and production-readiness checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Blockchain commands can sign transactions, deploy or upgrade programs, move tokens, or incur costs if run against the wrong cluster or wallet. <br>
Mitigation: Check the cluster, wallet, keypair path, and transaction effects before execution, and prefer localnet or devnet before mainnet. <br>
Risk: Wallet private keys, keypair files, RPC API keys, and other sensitive credentials may be exposed during development or deployment. <br>
Mitigation: Protect private keys and API keys, avoid pasting secrets into prompts or logs, and use least-privilege credentials where possible. <br>
Risk: Security examples and audit guidance can miss project-specific vulnerabilities or production constraints. <br>
Mitigation: Independently review security examples and obtain appropriate production review before relying on them for deployed programs. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/tenequm/solana-development) <br>
- [Skill instructions](SKILL.md) <br>
- [Anchor Framework Reference](references/anchor.md) <br>
- [Native Rust Reference](references/native-rust.md) <br>
- [Security Fundamentals](references/security-fundamentals.md) <br>
- [Security Checklists](references/security-checklists.md) <br>
- [Production Deployment](references/production-deployment.md) <br>
- [ZK Compression Docs](https://www.zkcompression.com/) <br>
- [Light Protocol](https://github.com/Lightprotocol/light-protocol) <br>
- [Solana Documentation](https://solana.com/docs) <br>
- [Anchor Documentation](https://www.anchor-lang.com/docs) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline code and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include blockchain commands that require wallet, cluster, keypair, and transaction review before execution.] <br>

## Skill Version(s): <br>
0.7.0 (source: SKILL.md metadata and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
