## Description: <br>
Build internet-native payments with the x402 open protocol - HTTP 402 Payment Required for on-chain micropayments with no accounts or API keys. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tenequm](https://clawhub.ai/user/tenequm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to design, implement, and review x402 payment flows for paid APIs, paywalled content, AI agent payments, MCP tools, and usage-based billing across TypeScript, Python, and Go. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet and facilitator keys can control funds if copied into generated x402 client, server, or facilitator code. <br>
Mitigation: Keep keys server-side, avoid browser exposure, use dedicated low-balance wallets, and store production secrets in a secret manager or KMS/HSM. <br>
Risk: Payment-flow examples may be adapted to mainnet or paid services without enough review. <br>
Mitigation: Review generated code, network IDs, facilitator URLs, wallet addresses, and settlement behavior before using it with mainnet funds. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tenequm/x402-development) <br>
- [Publisher Profile](https://clawhub.ai/user/tenequm) <br>
- [Skill Homepage](https://github.com/tenequm/skills/tree/main/skills/x402) <br>
- [x402 Documentation](https://docs.x402.org) <br>
- [x402 Protocol Repository](https://github.com/x402-foundation/x402) <br>
- [Core Concepts](references/core-concepts.md) <br>
- [x402 Protocol Specification (v2)](references/protocol-spec.md) <br>
- [TypeScript SDK Reference](references/typescript-sdk.md) <br>
- [Python SDK Reference](references/python-sdk.md) <br>
- [Go SDK Reference](references/go-sdk.md) <br>
- [EVM Scheme Reference](references/evm-scheme.md) <br>
- [Solana (SVM) Exact Scheme Reference](references/svm-scheme.md) <br>
- [Transport Implementations](references/transports.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with code snippets and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include wallet, facilitator, network, and package configuration guidance; generated code should be reviewed before use with funds.] <br>

## Skill Version(s): <br>
0.9.0 (source: frontmatter and server release evidence, released 2026-06-09) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
