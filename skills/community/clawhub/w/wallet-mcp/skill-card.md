## Description:

wallet-mcp lets MCP-compatible agents generate, store, inspect, import, export, fund, sweep, and manage Solana and EVM wallets with JSON tool responses.

This skill is for research and development only.

## Publisher:

[genoshide](https://clawhub.ai/user/genoshide)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to let an agent manage labeled groups of Solana and EVM wallets, including wallet generation, balance checks, token scans, batch transfers, sweeps, imports, and exports. The artifact states the tool is for educational and research purposes and does not provide financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: This skill gives agents broad authority over private keys and fund-moving wallet operations.

Mitigation: Install it only when agent-managed wallets are intended, use dedicated low-value wallets, and review transfer or sweep actions before execution.

Risk: Wallet private keys may be stored persistently on disk.

Mitigation: Keep WALLET_DATA_DIR on encrypted storage with strict file permissions and avoid committing or sharing wallet data files.

Risk: Exposed network transport can make wallet-management capability reachable beyond the intended client.

Mitigation: Do not expose HTTP transport publicly; place any remote access behind strong authentication such as mTLS or a protected reverse proxy.

Risk: Automatic persistent setup can add wallet-management instructions to an agent's retained tool context.

Mitigation: Review generated TOOLS.md entries manually before relying on persistent setup, especially on shared hosts or production agents.

Risk: Installing or updating from wrapper source without review can introduce unintended wallet behavior.

Mitigation: Pin and verify the source used for installation and inspect changes before upgrading active wallet-management environments.

## Reference(s):

- [ClawHub wallet-mcp listing](https://clawhub.ai/genoshide/skills/wallet-mcp)
- [README](artifact/README.md)
- [Security Policy](artifact/SECURITY.md)
- [Installation Guide](artifact/INSTALLATION.md)
- [Examples](artifact/EXAMPLES.md)
- [Changelog](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON tool responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [All wallet.py commands are documented as synchronous and return JSON immediately.]

## Skill Version(s):

1.5.0 (source: server release metadata, changelog, pyproject.toml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
