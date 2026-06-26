## Description: <br>
Perform EVM Web3 on-chain operations such as checking addresses, scanning portfolios, transferring assets, swapping or bridging tokens, minting NFTs, tracking PnL, monitoring prices, generating trading signals, auditing contracts, tracking whale activity, and creating wallets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[perasyudha](https://clawhub.ai/user/perasyudha) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Web3 operators and developers use this skill to let an agent prepare and run EVM wallet workflows, including balance checks, portfolio scans, transfers, swaps, bridges, NFT mints, contract audits, monitoring, and trading signal summaries. The skill is appropriate only for users who intend to operate a local hot-wallet automation tool with human transaction review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent direct wallet-signing power for EVM transactions. <br>
Mitigation: Use only a dedicated low-value hot wallet, never a primary wallet or seed phrase, and review every transaction outside the agent before broadcast. <br>
Risk: .env contents and command output or logs can expose wallet-control material. <br>
Mitigation: Restrict access to the local environment file, avoid sharing logs or outputs that include wallet secrets, and run the skill in a local isolated environment. <br>
Risk: Untrusted prompts or exposed MCP tools could lead to unsafe transaction proposals. <br>
Mitigation: Avoid exposing the skill to untrusted prompts, require explicit human approval, and use simulation before sending value-bearing transactions. <br>


## Reference(s): <br>
- [ClawHub Web3 Ops Release Page](https://clawhub.ai/perasyudha/web3-ops) <br>
- [README](README.md) <br>
- [Security Policy](SECURITY.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI command examples and JSON-readable command output when --json is used] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce transaction hashes, explorer URLs, balances, security findings, trading signals, alerts, and wallet configuration guidance.] <br>

## Skill Version(s): <br>
1.1.4 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
