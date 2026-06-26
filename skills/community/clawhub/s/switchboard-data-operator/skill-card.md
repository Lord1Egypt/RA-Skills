## Description: <br>
Autonomous operator for Switchboard on-demand feeds, Surge streaming, and randomness that designs jobs, simulates via Crossbar, and deploys, updates, and reads feeds across Solana/SVM, EVM, Sui, and other Switchboard-supported chains with user-controlled security, spend limits, and allow/deny lists. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oakencore](https://clawhub.ai/user/oakencore) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, protocol teams, feed creators, DeFi teams, and automation operators use this skill to plan, simulate, deploy, update, read, and integrate Switchboard oracle feeds, Surge streams, and randomness across supported blockchain networks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide blockchain transactions that write state, pay fees, or move funds. <br>
Mitigation: Use read_only or execute_with_approval by default, define strict per-transaction, daily, and total spend limits, and require explicit approval before mainnet signing. <br>
Risk: The skill may interact with chain programs, contracts, RPC endpoints, Crossbar URLs, or feeds that the user did not intend to authorize. <br>
Mitigation: Set allowlists or denylists for program IDs, contract addresses, RPC endpoints, Crossbar URLs, and data sources before execution. <br>
Risk: Secrets such as private keys, API keys, JWTs, or seed phrases could be exposed if handled carelessly. <br>
Mitigation: Use keystores or secret managers, reference secrets by placeholder names, avoid printing secret values, and avoid placing API keys in URLs when headers or managed secrets are available. <br>


## Reference(s): <br>
- [Switchboard Documentation](https://docs.switchboard.xyz/) <br>
- [Switchboard Docs by Chain](https://docs.switchboard.xyz/docs-by-chain) <br>
- [Crossbar](https://docs.switchboard.xyz/tooling/crossbar) <br>
- [Run Crossbar with Docker Compose](https://docs.switchboard.xyz/tooling/crossbar/run-crossbar-with-docker-compose) <br>
- [Switchboard CLI](https://docs.switchboard.xyz/tooling/cli) <br>
- [Switchboard SDKs](https://docs.switchboard.xyz/tooling/sdks) <br>
- [Deploy Feed](https://docs.switchboard.xyz/custom-feeds/build-and-deploy-feed/deploy-feed) <br>
- [Variable Overrides](https://docs.switchboard.xyz/custom-feeds/advanced-feed-configuration/data-feed-variable-overrides) <br>
- [Task Types Reference](https://explorer.switchboardlabs.xyz/task-docs) <br>
- [Feed Builder](https://explorer.switchboardlabs.xyz/feed-builder) <br>
- [Switchboard On-Demand Examples](https://github.com/switchboard-xyz/sb-on-demand-examples) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline code blocks, command examples, configuration guidance, and structured plans] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include OperatorPolicy, execution steps, rollback or recovery notes, and risks and mitigations when relevant.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
