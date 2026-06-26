## Description: <br>
Generate, manage, and operate Solana and EVM wallets through an MCP-compatible agent interface with JSON outputs for wallet creation, balances, transfers, sweeps, imports, exports, and token scans. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[genoshide](https://clawhub.ai/user/genoshide) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agent users use this skill to automate Solana and EVM wallet administration, including wallet generation, group management, balance checks, batch sends, sweeps, token account scans, imports, and exports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can store private keys and move or sweep crypto funds without built-in confirmation safeguards. <br>
Mitigation: Use dedicated low-balance wallets and manually verify every send, sweep, account closure, key export, import, and group deletion before allowing execution. <br>
Risk: Wallet data may contain plaintext private keys in ~/.wallet-mcp/wallets.csv. <br>
Mitigation: Protect the wallet data directory with restrictive file permissions, disk encryption, and a storage location that is not exposed through shares, APIs, or source control. <br>
Risk: Private keys may be exposed through chat, shell arguments, or exported backup files. <br>
Mitigation: Prefer stored wallet labels over raw key arguments, avoid pasting private keys into chat or shell commands, and encrypt any backup that includes keys. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/genoshide/wallet-mcp) <br>
- [README](artifact/README.md) <br>
- [Installation Guide](artifact/INSTALLATION.md) <br>
- [Examples](artifact/EXAMPLES.md) <br>
- [Security Policy](artifact/SECURITY.md) <br>
- [OpenClaw Skill](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON command outputs and shell or configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Wallet operations return JSON; private-key display is masked by default in listing output.] <br>

## Skill Version(s): <br>
1.5.0 (source: server release evidence, pyproject.toml, README badge, changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
