## Description: <br>
Register agents on the Zeru ERC-8004 Identity Registry, manage wallets and metadata, and read on-chain state. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[elitex45](https://clawhub.ai/user/elitex45) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to register AI agents on Zeru's ERC-8004 Identity Registry, inspect registry state, check registration fees, and manage agent metadata or wallet settings on Base Mainnet or Base Sepolia. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use PRIVATE_KEY with a funded wallet to make irreversible on-chain registry changes. <br>
Mitigation: Use a dedicated low-balance or testnet wallet, never a primary wallet key, and review every write command before execution. <br>
Risk: Write commands do not include confirmation or dry-run safeguards in the provided artifact. <br>
Mitigation: Prefer manual execution for register, set-metadata, and unset-wallet operations until confirmation or dry-run safeguards are added. <br>
Risk: Fetched agent metadata and hosted agent URI contents are untrusted remote content. <br>
Mitigation: Inspect fetched metadata before reuse and avoid feeding it into sensitive workflows without review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/elitex45/zscore) <br>
- [ERC-8004 registration-v1 schema](https://eips.ethereum.org/EIPS/eip-8004#registration-v1) <br>
- [OASF reference](https://github.com/agntcy/oasf/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Text] <br>
**Output Format:** [Markdown guidance with inline shell commands; command execution returns CLI text, transaction hashes, and JSON-derived agent metadata.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Write operations require PRIVATE_KEY and a funded wallet; read-only commands can run without a private key.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
