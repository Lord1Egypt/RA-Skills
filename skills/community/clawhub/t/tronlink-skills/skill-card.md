## Description: <br>
AI agent skills for TronLink wallet and the TRON ecosystem that provide wallet management, token queries, market data, DEX swap quotes, resource management, and TRX staking guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bbsyaya](https://clawhub.ai/user/bbsyaya) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users, developers, and agents use this skill set to query TRON wallets, tokens, market data, swap routes, network resources, and staking information through TronLink-oriented workflows. It is intended for read-only analysis and command guidance across the TRON ecosystem. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The wallet-labeled release installs a broader persistent TRON query suite than wallet balance and history lookup alone. <br>
Mitigation: Install only when the full TronLink TRON query suite is desired, and review the enabled skills and MCP registration scope before use. <br>
Risk: Remote installer commands from a moving branch can change after review. <br>
Mitigation: Review or pin the installer content before execution instead of curl-piping directly from the latest branch. <br>
Risk: Public wallet addresses, contract IDs, quote inputs, and optional API keys may be sent to TRON-related API services. <br>
Mitigation: Do not provide seed phrases or private keys; use only public addresses and project-scoped API credentials appropriate for TronGrid or related services. <br>


## Reference(s): <br>
- [TRON Resource Model](docs/resource-model.md) <br>
- [TRON Staking Guide](docs/staking-guide.md) <br>
- [Claude Integration Guide](docs/claude-integration-guide.md) <br>
- [TronGrid](https://trongrid.io) <br>
- [ClawHub Skill Listing](https://clawhub.ai/bbsyaya/tronlink-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON-style command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only TRON query workflows may use public wallet addresses, token contracts, quote inputs, and an optional TRONGRID_API_KEY.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
