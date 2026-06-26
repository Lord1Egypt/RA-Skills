## Description: <br>
Rustok Wallet lets an agent use a local self-custody Ethereum wallet over stdio MCP to read wallet context, preview transactions, execute sends, and sign messages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[temrjan](https://clawhub.ai/user/temrjan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to connect an AI agent to a local Ethereum wallet for balance checks, DeFi position review, transaction preview, transaction execution, and message signing. It is intended for users who accept self-custody responsibility for live funds. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The wallet can operate on live Ethereum networks and has no hard-coded spending limits. <br>
Mitigation: Preview each transaction, show amount, destination, estimated cost, and risk level before execution, and require explicit user approval before moving funds. <br>
Risk: Private keys and the recovery phrase are local self-custody secrets. <br>
Mitigation: Keep the recovery phrase offline, protect the keyring password, and use the default stdio setup rather than exposing the gateway over a network. <br>
Risk: The wallet depends on Docker, a created wallet volume, and RPC connectivity. <br>
Mitigation: Complete onboarding, configure the required environment variables, and run the included health check before relying on the wallet. <br>


## Reference(s): <br>
- [ClawHub Rustok Wallet](https://clawhub.ai/temrjan/rustok-wallet) <br>
- [Rustok MCP Homepage](https://github.com/rustok-org/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON MCP configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Docker, an initialized local wallet volume, a keyring password, and an Ethereum RPC URL.] <br>

## Skill Version(s): <br>
0.3.2 (source: frontmatter, claw.json, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
