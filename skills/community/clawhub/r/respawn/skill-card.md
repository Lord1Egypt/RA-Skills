## Description: <br>
Anchors agent identity and memory pointers on the Autonomys Network so a new agent instance can recover from an address without relying on local state. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xautonomys](https://clawhub.ai/user/0xautonomys) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to create and manage Autonomys wallets, check balances, move or bridge AI3/tAI3, publish on-chain remarks, and anchor or retrieve memory CIDs for agent recovery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can let an agent manage a wallet and spend or bridge AI3/tAI3. <br>
Mitigation: Use a dedicated low-balance wallet, start on Chronos testnet, and require human review before transfers, bridges, withdrawals, or mainnet anchors. <br>
Risk: On-chain CIDs and remarks are permanent once published. <br>
Mitigation: Review data before anchoring or remark submission and avoid publishing secrets, private data, or unapproved records. <br>
Risk: Wallet mnemonics and passphrases can expose funds if handled unsafely. <br>
Mitigation: Back up recovery phrases securely, avoid command-line passphrases, and prefer a restricted passphrase file or interactive prompt. <br>
Risk: The server security verdict flags weak built-in guardrails for asset-moving and permanent publishing authority. <br>
Mitigation: Treat transaction-bearing commands as approval-gated operations and monitor balances so failed anchoring is surfaced immediately. <br>


## Reference(s): <br>
- [Auto Respawn on ClawHub](https://clawhub.ai/0xautonomys/respawn) <br>
- [auto-respawn CLI Reference](references/auto-respawn-commands.md) <br>
- [Autonomys Network](references/autonomys-network.md) <br>
- [MemoryChain contract source](https://github.com/autojeremy/openclaw-memory-chain) <br>
- [Autonomys SDK](https://github.com/autonomys/auto-sdk) <br>
- [Chronos testnet faucet](https://autonomysfaucet.xyz/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create encrypted local wallet files and submit blockchain transactions when the operator approves transaction-bearing actions.] <br>

## Skill Version(s): <br>
0.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
